# bouw10.py: s10 = s9 + elk onderdeel 3 tinten, schaduw volgt de vorm (vleugels/lijf/staart uit de cel-shading van het
# model, blauw.py), poten netjes. Vorm en oog bevroren (script bewijst het).
import numpy as np
from PIL import Image
from blauw import herkleur
PAL = [(255, 255, 255), (16, 14, 24),
       (110, 132, 194),                                     # 2 navy licht  (= gezicht midden)
       (78, 68, 122),                                       # 3 navy midden (= gezicht schaduw, = krop donker)
       (34, 32, 58),                                        # 4 navy donker (= grijs donker/selout poten en snavel)
       (244, 236, 212), (214, 204, 178), (172, 160, 134),   # 5-7 creme licht/midden/schaduw
       (190, 190, 186), (134, 134, 132),                    # 8-9 grijs licht/midden (snavel, poten)
       (184, 136, 188), (146, 96, 148),                     # 10-11 krop licht/midden
       (196, 60, 52),                                       # 12 oogrood (= kuif licht)
       (150, 84, 56), (104, 48, 34),                        # 13-14 kuif midden/donker
       (110, 150, 194)]                                     # 15 gezicht licht
S9 = np.array(Image.open('../s9/hoatzin.png')).astype(int)
MAP = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 7, 8: 12, 9: 10, 10: 11, 11: 3, 12: 12, 13: 13, 14: 14, 15: 9}
B = np.vectorize(MAP.get)(S9)
G = np.load('../s7/groep.npy', allow_pickle=True)
creme = lambda x, y: G[y, x] == 'creme' and S9[y, x] in (5, 7)
# blauw: vleugels, lijf, staart
B = herkleur(B, [])
def uit(x, y, dx, dy, ok, n=4):
    for k in range(1, n + 1):
        xx, yy = x + k * dx, y + k * dy
        if not (0 <= xx < 64 and 0 <= yy < 64) or C[yy, xx] not in ok: return k
    return n + 1
C = B.copy()
for y in range(64):
    for x in range(64):
        if creme(x, y):                                    # nek en staartpunt: licht linksboven, midden, sikkel rechtsonder
            br = min(uit(x, y, 1, 0, (5, 7)), uit(x, y, 0, 1, (5, 7)), uit(x, y, 1, 1, (5, 7)))
            tl = min(uit(x, y, -1, 0, (5, 7)), uit(x, y, 0, -1, (5, 7)))
            B[y, x] = 7 if br <= 1 else 6 if (br <= 3 or (y <= 34 and x <= 18 and tl <= 1 and C[y - 1, x] == 1 and x >= 12)) else 5
        elif S9[y, x] in (12, 13, 14) and 15 <= y <= 30:   # kuif
            ok = (12, 13, 14)
            br = min(uit(x, y, 1, 0, ok), uit(x, y, 0, 1, ok), uit(x, y, 1, 1, ok))
            tl = min(uit(x, y, -1, 0, ok), uit(x, y, 0, -1, ok), uit(x, y, -1, -1, ok))
            dun = uit(x, y, -1, 0, ok) + uit(x, y, 1, 0, ok) <= 3 and uit(x, y, 0, -1, ok) + uit(x, y, 0, 1, ok) <= 3
            B[y, x] = 13 if dun else 14 if br <= 1 else 12 if tl <= 1 else 13
# gezicht (blauwe ring): licht linksboven, midden, schaduw rechtsonder
for x, y in [(7, 28), (8, 28), (9, 28), (10, 28), (6, 29), (7, 29), (5, 30), (6, 30)]: B[y, x] = 15
for x, y in [(9, 32), (10, 32), (11, 31)]: B[y, x] = 3
# snavel
for (x, y), v in {(2, 32): 8, (3, 32): 8, (4, 32): 8, (5, 32): 9, (4, 33): 9, (5, 33): 4,
                  (5, 34): 8, (6, 34): 9, (7, 34): 9, (8, 34): 4}.items(): B[y, x] = v
# poten: scheen licht boven -> midden onder, tenen grijs met een lichte klauwpunt, lijn eronder
POOT = {51: (30, '9'), 52: (28, '8'), 53: (27, '8'), 54: (26, '9'), 55: (25, '89'),
        56: (18, '9999999889999'), 57: (17, '89911'),
        'b51': (42, '9'), 'b53': (41, '8'), 'b54': (41, '8'), 'b55': (40, '9'), 'b56': (40, '9'),
        'b57': (38, '489999'), 58: (34, '4444899'), 59: (33, '999199'), 60: (32, '89')}
POOT[56] = (18, '9999999889998'); POOT['b59'] = (39, '9')
for k, (x0, st) in POOT.items():
    y = int(str(k).lstrip('b'))
    for i, ch in enumerate(st): B[y, x0 + i] = int(ch, 16)
# oog bevroren: zwart + 6 rood + ring blauw (ring nu 2 tinten blauw + 1 schaduw)
OOG = [(9, 29), (10, 29), (8, 30), (10, 30), (9, 31), (10, 31)]
assert all(B[y, x] == 12 for x, y in OOG) and B[30, 9] == 1
# dambord-reparatie (blauw): rechtsonder van de stap wordt de buurtint
for _ in range(3):
    for y in range(63):
        for x in range(63):
            p, q, r, t = B[y, x], B[y, x + 1], B[y + 1, x], B[y + 1, x + 1]
            if p and q and p == t and q == r and p != q and {p, q} <= {2, 3, 4}: B[y + 1, x + 1] = q
im = Image.fromarray(B.astype(np.uint8), 'P'); im.putpalette([c for p in PAL for c in p]); im.save('hoatzin.png', transparency=0)
im.convert('RGB').resize((512, 512), Image.NEAREST).save('hoatzin_8x.png')
with open('normal.pal', 'w') as f: f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % p for p in PAL))
print('silhouet anders dan s9:', int(((S9 > 0) != (B > 0)).sum()))
