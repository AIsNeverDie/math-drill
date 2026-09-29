import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

const PORT = 8000;
const ROOT = path.resolve('app');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2',
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.json': 'application/json',
};

const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0].split('#')[0];
  if (reqPath.endsWith('/')) reqPath += 'index.html';
  
  const filePath = path.join(ROOT, reqPath);
  
  if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found');
    return;
  }

  const ext = path.extname(filePath);
  const contentType = MIME[ext] || 'application/octet-stream';
  const rawData = fs.readFileSync(filePath);
  const acceptEncoding = req.headers['accept-encoding'] || '';

  // WOFF2 is already compressed, don't re-compress
  const shouldCompress = ['.html', '.js', '.css', '.svg', '.json'].includes(ext) && rawData.length > 512;

  if (shouldCompress && acceptEncoding.includes('br')) {
    const compressed = zlib.brotliCompressSync(rawData);
    res.writeHead(200, {
      'Content-Type': contentType,
      'Content-Encoding': 'br',
      'Vary': 'Accept-Encoding',
      'Content-Length': compressed.length,
      'Cache-Control': 'no-cache',
    });
    res.end(compressed);
  } else if (shouldCompress && acceptEncoding.includes('gzip')) {
    const compressed = zlib.gzipSync(rawData);
    res.writeHead(200, {
      'Content-Type': contentType,
      'Content-Encoding': 'gzip',
      'Vary': 'Accept-Encoding',
      'Content-Length': compressed.length,
      'Cache-Control': 'no-cache',
    });
    res.end(compressed);
  } else {
    res.writeHead(200, {
      'Content-Type': contentType,
      'Content-Length': rawData.length,
      'Cache-Control': 'no-cache',
    });
    res.end(rawData);
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`[DevServer] High-performance Brotli/Gzip server running at http://localhost:${PORT}/`);
});
