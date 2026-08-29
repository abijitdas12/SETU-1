import re

filepath = 'frontend/public/assets/index-v5.js'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Search for lines ending with .join(` and fix the split
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.rstrip().endswith(".join(`") and i + 1 < len(lines):
        next_line = lines[i+1]
        if next_line.lstrip().startswith("`).forEach"):
            # Merge line and next_line
            merged_line = line.rstrip()[:-7] + '.join("\\n").forEach' + next_line.lstrip()[10:]
            new_lines.append(merged_line)
            i += 2
            continue
        elif next_line.lstrip().startswith("`)."):
            rest = next_line.lstrip()[2:]
            merged_line = line.rstrip()[:-7] + '.join("\\n").' + rest
            new_lines.append(merged_line)
            i += 2
            continue
    new_lines.append(line)

fixed_content = "".join(new_lines)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

with open('frontend/dist/assets/index-v5.js', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print(f"Fixed content written. New line count: {len(new_lines)}")
