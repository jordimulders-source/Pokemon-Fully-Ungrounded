# poten.py: poten met de hand op het raster (vorm uit het model, legs.png): schenen 3 tinten (licht links), tenen met
# lichte bovenrij en donkere onderrij, zwarte klauwpunten; verre poot (links) een stap donkerder (E/2), nabije F/E/2.
# Omlijning: 2 aan de lichtkant (boven/links), 1 aan de schaduwkant. Leest kuif.npy, schrijft poten.npy + hoatzin.png
import numpy as np
H = '0123456789ABCDEF'
# r11: stevige poten naar het model (legs.png gemeten): schenen 4 px vulling, tenen 3 rijen, klauwen 2 px zwart.
# Vulling per rij (x0, x1) inclusief; schaduw automatisch: licht waar links/boven buiten de poot, donker rechts/onder.
VER_F = {49:[(25,28)], 50:[(25,28)], 51:[(24,27)], 52:[(24,27)], 53:[(23,26)], 54:[(23,26)],
         55:[(18,26)], 56:[(16,28)], 57:[(16,28)], 58:[(21,24)], 59:[(21,23)], 60:[(22,23)]}
VER_K = [(15,57),(14,58),(15,58),(29,58),(29,59),(22,61),(23,61)]
NAB_F = {49:[(31,34)], 50:[(31,34)], 51:[(31,34)], 52:[(31,34)], 53:[(31,34)], 54:[(31,34)],
         55:[(30,35)], 56:[(28,36)], 57:[(28,37)], 58:[(30,32),(36,37)], 59:[(30,32)], 60:[(30,31)], 61:[(30,31)]}
NAB_K = [(27,57),(27,58),(38,58),(38,59),(30,62),(31,62)]
def masker(F):
    m = np.zeros((64,64), bool)
    for y, rs in F.items():
        for x0, x1 in rs: m[y, x0:x1+1] = True
    return m
a = np.load('kuif.npy'); P = np.load('part.npy')
# oude poten weg (onderdelen poot_v/poot_n en hun ring) in het pootgebied
for y in range(49, 64):
    for x in range(13, 38):
        if y == 49 and not (24 <= x <= 36): continue
        if P[y, x] in (1,):   # staart blijft
            continue
        if y >= 50 or P[y, x] in (5, 6) or a[y, x] in (14, 15):
            a[y, x] = 0
mv, mn = masker(VER_F), masker(NAB_F)
mv &= ~mn
def kleur(m, lt, md, dk):
    for y, x in zip(*np.nonzero(m)):
        uit = lambda yy, xx: not (0 <= yy < 64 and 0 <= xx < 64 and m[yy, xx])
        c = md
        if uit(y, x-1) or uit(y-1, x): c = lt
        if uit(y, x+1) or uit(y+1, x): c = dk if c == md else c
        if uit(y+1, x) and not uit(y-1, x): c = dk
        a[y, x] = c
kleur(mv, 14, 14, 2)         # verre poot: een stap donkerder (geen lichte tint)
kleur(mn, 15, 14, 2)         # nabije poot: 3 grijstinten
alle = mv | mn
for y, x in zip(*np.nonzero(alle)):
    for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy, xx = y+dy, x+dx
        if 0 <= yy < 64 and 0 <= xx < 64 and not alle[yy, xx] and a[yy, xx] == 0:
            a[yy, xx] = 1 if (dx > 0 or dy > 0) else 2
for x, y in VER_K + NAB_K: a[y, x] = 1
for y in range(44, 50):
    for x in range(13, 38):
        if a[y, x] in (14, 15) and not ((x0 := (14 if x < 27 else 27)) <= x and False):
            a[y, x] = 11
np.save('poten.npy', a)
if __name__ == '__main__':
    from PIL import Image; from geom import PAL
    im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(sum(PAL, ()) + (0,)*(768-48)); im.save('hoatzin.png', transparency=0)
