import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const LOCALES = ['en', 'ja', 'zh-CN', 'zh-TW'];
const SRC = path.resolve('src');
const DIST = path.resolve('app');

console.log('[BUILD] Starting i18n build pipeline: src/ -> app/');

// Ensure root files in app/
fs.mkdirSync(DIST, { recursive: true });
if (fs.existsSync(path.join(SRC, 'index.html'))) {
  fs.copyFileSync(path.join(SRC, 'index.html'), path.join(DIST, 'index.html'));
}
if (fs.existsSync(path.join(SRC, '_headers'))) {
  fs.copyFileSync(path.join(SRC, '_headers'), path.join(DIST, '_headers'));
}
if (fs.existsSync(path.join(SRC, 'img'))) {
  fs.cpSync(path.join(SRC, 'img'), path.join(DIST, 'img'), { recursive: true });
}

// Build each locale into app/${lang}
for (const lang of LOCALES) {
  const destDir = path.join(DIST, lang);
  fs.mkdirSync(destDir, { recursive: true });

  const srcLangDir = path.join(SRC, lang);
  if (!fs.existsSync(srcLangDir)) continue;

  // Process files inside src/${lang}
  function buildDir(sDir, dDir) {
    fs.mkdirSync(dDir, { recursive: true });
    for (const entry of fs.readdirSync(sDir, { withFileTypes: true })) {
      const sp = path.join(sDir, entry.name);
      const dp = path.join(dDir, entry.name);
      if (entry.isDirectory()) {
        buildDir(sp, dp);
      } else {
        const ext = path.extname(entry.name);
        if (ext === '.css' || ext === '.js') {
          execSync(`npx esbuild "${sp}" --minify --outfile="${dp}"`);
        } else {
          fs.copyFileSync(sp, dp);
        }
      }
    }
  }

  buildDir(srcLangDir, destDir);
  console.log(`[BUILD] Compiled locale ${lang} -> app/${lang}/`);
}

console.log('[BUILD] Build complete! All CSS and JS minified into app/.');
