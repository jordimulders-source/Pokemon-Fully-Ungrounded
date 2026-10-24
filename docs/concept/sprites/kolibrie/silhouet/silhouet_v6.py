"""Kolibrie silhouet v6 (Jordi, 24 okt): pose en anatomie van Jordi's foto van een drinkende kolibrie
(kop links, snavel schuin omlaag in een bloem, vleugels als V omhoog, staart naar rechts, 3/4).
De foto stond niet als bestand in de sessie; de omtrek is punt voor punt overgenomen in
fotocoördinaten (2000x1334), niet verzonnen. Daarna: staart -> franje + drie slierten, jeguaka op de kruin."""
import os, math
import numpy as np
from PIL import Image, ImageDraw
from silhouet import catmull, tube, SS, HERE

# omtrek kop + lijf + staartwortel (met de klok mee vanaf de snavelbasis)
BODY = [(1000, 612), (978, 580), (970, 520), (985, 465), (1020, 425), (1070, 412), (1120, 425), (1165, 450),
        (1210, 465), (1290, 480), (1370, 560), (1400, 615), (1470, 635), (1560, 670), (1640, 705), (1665, 715),
        (1640, 722), (1540, 722), (1440, 725), (1360, 722), (1300, 730), (1230, 722), (1160, 690), (1100, 650),
        (1050, 615), (1015, 620)]
BEAK = [(1005, 612), (965, 690), (920, 778)]
# verre vleugel: smal lemmet recht omhoog vanaf de schouder
FAR = [(1215, 445), (1290, 380), (1400, 250), (1495, 120), (1512, 112), (1530, 150), (1445, 285), (1345, 415), (1285, 465)]  # +25 px breder: anders 1 px dun op 64
# nabije vleugel: brede aanzet op de rug (1265,455)-(1385,610), rechte stompe punt rechtsboven
NEAR = [(1265, 455), (1330, 415), (1450, 365), (1600, 310), (1720, 268), (1805, 255), (1812, 268), (1795, 285),
        (1720, 310), (1640, 350), (1560, 410), (1480, 480), (1420, 550), (1385, 610), (1340, 560)]
CROWN = (1095, 420)
TAILBASE = (1575, 692)
BOX, WIDTH = 64, 50


def build(own_tail=True):
    xs = [p[0] for p in BODY + BEAK + FAR + NEAR]; ys = [p[1] for p in BODY + BEAK + FAR + NEAR]
    k = WIDTH / (max(xs) - min(xs))
    ox, oy = 2 - min(xs) * k, 4 - min(ys) * k
    T = lambda p: (p[0] * k + ox, p[1] * k + oy)
    im = Image.new('L', (BOX * SS, BOX * SS), 0)
    d = ImageDraw.Draw(im)
    for poly in (FAR, NEAR):
        d.polygon([(T(p)[0] * SS, T(p)[1] * SS) for p in poly], fill=255)
    body = BODY
    if own_tail:
        # korte staartwaaier van de foto eraf (vanaf de staartwortel), eigen staart erop
        body = [p for p in BODY if p[0] < 1600]
    c = catmull([T(p) for p in body] + [T(body[0])], 10)
    d.polygon([(x * SS, y * SS) for x, y in c], fill=255)
    tube(d, [T(p) for p in BEAK], 2.0, 1.3)  # min. 2 px, anders breekt hij op 64
    if own_tail:
        cx, cy = T(CROWN)
        # jeguaka: drie korte veertjes langs de kruin naar achteren (niet omhoog: dat leest als oren)
        # v6b (Jordi): langer; licht gebogen veren, de bovenste het langst
        # schuin omhoog naar achteren, in de ruimte tussen kop en verre vleugel (anders verdwijnt hij in de rug)
        for dx, dy in ((0.0, -7.5), (3.4, -7.2), (6.4, -5.0)):
            tube(d, [(cx, cy + 0.8), (cx + dx * 0.35, cy + 0.8 + dy * 0.55), (cx + dx, cy + 0.8 + dy)], 1.6, 1.0)
        tx, ty = T(TAILBASE)
        for a in (-20, 5, 30):
            r = math.radians(a)
            tube(d, [(tx - 1, ty), (tx - 1 + math.cos(r) * 6, ty + math.sin(r) * 6)], 2.6, 1.5)
        # drie slierten: eerst naar rechts, dan met één Articuno-krul omlaag
        ribbons = [[(tx, ty), (tx + 8, ty - 2), (tx + 15, ty + 1), (tx + 17, ty + 7), (tx + 13, ty + 10)],
                   [(tx, ty + 0.5), (tx + 7, ty + 3), (tx + 11, ty + 9), (tx + 9, ty + 14), (tx + 4, ty + 15)],
                   [(tx - 1, ty + 1), (tx + 3, ty + 7), (tx + 3, ty + 13), (tx - 1, ty + 17)]]
        for rb in ribbons:
            tube(d, rb, 1.6, 1.2)
            (px, py), (x, y) = rb[-2], rb[-1]
            a = math.atan2(y - py, x - px)
            tube(d, [(x, y), (x + math.cos(a) * 3, y + math.sin(a) * 3)], 1.4, 3.8)
    return np.array(im.resize((BOX, BOX), Image.BOX)) > 110


def sil(m):
    a = np.zeros((64, 64, 4), np.uint8); a[m] = (40, 30, 60, 255)
    return Image.fromarray(a)


if __name__ == '__main__':
    A, B = sil(build(False)), sil(build(True))
    W = Image.new('RGB', (256 * 2 + 10 + 64 * 2 + 40, 280), (236, 236, 230))
    for i, S in enumerate((A, B)):
        W.paste(S.resize((256, 256), Image.NEAREST), (i * 266, 0), S.resize((256, 256), Image.NEAREST))
        W.paste(S, (540 + i * 74, 20), S)
    dr = ImageDraw.Draw(W)
    dr.text((2, 262), 'foto-omtrek (zuiver)', fill='black')
    dr.text((268, 262), '+ jeguaka + eigen staart', fill='black')
    dr.text((540, 90), '1x', fill='black')
    W.save(os.path.join(HERE, 'silhouet_v6.png'))
    B.save(os.path.join(HERE, 'silhouet_v6_1x.png'))
