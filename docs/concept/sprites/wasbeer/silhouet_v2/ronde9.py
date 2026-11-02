"""Silhouet ronde 9: Jordi's schets over de Sneasel-klauw (rode boog linksboven = stuk weg = binnenkant van de haak;
"vergroot de klauwen") + "twee klauwen die even lang zijn met daartussen een kleine inkeping zoals een koevoet".
Basis = ronde 7 (Sneasel-klauw 1:1 met het stuk binnen de boog weg); alleen de onderste klauw vervangen door
2 klauwen van 2 px tegen elkaar, even lang, inkeping 1x1 in de punt. Diff 0 buiten zone 1 t.o.v. ronde2.txt."""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
lees = lambda p: np.array([[c == '#' for c in r.rstrip('\n')] for r in open(os.path.join(HERE, p)) if r.strip()])
r2, a = lees('ronde2.txt'), lees('ronde7.txt')
a[39:43, 4:14] = False
for y, xs in {39: range(8, 14), 40: range(7, 13), 41: range(6, 11), 42: (6, 7, 9, 10)}.items():   # (8,42) leeg = inkeping
    for x in xs:
        a[y, x] = True
d = a != r2; ys, xs = np.nonzero(d)
print('t.o.v. ronde2', d.sum(), 'buiten zone', sum(1 for x, y in zip(xs, ys) if not (4 <= x <= 13 and 33 <= y <= 42)), 'totaal', a.sum())
open(os.path.join(HERE, 'ronde9.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in a) + '\n')
Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(HERE, 'ronde9_1x.png'))
K = 16
sn = np.array(Image.open(os.path.join(HERE, '../../../../../graphics/pokemon/sneasel/anim_front.png')))[:64, :64]
snm = sn != 0
def kader(m, rood=()):
    im = Image.new('RGB', (12 * K, 12 * K), 'white'); px = im.load()
    for y in range(32, 44):
        for x in range(3, 15):
            c = (220, 40, 40) if (x, y) in rood else ((40, 34, 34) if m[y, x] else (255, 255, 255))
            for dy in range(K):
                for dx in range(K):
                    px[(x - 3) * K + dx, (y - 32) * K + dy] = c if (dx and dy) else (205, 205, 215)
    return im
vel = Image.new('RGB', (24 * K + 40 + 64 + 140, 12 * K), 'white')
vel.paste(kader(snm, [(7, 37), (8, 37), (9, 37), (7, 38), (8, 38), (9, 38)]), (0, 0)); vel.paste(kader(a), (12 * K + 20, 0))
one = Image.fromarray(np.where(a, 40, 255).astype(np.uint8)).convert('RGB')
vel.paste(one, (24 * K + 40, 0)); vel.paste(one.resize((128, 128), Image.NEAREST), (24 * K + 40 + 70, 0))
vel.save(os.path.join(HERE, 'vel_ronde9_klauw.png'))
