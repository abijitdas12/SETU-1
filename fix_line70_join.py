with open('frontend/public/assets/index-v5.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines before fix: {len(lines)}")

line69 = lines[69].rstrip('\r\n')
line70 = lines[70].lstrip()

print("Line 69 end:", repr(line69[-30:]))
print("Line 70 start:", repr(line70[:30]))

if line69.endswith("e&&e.split(`") and line70.startswith("`).forEach"):
    fixed_line = line69[:-12] + 'e&&e.split("\\n").forEach' + line70[10:]
    lines[69] = fixed_line + '\n'
    lines.pop(70)
    print("MATCH AND MERGE SUCCESSFUL!")

with open('frontend/public/assets/index-v5.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

with open('frontend/dist/assets/index-v5.js', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done.")
