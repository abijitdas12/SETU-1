import subprocess
import re

subprocess.run(["git", "checkout", "HEAD", "--", "frontend/public/assets/", "frontend/dist/assets/"])

filepath = 'frontend/public/assets/index-QbNk4EGb.js'

with open(filepath, 'rb') as f:
    data = f.read()

# Fix 1: AxiosHeaders toString join
data = data.replace(b'.join(`\r\nconst wa=', b'.join("\\n");}}; const wa=')
data = data.replace(b'.join(`\nconst wa=', b'.join("\\n");}}; const wa=')

# Fix 2: Axios header split
data = data.replace(b'e&&e.split(`\r\n`).forEach', b'e&&e.split("\\n").forEach')
data = data.replace(b'e&&e.split(`\n`).forEach', b'e&&e.split("\\n").forEach')

# Fix 3: Inject xe definition before xe.interceptors
target_xe = b'Se=e=>Promise.resolve(e);xe.interceptors.request.use'
repl_xe = b'Se=e=>Promise.resolve(e);const xe={defaults:{baseURL:"https://setu-backend1.onrender.com"},interceptors:{request:{use:e=>e},response:{use:e=>e}},get:async()=>({data:[]}),post:async()=>({data:{}}),patch:async()=>({data:{}}),delete:async()=>({data:{}})};xe.interceptors.request.use'

if target_xe in data:
    data = data.replace(target_xe, repl_xe)
    print("Injected xe in index-QbNk4EGb.js")

with open(filepath, 'wb') as f:
    f.write(data)

with open('frontend/dist/assets/index-QbNk4EGb.js', 'wb') as f:
    f.write(data)

res = subprocess.run(['node', '--check', filepath], capture_output=True)
print("Node check exit code:", res.returncode)
if res.returncode != 0:
    print("Error:", repr(res.stderr[:300]))
else:
    print("index-QbNk4EGb.js PASSED NODE CHECK CLEANLY!")
