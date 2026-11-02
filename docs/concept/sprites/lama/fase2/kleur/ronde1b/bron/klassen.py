"""Kaart van de onderdelen: per spritepixel de meerderheidsklasse van het 4x4-blok in de onderlaag.
Alleen als kaart gebruikt bij het met de hand typen van raster.txt; er wordt niets uit gekopieerd."""
import os
from collections import Counter
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
SIL = os.path.join(HERE, '../../../silhouet/ronde1b.txt')
im = Image.open(os.path.join(HERE, '../../../silhouet/onderlaag_256.png')).convert('RGB')
REF = {'B': (200, 142, 85), 'b': (181, 122, 69), 'H': (168, 106, 58), 'L': (144, 97, 55), 'R': (208, 42, 42),
       'U': (47, 95, 184), 'G': (46, 154, 89), 'K': (35, 28, 28), 'Y': (240, 200, 60), 'P': (230, 80, 160), 'T': (40, 170, 170)}
def cls(c):
    if min(c) > 240: return None
    return min(REF, key=lambda k: sum((a - b) ** 2 for a, b in zip(REF[k], c)))
sil = [l.rstrip('\n') for l in open(SIL)]
out = []
for y in range(64):
    row = ''
    for x in range(64):
        if sil[y][x] != '#': row += '.'; continue
        cnt = Counter(cls(im.getpixel((x * 4 + i, y * 4 + j))) for i in range(4) for j in range(4))
        cnt.pop(None, None)
        if not cnt: row += '?'; continue
        k = [k for k, n in cnt.most_common() if k != 'K']
        row += 'K' if cnt.get('K', 0) >= 10 or not k else k[0]
    out.append(row)
open(os.path.join(HERE, 'klassen.txt'), 'w').write('\n'.join(out) + '\n')
print('     ' + ''.join(str(i % 10) for i in range(64)))
for y, r in enumerate(out): print('%2d   ' % y + r)
