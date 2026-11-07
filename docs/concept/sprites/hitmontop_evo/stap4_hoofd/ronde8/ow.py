"""Ronde 8: bron = Hitmontops overworld-sprite (frame 1), kop rechtop en van voren."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from hulp import *
from PIL import Image
OWIM = Image.open(os.path.join(ROOT, 'graphics/pokemon/hitmontop/overworld.png'))

def stap1():
    """uitsnede van de kop (regel van stap3b KOP_OW: geen blauw, geen handen onder de kin), OW-palet -> frontpalet."""
    px = OWIM.load(); d = {}
    for y in range(8, 23):
        for x in range(4, 27):
            v = px[x, y]
            if v and v not in (7, 8, 9, 10) and not (y >= 21 and (x <= 9 or x >= 21)):
                d[(x, y)] = v
    m = {2: 3, 4: 4, 3: 5, 1: 5, 5: 15, 6: 1}
    out = {p: m[v] for p, v in d.items()}
    N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for p in out:                      # omlijning zoals de frontsprite: buitenrand zwart
        if any((p[0] + a, p[1] + b) not in out for a, b in N4): out[p] = 15
    return out

def dubbel(d, kolommen=(), rijen=()):
    """kolommen/rijen verdubbelen (in vlakke delen): alles rechts/onder schuift op."""
    out = {}
    for (x, y), i in d.items():
        nx = x + sum(1 for k in kolommen if k < x); ny = y + sum(1 for r in rijen if r < y)
        out[(nx, ny)] = i
        if x in kolommen: out[(nx + 1, ny)] = i
        if y in rijen: out[(nx, ny + 1)] = i
        if x in kolommen and y in rijen: out[(nx + 1, ny + 1)] = i
    return out
