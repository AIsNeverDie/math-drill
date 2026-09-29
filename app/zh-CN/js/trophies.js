// Trophies (id036): many small achievements, like the ones in mobile games.
// Each series is one measure with rising steps; every step is a trophy.
// Days and streaks get dense steps; volume series get wide ones so long
// sessions are not pushed too hard (docs/SPEC.md 14.7). Nothing is
// random, conditions are always shown (except a few secrets), and a trophy,
// once earned, is kept.
import { SKILLS, LANES } from './skills.js';
import { isUnlocked, isMastered, starsOf } from './session.js';

export const CATS = ['坚持打卡', '勤学苦练', '技能掌握', '不断进步', '加分挑战', '连对连击', '准确率', '多帕能量', '错题复习', '年级通关', '图鉴收藏', '隐藏成就'];

const fmt = (n) => (n >= 10000 && n % 10000 === 0 ? `${n / 10000}万` : n.toLocaleString('zh-CN'));
const DOPA_LABEL = { 2: '100', 3: '1000', 4: '1万', 5: '10万', 6: '100万', 7: '1000万', 8: '1亿', 9: '10亿' };
const RANKS = ['bronze', 'silver', 'gold', 'rainbow'];
export const RANK_NAME = { bronze: '铜牌', silver: '银牌', gold: '金牌', rainbow: '彩虹', secret: '隐藏' };

// Rank by position in its series: first ~30% bronze, then silver, gold, and the last step rainbow.
function rankAt(i, n) {
  if (n === 1) return 'gold';
  if (i === n - 1) return 'rainbow';
  return RANKS[Math.min(2, Math.floor((i / (n - 1)) * 3.3))];
}

// A series: { key, cat, title, metric, steps, name(v), desc(v) } or explicit items.
const SERIES_DEFS = [
  { key: 'streak', cat: '坚持打卡', title: '连续练习天数', metric: 'bestStreak', steps: [3, 5, 7, 10, 14, 21, 30, 50, 75, 100, 150, 200, 365], name: (v) => `连续 ${v} 天`, desc: (v) => `连续 ${v} 天坚持练习` },
  { key: 'days', cat: '坚持打卡', title: '累计打卡天数', metric: 'days', steps: [1, 3, 5, 7, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 300, 365, 500, 730, 1000], name: (v) => `打卡 ${fmt(v)} 天`, desc: (v) => `累计练习达到 ${fmt(v)} 天` },
  { key: 'stickers', cat: '坚持打卡', title: '登录签到印章', metric: 'stickers', steps: [1, 7, 14, 30, 50, 100, 200, 365], name: (v) => `印章 ${v} 枚`, desc: (v) => `累计收集 ${v} 枚登录签到印章` },
  { key: 'crowns', cat: '坚持打卡', title: '皇冠印章', metric: 'crowns', steps: [1, 3, 5, 10, 20, 52], name: (v) => `皇冠 ${v} 枚`, desc: (v) => `累计获得第 7 天的皇冠印章 ${v} 枚` },
  { key: 'problems', cat: '勤学苦练', title: '做题总数', metric: 'problems', steps: [10, 30, 50, 100, 200, 300, 500, 750, 1000, 1500, 2000, 3000, 5000, 7500, 10000, 20000, 30000, 50000, 100000], name: (v) => `做对 ${fmt(v)} 题`, desc: (v) => `累计做对 ${fmt(v)} 道算术题` },
  { key: 'cells', cat: '勤学苦练', title: '输入数字位数', metric: 'cells', steps: [100, 500, 1000, 3000, 5000, 10000, 30000, 50000, 100000, 300000], name: (v) => `输入 ${fmt(v)} 位数`, desc: (v) => `累计填入 ${fmt(v)} 位正确数字` },
  { key: 'plays', cat: '勤学苦练', title: '练习轮数', metric: 'plays', steps: [1, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000, 2000], name: (v) => `完成 ${fmt(v)} 轮`, desc: (v) => `累计完成 ${fmt(v)} 轮练习` },
  { key: 'minutes', cat: '勤学苦练', title: '累计专注时长', metric: 'minutes', steps: [10, 30, 60, 120, 300, 600, 1200, 3000], name: (v) => (v >= 60 ? `累计 ${v / 60} 小时` : `累计 ${v} 分钟`), desc: (v) => `累计专注练习 ${v >= 60 ? `${v / 60} 小时` : `${v} 分钟`}` },
  { key: 'unlocked', cat: '技能掌握', title: '解锁新技能', metric: 'unlocked', steps: [3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 58], name: (v) => `解锁 ${v} 项`, desc: (v) => `在技能树中解锁 ${v} 项技能` },
  { key: 'mastered', cat: '技能掌握', title: '精通掌握技能', metric: 'mastered', steps: [1, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 58], name: (v) => `精通 ${v} 项`, desc: (v) => `掌握并精通 ${v} 项数学技能` },
  { key: 'gradeDone', cat: '技能掌握', title: '通关整个年级', items: [1, 2, 3, 4, 5, 6].map((g) => ({ id: `gradeDone-${g}`, metric: `gradeDone${g}`, need: 1, name: `${g}年级全部掌握`, desc: `掌握 ${g} 年级的所有计算技能` })) },
  { key: 'laneDone', cat: '技能掌握', title: '精通整个计算分支', items: LANES.map((l, i) => ({ id: `laneDone-${i}`, metric: `laneDone${i}`, need: 1, name: `${l} 全部掌握`, desc: `掌握「${l}」分支下的全部技能` })) },
  { key: 'extras', cat: '加分挑战', title: '进入加时赛', metric: 'extras', steps: [1, 3, 5, 10, 20, 30, 50, 100, 200, 300], name: (v) => `加时赛 ${v} 次`, desc: (v) => `成功进入加时赛 ${v} 次` },
  { key: 'extraBest', cat: '加分挑战', title: '单次加时赛最高纪录', metric: 'extraBest', steps: [3, 5, 7, 10, 12, 15, 18, 20, 23, 25, 30], name: (v) => `单次 ${v} 题`, desc: (v) => `在单次加时赛中答对 ${v} 题` },
  { key: 'extraSolved', cat: '加分挑战', title: '加时赛答对总数', metric: 'extraSolved', steps: [10, 30, 50, 100, 200, 300, 500, 1000, 2000, 3000], name: (v) => `加时赛答对 ${fmt(v)} 题`, desc: (v) => `在加时赛中累计答对 ${fmt(v)} 题` },
  { key: 'combo', cat: '连对连击', title: '连对纪录', metric: 'maxCombo', steps: [5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 300], name: (v) => `${v} 连对`, desc: (v) => `达成 ${v} 连对` },
  { key: 'perfects', cat: '准确率', title: '完美无失误完赛', metric: 'perfects', steps: [1, 3, 5, 10, 20, 30, 50, 100, 200, 300], name: (v) => `完美通关 ${v} 次`, desc: (v) => `以 100% 首次正确率完成 ${v} 轮练习` },
  { key: 'firstTry', cat: '准确率', title: '首次即答对', metric: 'firstTry', steps: [10, 50, 100, 300, 500, 1000, 3000, 5000, 10000, 30000], name: (v) => `首次答对 ${fmt(v)} 题`, desc: (v) => `一次作答就成功的题目达到 ${fmt(v)} 题` },
  { key: 'dopa', cat: '多帕能量', title: '多帕能量', metric: 'bestDopaL', steps: [2, 3, 4, 5, 6, 7, 8, 9], name: (v) => `${DOPA_LABEL[v]} 多帕`, desc: (v) => `单局多帕能量突破 ${DOPA_LABEL[v]}` },
  { key: 'review', cat: '错题复习', title: '错题复习', metric: 'reviewSolved', steps: [1, 5, 10, 30, 50, 100, 200, 300], name: (v) => `复习 ${v} 题`, desc: (v) => `重新攻克 ${v} 道错题` },
  ...[1, 2, 3, 4, 5, 6].map((g) => ({ key: `grade${g}`, cat: '年级通关', title: `练习${g}年级`, metric: `gradePlays${g}`, steps: [1, 10, 30], name: (v) => `${g} 年级 ${v} 轮`, desc: (v) => `完成 ${g} 年级模式练习 ${v} 次` })),
  { key: 'secret', cat: '隐藏成就', title: '隐藏成就', items: [
    { id: 'secret-perfect14', metric: 'flag:perfect14', need: 1, name: '14题全对大满贯', desc: '在14题模式中0失误完美过关', secret: true },
    { id: 'secret-extraClean', metric: 'flag:extraClean', need: 1, name: '加分关零失误', desc: '在 Extra 加分关做对5题以上且0失误', secret: true },
    { id: 'secret-sunday', metric: 'flag:sunday', need: 1, name: '周日不偷懒', desc: '在周日开启数学练习', secret: true },
    { id: 'secret-newyear', metric: 'flag:newyear', need: 1, name: '新年第一练', desc: '在元旦（1月1日）练习数学', secret: true },
    { id: 'secret-comeback', metric: 'flag:comeback', need: 1, name: '欢迎回归！', desc: '间隔一周以上再次回来练习', secret: true },
    { id: 'secret-allmodes', metric: 'allModes', need: 1, name: '全能小达人', desc: '完整体验过我的等级、年级、专项练习与错题复习全部4种模式', secret: true },
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
  { key: 'questDays', cat: '坚持打卡', title: '每日任务全部达成', metric: 'questDays', steps: [1, 3, 7, 14, 30, 50, 100, 200, 365], name: (v) => `全通关 ${v} 天`, desc: (v) => `完成当天全部每日任务达到 ${v} 天` },
  { key: 'questRun', cat: '坚持打卡', title: '连续完成每日任务', metric: 'questRun', steps: [2, 3, 5, 7, 14, 30], name: (v) => `连续 ${v} 天全清`, desc: (v) => `连续 ${v} 天完成全部每日任务` },
  { key: 'hammer', cat: '坚持打卡', title: '打卡补签锤', metric: 'hammerUsed', steps: [1, 3, 10], name: (v) => (v === 1 ? '初次补签' : `补签 ${v} 次`), desc: (v) => `使用打卡锤保住连续打卡 ${v} 次` },
  { key: 'starsTotal', cat: '技能掌握', title: '收集技能星星', metric: 'starsTotal', steps: [5, 10, 25, 50, 75, 100, 150, 200, 250, 290], name: (v) => `星星 ${v} 颗`, desc: (v) => `累计收集技能星星 ${v} 颗` },
  { key: 'star5', cat: '技能掌握', title: '升至 ☆5 的技能', metric: 'star5', steps: [1, 3, 5, 10, 20, 30, 58], name: (v) => `☆5技能 ${v} 个`, desc: (v) => `将 ${v} 个技能提升至 ☆5 满星` },
  { key: 'gradeStar3', cat: '技能掌握', title: '整个年级达到 ☆3', items: [1, 2, 3, 4, 5, 6].map((g) => ({ id: `gradeStar3-${g}`, metric: `gradeStar3${g}`, need: 1, name: `${g}年级全员☆3`, desc: `将 ${g} 年级的所有技能都提升至 ☆3 以上` })) },
  { key: 'polished', cat: '不断进步', title: '温故知新除锈', metric: 'polished', steps: [1, 3, 5, 10, 30, 50], name: (v) => `重新点亮 ${v} 次`, desc: (v) => `复习变生疏的技能使其重新闪亮 ${v} 次` },
  { key: 'capsules', cat: '不断进步', title: '时光胶囊', metric: 'capsules', steps: [1, 3, 5, 10, 30], name: (v) => `开启胶囊 ${v} 次`, desc: (v) => `开启 ${v} 次挑战过去的时光胶囊` },
  { key: 'capsuleFaster', cat: '不断进步', title: '超越过去的自己', metric: 'capsuleFaster', steps: [1, 5, 10], name: (v) => `超越以往 ${v} 次`, desc: (v) => `在时光胶囊中比最初挑战时更快答完（${v}次）` },
  { key: 'grew', cat: '不断进步', title: '你进步了！', metric: 'grew', steps: [1, 5, 10, 30, 50, 100], name: (v) => `进步 ${v} 次`, desc: (v) => `在结算页面获得「你进步了！」评价 ${v} 次` },
  { key: 'items', cat: '图鉴收藏', title: '图鉴收藏总数', metric: 'itemsOwned', steps: [10, 20, 30, 40, 47], name: (v) => `收集 ${v} 件`, desc: (v) => `在收藏馆累计解锁 ${v} 件特效物品` },
  { key: 'catComplete', cat: '图鉴收藏', title: '集齐整个分类', metric: 'catComplete', steps: [1, 3, 5, 8], name: (v) => `集齐 ${v} 个分类`, desc: (v) => `将收藏馆中 ${v} 个分类的物品全部集齐` },
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
