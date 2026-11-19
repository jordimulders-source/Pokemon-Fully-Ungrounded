# Technische opschoning van onderlaag.png -> stap1.png (alleen regels, niets getekend)
# R1 losse lijnpixels binnen de vacht (<=1 lijnbuur) -> vachttoon van de buren
# R2 losse tintpixels (geen enkele 4-buur met dezelfde index, binnen het silhouet) -> meest voorkomende buur
# R3 binnenlijnen tussen vacht en vacht -> donkere vachttoon 2 (Gen 3: binnenlijnen in een donkere tint van het vlak)
# R4 buitenlijn: rand van het silhouet -> 1 (rood: 7)
import os, sys; import numpy as np; from PIL import Image
from collections import Counter
HIER = os.path.dirname(os.path.abspath(__file__)); R1D = os.path.dirname(HIER); sys.path.insert(0, HIER)
from reduceer import save
a = np.asarray(Image.open(os.path.join(R1D, 'onderlaag.png'))).astype(int).copy()
H, W = a.shape
FUR = {2, 3, 4, 5, 6}; RED = {7, 8, 9}
def nb4(y, x): return [(y + dy, x + dx) for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)) if 0 <= y + dy < H and 0 <= x + dx < W]
def nb8(y, x): return [(y + dy, x + dx) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy or dx) and 0 <= y + dy < H and 0 <= x + dx < W]
def rand(y, x): return any(a[p] == 0 for p in nb4(y, x)) or y in (0, H - 1) or x in (0, W - 1)
# R1
b = a.copy()
for y in range(H):
    for x in range(W):
        if a[y, x] == 1 and not rand(y, x):
            if sum(a[p] == 1 for p in nb8(y, x)) <= 1:
                c = Counter(a[p] for p in nb8(y, x) if a[p] not in (0, 1))
                if c: b[y, x] = c.most_common(1)[0][0]
a = b
# R2 (twee keer)
for _ in range(2):
    b = a.copy()
    for y in range(H):
        for x in range(W):
            v = a[y, x]
            if v in (0, 1) or v in (10, 11, 12): continue
            n = [a[p] for p in nb4(y, x)]
            if 0 in n: continue
            if v not in n:
                c = Counter(q for q in n if q != 1)
                if c and c.most_common(1)[0][1] >= 2: b[y, x] = c.most_common(1)[0][0]
    a = b
# R3
b = a.copy()
for y in range(H):
    for x in range(W):
        if a[y, x] == 1 and not rand(y, x):
            n = [a[p] for p in nb8(y, x) if a[p] != 1]
            if n and all(q in FUR for q in n): b[y, x] = 2
a = b
# R4
b = a.copy()
for y in range(H):
    for x in range(W):
        if a[y, x] and rand(y, x) and a[y, x] != 1:
            b[y, x] = 7 if a[y, x] in RED else (14 if a[y, x] in (13, 14) else 1)
a = b
save(a, os.path.join(R1D, 'stap1.png'))
o = np.asarray(Image.open(os.path.join(R1D, 'onderlaag.png')))
print('stap1: px', (a > 0).sum(), 'afwijkend van onderlaag', (a != o).sum())
