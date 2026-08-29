import glob
import subprocess

subprocess.run(["git", "checkout", "HEAD", "--", "frontend/public/assets/", "frontend/dist/assets/"])

js_files = glob.glob('frontend/public/assets/*.js') + glob.glob('frontend/dist/assets/*.js')

for filepath in js_files:
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # 1. Fix AxiosHeaders toString class method join + const wa
    data = data.replace(b'.join(`\r\nconst wa=', b'.join("\\n");}}; const wa=')
    data = data.replace(b'.join(`\nconst wa=', b'.join("\\n");}}; const wa=')
    
    # 2. Fix Axios header split
    data = data.replace(b'e&&e.split(`\r\n`).forEach', b'e&&e.split("\\n").forEach')
    data = data.replace(b'e&&e.split(`\n`).forEach', b'e&&e.split("\\n").forEach')
    
    # 3. Inject const xe definition if xe.interceptors is present but const xe is missing
    if b'xe.interceptors.request.use' in data and b'const xe=' not in data and b'const xe =' not in data:
        target_xe = b'Se=e=>Promise.resolve(e);xe.interceptors.request.use'
        repl_xe = b'Se=e=>Promise.resolve(e);const xe=axios.create({baseURL: "https://setu-backend1.onrender.com", headers: { "Content-Type": "application/json" } });xe.interceptors.request.use'
        if target_xe in data:
            data = data.replace(target_xe, repl_xe)
            print(f"Injected const xe in {filepath}")

    with open(filepath, 'wb') as f:
        f.write(data)
    
    res = subprocess.run(['node', '--check', filepath], capture_output=True)
    if res.returncode == 0:
        print(f"[OK] {filepath} PASSED syntax check cleanly!")
    else:
        print(f"[FAIL] {filepath} FAILED syntax check: {res.stderr[:200]}")

print("Processing complete.")
