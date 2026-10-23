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
    44: (28, '23331'),
    45: (28, '23331'),
    46: (29, '23331'),
    47: (29, '23331'),
    48: (29, '23331'),
    49: (29, '233331'),
    50: (29, '111111'),
}
B.KLAUW_VER = ((26, 47), B.KLAUW_VER[1])
B.BUIK = {
    43: (31, '33333333'),
    44: (33, '11111'),
}
# verre achterpoot: grotendeels achter de nabije; dij naar achteren, voet naar voren
B.VERRE_ACHTER = {
    45: (42, '23331'),
    46: (42, '23331'),
    47: (42, '233331'),
    48: (42, '233331'),
    49: (42, '233331'),
    50: (41, '2333331'),
    51: (41, '2333331'),
    52: (41, '1111111'),
}
# nabije achterpoot: vorm van ronde 20 (hak naar achteren), op ronde-21-positie, scheen 1 px dikker aan de voorkant
NABIJ_ACHTER = {
    42: (45, '4431'),
    43: (39, '2445444431'),
    44: (38, '24454444431'),
    45: (38, '2444444431'),
    46: (37, '244444331'),
    47: (36, '24444331'),
    48: (35, '2444331'),
    49: (34, '2444331'),
    50: (34, '244431'),
    51: (33, '2444431'),
    52: (32, '24444331'),
    53: (32, '12313331'),
    54: (33, '11.1111'),
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
