"""Project Grounded: genereert de graphics voor de Deoxys-gevechtstransitie (ruimte + DNA-helix).
Een sterrenhemel met een horizontale dubbele helix (oranje/cyaan, de kleuren van Deoxys) door het midden.
Het beeld is 256 breed zodat het naadloos horizontaal kan scrollen (BG0 is 32 tiles breed).
Schrijft graphics/battle_transitions/deoxys.png (tiles), deoxys.bin (tilemap 32x32, palet 15)
en deoxys.pal (NFRAMES paletten voor het twinkelen van de sterren).
Gebruik: python3 tools/grounded/deoxys_transition.py"""
import math, random, struct
from PIL import Image

W, H = 256, 160
PERIOD = 64          # helixperiode in pixels (deelt 256)
CY, AMP = 80, 22     # midden en amplitude van de helix
NFRAMES = 8
random.seed(386)

img = [[0] * W for _ in range(H)]
# sterren (indices 1-4, elk met een eigen twinkelfase), niet in de helixband
for _ in range(120):
    x, y = random.randrange(W), random.randrange(H)
    if abs(y - CY) < AMP + 10:
        continue
    img[y][x] = random.randint(1, 4)
    if random.random() < 0.15 and x + 1 < W and y + 1 < H:   # een paar grotere sterren
        img[y][x + 1] = img[y + 1][x] = img[y][x]

def strand(x, phase):
    t = 2 * math.pi * x / PERIOD + phase
    return CY + AMP * math.sin(t), math.cos(t)   # y, diepte (>0 = voor)

def put(x, y, c):
    y = int(round(y))
    for dy in (-1, 0, 1):
        if 0 <= y + dy < H:
            img[y + dy][x % W] = c

layers = []
for x in range(W):
    for k, (phase, base) in enumerate(((0.0, 5), (math.pi, 8))):
        y, d = strand(x, phase)
        shade = 0 if d < -0.3 else (1 if d < 0.4 else 2)
        layers.append((d, x, y, base + shade))
# basenparen (sporten) om de 8 pixels, kleur wisselend
rungs = []
for x in range(4, W, 8):
    y1, _ = strand(x, 0.0); y2, _ = strand(x, math.pi)
    c = 11 if (x // 8) % 2 else 12
    for y in range(int(min(y1, y2)) + 2, int(max(y1, y2)) - 1):
        rungs.append((x, y, c))
# achterkant, dan sporten, dan voorkant
for d, x, y, c in sorted(layers):
    if d < 0: put(x, y, c)
for x, y, c in rungs:
    img[y][x] = c
for d, x, y, c in sorted(layers):
    if d >= 0: put(x, y, c)

tiles, index, tilemap = [], {}, [0] * 1024
blank = tuple([0] * 64); tiles.append(blank); index[blank] = 0
for ty in range(H // 8):
    for tx in range(W // 8):
        t = tuple(img[ty * 8 + py][tx * 8 + px] for py in range(8) for px in range(8))
        if t not in index:
            index[t] = len(tiles); tiles.append(t)
        tilemap[ty * 32 + tx] = index[t] | (15 << 12)
assert len(tiles) <= 512, len(tiles)

out = Image.new('P', (128, ((len(tiles) + 15) // 16) * 8))
for n, t in enumerate(tiles):
    for p, v in enumerate(t):
        out.putpixel(((n % 16) * 8 + p % 8, (n // 16) * 8 + p // 8), v)

ORANGE = [(120, 40, 16), (216, 96, 40), (255, 168, 96)]   # strand A: achter, midden, voor
CYAN = [(16, 80, 110), (40, 176, 208), (160, 240, 255)]  # strand B
RUNGS = [(150, 80, 200), (240, 220, 120)]                # paars kristal, geel
NEBULA = [(20, 8, 40), (40, 16, 72), (70, 30, 110)]      # ongebruikt, voor later
frames = []
for f in range(NFRAMES):
    pal = [(0, 0, 0)]
    for s in range(4):
        b = 0.35 + 0.65 * (0.5 + 0.5 * math.cos(2 * math.pi * (f / NFRAMES + s / 4)))
        pal.append(tuple(int(255 * b) for _ in range(3)))
    pal += ORANGE + CYAN + RUNGS + NEBULA
    frames.append(pal)
out.putpalette([v for c in frames[0] for v in c] + [0] * (768 - 48))
out.save('graphics/battle_transitions/deoxys.png')
open('graphics/battle_transitions/deoxys.bin', 'wb').write(struct.pack('<1024H', *tilemap))
with open('graphics/battle_transitions/deoxys.pal', 'w', newline='\r\n') as fp:
    fp.write('JASC-PAL\n0100\n%d\n' % (16 * NFRAMES))
    for pal in frames:
        for c in pal:
            fp.write('%d %d %d\n' % c)
print('tiles:', len(tiles))
