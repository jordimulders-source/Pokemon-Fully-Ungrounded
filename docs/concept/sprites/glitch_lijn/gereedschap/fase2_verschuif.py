# Trainer-effect (Jordi, 25 nov): "hij heeft lijnen getrokken van 1 pixel van boven naar beneden en die
# lijnen in zijn geheel bijv iets naar beneden, iets naar boven gezet". Elke kolom van 1 px (hele hoogte)
# schuift als geheel omhoog of omlaag. Gebruik: IN OUT max_verschuiving kans x0 x1 seed
import sys, random; from PIL import Image; import numpy as np
IN, OUT = sys.argv[1], sys.argv[2]
m, kans, x0, x1, seed = int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
rnd = random.Random(seed)
a = np.asarray(Image.open(IN).convert('RGB')); H, W, _ = a.shape
out = np.full_like(a, 255)
for x in range(W):
    d = rnd.randint(-m, m) if x0 <= x < x1 and rnd.random() < kans else 0
    col = a[:, x]
    if d > 0: out[d:, x] = col[:H - d]
    elif d < 0: out[:H + d, x] = col[-d:]
    else: out[:, x] = col
Image.fromarray(out).save(OUT)
