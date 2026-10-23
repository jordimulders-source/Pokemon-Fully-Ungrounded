#!/usr/bin/env python3
"""Stap 1b (kop): stap 1 + gezicht van Galar-Linoone.
Oog + oogpatroon (lob, wimper, lid) 5 px naar voren (naar de snuit); masker als vlakke band
van het oog tot boven de neus; wenkbrauw direct op de maskerrand boven het oog.
Met de hand per rij uitgeschreven, kolommen x11..x36 (26 tekens).
Tekens = paletindex (hex), '.' = ongemoeid laten (niet: transparant)."""
from PIL import Image
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
ST1 = os.path.join(H, '../../stap1_kop/anim_front.png')
X0 = 11
#            x11       x21       x31
#            |         |         |
RIJEN = {
    26: '.............444..2....4..',   # oude wenkbrauw (x24-26) en lobpunt (x34) -> vacht; lobpunt nu x29
    27: '........78776442224444444.',   # wenkbrauw x19-23 direct op de maskerrand; lob x26-28
    28: '....3322222221222444444...',   # bandtop vlak van snuit tot oog (y28); glans 3 voorop
    29: '...32222111112222444444444',   # lid x19-23
    30: '..322222eec1e2222444444444',   # oog x19-23
    31: '32222222dd11d2222444444444',   # band tot boven de neus (x11-12)
    32: '..2222222ddd22222444444444',   # goud onder, wang bruin vanaf x28
}
def bouw():
    a = Image.open(ST1)
    out = a.copy()
    for f in (0, 63):            # frame 2 ligt 1 rij hoger (y + 64 - 1)
        for y, rij in RIJEN.items():
            assert len(rij) == 26, (y, len(rij))
            for dx, s in enumerate(rij):
                if s != '.':
                    out.putpixel((X0 + dx, y + f), int(s, 16))
    return a, out
if __name__ == '__main__':
    a, out = bouw()
    out.save(os.path.join(H, '../anim_front.png'), transparency=0)
    for f in (0, 64):
        d = [(x, y - f) for y in range(f, f + 64) for x in range(64)
             if a.getpixel((x, y)) != out.getpixel((x, y))]
        print('frame', 1 + f // 64, 'gewijzigd t.o.v. stap 1:', len(d),
              'bbox x', min(p[0] for p in d), '-', max(p[0] for p in d),
              'y', min(p[1] for p in d), '-', max(p[1] for p in d))
