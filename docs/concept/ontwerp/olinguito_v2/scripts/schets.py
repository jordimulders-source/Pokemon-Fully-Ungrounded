"""Olinguito v2 (24 okt): modeltekening zonder pixels.
Ronde 1: schetsen_v1.png (staart omhoog/omlaag; Jordi koos omhoog).
Ronde 2 (Jordi): dunnere olinguito-staart, één oog en één dominant oor (profiel zoals Linoone),
meer olinguito/minder wasbeer, kortere neus (langer pas bij de coati), klauwen meer Linoone,
dynamischere poten met de achterpoten onder het lijf naar voren (boomfoto), geen buikvlak.
Ronde 3 (Jordi): rondere kop, langere staart (foto's), asymmetrische dynamische poten (boomfoto).
Ronde 4 (Jordi): veel kleiner oog (foto's), kop meer diagonaal naar de kijker (zoals Pokémon-sprites), oor iets groter.
Draaien vanuit de repo-root: python3 docs/concept/ontwerp/olinguito_v2/scripts/schets.py"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'olinguito', 'scripts'))
from lib import *
from PIL import ImageFont

BR = '#6A4630'   # donkerbruine vacht
HD = '#6B5442'   # grijzig bruine kop (zoals op de foto's)
FAR = '#4C3121'  # verre poten
TAN = '#C79A58'  # goudbruine keel/buik
MK = '#3A271B'   # zacht donker rond het oog (geen wasbeerband)
NO = '#C98088'   # roze neus
EY = '#B9481C'   # roodbruin oog
CL = '#EDE3CC'   # klauwen
OUT = os.path.join(HERE, '..')


def tail(c):
    pts = (qbez((204, 104), (250, 80), (236, 34), 12)[:-1] + qbez((236, 34), (222, 4), (186, 12), 10)[:-1]
           + qbez((186, 12), (158, 20), (156, 46), 8))
    n = len(pts) - 1
    w = [17 + 3 * math.sin(math.pi * i / n) - 9 * (i / n) ** 2 for i in range(n + 1)]
    c.part(blob(tube(pts, w)[::2], 6), BR)


def paw_claws(c, x, y, ang, L=34, col=CL):
    """Twee lange, licht gebogen klauwen (Linoone), naar voren-omlaag."""
    for dx, dy, k in ((0, 0, 1.0), (8, 3, 0.85)):
        bx, by = x + dx, y + dy
        tx = bx + math.cos(math.radians(ang)) * L * k
        ty = by + math.sin(math.radians(ang)) * L * k
        c.part(claw((bx, by), (tx, ty), -6, 9), col, line=1.6)


def hind_foot(c, x, y, col):
    c.part(ell(x, y, 12, 7, -10), col)
    for i in range(3):
        c.part(claw((x - 10 + i * 5, y + 2), (x - 17 + i * 5, y + 9), 2, 3.5), CL, line=1)


def draw():
    c = Canvas()
    # verre achterpoot: gestrekt naar achteren, zet zich af
    c.part(tube([(192, 124), (214, 150), (232, 168)], [26, 19, 15]), FAR)
    c.part(ell(236, 170, 11, 7, 30), FAR)
    # verre voorpoot: ver gestrekt naar voren-omlaag, grijpt
    c.part(tube([(96, 164), (68, 200), (46, 222)], [24, 19, 16]), FAR)
    c.part(ell(43, 223, 11, 8, -35), FAR)
    paw_claws(c, 36, 225, 160, 30, '#D8CDB4')
    tail(c)
    # romp: boog van borst (linksonder) naar romp (rechtsboven)
    c.part(blob([(76, 148), (96, 122), (128, 102), (162, 86), (194, 82), (214, 96), (216, 120),
                 (200, 140), (166, 152), (132, 170), (104, 188), (80, 180)]), BR)
    # nabije achterpoot: opgetrokken, knie hoog naar voren, hak terug, voet naar voren onder de buik
    c.part(blob([(178, 98), (206, 102), (214, 124), (200, 146), (174, 148), (166, 128)]), BR)
    c.part(tube([(172, 144), (182, 168), (164, 182)], [20, 16, 14]), BR)
    hind_foot(c, 158, 184, BR)
    # nabije voorpoot: opgetild en gebogen (stapt), elleboog naar achteren, klauwen hangen omlaag
    c.part(tube([(114, 150), (134, 182), (112, 196)], [28, 22, 18]), BR)
    c.part(ell(106, 198, 12, 9, -10), BR)
    paw_claws(c, 98, 202, 128)
    # kop in 3/4 naar de kijker (vergroot rond de nek)
    k, px, py = 1.25, 80, 168
    T = lambda pts: [(px + (x - px) * k, py + (y - py) * k) for x, y in pts]
    E = lambda x, y, rx, ry, r=0: T(ell(x, y, rx, ry, r))
    # verre oor: alleen een randje boven de schedel
    c.part(E(62, 127, 8, 7, -15), BR)
    # kop en snuit als één vorm (geen naad), snuit uit het midden van het gezicht naar de kijker
    snout = T([(54, 166), (46, 178), (43, 188), (48, 197), (60, 199), (74, 190), (80, 176), (68, 166)])
    h = c.part(c.mask(E(70, 154, 29, 28)) | c.mask(blob(snout)), HD)
    # nabije oor: dominant, achter op de kop
    e1 = c.part(E(89, 129, 15, 14, 20), HD)
    c.mark(E(89, 131, 8, 8), TAN, e1)
    # korte snuit, naar de kijker gedraaid: wijst meer omlaag, breder aan de basis
    hs = h
    # snuitrug: korte lijn die de snuit uit het gezicht laat komen
    c.stroke(T(qbez((47, 177), (52, 168), (60, 164), 8)), 1.6)
    c.mark(blob(T([(52, 200), (64, 198), (78, 188), (92, 174), (98, 186), (64, 210), (48, 208)])), TAN, hs)
    # zacht donker rond het oog
    c.mark(blob(T([(54, 152), (60, 144), (70, 143), (76, 149), (74, 158), (66, 162), (57, 160)])), MK, hs)
    x, y, rx, ry = 65, 152, 4.6, 5.0
    m = c.part(E(x, y, rx, ry, -10), EY, line=1.0)
    c.part(E(x - rx * 0.15, y + ry * 0.1, rx * 0.55, ry * 0.62), '#1A0F0B', line=0, clip=m)
    c.part(E(x - rx * 0.35, y - ry * 0.35, rx * 0.3, rx * 0.3), '#FFFFFF', line=0, clip=m)
    c.stroke(T([(x - rx * 1.4, y - ry * 0.7), (x + rx * 1.3, y - ry * 1.25)]), 2.2)
    c.part(E(46, 192, 5, 4.5, -10), NO, line=1.4)
    c.stroke(T(qbez((52, 198), (58, 201), (65, 197), 8)), 1.4)
    return c.finish(outer=3.0)


F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)


def sheet():
    a, sa = draw()
    a.save(os.path.join(OUT, 'schets_v2_ronde4.png'))
    W, H = 256 * 3 + 40, 256 + 110
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 8), 'Olinguito v2, ronde 4: schets (geen pixels)', font=FB, fill=(30, 30, 30))
    im.paste(a, (10, 34))
    silim = Image.new('RGB', (256, 256), 'white')
    silim.paste(Image.new('RGB', (256, 256), (70, 66, 84)), (0, 0), sa)
    im.paste(silim, (276, 34))
    small = a.resize((64, 64), Image.LANCZOS).resize((256, 256), Image.NEAREST)
    im.paste(small, (542, 34))
    for x, t in ((10, 'schets'), (276, 'silhouet'), (542, 'op spritegrootte (64×64)')):
        d.text((x, 292), t, font=FS, fill=(90, 90, 90))
    lines = ['Kop in 3/4 zoals Linoone: één oog, één dominant oor. Dunnere staart omhoog, kortere snuit, zacht masker.',
             'Ronde 4: klein oog, kop meer diagonaal naar de kijker, groter oor (ronde 3: kop, staart, poten).']
    for i, ln in enumerate(lines):
        d.text((10, 312 + i * 18), ln, font=F, fill=(30, 30, 30))
    im.save(os.path.join(OUT, 'schetsen_v2_ronde4.png'))


sheet()
