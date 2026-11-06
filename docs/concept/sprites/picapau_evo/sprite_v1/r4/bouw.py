"""raster.txt (één teken per paletindex) -> picapau_evo.png (geïndexeerd) + normal.pal. Gebruik: python3.11 bouw.py [raster]"""
import sys
from PIL import Image
from palet import PAL, IDX, lees
fn = sys.argv[1] if len(sys.argv) > 1 else 'raster.txt'
out = sys.argv[2] if len(sys.argv) > 2 else 'picapau_evo.png'
g = lees(fn)
im = Image.new('P', (64, 64)); im.putpalette([v for _, c in PAL for v in c])
im.putdata([IDX[c] for r in g for c in r]); im.save(out, transparency=0)
if out == 'picapau_evo.png':
    with open('normal.pal', 'w') as f:
        f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join(f'{c[0]} {c[1]} {c[2]}\r\n' for _, c in PAL))
print('ok', sum(c != '.' for r in g for c in r), 'px')
