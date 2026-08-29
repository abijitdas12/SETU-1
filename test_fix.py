import subprocess
import re

subprocess.run(["git", "checkout", "HEAD", "--", "frontend/public/assets/index-v5.js", "frontend/dist/assets/index-v5.js"])

with open('frontend/public/assets/index-v5.js', 'rb') as f:
    data = f.read()

data = data.replace(b'.join(`\r\nconst wa=', b'.join("\\n")} } const wa=')
data = data.replace(b'.join(`\nconst wa=', b'.join("\\n")} } const wa=')

data = re.sub(rb'return e&&e\.split\(`[\r\n]*`\)\.forEach', rb'return e&&e.split("\\n").forEach', data)
data = re.sub(rb'return e&&e\.split\(`[\r\n]+', rb'return e&&e.split("\\n").forEach', data)

with open('frontend/public/assets/index-v5.js', 'wb') as f:
    f.write(data)

res = subprocess.run(['node', '--check', 'frontend/public/assets/index-v5.js'], capture_output=True)
print("Exit code:", res.returncode)
print("Stderr raw:", repr(res.stderr[-1000:]))
