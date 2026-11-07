"""Vel silhouet ronde 5f: alleen 5f op 4x en 1x (licht/groen), 5f over het poppetje, en de kop 8x naast de poppetjeskop
met de 5f-omtrek erover. Draaien: python3 vel5f.py -> vel_ronde5f.png"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
S = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, 'ronde5f.txt')) if l.strip()])
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
W = Image.new('RGB', (1200, 420), (250, 250, 250)); d = ImageDraw.Draw(W)
d.text((10, 6), f'Lama fase 2, silhouet ronde 5f ({int(S.sum())} px): kop overgetrokken van het goedgekeurde poppetje', fill=0, font=F)
def sil(m, bg=(250, 250, 250)):
    a = np.full(m.shape + (3,), bg, np.uint8); a[m] = (38, 30, 48); return Image.fromarray(a)
def outline(img, m, s, ox=0, oy=0):
    dd = ImageDraw.Draw(img)
    for y, x in np.argwhere(m):
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < m.shape[0] and 0 <= xx < 64 and m[yy, xx]: continue
            X, Y = (x - ox) * s, (y - oy) * s
            if dy: dd.line([(X, Y + (s if dy > 0 else 0)), (X + s, Y + (s if dy > 0 else 0))], fill=(120, 0, 200), width=max(1, s // 4))
            else: dd.line([(X + (s if dx > 0 else 0), Y), (X + (s if dx > 0 else 0), Y + s)], fill=(120, 0, 200), width=max(1, s // 4))
W.paste(sil(S).resize((256, 256), Image.NEAREST), (10, 30)); d.rectangle([10, 30, 265, 285], outline=(210, 210, 210))
d.text((10, 290), 'ronde 5f, 4x', fill=0, font=F)
W.paste(sil(S), (20, 320)); W.paste(sil(S, (120, 160, 120)), (110, 320)); d.text((190, 345), '1x', fill=0, font=F)
U = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGB')
u = U.copy(); outline(u, S, 4); W.paste(u, (280, 30)); d.text((280, 290), 'ronde 5f over het poppetje', fill=0, font=F)
crop = U.crop((32, 0, 128, 96)).resize((192, 192), Image.NEAREST)          # kop: x8-31, y0-23
W.paste(crop, (550, 30)); d.text((550, 226), 'poppetje: kop (8x)', fill=0, font=F)
W.paste(sil(S[:24, 8:32]).resize((192, 192), Image.NEAREST), (750, 30)); d.text((750, 226), '5f: kop (8x)', fill=0, font=F)
ko = crop.copy(); outline(ko, S, 8, 8, 0); W.paste(ko, (950, 30)); d.text((950, 226), '5f-omtrek over poppetjeskop', fill=0, font=F)
W.save(os.path.join(HERE, 'vel_ronde5f.png'))
