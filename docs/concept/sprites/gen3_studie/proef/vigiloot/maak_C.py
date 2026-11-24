"""Variant C: vachtramp opgetild (Ursaring-afstanden) + lichtzones omgedraaid. Bouwt op na.png (A).
Gerichte pixellijst per rij, geen kwantiseren/blur. Draai vanuit de repo-root."""
from PIL import Image
D = 'docs/concept/sprites/gen3_studie/proef/vigiloot/'
H = '0123456789ABCDEF'
# (y, x_start, tekst): alleen vachtpixels (3/5/6/7) -> 5/6/7
ZONES = {
 'schouder/borst: een lichtzone 7 (glanskern 3 weg)': [
     (21, 18, '777777'), (22, 16, '7777777'), (23, 16, '777777'), (24, 16, '77777'),
     (25, 16, '7777'), (26, 16, '777'), (27, 16, '77')],
 'nabije dij: licht op de bolling bovenaan, grond 6, sikkel 5 onder': [
     (39, 23, '7776'), (40, 22, '777'), (41, 21, '77776'), (42, 20, '7777666'),
     (43, 20, '77766655'), (44, 19, '6666665555'), (45, 18, '6666655555'),
     (46, 17, '666655555'), (47, 17, '6655555'), (48, 16, '6555555')],
 'verre dij: schaduwsikkel 5 smaller, grondtint 6 groter': [
     (36, 37, '66'), (37, 37, '66'), (38, 37, '66'), (39, 38, '6'), (40, 38, '66'),
     (41, 37, '66'), (42, 36, '66'), (43, 35, '66'), (44, 35, '66')],
}
PAL = {4: (58, 46, 40), 5: (110, 92, 78), 6: (146, 126, 106), 7: (180, 160, 134)}
FUR = {3, 5, 6, 7}
im = Image.open(D + 'na.png'); px = im.load(); a = im.copy(); ap = a.load()
for zone, segs in ZONES.items():
    n = 0
    for (y, x0, s) in segs:
        for i, ch in enumerate(s):
            x = x0 + i; new = H.index(ch)
            assert ap[x, y] in FUR and new in FUR, (zone, x, y, ap[x, y])
            n += ap[x, y] != new; px[x, y] = new
    print(f'{n:3d}  {zone} (t.o.v. A)')
p = im.getpalette()
for i, c in PAL.items(): p[3*i:3*i+3] = list(c)
im.putpalette(p); im.save(D + 'na_C.png')
lum = lambda c: round(.299*c[0] + .587*c[1] + .114*c[2])
print('ramp C', [(i, lum(p[3*i:3*i+3])) for i in (4, 5, 6, 7, 3)])
