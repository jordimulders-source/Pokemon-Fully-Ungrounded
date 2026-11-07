"""Ronde 1m: vuistarm per pixel met de hand (Claude, 5 nov), basis 1j (vorm = model), naar het model op 64 px.
Jordi: "waarom volg je het model niet?" / "kijk die pixellijn ruimte is prima" / "maar dan moet de hele arm meebuigen en
daardoor iets dikker zijn en niet gewoon een streepje". -> pols geleidelijk (model: 5-6-8 px), arm ±8 px dik over de hele
lengte, 1 px lucht langs de kop (zoals 1k), bovenrand buigt mee de schouder in en sluit aan op de rugomtrek (26,30).
Licht aan de binnenbocht (model), kleurige omlijning (2) aan de lichtkant, zwart (1) aan de schaduwkant."""
import os
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
src = Image.open(os.path.join(H, '../ronde1j/nachtaap_fase3.png')); a = np.array(src); pal = src.getpalette(); oud = a.copy()
# rij: (eerste x, indices)
R = {22: (9, [1, 2, 5, 5, 4, 3, 1]),
     23: (10, [2, 5, 5, 4, 4, 3, 1]),
     24: (10, [2, 5, 5, 4, 4, 4, 3, 1]),
     25: (11, [2, 5, 5, 4, 4, 4, 3, 1]),
     26: (12, [2, 5, 5, 4, 4, 4, 3, 3, 1]),
     27: (14, [0, 2, 5, 4, 4, 4, 3, 3, 1]),
     28: (15, [0, 2, 5, 4, 4, 4, 3, 3, 1]),
     29: (16, [0, 2, 5, 4, 4, 4, 3, 3, 3, 1]),
     30: (17, [0, 2, 5, 4, 4, 4, 3, 3, 3]),       # x26.. = bestaande rugomtrek (2 2 2)
     31: (18, [0, 2, 5, 4, 4, 4, 4, 4]),          # x26.. = bestaand rugvlak
     32: (19, [3, 5, 4, 4])}
def kop(x, y): return y >= 27 and x <= 13 + (y - 27)
GRENS = {22: 25, 23: 25, 24: 25, 25: 25, 26: 25, 27: 25, 28: 25, 29: 25, 30: 25, 31: 22}   # rechts daarvan: rug, blijft
for y in range(22, 32):                       # oude arm wissen (kop, vuist en rug blijven)
    for x in range(9, GRENS[y] + 1):
        if not kop(x, y) and not (y == 22 and x < 9): a[y, x] = 0
for y, (x0, cs) in R.items():
    for i, c in enumerate(cs): a[y, x0 + i] = c
a[21, 13] = 1                                  # bovenkant pols sluit aan op de vuistonderkant
# omlijning op elke trede: armpixel naast lege ruimte -> 2 aan de lichtkant (onder/links), 1 aan de schaduwkant (boven/rechts)
for y in range(21, 33):
    for x in range(9, 27):
        if a[y, x] in (3, 4, 5) and not kop(x, y):
            boven = y > 0 and a[y - 1, x] == 0; rechts = a[y, x + 1] == 0
            onder = a[y + 1, x] == 0; links = a[y, x - 1] == 0
            if boven or rechts: a[y, x] = 1
            elif onder or links: a[y, x] = 2
a[26, 13] = 2                                  # onderrand arm doorlopend tot de spleet
im = Image.fromarray(a, 'P'); im.putpalette(pal); im.save(os.path.join(H, 'nachtaap_fase3.png'), transparency=0)
d = np.argwhere(a != oud); print('gewijzigd t.o.v. 1j:', len(d), 'px in rijen', sorted(set(int(y) for y, x in d)))
op = [(x, y) for y in range(64) for x in range(64) if a[y, x] in (3, 4, 5) and any(
    0 <= y + dy < 64 and 0 <= x + dx < 64 and a[y + dy, x + dx] == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
print('open randen', op)
