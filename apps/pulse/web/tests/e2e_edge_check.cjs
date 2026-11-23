// apps/pulse/web/tests/e2e_edge_check.cjs
// Verificación E2E determinista con Microsoft Edge Headless CDP (1440x900 y 390x844, ES y EN) — Hito 7.14.
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawn } = require('child_process');
const net = require('net');

const REPO_ROOT = path.resolve(__dirname, '..', '..', '..', '..');
const STATIC_ROOT = path.join(REPO_ROOT, 'static');
const EDGE_PATHS = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
];

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
};

function findEdge() {
  for (const p of EDGE_PATHS) if (fs.existsSync(p)) return p;
  throw new Error('Microsoft Edge binary not found.');
}

function getFreePort() {
  return new Promise((resolve, reject) => {
    const s = net.createServer();
    s.unref();
    s.on('error', reject);
    s.listen(0, '127.0.0.1', () => {
      const { port } = s.address();
      s.close(() => resolve(port));
    });
  });
}

function startStaticServer(httpErrors) {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const urlPath = (req.url || '/').split('?')[0];
      let rel = decodeURIComponent(urlPath).replace(/^\/+/, '');
      if (!rel || urlPath.endsWith('/')) rel = path.join(rel, 'index.html');
      let full = path.join(STATIC_ROOT, rel);
      if (fs.existsSync(full) && fs.statSync(full).isDirectory()) full = path.join(full, 'index.html');
      if (!full.startsWith(STATIC_ROOT) || !fs.existsSync(full)) {
        if (!urlPath.includes('favicon.ico')) {
          httpErrors.push({ url: req.url, status: 404 });
        }
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(full)] || 'application/octet-stream' });
      fs.createReadStream(full).pipe(res);
    });
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => resolve({ server, port: server.address().port }));
  });
}

class Cdp {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.id = 0;
    this.pending = new Map();
    this.consoleErrors = [];
    this.exceptions = [];
    this.httpFailures = [];
    this.ready = new Promise((res, rej) => {
      this.ws.addEventListener('open', res);
      this.ws.addEventListener('error', rej);
    });
    this.ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { res, rej } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) rej(new Error(msg.error.message));
        else res(msg.result);
      } else if (msg.method === 'Runtime.exceptionThrown') {
        this.exceptions.push(msg.params.exceptionDetails?.text || 'RuntimeException');
      } else if (msg.method === 'Runtime.consoleAPICalled' && msg.params.type === 'error') {
        this.consoleErrors.push(msg.params.args.map((a) => a.value || a.description).join(' '));
      } else if (msg.method === 'Network.responseReceived') {
        const resp = msg.params.response || {};
        if (resp.url && resp.url.startsWith('http://127.0.0.1:') && resp.status >= 400 && !resp.url.includes('favicon.ico')) {
          this.httpFailures.push({ url: resp.url, status: resp.status });
        }
      }
    });
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => {
      this.pending.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
  async evalJs(expression) {
    const r = await this.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.text || 'EvalError');
    return r.result?.value;
  }
  close() {
    this.ws.close();
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitForWsUrl(debugPort) {
  for (let i = 0; i < 40; i++) {
    try {
      const resp = await fetch(`http://127.0.0.1:${debugPort}/json`);
      const targets = await resp.json();
      const page = targets.find((t) => t.type === 'page' && t.webSocketDebuggerUrl);
      if (page) return page.webSocketDebuggerUrl;
    } catch { /* retry */ }
    await sleep(200);
  }
  throw new Error('Timed out waiting for Edge CDP target.');
}

async function runAudit() {
  const serverHttpErrors = [];
  const { server, port } = await startStaticServer(serverHttpErrors);
  const debugPort = await getFreePort();
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pulse-edge-'));

  const edge = spawn(
    findEdge(),
    [
      '--headless=new',
      '--disable-gpu',
      '--no-first-run',
      '--no-default-browser-check',
      `--remote-debugging-port=${debugPort}`,
      `--user-data-dir=${userDataDir}`,
      'about:blank',
    ],
    { stdio: 'ignore' }
  );

  const results = [];
  let cdp;
  try {
    const wsUrl = await waitForWsUrl(debugPort);
    cdp = new Cdp(wsUrl);
    await cdp.ready;
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('Network.enable');

    const matrix = [
      { name: 'desktop-es', w: 1440, h: 900, lang: 'es' },
      { name: 'desktop-en', w: 1440, h: 900, lang: 'en' },
      { name: 'mobile-es', w: 390, h: 844, lang: 'es' },
      { name: 'mobile-en', w: 390, h: 844, lang: 'en' },
    ];

    for (const tc of matrix) {
      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: tc.w,
        height: tc.h,
        deviceScaleFactor: 1,
        mobile: tc.w < 600,
      });

      await cdp.send('Page.navigate', { url: 'about:blank' });
      await sleep(100);
      const targetUrl = `http://127.0.0.1:${port}/apps/pulse/?tab=channels&lang=${tc.lang}`;
      await cdp.send('Page.navigate', { url: targetUrl });

      // Esperar a que React hidrate el panel de Canales & Audiencia
      let hydrated = false;
      for (let i = 0; i < 30; i++) {
        await sleep(250);
        const ready = await cdp.evalJs(`Boolean(document.querySelector('.channels-wrapper') && document.querySelector('.channel-matrix-table'))`);
        if (ready) {
          hydrated = true;
          break;
        }
      }
      if (!hydrated) {
        throw new Error(`[${tc.name}] Panel Canales & Audiencia no hidrató a tiempo.`);
      }

      // Verificar métricas DOM, Sandbox educativo, badge X stand-by y cero overflow
      const domReport = await cdp.evalJs(`(() => {
        const docEl = document.documentElement;
        const body = document.body;
        const tabBtn = document.querySelector('#tab-channels');
        const rows = document.querySelectorAll('.channel-matrix-table tbody tr').length;
        const funnelCards = document.querySelectorAll('.channel-funnel-card').length;
        const sandboxBadge = document.querySelector('.channels-mode-pill')?.textContent || '';
        const xBadge = document.querySelector('.x-standby-pill')?.textContent || '';
        const roiCards = document.querySelectorAll('.roi-v2-card').length;
        const recCards = document.querySelectorAll('.rec-card').length;
        const cw = docEl.clientWidth;
        const offenders = Array.from(document.querySelectorAll('*'))
          .filter((el) => el.getBoundingClientRect().right > cw + 1)
          .slice(0, 8)
          .map((el) => el.tagName + '.' + (el.className || '') + ' (right=' + Math.round(el.getBoundingClientRect().right) + ')');
        return {
          scrollWidth: docEl.scrollWidth,
          clientWidth: cw,
          bodyScrollWidth: body.scrollWidth,
          offenders,
          tabSelected: tabBtn?.getAttribute('aria-selected'),
          rows,
          funnelCards,
          sandboxBadge,
          xBadge,
          roiCards,
          recCards,
        };
      })()`);

      if (domReport.scrollWidth > domReport.clientWidth) {
        throw new Error(`[${tc.name}] Horizontal overflow detected: scrollWidth=${domReport.scrollWidth} > clientWidth=${domReport.clientWidth} offenders=${JSON.stringify(domReport.offenders)}`);
      }
      if (domReport.tabSelected !== 'true') {
        throw new Error(`[${tc.name}] #tab-channels aria-selected expected 'true', got ${domReport.tabSelected}`);
      }
      if (domReport.funnelCards !== 4 || domReport.rows < 4 || domReport.roiCards < 2 || domReport.recCards < 2) {
        throw new Error(`[${tc.name}] Incomplete Channels panel DOM: ${JSON.stringify(domReport)}`);
      }
      if (!domReport.sandboxBadge.includes('SANDBOX')) {
        throw new Error(`[${tc.name}] Missing public Sandbox label: ${domReport.sandboxBadge}`);
      }
      if (!domReport.xBadge.toLowerCase().includes('stand-by')) {
        throw new Error(`[${tc.name}] Missing X stand-by label: ${domReport.xBadge}`);
      }

      // Interacción: filtrar idioma EN en la matriz
      await cdp.evalJs(`(() => {
        const enBtn = Array.from(document.querySelectorAll('.lang-pill-group button')).find((b) => b.textContent?.trim() === 'EN');
        if (enBtn) enBtn.click();
      })()`);
      await sleep(150);

      results.push({ name: tc.name, ...domReport });
    }

    if (cdp.consoleErrors.length > 0 || cdp.exceptions.length > 0 || cdp.httpFailures.length > 0 || serverHttpErrors.length > 0) {
      throw new Error(
        `Runtime errors detected: console=${JSON.stringify(cdp.consoleErrors)} exceptions=${JSON.stringify(cdp.exceptions)} http=${JSON.stringify(cdp.httpFailures)} server404=${JSON.stringify(serverHttpErrors)}`
      );
    }

    console.log('E2E_PULSE_CHANNELS_PASS ✅', JSON.stringify(results));
  } finally {
    try { cdp?.close(); } catch { /* ignore */ }
    try { edge.kill('SIGKILL'); } catch { /* ignore */ }
    server.close();
    try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch { /* ignore */ }
  }
}

runAudit().catch((err) => {
  console.error('E2E_PULSE_CHANNELS_FAIL ❌', err);
  process.exit(1);
});
