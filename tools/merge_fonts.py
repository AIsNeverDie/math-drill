import urllib.request, pathlib
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

# Source URLs
zcool_url = 'https://raw.githubusercontent.com/google/fonts/main/ofl/zcoolkuaile/ZCOOLKuaiLe-Regular.ttf'
urllib.request.urlretrieve(zcool_url, '/tmp/zcool.ttf')

# For each Chinese game (zh-CN, zh-TW), let's check missing glyphs in dela and zen
for game_name in ['app/zh-CN', 'app/zh-TW']:
    game_path = pathlib.Path(game_name)
    chars = {chr(c) for c in range(0x20, 0x7f)}
    for f in [*game_path.glob('*.html'), *game_path.glob('*.css'), *game_path.glob('js/*.js')]:
        chars |= set(f.read_text(encoding='utf-8'))
    chars |= set('０１２３４５６７８９＋−×÷＝、。・！？「」（）ー〜…')
    
    # Subset ZCOOL KuaiLe as a chunky fallback
    zcool_font = TTFont('/tmp/zcool.ttf')
    options = Options()
    options.flavor = 'woff2'
    subsetter = Subsetter(options=options)
    subsetter.populate(text=''.join(chars))
    subsetter.subset(zcool_font)
    out_path = game_path / 'fonts' / 'zcool-kuaile.woff2'
    zcool_font.save(str(out_path))
    print(f'Saved {out_path}')

