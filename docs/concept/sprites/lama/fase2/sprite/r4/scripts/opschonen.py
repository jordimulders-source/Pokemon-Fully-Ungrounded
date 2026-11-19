# Llamauler r3 stap 2: alleen technische regels op de onderlaag (geen vormen):
#  a) buitenlijn 1 px: elke pixel die aan transparant grenst wordt lijn (zacht 2 aan de lichtkant links/boven, donker 1 elders;
#     rood/verre poot/polsband altijd 1)
#  b) ruis: losse wolpixel (4/5/6) zonder gelijke 4-buur -> meest voorkomende wolbuur; losse binnenlijnpixel (3) zonder
#     lijnbuur (1/2/3, 8-buren) -> meest voorkomende wolbuur
import os, json, numpy as np
from collections import Counter
HIER = os.path.dirname(os.path.abspath(__file__))
o = np.load(os.path.join(HIER, 'onderlaag_idx.npy'))
a = o.copy(); H, W = a.shape
N4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
N8 = N4 + [(-1, -1), (-1, 1), (1, -1), (1, 1)]
def g(arr, x, y): return arr[y, x] if 0 <= x < W and 0 <= y < H else 0
WOL = (4, 5, 6)
# b) ruis eerst (op de onderlaag), twee keer
for _ in range(2):
    b = a.copy()
    for y in range(H):
        for x in range(W):
            v = a[y, x]
            if v in WOL and not any(g(a, x + dx, y + dy) == v for dx, dy in N4):
                c = Counter(g(a, x + dx, y + dy) for dx, dy in N8 if g(a, x + dx, y + dy) in WOL)
                if c: b[y, x] = c.most_common(1)[0][0]
            elif v == 3 and not any(g(a, x + dx, y + dy) in (1, 2, 3) for dx, dy in N8):
                c = Counter(g(a, x + dx, y + dy) for dx, dy in N8 if g(a, x + dx, y + dy) in WOL)
                if c: b[y, x] = c.most_common(1)[0][0]
    a = b
# a) buitenlijn. Kleur per randpixel uit de gemiddelde richting van de lege pixels in een 5x5-venster:
#    wijst die naar links/boven (lichtkant) en is de pixel wol -> zachte lijn 2, anders donker 1. Daarna gladgestreken
#    langs de rand (geen 1/2 om en om): een 2 zonder 2-buur op de rand -> 1, een 1 tussen twee 2'en -> 2.
b = a.copy(); rand = []
for y in range(H):
    for x in range(W):
        v = a[y, x]
        if v == 0 or not any(g(a, x + dx, y + dy) == 0 for dx, dy in N4): continue
        rand.append((x, y))
        if v in (12, 13, 14): continue
        sx = sy = 0
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if (dx or dy) and g(a, x + dx, y + dy) == 0: sx += dx; sy += dy
        n = (sx * sx + sy * sy) ** .5 or 1
        licht = (sx + sy) / n < -0.35
        b[y, x] = 2 if (licht and v in (2, 3, 4, 5, 6)) else 1
R = set(rand)
for _ in range(2):
    c = b.copy()
    for x, y in rand:
        nb = [b[y + dy, x + dx] for dx, dy in N8 if (x + dx, y + dy) in R]
        if b[y, x] == 2 and nb.count(2) == 0: c[y, x] = 1
        elif b[y, x] == 1 and nb.count(2) >= 2 and a[y, x] in (2, 3, 4, 5, 6): c[y, x] = 2
    b = c
a = b
np.save(os.path.join(HIER, 'stap2_idx.npy'), a)
print('anders dan onderlaag:', int((a != o).sum()), 'alfa-diff:', int(((a > 0) != (o > 0)).sum()))
