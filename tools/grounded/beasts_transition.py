"""Project Grounded: genereert de graphics voor de gevechtstransities van Raikou en Entei.
Raikou (bliksem): graphics/battle_transitions/raikou.png (tiles), raikou.bin (RAIKOU_BOLTS tilemaps van 32x32,
  elk een bliksemschicht rond x=128, palet 15) en raikou.pal (16 kleuren).
Entei (vuur): graphics/battle_transitions/entei.png (tiles: vlakvuur, randvlammen en een klein steekvlammetje in
  4 frames) en entei.pal (ENTEI_FRAMES paletten voor het flakkeren). De tilemap maakt de code zelf (groeiende cirkel).
Gebruik: python3 tools/grounded/beasts_transition.py"""
import math, random, struct
from PIL import Image

OUT = 'graphics/battle_transitions/'

def save_tiles(tiles, path, pal):
    cols = 16
    rows = (len(tiles) + cols - 1) // cols
    img = Image.new('P', (cols * 8, rows * 8))
    for i, tile in enumerate(tiles):
        ox, oy = (i % cols) * 8, (i // cols) * 8
        for p, v in enumerate(tile):
            img.putpixel((ox + p % 8, oy + p // 8), v)
    img.putpalette([v * 8 for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    img.save(path)

def save_pal(frames, path):
    with open(path, 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n%d\n' % (16 * len(frames)))
        for pal in frames:
            for c in pal:
                fp.write('%d %d %d\n' % tuple(v * 8 for v in c))

# ---------------------------------------------------------------- Raikou
RAIKOU_BOLTS = 3
rnd = random.Random(243)

def bolt(seed):
    """Pixelraster 256x160 met een gekartelde bliksemschicht (plus zijtakken) rond x=128."""
    r = random.Random(seed)
    heat = [[0] * 256 for _ in range(160)]
    def stroke(x, y, length, width, drift):
        pts = [(x, y)]
        while y < 160 and length > 0:
            step = r.randint(6, 14)
            x += r.randint(-9, 9) + drift
            y += step
            length -= step
            pts.append((x, y))
            if width > 1 and r.random() < 0.18:
                stroke(x, y, r.randint(20, 50), 1, r.choice((-4, 4)))
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0), 1)
            for k in range(n + 1):
                px = x0 + (x1 - x0) * k / n
                py = y0 + (y1 - y0) * k / n
                for dy in range(-4, 5):
                    for dx in range(-4, 5):
                        xx, yy = int(round(px + dx)), int(round(py + dy))
                        if 0 <= xx < 256 and 0 <= yy < 160:
                            d = math.hypot(dx, dy)
                            # 4 = witte kern, 3 = geel, 2 = cyaan gloed, 1 = blauwe halo
                            v = 4 if d <= width * 0.6 else 3 if d <= width * 0.6 + 1 else 2 if d <= width + 1.8 else 1 if d <= width + 3.2 else 0
                            heat[yy][xx] = max(heat[yy][xx], v)
    stroke(128, -4, 999, 2, 0)
    return heat

tiles, index = [tuple([0] * 64)], {tuple([0] * 64): 0}
maps = []
for b in range(RAIKOU_BOLTS):
    heat = bolt(1000 + b * 77)
    tm = [0] * (32 * 32)
    for ty in range(20):
        for tx in range(32):
            tile = tuple(heat[ty * 8 + py][tx * 8 + px] for py in range(8) for px in range(8))
            if tile not in index:
                index[tile] = len(tiles); tiles.append(tile)
            tm[ty * 32 + tx] = index[tile] | (15 << 12)
    maps += tm
assert len(tiles) <= 512, len(tiles)
pal = [(0, 0, 0), (6, 6, 20), (12, 26, 31), (31, 31, 16), (31, 31, 31)] + [(0, 0, 0)] * 11
save_tiles(tiles, OUT + 'raikou.png', pal)
save_pal([pal], OUT + 'raikou.pal')
open(OUT + 'raikou.bin', 'wb').write(struct.pack('<%dH' % len(maps), *maps))
print('raikou tiles:', len(tiles))

# ---------------------------------------------------------------- Entei
ENTEI_FRAMES = 8
r = random.Random(244)

def noise_tile(seed, lo, hi, holes=0.0):
    rr = random.Random(seed)
    t = []
    for py in range(8):
        for px in range(8):
            if rr.random() < holes:
                t.append(0)
            else:
                t.append(rr.randint(lo, hi))
    return t

fire = []
# 1-4: vlakvuur (heet, weinig variatie per pixel), 5-8: randvlammen (koeler, met gaten)
for i in range(4):
    fire.append(noise_tile(10 + i, 7, 13))
for i in range(4):
    # randtile: tongetjes die van onder naar boven uitdunnen
    rr = random.Random(20 + i)
    t = []
    cols = [rr.randint(2, 8) for _ in range(8)]
    for py in range(8):
        for px in range(8):
            h = 8 - py
            t.append(rr.randint(3, 9) if h <= cols[px] and rr.random() > 0.15 else 0)
    fire.append(t)

# 9..: klein steekvlammetje (16x24 pixels = 2x3 tiles) in 4 frames
def small_flame(f):
    img = [[0] * 16 for _ in range(24)]
    for y in range(24):
        for x in range(16):
            ny = y / 23.0                       # 0 = top, 1 = onderkant
            sway = math.sin(ny * 5 + f * 1.6) * (1 - ny) * 2.5
            w = 7.5 * math.sin(math.pi * min(1.0, ny * 0.95 + 0.05)) ** 0.7 * (0.35 + 0.65 * ny)
            d = abs(x - 7.5 - sway)
            if d < w:
                core = 1 - d / w
                v = 3 + core * 9 + ny * 3
                img[y][x] = max(1, min(15, int(v)))
    return img

for f in range(4):
    img = small_flame(f)
    for ty in range(3):
        for tx in range(2):
            fire.append([img[ty * 8 + py][tx * 8 + px] for py in range(8) for px in range(8)])

tiles = [[0] * 64] + fire
assert len(tiles) == 1 + 8 + 24

STOPS = [(6, 0, 0), (20, 2, 0), (31, 10, 0), (31, 20, 2), (31, 29, 10), (31, 31, 26)]
def heat_col(h):
    h = max(0.0, min(1.0, h)) * (len(STOPS) - 1)
    i = min(int(h), len(STOPS) - 2)
    f = h - i
    return tuple(int(round(STOPS[i][k] + (STOPS[i + 1][k] - STOPS[i][k]) * f)) for k in range(3))

frames = []
for f in range(ENTEI_FRAMES):
    pal = [(0, 0, 0)]
    for i in range(1, 16):
        flick = 0.10 * math.sin(2 * math.pi * f / ENTEI_FRAMES + i * 1.7)
        pal.append(heat_col(i / 15 + flick))
    frames.append(pal)
save_tiles(tiles, OUT + 'entei.png', frames[0])
save_pal(frames, OUT + 'entei.pal')
print('entei tiles:', len(tiles))
