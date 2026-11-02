"""Bouwt variant_jonger2.txt + _1x.png uit de met de hand getypte spans.txt (alleen bouwen; geen vormen)."""
import os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
g = [['.'] * 64 for _ in range(64)]
for line in open(os.path.join(H, 'spans.txt')):
    if line.startswith('#') or not line.strip(): continue
    y, *sp = line.split(); y = int(y)
    for s in sp:
        a, b = map(int, s.split('-'))
        for x in range(a, b + 1): g[y][x] = '#'
open(os.path.join(H, 'variant_jonger2.txt'), 'w').write('\n'.join(''.join(r) for r in g) + '\n')
im = Image.new('P', (64, 64)); im.putpalette([152, 208, 160, 108, 58, 32] + [0] * 762)
im.putdata([1 if g[y][x] == '#' else 0 for y in range(64) for x in range(64)]); im.save(os.path.join(H, 'variant_jonger2_1x.png'), transparency=0)
ys = [y for y in range(64) if '#' in g[y]]
print('px', sum(r.count('#') for r in g), 'hoogte', ys[0], ys[-1], 'kop (tot de kin, y25)', round(100 * (25 - ys[0] + 1) / (ys[-1] - ys[0] + 1)), '%')
