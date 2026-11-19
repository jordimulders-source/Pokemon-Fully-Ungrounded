# Llamauler r3 stap 3: handreparaties alleen waar de reductie ruis/te weinig resolutie geeft, elk naar een meting in het model
# (coördinaten = spritepixels; modelposities gemeten met meet.py / naast.py, zie NOTITIES.md). Silhouet blijft gelijk (assert).
import os, json, numpy as np
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__)); R3 = os.path.dirname(HIER)
from toon import png
s2 = np.load(os.path.join(HIER, 'stap2_idx.npy'))
a = s2.copy()
PAL = [tuple(c) for c in json.load(open(os.path.join(HIER, 'palet.json')))]
log = {}
def zet(zone, pts, v):
    for x, y in pts:
        assert a[y, x] != 0, (zone, x, y)
        if a[y, x] != v: log.setdefault(zone, []).append((x, y)); a[y, x] = v

# --- oog (model: zwaar vlak ooglid x 15,8-19,8 op y 14,0-14,4; oogwit 16 en 18,5-19,3; iris/pupil 17,0-18,3; y 14,4-15,9)
zet('oog', [(16, 14), (17, 14), (18, 14), (19, 14)], 1)
zet('oog', [(16, 15), (19, 15)], 7)
zet('oog', [(17, 15)], 1)
zet('oog', [(18, 15)], 8)

# --- kwastjes aan de oren (model: links x 9,7-12,3 y 4,2-9,0 met knoop (11,7; 4,5); rechts x 22,8-26,2 met knoop (23,3; 4,5))
zet('kwastjes', [(11, 5)], 10); zet('kwastjes', [(11, 6)], 11); zet('kwastjes', [(11, 7), (11, 8)], 10)
zet('kwastjes', [(23, 5)], 10); zet('kwastjes', [(23, 6)], 11); zet('kwastjes', [(24, 6)], 10)
zet('kwastjes', [(23, 7)], 10); zet('kwastjes', [(24, 7)], 9); zet('kwastjes', [(23, 8)], 10); zet('kwastjes', [(24, 8)], 9)

# --- halsband (toegestane afwijking: strepen 1 px rood/geel/groen; middenlijn gemeten: kol 12-20 y 30,4-30,8, kol 21 29,6,
#     kol 22 29,0, kol 23 28,1) -> geel op rij 30 (kol 13-20), 29 (kol 21), 28 (kol 22-23)
mid = {c: 30 for c in range(13, 21)}; mid.update({21: 29, 22: 28, 23: 28})
for c, m in mid.items():
    zet('halsband', [(c, m - 1)], 10); zet('halsband', [(c, m)], 12); zet('halsband', [(c, m + 1)], 13)

# --- pompons (toegestane afwijking: stipjes met donkere rand); 2x2 op het gemeten kleurzwaartepunt:
#     rood links (12,3; 33,0) rood rechts (25,3; 29,6) geel (15,2; 34,1) groen (19,4; 33,5) blauw (22,7; 32,0)
WOL = (2, 3, 4, 5, 6)
def pompon(x0, y0, kleur, naam):
    cel = [(x0, y0), (x0 + 1, y0), (x0, y0 + 1), (x0 + 1, y0 + 1)]
    for p in cel: zet(naam, [p], kleur[cel.index(p)])
    ring = [(x0 - 1, y0), (x0 - 1, y0 + 1), (x0, y0 - 1), (x0 + 1, y0 - 1), (x0 + 2, y0), (x0 + 2, y0 + 1), (x0, y0 + 2), (x0 + 1, y0 + 2)]
    for x, y in ring:
        if a[y, x] in WOL:
            zet(naam, [(x, y)], 2 if (x < x0 or y < y0) else 1)
pompon(11, 32, [10, 11, 9, 10], 'pompon rood l')
pompon(24, 29, [11, 10, 10, 9], 'pompon rood r')
pompon(14, 33, [12] * 4, 'pompon geel')
pompon(18, 33, [13] * 4, 'pompon groen')
pompon(22, 31, [14] * 4, 'pompon blauw')
zet('pompon geel', [(15, 32)], 2)          # touwtje van band naar pompon (model x 15, y 31,5-33,4)
# resten van de gereduceerde pompons buiten de 2x2 -> rand
zet('pompon groen', [(19, 32)], 2); zet('pompon groen', [(20, 33)], 1); zet('pompon rood l', [(12, 34)], 1)

# (kwastjes aan het kleed: de reductie zet ze al op de modelplek (32,41)-(32,42) en (42,41); niet aangeraakt)

# --- hoeven onder de handschoenen (model: nabij twee crème nagels x 12,6-13,9 en 14,6-16,3 op y 61,8-63;
#     ver twee grijze nagels x 22,5-24 en 24,5-26,3 op y 61,2-62,2)
zet('hoeven', [(13, 62), (15, 62)], 7)
zet('hoeven', [(23, 61), (25, 61)], 15)

assert ((a > 0) != (s2 > 0)).sum() == 0, 'silhouet gewijzigd'
np.save(os.path.join(HIER, 'lama_idx.npy'), a)
png(a, PAL, os.path.join(R3, 'lama.png'))
for z, p in log.items(): print('%-15s %3d px' % (z, len(p)))
print('totaal hand', sum(len(p) for p in log.values()), 'kleuren', len(np.unique(a)) - 1)
