# donkere segmenten langs stralen vanaf het irismidden: model (L<70) vs sprite (palet-L<100); gebruik: python3 profiel.py sprite.png
import numpy as np, sys
from PIL import Image
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(float); k = 12.703
LM = M @ [.299, .587, .114]
S = Image.open(sys.argv[1]); a = np.array(S); P = np.array(S.getpalette()[:48]).reshape(16, 3) @ [.299, .587, .114]
cx, cy = 18.5, 34.9
def seg(f, rs):
    out = []; inn = False
    for r, v in zip(rs, f):
        if v and not inn: s0 = r; inn = True
        if not v and inn: out.append((s0, r)); inn = False
    if inn: out.append((s0, rs[-1]))
    return out
for ang in range(0, 360, 15):
    t = np.radians(ang); dx, dy = np.cos(t), -np.sin(t); rs = np.arange(2, 13.5, 0.1)
    m = []; s = []
    for r in rs:
        x, y = cx + r * dx, cy + r * dy
        m.append(LM[int(143 + (y - 7) * k), int(103 + x * k)] < 70)
        v = a[int(y), int(x)]; s.append(v != 0 and P[v] < 100 and v not in (9, 10, 11))
    print('%3d model: %-55s sprite: %s' % (ang, ' '.join('%.1f-%.1f' % q for q in seg(m, rs)), ' '.join('%.1f-%.1f' % q for q in seg(s, rs))))
