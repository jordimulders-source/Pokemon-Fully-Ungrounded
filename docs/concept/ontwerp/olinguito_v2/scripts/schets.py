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
Ronde 8 (Jordi): achterpoten gehurkt (boomfoto's): grote dij, knie scherp gebogen, hak laag, voet plat naar voren.
Ronde 9 (Jordi): echte driekwartpose: voorpoten naast elkaar van voren, lijf verkort naar achteren.
Ronde 10 (Jordi): lijf + kop verder gedraaid zoals Rattata/Growlithe/Galar-Zigzagoon (referentie_driekwart_*):
kop vooraan, gezicht naar de kijker, snuit schuin links-omlaag, lijf erachter naar rechtsboven; 3 poten zichtbaar.
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
    pts = (qbez((192, 108), (240, 84), (226, 38), 12)[:-1] + qbez((224, 36), (212, 8), (178, 16), 10)[:-1]
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


def crouch_leg(c, hip, knee, hock, toe, col, foot_col, w=22):
    """Gehurkte achterpoot: dij naar voren-omlaag, scheen scherp terug naar een lage hak,
    voet plat naar voren (zoals op de boomfoto's)."""
    c.part(blob(tube([hip, knee, hock], [w, w * 0.75, w * 0.55])), col)
    c.part(tube([hock, toe], [w * 0.55, w * 0.45]), foot_col)
    for i in range(3):
        c.part(claw((toe[0] - 2 + i * 4, toe[1] + 1), (toe[0] - 9 + i * 4, toe[1] + 7), 2, 3.5), CL, line=1)


def head_pts(pts, sc=0.5, rot=26, anchor=(93, 222), at=(46, 190), pivot=(215, 40)):
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
    # Driekwart zoals Rattata/Growlithe: de kop vooraan links met het gezicht naar de kijker,
    # de borst eronder, het lijf erachter schuin naar rechtsboven (grotendeels achter de kop).
    # verre achterpoot valt achter de nabije weg: 3 poten zichtbaar (Jordi)
    tail(c)
    lijf = c.mask(blob([(96, 128), (120, 104), (150, 94), (176, 96), (194, 110), (196, 134), (184, 156),
                        (160, 174), (132, 194), (104, 198), (88, 176)]))
    c.part(lijf | c.mask(ell(174, 140, 24, 24, -20)), BR)
    c.stroke(qbez((154, 122), (146, 148), (164, 162), 10), 2.0)
    # nabije achterpoot: gehurkt, rechtsonder
    crouch_leg(c, (172, 148), (152, 174), (176, 194), (156, 204), BR, PAW, w=26)
    # verre voorpoot: rechts naast de nabije, licht gebogen, staat
    c.part(c.mask(ell(122, 176, 15, 17)) | c.mask(tube([(124, 182), (132, 204), (124, 220)], [22, 18, 15])), FAR)
    c.part(ell(120, 222, 10, 7, -10), '#9C6E66')
    paw_claws(c, 113, 225, 160, 30, '#D8CDB4')
    # nabije voorpoot: onder de kin, stapt naar voren-links
    c.part(c.mask(ell(94, 174, 18, 20)) | c.mask(tube([(92, 180), (80, 206), (66, 228)], [28, 22, 18])), BR)
    c.part(ell(62, 230, 12, 9, -30), PAW)
    paw_claws(c, 54, 234, 155)
    # kop in driekwart: ronde schedel (vorm van referentie_kop.png), gezicht naar de kijker,
    # verkorte snuit schuin links-omlaag; de verre wang blijft links van de snuit zichtbaar
    k, px, py = 1.2, 100, 176
    T = lambda pts: [(px + (x - px) * k, py + (y - py) * k) for x, y in pts]
    E = lambda x, y, rx, ry, r=0: T(ell(x, y, rx, ry, r))
    c.part(E(82, 112, 7, 6), EAR)                      # verre oor: randje achter de schedel
    h = c.part(c.mask(E(98, 140, 36, 33, -10)) |
               c.mask(blob(T([(82, 136), (66, 150), (56, 166), (51, 178), (57, 187), (72, 187), (90, 176), (98, 158)]))), HD)
    # warme kruin achter-rechts, lichtere snuitpunt
    c.mark(blob(T([(96, 98), (146, 104), (146, 176), (128, 152), (118, 126), (104, 112)])), BR, h)
    c.mark(blob(T([(48, 170), (62, 167), (78, 178), (72, 194), (48, 194)])), MZ, h)
    # zwart masker zoals Patrat: rond het oog en over de snuitrug naar het verre oog (achter de snuitrug),
    # niet rond de kop; bovenrand zakt naar de snuitrug (loerend)
    c.mark(blob(T([(110, 140), (108, 153), (100, 156), (91, 152), (78, 151), (67, 150), (66, 145), (78, 143), (91, 139), (102, 135)])), MK, h)
    # nabije oor: dominant, achter-boven op de kop
    e1 = c.part(E(124, 110, 15, 14, 20), EAR)
    c.mark(E(125, 112, 10, 9, 20), EARIN, e1)
    ex, ey = T([(100, 146)])[0]
    m = c.part(ell(ex, ey, 5.6, 5.8), EY, line=1.0)
    c.part(ell(ex - 0.6, ey + 0.6, 2.8, 3.2), '#1A0F0B', line=0, clip=m)
    c.part(ell(ex - 1.8, ey - 1.8, 1.4, 1.4), '#FFFFFF', line=0, clip=m)
    c.part(E(53, 180, 6, 5, -20), NO, line=1.4)
    c.dot(*T([(51, 181)])[0], 1.0, '#5A2A2A')
    c.dot(*T([(56, 182)])[0], 1.0, '#5A2A2A')
    c.stroke(T(qbez((60, 188), (69, 191), (78, 186), 8)), 1.3)
    return c.finish(outer=3.0)


F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)


def sheet():
    a, sa = draw()
    a.save(os.path.join(OUT, 'schets_v2_ronde10.png'))
    W, H = 256 * 3 + 40, 256 + 110
    im = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(im)
    d.text((10, 8), 'Olinguito v2, ronde 10: schets (geen pixels)', font=FB, fill=(30, 30, 30))
    im.paste(a, (10, 34))
    silim = Image.new('RGB', (256, 256), 'white')
    silim.paste(Image.new('RGB', (256, 256), (70, 66, 84)), (0, 0), sa)
    im.paste(silim, (276, 34))
    small = a.resize((64, 64), Image.LANCZOS).resize((256, 256), Image.NEAREST)
    im.paste(small, (542, 34))
    for x, t in ((10, 'schets'), (276, 'silhouet'), (542, 'op spritegrootte (64×64)')):
        d.text((x, 292), t, font=FS, fill=(90, 90, 90))
    lines = ['Kop overgetrokken van de foto, één oog, één dominant oor, lange dunne staart omhoog.',
             'Driekwart zoals Rattata/Growlithe: kop vooraan met het gezicht naar de kijker, lijf erachter naar rechtsboven.']
    for i, ln in enumerate(lines):
        d.text((10, 312 + i * 18), ln, font=F, fill=(30, 30, 30))
    im.save(os.path.join(OUT, 'schetsen_v2_ronde10.png'))


sheet()
