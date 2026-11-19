# kuif.py: kuif met de hand op het raster. Plukken en kruin afgelezen op het model (kopm.png, 30x):
# K1 omhoog-links (punt 6,9), K2 omhoog (11,10), K3 omhoog-rechts (16,10), K4 naar het twijgje (23,7),
# K5 naar (26,12), K6 hangend naar achteren (29,19). Per pluk lichtkant 7 / midden 6 / schaduwkant 2;
# de kruin onderaan als één massa met de plukgrenzen als donkere lijnen. Omlijning automatisch:
# tegen de achtergrond 1 (schaduwkant) of 2 (lichtkant), over verre vleugel/nek een donkere rand 2.
import numpy as np
F = {}
def r(y, x0, s):
    for i, c in enumerate(s):
        if c != '.': F[(x0+i, y)] = int(c)
#            x
# losse plukken (boven, over de verre vleugel): lichtkant 7, midden 6
r(7,  23, "7")
r(8,  22, "76")
r(9,   6, "7");   r(9, 21, "76")
r(10,  6, "76");  r(10, 11, "7");   r(10, 16, "7");   r(10, 20, "76")
r(11,  7, "76");  r(11, 10, "76");  r(11, 15, "76");  r(11, 19, "76")
r(12,  7, "76");  r(12, 10, "76");  r(12, 14, "76");  r(12, 18, "76");  r(12, 24, "777")
r(13,  8, "7276"); r(13, 14, "76"); r(13, 17, "762"); r(13, 21, "777666")
# kruin: één massa, lichte rand links, twee plukgrenzen (lijn A en C) die naar rechtsboven lopen, sikkel onderaan
r(14,  8, "767662766662766622")
r(15,  8, "7666627666626222")
r(16,  8, "766627666627677777")
r(17,  8, "76662766627666666677")
r(18,  8, "666666666262222222667")
r(19,  8, "6622");  r(19, 15, "2222");  r(19, 28, "66")
r(20,  8, "222")
def zet(a, part=None):
    kz = np.zeros(a.shape, bool)
    for (x, y), c in F.items(): a[y, x] = c; kz[y, x] = True
    # omlijning
    for (x, y) in list(F):
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            xx, yy = x+dx, y+dy
            if kz[yy, xx]: continue
            v = a[yy, xx]
            if v == 0:
                a[yy, xx] = 1 if (dx > 0 or dy > 0) else 2
            elif v in (3, 4, 5):          # verre vleugel / nek: donkere rand rond de haardos
                a[yy, xx] = 2
    return a
if __name__ == '__main__':
    from PIL import Image; from geom import PAL
    a = zet(np.load('kop.npy')); np.save('kuif.npy', a)
    im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('hoatzin.png', transparency=0)
