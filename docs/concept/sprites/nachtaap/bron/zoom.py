"""zoom.py png frame x0 y0 x1 y1 out  -> 12x crop met coordinaten"""
import sys, numpy as np
from PIL import Image, ImageDraw
p, f, x0, y0, x1, y1, out = sys.argv[1], int(sys.argv[2]), *map(int, sys.argv[3:7]), sys.argv[7]
im = Image.open(p); a = np.array(im)[f * 64:(f + 1) * 64]; pal = im.getpalette()
Z = 12; W = (x1 - x0) * Z; H = (y1 - y0) * Z
img = Image.new('RGB', (W + 30, H + 20), 'white'); d = ImageDraw.Draw(img)
for y in range(y0, y1):
    for x in range(x0, x1):
        v = a[y, x]; c = (205, 205, 205) if v == 0 else tuple(pal[3 * v:3 * v + 3])
        d.rectangle([30 + (x - x0) * Z, 20 + (y - y0) * Z, 30 + (x - x0 + 1) * Z - 1, 20 + (y - y0 + 1) * Z - 1], fill=c)
        if v == 0 and (x + y) % 2: pass
for x in range(x0, x1):
    if x % 2 == 0: d.text((30 + (x - x0) * Z + 1, 4), str(x), fill='black')
    if x % 4 == 0: d.line([(30 + (x - x0) * Z, 20), (30 + (x - x0) * Z, H + 20)], fill=(150, 150, 255))
for y in range(y0, y1):
    if y % 2 == 0: d.text((2, 20 + (y - y0) * Z + 1), str(y), fill='black')
    if y % 4 == 0: d.line([(30, 20 + (y - y0) * Z), (W + 30, 20 + (y - y0) * Z)], fill=(150, 150, 255))
img.save(out)
