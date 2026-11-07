"""Korrels weg uit model50.txt: herhaald de flip (1 px, alleen pixels met dekking 0,2-0,8 = naast de 50%-grens) die het
aantal korrels het meest verlaagt; bij gelijkspel de flip met dekking het dichtst bij 0,5. Schrijft ronde1.txt."""
import os, sys, io, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ['korrel.py']
src = open(os.path.join(HERE, 'korrel.py')).read().split('for p in sys.argv')[0]
ns = {'__file__': os.path.join(HERE, 'korrel.py')}; exec(src, ns)
korrels = ns['korrels']
cov = np.load(os.path.join(HERE, 'dekking.npy'))
S = cov >= 0.5
STAART = np.zeros((64, 64), bool); STAART[20:42, 44:64] = True
# spiraal: spleten tussen de windingen (< 1 px, dekking 0,2-0,45) dicht; de windingen komen als lijnen in de kleur
# (zoals de spiraal van fase 2); alleen het echte gat in het midden blijft open
from scipy import ndimage as nd
leeg = cov < 0.2; lab, _ = nd.label(np.pad(leeg, 1, constant_values=True)); buiten = (lab == lab[0, 0])[1:-1, 1:-1]
grens_buiten = nd.binary_dilation(buiten) & ~buiten  # niet de buitenrand dikker maken (keurder ronde 1)
S[STAART & (cov >= 0.2) & ~grens_buiten] = True
def score(S):
    u, i, t = korrels(S); return int((u & ~STAART).sum()) + int((i & ~STAART).sum()) + len([1 for x, y, _ in t if not STAART[y, x]])
s = score(S); flips = []
while s > 0:
    u, i, t = korrels(S)
    kand = set(zip(*np.nonzero(u))) | set(zip(*np.nonzero(i))) | {(y, x) for x, y, _ in t}
    buren = set()
    for y, x in kand:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                yy, xx = y + dy, x + dx
                if 0 <= yy < 64 and 0 <= xx < 64 and 0.2 <= cov[yy, xx] <= 0.8 and not STAART[yy, xx]: buren.add((yy, xx))
    best = None
    for y, x in buren:
        S[y, x] = ~S[y, x]; sc = score(S); S[y, x] = ~S[y, x]
        key = (sc, abs(cov[y, x] - 0.5))
        if best is None or key < best[0]: best = (key, (y, x))
    if best is None or best[0][0] >= s: break
    y, x = best[1]; S[y, x] = ~S[y, x]; flips.append((x, y, round(float(cov[y, x]), 2), '+' if S[y, x] else '-')); s = best[0][0]
# spiraalmidden als rond gat (2-3 px) en de 1-px-spleet tussen staartwortel en buitenste winding dicht (met de hand)
for x in (53, 54, 55):
    for y in (31, 32, 33, 34): S[y, x] = False  # spiraalgat 3x4, zo groot als het gat in het model (keurder: 'echte gat')
for x, y in ((50, 36), (50, 37), (51, 37), (53, 30), (52, 32), (54, 35)): S[y, x] = True; flips.append((x, y, round(float(cov[y, x]), 2), '+ hand'))
for x, y in ((55, 32),): pass
open(os.path.join(HERE, 'ronde1.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in S) + '\n')
print('korrels over:', s, '| flips:', len(flips)); [print('  ', f) for f in flips]
