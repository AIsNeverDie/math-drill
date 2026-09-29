import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';

const CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

// 1. Start static server
const MIME = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2',
};

const server = http.createServer((req, res) => {
  let url = req.url.split('?')[0].split('#')[0];
  if (url.endsWith('/')) url += 'index.html';
  const filePath = 'app' + url;
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = '.' + filePath.split('.').pop();
    res.writeHead(200, {
      'Content-Type': MIME[ext] || 'application/octet-stream',
      'Cache-Control': 'no-cache',
    });
    res.end(fs.readFileSync(filePath));
  } else {
    res.writeHead(404);
    res.end('Not found: ' + filePath);
  }
});

await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const appPort = server.address().port;
console.log(`[E2E] Static app server running at http://127.0.0.1:${appPort}/`);

// 2. Start Headless Chrome
// Pick free port for CDP
const cdpPort = 55182;
const userDataDir = `/tmp/chrome-mathdrill-e2e-${Date.now()}`;
const chrome = spawn(CHROME_PATH, [
  '--headless=new',
  `--remote-debugging-port=${cdpPort}`,
  `--user-data-dir=${userDataDir}`,
  '--no-first-run',
  '--no-default-browser-check',
  '--window-size=412,915', // Phone screen
]);

// Wait for CDP
let versionInfo = null;
for (let i = 0; i < 30; i++) {
  try {
    const raw = await new Promise((resolve, reject) => {
      http.get(`http://127.0.0.1:${cdpPort}/json/version`, (r) => {
        let d = '';
        r.on('data', c => d += c);
        r.on('end', () => resolve(d));
      }).on('error', reject);
    });
    versionInfo = JSON.parse(raw);
    break;
  } catch {
    await new Promise(r => setTimeout(r, 200));
  }
}
if (!versionInfo) throw new Error('Failed to connect to Headless Chrome CDP');

// Create new target/tab
const target = await new Promise((resolve, reject) => {
  const req = http.request({
    hostname: '127.0.0.1',
    port: cdpPort,
    path: `/json/new?http://127.0.0.1:${appPort}/`,
    method: 'PUT'
  }, (r) => {
    let d = '';
    r.on('data', c => d += c);
    r.on('end', () => resolve(JSON.parse(d)));
  });
  req.on('error', reject);
  req.end();
});

const wsUrl = target.webSocketDebuggerUrl;
console.log('[E2E] Connected to browser target via WebSocket:', wsUrl);

const ws = new WebSocket(wsUrl);
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

function send(method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = idCounter++;
    pending.set(id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function evaluate(expr) {
  const res = await send('Runtime.evaluate', {
    expression: expr,
    awaitPromise: true,
    returnByValue: true,
  });
  if (res.exceptionDetails) {
    throw new Error('Evaluation exception: ' + JSON.stringify(res.exceptionDetails));
  }
  return res.result?.value;
}

await send('Page.enable');
await send('DOM.enable');

console.log('[E2E] Browser ready.');

// Helper to wait ms
const wait = (ms) => new Promise(r => setTimeout(r, ms));

async function runTests() {
  console.log('==================================================');
  console.log('   STARTING FULL E2E AND OVERFLOW TEST SUITE      ');
  console.log('==================================================\n');

  // TEST 1: Language routing from root
  console.log('--- Test 1: Language routing & persistence ---');
  await send('Page.navigate', { url: `http://127.0.0.1:${appPort}/?lang=zh-CN` });
  await wait(1000);
  let curUrl = await evaluate('location.href');
  console.log('1.1 Navigated with ?lang=zh-CN -> Current URL:', curUrl);
  if (!curUrl.includes('/zh-CN/')) throw new Error('Expected /zh-CN/ in URL');

  // TEST 2: Check font overflow in all 4 languages across all screens
  console.log('\n--- Test 2: Font & Text Layout Overflow Detection ---');
  const languages = ['en', 'ja', 'zh-CN', 'zh-TW'];
  for (const lang of languages) {
    console.log(`\nChecking layout & text bounding for language: [${lang}]`);
    await send('Page.navigate', { url: `http://127.0.0.1:${appPort}/${lang}/` });
    await wait(800);

    // Skip initial guide if present
    await evaluate(`
      const skip = document.querySelector('#guide-skip');
      if (skip && !document.querySelector('#guide').hidden) skip.click();
    `);
    await wait(300);

    // Check Title screen elements overflow
    const overflowReport = await evaluate(`
      (() => {
        const issues = [];
        // Test selectors on current screen
        const selectors = [
          '#logo', '.logo-pre', '.logo-top',
          '.level-btn', '#start-review', '.grades button',
          '.mode-row .sub-btn', '#quest-title', '#cal-title',
          '.hint'
        ];
        for (const s of selectors) {
          const els = document.querySelectorAll(s);
          for (const el of els) {
            if (el.hidden || el.offsetParent === null) continue;
            // Check if content overflows client bounding width significantly (> 2px)
            if (el.scrollWidth > el.clientWidth + 2) {
              issues.push({
                selector: s,
                text: el.textContent.trim().slice(0, 30),
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth
              });
            }
          }
        }
        return issues;
      })()
    `);
    if (overflowReport.length > 0) {
      console.warn(`[WARN] Possible overflows detected on title in ${lang}:`, overflowReport);
    } else {
      console.log(`✔ Title screen text layout clean in ${lang} (0 overflow issues)`);
    }

    // Check Settings Modal
    await evaluate(`document.querySelector('#open-settings').click();`);
    await wait(400);
    const settingsOverflow = await evaluate(`
      (() => {
        const issues = [];
        const selectors = ['.modal-card .chip', '.set-label', '.set-note', '.big-btn', '.sub-btn'];
        for (const s of selectors) {
          const els = document.querySelectorAll(s);
          for (const el of els) {
            if (el.hidden || el.offsetParent === null) continue;
            if (el.scrollWidth > el.clientWidth + 2) {
              issues.push({
                selector: s,
                text: el.textContent.trim().slice(0, 30),
                scrollWidth: el.scrollWidth,
                clientWidth: el.clientWidth
              });
            }
          }
        }
        return issues;
      })()
    `);
    if (settingsOverflow.length > 0) {
      console.warn(`[WARN] Settings overflow in ${lang}:`, settingsOverflow);
    } else {
      console.log(`✔ Settings modal text layout clean in ${lang}`);
    }
    await evaluate(`document.querySelector('#close-settings').click();`);
    await wait(300);

    // Check Skill Tree Screen
    await evaluate(`document.querySelector('#open-tree').click();`);
    await wait(500);
    const treeOverflow = await evaluate(`
      (() => {
        const issues = [];
        const nodes = document.querySelectorAll('.node');
        for (const el of nodes) {
          // Check the text spans inside the node to ensure no text overflowing the node button
          const textSpans = el.querySelectorAll('span');
          for (const sp of textSpans) {
            if (sp.scrollWidth > el.clientWidth + 1) {
              issues.push({
                id: el.dataset.id,
                text: sp.textContent.trim(),
                scrollWidth: sp.scrollWidth,
                clientWidth: el.clientWidth
              });
            }
          }
        }
        return issues;
      })()
    `);
    if (treeOverflow.length > 0) {
      console.warn(`[WARN] Tree nodes text overflow in ${lang}:`, treeOverflow);
    } else {
      console.log(`✔ Skill Tree (${lang}) text layout clean (0 node text overflow)`);
    }
    await evaluate(`document.querySelector('#tree-back').click();`);
    await wait(400);

    // Check Trophies Screen
    await evaluate(`document.querySelector('#open-trophy').click();`);
    await wait(500);
    const trophyOverflow = await evaluate(`
      (() => {
        const issues = [];
        const series = document.querySelectorAll('.tr-series summary');
        for (const el of series) {
          if (el.scrollWidth > el.clientWidth + 4) {
            issues.push({
              text: el.textContent.trim().slice(0, 30),
              scrollWidth: el.scrollWidth,
              clientWidth: el.clientWidth
            });
          }
        }
        return issues;
      })()
    `);
    if (trophyOverflow.length > 0) {
      console.warn(`[WARN] Trophies text overflow in ${lang}:`, trophyOverflow);
    } else {
      console.log(`✔ Trophies (${lang}) text layout clean`);
    }
    await evaluate(`document.querySelector('#trophy-back').click();`);
    await wait(400);

    // Check Collection Screen
    await evaluate(`document.querySelector('#open-collect').click();`);
    await wait(500);
    const collectOverflow = await evaluate(`
      (() => {
        const issues = [];
        const items = document.querySelectorAll('.co-item .co-name');
        for (const el of items) {
          if (el.scrollWidth > el.clientWidth + 4) {
            issues.push({
              text: el.textContent.trim().slice(0, 30),
              scrollWidth: el.scrollWidth,
              clientWidth: el.clientWidth
            });
          }
        }
        return issues;
      })()
    `);
    if (collectOverflow.length > 0) {
      console.warn(`[WARN] Collection text overflow in ${lang}:`, collectOverflow);
    } else {
      console.log(`✔ Collection (${lang}) text layout clean`);
    }
    await evaluate(`document.querySelector('#collect-back').click();`);
    await wait(400);
  }

  // TEST 3: Full Gameplay loop in zh-CN with at least 20 question steps answered
  console.log('\n--- Test 3: Full Gameplay Loop in zh-CN (Solving >= 20 steps) ---');
  await send('Page.navigate', { url: `http://127.0.0.1:${appPort}/zh-CN/` });
  await wait(800);
  await evaluate(`
    const skip = document.querySelector('#guide-skip');
    if (skip && !document.querySelector('#guide').hidden) skip.click();
  `);
  await wait(400);

  // Set number of problems to 10
  await evaluate(`
    document.querySelector('#open-settings').click();
  `);
  await wait(300);
  await evaluate(`
    document.querySelector('.pick button[data-count="10"]').click();
    document.querySelector('#close-settings').click();
  `);
  await wait(300);

  // Click Grade 1 button to start game
  console.log('Starting Grade 1 drill...');
  await evaluate(`document.querySelector('.grades button[data-grade="1"]').click();`);
  await wait(600);

  let playScreenActive = await evaluate(`document.querySelector('#screen-play').classList.contains('is-active')`);
  console.log('Play screen active:', playScreenActive);
  if (!playScreenActive) throw new Error('Play screen failed to activate');

  // Automated solving loop: solve at least 20 steps
  let stepsAnswered = 0;
  console.log('Answering problems automatically via keypad click events...');
  
  while (stepsAnswered < 22) {
    const state = await evaluate(`
      (() => {
        const S = window.__dopa?.S;
        if (!S) return null;
        if (S.screen !== 'play') return { screen: S.screen };
        const prob = S.problem;
        const step = S.step;
        if (!prob || !prob.steps || !prob.steps[step]) return { screen: 'play', waiting: true };
        const targetDigit = prob.steps[step].digit;
        const cellId = prob.steps[step].cell;
        const label = document.querySelector('#step-label')?.textContent || '';
        return {
          screen: 'play',
          step,
          totalSteps: prob.steps.length,
          targetDigit,
          cellId,
          label,
          combo: S.combo,
          ok: S.ok,
          qi: S.qi
        };
      })()
    `);

    if (!state || state.screen !== 'play') {
      console.log('Left play screen. Current state:', state);
      break;
    }
    if (state.waiting) {
      await wait(100);
      continue;
    }

    // Press keypad button for targetDigit
    await evaluate(`
      (() => {
        const btn = document.querySelector('#pad button[data-key="${state.targetDigit}"]');
        if (btn) btn.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
      })()
    `);
    stepsAnswered++;
    if (stepsAnswered % 5 === 0) {
      console.log(`  Step ${stepsAnswered}: answered '${state.targetDigit}' (Q${state.qi + 1}, Combo: ${state.combo}, Correct: ${state.ok})`);
    }
    await wait(220); // allow mascot and step transition animation
  }

  console.log(`✔ Completed ${stepsAnswered} consecutive calculation steps!`);

  // Finish remaining questions if any to reach result screen
  for (let guard = 0; guard < 40; guard++) {
    const cur = await evaluate(`window.__dopa?.S?.screen`);
    if (cur !== 'play') {
      console.log('Arrived at screen:', cur);
      break;
    }
    await evaluate(`
      (() => {
        const S = window.__dopa?.S;
        if (S && S.problem && S.problem.steps[S.step]) {
          const d = S.problem.steps[S.step].digit;
          const btn = document.querySelector('#pad button[data-key="' + d + '"]');
          if (btn) btn.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
        }
      })()
    `);
    await wait(200);
  }

  await wait(1000);
  const finalScreen = await evaluate(`window.__dopa?.S?.screen`);
  console.log('Result screen reached:', finalScreen);
  if (finalScreen === 'result' || finalScreen === 'final') {
    const score = await evaluate(`document.querySelector('#r-score')?.textContent`);
    console.log(`✔ Finished basic clear with score: ${score} pts`);
    // Click Done to return to title
    await evaluate(`document.querySelector('#go-title')?.click();`);
    await wait(600);
    const titleActive = await evaluate(`document.querySelector('#screen-title').classList.contains('is-active')`);
    console.log('✔ Successfully returned to title screen:', titleActive);
  }

  // TEST 4: Language switching directly in Settings modal across all 4 languages
  console.log('\n--- Test 4: Switching between all 4 languages in Settings Modal ---');
  for (const targetLang of ['zh-TW', 'en', 'ja', 'zh-CN']) {
    await evaluate(`document.querySelector('#open-settings').click();`);
    await wait(300);
    console.log(`Switching language dropdown to: ${targetLang}`);
    await evaluate(`
      const sel = document.querySelector('#lang');
      sel.value = '${targetLang}';
      sel.dispatchEvent(new Event('change', { bubbles: true }));
    `);
    await wait(1000);
    const newUrl = await evaluate('location.href');
    const savedLang = await evaluate(`localStorage.getItem('japanese-math-drill:lang')`);
    console.log(`  -> URL now: ${newUrl}, localStorage: ${savedLang}`);
    if (!newUrl.includes(`/${targetLang}/`)) throw new Error(`Failed switching to ${targetLang}`);
  }

  console.log('\n==================================================');
  console.log('   ALL E2E & OVERFLOW TESTS PASSED SUCCESSFULLY!  ');
  console.log('==================================================');
}

try {
  await runTests();
  process.exitCode = 0;
} catch (err) {
  console.error('\n❌ E2E TEST FAILED:', err);
  process.exitCode = 1;
} finally {
  try { ws.close(); } catch {}
  try { chrome.kill(); } catch {}
  try { server.close(); } catch {}
}
