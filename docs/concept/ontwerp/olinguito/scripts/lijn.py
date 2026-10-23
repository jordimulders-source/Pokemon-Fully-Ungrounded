"""Ruwe modeltekening van de hele lijn (concept B, Haakstaart): fase 1 + fase 2 (coati) + fase 3 (Robin Hood-wasbeer).
Zelfde stijl en bibliotheek als concepts.py. Draaien vanuit de repo-root:
    python3 docs/concept/ontwerp/olinguito/scripts/lijn.py
Schrijft docs/concept/ontwerp/olinguito/lijn.png."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
from lib import *
import concepts as C

OR2 = '#C8692E'   # fase 2: iets dieper roodbruin (coati)
OR3 = '#9C5A34'   # fase 3: warm donkerbruin (krabbenetende wasbeer), nog steeds geen grijs
CH = C.CH
CR = C.CR
CL = C.CL
GO = C.GO


def ringtail(c, pts, w0, w1, base, rings, tip=CH):
    n = len(pts)
    ws = [w0 + (w1 - w0) * i / (n - 1) for i in range(n)]
    m = c.part(tube(pts, ws), base, line=2.0)
    for a, b in rings:
        c.mark(tube(pts[a:b + 1], [w + 8 for w in ws[a:b + 1]]), CH, m)
    if tip:
        c.mark(tube(pts[-4:], [w + 8 for w in ws[-4:]]), tip, m)
    return m


def hook_barb(c, pts):
    c.part(blob(pts), CH, line=1.6)


def fase2():
    """Coati: op vier poten, snuit omhoog, staart rechtop als herdersstaf met de weerhaak; lange graafklauwen."""
    c = Canvas()
    tp = qbez((190, 150), (226, 96), (206, 34), 18) + qbez((206, 34), (190, 6), (162, 18), 10)[1:] + qbez((162, 18), (150, 30), (160, 46), 6)[1:]
    ringtail(c, tp, 22, 9, OR2, [(5, 7), (10, 12), (15, 17), (20, 22)])
    hook_barb(c, [(152, 40), (166, 42), (176, 58), (162, 54)])
    # verre poten
    for x in (118, 196):
        c.part(tube(qbez((x, 170), (x - 6, 196), (x - 2, 216), 8), [18 - i for i in range(9)]), OR2, line=2.0)
        c.part(ell(x - 4, 218, 11, 6), CH)
    # lijf: lang en laag
    body = c.part(blob([(78, 140), (128, 124), (186, 126), (214, 150), (204, 180), (150, 188), (100, 182), (72, 164)]), OR2)
    c.mark(ell(126, 176, 40, 12), CR, body)
    # nabije poten met lange klauwen
    for x in (98, 172):
        c.part(tube(qbez((x, 166), (x - 6, 198), (x - 2, 222), 8), [22 - i for i in range(9)]), OR2, line=2.0)
        c.part(ell(x - 6, 224, 13, 7), CH)
        for d in (-14, -8, -2):
            c.part(claw((x + d, 226), (x + d - 12, 238), -4, 7), CL, line=1.2)
    # kop: langere snuit die omhoog wipt, oren kleiner, zelfde band
    hx, hy, R = 74, 112, 32
    e1 = c.part(ell(hx - 12, hy - 28, 9, 10, -15), OR2); c.mark(ell(hx - 12, hy - 27, 4, 5), CR, e1)
    e2 = c.part(ell(hx + 16, hy - 30, 8, 9, 15), OR2); c.mark(ell(hx + 16, hy - 29, 4, 4), CR, e2)
    h = c.part(ell(hx, hy, R, R * 0.86), OR2)
    c.mark(blob([(hx - 40, hy - 12), (hx - 6, hy - 18), (hx + 30, hy - 20), (hx + 36, hy - 4), (hx + 10, hy + 2),
                 (hx - 10, hy + 6), (hx - 40, hy + 4)]), CH, h)
    sn = c.part([(hx - 20, hy + 2), (hx - 56, hy - 8), (hx - 66, hy - 12), (hx - 64, hy - 2), (hx - 30, hy + 22)], CR, line=1.6)
    c.part(ell(hx - 64, hy - 8, 6, 5), '#3A2420', line=1.0)
    C.sly_eye(c, hx - 12, hy - 7, 6.5, 5.5, 2.4)
    C.sly_eye(c, hx + 14, hy - 9, 5.5, 5, 2.0)
    c.stroke(qbez((hx - 44, hy + 10), (hx - 30, hy + 16), (hx - 18, hy + 10)), 2.0)
    return c


def fase3():
    """Krabbenetende wasbeer als Robin Hood: rechtop, staart als gespannen boog over de schouder (haak = pijlpunt),
    een puntige vachtkap (uit de kruin, geen kleding), klauwen als dolken. Masker = het Robin Hood-masker."""
    c = Canvas()
    # staart: van de heup omhoog en als boog over de schouder naar voren, haak aan het eind
    tp = qbez((150, 196), (246, 150), (206, 40), 22) + qbez((206, 40), (170, 0), (110, 22), 14)[1:] + qbez((110, 22), (96, 30), (104, 44), 5)[1:]
    ringtail(c, tp, 24, 9, OR3, [(5, 7), (11, 13), (17, 19), (23, 25), (29, 31)])
    hook_barb(c, [(96, 40), (108, 42), (118, 58), (104, 54)])
    # benen
    for x, d in ((116, -6), (150, 6)):
        c.part(ell(x, 196, 16, 17), OR3)
        c.part(tube(qbez((x, 200), (x + d * 1.4, 222), (x + d, 236), 8), [22 - i for i in range(9)]), OR3, line=2.0)
        c.part(ell(x + d - 4, 240, 16, 7), CH)
    # lijf: slank, rechtop, creme borst
    body = c.part(blob([(104, 98), (150, 96), (168, 128), (160, 164), (168, 192), (134, 204), (104, 192), (98, 160), (90, 128)]), OR3)
    c.mark(ell(128, 150, 18, 34), CR, body)
    # vachtkap: kruinvacht in maskerkleur, punt naar achteren (Robin Hood uit het eigen lijf)
    hx, hy, R = 128, 70, 30
    c.part([(hx - 26, hy - 22), (hx + 4, hy - 40), (hx + 40, hy - 38), (hx + 70, hy - 52), (hx + 50, hy - 26), (hx + 30, hy - 8)], CH, line=2.0)
    e1 = c.part(ell(hx - 18, hy - 26, 8, 10, -15), OR3); c.mark(ell(hx - 18, hy - 25, 4, 5), CR, e1)
    h = c.part(ell(hx, hy, R, R * 0.92), OR3)
    c.mark([(hx - 40, hy - 30), (hx + 40, hy - 36), (hx + 40, hy - 16), (hx - 10, hy - 18), (hx - 40, hy - 12)], CH, h)
    # masker: smalle Robin Hood-band met punten aan de zijkant
    c.mark(blob([(hx - 40, hy - 6), (hx - 14, hy - 12), (hx + 16, hy - 14), (hx + 40, hy - 12), (hx + 36, hy + 4),
                 (hx + 6, hy + 2), (hx - 12, hy + 6), (hx - 40, hy + 6)]), CH, h)
    c.part(ell(hx - 22, hy + 12, 14, 10, -8), CR, line=1.6)
    c.part(ell(hx - 34, hy + 8, 5, 4), '#3A2420', line=1.0)
    C.sly_eye(c, hx - 10, hy - 3, 6.5, 5, 2.6)
    C.sly_eye(c, hx + 16, hy - 5, 5.5, 4.5, 2.2)
    c.stroke(qbez((hx - 30, hy + 18), (hx - 18, hy + 22), (hx - 6, hy + 14)), 2.0)
    # armen: één hand vooruit met klauwen als dolken, de andere omlaag
    c.part(tube([(108, 112), (82, 124), (60, 118)], [18, 16, 15]), OR3, line=2.0)
    c.part(ell(58, 118, 11, 9), CH)
    for b_, t_, bd in [((54, 110), (16, 92), 5), ((50, 118), (10, 116), 2), ((54, 126), (18, 140), -3)]:
        c.part(claw(b_, t_, bd, 11), CL, line=1.3)
    c.part(tube([(154, 112), (172, 140), (176, 164)], [18, 16, 15]), OR3, line=2.0)
    c.part(ell(176, 166, 11, 9), CH)
    for b_, t_, bd in [((170, 172), (164, 206), -4), ((178, 174), (180, 210), -3), ((186, 170), (198, 202), -2)]:
        c.part(claw(b_, t_, bd, 10), CL, line=1.2)
    return c


if __name__ == '__main__':
    REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../..')) + '/'
    OUT = REPO + 'docs/concept/ontwerp/olinguito/lijn.png'
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
    ims = [C.concept_B().finish()[0], fase2().finish()[0], fase3().finish()[0]]
    lines = [
        'Fase 1 (olinguito): zit braaf, klauwen gevouwen, kijkt opzij; de dief zit in de haakstaart achter zijn rug.',
        'Fase 2 (coati): op vier poten, snuit omhoog, staart rechtop als herdersstaf met dezelfde weerhaak; lange graafklauwen.',
        'Fase 3 (krabbenetende wasbeer): rechtop; de staart loopt als gespannen boog over de schouder (de haak is de pijlpunt),',
        '   een puntige vachtkap uit de kruin en het masker als Robin Hood-masker; klauwen als dolken. Geen kleding: alles is vacht.',
        'Kleur wordt per fase dieper (oranjebruin → roodbruin → warm donkerbruin); creme, chocolade en goud blijven gelijk.',
    ]
    W = max(768, int(max(ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(ln, font=F) for ln in lines)) + 24)
    H = 36 + 256 + 22 + 18 * len(lines) + 10
    sheet = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), 'Olinguito-lijn (concept B, Haakstaart)', font=FB, fill=(30, 30, 30))
    d.text((370, 12), 'ruwe modeltekening, fase 2 en 3 nog niet goedgekeurd', font=FS, fill=(90, 90, 90))
    for i, im in enumerate(ims):
        sheet.paste(im, (i * 256, 36))
    for i, t in enumerate(['fase 1: olinguito', 'fase 2: coati', 'fase 3: wasbeer (Robin Hood)']):
        d.text((i * 256 + 10, 36 + 256), t, font=FS, fill=(90, 90, 90))
    y = 36 + 256 + 22
    for ln in lines:
        d.text((10, y), ln, font=F, fill=(30, 30, 30))
        y += 18
    sheet.save(OUT)
    print(OUT)
