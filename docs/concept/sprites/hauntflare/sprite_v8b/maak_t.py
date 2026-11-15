"""Kandidaat T: v7-mond opgerekt (rek.py: rijen gedupliceerd, 5 rijen open) + tanden vast aan de lip zoals R."""
from PIL import Image
import os, rek
from tanden import rij
H = os.path.dirname(os.path.abspath(__file__))
# Tanden ongelijk (Jordi: "niet allemaal precies hetzelfde"): verre (linker) boventand klein, nabije groot;
# ondertanden kleiner en verschillend; punten verspringend.
T = (rij(33, 24, '1771777711')     # voeten in de bovenlip: ver x25-26 (2 breed), dichtbij x28-31 (4 breed)
   + rij(34, 24, '171a1771a')      # ver: punt (25,34); dichtbij: (29-30,34)
   + rij(35, 29, '171')            # dichtbij: punt (30,35), 3 rijen lang
   + rij(37, 27, '272')            # ondertand dichtbij: punt (28,37)
   + rij(38, 24, '7227772')        # ondertand ver: punt (24,38); dichtbij verbreedt x27-29
   + rij(39, 24, '7717777')        # voeten in de onderlip, inkeping (26,39)
   + rij(40, 27, '77'))            # kinschaduw onder de voet weg
def bouw():
    im, b = rek.rek()
    for x, y, c in T: b[y, x] = c
    out = Image.fromarray(b, 'P'); out.putpalette(im.getpalette())
    p = os.path.join(H, 'kandidaat_T.png'); out.save(p, transparency=0); return p
if __name__ == '__main__': print(bouw())
