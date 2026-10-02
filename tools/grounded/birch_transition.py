"""Project Grounded: genereert de graphics voor Birch' gevechtstransitie (bruine prut die over het beeld druipt).
Tiles (vaste volgorde, de C-code rekent erop):
  0        leeg
  1-4      massieve bruine prut (1-3 spikkels, 4 met een maiskorrel; de C-code kiest 4 zelden)
  5-36     druprand: 4 rijen x 8 kolommen (periode 64 px), onderste rij = voorkant
Palet 15: graphics/battle_transitions/birch.pal
Gebruik: python3 tools/grounded/birch_transition.py"""
import math, random, struct
from PIL import Image

random.seed(1)
BASE, DARK, LIGHT, OUT, WHITE, BLACK, MOUTH, TONGUE, CORN = 1, 2, 3, 4, 5, 6, 7, 8, 13

def solid_tile(v):
    t = [[BASE] * 8 for _ in range(8)]
    for _ in range(2 if v < 3 else 1):
        t[random.randrange(8)][random.randrange(8)] = DARK
    if v == 1:
        t[random.randrange(8)][random.randrange(8)] = LIGHT
    if v == 3:   # maiskorrel
        x, y = 3, 3
        t[y][x] = t[y][x + 1] = t[y + 1][x] = t[y + 1][x + 1] = CORN
    return t

tiles = [[[0] * 8 for _ in range(8)]] + [solid_tile(v) for v in range(4)]

# druprand: 32 px hoog, 64 breed; boven massief, onderaan druppels van verschillende lengte
edge = [[0] * 64 for _ in range(32)]
drops = [(4, 30, 4), (14, 18, 3), (24, 27, 5), (37, 22, 3), (47, 31, 4), (57, 16, 3)]
for x in range(64):
    base = 8 + 3 * math.sin(2 * math.pi * x / 64 * 2)   # golvende onderkant van de prut
    depth = base
    for cx, ln, r in drops:
        d = abs(x - cx)
        if d <= r:
            depth = max(depth, ln - (r - math.sqrt(r * r - d * d)) if d < r else base)
    for y in range(32):
        if y < depth:
            edge[y][x] = BASE
    for y in range(32):   # donkere rand onder elke kolom
        if edge[y][x] == BASE and (y + 1 >= 32 or edge[y + 1][x] == 0):
            edge[y][x] = DARK
for x in range(0, 64, 9):   # een paar spikkels
    y = random.randrange(0, 6); edge[y][x] = DARK
for cx, ln, r in drops:     # glimlichtje in elke druppel
    if 0 < ln - r < 32:
        edge[int(ln - r)][cx - 1] = LIGHT
for ry in range(4):
    for cx in range(8):
        tiles.append([[edge[ry * 8 + y][cx * 8 + x] for x in range(8)] for y in range(8)])
assert len(tiles) == 37


img = Image.new('P', (128, ((len(tiles) + 15) // 16) * 8))
for n, t in enumerate(tiles):
    for y in range(8):
        for x in range(8):
            img.putpixel(((n % 16) * 8 + x, (n // 16) * 8 + y), t[y][x])

PAL = [(0, 0, 0), (104, 62, 26), (70, 40, 16), (176, 120, 64), (40, 22, 8)] + [(0, 0, 0)] * 8 + [(248, 216, 64), (0, 0, 0), (0, 0, 0)]
frames = [PAL]
img.putpalette([v for c in frames[0] for v in c] + [0] * (768 - 48))
img.save('graphics/battle_transitions/birch.png')
with open('graphics/battle_transitions/birch.pal', 'w', newline='\r\n') as fp:
    fp.write('JASC-PAL\n0100\n16\n')
    for p in frames:
        for c in p:
            fp.write('%d %d %d\n' % c)
print('tiles', len(tiles))
