#!/usr/bin/env python3
"""Eindkeuring mug r5: tintwissels (x, y, van_index, naar_index) op een kopie van sprite_r5/mug_r5.png.
Controleert per pixel de oude index en dat de alpha-diff met r5 0 is (stopt anders).
Schrijft voorstel.png (MOET+MAG), voorstel_8x.png en vel.png.
Gebruik: python3 wissels.py [--geen-mag]
Indexen: 1 # · 2 k · 3 d · 4 g · 5 w · 6 P · 7 p · 8 q · 9 L · 10 l · 11 i · 12 Y · 13 y · 14 E · 15 e"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

HIER = os.path.dirname(os.path.abspath(__file__)); BASIS = os.path.dirname(HIER)
R5 = os.path.join(BASIS, 'sprite_r5/mug_r5.png')
MODEL = os.path.join(BASIS, 'referenties/gemini_gekozen_r1.png')

MOET = {
    # A. achterlijf: één hooglichtstrook en een sikkel i.p.v. losse q-spikkels; paars los van de grijze schaal (L) en van de poot (i)
    'ACHTERLIJF': [
        (43, 38, 7, 6), (43, 39, 7, 6),            # p naast L (zelfde helderheid 92/84) -> P
        (45, 41, 7, 8),                            # bovenrand paneel onder de schaal licht
        (44, 43, 7, 8), (44, 44, 7, 8), (45, 45, 7, 8),  # hooglichtstrook langs de poot doortrekken
        (46, 46, 7, 6),                            # sikkel onderaan
        (37, 37, 8, 7),                            # q tegen poot-i (146/143) -> p: poot en paneel los
    ],
    # B. borststuk onder: 11 px vlak q -> rechterkant p (schaduw rechts, zoals het model)
    'BORSTSTUK': [(30, 29, 8, 7), (29, 30, 8, 7), (30, 30, 8, 7)],
    # C. gele knie op lichtrichting linksboven
    'KNIE': [(23, 45, 12, 13), (25, 45, 13, 12)],
}
MAG = {
    'GEEL': [(40, 34, 13, 12), (40, 35, 13, 12),   # ring achterlijf: rechts in schaduw
             (34, 26, 13, 12), (34, 27, 13, 12),   # schoudergewricht: rechts in schaduw
             (23, 35, 12, 13)],                    # elleboog klauwarm: bovenkant licht
    'VLEUGELTIP': [(55, 18, 5, 4), (56, 18, 5, 4), (57, 18, 5, 4),  # w tegen y (227/212) smelt
                   (22, 2, 5, 4), (22, 3, 5, 4)],
    'ADER': [(45, 7, 3, 5)],                       # d tussen selout en glansstrook (L d w)
}


def pas_toe(a, groepen):
    for naam, lijst in groepen.items():
        for x, y, van, naar in lijst:
            if a[y, x] != van:
                sys.exit(f'STOP {naam} ({x},{y}): index {a[y, x]}, verwacht {van}')
            a[y, x] = naar
    return a


def rgb(a, pal, bg):
    r = pal[a].copy(); r[a == 0] = bg
    return Image.fromarray(r.astype(np.uint8))


def model_8x():
    sys.path.insert(0, os.path.join(BASIS, 'sprite_r5'))
    from celmeting import X0, Y0, sx, sy
    M = Image.open(MODEL).convert('RGB')
    box = (X0 - 4 * sx, Y0 - 1 * sy + 2, X0 + 60 * sx, Y0 + 63 * sy + 2)
    m = M.crop(tuple(int(round(v)) for v in box)).resize((512, 512), Image.LANCZOS)
    return m


def main():
    im = Image.open(R5); pal = np.array(im.getpalette()[:48]).reshape(16, 3)
    r5 = np.array(im)
    moet = pas_toe(r5.copy(), MOET)
    alles = pas_toe(moet.copy(), MAG) if '--geen-mag' not in sys.argv else moet.copy()
    for naam, b in (('MOET', moet), ('MOET+MAG', alles)):
        if ((b == 0) != (r5 == 0)).any():
            sys.exit(f'STOP alpha-diff {naam} != 0')
    print('alpha-diff 0; pixels gewijzigd: MOET', int((moet != r5).sum()), '| MOET+MAG', int((alles != r5).sum()))
    out = im.copy(); out.putdata(alles.flatten().tolist()); out.save(os.path.join(HIER, 'voorstel.png'), transparency=0)
    bg = (200, 225, 205)
    rgb(alles, pal, bg).resize((512, 512), Image.NEAREST).save(os.path.join(HIER, 'voorstel_8x.png'))
    # vel: rij 1 = r5 | alleen MOET | MOET+MAG | model op 8x; rij 2 = 1x en 2x op licht en donker (r5 en voorstel)
    rij1 = [rgb(b, pal, bg).resize((512, 512), Image.NEAREST) for b in (r5, moet, alles)] + [model_8x()]
    W = 4 * 512 + 3 * 16
    vel = Image.new('RGB', (W, 512 + 40 + 24 + 160), 'white'); d = ImageDraw.Draw(vel)
    for i, (p, t) in enumerate(zip(rij1, ('r5', 'alleen MOET', 'MOET+MAG', 'model'))):
        vel.paste(p, (i * 528, 24)); d.text((i * 528 + 4, 6), t, fill=(0, 0, 0))
    y = 24 + 512 + 24; x = 0
    for bgk in ((248, 248, 248), (40, 40, 48)):
        for b, t in ((r5, 'r5'), (alles, 'voorstel')):
            for z in (1, 2):
                s = rgb(b, pal, bgk).resize((64 * z, 64 * z), Image.NEAREST)
                vak = Image.new('RGB', (64 * z + 16, 144), bgk); vak.paste(s, (8, 8)); vel.paste(vak, (x, y))
                d.text((x + 2, y + 146), f'{t} {z}x', fill=(0, 0, 0)); x += 64 * z + 24
    vel.save(os.path.join(HIER, 'vel.png'))


if __name__ == '__main__':
    main()
