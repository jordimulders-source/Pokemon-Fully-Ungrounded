#!/usr/bin/env python3
"""Olinguito ronde 21b: dikkere, korte poten in eigen hoeken (Poochyena / Galar-Linoone), op basis van ronde 21.
Alles buiten de pootzone en de staart komt letterlijk uit ronde 20 (via het ronde-21-script, incl. de kaaklijn).
Klauwblokken: dezelfde grootte en vorm als ronde 21. Alleen de pootlagen zijn nieuw."""
from PIL import Image
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..')
sys.path.insert(0, os.path.join(R, 'ronde21', 'bron'))
import bouw_ronde21 as B

# nabije voorpoot: stevig, schuin naar voren (gewicht op de poot), taps naar de pols, poot plat naar voren
B.NABIJ_VOOR = {
    40: (24, '22455433'),
    41: (23, '224554331'),
    42: (22, '22455443311'),
    43: (22, '2455544311'),
    44: (21, '245554431'),
    45: (20, '245544431'),
    46: (20, '24554431'),
    47: (19, '24544431'),
    48: (19, '2444431'),
    49: (18, '24444331'),
    50: (17, '244443331'),
    51: (17, '2313133311'),
    52: (18, '11111111'),
}
B.KLAUW_NABIJ = ((13, 48), B.KLAUW_NABIJ[1])
# verre voorpoot: korter (perspectief), iets naar achteren, schaduwtint; poot naar voren
B.VERRE_VOOR = {
    44: (28, '233331'),
    45: (29, '23331'),
    46: (29, '23331'),
    47: (30, '23331'),
    48: (30, '23331'),
    49: (30, '233331'),
    50: (30, '11111'),
}
B.KLAUW_VER = ((27, 47), B.KLAUW_VER[1])
B.BUIK = {
    43: (31, '33333333'),
    44: (34, '111111'),
}
# verre achterpoot: grotendeels achter de nabije; dij naar achteren, voet naar voren
B.VERRE_ACHTER = {
    45: (37, '233'),
    46: (37, '233'),
    47: (36, '233'),
    48: (36, '233'),
    49: (35, '2331'),
    50: (35, '23331'),
    51: (35, '11111'),
}
# nabije achterpoot: vorm van ronde 20 (hak naar achteren), op ronde-21-positie, scheen 1 px dikker aan de voorkant
NABIJ_ACHTER = {
    42: (46, '431'),
    43: (40, '24454431'),
    44: (40, '2444431'),
    45: (39, '2444311'),
    46: (38, '244431'),
    47: (38, '2444331'),
    48: (38, '2444331'),
    49: (38, '244331'),
    50: (37, '244431'),
    51: (37, '244431'),
    52: (36, '2444331'),
    53: (36, '1231331'),
    54: (37, '11.111'),
}
B.B20.NABIJE_ACHTERPOOT = NABIJ_ACHTER
B.HIND_DX = 0
B.FRAME2 = {}

if __name__ == '__main__':
    r20, out = B.bouw()
    out.save(os.path.join(H, '..', 'anim_front.png'), transparency=0)
    for f in (0, 1):
        n = sum(1 for y in range(64) for x in range(64) if out.getpixel((x, y + 64 * f)))
        print('frame %d: %d px' % (f + 1, n))
