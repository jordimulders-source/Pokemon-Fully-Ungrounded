#!/usr/bin/env python3
"""Stap 1 (kop): ronde 18 + gezicht in Galar-Linoone-constructie.
Alleen de gezichtszone x9-23, y25-33 (frame 2: een rij hoger) verandert.
Het verre oog, de verre maskerlob en de verre wenkbrauw worden de bruine neusbrug;
het masker rond het nabije oog loopt als band door tot de neus.
Oren, nabij oog, nabije maskerlob, grijns, lijf, poten en staart: ronde 18.
Tekens = PNG-paletindex (hex), '.' = ongemoeid laten (niet: transparant)."""
from PIL import Image
import os
H = os.path.dirname(os.path.abspath(__file__))
R18 = os.path.join(H, '../../ronde18/anim_front.png')
X0 = 9
# Met de hand per rij, kolommen x9..x23 (15 tekens). Frame 1-rij.
RIJEN = {
    26: '.......5554....',   # verre wenkbrauw (crème) weg: voorhoofd
    27: '.......5..4....',   # x16 crème weg, x19 crème weg
    28: '......5544444..',   # verre maskerlob boven -> neusbrug (x20-21 hooglicht 5 -> 4)
    29: '.....5544444422',   # brug; maskerrand op x22 (golf naar het oog)
    30: '....5444422....',   # brug loopt schuin omlaag; masker vanaf x19
    31: '..4...42222....',   # x11 brug tot boven de neus; ver oog (C,1,E) -> masker
    32: '.....3222DD....'.replace('DD', '22'),  # ver oog (D,D) -> masker
}
def bouw():
    a = Image.open(R18)
    out = a.copy()
    for f in (0, 63):            # frame 2 ligt 1 rij hoger (y + 64 - 1)
        for y, rij in RIJEN.items():
            assert len(rij) == 15, (y, rij)
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
        print('frame', 1 + f // 64, 'gewijzigd:', len(d),
              'bbox x', min(p[0] for p in d), '-', max(p[0] for p in d),
              'y', min(p[1] for p in d), '-', max(p[1] for p in d))
