"""Project Grounded: genereert de tiles en paletten voor de route-transities (gevechtsovergangen per gebied).
Per transitie: graphics/battle_transitions/route_<naam>.png (tiles, index 0 = leeg) en route_<naam>.pal
(1 of meer paletten van 16 kleuren). De tilemaps bouwt de code in src/battle_transition.c zelf op.
Gebruik: python3 tools/grounded/route_transitions.py"""
import math, random
from PIL import Image

OUT = 'graphics/battle_transitions/'


def save(name, tiles, pals):
    tiles = [[0] * 64] + tiles
    cols = 16
    rows = (len(tiles) + cols - 1) // cols
    img = Image.new('P', (cols * 8, rows * 8))
    for i, tile in enumerate(tiles):
        ox, oy = (i % cols) * 8, (i // cols) * 8
        for p, v in enumerate(tile):
            img.putpixel((ox + p % 8, oy + p // 8), v)
    img.putpalette([v * 8 for c in pals[0] for v in c] + [0] * (768 - 48))
    img.save(OUT + 'route_%s.png' % name)
    with open(OUT + 'route_%s.pal' % name, 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n%d\n' % (16 * len(pals)))
        for pal in pals:
            for c in pal:
                fp.write('%d %d %d\n' % tuple(v * 8 for v in c))
    print(name, len(tiles), 'tiles')


def pad(pal):
    return pal + [(0, 0, 0)] * (16 - len(pal))


def tile(fn):
    return [fn(x, y) for y in range(8) for x in range(8)]


def cycle(base, n, amp=3):
    """n paletten waarin de kleuren 1.. licht golven (schittering)."""
    out = []
    for f in range(n):
        pal = [base[0]]
        for i, c in enumerate(base[1:], 1):
            d = int(round(amp * math.sin(2 * math.pi * f / n + i * 1.3)))
            pal.append(tuple(max(0, min(31, v + d)) for v in c))
        out.append(pad(pal))
    return out


# ------------------------------------------------------------------ zee: golf van rechts naar links
# 1-4 water, 5 schuimrand, 6 schuim, 7 schuim->water, 8 spatdruppels
SEA = [(0, 0, 0), (2, 6, 16), (4, 10, 22), (6, 15, 27), (12, 21, 30), (20, 27, 31), (27, 31, 31), (31, 31, 31)]
r = random.Random(1)
def water(seed):
    """GBA-zeewater: horizontale rimpels (licht boven, donker onder) op een middenblauw."""
    rr = random.Random(seed)
    t = [[2] * 8 for _ in range(8)]
    for y in (1, 5):
        x0 = rr.randint(0, 7)
        for d in range(rr.randint(3, 5)):
            t[y][(x0 + d) % 8] = 4
            t[(y + 1) % 8][(x0 + d + 1) % 8] = 3
    for y in (3, 7):
        x0 = rr.randint(0, 7)
        for d in range(rr.randint(2, 4)):
            t[y][(x0 + d) % 8] = 1
    return [t[y][x] for y in range(8) for x in range(8)]
wave = [water(10 + k) for k in range(4)]
rr = random.Random(20)
wave.append(tile(lambda x, y: 0 if x < rr.randint(0, 5) - (y % 3) else (7 if rr.random() < 0.5 else 6)))
wave.append(tile(lambda x, y: rr.choice((5, 6, 6, 7))))
wave.append(tile(lambda x, y: rr.choice((5, 6, 7)) if x < 3 + rr.randint(0, 3) else rr.choice((3, 4, 5))))
wave.append(tile(lambda x, y: (7 if rr.random() < 0.5 else 6) if rr.random() < 0.13 else 0))
save('wave', wave, cycle(SEA, 4, 2))

# ------------------------------------------------------------------ strand: golf uit de verte die over je heen spoelt
# 1-3 water (verre zee), 4-5 golfwand, 6 schuimkam (onder), 7 schuimkam (boven), 8 schuimspetters
beach = [water(30 + k) for k in range(3)]
for k in range(2):
    rr = random.Random(40 + k)
    beach.append(tile(lambda x, y: 1 + (1 if rr.random() < 0.35 else 0) + (1 if y > 5 and rr.random() < 0.4 else 0)))
rr = random.Random(50)
beach.append(tile(lambda x, y: rr.choice((6, 7, 7)) if y < 6 - (rr.random() < 0.3) else rr.choice((5, 6))))
beach.append(tile(lambda x, y: rr.choice((6, 7)) if y > 3 + int(2 * math.sin(x * 1.1)) else rr.choice((3, 4, 4))))
beach.append(tile(lambda x, y: 7 if rr.random() < 0.12 else 0))
save('beach', beach, cycle(SEA, 4, 2))

# ------------------------------------------------------------------ onder water: luchtbellen van beneden naar boven
# 1 klein belletje, 2 middel, 3 groot (2x2: 3-6), 7 sliert piepkleine belletjes
BUB = pad([(0, 0, 0), (10, 22, 30), (18, 28, 31), (31, 31, 31), (6, 14, 24)])
def ring(cx, cy, rad, x, y):
    d = math.hypot(x - cx, y - cy)
    if abs(d - rad) < 0.75:
        return 1 if (x - cx) + (y - cy) > 0 else 2
    if math.hypot(x - cx + rad * 0.4, y - cy + rad * 0.4) < max(0.8, rad * 0.25):
        return 3
    return 0
bub = [tile(lambda x, y: ring(3.5, 3.5, 1.8, x, y)), tile(lambda x, y: ring(3.5, 3.5, 3.0, x, y))]
for ty in range(2):
    for tx in range(2):
        bub.append(tile(lambda x, y, tx=tx, ty=ty: ring(7.5, 7.5, 6.6, x + tx * 8, y + ty * 8)))
rr = random.Random(60)
bub.append(tile(lambda x, y: (2 if rr.random() < 0.5 else 3) if (x % 3 == 1 and rr.random() < 0.18) else 0))
save('bubbles', bub, [BUB])

# ------------------------------------------------------------------ sneeuw: steeds meer vlokken tot het scherm dichtsneeuwt
# 1-3 losse vlokken, 4-5 dichte sneeuw, 6 volledig wit
SNOW = pad([(0, 0, 0), (31, 31, 31), (24, 27, 31), (18, 22, 28)])
def flakes(seed, n):
    rr = random.Random(seed)
    pts = {(rr.randint(0, 7), rr.randint(0, 7)): rr.choice((1, 2)) for _ in range(n)}
    def f(x, y):
        if (x, y) in pts:
            return pts[(x, y)]
        if any((x + dx, y + dy) in pts for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) and rr.random() < 0.25:
            return 3
        return 0
    return tile(f)
snow = [flakes(70, 1), flakes(71, 2), flakes(72, 3), flakes(73, 14), flakes(74, 26)]
rr = random.Random(75)
snow.append(tile(lambda x, y: 1 if rr.random() < 0.85 else 2))
save('snow', snow, [SNOW])

# ------------------------------------------------------------------ Route 113: as waait door het beeld
# 1-3 losse asdeeltjes (horizontaal uitgesmeerd), 4-5 dichte as, 6 helemaal grijs
ASH = pad([(0, 0, 0), (22, 22, 22), (15, 15, 16), (9, 9, 10), (27, 27, 26)])
def ashtile(seed, n):
    rr = random.Random(seed)
    t = [[0] * 8 for _ in range(8)]
    for _ in range(n):
        x, y, ln = rr.randint(0, 7), rr.randint(0, 7), rr.randint(1, 4)
        c = rr.choice((1, 2, 3))
        for d in range(ln):
            t[y][(x + d) % 8] = c if d < ln - 1 else 4
    return [t[y][x] for y in range(8) for x in range(8)]
ash = [ashtile(80, 1), ashtile(81, 2), ashtile(82, 3), ashtile(83, 12), ashtile(84, 22)]
rr = random.Random(85)
ash.append(tile(lambda x, y: rr.choice((1, 1, 2, 4))))
save('ash', ash, [ASH])

# ------------------------------------------------------------------ woestijn: zandstorm, lagen zand van onder naar boven
# 1-2 zandkam (bovenrand van een laag), 3-6 zandlagen (4 tinten), 7-8 vliegend zand
SAND = pad([(0, 0, 0), (30, 26, 17), (27, 22, 13), (24, 18, 10), (20, 15, 8), (31, 29, 22), (17, 12, 6)])
sand = []
for k in range(2):
    rr = random.Random(90 + k)
    sand.append(tile(lambda x, y, k=k: 0 if y < 3 + int(2 * math.sin((x + 4 * k) * 0.8)) else (5 if y < 5 + int(2 * math.sin((x + 4 * k) * 0.8)) else 1)))
for k, c in enumerate((1, 2, 3, 4)):
    rr = random.Random(95 + k)
    sand.append(tile(lambda x, y, c=c: c if rr.random() > 0.12 else rr.choice((5, 6))))
for k in range(2):
    rr = random.Random(99 + k)
    sand.append(tile(lambda x, y: rr.choice((1, 2, 5)) if (y in (2, 5) and rr.random() < 0.5) else 0))
save('sand', sand, [SAND])

# ------------------------------------------------------------------ Cycling Road: POV op de fiets over de weg
# volledig beeld (240x160): lucht, zee, weg in perspectief met bewegende strepen (kleurcyclus), stuur onderaan
# kleuren: 1-4 asfalt-banden, 5-8 middenstreep-banden, 9-12 rand-banden, 13 lucht, 14 zee, 15 stuur
HOR = 52
img = [[13] * 240 for _ in range(160)]
for y in range(HOR, 160):
    d = y - HOR + 1
    z = 900.0 / d                       # diepte
    band = int(z / 9) % 4
    half = 5 + d * 1.0                 # halve wegbreedte
    for x in range(240):
        dx = abs(x - 120)
        if dx > half + 3 + d * 0.08:
            img[y][x] = 14
        elif dx > half:
            img[y][x] = 9 + band
        elif dx < 1 + d * 0.04:
            img[y][x] = 5 + band
        else:
            img[y][x] = 1 + band
# stuur en handen onderaan
for y in range(128, 160):
    for x in range(240):
        yy = y - 128
        bar = abs(yy - 16 - ((x - 120) / 60.0) ** 2 * 5) < 4.5 and 14 < x < 226
        stem = abs(x - 120) < 10 and yy > 12
        grip = (abs(x - 30) < 18 or abs(x - 210) < 18) and 8 < yy < 32
        if bar or stem or grip:
            img[y][x] = 15
tiles, index, tm = [], {}, []
for ty in range(20):
    for tx in range(30):
        t = tuple(img[ty * 8 + py][tx * 8 + px] for py in range(8) for px in range(8))
        if t not in index:
            index[t] = len(tiles) + 1; tiles.append(list(t))
        tm.append(index[t])
pals = []
ROAD = [(9, 9, 10), (12, 12, 13)]
for f in range(4):
    pal = [(0, 0, 0)]
    for b in range(4):
        pal.append(ROAD[(b + f) % 4 < 2])
    for b in range(4):
        pal.append((31, 31, 31) if (b + f) % 4 < 2 else ROAD[1])
    for b in range(4):
        pal.append((31, 6, 6) if (b + f) % 4 < 2 else (31, 31, 31))
    pal += [(14, 22, 31), (4, 12, 24), (5, 4, 4)]
    pals.append(pal)
save('cycling', tiles, pals)
import struct
open(OUT + 'route_cycling.bin', 'wb').write(struct.pack('<%dH' % len(tm), *tm))
