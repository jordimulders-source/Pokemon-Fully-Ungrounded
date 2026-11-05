"""Coathief silhouet ronde 2 (Jordi, 25 okt): kleine reparaties op het bevroren ronde 1, alleen in benoemde zones.
Z1 oren (x 14-26, y 30-33): ronde toppen i.p.v. afgeknipt. Z2 klauwen opgetilde poot (x 10-23, y 56-62): langere haken naar
linksvoor. Z3 staande verre voorpoot (x 20-33, y 50-62): bovenarm breder, knik bij de pols, platte voet; losse teentjes weg."""
import numpy as np
rows = [l.rstrip('\n') for l in open('ronde1.txt')]
g = [list(r) for r in rows]
def zone(x0, x1, spans):
    for y, sp in spans.items():
        for x in range(x0, x1 + 1): g[y][x] = '.'
        for a, b in sp:
            for x in range(a, b + 1): g[y][x] = '#'
zone(14, 26, {30: [], 31: [(21, 23)], 32: [(16, 17), (20, 24)], 33: [(15, 18), (20, 25)]})
zone(10, 23, {56: [(17, 23)], 57: [(15, 18), (19, 22)], 58: [(13, 16), (18, 20)], 59: [(12, 14), (16, 18)],
              60: [(12, 13), (16, 17)], 61: [(12, 12), (16, 16)], 62: []})
zone(26, 33, {50: [(26, 32)], 51: [(26, 32)], 52: [(26, 32)], 53: [(27, 32)], 54: [(27, 31)], 55: [(27, 31)],
              56: [(27, 31)], 57: [(27, 31)], 58: [(27, 30)], 59: [(26, 30)]})
zone(24, 33, {60: [(25, 31)], 61: [(24, 31)], 62: []})
for x in range(19, 24): g[62][x] = '.'
open('ronde2.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')
A = np.array([[c == '#' for c in r] for r in rows]); B = np.array([[c == '#' for c in ''.join(r)] for r in g])
d = np.argwhere(A != B)
inz = lambda y, x: (14 <= x <= 26 and 30 <= y <= 33) or (10 <= x <= 23 and 56 <= y <= 62) or (26 <= x <= 33 and 50 <= y <= 59) or (24 <= x <= 33 and 60 <= y <= 62) or (y == 62 and 19 <= x <= 23)
print('px', A.sum(), '->', B.sum(), '| gewijzigd', len(d), '| buiten zones', sum(not inz(*p) for p in d))
