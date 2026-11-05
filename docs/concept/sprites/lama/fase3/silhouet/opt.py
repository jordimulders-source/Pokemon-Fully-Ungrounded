"""Haalt korrels weg uit het model op de 50%-grens: probeert rond elke korrel alle 1- en 2-px-flips van pixels die direct naast
de 50%-grens liggen (dus max. 1 px afwijking), kiest op minste korrels (korrel.py) en daarna kleinste som |dekking - 0,5|.
Draaien: python3 opt.py uit.txt  (leest alpha.npy uit deze map). Het resultaat wordt daarna met de hand nagekeken."""
import os, sys, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
uit = sys.argv[1] if len(sys.argv) > 1 else 'ronde_auto.txt'
src = open(os.path.join(HERE, 'korrel.py')).read().split('for p in sys.argv')[0]
exec(src)  # definieert korrels()
a = np.load(os.path.join(HERE, 'alpha.npy')); k = a.shape[0] // 64; c = a.reshape(64, k, 64, k).mean((1, 3)); M = c >= .5
def dil(m):
    P = np.pad(m, 1); o = np.zeros_like(m)
    for dy in range(3):
        for dx in range(3): o |= P[dy:dy+64, dx:dx+64]
    return o
ok = (~M & dil(M)) | (M & dil(~M))  # flips die max. 1 px van de grens liggen
def score(S):
    u, i, t = korrels(S); return int(u.sum()) + int(i.sum()) + len(t)
def cost(S): d = S != M; return float(abs(c[d] - .5).sum())
S = M.copy()
while True:
    k0 = score(S)
    if k0 == 0: break
    u, i, t = korrels(S)
    pts = set(zip(*np.nonzero(u | i))) | set((y, x) for x, y, _ in t)
    cand = sorted({(y + dy, x + dx) for y, x in pts for dy in range(-2, 3) for dx in range(-2, 3)
                   if 0 <= y + dy < 64 and 0 <= x + dx < 64 and ok[y + dy, x + dx]})
    opts = [(p,) for p in cand] + [p for p in itertools.combinations(cand, 2)
                                   if abs(p[0][0] - p[1][0]) <= 2 and abs(p[0][1] - p[1][1]) <= 2]
    best = None
    for fl in opts:
        T = S.copy()
        for p in fl: T[p] = ~T[p]
        sc = (score(T), cost(T))
        if best is None or sc < best[0]: best = (sc, fl)
    if best[0][0] >= k0: print('vast op', k0, 'korrels'); break
    for p in best[1]: S[p] = ~S[p]
    print('flip', [f'{"+" if S[y, x] else "-"}x{x} y{y} ({c[y, x]:.2f})' for y, x in best[1]], '-> korrels', best[0][0])
open(os.path.join(HERE, uit), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in S) + '\n')
print(f'{uit}: {int(S.sum())} px, {int((S != M).sum())} afwijkingen van het model')
