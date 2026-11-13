# steenjaguar r1: natief (Gemini-raster terug) -> exacte 2x2-reductie per mozaiekstuk. Niets getekend.
# Regels: elke spritepixel komt uit zijn 2x2-blok; stukken (tegels) worden in het model gesegmenteerd;
# tussen twee tegels 1 px lijn op de plek waar het model zijn voeg heeft (voegkleur, of zwart waar het model
# een zwarte contourlijn heeft); zwarte tegels zonder voeg; buitenomlijning 1 px; per kleurgroep 3 tinten
# (modeltinten), clusters < 3 px nemen de buurtint aan binnen dezelfde tegel.
# gebruik: python3 reduceer.py natief.png uit.png OY OX   (schrijft ook uit_labels.npy)
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage as nd

IN, UIT = sys.argv[1], sys.argv[2]
SELOUT = len(sys.argv) > 5 and sys.argv[5] == 'selout'
OY, OX = int(sys.argv[3]), int(sys.argv[4])
a = np.asarray(Image.open(IN).convert('RGB')).astype(float)
H, W = a.shape[:2]

# --- achtergrond: bijna-wit verbonden met de rand (tanden zijn ook wit maar ingesloten)
white = a.min(2) >= 215
lab, n = nd.label(white)
border = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
bg = np.isin(lab, list(border))

# --- referentiekleuren per klasse (gemeten met k-means op het natief)
REF = {
 'K':  [(4, 3, 4)],
 'D':  [(34, 31, 31), (52, 45, 44), (70, 58, 54), (82, 75, 80)],
 'B0': [(86, 92, 139)], 'B1': [(123, 127, 176)], 'B2': [(172, 173, 212)],
 'R0': [(103, 56, 48), (121, 67, 57), (80, 44, 38)], 'R1': [(153, 88, 73), (166, 102, 86)], 'R2': [(192, 130, 114)],
 'C0': [(159, 140, 116)], 'C1': [(204, 189, 158)], 'C2': [(236, 231, 214)],
 'W':  [(250, 252, 255)],
}
names = list(REF)
refs = []; rcls = []
for k in names:
    for c in REF[k]:
        refs.append(c); rcls.append(k)
refs = np.array(refs, float)
d = ((a[..., None, :] - refs[None, None]) ** 2).sum(-1)
cls = np.array(rcls)[np.argmin(d, -1)]
lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
sat = (a.max(2) - a.min(2)) / np.maximum(a.max(2), 1)
cls[(lum < 100) & (sat < 0.35) & (cls != 'K')] = 'D'   # grijsbruine voegen, niet donkerrood
cls[bg] = 'bg'
# W alleen binnen het lijf (tanden); crème-wit en tandwit lijken op elkaar: blauwige witte -> W
# tanden: blauwig wit, alleen in de muil (x < 32)
xx = np.arange(W)[None, :].repeat(H, 0)
cls[(cls == 'W') & (xx >= 32)] = 'C2'
teeth = (a.min(2) > 200) & (a[..., 2] >= a[..., 0] - 2) & (xx < 32) & ~bg
cls[teeth] = 'W'

group = {'K': 'line', 'D': 'line', 'B0': 'B', 'B1': 'B', 'B2': 'B', 'R0': 'R', 'R1': 'R', 'R2': 'R',
         'C0': 'C', 'C1': 'C', 'C2': 'C', 'W': 'W', 'bg': 'bg'}
G = np.vectorize(group.get)(cls)
dark = G == 'line'
# zwarte tegels: donker en minstens 2x2 dik
blk = nd.binary_opening(dark, np.ones((2, 2)))
blab, bn = nd.label(blk)
sz = nd.sum(blk, blab, range(1, bn + 1))
blk = np.isin(blab, [i + 1 for i, s in enumerate(sz) if s >= 5])
G[blk] = 'X'
line = dark & ~blk
Kline = line & (cls == 'K')

# --- tegels: verbonden stukken van dezelfde kleurgroep (lijnen scheiden ze)
tile = np.zeros((H, W), int); nt = 0; tgrp = {0: 'none'}
for g in ['B', 'R', 'C', 'W', 'X']:
    l, k = nd.label(G == g)
    for i in range(1, k + 1):
        m = l == i
        nt += 1; tile[m] = nt; tgrp[nt] = g
tsize = np.bincount(tile.ravel(), minlength=nt + 1)
# kleine stukjes (<4 px, antialias-resten) bij de buurtegel
for t in range(1, nt + 1):
    if 0 < tsize[t] < 4:
        m = tile == t
        ring = nd.binary_dilation(m) & ~m & (tile > 0) & (tile != t)
        if ring.any():
            v, c = np.unique(tile[ring], return_counts=True)
            tile[m] = v[np.argmax(c)]
        else:
            tile[m] = 0
tsize = np.bincount(tile.ravel(), minlength=nt + 1)
# lijnpixels krijgen de dichtstbijzijnde tegel (voor de meerderheid per blok)
_, ind = nd.distance_transform_edt(tile == 0, return_indices=True)
tileN = tile[ind[0], ind[1]]
tileN[bg] = 0

# --- reductie
h = (H - OY) // 2; w = (W - OX) // 2
def blk_(j, i):
    return (slice(OY + 2 * j, OY + 2 * j + 2), slice(OX + 2 * i, OX + 2 * i + 2))
body = np.zeros((h, w), bool); T = np.zeros((h, w), int)
nline = np.zeros((h, w), int); nK = np.zeros((h, w), int)
for j in range(h):
    for i in range(w):
        s = blk_(j, i)
        nb = (~bg[s]).sum()
        if nb < 2: continue
        body[j, i] = True
        nline[j, i] = line[s].sum(); nK[j, i] = Kline[s].sum()
        # meerderheid: echte tegelpixels tellen dubbel, lijnpixels via dichtstbijzijnde tegel enkel
        votes = {}
        for t, isl in zip(tileN[s].ravel(), line[s].ravel() | bg[s].ravel()):
            if t == 0: continue
            votes[t] = votes.get(t, 0) + (1 if isl else 2)
        if not votes: T[j, i] = -1; continue
        best = max(votes.values())
        cand = [t for t in votes if votes[t] == best]
        T[j, i] = min(cand, key=lambda t: tsize[t])  # gelijk: kleinste tegel wint (beschermt kleine stukken)
edge = body & ~nd.binary_erosion(body)
# tegelkaart gladmaken: losse uitsteeksels (3 van 4 buren een andere, gelijke tegel) erbij
for it in range(2):
    ssz = np.bincount(T[T > 0].ravel(), minlength=nt + 1)
    for j in range(1, h - 1):
        for i in range(1, w - 1):
            if not body[j, i] or edge[j, i] or T[j, i] <= 0: continue
            nb4 = [T[j - 1, i], T[j + 1, i], T[j, i - 1], T[j, i + 1]]
            v, c = np.unique([t for t in nb4 if t > 0 and t != T[j, i]], return_counts=True)
            if len(v) and c.max() >= 3 and ssz[T[j, i]] > 4:
                ssz[T[j, i]] -= 1; T[j, i] = v[np.argmax(c)]; ssz[T[j, i]] += 1

# lijnen tussen tegels
L = np.zeros((h, w), int)  # 0 geen, 1 zwart contour, 2 voeg
for j in range(h):
    for i in range(w):
        if not body[j, i] or edge[j, i]: continue
        for dj, di in ((0, 1), (1, 0)):
            q = (j + dj, i + di)
            if q[0] >= h or q[1] >= w or not body[q] or edge[q]: continue
            tp, tq = T[j, i], T[q]
            if tp == tq or tp <= 0 or tq <= 0: continue
            if tgrp[tp] == 'X' or tgrp[tq] == 'X': continue
            # waar ligt de modelvoeg? bij de pixel met meer lijnpixels; gelijk: de grotere tegel offert
            if nline[j, i] > nline[q]: who = (j, i)
            elif nline[q] > nline[j, i]: who = q
            else: who = (j, i) if tsize[tp] >= tsize[tq] else q
            kk = nK[j, i] + nK[q]; ll = nline[j, i] + nline[q]
            if ll == 0: continue  # r2: alleen een voeg waar het model er een heeft
            col = 1 if (ll > 0 and kk * 2 > ll) else 2
            if not (j > 19 and i < 16): col = 2  # r2: binnenlijnen in de donkere tint van het vlak, zwart alleen in de muil
            L[who] = max(L[who], col) if L[who] != 2 or col == 2 else 2
            if col == 1: L[who] = 1

# tinten per tegel
TONES = {'B': ['B0', 'B1', 'B2'], 'R': ['R0', 'R1', 'R2'], 'C': ['C0', 'C1', 'C2'], 'W': ['W'], 'X': ['X']}
tone = np.full((h, w), '', object)
tdom = {}
for t in range(1, nt + 1):
    if tsize[t] == 0: continue
    v, c = np.unique(cls[tile == t], return_counts=True)
    tdom[t] = v[np.argmax(c)] if tgrp[t] != 'X' else 'X'
for j in range(h):
    for i in range(w):
        t = T[j, i]
        if t <= 0: continue
        s = blk_(j, i)
        m = (tile[s] == t)
        if tgrp[t] == 'X': tone[j, i] = 'X'; continue
        if m.any():
            v, c = np.unique(cls[s][m], return_counts=True)
            ok = [(cc, vv) for vv, cc in zip(v, c) if vv in TONES[tgrp[t]]]
            tone[j, i] = max(ok)[1] if ok else tdom[t]
        else:
            tone[j, i] = tdom[t]
# ontkorrelen: per tegel clusters < 3 px van een tint -> meest voorkomende buurtint in dezelfde tegel
fillm = body & ~edge & (L == 0) & (T > 0)
for it in range(3):
    changed = 0
    for t in np.unique(T[fillm]):
        if tgrp[t] in ('X', 'W'): continue
        mt = fillm & (T == t)
        for tn in TONES[tgrp[t]]:
            l, k = nd.label(mt & (tone == tn))
            for ci in range(1, k + 1):
                m = l == ci
                if m.sum() >= 4: continue
                ring = nd.binary_dilation(m) & mt & ~m
                if not ring.any(): continue
                v, c = np.unique(tone[ring], return_counts=True)
                if v[np.argmax(c)] != tn:
                    tone[m] = v[np.argmax(c)]; changed += 1
    if not changed: break

# --- uitvoer als labelraster
out = np.full((h, w), '.', object)
for j in range(h):
    for i in range(w):
        if not body[j, i]: continue
        if edge[j, i]:
            # selout: rand aan de lichtkant (achtergrond boven of links) in de donkere tint van het vlak eronder
            lichtkant = (j > 0 and not body[j - 1, i]) or (i > 0 and not body[j, i - 1])
            schaduw = (j < h - 1 and not body[j + 1, i]) or (i < w - 1 and not body[j, i + 1])
            g = tgrp.get(T[j, i], 'X') if T[j, i] > 0 else 'X'
            out[j, i] = {'B': 'DB', 'R': 'DR', 'C': 'DR'}.get(g, 'K') if (SELOUT and lichtkant and not schaduw) else 'K'
        elif L[j, i] == 1: out[j, i] = 'K'
        elif L[j, i] == 2: out[j, i] = {'B': 'DB', 'R': 'DR', 'C': 'DR', 'W': 'K', 'X': 'K'}.get(tgrp.get(T[j, i]), 'DR')
        elif T[j, i] <= 0: out[j, i] = 'K'
        else: out[j, i] = tone[j, i]
np.save(UIT.replace('.png', '_lab.npy'), out)
# ontbrekende tegels
lost = []
for t in range(1, nt + 1):
    if tsize[t] >= 8 and not ((T == t) & ~np.isin(out, ['S', 'K', 'DB', 'DR'])).any():
        ys, xs = np.where(tile == t); lost.append((tgrp[t], int(tsize[t]), int(xs.mean()), int(ys.mean())))
print('fase', OY, OX, 'verloren tegels', len(lost), lost)
