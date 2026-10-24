"""Olinguito v2 (24 okt): modeltekening zonder pixels.
Ronde 1: schetsen_v1.png (staart omhoog/omlaag; Jordi koos omhoog).
Ronde 2 (Jordi): dunnere olinguito-staart, één oog en één dominant oor (profiel zoals Linoone),
meer olinguito/minder wasbeer, kortere neus (langer pas bij de coati), klauwen meer Linoone,
dynamischere poten met de achterpoten onder het lijf naar voren (boomfoto), geen buikvlak.
Ronde 3 (Jordi): rondere kop, langere staart (foto's), asymmetrische dynamische poten (boomfoto).
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
    # kop in profiel (vergroot rond de nek)
    k, px, py = 1.25, 80, 168
    T = lambda pts: [(px + (x - px) * k, py + (y - py) * k) for x, y in pts]
    E = lambda x, y, rx, ry, r=0: T(ell(x, y, rx, ry, r))
    # verre oor: alleen een randje boven de schedel
    c.part(E(62, 127, 8, 7, -15), BR)
    h = c.part(E(70, 154, 29, 28), HD)
    # nabije oor: dominant, achter op de kop
    e1 = c.part(E(88, 130, 12, 11, 20), HD)
    c.mark(E(88, 132, 6, 6), TAN, e1)
    # korte snuit (langer pas bij de coati)
    sn = c.part(blob(T([(50, 154), (40, 164), (32, 176), (30, 184), (36, 190), (52, 190), (70, 182), (64, 164)])), HD, line=0)
    hs = h | sn
    c.mark(blob(T([(38, 188), (54, 188), (74, 182), (92, 172), (98, 186), (60, 204), (36, 204)])), TAN, hs)
    # zacht donker rond het oog
    c.mark(blob(T([(42, 160), (48, 148), (60, 144), (72, 150), (72, 164), (62, 172), (48, 172)])), MK, hs)
    x, y, rx, ry = 58, 158, 8.5, 9.5
    m = c.part(E(x, y, rx, ry, -10), EY, line=1.2)
    c.part(E(x - rx * 0.2, y + ry * 0.12, rx * 0.5, ry * 0.58), '#1A0F0B', line=0, clip=m)
    c.part(E(x - rx * 0.35, y - ry * 0.35, rx * 0.28, rx * 0.28), '#FFFFFF', line=0, clip=m)
    c.stroke(T([(x - rx * 1.2, y - ry * 0.5), (x + rx * 1.1, y - ry * 0.95)]), 2.4)
    c.part(E(31, 183, 5, 4.5, -20), NO, line=1.4)
    c.stroke(T(qbez((36, 190), (42, 193), (49, 190), 8)), 1.4)
    return c.finish(outer=3.0)


F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)


def sheet():
    a, sa = draw()
    a.save(os.path.join(OUT, 'schets_v2_ronde3.png'))
    W, H = 256 * 3 + 40, 256 + 110
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 8), 'Olinguito v2, ronde 3: schets (geen pixels)', font=FB, fill=(30, 30, 30))
    im.paste(a, (10, 34))
    silim = Image.new('RGB', (256, 256), 'white')
    silim.paste(Image.new('RGB', (256, 256), (70, 66, 84)), (0, 0), sa)
    im.paste(silim, (276, 34))
    small = a.resize((64, 64), Image.LANCZOS).resize((256, 256), Image.NEAREST)
    im.paste(small, (542, 34))
    for x, t in ((10, 'schets'), (276, 'silhouet'), (542, 'op spritegrootte (64×64)')):
        d.text((x, 292), t, font=FS, fill=(90, 90, 90))
    lines = ['Profiel zoals Linoone: één oog, één dominant oor. Dunnere staart omhoog, kortere snuit, zacht masker.',
             'Ronde 3: rondere kop, langere staart, poten asymmetrisch (voorpoot gestrekt/opgetild, achterpoot opgetrokken/gestrekt).']
    for i, ln in enumerate(lines):
        d.text((10, 312 + i * 18), ln, font=F, fill=(30, 30, 30))
    im.save(os.path.join(OUT, 'schetsen_v2_ronde3.png'))


sheet()
