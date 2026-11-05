"""Nachtaap fase 3, stap 2: bron voor het silhouet = het goedgekeurde 2D-model (../model2d/model.png; Jordi 5 nov:
"Maak een silhouet en dan gaan we een sprite bouwen"). Schrijft model50.txt (50%-dekking op 64), dekking.npy/.txt.
Maan en rugpatroon volgen in de sprite (Jordi), niet in het silhouet."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
FILL = float(sys.argv[1]) if len(sys.argv) > 1 else 0.97
im = Image.open(os.path.join(HERE, '../model2d/model.png')).convert('RGBA')
a = np.asarray(im)[..., 3].astype(float) / 255
ys, xs = np.nonzero(a > 0.5)
x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
side = max(x1 - x0, y1 - y0) / FILL
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
k = 16  # 64*16 = 1024 subsamples per as
box = (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2)
A = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((64 * k, 64 * k), Image.BILINEAR, box=box)).astype(float) / 255
cov = A.reshape(64, k, 64, k).mean((1, 3))
# onderaan uitlijnen (sprite staat/zweeft op de onderrand van het vak, Gen 3): schuif omlaag zodat de onderste rij 63 is
rows = np.nonzero((cov >= 0.5).any(1))[0]; sh = 63 - rows.max()
cov = np.roll(cov, sh, axis=0); cov[:sh] = 0
np.save(os.path.join(HERE, 'dekking.npy'), cov)
M = cov >= 0.5
open(os.path.join(HERE, 'model50.txt'), 'w').write('\n'.join(''.join('#' if v else '.' for v in r) for r in M) + '\n')
open(os.path.join(HERE, 'dekking.txt'), 'w').write('\n'.join(''.join('#' if v > 0.95 else ('.' if v < 0.05 else str(int(v * 10))) for v in r) for r in cov) + '\n')
# onderlaag op 256 in hetzelfde vak (voor vel en maker)
rgb = im.resize((256, 256), Image.LANCZOS, box=box)
rgb = Image.fromarray(np.roll(np.asarray(rgb), sh * 4, axis=0)); rgb.save(os.path.join(HERE, 'onderlaag_256.png'))
ys, xs = np.nonzero(M)
print('px', int(M.sum()), 'box', xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, 'x', xs.min(), xs.max(), 'y', ys.min(), ys.max())
