import re

filepath = 'frontend/public/assets/index-v5.js'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'e&&e\.split\(`[\r\n]+`\)\.forEach'
replacement = r'e&&e.split("\n").forEach'

new_content, count = re.subn(pattern, replacement, content)
print(f"Replaced count: {count}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

with open('frontend/dist/assets/index-v5.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fix completed successfully.")
