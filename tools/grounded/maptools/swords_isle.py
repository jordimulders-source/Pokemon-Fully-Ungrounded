"""Project Grounded: Uncharted Isle (Keldeo), wilde zee met echte draaikolken (aangeroepen door swords_keldeo.py).

Eigen secondary tileset uncharted_isle (primary General) met een tilesetanimatie:
- draaikolk 2x2 (32x32, 8 frames, drie spiraalarmen die 15 graden per frame draaien; General-waterpalet 4). Alle
  draaikolken delen tiles 16-31; de animatie (src/tileset_anims.c, InitTilesetAnim_UnchartedIsle) kopieert elke
  8 frames het volgende frame. Gespiegeld (h-flip) draait dezelfde kolk de andere kant op. Onder elke kolk ligt het
  geanimeerde General-zeewater (onderlaag), de kolk zelf is de bovenlaag en loopt aan de rand geditherd uit.
- rotsen in drie maten (1x1, 2x2, 3x3-zuil) met een schuimkraag (palet 6), wrakhout en steentjes op het eiland,
  branding (schuim, palet 4) op het zeewater langs de zandbank en de rotsen, en schuimkoppen op open zee.
De rand van de kaart (border) is ook een draaikolk. Deterministisch (vaste seed); opnieuw draaien geeft hetzelfde."""
import math, os, random, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ogerpon_quest as oq          # zet ook de werkmap op de repo-root
import jungle_tileset as J
import sea_temple_lugia as stl
from PIL import Image

TS = 'data/tilesets/secondary/uncharted_isle'
SOLID = 0xc00
P_WATER, P_ROCK = 4, 6
WHIRL_SLOT, WHIRL_FRAMES = 16, 8
ROCK_PAL = [(0, 0, 0),
            (40, 40, 56), (72, 72, 88), (104, 104, 120), (144, 144, 152), (184, 184, 192),   # 1-5 rots
            (248, 248, 248), (200, 216, 240),                                                # 6-7 schuim
            (56, 64, 96),                                                                    # 8 natte rots
            (88, 64, 48), (136, 104, 72), (184, 152, 112), (216, 200, 168),                  # 9-12 wrakhout
            (40, 96, 64), (72, 144, 88), (112, 152, 80)]                                     # 13-15 wier/mos
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def dith(x, y, a):
    return BAYER[y & 3][x & 3] < a * 16


GEN_MT = open('data/tilesets/primary/general/metatiles.bin', 'rb').read()
GEN_AT = open('data/tilesets/primary/general/metatile_attributes.bin', 'rb').read()


def gen(m):
    e = struct.unpack_from('<8H', GEN_MT, m * 16)
    return list(e[:4]), list(e[4:]), struct.unpack_from('<H', GEN_AT, m * 2)[0]


class IsleTiles:
    def __init__(self):
        self.tiles = [[[0] * 8 for _ in range(8)] for _ in range(512)]
        self.reserved = set(range(WHIRL_SLOT, WHIRL_SLOT + 16))
        self.free = [t for t in range(1, 512) if t not in self.reserved]
        self.tidx, self.midx, self.mts, self.attrs = {}, {}, bytearray(), bytearray()

    def tile(self, pix):
        t = tuple(tuple(r) for r in pix)
        if not any(any(r) for r in t):
            return 0
        for hf in (0, 1):
            for vf in (0, 1):
                v = tuple(tuple(r[::-1] if hf else r) for r in (t[::-1] if vf else t))
                if v in self.tidx:
                    return self.tidx[v] | (hf << 10) | (vf << 11)
        slot = self.free.pop(0)
        self.tiles[slot] = [list(r) for r in t]
        self.tidx[t] = 512 + slot
        return 512 + slot

    def cut(self, cv, ox, oy, pal):
        ent = []
        for k in range(4):
            x0, y0 = ox + (k % 2) * 8, oy + (k // 2) * 8
            t = self.tile([[cv.get(x0 + x, y0 + y) for x in range(8)] for y in range(8)])
            ent.append(0 if t == 0 else t | (pal << 12))
        return ent

    def metatile(self, bottom, top, attr):
        key = (tuple(bottom), tuple(top), attr)
        if key not in self.midx:
            self.midx[key] = 512 + len(self.mts) // 16
            assert self.midx[key] < 1024
            self.mts += struct.pack('<8H', *(list(bottom) + list(top)))
            self.attrs += struct.pack('<H', attr)
        return self.midx[key]

    def save(self, frames):
        os.makedirs(TS + '/palettes', exist_ok=True)
        os.makedirs(TS + '/anim/whirlpool', exist_ok=True)
        pngpal = Image.open(J.GEN + '/tiles.png').getpalette()
        used = max(i for i in range(512) if any(any(r) for r in self.tiles[i]) or i in self.reserved) + 1
        rows = (used + 15) // 16
        out = Image.new('P', (128, rows * 8), 0)
        out.putpalette(pngpal)
        for n in range(rows * 16):
            for y in range(8):
                for x in range(8):
                    out.putpixel(((n % 16) * 8 + x, (n // 16) * 8 + y), self.tiles[n][y][x])
        out.save(TS + '/tiles.png')
        for f, tiles in enumerate(frames):
            im = Image.new('P', (128, 8), 0)
            im.putpalette(pngpal)
            for n, t in enumerate(tiles):
                for y in range(8):
                    for x in range(8):
                        im.putpixel((n * 8 + x, y), t[y][x])
            im.save('%s/anim/whirlpool/%d.png' % (TS, f))
        for i in range(16):
            J.write_pal('%s/palettes/%02d.pal' % (TS, i), [J.q(c) for c in ROCK_PAL] if i == P_ROCK else [(0, 0, 0)] * 16)
        open(TS + '/metatiles.bin', 'wb').write(self.mts)
        open(TS + '/metatile_attributes.bin', 'wb').write(self.attrs)
        return used, len(self.mts) // 16


# ====================================================================== tekenen
def whirl_frame(f):
    """32x32 draaikolk (palet 4), frame f van WHIRL_FRAMES; 0 = doorzichtig (zeewater eronder)."""
    cv = J.Canvas(32, 32)
    R = 15.8
    phase = f * 2 * math.pi / WHIRL_FRAMES
    for y in range(32):
        for x in range(32):
            dx, dy = x - 15.5, y - 15.5
            r = math.hypot(dx, dy)
            if r > R:
                continue
            th = math.atan2(dy, dx)
            s = math.cos(3 * th + 0.55 * r - phase)
            s2 = math.cos(3 * th + 0.55 * r - phase + 0.9)
            depth = 1 - r / R
            if r < 2.2:
                c = 10
            elif r < 3.6:
                c = 9 if s < 0.3 else 8
            elif s > 0.62:                      # schuimkam op de arm
                c = 1 if r > 10.5 else (2 if r > 7 else 11)
            elif s > 0.35 and s2 > 0:
                c = 11 if r > 8 else 12
            elif s < -0.45:                     # dal tussen de armen
                c = 10 if depth > 0.55 else (9 if depth > 0.3 else 8)
            else:
                c = 9 if depth > 0.5 else (8 if depth > 0.25 else 14)
            if r > 12.2:                        # rand: alleen schuim en wat zee, geditherd weg
                if c in (1, 2, 11, 12):
                    if not dith(x, y, (R - r) / 2.2 + 0.25):
                        c = 0
                elif not dith(x + 1, y + 2, (R - r) / 3.6 - 0.1):
                    c = 0
            cv.p[y][x] = c
    return cv


def rock(w, h, seed, ring=True, tall=False):
    """Rots (palet 6) op een canvas van w x h pixels, met een schuimkraag als ring (op water)."""
    rr = random.Random(seed)
    cv = J.Canvas(w, h)
    m = 3.5 if ring else 1.0
    ax, ay = w / 2 - m, h / 2 - m
    cx, cy = w / 2 - 0.5, h / 2 - 0.5 + (0.5 if ring else 0)
    harm = [(rr.uniform(0, 6.3), rr.uniform(0.04, 0.10), k) for k in (2, 3, 5)]
    facets = [(rr.uniform(-1, 1), rr.uniform(-1, 1), rr.uniform(-0.25, 0.25)) for _ in range(6)]

    def norm(x, y):
        dx, dy = (x - cx) / ax, (y - cy) / ay
        th = math.atan2(dy, dx)
        return math.hypot(dx, dy) / (1 + sum(a * math.cos(k * th + p) for p, a, k in harm))
    inside = [[norm(x, y) < 1 for x in range(w)] for y in range(h)]
    for y in range(h):
        for x in range(w):
            if not inside[y][x]:
                continue
            dx, dy = (x - cx) / ax, (y - cy) / ay
            d = norm(x, y)
            lit = -0.55 * dx - 0.75 * dy + 0.35 * (1 - d)
            for fx, fy, b in facets:            # facetten: vlakken met een eigen helderheid
                if (dx - fx * 0.5) * fx + (dy - fy * 0.5) * fy > 0:
                    lit += b
            if tall:
                lit += 0.25 * math.sin(dx * 7 + rr.random() * 0.2) * 0.4
            c = 5 if lit > 0.75 else 4 if lit > 0.3 else 3 if lit > -0.15 else 2
            if dy > 0.55 and ring:              # natte voet bij de waterlijn
                c = 8 if dith(x, y, (dy - 0.55) * 2.5) else min(c, 2)
            edge = any(not (0 <= x + a < w and 0 <= y + b < h) or not inside[y + b][x + a]
                       for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            cv.p[y][x] = 1 if edge else c
    for _ in range(max(1, w * h // 160)):       # barsten
        x, y = rr.randrange(w), rr.randrange(h)
        for _ in range(rr.randrange(2, 5)):
            if 0 <= x < w and 0 <= y < h and inside[y][x] and cv.p[y][x] not in (1, 8):
                cv.p[y][x] = 2
            x += rr.choice((-1, 0, 1)); y += 1
    if ring:                                    # schuimkraag rond de rots
        for y in range(h):
            for x in range(w):
                if inside[y][x]:
                    continue
                d = norm(x, y)
                g = (d - 1) * min(ax, ay)       # pixels buiten de rots (ongeveer)
                if g < 1.1 and dith(x, y, 0.8):
                    cv.p[y][x] = 6
                elif g < 2.4 and dith(x + 1, y, 0.45):
                    cv.p[y][x] = 7 if (x + y) & 1 else 6
                elif g < 3.4 and dith(x + 2, y + 1, 0.15):
                    cv.p[y][x] = 7
    return cv


def driftwood(seed):
    """Gebleekt stuk wrakhout (32x16, palet 6) met een afgebroken tak."""
    rr = random.Random(seed)
    cv = J.Canvas(32, 16)
    for x in range(3, 29):
        mid = 9 + 1.2 * math.sin(x * 0.25 + seed)
        half = 3.3 if 5 < x < 26 else 2.6
        for y in range(16):
            d = (y - mid) / half
            if abs(d) <= 1:
                c = 12 if d < -0.4 else 11 if d < 0.2 else 10
                if (x * 3 + int(y * 1.7)) % 7 == 0 and abs(d) < 0.8:
                    c = 10 if c != 10 else 9          # nerven
                if abs(d) > 0.85:
                    c = 9
                cv.p[y][x] = c
    bx = rr.randrange(10, 20)
    for i in range(5):                                 # tak
        cv.set(bx + i, int(9 - 2.5 - i * 0.8), 11 if i < 4 else 12)
        cv.set(bx + i, int(9 - 2.5 - i * 0.8) + 1, 9)
    for y in range(16):                                # schaduw op het zand
        for x in range(3, 29):
            if cv.p[y][x] == 0 and y > 0 and cv.p[y - 1][x] in (9, 10, 11) and (x + y) & 1:
                cv.p[y][x] = 9
    return cv


def foam(mask, diag, var=2):
    """Branding (palet 4) op een zeewatervak; mask = buren met zandbank/rots (N, O, Z, W), diag = hoeken."""
    """Losse, korte golfkammetjes evenwijdig aan de kust (geen doorlopende lijn, anders lijkt het een hek)."""
    cv = J.Canvas(16, 16)

    def crest(u0, u1, v, horiz, flip):
        n = u1 - u0
        for i in range(n + 1):
            u = u0 + i
            b = math.sin(i / max(1, n) * math.pi) * 1.1          # boogje, bol naar de kust toe
            vv = v - b if not flip else v + b
            x, y = (u, vv) if horiz else (vv, u)
            cv.set(x, y, 1 if 0 < i < n else 11)
            x2, y2 = (u, vv + (1 if not flip else -1)) if horiz else (vv + (1 if not flip else -1), u)
            if i % 2 == 0:
                cv.set(x2, y2, 11)
    sides = [(1, True, False, 2), (2, False, True, 13), (4, True, True, 13), (8, False, False, 2)]
    for bit, horiz, flip, v in sides:
        if mask & bit:
            near = v - 2 if flip else v + 2
            if var in (0, 2):
                crest(2, 6, v if bit in (1, 8) else near, horiz, flip)
            if var in (1, 2):
                crest(9, 13, near if bit in (1, 8) else v, horiz, flip)
    for k, (cx, cy) in enumerate(((15, 0), (15, 15), (0, 15), (0, 0))):
        if diag & (1 << k):                                      # kort kammetje in de hoek
            for i in range(4):
                a = (i / 3.0) * math.pi / 2
                x = cx + (4 * math.cos(a) if cx == 0 else -4 * math.cos(a))
                y = cy + (4 * math.sin(a) if cy == 0 else -4 * math.sin(a))
                cv.set(x, y, 1 if 0 < i < 3 else 11)
    return cv


def whitecap(v):
    """Schuimkop op open zee (palet 4)."""
    cv = J.Canvas(16, 16)
    pts = [((3, 6), (8, 5)), ((6, 10), (12, 9)), ((2, 11), (6, 10))][v]
    for (x0, y0), (x1, y1) in [pts] + ([((9, 4), (12, 3))] if v == 0 else []):
        n = x1 - x0
        for i in range(n + 1):
            x = x0 + i
            y = y0 + (y1 - y0) * i / max(1, n) - math.sin(i / max(1, n) * math.pi) * 1.2
            cv.set(x, y, 1 if 0 < i < n else 2)
            cv.set(x, y + 1, 11)
            if i % 2 == 0:
                cv.set(x + 1, y + 2, 13)
    return cv


# ====================================================================== kaart
def build(IW, IH, KELDEO, ARRIVE, BRINEY, BOAT, rng):
    W, H = IW, IH
    ts = IsleTiles()
    WATER = gen(0x170)
    frames = []
    for f in range(WHIRL_FRAMES):
        cv = whirl_frame(f)
        frames.append([[[cv.p[ty * 8 + y][tx * 8 + x] for x in range(8)] for y in range(8)]
                       for ty in range(4) for tx in range(4)])
    for i, t in enumerate(frames[0]):
        ts.tiles[WHIRL_SLOT + i] = t
    whirl_at = (WATER[2] & 0xF000)                       # laag 'covered', gedrag normaal; massief in de kaart

    def whirl_piece(mirror):
        piece = []
        for my in range(2):
            for mx in range(2):
                top = []
                for ty in (2 * my, 2 * my + 1):
                    for tx in (2 * mx, 2 * mx + 1):
                        sx = 3 - tx if mirror else tx
                        top.append((512 + WHIRL_SLOT + ty * 4 + sx) | (P_WATER << 12) | ((1 << 10) if mirror else 0))
                piece.append(ts.metatile(WATER[0], top, whirl_at))
        return piece
    WHIRL = [whirl_piece(False), whirl_piece(True)]

    def overlay(base, cv, ox, oy, pal, attr=None):
        b, t, at = base
        return ts.metatile(b, ts.cut(cv, ox, oy, pal), at if attr is None else attr)

    def piece(cv, base, pal=P_ROCK):
        return [overlay(base, cv, i * 16, j * 16, pal) for j in range(cv.h // 16) for i in range(cv.w // 16)]
    ROCK1 = [piece(rock(16, 16, s), WATER) for s in (1, 2, 3)]
    ROCK2 = [piece(rock(32, 32, s), WATER) for s in (11, 12)]
    STACK = piece(rock(48, 48, 21, tall=True), WATER)
    SAND, SHOAL = gen(0x124), gen(0x19e)
    SAND_ROCK = [piece(rock(16, 16, s, ring=False), (SAND[0], [0] * 4, SAND[2])) for s in (31, 32)]
    SHOAL_ROCK = [piece(rock(16, 16, s), SHOAL) for s in (41,)]
    WOOD = [piece(driftwood(s), (SAND[0], [0] * 4, SAND[2])) for s in (1, 4)]

    # --- zandbank en zandplaat (zoals voorheen, met een grilliger kust)
    M = [[0x170] * W for _ in range(H)]

    def blob(rx, ry, noise, inside=None):
        G = [[0] * (W + 1) for _ in range(H + 1)]
        lobes = [(rng.uniform(0, 6.3), rng.uniform(0.05, 0.13), k) for k in (3, 5)]
        for y in range(1, H):
            for x in range(1, W):
                th = math.atan2((y - 10.5) / ry, (x - 14.0) / rx)
                wob = 1 + sum(a * math.cos(k * th + p) for p, a, k in lobes)
                d = ((x - 14.0) / rx) ** 2 + ((y - 10.5) / ry) ** 2
                if d < wob + rng.uniform(-noise, noise) and (inside is None or all(
                        inside[y + b][x + a] for a in (-1, 0, 1) for b in (-1, 0, 1))):
                    G[y][x] = 1
        changed = True
        while changed:
            changed = False
            for y in range(1, H):
                for x in range(1, W):
                    if G[y][x] and G[y - 1][x] + G[y + 1][x] + G[y][x - 1] + G[y][x + 1] < 2:
                        G[y][x] = 0; changed = True
            for y in range(H):
                for x in range(W):
                    q = (G[y][x], G[y][x + 1], G[y + 1][x], G[y + 1][x + 1])
                    if q in ((1, 0, 0, 1), (0, 1, 1, 0)):
                        v = 1 if inside is None else 0
                        G[y][x] = G[y][x + 1] = G[y + 1][x] = G[y + 1][x + 1] = v
                        changed = True
        return G
    V = blob(8.6, 5.8, 0.10)
    S = blob(5.6, 3.4, 0.08, inside=V)
    for y in range(H):
        for x in range(W):
            q = (V[y][x], V[y][x + 1], V[y + 1][x], V[y + 1][x + 1])
            M[y][x] = stl.SHOAL_MS[q]
            s4 = (S[y][x], S[y][x + 1], S[y + 1][x], S[y + 1][x + 1])
            if any(s4):
                assert q == (1, 1, 1, 1), ('zand tegen de rand', x, y)
                M[y][x] = SAND_MS[s4]
    shoal = {(x, y) for y in range(H) for x in range(W) if M[y][x] != 0x170}
    feature = {}                                          # (x,y) -> 'whirl' / 'rock'

    def beh(m):
        m &= 0x3FF
        if m < 512:
            return struct.unpack_from('<H', GEN_AT, m * 2)[0] & 0xFF
        return struct.unpack_from('<H', ts.attrs, (m - 512) * 2)[0] & 0xFF

    def free(x, y, w, h, gap=1):
        for yy in range(y - gap, y + h + gap):
            for xx in range(x - gap, x + w + gap):
                if not (0 <= xx < W and 0 <= yy < H):
                    continue
                if (xx, yy) in shoal or (xx, yy) in feature:
                    return False
        return all(0 <= x + i < W and 0 <= y + j < H for i in range(w) for j in range(h))

    def put(x, y, mts, w, kind):
        for i, mt in enumerate(mts):
            M[y + i // w][x + i % w] = mt | SOLID
            feature[(x + i % w, y + i // w)] = kind

    keep = {(BOAT[0] + dx, BOAT[1] + dy) for dx in (-1, 0, 1, 2) for dy in (-1, 0, 1, 2)}
    for x, y in [(ARRIVE[0], ARRIVE[1] + 1), (BOAT[0], BOAT[1] - 1)]:
        keep.add((x, y))

    def ok(x, y, w, h, gap=1):
        return free(x, y, w, h, gap) and not any((x + i, y + j) in keep for i in range(-1, w + 1) for j in range(-1, h + 1))
    # rotszuilen (3x3) in twee hoeken, dan de buitenring: draaikolken (afwisselend links- en rechtsom) en rotsen
    stacks = 0
    for x, y in rng.sample([(1, 1), (W - 4, 1), (1, H - 4), (W - 4, H - 4)], 4):
        if stacks < 2 and ok(x, y, 3, 3, 0):
            put(x, y, STACK, 3, 'rock'); stacks += 1
    n = 0
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            if (x in (0, W - 2) or y in (0, H - 2)) and free(x, y, 2, 2, 0):
                if rng.random() < 0.18:
                    put(x, y, rng.choice(ROCK2), 2, 'rock')
                else:
                    put(x, y, WHIRL[n % 2], 2, 'whirl'); n += 1
    # tweede ring: open plekken krijgen een kolk of rots
    for y in range(2, H - 2, 2):
        for x in range(2, W - 2, 2):
            if (x in (2, W - 4) or y in (2, H - 4)) and rng.random() < 0.5 and ok(x, y, 2, 2, 0):
                if rng.random() < 0.3:
                    put(x, y, rng.choice(ROCK2), 2, 'rock')
                else:
                    put(x, y, WHIRL[n % 2], 2, 'whirl'); n += 1
    # nog een paar kolken dichter bij het eiland, dan losse steentjes in het open water
    tries, inner = 0, 0
    while inner < 5 and tries < 400:
        tries += 1
        x, y = rng.randrange(1, W - 2), rng.randrange(1, H - 2)
        if ok(x, y, 2, 2):
            put(x, y, WHIRL[n % 2], 2, 'whirl'); n += 1; inner += 1
    tries, small = 0, 0
    while small < 10 and tries < 600:
        tries += 1
        x, y = rng.randrange(1, W - 1), rng.randrange(1, H - 1)
        if ok(x, y, 1, 1):
            put(x, y, rng.choice(ROCK1), 1, 'rock'); small += 1
    # eiland: wrakhout en steentjes, alleen als alles te voet verbonden blijft
    sand = {(x, y) for y in range(H) for x in range(W) if M[y][x] & 0x3FF == 0x124}
    shoal_flat = {(x, y) for y in range(H) for x in range(W) if M[y][x] & 0x3FF == 0x19e}
    near_ev = {(p[0] + a, p[1] + b) for p in (KELDEO, ARRIVE, BRINEY, (KELDEO[0], KELDEO[1] + 1))
               for a in (-1, 0, 1) for b in (-1, 0, 1)}

    def foot_ok(cells):
        foot = {(x, y) for y in range(H) for x in range(W) if not M[y][x] & SOLID and beh(M[y][x]) != 0x15} - set(cells)
        r = oq.reach(M, [ARRIVE], blocked=({(x, y) for y in range(H) for x in range(W)} - foot) | {KELDEO, BRINEY})
        return len(r) == len(foot) - 2
    deco = 0
    for kind, opts, w, pool, want in (('wood', WOOD, 2, sand, 2), ('rock', SAND_ROCK, 1, sand, 3),
                                      ('rock', SHOAL_ROCK, 1, shoal_flat, 2)):
        cand = sorted(pool)
        rng.shuffle(cand)
        got = 0
        for x, y in cand:
            if got >= want:
                break
            cells = [(x + i, y) for i in range(w)]
            if all(c in pool and c not in near_ev and c not in feature for c in cells) and \
                    all((c[0], c[1] + 1) not in feature for c in cells) and foot_ok(cells):
                saved = [M[c[1]][c[0]] for c in cells]
                put(x, y, rng.choice(opts), w, 'deco')
                if not foot_ok([]):
                    for c, v in zip(cells, saved):
                        M[c[1]][c[0]] = v; feature.pop(c)
                    continue
                got += 1; deco += 1
    # branding en schuimkoppen
    foam_n = cap_n = 0
    for y in range(H):
        for x in range(W):
            if M[y][x] != 0x170:
                continue
            def hit(a, b):
                p = (x + a, y + b)
                return p in shoal
            mask = sum(1 << k for k, (a, b) in enumerate(((0, -1), (1, 0), (0, 1), (-1, 0))) if hit(a, b))
            diag = 0
            for k, (a, b) in enumerate(((1, -1), (1, 1), (-1, 1), (-1, -1))):
                if hit(a, b) and not hit(a, 0) and not hit(0, b):
                    diag |= 1 << k
            if (mask or diag) and rng.random() < 0.7:
                M[y][x] = overlay(WATER, foam(mask, diag, rng.randrange(3)), 0, 0, P_WATER); foam_n += 1
            elif rng.random() < 0.16 and not any(feature.get((x + a, y + b)) == 'whirl'
                                                for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                M[y][x] = overlay(WATER, whitecap(rng.randrange(3)), 0, 0, P_WATER); cap_n += 1
    # hoogtes: zeewater 1, ondiepte en zand 3
    for y in range(H):
        for x in range(W):
            if not M[y][x] & SOLID:
                M[y][x] |= (1 << 12) if beh(M[y][x]) == 0x15 else (3 << 12)
    stats = {'kolken': n, 'zuilen': stacks, 'steentjes': small, 'eiland': deco, 'branding': foam_n, 'schuimkoppen': cap_n}
    return ts, frames, M, WHIRL[0], beh, stats


SAND_MS = {(1, 1, 1, 1): 0x124, (0, 0, 0, 1): 0x195, (0, 0, 1, 1): 0x196, (0, 0, 1, 0): 0x197, (0, 1, 0, 1): 0x19d,
           (1, 0, 1, 0): 0x19f, (0, 1, 0, 0): 0x1a5, (1, 1, 0, 0): 0x1a6, (1, 0, 0, 0): 0x1a7,
           (0, 1, 1, 1): 0x185, (1, 0, 1, 1): 0x186, (1, 1, 0, 1): 0x18d, (1, 1, 1, 0): 0x18e}


def register():
    hdr = open('src/data/tilesets/headers.h').read()
    if 'gTileset_UnchartedIsle' not in hdr:
        hdr += '''
const struct Tileset gTileset_UnchartedIsle = // Project Grounded: Keldeo-eiland, draaikolken (swords_isle.py)
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_UnchartedIsle,
    .palettes = gTilesetPalettes_UnchartedIsle,
    .metatiles = gMetatiles_UnchartedIsle,
    .metatileAttributes = gMetatileAttributes_UnchartedIsle,
    .callback = InitTilesetAnim_UnchartedIsle,
};
'''
        open('src/data/tilesets/headers.h', 'w').write(hdr)
    gfx = open('src/data/tilesets/graphics.h').read()
    if 'gTilesetTiles_UnchartedIsle' not in gfx:
        gfx += '\nconst u32 gTilesetTiles_UnchartedIsle[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n\n' % TS
        gfx += 'const u16 gTilesetPalettes_UnchartedIsle[][16] =\n{\n'
        gfx += ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (TS, i) for i in range(16)) + '};\n'
        open('src/data/tilesets/graphics.h', 'w').write(gfx)
    mh = open('src/data/tilesets/metatiles.h').read()
    if 'gMetatiles_UnchartedIsle' not in mh:
        mh += '\nconst u16 gMetatiles_UnchartedIsle[] = INCBIN_U16("%s/metatiles.bin");\n' % TS
        mh += 'const u16 gMetatileAttributes_UnchartedIsle[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % TS
        open('src/data/tilesets/metatiles.h', 'w').write(mh)
    h = open('include/tileset_anims.h').read()
    if 'InitTilesetAnim_UnchartedIsle' not in h:
        h = h.replace('void InitTilesetAnim_Sootopolis(void);\n',
                      'void InitTilesetAnim_Sootopolis(void);\nvoid InitTilesetAnim_UnchartedIsle(void); // Project Grounded\n', 1)
        open('include/tileset_anims.h', 'w').write(h)
    c = open('src/tileset_anims.c').read()
    if 'InitTilesetAnim_UnchartedIsle' not in c:
        frames = ''.join('const u16 gTilesetAnims_UnchartedIsle_Whirlpool_Frame%d[] = INCBIN_U16("%s/anim/whirlpool/%d.4bpp");\n'
                         % (i, TS, i) for i in range(WHIRL_FRAMES))
        table = 'const u16 *const gTilesetAnims_UnchartedIsle_Whirlpool[] = {\n' + ''.join(
            '    gTilesetAnims_UnchartedIsle_Whirlpool_Frame%d,\n' % i for i in range(WHIRL_FRAMES)) + '};\n'
        anchor = 'const u16 *const gTilesetAnims_Sootopolis_StormyWater[] = {'
        i = c.index(anchor)
        c = c[:i] + '// Project Grounded: draaikolken van het Keldeo-eiland (tools/grounded/maptools/swords_isle.py)\n' + \
            frames + table + '\n' + c[i:]
        fn = '''
// Project Grounded: draaikolken van het Keldeo-eiland; tiles %d-%d van de secondary, elke 8 frames een stap
static void QueueAnimTiles_UnchartedIsle_Whirlpool(u16 timer)
{
    u16 i = timer %% ARRAY_COUNT(gTilesetAnims_UnchartedIsle_Whirlpool);
    AppendTilesetAnimToBuffer(gTilesetAnims_UnchartedIsle_Whirlpool[i], (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + %d)), 16 * TILE_SIZE_4BPP);
}

static void TilesetAnim_UnchartedIsle(u16 timer)
{
    if (timer %% 8 == 0)
        QueueAnimTiles_UnchartedIsle_Whirlpool(timer / 8);
}

void InitTilesetAnim_UnchartedIsle(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_UnchartedIsle;
}
''' % (WHIRL_SLOT, WHIRL_SLOT + 15, WHIRL_SLOT)
        c = c.rstrip('\n') + '\n' + fn
        open('src/tileset_anims.c', 'w').write(c)

