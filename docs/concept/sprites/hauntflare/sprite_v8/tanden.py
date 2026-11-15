"""Hauntflare v8: alleen tanden in de v7-mond. Rasters x18-35, y32-38 (hex-index per pixel)."""
from PIL import Image
import numpy as np, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
V7 = os.path.join(HERE, '..', 'sprite_v7', 'hauntflare_v7.png')
X0, Y0 = 18, 32
#            x: 890123456789012345
KAND = {
 # I: F, maar donkerrood achter de tanden (tong begint lager) zodat de tanden loskomen
 'I': ['777778777777811177',
       '7717771111111aa177',
       '771181a87a887aa277',
       '77711aa85558aa2777',
       '777171555555527776',
       '777778118152277766',
       '677777888227777766'],
 # J: I + twee kleine ondertanden (G)
 'J': ['777778777777811177',
       '7717771111111aa177',
       '771181a87a887aa277',
       '77711aa85558aa2777',
       '777171555855827776',
       '777778118812277766',
       '677777888227777766'],
 # K: drie boventanden (H) op donkerrood, tong lager
 'K': ['777778777777811177',
       '7717771111111aa177',
       '7711818a87a887a277',
       '77711aaa855a8a2777',
       '777171555555527776',
       '777778118152277766',
       '677777888227777766'],
}
def bouw(naam, rij):
    im = Image.open(V7); a = np.array(im).copy()
    for i, r in enumerate(rij):
        assert len(r) == 18, (naam, i, len(r))
        for j, c in enumerate(r):
            a[Y0+i, X0+j] = int(c, 16)
    out = Image.fromarray(a, 'P'); out.putpalette(im.getpalette())
    p = os.path.join(HERE, f'kandidaat_{naam}.png'); out.save(p, transparency=0)
    return p
if __name__ == '__main__':
    for k, v in KAND.items(): print(bouw(k, v))
