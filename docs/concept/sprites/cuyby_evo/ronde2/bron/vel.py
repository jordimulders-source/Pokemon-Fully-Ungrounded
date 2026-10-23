"""Vergelijkingsvel en metingen voor de Cuyby-evolutie ronde 2 (Cuyby ronde 3, ronde 1 en echte Gen 3-sprites ernaast).

Vanuit de repo-root: python3 docs/concept/sprites/cuyby_evo/ronde2/bron/vel.py
Schrijft compare.png en drukt de metingen af (de rasters schrijft bouw9.py).
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../../../../..'))
sys.path.insert(0, os.path.join(REPO, 'docs/concept/sprites/nachtaap/ronde7/bron'))
sys.path.insert(0, HERE)
from vellen import load

S = REPO + '/docs/concept/sprites/'
G = REPO + '/graphics/pokemon/'
OUT = os.path.join(HERE, '..')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)

ITEMS = [('Cuyby ronde 3', S + 'cuyby/ronde3/anim_front.png', 0),
         ('evolutie ronde 1', S + 'cuyby_evo/ronde1/anim_front.png', 0),
         ('ronde 2 f1', S + 'cuyby_evo/ronde2/anim_front.png', 0),
         ('ronde 2 f2', S + 'cuyby_evo/ronde2/anim_front.png', 1)] + \
        [(n + ' (Gen 3)', G + n + '/anim_front_gba.png', 0) for n in ('piloswine', 'ninetales', 'furret')]


def measure(im):
    px = im.load()
    opaque = lambda x, y: 0 <= x < 64 and 0 <= y < 64 and px[x, y][3] > 0
    area = sum(1 for y in range(64) for x in range(64) if opaque(x, y))
    bb = im.getbbox()
    rim = [(x, y) for y in range(64) for x in range(64) if opaque(x, y) and
           any(not opaque(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    lum = lambda c: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
    dark = sum(1 for x, y in rim if lum(px[x, y]) < 100) / len(rim)
    black = sum(1 for x, y in rim if max(px[x, y][:3]) < 48) / len(rim)
    return area, (bb[2] - bb[0], bb[3] - bb[1]), dark, black


def sheet(out):
    sc, cw = 3, 64 * 3 + 16
    W, H = 8 + len(ITEMS) * cw, 32 + 64 * sc + 26 + 100
    img = Image.new('RGB', (W, H), (232, 236, 240))
    d = ImageDraw.Draw(img)
    d.text((8, 6), 'Cuyby-evolutie ronde 2: langhaarcavia als wandelende hooiberg, naast Cuyby ronde 3, ronde 1 en Gen 3',
           fill=(20, 20, 20), font=FB)
    for i, (lab, p, fr) in enumerate(ITEMS):
        sp = load(p, fr)
        x = 8 + i * cw
        big = sp.resize((64 * sc, 64 * sc), Image.NEAREST)
        img.paste(big, (x, 32), big)
        d.text((x, 32 + 194), lab, fill=(40, 40, 40), font=F)
        img.paste(sp, (x + 64, 32 + 64 * sc + 30), sp)
    d.text((8, 32 + 64 * sc + 30), '1x:', fill=(40, 40, 40), font=F)
    img.save(out)


if __name__ == '__main__':
    sheet(os.path.join(OUT, 'compare.png'))
    print('| | oppervlak | b x h | donkere buitenrand | waarvan zwart |')
    for lab, p, fr in ITEMS:
        a, (w, h), dk, bl = measure(load(p, fr))
        print('| %s | %d | %dx%d | %.2f | %.2f |' % (lab, a, w, h, dk, bl))
