# Reparaties per zone op stap1 (opgeschoonde reductie) -> lama.png + telling per zone t.o.v. onderlaag.png
# Elke reparatie staat hier als (rij, x_start, 'tekens'); '.' = transparant, '_' = laten staan.
# Tekens: 1-9, a-e = paletindex (zie reduceer.PAL).
import os, sys; import numpy as np; from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__)); R1D = os.path.dirname(HIER); sys.path.insert(0, HIER)
from reduceer import save
a = np.asarray(Image.open(os.path.join(R1D, 'stap1.png'))).astype(int).copy()
o = np.asarray(Image.open(os.path.join(R1D, 'onderlaag.png'))).astype(int)
zone = np.full(a.shape, '', object)
def zet(naam, regels, wis=None):
    if wis:  # (y0, y1, x0, x1) eerst leegmaken
        y0, y1, x0, x1 = wis; a[y0:y1 + 1, x0:x1 + 1] = 0; zone[y0:y1 + 1, x0:x1 + 1] = naam
    for y, x, s in regels:
        for k, ch in enumerate(s):
            if ch == '_': continue
            a[y, x + k] = 0 if ch == '.' else int(ch, 16); zone[y, x + k] = naam
exec(open(os.path.join(HIER, 'zones.py')).read())
save(a, os.path.join(R1D, 'lama.png'))
d = a != o
print('lama.png: px', (a > 0).sum(), 'kleuren', len(set(a.ravel())) - 1, 'afwijkend van onderlaag totaal', d.sum())
for naam in sorted(set(zone[d]) - {''}): print('  zone %-12s %3d px' % (naam, (d & (zone == naam)).sum()))
print('  opschoonregels (stap1) %3d px' % (d & (zone == '')).sum())
ys, xs = np.nonzero(a); print('box', xs.max() - xs.min() + 1, 'x', ys.max() - ys.min() + 1, 'rijen', ys.min(), '-', ys.max())
