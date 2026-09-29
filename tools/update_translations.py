import re, pathlib

# ---------------------------------------------------------------------
# 1. Update HTML files for zh-CN and zh-TW
# ---------------------------------------------------------------------
with open('app/en/index.html', 'r', encoding='utf-8') as f:
    en_html = f.read()

def generate_html(is_tw=False):
    h = en_html
    target_val = 'zh-TW' if is_tw else 'zh-CN'
    h = h.replace('<html lang="en">', f'<html lang="{target_val}">')
    h = h.replace('<title>Japanese Math Drill</title>', f'<title>{"日系數學特訓" if is_tw else "日系数学特训"} (Japanese Math Drill)</title>')
    h = h.replace('content="A math drill where every answer makes the show and the music bigger and bigger."',
                  'content="一款每答對一題，舞台與音樂就會越加華麗熱烈的日系數學算術特訓遊戲。"' if is_tw else
                  'content="一款每答对一题，舞台与音乐就会越加华丽热烈的日系数学算术特训游戏。"')
    h = h.replace('aria-label="Japanese Math Drill"', 'aria-label="日系數學特訓"' if is_tw else 'aria-label="日系数学特训"')
    h = h.replace('<span class="logo-pre" aria-hidden="true">JAPANESE</span>', '<span class="logo-pre" aria-hidden="true">日系</span>')
    h = h.replace('<span class="logo-top" aria-hidden="true"><i data-c="M">M</i><i data-c="A">A</i><i data-c="T">T</i><i data-c="H">H</i></span>',
                  '<span class="logo-top" aria-hidden="true"><i data-c="數">數</i><i data-c="學">學</i></span>' if is_tw else
                  '<span class="logo-top" aria-hidden="true"><i data-c="数">数</i><i data-c="学">学</i></span>')
    h = h.replace('<i>D</i><i>R</i><i>I</i><i>L</i><i>L</i>', '<i>特</i><i>訓</i>' if is_tw else '<i>特</i><i>训</i>')
    h = h.replace('aria-label="Settings"', 'aria-label="設定"' if is_tw else 'aria-label="设置"')
    h = h.replace('aria-label="How to play"', 'aria-label="玩法指引"' if is_tw else 'aria-label="玩法说明"')
    h = h.replace('My Level<small id="level-sub">Starts with a skill check</small>',
                  '我的等級<small id="level-sub">初次遊玩先進行實力測試</small>' if is_tw else
                  '我的等级<small id="level-sub">初次进入先进行实力测试</small>')
    h = h.replace('Review <b id="review-count">0</b>', '錯題複習 <b id="review-count">0</b>' if is_tw else '错题复习 <b id="review-count">0</b>')
    h = h.replace('aria-label="By grade"', 'aria-label="年級分類"' if is_tw else 'aria-label="年级分类"')
    for g in range(1, 7):
        h = h.replace(f'<button type="button" data-grade="{g}"><small>Grade</small>{g}</button>',
                      f'<button type="button" data-grade="{g}">{g}<small>{"年級" if is_tw else "年级"}</small></button>')
    h = h.replace('Skill Tree <b id="tree-badge"></b>', '技能樹 <b id="tree-badge"></b>' if is_tw else '技能树 <b id="tree-badge"></b>')
    h = h.replace('Trophies <b id="trophy-badge"></b>', '獎盃成就 <b id="trophy-badge"></b>' if is_tw else '奖杯成就 <b id="trophy-badge"></b>')
    h = h.replace('Collection <b id="collect-badge"></b>', '圖鑑收藏 <b id="collect-badge"></b>' if is_tw else '图鉴收藏 <b id="collect-badge"></b>')
    
    # Quests & Calendar
    h = h.replace('<h2 id="quest-title">Today\'s Quests</h2>', '<h2 id="quest-title">今日任務</h2>' if is_tw else '<h2 id="quest-title">今日任务</h2>')
    h = h.replace('<h2 id="cal-title">Calendar</h2>', '<h2 id="cal-title">日曆打卡</h2>' if is_tw else '<h2 id="cal-title">日历打卡</h2>')
    h = h.replace('aria-label="Previous month"', 'aria-label="上個月"' if is_tw else 'aria-label="上个月"')
    h = h.replace('aria-label="Next month"', 'aria-label="下個月"' if is_tw else 'aria-label="下个月"')
    h = h.replace('<span>Sun</span><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span>',
                  '<span>日</span><span>一</span><span>二</span><span>三</span><span>四</span><span>五</span><span>六</span>')
    h = h.replace('You can also use the number keys and Backspace',
                  '也可使用鍵盤數字鍵與 Backspace 進行作答' if is_tw else '也可使用键盘数字键与 Backspace 进行作答')
    h = h.replace('aria-label="Back"', 'aria-label="返回"')
    h = h.replace('<h2 id="tree-title">Skill Tree</h2>', '<h2 id="tree-title">技能樹</h2>' if is_tw else '<h2 id="tree-title">技能树</h2>')
    h = h.replace('Tap to practice (mastered: star goals) · Long-press to erase',
                  '點擊開始練習（已精通單元可查看星級目標）· 長按重置記錄' if is_tw else
                  '点击开始练习（已精通技能可查看星级目标）· 长按重置记录')
    h = h.replace('<h2 id="trophy-title">Trophies</h2>', '<h2 id="trophy-title">獎盃成就</h2>' if is_tw else '<h2 id="trophy-title">奖杯成就</h2>')
    h = h.replace('aria-label="Filter"', 'aria-label="篩選"' if is_tw else 'aria-label="筛选"')
    h = h.replace('<button type="button" data-f="all" aria-pressed="true">All</button>', '<button type="button" data-f="all" aria-pressed="true">全部</button>')
    h = h.replace('<button type="button" data-f="got" aria-pressed="false">Earned</button>', '<button type="button" data-f="got" aria-pressed="false">已獲得</button>' if is_tw else '<button type="button" data-f="got" aria-pressed="false">已获得</button>')
    h = h.replace('<button type="button" data-f="next" aria-pressed="false">Not yet</button>', '<button type="button" data-f="next" aria-pressed="false">未獲得</button>' if is_tw else '<button type="button" data-f="next" aria-pressed="false">未获得</button>')
    h = h.replace('<button type="button" data-f="soon" aria-pressed="false">Almost</button>', '<button type="button" data-f="soon" aria-pressed="false">即將達成</button>' if is_tw else '<button type="button" data-f="soon" aria-pressed="false">即将达成</button>')
    h = h.replace('<h2 id="collect-title">Collection</h2>', '<h2 id="collect-title">圖鑑收藏</h2>' if is_tw else '<h2 id="collect-title">图鉴收藏</h2>')
    h = h.replace('aria-label="Categories"', 'aria-label="特效分類"' if is_tw else 'aria-label="特效分类"')
    h = h.replace('aria-label="Back to the title"', 'aria-label="返回標題畫面"' if is_tw else 'aria-label="返回主标题"')
    h = h.replace('Goal 2:40', '目標 2:40' if is_tw else '目标 2:40')
    h = h.replace('aria-label="Mute"', 'aria-label="靜音"' if is_tw else 'aria-label="静音"')
    h = h.replace('Correct <b id="ok">0</b>', '答對 <b id="ok">0</b>' if is_tw else '答对 <b id="ok">0</b>')
    h = h.replace('Oops <b id="ng">0</b>', '失誤 <b id="ng">0</b>' if is_tw else '失误 <b id="ng">0</b>')
    h = h.replace('<small>combo</small>', '<small>連擊</small>' if is_tw else '<small>连击</small>')
    h = h.replace('Dopa', '多帕')
    h = h.replace('<span class="chip" id="qtitle">Addition</span>', '<span class="chip" id="qtitle">加法</span>')
    h = h.replace('<p class="step-label" id="step-label" aria-live="polite">Ones place</p>',
                  '<p class="step-label" id="step-label" aria-live="polite">個位</p>' if is_tw else
                  '<p class="step-label" id="step-label" aria-live="polite">个位</p>')
    h = h.replace('LAST DIGIT!', '最後一位！' if is_tw else '最后一位！')
    h = h.replace('aria-label="Delete one digit"', 'aria-label="刪除一位數字"' if is_tw else 'aria-label="删除一位数字"')
    h = h.replace('Basic clear!', '基礎關卡通關！' if is_tw else '基础关卡通关！')
    h = h.replace('<span>pts</span>', '<span>分</span>')
    h = h.replace('<dt>Correct</dt>', '<dt>答對</dt>' if is_tw else '<dt>答对</dt>')
    h = h.replace('<dt>Oops</dt>', '<dt>失誤</dt>' if is_tw else '<dt>失误</dt>')
    h = h.replace('<dt>First-try rate</dt>', '<dt>初次正確率</dt>' if is_tw else '<dt>首次正确率</dt>')
    h = h.replace('<dt>Time</dt>', '<dt>用時</dt>' if is_tw else '<dt>用时</dt>')
    h = h.replace('Play Extra<small>90 seconds</small>', '進入 Extra 加分挑戰<small>限時 90 秒</small>' if is_tw else '进入 Extra 加分挑战<small>限时 90 秒</small>')
    h = h.replace('Redo missed problems', '重做錯題' if is_tw else '重做错题')
    h = h.replace('See Skill Tree', '查看技能樹' if is_tw else '查看技能树')
    h = h.replace('Play again', '再來一輪' if is_tw else '再来一轮')
    h = h.replace('<button type="button" id="go-title" class="sub-btn">Done</button>',
                  '<button type="button" id="go-title" class="sub-btn">返回主畫面</button>' if is_tw else
                  '<button type="button" id="go-title" class="sub-btn">返回主页面</button>')
    h = h.replace('Extra finished!', 'Extra 挑戰結束！' if is_tw else 'Extra 挑战结束！')
    h = h.replace('<dt>Extra correct</dt>', '<dt>Extra 答對</dt>' if is_tw else '<dt>Extra 答对</dt>')
    h = h.replace('<dt>Extra oops</dt>', '<dt>Extra 失誤</dt>' if is_tw else '<dt>Extra 失误</dt>')
    h = h.replace('<dt>Basic oops</dt>', '<dt>基礎關失誤</dt>' if is_tw else '<dt>基础关失误</dt>')
    h = h.replace('<dt>Basic time</dt>', '<dt>基礎關用時</dt>' if is_tw else '<dt>基础关用时</dt>')
    h = h.replace('<button type="button" id="again" class="big-btn">Done</button>',
                  '<button type="button" id="again" class="big-btn">完成</button>')
    h = h.replace('<p class="breakdown" id="f-break">Basic 100 + Extra 0</p>',
                  '<p class="breakdown" id="f-break">基礎關 100 + Extra 0</p>' if is_tw else
                  '<p class="breakdown" id="f-break">基础关 100 + Extra 0</p>')
    h = h.replace('<h2 id="settings-title" class="chip">Settings</h2>', '<h2 id="settings-title" class="chip">設定</h2>' if is_tw else '<h2 id="settings-title" class="chip">设置</h2>')
    h = h.replace('<span class="set-label">Number of problems</span>', '<span class="set-label">每輪題目數量</span>' if is_tw else '<span class="set-label">每轮题目数量</span>')
    h = h.replace('aria-label="Number of problems"', 'aria-label="每輪題目數量"' if is_tw else 'aria-label="每轮题目数量"')
    h = h.replace('<span class="set-label">Sound</span>', '<span class="set-label">聲音效果</span>' if is_tw else '<span class="set-label">声音效果</span>')
    h = h.replace('<b>On</b>', '<b>開啟</b>' if is_tw else '<b>开启</b>')
    h = h.replace('aria-label="Volume"', 'aria-label="音量大小"')
    h = h.replace('<span class="set-label">Motion <b id="motion-val">100%</b></span>',
                  '<span class="set-label">畫面動效強度 <b id="motion-val">100%</b></span>' if is_tw else
                  '<span class="set-label">画面动效强度 <b id="motion-val">100%</b></span>')
    h = h.replace('aria-label="Motion"', 'aria-label="動效強度"' if is_tw else 'aria-label="动效强度"')
    h = h.replace('At 0%, shaking, flashes, confetti and movement stop',
                  '設為 0% 時將關閉螢幕震動、閃爍、碎紙彩帶與鏡頭晃動' if is_tw else
                  '设为 0% 时将关闭屏幕震动、闪烁、彩带碎屑与镜头移动')
    h = h.replace('<span class="set-label">Demo play</span>', '<span class="set-label">示範演示</span>' if is_tw else '<span class="set-label">示范演示</span>')
    h = h.replace('▶ Watch it play itself', '▶ 觀看自動遊玩演示' if is_tw else '▶ 观看自动游玩演示')
    h = h.replace('Tap the screen or press a key to stop (nothing is recorded)',
                  '點擊螢幕或按鍵即可隨時結束（不記錄任何成績）' if is_tw else
                  '点击屏幕或按键即可随时退出（不记录任何成绩）')
    h = h.replace('<span class="set-label">Data</span>', '<span class="set-label">存檔資料</span>' if is_tw else '<span class="set-label">存档数据</span>')
    h = h.replace('Reset everything', '清除重置所有資料' if is_tw else '清除重置所有数据')
    h = h.replace('Erases all data and starts over from the beginning',
                  '將清除所有練習記錄與解鎖內容，完全回到初始狀態' if is_tw else
                  '将清除所有练习记录与解锁内容，彻底回到初始状态')
    h = h.replace('<button type="button" class="big-btn" id="close-settings">Close</button>',
                  '<button type="button" class="big-btn" id="close-settings">關閉</button>' if is_tw else
                  '<button type="button" class="big-btn" id="close-settings">关闭</button>')
    h = h.replace('<h2 id="bonus-title" class="chip">Login bonus</h2>', '<h2 id="bonus-title" class="chip">登入獎勵</h2>' if is_tw else '<h2 id="bonus-title" class="chip">登录奖励</h2>')
    h = h.replace('<button type="button" class="big-btn" id="bonus-ok">Collect</button>',
                  '<button type="button" class="big-btn" id="bonus-ok">領取獎勵</button>' if is_tw else
                  '<button type="button" class="big-btn" id="bonus-ok">领取奖励</button>')
    h = h.replace('<button type="button" class="sub-btn" id="si-close">Close</button>',
                  '<button type="button" class="sub-btn" id="si-close">關閉</button>' if is_tw else
                  '<button type="button" class="sub-btn" id="si-close">关闭</button>')
    h = h.replace('<button type="button" class="sub-btn si-go" id="si-go">Practice</button>',
                  '<button type="button" class="sub-btn si-go" id="si-go">開始練習</button>' if is_tw else
                  '<button type="button" class="sub-btn si-go" id="si-go">开始练习</button>')
    h = h.replace('<h2 id="tg-title" class="chip">New trophy!</h2>', '<h2 id="tg-title" class="chip">解鎖新成就！</h2>' if is_tw else '<h2 id="tg-title" class="chip">解锁新成就！</h2>')
    h = h.replace('<button type="button" class="big-btn" id="tg-ok">Awesome!</button>',
                  '<button type="button" class="big-btn" id="tg-ok">太棒了！</button>')
    h = h.replace('<h2 id="hammer-title" class="chip">Streak Hammer</h2>', '<h2 id="hammer-title" class="chip">打卡補簽槌</h2>' if is_tw else '<h2 id="hammer-title" class="chip">打卡补签锤</h2>')
    h = h.replace('<button type="button" class="sub-btn" id="hammer-no">No thanks</button>',
                  '<button type="button" class="sub-btn" id="hammer-no">先不用</button>')
    h = h.replace('<button type="button" class="sub-btn hammer-yes" id="hammer-yes">Use it</button>',
                  '<button type="button" class="sub-btn hammer-yes" id="hammer-yes">使用補簽</button>' if is_tw else
                  '<button type="button" class="sub-btn hammer-yes" id="hammer-yes">使用补签</button>')
    h = h.replace('<h2 id="confirm-title" class="chip">Erase skill</h2>', '<h2 id="confirm-title" class="chip">確認重置</h2>' if is_tw else '<h2 id="confirm-title" class="chip">确认重置</h2>')
    h = h.replace('<button type="button" class="sub-btn" id="confirm-no">Cancel</button>',
                  '<button type="button" class="sub-btn" id="confirm-no">取消</button>')
    h = h.replace('<button type="button" class="sub-btn danger" id="confirm-yes">Erase</button>',
                  '<button type="button" class="sub-btn danger" id="confirm-yes">確認重置</button>' if is_tw else
                  '<button type="button" class="sub-btn danger" id="confirm-yes">确认重置</button>')
    h = h.replace('<h2 id="day-title" class="chip">Plays</h2>', '<h2 id="day-title" class="chip">練習記錄</h2>' if is_tw else '<h2 id="day-title" class="chip">练习记录</h2>')
    h = h.replace('<button type="button" class="big-btn" id="close-day">Close</button>',
                  '<button type="button" class="big-btn" id="close-day">關閉</button>' if is_tw else
                  '<button type="button" class="big-btn" id="close-day">关闭</button>')
    h = h.replace('This game needs JavaScript to run.', '本遊戲需要啟用 JavaScript 才能運行。' if is_tw else '本游戏需要启用 JavaScript 才能运行。')

    # Selected option in select id="lang"
    h = re.sub(r'<option value=".*?" lang=".*?" selected>', lambda m: m.group(0).replace(' selected', ''), h)
    h = h.replace(f'<option value="{target_val}" lang="{target_val}">', f'<option value="{target_val}" lang="{target_val}" selected>')
    return h

with open('app/zh-CN/index.html', 'w', encoding='utf-8') as f:
    f.write(generate_html(False))
with open('app/zh-TW/index.html', 'w', encoding='utf-8') as f:
    f.write(generate_html(True))

print("index.html regenerated cleanly!")
