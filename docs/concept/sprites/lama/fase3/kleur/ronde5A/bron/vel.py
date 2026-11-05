"""Gezamenlijk vel ronde 5 (A en B): 1x/2x/4x licht en donker naast 4b en fase 2; kop 8x (A, B, render B); oog 12x naast
Slaking/Slakoth (oogstudie). -> ../../vel_ronde5.png (in fase3/kleur/)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); K = os.path.join(HERE, '../..'); ROOT = os.path.join(K, *['..'] * 6)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
LICHT, DONKER = (248, 248, 244, 255), (44, 44, 56, 255)
def on(im, bg, s=1):
    b = Image.new('RGBA', im.size, bg); b.alpha_composite(im.convert('RGBA')); return b.resize((im.width * s, im.height * s), Image.NEAREST)
def load(p):
    raw = Image.open(p).crop((0, 0, 64, 64)); im = raw.convert('RGBA')
    if raw.mode == 'P': im.putalpha(Image.fromarray(((np.array(raw) != 0) * 255).astype('uint8')))
    return im
A = load(os.path.join(K, 'ronde5A/lama3.png')); B = load(os.path.join(K, 'ronde5B/lama3.png'))
r4b = load(os.path.join(K, 'ronde4b/lama3.png')); f2 = load(os.path.join(ROOT, 'docs/concept/sprites/lama/fase2/af/lama.png'))
W = Image.new('RGBA', (1460, 1120), LICHT); d = ImageDraw.Draw(W)
d.text((10, 6), 'Lama fase 3, kleur ronde 5: A (kop 1,25x, lijf op silhouet A) en B (kop 1,1x, lijf = 2b); oog: zichtbaar bovenlid, oogwit, kleine pupil', fill=(0, 0, 0), font=F)
x = 10
for n, im in [('A', A), ('B', B)]:
    W.paste(on(im, LICHT, 4), (x, 30)); W.paste(on(im, DONKER, 4), (x + 262, 30)); d.text((x, 290), f'{n}: 4x licht / donker', fill=(0, 0, 0), font=F); x += 530
W.paste(on(A, LICHT), (1080, 40)); W.paste(on(B, LICHT), (1150, 40)); W.paste(on(A, DONKER), (1080, 110)); W.paste(on(B, DONKER), (1150, 110))
d.text((1080, 180), '1x: A | B', fill=(0, 0, 0), font=F)
x = 10
for n, im in [('A', A), ('B', B), ('ronde 4b', r4b), ('lama fase 2', f2)]:
    W.paste(on(im, LICHT, 2), (x, 320)); W.paste(on(im, DONKER, 2), (x, 456)); W.paste(on(im, LICHT), (x + 30, 592))
    d.text((x, 660), n, fill=(0, 0, 0), font=F); x += 140
d.text((580, 320), '2x licht, 2x donker, 1x licht', fill=(0, 0, 0), font=F)
box = (8, 0, 36, 26); s = 8
W.paste(on(A.crop(box), LICHT, s), (10, 690)); W.paste(on(B.crop(box), LICHT, s), (250, 690))
ov = Image.open(os.path.join(K, 'kopbron/kop_overtrekvel_B.png')).convert('RGBA'); ov = ov.crop((0, 0, ov.width // 2, ov.height))
ov = ov.resize((int(ov.width * 208 / ov.height), 208), Image.LANCZOS); W.alpha_composite(ov, (490, 690))
d.text((10, 902), 'kop 8x: A', fill=(0, 0, 0), font=F); d.text((250, 902), 'kop 8x: B', fill=(0, 0, 0), font=F); d.text((490, 902), 'render model (B)', fill=(0, 0, 0), font=F)
# oog 12x: uitsneden 9x7 rond het oog
x = 10
for n, im, c in [('oog A', A, (20, 11)), ('oog B', B, (20, 10))]:
    W.paste(on(im.crop((c[0], c[1], c[0] + 9, c[1] + 8)), LICHT, 12), (x, 930)); d.text((x, 1030), n, fill=(0, 0, 0), font=F); x += 120
og = Image.open(os.path.join(ROOT, 'docs/concept/sprites/lama/fase3/oogstudie/ogen_12x.png')).convert('RGBA')
og = og.crop((0, 20, 520, 240)); og = og.resize((int(og.width * 0.8), int(og.height * 0.8)), Image.NEAREST)
W.alpha_composite(og, (260, 920)); d.text((260, 1100), 'oogstudie: Slakoth, Slaking, Vigoroth (12x)', fill=(0, 0, 0), font=F)
W.convert('RGB').save(os.path.join(K, 'vel_ronde5.png'))
