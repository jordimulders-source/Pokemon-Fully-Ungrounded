"""Coathief silhouet ronde 3 (Jordi, 25 okt: "hij heeft nu 1 poot met klauwen en 1 zonder"): op ronde 2 alleen
zone x 18-25, y 58-62: 2 kleine klauwen voor de voet van de staande verre voorpoot, op de grond, naar linksvoor."""
import numpy as np
rows = [l.rstrip('\n') for l in open('ronde2.txt')]
g = [list(r) for r in rows]
add = {59: [(23, 25)], 60: [(21, 24)], 61: [(19, 20)], 62: [(21, 24)]}  # voorstel maker r5: lucht tussen de klauwen
for y, sp in add.items():
    for a, b in sp:
        for x in range(a, b + 1): g[y][x] = '#'
open('ronde3.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')
A = np.array([[c == '#' for c in r] for r in rows]); B = np.array([[c == '#' for c in ''.join(r)] for r in g])
d = np.argwhere(A != B)
print('px', A.sum(), '->', B.sum(), '| gewijzigd', len(d), '| buiten zone', sum(not (18 <= x <= 25 and 58 <= y <= 62) for y, x in d))
