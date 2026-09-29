for lang, is_tw in [('zh-CN', False), ('zh-TW', True)]:
    path = f'app/{lang}/js/main.js'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Day title: e.g. 5月10日
    text = text.replace(
        "$('#day-title').textContent = `${MONTHS[m - 1]} ${d}`;",
        "$('#day-title').textContent = `${MONTHS[m - 1]}${d}日`;"
    )

    # Day list entry
    old_entry = "return `<li><span class=\"t\">${time}</span><span class=\"m\">${name}</span><span class=\"s\">${`${(h.score || 0).toLocaleString('en-US')} pts`}</span><span class=\"d\">${`Correct ${h.ok ?? '-'} · Oops ${h.ng ?? '-'}${extra} · ${fmtTime(h.timeMs || 0)}`}</span></li>`;"

    pts_str = '分'
    correct_str = '答對' if is_tw else '答对'
    oops_str = '失誤' if is_tw else '失误'

    new_entry = f'return `<li><span class="t">${{time}}</span><span class="m">${{name}}</span><span class="s">${{`${{(h.score || 0).toLocaleString("zh-CN")}} {pts_str}`}}</span><span class="d">${{`{correct_str} ${{h.ok ?? "-"}} · {oops_str} ${{h.ng ?? "-"}}${{extra}} · ${{fmtTime(h.timeMs || 0)}}`}}</span></li>`;'

    if old_entry in text:
        text = text.replace(old_entry, new_entry)
        print(f'Replaced in {lang}')
    else:
        print(f'old_entry not found in {lang}')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

