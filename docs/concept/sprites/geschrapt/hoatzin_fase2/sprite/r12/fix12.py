# fix12.py (r12): kleine opschoning na alle onderdelen: losse 3 tussen twee 2'en in de staart -> 2 (geen om-en-om),
# en schrijft hoatzin.png. Leest staart12.npy.
import numpy as np; from PIL import Image
from geom import PAL
a = np.load('staart12.npy'); P = np.load('part.npy')
for y in range(44, 64):
    for x in range(36, 63):
        if P[y, x] == 1 and a[y, x] == 3 and a[y, x-1] == 2 and a[y, x+1] == 2: a[y, x] = 2
# losse dambordjes per hand: kuifbases F5/F6 verbinden, F6-top, verre teen aan de voet
a[18, 18] = 6; a[19, 27] = 2; a[56, 23] = 14
a[21, 12] = 15          # glanspixel linksboven in het rode oog
# overige 2x2-dambordjes in staart (2/3) en nek (3/4): één pixel gelijk maken -> trapje i.p.v. dambord
for ronde in range(4):
    for y in range(63):
        for x in range(63):
            p, q, r, t = a[y,x], a[y,x+1], a[y+1,x], a[y+1,x+1]
            if not (p and q and p == t and q == r and p != q): continue
            s_ = {int(p), int(q)}
            if s_ == {2, 3}:
                if p == 3: a[y, x] = 2
                else: a[y, x+1] = 2
            elif s_ == {3, 4}:
                if p == 4: a[y, x] = 3
                else: a[y, x+1] = 3
np.save('r12.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('hoatzin.png', transparency=0)
