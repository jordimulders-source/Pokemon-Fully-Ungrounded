"""Vel silhouet ronde 5e: alleen 5e op 4x en 1x (licht/groen), 5e over het poppetje, en de kop uitvergroot (8x) naast de
poppetjeskop; onderaan de 1x-toets naast Girafarig, Ponyta, Rapidash en Stantler. Draaien: python3 vel5e.py -> vel_ronde5e.png"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '../../../../../..')
S = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, 'ronde5e.txt')) if l.strip()])
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
W = Image.new('RGB', (1130, 470), (250, 250, 250)); d = ImageDraw.Draw(W)
d.text((10, 6), f'Lama fase 2, silhouet ronde 5e ({int(S.sum())} px): kop driekwart zoals het poppetje', fill=0, font=F)
def sil(m, bg=(250, 250, 250)):
    a = np.full(m.shape + (3,), bg, np.uint8); a[m] = (38, 30, 48); return Image.fromarray(a)
W.paste(sil(S).resize((256, 256), Image.NEAREST), (10, 30)); d.rectangle([10, 30, 265, 285], outline=(210, 210, 210))
d.text((10, 290), 'ronde 5e, 4x', fill=0, font=F)
def outline(img, m, s, ox=0, oy=0):
    dd = ImageDraw.Draw(img)
    for y in range(64):
        for x in range(64):
            if not m[y, x]: continue
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < 64 and 0 <= xx < 64 and m[yy, xx]: continue
                X, Y = (x - ox) * s, (y - oy) * s
                if dy: dd.line([(X, Y + (s if dy > 0 else 0)), (X + s, Y + (s if dy > 0 else 0))], fill=(120, 0, 200), width=max(1, s // 4))
                else: dd.line([(X + (s if dx > 0 else 0), Y), (X + (s if dx > 0 else 0), Y + s)], fill=(120, 0, 200), width=max(1, s // 4))
U = Image.open(os.path.join(HERE, 'onderlaag_256.png')).convert('RGB')
u = U.copy(); outline(u, S, 4); W.paste(u, (280, 30)); d.text((280, 290), 'ronde 5e over het poppetje', fill=0, font=F)
# kop 8x: kader x8-31, y0-23
crop = U.crop((8 * 4, 0, 32 * 4, 24 * 4)).resize((192, 192), Image.NEAREST)
W.paste(crop, (550, 30)); d.text((550, 226), 'poppetje: kop', fill=0, font=F)
k = sil(S[:24, 8:32]).resize((192, 192), Image.NEAREST); W.paste(k, (750, 30)); d.text((750, 226), '5e: kop (8x)', fill=0, font=F)
ko = U.crop((32, 0, 128, 96)).resize((192, 192), Image.BICUBIC); outline(ko, S, 8, 8, 0); W.paste(ko, (950, 30))
d.text((950, 226), '5e-omtrek over de kop', fill=0, font=F)
# 1x-toets
x0 = 550; d.text((x0, 255), '1x-toets (licht / groen):', fill=0, font=F)
refs = [('5e', S)] + [(n, np.array(Image.open(os.path.join(ROOT, f'graphics/pokemon/{n}/anim_front_gba.png')))[:64] != 0)
                     for n in ('girafarig', 'ponyta', 'rapidash', 'stantler')]
for i, (n, m) in enumerate(refs):
    W.paste(sil(m), (x0 + i * 112, 280)); W.paste(sil(m, (120, 160, 120)), (x0 + i * 112, 350)); d.text((x0 + i * 112, 418), n, fill=0, font=F)
W.paste(sil(S), (20, 320)); W.paste(sil(S, (120, 160, 120)), (110, 320)); d.text((20, 390), 'ronde 5e, 1x', fill=0, font=F)
W.save(os.path.join(HERE, 'vel_ronde5e.png'))
