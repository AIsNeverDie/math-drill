// Trophies (id036): many small achievements, like the ones in mobile games.
// Each series is one measure with rising steps; every step is a trophy.
// Days and streaks get dense steps; volume series get wide ones so long
// sessions are not pushed too hard (docs/SPEC.md 14.7). Nothing is
// random, conditions are always shown (except a few secrets), and a trophy,
// once earned, is kept.
import { SKILLS, LANES } from './skills.js';
import { isUnlocked, isMastered, starsOf } from './session.js';

export const CATS = ['堅持打卡', '勤学苦练', '技能掌握', '不断进步', '加分挑战', '連對连击', '正確率', '多帕能量', '错題複習', '年級通關', '圖鑑收藏', '隱藏成就'];

const fmt = (n) => (n >= 10000 && n % 10000 === 0 ? `${n / 10000}萬` : n.toLocaleString('zh-TW'));
const DOPA_LABEL = { 2: '100', 3: '1000', 4: '1萬', 5: '10萬', 6: '100萬', 7: '1000萬', 8: '1億', 9: '10億' };
const RANKS = ['bronze', 'silver', 'gold', 'rainbow'];
export const RANK_NAME = { bronze: '銅牌', silver: '銀牌', gold: '金牌', rainbow: '彩虹', secret: '隱藏' };

// Rank by position in its series: first ~30% bronze, then silver, gold, and the last step rainbow.
function rankAt(i, n) {
  if (n === 1) return 'gold';
  if (i === n - 1) return 'rainbow';
  return RANKS[Math.min(2, Math.floor((i / (n - 1)) * 3.3))];
}

// A series: { key, cat, title, metric, steps, name(v), desc(v) } or explicit items.
const SERIES_DEFS = [
  { key: 'streak', cat: '堅持打卡', title: '連續練習天數', metric: 'bestStreak', steps: [3, 5, 7, 10, 14, 21, 30, 50, 75, 100, 150, 200, 365], name: (v) => `連續 ${v} 天`, desc: (v) => `連續 ${v} 天堅持練習` },
  { key: 'days', cat: '堅持打卡', title: '累計打卡天數', metric: 'days', steps: [1, 3, 5, 7, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 300, 365, 500, 730, 1000], name: (v) => `打卡 ${fmt(v)} 天`, desc: (v) => `累計練習达到 ${fmt(v)} 天` },
  { key: 'stickers', cat: '堅持打卡', title: '登入簽到印章', metric: 'stickers', steps: [1, 7, 14, 30, 50, 100, 200, 365], name: (v) => `印章 ${v} 枚`, desc: (v) => `累計收集 ${v} 枚登入簽到印章` },
  { key: 'crowns', cat: '堅持打卡', title: '皇冠印章', metric: 'crowns', steps: [1, 3, 5, 10, 20, 52], name: (v) => `皇冠 ${v} 枚`, desc: (v) => `累計获得第 7 天的皇冠印章 ${v} 枚` },
  { key: 'problems', cat: '勤学苦练', title: '做題總數', metric: 'problems', steps: [10, 30, 50, 100, 200, 300, 500, 750, 1000, 1500, 2000, 3000, 5000, 7500, 10000, 20000, 30000, 50000, 100000], name: (v) => `答對 ${fmt(v)} 題`, desc: (v) => `累計答對 ${fmt(v)} 道算術題` },
  { key: 'cells', cat: '勤学苦练', title: '輸入数字位數', metric: 'cells', steps: [100, 500, 1000, 3000, 5000, 10000, 30000, 50000, 100000, 300000], name: (v) => `輸入 ${fmt(v)} 位數`, desc: (v) => `累計填入 ${fmt(v)} 位正确数字` },
  { key: 'plays', cat: '勤学苦练', title: '練習輪数', metric: 'plays', steps: [1, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000, 2000], name: (v) => `完成 ${fmt(v)} 輪`, desc: (v) => `累計完成 ${fmt(v)} 輪練習` },
  { key: 'minutes', cat: '勤学苦练', title: '累計專注時長', metric: 'minutes', steps: [10, 30, 60, 120, 300, 600, 1200, 3000], name: (v) => (v >= 60 ? `累計 ${v / 60} 小時` : `累計 ${v} 分鐘`), desc: (v) => `累計專注練習 ${v >= 60 ? `${v / 60} 小時` : `${v} 分鐘`}` },
  { key: 'unlocked', cat: '技能掌握', title: '解鎖新技能', metric: 'unlocked', steps: [3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 58], name: (v) => `解鎖 ${v} 項`, desc: (v) => `在技能树中解鎖 ${v} 項技能` },
  { key: 'mastered', cat: '技能掌握', title: '精通掌握技能', metric: 'mastered', steps: [1, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 58], name: (v) => `精通 ${v} 項`, desc: (v) => `掌握并精通 ${v} 項數學技能` },
  { key: 'gradeDone', cat: '技能掌握', title: '通關整個年級', items: [1, 2, 3, 4, 5, 6].map((g) => ({ id: `gradeDone-${g}`, metric: `gradeDone${g}`, need: 1, name: `${g}年級全部掌握`, desc: `掌握 ${g} 年級的所有计算技能` })) },
  { key: 'laneDone', cat: '技能掌握', title: '精通整個计算分支', items: LANES.map((l, i) => ({ id: `laneDone-${i}`, metric: `laneDone${i}`, need: 1, name: `${l} 全部掌握`, desc: `掌握「${l}」分支下的全部技能` })) },
  { key: 'extras', cat: '加分挑战', title: '進入加時賽', metric: 'extras', steps: [1, 3, 5, 10, 20, 30, 50, 100, 200, 300], name: (v) => `加時賽 ${v} 次`, desc: (v) => `成功進入加時賽 ${v} 次` },
  { key: 'extraBest', cat: '加分挑战', title: '單次加時賽最高紀錄', metric: 'extraBest', steps: [3, 5, 7, 10, 12, 15, 18, 20, 23, 25, 30], name: (v) => `單次 ${v} 題`, desc: (v) => `在單次加時賽中答對 ${v} 題` },
  { key: 'extraSolved', cat: '加分挑战', title: '加時賽答對總數', metric: 'extraSolved', steps: [10, 30, 50, 100, 200, 300, 500, 1000, 2000, 3000], name: (v) => `加時賽答對 ${fmt(v)} 題`, desc: (v) => `在加時賽中累計答對 ${fmt(v)} 題` },
  { key: 'combo', cat: '連對连击', title: '連對紀錄', metric: 'maxCombo', steps: [5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 300], name: (v) => `${v} 連對`, desc: (v) => `達成 ${v} 連對` },
  { key: 'perfects', cat: '正確率', title: '完美无失誤完賽', metric: 'perfects', steps: [1, 3, 5, 10, 20, 30, 50, 100, 200, 300], name: (v) => `完美通關 ${v} 次`, desc: (v) => `以 100% 首次正确率完成 ${v} 輪練習` },
  { key: 'firstTry', cat: '正確率', title: '首次即答對', metric: 'firstTry', steps: [10, 50, 100, 300, 500, 1000, 3000, 5000, 10000, 30000], name: (v) => `首次答對 ${fmt(v)} 題`, desc: (v) => `一次作答就成功的題目达到 ${fmt(v)} 題` },
  { key: 'dopa', cat: '多帕能量', title: '多帕能量', metric: 'bestDopaL', steps: [2, 3, 4, 5, 6, 7, 8, 9], name: (v) => `${DOPA_LABEL[v]} 多帕`, desc: (v) => `单局多帕能量突破 ${DOPA_LABEL[v]}` },
  { key: 'review', cat: '错題複習', title: '错題複習', metric: 'reviewSolved', steps: [1, 5, 10, 30, 50, 100, 200, 300], name: (v) => `複習 ${v} 題`, desc: (v) => `重新攻克 ${v} 道错題` },
  ...[1, 2, 3, 4, 5, 6].map((g) => ({ key: `grade${g}`, cat: '年級通關', title: `練習${g}年級`, metric: `gradePlays${g}`, steps: [1, 10, 30], name: (v) => `${g} 年級 ${v} 輪`, desc: (v) => `完成 ${g} 年級模式練習 ${v} 次` })),
  { key: 'secret', cat: '隱藏成就', title: '隱藏成就', items: [
    { id: 'secret-perfect14', metric: 'flag:perfect14', need: 1, name: '14題全对大滿貫', desc: '在14題模式中0失誤完美過關', secret: true },
    { id: 'secret-extraClean', metric: 'flag:extraClean', need: 1, name: '加分挑戰零失誤', desc: '在 Extra 加分挑戰答對5題以上且0失誤', secret: true },
    { id: 'secret-sunday', metric: 'flag:sunday', need: 1, name: '週日不偷懶', desc: '在週日開啟數學練習', secret: true },
    { id: 'secret-newyear', metric: 'flag:newyear', need: 1, name: '新年第一練', desc: '在元旦（1月1日）練習數學', secret: true },
    { id: 'secret-comeback', metric: 'flag:comeback', need: 1, name: '歡迎回歸！', desc: '間隔一週以上再次回来練習', secret: true },
    { id: 'secret-allmodes', metric: 'allModes', need: 1, name: '全能小達人', desc: '完整體驗过我的等級、年級、专項練習与错題複習全部4种模式', secret: true },
  ] },
];

// Other features add their own series (id045). Keep this list append-only.
export const SERIES = [];
export const TROPHIES = [];
export const TROPHY = {};
export function addSeries(def) {
  const items = def.items
    ? def.items.map((it, i, a) => ({ rank: it.secret ? 'secret' : rankAt(i, a.length), ...it }))
    : def.steps.map((v, i, a) => ({ id: `${def.key}-${v}`, metric: def.metric, need: v, name: def.name(v), desc: def.desc(v), rank: rankAt(i, a.length) }));
  const series = { key: def.key, cat: def.cat, title: def.title, items: items.map((it) => ({ ...it, series: def.key, cat: def.cat, reward: it.reward || null })) };
  SERIES.push(series);
  for (const it of series.items) { TROPHIES.push(it); TROPHY[it.id] = it; }
  return series;
}
SERIES_DEFS.forEach(addSeries);

// id045: the features added after id036 (stars, quests, hammer, rust,
// time capsule, "のびたよ", collection).
[
  { key: 'questDays', cat: '堅持打卡', title: '每日任務全部達成', metric: 'questDays', steps: [1, 3, 7, 14, 30, 50, 100, 200, 365], name: (v) => `全通關 ${v} 天`, desc: (v) => `完成当天全部每日任務达到 ${v} 天` },
  { key: 'questRun', cat: '堅持打卡', title: '連續完成每日任務', metric: 'questRun', steps: [2, 3, 5, 7, 14, 30], name: (v) => `連續 ${v} 天全清`, desc: (v) => `連續 ${v} 天完成全部每日任務` },
  { key: 'hammer', cat: '堅持打卡', title: '打卡補簽锤', metric: 'hammerUsed', steps: [1, 3, 10], name: (v) => (v === 1 ? '初次補簽' : `補簽 ${v} 次`), desc: (v) => `使用打卡锤保住連續打卡 ${v} 次` },
  { key: 'starsTotal', cat: '技能掌握', title: '收集技能星星', metric: 'starsTotal', steps: [5, 10, 25, 50, 75, 100, 150, 200, 250, 290], name: (v) => `星星 ${v} 顆`, desc: (v) => `累計收集技能星星 ${v} 顆` },
  { key: 'star5', cat: '技能掌握', title: '升至 ☆5 的技能', metric: 'star5', steps: [1, 3, 5, 10, 20, 30, 58], name: (v) => `☆5技能 ${v} 個`, desc: (v) => `将 ${v} 個技能提升至 ☆5 滿星` },
  { key: 'gradeStar3', cat: '技能掌握', title: '整個年級达到 ☆3', items: [1, 2, 3, 4, 5, 6].map((g) => ({ id: `gradeStar3-${g}`, metric: `gradeStar3${g}`, need: 1, name: `${g}年級全員☆3`, desc: `将 ${g} 年級的所有技能都提升至 ☆3 以上` })) },
  { key: 'polished', cat: '不断进步', title: '温故知新除鏽', metric: 'polished', steps: [1, 3, 5, 10, 30, 50], name: (v) => `重新點亮 ${v} 次`, desc: (v) => `複習变生疏的技能使其重新閃亮 ${v} 次` },
  { key: 'capsules', cat: '不断进步', title: '時光膠囊', metric: 'capsules', steps: [1, 3, 5, 10, 30], name: (v) => `開啟胶囊 ${v} 次`, desc: (v) => `開啟 ${v} 次挑战过去的時光膠囊` },
  { key: 'capsuleFaster', cat: '不断进步', title: '超越过去的自己', metric: 'capsuleFaster', steps: [1, 5, 10], name: (v) => `超越以往 ${v} 次`, desc: (v) => `在時光膠囊中比最初挑战时更快答完（${v}次）` },
  { key: 'grew', cat: '不断进步', title: '你进步了！', metric: 'grew', steps: [1, 5, 10, 30, 50, 100], name: (v) => `进步 ${v} 次`, desc: (v) => `在结算页面获得「你进步了！」評價 ${v} 次` },
  { key: 'items', cat: '圖鑑收藏', title: '圖鑑收藏總數', metric: 'itemsOwned', steps: [10, 20, 30, 40, 47], name: (v) => `收集 ${v} 件`, desc: (v) => `在收藏馆累計解鎖 ${v} 件特效物品` },
  { key: 'catComplete', cat: '圖鑑收藏', title: '集齊整個分類', metric: 'catComplete', steps: [1, 3, 5, 8], name: (v) => `集齊 ${v} 個分類`, desc: (v) => `将收藏馆中 ${v} 個分類的物品全部集齊` },
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
