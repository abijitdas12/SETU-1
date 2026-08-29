import glob
import subprocess

subprocess.run(["git", "checkout", "HEAD", "--", "frontend/public/assets/", "frontend/dist/assets/"])

js_files = glob.glob('frontend/public/assets/*.js') + glob.glob('frontend/dist/assets/*.js')

xe_code = b"""var xe = {
  baseURL: "https://setu-backend1.onrender.com",
  interceptors: {
    request: { use: function(fn1, fn2){ this.fn = fn1; } },
    response: { use: function(fn1, fn2){ this.fn = fn1; } }
  },
  async request(config) {
    let url = config.url || '';
    if (!url.startsWith('http')) {
      url = this.baseURL + (url.startsWith('/') ? '' : '/') + url;
    }
    let headers = config.headers || {};
    const token = localStorage.getItem('access_token');
    if (token) { headers.Authorization = 'Bearer ' + token; }
    try {
      const res = await fetch(url, {
        method: config.method || 'GET',
        headers: { 'Content-Type': 'application/json', ...headers },
        body: config.data ? (typeof config.data === 'string' ? config.data : JSON.stringify(config.data)) : undefined
      });
      const data = await res.json().catch(() => ({}));
      return { status: res.status, data: data, headers: res.headers };
    } catch (err) {
      return { status: 500, data: [], headers: {} };
    }
  },
  get(url, config={}) { return this.request({ ...config, method: 'GET', url }); },
  post(url, data, config={}) { return this.request({ ...config, method: 'POST', url, data }); },
  put(url, data, config={}) { return this.request({ ...config, method: 'PUT', url, data }); },
  patch(url, data, config={}) { return this.request({ ...config, method: 'PATCH', url, data }); },
  delete(url, config={}) { return this.request({ ...config, method: 'DELETE', url }); }
};"""

for filepath in js_files:
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # 1. Fix AxiosHeaders toString class method join + const wa
    data = data.replace(b'.join(`\r\nconst wa=', b'.join("\\n");}}; const wa=')
    data = data.replace(b'.join(`\nconst wa=', b'.join("\\n");}}; const wa=')
    
    # 2. Fix Axios header split
    data = data.replace(b'e&&e.split(`\r\n`).forEach', b'e&&e.split("\\n").forEach')
    data = data.replace(b'e&&e.split(`\n`).forEach', b'e&&e.split("\\n").forEach')
    
    # 3. Inject bulletproof xe client
    target_xe = b'Se=e=>Promise.resolve(e);xe.interceptors.request.use'
    repl_xe = b'Se=e=>Promise.resolve(e);' + xe_code + b';xe.interceptors.request.use'

    if target_xe in data:
        data = data.replace(target_xe, repl_xe)
        print(f"Injected bulletproof xe in {filepath}")

    with open(filepath, 'wb') as f:
        f.write(data)
    
    res = subprocess.run(['node', '--check', filepath], capture_output=True)
    if res.returncode == 0:
        print(f"[OK] {filepath} PASSED syntax check cleanly!")
    else:
        print(f"[FAIL] {filepath} FAILED syntax check: {res.stderr[:200]}")

print("Processing complete.")
