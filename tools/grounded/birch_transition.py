"""Project Grounded: genereert de graphics voor Birch' gevechtstransitie (poep-thema).
Tiles (vaste volgorde, de C-code rekent erop):
  0        leeg
  1-4      massieve bruine prut (1-3 spikkels, 4 met een maiskorrel; de C-code kiest 4 zelden)
  5-36     druprand: 4 rijen x 8 kolommen (periode 64 px), onderste rij = voorkant
  37-156   drol-emoji met stanklijnen: 12 x 10 tiles, prut erachter
Palet 15 (4 frames, de stanklijnen bewegen door paletcycli): graphics/battle_transitions/birch.pal
Gebruik: python3 tools/grounded/birch_transition.py"""
import math, random, struct
from PIL import Image

random.seed(1)
BASE, DARK, LIGHT, OUT, WHITE, BLACK, MOUTH, TONGUE, CORN = 1, 2, 3, 4, 5, 6, 7, 8, 13
EMO1, EMO2, EMO3 = 14, 15, 3     # emoji: midden, licht, schaduw (licht van de prut)
STINK = [9, 10, 11, 12]

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

# drol-emoji 96 x 80 met prut erachter
EW, EH = 96, 80
emo = [[BASE] * EW for _ in range(EH)]
for _ in range(40):
    emo[random.randrange(EH)][random.randrange(EW)] = DARK
def ellipse(cx, cy, rx, ry, c, outline=True):
    for y in range(EH):
        for x in range(EW):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 1:
                emo[y][x] = c
            elif outline and d <= (1 + 2.2 / min(rx, ry)) ** 2:
                if emo[y][x] not in (EMO1, EMO2, EMO3):
                    emo[y][x] = OUT
# drie lagen + tipje (van onder naar boven tekenen zodat de bovenste over de onderste valt)
ellipse(48, 66, 34, 11, EMO1)
ellipse(48, 52, 27, 10, EMO1)
ellipse(48, 40, 19, 9, EMO1)
for y in range(22, 33):     # tipje dat naar rechts krult
    w = (y - 22) * 0.7 + 1
    cx = 50 + (33 - y) * 0.35
    for x in range(EW):
        if abs(x - cx) <= w:
            emo[y][x] = EMO1
        elif abs(x - cx) <= w + 1.2 and emo[y][x] not in (EMO1, EMO2, EMO3):
            emo[y][x] = OUT
# glimlicht en schaduw per laag
for (cx, cy, rx, ry) in [(48, 66, 34, 11), (48, 52, 27, 10), (48, 40, 19, 9)]:
    for y in range(EH):
        for x in range(EW):
            if emo[y][x] != EMO1: continue
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d > 1: continue
            if y < cy - ry * 0.45 and x < cx: emo[y][x] = EMO2
            elif y > cy + ry * 0.55: emo[y][x] = EMO3
# ogen
for ex in (38, 58):
    ellipse(ex, 49, 6, 7, WHITE, outline=False)
    for y in range(EH):
        for x in range(EW):
            if ((x - ex - 1) / 2.6) ** 2 + ((y - 50) / 3.2) ** 2 <= 1: emo[y][x] = BLACK
    emo[47][ex + 1] = WHITE
# grote grijns
for y in range(EH):
    for x in range(EW):
        dx = (x - 48) / 15; dy = (y - 59) / 7
        if dx * dx + dy * dy <= 1 and y >= 59:
            emo[y][x] = MOUTH
            if y == 59 or y == 60: emo[y][x] = WHITE      # tanden
            if ((x - 48) / 7) ** 2 + ((y - 65) / 2.5) ** 2 <= 1: emo[y][x] = TONGUE
            if ((dx * dx + dy * dy) > 0.82): emo[y][x] = BLACK
for x in range(33, 64):
    if emo[59][x] in (WHITE, MOUTH): emo[58][x] = BLACK
# stanklijnen: golvende lijnen boven de drol, elke pixel een fase-index zodat ze omhoog 'stromen'
for lx in (22, 48, 74):
    for y in range(2, 26):
        x = int(round(lx + 3 * math.sin(y / 3.0 + lx)))
        if emo[y][x] == BASE or emo[y][x] == DARK:
            emo[y][x] = STINK[(y // 3) % 4]
            if emo[y][x + 1] in (BASE, DARK): emo[y][x + 1] = STINK[(y // 3) % 4]
for ty in range(EH // 8):
    for tx in range(EW // 8):
        tiles.append([[emo[ty * 8 + y][tx * 8 + x] for x in range(8)] for y in range(8)])
assert len(tiles) == 157

img = Image.new('P', (128, ((len(tiles) + 15) // 16) * 8))
for n, t in enumerate(tiles):
    for y in range(8):
        for x in range(8):
            img.putpixel(((n % 16) * 8 + x, (n // 16) * 8 + y), t[y][x])

def pal(frame):
    p = [(0, 0, 0), (104, 62, 26), (70, 40, 16), (176, 120, 64), (40, 22, 8), (255, 255, 255), (16, 8, 0),
         (150, 30, 30), (240, 120, 140)]
    for i in range(4):   # stank: 2 van de 4 fasen zichtbaar, schuift elke frame
        on = (i - frame) % 4 < 2
        p.append((120, 200, 60) if on and (i - frame) % 4 == 0 else ((80, 150, 40) if on else (104, 62, 26)))
    p += [(248, 216, 64), (150, 96, 44), (204, 150, 88)]
    return p
frames = [pal(f) for f in range(4)]
img.putpalette([v for c in frames[0] for v in c] + [0] * (768 - 48))
img.save('graphics/battle_transitions/birch.png')
with open('graphics/battle_transitions/birch.pal', 'w', newline='\r\n') as fp:
    fp.write('JASC-PAL\n0100\n%d\n' % 64)
    for p in frames:
        for c in p:
            fp.write('%d %d %d\n' % c)
print('tiles', len(tiles))
