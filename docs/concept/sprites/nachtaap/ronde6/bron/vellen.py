"""Vergelijkingsvel + blinde rij voor nachtaap ronde 6 en Cuyby ronde 2.

Vanuit de repo-root: python3 docs/concept/sprites/nachtaap/ronde6/bron/vellen.py
"""
import os, random
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
    pal = None
    if path.endswith('_gba.png'):
        pal = path.replace('anim_front_gba.png', 'normal_gba.pal')
    elif os.path.exists(os.path.join(os.path.dirname(path), 'normal.pal')):
        pal = os.path.join(os.path.dirname(path), 'normal.pal')
    lines = open(pal).read().split('\n')[3:]
    cols = [tuple(int(v) for v in l.split()) for l in lines if l.strip()]
    im = im.crop((0, frame * 64, 64, frame * 64 + 64))
    out = Image.new('RGBA', (64, 64))
    out.putdata([(0, 0, 0, 0) if i == 0 else cols[i] + (255,) for i in im.getdata()])
    return out


def concept(name, key):
    im = Image.open(O + name + '/concept_%s.png' % key).convert('RGB').crop((16, 40, 272, 296))
    return im.resize((192, 192), Image.LANCZOS)


def compare(name, key, cand, refs, out, title):
    sc = 3
    cw = 64 * sc + 64 + 16
    items = [('ronde f1', cand, 0), ('ronde f2', cand, 1)] + [(r, G + r + '/anim_front_gba.png', 0) for r in refs]
    cols = 1 + len(items)
    W = cols * cw + 20
    H = 64 * sc + 60 + 120
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((8, 6), title, fill=(20, 20, 20), font=FB)
    img.paste(concept(name, key), (8, 32))
    d.text((8, 32 + 194), 'modeltekening concept ' + key, fill=(40, 40, 40), font=F)
    for i, (lab, p, fr) in enumerate(items):
        sp = load(p, fr)
        x = 8 + (i + 1) * cw
        big = sp.resize((64 * sc, 64 * sc), Image.NEAREST)
        img.paste(big, (x, 32), big)
        img.paste(sp, (x + 64 * sc + 6, 32 + 64 * sc - 64), sp)
        d.text((x, 32 + 194), lab + (' (Gen 3)' if p.startswith(G) else ''), fill=(40, 40, 40), font=F)
    # rij op 1x naast elkaar, zoals in het spel
    y = 32 + 64 * sc + 40
    d.text((8, y - 14), '1x naast elkaar (kandidaat eerst)', fill=(40, 40, 40), font=F)
    for i, (lab, p, fr) in enumerate(items):
        if fr:
            continue
        sp = load(p, 0)
        img.paste(sp, (8 + i * 70, y), sp)
    img.save(out)


def blind(cand, names, out, seed):
    items = [(G + n + '/anim_front_gba.png', n) for n in names]
    rnd = random.Random(seed)
    pos = rnd.randrange(len(items) + 1)
    items.insert(pos, (cand, 'KANDIDAAT'))
    sc = 2
    per = 7
    rows = (len(items) + per - 1) // per
    img = Image.new('RGB', (per * 64 * sc + 20, rows * (64 * sc + 14) + 20), (152, 208, 136))
    d = ImageDraw.Draw(img)
    for i, (p, n) in enumerate(items):
        sp = load(p, 0).resize((64 * sc, 64 * sc), Image.NEAREST)
        x = 10 + (i % per) * 64 * sc
        y = 10 + (i // per) * (64 * sc + 14)
        img.paste(sp, (x, y + 12), sp)
        d.text((x + 2, y), str(i + 1), fill=(0, 0, 0), font=F)
    img.save(out)
    return pos + 1, [n for _, n in items]


if __name__ == '__main__':
    na = S + 'nachtaap/ronde6/'
    cu = S + 'cuyby/ronde2/'
    compare('nachtaap', 'B', na + 'anim_front.png', ['aipom', 'abra', 'natu', 'ralts'], na + 'compare.png',
            'Nachtaap fase 1, ronde 6: met de hand op het Aipom/Abra-skelet, naar concept B')
    compare('cuyby', 'C2', cu + 'anim_front.png', ['jigglypuff', 'skitty', 'whismur', 'swablu'], cu + 'compare.png',
            'Cuyby fase 1, ronde 2: met de hand op het Jigglypuff/Skitty-skelet, naar concept C2')
    print('nachtaap', blind(na + 'anim_front.png', ['treecko', 'torchic', 'mudkip', 'aipom', 'abra', 'natu', 'ralts', 'meditite',
                                                    'spoink', 'smoochum', 'teddiursa', 'skitty'], na + 'blindtest.png', 61))
    print('cuyby', blind(cu + 'anim_front.png', ['jigglypuff', 'igglybuff', 'skitty', 'whismur', 'swablu', 'mareep', 'zigzagoon',
                                                 'sentret', 'teddiursa', 'azurill', 'snubbull', 'clefairy'], cu + 'blindtest.png', 62))
