# Trainer-effect (Jordi, 25 nov): "hij heeft lijnen getrokken van 1 pixel van boven naar beneden en die
# lijnen in zijn geheel bijv iets naar beneden, iets naar boven gezet". Elke kolom van 1 px (hele hoogte)
# schuift als geheel omhoog of omlaag. Jordi: "of juist iets naar rechts of links": met as 'rij' schuiven
# rijen van 1 px (hele breedte) naar links/rechts. Gebruik: IN OUT max kans van tot seed [kolom|rij]
import sys, random; from PIL import Image; import numpy as np
IN, OUT = sys.argv[1], sys.argv[2]
m, kans, x0, x1, seed = int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
rnd = random.Random(seed)
rij = len(sys.argv) > 8 and sys.argv[8] == 'rij'
a = np.asarray(Image.open(IN).convert('RGB'))
if rij: a = a.transpose(1, 0, 2)
H, W, _ = a.shape
out = np.full_like(a, 255)
for x in range(W):
    d = rnd.randint(-m, m) if x0 <= x < x1 and rnd.random() < kans else 0
    col = a[:, x]
    if d > 0: out[d:, x] = col[:H - d]
    elif d < 0: out[:H + d, x] = col[-d:]
    else: out[:, x] = col
if rij: out = out.transpose(1, 0, 2)
Image.fromarray(np.ascontiguousarray(out)).save(OUT)
