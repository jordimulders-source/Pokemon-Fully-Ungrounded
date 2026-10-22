"""Nachtaap fase 1, ronde 2 ("Maanogen"): bouwt anim_front.png + normal.pal.
python3 build.py <uitmap> [--preview pad.png]
Vormen uit tools/concept/sprites/layerlib.py, details (ogen, teken, handen) per pixel.
"""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../../../../tools/concept/sprites'))
from layerlib import *

# ---- palet (index: kleur) ----
PAL = [hexc(h) for h in [
    '#94CD9C',                                  # 0 transparant
    '#DED5F6', '#A99CD5', '#7465A4', '#41356A',  # 1-4 vacht licht->donker (2 = basis, 4 = selout)
    '#F6F6FF', '#BDC5DE', '#8B8BB4',             # 5-7 zilver: sikkels, snuit, voorhoofd
    '#FFAED5', '#EE6AA4', '#AC3973',             # 8-10 magenta: neus, oren, kussentjes, staartpunt, ruit
    '#EEFFF6', '#8BEEE6', '#39A4AC',             # 11-13 ogen (maangloed)
    '#FFFFFF',                                   # 14 glans
    '#101010']]                                  # 15 omlijning
RAMPS = {'vacht': [1, 2, 3, 4, 3], 'zilver': [5, 6, 7, 7], 'magenta': [8, 9, 10, 10]}

HX, HY = 28, 24           # middelpunt van de kop
SX, SY = 51, 30           # middelpunt van de spiraal


def tail_pts(up):
    return bezier((HX + 8, 53), (SX - 1, 54), (SX + 0.3, SY + 10.5 - up)) + \
        spiral(SX, SY - up, 10.5, 1.8, 90, 90 - 560)


def body(frame):
    C = Canvas()
    up = 1 if frame == 2 else 0
    # staart: steel vanachter het lijf en de Nazca-spiraal (1 3/4 slag, 2 px dik)
    tp = tail_pts(up)
    C.layer(stroke(tp, 2.05), 'vacht', light=(SX - 3, SY - 3 - up, 12, 12), shade=(0.5, -0.3),
            inner=stroke(tp, 1.05))
    # oortjes (achter de kop)
    for ex in (HX - 14, HX + 14):
        C.layer(ellipse(ex, HY - 7, 4.2, 4.2), 'vacht', light=(ex, HY - 7, 4.2, 4.2))
    # gevouwen benen en peerlijf
    C.layer(ellipse(HX, 53.5, 12, 4.2), 'vacht', light=(HX - 2, 52, 12, 4.5), shade=(0.6, -0.3))
    C.layer(ellipse(HX, 45, 10, 9.5), 'vacht', light=(HX - 2, 43, 10, 9.5))
    # zilveren borst
    C.layer(ellipse(HX, 46.5, 5.5, 6), 'zilver', light=(HX - 1, 45, 5.5, 6), shade=(0.4, -0.3))
    # voeten met de tenen naar buiten
    C.layer(ellipse(HX - 12, 56.3, 5.0, 2.1), 'vacht', light=(HX - 13, 55.5, 5.0, 2.1))
    C.layer(ellipse(HX + 12, 56.3, 5.0, 2.1), 'vacht', light=(HX + 11, 55.5, 5.0, 2.1))
    # kop
    C.layer(ellipse(HX, HY, 15.5, 12.5), 'vacht', light=(HX - 3, HY - 3, 15.5, 12.5), shade=(0.5, -0.42))
    # armen: schouder -> elleboog langs het lijf -> hand voor de borst
    C.layer(stroke_var([(HX + 8, 38), (HX + 8, 43), (HX + 4, 45)], [2.0, 2.0, 1.7]), 'vacht',
            light=(HX + 6, 40, 4, 6), shade=(0.3, -0.2))
    if frame == 1:
        C.layer(stroke_var([(HX - 8, 38), (HX - 8, 43), (HX - 4, 45)], [2.0, 2.0, 1.7]), 'vacht',
                light=(HX - 9, 40, 4, 6), shade=(0.3, -0.3))
    else:
        # zegenende hand omhoog (links van de kijker, aan de lichtkant)
        C.layer(stroke_var([(HX - 8, 37.5), (HX - 14, 37), (HX - 16, 32)], [2.0, 2.0, 1.8]), 'vacht',
                light=(HX - 15, 34, 5, 5), shade=(0.3, -0.3))
    # snuit
    C.layer(ellipse(HX, HY + 8.6, 4.2, 3.0), 'zilver', light=(HX - 1, HY + 8, 4.2, 3.0), shade=(0.45, -0.35))
    return C


def disk(cx, cy, r):
    return ellipse(cx, cy, r, r)


def eyes(C, frame):
    idx = C.idx
    for ex in (HX - 6, HX + 6):
        cx, cy = ex + 0.0, HY + 1.5
        E = disk(cx, cy, 5.3)
        rim = E & ~disk(cx, cy, 4.3)
        inner = E & ~rim
        if frame == 1:
            # oogleden halfdicht: alleen een gloeiende maansikkel onderin
            lid = inner & disk(cx, cy - 2.0, 4.4)
            moon = inner & ~lid
            idx[lid] = 3
            idx[lid & disk(cx - 1.5, cy - 3.0, 2.4)] = 2
            p = np.pad(moon, 1)
            idx[lid & (p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:])] = 4    # zachte ooglidlijn
            idx[moon] = 11
            idx[moon & ~disk(cx - 0.6, cy - 0.8, 4.1)] = 12
            idx[rim & (YY < cy + 0.5)] = 4      # zacht ooglid: geen zwarte bril
            idx[rim & (YY >= cy + 0.5)] = 15
            continue
        else:
            # wijd open: volle maan met een kleine pupil
            idx[inner] = 12
            idx[inner & disk(cx - 0.4, cy - 0.3, 2.9)] = 11
            idx[inner & ~disk(cx - 0.7, cy - 0.7, 3.8)] = 13
            px, py = int(cx), int(cy)
            idx[py - 1:py + 1, px - 1:px + 1] = 15
            idx[py - 3, px - 3] = 14
            idx[py - 3, px - 2] = 14
        idx[rim] = 15


def forehead(C):
    """Twee symmetrische zilveren sikkels boven de ogen + magenta ruit in het midden."""
    idx = C.idx
    for ex in (HX - 6, HX + 6):
        cx, cy = ex, HY + 1.5
        arc = disk(cx, cy, 8.4) & ~disk(cx, cy + 2.0, 7.6) & (YY < cy - 1.0)
        arc &= (C.z >= 0) & (C.part == 'vacht') & (idx != 15)
        idx[arc] = 5
        idx[arc & (XX > cx + 3.5)] = 6
    C.stamp(HX - 3, HY - 12, ['..00..',
                              '.0890.',
                              '089990',
                              '.0990.',
                              '..00..'], {'8': 8, '9': 9, '0': 10})


HANDS1 = ['....ss....',
          '...s99s...',
          '...s12s...',
          '..s11s2s..',
          '..s1ss2s..',
          '.s11..22s.',
          '.s1s..s2s.',
          '.s11ss23s.',
          '..ssssss..']
HANDS2 = ['....ss....',
          '....s9s...',
          '....s2s...',
          '....s22s..',
          '.....s2s..',
          '.....s2s..',
          '.....s23s.',
          '.....s33s.',
          '......ss..']
RAISED = ['.s..s..s.',
          's9ss9ss9s',
          's1ss1ss1s',
          's1ss1ss2s',
          's1111122s',
          '.s11122s.',
          '..s122s..',
          '...sss...']
KEY = {'s': 15, '9': 9, '8': 8, '1': 1, '2': 2, '3': 3}


def details(C, frame):
    idx = C.idx
    up = 1 if frame == 2 else 0
    # neusje (klein omgekeerd hartje)
    C.stamp(HX - 2, HY + 7, ['.99.', '.00.'], {'9': 9, '0': 10})
    if frame == 2:
        C.stamp(HX - 1, HY + 10, ['00'], {'0': 10})
    # binnenkant oren
    for ex in (HX - 14, HX + 14):
        C.stamp(ex - 2, HY - 9, ['89', '99', '90'], {'8': 8, '9': 9, '0': 10})
    # vingertoppen tegen elkaar voor de borst
    C.stamp(HX - 5, 37, HANDS1 if frame == 1 else HANDS2, KEY)
    if frame == 2:
        C.stamp(HX - 20, 25, RAISED, KEY)
    # gloeiende staartpunt (binnenste stuk van de spiraal)
    tp = tail_pts(up)
    m = stroke(tp[-28:], 1.05) & (idx != 15)
    idx[m] = 9
    idx[m & stroke(tp[-28:-16], 1.05) & (YY < SY - up + 1)] = 8


def build(frame):
    C = body(frame)
    C.render(RAMPS)
    eyes(C, frame)
    forehead(C)
    details(C, frame)
    return C.idx


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    f1, f2 = build(1), build(2)
    save_indexed(os.path.join(out, 'anim_front.png'), [f1, f2], PAL)
    write_pal(os.path.join(out, 'normal.pal'), PAL)
    if '--preview' in sys.argv:
        preview([f1, f2], PAL, 8).save(sys.argv[sys.argv.index('--preview') + 1])
