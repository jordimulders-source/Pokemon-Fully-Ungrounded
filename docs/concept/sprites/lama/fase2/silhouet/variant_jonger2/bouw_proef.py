"""Bouwt proef_lama.png uit proef.txt (met de hand getypt) en controleert: past op variant_jonger2.txt, open randen, kleuren."""
import os, sys
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
LET = '.kdsblhqrmnytpuw'
PAL = [(152,208,160),(42,22,26),(108,58,32),(168,104,58),(214,154,82),(239,194,122),(248,226,168),(242,112,94),
       (216,52,60),(152,32,58),(74,60,64),(248,192,48),(32,172,168),(222,48,132),(76,92,168),(250,246,236)]
g = [['.'] * 64 for _ in range(64)]
for ln, l in enumerate(open(os.path.join(H, 'proef.txt')), 1):
    if l.startswith('#') or not l.strip(): continue
    y, x0, s = l.split(); y, x0 = int(y), int(x0)
    for i, c in enumerate(s):
        if g[y][x0 + i] != '.': sys.exit(f'regel {ln}: dubbel {x0+i},{y}')
        g[y][x0 + i] = c
sil = [l.rstrip('\n') for l in open(os.path.join(H, 'variant_jonger2.txt'))]
miss = [(x, y) for y in range(64) for x in range(64) if (sil[y][x] == '#') != (g[y][x] != '.')]
def at(x, y): return g[y][x] if 0 <= x < 64 and 0 <= y < 64 else '.'
op = [(x, y, g[y][x]) for y in range(64) for x in range(64) if g[y][x] not in '.kdmn'
      and any(at(x + a, y + b) == '.' for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
im = Image.new('P', (64, 64)); im.putpalette([v for c in PAL for v in c])
im.putdata([LET.index(g[y][x]) for y in range(64) for x in range(64)]); im.save(os.path.join(H, 'proef_lama.png'), transparency=0)
print('alpha-diff', len(miss), miss[:40]); print('open randen', len(op), op); print('kleuren', len({c for r in g for c in r}))
