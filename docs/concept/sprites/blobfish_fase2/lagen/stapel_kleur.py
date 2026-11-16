# Rechtsonder (+2 lagen, telkens 6% breder, gecentreerd); elke laag een andere kleur (tint vervangen), donkerder.
# Gebruik: stapel_kleur.py r5.png uit.png "tint1,verz1,helder1" "tint2,verz2,helder2"   (tint 0-360)
import sys, colorsys
from PIL import Image
import numpy as np
src, out = sys.argv[1], sys.argv[2]
kleuren = [tuple(map(float, k.split(','))) for k in sys.argv[3:5]]
a = np.array(Image.open(src).convert('RGBA'))
a[(a[...,:3].astype(int).sum(2) >= 720)] = (0,0,0,0)
full = Image.fromarray(a); band = np.array(full.crop((0, 672, 1024, 820)))
def kleur(b, tint, verz, helder):
    rgb = b[..., :3] / 255.0; o = b.copy()
    h, s, v = np.vectorize(colorsys.rgb_to_hsv)(rgb[...,0], rgb[...,1], rgb[...,2])
    lijn = v < 0.25                                   # zwarte lijn blijft
    s2 = np.clip(s * verz + 0.15, 0, 1); v2 = v * helder
    r, g, bb = np.vectorize(colorsys.hsv_to_rgb)(np.full_like(h, tint/360), s2, v2)
    nieuw = (np.dstack([r, g, bb]) * 255).astype(np.uint8)
    o[..., :3] = np.where(lijn[..., None], b[..., :3], nieuw)
    return Image.fromarray(o)
canvas = Image.new('RGBA', (1024, 1024 + 128), (0,0,0,0))
for i in (2, 1):
    b = kleur(band, *kleuren[i-1]); w = int(1024 * 1.06**i)
    b = b.resize((w, b.height), Image.NEAREST)
    canvas.alpha_composite(b, ((1024 - w)//2, 672 + i*64))
canvas.alpha_composite(full, (0, 0))
c = canvas.crop(canvas.getbbox()); s = max(c.size) + 80
o = Image.new('RGBA', (s, s), (255,255,255,255)); o.alpha_composite(c, ((s-c.width)//2, (s-c.height)//2))
o.convert('RGB').save(out)
