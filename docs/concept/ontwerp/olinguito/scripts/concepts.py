import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
import math

OR = '#E58A3A'   # oranjebruine vacht (echte olinguito)
CR = '#FBE2AE'   # creme snuit/buik/klauwen
CH = '#6E3C27'   # chocolade masker/sokken/ringen
GO = '#FFC21F'   # goudgele ogen (enige gloeiende accent)
CL = '#FFF3D9'   # klauwen (creme-familie)


def sly_eye(c, x, y, rx, ry, lid_tilt, iris=GO, clip=None):
    """Sluw half-dicht oog: iris + pupil + glans, bovenste deel afgedekt door het ooglid."""
    m = c.part(ell(x, y, rx, ry), iris, line=1.2)
    c.part(ell(x - rx * 0.15, y + ry * 0.1, rx * 0.38, ry * 0.62), '#2A1A16', line=0, clip=m)
    c.part(ell(x - rx * 0.32, y - ry * 0.05, rx * 0.2, rx * 0.2), '#FFFFFF', line=0, clip=m)
    # ooglid: schuine afdekking (sluw), in maskerkleur, met lijn
    lid = [(x - rx * 1.4, y - ry * 1.6), (x + rx * 1.4, y - ry * 1.6),
           (x + rx * 1.4, y - ry * 0.05 + lid_tilt), (x - rx * 1.4, y - ry * 0.05 - lid_tilt)]
    lm = c.mask(lid) & m
    c.rgb[lm] = hexc(CH)
    edge = [(x - rx * 1.25, y - ry * 0.05 - lid_tilt * 0.9), (x + rx * 1.25, y - ry * 0.05 + lid_tilt * 0.9)]
    c.stroke(edge, 2.2)


def zigzag(top, bottom, h, back):
    """Getande vachtrand: tussen de punten van `top` steken pieken omhoog en naar achteren."""
    out = []
    for i in range(len(top) - 1):
        a, b = top[i], top[i + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        nx, ny = dy / L, -dx / L
        out.append(a)
        out.append(((a[0] + b[0]) / 2 + nx * h + dx * back, (a[1] + b[1]) / 2 + ny * h + dy * back))
    out.append(top[-1])
    return out + bottom[::-1]


def side_eye(c, x, y, rx, ry):
    """Grote 'onschuldige' ogen die opzij kijken (naar de staart)."""
    m = c.part(ell(x, y, rx, ry), GO, line=1.2)
    c.part(ell(x + rx * 0.35, y + ry * 0.05, rx * 0.45, ry * 0.6), '#2A1A16', line=0, clip=m)
    c.part(ell(x + rx * 0.2, y - ry * 0.3, rx * 0.22, rx * 0.22), '#FFFFFF', line=0, clip=m)


def head(c, hx, hy, R, eyes='sly', mask_col=CH, ear_inner=CR, smirk=True, ears=True, extra_behind=None, ear_col=OR, cap=None):
    if extra_behind:
        extra_behind()
    if ears:
        e1 = c.part(ell(hx - R * 0.62, hy - R * 0.78, R * 0.30, R * 0.28, -20), ear_col)
        c.mark(ell(hx - R * 0.60, hy - R * 0.74, R * 0.15, R * 0.14, -20), ear_inner, e1)
        e2 = c.part(ell(hx + R * 0.55, hy - R * 0.88, R * 0.27, R * 0.26, 20), ear_col)
        c.mark(ell(hx + R * 0.55, hy - R * 0.84, R * 0.13, R * 0.12, 20), ear_inner, e2)
    h = c.part(ell(hx, hy, R * 1.05, R * 0.94), OR)
    # masker: één band dwars over de ogen (vachttekening, geen bril)
    band = blob([(hx - R * 1.2, hy - R * 0.30), (hx - R * 0.3, hy - R * 0.42), (hx + R * 0.5, hy - R * 0.50),
                 (hx + R * 1.2, hy - R * 0.42), (hx + R * 1.2, hy + R * 0.02), (hx + R * 0.5, hy + R * 0.02),
                 (hx + R * 0.05, hy + R * 0.18), (hx - R * 0.45, hy + R * 0.12), (hx - R * 1.2, hy + R * 0.10)])
    c.mark(band, mask_col, h)
    if cap:
        c.mark(cap, mask_col, h)
    # snuit (kort, teddybeer), steekt iets uit naar links
    mz = c.part(ell(hx - R * 0.55, hy + R * 0.38, R * 0.50, R * 0.34, -8), CR, line=1.6)
    c.part(ell(hx - R * 0.98, hy + R * 0.25, R * 0.15, R * 0.11), '#3A2420', line=1.0)
    c.dot(hx - R * 1.02, hy + R * 0.21, R * 0.04, '#FFFFFF')
    # ogen in de band
    if eyes == 'side':
        side_eye(c, hx - R * 0.42, hy - R * 0.14, R * 0.19, R * 0.22)
        side_eye(c, hx + R * 0.30, hy - R * 0.20, R * 0.15, R * 0.19)
    elif eyes == 'narrow':
        sly_eye(c, hx - R * 0.42, hy - R * 0.12, R * 0.22, R * 0.15, R * 0.10)
        sly_eye(c, hx + R * 0.30, hy - R * 0.18, R * 0.18, R * 0.13, R * 0.09)
    else:
        sly_eye(c, hx - R * 0.42, hy - R * 0.12, R * 0.20, R * 0.17, R * 0.07)
        sly_eye(c, hx + R * 0.30, hy - R * 0.18, R * 0.16, R * 0.15, R * 0.06)
    if smirk:
        # scheve grijns met een hoektand
        c.stroke(qbez((hx - R * 0.88, hy + R * 0.50), (hx - R * 0.55, hy + R * 0.66), (hx - R * 0.18, hy + R * 0.42)), 2.0)
        c.part([(hx - R * 0.40, hy + R * 0.56), (hx - R * 0.30, hy + R * 0.52), (hx - R * 0.36, hy + R * 0.70)], '#FFFFFF', line=1.0)
    return h


def tail_rings(c, pts, widths, rings, tip_col=CH, base=OR):
    """Geringde staart als doorlopende buis; ringen als vachttekening (index-bereiken)."""
    tm = c.part(tube(pts, widths), base, line=2.0)
    for a, b in rings:
        sub = pts[a:b + 1]
        c.mark(tube(sub, [w + 8 for w in widths[a:b + 1]]), CH, tm)
    if tip_col:
        c.mark(tube(pts[-4:], [w + 8 for w in widths[-4:]]), tip_col, tm)
    return tm


# ---------------------------------------------------------------- A: Klauwdief
def concept_A():
    c = Canvas()
    # staart achter, omhoog naar rechts en krul aan het eind
    tp = qbez((160, 200), (252, 198), (236, 112), 30) + qbez((236, 112), (230, 84), (244, 74), 8)[1:]
    ws = [30 - 10 * i / (len(tp) - 1) for i in range(len(tp))]
    ws[-1] = 6; ws[-2] = 13
    tail_rings(c, tp, ws, [(9, 12), (16, 19), (23, 26), (29, 32)])
    # verre achterpoot
    c.part(ell(170, 213, 17, 11), CH)
    # lijf (peer, licht voorovergebogen, op de tenen)
    body = c.part(blob([(112, 140), (148, 130), (174, 150), (182, 186), (168, 214), (132, 220), (108, 202), (100, 170)]), OR)
    c.mark(ell(128, 182, 22, 30, -10), CR, body)
    # nabije achterpoot (dij + sok + tenen)
    th = c.part(ell(128, 204, 22, 18, -15), OR)
    c.part(blob([(104, 214), (128, 208), (140, 220), (130, 230), (100, 230)]), CH)
    # verre arm omlaag naar voren, klauwen naar beneden
    c.part(tube(qbez((112, 160), (92, 168), (80, 186)), [18 - 3 * i / 24 for i in range(25)]), OR, open_at=(112, 160, 10))
    for b, t, bd in [((68, 190), (44, 222), -10), ((78, 195), (64, 236), -10), ((89, 195), (90, 232), -8)]:
        c.part(claw(b, t, bd, 16), CL, line=1.6)
    c.part(ell(79, 188, 14, 11), CH)
    # kop
    head(c, 96, 96, 50)
    # nabije arm omhoog naast de kop: de klauwen zijn het silhouet
    c.part(tube(qbez((150, 160), (178, 152), (180, 124)), [19] * 25), OR, open_at=(150, 160, 11))
    for b, t, bd in [((169, 114), (154, 70), 12), ((179, 110), (182, 58), 11), ((190, 114), (218, 74), 9)]:
        c.part(claw(b, t, bd, 17), CL, line=1.6)
    c.part(ell(180, 120, 15, 12), CH)
    return c


# ---------------------------------------------------------------- B: Haakstaart
def concept_B():
    c = Canvas()
    # staart: dik en rechtop achter het lijf (zoals een coati), bovenaan een haak naar voren
    tp = (qbez((160, 214), (226, 214), (218, 130), 16) + qbez((218, 130), (214, 22), (172, 16), 14)[1:]
          + qbez((172, 16), (148, 12), (154, 32), 8)[1:] + qbez((154, 32), (158, 42), (168, 38), 4)[1:])
    n = len(tp)
    ws = [30 - 12 * i / (n - 1) for i in range(n)]
    ws[-1] = 6; ws[-2] = 11; ws[-3] = 14
    tail_rings(c, tp, ws, [(8, 11), (15, 18), (21, 24), (27, 30)])
    c.part(blob([(150, 28), (164, 32), (178, 50), (164, 44), (152, 42)]), CH, line=1.6)
    # lijf zittend, onschuldig rechtop
    body = c.part(blob([(112, 146), (150, 140), (174, 164), (184, 200), (172, 226), (132, 230), (106, 214), (100, 180)]), OR)
    c.mark(ell(130, 192, 24, 30, -4), CR, body)
    # achterpoten (haunches) + voeten
    c.part(ell(166, 206, 22, 22, 10), OR)
    c.part(blob([(150, 224), (178, 220), (186, 232), (150, 236)]), CH)
    c.part(blob([(96, 224), (124, 220), (130, 232), (94, 236)]), CH)
    head(c, 100, 104, 48, eyes='side')
    # voorpoten samen voor de buik, klauwen met de toppen tegen elkaar ('gevouwen', schurkengebaar)
    c.part(tube(qbez((110, 156), (80, 184), (116, 190)), [17] * 25), OR, open_at=(110, 156, 9))
    c.part(tube(qbez((158, 158), (184, 186), (146, 192)), [17] * 25), OR, open_at=(158, 158, 9))
    for b_, t_, bd in [((112, 184), (124, 150), -7), ((120, 186), (130, 154), -6)]:
        c.part(claw(b_, t_, bd, 13), CL, line=1.4)
    for b_, t_, bd in [((152, 186), (138, 150), 7), ((144, 188), (134, 156), 6)]:
        c.part(claw(b_, t_, bd, 13), CL, line=1.4)
    c.part(ell(116, 190, 13, 11), CH)
    c.part(ell(146, 192, 13, 11), CH)
    return c


# ---------------------------------------------------------------- C: Mantel
PL = CH          # mantel = zelfde donkere vacht als masker en sokken


def concept_C():
    c = Canvas()
    hx, hy, R = 84, 118, 46
    # staart laag en pluizig achter
    tp = qbez((186, 186), (238, 196), (244, 146), 22)
    n = len(tp)
    ws = [24 + 6 * math.sin(math.pi * i / (n - 1)) for i in range(n)]
    ws[-1] = 10; ws[-2] = 18
    tail_rings(c, tp, ws, [(6, 9), (13, 16), (19, 21)], tip_col=CH)
    # verre poten
    c.part(ell(198, 214, 12, 10), CH)
    c.part(ell(126, 216, 11, 9), CH)
    # lijf laag, sluipend
    body = c.part(blob([(104, 150), (150, 138), (198, 150), (212, 184), (194, 208), (140, 212), (108, 202), (96, 176)]), OR)
    c.mark(ell(146, 204, 36, 12), CR, body)
    # mantel: donkere zadelvacht over nek en rug, getande onderrand (zoals Poochyena's tweekleur)
    c.mark([(90, 110), (150, 118), (206, 136), (224, 170), (210, 166), (200, 180), (188, 162), (176, 178), (164, 160),
            (150, 176), (140, 158), (126, 172), (116, 154), (100, 166)], PL, body)
    # manen: getande donkere vacht van kruin over nek tot rug, punten naar achteren
    c.part(zigzag(qbez((92, 90), (150, 88), (208, 140), 5), qbez((96, 124), (160, 132), (204, 158), 5), 24, 0.6), PL)
    # achterpoot + voorpoot met klauwen
    c.part(ell(190, 196, 18, 16), OR)
    c.part(blob([(178, 208), (200, 206), (208, 218), (178, 222)]), CH)
    c.part(tube(qbez((112, 184), (106, 204), (100, 214)), [17] * 25), OR, open_at=(112, 184, 10))
    c.part(ell(96, 218, 13, 8), CH)
    for b_, t_, bd in [((84, 218), (60, 228), -7), ((92, 222), (72, 238), -7)]:
        c.part(claw(b_, t_, bd, 12), CL, line=1.3)
    # kop: donkere schedel die in het masker overloopt, met getande rand
    cap = [(hx - R * 1.1, hy - R * 1.2), (hx + R * 1.3, hy - R * 1.3), (hx + R * 1.3, hy - R * 0.1),
           (hx + R * 0.80, hy - R * 0.36), (hx + R * 0.62, hy - R * 0.70), (hx + R * 0.38, hy - R * 0.44),
           (hx + R * 0.05, hy - R * 0.76), (hx - R * 0.20, hy - R * 0.46), (hx - R * 0.55, hy - R * 0.74),
           (hx - R * 0.80, hy - R * 0.40), (hx - R * 1.3, hy - R * 0.5)]
    head(c, hx, hy, R, mask_col=PL, ear_col=PL, ear_inner=OR, eyes='narrow')
    return c


# ---------------------------------------------------------------- silhouetten fase 2 en 3
G = '#4A4A5C'


def ringtail(c, pts, w0, w1):
    n = len(pts)
    c.part(tube(pts, [w0 + (w1 - w0) * i / (n - 1) for i in range(n)]), G, line=0)


def coati(c, tail='up', mane=False, claw_up=False):
    """Fase 2: coati op vier poten, lange opgewipte snuit, staart rechtop."""
    if tail == 'up':
        ringtail(c, qbez((196, 150), (214, 90), (206, 30), 20), 20, 10)
    elif tail == 'hook':
        ringtail(c, qbez((196, 150), (220, 60), (190, 22), 20) + qbez((190, 22), (164, 6), (160, 34), 8)[1:], 22, 8)
        c.part(blob([(152, 28), (168, 32), (176, 50), (160, 44)]), G, line=0)
    c.part(blob([(80, 140), (130, 126), (190, 130), (214, 156), (200, 184), (140, 190), (96, 180)]), G, line=0)
    for x in (96, 124, 172, 196):
        c.part(tube(qbez((x, 164), (x - 10, 196), (x - 4, 222), 8), [22 - i for i in range(9)]), G, line=0)
        c.part(ell(x - 8, 223, 11, 6), G, line=0)
    # kop met lange snuit die omhoog wipt
    c.part(ell(76, 118, 30, 26), G, line=0)
    c.part([(56, 108), (20, 96), (10, 88), (14, 100), (52, 132)], G, line=0)
    c.part(ell(76, 90, 9, 10), G, line=0)
    c.part(ell(98, 94, 9, 10), G, line=0)
    if mane:
        c.part(zigzag(qbez((70, 96), (140, 100), (214, 140), 7), qbez((80, 128), (150, 136), (210, 158), 7), 22, 0.6), G, line=0)
        ringtail(c, qbez((206, 156), (246, 150), (250, 112), 16), 22, 10)
    if claw_up:
        c.part(tube(qbez((100, 168), (76, 186), (58, 176), 8), [18 - i * 0.5 for i in range(9)]), G, line=0)
        for b_, t_, bd in [((56, 168), (22, 150), 7), ((54, 176), (16, 172), 4), ((58, 182), (24, 196), 0)]:
            c.part(claw(b_, t_, bd, 14), G, line=0)
    else:
        for x in (90, 118):
            for dx in (-12, -6, 0):
                c.part(claw((x + dx, 220), (x + dx - 14, 232), -4, 8), G, line=0)


def bandit(c, hood=False):
    """Fase 3: wasbeer op twee poten, slank en rechtop."""
    if hood:
        # mantel van vacht achter het lijf met getande zoom, en een kap met een punt naar achteren
        c.part([(140, 40), (200, 6), (184, 50), (204, 100), (222, 160), (230, 214), (214, 204), (206, 224), (192, 206),
                (180, 226), (168, 206), (156, 220), (150, 130)], G, line=0)
        c.part(blob([(98, 56), (116, 32), (150, 26), (172, 44), (170, 82), (150, 96), (112, 90)]), G, line=0)
    c.part(blob([(104, 98), (152, 96), (168, 128), (158, 160), (168, 190), (136, 202), (106, 190), (100, 160), (92, 128)]), G, line=0)
    for x, d in ((118, -8), (150, 8)):
        c.part(ell(x, 196, 16, 18), G, line=0)
        c.part(tube(qbez((x, 200), (x + d * 1.5, 222), (x + d, 236), 8), [24 - i for i in range(9)]), G, line=0)
        c.part(ell(x + d - 6, 240, 17, 7), G, line=0)
    c.part(ell(130, 66, 30, 28), G, line=0)
    c.part(ell(102, 76, 17, 11, -10), G, line=0)
    if not hood:
        c.part(ell(110, 38, 10, 12, -15), G, line=0)
        c.part(ell(150, 38, 10, 12, 15), G, line=0)


def evo_A2():
    c = Canvas(); coati(c, tail='up', claw_up=True); return c


def evo_A3():
    c = Canvas()
    ringtail(c, qbez((150, 180), (230, 190), (220, 110), 20), 24, 12)
    bandit(c)
    # beide handen met lange klauwen: één hand vooruit als dolken, één omlaag
    c.part(tube([(110, 110), (80, 120), (56, 112)], [18, 16, 15]), G, line=0)
    for b_, t_, bd in [((56, 104), (10, 84), 6), ((52, 112), (6, 108), 3), ((56, 120), (12, 132), -3)]:
        c.part(claw(b_, t_, bd, 13), G, line=0)
    c.part(tube([(156, 112), (176, 140), (182, 166)], [18, 16, 15]), G, line=0)
    for b_, t_, bd in [((176, 168), (170, 214), -5), ((184, 170), (186, 216), -4), ((190, 166), (204, 206), -3)]:
        c.part(claw(b_, t_, bd, 12), G, line=0)
    return c


def evo_B2():
    c = Canvas(); coati(c, tail='hook'); return c


def evo_B3():
    c = Canvas()
    # staart als boog: van achter de heup over de schouder naar voren, haak aan het eind
    ringtail(c, qbez((150, 190), (250, 140), (200, 30), 24) + qbez((200, 30), (150, -14), (96, 18), 14)[1:], 26, 12)
    c.part(blob([(88, 12), (100, 20), (108, 40), (94, 30)]), G, line=0)
    bandit(c)
    c.part(tube([(110, 112), (88, 140), (92, 168)], [17, 15, 14]), G, line=0)
    c.part(tube([(154, 112), (172, 140), (166, 168)], [17, 15, 14]), G, line=0)
    for x in (92, 166):
        for d in (-8, 0, 8):
            c.part(claw((x + d / 2, 166), (x + d, 196), -3, 9), G, line=0)
    return c


def evo_C2():
    c = Canvas(); coati(c, tail=None, mane=True); return c


def evo_C3():
    c = Canvas()
    ringtail(c, qbez((150, 186), (230, 196), (224, 130), 20), 24, 12)
    bandit(c, hood=True)
    c.part(tube([(110, 112), (84, 136), (74, 160)], [17, 15, 14]), G, line=0)
    for b_, t_, bd in [((70, 160), (56, 196), -4), ((76, 162), (70, 202), -3), ((82, 160), (86, 196), -2)]:
        c.part(claw(b_, t_, bd, 11), G, line=0)
    return c


if __name__ == '__main__':
    import os
    out = os.environ.get('OUT', '/tmp/')
    for name in sys.argv[1:]:
        im, sil = globals()[('concept_' + name) if len(name) == 1 else ('evo_' + name)]().finish()
        im.save(out + 'test_' + name + '.png')
        im.resize((512, 512), Image.NEAREST).save(out + 'test_' + name + '_2x.png')
