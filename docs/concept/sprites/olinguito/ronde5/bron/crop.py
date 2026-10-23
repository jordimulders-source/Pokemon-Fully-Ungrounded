"""crop.py in.png uit.png x0 y0 x1 y1 zoom [frame]: uitsnede vergroot met raster + 1x/2x/3x van het hele frame."""
import sys
import numpy as np
from PIL import Image, ImageDraw
src, dst = sys.argv[1], sys.argv[2]
x0, y0, x1, y1, z = map(int, sys.argv[3:8])
k = int(sys.argv[8]) if len(sys.argv) > 8 else 0
im = Image.open(src); a = np.array(im)[64 * k:64 * k + 64]; p = im.getpalette()
rgb = np.array(p[:48]).reshape(16, 3)
img = np.zeros((64, 64, 3), np.uint8); img[:] = (238, 238, 238)
img[a > 0] = rgb[a[a > 0]]
c = Image.fromarray(img[y0:y1, x0:x1]).resize(((x1 - x0) * z, (y1 - y0) * z), Image.NEAREST)
W = c.width + 64 * 6 + 40
sh = Image.new('RGB', (W, max(c.height, 200)), (200, 200, 200)); sh.paste(c, (0, 0))
d = ImageDraw.Draw(sh)
for x in range(x0, x1 + 1):
    d.line([((x - x0) * z, 0), ((x - x0) * z, c.height)], fill=(170, 170, 170) if x % 5 else (90, 90, 200))
for y in range(y0, y1 + 1):
    d.line([(0, (y - y0) * z), (c.width, (y - y0) * z)], fill=(170, 170, 170) if y % 5 else (90, 90, 200))
full = Image.fromarray(img)
sh.paste(full, (c.width + 8, 0))
sh.paste(full.resize((128, 128), Image.NEAREST), (c.width + 80, 0))
sh.paste(full.resize((192, 192), Image.NEAREST), (c.width + 216, 0))
sh.save(dst)
