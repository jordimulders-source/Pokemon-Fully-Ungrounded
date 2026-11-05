"""Vel silhouet ronde 5b: ronde 5 | 5b | Girafarig | Ponyta | Mareep op 4x en 1x + 5b over het poppetje.
op 4x en 1x (licht en groen). Draaien: python3 vel.py -> vel_ronde5b.png"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '../../../../../..')
def load(p): return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, p)) if l.strip()])
def sprite(p): return np.array(Image.open(os.path.join(ROOT, p)))[:64] != 0
R5 = load('ronde5b.txt')
items = [('ronde 5', load('ronde5.txt')), ('ronde 5b', R5)]
items += [(n.capitalize(), sprite(f'graphics/pokemon/{n}/anim_front_gba.png')) for n in ('girafarig', 'ponyta', 'mareep')]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
CW = 268; W = Image.new('RGB', (CW * (len(items) + 1) + 10, 420), (250, 250, 250)); d = ImageDraw.Draw(W)
d.text((10, 6), 'Lama fase 2, silhouet ronde 5 -> 5b (ronde wolmassa, Girafarig/Ponyta-poten) naast echte Gen 3-sprites; 4x en 1x', fill=0, font=F)
for i, (n, m) in enumerate(items):
    x0 = 10 + i * CW
    im = np.full((64, 64, 3), 250, np.uint8); im[m] = (38, 30, 48)
    W.paste(Image.fromarray(im).resize((256, 256), Image.NEAREST), (x0, 30))
    d.rectangle([x0, 30, x0 + 255, 285], outline=(210, 210, 210))
    d.text((x0, 292), f'{n}: {int(m.sum())} px', fill=0, font=F)
    for k, bg in enumerate(((250, 250, 250), (120, 160, 120))):
        g = np.full((64, 64, 3), bg, np.uint8); g[m] = (38, 30, 48)
        W.paste(Image.fromarray(g), (x0 + 20 + k * 90, 320))
# ronde 5 als omtrek over het poppetje
x0 = 10 + len(items) * CW
u = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGB'); du = ImageDraw.Draw(u)
for y in range(64):
    for x in range(64):
        if not R5[y, x]: continue
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            yy, xx = y + dy, x + dx
            if not (0 <= yy < 64 and 0 <= xx < 64 and R5[yy, xx]):
                if dy: du.line([(x * 4, y * 4 + (4 if dy > 0 else 0)), (x * 4 + 3, y * 4 + (4 if dy > 0 else 0))], fill=(120, 0, 200), width=1)
                else: du.line([(x * 4 + (4 if dx > 0 else 0), y * 4), (x * 4 + (4 if dx > 0 else 0), y * 4 + 3)], fill=(120, 0, 200), width=1)
W.paste(u, (x0, 30)); d.text((x0, 292), 'ronde 5b over het poppetje', fill=0, font=F)
W.save(os.path.join(HERE, 'vel_ronde5b.png'))
