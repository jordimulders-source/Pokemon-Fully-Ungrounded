"""Project Grounded: tilesets van Chargestone Cave (Spacetime Cave-sidequest, Unova in een andere tijd).

  chargestone_general  (primary)   General-tiles/metatiles met donkerblauw getinte paletten (alleen paletten).
  chargestone          (secondary) Kopie van Meteor Falls (zelfde metatile-nummers, dus meteor_falls_ext.Map werkt)
                       met donkerblauwe paletten + achteraan eigen metatiles op palet 9:
                       zwevende magneetstenen (2x2, twee vormen, elk ook gespiegeld), een zwevende scherf (1x1)
                       en twee vonkjes op de vloer (beloopbaar). De stenen zijn procedureel getekend (geen bronsheet).
                       9 okt (Jordi: te steriel): grote zwevende steen (3x3), kleine steentjes, kristallen (1x1, 2x2),
                       gloeiende scheuren (beloopbaar) op palet 9; kabels (beloopbaar), Colress' machineresten,
                       een terminal, een spoel en schroot op palet 11 (staal/koper/amber). Ongebruikte Meteor Falls-
                       tiles vallen weg (de tileset zat vol), de metatile-nummers blijven gelijk.
Gebruik: python3 tools/grounded/maptools/chargestone_tiles.py   (daarna make voor de tiles.4bpp)
Geeft de metatile-nummers terug via ids() (ook zonder opnieuw te genereren)."""
import os, struct, math, random
import numpy as np
from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)

SRC = 'data/tilesets/secondary/meteor_falls'
DST = 'data/tilesets/secondary/chargestone'
PRIM_SRC = 'data/tilesets/primary/general'
PRIM = 'data/tilesets/primary/chargestone_general'
PAL = 9
DARK = 10        # verdonkerd palet 6: rotsbovenkant buiten de wanden
MPAL = 11        # machines en kabels
FLOOR_MT = 0x201
BACKDROP = (10, 14, 32)
VOID_MT = 0x211          # Meteor Falls: alleen tile 0 -> achtergrondkleur

# palet 9: zwevende stenen en kristallen
CS = [(255, 0, 255), (12, 18, 48), (28, 40, 88), (40, 60, 120), (60, 88, 160), (88, 124, 196), (128, 164, 224),
      (32, 104, 216), (56, 152, 248), (120, 200, 248), (200, 236, 248), (248, 248, 248), (72, 136, 216),
      (144, 192, 240), (0, 0, 0), (0, 0, 0)]
# palet 11: staal, koper, amber, rood, kabels
MS = [(255, 0, 255), (14, 16, 26), (40, 46, 60), (72, 82, 100), (118, 128, 146), (184, 192, 204), (92, 54, 34),
      (156, 94, 50), (214, 150, 86), (248, 188, 56), (216, 52, 44), (248, 248, 248), (96, 204, 248), (24, 30, 44),
      (52, 62, 82), (0, 0, 0)]


def jasc(path):
    L = open(path).read().replace('\r', '').split('\n')[3:19]
    return [tuple(int(v) for v in l.split()) for l in L]


def write_pal(path, cols):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % tuple(c) for c in cols))


def lum(c):
    return 0.30 * c[0] + 0.55 * c[1] + 0.15 * c[2]


def tint(c):
    """Donker, koel blauw: helderheid blijft grotendeels, kleur wordt staalblauw."""
    L = lum(c)
    t = (L * 0.34 + 6, L * 0.45 + 8, L * 0.76 + 18)
    return tuple(int(min(248, max(0, 0.10 * a + 0.90 * b))) for a, b in zip(c, t))


# ---------------------------------------------------------------------------------------------- tekenen
def _stone(seed, w=32, h=32, ry=10.5, cy=11.0, crystals=3):
    """Zwevende magneetsteen (RGBA-indices, 0 = transparant): een gefacetteerde blok met blauwe kristallen,
    daaronder een gloeiende lichtvlek op de vloer (geen contact: de steen zweeft)."""
    rnd = random.Random(seed)
    img = np.zeros((h, w), np.uint8)
    cx = w / 2 - 0.5
    rx = w / 2 - 3.2
    # vorm: superellips met ruis per hoek
    noise = [rnd.uniform(-0.12, 0.12) for _ in range(12)]
    body = np.zeros((h, w), bool)
    for y in range(h):
        for x in range(w):
            dx, dy = (x - cx) / rx, (y - cy) / ry
            a = math.atan2(dy, dx)
            k = int((a + math.pi) / (2 * math.pi) * 12) % 12
            r = (abs(dx) ** 2.4 + abs(dy) ** 2.4) ** (1 / 2.4)
            if r < 1.0 + noise[k]:
                body[y, x] = True
    # schaduw/licht: licht van linksboven, facetten via kwantisatie
    for y in range(h):
        for x in range(w):
            if not body[y, x]:
                continue
            dx, dy = (x - cx) / rx, (y - cy) / ry
            s = -0.55 * dx - 0.75 * dy + 0.25
            s += 0.18 * (((x // 5) + (y // 4)) % 2) - 0.09        # grove facetten
            v = 2 if s < -0.35 else 3 if s < 0.05 else 4 if s < 0.45 else 5
            img[y, x] = v
    # kristallen: driehoekige uitsteeksels (lichtblauw) die uit de bovenkant/zijkant steken
    for i in range(crystals):
        bx = int(cx + rnd.uniform(-rx * 0.6, rx * 0.6))
        by = int(cy - ry * rnd.uniform(0.0, 0.7))
        hgt = min(rnd.randint(6, 10), by - 1)
        wid = rnd.randint(2, 3)
        lean = rnd.choice((-1, 0, 1))
        for t in range(hgt):
            yy = by - t
            half = wid * (1 - t / hgt) + 0.4
            xc = bx + lean * t / 3
            for xx in range(int(xc - half), int(xc + half) + 1):
                if 0 <= yy < h and 0 <= xx < w:
                    side = xx < xc
                    img[yy, xx] = 10 if (t > hgt - 3) else (9 if side else 7)
                    body[yy, xx] = True
        if 0 <= by < h:
            img[by, max(0, bx - 1):bx + 2] = 8
    # gloeiende aders
    for _ in range(4):
        x, y = rnd.randint(int(cx - rx * 0.6), int(cx + rx * 0.6)), rnd.randint(int(cy - 2), int(cy + ry * 0.6))
        for _ in range(rnd.randint(3, 6)):
            if 0 <= y < h and 0 <= x < w and img[y, x] in (2, 3, 4):
                img[y, x] = 12 if img[y, x] < 4 else 13
            x += rnd.choice((-1, 0, 1)); y += rnd.choice((0, 1))
    # omlijning
    out = img.copy()
    for y in range(h):
        for x in range(w):
            if body[y, x]:
                continue
            if any(0 <= y + dy < h and 0 <= x + dx < w and body[y + dy, x + dx]
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y, x] = 1
    # lichtvlek op de vloer (geditherd), los van de steen
    gy = cy + ry + 5.0
    for y in range(h):
        for x in range(w):
            if out[y, x]:
                continue
            d = ((x - cx) / (rx * 0.85)) ** 2 + ((y - gy) / 2.6) ** 2
            if d < 0.35 and (x + y) % 2 == 0:
                out[y, x] = 13
            elif d < 1.0 and (x + y) % 2 == 0 and (x // 2 + y) % 2 == 0:
                out[y, x] = 12
    return out


def _shard(seed):
    """Kleine zwevende scherf (1x1) met een lichtpuntje eronder."""
    rnd = random.Random(seed)
    img = np.zeros((16, 16), np.uint8)
    cx = 7.5
    for y in range(1, 11):
        half = (1 - abs(y - 5.5) / 5.5) * 4.2
        for x in range(16):
            if abs(x - cx) <= half:
                img[y, x] = 10 if (y < 4 and x < cx) else 9 if x < cx else 7 if y > 7 else 8
    out = img.copy()
    for y in range(16):
        for x in range(16):
            if img[y, x]:
                continue
            if any(0 <= y + dy < 16 and 0 <= x + dx < 16 and img[y + dy, x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y, x] = 1
    for x in range(5, 11):
        if x % 2 == 0:
            out[14, x] = 13
    out[13, 7] = out[13, 8] = 12
    return out


def _sparkle(seed):
    """Vonkjes op de vloer (beloopbaar)."""
    rnd = random.Random(seed)
    img = np.zeros((16, 16), np.uint8)
    for _ in range(3):
        x, y = rnd.randint(2, 13), rnd.randint(2, 13)
        img[y, x] = 11
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            img[y + dy, x + dx] = 9
        if rnd.random() < 0.5:
            img[y + 2, x] = 13
    for _ in range(4):
        x, y = rnd.randint(1, 14), rnd.randint(1, 14)
        if not img[y, x]:
            img[y, x] = 12
    return img


def _outline(img, body, col=1):
    out = img.copy()
    h, w = img.shape
    for y in range(h):
        for x in range(w):
            if body[y, x]:
                continue
            if any(0 <= y + dy < h and 0 <= x + dx < w and body[y + dy, x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y, x] = col
    return out


def _crystal(seed, w=16, h=16, n=3, base=None, glow=True):
    """Kristalcluster dat uit de vloer groeit (palet 9): schuine spiesen, licht links, wit puntje, gloed aan de voet."""
    rnd = random.Random(seed)
    img = np.zeros((h, w), np.uint8)
    body = np.zeros((h, w), bool)
    base = base if base is not None else h - 3
    k = w / 16.0
    spikes = sorted(((rnd.uniform(w * 0.28, w * 0.72), rnd.randint(int(h * 0.45), int(h * 0.8)), rnd.uniform(1.6, 2.6) * k,
                      rnd.uniform(-0.3, 0.3) / k) for _ in range(n)), key=lambda t: -t[1])
    for bx, hgt, wid, lean in spikes:
        for t in range(hgt):
            yy = base - t
            half = wid * (1 - t / hgt) + 0.35
            xc = bx + lean * t
            for xx in range(int(math.floor(xc - half)), int(math.ceil(xc + half)) + 1):
                if 0 <= yy < h and 0 <= xx < w and abs(xx - xc) <= half:
                    img[yy, xx] = 11 if t >= hgt - 2 else (10 if xx < xc - 0.3 else 9 if xx < xc + 0.4 else 7)
                    body[yy, xx] = True
    out = _outline(img, body)
    if glow:
        for y in range(base + 1, h):
            for x in range(w):
                if not out[y, x] and abs(x - w / 2) < w * 0.35 and (x + y) % 2 == 0:
                    out[y, x] = 13 if y == base + 1 else 12
    return out


def _crack(seed):
    """Gloeiende scheur in de vloer (beloopbaar): grillige lijn met een geditherde blauwe gloed."""
    rnd = random.Random(seed)
    img = np.zeros((16, 16), np.uint8)
    pts = []
    x, y = rnd.uniform(1, 4), rnd.uniform(3, 12)
    while x < 15:
        pts.append((int(x), int(y)))
        x += rnd.uniform(0.8, 1.6); y = min(14, max(1, y + rnd.uniform(-1.3, 1.3)))
    core = set()
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for i in range(5):
            core.add((round(x0 + (x1 - x0) * i / 4), round(y0 + (y1 - y0) * i / 4)))
    if rnd.random() < 0.7:                           # zijtak
        bx, by = pts[len(pts) // 2]
        d = rnd.choice((-1, 1))
        for i in range(1, rnd.randint(3, 5)):
            core.add((bx + i // 2, by + d * i))
    for (cx_, cy_) in core:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                xx, yy = cx_ + dx, cy_ + dy
                if 0 <= xx < 16 and 0 <= yy < 16 and (xx, yy) not in core and not img[yy, xx] and (xx + yy) % 2 == 0:
                    img[yy, xx] = 12
    for (cx_, cy_) in core:
        if 0 <= cx_ < 16 and 0 <= cy_ < 15:
            img[cy_ + 1, cx_] = 7 if (cx_, cy_ + 1) not in core else img[cy_ + 1, cx_]
    for (cx_, cy_) in core:
        if 0 <= cx_ < 16 and 0 <= cy_ < 16:
            img[cy_, cx_] = 10 if rnd.random() < 0.5 else 9
    return img


def _seg_dist(px, py, a, b):
    (x0, y0), (x1, y1) = a, b
    vx, vy = x1 - x0, y1 - y0
    t = max(0.0, min(1.0, ((px - x0) * vx + (py - y0) * vy) / float(vx * vx + vy * vy or 1)))
    return math.hypot(px - (x0 + t * vx), py - (y0 + t * vy))


def _cable(kind):
    """Kabel over de vloer (palet 11, beloopbaar): H, V of een bocht (NE = van boven naar rechts, enz.)."""
    c = 7.5
    ends = {'N': (c, -2), 'S': (c, 17), 'W': (-2, c), 'E': (17, c)}
    segs = [(ends[kind[0]], (c, c)), ((c, c), ends[kind[1]])]
    img = np.zeros((16, 16), np.uint8)
    for y in range(16):
        for x in range(16):
            d = min(_seg_dist(x, y, a, b) for a, b in segs)
            if d <= 0.75:
                img[y, x] = 14
            elif d <= 1.7:
                img[y, x] = 13
            elif d <= 2.5:
                img[y, x] = 1
    return img


def _machine(seed):
    """Kapotte generator van Colress (2x2, palet 11): stalen kast, panelen, amber lampjes, een verbogen koperspoel."""
    rnd = random.Random(seed)
    img = np.zeros((32, 32), np.uint8)
    body = np.zeros((32, 32), bool)
    for y in range(9, 29):
        for x in range(3, 29):
            body[y, x] = True
            img[y, x] = 4 if y < 13 else 3
    for y in range(14, 28):                          # panelen
        img[y, 10] = img[y, 21] = 2
    for x in range(4, 28):
        img[13, x] = 2; img[28, x] = 2
    for y in range(16, 26, 2):                       # ventilatierooster
        for x in range(12, 20):
            img[y, x] = 2
    for x, y, c in ((6, 16, 9), (6, 19, 9), (6, 22, 10), (24, 16, 12), (25, 18, 9)):
        img[y, x] = c; img[y, x + 1] = c
    for y in range(10, 12):                          # bovenkant licht
        for x in range(5, 27):
            if (x + y) % 3:
                img[y, x] = 5
    for t in range(10):                              # verbogen spoel
        x, y = 20 + int(1.5 * math.sin(t / 2.0)), 9 - t
        for dx in (-2, -1, 0, 1, 2):
            if 0 <= y < 32:
                img[y, x + dx] = (8 if (t % 2) else 7) if abs(dx) < 2 else 6
                body[y, x + dx] = True
    for _ in range(5):                               # vonken
        x, y = rnd.randint(14, 28), rnd.randint(0, 6)
        if not body[y, x]:
            img[y, x] = 12
    for x in range(14, 22):                          # deuk/scheur
        y = 20 + (x - 14) // 3
        img[y, x] = 1
    out = _outline(img, body)
    for x in range(4, 28):                           # schaduw
        if (x % 2) == 0:
            out[30, x] = 13
    return out


def _console(seed):
    img = np.zeros((16, 16), np.uint8)
    body = np.zeros((16, 16), bool)
    for y in range(4, 15):
        for x in range(2, 14):
            body[y, x] = True; img[y, x] = 3 if y > 10 else 4
    for y in range(6, 10):
        for x in range(4, 12):
            img[y, x] = 12 if (y + x) % 3 else 11
    img[12, 4] = 9; img[12, 6] = 10; img[12, 9] = 9
    return _outline(img, body)


def _coil(seed):
    img = np.zeros((16, 16), np.uint8)
    body = np.zeros((16, 16), bool)
    for y in range(12, 15):
        for x in range(3, 13):
            body[y, x] = True; img[y, x] = 3 if y > 12 else 4
    for y in range(4, 12):
        for x in range(6, 10):
            body[y, x] = True; img[y, x] = 8 if y % 2 else 7
    for y in range(1, 5):
        for x in range(5, 11):
            if (x - 7.5) ** 2 + (y - 2.5) ** 2 <= 5:
                body[y, x] = True; img[y, x] = 11 if (x < 7 and y < 3) else 5
    out = _outline(img, body)
    for x, y in ((3, 2), (12, 3), (2, 6), (13, 7)):
        out[y, x] = 12
    return out


def _scrap(seed):
    rnd = random.Random(seed)
    img = np.zeros((16, 16), np.uint8)
    body = np.zeros((16, 16), bool)
    for _ in range(3):
        cx_, cy_ = rnd.uniform(4, 12), rnd.uniform(7, 12)
        rx, ry, a = rnd.uniform(2, 4), rnd.uniform(1, 2.2), rnd.uniform(0, math.pi)
        for y in range(16):
            for x in range(16):
                u = (x - cx_) * math.cos(a) + (y - cy_) * math.sin(a)
                v = -(x - cx_) * math.sin(a) + (y - cy_) * math.cos(a)
                if abs(u) <= rx and abs(v) <= ry:
                    body[y, x] = True
                    img[y, x] = 5 if v < -ry * 0.4 else 4 if v < ry * 0.3 else 3
    for t in range(9):                               # koperdraadje
        x, y = 3 + t, int(13 - 2 * math.sin(t / 2.5))
        img[y, x] = 7; body[y, x] = True
    return _outline(img, body)


# ---------------------------------------------------------------------------------------------- opbouw
def _tiles_of(png):
    idx = np.array(Image.open(png))
    n = idx.shape[0] // 8 * 16
    return [idx[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] for i in range(n)]


NT_SRC = 460      # Meteor Falls (-num_tiles 460)


def build():
    os.makedirs(PRIM + '/palettes', exist_ok=True)
    open(PRIM + '/BASE', 'w').write('general\n')
    for i in range(16):
        cols = jasc(PRIM_SRC + '/palettes/%02d.pal' % i)
        c0 = BACKDROP if i == 0 else cols[0]          # palet 0 kleur 0 = achtergrond (leegte buiten de grot)
        write_pal(PRIM + '/palettes/%02d.pal' % i, [c0] + [tint(c) for c in cols[1:]])
    os.makedirs(DST + '/palettes', exist_ok=True)
    for i in range(16):
        cols = jasc(SRC + '/palettes/%02d.pal' % i)
        if i == PAL:
            cols = CS
        elif i == MPAL:
            cols = MS
        elif i == DARK:
            p6 = jasc(SRC + '/palettes/06.pal')
            cols = [p6[0]] + [tuple(int(v * 0.42) for v in tint(c)) for c in p6[1:]]
        elif 6 <= i <= 12:
            cols = [cols[0]] + [tint(c) for c in cols[1:]]
        write_pal(DST + '/palettes/%02d.pal' % i, cols)
    tiles = _tiles_of(SRC + '/tiles.png')[:NT_SRC]
    mt = bytearray(open(SRC + '/metatiles.bin', 'rb').read())
    at = bytearray(open(SRC + '/metatile_attributes.bin', 'rb').read())
    # ongebruikte Meteor Falls-tiles weglaten (de tileset zat vol); metatiles naar de nieuwe nummers
    used = sorted({(e & 0x3FF) - 512 for e in struct.unpack('<%dH' % (len(mt) // 2), mt) if (e & 0x3FF) >= 512} | {0})
    remap = {o: n for n, o in enumerate(used)}
    tiles = [tiles[o] for o in used]
    ents = list(struct.unpack('<%dH' % (len(mt) // 2), mt))
    for i, e in enumerate(ents):
        if (e & 0x3FF) >= 512:
            ents[i] = (e & 0xFC00) | (512 + remap[(e & 0x3FF) - 512])
    mt = bytearray(struct.pack('<%dH' % len(ents), *ents))
    floor = struct.unpack_from('<4H', mt, (FLOOR_MT - 512) * 16)
    floor_attr = struct.unpack_from('<H', at, (FLOOR_MT - 512) * 2)[0]
    cache = {}

    def tile(t):
        """Tile-index + flipbits (ontdubbelt ook gespiegeld)."""
        if not t.any():
            return 0, 0
        for fl, v in ((0, t), (1, t[:, ::-1]), (2, t[::-1]), (3, t[::-1, ::-1])):
            k = v.tobytes()
            if k in cache:
                return cache[k], fl
        tiles.append(t.copy())
        cache[t.tobytes()] = len(tiles) - 1
        return len(tiles) - 1, 0

    def ent(t, pal=PAL):
        n, fl = tile(t)
        if n == 0 and not t.any():
            return 0
        return (512 + n) | (fl << 10) | (pal << 12)

    out = {}

    def add(key, art, cols, rows, blocked, flip=False, pal=PAL, walk_covered=False):
        ids = []
        for r in range(rows):
            for c in range(cols):
                q = art[r * 16:r * 16 + 16, c * 16:c * 16 + 16]
                if flip:
                    q = art[r * 16:r * 16 + 16, (cols - 1 - c) * 16:(cols - c) * 16][:, ::-1]
                top = [ent(q[sy:sy + 8, sx:sx + 8], pal) for sy in (0, 8) for sx in (0, 8)]
                mt.extend(struct.pack('<8H', *floor, *top))
                # COVERED: de speler loopt altijd vóór de steen langs (geen afgekapte hoofden); beloopbaar decor
                # houdt het vloergedrag (wilde Pokemon) maar ligt ook onder de speler
                at.extend(struct.pack('<H', 0x1000 if blocked else (0x1000 | (floor_attr & 0xFF)) if walk_covered
                                      else floor_attr))
                ids.append(len(mt) // 16 - 1 + 512)
        out[key] = ids

    sA, sB = _stone(7), _stone(31, crystals=4)
    add('stoneA', sA, 2, 2, True)
    add('stoneA_f', sA, 2, 2, True, flip=True)
    add('stoneB', sB, 2, 2, True)
    add('stoneB_f', sB, 2, 2, True, flip=True)
    add('shard', _shard(3), 1, 1, True)
    add('spark1', _sparkle(5), 1, 1, False)
    add('spark2', _sparkle(11), 1, 1, False)
    # donkere rotsbovenkant (buiten de wanden): dezelfde tiles op palet DARK (verdonkerd palet 6)
    for key, src_mt, which in (('rockD', FLOOR_MT, range(4)), ('lipD', 0x23e, range(4)), ('edgeED', 0x234, range(4)),
                               ('edgeWD', 0x23c, range(4)), ('rimSD', 0x286, (2, 3))):
        e = list(struct.unpack_from('<8H', mt, (src_mt - 512) * 16))
        for i in which:
            if e[i] >> 12 == 6:
                e[i] = (e[i] & 0x0FFF) | (DARK << 12)
        if key == 'rockD':
            e[4:] = [0x1000] * 4
        mt.extend(struct.pack('<8H', *e))
        at.extend(struct.pack('<H', 0))
        out[key] = [len(mt) // 16 - 1 + 512]
    # 9 okt: meer decor
    sL = _stone(53, w=48, h=48, ry=15.5, cy=17.0, crystals=5)
    add('stoneL', sL, 3, 3, True)
    add('stoneL_f', sL, 3, 3, True, flip=True)
    add('pebble1', _stone(71, w=16, h=16, ry=4.2, cy=6.0, crystals=1), 1, 1, True)
    add('pebble2', _stone(89, w=16, h=16, ry=4.6, cy=6.5, crystals=1), 1, 1, True)
    add('crys1', _crystal(5, n=3), 1, 1, True)
    add('crys2', _crystal(17, n=4), 1, 1, True)
    add('crysL', _crystal(29, w=32, h=32, n=6), 2, 2, True)
    for i, sd in enumerate((3, 14, 27)):
        add('crack%d' % (i + 1), _crack(sd), 1, 1, False, walk_covered=True)
    for k in ('WE', 'NS', 'NE', 'NW', 'SE', 'SW'):
        add('cable' + k, _cable(k), 1, 1, False, pal=MPAL, walk_covered=True)
    add('machine', _machine(7), 2, 2, True, pal=MPAL)
    add('console', _console(1), 1, 1, True, pal=MPAL)
    add('coil', _coil(1), 1, 1, True, pal=MPAL)
    add('scrap', _scrap(9), 1, 1, True, pal=MPAL)
    assert len(tiles) <= 512, len(tiles)
    n = (len(tiles) + 15) // 16 * 16
    img = np.zeros((n // 16 * 8, 128), np.uint8)
    for i, t in enumerate(tiles):
        img[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = t
    src = Image.open(SRC + '/tiles.png')
    im = Image.fromarray(img, 'P')
    im.putpalette(src.getpalette())
    im.save(DST + '/tiles.png')
    open(DST + '/metatiles.bin', 'wb').write(bytes(mt))
    open(DST + '/metatile_attributes.bin', 'wb').write(bytes(at))
    print(DST, len(tiles), 'tiles,', len(mt) // 16, 'metatiles')
    # voorbeeld (4x) voor de controle
    prev = Image.new('RGB', (16 * 8, 40), (40, 60, 120))
    pal = CS
    x = 0
    prev = Image.new('RGB', (520, 52), (40, 60, 120))
    arts = [(a, CS) for a in (sA, sB, sL, _shard(3), _sparkle(5), _stone(71, w=16, h=16, ry=4.2, cy=6.0, crystals=1),
                              _crystal(5, n=3), _crystal(17, n=4), _crystal(29, w=32, h=32, n=6), _crack(3), _crack(14),
                              _crack(27))]
    arts += [(a, MS) for a in (_cable('WE'), _cable('NE'), _cable('SW'), _machine(7), _console(1), _coil(1), _scrap(9))]
    for art, pal in arts:
        a = Image.fromarray(np.array([[pal[v] if v else (40, 60, 120) for v in row] for row in art], np.uint8))
        prev.paste(a, (x, 0)); x += art.shape[1] + 4
    return out, prev


def ids():
    """Metatile-nummers van de eigen tegels (vaste volgorde, zie build())."""
    first = 512 + 159
    names = [('stoneA', 4), ('stoneA_f', 4), ('stoneB', 4), ('stoneB_f', 4), ('shard', 1), ('spark1', 1), ('spark2', 1),
             ('rockD', 1), ('lipD', 1), ('edgeED', 1), ('edgeWD', 1), ('rimSD', 1),
             ('stoneL', 9), ('stoneL_f', 9), ('pebble1', 1), ('pebble2', 1), ('crys1', 1), ('crys2', 1), ('crysL', 4),
             ('crack1', 1), ('crack2', 1), ('crack3', 1), ('cableWE', 1), ('cableNS', 1), ('cableNE', 1), ('cableNW', 1),
             ('cableSE', 1), ('cableSW', 1), ('machine', 4), ('console', 1), ('coil', 1), ('scrap', 1)]
    out, n = {}, first
    for k, c in names:
        out[k] = list(range(n, n + c)); n += c
    return out


TILESETS = [  # (symbool, map, secondary?, tiles-symbool (None = eigen), metatiles-symbool, callback, omschrijving)
    ('ChargestoneGeneral', 'primary/chargestone_general', False, 'General', 'General', 'InitTilesetAnim_General',
     'Chargestone Cave: General donkerblauw'),
    ('Chargestone', 'secondary/chargestone', True, None, None, 'NULL', 'Chargestone Cave: Meteor Falls blauw + zwevende stenen'),
]


def register():
    gh = open('src/data/tilesets/graphics.h').read()
    mh = open('src/data/tilesets/metatiles.h').read()
    hh = open('src/data/tilesets/headers.h').read()
    for sym, d, sec, tiles_sym, mt_sym, cb, why in TILESETS:
        D = 'data/tilesets/' + d
        tsym, msym = tiles_sym or sym, mt_sym or sym
        if tiles_sym is None and 'gTilesetTiles_%s[]' % sym not in gh:
            gh += '\n// Project Grounded: %s (chargestone_tiles.py)\nconst u32 gTilesetTiles_%s[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n' % (why, sym, D)
        if 'gTilesetPalettes_%s[]' % sym not in gh:
            gh += ('\n// Project Grounded: %s (paletten)\nconst u16 gTilesetPalettes_%s[][16] =\n{\n' % (why, sym)
                   + ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (D, i) for i in range(16)) + '};\n')
        if mt_sym is None and 'gMetatiles_%s[]' % sym not in mh:
            mh += ('\nconst u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin"); // Project Grounded: %s\n'
                   'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % (sym, D, why, sym, D))
        if 'gTileset_%s =' % sym not in hh:
            hh += ('\nconst struct Tileset gTileset_%s = // Project Grounded: %s\n{\n'
                   '    .isCompressed = TRUE,\n    .isSecondary = %s,\n    .tiles = gTilesetTiles_%s,\n'
                   '    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n'
                   '    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = %s,\n};\n'
                   % (sym, why, 'TRUE' if sec else 'FALSE', tsym, sym, msym, msym, cb))
    open('src/data/tilesets/graphics.h', 'w').write(gh)
    open('src/data/tilesets/metatiles.h', 'w').write(mh)
    open('src/data/tilesets/headers.h', 'w').write(hh)


if __name__ == '__main__':
    o, prev = build()
    assert o == ids(), (o, ids())
    register()
    prev.resize((prev.width * 4, prev.height * 4), Image.NEAREST).save(
        os.environ.get('CS_PREVIEW', '/tmp/claude-0/-home-user-projectgrounded/ffd47e46-6a2e-5021-9ef2-b627d7dbd889/scratchpad/charge/stones.png'))
    print('klaar')
