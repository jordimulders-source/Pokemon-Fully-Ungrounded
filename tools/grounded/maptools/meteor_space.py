"""Project Grounded: de meteoriet in de ruimte (Deoxys-event vanuit het Space Center van Mossdeep, post-game).

Bouwt in één keer (idempotent, vaste seed):
- Tileset data/tilesets/secondary/meteor_space: donkere Meteor Falls-grond (kleuren van Meteor Falls via een
  donkere paarsgrijze ramp), zwarte ruimte met sterren, de aarde, een komeet, gloeiende kristallen (uit de
  Cave-tileset, andere tint). De randen van de meteoriet worden per pixel getekend (lichte rand boven, klifwand
  onder die in het zwart verdwijnt, ronde hoeken) en daarna per 16x16 ontdubbeld tot metatiles (emit() uit
  snow_tileset.py).
- Layout data/layouts/MeteorSpace (44x64) en kaart data/maps/MeteorSpace (map.json, objecten, coord-triggers).
- Registratie: layouts.json, map_groups.json, event_scripts.s (scripts.inc staat met de hand in de kaartmap).
Controleert de bereikbaarheid van alle events vanaf de landingsplek.

Gebruik: python3 tools/grounded/maptools/meteor_space.py [voorbeeld.png]
Nodig: gebouwde tiles.4bpp van general, meteor_falls en cave (het script roept make daarvoor aan)."""
import json, math, os, random, struct, subprocess, sys
from collections import deque
import numpy as np
from PIL import Image

src = open('tools/grounded/snow_tileset.py').read()
ns = {'np': np, 'Image': Image, 'struct': struct, 'os': os, 'LAYER_COVERED': 1}
exec(src[src.index('def to5('):src.rindex('\nif TOWN:')], ns)
emit = ns['emit']

NAME, CONST = 'MeteorSpace', 'METEOR_SPACE'
OUT = 'data/tilesets/secondary/meteor_space'
LAY = 'data/layouts/' + NAME
W, H = 44, 64
MB_NORMAL, MB_CAVE = 0x00, 0x08
SEED = 136

subprocess.run(['make', '-s', 'data/tilesets/primary/general/tiles.4bpp', 'data/tilesets/secondary/meteor_falls/tiles.4bpp',
                'data/tilesets/secondary/cave/tiles.4bpp'], check=True)


# ---------------------------------------------------------------- bronnen: metatiles van bestaande tilesets
def load_ts(path):
    tiles = open(path + '/tiles.4bpp', 'rb').read()
    mts = open(path + '/metatiles.bin', 'rb').read()
    pals = []
    for i in range(16):
        lines = open('%s/palettes/%02d.pal' % (path, i)).read().split('\n')[3:19]
        pals.append([tuple(map(int, l.split())) for l in lines])
    return tiles, mts, pals


GEN = load_ts('data/tilesets/primary/general')
SECS = {'meteor_falls': load_ts('data/tilesets/secondary/meteor_falls'), 'cave': load_ts('data/tilesets/secondary/cave')}


def mt_layers(sec, mid):
    """(onderlaag, bovenlaag) van metatile mid als 16x16 RGBA (kleur 0 = doorzichtig)."""
    st, sm, spal = SECS[sec]
    pt, _, ppal = GEN
    pal = ppal[:6] + spal[6:13] + ppal[13:]
    ent = struct.unpack_from('<8H', sm, (mid - 512) * 16)
    out = []
    for layer in range(2):
        a = np.zeros((16, 16, 4), np.int32)
        for k in range(4):
            e = ent[layer * 4 + k]
            t, hf, vf, pn = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            data, i = (pt, t) if t < 512 else (st, t - 512)
            b = data[i * 32:(i + 1) * 32]
            if len(b) < 32:
                continue
            for y in range(8):
                for x in range(8):
                    sx, sy = (7 - x if hf else x), (7 - y if vf else y)
                    c = (b[sy * 4 + sx // 2] >> (4 * (sx & 1))) & 15
                    if c:
                        a[(k // 2) * 8 + y, (k % 2) * 8 + x] = (*pal[pn][c], 255)
        out.append(a)
    return out


def mt_full(sec, mid):
    bot, top = mt_layers(sec, mid)
    m = top[..., 3:4] > 0
    return np.where(m, top, bot)


# ---------------------------------------------------------------- kleuren
VOID = np.array([6, 4, 14])
RAMP0, RAMP1 = np.array([10, 6, 20]), np.array([112, 98, 134])


def darken(a, gamma=1.4):
    """Meteor Falls-kleuren -> donkere paarsgrijze ramp (helderheid blijft de vorm dragen)."""
    out = a.copy()
    lum = (a[..., 0] * 0.30 + a[..., 1] * 0.55 + a[..., 2] * 0.15) / 255.0
    t = np.clip(lum, 0, 1) ** gamma
    out[..., :3] = (RAMP0[None, None] + (RAMP1 - RAMP0)[None, None] * t[..., None]).astype(np.int32)
    return out


def hue_glow(a, target):
    """Kristal uit de Cave-tileset: helderheid (hoogste kanaal) houden, kleur naar target trekken.
    Onverzadigde, donkere pixels (de schaduw op de grotvloer) worden een paarse schaduw."""
    out = a.copy()
    rgb = a[..., :3].astype(float)
    v = rgb.max(2) / 255.0
    sat = (rgb.max(2) - rgb.min(2)) / 255.0
    tgt = np.array(target, float)[None, None]
    t = np.clip(v, 0, 1)[..., None]
    col = np.where(t < 0.75, tgt * (0.35 + 0.65 * t / 0.75), tgt + (255 - tgt) * ((t - 0.75) / 0.25))
    shadow = ((sat < 0.35) & (v < 0.8))[..., None]
    col = np.where(shadow, np.array([26, 18, 40])[None, None], col)
    out[..., :3] = np.clip(col, 0, 255).astype(np.int32)
    return out


FLOOR = [darken(mt_full('meteor_falls', m)) for m in (0x201, 0x229)]
CLIFF = darken(mt_full('meteor_falls', 0x231), 1.0)           # klifwand (Meteor Falls), wordt naar onder zwart
DECOR = {
    'crater': [[darken(mt_full('meteor_falls', m)) for m in row] for row in ((0x282, 0x283), (0x28A, 0x28B))],
    'boulder': [[darken(mt_full('meteor_falls', m)) for m in row] for row in ((0x208, 0x209, 0x20A), (0x218, 0x219, 0x21A))],
    'rock': [[darken(mt_full('meteor_falls', 0x20E))]],
    'rock2': [[darken(mt_full('meteor_falls', 0x20F))]],
}


def crystal(ramp, flip=False):
    """Gloeiend kristalcluster (16x16): drie scherven met een donkere rand, een lichte en een middenvlak."""
    from PIL import ImageDraw
    dark, mid, light, glint = ramp
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    shards = [([(1, 15), (1, 10), (3, 7), (5, 11), (5, 15)], 3),
              ([(10, 15), (10, 11), (13, 7), (15, 11), (14, 15)], 12),
              ([(5, 15), (4, 6), (8, 0), (11, 6), (10, 15)], 8)]
    for pts, cx in shards:
        d.polygon(pts, fill=mid + (255,))
        right = [p for p in pts if p[0] >= cx] + [(cx, 15)]
        top = min(pts, key=lambda p: p[1])
        d.polygon([top] + [p for p in pts if p[0] > top[0]] + [(top[0], 15)], fill=light + (255,))
        d.line(pts + [pts[0]], fill=dark + (255,))
    d.point([(7, 3), (7, 4), (12, 9), (2, 11)], fill=glint + (255,))
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return np.array(im, dtype=np.int32)


CRYSTALS = [crystal(((16, 40, 64), (40, 168, 208), (120, 232, 248), (240, 255, 255))),
            crystal(((48, 12, 56), (176, 56, 200), (240, 136, 248), (255, 232, 255)), True),
            crystal(((24, 16, 72), (96, 80, 232), (168, 160, 255), (240, 240, 255)))]

# ---------------------------------------------------------------- de meteoriet (cellen)
rng = random.Random(SEED)
ground = np.zeros((H, W), bool)

PATH = [(9, 58), (17, 58), (27, 55), (34, 50), (33, 44), (24, 41), (14, 40), (8, 34), (11, 27), (21, 25),
        (30, 22), (35, 17), (31, 12), (24, 11), (22, 10)]
POCKETS = [[(28, 55), (34, 58), (39, 58)],            # Star Piece
           [(14, 40), (8, 43), (4, 46)],               # Moon Stone
           [(30, 22), (36, 24), (40, 27)]]             # Comet Shard


def noise1(i, s=0):
    r = random.Random(SEED * 1000 + s * 97 + i)
    return r.random()


def brush(points, r0, r1, salt):
    pts = []
    for (ax, ay), (bx, by) in zip(points, points[1:]):
        n = max(1, int(math.hypot(bx - ax, by - ay) * 2))
        for i in range(n):
            pts.append((ax + (bx - ax) * i / n, ay + (by - ay) * i / n))
    pts.append(points[-1])
    for i, (px, py) in enumerate(pts):
        rad = r0 + (r1 - r0) * (0.5 + 0.5 * math.sin(i * 0.37 + salt) * noise1(i // 6, salt))
        for y in range(int(py - rad - 1), int(py + rad + 2)):
            for x in range(int(px - rad - 1), int(px + rad + 2)):
                if 1 <= x < W - 1 and 1 <= y < H - 1 and math.hypot(x - px, y - py) <= rad:
                    ground[y, x] = True


brush(PATH, 1.9, 3.0, 1)
for k, p in enumerate(POCKETS):
    brush(p, 1.6, 2.3, 10 + k)
for (cx, cy, r) in [(9, 57, 3.2), (22, 9, 3.3)]:          # landingsplek en plein met de driehoek
    for y in range(H):
        for x in range(W):
            if math.hypot(x - cx, y - cy) <= r:
                ground[y, x] = True


def cleanup():
    changed = True
    while changed:
        changed = False
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                n = int(ground[y - 1, x]) + int(ground[y + 1, x]) + int(ground[y, x - 1]) + int(ground[y, x + 1])
                if ground[y, x] and n <= 1:
                    ground[y, x] = False; changed = True
                # smalle spleten (1 cel) dichtmaken: zien er rommelig uit met de klifwand
                if not ground[y, x] and ((ground[y - 1, x] and ground[y + 1, x]) or (ground[y, x - 1] and ground[y, x + 1])):
                    ground[y, x] = True; changed = True
        # 2 cellen hoog gat onder grond: klifwand + 1 rij leegte -> ook dicht (te krap voor een wand)
        for y in range(1, H - 2):
            for x in range(1, W - 1):
                if ground[y - 1, x] and not ground[y, x] and not ground[y + 1, x] and ground[y + 2, x]:
                    ground[y, x] = ground[y + 1, x] = True; changed = True


cleanup()
main = ground.copy()                                       # alles wat beloopbaar is

# losse rotsblokjes die in de ruimte zweven (niet bereikbaar, alleen decor)
ASTEROIDS = [(39, 46, 3, 2), (3, 22, 2, 2), (40, 7, 3, 2), (16, 50, 2, 2), (5, 12, 3, 3), (26, 33, 3, 2),
             (37, 34, 2, 2), (13, 16, 2, 2)]
asteroid = np.zeros((H, W), bool)
for (ax, ay, aw, ah) in ASTEROIDS:
    ys, xs = slice(max(0, ay - 3), ay + ah + 3), slice(max(0, ax - 3), ax + aw + 3)
    if ground[ys, xs].any():
        continue
    asteroid[ay:ay + ah, ax:ax + aw] = True
ground |= asteroid

# ---------------------------------------------------------------- events
LANDING = (9, 57)
BOX = (7, 56)
TRIANGLE = (22, 8)
DEOXYS_START = (22, 0)


def snap(p):
    return min(((x, y) for y in range(H) for x in range(W) if main[y, x]), key=lambda c: (math.hypot(c[0] - p[0], c[1] - p[1]), c))


ITEMS = {'STAR_PIECE': snap(POCKETS[0][-1]), 'MOON_STONE': snap(POCKETS[1][-1]), 'COMET_SHARD': snap(POCKETS[2][-1])}
RADIO = [snap(PATH[4]), snap(PATH[7]), snap(PATH[11])]    # coord-triggers: de radio van het Space Center
for (x, y) in list(ITEMS.values()) + [LANDING, BOX, TRIANGLE, (22, 9)]:
    assert main[y, x], ('event niet op de meteoriet', x, y)

KEEP = set()
for (x, y) in list(ITEMS.values()) + [LANDING, BOX, TRIANGLE] + RADIO:
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            KEEP.add((x + dx, y + dy))
for y in range(5, 13):
    for x in range(18, 27):
        KEEP.add((x, y))                                   # plein vrij houden


def reach(blocked):
    seen = {LANDING}
    q = deque([LANDING])
    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and main[ny, nx] and (nx, ny) not in blocked and (nx, ny) not in seen:
                seen.add((nx, ny)); q.append((nx, ny))
    return seen


def targets_ok(blocked):
    s = reach(blocked)
    need = list(ITEMS.values()) + RADIO + [(BOX[0] + 1, BOX[1]), (TRIANGLE[0], TRIANGLE[1] + 1)]
    return all(t in s for t in need)


blocked = {BOX, TRIANGLE}
assert targets_ok(blocked), 'events niet bereikbaar'


def interior(x, y, r=1):
    return all(0 <= x + dx < W and 0 <= y + dy < H and main[y + dy, x + dx] for dy in range(-r, r + 1) for dx in range(-r, r + 1))


decor = {}        # (x, y) -> (soort, dx, dy)
deco_blocked = set()


def try_place(kind, x, y, w, h, solid):
    cells = [(x + dx, y + dy) for dy in range(h) for dx in range(w)]
    if any(c in KEEP or c in decor or not interior(c[0], c[1]) for c in cells):
        return False
    if solid and not targets_ok(blocked | deco_blocked | set(cells)):
        return False
    # niet dicht op ander decor
    if any((cx + ex, cy + ey) in decor for (cx, cy) in cells for ex in (-1, 0, 1) for ey in (-1, 0, 1)):
        return False
    if solid:
        # de weg moet om een blok heen minstens 2 breed blijven: alle buren van het blok vrij en beloopbaar
        ring = [(cx + ex, cy + ey) for (cx, cy) in cells for ex in (-2, -1, 0, 1, 2) for ey in (-2, -1, 0, 1, 2)]
        if any(not main[ry, rx] for (rx, ry) in ring if 0 <= rx < W and 0 <= ry < H):
            return False
    for dy in range(h):
        for dx in range(w):
            decor[(x + dx, y + dy)] = (kind, dx, dy)
            if solid:
                deco_blocked.add((x + dx, y + dy))
    return True


cand = [(x, y) for y in range(H) for x in range(W) if main[y, x]]
rng.shuffle(cand)
counts = {'crater': 0, 'boulder': 0, 'rock': 0, 'rock2': 0}
want = {'crater': 7, 'boulder': 3, 'rock': 6, 'rock2': 6}
size = {'crater': (2, 2), 'boulder': (3, 2), 'rock': (1, 1), 'rock2': (1, 1)}
for kind in ('boulder', 'crater', 'rock', 'rock2'):
    for (x, y) in cand:
        if counts[kind] >= want[kind]:
            break
        w_, h_ = size[kind]
        if try_place(kind, x, y, w_, h_, kind != 'crater'):
            counts[kind] += 1

# kristallen aan de rand (grondcel met leegte ernaast), niet in de weg
crystals = {}
edge = [(x, y) for (x, y) in cand if not interior(x, y) and (x, y) not in KEEP and (x, y) not in decor]
for (x, y) in edge:
    if len(crystals) >= 16:
        break
    if any((x + ex, y + ey) in crystals for ex in range(-3, 4) for ey in range(-3, 4)):
        continue
    if not ground[y - 1, x]:
        continue                                           # niet op de bovenrand: daar steekt hij over de lucht
    if targets_ok(blocked | deco_blocked | {(x, y)}) and sum(int(main[y + ey, x + ex]) for ex in (-1, 0, 1) for ey in (-1, 0, 1)) >= 5:
        crystals[(x, y)] = len(crystals) % len(CRYSTALS)
        deco_blocked.add((x, y))

# vier kristallen rond het plein met de driehoek
for ang in (150, 210, 330, 30):
    best = None
    for (x, y) in cand:
        if interior(x, y) or (x, y) in decor or (x, y) == TRIANGLE or not ground[y - 1, x] or \
                any((x + ex, y + ey) in crystals for ex in (-1, 0, 1) for ey in (-1, 0, 1)):
            continue
        d = math.hypot(x - 22, y - 9)
        if not 2.5 <= d <= 4.5:
            continue
        a = math.degrees(math.atan2(y - 9, x - 22)) % 360
        score = abs((a - ang + 180) % 360 - 180)
        if best is None or score < best[0]:
            best = (score, x, y)
    if best and targets_ok(blocked | deco_blocked | {best[1:]}):
        crystals[best[1:]] = len(crystals) % len(CRYSTALS)
        deco_blocked.add(best[1:])

# radio: een lijn coord-triggers dwars over de weg (anders loop je er langs)
def span(p):
    best = None
    for dx, dy in ((1, 0), (0, 1)):
        cells = [p]
        for sgn in (1, -1):
            x, y = p[0] + dx * sgn, p[1] + dy * sgn
            while 0 <= x < W and 0 <= y < H and main[y, x]:
                cells.append((x, y))
                x, y = x + dx * sgn, y + dy * sgn
        if best is None or len(cells) < len(best):
            best = cells
    return sorted(best)


RADIO_CELLS = []
for p in RADIO:
    cells = [c for c in span(p) if c not in deco_blocked]
    assert (TRIANGLE[0], TRIANGLE[1] + 1) not in reach(blocked | deco_blocked | set(cells)), ('radio-lijn snijdt de weg niet door', p)
    RADIO_CELLS.append(cells)

# geen veld zonder encounters op de landingsplek en het plein
SAFE = set()
for (cx, cy, r) in [(LANDING[0], LANDING[1], 3.3), (22, 9, 3.4)]:
    for y in range(H):
        for x in range(W):
            if math.hypot(x - cx, y - cy) <= r:
                SAFE.add((x, y))

# ---------------------------------------------------------------- pixels
PW, PH = W * 16, H * 16
S = np.zeros((PH, PW), bool)
for y in range(H):
    for x in range(W):
        if ground[y, x]:
            S[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16] = True


def g(x, y):
    return 0 <= x < W and 0 <= y < H and ground[y, x]


for (ax, ay, aw, ah) in ASTEROIDS:                   # zwevende rotsen: ellips in plaats van rechthoek
    if not asteroid[ay, ax]:
        continue
    for py in range(ay * 16, (ay + ah) * 16):
        for px in range(ax * 16, (ax + aw) * 16):
            ex = (px + 0.5 - (ax + aw / 2) * 16) / (aw * 8)
            ey = (py + 0.5 - (ay + ah / 2) * 16) / (ah * 8)
            wob = 0.06 * math.sin(math.atan2(ey, ex) * 5 + ax)
            S[py, px] = ex * ex + ey * ey <= (0.98 + wob) ** 2

R_OUT, R_IN = 7, 4
for y in range(H):
    for x in range(W):
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            ox = x * 16 + (0 if dx < 0 else 15)
            oy = y * 16 + (0 if dy < 0 else 15)
            # u, v = pixels vanaf de hoek; buiten de cirkel om (R, R) ligt het stukje dat weg moet of erbij komt
            if asteroid[y, x]:
                continue
            if ground[y, x] and not g(x + dx, y) and not g(x, y + dy):
                for v in range(R_OUT):                     # buitenhoek afronden
                    for u in range(R_OUT):
                        if math.hypot(R_OUT - u - 0.5, R_OUT - v - 0.5) > R_OUT:
                            S[oy - dy * v, ox - dx * u] = False
            if not ground[y, x] and g(x + dx, y) and g(x, y + dy) and g(x + dx, y + dy) and not asteroid[y + dy, x + dx]:
                for v in range(R_IN):                      # binnenhoek opvullen (alleen beeld; de cel blijft dicht)
                    for u in range(R_IN):
                        if math.hypot(R_IN - u - 0.5, R_IN - v - 0.5) > R_IN:
                            S[oy - dy * v, ox - dx * u] = True

FACE_D = 13
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
img = np.zeros((PH, PW, 4), np.int32)
img[..., :3] = VOID
img[..., 3] = 255
face = np.full((PH, PW), -1, np.int32)                    # diepte onder de rand, -1 = geen wand
for px in range(PW):
    last = -999
    for py in range(PH):
        if S[py, px]:
            last = py
        else:
            d = py - last - 1
            if d < FACE_D:
                face[py, px] = d

HL1, HL2 = np.array([182, 166, 204]), np.array([128, 114, 152])
SIDE_L, SIDE_R = np.array([112, 100, 136]), np.array([40, 32, 58])
LIP = np.array([104, 92, 126])
OUTL = np.array([22, 16, 34])

for py in range(PH):
    cy, ty = py // 16, py % 16
    for px in range(PW):
        cx, tx = px // 16, px % 16
        if S[py, px]:
            var = 0
            if interior(cx, cy) and ((cx * 7 + cy * 13) % 5 == 0):
                var = 1
            col = FLOOR[var][ty, tx, :3]
            up1 = py == 0 or not S[py - 1, px]
            up2 = py > 1 and not S[py - 2, px]
            left = px == 0 or not S[py, px - 1]
            right = px == PW - 1 or not S[py, px + 1]
            down = py == PH - 1 or not S[py + 1, px]
            if up1:
                col = HL1
            elif up2:
                col = HL2
            elif down:
                col = LIP
            elif left:
                col = SIDE_L
            elif right:
                col = SIDE_R
            img[py, px, :3] = col
        elif face[py, px] >= 0:
            d = face[py, px]
            col = CLIFF[min(2 + d, 15), tx, :3].astype(float)
            fade = max(0.0, (d - 5) / (FACE_D - 5))            # 0 bovenaan, 1 onderaan
            if fade > BAYER[py % 4, px % 4] * 0.85 + 0.1:
                col = VOID
            else:
                col = col * (1 - 0.55 * fade)
            # zijkanten van de wand: donkere lijn
            lf = px > 0 and not S[py, px - 1] and face[py, px - 1] < 0
            rf = px < PW - 1 and not S[py, px + 1] and face[py, px + 1] < 0
            if (lf or rf) and fade < 0.9:
                col = OUTL
            if d == 0:
                col = OUTL
            img[py, px, :3] = np.array(col, np.int32)


# decor op de grond plakken
def paste(x, y, a):
    sub = img[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16]
    m = a[..., 3:4] > 0
    sub[...] = np.where(m, a, sub)


for (x, y), (kind, dx, dy) in decor.items():
    paste(x, y, DECOR[kind][dy][dx])
for (x, y), k in crystals.items():
    paste(x, y, CRYSTALS[k])


# ---------------------------------------------------------------- de ruimte: sterren, aarde, komeet
def cell_is_void(x, y):
    sl = (slice(y * 16, (y + 1) * 16), slice(x * 16, (x + 1) * 16))
    return not S[sl].any() and not (face[sl] >= 0).any()


def star_variant(v):
    r = random.Random(7000 + v)
    a = np.zeros((16, 16, 4), np.int32)
    if v == 0:
        return a
    for _ in range(r.choice((1, 1, 2, 2, 3))):
        x, y = r.randrange(1, 15), r.randrange(1, 15)
        c = r.choice([(200, 200, 224), (150, 168, 255), (255, 232, 176), (232, 232, 248), (120, 120, 150)])
        a[y, x] = (*c, 255)
    if v % 5 == 3:
        x, y = r.randrange(4, 12), r.randrange(4, 12)
        for (ex, ey) in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            a[y + ey, x + ex] = (255, 255, 255, 255) if (ex, ey) == (0, 0) else (150, 168, 232, 255)
    return a


STARS = [star_variant(v) for v in range(10)]
big = np.zeros((H, W), bool)                                # cellen met aarde/komeet: geen sterren


def earth(size=64):
    """De aarde zoals je hem vanaf de meteoriet ziet: oceaan, continenten, wolken, schaduwkant, dampkring."""
    r = random.Random(42)
    grid = [[r.random() for _ in range(9)] for _ in range(9)]

    def vnoise(u, v, f):
        u, v = u * f, v * f
        i, j = int(u) % 8, int(v) % 8
        fu, fv = u - int(u), v - int(v)
        fu, fv = fu * fu * (3 - 2 * fu), fv * fv * (3 - 2 * fv)
        a = grid[j][i] * (1 - fu) + grid[j][i + 1] * fu
        b = grid[j + 1][i] * (1 - fu) + grid[j + 1][i + 1] * fu
        return a * (1 - fv) + b * fv
    a = np.zeros((size, size, 4), np.int32)
    R = size / 2 - 3
    c = size / 2 - 0.5
    for y in range(size):
        for x in range(size):
            dx, dy = (x - c) / R, (y - c) / R
            d2 = dx * dx + dy * dy
            if d2 > 1.0:
                if d2 < 1.16 and (dx * -0.6 + dy * -0.8) > -0.2:
                    a[y, x] = (70, 120, 220, 255) if d2 < 1.07 else (40, 64, 140, 255)
                continue
            dz = math.sqrt(1 - d2)
            u, v = (math.atan2(dx, dz) + 2) * 0.9, (dy + 1.2) * 1.4
            land = vnoise(u, v, 2.0) * 0.65 + vnoise(u + 3, v + 1, 4.0) * 0.35
            cloud = vnoise(u + 5, v * 2.2 + 2, 3.0) * 0.6 + vnoise(u * 2 + 1, v + 4, 6.0) * 0.4
            if land > 0.58:
                base = np.array((72, 150, 64)) if land < 0.68 else np.array((150, 128, 72))
            else:
                base = np.array((32, 88, 200)) if land < 0.5 else np.array((48, 120, 216))
            if abs(dy) > 0.82:
                base = np.array((232, 240, 248))                       # poolkappen
            if cloud > 0.66:
                base = np.array((240, 244, 252))
            light = max(0.0, dx * -0.55 + dy * -0.45 + dz * 0.7)
            shade = min(1.0, 0.18 + light * 1.05)
            if shade < 0.32 and BAYER[y % 4, x % 4] > (shade - 0.15) * 4:
                col = np.array(VOID)
            else:
                col = base * shade
            a[y, x] = (*np.clip(col, 0, 255).astype(int), 255)
    return a


def comet(w=32, h=16):
    a = np.zeros((h, w, 4), np.int32)
    for i in range(26):
        x, y = 28 - i, 3 + i * 0.42
        t = i / 26
        for k, rad in enumerate((2.2 * (1 - t) + 0.6,)):
            for yy in range(h):
                for xx in range(w):
                    if math.hypot(xx - x, yy - y) <= rad:
                        bright = 1 - t
                        col = (255, 255, 255) if i < 2 else (int(120 + 135 * bright), int(160 + 95 * bright), 255)
                        if BAYER[yy % 4, xx % 4] < 0.25 + bright:
                            a[yy, xx] = (*col, 255)
    return a


def place_big(pic, pref, cw, ch):
    best = None
    for y in range(1, H - ch - 1):
        for x in range(1, W - cw - 1):
            if all(cell_is_void(x + i, y + j) for i in range(-1, cw + 1) for j in range(-1, ch + 1)):
                d = math.hypot(x - pref[0], y - pref[1])
                if best is None or d < best[0]:
                    best = (d, x, y)
    _, x, y = best
    sub = img[y * 16:(y + ch) * 16, x * 16:(x + cw) * 16]
    m = pic[..., 3:4] > 0
    sub[...] = np.where(m, pic, sub)
    big[y:y + ch, x:x + cw] = True
    return x, y


EARTH_AT = place_big(earth(), (14, 50), 4, 4)
COMET_AT = place_big(comet(), (33, 3), 2, 1)
for y in range(H):
    for x in range(W):
        if not big[y, x] and cell_is_void(x, y):
            h_ = (x * 2654435761 + y * 40503) & 0xFFFF
            v = 0 if h_ % 10 < 3 else 1 + h_ % 9
            sub = img[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16]
            m = STARS[v][..., 3:4] > 0
            sub[...] = np.where(m, STARS[v], sub)

# ---------------------------------------------------------------- zwevende Pokémon in de leegte (objecten)
FLOATERS = []
for (sp, pref) in [('MINIOR', (14, 54)), ('LUNATONE', (38, 40)), ('SOLROCK', (2, 30)), ('ELGYEM', (40, 19)),
                   ('MINIOR', (29, 8)), ('BEHEEYEM', (14, 21))]:
    best = None
    for y in range(2, H - 2):
        for x in range(2, W - 2):
            if big[y, x] or not cell_is_void(x, y) or any((x, y) == (f[1], f[2]) for f in FLOATERS):
                continue
            near = any(main[y + j, x + i] for i in (-2, -1, 0, 1, 2) for j in (-2, -1, 0, 1, 2))
            if not near:
                continue
            d = math.hypot(x - pref[0], y - pref[1])
            if best is None or d < best[0]:
                best = (d, x, y)
    FLOATERS.append((sp, best[1], best[2]))

# ---------------------------------------------------------------- metatiles
walk = set((x, y) for y in range(H) for x in range(W) if main[y, x]) - deco_blocked - {BOX, TRIANGLE}
names, metatiles, keymap = {}, [], {}
grid = [[0] * W for _ in range(H)]
for y in range(H):
    for x in range(W):
        a = img[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16].copy()
        beh = MB_CAVE if (x, y) in walk and (x, y) not in SAFE else MB_NORMAL
        key = (ns['to5'](a).astype(np.uint8).tobytes(), beh)
        if key not in keymap:
            keymap[key] = 0x200 + len(metatiles)
            metatiles.append(('m%d' % len(metatiles), Image.fromarray(a.astype(np.uint8), 'RGBA'), None, beh))
        grid[y][x] = keymap[key]
print('unieke metatiles:', len(metatiles))
res = emit(metatiles, OUT, 512, 6, 7)

# grens: zwarte leegte met sterren (vier cellen uit de linkerbovenhoek van de kaart)
border_ids = []
for (x, y) in [(0, 0), (1, 0), (0, 1), (1, 1)]:
    border_ids.append(grid[y][x])

os.makedirs(LAY, exist_ok=True)
open(LAY + '/map.bin', 'wb').write(b''.join(
    struct.pack('<H', grid[y][x] | ((0 if (x, y) in walk else 1) << 10) | (3 << 12)) for y in range(H) for x in range(W)))
open(LAY + '/border.bin', 'wb').write(struct.pack('<4H', *[b | (1 << 10) for b in border_ids]))

# gevechtsachtergrond: de grot van Hoenn in de donkere meteorietkleuren (BATTLE_ENVIRONMENT_SPACE)
lines = open('graphics/battle_environment/cave/palette.pal').read().split('\n')
out = lines[:3]
for l in lines[3:]:
    if not l.strip():
        continue
    r, g_, b = map(int, l.split())
    if (r, g_, b) == (0, 0, 0):
        out.append('0 0 0')
        continue
    t = min(1.0, (r * 0.30 + g_ * 0.55 + b * 0.15) / 230.0) ** 1.3
    c = np.array([6, 4, 16]) + (np.array([150, 134, 176]) - np.array([6, 4, 16])) * t
    out.append(' '.join(str(int(v) // 8 * 8) for v in c))
open('graphics/battle_environment/cave/space.pal', 'w').write('\n'.join(out) + '\n')

# ---------------------------------------------------------------- registratie
lj = open('data/layouts/layouts.json').read()
if '"LAYOUT_%s"' % CONST not in lj:
    i = lj.index('"id": "LAYOUT_BIRTH_ISLAND_EXTERIOR"'); j = lj.index('},', i) + 2
    lj = lj[:j] + '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_MeteorSpace",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (CONST, NAME, W, H, NAME, NAME) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)


def obj(local, gfx, x, y, mv, script, flag='0', elev=3):
    o = {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': mv, 'movement_range_x': 0,
         'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': '0',
         'script': script, 'flag': flag}
    if local:
        o = {'local_id': local, **o}
    return o


objs = [
    obj('LOCALID_METEOR_SPACE_TRIANGLE', 'OBJ_EVENT_GFX_DEOXYS_TRIANGLE_RED', TRIANGLE[0], TRIANGLE[1], 'MOVEMENT_TYPE_FACE_DOWN',
        NAME + '_EventScript_Triangle', 'FLAG_HIDE_BIRTH_ISLAND_DEOXYS_TRIANGLE'),
    obj('LOCALID_METEOR_SPACE_DEOXYS', 'OBJ_EVENT_GFX_DEOXYS', DEOXYS_START[0], DEOXYS_START[1], 'MOVEMENT_TYPE_FACE_DOWN',
        '0x0', 'FLAG_HIDE_DEOXYS', elev=0),
    obj('LOCALID_METEOR_SPACE_BOX', 'OBJ_EVENT_GFX_MOVING_BOX', BOX[0], BOX[1], 'MOVEMENT_TYPE_FACE_DOWN',
        NAME + '_EventScript_LandingBox'),
]
for item, (x, y) in ITEMS.items():
    o = obj(None, 'OBJ_EVENT_GFX_ITEM_BALL', x, y, 'MOVEMENT_TYPE_LOOK_AROUND', 'Common_EventScript_FindItem',
            'FLAG_ITEM_METEOR_SPACE_' + item)
    o['trainer_sight_or_berry_tree_id'] = 'ITEM_' + item
    objs.append(o)
for sp, x, y in FLOATERS:
    objs.append(obj(None, 'OBJ_EVENT_GFX_SPECIES(%s)' % sp, x, y, 'MOVEMENT_TYPE_WALK_IN_PLACE_DOWN',
                    NAME + '_EventScript_Floating' + sp.capitalize(), elev=0))

m = {
    'id': 'MAP_' + CONST, 'name': NAME, 'layout': 'LAYOUT_' + CONST, 'music': 'MUS_SEALED_CHAMBER',
    'region_map_section': 'MAPSEC_OUTER_SPACE', 'requires_flash': False, 'weather': 'WEATHER_NONE',
    'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': False, 'allow_running': True,
    'show_map_name': True, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
    'object_events': objs, 'warp_events': [],
    'coord_events': [{'type': 'trigger', 'x': x, 'y': y, 'elevation': 3, 'var': 'VAR_TEMP_1', 'var_value': str(i),
                      'script': NAME + '_EventScript_Radio%d' % (i + 1)} for i, cells in enumerate(RADIO_CELLS) for (x, y) in cells],
    'bg_events': [],
}
os.makedirs('data/maps/' + NAME, exist_ok=True)
open('data/maps/%s/map.json' % NAME, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

gj = open('data/maps/map_groups.json').read()
if '"%s"' % NAME not in gj:
    gj = gj.replace('    "FieryPath_HeatranLair"', '    "FieryPath_HeatranLair",\n    "%s"' % NAME, 1)
    open('data/maps/map_groups.json', 'w').write(gj)
es = open('data/event_scripts.s').read()
inc = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
if inc not in es:
    anchor = '\t.include "data/maps/FieryPath_HeatranLair/scripts.inc"\n'
    es = es.replace(anchor, anchor + inc, 1)
    open('data/event_scripts.s', 'w').write(es)

print('landing', LANDING, 'driehoek', TRIANGLE, 'aarde', EARTH_AT, 'komeet', COMET_AT)
print('decor', counts, 'kristallen', len(crystals), 'zwevers', FLOATERS)
print('beloopbaar', len(walk), 'cellen; weg tot de driehoek', len(reach(blocked | deco_blocked)))

if len(sys.argv) > 1:
    prev = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), 'RGBA')
    prev.save(sys.argv[1])
    for y in range(H):
        print(''.join('T' if (x, y) == TRIANGLE else 'B' if (x, y) == BOX else 'I' if (x, y) in ITEMS.values() else
                      'R' if any((x, y) in c for c in RADIO_CELLS) else 'c' if (x, y) in crystals else 'o' if (x, y) in decor else
                      '.' if (x, y) in walk else '#' if ground[y, x] else ' ' for x in range(W)))
