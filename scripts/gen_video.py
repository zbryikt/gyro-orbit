# usage: gen_video.py <image> <out.mp4> [duration] [resolution] [prompt]
import os, sys, json, time, base64, urllib.request
env = {}
for l in open(os.path.expanduser('~/.ssh/ai/envs')):
    l = l.strip()
    if '=' in l and not l.startswith('#'):
        k, v = l.split('=', 1); env[k.replace('export ', '').strip()] = v.strip().strip('"\'')
KEY = env['FALAI_API_KEY']
MODEL = 'minimax/h3-max-turbo/image-to-video'
img, out = sys.argv[1], sys.argv[2]
duration = float(sys.argv[3]) if len(sys.argv) > 3 else 1
resolution = sys.argv[4] if len(sys.argv) > 4 else '768P'
prompt = sys.argv[5] if len(sys.argv) > 5 else (
  "Bullet-time freeze frame. Time is completely frozen: the couple and everything in the scene are perfectly still statues. "
  "The camera makes one full 360-degree orbit around the couple at constant speed, keeping them centered in frame, "
  "revealing their sides and backs and the street behind the camera, and ends exactly where it started, so the last frame is identical to the first frame.")
uri = 'data:image/jpeg;base64,' + base64.b64encode(open(img, 'rb').read()).decode()
def call(url, data=None, method=None):
  req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, method=method,
    headers={'Authorization': 'Key ' + KEY, 'Content-Type': 'application/json'})
  try: return json.load(urllib.request.urlopen(req, timeout=120))
  except urllib.error.HTTPError as e: print(e.code, e.read().decode()[:800]); sys.exit(1)
body = {'prompt': prompt, 'image_url': uri, 'end_image_url': uri, 'duration': duration,
        'resolution': resolution, 'prompt_expansion_mode': 'disabled'}
r = call('https://queue.fal.run/' + MODEL, body)
print('request', r['request_id'], flush=True)
while True:
  s = call(r['status_url'])
  if s['status'] == 'COMPLETED': break
  time.sleep(4)
res = call(r['response_url'])
urllib.request.urlretrieve(res['video']['url'], out)
print('saved', out, res['video']['url'])
