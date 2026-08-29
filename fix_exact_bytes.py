with open('frontend/public/assets/index-v5.js', 'rb') as f:
    data = f.read()

target = b'.join(`\r\nconst wa='
target_lf = b'.join(`\nconst wa='
replacement = b'.join("\\r\\n");const wa='

if target in data:
    data = data.replace(target, replacement)
    print("Exact byte replacement (CRLF) target found!")
elif target_lf in data:
    data = data.replace(target_lf, replacement)
    print("Exact byte replacement (LF) target found!")
else:
    print("Target byte sequence not found.")

with open('frontend/public/assets/index-v5.js', 'wb') as f:
    f.write(data)
with open('frontend/dist/assets/index-v5.js', 'wb') as f:
    f.write(data)

print("Done writing byte fix.")
