import glob
import subprocess

subprocess.run(["git", "checkout", "HEAD", "--", "frontend/public/assets/", "frontend/dist/assets/"])

js_files = glob.glob('frontend/public/assets/*.js') + glob.glob('frontend/dist/assets/*.js')

for filepath in js_files:
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # Fix AxiosHeaders toString class method join + const wa
    data = data.replace(b'.join(`\r\nconst wa=', b'.join("\\n");}}; const wa=')
    data = data.replace(b'.join(`\nconst wa=', b'.join("\\n");}}; const wa=')
    
    # Fix Axios header split
    data = data.replace(b'e&&e.split(`\r\n`).forEach', b'e&&e.split("\\n").forEach')
    data = data.replace(b'e&&e.split(`\n`).forEach', b'e&&e.split("\\n").forEach')
    
    with open(filepath, 'wb') as f:
        f.write(data)
    
    res = subprocess.run(['node', '--check', filepath], capture_output=True)
    if res.returncode == 0:
        print(f"[OK] {filepath} PASSED syntax check cleanly!")
    else:
        print(f"[FAIL] {filepath} FAILED syntax check: {res.stderr[:200]}")

print("All asset files processed.")
