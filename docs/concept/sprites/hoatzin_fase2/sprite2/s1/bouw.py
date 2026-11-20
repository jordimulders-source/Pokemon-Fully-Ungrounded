# bouw.py: van onderlaag (kale reductie) naar sprite.
# 1 masker (alpha >= .45; dunne delen kuif/grijs/creme-staartpunt al vanaf .28)
# 2 tinten uit het model -> palet (helderheid uit elkaar), kleine tintvlekjes weg (modus binnen de zone)
# 3 binnenlijnen: grens tussen onderdelen (op het achterste onderdeel) + sterke modellijnen in het zwart
# 4 buitenlijn 1 px: zwart, selout (donkerste tint) aan de lichtkant (boven/links) van lichte vlakken
# 5 handlaag.txt (kop/poten/kuif naar het model) als laatste
import numpy as np
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
    if (lab == c).sum() >= 4: lijn |= lab == c
S[lijn] = 1

# buitenlijn
pad = np.pad(~mask, 1, constant_values=True)
rand = mask & (pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:])
g = nd.gaussian_filter(mask.astype(float), 1.2)
gy, gx = np.gradient(g)                     # wijst naar binnen
licht = (gy + gx) / (np.hypot(gx, gy) + 1e-6)   # >0: rand ligt boven/links
for j, i in zip(*np.where(rand)):
    zz = Z[j, i]
    if zz in SELOUT and licht[j, i] > 0.35:
        S[j, i] = SELOUT[zz]
    else:
        S[j, i] = 1
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
