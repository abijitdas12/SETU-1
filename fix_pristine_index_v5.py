import subprocess

subprocess.run(["git", "checkout", "HEAD", "--", "frontend/public/assets/index-v5.js", "frontend/dist/assets/index-v5.js"])

with open('frontend/public/assets/index-v5.js', 'rb') as f:
    data = f.read()

target_crlf = b'.join(`\r\nconst wa='
target_lf = b'.join(`\nconst wa='
replacement = b'.join("\\n");const wa='

if target_crlf in data:
    data = data.replace(target_crlf, replacement)
    print("Replaced CRLF target")
elif target_lf in data:
    data = data.replace(target_lf, replacement)
    print("Replaced LF target")
else:
    print("Neither target found!")

with open('frontend/public/assets/index-v5.js', 'wb') as f:
    f.write(data)
with open('frontend/dist/assets/index-v5.js', 'wb') as f:
    f.write(data)

print("Wrote files.")
