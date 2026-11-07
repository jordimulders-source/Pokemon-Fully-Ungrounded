"""Wasbeer ronde 12: onderlaag voor het met de hand getekende silhouet (ronde12.txt).
Massa en houding = omtrek van foto 10 (omtrek.py), gespiegeld (kijkt naar links) en geschaald zodat de
fotokop op de kop van ronde11.txt valt (schaal 0.154: dan valt de beenlengte op Weavile-lengte, ±16 rijen).
Kop = ronde11.txt (rijen 7-22, kolom <= 26), 3 rijen omhoog en 4 kolommen naar rechts (ruimte voor de klauwen). Dit is alleen de onderlaag; het eindsilhouet is
met de hand gelegd in ronde12.txt.
Draaien: python3 docs/concept/sprites/wasbeer/silhouet/onderlaag_r12.py  -> onderlaag_r12.txt"""
import os
import numpy as np
from PIL import Image, ImageDraw
import omtrek as O
HERE = os.path.dirname(os.path.abspath(__file__))
K, OX, OY, SHIFT, DX = 0.154, -14.7, -0.2, 3, 4   # schaal, verschuiving (na spiegeling), kop omhoog, kop opzij


def onderlaag():
    big = 8
    im = Image.new('L', (64 * big, 64 * big), 0)
    d = ImageDraw.Draw(im)
    f = lambda x, y: (((500 - x) * K + OX) * big, ((y) * K + OY) * big)
    for poly in (O.HEAD_BODY, O.EAR_NEAR, O.EAR_FAR, O.LEG_NEAR, O.LEG_FAR, O.TAIL):
        d.polygon([f(x, y) for x, y in poly], fill=255)
    for arm in (O.ARM_NEAR, O.ARM_FAR):
        for (x0, y0, r0), (x1, y1, r1) in zip(arm, arm[1:]):
            for i in range(11):
                t = i / 10
                x, y = f(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t); r = (r0 + (r1 - r0) * t) * K * big
                d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    sil = np.array(im.resize((64, 64), Image.BOX)) > 110
    kop = np.zeros((64, 64), bool)
    r11 = [l.rstrip('\n') for l in open(os.path.join(HERE, 'ronde11.txt'))]
    for y in range(7, 23):
        for x in range(27):
            if r11[y][x] == '#':
                kop[y - SHIFT, x + DX] = True
    return sil, kop


if __name__ == '__main__':
    sil, kop = onderlaag()
    rows = [''.join('K' if kop[y, x] else ('o' if sil[y, x] else '.') for x in range(64)) for y in range(64)]
    open(os.path.join(HERE, 'onderlaag_r12.txt'), 'w').write('\n'.join(rows) + '\n')
    print('\n'.join('%2d %s' % (i, r) for i, r in enumerate(rows)))
