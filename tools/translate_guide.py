# Guide translations
with open('app/en/js/guide.js', 'r', encoding='utf-8') as f:
    text = f.read()

def make_guide(is_tw=False):
    c = text
    if is_tw:
        c = c.replace(
            "const INTRO = { title: 'How to play', text: 'There are 3 ways\\nto pick your problems' };",
            "const INTRO = { title: '玩法介紹', text: '共有 3 種練習題目的\\n挑選方式喔！' };"
        )
        c = c.replace(
            "const LEVEL = { target: '#start', title: 'My Level', text: 'Problems that fit you right now.\\nIt starts with a skill check' };",
            "const LEVEL = { target: '#start', title: '我的等級', text: '為你量身打造的專屬題目。\\n初次進入會先進行實力測試！' };"
        )
        c = c.replace(
            "const GRADES = { target: '.grades', title: 'Grade 1 to Grade 6', text: 'Practice the problems\\nfrom a whole grade' };",
            "const GRADES = { target: '.grades', title: '一年級～六年級', text: '按各年級進度\\n進行全面的練習' };"
        )
        c = c.replace(
            "const TREE = { target: '#open-tree', title: 'Skill Tree', text: 'Pick the one kind of problem\\nyou want to practice' };",
            "const TREE = { target: '#open-tree', title: '技能樹', text: '自由選擇你想專項加強的\\n計算單元來練習' };"
        )
        c = c.replace(
            "const TROPHY = { target: '#open-trophy', title: 'Trophies', text: 'You earn them by playing.\\nKeep coming back for more' };",
            "const TROPHY = { target: '#open-trophy', title: '獎盃成就', text: '每次練習都能累積成就。\\n持續遊玩解鎖更多榮譽！' };"
        )
        c = c.replace(
            "const COLLECTION = { target: '#open-collect', title: 'Collection', text: 'Trophy rewards add backgrounds,\\nmusic, outfits and more\\nfor you to choose' };",
            "const COLLECTION = { target: '#open-collect', title: '收藏館', text: '獎盃獎勵可解鎖背景、\\n音樂、角色裝扮等豐富特效\\n供你隨心搭配！' };"
        )
        c = c.replace(
            "const LAST = { target: '#start', title: 'Not sure? Try My Level!', text: 'You can see this guide\\nagain with ?', recommend: true };",
            "const LAST = { target: '#start', title: '猶豫的話，先試試「我的等級」！', text: '點擊問號 ？ 可以\\n隨時再次查看本指引', recommend: true };"
        )
        c = c.replace("<span id=\"guide-recommend\" hidden>${'Recommended'}</span>", "<span id=\"guide-recommend\" hidden>推薦</span>")
        c = c.replace("<button type=\"button\" id=\"guide-skip\" class=\"sub-btn\">${'Skip'}</button>", "<button type=\"button\" id=\"guide-skip\" class=\"sub-btn\">略過</button>")
        c = c.replace("<button type=\"button\" class=\"sub-btn\" id=\"guide-back\">${'Back'}</button>", "<button type=\"button\" class=\"sub-btn\" id=\"guide-back\">上一步</button>")
        c = c.replace("<button type=\"button\" class=\"big-btn\" id=\"guide-next\">${'Next'}</button>", "<button type=\"button\" class=\"big-btn\" id=\"guide-next\">下一步</button>")
        c = c.replace("index === pages.length - 1 ? \"Let's go!\" : 'Next'", "index === pages.length - 1 ? '開始挑戰！' : '下一步'")
        c = c.replace("`Page ${index + 1} of ${pages.length}`", "`第 ${index + 1} / ${pages.length} 頁`")
        c = c.replace("document.createTextNode('You can see this guide\\nagain with ')", "document.createTextNode('點擊問號 ')")
        c = c.replace("document.createTextNode('')", "document.createTextNode(' 可以隨時再次查看本指引')")
    else:
        c = c.replace(
            "const INTRO = { title: 'How to play', text: 'There are 3 ways\\nto pick your problems' };",
            "const INTRO = { title: '玩法介绍', text: '共有 3 种练习题目的\\n挑选方式哦！' };"
        )
        c = c.replace(
            "const LEVEL = { target: '#start', title: 'My Level', text: 'Problems that fit you right now.\\nIt starts with a skill check' };",
            "const LEVEL = { target: '#start', title: '我的等级', text: '为你量身定制的专属题目。\\n首次进入会先进行实力测试！' };"
        )
        c = c.replace(
            "const GRADES = { target: '.grades', title: 'Grade 1 to Grade 6', text: 'Practice the problems\\nfrom a whole grade' };",
            "const GRADES = { target: '.grades', title: '一年级～六年级', text: '按各年级课本进度\\n进行全面的算术练习' };"
        )
        c = c.replace(
            "const TREE = { target: '#open-tree', title: 'Skill Tree', text: 'Pick the one kind of problem\\nyou want to practice' };",
            "const TREE = { target: '#open-tree', title: '技能树', text: '自由挑选你想专项强化的\\n计算技巧来练习' };"
        )
        c = c.replace(
            "const TROPHY = { target: '#open-trophy', title: 'Trophies', text: 'You earn them by playing.\\nKeep coming back for more' };",
            "const TROPHY = { target: '#open-trophy', title: '奖杯成就', text: '每次练习都能积累成就。\\n坚持练习解锁更多奖励！' };"
        )
        c = c.replace(
            "const COLLECTION = { target: '#open-collect', title: 'Collection', text: 'Trophy rewards add backgrounds,\\nmusic, outfits and more\\nfor you to choose' };",
            "const COLLECTION = { target: '#open-collect', title: '收藏馆', text: '奖杯奖励可解锁背景、\\n音乐、角色装扮等丰富特效\\n供你随时更换！' };"
        )
        c = c.replace(
            "const LAST = { target: '#start', title: 'Not sure? Try My Level!', text: 'You can see this guide\\nagain with ?', recommend: true };",
            "const LAST = { target: '#start', title: '犹豫的话，先试试「我的等级」！', text: '点击问号 ？ 可以\\n随时再次查看说明', recommend: true };"
        )
        c = c.replace("<span id=\"guide-recommend\" hidden>${'Recommended'}</span>", "<span id=\"guide-recommend\" hidden>推荐</span>")
        c = c.replace("<button type=\"button\" id=\"guide-skip\" class=\"sub-btn\">${'Skip'}</button>", "<button type=\"button\" id=\"guide-skip\" class=\"sub-btn\">跳过</button>")
        c = c.replace("<button type=\"button\" class=\"sub-btn\" id=\"guide-back\">${'Back'}</button>", "<button type=\"button\" class=\"sub-btn\" id=\"guide-back\">上一步</button>")
        c = c.replace("<button type=\"button\" class=\"big-btn\" id=\"guide-next\">${'Next'}</button>", "<button type=\"button\" class=\"big-btn\" id=\"guide-next\">下一步</button>")
        c = c.replace("index === pages.length - 1 ? \"Let's go!\" : 'Next'", "index === pages.length - 1 ? '开始挑战！' : '下一步'")
        c = c.replace("`Page ${index + 1} of ${pages.length}`", "`第 ${index + 1} / ${pages.length} 页`")
        c = c.replace("document.createTextNode('You can see this guide\\nagain with ')", "document.createTextNode('点击问号 ')")
        c = c.replace("document.createTextNode('')", "document.createTextNode(' 可以随时再次查看本说明')")
    return c

with open('app/zh-CN/js/guide.js', 'w', encoding='utf-8') as f:
    f.write(make_guide(False))
with open('app/zh-TW/js/guide.js', 'w', encoding='utf-8') as f:
    f.write(make_guide(True))

print("Updated guide.js for zh-CN and zh-TW")
