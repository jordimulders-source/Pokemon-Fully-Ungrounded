"""Palet (16 kleuren, index 0 transparant) -> normal.pal (JASC) en raster.txt -> kolibrie_pre.png (geïndexeerd)."""
import sys
from PIL import Image
PAL = [
    (152, 208, 160),  # 0 transparant
    (30, 20, 46),     # 1 omlijning schaduwkant (diep violet, geen zwart)
    (74, 58, 108),    # 2 omlijning lichtkant / diepe schaduw
    (118, 102, 162),  # 3 lila kernschaduw
    (164, 150, 208),  # 4 lila basis / hooglicht kap
    (202, 194, 236),  # 5 lila licht / buikschaduw
    (228, 224, 246),  # 6 buik lavendelwit
    (252, 250, 255),  # 7 buik hooglicht
    (48, 140, 156),   # 8 keelvlek blauwgroen
    (124, 210, 200),  # 9 keelvlek glans
    (60, 52, 78),     # A snavel/pootjes basis
    (108, 98, 176),   # B kap basis (koeler, dieper lila) / snavel hooglicht
    (250, 212, 72),   # C gele mondhoek
    (232, 166, 44),   # D mondhoek schaduw
    (74, 64, 136),    # E kap schaduw / iris onder
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
