"""Project Grounded: decor achteraan de Lavaridge-tileset (lavabuis onder Jagged Pass, top van Mt. Chimney).

Voegt nieuwe tiles toe na de 450 vanilla-tiles en nieuwe metatiles na de 441 vanilla-metatiles (vanilla-nummers
blijven gelijk, dus Lavaridge, Jagged Pass, Mt. Chimney, Fiery Path en de Magma Hideout veranderen niet).
Eigen palet 12 (was leeg): basalt, as, gloeiende sintels, zwavel en hout.

Elke decoratie bestaat in twee versies: op grotgrind (308) en op berggrond (271); de bovenlaag (de decoratie
zelf) is gedeeld. Alles is laagtype COVERED (onder de speler). Namen + nummers: lavaridge/decor.json
(gelezen door chimney_ext.py). Idempotent: begint steeds opnieuw vanaf de vanilla-aantallen.

Gebruik: python3 tools/grounded/lavaridge_decor.py [voorbeeld.png]
Daarna: make data/tilesets/secondary/lavaridge/tiles.4bpp (gebeurt ook gewoon bij make)."""
import json, math, os, random, re, struct, sys
from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
os.chdir(REPO)
TS = 'data/tilesets/secondary/lavaridge/'
BASE_TILES, BASE_METATILES = 450, 441
MAX_TILES = 512
random.seed(4519)

PAL12 = [(0, 0, 0),
         (41, 33, 41), (66, 57, 66), (98, 90, 98), (131, 123, 131),   # 1-4 basalt
         (205, 200, 200), (164, 160, 164),                           # 5-6 as
         (156, 32, 8), (238, 106, 16), (255, 205, 57),               # 7-9 sintels
         (139, 115, 24), (213, 189, 41), (246, 230, 106), (255, 255, 213),  # 10-13 zwavel
         (82, 52, 36), (139, 98, 65)]                                # 14-15 hout

# ---------------------------------------------------------------- tekenen (indices in palet 12, 0 = transparant)
def canvas(w, h):
    return [[0] * w for _ in range(h)]

def crystal(c, bx, by, wid, hgt, lean):
    """Zwavelkristal als prisma: linkervlak licht, rechtervlak midden, donkere rand, puntje bovenaan."""
    from PIL import ImageDraw
    im = Image.new('P', (len(c[0]), len(c)), 0)
    d = ImageDraw.Draw(im)
    tx, ty = bx + lean, by - hgt
    half = wid / 2.0
    L = [(bx - half, by), (tx - half, ty + half), (tx, ty - 1), (tx, by + 1)]
    R = [(tx, by + 1), (tx, ty - 1), (tx + half, ty + half), (bx + half, by)]
    d.polygon(L, fill=12, outline=10)
    d.polygon(R, fill=11, outline=10)
    d.line([(tx - 1, ty + 1), (bx - 1, by - 2)], fill=13)
    for y in range(len(c)):
        for x in range(len(c[0])):
            v = im.getpixel((x, y))
            if v: c[y][x] = v

def sulfur(seed, n):
    r = random.Random(seed)
    c = canvas(16, 16)
    # korst
    for y in range(12, 16):
        for x in range(1, 15):
            if abs(x - 7.5) / 7.0 + abs(y - 14) / 2.6 < 1 and r.random() < 0.85:
                c[y][x] = r.choice((10, 11, 11))
    xs = [4, 11, 7][:n] if n <= 3 else [3, 6, 9, 12]
    hs = [r.randint(6, 8), r.randint(5, 7), r.randint(9, 11)]
    order = sorted(range(n), key=lambda k: -hs[k])
    for k in order:
        crystal(c, xs[k], 14, r.choice((4, 5)), hs[k], r.choice((-2, -1, 1, 2)) if xs[k] != 7 else 0)
    return c

def ash(seed):
    r = random.Random(seed)
    c = canvas(16, 16)
    cx, cy, rx, ry = 8 + r.uniform(-1, 1), 10.5, r.uniform(5, 6.5), r.uniform(3.2, 4.2)
    for y in range(16):
        for x in range(16):
            d = ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2
            if d <= 1:
                shade = (x - cx) * 0.6 + (y - cy) * 1.0 + r.uniform(-1.2, 1.2)
                c[y][x] = 5 if shade < -1.5 else 6 if shade < 1.5 else 4
                if d > 0.82 and y > cy: c[y][x] = 3
    for _ in range(3):
        x, y = r.randint(2, 13), r.randint(13, 15)
        if c[y][x] == 0: c[y][x] = 6
    return c

def crack(seed, glow=True):
    r = random.Random(seed)
    c = canvas(16, 16)
    def line(x, y, ang, length, w):
        for i in range(length):
            xi, yi = int(round(x)), int(round(y))
            if not (0 <= xi < 16 and 0 <= yi < 16): return
            c[yi][xi] = 8 if glow and w else 7
            for dx, dy in ((1, 0), (0, 1)):
                xx, yy = xi + dx, yi + dy
                if 0 <= xx < 16 and 0 <= yy < 16 and c[yy][xx] == 0: c[yy][xx] = 1
            ang += r.uniform(-0.5, 0.5)
            x += math.cos(ang); y += math.sin(ang)
            if r.random() < 0.08 and length > 4:
                line(x, y, ang + r.choice((-1.1, 1.1)), length // 3, 0)
    a = r.uniform(0, math.pi)
    line(8 - 6 * math.cos(a), 8 - 6 * math.sin(a), a, 13, 1)
    # gloeiende kern
    for y in range(16):
        for x in range(16):
            if c[y][x] == 8 and r.random() < 0.3: c[y][x] = 9
    return c

def rock(w, h, seed, sym=False):
    """Kei (palet 11-kleuren via mapping later): we tekenen in palet 12 met basalttinten + licht."""
    r = random.Random(seed)
    c = canvas(w, h)
    cx, cy = w / 2.0, h * 0.58
    rx, ry = w * 0.46, h * 0.40
    for y in range(h):
        for x in range(w):
            xx = x if not sym or x < w / 2 else w - 1 - x
            d = ((xx + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2
            bump = 0.08 * math.sin(xx * 1.7 + seed) + 0.06 * math.cos(y * 2.3)
            if d <= 1 + bump:
                lx = (xx - cx) / rx; ly = (y - cy) / ry
                shade = lx * 0.5 + ly * 0.9
                c[y][x] = 4 if shade < -0.45 else 3 if shade < 0.15 else 2
                if d > 0.86 + bump: c[y][x] = 1
    # spleten
    for _ in range(max(1, w // 8)):
        x, y = r.randint(w // 4, 3 * w // 4), r.randint(h // 3, 2 * h // 3)
        for i in range(r.randint(2, 4)):
            if 0 <= x < w and 0 <= y < h and c[y][x] in (2, 3, 4): c[y][x] = 1
            x += r.choice((-1, 0, 1)); y += 1
    if sym:
        for y in range(h):
            for x in range(w // 2, w):
                c[y][x] = c[y][w - 1 - x]
    return c

def basalt(seed):
    """Gestolde lavastroom 32x32: donkere kussens met gloeiende naden, symmetrisch."""
    r = random.Random(seed)
    w = h = 32
    c = canvas(w, h)
    for y in range(h):
        for x in range(w // 2):
            dx = (x + .5 - 16) / 15.5; dy = (y + .5 - 18) / 9.5
            d = dx * dx + dy * dy + 0.10 * math.sin(y * 0.9) + 0.06 * math.cos(x * 1.3)
            if d <= 1:
                c[y][x] = 2 if d > 0.8 else 3
    # kussenranden (lichte bovenkant, donkere onderkant)
    for y in range(1, h - 1):
        for x in range(w // 2):
            if c[y][x] and c[y - 1][x] == 0: c[y][x] = 4
            if c[y][x] and c[y + 1][x] == 0: c[y][x] = 1
    for y0 in (14, 21):
        for x in range(2, 16):
            y = y0 + int(1.5 * math.sin(x * 0.7 + y0))
            if 0 <= y < h and c[y][x] not in (0,):
                c[y][x] = 7 if r.random() < 0.6 else 8
                if y + 1 < h and c[y + 1][x]: c[y + 1][x] = 1
    for y in range(h):
        for x in range(w // 2, w):
            c[y][x] = c[y][w - 1 - x]
    return c

def stump(seed):
    c = canvas(16, 16)
    for y in range(6, 15):
        for x in range(4, 12):
            c[y][x] = 15 if x < 7 else 14
    for x in range(4, 12): c[6][x] = 6; c[7][x] = 5 if 5 < x < 10 else 6
    for x in (5, 8, 10): c[10][x] = 14
    for x in (3, 12): c[14][x] = 14
    c[13][3] = 14; c[13][12] = 14
    for x in range(3, 13): c[15][x] = 1 if c[15][x] == 0 else c[15][x]
    return c

def deadtree(seed):
    """Dode, verkoolde boom: 16x32."""
    c = canvas(16, 32)
    for y in range(12, 31):
        for x in range(6, 10):
            c[y][x] = 15 if x < 8 else 14
    for x in (4, 5, 10, 11): c[30][x] = 14
    def branch(x, y, dx, dy, n):
        for i in range(n):
            if 0 <= x < 16 and 0 <= y < 32:
                c[y][x] = 14
                if 0 <= y - 1 and c[y - 1][x] == 0: c[y - 1][x] = 15
            x += dx; y += dy
    branch(7, 13, -1, -1, 6); branch(8, 15, 1, -1, 6); branch(7, 12, 0, -1, 9)
    branch(3, 8, -1, -1, 3); branch(12, 10, 1, -1, 3); branch(7, 4, 1, -1, 3)
    for x in range(3, 13): c[31][x] = 1
    return c

# ---------------------------------------------------------------- tiles verzamelen
def split(c):
    h, w = len(c), len(c[0])
    out = []
    for ty in range(0, h, 8):
        row = []
        for tx in range(0, w, 8):
            row.append(tuple(tuple(c[ty + y][tx + x] for x in range(8)) for y in range(8)))
        out.append(row)
    return out

EMPTY = tuple(tuple([0] * 8) for _ in range(8))
class Bank:
    def __init__(self):
        self.tiles = []; self.index = {}
    def add(self, t):
        if t == EMPTY: return 0, False, False          # primary-tile 0 is leeg
        for hf in (False, True):
            for vf in (False, True):
                v = t
                if hf: v = tuple(tuple(reversed(r)) for r in v)
                if vf: v = tuple(reversed(v))
                if v in self.index: return self.index[v], hf, vf
        i = 512 + BASE_TILES + len(self.tiles)
        self.tiles.append(t); self.index[t] = i
        return i, False, False

CAVE_BOTTOM = [(0x22f, 11)] * 4
GROUND_BOTTOM = [(0x052, 10), (0x053, 10), (0x062, 10), (0x063, 10)]
FLOOR_ATTR = {'cave': 0x08, 'ground': 0x0c}
COVERED = 1 << 12

ITEMS = [  # naam, tekening, botsen
    ('sulfur_a', sulfur(1, 2), True),
    ('sulfur_b', sulfur(7, 3), True),
    ('crack_a', crack(3), False),
    ('crack_b', crack(21), False),
    ('ash_a', ash(5), False),
    ('ash_b', ash(9), False),
    ('rock', rock(16, 16, 2), True),
    ('boulder', rock(32, 32, 6, sym=True), True),
    ('basalt', basalt(8), False),
    ('stump', stump(0), True),
    ('deadtree', deadtree(0), True),
]

def entry(tile, pal, hf=False, vf=False):
    return tile | (0x400 if hf else 0) | (0x800 if vf else 0) | (pal << 12)

def main():
    bank = Bank()
    parts = {}
    for name, art, col in ITEMS:
        parts[name] = [[bank.add(t) for t in row] for row in split(art)]
    assert BASE_TILES + len(bank.tiles) <= MAX_TILES, 'te veel tiles: %d' % (BASE_TILES + len(bank.tiles))
    # tiles.png
    im = Image.open(TS + 'tiles.png')
    pal = im.getpalette()
    W = 16
    total = BASE_TILES + len(bank.tiles)
    rows = (total + W - 1) // W
    new = Image.new('P', (128, rows * 8), 0); new.putpalette(pal)
    old = im.crop((0, 0, 128, min(im.height, (BASE_TILES + W - 1) // W * 8)))
    new.paste(old, (0, 0))
    px = new.load()
    # alles na BASE_TILES leegmaken (padding van de oude png)
    for i in range(BASE_TILES, rows * W):
        tx, ty = (i % W) * 8, (i // W) * 8
        for y in range(8):
            for x in range(8): px[tx + x, ty + y] = 0
    for k, t in enumerate(bank.tiles):
        i = BASE_TILES + k
        tx, ty = (i % W) * 8, (i // W) * 8
        for y in range(8):
            for x in range(8): px[tx + x, ty + y] = t[y][x]
    new.save(TS + 'tiles.png')
    # num_tiles in graphics_file_rules.mk
    mk = open('graphics_file_rules.mk').read()
    mk = re.sub(r'(secondary/lavaridge/tiles\.4bpp: %\.4bpp: %\.png\n\t\$\(GFX\) \$< \$@ -num_tiles )\d+', r'\g<1>%d' % total, mk)
    open('graphics_file_rules.mk', 'w').write(mk)
    # palet 12
    open(TS + 'palettes/12.pal', 'w').write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in PAL12))
    # metatiles
    mt = open(TS + 'metatiles.bin', 'rb').read()[:BASE_METATILES * 16]
    at = open(TS + 'metatile_attributes.bin', 'rb').read()[:BASE_METATILES * 2]
    names = {}
    n = BASE_METATILES
    for name, art, col in ITEMS:
        grid = parts[name]
        for floor, bottom in (('cave', CAVE_BOTTOM), ('ground', GROUND_BOTTOM)):
            ids = []
            for my in range(len(grid) // 2):
                row = []
                for mx in range(len(grid[0]) // 2):
                    q = [grid[my * 2][mx * 2], grid[my * 2][mx * 2 + 1], grid[my * 2 + 1][mx * 2], grid[my * 2 + 1][mx * 2 + 1]]
                    ent = [entry(t, p) for t, p in bottom] + [entry(t, 12, hf, vf) for t, hf, vf in q]
                    mt += struct.pack('<8H', *ent)
                    at += struct.pack('<H', FLOOR_ATTR[floor] | COVERED)
                    row.append(0x200 + n); n += 1
                ids.append(row)
            names['%s_%s' % (name, floor)] = {'ids': ids, 'collision': col}
    assert n <= 512, 'te veel metatiles: %d' % n
    open(TS + 'metatiles.bin', 'wb').write(mt)
    open(TS + 'metatile_attributes.bin', 'wb').write(at)
    json.dump(names, open(TS + 'decor.json', 'w'), indent=1)
    print('tiles %d (+%d), metatiles %d (+%d)' % (total, len(bank.tiles), n, n - BASE_METATILES))
    if len(sys.argv) > 1:
        S = 6
        prev = Image.new('RGB', (len(ITEMS) * 40 * S // 2, 40 * S // 2 * 2), (60, 40, 40))
        x = 0
        for name, art, col in ITEMS:
            for floor_rgb, oy in (((214, 160, 140), 0), ((150, 110, 100), 20)):
                h, w = len(art), len(art[0])
                for yy in range(h):
                    for xx in range(w):
                        v = art[yy][xx]
                        rgb = PAL12[v] if v else floor_rgb
                        for a in range(S // 2):
                            for b in range(S // 2):
                                prev.putpixel(((x + xx) * S // 2 + a, (oy * 2 + yy) * S // 2 + b), rgb)
            x += 40 // 1 if False else (len(art[0]) + 6)
        prev.save(sys.argv[1])

if __name__ == '__main__':
    main()
