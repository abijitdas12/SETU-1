import re

filepath = 'frontend/public/assets/index-v5.js'

with open(filepath, 'rb') as f:
    data = f.read()

pattern = rb'\.join\(`[\r\n]+`\)\.forEach'
replacement = rb'.join("\\r\\n").forEach'

data, count = re.subn(pattern, replacement, data)
print(f"Replaced count: {count}")

with open(filepath, 'wb') as f:
    f.write(data)

with open('frontend/dist/assets/index-v5.js', 'wb') as f:
    f.write(data)

print("Fix complete.")
