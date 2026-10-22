"""Nachtaap fase 1, ronde 3: zelfde ontwerp als ronde 2, afwerking naar echte Pokémon-sprites.
python3 build.py <uitmap> [--preview pad.png]

Verschil met ronde 2 (bron in ../ronde2/bron/build.py):
- palet zoals Game Freak het kiest (Espeon-lavendel met violette schaduw, Ralts-wit voor het
  zilver, Whismur-roze voor het accent) in plaats van pastel;
- schaduw als vlakken met een vaste breedte langs de onder-/rechterkant van elke vorm
  (verschuif-methode, zoals bij Abra) plus slagschaduw onder kop en armen, in plaats van
  elliptische verlopen; hooglicht als klein vlekje linksboven;
- omlijning: boven/links de donkerste tint (selout), onder/rechts zwart, binnenlijnen donkerste tint;
- ogen: lege maanschijven zonder pupil (frame 1), pupil + glans (frame 2);
- handen houden een gloeiende maanparel voor de buik (zaadje van de genezer);
- iets kleiner.
"""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../../../../tools/concept/sprites'))
from layerlib import *

PAL = [hexc(h) for h in [
    '#94CD9C',                                   # 0 transparant
    '#E6CDF6', '#B49CDE', '#8373BD', '#4A396A',  # 1-4 vacht licht->donker (2 basis, 4 selout/binnenlijn)
    '#F6F6FF', '#CDCDE6', '#9CA4C5',             # 5-7 zilver (sikkels, snuit)
    '#FFA4D5', '#E65AA4', '#9C2962',             # 8-10 magenta (edelsteen, oren, neus, vingertoppen, staartpunt)
    '#EEFFFF', '#62C5DE', '#293973',             # 11-13 ogen (maansikkel, gloed, nacht)
    '#FFFFFF',                                   # 14 glans
    '#101010']]                                  # 15 omlijning
RAMPS = {'vacht': [1, 2, 3, 4], 'zilver': [5, 6, 7, 7], 'magenta': [8, 9, 10, 10]}
SH = {'vacht': 3, 'zilver': 7, 'magenta': 10}
BASE = {'vacht': 2, 'zilver': 6, 'magenta': 9}
HL = {'vacht': 1, 'zilver': 5, 'magenta': 8}

HX, HY = 29, 27           # middelpunt kop
SX, SY = 50, 34           # middelpunt spiraal


def tail_pts(up):
    return bezier((HX + 7, 53), (SX - 1, 54.5), (SX + 0.3, SY + 9.6 - up)) + \
        spiral(SX, SY - up, 9.6, 1.6, 90, 90 - 560)


def shift(m, dx, dy):
    """m verschoven met (dx, dy); buiten het vak = False."""
    out = np.zeros_like(m)
    H, W = m.shape
    ys = slice(max(0, dy), H + min(0, dy)); yd = slice(max(0, -dy), H + min(0, -dy))
    xs = slice(max(0, dx), W + min(0, dx)); xd = slice(max(0, -dx), W + min(0, -dx))
    out[ys, xs] = m[yd, xd]
    return out


class Part:
    def __init__(self, mask, part, k=(3, 3), hl=None, cast=True):
        self.mask, self.part, self.k, self.hl, self.cast = mask, part, k, hl, cast


def parts(frame):
    up = 1 if frame == 2 else 0
    P = []
    tp = tail_pts(up)
    P.append(Part(stroke(tp, 2.05), 'vacht', k=(1, 1)))
    P[-1].inner = stroke(tp, 1.05)
    for ex in (HX - 14, HX + 14):
        P.append(Part(ellipse(ex, HY - 4, 3.2, 3.4), 'vacht', k=(2, 2)))
    for fx in (HX - 11, HX + 11):
        P.append(Part(ellipse(fx, 56.2, 4.4, 1.9), 'vacht', k=(2, 1)))
    P.append(Part(ellipse(HX, 53.0, 12.5, 4.3), 'vacht', k=(3, 2), hl=ellipse(HX - 9, 51.5, 2.5, 1.2)))
    P.append(Part(ellipse(HX, 46.5, 10.0, 8.5), 'vacht', k=(3, 3), hl=ellipse(HX - 6, 43, 1.5, 2)))
    # armen langs het lijf naar de schoot (frame 2: linkerarm omhoog, zegenend)
    if frame == 1:
        P.append(Part(stroke_var([(HX - 8, 41), (HX - 8.5, 46), (HX - 4, 48)], [1.9, 1.9, 1.7]), 'vacht', k=(1, 2)))
    else:
        P.append(Part(stroke_var([(HX - 8, 40), (HX - 13, 40), (HX - 15, 35)], [1.9, 1.9, 1.7]), 'vacht', k=(2, 2)))
    P.append(Part(stroke_var([(HX + 8, 41), (HX + 8.5, 46), (HX + 4, 48)], [1.9, 1.9, 1.7]), 'vacht', k=(2, 2)))
    # kop
    P.append(Part(ellipse(HX, HY, 14, 11.5), 'vacht', k=(4, 4), hl=ellipse(HX - 7, HY - 7, 3.2, 1.6)))
    # snuit
    P.append(Part(ellipse(HX, HY + 7.3, 3.8, 2.6), 'zilver', k=(1, 1)))
    return P


def render(P):
    zbuf = np.full((64, 64), -1)
    for z, p in enumerate(P):
        zbuf[p.mask] = z
    idx = np.zeros((64, 64), np.uint8)
    front = np.zeros((64, 64), bool)
    fronts = [None] * len(P)
    acc = np.zeros((64, 64), bool)
    for z in range(len(P) - 1, -1, -1):
        fronts[z] = acc.copy(); acc |= P[z].mask
    for z, p in enumerate(P):
        V = zbuf == z
        if not V.any(): continue
        kx, ky = p.k
        sh = V & ~shift(p.mask, -kx, -ky)               # kant weg van het licht
        if p.cast:
            sh |= V & shift(fronts[z], 1, 2) & ~fronts[z]   # slagschaduw onder voorliggende vormen
        idx[V] = BASE[p.part]
        idx[sh] = SH[p.part]
        if p.hl is not None:
            idx[V & p.hl & ~sh] = HL[p.part]
    # lijnen
    pz = np.pad(zbuf, 1, constant_values=-1)
    for y in range(64):
        for x in range(64):
            z = zbuf[y, x]
            if z < 0: continue
            dark = RAMPS[P[z].part][3]
            n = {(dx, dy): pz[1 + y + dy, 1 + x + dx] for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))}
            out = [d for d, v in n.items() if v < 0]
            behind = [d for d, v in n.items() if 0 <= v < z]
            if out:
                ox = sum(d[0] for d in out); oy = sum(d[1] for d in out)
                # selout: bovenkant de schaduwtint, linkerkant de donkerste tint, rest zwart
                if oy < 0:
                    idx[y, x] = SH[P[z].part]
                elif ox < 0 and oy <= 0:
                    idx[y, x] = dark
                else:
                    idx[y, x] = 15
            elif behind:
                bx = sum(d[0] for d in behind); by = sum(d[1] for d in behind)
                # binnenlijn: donkerste tint, aan de schaduwkant (onder/rechts) zwart
                idx[y, x] = 15 if (by > 0 and P[z].part == 'vacht' and x > HX + 2) else dark
    # staart: vulling expliciet (de slagen lopen over zichzelf)
    t = P[0]; V = (zbuf == 0) & ~t.inner
    pf = np.pad(t.inner, 1)
    for y, x in zip(*np.nonzero(V)):
        lit = (pf[y + 2, x + 1] or pf[y + 1, x + 2]) and not (pf[y, x + 1] or pf[y + 1, x])
        idx[y, x] = 4 if lit else 15
    V = (zbuf == 0) & t.inner
    idx[V] = 2
    idx[V & ~shift(t.inner, -1, -1)] = 3
    return idx, zbuf


def disk(cx, cy, r):
    return ellipse(cx, cy, r, r)


EYE1 = [' ddbbd ',
        'dbbdddd',
        'dbddddd',
        'bdddddd',
        'dddddcd',
        'ddddccc',
        ' dcccc ']


def eyes(idx, frame):
    """Frame 1: grote donkere nachtogen zonder zichtbare pupil, met een maansikkel als
    weerspiegeling en een zwakke gloed onderin. Frame 2: de iris licht op, kleine pupil."""
    for ex in (HX - 5.5, HX + 5.5):
        cx, cy = ex, HY + 1.5
        r = 4.8 if frame == 1 else 5.2
        E = disk(cx, cy, r)
        inner = disk(cx, cy, r - 1.0)
        rim = E & ~inner
        if frame == 1:
            # met de hand: maansikkel als glans linksboven, zwakke gloed rechtsonder
            C = Canvas(); C.idx = idx
            C.stamp(int(cx - 3.5), int(cy - 3.5), EYE1, {'b': 11, 'c': 12, 'd': 13})
        else:
            idx[inner] = 12
            idx[inner & disk(cx - 0.6, cy - 0.6, 2.6)] = 11
            idx[inner & ~disk(cx - 1.0, cy - 1.0, 4.4)] = 13
            px, py = int(round(cx - 0.5)), int(round(cy - 0.5))
            idx[py:py + 2, px:px + 2] = 15
            idx[py - 2, px - 2] = 14
        idx[rim] = 15
        top = disk(cx, cy - 0.6, r + 0.8) & ~E & (YY < cy - 2.5)
        idx[top & (idx == 2)] = 3
        idx[top & (idx == 1)] = 2


def forehead(idx):
    for ex, sgn in ((HX - 5.5, -1), (HX + 5.5, 1)):
        cx, cy = ex, HY + 1.5
        arc = disk(cx, cy, 7.6) & ~disk(cx - sgn * 0.6, cy + 1.6, 6.9) & (YY < cy - 2.0)
        arc &= (idx >= 1) & (idx <= 3)
        idx[arc] = 5
        idx[arc & (XX > cx + 2.5)] = 6
    C = Canvas(); C.idx = idx
    C.stamp(HX - 2, HY - 10, ['.44.',
                              '4894',
                              '4990',
                              '.40.'], {'4': 4, '8': 8, '9': 9, '0': 10})


# handen houden een kleine gloeiende maanparel voor de buik (zaadje van de genezer)
ORB = ['...XXXX...',
       '..XebbcX..',
       '.X9bbbbc9X',
       'X19bbbcc9X',
       'X11cbccd3X',
       'X111cdd23X',
       '.X11XX23X.',
       '..XX..XX..']
ORB2 = ['...XXXX...',              # frame 2: één hand houdt de parel
        '..XebbcX..',
        '..XbbbbcX.',
        '..XbbbccX.',
        '..XcbccdX.',
        '..XcddX23X',
        '...XXX223X',
        '......XXX.']
RAISED = ['.s.s.s.',
          's9s9s9s',
          's1s1s2s',
          's11112s',
          '.s1123s',
          '..sss..']
KEY = {'s': 15, 'X': 15, '9': 9, '8': 8, '1': 1, '2': 2, '3': 3, '4': 4, 'b': 11, 'c': 12, 'd': 13, 'e': 14}


def details(idx, frame):
    C = Canvas(); C.idx = idx
    up = 1 if frame == 2 else 0
    C.stamp(HX - 2, HY + 6, ['.99.', '.00.'], {'9': 9, '0': 10})          # neusje
    if frame == 2:
        C.stamp(HX - 1, HY + 9, ['00'], {'0': 10})
    for ex, ox in ((HX - 14, -1), (HX + 14, -1)):                           # binnenkant oren
        C.stamp(ex + ox, HY - 5, ['89', '90'], {'8': 8, '9': 9, '0': 10})
    C.stamp(HX - 5, 43, ORB if frame == 1 else ORB2, KEY)
    if frame == 2:
        C.stamp(HX - 19, 29, RAISED, KEY)
    tp = tail_pts(up)                                                       # gloeiende staartpunt
    m = stroke(tp[-26:], 1.05) & (idx != 15) & (idx != 4)
    idx[m] = 9
    idx[m & stroke(tp[-26:-14], 1.05) & (YY < SY - up + 1)] = 8


def build(frame):
    idx, z = render(parts(frame))
    eyes(idx, frame)
    forehead(idx)
    details(idx, frame)
    return idx


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    f1, f2 = build(1), build(2)
    save_indexed(os.path.join(out, 'anim_front.png'), [f1, f2], PAL)
    write_pal(os.path.join(out, 'normal.pal'), PAL)
    if '--preview' in sys.argv:
        preview([f1, f2], PAL, 8).save(sys.argv[sys.argv.index('--preview') + 1])
