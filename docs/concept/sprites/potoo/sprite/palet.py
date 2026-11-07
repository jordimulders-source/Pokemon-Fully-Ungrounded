"""Palet potoo-sprite (C2). Index 0 transparant. raster.txt -> png (geïndexeerd) + normal.pal."""
import sys
from PIL import Image
PAL = [
    (152, 208, 160),  # . 0 transparant
    (34, 26, 50),     # 1 buitenlijn schaduwkant, mondlijn, gaplijn
    (96, 82, 128),    # 2 selout lichtkant, binnenlijnen (kaakrand/kin, plooi, veerlijnen)
    (156, 148, 184),  # 3 vacht schaduw
    (194, 188, 216),  # 4 vacht halfschaduw
    (224, 220, 238),  # 5 vacht basis (bijna wit, lila zweem)
    (248, 246, 252),  # 6 vacht licht
    (150, 136, 146),  # 7 schorsstreepjes (grijsbruin)
    (8, 8, 12),       # 8 oog: puur zwart, geen glans
    (52, 38, 112),    # 9 muil donker (gehemelte, keel, V-spleet, binnenrand)
    (96, 76, 182),    # A muil midden (geestpaars)
    (138, 124, 224),  # B muil licht (kaakbodem, verre binnenwand)
    (178, 170, 240),  # C muil lichtst (tong)
    (238, 214, 238),  # D kaakrand/lip (licht rozelila)
    (86, 80, 98),     # E hoorn donker (haak, kaakpunt)
    (164, 158, 176),  # F hoorn licht (snavelrug)
]
CH = '.123456789ABCDEF'
def build(txt, out):
    rows = [l.rstrip('\n') for l in open(txt)][:64]
    im = Image.new('P', (64, 64), 0); im.putpalette([v for c in PAL for v in c])
    for y, r in enumerate(rows):
        for x, c in enumerate(r): im.putpixel((x, y), CH.index(c))
    im.info['transparency'] = 0
    im.save(out, transparency=0); return im
def pal(out):
    with open(out, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in PAL))
if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
