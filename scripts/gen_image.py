import os, sys, json, base64, urllib.request
env = {}
for l in open(os.path.expanduser('~/.ssh/ai/envs')):
    l = l.strip()
    if '=' in l and not l.startswith('#'):
        k, v = l.split('=', 1); env[k.replace('export ', '').strip()] = v.strip().strip('"\'')
prompt = sys.argv[1]; out = sys.argv[2]; model = sys.argv[3] if len(sys.argv) > 3 else 'gpt-image-1'
req = urllib.request.Request('https://api.openai.com/v1/images/generations',
  data=json.dumps({'model': model, 'prompt': prompt, 'size': '1024x1536', 'quality': 'high', 'n': 1}).encode(),
  headers={'Authorization': 'Bearer ' + env['OPENAI_API_KEY'], 'Content-Type': 'application/json'})
try:
  r = json.load(urllib.request.urlopen(req, timeout=300))
except urllib.error.HTTPError as e:
  print(e.code, e.read().decode()[:500]); sys.exit(1)
open(out, 'wb').write(base64.b64decode(r['data'][0]['b64_json'])); print('saved', out)
