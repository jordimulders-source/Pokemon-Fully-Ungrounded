# kale reductie van het model op het spriteraster (x 4-40, y 18-50): per spritepixel het blok modelpixels,
# dichtstbijzijnde kleur uit het r14-palet (modus van het blok + min-helderheid voor dunne lijnen)
import numpy as np
from PIL import Image
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(float); k = 12.703
S = Image.open('../r14/sprite.png'); P = np.array(S.getpalette()[:48]).reshape(16, 3).astype(float)
def blok(x, y):
    x0, x1 = int(round(103 + x * k)), int(round(103 + (x + 1) * k)); y0, y1 = int(round(143 + (y - 7) * k)), int(round(143 + (y - 6) * k))
    return M[y0:y1, x0:x1].reshape(-1, 3)
H = '.123456789ABCDEF'
def cls(c):
    if c.min() > 248: return 0
    d = ((P[1:] - c) ** 2).sum(1); return 1 + d.argmin()
out = {}
for mode in ('modus', 'centrum', 'donkerst'):
    g = np.zeros((64, 64), int)
    for y in range(18, 51):
        for x in range(4, 41):
            b = blok(x, y)
            if mode == 'centrum': c = b[len(b) // 2 + 6]
            elif mode == 'donkerst':
                Lb = b @ [.299, .587, .114]; c = b[Lb.argmin()] if (Lb < 45).mean() > 0.25 else np.median(b, 0)
            else:
                cs = np.array([cls(q) for q in b[::3]]); g[y, x] = np.bincount(cs).argmax(); continue
            g[y, x] = cls(c)
    out[mode] = g
    np.save('kaal_%s.npy' % mode, g)
print('   ' + ''.join(str(x % 10) for x in range(4, 41)))
for y in range(18, 51):
    print('%2d ' % y + '  '.join(''.join(H[v] for v in out[m][y, 4:41]) for m in ('modus', 'donkerst')))
