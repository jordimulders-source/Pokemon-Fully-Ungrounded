"""Silhouet ronde 7: verre klauw = de Sneasel-klauw letterlijk (frame 1, paletindex 7/11/12/13 = klauw, x 7-13, y 33-42,
1:1 op dezelfde plek aan onze pols), min het stuk binnen Jordi's rode boog (de bovenste korte klauw linksboven,
x 7-9, y 37-38). Alles buiten zone 1 = ronde2.txt (diff 0).
Draaien: python3 docs/concept/sprites/wasbeer/silhouet_v2/ronde7.py"""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../..')
r2 = np.array([[c == '#' for c in r.rstrip('\n')] for r in open(os.path.join(HERE, 'ronde2.txt')) if r.strip()])
a = r2.copy()
zone = np.zeros_like(a); zone[33:43, 4:12] = True          # zone 1: oude klauw eruit (pols/steel x >= 12 blijven)
a[zone] = False
sn = np.array(Image.open(os.path.join(ROOT, 'graphics/pokemon/sneasel/anim_front.png')))[:64, :64]
klauw = np.isin(sn, (7, 11, 12, 13)); klauw[:, 14:] = False; klauw[:33] = False
a |= klauw
WEG = [(7, 37), (8, 37), (9, 37), (7, 38), (8, 38), (9, 38)]   # Jordi's boog: stuk weg -> haakopening
for x, y in WEG:
    a[y, x] = False
d = a != r2
ys, xs = np.nonzero(d)
buiten = [(x, y) for x, y in zip(xs, ys) if not (4 <= x <= 13 and 33 <= y <= 42)]
print('gewijzigd', d.sum(), 'buiten zone', len(buiten), 'totaal', a.sum())
open(os.path.join(HERE, 'ronde7.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in a) + '\n')
Image.fromarray((a * 255).astype(np.uint8)).save(os.path.join(HERE, 'ronde7_1x.png'))
# vel: Sneasel-klauw 8x (rood = weg) | onze klauw 8x | sprite 1x, 2x
K = 16
def kader(m, rood=()):
    im = Image.new('RGB', (12 * K, 12 * K), 'white'); px = im.load()
    for y in range(32, 44):
        for x in range(3, 15):
            c = (40, 34, 34) if m[y, x] else (255, 255, 255)
            if (x, y) in rood:
                c = (220, 40, 40)
            for dy in range(K):
                for dx in range(K):
                    px[(x - 3) * K + dx, (y - 32) * K + dy] = c if (dx and dy) else (205, 205, 215)
    return im
snm = np.isin(sn, (7, 11, 12, 13)) | np.isin(sn, (3, 5, 6, 8))
vel = Image.new('RGB', (12 * K * 2 + 40 + 64 + 128 + 40, 12 * K), 'white')
vel.paste(kader(snm, WEG), (0, 0)); vel.paste(kader(a), (12 * K + 20, 0))
one = Image.fromarray(np.where(a, 40, 255).astype(np.uint8)).convert('RGB')
vel.paste(one, (24 * K + 40, 0)); vel.paste(one.resize((128, 128), Image.NEAREST), (24 * K + 40 + 70, 0))
vel.save(os.path.join(HERE, 'vel_ronde7_klauw.png'))
