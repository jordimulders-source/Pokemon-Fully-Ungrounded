# r5: stap 1-4 achter elkaar, dan lama.png + normal.pal, en controles
import subprocess, numpy as np
for s in ['stap1_vacht.py', 'stap2_bogen.py', 'stap3_lijnen.py', 'stap4_kleding.py']: subprocess.run(['python3', s], check=True)
from PIL import Image
from toon import png
from palet import PAL
a = np.load('stap4.npy'); r4b = np.array(Image.open('../../r4/lama_b.png'))
png(a, PAL, '../lama.png')
open('../normal.pal', 'w').write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in PAL))
d = (a > 0) != (r4b > 0)
def zone(x, y):
    if y < 20: return 'kop/kuif'
    if y < 36 and x < 27: return 'hals'
    if y <= 27 or (y < 36 and x >= 27 and y < 30): return 'rug'
    if x >= 46 and y < 48: return 'achterwerk'
    if y < 50: return 'buik/lijf'
    return 'poten'
Z = {}
for y, x in zip(*np.nonzero(d)): Z.setdefault(zone(x, y), []).append((x, y, '+' if a[y, x] else '-'))
for k, v in Z.items(): print('alfa-diff', k, len(v), v)
print('alfa-diff totaal', int(d.sum()), '| kleur anders dan r4b', int((a != r4b).sum()), '| kleuren', len(np.unique(a[a > 0])))
ys, xs = np.nonzero(a); print('box %dx%d, %d px' % (xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, (a > 0).sum()))
