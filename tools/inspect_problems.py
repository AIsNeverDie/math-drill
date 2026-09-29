import re

with open('app/ja/js/problems.js') as f_ja, open('app/en/js/problems.js') as f_en:
    ja = f_ja.read()
    en = f_en.read()

ja_labels = set(re.findall(r"label:\s*([`'\"][^`'\"]*?[`'\"])", ja))
en_labels = set(re.findall(r"label:\s*([`'\"][^`'\"]*?[`'\"])", en))

print('JA labels:', len(ja_labels), ja_labels)
print('EN labels:', len(en_labels), en_labels)
