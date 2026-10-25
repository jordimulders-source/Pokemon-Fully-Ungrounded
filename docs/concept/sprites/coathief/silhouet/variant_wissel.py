"""Coathief: variant 'voorpoten gewisseld' (Jordi, 25 okt: "nee de voorpoten zijn omgewisseld, kijk maar goed").
Zoals in de onderlaag: de NABIJE voorpoot staat (dichtbij, voor, voet naar voren met 2 klauwen op de grond), de VERRE
voorpoot is opgetild (erachter, links-boven, 2 hangende klauwen). Op ronde3 alleen zone x 8-33, y 50-62."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
rows = [l.rstrip('\n') for l in open('ronde3.txt')]
g = [list(r) for r in rows]
NEAR = {50: [(21, 32)], 51: [(20, 32)], 52: [(19, 27)], 53: [(19, 26)], 54: [(19, 26)], 55: [(19, 25)], 56: [(19, 25)],
        57: [(18, 25)], 58: [(18, 25)], 59: [(17, 25)], 60: [(13, 26)], 61: [(10, 13), (15, 17), (19, 26)], 62: [(9, 10), (13, 15)]}
FAR = {52: [(16, 18)], 53: [(12, 18)], 54: [(10, 17)], 55: [(10, 16)], 56: [(9, 10), (13, 14)], 57: [(8, 9), (12, 13)],
       58: [(8, 8), (12, 12)]}
for y in range(50, 63):
    for x in range(8, 34): g[y][x] = '.'
far = np.zeros((64, 64), bool)
for d, isfar in ((FAR, True), (NEAR, False)):
    for y, sp in d.items():
        for a, b in sp:
            for x in range(a, b + 1):
                g[y][x] = '#'; far[y, x] = isfar
open('variant_wissel.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')
A = np.array([[c == '#' for c in r] for r in rows]); B = np.array([[c == '#' for c in ''.join(r)] for r in g])
print('px', A.sum(), '->', B.sum(), 'gewijzigd', (A != B).sum())
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
u = Image.open('onderlaag_b1c_256.png').convert('RGBA')
spr = Image.open('../kleur/ronde5b/coathief.png').convert('RGBA')
def sil(m, f):
    a = np.zeros((64, 64, 4), np.uint8); a[m] = (40, 32, 44, 255); a[m & f] = (120, 110, 126, 255)
    return Image.fromarray(a)
W = Image.new('RGBA', (4 * 266 + 10, 300), (236, 236, 230, 255)); d = ImageDraw.Draw(W)
for i, (im, t) in enumerate(((u, 'onderlaag (ontwerp)'), (spr.resize((256, 256), Image.NEAREST), 'nu: ronde 5b'),
                             (sil(B, far).resize((256, 256), Image.NEAREST), 'variant: voorpoten gewisseld (verre poot lichter)'))):
    W.alpha_composite(im, (5 + 266 * i, 5)); d.text((5 + 266 * i, 268), t, fill='black', font=F)
W.alpha_composite(sil(B, far), (5 + 266 * 3 + 20, 5)); W.alpha_composite(sil(B, np.zeros_like(far)), (5 + 266 * 3 + 100, 5))
d.text((5 + 266 * 3 + 20, 75), 'variant 1x', fill='black', font=F)
W.convert('RGB').save('vel_variant_wissel.png')
