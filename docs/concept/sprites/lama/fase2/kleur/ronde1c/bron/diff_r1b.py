"""Diff ronde 1c t.o.v. ronde 1b: per keurderpunt, en 0 buiten de zones (bewijs)."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
a = Image.open(os.path.join(OUT, '../ronde1b/lama.png')); b = Image.open(os.path.join(OUT, 'lama.png'))
ch = [(x, y) for y in range(64) for x in range(64) if a.getpixel((x, y)) != b.getpixel((x, y))]
Z = [('1 halsband', 19, 31, 25, 31), ('2 aguayo', 37, 48, 25, 32), ('5 verre poten', 30, 44, 43, 58), ('3 nagels', 20, 31, 55, 62),
     ('4 buiklijn', 22, 50, 38, 40), ('6 spikkels', 36, 40, 36, 36)]
cnt = {}
for x, y in ch:
    z = next((n for n, x0, x1, y0, y1 in Z if x0 <= x <= x1 and y0 <= y <= y1), None)
    cnt[z] = cnt.get(z, 0) + 1
print('gewijzigd per punt:', {k: v for k, v in sorted(cnt.items(), key=str) if k}, '| totaal', len(ch), '| buiten de zones:', cnt.get(None, 0))
