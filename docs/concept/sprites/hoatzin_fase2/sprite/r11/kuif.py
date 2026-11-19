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
# losse plukken (boven, over de verre vleugel), r11 1 px smaller dan r10 (Jordi): punt 7, naar de basis 6
r(7,  23, "7")
r(8,  22, "7")
r(9,   6, "7");   r(9, 21, "7")
r(10,  6, "7");   r(10, 11, "7");   r(10, 16, "7");   r(10, 20, "7")
r(11,  7, "7");   r(11, 10, "7");   r(11, 15, "7");   r(11, 19, "6")
r(12,  7, "6");   r(12, 10, "6");   r(12, 14, "6");   r(12, 18, "6");   r(12, 24, "777")
r(13,  8, "6");   r(13, 10, "6");   r(13, 14, "6");   r(13, 17, "76"); r(13, 21, "777")
# kruin: één massa die op de kop aansluit (geen donkere band eronder), lichte rand links, twee plukgrenzen
r(14,  8, "767662766662766")
r(15,  8, "7666627666626")
r(16,  8, "766627666627677777")
r(17,  8, "76662766627666666677")
r(18,  8, "666666666266")
r(18, 26, "667")
r(19,  8, "6666");  r(19, 15, "6666");  r(19, 28, "6")
r(20,  8, "666")
P = np.load('part.npy')
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
            elif v in (3, 4, 5) and P[yy, xx] == 0 and yy < 16:   # alleen over de verre vleugel: donkere rand
                a[yy, xx] = 2
    # gaten waar de oude r9-kuif zat (niet verbonden met de achtergrond) dichten met de nektint, en
    # de buitenlijn rond zulke gaten weghalen (geen losse zwarte stukjes tussen kuif en kop)
    bg = np.zeros(a.shape, bool); st = [(0, 0)]; bg[0, 0] = True
    while st:
        y, x = st.pop()
        for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy, xx = y+dy, x+dx
            if 0 <= yy < 64 and 0 <= xx < 64 and not bg[yy, xx] and a[yy, xx] == 0: bg[yy, xx] = True; st.append((yy, xx))
    for y in range(6, 22):
        for x in range(15, 28):
            if a[y, x] == 0 and not bg[y, x]: a[y, x] = 3
    for y in range(6, 22):
        for x in range(15, 28):
            if a[y, x] == 1 and not kz[y, x] and not any(bg[y+dy, x+dx] for dy, dx in ((1,0),(-1,0),(0,1),(0,-1))):
                a[y, x] = 3 if y >= 16 else 2
    return a
if __name__ == '__main__':
    from PIL import Image; from geom import PAL
    a = zet(np.load('kop.npy')); np.save('kuif.npy', a)
    im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('hoatzin.png', transparency=0)
