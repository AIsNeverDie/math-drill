for lang, is_tw in [('zh-CN', False), ('zh-TW', True)]:
    path = f'app/{lang}/js/main.js'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Capsule intro envelope letter
    old_intro = '<small>TIME CAPSULE</small><b>From ${fmtDay(info.d)}</b><span>A problem from when you first started!</span>'
    cap_title = '時光膠囊' if is_tw else '时光胶囊'
    from_date = '來自 ${fmtDay(info.d)}' if is_tw else '来自 ${fmtDay(info.d)}'
    sub_desc = '這是你最初開始練習時做過的題目！' if is_tw else '这是你最初开始练习时做过的题目！'
    new_intro = f'<small>{cap_title}</small><b>{from_date}</b><span>{sub_desc}</span>'
    text = text.replace(old_intro, new_intro)

    # Day title format: ensure ${MONTHS[m - 1]}${d}日
    text = text.replace(
        "$('#day-title').textContent = `${MONTHS[m - 1]} ${d}`;",
        "$('#day-title').textContent = `${MONTHS[m - 1]}${d}日`;"
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

print("Capsule intro and dates updated!")
