"""Eenmalig: zet de ronde-8-lagen van olinguito en nachtaap om naar het delen.txt-formaat van ronde 9."""
import sys, os, importlib
REPO = '/home/user/projectgrounded/.claude/worktrees/agent-a8826cf9ffddf4d78'
S = REPO + '/docs/concept/sprites/'


def schrijf(pad, kop, delen):
    with open(pad, 'w') as f:
        f.write(kop)
        for naam, g, dy2 in delen:
            ys = [y for y in range(64) if any(c != '.' for c in g[y])]
            xs = [x for x in range(64) if any(g[y][x] != '.' for y in range(64))]
            f.write('## %s %d %d %d\n' % (naam, xs[0], ys[0], dy2))
            for y in range(ys[0], ys[-1] + 1):
                f.write(''.join(g[y][xs[0]:xs[-1] + 1]) + '\n')


# olinguito
sys.path.insert(0, S + 'olinguito/ronde8/bron')
import build
CH = {v: k for k, v in build.CH.items()}
lagen = [('staart.txt', 0, 0, -1), ('lijf.txt', 0, 0, 0), ('arm_achter.txt', 0, 0, -1), ('voeten.txt', 0, 0, 0),
         ('klauw_voor.txt', 0, 0, -1), ('arm_voor.txt', 0, 0, -1), ('kop.txt', 12, 16, -1)]
delen = []
for n, ox, oy, dy2 in lagen:
    g = build.compose([(n, ox, oy)])
    delen.append((n[:-4], [[CH[v] for v in r] for r in g], dy2))
schrijf(S + 'olinguito/ronde9/bron/delen.txt',
        '# Olinguito ronde 9: delen (achter naar voor). "## naam x y dy2" (dy2 = verschuiving in frame 2).\n'
        '# . transparant | 0 zwart | 1 omlijning-bruin | 2 schaduw | 3 basis | 4 hooglicht | 5 6 7 room | 8 9 a klauw | b wit | c goud | d donkergoud | e rood\n',
        delen)
with open(S + 'olinguito/ronde9/bron/palet.txt', 'w') as f:
    for i, c in enumerate(build.PAL):
        f.write('%s %d %d %d\n' % ((CH[i],) + tuple(c)))

# nachtaap
sys.path.insert(0, S + 'nachtaap/ronde8/bron')
sp = importlib.import_module('sprite')


def laag(grid, ox, oy):
    c = [['.'] * 64 for _ in range(64)]
    for y, r in enumerate(grid):
        for x, ch in enumerate(r):
            X, Y = ox + x + sp.SHIFT_X, oy + y + sp.SHIFT_Y
            if ch != '.' and 0 <= X < 64 and 0 <= Y < 64:
                c[Y][X] = ch
    return c


delen = [('staart', laag(sp.TAIL, sp.TAIL_X, sp.TAIL_Y), -1),
         ('lijf', laag(sp.BODY, sp.BODY_X, sp.BODY_Y), 0),
         ('kop', laag(sp.HEAD, sp.HEAD_X, sp.HEAD_Y), 1)]
schrijf(S + 'nachtaap/ronde9/bron/delen.txt',
        '# Nachtaap ronde 9: delen (achter naar voor). "## naam x y dy2" (dy2 = verschuiving in frame 2).\n', delen)
with open(S + 'nachtaap/ronde9/bron/palet.txt', 'w') as f:
    for ch, c in sp.PAL:
        f.write('%s %d %d %d\n' % ((ch,) + c))
