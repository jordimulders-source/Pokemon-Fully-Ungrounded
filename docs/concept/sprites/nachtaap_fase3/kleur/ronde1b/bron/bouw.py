"""raster.txt + nachtaap_fase3.png uit delen.txt; controleert tegen het bevroren silhouet."""
import os, sys
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
SIL = os.path.join(H, '../../../silhouet/ronde1.txt')
TEK = '.KDSVLFfPpBbGMmW'
PAL = [(152,208,160),(28,20,40),(50,48,98),(80,82,150),(114,118,190),(156,162,222),
       (72,56,100),(44,34,64),(214,170,204),(166,122,166),(184,230,255),(104,176,236),
       (40,98,176),(228,221,240),(170,164,198),(252,252,252)]
g = [['.']*64 for _ in range(64)]
for ln in open(os.path.join(H, 'delen.txt')):
    ln = ln.split('#')[0].rstrip()
    if not ln.strip(): continue
    y, x, s = ln.split()
    y, x = int(y), int(x)
    for i, c in enumerate(s):
        assert c in TEK, (y, x, c)
        g[y][x+i] = c
sil = [l.rstrip('\n') for l in open(SIL)]
bad = [(x, y) for y in range(64) for x in range(64) if (g[y][x] != '.') != (sil[y][x] == '#')]
print('alpha-diff', len(bad), bad[:40])
open(os.path.join(R, 'raster.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')
im = Image.new('P', (64, 64)); im.putpalette([v for c in PAL for v in c])
im.putdata([TEK.index(c) for r in g for c in r])
im.save(os.path.join(R, 'nachtaap_fase3.png'), transparency=0)
with open(os.path.join(R, 'normal.pal'), 'w') as f:
    f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join('%d %d %d\r\n' % c for c in PAL))
