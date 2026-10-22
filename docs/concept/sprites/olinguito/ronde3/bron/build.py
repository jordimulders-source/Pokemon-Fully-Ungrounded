"""Olinguito ronde 3 ("Zakkenroller", gebundelde klauwen, organisch masker, leesbare munt): bouwt anim_front.png + normal.pal.

  python3 build.py <uitmap>

Vormen + automatische schaduw/selout via tools/concept/sprites/shapepaint.py,
daarna gezicht, munt en details met de hand als ASCII-patches.
"""
import sys, os
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import numpy as np
from shapepaint import Canvas, patch, fix_outline, save_indexed, save_pal, hexc, hooks

PAL = [hexc(h) for h in [
    '#7BD5A4',  # 0 transparant
    '#C8805A', '#A65A34', '#7A3E2A', '#4E2621',   # 1-4 vacht: hooglicht, BASIS, schaduw, donkerst (selout, plooien, mond)
    '#5A4A5E', '#2E2436',                         # 5-6 donker: handschoenen, sokken, masker, ringen (BASIS 5? zie notities)
    '#EAD2A4', '#B8946A',                         # 7-8 crème: snuit, buik, binnenoor
    '#FFF2C4', '#F5C842', '#B0802C',              # 9-11 goud: ivoor-hooglicht, GOUD (iris, munt, klauwen), schaduw
    '#4A9E58', '#28683E',                         # 12-13 halsdoek: BASIS, schaduw
    '#FFFFFF',                                    # 14 wit: glans, hoektand
    '#101010',                                    # 15 omlijning
]]

RAMPS = {
    'vacht': [1, 2, 3, 4],
    'donker': [5, 5, 6, 6],
    'creme': [7, 7, 8, 8],
    'klauw': [9, 9, 11, 11],
    'munt': [9, 10, 11, 11],
    'doek': [12, 12, 13, 13],
}
# Alles is ontworpen op een groter raster en wordt met S verkleind rond het steunpunt
# (midden onder): lijf en kop worden kleiner (fase-1-maat), klauwen en ogen blijven
# even groot in pixels (relatief dus langer/groter, zoals bij echte basisvormen).
S, AX, AY = 0.84, 32.0, 59.0


def T(x, y):
    return AX + S * (x - AX), AY + S * (y - AY)


def Ti(x, y):
    a, b = T(x, y)
    return int(round(a)), int(round(b))


class SCanvas(Canvas):
    def _add(self, name, part, mask, **kw):
        if kw.get('hl'):
            hx, hy, hr = kw['hl']
            kw['hl'] = (*T(hx, hy), hr * S)
        return Canvas._add(self, name, part, mask, **kw)

    def ellipse(self, name, part, cx, cy, rx, ry, rot=0.0, **kw):
        cx, cy = T(cx, cy)
        return self._add(name, part, Canvas.ellipse_mask(self, cx, cy, rx * S, ry * S, rot), **kw)

    def ellipse_mask(self, cx, cy, rx, ry, rot=0.0):
        cx, cy = T(cx, cy); rx, ry = rx * S, ry * S
        return Canvas.ellipse_mask(self, cx, cy, rx, ry, rot)

    def poly(self, name, part, pts, **kw):
        return Canvas.poly(self, name, part, [T(x, y) for x, y in pts], **kw)

    def tube(self, name, part, pts, widths, **kw):
        return Canvas.tube(self, name, part, [T(x, y) for x, y in pts], [w * S for w in widths], **kw)


def shift_claws(claws):
    out = []
    for p in claws:
        bx, by = p[0]
        nx, ny = Ti(bx, by)
        out.append([(x - bx + nx, y - by + ny) for x, y in p])
    return out


K = {'h': 1, 'v': 2, 's': 3, 'd': 4, 'm': 5, 'M': 6, 'c': 7, 'C': 8,
     'i': 9, 'g': 10, 'G': 11, 'n': 12, 'N': 13, 'w': 14, 'o': 15}


def ringed_tail(c, pts, widths, rings, tipdark=0.84):
    o = c.tube('staart', 'vacht', pts, widths, shade=2.5)
    t = o.t

    def paint(x, y, cur):
        tv = t[y, x]
        dark = tv >= tipdark or any(a <= tv < b for a, b in rings)
        if dark:
            return 6 if cur in (3, 4) else 5
        return None
    o.paint = paint
    return o


def head(c, dy=0):
    c.ellipse('oor1', 'vacht', 16.5, 14 + dy, 4.3, 4.5, shade=2)
    c.ellipse('oor2', 'vacht', 35, 12.5 + dy, 4.6, 4.8, shade=2)
    c.ellipse('kop', 'vacht', 26, 23 + dy, 11.5, 10.5, shade=2.1, hl=(20, 16 + dy, 3.5))
    c.ellipse('snuit', 'creme', 16.5, 27.5 + dy, 5, 3.6, shade=2)


def _face_rows(eyes):
    """Bandietenmasker als organische vlek: twee afgeronde oogvlekken met een smalle brug,
    een 'traan' onder elk oog en een zachte punt naar achteren (geen rechte band).
    eyes: lijst (x, y, rijen) die eroverheen gaan."""
    rows = {22: [(28, 32)], 23: [(19, 22), (26, 34)], 24: [(17, 23), (25, 35)],
            25: [(16, 36)], 26: [(16, 37)], 27: [(17, 23), (26, 36)],
            28: [(18, 22), (27, 34)], 29: [(19, 21), (30, 32)]}
    g = {}
    for y, spans in rows.items():
        for a, b in spans:
            for x in range(a, b + 1):
                g[(x, y)] = 'm'
    # schaduwrand (index 6) onderaan elke kolom en aan de achterkant
    for (x, y) in list(g):
        if (x, y + 1) not in g or (x + 1, y) not in g and x > 30:
            g[(x, y)] = 'M'
    for ex, ey, er in eyes:
        for dy, row in enumerate(er):
            for dx, ch in enumerate(row):
                if ch != '.':
                    g[(ex + dx, ey + dy)] = ch
    return g


FACE_OPEN = _face_rows([
    (18, 25, ['ooooo', 'owgGo', '.ooo.']),
    (26, 24, ['oooooooo', 'owggoggo', 'oggGoGGo', '.oooooo.']),
])
FACE_CLOSED = _face_rows([
    (18, 25, ['..o..', '.ogo.', 'og.go']),
    (26, 24, ['..oooo..', '.oggggo.', 'ogG..Ggo', 'o......o']),
])


def coin(idx, cx, cy, rx, ry):
    """Munt per pixel: zwarte rand, ring (licht linksboven, donker rechtsonder),
    goud vlak, geslagen teken in het midden. Leesbaar op 1x als munt."""
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
        patch(idx, ix - 1, iy - 2, ['.G.', 'GgG', 'G.G', '.G.'][:0] or ['.G', 'GGG', '.G'], {'G': 11, 'g': 10})
        idx[iy - 2, ix - 2] = 9      # glansje op het vlak
    else:
        idx[iy, ix] = 11; idx[iy - 1, ix] = 11
        idx[iy - 2, ix - 1] = 9


def bundle(bx, by, rel, n=3, step=(3, 0), trim=(1, 0, 2)):
    """n evenwijdige nagels uit één poot: dezelfde kromming, vlak naast elkaar
    (1 px zwart ertussen), zodat ze samen als één klauwhand lezen."""
    out = []
    for k in range(n):
        p = [(bx + k * step[0] + x, by + k * step[1] + y) for x, y in rel]
        t = trim[k] if k < len(trim) else 0
        out.append(p[:len(p) - t] if t else p)
    return out


def face(idx, dy=0, closed=False):
    if os.environ.get('NOPATCH'):
        return
    # binnenoren donker (het masker-donker: hoort bij de 'inbrekerskleuren')
    x, y = Ti(16.5, 14); patch(idx, x - 1, y - 2 + dy, ['.M', 'MM', 'M.'], K)
    x, y = Ti(35, 12.5); patch(idx, x - 1, y - 2 + dy, ['MM', 'MM', '.M'], K)
    for (x, y), ch in (FACE_CLOSED if closed else FACE_OPEN).items():
        idx[y + dy, x] = K[ch]
    # neus
    patch(idx, 13, 30 + dy, ['ooo', 'oo.'], K)
    if not closed:
        # scheve grijns: één mondhoek omhoog, hoektand
        patch(idx, 16, 32 + dy, [
            'o.....o',
            '.ooooo.',
            '....w..',
        ], K)
    else:
        # bek open ("hehe")
        patch(idx, 16, 32 + dy, [
            'o.oooooo',
            '.owdddo.',
            '..oddo..',
            '...oo...',
        ], K)


def common_body(c, dy=0):
    c.ellipse('voet2', 'donker', 39, 56, 4, 2.2, line='black')
    c.ellipse('lijf', 'vacht', 31, 45, 10, 11, shade=2.2, hl=(26, 39, 3))
    b = c.ellipse('buik', 'creme', 27.5, 47.5, 5, 7, shade=2)
    b.mask &= c.ellipse_mask(31, 45, 9.5, 10.5)
    c.poly('doek', 'doek', [(19, 31 + dy), (37, 30 + dy), (37, 34 + dy), (30, 41 + dy), (27, 41 + dy), (21, 35 + dy)], shade=2, line='dark')
    c.poly('doek', 'doek', [(36, 31 + dy), (41, 32 + dy), (42, 36 + dy), (39, 37 + dy), (36, 35 + dy)])


CLAW_STYLES = {
    # A: haken samen omlaag en naar voren gekromd
    'A': (12, 45, [(0, 0), (0, 1), (0, 2), (-1, 3), (-1, 4), (-2, 5), (-3, 6), (-4, 6), (-5, 5)], (3, 0)),
    # B: recht omlaag hangende nagels, alleen de punten gekruld ("Freddy")
    'B': (12, 45, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (-1, 6), (-2, 6)], (3, 0)),
    # C: nagels naar voren, onder elkaar, punten hangen over (gekozen)
    'C': (12, 42, [(0, 0), (-1, 0), (-2, 0), (-3, 1), (-4, 1), (-5, 2), (-6, 3), (-6, 4)], (0, 3)),
}


def frame1(style='C'):
    c = SCanvas(64, 64, RAMPS)
    Canvas.selout_parts = {'vacht', 'creme', 'doek'}
    ringed_tail(c, [(37, 53), (46, 52), (51.5, 46), (53.5, 38), (52, 30), (48, 25), (44, 23.5)],
                [6.5, 7, 7, 6.5, 6, 4.5, 1.5], rings=[(0.22, 0.29), (0.43, 0.5), (0.63, 0.7)])
    common_body(c)
    head(c)
    # verste arm: bovenarm schuin omlaag, elleboog, handschoen, slap afhangende pols (bungelt)
    c.tube('arm1', 'vacht', [(25.5, 37), (21, 39.5)], [5.5, 5], line='dark', shade=2)
    c.tube('hand1', 'donker', [(21.5, 39.5), (16.5, 38.5)], [5, 4.4], line='black', shade=2)
    c.ellipse('hand1', 'donker', 14, 40.5, 4.2, 3.4, rot=-20)
    # dichtste arm naar de munt
    c.tube('arm2', 'vacht', [(37, 39), (38, 44)], [6, 5.5], line='dark', shade=2)
    c.tube('hand2', 'donker', [(38, 44), (37, 47.5), (34.5, 48.5)], [5.5, 5, 4.5], line='black', shade=2)
    c.ellipse('voet1', 'donker', 22, 55.5, 5.5, 2.6, line='black', shade=1.5)
    idx = c.render()
    face(idx)
    # munt groot en vrij op schoot
    coin(idx, 27.5, 48.5, 4.9, 4.9)
    # klauwen: één klauwhand (3 nagels samen), twee nageltoppen om de muntrand, achtervoet
    bx, by, rel, step = CLAW_STYLES[style]
    hand = bundle(bx, by, rel, step=step)
    hooks(idx, hand, keep=(5, 6), wide=2)
    hooks(idx, bundle(32, 45, [(0, 0), (-1, 0), (-2, 0), (-3, 1)], n=2, step=(0, 3), trim=(0, 1)), keep=(5, 6, 10, 9, 11), wide=1)
    hooks(idx, bundle(17, 55, [(0, 0), (-1, 0), (-2, 0), (-3, 1), (-4, 1)], n=2, step=(1, 2), trim=(0, 1)), keep=(5, 6), wide=2)
    return fix_outline(idx, selout=(4, 8, 13))


def frame2():
    c = SCanvas(64, 64, RAMPS)
    Canvas.selout_parts = {'vacht', 'creme', 'doek'}
    ringed_tail(c, [(37, 53), (47, 53), (54, 48), (58, 41), (59, 34), (58, 28.5), (55, 25.5)],
                [6.5, 7, 7, 6.5, 6, 4.5, 1.5], rings=[(0.22, 0.29), (0.43, 0.5), (0.63, 0.7)])
    common_body(c, dy=-1 / S)
    head(c, dy=-1 / S)
    # verste arm naar voren gestoken: klauwhand grijpt ("geef op")
    c.tube('arm1', 'vacht', [(24.5, 38), (19.5, 39.5)], [5.5, 5], line='dark', shade=2)
    c.tube('hand1', 'donker', [(20, 39.5), (12, 40)], [5, 4.5], line='black', shade=2)
    c.ellipse('hand1', 'donker', 10, 40, 3.4, 4, rot=0)
    # dichtste arm omhoog rechts, munt opgegooid
    c.tube('arm2', 'vacht', [(36, 38), (41, 34)], [6, 5.5], line='dark', shade=2)
    c.tube('hand2', 'donker', [(41, 34), (45, 29.5)], [5.5, 4.5], line='black', shade=2)
    c.ellipse('hand2', 'donker', 46, 28, 4, 3.3)
    c.ellipse('voet1', 'donker', 22, 55.5, 5.5, 2.6, line='black', shade=1.5)
    idx = c.render()
    face(idx, dy=-1, closed=True)
    coin(idx, 46.5, 12.5, 3.2, 4.4)
    # beide klauwhanden: nagels samen, omhoog en naar voren gekromd (graaigebaar)
    up = [(0, 0), (0, -1), (0, -2), (-1, -3), (-1, -4), (-2, -5), (-3, -6), (-4, -6), (-5, -5)]
    fwd = [(0, 0), (-1, 0), (-2, 0), (-3, 1), (-4, 1), (-5, 2), (-6, 3), (-6, 4), (-5, 5)]
    hooks(idx, bundle(11, 40, fwd, step=(0, 3), trim=(2, 0, 1)), keep=(5, 6), wide=2)
    hooks(idx, bundle(41, 30, up, step=(3, 0), trim=(1, 0, 2)), keep=(5, 6), wide=2)
    hooks(idx, bundle(17, 55, [(0, 0), (-1, 0), (-2, 0), (-3, 1), (-4, 1)], n=2, step=(1, 2), trim=(0, 1)), keep=(5, 6), wide=2)
    return fix_outline(idx, selout=(4, 8, 13))


NOPATCH = os.environ.get('NOPATCH')

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '.'
    os.makedirs(out, exist_ok=True)
    f1, f2 = frame1(), frame2()
    save_indexed(os.path.join(out, 'anim_front.png'), [f1, f2], PAL)
    save_pal(os.path.join(out, 'normal.pal'), PAL)
    print('ok', out)
