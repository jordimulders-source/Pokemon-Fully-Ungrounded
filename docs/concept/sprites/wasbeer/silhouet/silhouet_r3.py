"""Wasbeer silhouet ronde 3 (Jordi: "het moet meer in een driekwart pose"; geen driekwartfoto beschikbaar):
hybride. Lijf, poten, armen, koevoeten en staart van foto 10 (ronde 2) verkort in de lengte (driekwart: lijf
draait naar de kijker), kop vervangen door de driekwart kop van foto 6 (kop6.py), gespiegeld en geschaald
naar de kopmaat van foto 10. Daarna gespiegeld zodat hij naar links kijkt.
Draaien: python3 silhouet_r3.py -> ronde3.txt, ronde3_1x.png, vel_ronde3.png"""
import os
import numpy as np
from PIL import Image, ImageDraw
import omtrek as O
import silhouet as S
import kop6 as K

CX = 290                      # borst: draaipunt van de verkorting
F_BACK, F_FWD, F_TAIL = 0.78, 0.88, 0.62


def fs(x, tail=False):
    if x >= CX:
        return CX + (x - CX) * F_FWD
    return CX + (x - CX) * (F_TAIL if tail else F_BACK)


def P(poly, tail=False):
    return [(fs(x, tail), y) for x, y in poly]


def T(tube, tail=False):
    return [(fs(x, tail), y, r) for x, y, r in tube]


# lijf zonder de kop van foto 10 (nek dicht via (282, 72)); borst iets voller naar de kijker
BODY = [(300, 108), (296, 125), (298, 160), (292, 195), (280, 225), (268, 250), (252, 268), (225, 278), (195, 280),
        (170, 272), (155, 250), (150, 215), (152, 180), (160, 150), (180, 120), (200, 98), (225, 78), (248, 62),
        (282, 66)]
# kop van foto 6, gespiegeld (snuit naar rechts zoals foto 10), kopmaat foto 10 (±100 px hoog)
KS = 0.31
# snuit: de lijn draait om klauwen en snuit; op foto 6 is hij door de hoek kort, hier steekt hij schuin naar
# links-omlaag uit de wang (driekwart), zoals de coatisnuit van fase 2
SNOUT6 = [(700, 520, 46), (650, 556, 40), (605, 584, 33), (572, 600, 27)]


def head(pts):
    return [(302 + (745 - x) * KS, 6 + (y - 312) * KS) for x, y in pts]


def headtube(t):
    return [(302 + (745 - x) * KS, 6 + (y - 312) * KS, r * KS) for x, y, r in t]


def build():
    parts = [P(BODY), P(O.LEG_NEAR), P(O.LEG_FAR), P([p for p in O.TAIL if p[0] > 85], tail=True),
             head(K.HEAD6), head(K.EAR6_NEAR), head(K.EAR6_FAR)]
    tubes = [headtube(SNOUT6), T(S.ARM_NEAR), T(S.ARM_FAR), T(S.CROW_NEAR), T(S.CROW_FAR), T(S.TAIL_HOOK, tail=True)]
    xs = [x for p in parts for x, y in p] + [x + s * r for t in tubes for x, y, r in t for s in (-1, 1)]
    ys = [y for p in parts for x, y in p] + [y + s * r for t in tubes for x, y, r in t for s in (-1, 1)]
    k = S.H / (max(ys) - min(ys))
    ox = (64 - (max(xs) - min(xs)) * k) / 2 - min(xs) * k
    oy = S.TOP - min(ys) * k
    SS = S.SS
    im = Image.new('L', (64 * SS, 64 * SS), 0)
    d = ImageDraw.Draw(im)
    for p in parts:
        d.polygon([((x * k + ox) * SS, (y * k + oy) * SS) for x, y in p], fill=255)
    for t in tubes:
        O.tube(d, t, k * SS, ox * SS, oy * SS)
    return (np.array(im.resize((64, 64), Image.BOX)) >= 128)[:, ::-1]


if __name__ == '__main__':
    a = build()
    S.save_txt(a, os.path.join(O.HERE, 'ronde3.txt'))
    al = Image.fromarray((a * 255).astype(np.uint8))
    blk = Image.new('RGBA', (64, 64), (34, 30, 30, 255)); blk.putalpha(al)
    blk.save(os.path.join(O.HERE, 'ronde3_1x.png'))
    r2 = Image.open(os.path.join(O.HERE, 'ronde2_1x.png'))
    f10 = Image.open(O.FOTO).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT).resize((300, 225))
    f6 = Image.open(K.FOTO6).convert('RGB').crop((560, 280, 900, 640)).resize((200, 212))
    sheet = Image.new('RGB', (20 + 300 + 20 + 200 + 20 + 256 + 20 + 256 + 20 + 90 + 90, 300), (236, 234, 228))
    d = ImageDraw.Draw(sheet)
    x = 20
    for lab, img in (('foto 10 (lijf, gespiegeld)', f10), ('foto 6 (driekwart kop)', f6),
                     ('ronde 2 (4x)', r2.resize((256, 256), Image.NEAREST)), ('ronde 3 driekwart (4x)', blk.resize((256, 256), Image.NEAREST))):
        sheet.paste(img, (x, 34), img if img.mode == 'RGBA' else None); d.text((x, 14), lab, fill=(30, 30, 30)); x += img.width + 20
    sheet.paste(r2, (x, 34), r2); d.text((x, 104), 'r2 1x', fill=(30, 30, 30)); x += 90
    sheet.paste(blk, (x, 34), blk); d.text((x, 104), f'r3 1x ({int(a.sum())} px)', fill=(30, 30, 30))
    sheet.save(os.path.join(O.HERE, 'vel_ronde3.png'))
    print(int(a.sum()))
