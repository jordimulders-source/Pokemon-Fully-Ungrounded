"""Kandidaat T: v7-mond opgerekt (rek.py: rijen gedupliceerd, 5 rijen open) + tanden vast aan de lip, ongelijk (Haunter G3 / pixel-ref)."""
from PIL import Image
import os, rek
from tanden import rij
H = os.path.dirname(os.path.abspath(__file__))
# T: v7-mond opgerekt (rek.py) + tanden vast aan de lip, ongelijk, naar Haunter G3 / pixel-ref.
# Boven 2 V's: ver (links) klein: voet (25-26,33), punt (25,34); dichtbij groot: voet (29-31,33), (30-31,34), punt (30,35), zwarte lijn links;
# rechte lip ertussen (27-28,33). Onder zoals Haunter G3 (punt met zwarte lijn aan beide kanten, voet breekt de onderlip open):
# dichtbij punt (28,37) 2 hoog, voet x27-29; ver punt (24,38) 1 hoog, voet x24-25.
T = (rij(33, 24, '17711777') + rij(34, 24, 'a7aaa177a') + rij(35, 29, '17a')
   + rij(37, 27, '171')
   + rij(38, 24, '7157772')
   + rij(39, 24, '771777')
   + rij(40, 27, '77'))
def bouw(n, T):
    im, b = rek.rek()
    for x, y, c in T: b[y, x] = c
    out = Image.fromarray(b, 'P'); out.putpalette(im.getpalette())
    p = os.path.join(H, f'kandidaat_{n}.png'); out.save(p, transparency=0); return p
if __name__ == '__main__':
    print(bouw('T', T))
