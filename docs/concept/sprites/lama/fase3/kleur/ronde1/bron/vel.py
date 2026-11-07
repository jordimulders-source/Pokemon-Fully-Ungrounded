"""Vel kleur ronde 1 lama fase 3: lama3.png op 4x (licht en donker) naast de onderlaag, 1x op licht/donker, en op 2x en 1x
naast fase 2 en vijf Gen 3-studiesprites (Emerald anim_front.png, bovenste frame). Draaien: python3 vel.py -> ../vel_ronde1.png"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
ROOT = os.path.join(HERE, *['..'] * 8)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
LICHT, DONKER = (248, 248, 244, 255), (44, 44, 56, 255)
def on(im, bg, s=1):
    b = Image.new('RGBA', im.size, bg); b.alpha_composite(im.convert('RGBA')); return b.resize((im.width * s, im.height * s), Image.NEAREST)
spr = Image.open(os.path.join(OUT, 'lama3.png')).convert('RGBA')
W = Image.new('RGBA', (1320, 700), LICHT); d = ImageDraw.Draw(W)
d.text((10, 6), 'Lama fase 3, kleur ronde 1 (silhouet ronde 2 bevroren, alpha-diff 0)', fill=(0, 0, 0), font=F)
W.paste(Image.open(os.path.join(ROOT, 'docs/concept/sprites/lama/fase3/silhouet/onderlaag_256.png')).convert('RGBA'), (10, 30))
d.text((10, 290), 'onderlaag (poppetje W3)', fill=(0, 0, 0), font=F)
W.paste(on(spr, LICHT, 4), (280, 30)); W.paste(on(spr, DONKER, 4), (550, 30))
d.text((280, 290), 'ronde 1, 4x licht', fill=(0, 0, 0), font=F); d.text((550, 290), 'ronde 1, 4x donker', fill=(0, 0, 0), font=F)
W.paste(on(spr, LICHT), (830, 40)); W.paste(on(spr, DONKER), (910, 40)); d.text((830, 110), '1x licht / donker', fill=(0, 0, 0), font=F)
refs = [('lama fase 2', 'docs/concept/sprites/lama/fase2/af/lama.png'), ('entei', 'graphics/pokemon/entei/anim_front.png'),
        ('arcanine', 'graphics/pokemon/arcanine/anim_front.png'), ('tauros', 'graphics/pokemon/tauros/anim_front.png'),
        ('hariyama', 'graphics/pokemon/hariyama/anim_front.png'), ('machamp', 'graphics/pokemon/machamp/anim_front.png')]
x = 10
for n, p in [('fase 3 r1', None)] + refs:
    if p is None: im = spr
    else:
        raw = Image.open(os.path.join(ROOT, p)).crop((0, 0, 64, 64)); im = raw.convert('RGBA')
        if raw.mode == 'P': im.putalpha(Image.fromarray(((np.array(raw) != 0) * 255).astype('uint8')))
    W.paste(on(im, LICHT, 2), (x, 330)); W.paste(on(im, DONKER, 2), (x, 466))
    W.paste(on(im, LICHT), (x + 30, 604)); d.text((x, 674), n, fill=(0, 0, 0), font=F); x += 140
d.text((990, 330), '2x licht (boven), 2x donker,\n1x licht (onder)', fill=(0, 0, 0), font=F)
W.convert('RGB').save(os.path.join(OUT, 'vel_ronde1.png'))
