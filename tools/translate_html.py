import re

with open('app/en/index.html', 'r', encoding='utf-8') as f:
    en_html = f.read()

# Let's write generator for zh-CN and zh-TW index.html

def make_html(is_tw=False):
    h = en_html
    if is_tw:
        h = h.replace('<html lang="en">', '<html lang="zh-TW">')
        h = h.replace('<title>Japanese Math Drill</title>', '<title>日系數學特訓 (Japanese Math Drill)</title>')
        h = h.replace('content="A math drill where every answer makes the show and the music bigger and bigger."',
                      'content="一款每答對一題，舞台與音樂就會越加華麗熱烈的日系數學算術特訓遊戲。"')
        h = h.replace('aria-label="Japanese Math Drill"', 'aria-label="日系數學特訓"')
        h = h.replace('<span class="logo-pre" aria-hidden="true">JAPANESE</span>', '<span class="logo-pre" aria-hidden="true">日系</span>')
        h = h.replace('<span class="logo-top" aria-hidden="true"><i data-c="M">M</i><i data-c="A">A</i><i data-c="T">T</i><i data-c="H">H</i></span>',
                      '<span class="logo-top" aria-hidden="true"><i data-c="數">數</i><i data-c="學">學</i></span>')
        h = h.replace('<i>D</i><i>R</i><i>I</i><i>L</i><i>L</i>', '<i>特</i><i>訓</i>')
        h = h.replace('aria-label="Settings"', 'aria-label="設定"')
        h = h.replace('aria-label="How to play"', 'aria-label="玩法指引"')
        h = h.replace('My Level<small id="level-sub">Starts with a skill check</small>',
                      '我的等級<small id="level-sub">初次遊玩先進行實力測試</small>')
        h = h.replace('Review <b id="review-count">0</b>', '錯題複習 <b id="review-count">0</b>')
        h = h.replace('aria-label="By grade"', 'aria-label="年級分類"')
        for g in range(1, 7):
            h = h.replace(f'<button type="button" data-grade="{g}"><small>Grade</small>{g}</button>',
                          f'<button type="button" data-grade="{g}">{g}<small>年級</small></button>')
        h = h.replace('Skill Tree <b id="tree-badge"></b>', '技能樹 <b id="tree-badge"></b>')
        h = h.replace('Trophies <b id="trophy-badge"></b>', '獎盃成就 <b id="trophy-badge"></b>')
        h = h.replace('Collection <b id="collect-badge"></b>', '圖鑑收藏 <b id="collect-badge"></b>')
        h = h.replace("<h2>Today's Quests</h2>", "<h2>今日任務</h2>")
        h = h.replace('<h2>Calendar</h2>', '<h2>日曆打卡</h2>')
        h = h.replace('aria-label="Previous month"', 'aria-label="上個月"')
        h = h.replace('aria-label="Next month"', 'aria-label="下個月"')
        h = h.replace('<span>Sun</span><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span>',
                      '<span>日</span><span>一</span><span>二</span><span>三</span><span>四</span><span>五</span><span>六</span>')
        h = h.replace('You can also use the number keys and Backspace', '也可使用鍵盤數字鍵與 Backspace 進行作答')
        h = h.replace('aria-label="Back"', 'aria-label="返回"')
        h = h.replace('<h2>Skill Tree</h2>', '<h2>技能樹</h2>')
        h = h.replace('Tap to practice (mastered: star goals) · Long-press to erase',
                      '點擊開始練習（已精通單元可查看星級目標）· 長按重置記錄')
        h = h.replace('<h2>Trophies</h2>', '<h2>獎盃成就</h2>')
        h = h.replace('aria-label="Filter"', 'aria-label="篩選"')
        h = h.replace('<button type="button" data-f="all" aria-pressed="true">All</button>', '<button type="button" data-f="all" aria-pressed="true">全部</button>')
        h = h.replace('<button type="button" data-f="got" aria-pressed="false">Earned</button>', '<button type="button" data-f="got" aria-pressed="false">已獲得</button>')
        h = h.replace('<button type="button" data-f="next" aria-pressed="false">Not yet</button>', '<button type="button" data-f="next" aria-pressed="false">未獲得</button>')
        h = h.replace('<button type="button" data-f="soon" aria-pressed="false">Almost</button>', '<button type="button" data-f="soon" aria-pressed="false">即將達成</button>')
        h = h.replace('<h2>Collection</h2>', '<h2>圖鑑收藏</h2>')
        h = h.replace('aria-label="Categories"', 'aria-label="特效分類"')
        h = h.replace('aria-label="Back to the title"', 'aria-label="返回標題畫面"')
        h = h.replace('Goal 2:40', '目標 2:40')
        h = h.replace('aria-label="Mute"', 'aria-label="靜音"')
        h = h.replace('Correct <b id="ok">0</b>', '答對 <b id="ok">0</b>')
        h = h.replace('Oops <b id="ng">0</b>', '失誤 <b id="ng">0</b>')
        h = h.replace('Dopa', '多帕')
        h = h.replace('LAST DIGIT!', '最後一位！')
        h = h.replace('aria-label="Delete one digit"', 'aria-label="刪除一位數字"')
        h = h.replace('Basic clear!', '基礎關卡通關！')
        h = h.replace('<span>pts</span>', '<span>分</span>')
        h = h.replace('<dt>Correct</dt>', '<dt>答對</dt>')
        h = h.replace('<dt>Oops</dt>', '<dt>失誤</dt>')
        h = h.replace('<dt>First-try rate</dt>', '<dt>初次正確率</dt>')
        h = h.replace('<dt>Time</dt>', '<dt>用時</dt>')
        h = h.replace('Play Extra<small>90 seconds</small>', '進入 Extra 加分挑戰<small>限時 90 秒</small>')
        h = h.replace('Redo missed problems', '重做錯題')
        h = h.replace('See Skill Tree', '查看技能樹')
        h = h.replace('Play again', '再來一輪')
        h = h.replace('<button type="button" id="go-title" class="sub-btn">Done</button>',
                      '<button type="button" id="go-title" class="sub-btn">返回主畫面</button>')
        h = h.replace('Extra finished!', 'Extra 挑戰結束！')
        h = h.replace('<dt>Extra correct</dt>', '<dt>Extra 答對</dt>')
        h = h.replace('<dt>Extra oops</dt>', '<dt>Extra 失誤</dt>')
        h = h.replace('<dt>Basic oops</dt>', '<dt>基礎關失誤</dt>')
        h = h.replace('<dt>Basic time</dt>', '<dt>基礎關用時</dt>')
        h = h.replace('<button type="button" id="again" class="big-btn">Done</button>',
                      '<button type="button" id="again" class="big-btn">完成</button>')
        h = h.replace('<h2 id="settings-title" class="chip">Settings</h2>', '<h2 id="settings-title" class="chip">設定</h2>')
        h = h.replace('<span class="set-label">Number of problems</span>', '<span class="set-label">每輪題目數量</span>')
        h = h.replace('aria-label="Number of problems"', 'aria-label="每輪題目數量"')
        h = h.replace('<span class="set-label">Sound</span>', '<span class="set-label">聲音效果</span>')
        h = h.replace('<b>On</b>', '<b>開啟</b>')
        h = h.replace('aria-label="Volume"', 'aria-label="音量大小"')
        h = h.replace('<span class="set-label">Motion <b id="motion-val">100%</b></span>',
                      '<span class="set-label">畫面動效強度 <b id="motion-val">100%</b></span>')
        h = h.replace('aria-label="Motion"', 'aria-label="動效強度"')
        h = h.replace('At 0%, shaking, flashes, confetti and movement stop', '設為 0% 時將關閉螢幕震動、閃爍、碎紙彩帶與鏡頭晃動')
        h = h.replace('<span class="set-label">Demo play</span>', '<span class="set-label">示範演示</span>')
        h = h.replace('▶ Watch it play itself', '▶ 觀看自動遊玩演示')
        h = h.replace('Tap the screen or press a key to stop (nothing is recorded)', '點擊螢幕或按鍵即可隨時結束（不記錄任何成績）')
        h = h.replace('<span class="set-label">Data</span>', '<span class="set-label">存檔資料</span>')
        h = h.replace('Reset everything', '清除重置所有資料')
        h = h.replace('Erases all data and starts over from the beginning', '將清除所有練習記錄與解鎖內容，完全回到初始狀態')
        h = h.replace('<button type="button" class="big-btn" id="close-settings">Close</button>',
                      '<button type="button" class="big-btn" id="close-settings">關閉</button>')
        h = h.replace('<h2 id="bonus-title" class="chip">Login bonus</h2>', '<h2 id="bonus-title" class="chip">登入獎勵</h2>')
        h = h.replace('<button type="button" class="big-btn" id="bonus-ok">Collect</button>',
                      '<button type="button" class="big-btn" id="bonus-ok">領取獎勵</button>')
        h = h.replace('<button type="button" class="sub-btn" id="si-close">Close</button>',
                      '<button type="button" class="sub-btn" id="si-close">關閉</button>')
        h = h.replace('<button type="button" class="sub-btn si-go" id="si-go">Practice</button>',
                      '<button type="button" class="sub-btn si-go" id="si-go">開始練習</button>')
        h = h.replace('<h2 id="tg-title" class="chip">New trophy!</h2>', '<h2 id="tg-title" class="chip">解鎖新成就！</h2>')
        h = h.replace('<button type="button" class="big-btn" id="tg-ok">Awesome!</button>',
                      '<button type="button" class="big-btn" id="tg-ok">太棒了！</button>')
        h = h.replace('<h2 id="hammer-title" class="chip">Streak Hammer</h2>', '<h2 id="hammer-title" class="chip">打卡補簽槌</h2>')
        h = h.replace('<button type="button" class="sub-btn" id="hammer-no">No thanks</button>',
                      '<button type="button" class="sub-btn" id="hammer-no">先不用</button>')
        h = h.replace('<button type="button" class="sub-btn hammer-yes" id="hammer-yes">Use it</button>',
                      '<button type="button" class="sub-btn hammer-yes" id="hammer-yes">使用補簽</button>')
        h = h.replace('<h2 id="confirm-title" class="chip">Erase skill</h2>', '<h2 id="confirm-title" class="chip">確認重置</h2>')
        h = h.replace('<button type="button" class="sub-btn" id="confirm-no">Cancel</button>',
                      '<button type="button" class="sub-btn" id="confirm-no">取消</button>')
        h = h.replace('<button type="button" class="sub-btn danger" id="confirm-yes">Erase</button>',
                      '<button type="button" class="sub-btn danger" id="confirm-yes">確認重置</button>')
        h = h.replace('<h2 id="day-title" class="chip">Plays</h2>', '<h2 id="day-title" class="chip">練習記錄</h2>')
        h = h.replace('<button type="button" class="big-btn" id="close-day">Close</button>',
                      '<button type="button" class="big-btn" id="close-day">關閉</button>')
        h = h.replace('This game needs JavaScript to run.', '本遊戲需要啟用 JavaScript 才能運行。')
    else:
        h = h.replace('<html lang="en">', '<html lang="zh-CN">')
        h = h.replace('<title>Japanese Math Drill</title>', '<title>日系数学特训 (Japanese Math Drill)</title>')
        h = h.replace('content="A math drill where every answer makes the show and the music bigger and bigger."',
                      'content="一款每答对一题，舞台与音乐就会越加华丽热烈的日系数学算术特训游戏。"')
        h = h.replace('aria-label="Japanese Math Drill"', 'aria-label="日系数学特训"')
        h = h.replace('<span class="logo-pre" aria-hidden="true">JAPANESE</span>', '<span class="logo-pre" aria-hidden="true">日系</span>')
        h = h.replace('<span class="logo-top" aria-hidden="true"><i data-c="M">M</i><i data-c="A">A</i><i data-c="T">T</i><i data-c="H">H</i></span>',
                      '<span class="logo-top" aria-hidden="true"><i data-c="数">数</i><i data-c="学">学</i></span>')
        h = h.replace('<i>D</i><i>R</i><i>I</i><i>L</i><i>L</i>', '<i>特</i><i>训</i>')
        h = h.replace('aria-label="Settings"', 'aria-label="设置"')
        h = h.replace('aria-label="How to play"', 'aria-label="玩法说明"')
        h = h.replace('My Level<small id="level-sub">Starts with a skill check</small>',
                      '我的等级<small id="level-sub">初次进入先进行实力测试</small>')
        h = h.replace('Review <b id="review-count">0</b>', '错题复习 <b id="review-count">0</b>')
        h = h.replace('aria-label="By grade"', 'aria-label="年级分类"')
        for g in range(1, 7):
            h = h.replace(f'<button type="button" data-grade="{g}"><small>Grade</small>{g}</button>',
                          f'<button type="button" data-grade="{g}">{g}<small>年级</small></button>')
        h = h.replace('Skill Tree <b id="tree-badge"></b>', '技能树 <b id="tree-badge"></b>')
        h = h.replace('Trophies <b id="trophy-badge"></b>', '奖杯成就 <b id="trophy-badge"></b>')
        h = h.replace('Collection <b id="collect-badge"></b>', '图鉴收藏 <b id="collect-badge"></b>')
        h = h.replace("<h2>Today's Quests</h2>", "<h2>今日任务</h2>")
        h = h.replace('<h2>Calendar</h2>', '<h2>日历打卡</h2>')
        h = h.replace('aria-label="Previous month"', 'aria-label="上个月"')
        h = h.replace('aria-label="Next month"', 'aria-label="下个月"')
        h = h.replace('<span>Sun</span><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span>',
                      '<span>日</span><span>一</span><span>二</span><span>三</span><span>四</span><span>五</span><span>六</span>')
        h = h.replace('You can also use the number keys and Backspace', '也可使用键盘数字键与 Backspace 进行作答')
        h = h.replace('aria-label="Back"', 'aria-label="返回"')
        h = h.replace('<h2>Skill Tree</h2>', '<h2>技能树</h2>')
        h = h.replace('Tap to practice (mastered: star goals) · Long-press to erase',
                      '点击开始练习（已精通技能可查看星级目标）· 长按重置记录')
        h = h.replace('<h2>Trophies</h2>', '<h2>奖杯成就</h2>')
        h = h.replace('aria-label="Filter"', 'aria-label="筛选"')
        h = h.replace('<button type="button" data-f="all" aria-pressed="true">All</button>', '<button type="button" data-f="all" aria-pressed="true">全部</button>')
        h = h.replace('<button type="button" data-f="got" aria-pressed="false">Earned</button>', '<button type="button" data-f="got" aria-pressed="false">已获得</button>')
        h = h.replace('<button type="button" data-f="next" aria-pressed="false">Not yet</button>', '<button type="button" data-f="next" aria-pressed="false">未获得</button>')
        h = h.replace('<button type="button" data-f="soon" aria-pressed="false">Almost</button>', '<button type="button" data-f="soon" aria-pressed="false">即将达成</button>')
        h = h.replace('<h2>Collection</h2>', '<h2>图鉴收藏</h2>')
        h = h.replace('aria-label="Categories"', 'aria-label="特效分类"')
        h = h.replace('aria-label="Back to the title"', 'aria-label="返回主标题"')
        h = h.replace('Goal 2:40', '目标 2:40')
        h = h.replace('aria-label="Mute"', 'aria-label="静音"')
        h = h.replace('Correct <b id="ok">0</b>', '答对 <b id="ok">0</b>')
        h = h.replace('Oops <b id="ng">0</b>', '失误 <b id="ng">0</b>')
        h = h.replace('Dopa', '多帕')
        h = h.replace('LAST DIGIT!', '最后一位！')
        h = h.replace('aria-label="Delete one digit"', 'aria-label="删除一位数字"')
        h = h.replace('Basic clear!', '基础关卡通关！')
        h = h.replace('<span>pts</span>', '<span>分</span>')
        h = h.replace('<dt>Correct</dt>', '<dt>答对</dt>')
        h = h.replace('<dt>Oops</dt>', '<dt>失误</dt>')
        h = h.replace('<dt>First-try rate</dt>', '<dt>首次正确率</dt>')
        h = h.replace('<dt>Time</dt>', '<dt>用时</dt>')
        h = h.replace('Play Extra<small>90 seconds</small>', '进入 Extra 加分挑战<small>限时 90 秒</small>')
        h = h.replace('Redo missed problems', '重做错题')
        h = h.replace('See Skill Tree', '查看技能树')
        h = h.replace('Play again', '再来一轮')
        h = h.replace('<button type="button" id="go-title" class="sub-btn">Done</button>',
                      '<button type="button" id="go-title" class="sub-btn">返回主页面</button>')
        h = h.replace('Extra finished!', 'Extra 挑战结束！')
        h = h.replace('<dt>Extra correct</dt>', '<dt>Extra 答对</dt>')
        h = h.replace('<dt>Extra oops</dt>', '<dt>Extra 失误</dt>')
        h = h.replace('<dt>Basic oops</dt>', '<dt>基础关失误</dt>')
        h = h.replace('<dt>Basic time</dt>', '<dt>基础关用时</dt>')
        h = h.replace('<button type="button" id="again" class="big-btn">Done</button>',
                      '<button type="button" id="again" class="big-btn">完成</button>')
        h = h.replace('<h2 id="settings-title" class="chip">Settings</h2>', '<h2 id="settings-title" class="chip">设置</h2>')
        h = h.replace('<span class="set-label">Number of problems</span>', '<span class="set-label">每轮题目数量</span>')
        h = h.replace('aria-label="Number of problems"', 'aria-label="每轮题目数量"')
        h = h.replace('<span class="set-label">Sound</span>', '<span class="set-label">声音效果</span>')
        h = h.replace('<b>On</b>', '<b>开启</b>')
        h = h.replace('aria-label="Volume"', 'aria-label="音量大小"')
        h = h.replace('<span class="set-label">Motion <b id="motion-val">100%</b></span>',
                      '<span class="set-label">画面动效强度 <b id="motion-val">100%</b></span>')
        h = h.replace('aria-label="Motion"', 'aria-label="动效强度"')
        h = h.replace('At 0%, shaking, flashes, confetti and movement stop', '设为 0% 时将关闭屏幕震动、闪烁、彩带碎屑与镜头移动')
        h = h.replace('<span class="set-label">Demo play</span>', '<span class="set-label">示范演示</span>')
        h = h.replace('▶ Watch it play itself', '▶ 观看自动游玩演示')
        h = h.replace('Tap the screen or press a key to stop (nothing is recorded)', '点击屏幕或按键即可随时退出（不记录任何成绩）')
        h = h.replace('<span class="set-label">Data</span>', '<span class="set-label">存档数据</span>')
        h = h.replace('Reset everything', '清除重置所有数据')
        h = h.replace('Erases all data and starts over from the beginning', '将清除所有练习记录与解锁内容，彻底回到初始状态')
        h = h.replace('<button type="button" class="big-btn" id="close-settings">Close</button>',
                      '<button type="button" class="big-btn" id="close-settings">关闭</button>')
        h = h.replace('<h2 id="bonus-title" class="chip">Login bonus</h2>', '<h2 id="bonus-title" class="chip">登录奖励</h2>')
        h = h.replace('<button type="button" class="big-btn" id="bonus-ok">Collect</button>',
                      '<button type="button" class="big-btn" id="bonus-ok">领取奖励</button>')
        h = h.replace('<button type="button" class="sub-btn" id="si-close">Close</button>',
                      '<button type="button" class="sub-btn" id="si-close">关闭</button>')
        h = h.replace('<button type="button" class="sub-btn si-go" id="si-go">Practice</button>',
                      '<button type="button" class="sub-btn si-go" id="si-go">开始练习</button>')
        h = h.replace('<h2 id="tg-title" class="chip">New trophy!</h2>', '<h2 id="tg-title" class="chip">解锁新成就！</h2>')
        h = h.replace('<button type="button" class="big-btn" id="tg-ok">Awesome!</button>',
                      '<button type="button" class="big-btn" id="tg-ok">太棒了！</button>')
        h = h.replace('<h2 id="hammer-title" class="chip">Streak Hammer</h2>', '<h2 id="hammer-title" class="chip">打卡补签锤</h2>')
        h = h.replace('<button type="button" class="sub-btn" id="hammer-no">No thanks</button>',
                      '<button type="button" class="sub-btn" id="hammer-no">先不用</button>')
        h = h.replace('<button type="button" class="sub-btn hammer-yes" id="hammer-yes">Use it</button>',
                      '<button type="button" class="sub-btn hammer-yes" id="hammer-yes">使用补签</button>')
        h = h.replace('<h2 id="confirm-title" class="chip">Erase skill</h2>', '<h2 id="confirm-title" class="chip">确认重置</h2>')
        h = h.replace('<button type="button" class="sub-btn" id="confirm-no">Cancel</button>',
                      '<button type="button" class="sub-btn" id="confirm-no">取消</button>')
        h = h.replace('<button type="button" class="sub-btn danger" id="confirm-yes">Erase</button>',
                      '<button type="button" class="sub-btn danger" id="confirm-yes">确认重置</button>')
        h = h.replace('<h2 id="day-title" class="chip">Plays</h2>', '<h2 id="day-title" class="chip">练习记录</h2>')
        h = h.replace('<button type="button" class="big-btn" id="close-day">Close</button>',
                      '<button type="button" class="big-btn" id="close-day">关闭</button>')
        h = h.replace('This game needs JavaScript to run.', '本游戏需要启用 JavaScript 才能运行。')

    # Selected option in select id="lang"
    target_val = 'zh-TW' if is_tw else 'zh-CN'
    h = re.sub(r'<option value=".*?" lang=".*?" selected>', lambda m: m.group(0).replace(' selected', ''), h)
    h = h.replace(f'<option value="{target_val}" lang="{target_val}">', f'<option value="{target_val}" lang="{target_val}" selected>')
    return h

with open('app/zh-CN/index.html', 'w', encoding='utf-8') as f:
    f.write(make_html(False))
with open('app/zh-TW/index.html', 'w', encoding='utf-8') as f:
    f.write(make_html(True))

print("Updated index.html for zh-CN and zh-TW")
