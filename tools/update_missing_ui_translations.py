# Comprehensive update for any remaining untranslated strings in zh-CN and zh-TW

for lang, is_tw in [('zh-CN', False), ('zh-TW', True)]:
    # 1. main.js
    with open(f'app/{lang}/js/main.js', 'r', encoding='utf-8') as f:
        text = f.read()

    grade_str = '年級' if is_tw else '年级'
    text = text.replace(
        "$('#si-grade').textContent = `Grade ${sk.grade} · ${LANES[sk.lane]}`;",
        f"$('#si-grade').textContent = `${{sk.grade}} {grade_str} · ${{LANES[sk.lane]}}`;"
    )
    # Solved: N in skill info
    solved_str = '累計答對' if is_tw else '累计答对'
    text = text.replace(
        "Solved: ${r.n || 0}",
        f"{solved_str}：${{r.n || 0}}"
    )
    # Hint in repeated misses
    hint_str = '提示'
    text = text.replace(
        "<span class=\"help-text\">${`<b>Hint</b> ${st.help.text}`}</span>",
        f"<span class=\"help-text\">${{`<b>{hint_str}</b> ${{st.help.text}}`}}</span>"
    )
    # Unlocked! in announceUnlock
    unlock_str = '解鎖新技能！' if is_tw else '解锁新技能！'
    text = text.replace(
        "cutin(`Unlocked! ${name}`, Math.max(0.6, S.E));",
        f"cutin(`{unlock_str} ${{name}}`, Math.max(0.6, S.E));"
    )
    # Time capsule in renderSkillNews
    capsule_str = '時光膠囊' if is_tw else '时光胶囊'
    text = text.replace(
        "<b>Time capsule</b>",
        f"<b>{capsule_str}</b>"
    )
    # Polished! in renderSkillNews
    polished_str = '重煥光芒！' if is_tw else '重焕光彩！'
    text = text.replace(
        "`<p class=\"polish-news\">Polished! ${SKILL[id].name}</p>`",
        f"`<p class=\"polish-news\">{polished_str} ${{SKILL[id].name}}</p>`"
    )
    # Mastered! in renderSkillNews
    mastered_str = '完全精通！' if is_tw else '完全精通！'
    text = text.replace(
        "`<p class=\"mastered\">Mastered! ${SKILL[id].name}</p>`",
        f"`<p class=\"mastered\">{mastered_str} ${{SKILL[id].name}}</p>`"
    )
    # Unlocked! in renderSkillNews
    text = text.replace(
        "`<p>Unlocked! ${SKILL[id].name}</p>`",
        f"`<p>{unlock_str} ${{SKILL[id].name}}</p>`"
    )
    # Skill check done in renderSkillNews
    sk_done_prefix = '能力診斷完成：已掌握 ' if is_tw else '能力诊断完成：已掌握 '
    sk_done_suffix = ' 項技能' if is_tw else ' 项技能'
    text = text.replace(
        "Skill check done: ${SKILLS.filter((x) => stateOf(progress(), x.id) === 'mastered').length} cleared",
        f"{sk_done_prefix}${{SKILLS.filter((x) => stateOf(progress(), x.id) === 'mastered').length}}{sk_done_suffix}"
    )
    # Next: in level-sub
    next_prefix = '下一目標：「' if is_tw else '下一目标：「'
    text = text.replace(
        "Next: \"${SKILL[frontier(prog)[0] || ORDER[ORDER.length - 1]].name}\"",
        f"{next_prefix}${{SKILL[frontier(prog)[0] || ORDER[ORDER.length - 1]].name}}」"
    )
    # Starts with a skill check
    starts_str = '從能力診斷開始' if is_tw else '从能力诊断开始'
    text = text.replace(
        "'Starts with a skill check'",
        f"'{starts_str}'"
    )
    # Shine! Sparkle! in polishFx
    shine_str = '閃閃發光！' if is_tw else '闪闪发光！'
    text = text.replace(
        "'Shine! Sparkle!'",
        f"'{shine_str}'"
    )
    # Combo pop text
    combo_str = '連擊！' if is_tw else '连击！'
    text = text.replace(
        "`${S.combo} combo!`",
        f"`${{S.combo}} {combo_str}`"
    )
    combo_over = '連擊結束' if is_tw else '连击中断'
    combo_word = '連擊' if is_tw else '连击'
    text = text.replace(
        "timeout ? `${had} combo over` : `${had} combo`",
        f"timeout ? `${{had}} {combo_over}` : `${{had}} {combo_word}`"
    )
    # Dopa mult
    dopa_max = '多帕能量 ×2 MAX'
    text = text.replace(
        "'Dopa ×2 MAX'",
        f"'{dopa_max}'"
    )
    text = text.replace(
        "`Dopa ×${comboMult(S.combo).toFixed(2)}`",
        f"`多帕 ×${{comboMult(S.combo).toFixed(2)}}`"
    )
    # Extra floating pts
    text = text.replace(
        "`+${points.toLocaleString('en-US')} pts`",
        f"`+${{points.toLocaleString('zh-CN')}} 分`"
    )
    # 100 pts
    text = text.replace("bigStamp('100 pts');", "bigStamp('100 分！');")
    text = text.replace("banner.textContent = '100 pts!';", "banner.textContent = '100 分！';")
    # Reset confirm texts
    erase_msg = '這將清除所有打卡記錄、技能、成就獎杯、收藏物品、貼紙和設定。' if is_tw else '这将清除所有打卡记录、技能树、成就奖杯、图鉴收藏、签到印章和设置。'
    text = text.replace(
        "msg: 'This erases all records, skills, trophies, collection items, stickers and settings.'",
        f"msg: '{erase_msg}'"
    )
    really_title = '確定要徹底清除全部資料嗎？' if is_tw else '确定要彻底清除所有数据吗？'
    text = text.replace(
        "title: 'Really erase everything?'",
        f"title: '{really_title}'"
    )
    really_msg = '資料一旦清除將無法復原，請再次確認。' if is_tw else '数据一旦清除将无法找回，请再次确认。'
    text = text.replace(
        "msg: \"Once it's erased, it can't be brought back.\"",
        f"msg: '{really_msg}'"
    )
    # +N more in trophy / relock lists
    more_item = '項' if is_tw else '项'
    text = text.replace(
        "`<li class=\"more\">+${list.length - MAX} more</li>`",
        f"`<li class=\"more\">+${{list.length - MAX}} {more_item}...</li>`"
    )
    text = text.replace(
        "`<li class=\"more\">+${ids.length - MAX} more</li>`",
        f"`<li class=\"more\">+${{ids.length - MAX}} {more_item}...</li>`"
    )
    # Correct in stamp mark
    correct_str = "優秀" if is_tw else "优秀"
    text = text.replace("CORRECT", correct_str)

    with open(f'app/{lang}/js/main.js', 'w', encoding='utf-8') as f:
        f.write(text)

    # 2. unlocks.js names in Chinese
    with open(f'app/{lang}/js/unlocks.js', 'r', encoding='utf-8') as f:
        utext = f.read()

    hb_str = '頭帶' if is_tw else '运动头带'
    cape_str = '披風' if is_tw else '勇气披风'
    wiz_str = '魔法帽' if is_tw else '魔法师帽'
    hp_str = '耳機' if is_tw else '头戴耳机'
    utext = utext.replace("name: 'Headband'", f"name: '{hb_str}'")
    utext = utext.replace("name: 'Cape'", f"name: '{cape_str}'")
    utext = utext.replace("name: 'Wizard hat'", f"name: '{wiz_str}'")
    utext = utext.replace("name: 'Headphones'", f"name: '{hp_str}'")

    with open(f'app/{lang}/js/unlocks.js', 'w', encoding='utf-8') as f:
        f.write(utext)

print("Main.js and Unlocks.js fully translated!")
