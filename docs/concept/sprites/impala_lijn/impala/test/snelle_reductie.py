# Snelle test: haalt de illustratie (r5) een 64x64-sprite? Geen sprite, alleen een leesbaarheidscheck.
from PIL import Image
import numpy as np
src = Image.open("docs/concept/sprites/impala_lijn/impala/gemini/r5/impala_r5.png").convert("RGB")
a = np.asarray(src).astype(int); m = (a.sum(2) < 720)
ys, xs = np.where(m); box = (xs.min(), ys.min(), xs.max()+1, ys.max()+1)
c = src.crop(box); w, h = c.size; s = 62 / max(w, h)
out = []
for name, flt in [("box", Image.BOX), ("lanczos", Image.LANCZOS)]:
    r = c.resize((round(w*s), round(h*s)), flt).quantize(16, dither=Image.NONE).convert("RGB")
    can = Image.new("RGB", (64, 64), "white"); can.paste(r, ((64-r.width)//2, 64-r.height-1))
    out.append(can.resize((512, 512), Image.NEAREST))
v = Image.new("RGB", (1040, 512), "white"); v.paste(out[0], (0, 0)); v.paste(out[1], (528, 0))
v.save("docs/concept/sprites/impala_lijn/impala/test/snelle_reductie.png")
