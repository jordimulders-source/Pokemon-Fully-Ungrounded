"""Telt 'korrels' in een silhouet: 1-px uitstulpingen (pixels die geen 2x2-blok raken, opening) en 1-px inkepingen
(lege pixels die een 2x2-closing vult), plus enkelrijs-tanden (rand die 1 rij uitsteekt of inspringt t.o.v. beide buren).
Draaien: python3 korrel.py ronde3.txt [ronde3b.txt ...]"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
def load(p): return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, p)) if l.strip()])
def sq(m, rand=False):  # pixels gedekt door een volledig 2x2-blok
    P = np.pad(m, 1, constant_values=rand); out = np.zeros_like(m)
    for dy in (0, 1):
        for dx in (0, 1):
            blk = P[dy:dy+64, dx:dx+64] & P[dy+1:dy+65, dx:dx+64] & P[dy:dy+64, dx+1:dx+65] & P[dy+1:dy+65, dx+1:dx+65]
            out |= blk  # blok met linksboven op (y-1+dy, x-1+dx) bevat (y,x)
    return out
def korrels(S):
    uit = S & ~sq(S)            # 1-px uitsteeksels
    inn = ~S & ~sq(~S, True)          # 1-px inkepingen (lege pixels zonder 2x2 leeg blok)
    # enkelrijs-tanden langs verticale randen: per rij de x van elke segmentgrens, vergelijk met rij erboven/eronder
    tand = []
    for y in range(1, 63):
        for x in range(1, 63):
            for side in (-1, 1):  # -1: linkerrand (S[x] gevuld, S[x-1] leeg)
                if S[y, x] and not S[y, x + side]:
                    # uitstulping van 1 rij: boven en onder op deze x leeg aan dezelfde kant
                    if not S[y-1, x] and not S[y+1, x] and S[y, x - side]: tand.append((x, y, 'uit'))
                if not S[y, x] and S[y, x - side] and S[y-1, x] and S[y+1, x] and not S[y, x + side] if 0 < x + side < 64 else False:
                    tand.append((x, y, 'in'))
    for x in range(1, 63):
        for y in range(1, 63):
            for side in (-1, 1):  # horizontale randen
                if S[y, x] and not S[y + side, x] and not S[y, x-1] and not S[y, x+1] and S[y - side, x]: tand.append((x, y, 'uit'))
                if not S[y, x] and S[y - side, x] and S[y, x-1] and S[y, x+1] and not S[y + side, x]: tand.append((x, y, 'in'))
    return uit, inn, sorted(set(tand))
for p in sys.argv[1:] or ['ronde3.txt']:
    S = load(p); u, i, t = korrels(S)
    print(f'{p}: {int(S.sum())} px | korrels: {int(u.sum())} uitsteeksel-px, {int(i.sum())} inkeping-px, {len(t)} tanden van 1 rij/kolom')
    for x, y, k in t: print(f'   {k} x{x} y{y}')
    for y, x in zip(*np.nonzero(u)): print(f'   uitsteeksel-px x{x} y{y}')
    for y, x in zip(*np.nonzero(i)): print(f'   inkeping-px x{x} y{y}')
