"""Vel kleur ronde 3 lama fase 3: 4x licht/donker naast de onderlaag, 1x licht/donker; 2x en 1x naast ronde 2b, fase 2 en
Gen 3-referenties (snuit-binnenlijn: Girafarig, Stantler); kop 8x naast dezelfde uitsnede van de onderlaag. -> ../vel_ronde3.png"""
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
d.text((10, 6), 'Lama fase 3, kleur ronde 3 (kop ±1,25x groter dan het silhouet; overige zones 0 px diff met 2b)', fill=(0, 0, 0), font=F)
W.alpha_composite(on(ond, LICHT), (10, 30)); d.text((10, 290), 'onderlaag (poppetje W3)', fill=(0, 0, 0), font=F)
W.paste(on(spr, LICHT, 4), (280, 30)); W.paste(on(spr, DONKER, 4), (550, 30))
d.text((280, 290), 'ronde 3, 4x licht', fill=(0, 0, 0), font=F); d.text((550, 290), 'ronde 3, 4x donker', fill=(0, 0, 0), font=F)
W.paste(on(spr, LICHT), (830, 40)); W.paste(on(spr, DONKER), (910, 40)); d.text((830, 110), '1x licht / donker', fill=(0, 0, 0), font=F)
refs = [('ronde 3', spr), ('ronde 2b', load('docs/concept/sprites/lama/fase3/kleur/ronde2b/lama3.png')),
        ('lama fase 2', load('docs/concept/sprites/lama/fase2/af/lama.png')), ('girafarig', load('graphics/pokemon/girafarig/anim_front.png')),
        ('stantler', load('graphics/pokemon/stantler/anim_front.png')), ('entei', load('graphics/pokemon/entei/anim_front.png')),
        ('tauros', load('graphics/pokemon/tauros/anim_front.png'))]
x = 10
for n, im in refs:
    W.paste(on(im, LICHT, 2), (x, 320)); W.paste(on(im, DONKER, 2), (x, 456))
    W.paste(on(im, LICHT), (x + 30, 594)); d.text((x, 662), n, fill=(0, 0, 0), font=F); x += 140
d.text((1000, 320), '2x licht, 2x donker,\n1x licht', fill=(0, 0, 0), font=F)
# kop 8x: x12-33, y0-25
box = (10, 0, 32, 26); s = 8
W.alpha_composite(on(ond.crop((box[0] * 4, 0, box[2] * 4, box[3] * 4)).resize(((box[2] - box[0]) * s, box[3] * s), Image.LANCZOS), LICHT), (10, 690))
W.paste(on(Image.open(os.path.join(HERE, '../../ronde2b/lama3.png')).convert('RGBA').crop(box), LICHT, s), (200, 690))
W.paste(on(spr.crop(box), LICHT, s), (390, 690))
d.text((10, 900), 'kop 8x: onderlaag', fill=(0, 0, 0), font=F); d.text((200, 900), 'ronde 2b', fill=(0, 0, 0), font=F); d.text((390, 900), 'ronde 3', fill=(0, 0, 0), font=F)
W.convert('RGB').save(os.path.join(OUT, 'vel_ronde3.png'))
# foto-uitsnede lamakop (referenties/foto1) naast de kop 8x
W = Image.open(os.path.join(OUT, 'vel_ronde3.png')).convert('RGBA'); d = ImageDraw.Draw(W)
foto = Image.open(os.path.join(ROOT, 'docs/concept/sprites/lama/referenties/foto1_lama_driekwart_POSE.png')).convert('RGBA').crop((95, 55, 185, 160)).resize((180, 210), Image.LANCZOS)
W.paste(foto, (580, 690)); d.text((580, 900), 'foto1 (lamakop)', fill=(0, 0, 0), font=F)
W.convert('RGB').save(os.path.join(OUT, 'vel_ronde3.png'))
