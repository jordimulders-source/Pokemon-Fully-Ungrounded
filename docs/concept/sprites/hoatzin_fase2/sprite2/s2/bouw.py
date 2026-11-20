# bouw.py: van onderlaag (kale reductie) naar sprite.
# 1 masker (alpha >= .45; dunne delen kuif/grijs/creme-staartpunt al vanaf .28)
# 2 tinten uit het model -> palet (helderheid uit elkaar), kleine tintvlekjes weg (modus binnen de zone)
# 3 binnenlijnen: grens tussen onderdelen (op het achterste onderdeel) + sterke modellijnen in het zwart
# 4 buitenlijn 1 px: zwart, selout (donkerste tint) aan de lichtkant (boven/links) van lichte vlakken
# 5 handlaag.txt (kop/poten/kuif naar het model) als laatste
import numpy as np, os
PENMIN = int(os.environ.get('PENMIN', 6))   # (c) min. lengte modellijn in het zwart
from PIL import Image
from scipy import ndimage as nd
from klassen import ZONE
from palet import PAL, MAP, SELOUT, DONKER

K = np.load('onderlaag.npy'); A = np.load('alpha.npy'); F = np.load('frac.npy'); L = np.load('modellijn.npy')
zone = np.vectorize(lambda k: ZONE[k])(K)
dun = np.isin(zone, ['kuif', 'grijs']) | ((zone == 'creme') & (np.arange(64)[None, :] > 50))
mask = (A >= 0.45) | ((A >= 0.28) & dun)
# losse pixels (geen 4-buur) weg
nb = nd.convolve(mask.astype(int), np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]), mode='constant')
mask &= nb > 0

S = np.zeros((64, 64), int)
S[mask] = np.vectorize(lambda k: MAP[k])(K[mask])
# 2b: tint-eilandjes (< 3 px) binnen dezelfde zone opvullen met de omringende tint
Z = np.full((64, 64), '', object); Z[mask] = zone[mask]
for _ in range(2):
    for v in np.unique(S[mask]):
        lab, n = nd.label(S == v)
        for c in range(1, n + 1):
            m = lab == c
            if m.sum() >= 3: continue
            ring = nd.binary_dilation(m) & ~m & mask
            zz = Z[m][0]
            kand = [S[p] for p in zip(*np.where(ring)) if Z[p] == zz and S[p] != v]
            if kand: S[m] = np.bincount(kand).argmax()

PRI = {'oog': 7, 'blauw': 6, 'grijs': 5, 'kuif': 4, 'creme': 3, 'krop': 2, 'vleugel': 1, 'lijn': 0}
lijn = np.zeros((64, 64), bool)
for j in range(64):
    for i in range(64):
        if not mask[j, i]: continue
        for dj, di in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            y, x = j + dj, i + di
            if 0 <= y < 64 and 0 <= x < 64 and mask[y, x]:
                a, b = Z[j, i], Z[y, x]
                if a != b and PRI[a] < PRI[b] and not {a, b} <= {'oog', 'blauw'}:
                    lijn[j, i] = True
# sterke modellijnen in het zwart (vleugel/lijf/staart), alleen lange stukken
sterk = (L >= 0.2) & mask & (Z == 'vleugel')
lab, n = nd.label(sterk, structure=np.ones((3, 3)))
for c in range(1, n + 1):
    m = lab == c; yy, xx = np.where(m)
    if m.sum() >= PENMIN and max(np.ptp(yy), np.ptp(xx)) + 1 >= PENMIN: lijn |= m
S0 = S.copy()
S[lijn] = 1

# buitenlijn
pad = np.pad(~mask, 1, constant_values=True)
rand = mask & (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
g = nd.gaussian_filter(mask.astype(float), 1.2)
gy, gx = np.gradient(g)                     # wijst naar binnen
licht = (gy + gx) / (np.hypot(gx, gy) + 1e-6)   # >0: rand ligt boven/links
T = ~mask
def tp(y, x): return y < 0 or x < 0 or y > 63 or x > 63 or T[y, x]
for j, i in zip(*np.where(rand)):
    zz = Z[j, i]
    # dun deel: transparant aan twee overliggende kanten (1-2 px breed)
    dunH = tp(j, i - 1) and tp(j, i + 1); dunV = tp(j - 1, i) and tp(j + 1, i)
    smal = (tp(j, i - 1) and tp(j, i + 2)) or (tp(j, i + 1) and tp(j, i - 2)) or \
           (tp(j - 1, i) and tp(j + 2, i)) or (tp(j + 1, i) and tp(j - 2, i))
    if zz in SELOUT and (dunH or dunV):
        continue                                   # 1 px breed: modeltint houden
    if zz in SELOUT and smal and licht[j, i] > 0:
        continue                                   # 2 px breed: lichte kant = modeltint, schaduwkant = lijn
    if zz in SELOUT and licht[j, i] > 0.35:
        S[j, i] = SELOUT[zz]
    else:
        S[j, i] = 1
# dambord opheffen (technisch): bij diagonale lijn de onderste/schaduwpixel ook lijn maken
for _ in range(3):
    for y in range(63):
        for x in range(63):
            p, q, r, t = S[y, x], S[y, x + 1], S[y + 1, x], S[y + 1, x + 1]
            if p and q and p == t and q == r and p != q:
                if p == 1: S[y + 1, x] = 1          # lijn LB-RO... lijn op (y,x),(y+1,x+1): vul (y+1,x)
                elif q == 1: S[y + 1, x + 1] = 1    # lijn op (y,x+1),(y+1,x): vul (y+1,x+1)
                else: S[y + 1, x + 1] = p
# zwarte klonten (2x2 lijn binnenin): pixel met het minste modellijn terug naar de modeltint
for y in range(63):
    for x in range(63):
        b = S[y:y + 2, x:x + 2]
        if (b == 1).all() and not rand[y:y + 2, x:x + 2].any():
            c = [(L[y + a, x + d], y + a, x + d) for a in (0, 1) for d in (0, 1)]
            _, yy, xx = min(c); S[yy, xx] = S0[yy, xx]
# barcode (a 1 a 1 a): middelste lijnpixel terug naar de modeltint
for t in range(2):
    V = S if t == 0 else S.T; V0 = S0 if t == 0 else S0.T
    for i in range(64):
        for j in range(60):
            v = V[i, j:j + 5]
            if (v > 0).all() and v[0] == v[2] == v[4] and v[1] == v[3] and v[0] != v[1]:
                k = j + 1 if v[1] == 1 else j + 2
                if V[i, k] == 1: V[i, k] = V0[i, k]
# dambord opnieuw na klont/barcode (technisch): bij diagonale lijn de onderste/schaduwpixel ook lijn maken
for _ in range(3):
    for y in range(63):
        for x in range(63):
            p, q, r, t = S[y, x], S[y, x + 1], S[y + 1, x], S[y + 1, x + 1]
            if p and q and p == t and q == r and p != q:
                if p == 1: S[y + 1, x] = 1          # lijn LB-RO... lijn op (y,x),(y+1,x+1): vul (y+1,x)
                elif q == 1: S[y + 1, x + 1] = 1    # lijn op (y,x+1),(y+1,x): vul (y+1,x+1)
                else: S[y + 1, x + 1] = p
# losse tintpixels (1 px, geen 4-buur met dezelfde tint) -> meest voorkomende tint van dezelfde zone eromheen
for _ in range(2):
    for v in range(2, 16):
        if v == 14: continue                       # oog
        lab, n = nd.label(S == v)
        for c in range(1, n + 1):
            m = lab == c
            if m.sum() != 1: continue
            y, x = map(int, np.argwhere(m)[0])
            kand = [S[p] for p in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if 0 <= p[0] < 64 and 0 <= p[1] < 64
                    and S[p] > 1 and Z[p] == Z[y, x]]
            if len(kand) >= 2: S[y, x] = np.bincount(kand).argmax()
for y in range(63):
    for x in range(63):
        b = S[y:y + 2, x:x + 2]
        if (b == 1).all() and not rand[y:y + 2, x:x + 2].any():
            c = [(L[y + a, x + d], y + a, x + d) for a in (0, 1) for d in (0, 1)]
            _, yy, xx = min(c); S[yy, xx] = S0[yy, xx]
for y in range(63):                                # laatste dambordpass
    for x in range(63):
        p, q, r, t = S[y, x], S[y, x + 1], S[y + 1, x], S[y + 1, x + 1]
        if p and q and p == t and q == r and p != q:
            if p == 1: S[y, x + 1] = 1
            elif q == 1: S[y, x] = 1
np.save('auto.npy', S)

# handlaag
import os
if os.path.exists('handlaag.txt'):
    from handlaag import pas_toe
    S = pas_toe(S)
np.save('hoatzin.npy', S)
im = Image.fromarray(S.astype(np.uint8), 'P')
pal = [0, 0, 0] * 16
for i, c in enumerate(PAL): pal[3 * i:3 * i + 3] = c
im.putpalette(pal + [0] * (768 - len(pal)))
im.save('hoatzin.png', transparency=0)
im.resize((512, 512), Image.NEAREST).save('hoatzin_8x.png', transparency=0)
with open('normal.pal', 'w') as f:
    f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % tuple(c) for c in PAL))
print('kleuren', len(np.unique(S)), 'pixels', int((S > 0).sum()))
