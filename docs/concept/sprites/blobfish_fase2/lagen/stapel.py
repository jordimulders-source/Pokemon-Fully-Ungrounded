import sys
from PIL import Image
import numpy as np
src, n, dy, grow, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
dark = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0  # kleurfactor per laag (lager = donkerder)
im = Image.open(src).convert('RGBA')
a = np.array(im); a[(a[...,:3].astype(int).sum(2) >= 720)] = (0,0,0,0)
full = Image.fromarray(a)
band = full.crop((0, 672, 1024, 820))           # gesmolten laag (puddingvoet)
canvas = Image.new('RGBA', (1024, 1024 + n*dy), (0,0,0,0))
for i in range(n, 0, -1):                       # onderste laag eerst
    b = band
    if grow != 1:
        w = int(1024 * grow**i); b = band.resize((w, band.height), Image.NEAREST)
    if dark != 1:
        d = np.array(b).astype(float); f = dark**i
        d[..., :3] *= f
        b = Image.fromarray(d.clip(0, 255).astype(np.uint8))
    canvas.alpha_composite(b, ((1024 - b.width)//2 + 0, 672 + i*dy))
canvas.alpha_composite(full, (0, 0))
bb = canvas.getbbox(); c = canvas.crop(bb)
s = max(c.size) + 80; o = Image.new('RGBA', (s, s), (255,255,255,255))
o.alpha_composite(c, ((s-c.width)//2, (s-c.height)//2)); o.convert('RGB').save(out)
