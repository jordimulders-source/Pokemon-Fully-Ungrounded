"""Palet (16 kleuren, index 0 transparant) -> normal.pal (JASC) en raster.txt -> kolibrie_pre.png (geïndexeerd)."""
import sys
from PIL import Image
PAL = [
    (152, 208, 160),  # 0 transparant
    (20, 14, 30),     # 1 buitenlijn (bijna-zwart violet), oog, snavelrand
    (70, 52, 104),    # 2 binnenlijnen (kopvorm, kapnaad, buikgrens, veerlijnen) en selout bovenop
    (106, 88, 152),   # 3 lila schaduw
    (152, 136, 200),  # 4 lila basis
    (186, 176, 224),  # 5 lila licht / buikschaduw
    (228, 224, 246),  # 6 buik lavendelwit
    (255, 255, 255),  # 7 buik hooglicht en glans in het oog
    (92, 186, 142),   # 8 iris smaragd (was mondbinnenkant roze; die is nu 9)
    (176, 98, 40),    # 9 verre poot (donker warm); keelopening nu 1
    (40, 120, 92),    # A iris smaragd donker (snavel-donker A is nu 2)
    (102, 90, 172),   # B kap en vleugel basis
    (250, 212, 72),   # C gele mondhoek
    (226, 150, 40),   # D mondhoek omlijning/schaduw
    (72, 62, 134),    # E kap- en vleugelschaduw, iris
    (150, 142, 174),  # F snavel boventint, licht puntje poot
]
CH = '.123456789ABCDEF'
def build(txt='raster.txt', out='kolibrie_pre.png'):
    rows = [l.rstrip('\n') for l in open(txt)][:64]
    im = Image.new('P', (64, 64), 0); im.putpalette([v for c in PAL for v in c])
    for y, r in enumerate(rows):
        for x, c in enumerate(r): im.putpixel((x, y), CH.index(c))
    im.save(out, transparency=0); return im
if __name__ == '__main__':
    build()
    with open('normal.pal', 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in PAL))
