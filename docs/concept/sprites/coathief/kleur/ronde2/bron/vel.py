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
put(X4(co), 0, 0, LIGHT, 'Coathief kleur ronde 2, 4x (licht)')
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
# ronde 1 naast ronde 2: kop + voorpoten op 8x
r1 = Image.open(os.path.join(H, '../../ronde1/coathief.png')).convert('RGBA')
v = Image.new('RGBA', (2 * 256 + 20, 272 + 20), LIGHT); dv = ImageDraw.Draw(v)
for i, (n, im) in enumerate((('ronde 1', r1), ('ronde 2', co))):
    v.alpha_composite(im.crop((2, 30, 34, 64)).resize((256, 272), Image.NEAREST), (i * 276, 0))
    dv.text((i * 276, 275), n, fill=(30, 30, 30, 255))
v.save(os.path.join(H, '../r1_vs_r2_kop_poten.png'))
