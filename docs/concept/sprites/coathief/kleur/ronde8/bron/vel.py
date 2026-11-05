"""Maakt ../vel.png: Coathief 4x en 1x op licht en donker, naast onderlaag, olinguito (fase 1) en 5 Gen 3-sprites."""
import os
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(H, '../../../../../../..')
S = os.path.join(H, '../../..')
co = Image.open(os.path.join(H, '../coathief.png')).convert('RGBA')
ol = Image.open(os.path.join(S, '../olinguito_v2/af/olinguito.png')).convert('RGBA')
ond = Image.open(os.path.join(S, 'silhouet/onderlaag_b1c_256.png')).convert('RGBA')
refs = ['linoone', 'furret', 'mightyena', 'houndour', 'zigzagoon']
def tr(n):
    im = Image.open(os.path.join(ROOT, 'graphics/pokemon', n, 'anim_front_gba.png')).crop((0, 0, 64, 64)); im.info['transparency'] = 0
    return im.convert('RGBA')
R = [tr(n) for n in refs]
LIGHT = (236, 236, 230, 255); DARK = (40, 40, 52, 255)
o = Image.new('RGBA', (1340, 900), LIGHT); d = ImageDraw.Draw(o)
def put(im, x, y, bg=None, l=None):
    if bg:
        b = Image.new('RGBA', im.size, bg); b.alpha_composite(im); im = b
    o.paste(im, (x, y), im)
    if l: d.text((x, y + im.size[1] + 3), l, fill=(30, 30, 30, 255))
X4 = lambda im: im.resize((256, 256), Image.NEAREST)
put(X4(co), 0, 0, LIGHT, 'Coathief kleur ronde 8, 4x (licht)')
put(X4(co), 266, 0, DARK, '4x (donker)')
put(ond, 532, 0, (255, 255, 255, 255), 'onderlaag (B1, kop C)')
put(X4(ol), 798, 0, LIGHT, 'olinguito (fase 1, goedgekeurd), 4x')
put(co, 1070, 10, LIGHT, 'Coathief 1x'); put(co, 1150, 10, DARK, '')
put(ol, 1070, 110, LIGHT, 'olinguito 1x'); put(ol, 1150, 110, DARK, '')
for i, (n, r) in enumerate(zip(refs, R)):
    put(X4(r), i * 266, 290, LIGHT, n + ' (Gen 3), 4x')
row = [('Coathief', co), ('olinguito', ol)] + list(zip(refs, R))
for i, (n, r) in enumerate(row):
    put(r, 10 + i * 80, 590, LIGHT, n); put(r, 10 + i * 80, 690, DARK, '')
# lijn naast elkaar op 2x
put(ol.resize((128, 128), Image.NEAREST), 620, 590, LIGHT, 'fase 1 -> fase 2 (2x)')
put(co.resize((128, 128), Image.NEAREST), 760, 590, LIGHT, '')
put(ol.resize((128, 128), Image.NEAREST), 620, 740, DARK, '')
put(co.resize((128, 128), Image.NEAREST), 760, 740, DARK, '')
o.save(os.path.join(H, '../vel.png'))
# uitsneden 8x: kop + voorpoten, staartkrul
u = Image.new('RGBA', (32 * 8 + 10 + 16 * 8, 34 * 8), LIGHT)
k = co.crop((2, 30, 34, 64)).resize((256, 272), Image.NEAREST); u.alpha_composite(k, (0, 0))
s = co.crop((44, 0, 60, 34)).resize((128, 272), Image.NEAREST); u.alpha_composite(s, (266, 0))
u.save(os.path.join(H, '../uitsnede.png'))
# uitsnede voorpoten op 8x: onderlaag | 6d | 6e, licht en donker, plus 1x
Z = 8; W, Hh = 22 * Z, 17 * Z
RR = [('ronde 7b', Image.open(os.path.join(H, '../../ronde7b/coathief.png')).convert('RGBA')), ('ronde 8', co)]
v = Image.new('RGBA', (3 * (W + 10), 2 * Hh + 120), LIGHT); dv = ImageDraw.Draw(v)
wb = Image.new('RGBA', (W, Hh), (255, 255, 255, 255)); wb.alpha_composite(ond.crop((56, 184, 144, 252)).resize((W, Hh)))
v.paste(wb, (0, 0)); dv.text((0, Hh + 4), 'onderlaag', fill=(30, 30, 30))
for i, (n, im) in enumerate(RR):
    for j, bg in enumerate((LIGHT, DARK)):
        b = Image.new('RGBA', (64, 64), bg); b.alpha_composite(im)
        v.paste(b.crop((14, 46, 36, 63)).resize((W, Hh), Image.NEAREST), ((i + 1) * (W + 10), j * (Hh + 10)))
        v.paste(b, ((i + 1) * (W + 10) + j * 70, 2 * Hh + 40))
    dv.text(((i + 1) * (W + 10), 2 * Hh + 22), n, fill=(30, 30, 30))
v.save(os.path.join(H, '../onderlaag_7b_8_voorpoten.png'))
