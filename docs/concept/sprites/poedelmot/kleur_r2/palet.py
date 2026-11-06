"""Palet r2 + raster -> geïndexeerde png en JASC-pal."""
import sys, os
from PIL import Image
PAL = [
    (152, 208, 160),  # 0 transparant
    (16, 8, 8),       # 1 bijna zwart: oog, sprietvlak diep
    (56, 40, 32),     # 2 zwartbruin: buitenlijn schaduwkant, oogrand, sprietvlak
    (96, 72, 56),     # 3 donkerbruin: binnenlijnen, klauwtjes
    (136, 112, 96),   # 4 bruin: selout lichtkant, sprietbaarden onder, voetjes
    (176, 152, 128),  # 5 tan: sprietbaarden, schubpatroon donker
    (208, 184, 160),  # 6 lichttan: schubpatroon, vleugelschaduw, nerf
    (232, 216, 192),  # 7 crème warm: vleugels
    (216, 200, 192),  # 8 grijsroze: vachtschaduw (koel)
    (240, 232, 224),  # 9 crème licht: gezichtsmasker, vacht midden
    (248, 248, 248),  # A wit: vacht licht, oogglans
    (120, 112, 112),  # B grijs: oogreflectie
    (184, 168, 160),  # C koele diepe schaduw onder de pluimen
    (0, 0, 0), (0, 0, 0), (0, 0, 0),  # 13-15 ongebruikt
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
    H = os.path.dirname(os.path.abspath(__file__))
    a = sys.argv[1:] or [os.path.join(H, 'raster.txt'), os.path.join(H, 'poedelmot.png')]
    build(a[0], a[1]); write_pal(os.path.join(os.path.dirname(os.path.abspath(a[1])), 'normal.pal'))
