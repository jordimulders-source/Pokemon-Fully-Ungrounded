"""Nachtaap fase 1, ronde 4: 3/4-aanzicht naar links, zittend peerlijf met dijen en losse armen,
nachtaapmasker, halve oogleden, taps toelopende S-staart met Nazca-spiraal.
python3 build.py <uitmap> [--preview pad.png]

Opbouw: vormen (lagen, achter naar voor) met een halvemaanschaduw rechtsonder en omlijning
(boven/links de donkerste tint, onder/rechts zwart); daarna het gezicht, de handen met de
maanparel, de tenen en de staartpunt als handgetekende pixelrijen (stempels).
"""
import sys, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../../../../tools/concept/sprites'))
from layerlib import ellipse, stroke_var, bezier, spiral, XX, YY, save_indexed, write_pal, preview, hexc

PAL = [hexc(h) for h in [
    '#94CD9C',                                   # 0 transparant
    '#E6D5FF', '#AC94DE', '#7362B4', '#3E2E66',  # 1-4 vacht (2 basis, 3 schaduw, 4 donker: lijn + masker)
    '#F6F6FF', '#C5C5E6', '#8B94BD',             # 5-7 zilver: wenkbrauwvlekken, snuit, buik
    '#FFA4D5', '#E65AA4', '#9C2962',             # 8-10 roze: neus, staartpunt, binnenkant oren
    '#DEFFFF', '#5ABDDE', '#202C5E',             # 11-13 maan: parel + ogen (13 iris)
    '#FFFFFF',                                   # 14 glans
    '#101010']]                                  # 15 omlijning
RAMP = {'v': (1, 2, 3, 4), 'z': (5, 6, 7, 7)}


def shift(m, dx, dy):
    out = np.zeros_like(m); H, W = m.shape
    ys = slice(max(0, dy), H + min(0, dy)); yd = slice(max(0, -dy), H + min(0, -dy))
    xs = slice(max(0, dx), W + min(0, dx)); xd = slice(max(0, -dx), W + min(0, -dx))
    out[ys, xs] = m[yd, xd]; return out


def tail_shape(up=0):
    pts = bezier((38, 50), (46, 57), (50.5, 48.5)) + bezier((50.5, 48.5), (53.5, 42), (53, 37.5 - up))[1:] + \
        spiral(48.8, 32.5 - up, 6.3, 1.3, 50, 50 - 450, 120)[1:]
    r = np.linspace(2.0, 1.25, len(pts))
    return pts, stroke_var(pts, list(r)), stroke_var(pts, list(r - 1.0))


class S:
    def __init__(self, m, part='v', k=(3, 3), hl=None, inner=None):
        self.m, self.part, self.k, self.hl, self.inner = m, part, k, hl, inner


def shapes(frame):
    up = 1 if frame == 2 else 0
    pts, tm, ti = tail_shape(up)
    L = [S(tm, k=(1, 1), inner=ti),
         S(ellipse(40, 18.5 - up, 2.5, 2.7), k=(1, 1)),                          # verre oor
         S(ellipse(36.5, 51, 5.5, 4.6), k=(4, 3)),                               # verre dij
         S(ellipse(40.5, 56, 4.0, 1.8), k=(2, 1)),                               # verre voet
         S(ellipse(28, 47.5, 9.0, 8.0) | ellipse(27.5, 41, 6.5, 5), k=(4, 3),    # peerlijf
           hl=ellipse(23, 41, 1.6, 1.4)),
         S(ellipse(29, 48.5, 4.5, 4.5), 'z', k=(2, 2)),                          # lichte buik
         S(ellipse(21, 51.5, 6.5, 4.8), k=(4, 3), hl=ellipse(18, 49, 2.0, 1.2)),  # nabije dij
         S(ellipse(15.5, 56, 5.0, 2.0), k=(2, 1)),                               # nabije voet
         S(stroke_var([(34, 40), (35.5, 44.5), (31.5, 47)], [1.8, 1.8, 1.6]), k=(2, 2))]   # verre arm
    L.append(S(ellipse(27, 26.5 - up, 13.5, 11), k=(5, 4), hl=ellipse(20, 18.6 - up, 3.0, 1.2)))  # kop
    L.append(S(ellipse(13.8, 21 - up, 2.8, 3.0), k=(1, 1)))                     # nabije oor
    if frame == 1:
        L.append(S(stroke_var([(20.5, 40), (18.5, 44.5), (22.5, 47)], [1.9, 1.9, 1.7]), k=(1, 1)))
    else:                                                                        # zwaaiende arm
        L.append(S(stroke_var([(20.5, 40), (15, 41), (12.5, 36)], [1.9, 1.9, 1.7]), k=(1, 1)))
    L.append(S(ellipse(24, 33.0 - up, 4.3, 2.6), 'z', k=(1, 1)))              # snuit
    return L


def render(L):
    zb = np.full((64, 64), -1)
    for z, s in enumerate(L):
        zb[s.m] = z
    idx = np.zeros((64, 64), np.uint8)
    for z, s in enumerate(L):
        V = zb == z
        hl, b, sh, dk = RAMP[s.part]
        m = s.inner if s.inner is not None else s.m
        idx[V] = b
        idx[V & ~shift(m, -s.k[0], -s.k[1])] = sh
        if s.hl is not None:
            idx[V & s.hl] = hl
    pz = np.pad(zb, 1, constant_values=-1)
    for y in range(64):
        for x in range(64):
            z = zb[y, x]
            if z < 0: continue
            s = L[z]; dk = RAMP[s.part][3]
            if s.inner is not None:
                continue
            n = {(dx, dy): pz[1 + y + dy, 1 + x + dx] for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))}
            out = [d for d, v in n.items() if v < 0]
            beh = [d for d, v in n.items() if 0 <= v < z]
            if out:
                ox = sum(d[0] for d in out); oy = sum(d[1] for d in out)
                idx[y, x] = dk if (oy < 0 or (ox < 0 and oy <= 0)) else 15
            elif beh:
                idx[y, x] = dk
    # staart: lijn = alles buiten de vulling
    for z, s in enumerate(L):
        if s.inner is None: continue
        V = (zb == z) & ~s.inner
        pf = np.pad(s.inner, 1)
        for y, x in zip(*np.nonzero(V)):
            lit = (pf[y + 2, x + 1] or pf[y + 1, x + 2]) and not (pf[y, x + 1] or pf[y + 1, x])
            idx[y, x] = 4 if lit else 15
    return idx


KEY = {'.': None, ' ': None, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
       'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'X': 15, 'o': 0}


def stamp(idx, x0, y0, rows):
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            v = KEY[ch]
            if v is not None:
                idx[y0 + dy, x0 + dx] = v


# ---- handgetekende delen (x0, y0 = linksboven) ----
# gezicht: nachtaapmasker (donkere middenstreep, zijstrepen), witte vlekken boven de ogen,
# halve oogleden (Espurr/Natu), donkere iris met 1 glanspixel en 2 px maangloed onderin.
FACE = [  # x 15..34, y 18..30 (c0 = x15); nabij oog x17..23, verre oog x27..32, middenstreep x25
    '          4         ',
    '          4         ',
    '   55555  4  5555   ',
    '  5666665 4 566665  ',
    ' 4 66666  4  6666  4',
    ' 4333333324233333324',
    ' 4333333324233333324',
    ' 4XXXXXXX242XXXXXX24',
    ' 4deddddd222dedddd24',
    ' 4ddddddd222dddddd24',
    ' 4dddddcd222ddddcd24',
    ' 43dddcc32223dddc324',
    '  344444322234444 4 ',
]
MUZZLE = [  # x 20..27, y 31..34
    ' 566667 ',
    '56699667',
    '56677667',
    ' 677777 ',
]
EARS = {1: [(12, 20, ['44', '43']), (40, 18, ['4'])], 2: [(12, 19, ['44', '43']), (40, 17, ['4'])]}
PEARL = [  # x 22..31, y 42..48: parel in beide handen, vingers om de parel
    '   XXXX  ',
    '  Xbebb4 ',
    ' 1XbbbbcX',
    '12bbbbccX',
    '12Xbbcc32',
    ' 12XccX3X',
    '  XXXXX  ',
]
PEARL2 = [  # frame 2: alleen de verre hand houdt de parel
    '   XXXX  ',
    '  Xbebb4 ',
    '  XbbbbcX',
    '  XbbbccX',
    '  Xbbcc32',
    '   XccX3X',
    '    XXX  ',
]
HAND_UP = [  # zwaaiende handpalm met 3 vingers, in lijfkleur
    ' 4 4 4 ',
    '4242424',
    '4222224',
    '4122223',
    ' 41223X',
    '  4XX  ',
]
TOES = [  # nabije voet: 3 teentjes
    'X.X.X',
]


def build(frame):
    up = 1 if frame == 2 else 0
    L = shapes(frame)
    idx = render(L)
    stamp(idx, 15, 18 - up, FACE)
    stamp(idx, 20, 31 - up, MUZZLE)
    for x0, y0, rows in EARS[frame]:
        stamp(idx, x0, y0, rows)
    stamp(idx, 22, 42, PEARL if frame == 1 else PEARL2)
    if frame == 2:
        stamp(idx, 9, 31, HAND_UP)
    # staartpunt licht roze op
    pts, tm, ti = tail_shape(up)
    tip = stroke_var(pts[-20:], [0.9] * 20) & ti
    idx[tip] = 9
    idx[tip & stroke_var(pts[-20:-12], [0.9] * 8)] = 8
    return idx


if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    f1, f2 = build(1), build(2)
    save_indexed(os.path.join(out, 'anim_front.png'), [f1, f2], PAL)
    write_pal(os.path.join(out, 'normal.pal'), PAL)
    if '--preview' in sys.argv:
        preview([f1, f2], PAL, 8).save(sys.argv[sys.argv.index('--preview') + 1])
