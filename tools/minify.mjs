import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const LANGUAGES = ['zh-CN', 'zh-TW', 'en', 'ja'];

for (const lang of LANGUAGES) {
  const dir = path.resolve('app', lang);
  const cssFile = path.join(dir, 'style.css');
  if (fs.existsSync(cssFile)) {
    execSync(`npx esbuild "${cssFile}" --minify --allow-overwrite --outfile="${cssFile}"`);
    console.log(`Minified ${lang}/style.css`);
  }
  
  const jsDir = path.join(dir, 'js');
  if (fs.existsSync(jsDir)) {
    for (const jsFile of fs.readdirSync(jsDir)) {
      if (jsFile.endsWith('.js')) {
        const fullPath = path.join(jsDir, jsFile);
        execSync(`npx esbuild "${fullPath}" --minify --allow-overwrite --outfile="${fullPath}"`);
      }
    }
    console.log(`Minified all JS in ${lang}/js/`);
  }
}
console.log('All CSS and JS files minified successfully!');
