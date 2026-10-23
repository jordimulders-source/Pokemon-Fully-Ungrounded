"""Vergelijkingsvel en metingen voor de Cuyby-evolutie ronde 3: ronde 2 en ronde 3 (beide frames) naast Cuyby
en de bestudeerde echte sprites, op 3x en 1x.

Vanuit de repo-root: python3 docs/concept/sprites/cuyby_evo/ronde3/bron/vel.py
Schrijft compare.png en drukt de metingen af (de rasters schrijft bouw9.py).
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../../../../..'))
sys.path.insert(0, os.path.join(REPO, 'docs/concept/sprites/nachtaap/ronde7/bron'))
from vellen import load

S = REPO + '/docs/concept/sprites/'
G = REPO + '/graphics/pokemon/'
OUT = os.path.join(HERE, '..')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)


def echt(n):
    p = G + n + '/anim_front_gba.png'
    return p if os.path.exists(p) else G + n + '/anim_front.png'


RIJ1 = [('Cuyby ronde 3', S + 'cuyby/ronde3/anim_front.png', 0),
        ('evolutie ronde 2', S + 'cuyby_evo/ronde2/anim_front.png', 0),
        ('ronde 3 f1', S + 'cuyby_evo/ronde3/anim_front.png', 0),
        ('ronde 3 f2', S + 'cuyby_evo/ronde3/anim_front.png', 1)]
RIJ2 = [(n, echt(n), 0) for n in ('piloswine', 'swinub', 'mamoswine', 'mareep', 'linoone', 'furret',
                                  'ninetales', 'teddiursa')]


def measure(im):
    px = im.load()
    opaque = lambda x, y: 0 <= x < 64 and 0 <= y < 64 and px[x, y][3] > 0
    area = sum(1 for y in range(64) for x in range(64) if opaque(x, y))
    bb = im.getbbox()
    rim = [(x, y) for y in range(64) for x in range(64) if opaque(x, y) and
           any(not opaque(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    black = sum(1 for x, y in rim if max(px[x, y][:3]) < 48) / len(rim)
    return area, (bb[2] - bb[0], bb[3] - bb[1]), black


def sheet(out):
    sc, cw = 3, 64 * 3 + 16
    W = 8 + len(RIJ2) * cw
    rh = 64 * sc + 26 + 72
    img = Image.new('RGB', (W, 32 + 2 * rh), (232, 236, 240))
    d = ImageDraw.Draw(img)
    d.text((8, 6), 'Cuyby-evolutie ronde 3: diagonaal (3/4 links-voor), ruiger; boven ronde 2/3 en Cuyby, '
                   'onder de bestudeerde Gen 3/4-sprites (3x en 1x)', fill=(20, 20, 20), font=FB)
    for r, items in enumerate((RIJ1, RIJ2)):
        y0 = 32 + r * rh
        for i, (lab, p, fr) in enumerate(items):
            sp = load(p, fr)
            x = 8 + i * cw
            big = sp.resize((64 * sc, 64 * sc), Image.NEAREST)
            img.paste(big, (x, y0), big)
            d.text((x, y0 + 194), lab, fill=(40, 40, 40), font=F)
            img.paste(sp, (x + 64, y0 + 64 * sc + 24), sp)
    img.save(out)


if __name__ == '__main__':
    sheet(os.path.join(OUT, 'compare.png'))
    print('| | oppervlak | b x h | zwart in de buitenrand |')
    for lab, p, fr in RIJ1 + RIJ2:
        a, (w, h), bl = measure(load(p, fr))
        print('| %s | %d | %dx%d | %.2f |' % (lab, a, w, h, bl))
