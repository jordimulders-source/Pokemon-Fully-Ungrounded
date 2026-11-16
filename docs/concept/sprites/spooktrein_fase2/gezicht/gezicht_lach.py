# Lachende mond (16 nov): D-vorm (rechte bovenkant, opgetrokken mondhoeken, ronde onderkant) of lachende O
# (O met opkrullende hoeken). Zelfde 3/4-regels als gezicht34.py: linkerhelft = verre kant (x fac), 1 px geest eromheen,
# wagon ervoor. Ogen zwart + donkergroen (k2), 1 rij lager zodat ze dichter op de mondhoeken staan.
import sys
from PIL import Image
src, uit, vorm = sys.argv[1:4]
cx, fac, y0 = 32, 0.7, 14
im = Image.open(src); px = im.load()
for y in range(9, 24):
    for x in range(23, 45):
        if px[x, y] in (1, 5):
            b = [px[xx, y] for xx in list(range(x - 4, x)) + list(range(x + 1, x + 5)) if px[xx, y] in (2, 3, 4)]
            px[x, y] = max(set(b), key=b.count) if b else 2
binnen = {(x, y) for x in range(64) for y in range(30) if px[x, y] in (2, 3, 4)}
mag = {(x, y) for (x, y) in binnen if all((x + d, y) in binnen or px[x + d, y] in range(7, 14) for d in (-1, 1))}
VORMEN = {  # per rij: lijst van (van, tot) t.o.v. cx, ongeschaald
 'D': [[(-9, -7), (7, 9)], [(-9, -4), (4, 9)], [(-9, 9)], [(-9, 9)], [(-9, 9)], [(-9, 9)], [(-9, 9)], [(-9, 9)],
       [(-8, 8)], [(-7, 7)], [(-5, 5)], [(-3, 3)]],
 'O': [[(-4, 4), (-10, -10), (10, 10)], [(-6, 6), (-10, -9), (9, 10)], [(-7, 7), (-9, -8), (8, 9)], [(-8, 8)],
       [(-9, 9)], [(-9, 9)], [(-9, 9)], [(-9, 9)], [(-9, 9)], [(-8, 8)], [(-7, 7)], [(-5, 5)]],
}
sx = lambda d: cx + (round(d * fac) if d < 0 else d)
for i, segs in enumerate(VORMEN[vorm]):
    for a, b in segs:
        for x in range(sx(a), sx(b) + 1):
            if (x, y0 + i) in mag: px[x, y0 + i] = 1
VER = ['.11..', '1551.', '1..51', '1...1'] if 0 else ['..1..', '.151.', '15.51', '1...1']
NABIJ = ['..11..', '.1551.', '15..51', '1....1']
oy = y0 - len(NABIJ)  # 1 rij lager dan voorheen
for ox, oog in ((cx - 7, VER), (cx + 2, NABIJ)):
    for j, r in enumerate(oog):
        for i, c in enumerate(r):
            if c in '15': px[ox + i, oy + j] = int(c)
im.save(uit, transparency=0)
im.convert('RGB').resize((512, 512), Image.NEAREST).save(uit.replace('.png', '_8x.png'))
