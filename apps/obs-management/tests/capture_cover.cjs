// apps/obs-management/tests/capture_cover.cjs
// Captura determinista de portadas reales 1280x800 con Microsoft Edge Headless CDP.
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

function startStaticServer() {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      const urlPath = (req.url || '/').split('?')[0];
      let rel = decodeURIComponent(urlPath).replace(/^\/+/, '');
      if (!rel || urlPath.endsWith('/')) rel = path.join(rel, 'index.html');
      let full = path.join(STATIC_ROOT, rel);
      if (fs.existsSync(full) && fs.statSync(full).isDirectory()) full = path.join(full, 'index.html');
      if (!full.startsWith(STATIC_ROOT) || !fs.existsSync(full)) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      res.writeHead(200, { 'Content-Type': MIME[path.extname(full)] || 'application/octet-stream' });
      fs.createReadStream(full).pipe(res);
    });
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

class Cdp {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.id = 0;
    this.pending = new Map();
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

  close() {
    try { this.ws.close(); } catch { /* ignore */ }
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
    await sleep(150);
  }
  throw new Error('Timeout waiting for Edge CDP websocket target.');
}

async function capture() {
  const edgePath = findEdge();
  const server = await startStaticServer();
  const port = server.address().port;
  const cdpPort = await getFreePort();
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'edge-cover-'));

  const edgeArgs = [
    '--headless=new',
    `--remote-debugging-port=${cdpPort}`,
    `--user-data-dir=${userDataDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-gpu',
    '--window-size=1280,800',
    '--force-device-scale-factor=1',
    'about:blank',
  ];

  const edge = spawn(edgePath, edgeArgs);
  let cdp = null;

  try {
    const wsUrl = await waitForWsUrl(cdpPort);
    cdp = new Cdp(wsUrl);
    await cdp.ready;

    await cdp.send('Page.enable');
    await cdp.send('DOM.enable');
    await cdp.send('Network.enable');

    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: 1280,
      height: 800,
      deviceScaleFactor: 1,
      mobile: false,
    });

    const targets = [
      {
        lang: 'es',
        dest: path.join(REPO_ROOT, 'content', 'es', 'apps', 'obs-management', 'cover.png'),
        url: `http://127.0.0.1:${port}/apps/obs-management/?lang=es&scenario=drone-capacitor`,
      },
      {
        lang: 'en',
        dest: path.join(REPO_ROOT, 'content', 'en', 'apps', 'obs-management', 'cover.png'),
        url: `http://127.0.0.1:${port}/apps/obs-management/?lang=en&scenario=drone-capacitor`,
      },
    ];

    for (const t of targets) {
      console.log(`Navegando a: ${t.url}`);
      await cdp.send('Page.navigate', { url: t.url });
      await sleep(1500);

      const shot = await cdp.send('Page.captureScreenshot', {
        format: 'png',
        clip: {
          x: 0,
          y: 0,
          width: 1280,
          height: 800,
          scale: 1,
        },
      });

      const buf = Buffer.from(shot.data, 'base64');
      fs.mkdirSync(path.dirname(t.dest), { recursive: true });
      fs.writeFileSync(t.dest, buf);
      const stat = fs.statSync(t.dest);
      console.log(`Guardada portada ${t.lang}: ${t.dest} (${stat.size} bytes)`);
    }

    console.log('OK: Captura de portadas 1280x800 completada.');
  } finally {
    if (cdp) cdp.close();
    edge.kill();
    server.close();
    try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch { /* ignore */ }
  }
}

capture().catch((err) => {
  console.error('CAPTURE_ERROR:', err.message);
  process.exit(1);
});
