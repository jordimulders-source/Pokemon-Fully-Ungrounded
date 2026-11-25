# radiaalprofielen rond het irismidden (18,5; 34,9): model (helderheid, minima = donkere lijnen) en sprite
import numpy as np, sys
from PIL import Image
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(float); k = 12.703
L = M @ [0.299, 0.587, 0.114]
cx, cy = 18.5, 34.9
def mod(x, y):
    mx, my = 103 + x * k, 143 + (y - 7) * k
    return L[int(round(my)), int(round(mx))], M[int(round(my)), int(round(mx))]
sp = sys.argv[1] if len(sys.argv) > 1 else '../r14/sprite.png'
S = Image.open(sp); a = np.array(S); P = np.array(S.getpalette()[:48]).reshape(16, 3)
for ang in range(0, 360, 22):
    t = np.radians(ang); dx, dy = np.cos(t), -np.sin(t)
    rs = np.arange(0, 15.01, 0.25); v = np.array([mod(cx + r * dx, cy + r * dy)[0] for r in rs])
    mins = [rs[i] for i in range(1, len(rs) - 1) if v[i] < v[i - 1] and v[i] <= v[i + 1] and v[i] < 140]
    ss = ''
    for r in np.arange(0, 15, 1.0):
        x, y = int(np.floor(cx + r * dx + .5 * 0 + 0)), int(np.floor(cy + r * dy))
        x = int(np.floor(cx + r * dx)); y = int(np.floor(cy + r * dy))
        ss += '.123456789ABCDEF'[a[y, x]] if 0 <= x < 64 and 0 <= y < 64 else ' '
    print('%3d  model minima: %s' % (ang, ' '.join('%.2f(%d)' % (m, v[int(m * 4)]) for m in mins)))
    print('     model L: ' + ' '.join('%3d' % v[int(r * 4)] for r in np.arange(0, 15, 1.0)))
    print('     sprite : ' + '   '.join(ss))
