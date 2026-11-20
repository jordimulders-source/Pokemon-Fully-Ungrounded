# bouw10.py: s10 = s9, opnieuw ingekleurd naar de studie van bestaande sprites (STUDIE in NOTITIES.md).
# Vorm en oog bevroren (script bewijst het). Per vorm: grote lichte zone linksboven / donkere zone rechtsonder (Honchkrow),
# binnenlijnen in de donkerste vlaktint, zwart alleen op de buitencontour (Braviary), 1-px sikkel rechtsonder.
import numpy as np
from PIL import Image
from scipy import ndimage as nd
PAL = [(255, 255, 255), (16, 14, 24),
       (96, 108, 170),                                      # 2 navy lichte zone  (= gezicht midden)
       (64, 60, 104),                                       # 3 navy donkere zone (= gezicht schaduw, = krop donker)
       (32, 30, 54),                                        # 4 navy binnenlijn/sikkel (= grijs donker)
       (244, 236, 212), (208, 198, 172),                    # 5-6 creme licht/midden
       (146, 144, 136),                                     # 7 creme schaduw = grijs midden (Staraptor/Honchkrow: wit schaduwt grijs)
       (192, 192, 188),                                     # 8 grijs licht (snavel, poten)
       (184, 136, 188), (146, 96, 148),                     # 9-10 krop licht/midden
       (178, 108, 70), (142, 76, 52), (100, 46, 32),        # 11-13 kuif licht/midden/donker
       (196, 60, 52),                                       # 14 oogrood
       (110, 150, 194)]                                     # 15 gezicht licht
S9 = np.array(Image.open('../s9/hoatzin.png')).astype(int)
MAP = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 7, 8: 14, 9: 9, 10: 10, 11: 3, 12: 11, 13: 12, 14: 13, 15: 7}
B = np.vectorize(MAP.get)(S9)
for y in range(26, 34):
    for x in range(3, 13):
        if S9[y, x] == 2: B[y, x] = 15                    # gezichtsring
G = np.load('../s7/groep.npy', allow_pickle=True)
H, W = 64, 64
# ---- vormen (vleugels, lijf, staart) ----
def vorm(x, y):
    if x < 13 or y >= 50 or S9[y, x] not in (1, 2, 3, 4): return ''
    if y <= 30 and x <= 29: return 'ver'
    if y <= 32 and x >= 30: return 'nabij'
    if (x >= 44 and y >= 40) or (x >= 41 and y >= 46): return 'staart'
    if y >= 31 and x >= 26: return 'lijf'
    return ''
V = np.array([[vorm(x, y) for x in range(W)] for y in range(H)], object)
Z = B.copy()
for f in ('ver', 'nabij', 'lijf', 'staart'):
    M = V == f
    pad = np.pad(M, 1)
    tl = M & (~pad[1:-1, :-2] | ~pad[:-2, 1:-1])           # rand met lucht/andere vorm links of boven
    br = M & (~pad[1:-1, 2:] | ~pad[2:, 1:-1])
    dtl = nd.distance_transform_edt(~tl); dbr = nd.distance_transform_edt(~br)
    licht = (dtl <= 0.8 * dbr) if f != 'lijf' else (dtl <= 0.6 * dbr)
    for y, x in zip(*np.where(M)):
        buiten = any(not (0 <= x + a < W and 0 <= y + b < H) or S9[y + b, x + a] == 0 for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        if S9[y, x] == 1:
            Z[y, x] = 1 if buiten or any(V[y + b, x + a] not in (f, '') and S9[y + b, x + a] != 1
                                          for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + a < W and 0 <= y + b < H) else 4
            continue
        if f == 'ver': Z[y, x] = 2 if dtl[y, x] < 1.5 else 3        # verre vleugel: een stap donkerder, lichte rand
        else: Z[y, x] = 2 if licht[y, x] else 3
        if dbr[y, x] < 1.5 and f != 'ver': Z[y, x] = 4                 # sikkel langs de rand rechtsonder
B = Z
# binnenlijn in de lichte zone: een tint donkerder dan zwart -> 4 blijft; in de donkere zone wordt 4 te zwak -> zwart
C = B.copy()
for y, x in zip(*np.where(np.isin(V, ['ver', 'nabij', 'lijf', 'staart']) & (S9 == 1) & (C == 4))):
    buren = [C[y + b, x + a] for a in (-1, 0, 1) for b in (-1, 0, 1) if 0 <= x + a < W and 0 <= y + b < H]
    if buren.count(3) > buren.count(2): B[y, x] = 1
# ---- creme (nek, staartpunt): licht linksboven, midden, sikkel rechtsonder (Staraptor-borst) ----
C = B.copy()
def uit(x, y, dx, dy, ok, n=4):
    for k in range(1, n + 1):
        xx, yy = x + k * dx, y + k * dy
        if not (0 <= xx < W and 0 <= yy < H) or C[yy, xx] not in ok: return k
    return n + 1
for y in range(H):
    for x in range(W):
        if G[y, x] == 'creme' and S9[y, x] in (5, 7):
            ok = (5, 7)
            br = min(uit(x, y, 1, 0, ok), uit(x, y, 0, 1, ok), uit(x, y, 1, 1, ok))
            B[y, x] = 7 if br <= 1 else 6 if br <= 2 else 5
        elif S9[y, x] in (12, 13, 14) and 15 <= y <= 30:   # kuif (Pidgeot/Staraptor: licht linksboven, donker onder)
            ok = (11, 12, 13)
            br = min(uit(x, y, 1, 0, ok), uit(x, y, 0, 1, ok))
            tl = min(uit(x, y, -1, 0, ok), uit(x, y, 0, -1, ok))
            dun = uit(x, y, -1, 0, ok) + uit(x, y, 1, 0, ok) <= 3
            B[y, x] = 12 if dun and y <= 22 else 13 if br <= 1 else 11 if tl <= 1 else 12
# staartpunt: s9-grijs (oude creme-midden) hoort bij de creme
for y in range(45, 53):
    for x in range(47, 64):
        if B[y, x] == 8: B[y, x] = 6
# gezicht: ring licht linksboven, midden, schaduw rechtsonder
for x, y in [(9, 32), (10, 32), (11, 31), (11, 30)]:
    if B[y, x] == 15: B[y, x] = 3
for x, y in [(11, 29), (7, 32), (8, 32), (6, 31), (7, 31)]:
    if B[y, x] == 15: B[y, x] = 2
# snavel (Skarmory/Honchkrow-snavel: licht boven, midden, donker onder)
for (x, y), v in {(2, 32): 8, (3, 32): 8, (4, 32): 8, (5, 32): 7, (4, 33): 7, (5, 33): 4,
                  (5, 34): 8, (6, 34): 7, (7, 34): 7, (8, 34): 4}.items(): B[y, x] = v
# poten (Honchkrow/Skarmory: scheen licht->midden, tenen grijs met zwarte lijn, klauw = lichte punt)
POOT = {51: (30, '7'), 52: (28, '8'), 53: (27, '8'), 54: (26, '7'), 55: (25, '87'),
        56: (18, '7777777887778'), 57: (17, '87711'),
        'b51': (42, '7'), 'b53': (41, '8'), 'b54': (41, '8'), 'b55': (40, '7'), 'b56': (40, '7'),
        'b57': (38, '487777'), 58: (34, '4444877'), 59: (33, '777177'), 60: (32, '87')}
for k, (x0, st) in POOT.items():
    y = int(str(k).lstrip('b'))
    for i, ch in enumerate(st): B[y, x0 + i] = int(ch, 16)
# bewijs
OOG = [(9, 29), (10, 29), (8, 30), (10, 30), (9, 31), (10, 31)]
assert all(B[y, x] == 14 for x, y in OOG) and B[30, 9] == 1
for _ in range(3):
    for y in range(63):
        for x in range(63):
            p, q, r, t = B[y, x], B[y, x + 1], B[y + 1, x], B[y + 1, x + 1]
            if not (p and q and p == t and q == r and p != q): continue
            if {p, q} <= {2, 3, 4}: B[y + 1, x + 1] = q
            elif q == 1 and p in (2, 3, 4): B[y + 1, x] = 4            # diagonale stap van een penlijn: een lijnpixel in de donkerste tint
            elif p == 1 and q in (2, 3, 4): B[y + 1, x + 1] = 4
            elif 1 not in (p, q) and 14 not in (p, q): B[y + 1, x + 1] = q
            elif p == 12 and q == 1: B[y, x] = 13
im = Image.fromarray(B.astype(np.uint8), 'P'); im.putpalette([c for p in PAL for c in p]); im.save('hoatzin.png', transparency=0)
im.convert('RGB').resize((512, 512), Image.NEAREST).save('hoatzin_8x.png')
with open('normal.pal', 'w') as f: f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % p for p in PAL))
print('silhouet anders dan s9:', int(((S9 > 0) != (B > 0)).sum()))
