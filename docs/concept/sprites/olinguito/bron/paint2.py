"""Handwerk op de geschaalde basis (base_f1/base_f2.txt) -> f1.txt, f2.txt."""
from paint import *
from head import HEAD1, HEAD2, ARM2
from body import BODY1, BODY2

def dither(g, pairs=(('1', '2', 1), ('2', '3', 1))):
    """Overgangsband (schaakbord, 'depth' px breed) waar twee vachttinten elkaar
    raken: pixels van de donkere tint met de lichte tint binnen 'depth' px links
    of erboven worden op even (x+y) de lichte tint. Alleen binnen het vlak (alle
    8 buren vacht), dus nooit over de omlijning."""
    fur = set('123')
    out = [r[:] for r in g]
    for y in range(2, 62):
        for x in range(2, 62):
            if (x + y) % 2: continue
            nb8 = [g[y+dy][x+dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
            if not all(c in fur for c in nb8): continue
            for lo, hi, depth in pairs:
                if g[y][x] != hi: continue
                near = [g[y][x-k] for k in range(1, depth + 1)] + [g[y-k][x] for k in range(1, depth + 1)]
                if lo in near:
                    out[y][x] = lo
    for y in range(64): g[y][:] = out[y]

def run(frame):
    g = load('base_f%d.txt' % frame)
    def P(x0, y0, rows):
        patch(g, x0, y0, rows)
    if frame == 1:
        P(12, 17, HEAD1)
        P(8, 38, BODY1)
    else:
        P(11, 16, HEAD2)
        P(31, 20, ARM2)
        P(8, 38, BODY2)
        P(22, 37, ['4337777332'])
    dither(g, (('1','2',1),('2','3',2)))
    save(g, 'f%d.txt' % frame)

run(1); run(2)
