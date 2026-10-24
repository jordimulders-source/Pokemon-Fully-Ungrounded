#!/usr/bin/env python3
"""Controles: formaat, box, soliditeit, symmetrie, donker-aandeel, open randen, rechte omtrekstukken,
zwevende delen (losse componenten), bevroren gezicht (pixeldiff met ronde 23), transparency."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tools as T
from PIL import Image
OUTLINE = {1, 2}  # 9 (grijs) telt niet als omlijning naast transparant (keurder)
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
    # bevroren: hele kop van ronde 23 (neus, snuit, masker, oog, grijns, beide oren, schedelbovenkant),
    # behalve de achterkant van de schedel (x>=34, y25-33) die naar binnen mag
    return 8 <= x <= 35 and 18 <= y <= 38 and not (x >= 34 and 25 <= y <= 33)
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
        S = {(x, y) for y in range(64) for x in range(64) if g[y][x]}
        out = set(); st = [(0, 0)]
        while st:
            q = st.pop()
            if q in out or q in S or not (0 <= q[0] < 64 and 0 <= q[1] < 64): continue
            out.add(q); x, y = q; st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        holes = [(x, y) for y in range(64) for x in range(64) if (x, y) not in S and (x, y) not in out]
        print('  ingesloten gaten:', len(holes), holes[:12])
        ys = [y for y in range(64) if any(g[y])]
        print('  kophoogte: oortop y%d, kin y%d -> %.0f%% van de hoogte %d' % (min(ys), min(ys) + 20 - 1, 100 * 20 / (max(ys) - min(ys) + 1), max(ys) - min(ys) + 1))
        def ny(y): return y - 2 - f  # alles 2 rijen omhoog (poten langer); frame 2: nog 1 px
        fd = [(x, y) for y in range(64) for x in range(64) if face_zone(x, y) and 0 <= ny(y) < 64 and r23[0][y][x] != g[ny(y)][x]]
        print('  gezicht (bevroren zone) diff met ronde 23:', len(fd), fd[:12])
        st = straight(g); print('  rechte omtrekstukken >=5:', st)
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
