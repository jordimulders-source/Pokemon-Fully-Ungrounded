"""Coathief: variant 'loop' (Jordi, 25 okt: "als je naar onderlaag kijkt staat de andere poot verder naar voren [...]
die loop pose is net wat dynamischer"). Op ronde3 alleen de verre achterpoot (x 33-45, y 52-60): schuin vanaf de heup
naar voren-onder, voet op de grond onder de buik, zoals in de onderlaag."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
rows = [l.rstrip('\n') for l in open('ronde3.txt')]
g = [list(r) for r in rows]
leg = {52: (39, 44), 53: (38, 44), 54: (37, 43), 55: (36, 42), 56: (35, 41), 57: (34, 40), 58: (34, 39), 59: (34, 40)}
for y in range(52, 61):
    for x in range(33, 45): g[y][x] = '.'
for y, (a, b) in leg.items():
    for x in range(a, b + 1): g[y][x] = '#'
open('variant_loop.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')
A = np.array([[c == '#' for c in r] for r in rows]); B = np.array([[c == '#' for c in ''.join(r)] for r in g])
print('px', A.sum(), '->', B.sum(), 'gewijzigd', (A != B).sum())
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
u = Image.open('onderlaag_b1c_256.png').convert('RGBA')
spr = Image.open('../kleur/ronde5b/coathief.png').convert('RGBA')
def sil(m, hl=None):
    a = np.zeros((64, 64, 4), np.uint8); a[m] = (40, 32, 44, 255)
    if hl is not None: a[hl] = (200, 70, 60, 255)
    return Image.fromarray(a).resize((256, 256), Image.NEAREST)
W = Image.new('RGBA', (4 * 266 + 10, 290), (236, 236, 230, 255)); d = ImageDraw.Draw(W)
leg_old = np.zeros_like(A); leg_old[52:61, 33:45] = A[52:61, 33:45]
leg_new = np.zeros_like(B); leg_new[52:61, 33:45] = B[52:61, 33:45]
for i, (im, t) in enumerate(((u, 'onderlaag (ontwerp)'), (spr.resize((256, 256), Image.NEAREST), 'nu: ronde 5b'),
                             (sil(A, leg_old), 'nu: verre achterpoot (rood)'), (sil(B, leg_new), 'variant: poot schuin naar voren'))):
    W.alpha_composite(im, (5 + 266 * i, 5)); d.text((5 + 266 * i, 268), t, fill='black', font=F)
W.convert('RGB').save('vel_variant_loop.png')
