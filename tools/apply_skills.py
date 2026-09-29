import re
import sys

exec(open('tools/translate_skills.py').read())

def update_skills_file(path, lang_idx, lanes_str):
    with open('app/en/js/skills.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # replace LANES
    content = re.sub(r'export const LANES = \[.*?\];', lanes_str, content)
    
    for sk_id, names in skill_names.items():
        name = names[lang_idx]
        pattern = re.compile(rf"({{ id: '{sk_id}', name: )'.*?'(,)")
        content = pattern.sub(rf"\g<1>'{name}'\g<2>", content)
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated', path)

update_skills_file('app/zh-CN/js/skills.js', 0, lanes_cn)
update_skills_file('app/zh-TW/js/skills.js', 1, lanes_tw)
