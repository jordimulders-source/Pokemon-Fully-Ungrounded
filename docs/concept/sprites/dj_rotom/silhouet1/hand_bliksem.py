"""Handreparatie zone bliksem/spits: x 20..34, y 18..36 (rest = verkleinde bron)."""
import sys
from PIL import Image
import numpy as np
p = sys.argv[1]
im = Image.open(p); a = np.array(im)
Z = [  # x 20..34
"     ##        ",  # 18
"    #####      ",
"    ######     ",
"    ######     ",
"   ######      ",
"   ######      ",
"   #########   ",  # 24 zigzag-stap naar rechts
"   #########   ",
"   #########   ",
"   #########   ",
"   ###   ###   ",  # 28
"         ###   ",
"         ###   ",
"         ##    ",
"         ##    ",
"         ###   ",  # 33 spits
"        ####   ",
"        #####  ",
"        #####  ",  # 36
]
voor = a.copy()
for i, r in enumerate(Z):
    for j, c in enumerate(r):
        a[18 + i, 20 + j] = 1 if c == '#' else 0
print('gewijzigd in zone:', int((voor != a).sum()), 'px')
im2 = Image.fromarray(a, 'P'); im2.putpalette(im.getpalette()); im2.save(p, transparency=0)
