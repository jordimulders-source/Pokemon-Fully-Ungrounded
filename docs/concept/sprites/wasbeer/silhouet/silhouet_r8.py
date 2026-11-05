"""Wasbeer silhouet ronde 8 (Jordi, 2 nov): "ik heb een idee wat het wat leuker maakt. Een soort van bruine
burglar zak op zijn rug. De kop is trouwens echt minder goed nu" -> ronde 2 (foto 10, met de eigen kop van foto 10)
+ een dichtgeknoopte buitzak op de rug (steekt half boven de ruglijn uit, knoop met twee flapjes bovenaan).
Draaien: python3 silhouet_r8.py -> ronde8.txt, ronde8_1x.png, vel_ronde8.png"""
import os
import numpy as np
from PIL import Image, ImageDraw
import omtrek as O
import silhouet as S

# zak in fotocoördinaten van foto 10 (vóór spiegelen; de rug zit links): bol lijf, smalle hals, knoop
SACK = [(150, 150, 44), (140, 124, 42), (138, 100, 33), (146, 82, 20)]
NECK = [(148, 80, 10), (154, 66, 8)]
KNOT = [[(154, 66), (140, 52), (148, 48), (160, 60)], [(156, 64), (170, 54), (174, 60), (160, 68)]]


def build():
    pts = [p for poly in O.POLYS.values() for p in poly]
    tubes = [S.ARM_NEAR, S.ARM_FAR, S.CROW_NEAR, S.CROW_FAR, S.TAIL_HOOK, SACK, NECK]
    xs = [p[0] for p in pts] + [x + s * r for t in tubes for x, y, r in t for s in (-1, 1)] + [x for k in KNOT for x, y in k]
    ys = [p[1] for p in pts] + [y + s * r for t in tubes for x, y, r in t for s in (-1, 1)] + [y for k in KNOT for x, y in k]
    k = min(S.H / (max(ys) - min(ys)), 62 / (max(xs) - min(xs)))
    ox = (64 - (max(xs) - min(xs)) * k) / 2 - min(xs) * k
    oy = S.TOP - min(ys) * k
    im = Image.new('L', (64 * S.SS, 64 * S.SS), 0)
    d = ImageDraw.Draw(im)
    for name, poly in O.POLYS.items():
        if name == 'staart':
            poly = [p for p in poly if p[0] > 85]
        d.polygon([((x * k + ox) * S.SS, (y * k + oy) * S.SS) for x, y in poly], fill=255)
    for kn in KNOT:
        d.polygon([((x * k + ox) * S.SS, (y * k + oy) * S.SS) for x, y in kn], fill=255)
    for t in tubes:
        O.tube(d, t, k * S.SS, ox * S.SS, oy * S.SS)
    return (np.array(im.resize((64, 64), Image.BOX)) >= 128)[:, ::-1]


if __name__ == '__main__':
    a = build()
    S.save_txt(a, os.path.join(O.HERE, 'ronde8.txt'))
    blk = Image.new('RGBA', (64, 64), (34, 30, 30, 255)); blk.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    blk.save(os.path.join(O.HERE, 'ronde8_1x.png'))
    r2 = Image.open(os.path.join(O.HERE, 'ronde2_1x.png'))
    f10 = Image.open(O.FOTO).convert('RGB').transpose(Image.FLIP_LEFT_RIGHT).resize((256, 192))
    sheet = Image.new('RGB', (20 + (256 + 20) * 3 + 90 + 90, 320), (236, 234, 228))
    d = ImageDraw.Draw(sheet)
    x = 20
    for lab, img in (('foto 10', f10), ('ronde 2 (4x)', r2.resize((256, 256), Image.NEAREST)),
                     ('ronde 8: + buitzak op de rug (4x)', blk.resize((256, 256), Image.NEAREST))):
        sheet.paste(img, (x, 40), img if img.mode == 'RGBA' else None); d.text((x, 20), lab, fill=(30, 30, 30)); x += 276
    sheet.paste(r2, (x, 40), r2); d.text((x, 110), 'r2 1x', fill=(30, 30, 30)); x += 90
    sheet.paste(blk, (x, 40), blk); d.text((x, 110), f'r8 1x ({int(a.sum())} px)', fill=(30, 30, 30))
    sheet.save(os.path.join(O.HERE, 'vel_ronde8.png'))
    print(int(a.sum()))
