import { spawn } from 'node:child_process';
import http from 'node:http';

const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const port = 9222;

const chrome = spawn(chromePath, [
  '--headless=new',
  `--remote-debugging-port=${port}`,
  '--no-first-run',
  '--no-default-browser-check',
  '--user-data-dir=/tmp/chrome-test-profile-' + Date.now(),
]);

async function checkPort() {
  for (let i = 0; i < 20; i++) {
    try {
      const res = await new Promise((resolve, reject) => {
        http.get(`http://127.0.0.1:${port}/json/version`, (r) => {
          let data = '';
          r.on('data', chunk => data += chunk);
          r.on('end', () => resolve(data));
        }).on('error', reject);
      });
      console.log('Chrome CDP available:', JSON.parse(res)['Browser']);
      return true;
    } catch {
      await new Promise(r => setTimeout(r, 200));
    }
  }
  return false;
}

const ok = await checkPort();
chrome.kill();
process.exit(ok ? 0 : 1);
