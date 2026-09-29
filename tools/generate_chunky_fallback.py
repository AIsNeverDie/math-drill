import urllib.request, pathlib
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

# For zh-CN:
# Let's inspect DelaGothicOne and see which characters from zh-CN files are missing in Dela.
dela_font = TTFont('app/zh-CN/fonts/dela-gothic-one.woff2')
dela_cmap = dela_font.getBestCmap()

# Load ZCOOL KuaiLe
zcool_font = TTFont('/tmp/zcool.ttf')
zcool_cmap = zcool_font.getBestCmap()

game_path = pathlib.Path('app/zh-CN')
chars = set()
for f in [*game_path.glob('*.html'), *game_path.glob('*.css'), *game_path.glob('js/*.js')]:
    chars |= set(f.read_text(encoding='utf-8'))

missing_in_dela = {c for c in chars if ord(c) >= 0x4e00 and ord(c) not in dela_cmap and ord(c) in zcool_cmap}
print('Missing in Dela but in ZCOOL for zh-CN:', len(missing_in_dela), ''.join(sorted(missing_in_dela)))

# Subset ZCOOL KuaiLe with these missing chars (and full text) as Dela Fallback
options = Options()
options.flavor = 'woff2'
subsetter = Subsetter(options=options)
subsetter.populate(text=''.join(chars))
subsetter.subset(zcool_font)
zcool_font.save('app/zh-CN/fonts/chunky-fallback.woff2')
print('Saved app/zh-CN/fonts/chunky-fallback.woff2')

