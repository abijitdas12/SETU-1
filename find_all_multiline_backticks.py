import re

filepath = 'frontend/public/assets/index-v5.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Search for backtick followed by newlines
matches = list(re.finditer(r'`[\r\n]+[^`]*?`', content))
print(f"Found {len(matches)} multiline backtick matches:")

for i, m in enumerate(matches):
    snippet = m.group(0).replace('\r', '\\r').replace('\n', '\\n')
    start = max(0, m.start() - 30)
    end = min(len(content), m.end() + 30)
    context = content[start:end].replace('\r', '\\r').replace('\n', '\\n')
    print(f"[{i+1}] at pos {m.start()}: context = {context}")

