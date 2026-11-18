// apps/reading/tests/e2e_edge_check.js
// Verificación E2E determinista con Microsoft Edge Headless CDP en viewports 1440x900 y 390x844.
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

function assert(cond, msg) {
  if (!cond) throw new Error('E2E ASSERTION FAILED: ' + msg);
}

async function runE2E() {
  const edgeBin = findEdgeBinary();
  const debugPort = await getFreePort();
  const tmpProfile = fs.mkdtempSync(path.join(os.tmpdir(), 'edge-reading-e2e-'));
  const httpErrors = [];
  const { server, port } = await startStaticServer(httpErrors);
  const baseUrl = `http://127.0.0.1:${port}/apps/reading/?lang=es`;

  const edgeProc = spawn(edgeBin, [
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    `--remote-debugging-port=${debugPort}`,
    `--user-data-dir=${tmpProfile}`,
    'about:blank',
  ], { stdio: 'ignore' });

  let client = null;
  try {
    const target = await waitForTarget(debugPort);
    client = new CdpClient(target.webSocketDebuggerUrl);

    await client.send('Page.enable');
    await client.send('Runtime.enable');
    await client.send('Console.enable');
    await client.send('Network.enable');

    // ==================== 1. DESKTOP 1440x900 ====================
    await client.send('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false,
    });

    await client.send('Page.navigate', { url: baseUrl });
    for (let i = 0; i < 40; i++) {
      const ready = await client.evalJs(`document.readyState === 'complete' && document.querySelectorAll('.profile-chip').length === 3`);
      if (ready) break;
      await sleep(100);
    }

    const desktopInit = await client.evalJs(`({
      title: document.getElementById('shell-app-title')?.textContent,
      profiles: document.querySelectorAll('.profile-chip').length,
      tabs: document.querySelectorAll('.tab-btn').length,
      overflow: document.documentElement.scrollWidth > window.innerWidth,
      scrollWidth: document.documentElement.scrollWidth,
      innerWidth: window.innerWidth
    })`);
    assert(desktopInit.title === 'Lector Arcade', `Expected Lector Arcade, got ${desktopInit.title}`);
    assert(desktopInit.profiles === 3, `Expected 3 profiles, got ${desktopInit.profiles}`);
    assert(desktopInit.tabs === 3, `Expected 3 tabs, got ${desktopInit.tabs}`);
    assert(!desktopInit.overflow, `Desktop overflow: ${desktopInit.scrollWidth} > ${desktopInit.innerWidth}`);

    // Cambio ES -> EN -> ES
    await client.evalJs(`document.getElementById('lang-btn').click()`);
    await sleep(100);
    const enTitle = await client.evalJs(`document.getElementById('shell-app-title')?.textContent`);
    assert(enTitle === 'Reader Arcade', `Expected Reader Arcade in EN, got ${enTitle}`);

    await client.evalJs(`document.getElementById('lang-btn').click()`);
    await sleep(100);
    const esTitle = await client.evalJs(`document.getElementById('shell-app-title')?.textContent`);
    assert(esTitle === 'Lector Arcade', `Expected Lector Arcade back in ES, got ${esTitle}`);

    // Tema Claro <-> Oscuro (soporta inicio light o dark según OS)
    const initialTheme = await client.evalJs(`document.documentElement.getAttribute('data-theme')`);
    const expectedFlipped = initialTheme === 'dark' ? 'light' : 'dark';
    await client.evalJs(`document.getElementById('theme-btn').click()`);
    await sleep(100);
    assert(await client.evalJs(`document.documentElement.getAttribute('data-theme')`) === expectedFlipped, `Theme did not flip to ${expectedFlipped}`);
    await client.evalJs(`document.getElementById('theme-btn').click()`);
    await sleep(100);
    assert(await client.evalJs(`document.documentElement.getAttribute('data-theme')`) === initialTheme, `Theme did not flip back to ${initialTheme}`);

    // Pestaña Aprender + Mesa de Mezclas
    await client.evalJs(`document.querySelector('[data-tab="learn"]').click()`);
    await sleep(150);
    await client.evalJs(`document.querySelector('[data-learn-sub="direct"]').click()`);
    await sleep(150);
    const learnState = await client.evalJs(`({
      mixerPills: document.querySelectorAll('.mixer-pill').length,
      cards: document.querySelectorAll('.phonics-card').length,
      overflow: document.documentElement.scrollWidth > window.innerWidth
    })`);
    assert(learnState.mixerPills >= 8, `Expected >=8 mixer pills, got ${learnState.mixerPills}`);
    assert(learnState.cards === 5, `Expected 5 direct syllable cards, got ${learnState.cards}`);
    assert(!learnState.overflow, 'Desktop Learn overflow');

    // Pestaña Jugar en Nivel l3 (Letras Faltantes + Teclado Táctil 3D)
    await client.evalJs(`document.querySelector('[data-tab="play"]').click()`);
    await sleep(150);
    await client.evalJs(`document.querySelector('[data-level="l3"]').click(); document.querySelector('[data-mode="normal"]').click(); document.getElementById('btn-start').click();`);
    await sleep(200);
    const l3State = await client.evalJs(`(() => {
      const btn = document.querySelector('.alpha-btn[data-alpha-char]');
      const rect = btn ? btn.getBoundingClientRect() : { width: 0, height: 0 };
      return {
        slots: document.querySelectorAll('.letter-slot').length,
        blanks: document.querySelectorAll('.letter-slot.blank').length,
        alphaCount: document.querySelectorAll('.alpha-btn[data-alpha-char]').length,
        btnW: rect.width,
        btnH: rect.height
      };
    })()`);
    assert(l3State.slots >= 3, 'Expected >=3 letter slots in l3');
    assert(l3State.blanks >= 1, 'Expected >=1 blank slots in l3');
    assert(l3State.alphaCount >= 8 && l3State.alphaCount <= 10, `Expected 8-10 alpha keys, got ${l3State.alphaCount}`);
    assert(l3State.btnW >= 48 && l3State.btnH >= 48, `Alpha button too small: ${l3State.btnW}x${l3State.btnH}`);

    // Rellenar los huecos usando los botones táctiles y verificar feedback banner
    await client.evalJs(`(() => {
      const blanks = document.querySelectorAll('.letter-slot.blank').length;
      for (let i = 0; i < blanks; i++) {
        const b = document.querySelector('.alpha-btn[data-alpha-char]');
        if (b) b.click();
      }
    })()`);
    await sleep(150);
    const l3Banner = await client.evalJs(`Boolean(document.querySelector('#feedback-banner-container .feedback-banner'))`);
    assert(l3Banner, 'Expected feedback banner after filling all l3 slots');
    await client.evalJs(`document.getElementById('btn-exit-game').click()`);
    await sleep(150);

    // Pestaña Jugar en Nivel l5 (Frases 2 Líneas) Modo Contrarreloj (stopwatch)
    await client.evalJs(`document.querySelector('[data-level="l5"]').click(); document.querySelector('[data-mode="stopwatch"]').click(); document.getElementById('btn-start').click();`);
    await sleep(600);
    const l5Start = await client.evalJs(`({
      lines: document.querySelectorAll('.reading-sentence-line').length,
      hasPill: Boolean(document.getElementById('stopwatch-pill')),
      isFrozen: document.getElementById('stopwatch-pill')?.classList.contains('frozen'),
      hasReadBtn: Boolean(document.getElementById('btn-read-done'))
    })`);
    assert(l5Start.lines === 2, `Expected 2 lines in l5, got ${l5Start.lines}`);
    assert(l5Start.hasPill && !l5Start.isFrozen, 'Stopwatch should be active and not frozen');
    assert(l5Start.hasReadBtn, 'Missing #btn-read-done button');

    // Pulsar ¡Leído! -> congelar cronómetro instantáneamente + mostrar Micro-Check
    await client.evalJs(`document.getElementById('btn-read-done').click()`);
    await sleep(150);
    const frozenText1 = await client.evalJs(`document.getElementById('stopwatch-display')?.textContent`);
    await sleep(300);
    const frozenText2 = await client.evalJs(`document.getElementById('stopwatch-display')?.textContent`);
    const mcState = await client.evalJs(`({
      isFrozen: document.getElementById('stopwatch-pill')?.classList.contains('frozen'),
      mcCount: document.querySelectorAll('.micro-check-btn').length
    })`);
    assert(mcState.isFrozen, 'Stopwatch pill did not freeze on ¡Leído!');
    assert(frozenText1 === frozenText2, `Frozen stopwatch kept moving: ${frozenText1} -> ${frozenText2}`);
    assert(frozenText1.includes('PPM') || frozenText1.includes('WPM'), `Expected PPM in frozen stopwatch: ${frozenText1}`);
    assert(mcState.mcCount === 3, `Expected 3 micro-check options, got ${mcState.mcCount}`);

    await client.evalJs(`document.querySelector('.micro-check-btn').click()`);
    await sleep(150);
    assert(await client.evalJs(`Boolean(document.querySelector('.feedback-banner'))`), 'Missing feedback after micro-check');
    await client.evalJs(`document.getElementById('btn-exit-game').click()`);
    await sleep(150);

    // Pestaña Logros
    await client.evalJs(`document.querySelector('[data-tab="achievements"]').click()`);
    await sleep(150);
    const achState = await client.evalJs(`({
      medals: document.querySelectorAll('.medal-card').length,
      hasDiplomaBtn: Boolean(document.getElementById('btn-download-diploma')),
      hasDiplomaFn: typeof window.downloadReadingDiploma === 'function'
    })`);
    assert(achState.medals === 6, `Expected 6 medals, got ${achState.medals}`);
    assert(achState.hasDiplomaBtn && achState.hasDiplomaFn, 'Missing diploma button or function');

    // ==================== 2. MOBILE 390x844 ====================
    await client.send('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true,
    });
    await client.send('Page.navigate', { url: baseUrl });
    for (let i = 0; i < 40; i++) {
      const ready = await client.evalJs(`document.readyState === 'complete' && document.querySelectorAll('.profile-chip').length === 3`);
      if (ready) break;
      await sleep(100);
    }
    assert(!(await client.evalJs(`document.documentElement.scrollWidth > window.innerWidth`)), 'Mobile menu horizontal overflow');

    await client.evalJs(`document.querySelector('[data-tab="learn"]').click()`);
    await sleep(150);
    assert(!(await client.evalJs(`document.documentElement.scrollWidth > window.innerWidth`)), 'Mobile learn horizontal overflow');

    await client.evalJs(`document.querySelector('[data-tab="play"]').click()`);
    await sleep(150);
    await client.evalJs(`document.querySelector('[data-level="l3"]').click(); document.getElementById('btn-start').click();`);
    await sleep(150);
    assert(!(await client.evalJs(`document.documentElement.scrollWidth > window.innerWidth`)), 'Mobile l3 horizontal overflow');
    await client.evalJs(`document.getElementById('btn-exit-game').click()`);
    await sleep(150);

    await client.evalJs(`document.querySelector('[data-level="l5"]').click(); document.querySelector('[data-mode="stopwatch"]').click(); document.getElementById('btn-start').click();`);
    await sleep(150);
    assert(!(await client.evalJs(`document.documentElement.scrollWidth > window.innerWidth`)), 'Mobile l5 horizontal overflow');

    // ==================== 3. SHIM EN ====================
    await client.send('Page.navigate', { url: `http://127.0.0.1:${port}/apps/reading/en/` });
    for (let i = 0; i < 40; i++) {
      const ready = await client.evalJs(`document.readyState === 'complete' && document.getElementById('shell-app-title')?.textContent === 'Reader Arcade'`);
      if (ready) break;
      await sleep(100);
    }
    const shimTitle = await client.evalJs(`document.getElementById('shell-app-title')?.textContent`);
    assert(shimTitle === 'Reader Arcade', `EN shim did not redirect cleanly, got ${shimTitle}`);

    // Verificar 0 errores JS / consola / HTTP >= 400
    const consoleErrors = client.events
      .filter((e) => e.method === 'Console.messageAdded' && e.params.message.level === 'error')
      .map((e) => e.params.message.text);
    const pageErrors = client.events
      .filter((e) => e.method === 'Runtime.exceptionThrown')
      .map((e) => e.params.exceptionDetails?.text || 'RuntimeException');
    const netErrors = client.events
      .filter((e) => e.method === 'Network.responseReceived' && e.params.response.status >= 400)
      .map((e) => `${e.params.response.status} ${e.params.response.url}`);

    assert(consoleErrors.length === 0, 'Console errors: ' + JSON.stringify(consoleErrors));
    assert(pageErrors.length === 0, 'JS Exceptions: ' + JSON.stringify(pageErrors));
    assert(httpErrors.length === 0 && netErrors.length === 0, 'HTTP >= 400: ' + JSON.stringify([...httpErrors, ...netErrors]));

    console.log(JSON.stringify({
      status: 'E2E_PASS',
      desktop_1440x900: 'PASS',
      mobile_390x844: 'PASS',
      en_shim: 'PASS',
      consoleErrors: consoleErrors.length,
      pageErrors: pageErrors.length,
      httpErrors: httpErrors.length + netErrors.length,
      frozenStopwatchSample: frozenText1
    }, null, 2));
  } catch (err) {
    if (client) {
      const exs = client.events.filter((e) => e.method === 'Runtime.exceptionThrown' || e.method === 'Console.messageAdded');
      console.error('CDP EVENTS ON FAILURE:', JSON.stringify(exs, null, 2));
    }
    throw err;
  } finally {
    if (client) client.close();
    try { edgeProc.kill('SIGKILL'); } catch { /* */ }
    server.close();
    await sleep(200);
    try { fs.rmSync(tmpProfile, { recursive: true, force: true }); } catch { /* */ }
  }
}

runE2E().catch((err) => {
  console.error(err);
  process.exit(1);
});
