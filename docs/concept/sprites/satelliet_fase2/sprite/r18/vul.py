# Vul-toon van het model voor de panelen: per spritepixel de mediaan-helderheid van alleen de vulpixels (geen raster, geen lijn),
# gemiddeld over een venster van 3x3 spritepixels (de rasterlijnen van model en sprite liggen niet op dezelfde plek).
from PIL import Image; import numpy as np
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(float); k = 12.703
LM = .299 * M[..., 0] + .587 * M[..., 1] + .114 * M[..., 2]; SAT = M.max(2) - M.min(2)
V = np.full((64, 64), -1.0)
for y in range(64):
    for x in range(64):
        ya, yb = int(143 + (y - 8) * k), int(143 + (y - 5) * k); xa, xb = int(103 + (x - 1) * k), int(103 + (x + 2) * k)
        ya, xa = max(ya, 0), max(xa, 0); yb, xb = min(yb, 1024), min(xb, 1024)
        if yb <= ya or xb <= xa: continue
        l = LM[ya:yb, xa:xb]; s = SAT[ya:yb, xa:xb]
        m = (l > 38) & (l < 100) & (s > 30)
        if m.sum() > 20: V[y, x] = np.median(l[m])
np.save('vul_L.npy', V)
