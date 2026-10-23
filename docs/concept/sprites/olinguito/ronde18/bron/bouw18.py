#!/usr/bin/env python3
"""Ronde 18: kop = ronde 16 (pixel voor pixel), staart (x >= 48) = ronde 17,
alleen de neuspunt 1 of 2 px naar rechts. Gebruik: python3 bouw18.py (vanuit ronde18/bron)."""
from PIL import Image
import os
H = os.path.dirname(os.path.abspath(__file__))
R16 = os.path.join(H, '../../ronde16/anim_front.png')
R17 = os.path.join(H, '../../ronde17/anim_front.png')
S = '.0123456789abcde'          # symbool -> paletindex (zie ronde16/bron/palet.txt)
def idx(s): return S.index(s)

# Neus ronde 16, frame 1: x9-11, y32-34 ("0a0/000/050"); frame 2 een rij hoger.
NEUS_Y = {0: 32, 64: 64 + 31}
# Per variant: kolommen x9..x13 per rij (bovenste, midden, onderste neusrij).
# None = pixel ongemoeid laten.
VARIANTEN = {
    '1px': ['10a0.', '0000.', '1050.'],   # x9 bruine omlijning (rand), neus x10-12
    '2px': ['050a0', '06000', '06050'],   # x9 omlijning blijft, x10 snuitvlak, neus x11-13
}
def bouw(var):
    a = Image.open(R16); b = Image.open(R17)
    out = a.copy()
    for y in range(128):
        for x in range(48, 64):
            out.putpixel((x, y), b.getpixel((x, y)))
    rijen = VARIANTEN[var]
    for f, y0 in NEUS_Y.items():
        for dy, rij in enumerate(rijen):
            for dx, s in enumerate(rij):
                if s != '.':
                    out.putpixel((9 + dx, y0 + dy), idx(s))
    return a, out
if __name__ == '__main__':
    for var, pad in (('1px', '..'), ('2px', '../variant_2px')):
        a, out = bouw(var)
        d = os.path.join(H, pad)
        out.save(os.path.join(d, 'anim_front.png'))
        for f in (0, 64):
            n = sum(a.getpixel((x, y)) != out.getpixel((x, y))
                    for y in range(f, f + 64) for x in range(0, 48))
            print(var, 'frame', 1 + f // 64, 'hoofdpixels veranderd:', n)
