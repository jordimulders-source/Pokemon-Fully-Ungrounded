# r5 stap 1: vachttonen van lijf, hals en kop opnieuw uit het model, maar rustig (grote vlakken, één ramp 6/5/4).
# Silhouet = r4b (wolbogen komen in stap 2). Lijnen van gezicht/oor/kwastjes blijven; buitenlijn wordt in stap 3 opnieuw gezet.
import numpy as np
from PIL import Image
r4b = np.array(Image.open('../../r4/lama_b.png'))
T = np.load('toon_model.npy')[0]
a = r4b.copy(); H, W = a.shape
VACHT = (2, 3, 4, 5, 6)
def g(arr, x, y, d=0): return arr[y, x] if 0 <= x < W and 0 <= y < H else d
# vachtzone: rij 7-46, geen oren (boven rij 9 alleen de kap x 15-19), geen gezichtslijnen (snuit/mond/oog rij 13-19, x <= 20)
Z = np.zeros_like(a, bool)
for y in range(7, 47):
    for x in range(W):
        if a[y, x] not in VACHT: continue
        if y < 9 and not (15 <= x <= 19): continue
        Z[y, x] = True
# lijnen in het gezicht houden (mond, neusgat, kaaklijn): index 3/1 in rij 13-19, x 10-15
for y in range(13, 20):
    for x in range(10, 16):
        if a[y, x] in (1, 3): Z[y, x] = False
# modeltoon, gaten vullen met buurgemiddelde, dan glad (3x3, gewichten 1-2-1) binnen de zone
M = T.copy()
for _ in range(3):
    n = M.copy()
    for y, x in zip(*np.nonzero(Z & np.isnan(M))):
        v = [M[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if 0 <= y + dy < H and 0 <= x + dx < W and not np.isnan(M[y + dy, x + dx])]
        if v: n[y, x] = np.mean(v)
    M = n
K = {(-1, -1): 1, (0, -1): 2, (1, -1): 1, (-1, 0): 2, (0, 0): 4, (1, 0): 2, (-1, 1): 1, (0, 1): 2, (1, 1): 1}
G = M.copy()
for y, x in zip(*np.nonzero(Z)):
    s = w = 0
    for (dx, dy), k in K.items():
        if 0 <= y + dy < H and 0 <= x + dx < W and Z[y + dy, x + dx] and not np.isnan(M[y + dy, x + dx]):
            s += k * M[y + dy, x + dx]; w += k
    G[y, x] = s / w
np.save('glad.npy', G)
# één lichtbron linksboven: afstand tot de omtrek naar linksboven (licht) en naar rechtsonder (schaduw),
# gecombineerd met de grote licht/donker-vormen van het model (G)
silh = r4b > 0
def afst(x, y, dirs, maxd=6):
    best = maxd
    for dx, dy in dirs:
        for k in range(1, maxd):
            if not g(silh, x + k * dx, y + k * dy, False): best = min(best, k); break
    return best
LD = [(-1, 0), (0, -1), (-1, -1)]; SD = [(1, 0), (0, 1), (1, 1)]
LICHT, DONKER = 163, 136
t = np.full_like(a, 5)
for y, x in zip(*np.nonzero(Z)):
    dl, ds = afst(x, y, LD), afst(x, y, SD)
    l = G[y, x] >= LICHT or dl <= 2
    d = G[y, x] < DONKER or ds <= 3
    if l and d: t[y, x] = 6 if G[y, x] >= 150 else 4
    elif l: t[y, x] = 6
    elif d: t[y, x] = 4
for y, x in zip(*np.nonzero(Z)): a[y, x] = t[y, x]
# rust: 3x3-meerderheid (2x) en vlakjes < 4 px naar de meest voorkomende buur
from collections import Counter
for _ in range(2):
    b = a.copy()
    for y, x in zip(*np.nonzero(Z)):
        c = Counter(a[y + dy, x + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1) if Z[y + dy, x + dx])
        v, n = c.most_common(1)[0]
        if n >= 6 and v != a[y, x]: b[y, x] = v
    a = b
def vlakjes(a, Z, minn=4):
    seen = np.zeros_like(Z)
    for y, x in zip(*np.nonzero(Z)):
        if seen[y, x]: continue
        v = a[y, x]; st = [(x, y)]; comp = []; seen[y, x] = True
        while st:
            cx, cy = st.pop(); comp.append((cx, cy))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < W and 0 <= ny < H and Z[ny, nx] and not seen[ny, nx] and a[ny, nx] == v:
                    seen[ny, nx] = True; st.append((nx, ny))
        if len(comp) < minn:
            c = Counter(a[cy + dy, cx + dx] for cx, cy in comp for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                        if 0 <= cx + dx < W and 0 <= cy + dy < H and Z[cy + dy, cx + dx] and (cx + dx, cy + dy) not in comp)
            if c:
                for cx, cy in comp: a[cy, cx] = c.most_common(1)[0][0]
    return a
for _ in range(2): a = vlakjes(a, Z)
np.save('zone_vacht.npy', Z); np.save('stap1.npy', a)
print('vachtzone', Z.sum(), 'tonen', {v: int((a[Z] == v).sum()) for v in (4, 5, 6)})
