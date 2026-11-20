# rest14.py (r14): buikbovenrand, voeten, staart, nek/vleugel-binnenlijn op k14.npy -> hoatzin.png
# - buik (x16-35, y36-46): bovenrand als koepel van (17,40) naar (24,36); bovenste rij D links -> C rechts,
#   hooglicht D als kleine ovaal linksboven, sikkel B rechts (breder vanaf y42). Pixels boven de nieuwe rand -> nek (4/5).
# - nabije voet: palm + 3 tenen schuin gespreid (voor-links omlaag, midden omlaag, rechts omlaag), zwarte klauwen;
#   geen lichte balk op y56. Verre voet: lange teen met één onderrand (y56 = 2, y57 transparant).
# - staart bijna zwart (vlak 2, scheidingen 1, licht randje 3 links) zodat hij loskomt van de vleugel.
# - nek/vleugel: binnenlijn 1 langs de voorrand van de vleugel (x24-29, y24-35).
import numpy as np; from PIL import Image
from geom import PAL
a = np.load('k14.npy'); P = np.load('part.npy')
B, C, D = 11, 12, 13
# ---------------- buik ----------------
ytop = lambda x: 36 + 4 * ((x - 24) / 7.0) ** 2 if x <= 24 else 36
oud = a.copy()
xr = {}
for y in range(36, 47):
    xs = [x for x in range(14, 40) if oud[y, x] in (B, C, D)]
    xr[y] = max(xs) if xs else 0
for y in range(36, 47):
    for x in range(16, 26):
        bel = oud[y, x] in (B, C, D)
        nek = oud[y, x] in (3, 4, 5)
        onder = y >= ytop(x) - 0.5
        if bel and not onder:
            lb = oud[y, x-1] == 0 or oud[y, x-2] == 0
            a[y, x] = 3 if oud[y, x-1] == 0 else (5 if lb else 4)
        elif nek and onder and x >= 17 and P[y, x] in (2, 3):
            a[y, x] = C; oud[y, x] = C
for y in range(36, 47):
    xs = [x for x in range(14, 40) if a[y, x] in (B, C, D)]
    if not xs: continue
    for x in xs:
        if a[y, x-1] == 0: a[y, x] = B; continue          # linkerrand
        e = xr[y] - x; d = y - ytop(x)
        if e <= (2 if y >= 42 else 0) and x >= 23: c = B
        elif d < 1.0: c = D if x <= 21 else C
        elif ((x - 19.2) / 1.9) ** 2 + ((y - 39.9) / 1.3) ** 2 < 1: c = D
        else: c = C
        a[y, x] = c
# ---------------- voeten ----------------
for y in range(55, 64):
    for x in range(27 if y <= 56 else 26, 40):
        if a[y, x] in (14, 15) or (a[y, x] in (1, 2) and P[y, x] != 1): a[y, x] = 0
NAB = {55: [(30, 34)], 56: [(29, 35)], 57: [(28, 29), (31, 32), (35, 36)], 58: [(27, 28), (31, 32), (36, 37)],
       59: [(30, 31)], 60: [(30, 31)], 61: [(30, 30)]}
mn = np.zeros((64, 64), bool)
for y, rs in NAB.items():
    for x0, x1 in rs: mn[y, x0:x1+1] = True
uit = lambda yy, xx: not mn[yy, xx]
for y, x in zip(*np.nonzero(mn)):
    c = 14
    if uit(y, x-1) or (uit(y-1, x) and x <= 31): c = 15
    if uit(y+1, x) and y == 56 and c == 14: c = 2          # alleen de onderkant van de palm donker
    a[y, x] = c
for y, x in zip(*np.nonzero(mn)):
    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy, xx = y+dy, x+dx
        if not mn[yy, xx] and a[yy, xx] in (0, 14, 2) and not (yy == 54 and 30 <= xx <= 34):
            if a[yy, xx] == 0 or P[yy, xx] in (5,):
                a[yy, xx] = 2 if (dy < 0 and xx <= 31) else 1
for x, y in [(26, 59), (25, 60), (38, 59), (38, 60), (30, 62), (29, 63)]: a[y, x] = 1   # klauwen
# verre voet: lange teen met één onderrand
for x in range(16, 23):
    a[56, x] = 2; a[57, x] = 0
a[56, 16] = 1; a[57, 15] = 1; a[58, 15] = 1
# ---------------- staart ----------------
st = (P == 1) & (a != 0); st[:44] = False
bg = a == 0
rand = lambda y, x: any(0 <= y+dy < 64 and 0 <= x+dx < 64 and bg[y+dy, x+dx] for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)))
ax, ay = 11.0, 19.0; nn = np.hypot(ax, ay); ux, uy = ay/nn, -ax/nn     # dwars op de staartas (39,44)->(50,63)
for y, x in zip(*np.nonzero(st)):
    if rand(y, x): a[y, x] = 1; continue
    u = (x - 39) * ux + (y - 44) * uy
    a[y, x] = 1 if (y >= 48 and (abs(u - 0.8) < 0.6 or abs(u + 2.0) < 0.6)) else 2
for y, x in zip(*np.nonzero(st)):           # licht randje links (3) binnen de buitenlijn
    if a[y, x] == 2 and a[y, x-1] == 1 and bg[y, x-2] if x >= 2 else False: a[y, x] = 3
# ---------------- nek/vleugel-binnenlijn ----------------
Lw = {y: min([x for x in range(64) if P[y, x] == 4] or [64]) for y in range(64)}
for y in range(24, 36):
    x = Lw[y] - 1
    if 24 <= x <= 29 and a[y, x] in (2, 3): a[y, x] = 1
# losse reparaties: rest oude teen, inkeping verre vleugel, kuifbases F5/F6
a[56, 26] = 1; a[4, 11] = 1; a[18, 18] = 6
# staart: eventueel 2x2-dambord van scheidingslijn (1) en vlak (2) -> trapje
for ronde in range(4):
    for y in range(44, 63):
        for x in range(36, 63):
            p, q, r, t = a[y,x], a[y,x+1], a[y+1,x], a[y+1,x+1]
            if p and q and p == t and q == r and {int(p), int(q)} == {1, 2} and P[y, x] == 1:
                if p == 2: a[y, x] = 1
                else: a[y, x+1] = 1
np.save('r14.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('hoatzin.png', transparency=0)
