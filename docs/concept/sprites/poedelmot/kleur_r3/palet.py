"""Palet r3 + raster -> geïndexeerde png en JASC-pal."""
import sys, os
from PIL import Image
PAL = [
    (152, 208, 160),  # 0 transparant
    (16, 8, 8),       # 1 zwart: oog, kern van de sprieten
    (56, 40, 32),     # 2 zwartbruin: buitenlijn schaduwkant, oogrand
    (96, 72, 56),     # 3 donkerbruin: binnenlijnen, klauwtjes
    (144, 112, 96),   # 4 bruin: selout lichtkant, sprietrand boven, klauwtjes licht
    (184, 144, 112),  # 5 tan: achterlijfringen, sprietbaarden, schubbogen donker
    (216, 184, 152),  # 6 lichttan: vleugelschubben, achterlijf, oogring
    (240, 224, 200),  # 7 crème: vleugelbasis, snuit
    (184, 176, 200),  # 8 koel lila-grijs diep: schaduwsikkel onder
    (216, 208, 224),  # 9 koel lila-grijs licht: schaduw vacht
    (248, 240, 232),  # A wit (warm): vacht, glans
    (104, 72, 48),    # B warm bruin: reflectie in het oog
    (240, 232, 208),  # C crème licht: sprietnerf
    (0, 0, 0), (0, 0, 0), (0, 0, 0),
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
