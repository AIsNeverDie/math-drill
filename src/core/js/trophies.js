// Trophies (id036): many small achievements, like the ones in mobile games.
// Each series is one measure with rising steps; every step is a trophy.
// Days and streaks get dense steps; volume series get wide ones so long
// sessions are not pushed too hard (docs/SPEC.md 14.7). Nothing is
// random, conditions are always shown (except a few secrets), and a trophy,
// once earned, is kept.
import { SKILLS, LANES } from './skills.js';
import { isUnlocked, isMastered, starsOf } from './session.js';

const T = __I18N__;

export const CATS = T.trophy_cats || ['Keep it up', 'Hard work', 'Skills', 'Growth', 'Extra', 'Combo', 'Accuracy', 'Dopa', 'Review', 'Grades', 'Collection', 'Secret'];

const fmt = (n) => n.toLocaleString('en-US');
// English only: "1 sticker", "7 stickers"; "once", "twice", "3 times".
const nOf = (n, one, many = `${one}s`) => `${fmt(n)} ${n === 1 ? one : many}`;
const times = (n) => (n === 1 ? 'once' : n === 2 ? 'twice' : `${fmt(n)} times`);
const DOPA_LABEL = { 2: '100', 3: '1,000', 4: '10,000', 5: '100,000', 6: '1 million', 7: '10 million', 8: '100 million', 9: '1 billion' };
const RANKS = ['bronze', 'silver', 'gold', 'rainbow'];
export const RANK_NAME = T.trophy_rank_name || { bronze: 'Bronze', silver: 'Silver', gold: 'Gold', rainbow: 'Rainbow', secret: 'Secret' };

// Rank by position in its series: first ~30% bronze, then silver, gold, and the last step rainbow.
function rankAt(i, n) {
  if (n === 1) return 'gold';
  if (i === n - 1) return 'rainbow';
  return RANKS[Math.min(2, Math.floor((i / (n - 1)) * 3.3))];
}

// A series: { key, cat, title, metric, steps, name(v), desc(v) } or explicit items.
const SERIES_DEFS = [
  { key: 'streak', cat: 'Keep it up', title: 'Play days in a row', metric: 'bestStreak', steps: [3, 5, 7, 10, 14, 21, 30, 50, 75, 100, 150, 200, 365], name: (v) => `${v}-day streak`, desc: (v) => `Play ${v} days in a row` },
  { key: 'days', cat: 'Keep it up', title: 'Days played', metric: 'days', steps: [1, 3, 5, 7, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 300, 365, 500, 730, 1000], name: (v) => v === 1 ? 'First day' : `${fmt(v)} days played`, desc: (v) => v === 1 ? 'Play for the first time' : `Play on ${fmt(v)} different days` },
  { key: 'stickers', cat: 'Keep it up', title: 'Login stickers', metric: 'stickers', steps: [1, 7, 14, 30, 50, 100, 200, 365], name: (v) => nOf(v, 'sticker'), desc: (v) => `Collect ${nOf(v, 'login bonus sticker')}` },
  { key: 'crowns', cat: 'Keep it up', title: 'Crown stickers', metric: 'crowns', steps: [1, 3, 5, 10, 20, 52], name: (v) => nOf(v, 'crown'), desc: (v) => `Collect ${nOf(v, 'day-7 crown sticker')}` },
  { key: 'problems', cat: 'Hard work', title: 'Problems solved', metric: 'problems', steps: [10, 30, 50, 100, 200, 300, 500, 750, 1000, 1500, 2000, 3000, 5000, 7500, 10000, 20000, 30000, 50000, 100000], name: (v) => `Solve ${fmt(v)}`, desc: (v) => `Solve ${fmt(v)} problems in all` },
  { key: 'cells', cat: 'Hard work', title: 'Digits entered', metric: 'cells', steps: [100, 500, 1000, 3000, 5000, 10000, 30000, 50000, 100000, 300000], name: (v) => `${fmt(v)} digits`, desc: (v) => `Enter ${fmt(v)} correct digits in all` },
  { key: 'plays', cat: 'Hard work', title: 'Times played', metric: 'plays', steps: [1, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000, 2000], name: (v) => v === 1 ? 'First play' : `Play ${fmt(v)} times`, desc: (v) => `Finish ${nOf(v, 'drill')} all the way through` },
  { key: 'minutes', cat: 'Hard work', title: 'Time played', metric: 'minutes', steps: [10, 30, 60, 120, 300, 600, 1200, 3000], name: (v) => `${v >= 60 ? nOf(v / 60, 'hour') : `${v} minutes`} in all`, desc: (v) => `Play for ${v >= 60 ? nOf(v / 60, 'hour') : `${v} minutes`} in all` },
  { key: 'unlocked', cat: 'Skills', title: 'Skills unlocked', metric: 'unlocked', steps: [3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 58], name: (v) => `Unlock ${v}`, desc: (v) => `Unlock ${v} skills` },
  { key: 'mastered', cat: 'Skills', title: 'Skills mastered', metric: 'mastered', steps: [1, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 58], name: (v) => `Master ${v}`, desc: (v) => `Master ${nOf(v, 'skill')}` },
  { key: 'gradeDone', cat: 'Skills', title: 'Master a whole grade', items: [1, 2, 3, 4, 5, 6].map((g) => ({ id: `gradeDone-${g}`, metric: `gradeDone${g}`, need: 1, name: `Grade ${g} mastered`, desc: `Master every Grade ${g} skill` })) },
  { key: 'laneDone', cat: 'Skills', title: 'Master a whole branch', items: LANES.map((l, i) => ({ id: `laneDone-${i}`, metric: `laneDone${i}`, need: 1, name: `${l}: all mastered`, desc: `Master every skill in "${l}"` })) },
  { key: 'extras', cat: 'Extra', title: 'Reach Extra', metric: 'extras', steps: [1, 3, 5, 10, 20, 30, 50, 100, 200, 300], name: (v) => v === 1 ? 'First Extra' : `Extra ${fmt(v)} times`, desc: (v) => `Reach Extra ${times(v)}` },
  { key: 'extraBest', cat: 'Extra', title: 'Best single Extra', metric: 'extraBest', steps: [3, 5, 7, 10, 12, 15, 18, 20, 23, 25, 30], name: (v) => `${v} in one Extra`, desc: (v) => `Solve ${v} problems in one Extra` },
  { key: 'extraSolved', cat: 'Extra', title: 'Solved in Extra', metric: 'extraSolved', steps: [10, 30, 50, 100, 200, 300, 500, 1000, 2000, 3000], name: (v) => `${fmt(v)} Extra problems`, desc: (v) => `Solve ${fmt(v)} problems in Extra in all` },
  { key: 'combo', cat: 'Combo', title: 'Combo', metric: 'maxCombo', steps: [5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 300], name: (v) => `${v} combo`, desc: (v) => `Get a ${v} combo` },
  { key: 'perfects', cat: 'Accuracy', title: 'Flawless finish', metric: 'perfects', steps: [1, 3, 5, 10, 20, 30, 50, 100, 200, 300], name: (v) => nOf(v, 'flawless run'), desc: (v) => `Finish a drill with a 100% first-try rate ${times(v)}` },
  { key: 'firstTry', cat: 'Accuracy', title: 'Right on the first try', metric: 'firstTry', steps: [10, 50, 100, 300, 500, 1000, 3000, 5000, 10000, 30000], name: (v) => `${fmt(v)} first tries`, desc: (v) => `Get ${fmt(v)} problems right on the first try` },
  { key: 'dopa', cat: 'Dopa', title: 'Dopa', metric: 'bestDopaL', steps: [2, 3, 4, 5, 6, 7, 8, 9], name: (v) => `${DOPA_LABEL[v]} Dopa`, desc: (v) => `Pass ${DOPA_LABEL[v]} Dopa in one play` },
  { key: 'review', cat: 'Review', title: 'Review', metric: 'reviewSolved', steps: [1, 5, 10, 30, 50, 100, 200, 300], name: (v) => `Review ${v}`, desc: (v) => `Redo ${nOf(v, 'missed problem')}` },
  ...[1, 2, 3, 4, 5, 6].map((g) => ({ key: `grade${g}`, cat: 'Grades', title: `Play Grade ${g}`, metric: `gradePlays${g}`, steps: [1, 10, 30], name: (v) => `Grade ${g}: ${nOf(v, 'play')}`, desc: (v) => `Play "Grade ${g}" ${times(v)}` })),
  { key: 'secret', cat: 'Secret', title: 'Secret', items: [
    { id: 'secret-perfect14', metric: 'flag:perfect14', need: 1, name: 'Perfect 14', desc: 'Solve all 14 problems with zero oops', secret: true },
    { id: 'secret-extraClean', metric: 'flag:extraClean', need: 1, name: 'Clean Extra', desc: 'Solve 5 or more in Extra with zero oops', secret: true },
    { id: 'secret-sunday', metric: 'flag:sunday', need: 1, name: 'Sunday math', desc: 'Play on a Sunday', secret: true },
    { id: 'secret-newyear', metric: 'flag:newyear', need: 1, name: 'New Year drill', desc: 'Play on January 1', secret: true },
    { id: 'secret-comeback', metric: 'flag:comeback', need: 1, name: 'Welcome back!', desc: 'Play again after a week or more away', secret: true },
    { id: 'secret-allmodes', metric: 'allModes', need: 1, name: 'Every way to play', desc: 'Play My Level, a Grade drill, Practice and Review', secret: true },
  ] },
];

// Other features add their own series (id045). Keep this list append-only.
export const SERIES = [];
export const TROPHIES = [];
const DOPA_UNIT = {
  ja: { 2: '100', 3: '1000', 4: '1万', 5: '10万', 6: '100万', 7: '1000万', 8: '1億', 9: '10億' },
  'zh-CN': { 2: '100', 3: '1000', 4: '1万', 5: '10万', 6: '100万', 7: '1000万', 8: '1亿', 9: '10亿' },
  'zh-TW': { 2: '100', 3: '1000', 4: '1萬', 5: '10萬', 6: '100萬', 7: '1000萬', 8: '1億', 9: '10億' },
};

const formatNum = (n) => {
  const wan = T.lang === 'zh-TW' ? '萬' : '万';
  if (n === 10000) return '1' + wan;
  if (n === 20000) return '2' + wan;
  if (n === 30000) return '3' + wan;
  if (n === 50000) return '5' + wan;
  if (n === 100000) return '10' + wan;
  if (n === 300000) return '30' + wan;
  if (n >= 1000) return n.toLocaleString('en-US');
  return String(n);
};

const formatTime = (v) => {
  if (T.lang === 'ja') return v < 60 ? `${v}ふん` : `${Math.floor(v / 60)}時間`;
  if (T.lang === 'zh-TW') return v < 60 ? `${v} 分鐘` : `${Math.floor(v / 60)} 小時`;
  if (T.lang === 'zh-CN') return v < 60 ? `${v} 分钟` : `${Math.floor(v / 60)} 小时`;
  return v >= 60 ? nOf(v / 60, 'hour') : `${v} minutes`;
};

export const TROPHY = {};
export function addSeries(def) {
  const sConf = (T.series && T.series[def.key]) || {};
  const sTitle = sConf.title || def.title;
  const sCat = sConf.cat || def.cat;

  const items = def.items
    ? def.items.map((it, i, a) => {
        let name = it.name;
        let desc = it.desc;
        if (sConf.name) {
          if (def.key === 'gradeDone' || def.key === 'gradeStar3') {
            const g = i + 1;
            name = sConf.name.replace('{g}', g);
            desc = sConf.desc ? sConf.desc.replace('{g}', g) : desc;
          } else if (def.key === 'laneDone') {
            const laneName = (T.lanes && T.lanes[i]) || LANES[i];
            name = sConf.name.replace('{l}', laneName);
            desc = sConf.desc ? sConf.desc.replace('{l}', laneName) : desc;
          }
        }
        return { rank: it.secret ? 'secret' : rankAt(i, a.length), ...it, name, desc };
      })
    : def.steps.map((v, i, a) => {
        let name = def.name(v);
        let desc = def.desc(v);
        if (def.key === 'minutes' && sConf.name) {
          const tStr = formatTime(v);
          name = sConf.name.replace('{time}', tStr);
          if (sConf.desc) desc = sConf.desc.replace('{time}', tStr);
        } else if (def.key === 'dopa' && sConf.name) {
          const dVal = (DOPA_UNIT[T.lang] && DOPA_UNIT[T.lang][v]) || DOPA_LABEL[v];
          name = sConf.name.replace('{n}', dVal);
          if (sConf.desc) desc = sConf.desc.replace('{n}', dVal);
        } else if (def.key === 'hammer' && v === 1 && sConf.first_name) {
          name = sConf.first_name;
          if (sConf.desc) desc = sConf.desc.replace('{n}', formatNum(v));
        } else if (sConf.name) {
          name = sConf.name.replace('{n}', formatNum(v));
          if (sConf.desc) desc = sConf.desc.replace('{n}', formatNum(v));
        }
        return { id: `${def.key}-${v}`, metric: def.metric, need: v, name, desc, rank: rankAt(i, a.length) };
      });
  
  // Specific item overrides (e.g. secret achievements)
  items.forEach(it => {
    if (T.trophies && T.trophies[it.id]) {
      it.name = T.trophies[it.id].name || it.name;
      it.desc = T.trophies[it.id].desc || it.desc;
    }
  });

  const series = { key: def.key, cat: sCat, title: sTitle, items: items.map((it) => ({ ...it, series: def.key, cat: sCat, reward: it.reward || null })) };
  SERIES.push(series);
  for (const it of series.items) { TROPHIES.push(it); TROPHY[it.id] = it; }
  return series;
}
SERIES_DEFS.forEach(addSeries);

// id045: the features added after id036 (stars, quests, hammer, rust,
// time capsule, "You improved!", collection).
[
  { key: 'questDays', cat: 'Keep it up', title: 'Quests complete', metric: 'questDays', steps: [1, 3, 7, 14, 30, 50, 100, 200, 365], name: (v) => nOf(v, 'quest day'), desc: (v) => `Clear all of the day's quests on ${nOf(v, 'day')}` },
  { key: 'questRun', cat: 'Keep it up', title: 'Quest streak', metric: 'questRun', steps: [2, 3, 5, 7, 14, 30], name: (v) => `${v}-day quest streak`, desc: (v) => `Clear all quests ${v} days in a row` },
  { key: 'hammer', cat: 'Keep it up', title: 'Streak Hammer', metric: 'hammerUsed', steps: [1, 3, 10], name: (v) => v === 1 ? 'First save' : `${v} saves`, desc: (v) => `Use the Streak Hammer ${times(v)}` },
  { key: 'starsTotal', cat: 'Skills', title: 'Stars', metric: 'starsTotal', steps: [5, 10, 25, 50, 75, 100, 150, 200, 250, 290], name: (v) => `${v} stars`, desc: (v) => `Collect ${v} skill stars in all` },
  { key: 'star5', cat: 'Skills', title: '☆5 skills', metric: 'star5', steps: [1, 3, 5, 10, 20, 30, 58], name: (v) => v === 1 ? 'First ☆5 skill' : `${v} ☆5 skills`, desc: (v) => `Get ${nOf(v, 'skill')} to ☆5` },
  { key: 'gradeStar3', cat: 'Skills', title: 'Whole grade at ☆3', items: [1, 2, 3, 4, 5, 6].map((g) => ({ id: `gradeStar3-${g}`, metric: `gradeStar3${g}`, need: 1, name: `Grade ${g} all ☆3`, desc: `Get every Grade ${g} skill to ☆3 or more` })) },
  { key: 'polished', cat: 'Growth', title: 'Polish off rust', metric: 'polished', steps: [1, 3, 5, 10, 30, 50], name: (v) => v === 1 ? 'Shiny!' : `Shiny ×${v}`, desc: (v) => `Polish a rusty skill ${times(v)}` },
  { key: 'capsules', cat: 'Growth', title: 'Time capsules', metric: 'capsules', steps: [1, 3, 5, 10, 30], name: (v) => nOf(v, 'capsule'), desc: (v) => `Open ${nOf(v, 'time capsule')}` },
  { key: 'capsuleFaster', cat: 'Growth', title: 'Faster than back then', metric: 'capsuleFaster', steps: [1, 5, 10], name: (v) => v === 1 ? 'Faster than then' : `Faster ×${v}`, desc: (v) => `Beat your old time in a time capsule ${times(v)}` },
  { key: 'grew', cat: 'Growth', title: 'You improved!', metric: 'grew', steps: [1, 5, 10, 30, 50, 100], name: (v) => v === 1 ? 'Improved!' : `Improved ×${v}`, desc: (v) => `See "You improved!" on the results ${times(v)}` },
  { key: 'items', cat: 'Collection', title: 'Collection', metric: 'itemsOwned', steps: [10, 20, 30, 40, 47], name: (v) => `${v} items`, desc: (v) => `Collect ${v} items` },
  { key: 'catComplete', cat: 'Collection', title: 'Full sets', metric: 'catComplete', steps: [1, 3, 5, 8], name: (v) => nOf(v, 'full set'), desc: (v) => `Collect everything in ${nOf(v, 'category', 'categories')}` },
].forEach(addSeries);

// Numbers every trophy is measured against, from the saved state.
// snap: { stats, prog, bestStreak, stickers, crowns, ...extra metrics }
export function trophyMetrics(snap) {
  const s = snap.stats || {};
  const prog = snap.prog || { skills: {} };
  const m = {
    bestStreak: snap.bestStreak || 0, days: s.days || 0, stickers: snap.stickers || 0, crowns: snap.crowns || 0,
    problems: s.problems || 0, cells: s.cells || 0, plays: s.plays || 0, minutes: Math.floor((s.playMs || 0) / 60000),
    unlocked: SKILLS.filter((x) => isUnlocked(prog, x.id)).length, mastered: SKILLS.filter((x) => isMastered(prog, x.id)).length,
    extras: s.extras || 0, extraBest: s.extraBest || 0, extraSolved: s.extraSolved || 0, maxCombo: s.maxCombo || 0,
    perfects: s.perfects || 0, firstTry: s.firstTry || 0, bestDopaL: Math.floor((s.bestDopaL || 0) + 1e-9), reviewSolved: s.reviewSolved || 0,
  };
  const stars = Object.fromEntries(SKILLS.map((x) => [x.id, starsOf(prog, x.id)]));
  m.starsTotal = Object.values(stars).reduce((a, b) => a + b, 0);
  m.star5 = Object.values(stars).filter((n) => n >= 5).length;
  m.polished = s.polished || 0; m.capsules = s.capsules || 0; m.capsuleFaster = s.capsuleFaster || 0; m.grew = s.grew || 0;
  for (let g = 1; g <= 6; g++) {
    m[`gradeStar3${g}`] = SKILLS.filter((x) => x.grade === g).every((x) => stars[x.id] >= 3) ? 1 : 0;
    m[`gradeDone${g}`] = SKILLS.filter((x) => x.grade === g).every((x) => isMastered(prog, x.id)) ? 1 : 0;
    m[`gradePlays${g}`] = (s.grades || {})[g] || 0;
  }
  LANES.forEach((_, i) => { m[`laneDone${i}`] = SKILLS.filter((x) => x.lane === i).every((x) => isMastered(prog, x.id)) ? 1 : 0; });
  for (const [k, v] of Object.entries(s.flags || {})) if (v) m[`flag:${k}`] = 1;
  const modes = s.modes || {};
  m.allModes = ['level', 'grade', 'practice', 'review'].every((k) => modes[k]) ? 1 : 0;
  Object.assign(m, snap.extra || {});
  return m;
}
export const valueOf = (m, metric) => m[metric] || 0;

// Earn every trophy whose condition is met. Returns the new ones (in list order).
// `state` is the saved { got: { id: time } }; the first call earns what the
// existing records already reach and marks them as a batch.
export function evaluate(state, metrics, at = Date.now()) {
  state.got = state.got || {};
  const fresh = [];
  for (const t of TROPHIES) {
    if (state.got[t.id]) continue;
    if (valueOf(metrics, t.metric) >= t.need) { state.got[t.id] = at; fresh.push(t); }
  }
  if (!state.init) { state.init = true; state.batch = fresh.map((t) => t.id); return []; }
  return fresh;
}

export const earnedCount = (state) => TROPHIES.filter((t) => state.got && state.got[t.id]).length;

// Progress of one series for the list screen.
export function seriesView(series, state, metrics) {
  const got = series.items.filter((t) => state.got && state.got[t.id]);
  const next = series.items.find((t) => !(state.got && state.got[t.id]));
  const top = got[got.length - 1] || null;
  return { series, got, next, top, value: next ? valueOf(metrics, next.metric) : null };
}
