"""Palet poedellarve r1 (kleuren op het model gemeten) + raster -> geïndexeerde png en JASC-pal."""
import sys, os
from PIL import Image
PAL = [
    (152, 208, 160),  # 0 transparant
    (16, 8, 8),       # 1 zwart: ogen, neus
    (52, 40, 36),     # 2 buitenlijn (model: zwarte buitenlijn)
    (104, 88, 82),    # 3 donkere binnenlijn: plooien onder bolletjes, mond, oogreflectie, sprietkrul
    (146, 128, 120),  # 4 donker grijsbeige: segmentnaden in de schaduw, voetschaduw, sprietribbels
    (182, 162, 152),  # 5 grijsbeige: pootjes, sprietschaduw, naden (model voet (184,164,152))
    (206, 194, 182),  # 6 schaduw wit 2: onderkant segmenten, naden in het licht
    (230, 224, 212),  # 7 schaduw wit 1
    (194, 176, 162),  # 8 beige schaduw (snuit/oogvlek)
    (0, 0, 0),        # 9 (ongebruikt)
    (246, 244, 234),  # A wit (model (232-240,232-240,224))
    (0, 0, 0),        # B (ongebruikt)
    (0, 0, 0),        # C (ongebruikt)
    (218, 202, 184),  # D beige oogvlek/snuit (model (216,200,184))
    (0, 0, 0),        # E (ongebruikt)
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
    a = sys.argv[1:] or [os.path.join(H, 'raster.txt'), os.path.join(H, 'poedellarve.png')]
    build(a[0], a[1]); write_pal(os.path.join(os.path.dirname(os.path.abspath(a[1])), 'normal.pal'))
