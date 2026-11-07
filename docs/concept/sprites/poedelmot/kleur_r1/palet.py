"""Palet (index 0 transparant) + raster -> geïndexeerde png en JASC-pal."""
import sys
from PIL import Image
PAL = [
    (152, 208, 160),  # 0 transparant
    (24, 16, 16),     # 1 zwartbruin: buitenlijn schaduwkant, oog, sprieten
    (64, 48, 40),     # 2 donkerbruin: binnenkant van het oog (donkere glans)
    (104, 72, 56),    # 3 bruin: binnenlijnen (snuit, pluimen, kop/vleugel), achterlijf in schaduw
    (144, 104, 72),   # 4 tanbruin: sprietbaarden, voetjes, achterlijf, oogrand onder
    (184, 144, 104),  # 5 tan: schubkrullen op de vleugels, achterlijf, middennerf aan de basis, oogrand
    (216, 184, 152),  # 6 crème-tan: vachtschaduw, vleugelbasis, middennerf
    (240, 224, 200),  # 7 crème: vacht midden, vachtplukken
    (248, 248, 240),  # 8 wit: vacht licht, glans in het oog
    (112, 112, 120),  # 9 grijs: oogreflectie
    (160, 128, 104),  # A selout aan de lichtkant (links/boven)
    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),  # 11-15 ongebruikt
]
CH = '.123456789ABCDEF'
def build(txt, out):
    rows = [l.rstrip('\n') for l in open(txt)][:64]
    im = Image.new('P', (64, 64), 0); im.putpalette([v for c in PAL for v in c])
    for y, r in enumerate(rows):
        for x, c in enumerate(r): im.putpixel((x, y), CH.index(c))
    im.save(out, transparency=0); return im
def write_pal(path):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in PAL))
if __name__ == '__main__':
    import os
    H = os.path.dirname(os.path.abspath(__file__))
    a = sys.argv[1:] or [os.path.join(H, 'raster.txt'), os.path.join(H, 'poedelmot.png')]
    build(a[0], a[1])
    write_pal(os.path.join(os.path.dirname(os.path.abspath(a[1])), 'normal.pal'))
