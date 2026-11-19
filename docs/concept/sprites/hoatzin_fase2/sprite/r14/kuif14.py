# kuif14.py (r14): verre vleugel achter de kop + kruin + kuifveren opnieuw op het r13-raster (zone x4-30, y0-19).
# - verre vleugel: puntige veertoppen uit het model (toppen 8/3, 13/3, 17/4, 20/7), vlak een stap donkerder:
#   3 met 2 als schaduwkolom rechts per veer, geen 4 meer (geen kam van lichte staafjes).
# - kruin (x8-18, y17-19): vlak 6, licht 7 linksboven, 2 alleen als sikkel rechtsonder naar de nek.
# - veren F1-F6 waaierend vanaf de kruin, hoeken uit het model: F1 linksboven (tip 6,9), F2 omhoog (10,9), F3 steil
#   rechtsboven (16,9), F4 45 graden (tip 23,7), F5 vlak naar rechts (tip 26,12), F6 naar rechts en omlaag tot (29,19).
# Leest ../r13/hoatzin.png, schrijft k14.npy.
import numpy as np; from PIL import Image
a = np.array(Image.open('../r13/hoatzin.png')).astype(int)
L = {y: 32 for y in range(0, 16)}; L.update({16: 31, 17: 31, 18: 31, 19: 31})
for y in range(0, 19):
    for x in range(4, L[y]): a[y, x] = 0
# ---------- verre vleugel ----------
VW = {3: [(8, 8), (13, 13)], 4: [(8, 9), (12, 13), (17, 17)], 5: [(8, 10), (12, 14), (16, 17)],
      6: [(8, 10), (12, 14), (16, 18)], 7: [(8, 18), (20, 20)], 8: [(8, 20)], 9: [(8, 21)], 10: [(8, 22)],
      11: [(8, 22)], 12: [(8, 23)], 13: [(8, 24)], 14: [(8, 24)], 15: [(8, 25)], 16: [(8, 25)],
      17: [(8, 26)], 18: [(8, 26)]}
vw = np.zeros((64, 64), bool)
for y, rs in VW.items():
    for x0, x1 in rs: vw[y, x0:x1+1] = True
vw[19:22] = a[19:22] != 0; vw[19:22, :8] = False; vw[19:22, 28:] = False   # aansluiting op r13 eronder
for y in range(3, 19):
    for x in range(64):
        if vw[y, x]: a[y, x] = 3
# schaduwkolom (2) rechts in elke veer, van de top tot waar de veren samenkomen
for x, y0, y1 in [(9, 4, 4), (10, 5, 6), (13, 3, 4), (14, 5, 6), (17, 4, 5), (18, 6, 7), (20, 7, 8)]:
    for y in range(y0, y1+1): a[y, x] = 2
# ---------- kruin ----------
KR = {16: [(10, 15)], 17: [(9, 17)], 18: [(8, 18)]}
kr = np.zeros((64, 64), bool)
for y, rs in KR.items():
    for x0, x1 in rs: kr[y, x0:x1+1] = True
for y, x in zip(*np.nonzero(kr)):
    a[y, x] = 7 if x + y <= 26 else (2 if x + y >= 34 else 6)
# ---------- veren ----------
VEREN = {
 'F1': ([(9,16),(9,15),(8,14),(8,13),(7,12),(7,11),(6,10)], [(10,15),(9,14),(9,13),(8,12),(8,11)], [(6,9)], (1, 0)),
 'F2': ([(11,16),(11,15),(11,14),(10,13),(10,12),(10,11),(9,10)], [(12,15),(12,14),(11,13),(11,12)], [(9,9)], (1, 0)),
 'F3': ([(13,16),(13,15),(14,14),(15,13),(16,12),(17,11)], [(14,15),(15,14)], [(18,10)], (0, 1)),
 'F4': ([(16,16),(16,15),(17,14),(18,13),(19,12),(20,11),(21,10),(21,9),(22,8)], [(17,15),(18,14),(19,13),(20,12)], [(23,7)], (0, 1)),
 'F5': ([(18,17),(18,16),(19,15),(20,15),(21,14),(22,14),(23,13),(24,13),(25,12)], [(19,16),(20,16),(21,15),(22,15),(23,14)], [(26,12)], (0, 1)),
 'F6': ([(19,18),(20,18),(21,18),(22,17),(23,17),(24,17),(25,17),(26,18),(27,18),(28,19)], [(22,18),(23,18),(24,18),(25,18)], [(29,19)], (0, 1)),
}
veer = np.zeros((64, 64), bool); sch = {}
for nm, (kern, schaduw, tip, s) in VEREN.items():
    for x, y in kern: a[y, x] = 7; veer[y, x] = True; sch[(x, y)] = s
    for x, y in schaduw: a[y, x] = 6; veer[y, x] = True; sch[(x, y)] = s
    for x, y in tip: a[y, x] = 2; veer[y, x] = True; sch[(x, y)] = s
    a[kern[-1][1], kern[-1][0]] = 6
for y, x in zip(*np.nonzero(veer)):
    sx, sy = sch[(x, y)]
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        xx, yy = x+dx, y+dy
        if veer[yy, xx] or kr[yy, xx]: continue
        if a[yy, xx] == 0:
            a[yy, xx] = 1 if (dx > 0 or dy > 0) else 2
        elif vw[yy, xx] and (dx, dy) == (sx, sy) and yy < 19:
            a[yy, xx] = 2
for y, x in zip(*np.nonzero(kr)):
    for dx, dy in ((0,-1),(1,0)):
        xx, yy = x+dx, y+dy
        if not kr[yy, xx] and not veer[yy, xx] and vw[yy, xx]:
            a[yy, xx] = 2
vol = vw | kr | veer
# ---------- buitenlijn: toppen links 2 / rechts 1, linkerrand selout 2, rechterrand zwart ----------
TOP = [(7, 10, 8), (11, 14, 13), (15, 18, 17), (19, 30, 20)]
for y in range(0, 19):
    for x in range(4, 31):
        if a[y, x] != 0 or x >= L[y]: continue
        n = {(dx, dy): bool(vol[y+dy, x+dx]) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))}
        if not any(n.values()): continue
        if n[(1, 0)] and not n[(-1, 0)] and not n[(0, -1)] and x < 12:
            a[y, x] = 2
        elif n[(0, 1)] and not n[(-1, 0)]:
            t = next((m for x0, x1, m in TOP if x0 <= x <= x1), 0)
            a[y, x] = 2 if x <= t and not n[(1, 0)] else 1
        else:
            a[y, x] = 1
# ---------- rij 19: kruin onderrand (7 licht links, 6, sikkel 2 rechts) + F6-top ----------
for x, c in zip(range(6, 17), [2, 7, 6, 6, 6, 6, 6, 2, 2, 2, 2]): a[19, x] = c
a[20, 29] = 1; a[19, 30] = 1 if a[19, 30] == 0 else a[19, 30]
np.save('k14.npy', a)
