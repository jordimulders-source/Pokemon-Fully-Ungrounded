"""diff_r2.py: bewijs dat r4 alleen tint wijzigt t.o.v. kleur_r2: alpha-diff, ogen-diff, aantal pixels met andere index,
en van welke index naar welke. Ook: lijnpixels (index 1-4 in r2) die van index wisselden."""
import os
from collections import Counter
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
a = Image.open(os.path.join(H, '..', 'kleur_r2', 'poesrups.png')); b = Image.open(os.path.join(H, 'poesrups.png'))
assert a.mode == b.mode == 'P' and a.size == b.size == (64, 64)
P = [(x, y) for y in range(64) for x in range(64)]
alpha = [p for p in P if (a.getpixel(p) == 0) != (b.getpixel(p) == 0)]
OGEN = [(10, 55), (10, 56), (16, 55), (17, 55), (16, 56), (17, 56)]
ogen = [p for p in OGEN if a.getpixel(p) != b.getpixel(p)]
d = [p for p in P if a.getpixel(p) != b.getpixel(p)]
print('alpha-diff met kleur_r2:', len(alpha), alpha)
print('ogen-diff (6 px: nabij 2x2 + glans, ver 1x2):', len(ogen), ogen)
print('pixels met een andere index:', len(d), 'van', sum(a.getpixel(p) != 0 for p in P))
C = Counter((a.getpixel(p), b.getpixel(p)) for p in d)
CH = '.123456789ABCDEF'
for (u, v), n in sorted(C.items()): print(f'   {CH[u]} -> {CH[v]}: {n}')
lijn = [p for p in d if a.getpixel(p) in (1, 2, 3, 4)]
print('buitenlijn/donkere lijn (index 1-4 in r2) van index gewisseld:', len(lijn), lijn)
pa, pb = a.getpalette()[:48], b.getpalette()[:48]
print('paletwijzigingen (index: r2 -> r4):')
for i in range(16):
    if pa[i*3:i*3+3] != pb[i*3:i*3+3]: print(f'   {CH[i]}: {tuple(pa[i*3:i*3+3])} -> {tuple(pb[i*3:i*3+3])}')
