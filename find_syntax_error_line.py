import subprocess

with open('frontend/public/assets/index-v5.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Testing {len(lines)} lines...")

for i in range(len(lines)):
    with open('temp_test.js', 'w', encoding='utf-8') as tf:
        tf.writelines(lines[:i+1])
    res = subprocess.run(['node', '--check', 'temp_test.js'], capture_output=True)
    if res.returncode != 0:
        err = res.stderr.decode('utf-8', errors='ignore')
        if 'Unexpected end of input' in err:
            continue
        print(f"Syntax Error introduced at line {i+1}: {err.strip()[:300]}")
        print(f"Line content snippet: {repr(lines[i][:150])}")
        break
