import subprocess

subprocess.run(["git", "checkout", "HEAD", "--", "frontend/public/assets/index-v5.js", "frontend/dist/assets/index-v5.js"])

with open('frontend/public/assets/index-v5.js', 'rb') as f:
    data = f.read()

repls = [
    b'.join("\\n");}}; const wa=',
    b'.join("\\n");}};const wa=',
    b'.join("\\n")};;const wa=',
    b'.join("\\n")};; const wa=',
]

for try_repl in repls:
    test_data = data.replace(b'.join(`\nconst wa=', try_repl).replace(b'.join(`\r\nconst wa=', try_repl)
    test_data = test_data.replace(b'e&&e.split(`\n`).forEach', b'e&&e.split("\\n").forEach').replace(b'e&&e.split(`\r\n`).forEach', b'e&&e.split("\\n").forEach')
    with open('frontend/public/assets/index-v5.js', 'wb') as f:
        f.write(test_data)
    res = subprocess.run(['node', '--check', 'frontend/public/assets/index-v5.js'], capture_output=True)
    print(f"Try '{try_repl}': Exit code {res.returncode}")
    if res.returncode == 0:
        print("FOUND 100% VALID SYNTAX FIX!")
        with open('frontend/dist/assets/index-v5.js', 'wb') as f:
            f.write(test_data)
        break
    else:
        print("  Stderr:", repr(res.stderr[-200:]))
