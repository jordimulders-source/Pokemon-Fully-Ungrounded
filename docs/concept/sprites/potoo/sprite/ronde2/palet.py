"""Palet ronde 2 (C2, meer waardebereik; vleugel eigen donkerder toon). Index 0 transparant."""
import sys
from PIL import Image
PAL = [
    (152, 208, 160),  # . transparant
    (28, 20, 44),     # 1 buitenlijn, mondlijn, vleugelomlijning
    (90, 76, 124),    # 2 selout lichtkant, binnenlijnen (vleugelrand, veerlijnen, plooi)
    (142, 130, 176),  # 3 vleugel basis, diepe schaduw lijf
    (186, 178, 214),  # 4 schaduw lijf, vleugel-hooglicht (veerranden), hoornrug
    (226, 222, 240),  # 5 vacht basis
    (250, 248, 255),  # 6 vacht licht
    (150, 134, 146),  # 7 schorsstreepjes op de vacht (grijsbruin)
    (8, 8, 12),       # 8 oog, puur zwart
    (52, 38, 112),    # 9 muil donker
    (96, 76, 182),    # A muil midden
    (138, 124, 224),  # B muil licht
    (178, 170, 240),  # C tong
    (238, 214, 238),  # D kaakrand/lip
    (78, 72, 92),     # E hoorn (haak, snijrand, kaakpunt)
    (108, 96, 140),   # F vleugel schaduw, schorsstreepjes op de vleugel
]
CH = '.123456789ABCDEF'
def build(txt, out):
    rows = [l.rstrip('\n') for l in open(txt)][:64]
    im = Image.new('P', (64, 64), 0); im.putpalette([v for c in PAL for v in c])
    for y, r in enumerate(rows):
        for x, c in enumerate(r): im.putpixel((x, y), CH.index(c))
    im.save(out, transparency=0); return im
def pal(out):
    with open(out, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in PAL))
if __name__ == '__main__': build(sys.argv[1], sys.argv[2])
