import re

with open('app/en/js/main.js', 'r', encoding='utf-8') as f:
    en_main = f.read()

def generate_main(is_tw=False):
    c = en_main
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

        # MODE_NAMES and MODE_LABEL
        c = c.replace("const MODE_NAMES = { drill: (h) => h.count ? `${h.count}-problem drill` : 'Drill', level: () => 'My Level', grade: (h) => `Grade ${h.grade}`, review: () => 'Review', practice: (h) => `Practice (${SKILL[h.skill]?.name || ''})` };",
                      "const MODE_NAMES = { drill: (h) => h.count ? `${h.count}題練習` : '練習', level: () => '我的等級', grade: (h) => `${h.grade}年級`, review: () => '錯題複習', practice: (h) => `專項練習 (${SKILL[h.skill]?.name || ''})` };")
        c = c.replace("const MODE_LABEL = { level: 'My Level', grade: (g) => `Grade ${g}`, review: 'Review', practice: 'Practice', drill: 'Drill' };",
                      "const MODE_LABEL = { level: '我的等級', grade: (g) => `${g}年級`, review: '錯題複習', practice: '專項練習', drill: '綜合練習' };")

        # Quests
        c = c.replace('if (q.rewarded) return \'<b class="qdone">Complete!</b>\';',
                      'if (q.rewarded) return \'<b class="qdone">全部完成！</b>\';')
        c = c.replace('return `Clear all: <i class="qham">${HAMMER_SVG}</i>+1`;',
                      'return `全部通關：<i class="qham">${HAMMER_SVG}</i>+1`;')
        c = c.replace('el.innerHTML = `<p class="qm-head">${"Today\'s quests"} <span>${questRewardText(q)}</span></p><ol class="quest-list">${questRows(q.list)}</ol>${got ? `<p class="qm-got">${got.hammer ? `<i class="qham">${HAMMER_SVG}</i>You got a Streak Hammer!` : "Your hammers are full! Let\'s just celebrate."}</p>` : \'\'}`;',
                      'el.innerHTML = `<p class="qm-head">今日任務 <span>${questRewardText(q)}</span></p><ol class="quest-list">${questRows(q.list)}</ol>${got ? `<p class="qm-got">${got.hammer ? `<i class="qham">${HAMMER_SVG}</i>獲得了 1 支打卡補簽槌！` : "補簽槌已滿！盡情慶祝吧！"}</p>` : \'\'}`;')
        c = c.replace("el.innerHTML = q ? `<b>Quest clear!</b><span>${qs.questText(q)}</span>` : '<b>All quests complete!</b>';",
                      "el.innerHTML = q ? `<b>任務達成！</b><span>${qs.questText(q)}</span>` : '<b>今日任務全部達成！</b>';")

        # Play screen
        c = c.replace("$('#clock-label').textContent = `Goal ${fmtTime(S.targetMs)}`;",
                      "$('#clock-label').textContent = `目標 ${fmtTime(S.targetMs)}`;")
        c = c.replace("$('#clock-label').textContent = 'Left';",
                      "$('#clock-label').textContent = '剩餘時間';")
        c = c.replace("$('#clock-label').textContent = 'Over goal';",
                      "$('#clock-label').textContent = '超出目標用時';")
        c = c.replace("cutin(extra ? `EX ${S.extra.solved + 1}` : last ? 'Last one!' : `Q${S.qi + 1}`, E);",
                      "cutin(extra ? `EX ${S.extra.solved + 1}` : last ? '最後一題！' : `Q${S.qi + 1}`, E);")
        c = c.replace("bigStamp(\"Time's up!\");", "bigStamp('時間到！');")

        # Result screen
        c = c.replace("$('#result-title').textContent = review ? 'Review clear!' : `${modeName(S.plan)} clear!`;",
                      "$('#result-title').textContent = review ? '錯題複習通關！' : `${modeName(S.plan)} 通關！`;")
        c = c.replace("un.textContent = review ? '' : ok ? 'Extra unlocked!' : 'A first-try rate of 80% or more unlocks Extra';",
                      "un.textContent = review ? '' : ok ? 'Extra 加分挑戰已解鎖！' : '初次正確率達到 80% 以上即可進入 Extra 挑戰';")
        c = c.replace("$('#go-extra small').textContent = `${Math.round(EXTRA_MS / 1000)} seconds`;",
                      "$('#go-extra small').textContent = `限時 ${Math.round(EXTRA_MS / 1000)} 秒`;")
        c = c.replace("$('#f-break').textContent = `Basic ${BASIC_SCORE} + Extra ${S.extra.score.toLocaleString('en-US')}`;",
                      "$('#f-break').textContent = `基礎關 ${BASIC_SCORE} + Extra ${S.extra.score.toLocaleString('zh-TW')}`;")
        c = c.replace("btn.textContent = `Redo ${nOf(n, 'missed problem')}`;", "btn.textContent = `重做 ${n} 道錯題`;")

        # Growth & Time capsule
        c = c.replace("el.innerHTML = `<p class=\"gb-head\">${'You improved!'}</p>", "el.innerHTML = `<p class=\"gb-head\">自我成長！進步了！</p>")
        c = c.replace("const when = (x) => (x.kind === 'first' ? `First (${fmtDay(x.d)})` : growth.daysBetween(x.d, today) === 1 ? 'Yesterday' : fmtDay(x.d));",
                      "const when = (x) => (x.kind === 'first' ? `初次（${fmtDay(x.d)}）` : growth.daysBetween(x.d, today) === 1 ? '昨天' : fmtDay(x.d));")
        c = c.replace("const val = (what, v) => (what === 'time' ? `${Math.max(0.1, v / 1000).toFixed(1)}s` : `${Math.round(v * 100)}%`);",
                      "const val = (what, v) => (what === 'time' ? `${Math.max(0.1, v / 1000).toFixed(1)}秒` : `${Math.round(v * 100)}%`);")
        c = c.replace("x.what === 'time' ? 'Per problem' : 'First try'", "x.what === 'time' ? '每題用時' : '初次正確率'")
        c = c.replace("<small>${'Today'}</small>", "<small>今日</small>")
        c = c.replace("cmp.what === 'none' ? `<small>TIME CAPSULE</small><b>From ${day}</b><span>Solved it again!</span>`",
                      "cmp.what === 'none' ? `<small>時光膠囊</small><b>來自 ${day}</b><span>再次成功解出！</span>`")
        c = c.replace("`<small>TIME CAPSULE</small><span class=\"cr-row\"><span class=\"cr-old\"><i>Then</i>${cmp.what === 'time' ? sec(cmp.from) : `Oops ${cmp.from}`}</span><span class=\"cr-arrow\">→</span><span class=\"cr-new\"><i>Today</i>${cmp.what === 'time' ? sec(cmp.to) : `Oops ${cmp.to}`}</span></span>`",
                      "`<small>時光膠囊</small><span class=\"cr-row\"><span class=\"cr-old\"><i>當時</i>${cmp.what === 'time' ? sec(cmp.from) : `失誤 ${cmp.from}`}</span><span class=\"cr-arrow\">→</span><span class=\"cr-new\"><i>今日</i>${cmp.what === 'time' ? sec(cmp.to) : `失誤 ${cmp.to}`}</span></span>`")
        c = c.replace("const line = cmp.what === 'time' ? `${day} ${sec(cmp.from)} → today ${sec(cmp.to)}` : cmp.what === 'miss' ? `Oops: ${day} ${cmp.from} → today ${cmp.to}` : `Solved the problem from ${day} again`;",
                      "const line = cmp.what === 'time' ? `${day} ${sec(cmp.from)} → 今日 ${sec(cmp.to)}` : cmp.what === 'miss' ? `失誤：${day} ${cmp.from} → 今日 ${cmp.to}` : `再次成功解出 ${day} 的題目`;")
        c = c.replace("`<b>Time capsule</b>${S.capsuleNews}`", "`<b>時光膠囊</b>${S.capsuleNews}`")
        c = c.replace("`Polished! ${SKILL[id].name}`", "`重煥光彩！${SKILL[id].name}`")
        c = c.replace("`Now ☆${n}! ${SKILL[id].name}`", "`升至 ☆${n}！${SKILL[id].name}`")
        c = c.replace("`Mastered! ${SKILL[id].name}`", "`已精通！${SKILL[id].name}`")
        c = c.replace("`Unlocked! ${SKILL[id].name}`", "`已解鎖！${SKILL[id].name}`")
        c = c.replace("`Skill check done: ${SKILLS.filter((x) => stateOf(progress(), x.id) === 'mastered').length} cleared`",
                      "`實力測試完成：直接掌握 ${SKILLS.filter((x) => stateOf(progress(), x.id) === 'mastered').length} 項技能`")

        # Tree render
        c = c.replace("const name = sk.name.replace(/\\S+-\\S+/g, (w) => `<span class=\"nw\">${w}</span>`);\n    b.innerHTML = `<i class=\"hold\"></i><span class=\"g\">${`Grade ${sk.grade}`}</span><span>${name}</span>${st === 'learning' ? '<i class=\"ring\"></i>' : ''}${st === 'mastered' ? `<i class=\"stars s${stars}\">${starRow(stars)}</i>` : ''}${rusty ? '<i class=\"rust\" aria-hidden=\"true\">rust</i>' : ''}`;",
                      "const name = sk.name.replace(/\\S+-\\S+/g, (w) => `<span class=\"nw\">${w}</span>`);\n    b.innerHTML = `<i class=\"hold\"></i><span class=\"g\">${sk.grade}年級</span><span>${name}</span>${st === 'learning' ? '<i class=\"ring\"></i>' : ''}${st === 'mastered' ? `<i class=\"stars s${stars}\">${starRow(stars)}</i>` : ''}${rusty ? '<i class=\"rust\" aria-hidden=\"true\">生疏</i>' : ''}`;")
        c = c.replace("b.setAttribute('aria-label', `${sk.name}: ${{ locked: 'locked', new: 'new', learning: 'learning', mastered: `mastered, ${nOf(stars, 'star')}${rusty ? ', rusty' : ''}` }[st]}`);",
                      "b.setAttribute('aria-label', `${sk.name}: ${{ locked: '未解鎖', new: '新技能', learning: '練習中', mastered: `已掌握, ${stars}星${rusty ? ', 需要複習' : ''}` }[st]}`);")

        # Calendar & Badges
        c = c.replace("${MONTHS[m]} ${y}", "${y}年 ${MONTHS[m]}")
        c = c.replace("` : `${MONTHS[m]} ${d}`;", "` : `${m + 1}月${d}日`;")
        c = c.replace("`SAVED`", "`補簽`")
        c = c.replace("'<span class=\"nc\">SAVED</span>'", "'<span class=\"nc\">補簽</span>'")
        c = c.replace("label = info ? `${MONTHS[m]} ${d}: ${nOf(info.plays, 'play')}, best ${info.best} pts${questDays[key] ? ', quests complete' : ''}`",
                      "label = info ? `${m + 1}月${d}日: 完成 ${info.plays} 輪, 最高 ${info.best} 分${questDays[key] ? ', 今日任務全通關' : ''}`")
        c = c.replace("if (n >= 1) badges.push(`<span class=\"cal-badge${n >= 3 ? ' hot' : ''}\">${`Streak<b>${n}</b>${n === 1 ? 'day' : 'days'}${playedToday ? '' : ` (today makes ${n + 1})`}`}</span>`);\n  else badges.push('<span class=\"cal-badge\">Start a streak today!</span>');\n  if (best >= 2) badges.push(`<span class=\"cal-badge best\">${`Best<b>${best}</b>days`}</span>`);\n  if (bonus.total) badges.push(`<span class=\"cal-badge stk\">${`Stickers<b>${bonus.total}</b>`}</span>`);\n  const hammers = store.items().hammer;\n  badges.push(`<span class=\"cal-badge hmr\" aria-label=\"Streak Hammers: ${hammers}\"><i>${HAMMER_SVG}</i><b>${hammers}</b></span>`);",
                      "if (n >= 1) badges.push(`<span class=\"cal-badge${n >= 3 ? ' hot' : ''}\">連續打卡<b>${n}</b>天${playedToday ? '' : `（今天完成即達 ${n + 1} 天）`}</span>`);\n  else badges.push('<span class=\"cal-badge\">從今天開始連續打卡！</span>');\n  if (best >= 2) badges.push(`<span class=\"cal-badge best\">最高連續<b>${best}</b>天</span>`);\n  if (bonus.total) badges.push(`<span class=\"cal-badge stk\">簽到印章<b>${bonus.total}</b>個</span>`);\n  const hammers = store.items().hammer;\n  badges.push(`<span class=\"cal-badge hmr\" aria-label=\"補簽槌：${hammers}支\"><i>${HAMMER_SVG}</i><b>${hammers}</b></span>`);")

        # Bonus dialog
        c = c.replace("$('#bonus-run').innerHTML = res.run >= 2 ? `Day<b>${res.run}</b>in a row!` : \"Today\'s bonus\";",
                      "$('#bonus-run').innerHTML = res.run >= 2 ? `連續打卡第 <b>${res.run}</b> 天！` : '今日登入獎勵';")
        c = c.replace("slots.push(`<div class=\"bonus-slot${got ? ' got' : ''}${i === res.slot ? ' today stamping' : ''}${i === 7 ? ' big' : ''}\"><span class=\"d\">${`Day ${i}`}</span>${got ? stickerSvg(type) : i === 7 ? '?' : i}</div>`);",
                      "slots.push(`<div class=\"bonus-slot${got ? ' got' : ''}${i === res.slot ? ' today stamping' : ''}${i === 7 ? ' big' : ''}\"><span class=\"d\">第 ${i} 天</span>${got ? stickerSvg(type) : i === 7 ? '?' : i}</div>`);")
        c = c.replace("$('#bonus-note').textContent = res.slot === 7 ? \"Special sticker! It's on your calendar.\" : `${nOf(7 - res.slot, 'more day')} to a special sticker`;",
                      "$('#bonus-note').textContent = res.slot === 7 ? '獲得特別紀念印章！已蓋在你的日曆上。' : `再連續簽到 ${7 - res.slot} 天即可獲得特別紀念印章`;")

        # Trophies Dialog & List
        c = c.replace("$('#tg-title').textContent = 'New trophy!';", "$('#tg-title').textContent = '解鎖新成就！';")
        c = c.replace("$('#tg-sub').innerHTML = batch.length ? `<b>${batch.length}</b> earned from your past play!` : list.length > 1 ? `You earned <b>${list.length}</b>!` : '';",
                      "$('#tg-sub').innerHTML = batch.length ? `根據過往練習直接獲得 <b>${batch.length}</b> 項成就！` : list.length > 1 ? `獲得了 <b>${list.length}</b> 項新成就！` : '';")
        c = c.replace("+ rewards.map((it) => `<li class=\"reward\"><i>${itemThumb(it)}</i><span>${`<b>You got \"${it.name}\" (${catName(it.cat)})!</b><small>Pick it in the Collection</small>`}</span></li>`).join('');",
                      "+ rewards.map((it) => `<li class=\"reward\"><i>${itemThumb(it)}</i><span><b>獲得了特效「${it.name}」(${catName(it.cat)})！</b><small>可前往圖鑑收藏中選用</small></span></li>`).join('');")
        c = c.replace("const next = v.next ? `<span class=\"tr-next\">${`Next: ${secret ? '???' : v.next.name}${!secret && trophyValueText(v.next, v.value) ? ` (${trophyValueText(v.next, v.value)})` : ''}`}</span>` : '<span class=\"tr-next done\">Complete!</span>';",
                      "const next = v.next ? `<span class=\"tr-next\">下一目標：${secret ? '???' : v.next.name}${!secret && trophyValueText(v.next, v.value) ? ` (${trophyValueText(v.next, v.value)})` : ''}</span>` : '<span class=\"tr-next done\">全部完成！</span>';")
        c = c.replace("<small class=\"rw\">Reward: ${catName(rw.cat)} \"${rw.name}\"</small>",
                      "<small class=\"rw\">獎勵：${catName(rw.cat)}「${rw.name}」</small>")
        c = c.replace("<small>${hide ? 'Secret trophy' : x.desc}</small>",
                      "<small>${hide ? '隱藏成就' : x.desc}</small>")
        c = c.replace("$('#tr-list').innerHTML = html || '<p class=\"tr-empty\">Nothing here yet</p>';",
                      "$('#tr-list').innerHTML = html || '<p class=\"tr-empty\">暫無內容</p>';")

        # Collection
        c = c.replace("'Shuffle'", "'隨機輪換'")
        c = c.replace("'Changes every play'", "'每輪隨機使用已解鎖物品'")
        c = c.replace("auto ? '\"Shuffle\" picks a different one you own every play' : 'Your pick is used every time'",
                      "auto ? '「隨機輪換」將在每輪自動隨機使用已解鎖的特效' : '已鎖定使用你當前選中的特效'")
        c = c.replace("`Trophy: ${tro ? tro.name : ''}`", "`成就：${tro ? tro.name : ''}`")
        c = c.replace("${own ? '' : ` aria-label=\"Locked. Earn the trophy &quot;${tro ? tro.name : ''}&quot; to get it\"`}",
                      "${own ? '' : ` aria-label=\"未解鎖。達成成就「${tro ? tro.name : ''}」即可獲得\"`}")
        c = c.replace("<small class=\"co-lock\">Trophy: ${tro ? tro.name : ''}</small>",
                      "<small class=\"co-lock\">成就：${tro ? tro.name : ''}</small>")
        c = c.replace("`This erases all records, skills, trophies, collection items, stickers and settings.`",
                      "`此操作將清除所有練習記錄、技能星級、成就獎盃、收藏品與個性化設定。`")
        c = c.replace("`Really erase everything?`", "`真的要全部清除嗎？`")
        c = c.replace("`Once it's erased, it can't be brought back.`", "`清除後所有資料將徹底無法找回，請再次確認。`")
        c = c.replace("yes: 'Erase all', no: 'Cancel',", "yes: '確認全部清除', no: '取消',")
        c = c.replace("title: 'Reset everything',", "title: '清除所有資料',")

        # Hammer texts
        c = c.replace("`You didn't play on ${days}.<br>Stamp ${offer.days.length > 1 ? 'them' : 'it'} <b>SAVED</b>,<br>and your <b>${offer.run}</b>-day streak goes on!`",
                      "`${days}那天沒有練習算術。<br>使用補簽槌蓋上<b>補簽</b>印章，<br>即可延續連續 <b>${offer.run}</b> 天的打卡紀錄！`")
        c = c.replace("'Your hammers'", "'持有補簽槌'")
        c = c.replace("`Use ${nOf(offer.days.length, 'hammer')}`", "`使用 ${offer.days.length} 支補簽槌`")
        c = c.replace("`${offer.run}-day streak saved!`", "`連續 ${offer.run} 天打卡紀錄已保住！`")

        # Day list
        c = c.replace("label: `${fmtDay(h.day)}: ${modeName(h)}, ${h.score || 0} pts, ${nOf(h.ok || 0, 'correct')}, ${nOf(h.ng || 0, 'miss', 'misses')}`",
                      "label: `${fmtDay(h.day)}: ${modeName(h)}, ${h.score || 0} 分, 答對 ${h.ok || 0} 題, 失誤 ${h.ng || 0} 次`")
        c = c.replace("`Correct ${h.ok ?? 0} · Oops ${h.ng ?? 0}${extra} · ${fmtTime(h.timeMs || 0)}`",
                      "`答對 ${h.ok ?? 0} 題 · 失誤 ${h.ng ?? 0} 次${extra} · 用時 ${fmtTime(h.timeMs || 0)}`")
        c = c.replace("` · Extra ${h.extraOk}`", "` · Extra 答對 ${h.extraOk} 題`")

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

        # MODE_NAMES and MODE_LABEL
        c = c.replace("const MODE_NAMES = { drill: (h) => h.count ? `${h.count}-problem drill` : 'Drill', level: () => 'My Level', grade: (h) => `Grade ${h.grade}`, review: () => 'Review', practice: (h) => `Practice (${SKILL[h.skill]?.name || ''})` };",
                      "const MODE_NAMES = { drill: (h) => h.count ? `${h.count}题练习` : '练习', level: () => '我的等级', grade: (h) => `${h.grade}年级`, review: () => '错题复习', practice: (h) => `专项练习 (${SKILL[h.skill]?.name || ''})` };")
        c = c.replace("const MODE_LABEL = { level: 'My Level', grade: (g) => `Grade ${g}`, review: 'Review', practice: 'Practice', drill: 'Drill' };",
                      "const MODE_LABEL = { level: '我的等级', grade: (g) => `${g}年级`, review: '错题复习', practice: '专项练习', drill: '综合练习' };")

        # Quests
        c = c.replace('if (q.rewarded) return \'<b class="qdone">Complete!</b>\';',
                      'if (q.rewarded) return \'<b class="qdone">全部完成！</b>\';')
        c = c.replace('return `Clear all: <i class="qham">${HAMMER_SVG}</i>+1`;',
                      'return `全部通关：<i class="qham">${HAMMER_SVG}</i>+1`;')
        c = c.replace('el.innerHTML = `<p class="qm-head">${"Today\'s quests"} <span>${questRewardText(q)}</span></p><ol class="quest-list">${questRows(q.list)}</ol>${got ? `<p class="qm-got">${got.hammer ? `<i class="qham">${HAMMER_SVG}</i>You got a Streak Hammer!` : "Your hammers are full! Let\'s just celebrate."}</p>` : \'\'}`;',
                      'el.innerHTML = `<p class="qm-head">今日任务 <span>${questRewardText(q)}</span></p><ol class="quest-list">${questRows(q.list)}</ol>${got ? `<p class="qm-got">${got.hammer ? `<i class="qham">${HAMMER_SVG}</i>获得了 1 支打卡补签锤！` : "补签锤已满！尽情庆祝吧！"}</p>` : \'\'}`;')
        c = c.replace("el.innerHTML = q ? `<b>Quest clear!</b><span>${qs.questText(q)}</span>` : '<b>All quests complete!</b>';",
                      "el.innerHTML = q ? `<b>任务达成！</b><span>${qs.questText(q)}</span>` : '<b>今日任务全部达成！</b>';")

        # Play screen
        c = c.replace("$('#clock-label').textContent = `Goal ${fmtTime(S.targetMs)}`;",
                      "$('#clock-label').textContent = `目标 ${fmtTime(S.targetMs)}`;")
        c = c.replace("$('#clock-label').textContent = 'Left';",
                      "$('#clock-label').textContent = '剩余时间';")
        c = c.replace("$('#clock-label').textContent = 'Over goal';",
                      "$('#clock-label').textContent = '超出目标用时';")
        c = c.replace("cutin(extra ? `EX ${S.extra.solved + 1}` : last ? 'Last one!' : `Q${S.qi + 1}`, E);",
                      "cutin(extra ? `EX ${S.extra.solved + 1}` : last ? '最后一题！' : `Q${S.qi + 1}`, E);")
        c = c.replace("bigStamp(\"Time's up!\");", "bigStamp('时间到！');")

        # Result screen
        c = c.replace("$('#result-title').textContent = review ? 'Review clear!' : `${modeName(S.plan)} clear!`;",
                      "$('#result-title').textContent = review ? '错题复习通关！' : `${modeName(S.plan)} 通关！`;")
        c = c.replace("un.textContent = review ? '' : ok ? 'Extra unlocked!' : 'A first-try rate of 80% or more unlocks Extra';",
                      "un.textContent = review ? '' : ok ? 'Extra 加分挑战已解锁！' : '初次正确率达到 80% 以上即可进入 Extra 挑战';")
        c = c.replace("$('#go-extra small').textContent = `${Math.round(EXTRA_MS / 1000)} seconds`;",
                      "$('#go-extra small').textContent = `限时 ${Math.round(EXTRA_MS / 1000)} 秒`;")
        c = c.replace("$('#f-break').textContent = `Basic ${BASIC_SCORE} + Extra ${S.extra.score.toLocaleString('en-US')}`;",
                      "$('#f-break').textContent = `基础关 ${BASIC_SCORE} + Extra ${S.extra.score.toLocaleString('zh-CN')}`;")
        c = c.replace("btn.textContent = `Redo ${nOf(n, 'missed problem')}`;", "btn.textContent = `重做 ${n} 道错题`;")

        # Growth & Time capsule
        c = c.replace("el.innerHTML = `<p class=\"gb-head\">${'You improved!'}</p>", "el.innerHTML = `<p class=\"gb-head\">自我成长！进步了！</p>")
        c = c.replace("const when = (x) => (x.kind === 'first' ? `First (${fmtDay(x.d)})` : growth.daysBetween(x.d, today) === 1 ? 'Yesterday' : fmtDay(x.d));",
                      "const when = (x) => (x.kind === 'first' ? `初次（${fmtDay(x.d)}）` : growth.daysBetween(x.d, today) === 1 ? '昨天' : fmtDay(x.d));")
        c = c.replace("const val = (what, v) => (what === 'time' ? `${Math.max(0.1, v / 1000).toFixed(1)}s` : `${Math.round(v * 100)}%`);",
                      "const val = (what, v) => (what === 'time' ? `${Math.max(0.1, v / 1000).toFixed(1)}秒` : `${Math.round(v * 100)}%`);")
        c = c.replace("x.what === 'time' ? 'Per problem' : 'First try'", "x.what === 'time' ? '每题用时' : '初次正确率'")
        c = c.replace("<small>${'Today'}</small>", "<small>今日</small>")
        c = c.replace("cmp.what === 'none' ? `<small>TIME CAPSULE</small><b>From ${day}</b><span>Solved it again!</span>`",
                      "cmp.what === 'none' ? `<small>时光胶囊</small><b>来自 ${day}</b><span>再次成功解出！</span>`")
        c = c.replace("`<small>TIME CAPSULE</small><span class=\"cr-row\"><span class=\"cr-old\"><i>Then</i>${cmp.what === 'time' ? sec(cmp.from) : `Oops ${cmp.from}`}</span><span class=\"cr-arrow\">→</span><span class=\"cr-new\"><i>Today</i>${cmp.what === 'time' ? sec(cmp.to) : `Oops ${cmp.to}`}</span></span>`",
                      "`<small>时光胶囊</small><span class=\"cr-row\"><span class=\"cr-old\"><i>当时</i>${cmp.what === 'time' ? sec(cmp.from) : `失误 ${cmp.from}`}</span><span class=\"cr-arrow\">→</span><span class=\"cr-new\"><i>今日</i>${cmp.what === 'time' ? sec(cmp.to) : `失误 ${cmp.to}`}</span></span>`")
        c = c.replace("const line = cmp.what === 'time' ? `${day} ${sec(cmp.from)} → today ${sec(cmp.to)}` : cmp.what === 'miss' ? `Oops: ${day} ${cmp.from} → today ${cmp.to}` : `Solved the problem from ${day} again`;",
                      "const line = cmp.what === 'time' ? `${day} ${sec(cmp.from)} → 今日 ${sec(cmp.to)}` : cmp.what === 'miss' ? `失误：${day} ${cmp.from} → 今日 ${cmp.to}` : `再次成功解出 ${day} 的题目`;")
        c = c.replace("`<b>Time capsule</b>${S.capsuleNews}`", "`<b>时光胶囊</b>${S.capsuleNews}`")
        c = c.replace("`Polished! ${SKILL[id].name}`", "`重焕光彩！${SKILL[id].name}`")
        c = c.replace("`Now ☆${n}! ${SKILL[id].name}`", "`升至 ☆${n}！${SKILL[id].name}`")
        c = c.replace("`Mastered! ${SKILL[id].name}`", "`已精通！${SKILL[id].name}`")
        c = c.replace("`Unlocked! ${SKILL[id].name}`", "`已解锁！${SKILL[id].name}`")
        c = c.replace("`Skill check done: ${SKILLS.filter((x) => stateOf(progress(), x.id) === 'mastered').length} cleared`",
                      "`实力测试完成：直接掌握 ${SKILLS.filter((x) => stateOf(progress(), x.id) === 'mastered').length} 项技能`")

        # Tree render
        c = c.replace("const name = sk.name.replace(/\\S+-\\S+/g, (w) => `<span class=\"nw\">${w}</span>`);\n    b.innerHTML = `<i class=\"hold\"></i><span class=\"g\">${`Grade ${sk.grade}`}</span><span>${name}</span>${st === 'learning' ? '<i class=\"ring\"></i>' : ''}${st === 'mastered' ? `<i class=\"stars s${stars}\">${starRow(stars)}</i>` : ''}${rusty ? '<i class=\"rust\" aria-hidden=\"true\">rust</i>' : ''}`;",
                      "const name = sk.name.replace(/\\S+-\\S+/g, (w) => `<span class=\"nw\">${w}</span>`);\n    b.innerHTML = `<i class=\"hold\"></i><span class=\"g\">${sk.grade}年级</span><span>${name}</span>${st === 'learning' ? '<i class=\"ring\"></i>' : ''}${st === 'mastered' ? `<i class=\"stars s${stars}\">${starRow(stars)}</i>` : ''}${rusty ? '<i class=\"rust\" aria-hidden=\"true\">生疏</i>' : ''}`;")
        c = c.replace("b.setAttribute('aria-label', `${sk.name}: ${{ locked: 'locked', new: 'new', learning: 'learning', mastered: `mastered, ${nOf(stars, 'star')}${rusty ? ', rusty' : ''}` }[st]}`);",
                      "b.setAttribute('aria-label', `${sk.name}: ${{ locked: '未解锁', new: '新技能', learning: '练习中', mastered: `已掌握, ${stars}星${rusty ? ', 需要复习' : ''}` }[st]}`);")

        # Calendar & Badges
        c = c.replace("${MONTHS[m]} ${y}", "${y}年 ${MONTHS[m]}")
        c = c.replace("` : `${MONTHS[m]} ${d}`;", "` : `${m + 1}月${d}日`;")
        c = c.replace("`SAVED`", "`补签`")
        c = c.replace("'<span class=\"nc\">SAVED</span>'", "'<span class=\"nc\">补签</span>'")
        c = c.replace("label = info ? `${MONTHS[m]} ${d}: ${nOf(info.plays, 'play')}, best ${info.best} pts${questDays[key] ? ', quests complete' : ''}`",
                      "label = info ? `${m + 1}月${d}日: 完成 ${info.plays} 轮, 最高 ${info.best} 分${questDays[key] ? ', 今日任务全通关' : ''}`")
        c = c.replace("if (n >= 1) badges.push(`<span class=\"cal-badge${n >= 3 ? ' hot' : ''}\">${`Streak<b>${n}</b>${n === 1 ? 'day' : 'days'}${playedToday ? '' : ` (today makes ${n + 1})`}`}</span>`);\n  else badges.push('<span class=\"cal-badge\">Start a streak today!</span>');\n  if (best >= 2) badges.push(`<span class=\"cal-badge best\">${`Best<b>${best}</b>days`}</span>`);\n  if (bonus.total) badges.push(`<span class=\"cal-badge stk\">${`Stickers<b>${bonus.total}</b>`}</span>`);\n  const hammers = store.items().hammer;\n  badges.push(`<span class=\"cal-badge hmr\" aria-label=\"Streak Hammers: ${hammers}\"><i>${HAMMER_SVG}</i><b>${hammers}</b></span>`);",
                      "if (n >= 1) badges.push(`<span class=\"cal-badge${n >= 3 ? ' hot' : ''}\">连续打卡<b>${n}</b>天${playedToday ? '' : `（今天完成即达 ${n + 1} 天）`}</span>`);\n  else badges.push('<span class=\"cal-badge\">从今天开始连续打卡！</span>');\n  if (best >= 2) badges.push(`<span class=\"cal-badge best\">最高连续<b>${best}</b>天</span>`);\n  if (bonus.total) badges.push(`<span class=\"cal-badge stk\">签到印章<b>${bonus.total}</b>个</span>`);\n  const hammers = store.items().hammer;\n  badges.push(`<span class=\"cal-badge hmr\" aria-label=\"补签锤：${hammers}支\"><i>${HAMMER_SVG}</i><b>${hammers}</b></span>`);")

        # Bonus dialog
        c = c.replace("$('#bonus-run').innerHTML = res.run >= 2 ? `Day<b>${res.run}</b>in a row!` : \"Today\'s bonus\";",
                      "$('#bonus-run').innerHTML = res.run >= 2 ? `连续打卡第 <b>${res.run}</b> 天！` : '今日登录奖励';")
        c = c.replace("slots.push(`<div class=\"bonus-slot${got ? ' got' : ''}${i === res.slot ? ' today stamping' : ''}${i === 7 ? ' big' : ''}\"><span class=\"d\">${`Day ${i}`}</span>${got ? stickerSvg(type) : i === 7 ? '?' : i}</div>`);",
                      "slots.push(`<div class=\"bonus-slot${got ? ' got' : ''}${i === res.slot ? ' today stamping' : ''}${i === 7 ? ' big' : ''}\"><span class=\"d\">第 ${i} 天</span>${got ? stickerSvg(type) : i === 7 ? '?' : i}</div>`);")
        c = c.replace("$('#bonus-note').textContent = res.slot === 7 ? \"Special sticker! It's on your calendar.\" : `${nOf(7 - res.slot, 'more day')} to a special sticker`;",
                      "$('#bonus-note').textContent = res.slot === 7 ? '获得特别纪念印章！已盖在你的日历上。' : `再连续签到 ${7 - res.slot} 天即可获得特别纪念印章`;")

        # Trophies Dialog & List
        c = c.replace("$('#tg-title').textContent = 'New trophy!';", "$('#tg-title').textContent = '解锁新成就！';")
        c = c.replace("$('#tg-sub').innerHTML = batch.length ? `<b>${batch.length}</b> earned from your past play!` : list.length > 1 ? `You earned <b>${list.length}</b>!` : '';",
                      "$('#tg-sub').innerHTML = batch.length ? `根据过往练习直接获得 <b>${batch.length}</b> 项成就！` : list.length > 1 ? `获得了 <b>${list.length}</b> 项新成就！` : '';")
        c = c.replace("+ rewards.map((it) => `<li class=\"reward\"><i>${itemThumb(it)}</i><span>${`<b>You got \"${it.name}\" (${catName(it.cat)})!</b><small>Pick it in the Collection</small>`}</span></li>`).join('');",
                      "+ rewards.map((it) => `<li class=\"reward\"><i>${itemThumb(it)}</i><span><b>获得了特效「${it.name}」(${catName(it.cat)})！</b><small>可前往图鉴收藏中选用</small></span></li>`).join('');")
        c = c.replace("const next = v.next ? `<span class=\"tr-next\">${`Next: ${secret ? '???' : v.next.name}${!secret && trophyValueText(v.next, v.value) ? ` (${trophyValueText(v.next, v.value)})` : ''}`}</span>` : '<span class=\"tr-next done\">Complete!</span>';",
                      "const next = v.next ? `<span class=\"tr-next\">下一目标：${secret ? '???' : v.next.name}${!secret && trophyValueText(v.next, v.value) ? ` (${trophyValueText(v.next, v.value)})` : ''}</span>` : '<span class=\"tr-next done\">全部完成！</span>';")
        c = c.replace("<small class=\"rw\">Reward: ${catName(rw.cat)} \"${rw.name}\"</small>",
                      "<small class=\"rw\">奖励：${catName(rw.cat)}「${rw.name}」</small>")
        c = c.replace("<small>${hide ? 'Secret trophy' : x.desc}</small>",
                      "<small>${hide ? '隐藏成就' : x.desc}</small>")
        c = c.replace("$('#tr-list').innerHTML = html || '<p class=\"tr-empty\">Nothing here yet</p>';",
                      "$('#tr-list').innerHTML = html || '<p class=\"tr-empty\">暂无内容</p>';")

        # Collection
        c = c.replace("'Shuffle'", "'随机轮换'")
        c = c.replace("'Changes every play'", "'每轮随机使用已解锁物品'")
        c = c.replace("auto ? '\"Shuffle\" picks a different one you own every play' : 'Your pick is used every time'",
                      "auto ? '「随机轮换」将在每轮自动随机使用已解锁的特效' : '已锁定使用你当前选中的特效'")
        c = c.replace("`Trophy: ${tro ? tro.name : ''}`", "`成就：${tro ? tro.name : ''}`")
        c = c.replace("${own ? '' : ` aria-label=\"Locked. Earn the trophy &quot;${tro ? tro.name : ''}&quot; to get it\"`}",
                      "${own ? '' : ` aria-label=\"未解锁。达成成就「${tro ? tro.name : ''}」即可获得\"`}")
        c = c.replace("<small class=\"co-lock\">Trophy: ${tro ? tro.name : ''}</small>",
                      "<small class=\"co-lock\">成就：${tro ? tro.name : ''}</small>")
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

        # Day list
        c = c.replace("label: `${fmtDay(h.day)}: ${modeName(h)}, ${h.score || 0} pts, ${nOf(h.ok || 0, 'correct')}, ${nOf(h.ng || 0, 'miss', 'misses')}`",
                      "label: `${fmtDay(h.day)}: ${modeName(h)}, ${h.score || 0} 分, 答对 ${h.ok || 0} 题, 失误 ${h.ng || 0} 次`")
        c = c.replace("`Correct ${h.ok ?? 0} · Oops ${h.ng ?? 0}${extra} · ${fmtTime(h.timeMs || 0)}`",
                      "`答对 ${h.ok ?? 0} 题 · 失误 ${h.ng ?? 0} 次${extra} · 用时 ${fmtTime(h.timeMs || 0)}`")
        c = c.replace("` · Extra ${h.extraOk}`", "` · Extra 答对 ${h.extraOk} 题`")

        # Lang select event: target check
        c = c.replace("if (!target || target === 'en') return;", "if (!target || target === 'zh-CN') return;")

    return c

with open('app/zh-CN/js/main.js', 'w', encoding='utf-8') as f:
    f.write(generate_main(False))
with open('app/zh-TW/js/main.js', 'w', encoding='utf-8') as f:
    f.write(generate_main(True))

print("main.js updated successfully for zh-CN and zh-TW!")
