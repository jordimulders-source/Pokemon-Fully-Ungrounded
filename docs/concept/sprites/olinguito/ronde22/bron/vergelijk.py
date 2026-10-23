#!/usr/bin/env python3
"""compare.png voor ronde 22: ronde 21b, ronde 22 (fr1, fr2), Galar-Linoone, Poochyena op 1x en 3x;
daaronder de poten op 6x (21b | 22 | Linoone) met de voeten gemarkeerd (V = verre, N = nabije; vo = voor, a = achter)."""
from PIL import Image, ImageDraw
import os
H = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(H, '..', '..')
G = os.path.join(R, '..', '..', '..', '..', 'graphics', 'pokemon')
L = lambda *p: Image.open(os.path.join(*p))
r21b = L(R, 'ronde21b', 'anim_front.png'); r22 = L(R, 'ronde22', 'anim_front.png')
lin = L(R, 'referenties', 'galar_linoone_front.png'); poo = L(G, 'poochyena', 'anim_front.png')
BG = (200, 200, 200, 255)
fr = lambda im, f=0: im.convert('RGBA').crop((0, 64 * f, 64, 64 * f + 64))
up = lambda im, k: im.resize((im.width * k, im.height * k), Image.NEAREST)
cols = [('ronde 21b', fr(r21b)), ('ronde 22', fr(r22)), ('ronde 22 fr2', fr(r22, 1)),
        ('Galar-Linoone', fr(lin)), ('Poochyena', fr(poo))]
CW = 64 * 3 + 8
K = 6
out = Image.new('RGBA', (len(cols) * CW, 16 + 64 + 8 + 192 + 24 + 20 * K + 10), BG)
d = ImageDraw.Draw(out)
for i, (naam, im) in enumerate(cols):
    x = i * CW
    d.text((x + 2, 2), naam, fill=(0, 0, 0, 255))
    out.paste(im, (x, 16), im)
    b = up(im, 3); out.paste(b, (x, 88), b)
y8 = 88 + 192 + 24
d.text((2, y8 - 16), 'poten 6x: ronde 21b | ronde 22 | Galar-Linoone (voeten: Vvo/Nvo/Na/Va)', fill=(0, 0, 0, 255))
# voetposities (x, y van de voetzool) per sprite, frame 1
VOET = {
    'r21b': {'Nvo': (17, 55), 'Vvo': (27, 52), 'Na': (35, 54), 'Va': (44, 52)},
    'r22':  {'Vvo': (14, 54), 'Nvo': (25, 53), 'Na': (39, 54), 'Va': (46, 51)},
    'lin':  {'Vvo': (14, 49), 'Nvo': (32, 45), 'Na': (43, 48), 'Va': (54, 41)},
}
x = 0
for key, im, box in (('r21b', r21b, (8, 36, 52, 57)), ('r22', r22, (8, 36, 52, 57)), ('lin', lin, (2, 32, 60, 53))):
    c = up(fr(im).crop(box), K)
    out.paste(c, (x, y8), c)
    for naam, (vx, vy) in VOET[key].items():
        px, py = x + (vx - box[0]) * K, y8 + (vy - box[1]) * K
        d.ellipse((px - 3, py - 3, px + 3, py + 3), outline=(220, 0, 0, 255))
        d.text((px - 8, py + 4), naam, fill=(220, 0, 0, 255))
    x += c.width + 12
out = out.crop((0, 0, max(out.width, x), out.height))
out.save(os.path.join(R, 'ronde22', 'compare.png'))
print('compare.png', out.size)
