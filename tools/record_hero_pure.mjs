import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const MIME = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.svg': 'image/svg+xml' };

const htmlContent = `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    html, body { margin: 0; padding: 0; background: transparent; overflow: hidden; width: 320px; height: 320px; }
    svg { width: 320px; height: 320px; overflow: visible; }
  </style>
</head>
<body>
  <svg id="stage"><g id="back"></g><g id="front"></g></svg>
  <script type="module">
    import { Dopakichi } from '/zh-CN/js/dopakichi.js';
    const hero = new Dopakichi(document.getElementById('back'), { scale: 0.9, palette: 'pink', front: document.getElementById('front') });
    hero.place(160, 260);
    hero.blinkAt = performance.now() + 600;
    let last = performance.now();
    function loop(t) {
      const dt = Math.min(0.05, (t - last) / 1000);
      last = t;
      hero.update(dt, t);
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
  </script>
</body>
</html>`;

const server = http.createServer((req, res) => {
  let url = req.url.split('?')[0];
  if (url === '/hero-only.html') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(htmlContent);
    return;
  }
  const filePath = 'app' + url;
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = '.' + filePath.split('.').pop();
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(fs.readFileSync(filePath));
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

await new Promise(r => server.listen(0, '127.0.0.1', r));
const appPort = server.address().port;
const cdpPort = 55198;
const tmpDir = '/tmp/hero-isolated-frames';
fs.rmSync(tmpDir, { recursive: true, force: true });
fs.mkdirSync(tmpDir, { recursive: true });

console.log('Starting chrome...');
const chrome = spawn(CHROME_PATH, [
  '--headless=new',
  `--remote-debugging-port=${cdpPort}`,
  `--user-data-dir=/tmp/chrome-hero-iso-${Date.now()}`,
  '--no-first-run',
  '--no-default-browser-check',
  '--window-size=320,320',
]);

for (let i = 0; i < 30; i++) {
  try {
    await new Promise((res, rej) => http.get(`http://127.0.0.1:${cdpPort}/json/version`, res).on('error', rej));
    break;
  } catch {
    await new Promise(r => setTimeout(r, 200));
  }
}

console.log('Opening tab...');
const target = await new Promise((res, rej) => {
  const req = http.request({ hostname: '127.0.0.1', port: cdpPort, path: `/json/new?http://127.0.0.1:${appPort}/hero-only.html`, method: 'PUT' }, (r) => {
    let d = ''; r.on('data', c => d += c); r.on('end', () => res(JSON.parse(d)));
  });
  req.on('error', rej);
  req.end();
});

const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);

let idCounter = 1;
const pending = new Map();
ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  if (msg.id && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    if (msg.error) reject(msg.error);
    else resolve(msg.result);
  }
};
const send = (method, params = {}) => new Promise((resolve, reject) => {
  const id = idCounter++;
  pending.set(id, { resolve, reject });
  ws.send(JSON.stringify({ id, method, params }));
});

await send('Page.enable');
await send('Emulation.setDeviceMetricsOverride', {
  width: 320,
  height: 320,
  deviceScaleFactor: 1,
  mobile: false,
});
// Set transparent background
await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });

console.log('Waiting for animation to stabilize...');
await new Promise(r => setTimeout(r, 800));

const frames = 28;
console.log(`Capturing ${frames} frames...`);
for (let i = 0; i < frames; i++) {
  const shot = await send('Page.captureScreenshot', {
    format: 'png',
    fromSurface: true,
  });
  fs.writeFileSync(path.join(tmpDir, `frame_${String(i).padStart(3, '0')}.png`), Buffer.from(shot.data, 'base64'));
  await new Promise(r => setTimeout(r, 55)); // ~18 fps
}

chrome.kill();
server.close();
console.log(`Saved ${frames} frames to ${tmpDir}`);
