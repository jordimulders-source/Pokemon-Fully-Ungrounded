"""Controle ronde 3: korrels buiten de oren, afwijking van de poppetjemassa (alleen waar geen handvorm staat), losse delen.
Draaien: python3 controle.py  (na silhouet.py)"""
import os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
import silhouet as SI
_k = open(os.path.join(HERE, 'korrel.py')).read(); exec(_k[_k.index('def sq'):_k.index('for p in sys.argv')])
S = np.array([[c == '#' for c in l.strip()] for l in open(os.path.join(HERE, 'ronde3.txt'))])
D = np.array([list(l.strip()) for l in open(os.path.join(HERE, 'delen.txt'))])
ys = np.nonzero(S)[0]; dy = 4
vrij = SI.oorzone(dy)
u, i, t = korrels(S)
buiten = int((u & ~vrij).sum() + (i & ~vrij).sum()) + sum(1 for x, y, _ in t if not vrij[y, x])
print(f'px {int(S.sum())}; korrels buiten de oorpunten: {buiten}; in de oorpunten: {int((u & vrij).sum())} uit, {int((i & vrij).sum())} in, {sum(1 for x, y, _ in t if vrij[y, x])} tanden')
cov = np.roll(np.load(os.path.join(HERE, 'dekking_kaal.npy')), dy, 0); M = cov >= 0.5
kop = np.roll(SI.naar1x(SI.bol(*SI.KOP)), dy, 0)
poot = np.isin(D, ['P', 'p'])
hand = vrij | kop | poot | (D == 'S') | SI.reparatie(dy)   # handvormen en ronde-3-reparaties tellen niet als afwijking
d = (S != M) & ~hand
def dil(m):
    P = np.pad(m, 1); o = np.zeros_like(m)
    for a in range(3):
        for b in range(3): o |= P[a:a+64, b:b+64]
    return o
ver = d & ~((S & dil(M)) | (~S & dil(~M)))
print(f'massa poppetje (buiten kop, oren, poten, reparatiezones): {int(d.sum())} afwijkingen, waarvan > 1 px van de 50%-grens: {int(ver.sum())}')
for y, x in zip(*np.nonzero(d)): print(f'   {"+" if S[y, x] else "-"}x{x} y{y} (dekking {cov[y, x]:.2f})')
from collections import deque
seen = np.zeros_like(S); comp = 0
for y0, x0 in zip(*np.nonzero(S)):
    if seen[y0, x0]: continue
    comp += 1; q = deque([(y0, x0)]); seen[y0, x0] = 1
    while q:
        y, x = q.popleft()
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                yy, xx = y + a, x + b
                if 0 <= yy < 64 and 0 <= xx < 64 and S[yy, xx] and not seen[yy, xx]: seen[yy, xx] = 1; q.append((yy, xx))
print('componenten (8-buren):', comp)
