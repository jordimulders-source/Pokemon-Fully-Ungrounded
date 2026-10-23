"""Vergelijkingsvellen voor nachtaap ronde 7 en Cuyby ronde 3 (modeltekening, vorige ronde, nieuwe ronde
f1/f2 en echte Gen 3-sprites, op 3x en 1x).

Vanuit de repo-root: python3 docs/concept/sprites/nachtaap/ronde7/bron/vellen.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../../..'))
S = REPO + '/docs/concept/sprites/'
G = REPO + '/graphics/pokemon/'
O = REPO + '/docs/concept/ontwerp/'
BG = (232, 236, 240)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)


def load(path, frame=0):
    im = Image.open(path)
    if path.endswith('_gba.png'):
        pal = path.replace('anim_front_gba.png', 'normal_gba.pal')
    else:
        pal = os.path.join(os.path.dirname(path), 'normal.pal')
    lines = open(pal).read().split('\n')[3:]
    cols = [tuple(int(v) for v in l.split()) for l in lines if l.strip()]
    im = im.crop((0, frame * 64, 64, frame * 64 + 64))
    out = Image.new('RGBA', (64, 64))
    out.putdata([(0, 0, 0, 0) if i == 0 else cols[i] + (255,) for i in im.getdata()])
    return out


def concept(path):
    im = Image.open(path).convert('RGB').crop((16, 40, 272, 296))
    return im.resize((192, 192), Image.LANCZOS)


def sheet(concept_path, items, out, title):
    sc = 3
    cw = 64 * sc + 16
    W = 8 + (1 + len(items)) * cw
    H = 32 + 64 * sc + 26 + 100
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((8, 6), title, fill=(20, 20, 20), font=FB)
    img.paste(concept(concept_path), (8, 32))
    d.text((8, 32 + 194), 'modeltekening', fill=(40, 40, 40), font=F)
    for i, (lab, p, fr) in enumerate(items):
        sp = load(p, fr)
        x = 8 + (i + 1) * cw
        big = sp.resize((64 * sc, 64 * sc), Image.NEAREST)
        img.paste(big, (x, 32), big)
        d.text((x, 32 + 194), lab, fill=(40, 40, 40), font=F)
    y = 32 + 64 * sc + 30
    d.text((8, y), '1x zoals in het spel:', fill=(40, 40, 40), font=F)
    for i, (lab, p, fr) in enumerate(items):
        sp = load(p, fr)
        img.paste(sp, (8 + (i + 1) * cw + 64, y), sp)
    img.save(out)


if __name__ == '__main__':
    na = S + 'nachtaap/'
    sheet(O + 'nachtaap/concept_B.png',
          [('ronde 6', na + 'ronde6/anim_front.png', 0), ('ronde 7 f1', na + 'ronde7/anim_front.png', 0),
           ('ronde 7 f2', na + 'ronde7/anim_front.png', 1)] +
          [(n + ' (Gen 3)', G + n + '/anim_front_gba.png', 0) for n in ['aipom', 'espeon', 'umbreon', 'abra', 'murkrow']],
          na + 'ronde7/compare.png', 'Nachtaap ronde 7: pixel-over van concept B, per lichaamsdeel met de hand')
    cu = S + 'cuyby/'
    sheet(O + 'cuyby/concept_C2.png',
          [('ronde 2', cu + 'ronde2/anim_front.png', 0), ('ronde 3 f1', cu + 'ronde3/anim_front.png', 0),
           ('ronde 3 f2', cu + 'ronde3/anim_front.png', 1)] +
          [(n + ' (Gen 3)', G + n + '/anim_front_gba.png', 0) for n in ['teddiursa', 'vulpix', 'skitty', 'jigglypuff', 'whismur']],
          cu + 'ronde3/compare.png', 'Cuyby ronde 3: polijstronde (zelfde silhouet, schaduw/omlijning/ogen volgens de spritingregels)')
