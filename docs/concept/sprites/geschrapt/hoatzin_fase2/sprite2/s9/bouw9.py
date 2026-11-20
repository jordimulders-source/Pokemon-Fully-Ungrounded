# bouw9.py: s9 = s8 + Jordi/coordinator 20 nov. Vorm bevroren (silhouet = s8), alleen kleur en lijn. Oog: pixels gelijk.
#  1. snavel/poten eigen neutraal grijs (6 licht, 15 midden, 4 donker); creme heeft 5 licht + 7 schaduw (geen gedeelde tint)
#     paletplek vrij: gezichtsblauw = lichtste vleugeltint 2 (die is lichter en blauwer gemaakt)
#  2a. buitenrand zwart waar het onderdeel daarachter nog >= 2 px kleur houdt (dunne plukken/tenen houden hun kleur)
#  2b. waardebereik: 4 bijna zwart navy, 2 lichter
#  2c/d. sikkels: lijf, nabije vleugel, nek (licht linksboven, schaduw rechtsonder)
#  3. 2x2-blokje 4 op (40-41,39-40): (40,40),(41,40) -> 3
import numpy as np
from PIL import Image
PAL = [(255, 255, 255), (16, 14, 24),
       (110, 132, 194), (70, 72, 120), (34, 32, 58),        # 2-4 blauwzwart licht (= gezicht) / midden / schaduw
       (244, 236, 212),                                     # 5 creme licht
       (184, 184, 180),                                     # 6 grijs licht (snavel, poten)
       (178, 164, 136),                                     # 7 creme schaduw
       (196, 60, 52),                                       # 8 oog rood
       (184, 136, 188), (146, 96, 148), (98, 58, 104),      # 9-11 krop
       (178, 108, 70), (146, 80, 54), (106, 48, 34),        # 12-14 kuif
       (128, 128, 126)]                                     # 15 grijs midden (snavel, poten)
S8 = np.array(Image.open('../s8/hoatzin.png')).astype(int)
G = np.load('../s7/groep.npy', allow_pickle=True)
B = S8.copy()
grijs = lambda x, y: G[y, x] in ('grijs', 'poot') or (x <= 8 and 31 <= y <= 35) or y >= 49
for y in range(64):
    for x in range(64):
        v = S8[y, x]
        if v == 15: B[y, x] = 2                                   # gezicht -> blauw 2
        elif v in (6, 7):
            if grijs(x, y): B[y, x] = 6 if v == 6 else 15
            else: B[y, x] = 5 if v == 6 else 7                    # creme midden vervalt
OOG = [(x, y) for y in range(26, 33) for x in range(3, 13) if S8[y, x] in (8, 15) or (x, y) == (9, 30)]
inside = lambda x, y: 0 <= x < 64 and 0 <= y < 64 and B[y, x] > 0
# 2c/d. sikkels per vorm (op de nieuwe waarden)
C = B.copy()
def afst(x, y, dx, dy, ok, n=4):
    for k in range(1, n + 1):
        xx, yy = x + k * dx, y + k * dy
        if not (0 <= xx < 64 and 0 <= yy < 64) or C[yy, xx] not in ok: return k
    return n + 1
for y in range(64):
    for x in range(64):
        v = C[y, x]
        if v in (5, 7) and not grijs(x, y) and G[y, x] == 'creme':      # nek + staartpunt
            br = min(afst(x, y, 1, 0, (5, 7)), afst(x, y, 0, 1, (5, 7)), afst(x, y, 1, 1, (5, 7)))
            onderkop = y <= 34 and x <= 17 and afst(x, y, 0, -1, (5, 7)) <= 1
            B[y, x] = 7 if (br <= 1 or onderkop) else 5
        elif v == 3 and 27 <= x <= 46 and 30 <= y <= 49:                 # lijf
            br = min(afst(x, y, 1, 0, (2, 3, 4)), afst(x, y, 0, 1, (2, 3, 4)))
            tl = min(afst(x, y, -1, 0, (2, 3, 4)), afst(x, y, 0, -1, (2, 3, 4)))
            B[y, x] = 4 if br <= 2 else 2 if tl <= 3 else 3
        elif v == 3 and 30 <= x <= 48 and 5 <= y <= 24:                  # nabije vleugel: lichte voorrand/bovenrand
            tl = min(afst(x, y, -1, 0, (2, 3, 4)), afst(x, y, 0, -1, (2, 3, 4)), afst(x, y, -1, -1, (2, 3, 4)))
            if tl <= 2: B[y, x] = 2
# 2a. buitenrand zwart (behalve dunne delen en het oog)
D = B.copy()
for y in range(64):
    for x in range(64):
        if D[y, x] in (0, 1, 9, 10, 11) or (x, y) in OOG or y >= 49: continue   # krop: zie hieronder   # poten: s8-omlijning blijft (pootvorm bij Jordi)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            xx, yy = x + dx, y + dy
            if 0 <= xx < 64 and 0 <= yy < 64 and D[yy, xx] != 0: continue
            q1, q2 = (x - dx, y - dy), (x - 2 * dx, y - 2 * dy)
            if all(0 <= a < 64 and 0 <= b < 64 for a, b in (q1, q2)) and D[q1[1], q1[0]] not in (0, 1) and D[q2[1], q2[0]] != 0:
                B[y, x] = 1; break
# krop/buik (Jordi: "buik mag ook de zwarte lijn omheen zachter worden"): geen zwarte lijn maar de donkerste kroptint,
# aan de buitenrand en waar hij tegen lijf/nek ligt
KROP = (9, 10, 11); E = B.copy()
for y in range(37, 50):
    for x in range(18, 36):
        n4 = [E[y + b, x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        if E[y, x] in KROP and 0 in n4: B[y, x] = 11
        elif E[y, x] == 1 and any(v in KROP for v in n4): B[y, x] = 11
        elif E[y, x] == 11 and not any(E[y + b, x + a] in (0, 1) for a in (-1, 0, 1) for b in (-1, 0, 1)):
            B[y, x] = 10      # de rand is nu zelf de donkere sikkel: binnen een tint lichter, anders wordt de buik een blok
# dambord/om-en-om na de zwarte rand: de niet-zwarte pixel rechtsonder van de stap wordt de buurtint
for _ in range(3):
    for y in range(63):
        for x in range(63):
            p, q, r, t = B[y, x], B[y, x + 1], B[y + 1, x], B[y + 1, x + 1]
            if p and q and p == t and q == r and p != q and (x, y) not in OOG:
                if 1 in (p, q): B[y + 1, x + 1] = 1 if p == 1 else B[y + 1, x + 1]; B[y + 1, x] = 1 if q == 1 else B[y + 1, x]
                else: B[y + 1, x + 1] = q
# 3.
B[40, 40] = 3; B[40, 41] = 3
for x, y in OOG: B[y, x] = {15: 2}.get(S8[y, x], S8[y, x])
im = Image.fromarray(B.astype(np.uint8), 'P'); im.putpalette([c for p in PAL for c in p]); im.save('hoatzin.png', transparency=0)
im.convert('RGB').resize((512, 512), Image.NEAREST).save('hoatzin_8x.png')
with open('normal.pal', 'w') as f: f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % p for p in PAL))
print('silhouet anders dan s8:', int(((S8 > 0) != (B > 0)).sum()), '· px anders:', int((S8 != B).sum()))
