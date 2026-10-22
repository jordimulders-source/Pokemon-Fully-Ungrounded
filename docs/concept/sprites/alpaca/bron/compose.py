"""Alpaca (Fighting-starter fase 1), helemaal opgebouwd uit handgetekende sjablonen.

Volgorde = achter -> voor. Daarna een randpass: rechts/onder aan de buitenrand zwart (#),
linksboven de donkerste tint van het eigen onderdeel (selout). Losse pixels per frame als laatste.
Letters: A-D wol (licht->donker), e/f/g vacht, p/q/r kwastjes, i/j oog, m mond, w wit, # omlijning.
"""
import os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../../tools/concept/sprites'))
import ramp as R

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # docs/concept/sprites/alpaca
G = R.gba
PAL = [G(R.TRANSPARENT),
       G((255, 250, 222)), G((246, 226, 174)), G((206, 176, 126)), G((132, 100, 98)),   # 1-4 wol
       G((250, 196, 136)), G((206, 134, 80)), G((128, 70, 56)),                         # 5-7 vacht
       G((255, 128, 172)), G((230, 40, 112)), G((148, 24, 82)),                         # 8-10 kwastjes
       G((170, 92, 52)), G((84, 40, 30)),                                               # 11-12 oog
       G((214, 90, 110)),                                                               # 13 mond
       (255, 255, 255),                                                                 # 14 wit
       (16, 16, 16)]                                                                    # 15 omlijning
IDX = {'.': 0, 'A': 1, 'B': 2, 'C': 3, 'D': 4, 'e': 5, 'f': 6, 'g': 7, 'p': 8, 'q': 9, 'r': 10,
       'i': 11, 'j': 12, 'm': 13, 'w': 14, '#': 15}
DARK = {'A': 'C', 'B': 'C', 'C': 'C', 'D': 'D'}; DARK.update({c: 'g' for c in 'efg'}); DARK.update({c: 'r' for c in 'pqr'})

T = {}
T['curl'] = [
    "..BBBB..",
    ".BAABBB.",
    "BAABBBBC",
    "BABBBBCD",
    "BBBBBCCD",
    ".CBBCCD.",
    "..DDDD..",
]
T['curls'] = [
    ".BBBB.",
    "BAABBC",
    "BABBCD",
    "CBBCCD",
    ".DDDD.",
]
T['curlL'] = [
    "...BBBB...",
    ".BBAABBBB.",
    "BAAABBBBBC",
    "BAABBBBBCD",
    "BABBBBBBCD",
    "BBBBBBBCCD",
    ".CBBBBCCD.",
    "..DDDDDD..",
]
T['ear_n'] = [".g#.", "ge#.", "gef#", "gef#", "gff#", "gff#", "gff#", "gff#"]
T['ear_f'] = [".g#", "gf#", "gf#", "gg#", "gg#", "gg#"]
# oren plat naar achteren (boze alpaca)
T['ear_n2'] = ["....g#", "...gf#", "..gef#", ".gef#.", "gef#..", "gff#..", "gff#.."]
T['ear_f2'] = ["...g#", "..gg#", ".gg#.", "gg#..", "gg#.."]
T['pom_n'] = [".rrr.", "rppqr", "rpqqr", "rqqqr", ".rqr.", "..r.."]
T['pom_f'] = [".rrr.", "rpqqr", "rqqqr", ".rrr."]
T['face'] = [
    "    gffffffffffffffg    ",
    "   gfffffffffffffffffg  ",
    "  gffffffffffffffffffg  ",
    " gefffffffffffffffffffg ",
    " geffffffffffffffffffgg ",
    "geefffffffffffffffffggg ",
    "geeefffffffffffffffffgg ",
    "geeeefffffffffffffffggg ",
    "geeeefffffffffffffffgg  ",
    "geeeeffffffffffffffggg  ",
    " geeefffffffffffffggg   ",
    "  ggeeffffffffffgggg    ",
    "   gggffffffgggggg      ",
    "     gggggggggggg       ",
]
T['eye_n'] = ["..###", "##wj#", "#wjj#", "#jii#", ".###."]
T['eye_f'] = ["#.", "w#", "j#", "##"]
T['leg_n'] = ["effff", "effff", "efffg", "efffg", "effgg", "fgggg", "ggggg"]
T['leg_f'] = ["fffg", "fffg", "ffgg", "ffgg", "fggg", "gggg"]
# opgetilde voorpoot (frame 2): knie naar voren, hoef onder
T['leg_kick'] = [
    "...effff",
    "..efffff",
    ".efffgg.",
    "efffgg..",
    "effgg...",
    "fgggg...",
    "ggggg...",
]


def shade(tpl, k):
    """Sjabloon k tinten donkerder (wol A->B->C->D, vacht e->f->g)."""
    order = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'D', 'e': 'f', 'f': 'g', 'g': 'g'}
    out = []
    for row in tpl:
        r = row
        for _ in range(k):
            r = ''.join(order.get(ch, ch) for ch in r)
        out.append(r)
    return out


class Grid:
    def __init__(s):
        s.g = [['.'] * 64 for _ in range(64)]

    def put(s, name, x0, y0, dark=0, keep='.'):
        tpl = T[name] if isinstance(name, str) else name
        if dark:
            tpl = shade(tpl, dark)
        for y, row in enumerate(tpl):
            for x, ch in enumerate(row):
                if ch in '. ':
                    continue
                if 0 <= y0 + y < 64 and 0 <= x0 + x < 64:
                    s.g[y0 + y][x0 + x] = ch

    def mass(s, cx, cy, rx, ry, base='B', shadow='C', cut=0.9):
        for y in range(64):
            for x in range(64):
                u = (x + .5 - cx) / rx; v = (y + .5 - cy) / ry
                if u * u + v * v <= 1:
                    s.g[y][x] = shadow if u + v > cut else base

    def px(s, lst):
        for x, y, ch in lst:
            s.g[y][x] = ch

    def edges(s):
        g = s.g
        op = lambda y, x: 0 <= y < 64 and 0 <= x < 64 and g[y][x] != '.'
        out = [r[:] for r in g]
        for y in range(64):
            for x in range(64):
                if not op(y, x):
                    continue
                if not op(y, x + 1) or not op(y + 1, x):
                    out[y][x] = '#'
                elif (not op(y, x - 1) or not op(y - 1, x)) and g[y][x] in DARK:
                    out[y][x] = DARK[g[y][x]]
        s.g = out

    def arr(s):
        return np.array([[IDX[c] for c in r] for r in s.g], np.uint8)


def despeckle(g):
    """Losse pixels in de wol (alle 4 buren anders, 3+ gelijk) -> de meerderheid."""
    src = [r[:] for r in g.g]
    for y in range(1, 63):
        for x in range(1, 63):
            c = src[y][x]
            if c not in 'ABCD':
                continue
            nb = [src[y - 1][x], src[y + 1][x], src[y][x - 1], src[y][x + 1]]
            if c in nb:
                continue
            best = max(set(nb), key=nb.count)
            if nb.count(best) >= 3 and best in 'ABCD':
                g.g[y][x] = best


def head(G_, ox, oy, f2=False):
    P = lambda n, x, y, **k: G_.put(n, ox + x, oy + y, **k)
    if not f2:
        P('ear_n', 7, 0); P('ear_f', 20, 2); P('pom_n', 2, 2); P('pom_f', 22, 3)
    else:
        P('ear_n2', 7, 1); P('ear_f2', 20, 3); P('pom_n', 3, 3); P('pom_f', 23, 4)
    P('face', 0, 12)
    G_.mass(ox + 13.5, oy + 11.5, 10, 6.5)
    P('curl', 5, 4); P('curl', 12, 3); P('curls', 18, 6)
    P('eye_f', 5, 16); P('eye_n', 13, 15)
    P('curls', 19, 10); P('curl', 14, 8); P('curl', 0, 8); P('curls', 8, 12)
    if not f2:
        G_.px([(ox + 1, oy + 19, '#'), (ox + 2, oy + 22, 'g'), (ox + 3, oy + 22, '#'), (ox + 4, oy + 22, '#'), (ox + 5, oy + 21, 'g')])
    else:   # bek open: kreet
        rows = {19: "e#ee", 20: "g####g", 21: "#mmmm#", 22: ".wmm#", 23: "..##"}
        for yy, r in rows.items():
            for xx, ch in enumerate(r):
                G_.g[oy + yy][ox + xx] = ch


def body(G_, f2=False):
    dy = 0 if not f2 else -1
    # verre poten
    G_.put('leg_f', 44, 46, dark=1)
    G_.put('leg_f', 30, 46, dark=1)
    # nabije poten
    G_.put('leg_n', 39, 47)
    if not f2:
        G_.put('leg_n', 24, 47)
    else:
        G_.put('leg_kick', 18, 44)
    # staart
    ty = 33 if not f2 else 30
    G_.put('curls', 48, ty, dark=0)
    # lijf: massa + krullen, onderste rij eerst (bovenste krullen hangen over de onderste)
    G_.mass(37, 41 + dy, 12, 8, base='C', shadow='D', cut=0.7)
    for x, y, n, d in [(45, 43, 'curl', 1), (39, 44, 'curl', 1), (33, 44, 'curl', 1), (27, 43, 'curl', 1),
                       (46, 37, 'curl', 1), (40, 38, 'curlL', 0), (33, 38, 'curlL', 0), (26, 38, 'curl', 0),
                       (43, 32, 'curl', 0), (36, 31, 'curlL', 0), (29, 32, 'curl', 0)]:
        G_.put(n, x, y + dy, dark=d)
    # borst/nek onder de kop
    for x, y, n, d in [(22, 36, 'curl', 0), (21, 31, 'curls', 0), (26, 29, 'curl', 0)]:
        G_.put(n, x, y + (0 if not f2 else -2), dark=d)


def frame(f2=False):
    g = Grid()
    import gen
    inv = {v: k for k, v in IDX.items()}
    base = gen.build(f2)[2]
    g.g = [[inv[int(v)] for v in row] for row in base]
    despeckle(g)
    # zuinige dithering: 1 rij schaakbord-overgang B->C op het lijf (wol mag textuur hebben)
    src = [r[:] for r in g.g]
    for y in range(31, 52):
        for x in range(20, 56):
            if src[y][x] == 'C' and src[y - 1][x] == 'B' and src[y + 1][x] == 'C' and (x + y) % 2 == 0:
                g.g[y][x] = 'B'
    # wolkrullen in het lijf (zelfde taal als de kuif): boogjes in de schaduwtint
    dy = 0 if not f2 else -1
    for x, y in ([(31, 36), (38, 35), (44, 39), (35, 42), (28, 41)]):
        for ddx, ddy in ((2, 0), (2, 1), (1, 2), (0, 2)):
            xx, yy = x + ddx, y + ddy + dy
            if g.g[yy][xx] in 'AB':
                g.g[yy][xx] = 'C'
    if not f2:
        head(g, 8, 8)
    else:
        head(g, 7, 5, f2=True)
    g.edges()
    return g


def save(frames, path):
    a = np.vstack([f.arr() for f in frames])
    im = Image.fromarray(a, 'P')
    im.putpalette([v for c in PAL for v in c])
    im.save(path, transparency=0)


if __name__ == '__main__':
    f1, f2 = frame(False), frame(True)
    save([f1, f2], os.path.join(OUT, 'anim_front.png'))
    R.write_pal(os.path.join(OUT, 'normal.pal'), PAL)
    for k, f in enumerate((f1, f2)):
        with open(os.path.join(OUT, 'frame%d.txt' % (k + 1)), 'w') as fh:
            for r in f.g:
                fh.write(''.join(r) + '\n')
