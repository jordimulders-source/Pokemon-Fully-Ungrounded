# zoom.py bestand x0 x1 y0 y1 uit.png : uitsnede op 16x met raster en coordinaten
import sys, numpy as np
from PIL import Image, ImageDraw
f, x0, x1, y0, y1, uit = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
im = Image.open(f).convert('RGBA'); a = np.array(im); a[np.array(Image.open(f)) == 0] = (255, 255, 255, 255)
Z = 16; c = Image.fromarray(a[y0:y1, x0:x1, :3]).resize(((x1 - x0) * Z, (y1 - y0) * Z), Image.NEAREST)
v = Image.new('RGB', (c.width + 24, c.height + 24), 'white'); v.paste(c, (24, 24)); d = ImageDraw.Draw(v)
for x in range(x0, x1):
    d.line([(24 + (x - x0) * Z, 24), (24 + (x - x0) * Z, v.height)], fill=(200, 200, 200) if x % 5 else (255, 0, 0))
    if x % 2 == 0: d.text((24 + (x - x0) * Z + 2, 6), str(x), fill='black')
for y in range(y0, y1):
    d.line([(24, 24 + (y - y0) * Z), (v.width, 24 + (y - y0) * Z)], fill=(200, 200, 200) if y % 5 else (255, 0, 0))
    d.text((2, 24 + (y - y0) * Z + 3), str(y), fill='black')
v.save(uit)
