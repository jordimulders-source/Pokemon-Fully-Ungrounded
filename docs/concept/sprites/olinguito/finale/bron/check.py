#!/usr/bin/env python3
"""Controles: formaat, box, soliditeit, symmetrie, donker-aandeel, open randen, rechte omtrekstukken,
zwevende delen (losse componenten), bevroren gezicht (pixeldiff met ronde 23), transparency."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tools as T
from PIL import Image
OUTLINE = {1, 2, 9}
sys.path.insert(0, '/home/user/projectgrounded/docs/lessen/vormstudie/tools')
def shape_metrics(g):
    S = {(x, y) for y in range(64) for x in range(64) if g[y][x]}
    xs = [p[0] for p in S]; ys = [p[1] for p in S]
    x0, x1 = min(xs), max(xs)
    M = {(x0 + x1 - x, y) for x, y in S}
    sym = max(len(S & {(x + d, y) for x, y in M}) / len(S | {(x + d, y) for x, y in M}) for d in range(-4, 5))
    import shape as SH
    hp = []
    for x, y in S: hp += [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
    sol = len(S) / SH.hull_area(hp)
    dark = sum(1 for (x, y) in S if (lambda c: 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2])(T.PAL[g[y][x]]) < 55) / len(S)
    return len(S), (x0, min(ys), x1, max(ys)), x1 - x0 + 1, max(ys) - min(ys) + 1, sol, sym, dark
def open_edges(g):
    ob = []
    for y in range(64):
        for x in range(64):
            v = g[y][x]
            if v and v not in OUTLINE:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    X, Y = x + dx, y + dy
                    if not (0 <= X < 64 and 0 <= Y < 64) or g[Y][X] == 0: ob.append((x, y)); break
    return ob
def straight(g, minlen=5):
    """Rechte stukken in de buitenomtrek: horizontale runs van randpixels (boven/onder) en verticale (links/rechts)."""
    res = []
    for name, dx, dy in (('boven', 0, -1), ('onder', 0, 1), ('links', -1, 0), ('rechts', 1, 0)):
        edge = {(x, y) for y in range(64) for x in range(64) if g[y][x] and (not (0 <= x + dx < 64 and 0 <= y + dy < 64) or g[y + dy][x + dx] == 0)}
        if dy:
            for y in range(64):
                run = []
                for x in range(65):
                    if (x, y) in edge: run.append(x)
                    else:
                        if len(run) >= minlen: res.append((name, 'y%d x%d-%d (%d)' % (y, run[0], run[-1], len(run))))
                        run = []
        else:
            for x in range(64):
                run = []
                for y in range(65):
                    if (x, y) in edge: run.append(y)
                    else:
                        if len(run) >= minlen: res.append((name, 'x%d y%d-%d (%d)' % (x, run[0], run[-1], len(run))))
                        run = []
    return res
def components(g):
    S = {(x, y) for y in range(64) for x in range(64) if g[y][x]}
    comps = []
    while S:
        st = [S.pop()]; c = set(st)
        while st:
            x, y = st.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    p = (x + dx, y + dy)
                    if p in S: S.remove(p); c.add(p); st.append(p)
        comps.append(c)
    return comps
FACE = None
KOPDY = 1
def face_zone(x, y):
    # bevroren gezicht van ronde 23: neus/snuit/masker/oog/grijns/beide oren (x8-35, y18-38 in frame 1),
    # behalve de achterhoofdcontour x>=34 op y25-33 (die mag naar binnen)
    # gezicht: neus, snuit, masker, oog, grijns, verre oor (x8-28, y18-38); het nabije oor wordt apart vergeleken (2 px verschoven)
    return 8 <= x <= 28 and 18 <= y <= 38 and not (x >= 27 and y <= 24)
def run(p):
    im = Image.open(p)
    print('mode', im.mode, im.size, 'transparency', im.info.get('transparency'))
    r23 = [T.read_png(os.path.join(T.OL, 'ronde23', 'anim_front.png'), f) for f in (0, 1)]
    for f in (0, 1):
        g = T.read_png(p, f)
        A, box, w, h, sol, sym, dark = shape_metrics(g)
        print('frame %d: %d px, box %dx%d %s, soliditeit %.3f, symmetrie %.3f, donker %.3f' % (f + 1, A, w, h, box, sol, sym, dark))
        ob = open_edges(g); print('  open randen:', len(ob), ob[:20])
        comps = components(g); print('  delen (8-verbonden):', len(comps), [len(c) for c in comps])
        # ronde-23-rij -> eindrij: rijen <=24 +3, rij 25 weggeknipt (schedelrij zonder kenmerken), rijen 26-38 +2; frame 2: 1 omhoog
        def ny(y): return y + 3 - f if y <= 24 else (None if y == 25 else y + 2 - f)
        fd = [(x, y) for y in range(64) for x in range(64) if face_zone(x, y) and ny(y) is not None and r23[0][y][x] != g[ny(y)][x]]
        print('  gezicht (bevroren zone) diff met ronde 23:', len(fd), fd[:12])
        st = straight(g); print('  rechte omtrekstukken >=5:', st)
        if f == 0:
            r = r23[0]; oor = [(x, y) for y in range(19, 24) for x in range(29, 36) if r[y][x] and (y >= 23 and x < 30) is False]
            od = [(x, y) for (x, y) in oor if g[y + 3][x - 2] != r[y][x]]
            print('  nabije oor (ronde 23, 2 px naar links) diff:', len(od), od[:8])
if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(T.H, '..', 'anim_front.png'))

def profiles(g, minrun=5):
    """Regelmatige trappen in de omtrek (leest als rechte schuine lijn): per rij de linker-/rechterrand en per kolom
    de boven-/onderrand; meldt reeksen van >= minrun gelijke stappen (niet 0)."""
    out = []
    rows = [y for y in range(64) if any(g[y])]
    cols = [x for x in range(64) if any(g[y][x] for y in range(64))]
    L = {y: min(x for x in range(64) if g[y][x]) for y in rows}
    R = {y: max(x for x in range(64) if g[y][x]) for y in rows}
    T_ = {x: min(y for y in range(64) if g[y][x]) for x in cols}
    B = {x: max(y for y in range(64) if g[y][x]) for x in cols}
    for name, d, keys in (('links', L, rows), ('rechts', R, rows), ('boven', T_, cols), ('onder', B, cols)):
        st = [(keys[i], d[keys[i + 1]] - d[keys[i]]) for i in range(len(keys) - 1)]
        i = 0
        while i < len(st):
            j = i
            while j + 1 < len(st) and st[j + 1][1] == st[i][1]: j += 1
            if st[i][1] != 0 and abs(st[i][1]) == 1 and j - i + 1 >= minrun - 1:
                out.append('%s %d..%d stap %d' % (name, st[i][0], st[j][0] + 1, st[i][1]))
            i = j + 1
    return out
if __name__ == '__main__':
    for f in (0, 1):
        print('frame %d regelmatige trappen (>=5):' % (f + 1), profiles(T.read_png(os.path.join(T.H, '..', 'anim_front.png'), f)))
