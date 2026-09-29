import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import { fileURLToPath } from 'node:url';

const app = fileURLToPath(new URL('../app/', import.meta.url));
const root = readFileSync(new URL('../app/index.html', import.meta.url), 'utf8');
const redirect = root.match(/<script>([\s\S]*?)<\/script>/)?.[1];

test('root opens the saved language, with an explicit override and preserved URL state', () => {
  assert.ok(redirect);
  const nav = { languages: ['en-US'], language: 'en-US' };
  for (const [search, saved, hash, expected] of [
    ['', null, '', 'en/'],
    ['', 'ja', '', 'ja/'],
    ['', 'zh-CN', '', 'zh-CN/'],
    ['', 'zh-TW', '', 'zh-TW/'],
    ['?lang=en&from=home', 'ja', '#play', 'en/?from=home#play'],
    ['?lang=ja', 'en', '', 'ja/'],
    ['?lang=zh-CN', 'en', '', 'zh-CN/'],
    ['?lang=zh-TW', 'en', '', 'zh-TW/'],
  ]) {
    let destination;
    runInNewContext(redirect, {
      URLSearchParams,
      location: { search, hash, replace: (url) => { destination = url; } },
      localStorage: { getItem: () => saved },
      navigator: nav,
    });
    assert.equal(destination, expected);
  }
});

test('root defaults to English when browser storage is unavailable', () => {
  let destination;
  runInNewContext(redirect, {
    URLSearchParams,
    location: { search: '', hash: '', replace: (url) => { destination = url; } },
    localStorage: { getItem: () => { throw new Error('blocked'); } },
    navigator: { languages: ['en-US'], language: 'en-US' },
  });
  assert.equal(destination, 'en/');
});

test('root auto-detects browser language when no saved preference', () => {
  for (const [langs, expected] of [
    [['zh-TW', 'zh'], 'zh-TW/'],
    [['zh-HK'], 'zh-TW/'],
    [['zh-CN', 'zh'], 'zh-CN/'],
    [['zh'], 'zh-CN/'],
    [['ja-JP'], 'ja/'],
    [['fr-FR', 'en-US'], 'en/'],
    [['de-DE'], 'en/'],
  ]) {
    let destination;
    runInNewContext(redirect, {
      URLSearchParams,
      location: { search: '', hash: '', replace: (url) => { destination = url; } },
      localStorage: { getItem: () => null },
      navigator: { languages: langs, language: langs[0] },
    });
    assert.equal(destination, expected, `browser langs ${langs} → ${expected}`);
  }
});

test('all language routes include their own game assets', () => {
  for (const lang of ['en', 'ja', 'zh-CN', 'zh-TW']) {
    const html = readFileSync(`${app}${lang}/index.html`, 'utf8');
    for (const [, asset] of html.matchAll(/(?:href|src)="(icon\.svg|style\.css|js\/main\.js)(?:\?[^"]*)?"/g)) {
      assert.ok(existsSync(`${app}${lang}/${asset}`), `${lang}/${asset}`);
    }
  }
});
