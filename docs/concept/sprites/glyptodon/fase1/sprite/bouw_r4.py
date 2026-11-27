# r4 = r3-varianten met de lijnen rond het oog in de binnenlijntint (12 = 52/48/45) i.p.v. zwart,
# zodat alleen de pupil zwart blijft (Jordi: "fase 1 leest geen enkel oog als een oog, omdat de lijnen om het oog heen dezelfde kleur zijn als de pupil").
# Pupil = de zwarte pixel in het oogvak met de meeste witte buren (8-buren). Alle andere zwarte pixels in het oogvak
# en zwarte kop-pixels direct rond het oogvak (x9-14, y46-50, niet op de silhouetrand) -> 12. Verder pixelgelijk aan r3/r2.
import numpy as np
from PIL import Image
D = __file__.rsplit('/', 1)[0]
r2 = np.load(D + '/r2.npy'); pal = Image.open(D + '/r2.png').getpalette()
SAND = ['fecf', 'ffcc', 'fffe']
VAR = {'A': [r[::-1] for r in SAND[::-1]], 'B': [r[::-1] for r in SAND], 'C': SAND[::-1], 'D_extra': SAND}
MAP = {'f': 1, 'c': 11, 'e': 5}
H, W = r2.shape
def rand(a, y, x):
    return any(a[yy, xx] == 0 for yy in range(y-1, y+2) for xx in range(x-1, x+2) if 0 <= yy < H and 0 <= xx < W)
for k, rijen in VAR.items():
    a = r2.copy()
    for j, rij in enumerate(rijen):
        for i, ch in enumerate(rij): a[47 + j, 10 + i] = MAP[ch]
    zwart = [(y, x) for y in range(47, 50) for x in range(10, 14) if a[y, x] == 1]
    wit = lambda y, x: sum(a[yy, xx] == 11 for yy in range(y-1, y+2) for xx in range(x-1, x+2))
    pupil = max(zwart, key=lambda p: (wit(*p), -abs(p[1] - 11.5)))
    n = 0
    for y in range(46, 51):
        for x in range(9, 15):
            if a[y, x] == 1 and (y, x) != pupil and not rand(a, y, x): a[y, x] = 12; n += 1
    assert (a[:46] != r2[:46]).sum() == 0 and (a[51:] != r2[51:]).sum() == 0 and (a[:, :9] != r2[:, :9]).sum() == 0 and (a[:, 15:] != r2[:, 15:]).sum() == 0
    im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(pal); im.save(D + f'/r4_{k}.png', transparency=0)
    print(k, 'pupil (x,y)=', (pupil[1], pupil[0]), 'lijnpixels zwart->12:', n)
    for y in range(46, 51): print('   ', ''.join({0: '.', 1: '#', 11: 'O', 12: '+', 5: 'e'}.get(int(v), 'x') for v in a[y, 9:15]))
