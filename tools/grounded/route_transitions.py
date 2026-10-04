"""Project Grounded: genereert de tiles en paletten voor de route-transities (gevechtsovergangen per gebied).
Per transitie: graphics/battle_transitions/route_<naam>.png (tiles, index 0 = leeg) en route_<naam>.pal
(1 of meer paletten van 16 kleuren). De tilemaps bouwt de code in src/battle_transition.c zelf op.
Gebruik: python3 tools/grounded/route_transitions.py"""
import math, random, struct
from PIL import Image, ImageDraw

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


def blocks(fn, w, h):
    """Tekent een vorm van w x h tiles (fn(x, y) in pixels) en geeft de tiles rij voor rij terug."""
    out = []
    for ty in range(h):
        for tx in range(w):
            out.append(tile(lambda x, y, tx=tx, ty=ty: fn(x + tx * 8, y + ty * 8)))
    return out

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

# ------------------------------------------------------------------ Mt. Pyre: de ongeidentificeerde ghosts van Lavender Town
# de echte ghost-sprite uit Pokemon Red/Blue (pret/pokered, gfx/battle/ghost.png, 48x48, 4 grijstinten), pixel voor pixel:
# wit buiten de ghost wordt doorzichtig, wit binnenin (ogen, grijns) blijft wit, grijs wordt een paarse aura. tiles 1-36
PYRE = pad([(0, 0, 0), (1, 1, 2), (13, 5, 19), (22, 10, 28), (31, 31, 31)])
src = Image.open('graphics/grounded/ghost_pokered.png').convert('L')
GW, GH = src.size
outside, todo = set(), [(x, y) for x in range(GW) for y in (0, GH - 1)] + [(x, y) for y in range(GH) for x in (0, GW - 1)]
while todo:
    x, y = todo.pop()
    if (x, y) in outside or not (0 <= x < GW and 0 <= y < GH) or src.getpixel((x, y)) < 200:
        continue
    outside.add((x, y))
    todo += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
def ghost(x, y):
    v = src.getpixel((x, y))
    if v >= 200:
        return 0 if (x, y) in outside else 4
    return 1 if v < 40 else (2 if v < 128 else 3)
pyre = blocks(ghost, GW // 8, GH // 8)
save('pyre', pyre, [PYRE])

# ------------------------------------------------------------------ Sky Pillar: razendsnel de lucht in
# 1-2 snelheidsstrepen (verticaal), 3-6 wolk (2x2), 7 kleine wolk
SKY = pad([(0, 0, 0), (31, 31, 31), (24, 28, 31), (18, 24, 31), (12, 19, 30)])
sky = []
for k in range(2):
    rr = random.Random(120 + k)
    cols = rr.sample(range(8), 2)
    sky.append(tile(lambda x, y, cols=cols: (1 if y % 8 < 6 else 2) if x in cols else 0))
def cloud(x, y):
    d = min(math.hypot(x - 5, y - 9) / 5, math.hypot(x - 10, y - 7) / 6, math.hypot(x - 8, y - 11) / 6.5)
    if d < 0.7: return 1
    if d < 1.0: return 2
    return 0
for ty in range(2):
    for tx in range(2):
        sky.append(tile(lambda x, y, tx=tx, ty=ty: cloud(x + tx * 8, y + ty * 8)))
sky.append(tile(lambda x, y: 1 if math.hypot(x - 3.5, y - 4) < 2.5 else (2 if math.hypot(x - 3.5, y - 4) < 3.4 else 0)))
save('sky', sky, [SKY])

# ------------------------------------------------------------------ New Mauville: kortsluiting
# 1 zwart, 2 witte horizontale lijn (beeld gaat uit), 3 witte stip, 4-6 vonkbogen, 7 ruis
SHORT = pad([(0, 0, 0), (0, 0, 0), (31, 31, 31), (31, 31, 12), (12, 24, 31), (20, 20, 22)])
short = [tile(lambda x, y: 1), tile(lambda x, y: 2 if y in (3, 4) else 1), tile(lambda x, y: 2 if math.hypot(x - 3.5, y - 3.5) < 1.6 else 1)]
for k in range(3):
    rr = random.Random(130 + k)
    pts, y0 = {}, rr.randint(1, 6)
    for x in range(8):
        y0 = max(0, min(7, y0 + rr.randint(-2, 2)))
        pts[(x, y0)] = 2; pts[(x, max(0, y0 - 1))] = 3
        if rr.random() < 0.4: pts[(x, min(7, y0 + 1))] = 4
    short.append(tile(lambda x, y, pts=pts: pts.get((x, y), 0)))
rr = random.Random(135)
short.append(tile(lambda x, y: rr.choice((0, 0, 0, 5, 2, 1))))
# MissingNo uit graphics/grounded/missingno.png (Jordi; 60x60 cellen van 6,67 px). MissingNo beslaat cellen x 18-40,
# y 2-57 (23x56), L-vormig: linksboven (x < 25, y < 26) leeg. Op 2 px per cel = 46x112 in een vak van 6x14 tiles.
# Kleuren: lila, lichtroze (het wit binnen de vorm), perzik, zwart; tiles 8-91
SHORT[6:9] = [(16, 14, 19), (31, 29, 31), (30, 22, 17)]
mn = Image.open('graphics/grounded/missingno.png').convert('RGB')
CELL = mn.size[0] / 60.0
MNCOL = {(128, 112, 152): 6, (240, 176, 136): 8, (24, 16, 16): 1, (255, 255, 255): 7}
def mncell(i, j):
    if i < 7 and j < 24:
        return 0
    return MNCOL.get(mn.getpixel((int((18 + i + 0.5) * CELL), int((2 + j + 0.5) * CELL))), 7)
def missingno(x, y):
    i, j = (x - 1) // 2, y // 2
    if not (0 <= i < 23 and 0 <= j < 56):
        return 0
    return mncell(i, j)
short += blocks(missingno, 6, 14)
save('short', short, [SHORT])

# ------------------------------------------------------------------ Artisan Cave: het beeld wordt volgeschilderd
# per kleur (rood, geel, blauw, groen, paars) 2 tiles: penseelstreek (met haarstreepjes) en spetters
PAINTS = [((31, 6, 6), (22, 2, 2)), ((31, 27, 4), (26, 18, 0)), ((6, 14, 31), (2, 6, 22)), ((6, 26, 8), (2, 16, 4)), ((22, 8, 28), (13, 3, 18))]
pal = [(0, 0, 0)]
for a, b in PAINTS:
    pal += [a, b]
PAINT = pad(pal)
paint = []
for k, _ in enumerate(PAINTS):
    lo, hi = 1 + 2 * k, 2 + 2 * k
    rr = random.Random(140 + k)
    paint.append(tile(lambda x, y: hi if (y + rr.randint(0, 1)) % 3 == 0 else lo))
    paint.append(tile(lambda x, y: (lo if rr.random() < 0.7 else hi) if math.hypot(x - 3.5 + rr.random(), y - 3.5) < 2.2 + rr.random() * 1.5 else 0))
save('paint', paint, [PAINT])

# ------------------------------------------------------------------ Safari Zone: van bovenaf tussen de bomen door
# 1 bosgrond (donker), 2-10 boom (3x3), 11-14 struik (2x2), 15 gras
SAF = pad([(0, 0, 0), (3, 9, 3), (6, 15, 5), (10, 21, 7), (16, 26, 10), (8, 6, 3), (2, 5, 2)])
rr = random.Random(150)
saf = [tile(lambda x, y: 6 if rr.random() < 0.7 else 1)]
def tree(x, y):
    d = math.hypot(x - 11.5, y - 11.5)
    n = 0.8 * math.sin(math.atan2(y - 11.5, x - 11.5) * 7)
    if d < 10.5 + n:
        sh = (x - 11.5) + (y - 11.5)
        return 4 if sh < -9 else (3 if sh < 0 else (2 if d < 9 + n else 1))
    return 0
saf += [[6 if v == 0 else v for v in t] for t in blocks(tree, 3, 3)]
def bush(x, y):
    d = math.hypot(x - 7.5, y - 7.5)
    return (3 if x + y < 12 else 2) if d < 6.5 else (1 if d < 7.3 else 0)
saf += [[6 if v == 0 else v for v in t] for t in blocks(bush, 2, 2)]
saf.append(tile(lambda x, y: 3 if (x % 3 == 0 and y % 4 < 2) else 6))
save('safari', saf, [SAF])

# ------------------------------------------------------------------ Meteor Falls: zijwaarts tussen stalactieten en stalagmieten
# stalactiet (4 breed, 7 hoog, punt naar beneden): 1-28; stalagmiet (punt naar boven): 29-56; rotsplafond/-bodem 57
MET = pad([(0, 0, 0), (5, 4, 8), (10, 9, 14), (16, 15, 20), (23, 22, 27), (3, 3, 5), (29, 28, 31)])
def spike(up, seed):
    rr = random.Random(seed)
    knobs = [(rr.uniform(4, 28), rr.uniform(0, 40), rr.uniform(3, 6)) for _ in range(10)]
    def f(x, y):
        yy = 55 - y if up else y
        half = 15.5 * (1 - yy / 56.0) ** 0.9 + 1.5 * math.sin(yy * 0.5)
        dx = x - 15.5
        if abs(dx) > half:
            return 0
        if abs(dx) > half - 1.2:
            return 5
        h = -dx / max(half, 1) * 1.6                                   # licht van links
        for kx, ky, kr in knobs:
            dd = math.hypot(x - kx, yy - ky) / kr
            if dd < 1:
                h += (1 - dd) * 0.9
        if not up and yy > 46 and abs(dx) < 2:
            return 6                                                   # glinsterende druppelpunt
        return max(1, min(4, 2 + int(round(h))))
    return f
met = blocks(spike(False, 161), 4, 7) + blocks(spike(True, 162), 4, 7)
rr = random.Random(160)
met.append(tile(lambda x, y: rr.choice((5, 1, 1, 2))))
save('meteor', met, [MET])

# ------------------------------------------------------------------ Jagged Pass: POV op de fiets bergaf over een rotsig pad
# volledig beeld zoals de Cycling Road. Rotsen liggen op en naast het pad op vaste diepte-afstanden; elke rots hoort bij
# een fase (0-3). Per frame is maar een fase zichtbaar, zodat de rotsen op je af lijken te komen.
# kleuren: 1-4 padbanden, 5-12 rotsen (fase 0-3, licht/donker), 13 aslucht, 14 rotswand opzij, 15 stuur
HORJ = 46
img = [[13] * 240 for _ in range(160)]
def depth(y):
    return 900.0 / (y - HORJ + 1)
for y in range(HORJ, 160):
    d = y - HORJ + 1
    band = int(depth(y) / 9) % 4
    half = 10 + d * 1.15 + 6 * math.sin(d * 0.08)
    for x in range(240):
        dx = abs(x - 120 + 10 * math.sin(d * 0.05))
        img[y][x] = 14 if dx > half else 1 + band
# rotsen: banen (wereld-x) en diepte z = (n + fase/4) * D
D = 36.0                                   # = 4 padbanden van 9, zodat rotsen even snel gaan als het pad
rr = random.Random(180)
lanes = [-0.75, -0.35, 0.0, 0.35, 0.75]
rocks = []
for n in range(0, 12):
    for ph in range(4):
        if n == 0 and ph == 0:
            continue
        for lane in rr.sample(lanes, 2):
            rocks.append(((n + ph / 4.0) * D, lane + rr.uniform(-0.15, 0.15), ph, rr.uniform(0.7, 1.3)))
rocks.sort(key=lambda r: -r[0])           # ver eerst, dichtbij overschrijft
for z, lane, ph, size in rocks:
    y0 = HORJ - 1 + 900.0 / z               # schermrij van de voet van de rots
    if y0 >= 160 or y0 < HORJ + 1:
        continue
    d = y0 - HORJ + 1
    half = 10 + d * 1.15
    cx = 120 + lane * half
    rad = max(1.5, d * 0.34 * size)
    for y in range(int(y0 - rad * 1.4), int(y0) + 1):
        for x in range(int(cx - rad - 1), int(cx + rad + 2)):
            if 0 <= x < 240 and HORJ <= y < 160:
                if ((x - cx) / rad) ** 2 + ((y - y0 + rad * 0.55) / (rad * 0.9)) ** 2 <= 1:
                    lit = (x - cx) + (y - y0 + rad) < 0
                    img[y][x] = 5 + ph * 2 + (0 if lit else 1)
# stuur
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
GROUND = [(18, 12, 8), (20, 14, 10)]
ROCKL, ROCKD = (24, 20, 18), (11, 9, 9)
pals = []
for f in range(4):
    pal = [(0, 0, 0)]
    for b in range(4):
        pal.append(GROUND[(b + f) % 4 < 2])
    for ph in range(4):
        vis = (ph + f) % 4 == 0
        pal += [ROCKL, ROCKD] if vis else [(19, 13, 9), (19, 13, 9)]
    pal += [(16, 16, 17), (9, 6, 6), (5, 4, 4)]
    pals.append(pal)
save('jagged', tiles, pals)
open(OUT + 'route_jagged.bin', 'wb').write(struct.pack('<%dH' % len(tm), *tm))

# ------------------------------------------------------------------ regenwoud (Route 119, Fortree, Route 120)
# grote bladeren (4x4): 1-16 en 17-32 (gespiegeld), lianen 33-34, regenstrepen 35-36
RAIN = pad([(0, 0, 0), (2, 9, 4), (4, 15, 6), (8, 22, 9), (14, 27, 12), (20, 26, 31), (4, 7, 3)])
def leaf(flip):
    def f(x, y):
        if flip:
            x = 31 - x
        u, v = (x + y) / 2.0 - 16, (x - y) / 2.0     # langs en dwars op de bladnerf (diagonaal)
        if abs(u) > 15:
            return 0
        width = 7.5 * math.cos(u / 15 * math.pi / 2) ** 0.8
        if abs(v) <= width:
            if abs(v) < 0.6:
                return 4
            return 3 if v < 0 else (2 if abs(v) < width - 1.2 else 1)
        return 0
    return f
rainf = blocks(leaf(False), 4, 4) + blocks(leaf(True), 4, 4)
rainf.append(tile(lambda x, y: (2 if (y + x // 2) % 6 < 4 else 6) if 3 <= x <= 4 else 0))
rainf.append(tile(lambda x, y: (3 if y % 5 < 3 else 6) if 2 <= x <= 3 or (5 <= x <= 6 and y % 7 < 3) else 0))
rainf.append(tile(lambda x, y: 5 if (x - y // 3) % 8 == 0 and y % 8 < 5 else 0))
rainf.append(tile(lambda x, y: 5 if (x - y // 3 + 4) % 8 == 0 and (y + 3) % 8 < 4 else 0))
save('rainforest', rainf, [RAIN])

# ================================================================== unieke transities (soort / trainer / plek)
from PIL import ImageFont
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def text_mask(text, size):
    """Tekst als harde 1-bit pixels (geen anti-aliasing)."""
    font = ImageFont.truetype(BOLD, size)
    x0, y0, x1, y1 = font.getbbox(text)
    m = Image.new('1', (x1 - x0 + 2, y1 - y0 + 2), 0)
    ImageDraw.Draw(m).text((1 - x0, 1 - y0), text, font=font, fill=1)
    return m

def mask_tiles(w, h, fn):
    return blocks(fn, w, h)

# ------------------------------------------------------------------ Pikachu: geel scherm, twee rode wangen, "Pika!"
# 1 geel, 2-37 wang (6x6), 38.. tekst "Pika!" (op geel)
PIKA = pad([(0, 0, 0), (31, 27, 4), (30, 6, 4), (19, 2, 2), (2, 2, 2), (31, 31, 31)])
pika = [tile(lambda x, y: 1)]
def cheek(x, y):
    d = math.hypot(x - 23.5, y - 23.5)
    if d < 19:
        return 5 if math.hypot(x - 16, y - 15) < 4 else 2
    return 3 if d < 21.5 else 1
pika += blocks(cheek, 6, 6)
tm = text_mask('Pika!', 44)
TW, TH = (tm.size[0] + 7) // 8, (tm.size[1] + 7) // 8
pika += blocks(lambda x, y: 4 if x < tm.size[0] and y < tm.size[1] and tm.getpixel((x, y)) else 1, TW, TH)
save('pikachu', pika, [PIKA])
print('  Pika!-tekst', TW, 'x', TH, 'tiles')

# ------------------------------------------------------------------ Magikarp: het spartelende party-icoon, 3x vergroot (2 frames, 12x12)
# plus de front-sprite (64x128, 2 frames) als OBJ-sprite die in grote aantallen over elkaar heen spartelt
ic = Image.open('graphics/pokemon/magikarp/icon.png')
icpal = ic.getpalette()[:48]
KARP = [tuple(icpal[i * 3 + k] // 8 for k in range(3)) for i in range(16)]
karp = []
for fr in range(2):
    karp += blocks(lambda x, y, fr=fr: ic.getpixel((x // 3, y // 3 + fr * 32)), 12, 12)
save('magikarp', karp, [KARP])
mf = Image.open('graphics/pokemon/magikarp/anim_front.png')
mpal = [tuple(int(v) // 8 for v in l.split()) for l in open('graphics/pokemon/magikarp/normal.pal').read().split('\n')[3:19]]
mf.putpalette([v * 8 for c in mpal for v in c] + [0] * (768 - 48))
mf.save(OUT + 'sprite_magikarp.png')
with open(OUT + 'sprite_magikarp.pal', 'w', newline='\r\n') as fp:
    fp.write('JASC-PAL\n0100\n16\n')
    for c in mpal:
        fp.write('%d %d %d\n' % tuple(v * 8 for v in c))

# ------------------------------------------------------------------ Gabby & Ty: camerazoeker met REC en rode stip
# 1-4 hoeken (2x2 elk: LB, RB, LO, RO -> 1-16), 17 lijn horizontaal, 18 lijn verticaal, 19-22 rode stip (2x2),
# 23.. "REC", daarna batterij (3x2)
CAM = pad([(0, 0, 0), (31, 31, 31), (31, 4, 4), (8, 8, 8), (16, 31, 16)])
def corner(fx, fy):
    def f(x, y):
        xx, yy = (15 - x if fx else x), (15 - y if fy else y)
        if (xx < 3 and yy < 16) or (yy < 3 and xx < 16):
            return 1
        if (xx < 4 and yy < 16) or (yy < 4 and xx < 16):
            return 3
        return 0
    return f
cam = []
for fx, fy in ((0, 0), (1, 0), (0, 1), (1, 1)):
    cam += blocks(corner(fx, fy), 2, 2)
cam.append(tile(lambda x, y: 1 if y < 3 else (3 if y == 3 else 0)))
cam.append(tile(lambda x, y: 1 if x < 3 else (3 if x == 3 else 0)))
cam += blocks(lambda x, y: 2 if math.hypot(x - 7.5, y - 7.5) < 6 else (3 if math.hypot(x - 7.5, y - 7.5) < 7.2 else 0), 2, 2)
rec = text_mask('REC', 14)
RW, RH = (rec.size[0] + 7) // 8, (rec.size[1] + 7) // 8
def recf(x, y):
    if x < rec.size[0] and y < rec.size[1] and rec.getpixel((x, y)):
        return 1
    if any(0 <= x - dx < rec.size[0] and 0 <= y - dy < rec.size[1] and rec.getpixel((x - dx, y - dy)) for dx, dy in ((1, 0), (0, 1), (1, 1))):
        return 3
    return 0
cam += blocks(recf, RW, RH)
def battery(x, y):
    if 2 <= y <= 13 and 1 <= x <= 20:
        if y in (2, 13) or x in (1, 20):
            return 1
        return 4 if 3 <= x <= 18 and 4 <= y <= 11 and x < 15 else 0
    if 21 <= x <= 22 and 5 <= y <= 10:
        return 1
    return 0
cam += blocks(battery, 3, 2)
save('camera', cam, [CAM])
print('  REC', RW, 'x', RH)

# ------------------------------------------------------------------ Koffing/Weezing: het schedel-en-botten-teken op paars
# volledige afbeelding voor PatternWeave (zoals Aqua/Magma): palet 0-7 zwart, 8-15 paars/bot
KOFPAL = [(0, 0, 0)] * 8 + [(124, 108, 168), (72, 56, 110), (96, 82, 140), (150, 136, 190), (200, 192, 172), (232, 226, 210), (250, 248, 240), (40, 30, 64)]
W2, H2 = 240, 160
kimg = Image.new('P', (W2, H2), 8)
kd = ImageDraw.Draw(kimg)
for r in range(150, 0, -6):                                   # zachte paarse gloed naar het midden
    kd.ellipse((120 - r * 1.5, 80 - r, 120 + r * 1.5, 80 + r), fill=8 if r > 100 else (10 if r > 60 else 11))
cx, cy = 120, 84
def bone(x0, y0, x1, y1, w, fill, knob):
    kd.line((x0, y0, x1, y1), fill=fill, width=w)
    for (x, y) in ((x0, y0), (x1, y1)):
        dx, dy = (x1 - x0), (y1 - y0)
        n = math.hypot(dx, dy); px, py = -dy / n * knob * 0.7, dx / n * knob * 0.7
        for s in (-1, 1):
            kd.ellipse((x + s * px - knob, y + s * py - knob, x + s * px + knob, y + s * py + knob), fill=fill)
for fill, grow in ((15, 3), (12, 0)):                         # donkere rand, dan bot
    bone(cx - 44, cy + 2, cx + 44, cy + 58, 16 + grow * 2, fill, 9 + grow)
    bone(cx + 44, cy + 2, cx - 44, cy + 58, 16 + grow * 2, fill, 9 + grow)
kd.ellipse((cx - 30 - 3, cy - 64 - 3, cx + 30 + 3, cy - 16 + 3), fill=15)   # ring (schedel) bovenop
kd.ellipse((cx - 30, cy - 64, cx + 30, cy - 16), fill=13)
kd.ellipse((cx - 14 - 3, cy - 50 - 3, cx + 14 + 3, cy - 30 + 3), fill=15)
kd.ellipse((cx - 14, cy - 50, cx + 14, cy - 30), fill=10)
kd.arc((cx - 26, cy - 60, cx + 26, cy - 20), 200, 300, fill=14, width=3)   # glans
ktiles, kidx, ktm = [tuple([0] * 64)], {tuple([0] * 64): 0}, [0] * 1024
for ty in range(20):
    for tx in range(30):
        t = tuple(kimg.getpixel((tx * 8 + px, ty * 8 + py)) for py in range(8) for px in range(8))
        if t not in kidx:
            kidx[t] = len(ktiles); ktiles.append(t)
        ktm[ty * 32 + tx] = kidx[t] | (15 << 12)
rows = (len(ktiles) + 15) // 16
out = Image.new('P', (128, rows * 8))
for n, t in enumerate(ktiles):
    for p_, v in enumerate(t):
        out.putpixel(((n % 16) * 8 + p_ % 8, (n // 16) * 8 + p_ // 8), v)
out.putpalette([v for c in KOFPAL for v in c] + [0] * (768 - 48))
out.save(OUT + 'route_koffing.png')
open(OUT + 'route_koffing.bin', 'wb').write(struct.pack('<1024H', *ktm))
with open(OUT + 'route_koffing.pal', 'w', newline='\r\n') as fp:
    fp.write('JASC-PAL\n0100\n16\n')
    for c in KOFPAL:
        fp.write('%d %d %d\n' % c)
print('koffing', len(ktiles), 'tiles')

# ------------------------------------------------------------------ sprites (64x64, 4bpp) voor draaien/schalen
def save_sprite(name, img64, pal):
    img64.putpalette([v * 8 for c in pal for v in c] + [0] * (768 - 48))
    img64.save(OUT + 'sprite_%s.png' % name)
    with open(OUT + 'sprite_%s.pal' % name, 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n')
        for c in pal:
            fp.write('%d %d %d\n' % tuple(v * 8 for v in c))

# Psyduck: groot wit vraagteken met zwarte rand
q = text_mask('?', 60)
QPAL = pad([(0, 0, 0), (31, 31, 31), (2, 2, 2), (28, 24, 6)])
qi = Image.new('P', (64, 64), 0)
ox, oy = (64 - q.size[0]) // 2, (64 - q.size[1]) // 2
for y in range(64):
    for x in range(64):
        inside = lambda xx, yy: 0 <= xx - ox < q.size[0] and 0 <= yy - oy < q.size[1] and q.getpixel((xx - ox, yy - oy))
        if inside(x, y):
            qi.putpixel((x, y), 1)
        elif any(inside(x + dx, y + dy) for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)):
            qi.putpixel((x, y), 2)
save_sprite('question', qi, QPAL)

# Poochyena (Joey): de eerste frame van de front-sprite
po = Image.open('graphics/pokemon/poochyena/anim_front.png')
ppal = [tuple(int(v) // 8 for v in l.split()) for l in open('graphics/pokemon/poochyena/normal.pal').read().split('\n')[3:19]]
save_sprite('poochyena', po.crop((0, 0, 64, 64)), ppal)

# strandbal (Slateport): zes gekleurde parten, glans
BPAL = pad([(0, 0, 0), (31, 31, 31), (30, 4, 4), (4, 12, 30), (31, 26, 2), (4, 4, 6), (22, 22, 24)])
bi = Image.new('P', (64, 64), 0)
for y in range(64):
    for x in range(64):
        d = math.hypot(x - 31.5, y - 31.5)
        if d < 29:
            a = (math.degrees(math.atan2(y - 31.5, x - 31.5)) + 360) % 360
            seg = int(a // 60)
            c = (2, 1, 3, 1, 4, 1)[seg]
            if math.hypot(x - 22, y - 20) < 5:
                c = 1
            elif d > 26:
                c = 6 if c == 1 else c
            bi.putpixel((x, y), c)
        elif d < 31:
            bi.putpixel((x, y), 5)
save_sprite('beachball', bi, BPAL)

# strand met parasols (onderkant van het beeld, 30x6 tiles) voor de strandbal-transitie
# 1 zand, 2 zand donker, 3 parasol rood, 4 parasol wit, 5 paal, 6 schaduw, 7 zee, 8 schuim
BEACH = pad([(0, 0, 0), (30, 26, 17), (26, 21, 12), (30, 6, 6), (31, 31, 31), (14, 12, 10), (22, 18, 11), (8, 18, 30), (24, 30, 31)])
bimg = [[1] * 240 for _ in range(48)]
rr = random.Random(190)
for y in range(48):
    for x in range(240):
        if y < 6:
            bimg[y][x] = 7 if y < 4 else 8
        elif rr.random() < 0.08:
            bimg[y][x] = 2
for px_ in (30, 110, 190):
    for y in range(48):
        for x in range(240):
            dx, dy = x - px_, y - 20
            if dy <= 0 and dx * dx / 24.0 ** 2 + dy * dy / 14.0 ** 2 <= 1:
                bimg[y][x] = 3 if int((math.degrees(math.atan2(-dy, dx)) // 30)) % 2 == 0 else 4
            elif abs(dx) <= 1 and 0 < dy < 26:
                bimg[y][x] = 5
            elif 20 < dy < 26 and abs(dx - 8) < 18 and bimg[y][x] in (1, 2):
                bimg[y][x] = 6
btiles, bidx, btm = [], {}, []
for ty in range(6):
    for tx in range(30):
        t = tuple(bimg[ty * 8 + py][tx * 8 + px] for py in range(8) for px in range(8))
        if t not in bidx:
            bidx[t] = len(btiles) + 1; btiles.append(list(t))
        btm.append(bidx[t])
save('beachball', btiles, [BEACH])
open(OUT + 'route_beachball.bin', 'wb').write(struct.pack('<%dH' % len(btm), *btm))

# ------------------------------------------------------------------ Magikarp-collage: het hele scherm vol Magikarp, geen pixel achtergrond
# telkens een Magikarp (front-sprite, willekeurig frame/gespiegeld, soms 1,5x) over een nog lege plek, tot alles bedekt is
rr = random.Random(200)
frames = [mf.crop((0, 0, 64, 64)), mf.crop((0, 64, 64, 128))]
canvas = [[0] * 240 for _ in range(160)]
placed = 0
while True:
    empty = [(x, y) for y in range(0, 160, 3) for x in range(0, 240, 3) if canvas[y][x] == 0]
    if not empty:
        empty = [(x, y) for y in range(160) for x in range(240) if canvas[y][x] == 0]
        if not empty:
            break
    ex, ey = rr.choice(empty)
    fr = rr.choice(frames)
    if rr.random() < 0.5:
        fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    sc = rr.choice((1.0, 1.0, 1.5))
    size = int(64 * sc)
    spr = fr.resize((size, size), Image.NEAREST)
    ox, oy = ex - size // 2 + rr.randint(-8, 8), ey - size // 2 + rr.randint(-8, 8)
    for y in range(size):
        for x in range(size):
            v = spr.getpixel((x, y))
            if v and 0 <= ox + x < 240 and 0 <= oy + y < 160:
                canvas[oy + y][ox + x] = v
    placed += 1
ctiles, cidx, ctm = [], {}, []
for ty in range(20):
    for tx in range(30):
        t = tuple(canvas[ty * 8 + py][tx * 8 + px] for py in range(8) for px in range(8))
        if t not in cidx:
            cidx[t] = len(ctiles) + 1; ctiles.append(list(t))
        ctm.append(cidx[t])
save('magikarp_pile', ctiles, [mpal])
open(OUT + 'route_magikarp_pile.bin', 'wb').write(struct.pack('<%dH' % len(ctm), *ctm))
print('  collage:', placed, 'Magikarp')

# Colress: tandwiel (twee stuks draaien in elkaar en komen op je af), staal met een blauwe ring
GEAR_TEETH = 10
GPAL = pad([(0, 0, 0), (2, 3, 5), (8, 10, 13), (14, 16, 19), (21, 23, 26), (28, 29, 31), (5, 21, 28), (2, 12, 19)])
gi = Image.new('P', (64, 64), 0)
for y in range(64):
    for x in range(64):
        dx, dy = x - 31.5, y - 31.5
        d = math.hypot(dx, dy)
        a = math.atan2(dy, dx)
        # tand: trapezium-vormig profiel over de omtrek
        ph = (a * GEAR_TEETH / (2 * math.pi)) % 1.0
        tooth = min(1.0, max(0.0, 1.6 - abs(ph - 0.5) * 5.0))
        outer = 24 + 6 * tooth
        if d > outer or d < 6:
            continue
        light = -(dx + dy) / (d * 1.414 + 0.01)  # licht van linksboven
        if d > outer - 1.3 or d < 7.2:
            c = 1
        elif 15 <= d <= 18:
            c = 6 if light > -0.3 else 7  # blauwe ring
        elif d > 22 and tooth < 0.05:
            c = 3
        elif d > outer - 3.5 or d < 10:
            c = 5 if light > 0.5 else 4 if light > -0.2 else 2
        elif 10 <= d < 15 and int(((a + math.pi) * 3 / math.pi) * 2) % 2 == 0:
            c = 2  # gaten tussen de spaken
        else:
            c = 3 if light < 0.3 else 4
        gi.putpixel((x, y), c)
save_sprite('gear', gi, GPAL)

# ------------------------------------------------------------------ Zangoose: reuzenklauw (Crush Claw) scheurt het scherm
# BG-tiles (palet ZPAL): 1 zwart (scheur), 2-4 klauwstriem langs de anti-diagonaal (3 varianten),
# 5-7 scheurrand "zwart rechtsonder", 8-10 scheurrand "zwart linksboven" (gekarteld, rode gloed)
ZPAL = pad([(0, 0, 0), (1, 0, 2), (31, 31, 31), (31, 18, 18), (26, 4, 6), (14, 0, 2), (31, 26, 26)])
zr = random.Random(335)
def zstreak(v):
    off = (v - 1) * 0.6
    def f(x, y):
        d = abs(x + y - 7 + off * 0.0)
        wob = (zr.random() - 0.5) * 0.6
        if d + wob < 0.9:
            return 2
        if d + wob < 1.9:
            return 6
        if d + wob < 2.8:
            return 3
        return 4 if d + wob < 3.4 and zr.random() < 0.5 else 0
    return tile(f)
def zedge(lower, v):
    rr = random.Random(1000 + v * 7 + lower)
    jag = [rr.randint(-2, 2) for _ in range(16)]
    def f(x, y):
        s = x + y - 7 + jag[(x - y) % 16]
        inside = s > 0 if lower else s < 0
        if inside:
            return 1
        if abs(s) <= 1:
            return 4
        if abs(s) <= 2:
            return 5
        return 0
    return tile(f)
ztiles = [tile(lambda x, y: 1)] + [zstreak(v) for v in (1, 2, 3)] + [zedge(1, v) for v in range(3)] + [zedge(0, v) for v in range(3)]
save('zangoose', ztiles, [ZPAL])

# klauw-sprite: drie gebogen klauwen, wit met rode punt, wijzend naar linksonder
CPAL = pad([(0, 0, 0), (3, 2, 4), (31, 31, 31), (22, 22, 26), (14, 14, 18), (30, 6, 8), (18, 2, 4)])
ci = Image.new('P', (64, 64), 0)
cd = ImageDraw.Draw(ci)
for k, (ox, oy) in enumerate([(-11, -11), (0, 0), (11, 11)]):
    # boog van rechtsboven (basis) naar linksonder (punt)
    pts = []
    for i in range(24):
        t = i / 23
        x = 50 - t * 36 + ox - math.sin(t * math.pi) * 5
        y = 14 + t * 36 + oy - math.sin(t * math.pi) * 5
        pts.append((x, y, 4.5 * (1 - t) + 0.7))
    for x, y, r in pts:
        cd.ellipse((x - r - 1, y - r - 1, x + r + 1, y + r + 1), fill=1)
    for i, (x, y, r) in enumerate(pts):
        col = 5 if i > 17 else (2 if i % 6 < 4 else 3)
        cd.ellipse((x - r, y - r, x + r, y + r), fill=col)
        if r > 2:
            cd.ellipse((x - r + 1, y - r + 2, x + r - 1, y + r), fill=4 if col != 5 else 6)
            cd.ellipse((x - r, y - r, x + r - 2, y + r - 2), fill=col)
save_sprite('zangoose_claw', ci, CPAL)

# ------------------------------------------------------------------ Seviper: een schermvullende Poison Fang
# bovenkaak 240x160 (bek bovenin, twee enorme giftanden met druppels), onderkaak 240x40; tiles ontdubbeld
SPAL = pad([(0, 0, 0), (2, 0, 3), (10, 2, 10), (18, 4, 14), (31, 31, 31), (24, 24, 26), (18, 18, 22), (20, 4, 28), (28, 12, 31), (12, 2, 18), (26, 8, 10)])
def jaw_upper():
    im = Image.new('P', (240, 160), 0)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 239, 22), fill=1)
    for x in range(0, 240, 2):
        y = 22 + int(3 * math.sin(x / 9.0))
        d.line((x, 14, x, y), fill=2)
        d.line((x, y - 4, x, y), fill=3)
    for cx in (62, 178):
        # gebogen giftand: breed bij de basis, punt laag in beeld
        for i in range(120):
            t = i / 119
            x = cx + math.sin(t * 2.2) * 10 * (1 if cx < 120 else -1)
            y = 18 + t * 124
            r = 17 * (1 - t) ** 0.8 + 1
            d.ellipse((x - r - 1, y - r - 1, x + r + 1, y + r + 1), fill=1)
        for i in range(120):
            t = i / 119
            x = cx + math.sin(t * 2.2) * 10 * (1 if cx < 120 else -1)
            y = 18 + t * 124
            r = 17 * (1 - t) ** 0.8
            d.ellipse((x - r, y - r, x + r, y + r), fill=7 if t > 0.8 else 5)
            d.ellipse((x - r * 0.75, y - r, x + r * 0.35, y + r * 0.6), fill=4 if t <= 0.8 else 8)
        # gif loopt langs de punt naar beneden
        d.ellipse((cx - 4 + (10 if cx < 120 else -10) * math.sin(2.2), 140, cx + 4 + (10 if cx < 120 else -10) * math.sin(2.2), 152), fill=7)
        d.ellipse((cx - 2 + (10 if cx < 120 else -10) * math.sin(2.2), 142, cx + 1 + (10 if cx < 120 else -10) * math.sin(2.2), 146), fill=8)
    return im
def jaw_lower():
    im = Image.new('P', (240, 40), 0)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 18, 239, 39), fill=1)
    for x in range(0, 240, 2):
        y = 18 - int(3 * math.sin(x / 11.0 + 1))
        d.line((x, y, x, 26), fill=2)
        d.line((x, y, x, y + 4), fill=3)
    for cx in range(20, 240, 40):
        d.polygon([(cx - 6, 18), (cx + 6, 18), (cx, 4)], fill=5)
        d.line((cx - 3, 16, cx, 6), fill=4)
    return im
stiles, sidx = [], {}
def tmap(im):
    out = []
    for ty in range(im.height // 8):
        for tx in range(30):
            t = tuple(im.getpixel((tx * 8 + x, ty * 8 + y)) for y in range(8) for x in range(8))
            if not any(t):
                out.append(0); continue
            if t not in sidx:
                sidx[t] = len(stiles) + 1; stiles.append(list(t))
            out.append(sidx[t])
    return out
utm, ltm = tmap(jaw_upper()), tmap(jaw_lower())
save('seviper', stiles, [SPAL])
open(OUT + 'route_seviper_upper.bin', 'wb').write(struct.pack('<%dH' % len(utm), *utm))
open(OUT + 'route_seviper_lower.bin', 'wb').write(struct.pack('<%dH' % len(ltm), *ltm))

# ------------------------------------------------------------------ Heatran: lavapluimen en een uitbarsting
# 1-2 lava (stroming, kleurcyclus), 3 pluim linkerrand, 4 pluim rechterrand, 5-7 kop van de pluim (l/m/r),
# 8 druppels, 9 lava-oppervlak (golvende bovenrand van de vloed)
LAVA = [(0, 0, 0), (12, 2, 2), (22, 4, 2), (29, 10, 2), (31, 18, 4), (31, 26, 10), (31, 31, 22), (6, 2, 2)]
lr = random.Random(485)
def lava_px(x, y, v):
    s = math.sin((x * 0.9 + y * 0.35 + v * 2.1)) + math.sin((y * 0.7 - x * 0.3 + v))
    return 2 + int((s + 2) / 4 * 4.99)          # 2..6
def lava_tile(v):
    return tile(lambda x, y: lava_px(x, y, v))
def edge(left):
    def f(x, y):
        d = x if left else 7 - x                    # afstand tot de buitenkant
        w = 3 + int(1.5 * math.sin(y * 1.3 + (0 if left else 2)))
        if d < 7 - w:
            return 0
        if d == 7 - w:
            return 7 if lr.random() < 0.5 else 2
        return lava_px(x, y, 1)
    return tile(f)
def head(part):
    def f(x, y):
        gx = x + part * 8                           # 0..23 over de drie tiles
        top = 7 - int(6 * math.sin(math.pi * gx / 23) ** 0.6)
        if y < top:
            return 0
        if y == top:
            return 6
        return 5 if y < top + 2 else lava_px(gx, y, 2)
    return tile(f)
def drops():
    pts = [(1, 2), (5, 0), (3, 6), (6, 4)]
    return tile(lambda x, y: 5 if any(abs(x - a) + abs(y - b) <= 1 for a, b in pts) else 0)
def surface():
    def f(x, y):
        top = 3 + int(2 * math.sin(x * 0.8))
        return 0 if y < top else (6 if y == top else lava_px(x, y, 3))
    return tile(f)
htiles = [lava_tile(0), lava_tile(1), edge(True), edge(False), head(0), head(1), head(2), drops(), surface()]
save('heatran', htiles, cycle(pad(LAVA), 4, amp=2))

# ------------------------------------------------------------------ Shaymin: een wervelwind van Gracidea-bloemen en -blaadjes
# 1-2 Gracidea (roze / wit met roze hart), 3-6 roze blaadje (vier richtingen), 7-8 wit blaadje, 9 bloementapijt,
# 10 helemaal lichtroze, 11-14 grote Gracidea (2x2)
GRAC = pad([(0, 0, 0), (31, 20, 26), (29, 11, 20), (21, 5, 13), (31, 31, 31), (26, 24, 28), (31, 27, 8),
            (10, 22, 8), (5, 13, 5), (31, 26, 29)])
def gracidea(white):
    def f(x, y):
        dx, dy = x - 3.5, y - 3.5
        d = math.hypot(dx, dy)
        if d < 1.1:
            return 6
        if d > 3.9:
            return 0
        a = math.atan2(dy, dx)
        lobe = abs(math.cos(2.5 * (a + 0.3)))          # vijf bloemblaadjes
        if d > 1.6 + 2.4 * lobe:
            return 0
        if white:
            return 2 if d < 2.0 else (4 if d < 3.1 else 5)
        return 3 if d < 1.7 else (2 if d < 2.6 else 1)
    return tile(f)
def petal(ang, col):
    ca, sa = math.cos(ang), math.sin(ang)
    def f(x, y):
        u = (x - 3.5) * ca + (y - 3.5) * sa             # langs het blaadje
        v = -(x - 3.5) * sa + (y - 3.5) * ca
        if abs(u) > 3.2:
            return 0
        w = 1.8 * math.cos(u / 3.2 * math.pi / 2) ** 0.7 * (1.0 if u < 0 else 0.75)
        if abs(v) > w:
            return 0
        if col == 'pink':
            return 3 if u > 2.2 else (1 if v < -0.5 else 2)
        return 2 if u > 2.4 else (4 if v < 0.3 else 5)
    return tile(f)
def carpet(x, y):
    pts = [(1, 1, 0), (5, 2, 1), (2, 5, 1), (6, 6, 0)]
    for cx, cy, w in pts:
        d = abs(x - cx) + abs(y - cy)
        if d == 0:
            return 6
        if d == 1:
            return 4 if w else 2
    return 9 if (x + y) % 3 else 1
grac = [gracidea(False), gracidea(True)]
grac += [petal(a, 'pink') for a in (0.4, 0.4 + math.pi / 2, 0.4 + math.pi, 0.4 + 3 * math.pi / 2)]
grac += [petal(a, 'white') for a in (1.1, 1.1 + math.pi)]
grac.append(tile(carpet))
grac.append(tile(lambda x, y: 9))
def big_gracidea(x, y):
    dx, dy = x - 7.5, y - 7.5
    d = math.hypot(dx, dy)
    if d < 2.0:
        return 6
    a = math.atan2(dy, dx)
    lobe = abs(math.cos(2.5 * (a + 0.3)))
    if d > 2.6 + 5.2 * lobe:
        return 0
    if d < 3.0:
        return 3
    return 4 if d > 1.8 + 5.2 * lobe else (1 if dx + dy < 0 else 2)
grac += blocks(big_gracidea, 2, 2)                  # 11-14: grote Gracidea (2x2)
save('shaymin', grac, cycle(GRAC, 4, amp=1))
