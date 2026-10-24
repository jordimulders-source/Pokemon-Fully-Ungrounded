"""Olinguito v2 (24 okt): modeltekening zonder pixels. Pose naar de boomfoto en Linoone:
kop omlaag naar links, rug als boog omhoog, lange staart (variant A omhoog, B omlaag).
Draaien vanuit de repo-root: python3 docs/concept/ontwerp/olinguito_v2/scripts/schets.py"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'olinguito', 'scripts'))
from lib import *
from PIL import ImageFont

BR = '#6A4630'   # donkerbruine vacht
FAR = '#4C3121'  # verre poten
TAN = '#C79A58'  # goudbruine keel/buik (zoals op de foto's)
MK = '#2A1A12'   # masker
NO = '#B9747A'   # neus
EY = '#C4521C'   # roodbruine ogen
CL = '#EDE3CC'   # klauwen
OUT = os.path.join(HERE, '..')


def tail_up(c):
    pts = qbez((206, 100), (250, 70), (226, 26), 10)[:-1] + qbez((226, 26), (212, 6), (190, 22), 6)
    w = [30 + 10 * math.sin(math.pi * i / (len(pts) - 1)) - 20 * (i / (len(pts) - 1)) ** 2 for i in range(len(pts))]
    c.part(blob(tube(pts, w)[::2], 6), BR)


def tail_down(c):
    pts = qbez((206, 112), (240, 150), (226, 204), 10)[:-1] + qbez((226, 204), (218, 240), (190, 234), 7)
    w = [30 + 10 * math.sin(math.pi * i / (len(pts) - 1)) - 20 * (i / (len(pts) - 1)) ** 2 for i in range(len(pts))]
    c.part(blob(tube(pts, w)[::2], 6), BR)


def paw_claws(c, x, y, ang, L=48, col=CL):
    """Twee lange gebogen klauwen (Linoone/Sandslash), naar voren-omlaag."""
    for dx, dy, k in ((0, 0, 1.0), (9, 3, 0.85)):
        bx, by = x + dx, y + dy
        tx = bx + math.cos(math.radians(ang)) * L * k
        ty = by + math.sin(math.radians(ang)) * L * k
        c.part(claw((bx, by), (tx, ty), -11, 13), col, line=1.8)


def draw(tail):
    c = Canvas()
    # verre poten
    c.part(tube([(176, 136), (182, 160), (174, 180)], [26, 20, 17]), FAR)
    c.part(ell(170, 182, 12, 7), FAR)
    c.part(tube([(96, 164), (70, 196), (54, 210)], [26, 21, 18]), FAR)
    c.part(ell(50, 211, 12, 8, -30), FAR)
    paw_claws(c, 44, 212, 152, 42, '#D8CDB4')
    # staart
    tail(c)
    # romp: boog van borst (linksonder) naar romp (rechtsboven)
    body = c.part(blob([(76, 148), (96, 122), (128, 102), (162, 86), (194, 82), (214, 96), (216, 120),
                        (200, 140), (166, 152), (132, 170), (104, 188), (80, 180)]), BR)
    c.mark(blob([(84, 176), (106, 172), (136, 156), (168, 140), (200, 132), (200, 160), (120, 200), (80, 200)]), TAN, body)
    # nabije achterpoot (dij + onderbeen)
    c.part(blob([(178, 104), (204, 108), (212, 132), (200, 148), (180, 140)]), BR)
    c.part(tube([(200, 136), (208, 160), (198, 180)], [27, 21, 17]), BR)
    c.part(ell(194, 182, 13, 7), BR)
    for i in range(3):
        c.part(claw((186 + i * 5, 184), (180 + i * 5, 192), 2, 3.5), CL, line=1)
    # nabije voorpoot
    c.part(tube([(110, 158), (96, 190), (80, 214)], [30, 23, 19]), BR)
    c.part(ell(76, 215, 13, 9, -30), BR)
    paw_claws(c, 70, 218, 145)
    # kop: ronde schedel, kleine ronde oren, langere snuit omlaag naar links
    k, px, py = 1.25, 80, 168
    T = lambda pts: [(px + (x - px) * k, py + (y - py) * k) for x, y in pts]
    E = lambda x, y, rx, ry, r=0: T(ell(x, y, rx, ry, r))
    e2 = c.part(E(88, 128, 11, 10, 20), BR)
    c.mark(E(88, 130, 5, 5), TAN, e2)
    e1 = c.part(E(56, 126, 12, 11, -15), BR)
    c.mark(E(57, 128, 6, 6), TAN, e1)
    h = c.part(blob(T([(40, 150), (50, 132), (70, 126), (92, 134), (100, 152), (94, 170), (74, 182), (52, 176)])), BR)
    sn = c.part(blob(T([(54, 154), (40, 164), (28, 176), (21, 186), (24, 194), (36, 196), (54, 190), (72, 180), (66, 164)])), BR, line=0)
    c.mark(blob(T([(34, 196), (52, 189), (74, 182), (92, 172), (98, 186), (60, 204), (24, 204)])), TAN, h | sn)
    # masker: donker rond beide ogen, loopt als streep over de snuitrug
    hs = h | sn
    c.mark(blob(T([(32, 166), (42, 148), (62, 142), (82, 146), (84, 162), (70, 172), (48, 176), (32, 178)])), MK, hs)
    for x, y, rx, ry in ((64, 157, 8.5, 9), (41, 165, 6, 7.5)):
        m = c.part(E(x, y, rx, ry, -10), EY, line=1.2)
        c.part(E(x - rx * 0.1, y + ry * 0.15, rx * 0.45, ry * 0.55), '#1A0F0B', line=0, clip=m)
        c.part(E(x - rx * 0.35, y - ry * 0.35, rx * 0.28, rx * 0.28), '#FFFFFF', line=0, clip=m)
        # zware wenkbrauw/ooglid: maakt de blik loerend
        c.stroke(T([(x - rx * 1.2, y - ry * 0.55), (x + rx * 1.1, y - ry * 0.95)]), 2.4)
    c.part(E(23, 188, 6, 5, -20), NO, line=1.4)
    c.stroke(T(qbez((30, 197), (38, 200), (46, 196), 8)), 1.4)
    # snuitomlijning (de snuit is zonder eigen lijn getekend om naad met de kop te vermijden)
    return c.finish(outer=3.0)


F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)


def sheet():
    a, sa = draw(tail_up)
    b, sb = draw(tail_down)
    a.save(os.path.join(OUT, 'schets_A_staart_omhoog.png'))
    b.save(os.path.join(OUT, 'schets_B_staart_omlaag.png'))
    W, H = 256 * 4 + 50, 256 + 130
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 8), 'Olinguito v2: schets (geen pixels)', font=FB, fill=(30, 30, 30))
    x = 10
    for lab, img, sil in (('A: staart omhoog', a, sa), ('B: staart omlaag', b, sb)):
        im.paste(img, (x, 34))
        silim = Image.new('RGB', (256, 256), 'white')
        silim.paste(Image.new('RGB', (256, 256), (70, 66, 84)), (0, 0), sil)
        im.paste(silim, (x + 266, 34))
        d.text((x, 34 + 258), lab, font=FS, fill=(90, 90, 90))
        d.text((x + 266, 34 + 258), 'silhouet', font=FS, fill=(90, 90, 90))
        x += 532
    lines = ['Pose: boomfoto + Linoone: kop omlaag naar links, rug als boog omhoog, lange dikke staart.',
             'Olinguito: ronde kop, kleine ronde oren, donkerbruine vacht, goudbruine keel. Anders: langere snuit, donker masker, 2 lange klauwen per voorpoot.',
             'Sinister: roodbruine ogen in het masker onder een zware wenkbrauw.']
    for i, ln in enumerate(lines):
        d.text((10, 34 + 278 + i * 18), ln, font=F, fill=(30, 30, 30))
    im.save(os.path.join(OUT, 'schetsen.png'))


sheet()
