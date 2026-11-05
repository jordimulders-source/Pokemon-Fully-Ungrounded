"""Tweede pas (met de hand gekozen zones, alleen tintwissels, geen nieuwe vormen): leest raster.txt, schrijft raster.txt terug.
1) b->l op de lichtkant: hals links, flank boven, achterwerk boven, gezicht, borst, wolmouw/-broek (wol als hoofdtint licht).
2) verre poten: binnen-d (niet de linkerrand) -> s.
3) omlijning rechtsboven (oren, achterhoofd, nek, achterwerk boven, staart) k -> d: overgang zwart -> omlijningsbasis langs de omtrek (SPRITING par. 8)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SIL = [l.rstrip('\n') for l in open(os.path.join(HERE, '../../../silhouet/ronde2.txt'))]
lines = open(os.path.join(HERE, 'raster.txt')).read().split('\n')
segs = []
for l in lines:
    p = l.split()
    segs.append([int(p[0]), int(p[1]), list(p[2])] if len(p) == 3 and p[0].isdigit() else l)
def get(x, y):
    for s in segs:
        if isinstance(s, list) and s[0] == y and s[1] <= x < s[1] + len(s[2]): return s, x - s[1]
    return None, None
def swap(x, y, a, b):
    s, i = get(x, y)
    if s and s[2][i] == a: s[2][i] = b; return 1
    return 0
n = {'b->l': 0, 'd->s': 0, 'k->d': 0}
B2L = [(17, 22, 19, 23), (24, 29, 18, 22), (30, 31, 29, 31), (33, 34, 28, 46), (26, 31, 47, 50), (10, 19, 13, 16), (33, 35, 21, 26),
       (41, 44, 22, 24), (45, 49, 48, 49), (42, 44, 45, 48)]
for y0, y1, x0, x1 in B2L:
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): n['b->l'] += swap(x, y, 'b', 'l')
def runs(y):
    out, st = [], None
    for x in range(65):
        v = x < 64 and SIL[y][x] == '#'
        if v and st is None: st = x
        if not v and st is not None: out.append((st, x - 1)); st = None
    return out
for y in range(43, 58):
    for a, b in runs(y):
        if (29 <= a <= 32) or (39 <= a <= 42):
            for x in range(a + 1, b + 1): n['d->s'] += swap(x, y, 'd', 's')
for y in list(range(2, 9)) + list(range(9, 22)) + [24] + list(range(25, 30)) + list(range(19, 23)):
    rr = runs(y)
    for a, b in rr:
        if y <= 8 or (y <= 21 and b <= 28) or (y == 24 and b == 30) or (y >= 25 and b >= 50) or (19 <= y <= 22 and a >= 50):
            n['k->d'] += swap(b, y, 'k', 'd')
n['k->d'] += swap(20, 49, 'k', 'd')
out = [s if isinstance(s, str) else f'{s[0]} {s[1]} {"".join(s[2])}' for s in segs]
open(os.path.join(HERE, 'raster.txt'), 'w').write('\n'.join(out))
print(n)
