"""Olinguito ronde 4: dezelfde zakkenroller als ronde 3, opnieuw getekend als Gen 3-sprite.

  python3 build.py <uitmap>

Wat er anders is dan ronde 3 (zie NOTITIES.md):
- driekwart en dynamisch: sluipt op de tenen, lijf schuin naar voren, kop vooruit,
  verre ledematen kleiner en een tint donkerder, staart als S erachter;
- fase-1-verhoudingen: grote kop (±50% van de hoogte), klein lijf, stompe pootjes;
- Gen 3-schaduw (shapepaint.Canvas.render3): vaste schaduwvlakken onder/rechts,
  donkere binnenrand onderaan, slagschaduw onder kop/arm, strak hooglicht linksboven;
- Gen 3-ogen naar Poochyena (donker gezicht, sluw): oog van 6x2 zonder rand eromheen,
  zwart ooglid met 1 witte glans boven de pupil, iris met verloop.
"""
import sys, os
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from shapepaint import Canvas, patch, fix_outline, save_indexed, save_pal, hexc, hooks

PAL = [hexc(h) for h in [
    '#7BD5A4',                                    # 0 transparant
    '#C8805A', '#A65A34', '#7A3E2A', '#4E2621',   # 1-4 vacht: hooglicht, BASIS, schaduw, donkerst
    '#5A4A5E', '#2E2436',                         # 5-6 donker: handschoenen, sokken, masker, ringen
    '#EAD2A4', '#B8946A',                         # 7-8 crème: snuit, buik
    '#FFF2C4', '#F5C842', '#B0802C',              # 9-11 goud: ivoor, GOUD, schaduw
    '#4A9E58', '#28683E',                         # 12-13 halsdoek
    '#FFFFFF',                                    # 14 wit
    '#101010',                                    # 15 omlijning
]]
RAMPS = {
    'vacht': [1, 2, 3, 4],
    'donker': [5, 5, 6, 6],
    'creme': [7, 7, 8, 8],
    'doek': [12, 12, 13, 13],
}
K = {'h': 1, 'v': 2, 's': 3, 'd': 4, 'm': 5, 'M': 6, 'c': 7, 'C': 8,
     'i': 9, 'g': 10, 'G': 11, 'n': 12, 'N': 13, 'w': 14, 'o': 15}
SELOUT = (4, 8, 13)


def ringed_tail(c, pts, widths, rings, tipdark=0.86):
    o = c.tube('staart', 'vacht', pts, widths, shade=2)
    t = o.t

    def paint(x, y, cur):
        tv = t[y, x]
        if tv >= tipdark or any(a <= tv < b for a, b in rings):
            return 6 if cur in (3, 4) else 5
        return None
    o.paint = paint
    return o


def coin(idx, cx, cy, rx, ry):
    """Munt per pixel: zwarte rand, ring (licht linksboven, donker rechtsonder), goud vlak, teken."""
    for y in range(int(cy - ry - 2), int(cy + ry + 3)):
        for x in range(int(cx - rx - 2), int(cx + rx + 3)):
            d = ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2
            if d > (1 + 1.2 / min(rx, ry)) ** 2:
                continue
            if d > 1:
                v = 15
            elif d > (1 - 1.1 / min(rx, ry)) ** 2:
                v = 9 if (x + .5 - cx) + (y + .5 - cy) < -1 else 11
            else:
                v = 10
            idx[y, x] = v
    ix, iy = int(cx), int(cy)
    if rx >= 3.5:
        patch(idx, ix - 1, iy - 1, ['.G', 'GGG', '.G'], K)
        idx[iy - 2, ix - 2] = 9
    else:
        idx[iy, ix] = 11; idx[iy - 1, ix] = 11
        idx[iy - 2, ix - 1] = 9


def bundle(bx, by, rel, n=3, step=(3, 0), trim=(1, 0, 2)):
    """n evenwijdige nagels uit één poot (1 px zwart ertussen): één klauwhand."""
    out = []
    for k in range(n):
        p = [(bx + k * step[0] + x, by + k * step[1] + y) for x, y in rel]
        t = trim[k] if k < len(trim) else 0
        out.append(p[:len(p) - t] if t else p)
    return out


# ---- gezicht ---------------------------------------------------------------
def mask_map(spans):
    g = {}
    for y, ss in spans.items():
        for a, b in ss:
            for x in range(a, b + 1):
                g[(x, y)] = 'm'
    for (x, y) in list(g):
        if (x, y + 1) not in g or ((x + 1, y) not in g and (x - 1, y) in g and x > 28):
            g[(x, y)] = 'M'
    return g


# masker: twee afgeronde oogvlekken met een smalle brug, traan onder het dichtste oog,
# zachte punt naar achteren richting oor
MASK = {20: [(23, 28)], 21: [(15, 18), (22, 30)], 22: [(14, 31)], 23: [(14, 32)],
        24: [(14, 32)], 25: [(15, 19), (22, 31)], 26: [(16, 18), (23, 29)], 27: [(25, 28)]}
# Gen 3-ogen (Poochyena): zwart lid + glans boven de pupil, iris van licht naar donker
EYE_NEAR = ['owoGGG', 'Goiggs']        # 6x2, pupil voorin (naar de snuit)
EYE_FAR = ['wo', 'oG']                 # 2x2, verste oog (driekwart: smaller)
EYE_NEAR_SHUT = ['.oooo.', 'o....o']   # ^-oog voor "hehe"
EYE_FAR_SHUT = ['oo', '.o']


def face(idx, ox=0, oy=0, closed=False):
    for (x, y), ch in mask_map(MASK).items():
        if idx[y + oy, x + ox] not in (0, 15):
            idx[y + oy, x + ox] = K[ch]
    K2 = dict(K); K2['s'] = 6    # binnen het masker is de 'schaduw' van de iris het masker-donker
    if not closed:
        patch(idx, 24 + ox, 23 + oy, EYE_NEAR, K)
        patch(idx, 17 + ox, 23 + oy, EYE_FAR, K)
        # zwaar ooglid: één donkere pixel die het lid naar achteren verlengt (sluw)
        idx[22 + oy, 29 + ox] = 15
    else:
        patch(idx, 24 + ox, 23 + oy, EYE_NEAR_SHUT, K)
        patch(idx, 17 + ox, 23 + oy, EYE_FAR_SHUT, K)
    # binnenoren
    patch(idx, 16 + ox, 14 + oy, ['M', 'MM'], K)
    patch(idx, 30 + ox, 13 + oy, ['MM', 'MM'], K)
    # neus (2x2) en mond
    patch(idx, 9 + ox, 26 + oy, ['oo', 'oo'], K)
    if not closed:
        patch(idx, 11 + ox, 28 + oy, ['o....o', '.oooo.', '...w..'], K)
    else:
        patch(idx, 11 + ox, 28 + oy, ['oooooo', '.owddo', '..odo.', '...o..'], K)


# ---- lichaam ---------------------------------------------------------------
def body(c, oy=0, tail=None):
    ringed_tail(c, tail or [(38, 51), (47, 51), (53, 46), (55, 38), (53, 31), (49, 28), (46, 28.5)],
                [6, 6.5, 6.5, 6, 5, 3.5, 1.2], rings=[(0.24, 0.31), (0.46, 0.53), (0.66, 0.73)])
    # verre achterpoot (naar achteren gestrekt, donkerder)
    c.tube('poot2', 'vacht', [(39, 50), (43, 55)], [5, 4], tone=2, shade=1.5, line='dark')
    c.ellipse('voet2', 'donker', 45, 56.5, 3, 1.8, tone=2, line='black')
    # lijf: schuin naar voren (sluiphouding)
    c.ellipse('lijf', 'vacht', 32, 44 + oy, 8, 9.5, rot=-28, shade=2.5, hl=(28, 38 + oy, 2.5))
    b = c.ellipse('buik', 'creme', 28.5, 45 + oy, 4, 6.5, rot=-28, shade=2)
    b.mask &= c.ellipse_mask(32, 44 + oy, 7.4, 8.9, rot=-28)
    # dichtste achterpoot: dij + sok op de tenen
    c.ellipse('dij', 'vacht', 34, 51.5, 5, 4.5, rot=-20, shade=2, line='dark', hl=(32, 49, 2))
    c.tube('voet1', 'donker', [(31, 55.5), (27.5, 57)], [3.6, 3], line='black', shade=1.2)


def doek(c, oy=0, knot=((36, 30), (43, 27.5), (41.5, 31), (44, 34), (36, 33.5))):
    d = c.poly('doek', 'doek', [(18, 31 + oy), (35, 29.5 + oy), (36, 33 + oy), (27, 39 + oy), (24, 38.5 + oy), (20, 35 + oy)], shade=2, line='dark')
    c.poly('doek', 'doek', [(x, y + oy) for x, y in knot])
    return d


def head(c, ox=0, oy=0):
    c.ellipse('oor1', 'vacht', 16.5 + ox, 15.5 + oy, 3.2, 3.4, tone=2, shade=1.5)
    c.ellipse('oor2', 'vacht', 31 + ox, 14 + oy, 3.9, 4.1, shade=2, hl=(30 + ox, 12 + oy, 1.5))
    k = c.ellipse('kop', 'vacht', 23.5 + ox, 23.5 + oy, 10.5, 9.3, shade=2.2, hl=(19 + ox, 18 + oy, 3.2))
    c.ellipse('snuit', 'creme', 14 + ox, 27.5 + oy, 4.6, 3.2, shade=1.6)
    return k


def frame1():
    c = Canvas(64, 64, RAMPS)
    Canvas.selout_parts = {'vacht', 'creme', 'doek'}
    body(c)
    # verre arm: achter de kop vandaan, klauwhand hangt voor de borst (tenenloop-inbreker)
    c.tube('arm1', 'vacht', [(23, 35), (18, 38)], [4.5, 4], tone=2, shade=1.5, line='dark')
    c.tube('hand1', 'donker', [(18.5, 38), (15, 39)], [4, 3.6], tone=2, line='black', shade=1)
    c.ellipse('hand1', 'donker', 13.5, 39.5, 3.2, 2.8, tone=2)
    doek(c)
    head(c)
    # dichtste arm: houdt de munt tegen de borst
    c.tube('arm2', 'vacht', [(34, 37), (33, 42)], [5, 4.5], shade=2, line='dark')
    c.tube('hand2', 'donker', [(33, 42), (30.5, 44)], [4.6, 4.2], shade=1.5, line='black')
    idx = c.render3()
    face(idx)
    coin(idx, 25.5, 44, 4.4, 4.4)
    # klauwen: verre hand (gebundeld, hangt over), om de munt, achtervoet
    hooks(idx, bundle(11, 41, [(0, 0), (-1, 0), (-2, 1), (-3, 2), (-3, 3), (-3, 4), (-2, 5)], step=(2, 1), trim=(1, 0, 2)), keep=(5, 6), wide=1)
    hooks(idx, bundle(29, 42, [(0, 0), (-1, -1), (-2, -1), (-3, -1)], n=2, step=(0, 3), trim=(0, 1)), keep=(5, 6, 9, 10, 11), wide=1)
    hooks(idx, bundle(25, 56, [(0, 0), (-1, 0), (-2, 0), (-3, 1)], n=2, step=(1, 2), trim=(0, 1)), keep=(5, 6), wide=1)
    return fix_outline(idx, selout=SELOUT)


def frame2():
    c = Canvas(64, 64, RAMPS)
    Canvas.selout_parts = {'vacht', 'creme', 'doek'}
    body(c, tail=[(38, 51), (48, 52), (55, 47), (58, 39), (57, 32), (54, 28.5), (51, 28.5)])
    # verre arm: naar voren, klauwhand open ("geef op")
    c.tube('arm1', 'vacht', [(23, 35), (17, 36)], [4.5, 4], tone=2, shade=1.5, line='dark')
    c.tube('hand1', 'donker', [(17.5, 36), (12.5, 35.5)], [4, 3.6], tone=2, line='black', shade=1)
    c.ellipse('hand1', 'donker', 11, 35.5, 3.2, 3, tone=2)
    doek(c, oy=-1, knot=((36, 29), (44, 25), (42, 29.5), (45.5, 31.5), (36, 32.5)))
    head(c, oy=-1)
    # dichtste arm omhoog: heeft de munt opgegooid
    c.tube('arm2', 'vacht', [(34, 37), (38, 32)], [5, 4.5], shade=2, line='dark')
    c.tube('hand2', 'donker', [(38, 32), (40, 28)], [4.6, 4], shade=1.5, line='black')
    c.ellipse('hand2', 'donker', 40.5, 27, 3.2, 2.8)
    idx = c.render3()
    face(idx, oy=-1, closed=True)
    coin(idx, 44.5, 13.5, 2.8, 4.2)
    hooks(idx, bundle(8, 34, [(0, 0), (-1, 0), (-2, 0), (-3, 1), (-4, 2), (-4, 3)], step=(0, 2), trim=(1, 0, 2)), keep=(5, 6), wide=1)
    hooks(idx, bundle(38, 24, [(0, 0), (0, -1), (-1, -2), (-1, -3), (-2, -4), (-3, -4)], step=(2, 0), trim=(1, 0, 2)), keep=(5, 6), wide=1)
    hooks(idx, bundle(25, 56, [(0, 0), (-1, 0), (-2, 0), (-3, 1)], n=2, step=(1, 2), trim=(0, 1)), keep=(5, 6), wide=1)
    return fix_outline(idx, selout=SELOUT)


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    save_indexed(os.path.join(out, 'anim_front.png'), [frame1(), frame2()], PAL)
    save_pal(os.path.join(out, 'normal.pal'), PAL)
    print('ok', out)
