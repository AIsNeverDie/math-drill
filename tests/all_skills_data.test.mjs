import test from 'node:test';
import assert from 'node:assert/strict';

for (const lang of ['en', 'ja', 'zh-CN', 'zh-TW']) {
  test(`skills integrity in ${lang}`, async () => {
    const { SKILLS, SKILL, DEPTH, LANES } = await import(`../app/${lang}/js/skills.js`);
    assert.equal(SKILLS.length, 58);
    assert.equal(LANES.length, 4);
    for (const s of SKILLS) {
      assert.ok(s.name, `Skill ${s.id} in ${lang} missing name`);
      assert.ok(s.name.length > 0);
      for (const r of s.req) assert.ok(SKILL[r], `${s.id} needs ${r}`);
    }
  });
}
