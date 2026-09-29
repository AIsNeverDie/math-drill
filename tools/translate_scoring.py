# Scoring translations for zh-CN and zh-TW
# Chinese numbering: 万 (10^4), 亿 (10^8), 兆 (10^12), 京 (10^16), 垓 (10^20), 秭 (10^24), 穰 (10^28), 沟 (10^32), 涧 (10^36), 正 (10^40), 载 (10^44), 极 (10^48), 恒河沙 (10^52), 阿僧祇 (10^56), 那由他 (10^60), 不可思议 (10^64), 无量大数 (10^68)

content_cn = '''// Pure scoring and "dopa" curves (kept separate from the director for testing).

export const BASIC_SCORE = 100;
export const EXTRA_BASE = 10;

export const EXTRA_STEP = 5;
export const extraPoints = (k) => EXTRA_BASE + EXTRA_STEP * k;
export const extraTotal = (n) => EXTRA_BASE * n + EXTRA_STEP * (n * (n - 1)) / 2;

export const BASIC_DOPA_L = 2.3;
export function basicDopaL(frac) {
  const f = Math.min(1, Math.max(0, frac));
  return BASIC_DOPA_L * f ** 1.15;
}
const EXTRA_SPAN = 3.0; const EXTRA_TAU = 10;
export const extraDopaL = (n) => BASIC_DOPA_L + EXTRA_SPAN * (1 - Math.exp(-n / EXTRA_TAU));
export const extraProblemGain = (k) => extraDopaL(k + 1) - extraDopaL(k);
export const DOPA_MAX_L = 9.08;

export const COMBO_DOPA = { max: 2, full: 20 };
export const comboMult = (combo) => 1 + (COMBO_DOPA.max - 1) * Math.min(1, Math.max(0, combo) / COMBO_DOPA.full);
export const comboMaxed = (combo) => combo >= COMBO_DOPA.full;

export function addDopa(L, base, combo) {
  return Math.min(DOPA_MAX_L, L + Math.max(0.003, base) * comboMult(combo));
}

export const COMBO_TIME = { base: 3000, perGrade: 600, read: 2500 };
export function comboWindowMs(grade = 3, first = false) {
  const g = Math.min(6, Math.max(1, grade || 3));
  return COMBO_TIME.base + COMBO_TIME.perGrade * (g - 1) + (first ? COMBO_TIME.read : 0);
}
export const comboMilestone = (c) => [10, 20, 30, 50, 75].includes(c) || (c >= 100 && c % 50 === 0);

const UNITS = [[68, '无量大数'], [64, '不可思议'], [60, '那由他'], [56, '阿僧祇'], [52, '恒河沙'], [48, '极'], [44, '载'], [40, '正'], [36, '涧'], [32, '沟'], [28, '穰'], [24, '秭'], [20, '垓'], [16, '京'], [12, '兆'], [8, '亿'], [4, '万']];
const MILESTONES = [[3, '千'], [2, '百']];

export function fmtDopa(L) {
  if (!Number.isFinite(L) || L >= 72) return '∞';
  if (L < 4) return Math.round(10 ** L).toLocaleString('zh-CN');
  const u = UNITS.find(([e]) => L >= e - 1e-9);
  const m = 10 ** (L - u[0]);
  return (m < 10 ? m.toFixed(1) : String(Math.floor(m))) + u[1];
}

export function unitOf(L) {
  if (L >= 72) return '∞';
  if (L >= 4 && L < 8) return ['万', '十万', '百万', '千万'][Math.floor(L + 1e-9) - 4];
  const u = UNITS.find(([e]) => L >= e - 1e-9) || MILESTONES.find(([e]) => L >= e - 1e-9);
  return u ? u[1] : '';
}

const LABELS = { '∞': '∞', 百: '100', 千: '1000', 十万: '10万', 百万: '100万', 千万: '1000万' };
export const unitLabel = (u) => LABELS[u] || `1${u}`;
'''

content_tw = content_cn.replace('无量大数', '無量大數').replace('不可思议', '不可思議').replace('阿僧祇', '阿僧祇').replace('极', '極').replace('载', '載').replace('涧', '澗').replace('沟', '溝').replace('穰', '穰').replace('秭', '秭').replace('亿', '億').replace('zh-CN', 'zh-TW')

with open('app/zh-CN/js/scoring.js', 'w', encoding='utf-8') as f:
    f.write(content_cn)
with open('app/zh-TW/js/scoring.js', 'w', encoding='utf-8') as f:
    f.write(content_tw)
print("Updated scoring.js for zh-CN and zh-TW")
