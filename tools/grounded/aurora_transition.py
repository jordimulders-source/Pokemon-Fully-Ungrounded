"""Project Grounded: genereert de graphics voor de Suicune-gevechtstransitie (noorderlicht).
Schrijft graphics/battle_transitions/aurora.png (tiles), aurora.bin (tilemap 32x32, palet 15)
en aurora.pal (NFRAMES paletten van 16 kleuren voor de kleurcyclus).
Gebruik: python3 tools/grounded/aurora_transition.py"""
import math, struct
from PIL import Image

PERIOD = 80          # horizontale herhaling in pixels (houdt het aantal unieke tiles laag)
W, H = 240, 160
NFRAMES = 16

def level(x, y):
    x %= PERIOD
    t = 2 * math.pi * x / PERIOD
    # gordijnen: een paar golvende banden met fijne verticale streepjes
    c = 0.55 + 0.25 * math.sin(2 * t + 0.8 * math.sin(t)) + 0.2 * math.sin(5 * t + 1.3)
    streak = 0.75 + 0.25 * math.sin(x * 1.7 + 0.3 * y / 8)
    # verticaal: helder bovenin het midden, zacht uitlopend naar beneden (gordijnranden)
    top = 18 + 10 * math.sin(t + 0.5)
    v = math.exp(-((y - (top + 40)) / 38.0) ** 2)
    if y < top:
        v *= max(0.0, 1 - (top - y) / 10)
    val = max(0.0, min(1.0, c * streak * v * 1.25))
    return int(round(val * 15))

# volledige afbeelding opbouwen en in tiles ontdubbelen
tiles, index, tilemap = [], {}, [0] * (32 * 32)
blank = tuple([0] * 64)
tiles.append(blank); index[blank] = 0
for ty in range(H // 8):
    for tx in range(W // 8):
        tile = tuple(level(tx * 8 + px, ty * 8 + py) for py in range(8) for px in range(8))
        if tile not in index:
            index[tile] = len(tiles); tiles.append(tile)
        tilemap[ty * 32 + tx] = index[tile] | (15 << 12)
assert len(tiles) <= 512, len(tiles)

cols = 16
rows = (len(tiles) + cols - 1) // cols
img = Image.new('P', (cols * 8, rows * 8))
for i, tile in enumerate(tiles):
    ox, oy = (i % cols) * 8, (i // cols) * 8
    for p, v in enumerate(tile):
        img.putpixel((ox + p % 8, oy + p // 8), v)

def lerp(a, b, f):
    return tuple(a[k] + (b[k] - a[k]) * f for k in range(3))

STOPS = [(4, 31, 12), (6, 28, 31), (22, 10, 31), (4, 31, 12)]  # groen -> cyaan -> paars -> groen
def gradient(h):
    h = h % 1.0 * (len(STOPS) - 1)
    i = int(h)
    return lerp(STOPS[i], STOPS[i + 1], h - i)

frames = []
for f in range(NFRAMES):
    pal = [(0, 0, 0)]
    for i in range(1, 16):
        b = (i / 15) ** 0.8
        col = gradient(i / 15 * 0.7 + f / NFRAMES)
        pal.append(tuple(int(round(c * b)) for c in col))
    frames.append(pal)

img.putpalette([v * 8 for c in frames[0] for v in c] + [0] * (768 - 48))
img.save('graphics/battle_transitions/aurora.png')
open('graphics/battle_transitions/aurora.bin', 'wb').write(struct.pack('<%dH' % len(tilemap), *tilemap))
with open('graphics/battle_transitions/aurora.pal', 'w', newline='\r\n') as fp:
    fp.write('JASC-PAL\n0100\n%d\n' % (16 * NFRAMES))
    for pal in frames:
        for c in pal:
            fp.write('%d %d %d\n' % tuple(v * 8 for v in c))
print('tiles:', len(tiles))
