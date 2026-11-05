"""Kopstudie fase 3 (5 nov). Jordi: "de bombin mag ietsje meer aan de linkerkant uitsteken en iets groter worden. De oren moeten
wel zichtbaar blijven. De vlechten zijn onzichtbaar, het hoofd is ook nog steeds niet goed [...] anders moeten we ervoor kiezen om
het hoofd gewoon groter te maken". Varianten: kop 1.0/1.12/1.2 met grotere bombín (naar links) en dikkere vlechten naar buiten.
Rij 1 poppetje, rij 2 ruwe kleurverkleining naar 64 px (4x), rij 3 silhouet 50%. Draaien vanuit de repo-root."""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../ontwerp')); sys.path.insert(0, os.path.join(HERE, '../silhouet'))
import pop3d_lama as L, fase3_r4 as F4, vel_buff as V
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
L.set_vacht('bont (foto 4)'); L.COL['lid'] = L.COL['head']; L.COL['lip'] = '#C9A982'; F4.HEAD_YAW = 18
W3 = dict(breed=1.26, nr=7, legk=1.85)
VARS = [('nu (W3)', 1.0, (1.0, 0.0, 1.0, 0.0)), ('K1: hoed + vlecht, kop gelijk', 1.0, (1.3, -2.5, 1.3, 9.0)),
        ('K2: + kop 1,12', 1.12, (1.3, -2.5, 1.3, 9.0)), ('K3: + kop 1,2', 1.2, (1.3, -2.5, 1.3, 9.0))]
cell = 262
im = Image.new('RGB', (12 + cell * len(VARS), 44 + 3 * (cell + 26)), 'white'); d = ImageDraw.Draw(im)
d.text((12, 12), 'Lama fase 3 kopstudie: bombín groter en naar links, vlechten dikker en zichtbaar, kop groter?', font=FB, fill=(30, 30, 30))
for i, (lab, kk, (hk, hdx, bk, bz)) in enumerate(VARS):
    F4.HATK, F4.HAT_DX, F4.BRAIDK, F4.BRAID_Z = hk, hdx, bk, bz
    m = F4.fase3_r4('Y', kopk=kk, **W3)
    und, S = V.sil64(m, 45, 8)
    x = 12 + cell * i
    im.paste(und, (x, 44)); d.text((x + 4, 44 + 258), f'{lab}, kop {L.kopaandeel(m, 45):.0%}', font=F, fill=(60, 60, 60))
    big = np.array(und.resize((64, 64), Image.LANCZOS)); big[~S] = 255
    im.paste(Image.fromarray(big).resize((256, 256), Image.NEAREST), (x, 44 + cell + 26)); im.paste(Image.fromarray(big), (x + 190, 44 + cell + 26 + 190))
    d.text((x + 4, 44 + cell + 26 + 258), 'ruwe kleurverkleining 64 px (geen sprite)', font=F, fill=(60, 60, 60))
    s = np.full((64, 64, 3), 255, np.uint8); s[S] = (40, 30, 30)
    im.paste(Image.fromarray(s).resize((256, 256), Image.NEAREST), (x, 44 + 2 * (cell + 26)))
    d.text((x + 4, 44 + 2 * (cell + 26) + 258), f'silhouet {int(S.sum())} px', font=F, fill=(60, 60, 60))
im.save(os.path.join(HERE, 'vel_kopstudie.png'))
