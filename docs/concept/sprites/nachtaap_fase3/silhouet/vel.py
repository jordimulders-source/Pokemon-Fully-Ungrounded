"""Vel silhouet ronde 1: onderlaag | silhouet 4x | omtrek over de onderlaag | 1x naast Gen 3 en fase 1/2."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '../../../../..')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
S = np.array([[c == '#' for c in l.strip()] for l in open(os.path.join(HERE, 'ronde1.txt')) if l.strip()])
def sil(m, col=(40, 30, 50)):
    im = np.full((64, 64, 3), 255, np.uint8); im[m] = col; return Image.fromarray(im)
und = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGBA')
bg = Image.new('RGBA', und.size, 'white'); bg.alpha_composite(und); und = bg.convert('RGB')
o = np.array(und); big = np.array(sil(S).resize((256, 256), Image.NEAREST))[..., 0] < 128
from scipy import ndimage as nd
rand = big & ~nd.binary_erosion(big, iterations=2)
o[rand] = (220, 30, 60); ov = Image.fromarray(o)
im = Image.new('RGB', (12 + 266 * 4, 44 + 290 + 150), 'white'); d = ImageDraw.Draw(im)
d.text((12, 12), 'Nachtaap fase 3: silhouet ronde 1 (model overgetrokken op de 50%-dekking, alleen korrels weg)', font=FB, fill=(30, 30, 30))
for i, (t, lab) in enumerate(((und, 'onderlaag (model)'), (sil(S).resize((256, 256), Image.NEAREST), f'silhouet: {int(S.sum())} px'),
                              (ov, 'omtrek over het model'), (sil(S).resize((128, 128), Image.NEAREST), '2x'))):
    im.paste(t, (12 + 266 * i, 44)); d.text((16 + 266 * i, 304), lab, font=F, fill=(60, 60, 60))
y = 334; x = 12
def gba(n):
    p = os.path.join(ROOT, f'graphics/pokemon/{n}/anim_front_gba.png')
    a = Image.open(p); idx = np.array(a)[:64]; rgba = np.array(a.convert('RGBA'))[:64]; rgba[idx == 0, 3] = 0
    b = Image.new('RGBA', (64, 64), 'white'); b.alpha_composite(Image.fromarray(rgba)); return b.convert('RGB'), int((idx != 0).sum())
def eigen(p):
    a = Image.open(os.path.join(HERE, p)).convert('RGBA'); b = Image.new('RGBA', (64, 64), 'white'); b.alpha_composite(a)
    return b.convert('RGB'), int((np.array(a)[:64, :, 3] > 0).sum())
refs = [(sil(S), f'fase 3: {int(S.sum())}')]
for p, lab in (('../../nachtaap/ronde12/variant_spiraal/anim_front.png', 'fase 1'), ('../../nachtaap_evo/af/nachtaap_evo.png', 'fase 2')):
    try:
        t, n = eigen(p); refs.append((t.crop((0, 0, 64, 64)), f'{lab}: {n}'))
    except Exception as e: pass
for n in ('alakazam', 'medicham', 'deoxys', 'ambipom' if os.path.exists(os.path.join(ROOT, 'graphics/pokemon/ambipom/anim_front_gba.png')) else 'primeape', 'infernape' if os.path.exists(os.path.join(ROOT, 'graphics/pokemon/infernape/anim_front_gba.png')) else 'slaking'):
    try:
        t, k = gba(n); refs.append((t, f'{n}: {k}'))
    except Exception: pass
for t, lab in refs:
    im.paste(t, (x, y)); d.text((x, y + 70), lab, font=F, fill=(60, 60, 60)); x += 130
im.save(os.path.join(HERE, 'vel_ronde1.png'))
open(os.path.join(HERE, 'ronde1_1x.png'), 'wb'); sil(S).save(os.path.join(HERE, 'ronde1_1x.png'))
