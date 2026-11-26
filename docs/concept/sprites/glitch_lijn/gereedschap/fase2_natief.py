# Natief raster van een Gemini-beeld (1024 px) terughalen: pitch en fase per as fitten, mediaan per cel.
import sys; from PIL import Image; import numpy as np
IN, OUT = sys.argv[1], sys.argv[2]
PMIN, PMAX = (float(sys.argv[3]), float(sys.argv[4])) if len(sys.argv) > 4 else (14.5, 17.5)   # fase 3 r1: 10 11
a = np.asarray(Image.open(IN).convert('RGB')).astype(int)
def fit(g):
    best = None
    for p in np.arange(PMIN, PMAX, 0.01):
        for ph in np.arange(0, p, 0.5):
            idx = np.round(np.arange(ph, len(g), p)).astype(int); idx = idx[idx < len(g)]
            s = g[idx].mean()
            if best is None or s > best[0]: best = (s, p, ph)
    return best
gx = np.abs(np.diff(a, axis=1)).sum(axis=2).sum(axis=0).astype(float)
gy = np.abs(np.diff(a, axis=0)).sum(axis=2).sum(axis=1).astype(float)
_, px, phx = fit(gx); _, py, phy = fit(gy); print('pitch', px, phx, py, phy)
xs = np.arange(phx + 1 + px/2, 1024, px); ys = np.arange(phy + 1 + py/2, 1024, py)
out = np.zeros((len(ys), len(xs), 3), 'uint8')
for j, y in enumerate(ys):
    for i, x in enumerate(xs):
        r = max(1, int(min(px, py) / 5)); c = a[int(y-r):int(y+r+1), int(x-r):int(x+r+1)].reshape(-1, 3)
        out[j, i] = np.median(c, axis=0)
Image.fromarray(out).save(OUT); print(out.shape)
