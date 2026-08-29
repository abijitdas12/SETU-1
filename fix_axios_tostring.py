with open('frontend/public/assets/index-v5.js', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Replace toString template string join followed by const wa=
pattern = r'toString\(\)\{return Object\.entries\(this\.toJSON\(\)\)\.map\(\(\[t,n\]\)=>t\+": "\+n\)\.join\(`[\r\n]+const wa='
replacement = 'toString(){return Object.entries(this.toJSON()).map(([t,n])=>t+": "+n).join("\\n")}\nconst wa='

new_content, count = re.subn(pattern, replacement, content)
print(f"Axios toString replace count: {count}")

with open('frontend/public/assets/index-v5.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

with open('frontend/dist/assets/index-v5.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Write complete.")
