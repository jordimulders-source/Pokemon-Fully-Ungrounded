"""Nachtaap ronde 5: het lijf van ronde 4 met met de hand gezette ogen in de stijl van ronde 2/3.
python3 build.py <ronde5-map>   (schrijft anim_front.png en normal.pal)

De ogen staan hieronder als pixelraster (frame 1; frame 2 = dezelfde ogen 1 px hoger,
omdat de kop in frame 2 1 px omhoog komt).
Tekens: '.' = laten staan, '-' = vacht (2), '=' = schaduwvacht (3), 4 = masker/lijn,
b = maansikkel (11), c = nachtgloed (12), d = nachtblauw (13), e = glans (14), f = zwart (15).
"""
import sys, os, shutil
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
R4 = os.path.join(HERE, '..', '..', 'ronde4')
CH = '.123456789abcdef'

# (rij, kolom, raster); nabije oog (links, 8 breed) en verre oog (rechts, 7 breed, in de schaduw)
EYES = (
    (23, 15, ['-ffffff-',
              'ffebdddf',
              'fbbddddf',
              'fbdddddf',
              'fddddccf',
              'fdddcbcf',
              '4fdcccf-',
              '44ffff--']),
    (23, 27, ['-fffff==',
              'febddff=',
              'fbddddf=',
              'fdddddf4',
              'fddddcf4',
              'fddcbcf4',
              '=fdccf4=',
              '==fff===']),
)


def build():
    im = Image.open(os.path.join(R4, 'anim_front.png')); a = np.array(im); pal = im.getpalette()
    for k in range(2):
        f = a[k * 64:(k + 1) * 64]
        dy = -k
        # oude ogen (index 11-15) in het gezicht wissen
        for y in range(23, 31):
            for x in range(14, 36):
                if 11 <= f[y + dy, x] <= 15 and not (x in (14, 15, 35) and f[y + dy, x] == 15 and y >= 29):
                    f[y + dy, x] = 2 if x < 27 else 3
        for (y0, x0, rows) in EYES:
            for j, r in enumerate(rows):
                for i, c in enumerate(r):
                    if c == '.':
                        continue
                    f[y0 + j + dy, x0 + i] = 2 if c == '-' else 3 if c == '=' else CH.index(c)
    out = Image.fromarray(a, 'P'); out.putpalette(pal)
    return out


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..')
    build().save(os.path.join(d, 'anim_front.png'), transparency=0)
    shutil.copy(os.path.join(R4, 'normal.pal'), os.path.join(d, 'normal.pal'))
    print('anim_front.png + normal.pal ->', d)
