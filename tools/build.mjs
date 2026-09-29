import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const SRC = path.resolve('src');
const DIST = path.resolve('app');

console.log('[BUILD] Starting build pipeline: src/ -> app/');

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      const ext = path.extname(entry.name);
      if (ext === '.css') {
        execSync(`npx esbuild "${srcPath}" --minify --outfile="${destPath}"`);
      } else if (ext === '.js') {
        execSync(`npx esbuild "${srcPath}" --minify --outfile="${destPath}"`);
      } else {
        fs.copyFileSync(srcPath, destPath);
      }
    }
  }
}

copyDir(SRC, DIST);

console.log('[BUILD] Build complete! All CSS and JS minified into app/.');
