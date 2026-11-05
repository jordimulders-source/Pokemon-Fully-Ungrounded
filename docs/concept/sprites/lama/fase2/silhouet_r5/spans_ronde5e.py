"""Lama fase 2, silhouet ronde 5e: ronde5d.txt met alleen de kopzone (y0-21) opnieuw met de hand gezet:
kop driekwart zoals het poppetje (oren achter op de schedel, naar achteren/rechts in een V, ver oor schuiner en lager;
schedel langer naar achteren tot in de hals; snuit stomp naar links-voor zoals in 5d).
Draaien: python3 spans_ronde5e.py -> ronde5e.txt + ronde5e_1x.png"""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
def load(p): return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, p)) if l.strip()])
D5 = load('ronde5d.txt'); S = D5.copy(); S[:22] = False
NABIJ_OOR = {1: (20, 21), 2: (19, 21), 3: (18, 21), 4: (18, 21), 5: (18, 21), 6: (17, 20), 7: (17, 20), 8: (17, 19), 9: (17, 19)}
VER_OOR = {2: (26, 27), 3: (25, 27), 4: (24, 27), 5: (24, 27), 6: (23, 26), 7: (23, 26), 8: (22, 25), 9: (22, 25)}
SCHEDEL = {10: (16, 25), 11: (15, 26), 12: (14, 27), 13: (13, 28), 14: (12, 28), 15: (11, 28), 16: (11, 28),
           17: (11, 27), 18: (12, 26), 19: (13, 26), 20: (15, 26), 21: (16, 27)}
ZONES = {'nabij oor': NABIJ_OOR, 'ver oor': VER_OOR, 'schedel+snuit': SCHEDEL}
for Z in ZONES.values():
    for y, (a, b) in Z.items(): S[y, a:b + 1] = True
if __name__ == '__main__':
    open(os.path.join(HERE, 'ronde5e.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in S) + '\n')
    im = np.zeros((64, 64, 4), np.uint8); im[S] = (0, 0, 0, 255)
    Image.fromarray(im, 'RGBA').save(os.path.join(HERE, 'ronde5e_1x.png'))
    ys, xs = np.nonzero(S)
    print('px', S.sum(), '(5d', D5.sum(), ') box', xs.max() - xs.min() + 1, 'x', ys.max() - ys.min() + 1)
    k = S[:22] ^ D5[:22]
    print('kopzone y0-21: +%d / -%d' % ((S[:22] & ~D5[:22]).sum(), (D5[:22] & ~S[:22]).sum()), '| diff vanaf y22:', int((S[22:] ^ D5[22:]).sum()), 'px')
    B = load('direct.txt'); bz = np.argwhere(B)
    for n, Z in ZONES.items():
        pts = [(y, x) for y, (a, b) in Z.items() for x in range(a, b + 1)]
        d = max(np.sqrt(((bz - p) ** 2).sum(1)).min() for p in pts)
        print(f'  {n}: max afstand tot de bron (direct.txt) {d:.1f} px')
