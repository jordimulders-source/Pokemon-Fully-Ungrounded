# kuif12.py (r12): verre vleugel achter de kop + kruin + 7 losse kuifveren, met de hand op het raster.
# Vorm afgelezen op MODEL.png (modelgrid.py 2 0 34 30 30): lobben van de verre vleugel (toppen 8-9/3, 12-13/3.5,
# 16-17/4.8, 19-20/7.7, daarna schuine rechterrand tot 27/20), kuifveren (bruine strengen) uit de kruin:
# F1 omhoog-links (tip 6,9), F2 omhoog (11,8), F3 (17,9), F4 (tip 23,7 in de lucht), F5 (tip 26,12), F6 (krult naar 28,19),
# F7 laag (26,20). Leest ../r11/hoatzin.png, schrijft kuif12.npy.
import numpy as np; from PIL import Image
from geom import PAL
a = np.array(Image.open('../r11/hoatzin.png')).astype(int)

# ---------- 1. venster leegmaken (x4..30, y0..21), de nabije vleugel blijft ----------
L = {y: 32 for y in range(0, 16)}; L.update({16: 31, 17: 31, 18: 31, 19: 31, 20: 30, 21: 30})
for y in range(0, 22):
    for x in range(4, L[y]):
        a[y, x] = 0

# ---------- 2. verre vleugel: silhouet per rij (x0, x1), afgelezen op het model ----------
VW = {3: [(8, 9), (12, 13)], 4: [(8, 10), (12, 14)], 5: [(8, 10), (12, 14), (16, 17)],
      6: [(8, 10), (12, 14), (16, 18)], 7: [(8, 18)], 8: [(8, 20)], 9: [(8, 21)], 10: [(8, 22)],
      11: [(8, 22)], 12: [(8, 23)], 13: [(8, 24)], 14: [(8, 24)], 15: [(8, 25)], 16: [(8, 25)],
      17: [(8, 26)], 18: [(8, 26)], 19: [(8, 26)], 20: [(8, 27)], 21: [(8, 27)]}
vw = np.zeros((64, 64), bool)
for y, rs in VW.items():
    for x0, x1 in rs: vw[y, x0:x1+1] = True
a[vw] = 3
# per lob: lichte linkerkolom (4) in het bovenste deel, donkere scheiding (2) vanuit de inkeping, taps naar beneden
for x, y0, y1 in [(8, 3, 9), (12, 3, 8), (16, 5, 8), (19, 8, 9), (9, 3, 3), (13, 3, 4), (17, 5, 5)]:
    for y in range(y0, y1+1): a[y, x] = 4
for x, y0, y1 in [(11, 7, 9), (15, 7, 9), (18, 8, 9)]:
    for y in range(y0, y1+1): a[y, x] = 2
# achter de kop (onder de veren) ligt de verre vleugel in de schaduw
for y in range(19, 22):
    for x in range(19, 28):
        if vw[y, x]: a[y, x] = 2 if (x + y) % 7 else 3
# ---------- 3. kruin: ronde donkere massa boven de blauwe vlek ----------
KR = {16: [(10, 15)], 17: [(9, 17)], 18: [(8, 18)], 19: [(7, 10), (16, 18)],
      20: [(7, 9), (17, 18)], 21: [(7, 9)]}
kr = np.zeros((64, 64), bool)
for y, rs in KR.items():
    for x0, x1 in rs: kr[y, x0:x1+1] = True
a[kr] = 6
for (x, y) in [(10,16),(11,16),(9,17),(8,18),(7,19)]:   # licht op de boog linksboven
    a[y, x] = 7
for (x, y) in [(17,18),(18,18),(16,19),(17,19),(18,19),(17,20),(18,20),(15,18),(16,18),(9,21),(17,17)]:   # schaduw rechtsonder
    a[y, x] = 2
# ---------- 4. kuifveren: kern 7, schaduwkant 6, donkere top 2; (kern, schaduw, tip) ----------
VEREN = {
 'F1': ([(9,16),(9,15),(8,14),(8,13),(7,12),(7,11),(6,10)], [(10,15),(9,14),(9,13),(8,12),(8,11)], [(6,9)], (1, 0)),
 'F2': ([(11,15),(11,14),(11,13),(11,12),(10,11),(10,10)], [(12,14),(12,13),(12,12),(11,11)], [(10,9)], (1, 0)),
 'F3': ([(13,15),(13,14),(14,13),(14,12),(15,11),(15,10)], [(14,14),(15,13),(15,12),(16,11)], [(16,9)], (1, 0)),
 'F4': ([(16,16),(16,15),(17,14),(18,13),(19,12),(20,11),(21,10),(21,9),(22,8)], [(17,15),(18,14),(19,13),(20,12)], [(23,7)], (0, 1)),
 'F5': ([(18,17),(18,16),(19,15),(20,15),(21,14),(22,14),(23,13),(24,13),(25,12)], [(19,16),(20,16),(21,15),(22,15),(23,14)], [(26,12)], (0, 1)),
 'F6': ([(19,18),(20,18),(21,18),(22,17),(23,17),(24,17),(25,17),(26,18),(27,18)], [(21,19),(22,18),(23,18),(24,18),(25,18)], [(28,19)], (0, 1)),
}
veer = np.zeros((64, 64), bool); sch = {}
for nm, (kern, schaduw, tip, s) in VEREN.items():
    for x, y in kern: a[y, x] = 7; veer[y, x] = True; sch[(x, y)] = s
    for x, y in schaduw: a[y, x] = 6; veer[y, x] = True; sch[(x, y)] = s
    for x, y in tip: a[y, x] = 2; veer[y, x] = True; sch[(x, y)] = s
    a[kern[-1][1], kern[-1][0]] = 6          # pixel voor de top: overgang naar donker
# omlijning: over de verre vleugel alleen aan de schaduwkant (2); tegen de lucht rondom (1 schaduwkant, 2 lichtkant)
for y, x in zip(*np.nonzero(veer)):
    sx, sy = sch[(x, y)]
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        xx, yy = x+dx, y+dy
        if veer[yy, xx] or kr[yy, xx]: continue
        if a[yy, xx] == 0:
            a[yy, xx] = 1 if (dx > 0 or dy > 0) else 2
        elif vw[yy, xx] and (dx, dy) == (sx, sy):
            a[yy, xx] = 2
# kruinrand tegen de verre vleugel: donkere lijn 2 boven/rechts van de kruin
for y, x in zip(*np.nonzero(kr)):
    for dx, dy in ((0,-1),(1,0)):
        xx, yy = x+dx, y+dy
        if not kr[yy, xx] and not veer[yy, xx] and vw[yy, xx]:
            a[yy, xx] = 2
vol = vw | kr | veer
# ---------- 5. buitenlijn: zwart rechts/onder, selout 2 links, toppen van de lobben links 2 / rechts 1 ----------
LOBMID = [(7, 10, 9), (11, 14, 13), (15, 18, 17)]
for y in range(0, 23):
    for x in range(4, 31):
        if a[y, x] != 0 or x >= L.get(y, 64): continue
        n = {(dx, dy): bool(vol[y+dy, x+dx]) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))}
        if not any(n.values()): continue
        if n[(1, 0)] and not n[(-1, 0)] and not n[(0, -1)] and x < 12:
            a[y, x] = 2
        elif n[(0, 1)] and not n[(-1, 0)]:
            mid = next((m for x0, x1, m in LOBMID if x0 <= x <= x1), 0)
            a[y, x] = 2 if x < mid else 1
        else:
            a[y, x] = 1
np.save('kuif12.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('stap_kuif.png', transparency=0)
