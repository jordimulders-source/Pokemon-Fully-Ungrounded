# Puddingvoet van r5 als extra lagen eronder, per laag anders (geen copy-paste-look).
# Per laag: (breedtefactor, hoogtefactor, x-verschuiving, spiegelen, kleurfactor)
import sys
from PIL import Image, ImageOps
import numpy as np
src, out, var = sys.argv[1], sys.argv[2], sys.argv[3]
LAGEN = {
 'a': [(1.06, 1.00, 40, True, 0.92), (1.12, 0.90, -30, False, 0.85)],
 'b': [(1.08, 0.92, -50, True, 0.90), (1.14, 1.05, 35, True, 0.82)],
 'c': [(1.05, 1.08, 25, False, 0.91), (1.13, 0.88, -45, True, 0.84)],
}[var]
DY = [64, 128]
im = Image.open(src).convert('RGBA')
a = np.array(im); a[(a[...,:3].astype(int).sum(2) >= 720)] = (0,0,0,0)
full = Image.fromarray(a)
band = full.crop((0, 672, 1024, 820))
canvas = Image.new('RGBA', (1400, 1300), (0,0,0,0)); ox = 188
for i in (1, 0):
    gw, gh, sx, spiegel, f = LAGEN[i]
    b = ImageOps.mirror(band) if spiegel else band
    b = b.resize((int(1024*gw), int(band.height*gh)), Image.NEAREST)
    d = np.array(b).astype(float); d[..., :3] *= f
    b = Image.fromarray(d.clip(0, 255).astype(np.uint8))
    y = 672 + DY[i] + int(band.height*(1-gh))  # onderkant blijft op dezelfde plek
    canvas.alpha_composite(b, (ox + (1024 - b.width)//2 + sx, y))
canvas.alpha_composite(full, (ox, 0))
c = canvas.crop(canvas.getbbox()); s = max(c.size) + 80
o = Image.new('RGBA', (s, s), (255,255,255,255)); o.alpha_composite(c, ((s-c.width)//2, (s-c.height)//2))
o.convert('RGB').save(out)
