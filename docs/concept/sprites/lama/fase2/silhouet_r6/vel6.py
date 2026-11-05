"""Vel silhouet ronde 6: alleen ronde 6 op 4x en 1x (licht/groen), ronde 6 als omtrek over het poppetje, en de diffkaart in kleur
over het model op 4x (grijs = beide, groen = alleen ronde 6, rood = alleen model). Draaien: python3 vel6.py -> vel_ronde6.png"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); R5 = os.path.join(HERE, '../silhouet_r5')
S = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, 'ronde6.txt')) if l.strip()])
a = np.load(os.path.join(R5, 'kop_alpha.npy')); k = a.shape[0] // 64; M = a.reshape(64, k, 64, k).mean((1, 3)) >= 0.5
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
W = Image.new('RGB', (850, 420), (250, 250, 250)); d = ImageDraw.Draw(W)
d.text((10, 6), f'Lama fase 2, silhouet ronde 6 ({int(S.sum())} px): hele silhouet overgetrokken van het poppetje (+{int((S & ~M).sum())} / -{int((M & ~S).sum())} px)', fill=0, font=F)
def sil(m, bg=(250, 250, 250)):
    a = np.full(m.shape + (3,), bg, np.uint8); a[m] = (38, 30, 48); return Image.fromarray(a)
def outline(img, m, s):
    dd = ImageDraw.Draw(img)
    for y, x in np.argwhere(m):
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < 64 and 0 <= xx < 64 and m[yy, xx]: continue
            X, Y = x * s, y * s
            if dy: dd.line([(X, Y + (s if dy > 0 else 0)), (X + s, Y + (s if dy > 0 else 0))], fill=(120, 0, 200), width=1)
            else: dd.line([(X + (s if dx > 0 else 0), Y), (X + (s if dx > 0 else 0), Y + s)], fill=(120, 0, 200), width=1)
W.paste(sil(S).resize((256, 256), Image.NEAREST), (10, 30)); d.rectangle([10, 30, 265, 285], outline=(210, 210, 210))
d.text((10, 290), 'ronde 6, 4x', fill=0, font=F)
W.paste(sil(S), (20, 320)); W.paste(sil(S, (120, 160, 120)), (110, 320)); d.text((190, 345), '1x', fill=0, font=F)
U = Image.open(os.path.join(R5, 'onderlaag_256.png')).convert('RGB')
u = U.copy(); outline(u, S, 4); W.paste(u, (280, 30)); d.text((280, 290), 'ronde 6 (omtrek) over het poppetje', fill=0, font=F)
D = np.full((64, 64, 3), 250, np.uint8); D[S & M] = (150, 150, 160); D[S & ~M] = (0, 170, 60); D[M & ~S] = (220, 30, 30)
dimg = Image.blend(U, Image.fromarray(D).resize((256, 256), Image.NEAREST), 0.75)
W.paste(dimg, (550, 30)); d.text((550, 290), 'diff over het model: grijs beide,', fill=0, font=F)
d.text((550, 306), 'groen alleen ronde 6, rood alleen model', fill=0, font=F)
W.save(os.path.join(HERE, 'vel_ronde6.png'))
