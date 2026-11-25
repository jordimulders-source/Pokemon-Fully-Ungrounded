# Toonkaart van het model op het 64-raster: per spritepixel de mediaan-RGB en -helderheid van het binnenste van het modelblok.
from PIL import Image; import numpy as np
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(float); k = 12.703
LM = .299 * M[..., 0] + .587 * M[..., 1] + .114 * M[..., 2]
L = np.full((64, 64), -1.0); C = np.zeros((64, 64, 3))
for y in range(64):
    for x in range(64):
        ya, yb = int(143 + (y - 7) * k) + 2, int(143 + (y - 6) * k) - 2; xa, xb = int(103 + x * k) + 2, int(103 + (x + 1) * k) - 2
        if ya < 0 or yb > 1024 or xb > 1024: continue
        L[y, x] = np.median(LM[ya:yb, xa:xb]); C[y, x] = np.median(M[ya:yb, xa:xb].reshape(-1, 3), 0)
np.save('toon_L.npy', L); np.save('toon_C.npy', C)
