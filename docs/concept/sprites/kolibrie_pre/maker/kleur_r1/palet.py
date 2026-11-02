"""Palet (16 kleuren, index 0 transparant) -> normal.pal (JASC) en raster.txt -> kolibrie_pre.png (geïndexeerd)."""
import sys
from PIL import Image
PAL = [
    (152, 208, 160),  # 0 transparant
    (44, 32, 62),     # 1 omlijning schaduwkant (diep violet, geen zwart)
    (88, 72, 118),    # 2 donker grijsviolet: omlijning, diepe schaduw
    (126, 110, 160),  # 3 lila schaduw / gekleurde omlijning lichtkant
    (164, 150, 200),  # 4 lila basis
    (200, 190, 228),  # 5 lila licht / buikschaduw
    (226, 222, 242),  # 6 buik lavendelwit
    (250, 248, 255),  # 7 buik hooglicht
    (74, 150, 160),   # 8 blauwgroene glans
    (142, 208, 200),  # 9 blauwgroen licht
    (70, 62, 84),     # A snavel/pootjes basis
    (122, 114, 140),  # B snavel hooglicht
    (248, 208, 82),   # C gele mondhoek
    (214, 150, 52),   # D mondhoek schaduw
    (96, 80, 146),    # E iris onder (violet)
    (255, 255, 255),  # F glans
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
