"""meet_luma.py: helderheidsstappen (luma 0,3R+0,59G+0,11B) en pixelaantallen per tint van r4, naast r2."""
import os
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
for n, p in (('r2', os.path.join(H, '..', 'kleur_r2', 'poesrups.png')), ('r4', os.path.join(H, 'poesrups.png'))):
    im = Image.open(p); pal = im.getpalette(); cnt = dict((i, c) for c, i in im.getcolors())
    print(n); vorig = None
    for i in (10, 7, 6, 5, 4, 3, 2, 1):
        r, g, b = pal[i*3:i*3+3]; l = 0.3*r + 0.59*g + 0.11*b
        print(f'   {".123456789ABCDEF"[i]} ({r:3d},{g:3d},{b:3d}) luma {l:5.1f}' + (f'  stap {vorig-l:4.1f}' if vorig is not None else '          ') + f'  {cnt.get(i, 0):4d} px  R-B {r-b}')
        vorig = l
