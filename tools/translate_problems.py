import re

# Read Japanese base as it's cleaner and closer to standard math format (or EN base)
with open('app/ja/js/problems.js', 'r', encoding='utf-8') as f:
    ja = f.read()

# Let's inspect the diffs between EN and JA in problems.js:
# In EN:
# 1. PLACE = ['ones', 'tens', 'hundreds', 'thousands', 'ten thousands', 'hundred thousands']
#    JA: PLACE = ['一の位', '十の位', '百の位', '千の位', '万の位', '十万の位']
#    CN: PLACE = ['个位', '十位', '百位', '千位', '万位', '十万位']
#    TW: PLACE = ['個位', '十位', '百位', '千位', '萬位', '十萬位']
# 2. DEC_PLACE = ['tenths', 'hundredths', 'thousandths']
#    JA: DEC_PLACE = ['小数第一位', '小数第二位', '小数第三位']
#    CN: DEC_PLACE = ['十分位', '百分位', '千分位']
#    TW: DEC_PLACE = ['十分位', '百分位', '千分位']
# 3. table = (d, n) => ...
#    JA: `${d}のだん ${out.join(' ')}`
#    CN: `${d}的乘法口诀: ${out.join(' ')}`
#    TW: `${d}的乘法表: ${out.join(' ')}`
# 4. help text: 'くりあがりの 1' -> '进位的 1' / '進位的 1'
# 5. Titles:
#    'たしざん' -> '加法' / '加法'
#    '小数のたしざん' -> '小数加法' / '小數加法'
#    'ひきざん' -> '减法' / '減法'
#    '小数のひきざん' -> '小数减法' / '小數減法'
#    'かけざん' -> '乘法' / '乘法'
#    '小数のわりざん' -> '小数除法' / '小數除法'
#    'わりざん' -> '除法' / '除法'
#    'あまりのあるわりざん' -> '有余数的除法' / '有餘數的除法'
#    'いくつといくつ' -> '分成几和几' / '分成幾和幾'
#    '3つのかず' -> '三个数的运算' / '三數連加減'
#    '分数のたしひき' -> '分数加减法' / '分數加減'
#    'ぶんすう' -> '分数' / '分數'
#    '分数と整数' -> '分数与整数' / '分數與整數'
#    '小数と分数' -> '小数与分数' / '小數與分數'
#    'けいさんのきまり' -> '四则混合运算顺序' / '四則混合運算順序'
#    'がい数' -> '求近似数' / '求概數'
#    '約分' -> '约分' / '約分'
#    '百分率' -> '百分比' / '百分率'
#    'ひ' -> '比例' / '比例'
#    'xをもとめる' -> '解方程求 x' / '求未知數 x'
# 6. Labels:
#    'あまり' -> '余数' / '餘數'
#    '整数の部分' -> '整数部分' / '整數部分'
#    `商の${PLACE[cols - 1 - col]}` -> `商的${PLACE[cols - 1 - col]}`
#    'ひいた のこり' -> '相减的差' / '相減之差'
#    '商' -> '商'
#    `${factor}をかける` -> `乘 ${factor}` / '乘 ${factor}'
#    `たす（${PLACE[i]}）` -> `相加（${PLACE[i]}）`

def build_problems(is_tw=False):
    c = ja
    if is_tw:
        c = c.replace(
            "const PLACE = ['一の位', '十の位', '百の位', '千の位', '万の位', '十万の位'];",
            "const PLACE = ['個位', '十位', '百位', '千位', '萬位', '十萬位'];"
        )
        c = c.replace(
            "const DEC_PLACE = ['小数第一位', '小数第二位', '小数第三位'];",
            "const DEC_PLACE = ['十分位', '百分位', '千分位'];"
        )
        c = c.replace(
            "return `${d}のだん ${out.join(' ')}`;",
            "return `${d}的乘法表: ${out.join(' ')}`;"
        )
        c = c.replace("'くりあがりの 1'", "'進位的 1'")
        c = c.replace("`くりあがりの ${carry}`", "`進位的 ${carry}`")
        c = c.replace("'小数のたしざん'", "'小數加法'")
        c = c.replace("'たしざん'", "'加法'")
        c = c.replace("'小数のひきざん'", "'小數減法'")
        c = c.replace("'ひきざん'", "'減法'")
        c = c.replace("'かけざん'", "'乘法'")
        c = c.replace("`${factor}をかける`", "`乘 ${factor}`")
        c = c.replace("`たす（${PLACE[i]}）`", "`相加（${PLACE[i]}）`")
        c = c.replace("`商の${PLACE[cols - 1 - col]}`", "`商的${PLACE[cols - 1 - col]}`")
        c = c.replace("'商'", "'商'")
        c = c.replace("'ひいた のこり'", "'相減之差'")
        c = c.replace("'あまり'", "'餘數'")
        c = c.replace("'小数のわりざん'", "'小數除法'")
        c = c.replace("'あまりのあるわりざん'", "'有餘數除法'")
        c = c.replace("'わりざん'", "'除法'")
        c = c.replace("'いくつといくつ'", "'10的分成'")
        c = c.replace("'3つのかず'", "'連加連減'")
        c = c.replace("'分数のたしひき'", "'分數加減'")
        c = c.replace("'ぶんすう'", "'分數'")
        c = c.replace("'整数の部分'", "'整數部分'")
        c = c.replace("'分数と整数'", "'分數與整數'")
        c = c.replace("'小数と分数'", "'小數與分數'")
        c = c.replace("'けいさんのきまり'", "'運算順序'")
        c = c.replace("'がい数'", "'概數'")
        c = c.replace("'約分'", "'約分'")
        c = c.replace("'百分率'", "'百分率'")
        c = c.replace("'ひ'", "'比例'")
        c = c.replace("'xをもとめる'", "'求未知數 x'")
    else:
        c = c.replace(
            "const PLACE = ['一の位', '十の位', '百の位', '千の位', '万の位', '十万の位'];",
            "const PLACE = ['个位', '十位', '百位', '千位', '万位', '十万位'];"
        )
        c = c.replace(
            "const DEC_PLACE = ['小数第一位', '小数第二位', '小数第三位'];",
            "const DEC_PLACE = ['十分位', '百分位', '千分位'];"
        )
        c = c.replace(
            "return `${d}のだん ${out.join(' ')}`;",
            "return `${d}的乘法口诀: ${out.join(' ')}`;"
        )
        c = c.replace("'くりあがりの 1'", "'进位的 1'")
        c = c.replace("`くりあがりの ${carry}`", "`进位的 ${carry}`")
        c = c.replace("'小数のたしざん'", "'小数加法'")
        c = c.replace("'たしざん'", "'加法'")
        c = c.replace("'小数のひきざん'", "'小数减法'")
        c = c.replace("'ひきざん'", "'减法'")
        c = c.replace("'かけざん'", "'乘法'")
        c = c.replace("`${factor}をかける`", "`乘 ${factor}`")
        c = c.replace("`たす（${PLACE[i]}）`", "`相加（${PLACE[i]}）`")
        c = c.replace("`商の${PLACE[cols - 1 - col]}`", "`商的${PLACE[cols - 1 - col]}`")
        c = c.replace("'商'", "'商'")
        c = c.replace("'ひいた のこり'", "'相减的差'")
        c = c.replace("'あまり'", "'余数'")
        c = c.replace("'小数のわりざん'", "'小数除法'")
        c = c.replace("'あまりのあるわりざん'", "'有余数的除法'")
        c = c.replace("'わりざん'", "'除法'")
        c = c.replace("'いくつといくつ'", "'10的分成'")
        c = c.replace("'3つのかず'", "'连加连减'")
        c = c.replace("'分数のたしひき'", "'分数加减法'")
        c = c.replace("'ぶんすう'", "'分数'")
        c = c.replace("'整数の部分'", "'整数部分'")
        c = c.replace("'分数と整数'", "'分数与整数'")
        c = c.replace("'小数と分数'", "'小数与分数'")
        c = c.replace("'けいさんのきまり'", "'运算顺序'")
        c = c.replace("'がい数'", "'近似数'")
        c = c.replace("'約分'", "'约分'")
        c = c.replace("'百分率'", "'百分比'")
        c = c.replace("'ひ'", "'比例'")
        c = c.replace("'xをもとめる'", "'求未知数 x'")
    return c

with open('app/zh-CN/js/problems.js', 'w', encoding='utf-8') as f:
    f.write(build_problems(False))
with open('app/zh-TW/js/problems.js', 'w', encoding='utf-8') as f:
    f.write(build_problems(True))

print("Updated problems.js for zh-CN and zh-TW")
