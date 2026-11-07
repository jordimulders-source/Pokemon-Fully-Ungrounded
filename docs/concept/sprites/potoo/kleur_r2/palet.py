"""Potoo r1: palet (gemeten op model_lijf_30 met k-means) + raster -> geïndexeerde potoo.png en normal.pal (JASC)."""
import sys, os
from PIL import Image
PAL = [
    (64, 160, 64),    # 0 transparant
    (8, 8, 24),       # 1 zwart-navy: buitenlijn schaduwkant, oog, keelholte (model (5,5,22))
    (52, 50, 70),     # 2 donker grijsnavy: binnenlijnen, oogreflectie (model (47,46,58))
    (94, 92, 108),    # 3 donkergrijs: schaduw onderlijf/klauwen, spikkels (model (93,90,101))
    (126, 124, 132),  # 4 middengrijs: selout lichtkant, veerlijnen (model (124,122,126))
    (158, 154, 152),  # 5 warm grijs (model (156,152,150))
    (194, 189, 177),  # 6 licht warmgrijs (model (194,189,177))
    (226, 220, 200),  # 7 crème (model (226,220,200))
    (250, 250, 248),  # 8 wit (model (250,250,250))
    (44, 48, 92),     # 9 donkerblauw: muilschaduw (model (44,48,87))
    (60, 74, 134),    # A blauw (model (59,74,134))
    (104, 92, 148),   # B paars (model (105,91,144))
    (104, 136, 182),  # C lichtblauw (model (105,138,182))
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
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
    a = sys.argv[1:] or [os.path.join(H, 'raster.txt'), os.path.join(H, 'potoo.png')]
    build(a[0], a[1]); write_pal(os.path.join(os.path.dirname(os.path.abspath(a[1])), 'normal.pal'))
