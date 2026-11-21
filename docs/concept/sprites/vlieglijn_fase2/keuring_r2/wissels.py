#!/usr/bin/env python3
"""Eindkeuring r2 mug: wissels (x, y, van_index, naar_index) op een kopie van sprite_r2/mug_r2.png.

Indexen (normal.pal): 0=. 1=# 2=k 3=d 4=g 5=w 6=P 7=p 8=q 9=L 10=l 11=i 12=Y 13=y 14=E 15=e
Slot 6 (P) en 9 (L) worden in r2 niet gebruikt (vrij).

Gebruik: python3 wissels.py [--geen-moet] [--geen-mag]
Schrijft keuring_r2/voorstel.png (+ .txt), voorstel_8x.png en vel.png
(r2 | alleen MOET | MOET+MAG | model, alles op 8x).
"""
import sys, os
import numpy as np
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
BASIS = os.path.dirname(HIER)
SPRITE = os.path.join(BASIS, 'sprite_r2', 'mug_r2.png')
NATIEF = os.path.join(BASIS, 'maat', 'natief.png')

# MOET 1: volume achterlijf (Coathief-regel). Paarse panelen: q-hooglicht linksboven,
# P (vrij slot 6, 86,48,102) als schaduwsikkel rechtsonder; schaal: d-hooglicht op de bolling.
MOET = [
    # rechterpaneel
    (42, 36, 7, 8), (42, 37, 7, 8), (44, 41, 7, 8), (44, 42, 7, 8),
    (47, 45, 7, 6), (47, 46, 7, 6),
    # voorpaneel
    (37, 37, 7, 8), (35, 40, 7, 8), (36, 40, 7, 8),
    (38, 41, 7, 6), (39, 41, 7, 6),
    # schaal achterlijf: hooglicht 2 px breed i.p.v. 1-px-randlijn
    (40, 33, 2, 3), (41, 33, 2, 3),
]

# MAG 1: lone p-pikkel in het lichte borststuk
MAG = [(27, 29, 7, 8)]
# MAG 2: lichte selout op de lichtkant van vleugels en koepel: k -> slot 9 (opnieuw ingekleurd)
SELOUT = [
    # linkervleugel, linkerrand
    (21, 1), (22, 1), (21, 2), (21, 3), (21, 4), (21, 5), (22, 6), (22, 7), (22, 8),
    (22, 9), (22, 10), (23, 11), (23, 12), (24, 13), (24, 14),
    # grote rechtervleugel, bovenrand
    (55, 1), (56, 1), (57, 1), (58, 1), (53, 2), (54, 2), (50, 3), (51, 3), (52, 3),
    (48, 4), (49, 4), (47, 5), (45, 6), (46, 6), (43, 7), (44, 7), (43, 8), (42, 9),
    (41, 10), (40, 11), (39, 12), (38, 13), (37, 14), (37, 15), (36, 16), (35, 17),
    (35, 18), (34, 19), (33, 20),
    # kleine rechtervleugel, bovenrand
    (53, 17), (54, 17), (55, 17), (56, 17), (47, 18), (48, 18), (49, 18), (50, 18),
    (51, 18), (52, 18), (44, 19), (45, 19), (46, 19), (41, 20), (42, 20), (43, 20),
    (39, 21), (40, 21),
    # koepel, bovenrand
    (19, 15), (20, 15), (21, 15), (22, 15), (23, 15), (24, 15), (17, 16), (18, 16),
]
MAG += [(x, y, 2, 9) for x, y in SELOUT]
MAG += [(16, 17, 1, 9), (15, 18, 1, 9)]  # koepel linksboven: # -> selout
SLOT9_MAG = (92, 92, 108)  # nieuwe kleur voor vrij slot 9 (tussen k 56 en d 118)


def pas_toe(a, lijst):
    a = a.copy()
    for x, y, van, naar in lijst:
        if a[y, x] != van:
            raise SystemExit(f'({x},{y}) is {a[y, x]}, verwacht {van}')
        a[y, x] = naar
    return a


def maak(a, pal):
    im = Image.fromarray(a.astype(np.uint8), 'P')
    im.putpalette(pal)
    return im


def rgb(a, pal, bg=(200, 225, 200)):
    p = np.array(pal[:48]).reshape(16, 3)
    out = p[a].astype(np.uint8)
    out[a == 0] = bg
    return Image.fromarray(out, 'RGB')


def model64():
    nat = Image.open(NATIEF).convert('RGB')
    na = np.array(nat).astype(int)
    m = np.abs(na - 254).sum(2) > 30
    ys, xs = np.where(m)
    box = nat.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)).resize((56, 63), Image.BOX)
    mod = Image.new('RGB', (64, 64), (254, 254, 254))
    mod.paste(box, (4, 1))
    return mod


def main():
    doe_moet = '--geen-moet' not in sys.argv
    doe_mag = '--geen-mag' not in sys.argv
    src = Image.open(SPRITE)
    a0 = np.array(src)
    pal0 = src.getpalette()[:48]
    pal_mag = list(pal0)
    pal_mag[27:30] = SLOT9_MAG

    a_moet = pas_toe(a0, MOET)
    a_alles = pas_toe(a_moet, MAG)

    a = a0
    pal = pal0
    if doe_moet:
        a = pas_toe(a, MOET)
    if doe_mag:
        a = pas_toe(a, MAG)
        pal = pal_mag
    maak(a, pal).save(os.path.join(HIER, 'voorstel.png'))
    rgb(a, pal).resize((512, 512), Image.NEAREST).save(os.path.join(HIER, 'voorstel_8x.png'))
    tekens = '.#kdgwPpqLliYyEe'
    with open(os.path.join(HIER, 'voorstel.txt'), 'w') as f:
        f.write('# voorstel, tekens = paletindex: ' + tekens + '\n')
        for r in a:
            f.write(''.join(tekens[v] for v in r) + '\n')

    panelen = [rgb(a0, pal0), rgb(a_moet, pal0), rgb(a_alles, pal_mag), model64()]
    vel8 = Image.new('RGB', (4 * 512 + 3 * 10, 512 + 64 + 20), (255, 255, 255))
    for i, p in enumerate(panelen):
        vel8.paste(p.resize((512, 512), Image.NEAREST), (i * 522, 0))
        vel8.paste(p, (i * 522, 532))
        vel8.paste(p.resize((128, 128), Image.NEAREST).crop((0, 0, 128, 64)), (i * 522 + 80, 532)) if False else None
    vel8.save(os.path.join(HIER, 'vel.png'))

    fig = a > 0
    print('gewijzigd:', int((a != a0).sum()), 'px; silhouet-diff:', int(((a > 0) != (a0 > 0)).sum()))
    print('# in figuur: %.1f%%, k: %.1f%%' % (100 * (a == 1).sum() / fig.sum(), 100 * (a == 2).sum() / fig.sum()))


if __name__ == '__main__':
    main()
