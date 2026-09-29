import re

with open('app/en/js/main.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect ja main.js lines to see all localized expressions
# Months:
# EN: const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
# CN: const MONTHS = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
# TW: const MONTHS = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];

# Mode names:
# MODE_NAMES = { drill: (h) => h.count ? `${h.count}-problem drill` : 'Drill', level: () => 'My Level', grade: (h) => `Grade ${h.grade}`, review: () => 'Review', practice: (h) => `Practice (${SKILL[h.skill]?.name || ''})` };
# CN: drill: (h) => h.count ? `${h.count}题练习` : '练习', level: () => '我的等级', grade: (h) => `${h.grade}年级`, review: () => '错题复习', practice: (h) => `专项练习 (${SKILL[h.skill]?.name || ''})`
# TW: drill: (h) => h.count ? `${h.count}題練習` : '練習', level: () => '我的等級', grade: (h) => `${h.grade}年級`, review: () => '錯題複習', practice: (h) => `專項練習 (${SKILL[h.skill]?.name || ''})`

# Lang switcher:
# if (!target || target === 'zh-CN') return;
# location.replace(`../${target}/`);

def make_main(is_tw=False):
    c = text
    if is_tw:
        c = c.replace("const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];",
                      "const MONTHS = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];")
        c = c.replace("const fmtDay = (key) => { const [, m, d] = key.split('-').map(Number); return `${MONTHS[m - 1].slice(0, 3)} ${d}`; };",
                      "const fmtDay = (key) => { const [, m, d] = key.split('-').map(Number); return `${m}月${d}日`; };")
        c = c.replace("const nOf = (n, one, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;",
                      "const nOf = (n, one, many) => `${n} 個${one}`;")
        c = c.replace("const listJoin = (a) => (a.length < 2 ? a.join('') : `${a.slice(0, -1).join(', ')} and ${a[a.length - 1]}`);",
                      "const listJoin = (a) => (a.length < 2 ? a.join('') : `${a.slice(0, -1).join('、')}與${a[a.length - 1]}`);")
        
        # sound toggle
        c = c.replace("b.querySelector('b').textContent = m ? 'Off' : 'On';", "b.querySelector('b').textContent = m ? '關閉' : '開啟';")
        c = c.replace("$('#mute').setAttribute('aria-label', m ? 'Unmute' : 'Mute');", "$('#mute').setAttribute('aria-label', m ? '取消靜音' : '靜音');")
        
        # si-stars / si-next / si-note
        c = c.replace("${starRow(n)}<span>☆${n} / ${STAR_MAX}</span>", "${starRow(n)}<span>☆${n} / ${STAR_MAX}</span>")
        c = c.replace("`Next: ☆${next.n}`", "`下一階段：☆${next.n}`")
        c = c.replace("<p class=\"si-text done\">☆5 reached! Amazing!</p>", "<p class=\"si-text done\">已達成最高 ☆5！太出色了！</p>")
        c = c.replace("'A little rusty! One first-try answer makes it shine. '", "'有些生疏了！一次作答正確即可重新點亮。'")
        c = c.replace("` · Fastest: ${(best / 1000).toFixed(1)}s`", "` · 最快紀錄：${(best / 1000).toFixed(1)}秒`")
        c = c.replace("`Solved: ${r.n || 0}", "`已完成：${r.n || 0}題")

        # askRelock
        c = c.replace("toast('No records to erase yet');", "toast('目前尚無可重置的記錄');")
        c = c.replace("title: 'Erase skill',", "title: '重置單元記錄',")
        c = c.replace("`This erases your records for \"${SKILL[id].name}\".${deps ? `<br>The <b>${deps}</b> ${deps === 1 ? 'skill that builds' : 'skills that build'} on it will be erased and locked again too.` : ''}`",
                      "`將重置「${SKILL[id].name}」的全部練習記錄。${deps ? `<br>受其影響的 <b>${deps}</b> 個後續單元也將一併重置並重新鎖定。` : ''}`")
        c = c.replace("yes: 'Erase', no: 'Cancel',", "yes: '確認重置', no: '取消',")
        c = c.replace("toast(`Erased ${nOf(gone.length, 'skill')}`);", "toast(`已重置 ${gone.length} 個單元`);")

        # askToTitle
        c = c.replace("title: 'Back to the title?',", "title: '返回主畫面？',")
        c = c.replace("msg: playing ? 'This play will end here.' : \"You'll go back to the title screen.\",",
                      "msg: playing ? '當前挑戰進度將在此結束。' : '確定要返回主畫面嗎？',")
        c = c.replace("yes: 'Go back', no: playing ? 'Keep playing' : 'Stay here', danger: playing,",
                      "yes: '返回', no: playing ? '繼續挑戰' : '留在這裡', danger: playing,")

        # MODE_NAMES
        c = c.replace("const MODE_NAMES = { drill: (h) => h.count ? `${h.count}-problem drill` : 'Drill', level: () => 'My Level', grade: (h) => `Grade ${h.grade}`, review: () => 'Review', practice: (h) => `Practice (${SKILL[h.skill]?.name || ''})` };",
                      "const MODE_NAMES = { drill: (h) => h.count ? `${h.count}題練習` : '練習', level: () => '我的等級', grade: (h) => `${h.grade}年級`, review: () => '錯題複習', practice: (h) => `專項練習 (${SKILL[h.skill]?.name || ''})` };")

        # Calendar
        c = c.replace("${MONTHS[m]} ${y}", "${y}年 ${MONTHS[m]}")
        c = c.replace("` : `${MONTHS[m]} ${d}`;", "` : `${m + 1}月${d}日`;")
        c = c.replace("`SAVED`", "`補簽`")
        c = c.replace("'<span class=\"nc\">SAVED</span>'", "'<span class=\"nc\">補簽</span>'")
        c = c.replace("label = info ? `${MONTHS[m]} ${d}: ${nOf(info.plays, 'play')}, best ${info.best} pts${questDays[key] ? ', quests complete' : ''}`",
                      "label = info ? `${m + 1}月${d}日: 完成 ${info.plays} 輪, 最高 ${info.best} 分${questDays[key] ? ', 今日任務全通關' : ''}`")

        # Growth
        c = c.replace("el.innerHTML = `<p class=\"gb-head\">${'You improved!'}</p>", "el.innerHTML = `<p class=\"gb-head\">自我成長！進步了！</p>")
        c = c.replace("const when = (x) => (x.kind === 'first' ? `First (${fmtDay(x.d)})` : growth.daysBetween(x.d, today) === 1 ? 'Yesterday' : fmtDay(x.d));",
                      "const when = (x) => (x.kind === 'first' ? `初次（${fmtDay(x.d)}）` : growth.daysBetween(x.d, today) === 1 ? '昨天' : fmtDay(x.d));")
        c = c.replace("const val = (what, v) => (what === 'time' ? `${Math.max(0.1, v / 1000).toFixed(1)}s` : `${Math.round(v * 100)}%`);",
                      "const val = (what, v) => (what === 'time' ? `${Math.max(0.1, v / 1000).toFixed(1)}秒` : `${Math.round(v * 100)}%`);")
        c = c.replace("x.what === 'time' ? 'Per problem' : 'First try'", "x.what === 'time' ? '每題用時' : '初次正確率'")
        c = c.replace("<small>${'Today'}</small>", "<small>今日</small>")

        # Skill News
        c = c.replace("`<b>Time capsule</b>${S.capsuleNews}`", "`<b>時光膠囊</b>${S.capsuleNews}`")
        c = c.replace("`Polished! ${SKILL[id].name}`", "`重煥光芒！${SKILL[id].name}`")
        c = c.replace("`Now ☆${n}! ${SKILL[id].name}`", "`升至 ☆${n}！${SKILL[id].name}`")
        c = c.replace("`Mastered! ${SKILL[id].name}`", "`已精通！${SKILL[id].name}`")
        c = c.replace("`Unlocked! ${SKILL[id].name}`", "`已解鎖！${SKILL[id].name}`")
        c = c.replace("`Skill check done: ${SKILLS.filter((x) => stateOf(progress(), x.id) === 'mastered').length} cleared`",
                      "`實力測試完成：直接掌握 ${SKILLS.filter((x) => stateOf(progress(), x.id) === 'mastered').length} 個單元`")
        c = c.replace("btn.textContent = `Redo ${nOf(n, 'missed problem')}`;", "btn.textContent = `重做 ${n} 道錯題`;")

        # Title Sub
        c = c.replace("prog.placed ? `Next: \"${SKILL[frontier(prog)[0] || ORDER[ORDER.length - 1]].name}\"` : 'Starts with a skill check'",
                      "prog.placed ? `下一單元：「${SKILL[frontier(prog)[0] || ORDER[ORDER.length - 1]].name}」` : '初次遊玩先進行實力測試'")

        # Over goal clock label
        c = c.replace("$('#clock-label').textContent = 'Over goal';", "$('#clock-label').textContent = '超出目標用時';")

        # Collection & Hammer
        c = c.replace("'Shuffle'", "'隨機輪換'")
        c = c.replace("'Changes every play'", "'每輪隨機使用已解鎖物品'")
        c = c.replace("auto ? '\"Shuffle\" picks a different one you own every play' : 'Your pick is used every time'",
                      "auto ? '「隨機輪換」將在每輪自動隨機使用已解鎖的特效' : '已鎖定使用你當前選中的特效'")
        c = c.replace("`Trophy: ${tro ? tro.name : ''}`", "`成就：${tro ? tro.name : ''}`")
        c = c.replace("`This erases all records, skills, trophies, collection items, stickers and settings.`",
                      "`此操作將清除所有練習記錄、技能星級、成就獎盃、收藏品與自訂設定。`")
        c = c.replace("`Really erase everything?`", "`真的要全部清除嗎？`")
        c = c.replace("`Once it's erased, it can't be brought back.`", "`清除後所有進度將無法復原，請再次確認。`")
        c = c.replace("yes: 'Erase all', no: 'Cancel',", "yes: '確認全部清除', no: '取消',")
        c = c.replace("title: 'Reset everything',", "title: '清除所有資料',")

        # Hammer texts
        c = c.replace("`You didn't play on ${days}.<br>Stamp ${offer.days.length > 1 ? 'them' : 'it'} <b>SAVED</b>,<br>and your <b>${offer.run}</b>-day streak goes on!`",
                      "`${days}那天沒有練習算術。<br>使用補簽槌蓋上<b>補簽</b>印章，<br>即可延續連續 <b>${offer.run}</b> 天的打卡紀錄！`")
        c = c.replace("'Your hammers'", "'持有補簽槌'")
        c = c.replace("`Use ${nOf(offer.days.length, 'hammer')}`", "`使用 ${offer.days.length} 支補簽槌`")
        c = c.replace("`${offer.run}-day streak saved!`", "`連續 ${offer.run} 天打卡紀錄已保住！`")

        # Lang select event: target check
        c = c.replace("if (!target || target === 'en') return;", "if (!target || target === 'zh-TW') return;")
    else:
        c = c.replace("const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];",
                      "const MONTHS = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];")
        c = c.replace("const fmtDay = (key) => { const [, m, d] = key.split('-').map(Number); return `${MONTHS[m - 1].slice(0, 3)} ${d}`; };",
                      "const fmtDay = (key) => { const [, m, d] = key.split('-').map(Number); return `${m}月${d}日`; };")
        c = c.replace("const nOf = (n, one, many = `${one}s`) => `${n} ${n === 1 ? one : many}`;",
                      "const nOf = (n, one, many) => `${n} 个${one}`;")
        c = c.replace("const listJoin = (a) => (a.length < 2 ? a.join('') : `${a.slice(0, -1).join(', ')} and ${a[a.length - 1]}`);",
                      "const listJoin = (a) => (a.length < 2 ? a.join('') : `${a.slice(0, -1).join('、')}与${a[a.length - 1]}`);")
        
        # sound toggle
        c = c.replace("b.querySelector('b').textContent = m ? 'Off' : 'On';", "b.querySelector('b').textContent = m ? '关闭' : '开启';")
        c = c.replace("$('#mute').setAttribute('aria-label', m ? 'Unmute' : 'Mute');", "$('#mute').setAttribute('aria-label', m ? '取消静音' : '静音');")
        
        # si-stars / si-next / si-note
        c = c.replace("${starRow(n)}<span>☆${n} / ${STAR_MAX}</span>", "${starRow(n)}<span>☆${n} / ${STAR_MAX}</span>")
        c = c.replace("`Next: ☆${next.n}`", "`下一阶段：☆${next.n}`")
        c = c.replace("<p class=\"si-text done\">☆5 reached! Amazing!</p>", "<p class=\"si-text done\">已达成最高 ☆5！太出色了！</p>")
        c = c.replace("'A little rusty! One first-try answer makes it shine. '", "'有些生疏了！一次作答正确即可重新点亮。'")
        c = c.replace("` · Fastest: ${(best / 1000).toFixed(1)}s`", "` · 最快纪录：${(best / 1000).toFixed(1)}秒`")
        c = c.replace("`Solved: ${r.n || 0}", "`已完成：${r.n || 0}题")

        # askRelock
        c = c.replace("toast('No records to erase yet');", "toast('目前尚无可重置的记录');")
        c = c.replace("title: 'Erase skill',", "title: '重置技能记录',")
        c = c.replace("`This erases your records for \"${SKILL[id].name}\".${deps ? `<br>The <b>${deps}</b> ${deps === 1 ? 'skill that builds' : 'skills that build'} on it will be erased and locked again too.` : ''}`",
                      "`将重置「${SKILL[id].name}」的全部练习记录。${deps ? `<br>受其影响的 <b>${deps}</b> 个后续技能也将一并重置并重新锁定。` : ''}`")
        c = c.replace("yes: 'Erase', no: 'Cancel',", "yes: '确认重置', no: '取消',")
        c = c.replace("toast(`Erased ${nOf(gone.length, 'skill')}`);", "toast(`已重置 ${gone.length} 个技能`);")

        # askToTitle
        c = c.replace("title: 'Back to the title?',", "title: '返回主标题？',")
        c = c.replace("msg: playing ? 'This play will end here.' : \"You'll go back to the title screen.\",",
                      "msg: playing ? '当前挑战进度将在此结束。' : '确定要返回主页面吗？',")
        c = c.replace("yes: 'Go back', no: playing ? 'Keep playing' : 'Stay here', danger: playing,",
                      "yes: '返回', no: playing ? '继续挑战' : '留在当前', danger: playing,")

        # MODE_NAMES
        c = c.replace("const MODE_NAMES = { drill: (h) => h.count ? `${h.count}-problem drill` : 'Drill', level: () => 'My Level', grade: (h) => `Grade ${h.grade}`, review: () => 'Review', practice: (h) => `Practice (${SKILL[h.skill]?.name || ''})` };",
                      "const MODE_NAMES = { drill: (h) => h.count ? `${h.count}题练习` : '练习', level: () => '我的等级', grade: (h) => `${h.grade}年级`, review: () => '错题复习', practice: (h) => `专项练习 (${SKILL[h.skill]?.name || ''})` };")

        # Calendar
        c = c.replace("${MONTHS[m]} ${y}", "${y}年 ${MONTHS[m]}")
        c = c.replace("` : `${MONTHS[m]} ${d}`;", "` : `${m + 1}月${d}日`;")
        c = c.replace("`SAVED`", "`补签`")
        c = c.replace("'<span class=\"nc\">SAVED</span>'", "'<span class=\"nc\">补签</span>'")
        c = c.replace("label = info ? `${MONTHS[m]} ${d}: ${nOf(info.plays, 'play')}, best ${info.best} pts${questDays[key] ? ', quests complete' : ''}`",
                      "label = info ? `${m + 1}月${d}日: 完成 ${info.plays} 轮, 最高 ${info.best} 分${questDays[key] ? ', 今日任务全通关' : ''}`")

        # Growth
        c = c.replace("el.innerHTML = `<p class=\"gb-head\">${'You improved!'}</p>", "el.innerHTML = `<p class=\"gb-head\">自我成长！进步了！</p>")
        c = c.replace("const when = (x) => (x.kind === 'first' ? `First (${fmtDay(x.d)})` : growth.daysBetween(x.d, today) === 1 ? 'Yesterday' : fmtDay(x.d));",
                      "const when = (x) => (x.kind === 'first' ? `初次（${fmtDay(x.d)}）` : growth.daysBetween(x.d, today) === 1 ? '昨天' : fmtDay(x.d));")
        c = c.replace("const val = (what, v) => (what === 'time' ? `${Math.max(0.1, v / 1000).toFixed(1)}s` : `${Math.round(v * 100)}%`);",
                      "const val = (what, v) => (what === 'time' ? `${Math.max(0.1, v / 1000).toFixed(1)}秒` : `${Math.round(v * 100)}%`);")
        c = c.replace("x.what === 'time' ? 'Per problem' : 'First try'", "x.what === 'time' ? '每题用时' : '初次正确率'")
        c = c.replace("<small>${'Today'}</small>", "<small>今日</small>")

        # Skill News
        c = c.replace("`<b>Time capsule</b>${S.capsuleNews}`", "`<b>时光胶囊</b>${S.capsuleNews}`")
        c = c.replace("`Polished! ${SKILL[id].name}`", "`重焕光彩！${SKILL[id].name}`")
        c = c.replace("`Now ☆${n}! ${SKILL[id].name}`", "`升至 ☆${n}！${SKILL[id].name}`")
        c = c.replace("`Mastered! ${SKILL[id].name}`", "`已精通！${SKILL[id].name}`")
        c = c.replace("`Unlocked! ${SKILL[id].name}`", "`已解锁！${SKILL[id].name}`")
        c = c.replace("`Skill check done: ${SKILLS.filter((x) => stateOf(progress(), x.id) === 'mastered').length} cleared`",
                      "`实力测试完成：直接掌握 ${SKILLS.filter((x) => stateOf(progress(), x.id) === 'mastered').length} 项技能`")
        c = c.replace("btn.textContent = `Redo ${nOf(n, 'missed problem')}`;", "btn.textContent = `重做 ${n} 道错题`;")

        # Title Sub
        c = c.replace("prog.placed ? `Next: \"${SKILL[frontier(prog)[0] || ORDER[ORDER.length - 1]].name}\"` : 'Starts with a skill check'",
                      "prog.placed ? `下一技能：「${SKILL[frontier(prog)[0] || ORDER[ORDER.length - 1]].name}」` : '初次进入先进行实力测试'")

        # Over goal clock label
        c = c.replace("$('#clock-label').textContent = 'Over goal';", "$('#clock-label').textContent = '超出目标用时';")

        # Collection & Hammer
        c = c.replace("'Shuffle'", "'随机轮换'")
        c = c.replace("'Changes every play'", "'每轮随机使用已解锁物品'")
        c = c.replace("auto ? '\"Shuffle\" picks a different one you own every play' : 'Your pick is used every time'",
                      "auto ? '「随机轮换」将在每轮自动随机使用已解锁的特效' : '已锁定使用你当前选中的特效'")
        c = c.replace("`Trophy: ${tro ? tro.name : ''}`", "`成就：${tro ? tro.name : ''}`")
        c = c.replace("`This erases all records, skills, trophies, collection items, stickers and settings.`",
                      "`此操作将清除所有练习记录、技能星级、成就奖杯、收藏品与个性化设置。`")
        c = c.replace("`Really erase everything?`", "`真的要全部清除吗？`")
        c = c.replace("`Once it's erased, it can't be brought back.`", "`清除后所有数据将彻底无法找回，请再次确认。`")
        c = c.replace("yes: 'Erase all', no: 'Cancel',", "yes: '确认全部清除', no: '取消',")
        c = c.replace("title: 'Reset everything',", "title: '清除所有数据',")

        # Hammer texts
        c = c.replace("`You didn't play on ${days}.<br>Stamp ${offer.days.length > 1 ? 'them' : 'it'} <b>SAVED</b>,<br>and your <b>${offer.run}</b>-day streak goes on!`",
                      "`${days}那天没有练习算术。<br>使用补签锤盖上<b>补签</b>印章，<br>即可延续连续 <b>${offer.run}</b> 天的打卡纪录！`")
        c = c.replace("'Your hammers'", "'持有补签锤'")
        c = c.replace("`Use ${nOf(offer.days.length, 'hammer')}`", "`使用 ${offer.days.length} 支补签锤`")
        c = c.replace("`${offer.run}-day streak saved!`", "`连续 ${offer.run} 天打卡纪录已保住！`")

        # Lang select event: target check
        c = c.replace("if (!target || target === 'en') return;", "if (!target || target === 'zh-CN') return;")

    return c

with open('app/zh-CN/js/main.js', 'w', encoding='utf-8') as f:
    f.write(make_main(False))
with open('app/zh-TW/js/main.js', 'w', encoding='utf-8') as f:
    f.write(make_main(True))

print("Updated main.js for zh-CN and zh-TW")
