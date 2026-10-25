"""Coathief silhouet ronde 4 (Jordi, 25 okt, met krabbel `referenties/krabbel_jordi_voorpoten.png`): beide voorpoten
opnieuw zoals in de onderlaag, de rest gelijk aan ronde3. De opgetilde poot compact onder de kin (elleboog omlaag, poot
gekruld, klauwen hangen omlaag) i.p.v. ver naar links gestrekt ("dat wordt te scherp"); de staande poot erachter met
2 klauwen op de grond. Zone: x 8-33, y 50-62 (groepen gemeten op de render, zie onderaan)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
rows = [l.rstrip('\n') for l in open('ronde3.txt')]
g = [list(r) for r in rows]
SP = {50: [(22, 32)], 51: [(21, 32)], 52: [(20, 32)], 53: [(20, 32)], 54: [(19, 25), (27, 31)], 55: [(18, 25), (27, 31)],
      56: [(18, 24), (27, 31)], 57: [(17, 19), (21, 23), (27, 31)], 58: [(16, 18), (20, 22), (27, 30)],
      59: [(16, 17), (20, 21), (24, 30)], 60: [(16, 16), (20, 20), (22, 31)], 61: [(24, 31)], 62: [(21, 24)]}
for y in range(50, 63):
    for x in range(8, 34): g[y][x] = '.'
    for a, b in SP[y]:
        for x in range(a, b + 1): g[y][x] = '#'
open('ronde4.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')
A = np.array([[c == '#' for c in r] for r in rows]); B = np.array([[c == '#' for c in ''.join(r)] for r in g])
d = np.argwhere(A != B)
print('px', A.sum(), '->', B.sum(), '| gewijzigd', len(d), '| buiten zone', sum(not (8 <= x <= 33 and 50 <= y <= 62) for y, x in d))
a = np.zeros((64, 64, 4), np.uint8); a[B] = (40, 32, 44, 255); Image.fromarray(a).save('ronde4_1x.png')
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
u = Image.open('onderlaag_b1c_256.png').convert('RGBA')
def sil(m):
    a = np.zeros((64, 64, 4), np.uint8); a[m] = (40, 32, 44, 255); return Image.fromarray(a)
ov = u.copy(); s = sil(B).resize((256, 256), Image.NEAREST); s.putalpha(Image.fromarray((np.array(s)[..., 3] * 0.55).astype(np.uint8))); ov.alpha_composite(s)
W = Image.new('RGBA', (4 * 266 + 10, 300), (236, 236, 230, 255)); dr = ImageDraw.Draw(W)
for i, (im, t) in enumerate(((u, 'onderlaag'), (sil(A).resize((256, 256), Image.NEAREST), 'nu (ronde 5b)'),
                             (sil(B).resize((256, 256), Image.NEAREST), 'nieuw: voorpoten als de onderlaag'), (ov, 'nieuw over de onderlaag'))):
    W.alpha_composite(im, (5 + 266 * i, 5)); dr.text((5 + 266 * i, 268), t, fill='black', font=F)
W.convert('RGB').save('vel_ronde4.png')
