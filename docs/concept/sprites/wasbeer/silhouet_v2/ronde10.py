"""Silhouet ronde 10 (Jordi: "Pak de klauw van sneasel, trek de twee klauwen los van elkaar" · "en daartussen zet je die koevoet ruimte" · "dan zet je ze weer vast").
Sneasel-klauw 1:1 (frame 1, index 7/11/12/13, x 7-14, y 33-42). Klauw 1 = bovenste (y <= 38), klauw 2 = onderste
(y >= 39, x <= 12); klauw 2 schuift 1 px omlaag, zodat er 1 px lucht tussen de twee klauwen komt; hij blijft
aan de hand vast via (12-13, 39). Diff 0 buiten zone 1 t.o.v. ronde2.txt. Vel ook in Sneasel-kleuren."""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
lees = lambda p: np.array([[c == '#' for c in r.rstrip('\n')] for r in open(os.path.join(HERE, p)) if r.strip()])
r2 = lees('ronde2.txt')
im = Image.open(os.path.join(ROOT, 'graphics/pokemon/sneasel/anim_front.png')); pal = im.getpalette()
sn = np.array(im)[:64, :64]
idx = np.zeros((64, 64), int)                                   # paletindex van de nieuwe klauw (0 = leeg)
for y in range(33, 43):
    for x in range(7, 15):
        if sn[y, x] in (7, 11, 12, 13):
            if y >= 39 and x <= 12:
                idx[y + 1, x] = sn[y, x]                        # klauw 2 een rij omlaag
            else:
                idx[y, x] = sn[y, x]
idx[39, 10] = 12; idx[39, 11] = 12; idx[39, 12] = 13; idx[39, 13] = 13   # weer vast aan de basis: alleen bij de punten een inkeping (x 8-9)
a = r2.copy(); a[33:44, 4:12] = False
a |= idx > 0
d = a != r2; ys, xs = np.nonzero(d)
print('t.o.v. ronde2', d.sum(), 'buiten zone', sum(1 for x, y in zip(xs, ys) if not (4 <= x <= 14 and 33 <= y <= 43)), 'totaal', a.sum())
open(os.path.join(HERE, 'ronde10.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in a) + '\n')
Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(HERE, 'ronde10_1x.png'))
K = 16
P = lambda i: tuple(pal[i * 3:i * 3 + 3])
def kader(f):
    out = Image.new('RGB', (12 * K, 13 * K), 'white'); px = out.load()
    for y in range(32, 45):
        for x in range(3, 15):
            c = f(x, y)
            for dy in range(K):
                for dx in range(K):
                    px[(x - 3) * K + dx, (y - 32) * K + dy] = c if (dx and dy) else (205, 205, 215)
    return out
orig = kader(lambda x, y: P(sn[y, x]) if sn[y, x] in (7, 11, 12, 13) else (255, 255, 255))
nieuw = kader(lambda x, y: P(idx[y, x]) if idx[y, x] else ((90, 84, 80) if a[y, x] else (255, 255, 255)))
sil = kader(lambda x, y: (40, 34, 34) if a[y, x] else (255, 255, 255))
vel = Image.new('RGB', (36 * K + 60 + 64 + 140, 13 * K), 'white')
vel.paste(orig, (0, 0)); vel.paste(nieuw, (12 * K + 20, 0)); vel.paste(sil, (24 * K + 40, 0))
one = Image.fromarray(np.where(a, 40, 255).astype(np.uint8)).convert('RGB')
vel.paste(one, (36 * K + 60, 0)); vel.paste(one.resize((128, 128), Image.NEAREST), (36 * K + 60 + 70, 0))
vel.save(os.path.join(HERE, 'vel_ronde10_klauw.png'))
