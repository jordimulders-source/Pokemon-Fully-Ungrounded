"""Zoom 8x met raster en coordinaten (alleen kijken). Arg: optioneel bestand (standaard ../lama.png) en uitvoer."""
import os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '../lama.png')
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'zoom.png')
x0, y0, x1, y1 = [int(v) for v in sys.argv[3:7]] if len(sys.argv) > 6 else (0, 0, 64, 64)
S = 12
im = Image.open(src).convert('RGBA').crop((x0, y0, x1, y1))
W, H = im.size
bg = Image.new('RGBA', (W * S + 24, H * S + 16), (236, 236, 236, 255))
big = im.resize((W * S, H * S), Image.NEAREST)
bg.paste(big, (24, 16), big)
d = ImageDraw.Draw(bg)
for x in range(W + 1):
    c = (0, 0, 255, 90) if (x0 + x) % 5 == 0 else (0, 0, 0, 25)
    d.line([(24 + x * S, 16), (24 + x * S, 16 + H * S)], fill=c)
    if (x0 + x) % 5 == 0 and x < W: d.text((24 + x * S, 2), str(x0 + x), fill=(200, 0, 0, 255))
for y in range(H + 1):
    c = (0, 0, 255, 90) if (y0 + y) % 5 == 0 else (0, 0, 0, 25)
    d.line([(24, 16 + y * S), (24 + W * S, 16 + y * S)], fill=c)
    if (y0 + y) % 5 == 0 and y < H: d.text((2, 16 + y * S), str(y0 + y), fill=(200, 0, 0, 255))
bg.save(out)
