# nek12.py (r12): nek als eigen vorm, lichter dan de vleugel: lichte voorkant 5, vlak 4, sikkel 3 rechts,
# binnenlijn 2 waar de vleugel over de nek valt; nekschaduw onder de kuif; een paar korte donkere strepen (3)
# langs de nekcurve (schuin rechtsomlaag, zoals in het model; de vleugellijnen lopen linksomlaag en zijn 2).
# Plus: 1 px donkere rand (2) waar de vleugel over de buik valt. Leest kop12.npy, schrijft nek12.npy.
import numpy as np; from PIL import Image
from geom import PAL
a = np.load('kop12.npy'); P = np.load('part.npy')
BUIK = (11, 12, 13)
Lw = {}
for y in range(64):
    xs = [x for x in range(64) if P[y, x] == 4]
    Lw[y] = min(xs) if xs else 64
nek = np.zeros((64, 64), bool)
for y in range(21, 38):
    for x in range(11, Lw[y]):
        if P[y, x] == 2 and a[y, x] in (2, 3, 4, 5) and x >= 16 - (y < 26) * 0:
            nek[y, x] = True
# voorrand: eerste pixel na de buitenlijn/selout links laten staan
for y in range(21, 38):
    xs = [x for x in range(11, 40) if nek[y, x]]
    if not xs: continue
    x0 = xs[0]
    if y >= 27: nek[y, x0] = False          # selout aan de voorkant blijft
for y, x in zip(*np.nonzero(nek)):
    xs = [xx for xx in range(11, 40) if nek[y, xx]]
    dfr = x - xs[0]; dbk = Lw[y] - x
    if dbk == 1: c = 2
    elif dbk <= 3: c = 3
    elif dfr <= 1 and y >= 27: c = 5
    else: c = 4
    a[y, x] = c
# nekschaduw onder de kuif en de achterkant van de kop (rijen 21-25)
for y in range(21, 26):
    for x in range(17, Lw[y]):
        if nek[y, x]:
            g = y + (x - 17) * 0.3            # schaduwgrens loopt schuin: achter de kop lager, naar de vleugel hoger
            if g < 23.6: a[y, x] = 2
            elif g < 25.2: a[y, x] = 3
# F7: lage kuifstreng in de nekschaduw (bruin 6, dof), uit het model (16,20.5)->(26,20.5)
for x, y in [(19,20),(20,20),(21,20),(22,21),(23,21)]:
    a[y, x] = 6
# korte nekstrepen langs de curve (3), weinig
for x, y in [(18,26),(19,27),(19,28), (21,28),(22,29),(22,30), (19,31),(20,32), (22,33),(23,34)]:
    if nek[y, x]: a[y, x] = 3
# vleugel over de buik: donkere rand
for y in range(36, 44):
    for x in range(20, 32):
        if a[y, x] in (3, 4, 5) and a[y, x-1] in BUIK and P[y, x] == 4:
            a[y, x] = 2
np.save('nek12.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('stap_nek.png', transparency=0)
