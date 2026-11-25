// apps/obs-management/tests/e2e_edge_check.cjs
// Verificación E2E determinista con Microsoft Edge Headless CDP (1440x900 y 390x844, ES y EN).
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawn } = require('child_process');
const net = require('net');

const REPO_ROOT = path.resolve(__dirname, '..', '..', '..');
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
        httpErrors.push({ url: req.url, status: 404 });
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
    this.externalRequests = [];
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
      } else if (msg.method === 'Network.requestWillBeSent') {
        const u = msg.params.request?.url || '';
        if (/^https?:\/\//.test(u) && !u.startsWith('http://127.0.0.1:') && !u.startsWith('http://localhost:')) {
          this.externalRequests.push(u);
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
  close() { this.ws.close(); }
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
  const httpErrors = [];
  const { server, port } = await startStaticServer(httpErrors);
  const debugPort = await getFreePort();
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'obs-edge-'));

  const edge = spawn(findEdge(), [
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    `--remote-debugging-port=${debugPort}`,
    `--user-data-dir=${userDataDir}`,
    'about:blank',
  ], { stdio: 'ignore' });

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
      { name: 'desktop-es', w: 1440, h: 900, lang: 'es', maxHeader: 64 },
      { name: 'desktop-en', w: 1440, h: 900, lang: 'en', maxHeader: 64 },
      { name: 'mobile-es', w: 390, h: 844, lang: 'es', maxHeader: 56 },
      { name: 'mobile-en', w: 390, h: 844, lang: 'en', maxHeader: 56 },
    ];

    for (const tc of matrix) {
      await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: tc.w,
        height: tc.h,
        deviceScaleFactor: 1,
        mobile: tc.w <= 768,
      });

      const targetUrl = `http://127.0.0.1:${port}/apps/obs-management/?lang=${tc.lang}&scenario=drone-capacitor`;
      await cdp.send('Page.navigate', { url: targetUrl });
      await sleep(700);

      const snap = await cdp.evalJs(`(() => {
        const headerH = Math.round(document.querySelector('.app-header').getBoundingClientRect().height);
        const overflow = document.documentElement.scrollWidth - document.documentElement.clientWidth;
        const rows = document.querySelectorAll('#skuTableBody tr').length;
        const kpiRisk = document.getElementById('kpiTotalRisk').textContent;
        const backHref = document.getElementById('linkBackCatalog').getAttribute('href');
        const seriesHref = document.getElementById('linkSeries').getAttribute('href');
        const langAttr = document.documentElement.lang;
        // Switch to simulator & inject EOL
        document.querySelector('.tab-btn[data-view="simulator"]').click();
        const svgNodes = document.querySelectorAll('#bomGraphWrap svg .bom-node').length;
        // Switch to LTB calculator
        document.querySelector('.tab-btn[data-view="ltb"]').click();
        const verdict = document.getElementById('ltbVerdictTitle').textContent;
        // Open CSV dialog & load 1-click sample
        document.getElementById('btnOpenCsv').click();
        const dlgOpen = document.getElementById('csvDialog').open;
        document.getElementById('btnCsvSample').click();
        const csvMsg = document.getElementById('csvFeedback').textContent;
        document.getElementById('csvDialog').close();
        // Return to cockpit and verify overflow after interactions
        document.querySelector('.tab-btn[data-view="cockpit"]').click();
        const overflowAfter = document.documentElement.scrollWidth - document.documentElement.clientWidth;
        return { headerH, overflow, overflowAfter, rows, kpiRisk, backHref, seriesHref, langAttr, svgNodes, verdict, dlgOpen, csvMsg };
      })()`);

      if (snap.headerH > tc.maxHeader) throw new Error(`${tc.name}: header height ${snap.headerH}px > ${tc.maxHeader}px`);
      if (snap.overflow > 0 || snap.overflowAfter > 0) throw new Error(`${tc.name}: horizontal overflow ${snap.overflow}/${snap.overflowAfter}px`);
      if (snap.rows < 2) throw new Error(`${tc.name}: expected >=2 table rows, got ${snap.rows}`);
      if (snap.langAttr !== tc.lang) throw new Error(`${tc.name}: lang=${snap.langAttr}`);
      if (tc.lang === 'en' && (snap.backHref.startsWith('/es/') || snap.seriesHref.startsWith('/es/'))) {
        throw new Error(`${tc.name}: EN link points to /es/`);
      }
      if (snap.svgNodes < 4) throw new Error(`${tc.name}: expected >=4 SVG BOM nodes, got ${snap.svgNodes}`);
      if (!snap.verdict || snap.verdict === '—') throw new Error(`${tc.name}: empty LTB verdict`);
      if (!snap.dlgOpen || !snap.csvMsg) throw new Error(`${tc.name}: CSV dialog/sample failed`);

      results.push({ case: tc.name, ...snap });
    }

    if (httpErrors.length) throw new Error(`HTTP >=400 errors: ${JSON.stringify(httpErrors)}`);
    if (cdp.consoleErrors.length) throw new Error(`Console errors: ${JSON.stringify(cdp.consoleErrors)}`);
    if (cdp.exceptions.length) throw new Error(`JS exceptions: ${JSON.stringify(cdp.exceptions)}`);
    if (cdp.externalRequests.length) throw new Error(`External CDN requests: ${JSON.stringify(cdp.externalRequests)}`);

    console.log(JSON.stringify({ status: 'E2E_PASS', cases: results }, null, 2));
  } finally {
    if (cdp) cdp.close();
    edge.kill();
    server.close();
    try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch { /* ignore */ }
  }
}

runAudit().catch((err) => {
  console.error('E2E_FAIL:', err.message);
  process.exit(1);
});
