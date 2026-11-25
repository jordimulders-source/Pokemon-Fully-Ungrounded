# Trainer-effect (referenties/corruptie_trainer_red.png): in een paar zones valt de sprite uiteen in
# losse pixels: bestaande pixels vallen weg of verspringen een paar px; dichter naar de buitenrand.
# Alleen bestaande pixels; niets getekend. Gebruik: IN OUT sterkte seed
import sys, random; from PIL import Image; import numpy as np
IN, OUT, st, seed = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4])
rnd = random.Random(seed)
a = np.asarray(Image.open(IN).convert('RGB')).astype(int); H, W, _ = a.shape
fg = a.mean(2) < 235
out = np.full_like(a, 255)
out[fg] = a[fg]
# zones: (x0, x1, y0, y1, richting van de buitenrand) – linkerkant en linksonder, zoals bij de trainer
zones = [(0, 22, 33, 52, 'links'), (14, 30, 12, 30, 'links'), (40, 56, 44, 52, 'onder')]
for x0, x1, y0, y1, r in zones:
    for y in range(y0, y1):
        for x in range(x0, x1):
            if not fg[y, x]: continue
            t = (x1 - x) / (x1 - x0) if r == 'links' else (y - y0) / (y1 - y0)   # 1 = buitenrand
            p = st * t
            u = rnd.random()
            if u < p * 0.55:
                out[y, x] = 255                                   # pixel valt weg
            elif u < p * 0.85:
                nx = x + rnd.choice((-3, -2, -1, 1, 2)); ny = y + rnd.choice((0, 0, 1))
                if 0 <= nx < W and 0 <= ny < H and out[ny, nx].mean() > 235:
                    out[ny, nx] = a[y, x]                          # pixel verspringt naar een lege plek
                out[y, x] = 255
im = Image.fromarray(out.astype('uint8')); im.save(OUT)
