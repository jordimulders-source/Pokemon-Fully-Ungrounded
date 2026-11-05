"""Wasbeer silhouet ronde 7 (Jordi, 2 nov: "ja doe maar, terug naar ronde 2"): ronde 2 = foto 10 overgetrokken
(massa en houding van het echte dier, gespiegeld, armen/koevoeten korter, haakstaart), met de kop vervangen door de
driekwart kop van foto 11 (kop11.py: brede wangen, korte snuit, kleine neus, rond nabij oor). Driekwart komt
verder uit de kleur (lichte borst naar de kijker, masker over beide ogen, verre kant in schaduw).
Draaien: python3 silhouet_r7.py -> ronde7.txt, ronde7_1x.png, vel_ronde7.png"""
import os
import numpy as np
from PIL import Image, ImageDraw
import omtrek as O
import silhouet as S
import kop11 as K
from silhouet_r3 import BODY        # lijf van foto 10 zonder de kop (nek dicht)

KS = 0.38                           # kop foto 11 -> kopmaat foto 10
NX, NY = 348, 86                    # neus op de plek van de neus van foto 10 (fotocoördinaten, vóór het spiegelen)


def kp(p):                          # foto 11 kijkt naar links, foto 10 (vóór spiegelen) naar rechts: x spiegelen
    return (NX - (p[0] - K.NOSE11[0]) * KS, NY + (p[1] - K.NOSE11[1]) * KS)


def build():
    parts = [BODY, O.LEG_NEAR, O.LEG_FAR, [p for p in O.TAIL if p[0] > 85]] + \
            [[kp(p) for p in poly] for poly in (K.HEAD11, K.EAR11_NEAR, K.EAR11_FAR)]
    tubes = [S.ARM_NEAR, S.ARM_FAR, S.CROW_NEAR, S.CROW_FAR, S.TAIL_HOOK]
    xs = [x for p in parts for x, y in p] + [x + s * r for t in tubes for x, y, r in t for s in (-1, 1)]
    ys = [y for p in parts for x, y in p] + [y + s * r for t in tubes for x, y, r in t for s in (-1, 1)]
    k = min(S.H / (max(ys) - min(ys)), 62 / (max(xs) - min(xs)))   # niet buiten de 64 px
    ox = (64 - (max(xs) - min(xs)) * k) / 2 - min(xs) * k
    oy = S.TOP - min(ys) * k
    im = Image.new('L', (64 * S.SS, 64 * S.SS), 0)
    d = ImageDraw.Draw(im)
    for p in parts:
        d.polygon([((x * k + ox) * S.SS, (y * k + oy) * S.SS) for x, y in p], fill=255)
    for t in tubes:
        O.tube(d, t, k * S.SS, ox * S.SS, oy * S.SS)
    return (np.array(im.resize((64, 64), Image.BOX)) >= 128)[:, ::-1]


if __name__ == '__main__':
    a = build()
    S.save_txt(a, os.path.join(O.HERE, 'ronde7.txt'))
    blk = Image.new('RGBA', (64, 64), (34, 30, 30, 255)); blk.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    blk.save(os.path.join(O.HERE, 'ronde7_1x.png'))
    r2 = Image.open(os.path.join(O.HERE, 'ronde2_1x.png'))
    f10 = Image.open(O.FOTO).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT).resize((256, 192))
    f11 = Image.open(K.FOTO11).convert('RGB').crop((180, 80, 540, 320)).resize((256, 171))
    sheet = Image.new('RGB', (20 + (256 + 20) * 4 + 90 + 90, 320), (236, 234, 228))
    d = ImageDraw.Draw(sheet)
    x = 20
    for lab, img in (('foto 10 (lijf)', f10), ('foto 11 (driekwart kop)', f11), ('ronde 2 (4x)', r2.resize((256, 256), Image.NEAREST)),
                     ('ronde 7 (4x)', blk.resize((256, 256), Image.NEAREST))):
        sheet.paste(img, (x, 40), img if img.mode == 'RGBA' else None); d.text((x, 20), lab, fill=(30, 30, 30)); x += 276
    sheet.paste(r2, (x, 40), r2); d.text((x, 110), 'r2 1x', fill=(30, 30, 30)); x += 90
    sheet.paste(blk, (x, 40), blk); d.text((x, 110), f'r7 1x ({int(a.sum())} px)', fill=(30, 30, 30))
    sheet.save(os.path.join(O.HERE, 'vel_ronde7.png'))
    print(int(a.sum()))
