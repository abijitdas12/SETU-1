import subprocess

subprocess.run(["git", "checkout", "HEAD", "--", "frontend/public/assets/index-v5.js", "frontend/dist/assets/index-v5.js"])

with open('frontend/public/assets/index-v5.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Original lines count: {len(lines)}")

i = 0
fixed_lines = []
while i < len(lines):
    current = lines[i].rstrip('\r\n')
    while current.count('`') % 2 != 0 and i + 1 < len(lines):
        i += 1
        next_part = lines[i].lstrip()
        current = current + "\\n" + next_part.rstrip('\r\n')
        print(f"Multi-line backtick merged line {i}")
    
    current = current.replace('split(`\\n`)', 'split("\\n")')
    current = current.replace('join(`\\n`)', 'join("\\n")')
    
    fixed_lines.append(current + '\n')
    i += 1

content = "".join(fixed_lines)

with open('frontend/public/assets/index-v5.js', 'w', encoding='utf-8') as f:
    f.write(content)

with open('frontend/dist/assets/index-v5.js', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"New total lines: {len(content.splitlines())}")
