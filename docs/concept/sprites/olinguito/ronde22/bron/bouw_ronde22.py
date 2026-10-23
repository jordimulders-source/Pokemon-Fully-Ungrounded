#!/usr/bin/env python3
"""Olinguito ronde 22: pootconfiguratie van Galar-Linoone, diagonale stap (geen telgang).
Basis: ronde 21b (zelfde lagen, zelfde klauwblokken, zelfde dikke poten). Alleen de pootlagen veranderen:
- verre voorpoot vooraan onder de kin (schaduwtint, 2 kleine klauwen), schuin naar voren, zoals Linoone;
- nabije voorpoot onder de borst, licht naar achteren (zoals Linoone's nabije voorpoot);
- nabije achterpoot naar voren (hak blijft), scheen 1-3 px steiler zodat er lucht is naar de voorpoot;
- verre achterpoot naar achteren (ongewijzigd).
Diagonale paren: vóór = verre voor + nabije achter; achter = nabije voor + verre achter."""
from PIL import Image
import os, sys
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..')
sys.path.insert(0, os.path.join(R, 'ronde21b', 'bron'))
sys.path.insert(0, os.path.join(R, 'ronde21', 'bron'))
import bouw_ronde21b as P          # zet de 21b-lagen in B
import bouw_ronde21 as B

# nabije voorpoot: schouder van 21b, poot loodrecht tot iets naar achteren, voet onder de borst
B.NABIJ_VOOR = {
    40: (24, '22455433'),
    41: (23, '224554331'),
    42: (23, '2245544331'),
    43: (24, '245554431'),
    44: (25, '245554431'),
    45: (26, '24554431'),
    46: (27, '24544431'),
    47: (27, '24444331'),
    48: (26, '244443331'),
    49: (26, '2313133311'),
    50: (27, '11111111'),
}
B.KLAUW_NABIJ = ((22, 46), P.B.KLAUW_NABIJ[1])
# verre voorpoot: vooraan onder de kin (Linoone), schuin naar voren, schaduwtint, even dik als in 21b;
# de voet staat vooraan het laagst, zoals bij Linoone
B.VERRE_VOOR = {
    40: (19, '23333'),
    41: (19, '23331'),
    42: (19, '23331'),
    43: (18, '23331'),
    44: (18, '23331'),
    45: (18, '23331'),
    46: (17, '23331'),
    47: (17, '23331'),
    48: (17, '23331'),
    49: (16, '23331'),
    50: (15, '233331'),
    51: (15, '233331'),
    52: (15, '11111'),
}
B.KLAUW_VER = ((12, 49), P.B.KLAUW_VER[1])
# nabije achterpoot: 21b, onderbeen per rij iets naar achteren (dx), voet blijft vóór de heup; hak ongewijzigd
DX = {46: 0, 47: 1, 48: 2, 49: 3, 50: 3, 51: 4, 52: 4, 53: 4, 54: 4}
B.B20.NABIJE_ACHTERPOOT = {y: (x0 + DX.get(y, 0), s) for y, (x0, s) in P.NABIJ_ACHTER.items()}

if __name__ == '__main__':
    r20, out = B.bouw()
    out.save(os.path.join(H, '..', 'anim_front.png'), transparency=0)
    for f in (0, 1):
        n = sum(1 for y in range(64) for x in range(64) if out.getpixel((x, y + 64 * f)))
        print('frame %d: %d px' % (f + 1, n))
