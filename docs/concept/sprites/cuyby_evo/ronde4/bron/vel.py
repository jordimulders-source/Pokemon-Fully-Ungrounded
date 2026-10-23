"""Vergelijkingsvel en metingen voor de Cuyby-evolutie ronde 4: ronde 3 tegenover ronde 4 (beide frames), naast
Cuyby en drie echte Gen 3-sprites, op 3x en 1x (licht en donker).

Vanuit de repo-root: python3 docs/concept/sprites/cuyby_evo/ronde4/bron/vel.py
Schrijft compare.png en drukt de metingen af. De Gen 3-sprites komen uit ronde3/keuring/gen3 (haal_gen3.py).
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../../../../..'))
sys.path.insert(0, os.path.join(REPO, 'docs/concept/sprites/nachtaap/ronde7/bron'))
sys.path.insert(0, os.path.join(REPO, 'docs/concept/sprites/cuyby_evo/ronde3/keuring'))
from vellen import load
from keuring import measure

S = REPO + '/docs/concept/sprites/'
G3 = S + 'cuyby_evo/ronde3/keuring/gen3/'
OUT = os.path.join(HERE, '..')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)

ITEMS = [('ronde 3 f1', S + 'cuyby_evo/ronde3/anim_front.png', 0),
         ('ronde 4 f1', S + 'cuyby_evo/ronde4/anim_front.png', 0),
         ('ronde 4 f2', S + 'cuyby_evo/ronde4/anim_front.png', 1),
         ('Cuyby ronde 3', S + 'cuyby/ronde3/anim_front.png', 0)] + \
        [(n, G3 + n + '/anim_front_gba.png', 0) for n in ('piloswine', 'mareep', 'linoone')]


def sheet(out):
    sc, cw = 3, 64 * 3 + 16
    W = 8 + len(ITEMS) * cw
    img = Image.new('RGB', (W, 32 + 64 * sc + 26 + 72), (232, 236, 240))
    d = ImageDraw.Draw(img)
    d.text((8, 6), 'Cuyby-evolutie ronde 3 tegenover ronde 4 (snuit kleiner, haar verder over het gezicht, '
                   'open randen dicht), naast Cuyby en Gen 3 (3x en 1x)', fill=(20, 20, 20), font=FB)
    for i, (lab, p, fr) in enumerate(ITEMS):
        sp = load(p, fr)
        x, y0 = 8 + i * cw, 32
        big = sp.resize((64 * sc, 64 * sc), Image.NEAREST)
        img.paste(big, (x, y0), big)
        d.text((x, y0 + 194), lab, fill=(40, 40, 40), font=F)
        donker = Image.new('RGB', (64, 64), (60, 70, 80))
        donker.paste(sp, (0, 0), sp)
        img.paste(sp, (x + 20, y0 + 64 * sc + 24), sp)
        img.paste(donker, (x + 100, y0 + 64 * sc + 24))
    img.save(out)


if __name__ == '__main__':
    sheet(os.path.join(OUT, 'compare.png'))
    print('| sprite | oppervlak | b x h | zwart rand | zwart lichtkant | zwart schaduwkant | kleuren |')
    print('|---|---|---|---|---|---|---|')
    for lab, p, fr in ITEMS:
        a, (w, h), bl, li, sh, c = measure(load(p, fr))
        print('| %s | %d | %dx%d | %.2f | %.2f | %.2f | %d |' % (lab, a, w, h, bl, li, sh, c))
