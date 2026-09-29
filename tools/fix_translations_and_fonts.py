import re
import pathlib

# 1. Update app/zh-CN/js/problems.js
with open('app/zh-CN/js/problems.js', 'r', encoding='utf-8') as f:
    cn_prob = f.read()

# Replace こたえ with 答案
cn_prob = cn_prob.replace("label: t.label || 'こたえ'", "label: t.label || '答案'")
# Replace あまり with 余
cn_prob = cn_prob.replace("const answer = rem ? `${q} あまり ${rem}` : String(q);", "const answer = rem ? `${q} 余 ${rem}` : String(q);")
cn_prob = cn_prob.replace("answer: `${q} あまり ${rem}`", "answer: `${q} 余 ${rem}`")
# Line 169
cn_prob = cn_prob.replace("title: P ? '小数のかけざん' : '乘法'", "title: P ? '小数乘法' : '乘法'")
# Line 202
cn_prob = cn_prob.replace("hint: `${cur}の中に${d}はいくつ`", "hint: `${cur} 中有几个 ${d}`")
# Line 322
cn_prob = cn_prob.replace("text: `${Math.floor(n / d)}と${n % d}/${d}`", "text: `${Math.floor(n / d)}又${n % d}/${d}`")
# Line 330
cn_prob = cn_prob.replace("return buildH([{ n: total }, { w: 'は' }, { n: a }, { w: 'と' }, { ans: total - a }], { title: '10的分成', text: `${total}は${a}と`, answer: String(total - a), help: `${a}に いくつで ${total}` });",
                          "return buildH([{ n: total }, { w: '分成' }, { n: a }, { w: '和' }, { ans: total - a }], { title: '10的分成', text: `${total}分成${a}和`, answer: String(total - a), help: `${a} 和几凑成 ${total}` });")
# Line 341
cn_prob = cn_prob.replace("const help = carry === 'yes' ? `${x}に ${10 - (x % 10)}で 10` : null;",
                          "const help = carry === 'yes' ? `凑10：${x} ＋ ${10 - (x % 10)}` : null;")
# Line 367
cn_prob = cn_prob.replace("help: `まず ${a} ${o1} ${b} ＝ ${s1}`", "help: `先算：${a} ${o1} ${b} ＝ ${s1}`")
# Line 377
cn_prob = cn_prob.replace("help: `${a / 10} × ${b} の 10こぶん`", "help: `${a / 10} × ${b} 的 10 倍`")
# Line 381
cn_prob = cn_prob.replace("return buildH([{ n: q * d }, { w: 'の' }, fracTok(1, d), { w: 'は' }, { ans: q }], { title: '分数', text: `${q * d}の1/${d}`, answer: String(q), help: `${q * d}を ${d}つに わける` });",
                          "return buildH([{ n: q * d }, { w: '的' }, fracTok(1, d), { w: '是' }, { ans: q }], { title: '分数', text: `${q * d}的1/${d}`, answer: String(q), help: `把 ${q * d} 平均分成 ${d} 份` });")
# Line 396
cn_prob = cn_prob.replace("help: `${q * d} ÷ ${d} の 10こぶん`", "help: `${q * d} ÷ ${d}，再 × 10`")
# Line 398
cn_prob = cn_prob.replace("help: `${Math.floor(D / 10) * 10} ÷ ${d} と ${D % 10} ÷ ${d}`", "help: `${Math.floor(D / 10) * 10} ÷ ${d} 与 ${D % 10} ÷ ${d}`")
# Line 474
cn_prob = cn_prob.replace("help: `${D} ÷ ${d} を 考える`", "help: `想：${D} ÷ ${d}`")
# Line 481, 483
cn_prob = cn_prob.replace("help: `${D} ÷ ${d} と 同じ`", "help: `相当于 ${D} ÷ ${d}`")
cn_prob = cn_prob.replace("help: `${D2} ÷ ${d2} と 同じ`", "help: `相当于 ${D2} ÷ ${d2}`")
# Line 493
cn_prob = cn_prob.replace("return buildH([{ n: a }, { w: 'と' }, { n: b }, { w: 'の' }, { br: true }, { w }, { op: '＝' }, { ans }], { title: w, text: `${a}と${b}の${w}`, answer: String(ans), help: kind === 'gcd' ? `どちらも わりきれる 数` : `${Math.max(a, b)}のばいすう` });",
                          "return buildH([{ n: a }, { w: '和' }, { n: b }, { w: '的' }, { br: true }, { w }, { op: '＝' }, { ans }], { title: w, text: `${a}和${b}的${w}`, answer: String(ans), help: kind === 'gcd' ? '能同时整除两数的最大数' : `${Math.max(a, b)} 的倍数` });")
# Lines 503-506
cn_prob = cn_prob.replace("help = `先に ${b} × ${c}`;", "help = `先算 ${b} × ${c}`;")
cn_prob = cn_prob.replace("help = `先に ${b} ＋ ${c}`;", "help = `先算 ${b} ＋ ${c}`;")
cn_prob = cn_prob.replace("help = `先に ${a} − ${b}`;", "help = `先算 ${a} − ${b}`;")
# Line 519
cn_prob = cn_prob.replace("return buildH([{ n }, { w: 'を' }, { br: true }, { w: `${nm}の位まで` }, { op: '→' }, { ans }], { title: '近似数', text: `${n}を${nm}の位までのがい数に`, answer: String(ans), help: `${['一', '十', '百'][pl - 1]}の位を 四捨五入` });",
                          "return buildH([{ n }, { w: '精确到' }, { br: true }, { w: `${nm}位` }, { op: '→' }, { ans }], { title: '近似数', text: `${n}精确到${nm}位`, answer: String(ans), help: `将${['个', '十', '百'][pl - 1]}位四舍五入` });")
# Line 526
cn_prob = cn_prob.replace("return buildH([{ n: base }, { w: 'の' }, { n: p }, { op: '%' }, { op: '＝' }, { ans }], { title: '百分比', text: `${base}の${p}%`, answer: String(ans), help: `${base} × ${p / 100}` });",
                          "return buildH([{ n: base }, { w: '的' }, { n: p }, { op: '%' }, { op: '＝' }, { ans }], { title: '百分比', text: `${base}的${p}%`, answer: String(ans), help: `${base} × ${p / 100}` });")
# Line 536
cn_prob = cn_prob.replace("help: `${k}ばい`", "help: `扩大 ${k} 倍`")
# Line 553
cn_prob = cn_prob.replace("help: `${k}で わる`", "help: `分子分母同时除以 ${k}`")
# Line 564
cn_prob = cn_prob.replace("text: `${w1}と${n1}/${d} ${add ? '+' : '−'} ${w2}と${n2}/${d}`", "text: `${w1}又${n1}/${d} ${add ? '+' : '−'} ${w2}又${n2}/${d}`")
cn_prob = cn_prob.replace("answer: res >= d ? `${Math.floor(res / d)}と${res % d}/${d}` : `${res}/${d}`", "answer: res >= d ? `${Math.floor(res / d)}又${res % d}/${d}` : `${res}/${d}`")
cn_prob = cn_prob.replace("help: `分母は ${d} のまま`", "help: `分母保持 ${d} 不变`")
# Line 578
cn_prob = cn_prob.replace("help: `通分すると 分母は ${L}`", "help: `通分公分母：${L}`")
# Line 586
cn_prob = cn_prob.replace("help: mul ? `分子に ${k} をかける` : `分母に ${k} をかける`", "help: mul ? `分子乘以 ${k}` : `分母乘以 ${k}`")
# Line 594
cn_prob = cn_prob.replace("title: op === 'mul' ? '分数のかけざん' : '分数のわりざん'", "title: op === 'mul' ? '分数乘法' : '分数除法'")
cn_prob = cn_prob.replace("help: op === 'mul' ? '分母どうし・分子どうしをかける' : `${n2}/${d2} を ひっくりかえして かける`",
                          "help: op === 'mul' ? '分子乘分子，分母乘分母' : `颠倒 ${n2}/${d2} 分子分母相乘`")

with open('app/zh-CN/js/problems.js', 'w', encoding='utf-8') as f:
    f.write(cn_prob)

# 2. Update app/zh-TW/js/problems.js
with open('app/zh-TW/js/problems.js', 'r', encoding='utf-8') as f:
    tw_prob = f.read()

tw_prob = tw_prob.replace("label: t.label || 'こたえ'", "label: t.label || '答案'")
tw_prob = tw_prob.replace("const answer = rem ? `${q} あまり ${rem}` : String(q);", "const answer = rem ? `${q} 餘 ${rem}` : String(q);")
tw_prob = tw_prob.replace("answer: `${q} あまり ${rem}`", "answer: `${q} 餘 ${rem}`")
tw_prob = tw_prob.replace("title: P ? '小数のかけざん' : '乘法'", "title: P ? '小數乘法' : '乘法'")
tw_prob = tw_prob.replace("title: P ? '小數のかけざん' : '乘法'", "title: P ? '小數乘法' : '乘法'")
tw_prob = tw_prob.replace("hint: `${cur}の中に${d}はいくつ`", "hint: `${cur} 中有幾個 ${d}`")
tw_prob = tw_prob.replace("text: `${Math.floor(n / d)}と${n % d}/${d}`", "text: `${Math.floor(n / d)}又${n % d}/${d}`")
tw_prob = tw_prob.replace("return buildH([{ n: total }, { w: 'は' }, { n: a }, { w: 'と' }, { ans: total - a }], { title: '10的分成', text: `${total}は${a}と`, answer: String(total - a), help: `${a}に いくつで ${total}` });",
                          "return buildH([{ n: total }, { w: '分成' }, { n: a }, { w: '和' }, { ans: total - a }], { title: '10的分成', text: `${total}分成${a}和`, answer: String(total - a), help: `${a} 和幾湊成 ${total}` });")
tw_prob = tw_prob.replace("const help = carry === 'yes' ? `${x}に ${10 - (x % 10)}で 10` : null;",
                          "const help = carry === 'yes' ? `湊10：${x} ＋ ${10 - (x % 10)}` : null;")
tw_prob = tw_prob.replace("help: `まず ${a} ${o1} ${b} ＝ ${s1}`", "help: `先算：${a} ${o1} ${b} ＝ ${s1}`")
tw_prob = tw_prob.replace("help: `${a / 10} × ${b} の 10こぶん`", "help: `${a / 10} × ${b} 的 10 倍`")
tw_prob = tw_prob.replace("return buildH([{ n: q * d }, { w: 'の' }, fracTok(1, d), { w: 'は' }, { ans: q }], { title: '分數', text: `${q * d}の1/${d}`, answer: String(q), help: `${q * d}を ${d}つに わける` });",
                          "return buildH([{ n: q * d }, { w: '的' }, fracTok(1, d), { w: '是' }, { ans: q }], { title: '分數', text: `${q * d}的1/${d}`, answer: String(q), help: `把 ${q * d} 平均分成 ${d} 份` });")
tw_prob = tw_prob.replace("help: `${q * d} ÷ ${d} の 10こぶん`", "help: `${q * d} ÷ ${d}，再 × 10`")
tw_prob = tw_prob.replace("help: `${Math.floor(D / 10) * 10} ÷ ${d} と ${D % 10} ÷ ${d}`", "help: `${Math.floor(D / 10) * 10} ÷ ${d} 與 ${D % 10} ÷ ${d}`")
tw_prob = tw_prob.replace("help: `${D} ÷ ${d} を 考える`", "help: `想：${D} ÷ ${d}`")
tw_prob = tw_prob.replace("help: `${D} ÷ ${d} と 同じ`", "help: `相當於 ${D} ÷ ${d}`")
tw_prob = tw_prob.replace("help: `${D2} ÷ ${d2} と 同じ`", "help: `相當於 ${D2} ÷ ${d2}`")
tw_prob = tw_prob.replace("return buildH([{ n: a }, { w: 'と' }, { n: b }, { w: 'の' }, { br: true }, { w }, { op: '＝' }, { ans }], { title: w, text: `${a}と${b}の${w}`, answer: String(ans), help: kind === 'gcd' ? `どちらも わりきれる 数` : `${Math.max(a, b)}のばいすう` });",
                          "return buildH([{ n: a }, { w: '和' }, { n: b }, { w: '的' }, { br: true }, { w }, { op: '＝' }, { ans }], { title: w, text: `${a}和${b}的${w}`, answer: String(ans), help: kind === 'gcd' ? '能同時整除兩數的最大數' : `${Math.max(a, b)} 的倍數` });")
tw_prob = tw_prob.replace("help = `先に ${b} × ${c}`;", "help = `先算 ${b} × ${c}`;")
tw_prob = tw_prob.replace("help = `先に ${b} ＋ ${c}`;", "help = `先算 ${b} ＋ ${c}`;")
tw_prob = tw_prob.replace("help = `先に ${a} − ${b}`;", "help = `先算 ${a} − ${b}`;")
tw_prob = tw_prob.replace("return buildH([{ n }, { w: 'を' }, { br: true }, { w: `${nm}の位まで` }, { op: '→' }, { ans }], { title: '近似数', text: `${n}を${nm}の位までのがい数に`, answer: String(ans), help: `${['一', '十', '百'][pl - 1]}の位を 四捨五入` });",
                          "return buildH([{ n }, { w: '精確到' }, { br: true }, { w: `${nm}位` }, { op: '→' }, { ans }], { title: '概數', text: `${n}精確到${nm}位`, answer: String(ans), help: `將${['個', '十', '百'][pl - 1]}位四捨五入` });")
tw_prob = tw_prob.replace("return buildH([{ n: base }, { w: 'の' }, { n: p }, { op: '%' }, { op: '＝' }, { ans }], { title: '百分比', text: `${base}の${p}%`, answer: String(ans), help: `${base} × ${p / 100}` });",
                          "return buildH([{ n: base }, { w: '的' }, { n: p }, { op: '%' }, { op: '＝' }, { ans }], { title: '百分比', text: `${base}的${p}%`, answer: String(ans), help: `${base} × ${p / 100}` });")
tw_prob = tw_prob.replace("help: `${k}ばい`", "help: `擴大 ${k} 倍`")
tw_prob = tw_prob.replace("help: `${k}で わる`", "help: `分子分母同時除以 ${k}`")
tw_prob = tw_prob.replace("text: `${w1}と${n1}/${d} ${add ? '+' : '−'} ${w2}と${n2}/${d}`", "text: `${w1}又${n1}/${d} ${add ? '+' : '−'} ${w2}又${n2}/${d}`")
tw_prob = tw_prob.replace("answer: res >= d ? `${Math.floor(res / d)}と${res % d}/${d}` : `${res}/${d}`", "answer: res >= d ? `${Math.floor(res / d)}又${res % d}/${d}` : `${res}/${d}`")
tw_prob = tw_prob.replace("help: `分母は ${d} のまま`", "help: `分母保持 ${d} 不變`")
tw_prob = tw_prob.replace("help: `通分すると 分母は ${L}`", "help: `通分公分母：${L}`")
tw_prob = tw_prob.replace("help: mul ? `分子に ${k} をかける` : `分母に ${k} をかける`", "help: mul ? `分子乘以 ${k}` : `分母乘以 ${k}`")
tw_prob = tw_prob.replace("title: op === 'mul' ? '分数のかけざん' : '分数のわりざん'", "title: op === 'mul' ? '分數乘法' : '分數除法'")
tw_prob = tw_prob.replace("title: op === 'mul' ? '分數のかけざん' : '分數のわりざん'", "title: op === 'mul' ? '分數乘法' : '分數除法'")
tw_prob = tw_prob.replace("help: op === 'mul' ? '分母どうし・分子どうしをかける' : `${n2}/${d2} を ひっくりかえして かける`",
                          "help: op === 'mul' ? '分子乘分子，分母乘分母' : `顛倒 ${n2}/${d2} 分子分母相乘`")

with open('app/zh-TW/js/problems.js', 'w', encoding='utf-8') as f:
    f.write(tw_prob)

print("problems.js updated successfully for zh-CN and zh-TW")
