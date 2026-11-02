"""Coathief silhouet ronde 1: direct verkleinde render (direct.txt) + handreparaties in benoemde zones.
Zone 1 voorpoten (x 15-33, y 50-63): opgetilde nabije poot met 2 hangende klauwen los van de staande verre poot.
Zone 2 nabije achtervoet (x 44-55, y 60-61): platte voet, los pixel weg."""
import numpy as np
rows = [l.rstrip('\n') for l in open('direct.txt')]
g = [list(r) for r in rows]
Z1 = {50: [(22, 31)], 51: [(21, 31)], 52: [(20, 31)], 53: [(19, 24), (27, 31)], 54: [(18, 24), (27, 31)],
      55: [(18, 24), (27, 31)], 56: [(17, 23), (27, 31)], 57: [(16, 18), (20, 22), (27, 31)],
      58: [(16, 17), (19, 21), (27, 31)], 59: [(16, 17), (20, 21), (27, 31)], 60: [(17, 17), (21, 21), (26, 31)],
      61: [(23, 31)], 62: [(21, 22), (24, 25)], 63: []}
for y, sp in Z1.items():
    for x in range(15, 34): g[y][x] = '.'
    for a, b in sp:
        for x in range(a, b + 1): g[y][x] = '#'
for y in (60, 61):
    for x in range(44, 56): g[y][x] = '.'
for x in range(46, 52): g[60][x] = '#'
open('ronde1.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')
A = np.array([[c == '#' for c in r] for r in rows]); B = np.array([[c == '#' for c in ''.join(r)] for r in g])
d = np.argwhere(A != B)
out = [p for p in d if not ((15 <= p[1] <= 33 and 50 <= p[0] <= 63) or (44 <= p[1] <= 55 and 60 <= p[0] <= 61))]
print('px', A.sum(), '->', B.sum(), '| gewijzigd', len(d), '| buiten de zones', len(out))
