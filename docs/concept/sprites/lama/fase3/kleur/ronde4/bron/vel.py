"""Vel kleur ronde 4 lama fase 3: 4x licht/donker naast de onderlaag, 1x licht/donker; 2x en 1x naast ronde 2, fase 2 en
Gen 3-referenties (snuit-binnenlijn: Girafarig, Stantler); kop 8x naast dezelfde uitsnede van de onderlaag. -> ../vel_ronde4.png"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
ROOT = os.path.join(HERE, *['..'] * 8)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
LICHT, DONKER = (248, 248, 244, 255), (44, 44, 56, 255)
def on(im, bg, s=1):
    b = Image.new('RGBA', im.size, bg); b.alpha_composite(im.convert('RGBA')); return b.resize((im.width * s, im.height * s), Image.NEAREST)
def load(p):
    raw = Image.open(os.path.join(ROOT, p)).crop((0, 0, 64, 64)); im = raw.convert('RGBA')
    if raw.mode == 'P': im.putalpha(Image.fromarray(((np.array(raw) != 0) * 255).astype('uint8')))
    return im
spr = Image.open(os.path.join(OUT, 'lama3.png')).convert('RGBA')
ond = Image.open(os.path.join(ROOT, 'docs/concept/sprites/lama/fase3/silhouet/onderlaag_256.png')).convert('RGBA')
W = Image.new('RGBA', (1300, 960), LICHT); d = ImageDraw.Draw(W)
d.text((10, 6), 'Lama fase 3, kleur ronde 4 (kop overgetrokken van kopbron, 1,25x; rest 0 px diff met 2b)', fill=(0, 0, 0), font=F)
W.alpha_composite(on(ond, LICHT), (10, 30)); d.text((10, 290), 'onderlaag (poppetje W3)', fill=(0, 0, 0), font=F)
W.paste(on(spr, LICHT, 4), (280, 30)); W.paste(on(spr, DONKER, 4), (550, 30))
d.text((280, 290), 'ronde 4, 4x licht', fill=(0, 0, 0), font=F); d.text((550, 290), 'ronde 4, 4x donker', fill=(0, 0, 0), font=F)
W.paste(on(spr, LICHT), (830, 40)); W.paste(on(spr, DONKER), (910, 40)); d.text((830, 110), '1x licht / donker', fill=(0, 0, 0), font=F)
refs = [('ronde 4', spr), ('ronde 2b', load('docs/concept/sprites/lama/fase3/kleur/ronde2b/lama3.png')),
        ('lama fase 2', load('docs/concept/sprites/lama/fase2/af/lama.png')), ('girafarig', load('graphics/pokemon/girafarig/anim_front.png')),
        ('stantler', load('graphics/pokemon/stantler/anim_front.png')), ('entei', load('graphics/pokemon/entei/anim_front.png')),
        ('tauros', load('graphics/pokemon/tauros/anim_front.png'))]
x = 10
for n, im in refs:
    W.paste(on(im, LICHT, 2), (x, 320)); W.paste(on(im, DONKER, 2), (x, 456))
    W.paste(on(im, LICHT), (x + 30, 594)); d.text((x, 662), n, fill=(0, 0, 0), font=F); x += 140
d.text((1000, 320), '2x licht, 2x donker,\n1x licht', fill=(0, 0, 0), font=F)
# kop 8x: overtrekvel-render | kop_kleur_64 | ronde 4 (x8-35, y0-25)
KB = os.path.join(ROOT, 'docs/concept/sprites/lama/fase3/kleur/kopbron')
ov = Image.open(os.path.join(KB, 'kop_overtrekvel.png')).convert('RGBA'); ov = ov.crop((0, 0, ov.width // 2, ov.height))
ov = ov.resize((int(ov.width * 208 / ov.height), 208), Image.LANCZOS); W.alpha_composite(ov, (10, 690))
box = (8, 0, 36, 26); s = 8
kk = Image.open(os.path.join(KB, 'kop_kleur_64.png')).convert('RGBA').crop(box).resize((28 * s, 26 * s), Image.NEAREST)
x1 = 20 + ov.width; W.alpha_composite(kk, (x1, 690)); W.paste(on(spr.crop(box), LICHT, s), (x1 + 234, 690))
d.text((10, 902), 'overtrekvel (render model, kop 1,25x)', fill=(0, 0, 0), font=F); d.text((x1, 902), 'kop_kleur_64', fill=(0, 0, 0), font=F)
d.text((x1 + 234, 902), 'ronde 4', fill=(0, 0, 0), font=F)
W.convert('RGB').save(os.path.join(OUT, 'vel_ronde4.png'))
