# 估計每幀相機繞行角度: 相鄰幀用光流量測背景水平位移 ( 排除中央主體 ), 累加後正規化成 360 度.
# usage: analyze_angles.py <frames_dir>  ->  印出 JSON 陣列 ( 每幀角度, 0 起算 )
import sys, glob, json, cv2, numpy as np
files = sorted(glob.glob(sys.argv[1] + '/*.jpg'))
W = 480
def load(f):
  im = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
  return cv2.resize(im, (W, int(im.shape[0] * W / im.shape[1])), interpolation=cv2.INTER_AREA)
ims = [load(f) for f in files]
h = ims[0].shape[0]
mask = np.ones((h, W), bool); mask[:, int(W * .3):int(W * .7)] = False  # 中央 40% 是主體, 不計
dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)  # 對大位移比 Farneback 穩
raw = []
for i in range(len(ims)):
  a, b = ims[i], ims[(i + 1) % len(ims)]  # 最後一幀接回第一幀也算一步
  flow = dis.calc(a, b, None)
  dx = flow[..., 0][mask]
  raw.append(float(np.median(dx)))
raw = np.array(raw)
sign = np.sign(np.median(raw))
steps = np.clip(raw * sign, 0, None)  # 方向相反的步 ( 量測雜訊 ) 視為 0
ang = np.concatenate([[0], np.cumsum(steps)[:-1]]) / steps.sum() * 360
print(json.dumps([round(float(x), 2) for x in ang]))
sys.stderr.write('raw dx(px): ' + ' '.join(f'{s:.1f}' for s in raw) + '\n')
