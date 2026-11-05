"""Diff ronde 1b t.o.v. ronde 1: per zone, en 0 buiten de zones (bewijs)."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
a = Image.open(os.path.join(OUT, '../ronde1/lama.png')); b = Image.open(os.path.join(OUT, 'lama.png'))
ch = {(x, y) for y in range(64) for x in range(64) if a.getpixel((x, y)) != b.getpixel((x, y))}
def zone(x, y):
    if 23 <= y <= 44 and not (y == 23 and x <= 15) and not (y <= 24 and x >= 50) and not (y >= 41 and x <= 34):
        if 36 <= x <= 47 and 25 <= y <= 33: return 'aguayo'
        if 19 <= x <= 31 and 26 <= y <= 31: return 'halsband'
        return 'romp/dij/hals'
    return None
cnt = {}
for x, y in ch: cnt[zone(x, y)] = cnt.get(zone(x, y), 0) + 1
print('gewijzigd per zone:', {k: v for k, v in cnt.items() if k}, '| buiten de zones:', cnt.get(None, 0))
