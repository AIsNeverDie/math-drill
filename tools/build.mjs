import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const LOCALES = ['en', 'ja', 'zh-CN', 'zh-TW'];
const SRC = path.resolve('src');
const CORE = path.join(SRC, 'core');
const DIST = path.resolve('app');
const TEMP_DIR = path.resolve('.build_temp');

const CORE_JS_FILES = [
  'audio.js','bg.js','core.js','dopakichi.js','fx.js','growth.js','guide.js',
  'main.js','problems.js','quests.js','scoring.js','session.js','skills.js',
  'store.js','trophies.js','unlocks.js'
];

console.log('[BUILD] Starting build...');
fs.mkdirSync(DIST, { recursive: true });
fs.mkdirSync(TEMP_DIR, { recursive: true });

// Copy root-level assets
if (fs.existsSync(path.join(SRC, 'index.html'))) {
  fs.copyFileSync(path.join(SRC, 'index.html'), path.join(DIST, 'index.html'));
}
if (fs.existsSync(path.join(SRC, '_headers'))) {
  fs.copyFileSync(path.join(SRC, '_headers'), path.join(DIST, '_headers'));
}
if (fs.existsSync(path.join(CORE, 'img'))) {
  fs.cpSync(path.join(CORE, 'img'), path.join(DIST, 'img'), { recursive: true });
}

const HTML_LOCALES_FILE = path.resolve('tools', 'html_locales.json');
const HTML_LOCALES = fs.existsSync(HTML_LOCALES_FILE)
  ? JSON.parse(fs.readFileSync(HTML_LOCALES_FILE, 'utf8'))
  : {};

for (const lang of LOCALES) {
  const localeFile = path.join(SRC, 'locales', `${lang}.json`);
  const localeData = JSON.parse(fs.readFileSync(localeFile, 'utf8'));
  
  // Inject localeData as i18n
  const i18nStr = JSON.stringify(localeData);
  const localeDir = path.join(SRC, 'locales', lang);

  const destDir = path.join(DIST, lang);
  const tempLangDir = path.join(TEMP_DIR, lang);
  fs.mkdirSync(destDir, { recursive: true });
  fs.mkdirSync(path.join(tempLangDir, 'js'), { recursive: true });
  
  const coreDir = path.join(CORE);
  if (fs.existsSync(path.join(coreDir, 'fonts'))) {
    const fontsDestDir = path.join(destDir, 'fonts');
    fs.mkdirSync(fontsDestDir, { recursive: true });
    const fonts = fs.readdirSync(path.join(coreDir, 'fonts'));
    for (const f of fonts) {
      if (lang.startsWith('zh') && f.includes('zen-maru')) continue;
      if ((lang === 'ja' || lang === 'en') && f.includes('chunky-fallback')) continue;
      fs.copyFileSync(path.join(coreDir, 'fonts', f), path.join(fontsDestDir, f));
    }
  }
  
  if (fs.existsSync(path.join(coreDir, 'icon.svg'))) {
    fs.copyFileSync(path.join(coreDir, 'icon.svg'), path.join(destDir, 'icon.svg'));
  }

  if (fs.existsSync(path.join(coreDir, 'img'))) {
    fs.cpSync(path.join(coreDir, 'img'), path.join(destDir, 'img'), { recursive: true });
  }
  
  // index.html: generate from core/index.html using locale html replacements (or file override if present)
  const langHtmlPath = path.join(localeDir, 'index.html');
  let htmlContent;
  if (fs.existsSync(langHtmlPath)) {
    htmlContent = fs.readFileSync(langHtmlPath, 'utf8');
  } else {
    htmlContent = fs.readFileSync(path.join(CORE, 'index.html'), 'utf8');
    const htmlReplacements = HTML_LOCALES[lang] || localeData.html;
    if (htmlReplacements) {
      for (const [target, rep] of Object.entries(htmlReplacements)) {
        if (rep === '__NO_LOGO_PRE__') {
          htmlContent = htmlContent.replace('        ' + target + '\n', '');
          htmlContent = htmlContent.replace(target, '');
        } else {
          htmlContent = htmlContent.replace(target, rep);
        }
      }
    }
  }
  fs.writeFileSync(path.join(destDir, 'index.html'), htmlContent);
  
  // style.css: check src/locales/${lang}/style.css, else src/core/css/style.css
  const langCssPath = path.join(localeDir, 'style.css');
  const cssContent = fs.existsSync(langCssPath)
    ? fs.readFileSync(langCssPath, 'utf8')
    : fs.readFileSync(path.join(CORE, 'css', 'style.css'), 'utf8');
  const tempCss = path.join(tempLangDir, 'style.css');
  fs.writeFileSync(tempCss, cssContent);
  const destCss = path.join(destDir, 'style.css');
  execSync(`npx esbuild "${tempCss}" --minify --outfile="${destCss}"`);
  
  const jsDir = path.join(destDir, 'js');
  fs.mkdirSync(jsDir, { recursive: true });
  
  for (const jsFile of CORE_JS_FILES) {
    let content;
    const langJsPath = path.join(localeDir, jsFile);
    if (fs.existsSync(langJsPath)) {
      content = fs.readFileSync(langJsPath, 'utf8');
    } else {
      content = fs.readFileSync(path.join(CORE, 'js', jsFile), 'utf8');
      if (content.includes('__I18N__')) {
        content = content.replace('__I18N__', () => i18nStr);
      }
    }
    const tempJs = path.join(tempLangDir, 'js', jsFile);
    const destJs = path.join(jsDir, jsFile);
    fs.writeFileSync(tempJs, content);
    execSync(`npx esbuild "${tempJs}" --minify --charset=utf8 --outfile="${destJs}"`);
  }
  
  console.log(`[BUILD] Successfully compiled locale: ${lang} -> app/${lang}/`);
}

fs.rmSync(TEMP_DIR, { recursive: true, force: true });
console.log('[BUILD] Build complete!');
