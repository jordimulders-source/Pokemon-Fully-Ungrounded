"""Silhouet af = silhouet2 variant B (k 0,18) + bliksem-noot met de hand dikker (zone x 19..30, y 19..32)."""
import sys
from PIL import Image
import numpy as np
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src); a = np.array(im); voor = a.copy()
Z = [
"   ##       ",  # 19
"  #####     ",
"  ######    ",
"  ######    ",
" ######     ",
" ######     ",
" #########  ",  # 25 zigzag-stap
" #########  ",
" #########  ",
" ###  ####  ",
"       ###  ",  # 29 punt naar de spits
"       ###  ",
"       ###  ",
"       ###  ",  # 32
]
for i, r in enumerate(Z):
    for j, c in enumerate(r):
        a[19 + i, 19 + j] = 1 if c == '#' else 0
d = np.argwhere(a != voor)
print('gewijzigd', len(d), 'px; buiten zone', sum(1 for y, x in d if not (19 <= y <= 32 and 19 <= x <= 30)))
o = Image.fromarray(a, 'P'); o.putpalette(im.getpalette()); o.save(dst, transparency=0)
