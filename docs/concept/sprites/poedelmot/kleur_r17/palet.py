"""Palet r9 (bronkleuren per zone gemeten) + raster -> geïndexeerde png en JASC-pal."""
import sys, os
from PIL import Image
PAL = [
    (152, 208, 160),  # 0 transparant
    (16, 8, 8),       # 1 zwart: oog, sprietvlak
    (56, 40, 32),     # 2 zwartbruin: buitenlijn schaduwkant, oogrand
    (96, 72, 56),     # 3 donkerbruin: binnenlijnen, klauwtjes
    (152, 120, 104),  # 4 bruin: selout lichtkant, klauwtjes licht, sprietbaarden onder
    (176, 144, 120),  # 5 tan donker: schubbogen bij de vleugelvoet, achterlijfringen, sprietbaarden
    (200, 168, 136),  # 6 tan: krullen, buikplaten, vleugelvoet, oogring
    (232, 212, 184),  # 7 crème: schaduw vacht, vleugelvlak, snuit
    (198, 176, 162),  # 8 licht grijsbeige: bovenste plaat middenstuk, B2-dons (gemeten (194,167,146)/(200,185,178))
    (158, 124, 112),  # 9 grijsbruin: onderste plaat middenstuk (gemeten (160,125,113), lum 133)
    (248, 248, 240),  # A wit (warm): vacht, glans
    (72, 64, 48),     # B donker olijf: zwakke reflectie onderin het oog
    (240, 232, 208),  # C licht crème: sprietnerf
    (214, 190, 168),  # D zachte tan: vlakken voorvleugel (gemeten op het model)
    (0, 0, 0), (0, 0, 0),
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
