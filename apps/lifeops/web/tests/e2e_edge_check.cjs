// apps/lifeops/web/tests/e2e_edge_check.cjs
// Verificación E2E determinista con Microsoft Edge Headless CDP (390x844 y 1440x900).
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

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
};

function findEdgeBinary() {
  for (const p of EDGE_PATHS) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error('Microsoft Edge binary not found on host.');
}

function getFreePort() {
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.unref();
    srv.on('error', reject);
    srv.listen(0, '127.0.0.1', () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
  });
}

function startStaticServer(httpErrors) {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const urlPath = (req.url || '/').split('?')[0];
      let relPath = decodeURIComponent(urlPath).replace(/^\/+/, '');
      if (!relPath || urlPath.endsWith('/')) {
        relPath = path.join(relPath, 'index.html');
      }
      let fullPath = path.join(STATIC_ROOT, relPath);
      if (fs.existsSync(fullPath) && fs.statSync(fullPath).isDirectory()) {
        fullPath = path.join(fullPath, 'index.html');
      }

      if (!fullPath.startsWith(STATIC_ROOT) || !fs.existsSync(fullPath)) {
        httpErrors.push({ url: req.url, status: 404 });
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not found');
        return;
      }

      const ext = path.extname(fullPath).toLowerCase();
      res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
      fs.createReadStream(fullPath).pipe(res);
    });

    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      resolve({ server, port: server.address().port });
    });
  });
}

class CdpClient {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.id = 0;
    this.pending = new Map();
    this.events = [];
    this.ready = new Promise((resolve, reject) => {
      this.ws.addEventListener('open', resolve);
      this.ws.addEventListener('error', reject);
    });
    this.ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id && this.pending.has(msg.id)) {
        const { resolve, reject } = this.pending.get(msg.id);
        this.pending.delete(msg.id);
        if (msg.error) reject(new Error(msg.error.message));
        else resolve(msg.result);
      } else if (msg.method) {
        this.events.push(msg);
      }
    });
  }

  async send(method, params = {}) {
    await this.ready;
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evalJs(expr) {
    const res = await this.send('Runtime.evaluate', {
      expression: expr,
      returnByValue: true,
      awaitPromise: true,
    });
    if (res.exceptionDetails) {
      throw new Error('JS Eval Error: ' + JSON.stringify(res.exceptionDetails));
    }
    return res.result ? res.result.value : undefined;
  }

  close() {
    try { this.ws.close(); } catch { /* ignore */ }
  }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitForTarget(debugPort) {
  for (let i = 0; i < 40; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${debugPort}/json/list`);
      if (r.ok) {
        const list = await r.json();
        const page = list.find((t) => t.type === 'page' && t.webSocketDebuggerUrl);
        if (page) return page;
      }
    } catch { /* retry */ }
    await sleep(150);
  }
  throw new Error('Timed out waiting for Edge CDP target.');
}

async function waitForCondition(cdp, expr, timeoutMs = 8000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const ok = await cdp.evalJs(expr);
    if (ok) return true;
    await sleep(120);
  }
  throw new Error(`Timeout waiting for condition: ${expr}`);
}

function assert(cond, msg) {
  if (!cond) throw new Error(`ASSERTION FAILED: ${msg}`);
}

async function run() {
  const edgeBin = findEdgeBinary();
  const httpErrors = [];
  const { server, port } = await startStaticServer(httpErrors);
  const debugPort = await getFreePort();
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'lifeops-edge-'));

  const edgeProc = spawn(
    edgeBin,
    [
      `--remote-debugging-port=${debugPort}`,
      `--user-data-dir=${userDataDir}`,
      '--headless=new',
      '--disable-gpu',
      '--no-first-run',
      '--no-default-browser-check',
      'about:blank',
    ],
    { stdio: 'ignore' }
  );

  let cdp;
  try {
    const target = await waitForTarget(debugPort);
    cdp = new CdpClient(target.webSocketDebuggerUrl);
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false,
    });

    const baseUrl = `http://127.0.0.1:${port}/apps/lifeops/#/personal?tab=sport&mock=true&lang=es`;
    await cdp.send('Page.navigate', { url: baseUrl });
    await waitForCondition(cdp, "document.querySelectorAll('.workout-card').length === 12");

    // 1. Desktop checks: 12 cards default, range text, summary KPIs
    const desktopP1 = await cdp.evalJs(`(() => ({
      count: document.querySelectorAll('.workout-card').length,
      firstTitle: document.querySelector('.workout-title')?.textContent?.trim(),
      rangeText: document.querySelector('.paginator-range-text')?.textContent?.trim(),
      kpiKm: document.querySelector('.metrics-banner .metric-value')?.textContent?.trim(),
      hash: window.location.hash,
    }))()`);
    assert(desktopP1.count === 12, `Expected 12 cards, got ${desktopP1.count}`);
    assert(desktopP1.rangeText && desktopP1.rangeText.includes('1–12') && desktopP1.rangeText.includes('64'),
      `Unexpected rangeText on P1: ${desktopP1.rangeText}`);
    assert(desktopP1.kpiKm && !desktopP1.kpiKm.startsWith('0.0') && !desktopP1.kpiKm.startsWith('—'),
      `Unexpected KPI km: ${desktopP1.kpiKm}`);

    // 2. Navigate to Page 2
    await cdp.evalJs("document.querySelector('button[aria-label=\"Siguiente\"]')?.click()");
    await waitForCondition(cdp, "document.querySelector('.paginator-range-text')?.textContent?.includes('13–24')");
    const desktopP2 = await cdp.evalJs(`(() => ({
      count: document.querySelectorAll('.workout-card').length,
      firstTitle: document.querySelector('.workout-title')?.textContent?.trim(),
      hash: window.location.hash,
    }))()`);
    assert(desktopP2.count === 12, `Expected 12 cards on P2, got ${desktopP2.count}`);
    assert(desktopP2.firstTitle !== desktopP1.firstTitle, 'Page 2 firstTitle should differ from Page 1');
    assert(desktopP2.hash.includes('page=2'), `Expected page=2 in hash, got ${desktopP2.hash}`);

    // 3. Switch Page Size to 24 and then 48
    await cdp.evalJs("Array.from(document.querySelectorAll('.page-size-btn')).find(b => b.textContent.trim() === '24')?.click()");
    await waitForCondition(cdp, "document.querySelectorAll('.workout-card').length === 24");
    const desktop24 = await cdp.evalJs("({ hash: window.location.hash, range: document.querySelector('.paginator-range-text')?.textContent?.trim() })");
    assert(desktop24.hash.includes('page=1') && desktop24.hash.includes('size=24'), `Expected page=1&size=24, got ${desktop24.hash}`);

    await cdp.evalJs("Array.from(document.querySelectorAll('.page-size-btn')).find(b => b.textContent.trim() === '48')?.click()");
    await waitForCondition(cdp, "document.querySelectorAll('.workout-card').length === 48");
    const desktop48 = await cdp.evalJs("({ hash: window.location.hash, range: document.querySelector('.paginator-range-text')?.textContent?.trim() })");
    assert(desktop48.hash.includes('size=48') && desktop48.range.includes('1–48'), `Unexpected 48-size state: ${JSON.stringify(desktop48)}`);

    // Restore 12 for mobile check
    await cdp.evalJs("Array.from(document.querySelectorAll('.page-size-btn')).find(b => b.textContent.trim() === '12')?.click()");
    await waitForCondition(cdp, "document.querySelectorAll('.workout-card').length === 12");

    // 4. Mobile 390x844 check (including override of stale desktop 'table' preference)
    await cdp.evalJs("localStorage.setItem('lifeops_view_sport', 'table'); sessionStorage.removeItem('lifeops_view_sport_session');");
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true,
    });
    await cdp.send('Page.reload', { ignoreCache: true });
    await waitForCondition(cdp, "document.querySelectorAll('.workout-card').length === 12");

    const mobileCheck = await cdp.evalJs(`(() => {
      const cards = document.querySelectorAll('.workout-card').length;
      const tables = document.querySelectorAll('.module-data-table').length;
      const mobPag = document.querySelector('.paginator-pages-mobile');
      const deskPag = document.querySelector('.paginator-pages-desktop');
      const stepBtn = document.querySelector('.paginator-step-btn');
      const sizeBtn = document.querySelector('.page-size-btn');
      return {
        cards,
        tables,
        mobText: mobPag?.textContent?.trim(),
        mobDisplay: mobPag ? getComputedStyle(mobPag).display : null,
        deskDisplay: deskPag ? getComputedStyle(deskPag).display : null,
        stepHeight: stepBtn ? stepBtn.getBoundingClientRect().height : 0,
        sizeHeight: sizeBtn ? sizeBtn.getBoundingClientRect().height : 0,
        scrollWidth: document.documentElement.scrollWidth,
      };
    })()`);

    assert(mobileCheck.cards === 12 && mobileCheck.tables === 0,
      `Mobile should default to Cards (12 cards, 0 tables), got ${JSON.stringify(mobileCheck)}`);
    assert(mobileCheck.mobDisplay !== 'none' && mobileCheck.deskDisplay === 'none',
      `Mobile paginator layout mismatch: ${JSON.stringify(mobileCheck)}`);
    assert(mobileCheck.stepHeight >= 44 && mobileCheck.sizeHeight >= 44,
      `Mobile touch targets < 44px: ${JSON.stringify(mobileCheck)}`);
    assert(mobileCheck.scrollWidth <= 390,
      `Mobile horizontal overflow detected: scrollWidth=${mobileCheck.scrollWidth}`);

    // 5. INV-16: Verify simulated API error renders .sport-error-state (NEVER .empty-state)
    await cdp.send('Fetch.enable', {
      patterns: [{ urlPattern: '*lifeops-api.onrender.com*' }],
    });
    cdp.ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.method === 'Fetch.requestPaused') {
        const method = msg.params?.request?.method || 'GET';
        if (method === 'OPTIONS') {
          cdp.send('Fetch.fulfillRequest', {
            requestId: msg.params.requestId,
            responseCode: 204,
            responseHeaders: [
              { name: 'Access-Control-Allow-Origin', value: '*' },
              { name: 'Access-Control-Allow-Headers', value: '*' },
              { name: 'Access-Control-Allow-Methods', value: 'GET,POST,PATCH,DELETE,OPTIONS' },
            ],
            body: '',
          }).catch(() => null);
          return;
        }
        cdp.send('Fetch.fulfillRequest', {
          requestId: msg.params.requestId,
          responseCode: 400,
          responseHeaders: [
            { name: 'Content-Type', value: 'application/json' },
            { name: 'Access-Control-Allow-Origin', value: '*' },
          ],
          body: Buffer.from(JSON.stringify({ detail: 'Simulated outage for INV-16' })).toString('base64'),
        }).catch(() => null);
      }
    });

    await cdp.evalJs(`(() => {
      localStorage.clear();
      sessionStorage.clear();
      const exp = Math.floor(Date.now() / 1000) + 3600;
      const b64 = (obj) => btoa(JSON.stringify(obj)).replace(/=/g, '').replace(/\\+/g, '-').replace(/\\//g, '_');
      const fakeJwt = b64({ alg: 'HS256', typ: 'JWT' }) + '.' + b64({ sub: 'e2e-user-1', role: 'authenticated', exp }) + '.sig';
      localStorage.setItem('sb-wkbmxekmofrjtcsyytrv-auth-token', JSON.stringify({
        access_token: fakeJwt,
        refresh_token: 'e2e-fake-refresh',
        expires_in: 3600,
        expires_at: exp,
        token_type: 'bearer',
        user: { id: 'e2e-user-1', email: 'e2e@datalaria.com', role: 'authenticated', aud: 'authenticated' }
      }));
    })()`);
    // Full reload via about:blank -> target URL so AuthProvider re-initializes without mock=true
    await cdp.send('Page.navigate', { url: 'about:blank' });
    await sleep(150);
    await cdp.send('Page.navigate', { url: `http://127.0.0.1:${port}/apps/lifeops/#/personal?tab=sport&lang=es` });
    await waitForCondition(cdp, "document.querySelectorAll('.sport-error-state').length === 1", 10000);

    const inv16Check = await cdp.evalJs(`(() => ({
      hasErrorState: document.querySelectorAll('.sport-error-state').length === 1,
      hasEmptyState: document.querySelectorAll('.empty-state').length > 0,
      hasRetryBtn: document.querySelectorAll('.sport-retry-btn').length === 1,
      errorDetail: document.querySelector('.sport-error-detail')?.textContent?.trim(),
    }))()`);
    assert(inv16Check.hasErrorState && !inv16Check.hasEmptyState && inv16Check.hasRetryBtn,
      `INV-16 violation: ${JSON.stringify(inv16Check)}`);

    // 6. Check zero runtime exceptions or 404s
    const consoleErrors = cdp.events
      .filter((e) => e.method === 'Runtime.exceptionThrown')
      .map((e) => e.params?.exceptionDetails?.text || 'Exception');
    assert(consoleErrors.length === 0, `Runtime exceptions: ${JSON.stringify(consoleErrors)}`);
    assert(httpErrors.length === 0, `Static HTTP 404 errors: ${JSON.stringify(httpErrors)}`);

    console.log('E2E EDGE CHECK PASSED ✅', JSON.stringify({ desktopP1, desktopP2, mobileCheck, inv16Check }));
  } finally {
    if (cdp) cdp.close();
    try { edgeProc.kill('SIGKILL'); } catch { /* ignore */ }
    server.close();
    try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch { /* ignore */ }
  }
}

run().catch((err) => {
  console.error('E2E EDGE CHECK FAILED ❌', err);
  process.exit(1);
});
