"""Keuringsvel en metingen voor de Cuyby-evolutie (onafhankelijke keuring van ronde 3).
Vanuit de repo-root: python3 docs/concept/sprites/cuyby_evo/ronde3/keuring/keuring.py
Schrijft keuring/vel_3x.png (3x + 1x op licht en donker) en keuring/vel_1x.png (alleen 1x) en drukt per
sprite de metingen af.
'zwart lichtkant/schaduwkant': aandeel zwart (max RGB < 48) onder de randpixels waarvan de lege buur
alleen links/boven ligt (lichtkant) tegenover alleen rechts/onder (schaduwkant).
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
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
EIGEN = [('evo ronde 3 f1', S + 'cuyby_evo/ronde3/anim_front.png', 0),
         ('evo ronde 3 f2', S + 'cuyby_evo/ronde3/anim_front.png', 1),
         ('Cuyby ronde 3', S + 'cuyby/ronde3/anim_front.png', 0)]
NAMEN = ['mareep', 'swinub', 'piloswine', 'linoone', 'furret', 'teddiursa', 'ninetales', 'vulpix',
         'eevee', 'skitty', 'zigzagoon', 'whismur', 'swablu', 'mawile']
# echte Gen 3-sprites uit de git-geschiedenis (haal_gen3.py); de huidige graphics/pokemon/ is nieuwer
ECHT = [(n, os.path.join(HERE, 'gen3', n, 'anim_front_gba.png'), 0) for n in NAMEN]


def measure(im):
    px = im.load()
    op = lambda x, y: 0 <= x < 64 and 0 <= y < 64 and px[x, y][3] > 0
    area = sum(op(x, y) for y in range(64) for x in range(64))
    bb = im.getbbox()
    rim, lit, sh = [], [], []
    for y in range(64):
        for x in range(64):
            if not op(x, y):
                continue
            ul = not op(x - 1, y) or not op(x, y - 1)
            dr = not op(x + 1, y) or not op(x, y + 1)
            if ul or dr:
                b = max(px[x, y][:3]) < 48
                rim.append(b)
                if ul and not dr:
                    lit.append(b)
                elif dr and not ul:
                    sh.append(b)
    f = lambda l: sum(l) / max(len(l), 1)
    cols = len(set(px[x, y][:3] for y in range(64) for x in range(64) if op(x, y)))
    return area, (bb[2] - bb[0], bb[3] - bb[1]), f(rim), f(lit), f(sh), cols


def vel(items, out, sc, titel, per_rij=6):
    cw = max(64 * sc, 140) + 12
    rh = 64 * sc + 18 + 64 + 8
    rows = (len(items) + per_rij - 1) // per_rij
    img = Image.new('RGB', (8 + per_rij * cw, 30 + rows * rh), (232, 236, 240))
    d = ImageDraw.Draw(img)
    d.text((8, 6), titel, fill=(20, 20, 20), font=FB)
    for i, (lab, p, fr) in enumerate(items):
        sp = load(p, fr)
        x, y = 8 + (i % per_rij) * cw, 30 + (i // per_rij) * rh
        if sc > 1:
            big = sp.resize((64 * sc, 64 * sc), Image.NEAREST)
            img.paste(big, (x, y), big)
        d.text((x, y + 64 * sc + 2), lab, fill=(40, 40, 40), font=F)
        donker = Image.new('RGB', (64, 64), (60, 70, 80))
        donker.paste(sp, (0, 0), sp)
        img.paste(sp, (x, y + 64 * sc + 16), sp)
        img.paste(donker, (x + 68, y + 64 * sc + 16))
    img.save(out)


if __name__ == '__main__':
    alle = EIGEN + ECHT
    vel(alle, os.path.join(HERE, 'vel_3x.png'), 3,
        'Keuring Cuyby-evolutie ronde 3: eigen werk (eerste 3) naast 14 echte Gen 3-sprites, 3x en 1x')
    vel(alle, os.path.join(HERE, 'vel_1x.png'), 1, 'Alleen 1x (licht en donker)', per_rij=6)
    print('| sprite | oppervlak | b x h | zwart rand | zwart lichtkant | zwart schaduwkant | kleuren |')
    print('|---|---|---|---|---|---|---|')
    for lab, p, fr in alle:
        a, (w, h), bl, li, sh, c = measure(load(p, fr))
        print('| %s | %d | %dx%d | %.2f | %.2f | %.2f | %d |' % (lab, a, w, h, bl, li, sh, c))
