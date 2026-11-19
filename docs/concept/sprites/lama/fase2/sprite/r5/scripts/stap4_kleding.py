# r5 stap 4: kleed, polsbanden en handschoenen in dezelfde licht-logica (licht linksboven, schaduw rechtsonder, ver een stap donkerder),
# zonder vlekken; vormen blijven (silhouet ongewijzigd t.o.v. stap 3).
import numpy as np
a = np.load('stap3.npy'); s3 = a.copy(); H, W = a.shape
KLEED = (9, 10, 11)
def g(x, y): return a[y, x] if 0 <= x < W and 0 <= y < H else 0
# --- kleed (model: boven rij 27-34 helderheid 100-120, onder rij 35-40 70-80, randen donkerder; lichte strepen onder op x 34 en 39)
kl = [(x, y) for y in range(27, 41) for x in range(26, 45) if a[y, x] in KLEED]
xs = {}
for x, y in kl: xs.setdefault(y, []).append(x)
for x, y in kl:
    lo, hi = min(xs[y]), max(xs[y])
    if y <= 34:
        v = 10
        if y <= 29 and x <= lo + 6: v = 11            # licht op de bovenkant links (licht linksboven)
        if x == hi or (y >= 32 and x == lo): v = 9   # omslag aan de zijkant in schaduw
    else:
        v = 9
        if x in (34, 39): v = 10                      # lichte strepen (gemeten)
    a[y, x] = v
# --- polsband nabij (model rij 54,5-57,5: grijs boven, zwart onder): licht 8, midden 15, donker 1
for x, y in [(17, 55)]: a[y, x] = 1
for x, y in [(18, 55), (19, 55)]: a[y, x] = 8
for x, y in [(20, 55), (17, 56), (18, 56), (19, 56)]: a[y, x] = 15
for x, y in [(20, 56), (21, 55), (21, 56), (18, 57), (19, 57), (20, 57), (21, 57)]: a[y, x] = 1
# --- polsband ver (model rij 53-56, zwart met grijze bovenrand): een stap donkerder: 15 boven, 1 onder
for x, y in [(25, 55), (26, 55)]: a[y, x] = 15
for x, y in [(25, 56), (26, 56), (27, 56)]: a[y, x] = 1
# --- handschoenen: per pixel licht/basis/schaduw uit de afstand tot de rand linksboven/rechtsonder
def afst(x, y, dirs, binnen):
    best = 9
    for dx, dy in dirs:
        k = 1
        while (x + k * dx, y + k * dy) in binnen: k += 1
        best = min(best, k)
    return best
for naam, xr, ramp in [('nabij', range(10, 22), (11, 10, 9)), ('ver', range(22, 30), (10, 9, 9))]:
    hs = {(x, y) for y in range(57, 63) for x in xr if a[y, x] in KLEED}
    for x, y in hs:
        dl = afst(x, y, [(-1, 0), (0, -1), (-1, -1)], hs); ds = afst(x, y, [(1, 0), (0, 1), (1, 1)], hs)
        a[y, x] = ramp[0] if (dl <= 2 and ds > 1) else ramp[2] if ds <= 1 else ramp[1]
# nagels ver (model: twee grijze nagels x 22,5-24 en 24,5-26,3 op rij 61-62)
a[61, 23] = 15; a[61, 24] = 1; a[61, 25] = 15
# iris: grijs 15 (index 8 wordt het licht van de polsband)
a[15, 18] = 15
# losse vachtpixel (4/5/6 zonder gelijke 4-buur) in lijf/hals/kop -> meest voorkomende vachtbuur
from collections import Counter
for y in range(7, 47):
    for x in range(W):
        v = a[y, x]
        nb = [a[y + dy, x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < W]
        if v in (4, 5, 6) and v not in nb:
            c = Counter(n for n in nb if n in (4, 5, 6))
            if c: a[y, x] = c.most_common(1)[0][0]
assert ((a > 0) == (s3 > 0)).all()
np.save('stap4.npy', a); print('anders dan stap 3:', int((a != s3).sum()))
