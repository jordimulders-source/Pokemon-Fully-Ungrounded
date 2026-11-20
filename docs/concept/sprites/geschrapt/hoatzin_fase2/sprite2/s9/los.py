# los.py [png]: losse tintpixels = tint (geen lijn) zonder enige 8-buur met dezelfde tint
import sys, numpy as np
from PIL import Image
S = np.array(Image.open(sys.argv[1] if len(sys.argv) > 1 else 'hoatzin.png')).astype(int); r = []
for y in range(64):
    for x in range(64):
        v = S[y, x]
        if v < 2 or v == 14: continue
        if not any(S[y + a, x + b] == v for a in (-1, 0, 1) for b in (-1, 0, 1) if (a or b) and 0 <= y + a < 64 and 0 <= x + b < 64):
            r.append((x, y, int(v)))
print('losse tintpixels', len(r), r)
