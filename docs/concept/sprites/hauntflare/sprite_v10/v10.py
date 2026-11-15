"""Hauntflare v10 = v9 + alleen twee tanden (Jordi: "als je die linksonderin net wat groter maakt en rechtsboven net wat kleiner, dan keur ik de tanden goed").
- Rechtsboven: kolom x31 eraf: (31,33) 7->1 (lip), (31,34) 7->a (binnenkant). Tand nu (29-30,33), (30,34), punt (30,35).
- Linksonder: 1 px erbij omhoog de tong in: (24,37) 5->7, zwart erlangs (23,37) 5->1, (25,37) 5->1."""
from PIL import Image
import numpy as np, os, sys
H = os.path.dirname(os.path.abspath(__file__))
V9 = os.path.join(H, '..', 'sprite_v9', 'hauntflare_v9.png')
W = {(31,33):1, (31,34):10, (24,37):7, (23,37):1, (25,37):1}
def bouw(W, naam='hauntflare_v10.png'):
    im = Image.open(V9); a = np.array(im)
    for (x, y), c in W.items(): a[y, x] = c
    o = Image.fromarray(a, 'P'); o.putpalette(im.getpalette()); o.save(os.path.join(H, naam), transparency=0)
    return a
if __name__ == '__main__':
    a = bouw(W)
    print('    '+''.join(str(x%10) for x in range(18,36)))
    for y in range(31,41): print(y, ''.join('%x'%v for v in a[y,18:36]))
