"""Score: gemiddelde afstand (px) van de foto-omtrek tegen de lucht (kruin + voorkant + kaak) tot de render-omtrek, na uitlijnen op het oog."""
import sys, glob, subprocess
import numpy as np
from PIL import Image
REF = '../referenties/jordi_great_potoo_bek_open_duo.webp'
EX, EY, ER = 380.0, 225.0, 30.0
f = np.asarray(Image.open(REF).convert('RGB')).astype(int)[:, :640]
# omtrek met de hand overgetrokken (originele pixels): kruin -> snaveltip -> verre kaakrand -> kaakpunt -> keel
LIJN = [(325, 125), (400, 110), (450, 125), (485, 170), (505, 210), (520, 240), (522, 245), (520, 280), (505, 330),
        (485, 380), (460, 420), (430, 450), (410, 465), (405, 480), (410, 520)]
fp = []
for (x0, y0), (x1, y1) in zip(LIJN, LIJN[1:]):
    n = int(np.hypot(x1 - x0, y1 - y0) / 2) + 1
    for t in np.linspace(0, 1, n, endpoint=False): fp.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
fp = np.array(fp)
def oog(r):
    a = r[..., 3] > 128; zw = a & (r[..., :3].max(-1) < 45) & ((r[..., 2] - r[..., 0]) < 10)
    from collections import deque
    lab = np.zeros(zw.shape, int); n = 0; best = []
    for y0, x0 in zip(*np.nonzero(zw)):
        if lab[y0, x0]: continue
        n += 1; q = deque([(y0, x0)]); lab[y0, x0] = n; pts = []
        while q:
            y, x = q.popleft(); pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                Y, X = y + dy, x + dx
                if 0 <= Y < zw.shape[0] and 0 <= X < zw.shape[1] and zw[Y, X] and not lab[Y, X]: lab[Y, X] = n; q.append((Y, X))
        if len(pts) > len(best): best = pts
    p = np.array(best); return p[:, 1].mean(), p[:, 0].mean(), np.sqrt(len(p) / np.pi)
if __name__ == "__main__":
  res = []
  for fn in sorted(glob.glob(sys.argv[1] + '/*.png')):
      r = np.asarray(Image.open(fn).convert('RGBA')).astype(int)
      cx, cy, rr = oog(r); s = ER / rr
      a = r[..., 3] > 128
      rd = a & ~(np.roll(a, 1, 0) & np.roll(a, -1, 0) & np.roll(a, 1, 1) & np.roll(a, -1, 1))
      ry, rx = np.nonzero(rd)
      rp = np.stack([(rx - cx) * s + EX, (ry - cy) * s + EY], 1)
      rp = rp[(rp[:, 0] > 280) & (rp[:, 1] < 490)]
      d = np.sqrt(((fp[:, None, :] - rp[None, ::3, :]) ** 2).sum(-1)).min(1)
      res.append((d.mean(), fn.split('/')[-1], round(s, 2)))
  for r_ in sorted(res): print(round(r_[0], 1), r_[1], r_[2])
