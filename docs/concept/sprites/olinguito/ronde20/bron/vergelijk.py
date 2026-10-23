#!/usr/bin/env python3
"""compare.png voor ronde 20: stap 1b, ronde 20 (frame 1 en 2), Galar-Linoone, Poochyena, Sandslash
op 1x en 3x, plus kop en klauwen op 8x."""
from PIL import Image, ImageDraw
import os
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..')
G = os.path.join(R, '..', '..', '..', '..', 'graphics', 'pokemon')
st1b = Image.open(os.path.join(R, 'stap1b_kop', 'anim_front.png'))
r20 = Image.open(os.path.join(R, 'ronde20', 'anim_front.png'))
lin = Image.open(os.path.join(R, 'referenties', 'galar_linoone_front.png'))
poo = Image.open(os.path.join(G, 'poochyena', 'anim_front.png'))
san = Image.open(os.path.join(G, 'sandslash', 'anim_front.png'))
BG = (200, 200, 200, 255)
def fr(im, f=0):
    return im.convert('RGBA').crop((0, 64 * f, 64, 64 * f + 64))
def up(im, k):
    return im.resize((im.width * k, im.height * k), Image.NEAREST)
cols = [('stap 1b', fr(st1b)), ('ronde 20', fr(r20)), ('ronde 20 fr2', fr(r20, 1)),
        ('Galar-Linoone', fr(lin)), ('Poochyena', fr(poo)), ('Sandslash', fr(san))]
CW = 64 * 3 + 8
out = Image.new('RGBA', (len(cols) * CW, 16 + 64 + 8 + 192 + 20 + 26 * 8 + 10), BG)
d = ImageDraw.Draw(out)
for i, (naam, im) in enumerate(cols):
    x = i * CW
    d.text((x + 2, 2), naam, fill=(0, 0, 0, 255))
    out.paste(im, (x, 16), im)
    b = up(im, 3); out.paste(b, (x, 88), b)
y8 = 88 + 192 + 20
d.text((2, y8 - 14), 'kop 8x: stap 1b | ronde 20      klauwen 8x: ronde 20 | Sandslash', fill=(0, 0, 0, 255))
k1 = up(fr(st1b).crop((8, 18, 40, 44)), 8); out.paste(k1, (0, y8), k1)
k2 = up(fr(r20).crop((8, 18, 40, 44)), 8); out.paste(k2, (32 * 8 + 8, y8), k2)
c1 = up(fr(r20).crop((10, 40, 36, 56)), 8); out.paste(c1, (64 * 8 + 24, y8), c1)
c2 = up(fr(san).crop((2, 32, 18, 48)), 8); out.paste(c2, (64 * 8 + 24 + 26 * 8 + 8, y8), c2)
out.save(os.path.join(R, 'ronde20', 'compare.png'))
print('compare.png', out.size)
