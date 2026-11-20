# r5 stap 3: lijnen. (a) kleed krijgt een donkere omranding op de wol (vacht grenzend aan kleed -> 3, zoals de zwarte kleedrand
# in het model); (b) wolbogen binnenin: korte lijnen (3) die vanuit elke inkeping de boog volgen, en de bogen van de kap;
# (c) buitenlijn opnieuw: lichtkant (lege buren linksboven) zachte lijn 2, schaduwkant donker 1, niet om en om.
import numpy as np
from PIL import Image
a = np.load('stap2.npy'); r4b = np.array(Image.open('../../r4/lama_b.png')); Z = np.load('zone_vacht.npy')
H, W = a.shape
def g(x, y): return a[y, x] if 0 <= x < W and 0 <= y < H else 0
N4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]; N8 = N4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
KLEED = (9, 10, 11)
# kleed: oude bovenrand die nu binnen ligt (onder de kleedbult) -> kleedrood
for x, y in [(35, 27), (36, 27), (37, 27)]: a[y, x] = 10
# nieuwe wolpixels en oude buitenlijn die nu binnen ligt -> vacht 5/6 (lichtkant boven)
for x, y in [(44, 27), (45, 27)]: a[y, x] = 6
for x, y in [(12, 25)]: a[y, x] = 6
Z = Z.copy()
for x, y in [(44, 26), (45, 26), (44, 27), (45, 27), (12, 25)]: Z[y, x] = True
# (a) kleedrand op de wol
for y in range(26, 44):
    for x in range(24, 46):
        if Z[y, x] and a[y, x] in (4, 5, 6) and any(g(x + dx, y + dy) in KLEED for dx, dy in N4) and y >= 29:
            a[y, x] = 3
# (b) bogen binnenin (handmatig, op de modelplekken; zie NOTITIES)
BOGEN = {
    # kap: drie bollen met ronde onderkant (model: onderrand kap y 12,0-12,5, bollen x 11,5-14 / 14-16,5 / 16,5-19)
    'kap': [(12, 11), (13, 12), (14, 12), (15, 11), (16, 12), (17, 12), (18, 11), (19, 12)],
    # hals achter: vanuit de inkepingen rij 17, 21, 24 een lijn van 2 px schuin naar linksonder (boog van de bol erboven)
    'hals achter': [(22, 17), (21, 18), (22, 21), (21, 22), (22, 24), (21, 25)],
    # hals voor: inkeping rij 26 -> boog naar rechtsonder
    'hals voor': [(14, 26), (15, 27)],
    # rug: inkeping x 42-43 -> boog omlaag naar links; voor de staart (49,28) -> boog
    'rug': [(43, 29), (43, 30), (48, 29)],
    # achterwerk: inkepingen rij 40 en 43-44 -> boog naar linksboven
    'achterwerk': [(46, 40), (45, 39), (46, 43), (45, 43)],
    # buik: inkeping x 29 en x 32 -> boog omhoog
    'buik': [(29, 45), (30, 44), (32, 44), (33, 43)],
    # voorpoot-schouderbol tegen de borst (model-lijn x 17-19, y 41-46; r4b), rond
    'schouder': [(20, 40), (19, 41), (18, 42), (18, 43), (17, 44), (17, 45), (17, 46)],
    # achterbol boven de achterpoot (model: boog x 34-37, y 41-46)
    'achterbol': [(36, 42), (35, 43), (35, 44), (35, 45), (36, 46)],
}
for k, pts in BOGEN.items():
    for x, y in pts:
        assert a[y, x] != 0, (k, x, y)
        a[y, x] = 3
a[11, 13] = 5   # schaduwonderrand van de eerste kapbol (boven de boog)
np.save('stap3a.npy', a)
# (c) buitenlijn voor romp/hals/kop (rij 7-47); poten (r4b) blijven zoals ze zijn
silh = a > 0
def leeg(x, y): return not (0 <= x < W and 0 <= y < H) or not silh[y, x]
b = a.copy(); rand = []
for y in range(7, 48):
    for x in range(W):
        if not silh[y, x] or not any(leeg(x + dx, y + dy) for dx, dy in N4): continue
        v = a[y, x]
        if v in (12, 13, 14, 7, 8): continue
        if v in KLEED or (r4b[y, x] == 1 and any(0 <= y + dy < H and 0 <= x + dx < W and r4b[y + dy, x + dx] in KLEED for dx, dy in N8)) or (x, y) in [(35, 26), (36, 26), (37, 26)]:
            b[y, x] = 1; continue
        if not (Z[y, x] or v in (2, 3, 4, 5, 6) or r4b[y, x] in (1, 2)): continue
        if v in (9, 10, 11): continue
        sx = sy = 0
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if (dx or dy) and leeg(x + dx, y + dy): sx += dx; sy += dy
        n = (sx * sx + sy * sy) ** .5 or 1
        b[y, x] = 2 if (sx + sy) / n < -0.35 else 1
        rand.append((x, y))
R = set(rand)
for _ in range(2):
    c = b.copy()
    for x, y in rand:
        nb = [b[y + dy, x + dx] for dx, dy in N8 if (x + dx, y + dy) in R]
        if b[y, x] == 2 and nb.count(2) == 0: c[y, x] = 1
        elif b[y, x] == 1 and nb.count(2) >= 2: c[y, x] = 2
    b = c
a = b
np.save('stap3.npy', a); np.save('zone_vacht3.npy', Z)
print('ok')
