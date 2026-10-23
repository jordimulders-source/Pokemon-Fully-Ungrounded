#!/usr/bin/env python3
"""compare.png voor ronde 21: stap 1b, ronde 20, ronde 21 (fr1, fr2), variant kop lager, Galar-Linoone,
Poochyena, Sandslash op 1x en 3x; poten en klauwen op 8x (ronde 20 | ronde 21 | Sandslash)."""
from PIL import Image, ImageDraw
import os
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..')
G = os.path.join(R, '..', '..', '..', '..', 'graphics', 'pokemon')
L = lambda *p: Image.open(os.path.join(*p))
st1b = L(R, 'stap1b_kop', 'anim_front.png'); r20 = L(R, 'ronde20', 'anim_front.png')
r21 = L(R, 'ronde21', 'anim_front.png'); var = L(R, 'ronde21', 'variant_kop_lager', 'anim_front.png')
lin = L(R, 'referenties', 'galar_linoone_front.png')
poo = L(G, 'poochyena', 'anim_front.png'); san = L(G, 'sandslash', 'anim_front.png')
BG = (200, 200, 200, 255)
fr = lambda im, f=0: im.convert('RGBA').crop((0, 64 * f, 64, 64 * f + 64))
up = lambda im, k: im.resize((im.width * k, im.height * k), Image.NEAREST)
cols = [('stap 1b', fr(st1b)), ('ronde 20', fr(r20)), ('ronde 21', fr(r21)), ('ronde 21 fr2', fr(r21, 1)),
        ('variant kop -2', fr(var)), ('Galar-Linoone', fr(lin)), ('Poochyena', fr(poo)), ('Sandslash', fr(san))]
CW = 64 * 3 + 8
out = Image.new('RGBA', (len(cols) * CW, 16 + 64 + 8 + 192 + 20 + 18 * 8 + 10), BG)
d = ImageDraw.Draw(out)
for i, (naam, im) in enumerate(cols):
    x = i * CW
    d.text((x + 2, 2), naam, fill=(0, 0, 0, 255))
    out.paste(im, (x, 16), im)
    b = up(im, 3); out.paste(b, (x, 88), b)
y8 = 88 + 192 + 20
d.text((2, y8 - 14), 'poten 8x: ronde 20 | ronde 21          klauwen Sandslash 8x', fill=(0, 0, 0, 255))
x = 0
for im, box in ((r20, (10, 38, 52, 56)), (r21, (10, 38, 52, 56)), (san, (2, 32, 18, 50))):
    c = up(fr(im).crop(box), 8); out.paste(c, (x, y8), c); x += c.width + 12
out.save(os.path.join(R, 'ronde21', 'compare.png'))
print('compare.png', out.size)
