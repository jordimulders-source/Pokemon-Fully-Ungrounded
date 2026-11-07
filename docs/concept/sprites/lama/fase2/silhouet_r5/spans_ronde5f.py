"""Lama fase 2, silhouet ronde 5f: ronde5e.txt met alleen de kopzone (y0-21) OVERGETROKKEN van het goedgekeurde poppetje
(dekkingskaart uit kop_dekking.py, drempel ~0,5 per 64-pixel). Elke rij met de hand gezet; afwijkingen staan erbij.
Draaien: python3 spans_ronde5f.py -> ronde5f.txt + ronde5f_1x.png"""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
def load(p): return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, p)) if l.strip()])
E = load('ronde5e.txt'); S = E.copy(); S[:22] = False
NABIJ_OOR = {2: (17, 18),                      # top: y1 x18 (0,8) weg -> anders 1-px uitsteeksel (afwijking 1)
             3: (17, 18), 4: (16, 18), 5: (16, 18), 6: (16, 18), 7: (17, 18), 8: (17, 18), 9: (17, 19)}
VER_OOR = {1: (21, 22), 2: (21, 23),            # y2 x21 (0,1) erbij -> anders is de top een uitsteeksel (afwijking 1)
           3: (22, 23), 4: (22, 24), 5: (22, 24),
           6: (22, 24),                         # x22 (0,4) erbij -> anders een tand in de binnenrand (afwijking <1)
           7: (22, 24), 8: (22, 24),
           9: (22, 23)}                         # x21 (0,5) weg -> 2 kolommen lucht tussen de oorvoeten (afwijking 1)
KRUIN = {10: (17, 23), 11: (16, 23), 12: (15, 24), 13: (14, 25)}
SNUIT = {14: (13, 25), 15: (12, 25), 16: (12, 24), 17: (13, 24), 18: (13, 24)}
KAAK = {19: (14, 24), 20: (16, 24),
        21: (16, 25)}                           # achterrand x25 = poppetje (hals-achterrand vrijgegeven, zie HALS)
ZONES = {'oor nabij': NABIJ_OOR, 'oor ver': VER_OOR, 'kruin': KRUIN, 'snuit': SNUIT, 'kaak + aansluiting hals': KAAK}
for Z in ZONES.values():
    for y, (a, b) in Z.items(): S[y, a:b + 1] = True
# HALS-ACHTERRAND (vrijgegeven door Claude: y20-30, alleen x>23): volgt het poppetje op de 0,5-grens, kaarsrecht op x25 (y21-25);
# y26-30 blijven vol (rug/schoft; poppetje y26 x26-27 = 0,1/0,0 maar op <= 1 px van de omtrek en zonder dip, R1)
HALS = {22: 25, 23: 25, 24: 25, 25: 25}
for y, xr in HALS.items(): S[y, xr + 1:28] = False
if __name__ == '__main__':
    open(os.path.join(HERE, 'ronde5f.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in S) + '\n')
    im = np.zeros((64, 64, 4), np.uint8); im[S] = (0, 0, 0, 255)
    Image.fromarray(im, 'RGBA').save(os.path.join(HERE, 'ronde5f_1x.png'))
    ys, xs = np.nonzero(S)
    print('px', S.sum(), '(5e', E.sum(), ') box', xs.max() - xs.min() + 1, 'x', ys.max() - ys.min() + 1)
    print('kopzone y0-21: +%d / -%d t.o.v. 5e' % ((S[:22] & ~E[:22]).sum(), (E[:22] & ~S[:22]).sum()), '| diff vanaf y22:', int((S[22:] ^ E[22:]).sum()), 'px')
    # afstand tot de omtrek van het poppetje: per pixel dat afwijkt van de 0,5-drempel van de dekking
    a = np.load(os.path.join(HERE, 'kop_alpha.npy')); k = a.shape[0] // 64; cov = a.reshape(64, k, 64, k).mean((1, 3))
    T = cov >= 0.5
    def dist(p, M):
        z = np.argwhere(M); return np.sqrt(((z - p) ** 2).sum(1)).min() if len(z) else 99
    for n, Z in ZONES.items():
        rows = list(Z); m = np.zeros_like(S); m[rows] = True
        extra = [(y, x) for y, x in np.argwhere(S & ~T & m)]; mis = [(y, x) for y, x in np.argwhere(T & ~S & m)]
        de = max([dist(np.array(p), T) for p in extra], default=0); dm = max([dist(np.array(p), S) for p in mis], default=0)
        print(f'  {n:24s} rijen y{min(rows)}-{max(rows)}: {len(extra)} px erbij (max {de:.1f}), {len(mis)} px weg (max {dm:.1f}) t.o.v. het poppetje')
