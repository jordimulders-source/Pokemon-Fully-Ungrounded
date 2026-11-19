# Llamauler r3 stap 1: kale reductie van model_v3 -> onderlaag_idx.npy (+ zone.npy)
# Niets getekend: silhouet = modelalfa (dekking >= 0,45); elke binnenpixel krijgt de toon van het model op die plek:
#  - wol: gem. helderheid van de wolpixels zonder lijn -> band (licht / basis / schaduw / diep)
#  - binnenlijnen: waar het model een lijn heeft (lijnpixels < 100 in het blok >= LIJN), uitgedund tot 1 px
#    (alleen de cel met het meeste lijn loodrecht op de lijnrichting houdt hem: 'non-maximum suppression')
#  - rood/geel/groen/blauw/grijs: klasse met de meeste modelpixels, toon uit hun helderheid
import os, json, numpy as np
from meet import cel, lijnfrac, HIER

DEK = 0.45
LICHT, BASIS, DIEP = 162, 146, 118   # banden op de gem. helderheid van de wolpixels zonder lijn
LIJN = 0.12                           # min. aandeel lijnpixels voor een binnenlijn
def furtoon(m):
    if m >= LICHT: return 6
    if m >= BASIS: return 5
    if m >= DIEP: return 4
    return 3
def vertoon(m): return 3 if m >= 95 else 2       # verre poten: binnenlijn-/lijntonen (donkerder dan de nabije)
def kleedtoon(px, y):
    # kleed: aandeel lichte draden (rood met helderheid >= 105) in het blok -> streep/patroon uit het model
    f = (px.mean(1) >= 105).mean()
    if y >= 35: return 10 if f >= 0.12 else 9
    return 11 if f >= 0.62 else 10 if f >= 0.25 else 9
def roodtoon(l):
    if l >= 118: return 11
    if l >= 92: return 10
    return 9
NAMEN = {1: 'lijn donker', 2: 'lijn zacht', 3: 'wol diep / binnenlijn', 4: 'wol schaduw', 5: 'wol basis', 6: 'wol licht',
         7: 'creme (oogwit, hoefnagels)', 8: 'vrij', 9: 'rood donker', 10: 'rood', 11: 'rood licht',
         12: 'geel', 13: 'groen', 14: 'blauw', 15: 'polsband grijs'}

out = np.zeros((64, 64), int)
zone = np.full((64, 64), '', object)
F = np.zeros((64, 64)); Q = np.zeros((64, 64), int)
for y in range(64):
    for x in range(64):
        c = cel(x, y)
        if c is None or c['dek'] < DEK: continue
        n = c['n']; w = dict(n)
        for k in ('yel', 'grn', 'blu'): w[k] *= 2.0
        w['red'] *= 1.2; w['gry'] *= 1.2
        k = max(w, key=w.get); zone[y, x] = k
        px = c['rgb'][k]; lp = px.mean(1); l = lp.mean()
        zonder = lp[lp >= 100]; m = zonder.mean() if len(zonder) else l
        if k == 'fur': v = furtoon(m)
        elif k == 'ver': v = vertoon(m)
        elif k == 'red': v = (kleedtoon(px, y) if y < 45 else roodtoon(l)) if l >= 60 else 1
        elif k == 'yel': v = 12
        elif k == 'grn': v = 13 if l >= 60 else 1
        elif k == 'blu': v = 14 if l >= 70 else 1
        elif k == 'gry': v = 15 if l >= 50 else 1
        out[y, x] = v
        if k == 'fur':      # verre poten (2-3 px breed) krijgen geen binnenlijnen
            F[y, x], Q[y, x] = lijnfrac(x, y)

PERP = {0: [(0, -1), (0, 1)], 1: [(1, -1), (-1, 1)], 2: [(-1, 0), (1, 0)], 3: [(1, 1), (-1, -1)]}
lijn = np.zeros((64, 64), bool)
for y in range(1, 63):
    for x in range(1, 63):
        if F[y, x] < LIJN: continue
        if all(F[y, x] >= F[y + dy, x + dx] for dx, dy in PERP[Q[y, x]]):
            lijn[y, x] = True
for y, x in zip(*np.nonzero(lijn)):
    out[y, x] = 3 if zone[y, x] == 'fur' else 1

np.save(os.path.join(HIER, 'zone.npy'), zone.astype(str))
np.save(os.path.join(HIER, 'lijnfrac.npy'), F)
np.save(os.path.join(HIER, 'onderlaag_idx.npy'), out)
for v in range(1, 16): print(v, NAMEN[v], int((out == v).sum()))
ys, xs = np.nonzero(out)
print('box', xs.min(), xs.max(), ys.min(), ys.max(), 'px', (out > 0).sum(), 'binnenlijn', int(lijn.sum()))
