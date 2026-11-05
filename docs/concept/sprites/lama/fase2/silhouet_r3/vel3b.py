"""Vel silhouet ronde 3b: ronde 3 | ronde 3b | Flaaffy | Mareep op 4x en 1x (licht en groen), plus ronde 3b over de onderlaag.
Schrijft ook ronde3b_1x.png. Draaien: python3 vel3b.py"""
import os
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, *['..'] * 6))
DARK = (40, 32, 48)
def load(p): return np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, p)) if l.strip()])
def gf(n): return np.array(Image.open(os.path.join(ROOT, 'graphics/pokemon', n, 'anim_front.png')))[:64, :64] != 0
def sil(a, s, bg=(255, 255, 255)):
    im = np.full(a.shape + (3,), bg, np.uint8); im[a] = DARK
    return Image.fromarray(im).resize((64 * s, 64 * s), Image.NEAREST)
r3, r3b = load('ronde3.txt'), load('ronde3b.txt')
p = Image.fromarray(r3b.astype(np.uint8), 'P'); p.putpalette([255, 255, 255, *DARK] + [0] * 762); p.save(os.path.join(HERE, 'ronde3b_1x.png'), transparency=0)
und = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGBA'); ub = Image.new('RGBA', und.size, 'white'); ub.alpha_composite(und)
lay = Image.new('RGBA', ub.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
for y, x in zip(*np.nonzero(r3b)): d.rectangle([x * 4, y * 4, x * 4 + 3, y * 4 + 3], fill=(40, 40, 170, 110))
ub.alpha_composite(lay)
items = [('ronde 3 (korrelig)', r3), ('ronde 3b', r3b), ('Flaaffy', gf('flaaffy')), ('Mareep', gf('mareep'))]
img = Image.new('RGB', (12 + 5 * 272, 22 + 256 + 12 + 64 + 40), (255, 255, 255)); d = ImageDraw.Draw(img)
for i, (t, a) in enumerate(items):
    x = 12 + i * 272; img.paste(sil(a, 4), (x, 22)); d.text((x, 6), f'{t} ({int(a.sum())} px)', fill=(0, 0, 0))
    img.paste(sil(a, 1), (x + 40, 290)); img.paste(sil(a, 1, (120, 160, 120)), (x + 130, 290))
x = 12 + 4 * 272; img.paste(ub.convert('RGB'), (x, 22)); d.text((x, 6), 'ronde 3b over het poppetje', fill=(0, 0, 0))
d.text((x, 300), 'korrels (1-px tanden/inkepingen):', fill=(0, 0, 0)); d.text((x, 314), 'ronde 3: 21 tanden, 22 px  ->  3b: 0', fill=(0, 0, 0))
img.save(os.path.join(HERE, 'vel_ronde3b.png')); print(img.size)
