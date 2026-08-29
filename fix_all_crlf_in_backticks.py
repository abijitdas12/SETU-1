import subprocess

subprocess.run(["git", "checkout", "HEAD", "--", "frontend/public/assets/index-v5.js", "frontend/dist/assets/index-v5.js"])

with open('frontend/public/assets/index-v5.js', 'rb') as f:
    data = f.read()

parts = data.split(b'`')
print(f"Parts count: {len(parts)}")

new_parts = []
for i, p in enumerate(parts):
    if i % 2 == 1:
        # Replace \r\n inside backticks with \n
        p = p.replace(b'\r\n', b'\n')
    new_parts.append(p)

fixed_data = b'`'.join(new_parts)

with open('frontend/public/assets/index-v5.js', 'wb') as f:
    f.write(fixed_data)

with open('frontend/dist/assets/index-v5.js', 'wb') as f:
    f.write(fixed_data)

print("CRLF template string normalization complete.")
