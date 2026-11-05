"""silhouet.txt -> silhouet_1x.png (+ optioneel vergroting)."""
import sys
from PIL import Image
rows = [l.rstrip('\n') for l in open('silhouet.txt')][:64]
im = Image.new('P', (64, 64), 0); im.putpalette([255, 255, 255, 40, 30, 60] + [0] * 762)
for y, r in enumerate(rows):
    for x, c in enumerate(r):
        if c == '#': im.putpixel((x, y), 1)
im.save('silhouet_1x.png', transparency=0)
if len(sys.argv) > 1: im.convert('RGB').resize((64 * int(sys.argv[2]),) * 2, Image.NEAREST).save(sys.argv[1])
