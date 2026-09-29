# Quests translations for zh-CN and zh-TW
with open('app/en/js/quests.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace quest texts:
# 'Play once' -> '练习 1 次' / '練習 1 次'
# 'Get a 5 combo' -> '达成 5 连对' / '達成 5 連對'
# 'Get 5 right on the first try' -> '首次作答正确 5 题' / '首次作答正確 5 題'
# 'Review 1 problem' -> '复习 1 道错题' / '複習 1 道錯題'
# 'Solve 1 from a NEW skill' -> '尝试新技能答对 1 题' / '嘗試新技能答對 1 題'
# 'Reach Extra' -> '进入 Extra 加分关卡' / '進入 Extra 加分挑戰'
# 'Solve 5 in Extra' -> '在 Extra 答对 5 题' / '在 Extra 答對 5 題'
# 'Get a 20 combo' -> '达成 20 连对' / '達成 20 連對'
# 'Play twice' -> '练习 2 次' / '練習 2 次'
# 'Play one Grade drill' -> '完成 1 次年级练习' / '完成 1 次年級練習'
# 'Solve 10 from skills you are learning' -> '做 10 道正在学习的技能题' / '做 10 題正在學習的單元'
# Polish: `擦亮「${name}」（做 3 题）` / `磨練「${name}」（做 3 題）`

def make_quests(is_tw=False):
    c = text
    if is_tw:
        c = c.replace("'Play once'", "'練習 1 次'")
        c = c.replace("'Get a 5 combo'", "'達成 5 連對'")
        c = c.replace("'Get 5 right on the first try'", "'首次即答對 5 題'")
        c = c.replace("'Review 1 problem'", "'複習 1 道錯題'")
        c = c.replace("'Solve 1 from a NEW skill'", "'練習新單元答對 1 題'")
        c = c.replace("'Reach Extra'", "'進入 Extra 加分挑戰'")
        c = c.replace("'Solve 5 in Extra'", "'在 Extra 答對 5 題'")
        c = c.replace("'Get a 20 combo'", "'達成 20 連對'")
        c = c.replace("'Play twice'", "'練習 2 次'")
        c = c.replace("'Play one Grade drill'", "'完成 1 次年級練習'")
        c = c.replace("'Solve 10 from skills you are learning'", "'做 10 題正在學習的單元'")
        c = c.replace('return `Polish "${name}" (3 problems)`;', 'return `磨練「${name}」（3 題）`;')
    else:
        c = c.replace("'Play once'", "'练习 1 次'")
        c = c.replace("'Get a 5 combo'", "'达成 5 连对'")
        c = c.replace("'Get 5 right on the first try'", "'首次即答对 5 题'")
        c = c.replace("'Review 1 problem'", "'复习 1 道错题'")
        c = c.replace("'Solve 1 from a NEW skill'", "'练习新技能答对 1 题'")
        c = c.replace("'Reach Extra'", "'进入 Extra 加分挑战'")
        c = c.replace("'Solve 5 in Extra'", "'在 Extra 答对 5 题'")
        c = c.replace("'Get a 20 combo'", "'达成 20 连对'")
        c = c.replace("'Play twice'", "'练习 2 次'")
        c = c.replace("'Play one Grade drill'", "'完成 1 次年级练习'")
        c = c.replace("'Solve 10 from skills you are learning'", "'做 10 道正在学习的技能题'")
        c = c.replace('return `Polish "${name}" (3 problems)`;', 'return `擦亮「${name}」（3 题）`;')
    return c

with open('app/zh-CN/js/quests.js', 'w', encoding='utf-8') as f:
    f.write(make_quests(False))
with open('app/zh-TW/js/quests.js', 'w', encoding='utf-8') as f:
    f.write(make_quests(True))

print("Updated quests.js for zh-CN and zh-TW")
