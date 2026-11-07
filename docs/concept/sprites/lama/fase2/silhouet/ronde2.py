"""Silhouet ronde 2: bouwt ronde2.txt/_1x.png uit de handgetypte runs (ronde2_runs.txt), diff per onderdeel t.o.v. ronde 1b,
controles (1-px-spleten, uitsteeksels, rechte randruns >= 4 in de poten). Draaien vanuit de repo-root:
python3 docs/concept/sprites/lama/fase2/silhouet/ronde2.py"""
import os, itertools
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
g = np.zeros((64, 64), bool)
for line in open(os.path.join(HERE, 'ronde2_runs.txt')):
    if line.startswith('#') or not line.strip(): continue
    y, runs = line.split(':'); y = int(y)
    for r in runs.split():
        a, b = map(int, r.split('-')); g[y, a:b + 1] = True
open(os.path.join(HERE, 'ronde2.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in row) for row in g) + '\n')
im = Image.fromarray(g.astype(np.uint8), 'P'); im.putpalette([255, 255, 255, 40, 32, 48] + [0] * 762)
im.save(os.path.join(HERE, 'ronde2_1x.png'), transparency=0)
old = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, 'ronde1b.txt')) if l.strip()])
ys, xs = np.nonzero(g)
print(f'ronde2: px {g.sum()} (ronde1b {old.sum()}), box {xs.max()-xs.min()+1}x{ys.max()-ys.min()+1}, y {ys.min()}-{ys.max()}')
# kop = oortop t/m kin (r23)
print(f'kop: r{ys.min()}-23 = {(23-ys.min()+1)/(ys.max()-ys.min()+1)*100:.0f}% van de hoogte')
Z = [('oren', 0, 7, 0, 30), ('kop (kruin, snuit)', 8, 23, 0, 16), ('hals (wol)', 8, 34, 16, 33), ('staart', 18, 24, 46, 63),
     ('lijf/borst', 24, 40, 0, 63), ('opgetilde voorpoot', 41, 63, 0, 28), ('verre voorpoot', 41, 63, 29, 37), ('achterpoten', 41, 63, 38, 63)]
seen = np.zeros_like(g)
for n, y0, y1, x0, x1 in Z:
    m = np.zeros_like(g); m[y0:y1 + 1, x0:x1 + 1] = True; m &= ~seen; seen |= m
    print(f'  {n:20s} +{(g & ~old & m).sum():3d} / -{(old & ~g & m).sum():3d}')
print('  rest', ((g != old) & ~seen).sum())
for y in range(64):
    for x in range(1, 63):
        if not g[y, x] and g[y, x - 1] and g[y, x + 1]: print('1px-spleet', x, y)
for y in range(1, 63):
    for x in range(1, 63):
        if g[y, x] and g[y-1:y+2, x-1:x+2].sum() - 1 <= 1: print('uitsteeksel', x, y)
        if g[y, x] and g[y+1, x+1] and not g[y, x+1] and not g[y+1, x]: print('diagonaal', x, y)
        if g[y, x] and g[y+1, x-1] and not g[y, x-1] and not g[y+1, x]: print('diagonaal', x, y)
# rechte verticale randruns >= 4 in de poten (r43-56), per run
def runs_in_row(y):
    out, s = [], None
    for x in range(65):
        v = x < 64 and g[y, x]
        if v and s is None: s = x
        if not v and s is not None: out.append((s, x - 1)); s = None
    return out
# per poot: de run in die rij die de referentiekolom bevat (handschoen-rijen r50-56 van de opgetilde poot = kleding, bevroren)
for y0, y1, xc, n in [(43, 49, 23, 'opgetild (tot pols)'), (43, 56, 33, 'verre voor'), (45, 58, 42, 'verre achter'), (45, 61, 49, 'nabije achter')]:
    for side in ('L', 'R'):
        e = []
        for y in range(y0, y1 + 1):
            r = [rr for rr in runs_in_row(y) if rr[0] - 3 <= xc <= rr[1] + 3]
            if r: rr = min(r, key=lambda t: abs((t[0] + t[1]) / 2 - xc)); e.append(rr[0] if side == 'L' else rr[1])
        runs = [len(list(v)) for k, v in itertools.groupby(e)]
        print(f'  randruns {n} {side}: {runs} (max {max(runs)})')
