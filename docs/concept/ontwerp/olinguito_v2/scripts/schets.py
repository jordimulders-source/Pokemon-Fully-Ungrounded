"""Olinguito v2 (24 okt): modeltekening zonder pixels.
Ronde 1: schetsen_v1.png (staart omhoog/omlaag; Jordi koos omhoog).
Ronde 2 (Jordi): dunnere olinguito-staart, één oog en één dominant oor (profiel zoals Linoone),
meer olinguito/minder wasbeer, kortere neus (langer pas bij de coati), klauwen meer Linoone,
dynamischere poten met de achterpoten onder het lijf naar voren (boomfoto), geen buikvlak.
Ronde 3 (Jordi): rondere kop, langere staart (foto's), asymmetrische dynamische poten (boomfoto).
Ronde 4 (Jordi): veel kleiner oog (foto's), kop meer diagonaal naar de kijker (zoals Pokémon-sprites), oor iets groter.
Ronde 5 (Jordi): kopvorm naar referentie_kop.png (afgekeurd: niet dezelfde vorm).
Ronde 6 (Jordi): kop overgetrokken van referentie_kop.png (neus omlaag, oog laag bij de snuit, hoog voorhoofd,
oor bovenop); kleiner lijf, poten verder naar voren onder het lijf (boomfoto's).
Ronde 7 (Jordi): pose diagonaler (3/4 zoals Linoone, niet van opzij), poten niet op één lijn maar dynamisch
(zoals de olinguito beweegt), zwart masker oog-tot-oog over de snuitrug zoals Patrat, alleen net rond het oog.
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
MK = '#241712'   # zwart masker (Patrat-achtig, alleen rond het oog)
NO = '#C98088'   # roze neus
EY = '#B9481C'   # roodbruin oog
CL = '#EDE3CC'   # klauwen
MZ = '#8D7E76'   # lichtgrijze snuitpunt
EAR = '#4A3324'  # oorrand
EARIN = '#8A6C55'  # binnenkant oor
PAW = '#C08A80'  # roze voeten (foto's)
OUT = os.path.join(HERE, '..')


def tail(c):
    pts = (qbez((186, 104), (236, 82), (224, 36), 12)[:-1] + qbez((224, 36), (212, 8), (178, 16), 10)[:-1]
           + qbez((178, 16), (150, 24), (148, 48), 8))
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
    c.part(ell(x, y, 11, 7, -10), col)
    for i in range(3):
        c.part(claw((x - 9 + i * 5, y + 2), (x - 16 + i * 5, y + 9), 2, 3.5), CL, line=1)


def head_pts(pts, sc=0.45, rot=12, anchor=(93, 222), at=(38, 188), pivot=(215, 40)):
    """Punten uit referentie_kop.png (217x242) naar het canvas: schalen, iets draaien zodat
    de neus schuin naar links-omlaag wijst (diagonaal naar de kijker), neus op `at`."""
    r = math.radians(rot)
    def f(x, y):
        x, y = x - pivot[0], y - pivot[1]
        return x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r)
    ax, ay = f(*anchor)
    return [(at[0] + (f(x, y)[0] - ax) * sc, at[1] + (f(x, y)[1] - ay) * sc) for x, y in pts]


def draw():
    c = Canvas()
    H = head_pts
    He = lambda x, y, rx, ry, rot=0: H(ell(x, y, rx, ry, rot))
    # Diepte (3/4 zoals Linoone): de voorkant is dichtbij (groot, laag), de romp ver weg (kleiner, hoger).
    # Verre poten staan rechts van en hoger dan de nabije; elke poot in een andere fase van de stap.
    # verre achterpoot: gestrekt naar achteren, zet zich af (ver weg: hoog en klein)
    c.part(tube([(182, 120), (200, 140), (214, 156)], [20, 15, 12]), FAR)
    c.part(ell(218, 158, 9, 6, 35), '#9C6E66')
    # verre voorpoot: opgetild en gebogen, klauwen hangen (stapt)
    c.part(tube([(124, 146), (140, 170), (128, 188)], [20, 16, 13]), FAR)
    c.part(ell(124, 190, 9, 7, -10), '#9C6E66')
    paw_claws(c, 118, 193, 118, 26, '#D8CDB4')
    tail(c)
    # lijf loopt taps toe van de brede borst (dichtbij) naar de kleinere romp (ver weg)
    lijf = c.mask(blob([(82, 166), (88, 134), (112, 112), (142, 98), (166, 90), (184, 96), (190, 112),
                        (180, 130), (158, 146), (132, 166), (110, 192), (90, 190)]))
    c.part(lijf | c.mask(ell(172, 116, 18, 18, -20)), BR)
    c.stroke(qbez((158, 104), (150, 126), (166, 138), 10), 2.0)
    # nabije achterpoot: stapt naar voren onder de buik, voet laag (dichtbij)
    c.part(tube(qbez((166, 130), (140, 160), (162, 180), 10) + [(160, 192), (156, 202)], [24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 15, 14, 13]), BR)
    hind_foot(c, 152, 205, PAW)
    # nabije voorpoot: dikke schouder voor de borst, ver gestrekt naar voren-omlaag naar de kijker
    c.part(c.mask(ell(106, 160, 19, 22, -20)) | c.mask(tube([(104, 166), (86, 196), (68, 222)], [30, 22, 18])), BR)
    c.part(ell(64, 224, 12, 9, -30), PAW)
    paw_claws(c, 56, 228, 152)
    # kop, overgetrokken van referentie_kop.png: neus omlaag, oog laag bij de snuit, hoog rond voorhoofd
    c.part(H([(200, 22), (230, 60), (226, 110)]) and He(66, 34, 13, 12), EAR)   # verre oor: randje
    h = c.part(blob(H([(93, 230), (80, 220), (64, 198), (44, 166), (30, 125), (32, 88), (44, 54), (66, 26), (96, 10),
                       (128, 6), (162, 14), (190, 38), (208, 66), (212, 100), (204, 132), (184, 158), (152, 184),
                       (124, 206), (106, 224)])), HD)
    # warme kruin alleen achter-rechts, grijs gezicht, lichtere snuitpunt
    c.mark(blob(H([(150, 0), (240, 0), (240, 150), (206, 132), (198, 92), (182, 56), (162, 34)])), BR, h)
    c.mark(blob(H([(70, 196), (100, 186), (130, 198), (114, 238), (78, 238)])), MZ, h)
    # zwart masker zoals Patrat: van het oog over de snuitrug naar het verre oog (achter de omtrek),
    # alleen net rond het oog, niet rond de kop; schuine bovenrand = loerende blik
    c.mark(blob(H([(130, 122), (126, 156), (108, 162), (88, 154), (58, 148), (28, 146), (27, 134),
                   (56, 132), (84, 120), (108, 110)])), MK, h)
    # oor bovenop de kop, naar voren gericht: donkere rand, lichtere binnenkant
    e1 = c.part(He(124, 26, 32, 28, -5), EAR)
    c.mark(He(126, 33, 22, 19, -5), EARIN, e1)
    # oog laag in het gezicht, dicht bij de snuit
    ex, ey = H([(106, 137)])[0]
    m = c.part(ell(ex, ey, 5.6, 5.8), EY, line=1.0)
    c.part(ell(ex - 0.6, ey + 0.6, 2.8, 3.2), '#1A0F0B', line=0, clip=m)
    c.part(ell(ex - 1.8, ey - 1.8, 1.4, 1.4), '#FFFFFF', line=0, clip=m)
    c.part(He(93, 212, 14, 11), NO, line=1.4)
    for nx in (86, 99):
        c.dot(*H([(nx, 214)])[0], 0.9, '#5A2A2A')
    c.stroke(H(qbez((100, 226), (112, 224), (122, 214), 8)), 1.3)
    return c.finish(outer=3.0)


F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)


def sheet():
    a, sa = draw()
    a.save(os.path.join(OUT, 'schets_v2_ronde7.png'))
    W, H = 256 * 3 + 40, 256 + 110
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 8), 'Olinguito v2, ronde 7: schets (geen pixels)', font=FB, fill=(30, 30, 30))
    im.paste(a, (10, 34))
    silim = Image.new('RGB', (256, 256), 'white')
    silim.paste(Image.new('RGB', (256, 256), (70, 66, 84)), (0, 0), sa)
    im.paste(silim, (276, 34))
    small = a.resize((64, 64), Image.LANCZOS).resize((256, 256), Image.NEAREST)
    im.paste(small, (542, 34))
    for x, t in ((10, 'schets'), (276, 'silhouet'), (542, 'op spritegrootte (64×64)')):
        d.text((x, 292), t, font=FS, fill=(90, 90, 90))
    lines = ['Kop overgetrokken van de foto, één oog, één dominant oor, lange dunne staart omhoog.',
             'Ronde 7: diagonaler (dichtbij groot/laag, romp ver weg), poten in verschillende fasen, masker oog-tot-oog.']
    for i, ln in enumerate(lines):
        d.text((10, 312 + i * 18), ln, font=F, fill=(30, 30, 30))
    im.save(os.path.join(OUT, 'schetsen_v2_ronde7.png'))


sheet()
