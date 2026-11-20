# raster.py png x0 y0 x1 y1 [schaal] -> scratchpad/raster.png met coordinatenraster
import sys
from PIL import Image, ImageDraw
im = Image.open(sys.argv[1]).convert('RGBA'); x0, y0, x1, y1 = map(int, sys.argv[2:6]); s = int(sys.argv[6]) if len(sys.argv) > 6 else 16
c = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * s, (y1 - y0) * s), Image.NEAREST)
V = Image.new('RGB', (c.width + 30, c.height + 20), (255, 255, 255)); V.paste(c, (30, 20), c); d = ImageDraw.Draw(V)
for x in range(x0, x1):
    d.line([(30 + (x - x0) * s, 20), (30 + (x - x0) * s, V.height)], fill=(220, 220, 220) if x % 5 else (255, 0, 0))
    if x % 5 == 0: d.text((32 + (x - x0) * s, 4), str(x), fill=(255, 0, 0))
for y in range(y0, y1):
    d.line([(30, 20 + (y - y0) * s), (V.width, 20 + (y - y0) * s)], fill=(220, 220, 220) if y % 5 else (255, 0, 0))
    if y % 5 == 0: d.text((2, 22 + (y - y0) * s), str(y), fill=(255, 0, 0))
V.save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/c799a334-5afa-5ce2-a1de-fd8513506124/scratchpad/raster.png')
