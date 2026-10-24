"""Vergelijkingsvel ronde 5: eind vs ronde 5, oog-uitsneden 8x naast echte oogjes, 1x naast referenties."""
import os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.join(HERE, '../../../../../graphics/pokemon/')
LICHT, DONKER = (235, 235, 230, 255), (40, 40, 48, 255)

def pal(path):
    L = open(path).read().split('\n'); n = int(L[2])
    return [tuple(map(int, L[3 + i].split())) for i in range(n)]

def ref(name):
    d = G + name + '/'
    f = next(d + n for n in ('anim_front_gba.png', 'anim_front.png', 'front.png') if os.path.exists(d + n))
    pf = d + 'normal_gba.pal' if f.endswith('_gba.png') and os.path.exists(d + 'normal_gba.pal') else d + 'normal.pal'
    im = Image.open(f).convert('P') if Image.open(f).mode == 'P' else Image.open(f)
    P = pal(pf); a = im.load(); out = Image.new('RGBA', (64, 64)); o = out.load()
    for y in range(64):
        for x in range(64):
            i = a[x, y]
            if i: o[x, y] = P[i] + (255,)
    return out

def op(im, bg, z=1):
    t = Image.new('RGBA', im.size, bg); t.alpha_composite(im)
    return t.resize((im.width * z, im.height * z), Image.NEAREST)

eind = Image.open(os.path.join(HERE, '../eind/kolibrie.png')).convert('RGBA')
r5 = Image.open(os.path.join(HERE, 'kolibrie.png')).convert('RGBA')

W = 1400; H = 1500
V = Image.new('RGBA', (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(V)
# 1. eind en ronde 5 op 4x en 1x, licht en donker
d.text((8, 4), 'eind (links) en ronde 5 (rechts), 4x en 1x, licht en donker', fill=(0, 0, 0, 255))
x = 8
for im, lab in ((eind, 'eind'), (r5, 'ronde 5')):
    for bg in (LICHT, DONKER):
        V.paste(op(im, bg, 4), (x, 20)); V.paste(op(im, bg, 1), (x, 280)); V.paste(op(im, bg, 2), (x + 80, 280))
        d.text((x, 410), lab, fill=(0, 0, 0, 255)); x += 266 if bg == DONKER else 266
        x += 0
# 2. oog-uitsneden 8x
EYES = [('kolibrie eind', eind, 10, 26), ('kolibrie r5', r5, 10, 26),
        ('corviknight', 'corviknight', 24, 9), ('kilowattrel', 'kilowattrel', 20, 13), ('doduo', 'doduo', 37, 12),
        ('ducklett', 'ducklett', 24, 21), ('wingull', 'wingull', 36, 20), ('spearow', 'spearow', 25, 23),
        ('natu', 'natu', 30, 28), ('xatu', 'xatu', 31, 14), ('corvisquire', 'corvisquire', 29, 28),
        ('honchkrow', 'honchkrow', 30, 20), ('murkrow', 'murkrow', 36, 26), ('chatot', 'chatot', 25, 30),
        ('swellow', 'swellow', 14, 15), ('taillow', 'taillow', 22, 23), ('fearow', 'fearow', 49, 25),
        ('pidgeot', 'pidgeot', 13, 25), ('starly', 'starly', 28, 28)]
y0 = 430; d.text((8, y0), 'oog-uitsneden 9x9 op 8x (kolibrie eerst)', fill=(0, 0, 0, 255))
for i, (lab, src, cx, cy) in enumerate(EYES):
    im = src if isinstance(src, Image.Image) else ref(src)
    c = op(im, LICHT).crop((cx - 4, cy - 4, cx + 5, cy + 5)).resize((72, 72), Image.NEAREST)
    xx, yy = 8 + (i % 10) * 136, y0 + 16 + (i // 10) * 100
    V.paste(c, (xx, yy + 12)); d.text((xx, yy), lab, fill=(0, 0, 0, 255))
    c1 = op(im, LICHT).crop((cx - 12, cy - 12, cx + 13, cy + 13))
    V.paste(c1.resize((50, 50), Image.NEAREST), (xx + 78, yy + 12)); V.paste(c1, (xx + 78, yy + 64))
# 3. 1x (en 2x) naast referenties
REFS = ['swellow', 'taillow', 'honchkrow', 'murkrow', 'fearow', 'crobat', 'ho_oh', 'articuno', 'corviknight', 'kilowattrel']
y0 = 660
for row, bg in enumerate((LICHT, DONKER)):
    yy = y0 + row * 400
    d.text((8, yy), '1x (boven) en 2x (onder): eind, ronde 5, ' + ', '.join(REFS), fill=(0, 0, 0, 255))
    ims = [eind, r5] + [ref(n) for n in REFS]
    for i, im in enumerate(ims):
        V.paste(op(im, bg, 1), (8 + i * 68, yy + 16))
        V.paste(op(im, bg, 2), (8 + (i % 6) * 132, yy + 90 + (i // 6) * 132))
V.save(os.path.join(HERE, 'vel.png'))
