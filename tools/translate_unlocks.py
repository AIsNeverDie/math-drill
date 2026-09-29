# Unlocks translations
with open('app/en/js/unlocks.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Categories:
# bg: '背景'
# mark: '批改印章' / '批改印章'
# particle: '彩带碎屑' / '碎紙彩帶'
# music: '背景音乐' / '背景音樂'
# costume: '角色装扮' / '角色造型'
# color: '多帕吉颜色' / '多帕吉顏色'
# crowd: '喝彩观众' / '喝采觀眾'
# finale: '通关庆典' / '通關慶典'

cats_cn = """export const CATS = [
  { key: 'bg', name: '背景' },
  { key: 'mark', name: '批改印章' },
  { key: 'particle', name: '彩带特效' },
  { key: 'music', name: '音乐' },
  { key: 'costume', name: '装扮' },
  { key: 'color', name: '身体颜色' },
  { key: 'crowd', name: '观众' },
  { key: 'finale', name: '庆典' },
];"""

cats_tw = """export const CATS = [
  { key: 'bg', name: '背景' },
  { key: 'mark', name: '批改印章' },
  { key: 'particle', name: '碎紙特效' },
  { key: 'music', name: '音樂' },
  { key: 'costume', name: '造型' },
  { key: 'color', name: '身體顏色' },
  { key: 'crowd', name: '觀眾' },
  { key: 'finale', name: '慶典' },
];"""

items_map = {
  'bg:classic': ('经典放射线', '經典放射線'),
  'mark:hanamaru': ('大红花圆圈', '小紅花圓圈'),
  'particle:classic': ('纸屑彩带', '碎紙彩帶'),
  'music:classic': ('木琴进行曲', '木琴進行曲'),
  'costume:none': ('无', '無'),
  'color:pink': ('粉红', '粉紅'),
  'crowd:classic': ('多彩伙伴', '多彩夥伴'),
  'finale:classic': ('巨大多帕吉', '巨大多帕吉'),

  'costume:cap': ('小帽子', '小帽子'),
  'particle:note': ('音符', '音符'),
  'mark:stamp': ('优秀印章', '優秀印章'),
  'bg:night': ('星空夜景', '星空夜景'),
  'color:blue': ('天蓝', '天藍'),
  'finale:fireworks': ('烟花大会', '煙火大會'),
  'music:chip': ('8位元电子音', '8位元電子音'),
  'crowd:costume': ('盛装伙伴', '盛裝夥伴'),

  'bg:sea': ('深海气泡', '深海氣泡'),
  'bg:festival': ('祭典夏日', '祭典夏日'),
  'bg:paper': ('折纸艺术', '摺紙藝術'),
  'bg:space': ('浩瀚宇宙', '浩瀚宇宙'),
  'mark:medal': ('金牌勋章', '金牌勳章'),
  'mark:crown': ('皇冠', '皇冠'),
  'mark:ring': ('烟花光环', '煙火光環'),
  'particle:petal': ('花瓣飘落', '花瓣飄落'),
  'particle:digit': ('飞舞数字', '飛舞數字'),
  'particle:bubble': ('梦幻气泡', '夢幻氣泡'),
  'particle:candy': ('美味糖果', '美味糖果'),

  'music:matsuri': ('热烈祭典', '熱烈祭典'),
  'music:brass': ('欢快铜管', '歡快銅管'),
  'music:electro': ('动感电音', '動感電音'),
  'finale:rocket': ('火箭升空', '火箭升空'),
  'finale:parade': ('欢乐游行', '歡樂遊行'),

  'color:yellow': ('亮黄', '亮黃'),
  'color:mint': ('薄荷绿', '薄荷綠'),
  'color:violet': ('梦幻紫', '夢幻紫'),
  'color:coral': ('珊瑚红', '珊瑚紅'),
  'color:snow': ('雪白', '雪白'),
  'color:gold': ('闪耀金', '閃耀金'),
  'color:rainbow': ('彩虹炫彩', '彩虹炫彩'),

  'costume:ribbon': ('蝴蝶结', '蝴蝶結'),
  'costume:glasses': ('帅气眼镜', '帥氣眼鏡'),
  'costume:crown': ('小皇冠', '小皇冠'),
  'costume:flower': ('向日葵', '向日葵'),
  'costume:bandana': ('探险头巾', '探險頭巾'),
  'costume:headphone': ('音乐耳机', '音樂耳機'),
  'costume:chef': ('主厨帽', '主廚帽'),
  'costume:stars': ('星星发夹', '星星髮夾'),

  'crowd:rainbow': ('彩虹小队', '彩虹小隊'),
  'crowd:twins': ('粉红大队', '粉紅大隊'),
}

import re

def update_unlocks(is_tw=False):
    c = text
    # replace CATS
    c = re.sub(r'export const CATS = \[[\s\S]*?\];', cats_tw if is_tw else cats_cn, c)
    # replace item names
    for item_id, names in items_map.items():
        name = names[1] if is_tw else names[0]
        c = re.sub(rf"({{ id: '{item_id}', cat: '.*?', name: )'.*?'(,)", rf"\g<1>'{name}'\g<2>", c)
    return c

with open('app/zh-CN/js/unlocks.js', 'w', encoding='utf-8') as f:
    f.write(update_unlocks(False))
with open('app/zh-TW/js/unlocks.js', 'w', encoding='utf-8') as f:
    f.write(update_unlocks(True))

print("Updated unlocks.js for zh-CN and zh-TW")
