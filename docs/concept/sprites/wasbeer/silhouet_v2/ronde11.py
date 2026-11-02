"""Silhouet ronde 11 (Jordi: "het is letterlijk een inkeping tussen 2 klauwen" · "je verandert telkens de hele vorm").
De Sneasel-klauw exact 1:1 (frame 1, index 7/11/12/13, x 7-14, y 33-42), NIETS verschoven; alleen de inkeping tussen
de bovenste en de onderste klauw weg: (8,39) en (9,39). Diff 0 buiten zone 1 t.o.v. ronde2.txt."""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
lees = lambda p: np.array([[c == '#' for c in r.rstrip('\n')] for r in open(os.path.join(HERE, p)) if r.strip()])
r2 = lees('ronde2.txt')
im = Image.open(os.path.join(ROOT, 'graphics/pokemon/sneasel/anim_front.png')); pal = im.getpalette()
sn = np.array(im)[:64, :64]
idx = np.zeros((64, 64), int)
for y in range(33, 43):
    for x in range(7, 15):
        if sn[y, x] in (7, 11, 12, 13):
            idx[y, x] = sn[y, x]
INKEPING = [(8, 39), (9, 39)]
for x, y in INKEPING:
    idx[y, x] = 0
a = r2.copy(); a[33:43, 4:12] = False
a |= idx > 0
d = a != r2; ys, xs = np.nonzero(d)
print('t.o.v. ronde2', d.sum(), 'buiten zone', sum(1 for x, y in zip(xs, ys) if not (4 <= x <= 14 and 33 <= y <= 42)), 'totaal', a.sum())
open(os.path.join(HERE, 'ronde11.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in a) + '\n')
Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(HERE, 'ronde11_1x.png'))
K = 16
P = lambda i: tuple(pal[i * 3:i * 3 + 3])
def kader(f):
    out = Image.new('RGB', (12 * K, 12 * K), 'white'); px = out.load()
    for y in range(32, 44):
        for x in range(3, 15):
            c = f(x, y)
            for dy in range(K):
                for dx in range(K):
                    px[(x - 3) * K + dx, (y - 32) * K + dy] = c if (dx and dy) else (205, 205, 215)
    return out
orig = kader(lambda x, y: (220, 40, 40) if (x, y) in INKEPING else (P(sn[y, x]) if sn[y, x] in (7, 11, 12, 13) else (255, 255, 255)))
nieuw = kader(lambda x, y: P(idx[y, x]) if idx[y, x] else ((90, 84, 80) if a[y, x] else (255, 255, 255)))
sil = kader(lambda x, y: (40, 34, 34) if a[y, x] else (255, 255, 255))
vel = Image.new('RGB', (36 * K + 60 + 64 + 140, 12 * K), 'white')
vel.paste(orig, (0, 0)); vel.paste(nieuw, (12 * K + 20, 0)); vel.paste(sil, (24 * K + 40, 0))
one = Image.fromarray(np.where(a, 40, 255).astype(np.uint8)).convert('RGB')
vel.paste(one, (36 * K + 60, 0)); vel.paste(one.resize((128, 128), Image.NEAREST), (36 * K + 60 + 70, 0))
vel.save(os.path.join(HERE, 'vel_ronde11_klauw.png'))
