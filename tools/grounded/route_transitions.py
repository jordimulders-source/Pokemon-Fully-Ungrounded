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

# ------------------------------------------------------------------ Shaymin: een wervelwind van bloemen in alle kleuren (Gracidea voorop)
# Drie paletten (BG-palet 15, 14 en 13), elk 4 standen (lichte schittering): .pal = [p15 x4, p14 x4, p13 x4].
# Per palet: 1 wit, 2 wit schaduw, 3-4 blad (licht/donker), 5 geel hart, 6 bruin hart, 7-9 / 10-12 / 13-15 drie
# bloemkleuren (licht, midden, donker). p15: roze (Gracidea), rood, fuchsia; p14: geel, oranje, zalm; p13: blauw,
# paars, lila. Tiles: eerst SH_SMALL kleine bloemen/blaadjes (8x8), dan SH_BIG grote bloemen (2x2), dan SH_CARPET
# tapijttiles (gras met een bloem). Volgorde en palet per tile staan in de tabellen in src/battle_transition.c.
SH_COMMON = [(31, 31, 31), (24, 23, 27), (14, 26, 8), (5, 15, 6), (31, 27, 6), (17, 8, 3)]
SH_FAM = {15: [((31, 22, 27), (29, 11, 20), (20, 4, 12)),     # Gracidea-roze
               ((31, 11, 9), (25, 3, 4), (14, 1, 3)),          # rood
               ((31, 14, 29), (24, 4, 22), (14, 1, 13))],      # fuchsia
          14: [((31, 31, 14), (31, 25, 3), (24, 15, 1)),       # geel
               ((31, 22, 8), (31, 14, 2), (21, 7, 1)),         # oranje
               ((31, 24, 20), (30, 15, 12), (20, 7, 7))],      # zalm
          13: [((20, 28, 31), (8, 16, 31), (3, 6, 20)),        # blauw
               ((24, 16, 31), (16, 6, 28), (8, 2, 16)),        # paars
               ((29, 25, 31), (23, 18, 31), (14, 10, 24))]}    # lila
def sh_pal(p, f):
    base = [(0, 0, 0)] + SH_COMMON + [c for fam in SH_FAM[p] for c in fam]
    out = [base[0]]
    for i, c in enumerate(base[1:], 1):
        d = int(round(1.4 * math.sin(2 * math.pi * f / 4 + i * 1.3)))
        out.append(tuple(max(0, min(31, v + d)) for v in c))
    return out
SH_W, SH_WS, SH_G, SH_GD, SH_Y, SH_BR = 1, 2, 3, 4, 5, 6
def fam(k):
    return (7 + 3 * k, 8 + 3 * k, 9 + 3 * k)

def sh_flower(size, n, round_, cols, center=SH_Y, cr=1.1, ring=None, rot=0.3, depth=0.55, rays=False):
    """bloem van boven: n bloemblaadjes (rond of spits, of dunne stralen), licht linksboven, donker aan de rand"""
    c0 = (size - 1) / 2.0
    R = size / 2.0 - 0.15
    def f(x, y):
        dx, dy = x - c0, y - c0
        d = math.hypot(dx, dy)
        if d < cr:
            return center if d < cr - 0.6 or (x + y) % 2 else (SH_BR if center == SH_Y else center)
        if ring and d < ring[0]:
            return ring[1]
        a = math.atan2(dy, dx) + rot
        lobe = abs(math.cos(n * a / 2))
        if rays:
            lobe = 1.0 if lobe > 0.45 else 0.0
        elif round_:
            lobe = lobe ** 0.5
        edge = R * (1 - depth) + R * depth * lobe
        if d > edge:
            return 0
        light, mid, dark = cols
        if d > edge - 0.9 or (rays and lobe < 1):
            return dark
        return light if dx + dy < -0.6 * d else mid
    return f

T_TULIP = ['.a.ab.b.', '.aabbbc.', '.abbbbc.', '.abbbbc.', '..bbbc..', '...g....', '.Gg.....', '..g.....']
T_ROSE = ['..bbbb..', '.baaacb.', 'bacbbacb', 'baabcacb', 'bacccacb', '.baaacc.', '..bccc..', '........']
T_BELL = ['....gg..', '..gg..g.', '.g....g.', 'ab...abc', 'bbc..bbc', 'c.c..c.c', '........', '........']
T_LAV = ['...a....', '..aba...', '...bc...', '..abc...', '...bc...', '..abcG..', '...gG...', '...g....']
T_LEAF = ['......Gg', '....GGg.', '..GGGg..', '.GGGgg..', '.Ggg....', 'gg......', 'g.......', '........']
T_PETAL = ['........', '...aa...', '..aabb..', '.abbbbc.', '.bbbbcc.', '..bccc..', '...c....', '........']
def sh_tmpl(rows, cols):
    m = {'.': 0, 'a': cols[0], 'b': cols[1], 'c': cols[2], 'G': SH_G, 'g': SH_GD, 'W': SH_W, 'Y': SH_Y}
    return [m[rows[y][x]] for y in range(8) for x in range(8)]

# kleine tiles: (tile, palet)
sh_small = [
    (tile(sh_flower(8, 5, False, fam(0), cr=1.3)), 15),                 # Gracidea
    (tile(sh_flower(8, 5, False, (SH_W, SH_W, fam(0)[1]), center=fam(0)[2], cr=1.2)), 15),  # witte Gracidea, roze hart
    (sh_tmpl(T_ROSE, fam(1)), 15),                                       # roos
    (sh_tmpl(T_TULIP, fam(1)), 15),                                      # rode tulp
    (tile(sh_flower(8, 8, False, fam(2), cr=1.2, depth=0.4)), 15),      # cosmea (fuchsia)
    (sh_tmpl(T_PETAL, fam(0)), 15),                                      # roze blaadje
    (sh_tmpl(T_PETAL, fam(1)), 15),                                      # rood blaadje
    (sh_tmpl(T_LEAF, fam(0)), 15),                                       # blad
    (tile(sh_flower(8, 12, False, (SH_W, SH_W, SH_WS), cr=1.6, rays=True)), 14),   # madeliefje
    (tile(sh_flower(8, 5, True, fam(0), cr=1.0, depth=0.35)), 14),      # boterbloem
    (tile(sh_flower(8, 10, True, fam(1), center=fam(1)[2], cr=1.4, depth=0.25)), 14),  # goudsbloem
    (sh_tmpl(T_TULIP, fam(0)), 14),                                      # gele tulp
    (sh_tmpl(T_TULIP, fam(2)), 14),                                      # zalmroze tulp
    (sh_tmpl(T_PETAL, fam(0)), 14),                                      # geel blaadje
    (sh_tmpl(T_PETAL, fam(1)), 14),                                      # oranje blaadje
    (sh_tmpl(T_PETAL, (SH_W, SH_W, SH_WS)), 14),                          # wit blaadje
    (tile(sh_flower(8, 5, True, fam(0), cr=1.5, ring=(1.6, SH_W), depth=0.3)), 13),  # vergeet-mij-nietje
    (tile(sh_flower(8, 4, False, fam(1), center=SH_Y, cr=1.0, depth=0.5, rot=0.0)), 13),  # viooltje
    (sh_tmpl(T_BELL, fam(0)), 13),                                       # klokjes
    (sh_tmpl(T_LAV, fam(1)), 13),                                        # lavendel
    (tile(sh_flower(8, 6, False, fam(2), cr=1.1)), 13),                 # lila stervormpje
    (sh_tmpl(T_PETAL, fam(0)), 13),                                      # blauw blaadje
    (sh_tmpl(T_PETAL, fam(1)), 13),                                      # paars blaadje
    (sh_tmpl(T_PETAL, fam(2)), 13),                                      # lila blaadje
]
# grote bloemen (16x16)
sh_big = [
    (sh_flower(16, 5, False, fam(0), cr=2.4, depth=0.6), 15),            # grote Gracidea
    (None, 15),                                                           # grote roos (hieronder)
    (sh_flower(16, 16, False, fam(0), center=SH_BR, cr=4.2, rays=True), 14),   # zonnebloem
    (sh_flower(16, 14, False, (SH_W, SH_W, SH_WS), cr=3.0, rays=True), 14),    # margriet
    (sh_flower(16, 5, True, fam(0), cr=2.0, ring=(3.2, SH_W), depth=0.25), 13),  # blauwe winde
    (sh_flower(16, 6, False, fam(1), cr=1.8, depth=0.7, rot=0.0), 13),   # paarse ster (clematis)
]
def sh_bigrose(x, y):
    dx, dy = x - 7.5, y - 7.5
    d = math.hypot(dx, dy)
    if d > 7.4:
        return 0
    a = math.atan2(dy, dx)
    s = (d * 0.9 + a * 1.2) % (2 * math.pi)                # spiraal van blaadjes
    light, mid, dark = fam(1)
    if d > 6.6:
        return dark
    if s < 0.9:
        return dark
    return light if s > 4.0 and dx + dy < 0 else mid
sh_big[1] = (sh_bigrose, 15)
SH_CARPET_FLOWERS = (0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20)   # de bloemen (geen blaadjes)
def sh_carpet(k):
    """tapijttile: gras met een van de kleine bloemen erop"""
    gr2 = random.Random(400 + k)
    t, p = sh_small[k]
    return ([v if v else (SH_G if gr2.random() < 0.65 else SH_GD) for v in t], p)
sh_carpet_tiles = [sh_carpet(k) for k in SH_CARPET_FLOWERS]
shay = [t for t, p in sh_small]
for f, p in sh_big:
    shay += blocks(f, 2, 2)
shay += [t for t, p in sh_carpet_tiles]
save('shaymin', shay, [sh_pal(p, f) for p in (15, 14, 13) for f in range(4)])
# vooraf berekende tabellen (delen is traag op de GBA): _petals.bin = per bloem (210) 3 bytes: straal-offset, hoek-offset,
# tile (1-24 klein; 0x80 | n = grote bloem n); _carpet.bin = 30x20 tapijtcellen (bit 0-5 tile, bit 6 spiegelen)
SH_PETALS, SH_CARPET0 = 210, 1 + len(sh_small) + 4 * len(sh_big)
pet = []
for i in range(SH_PETALS):
    pet += [(i // 3) * 6 % 150, ((i % 3) * 85 + (i // 75) * 43 + (i * 13) % 20) & 0xFF,
            0x80 | ((i // 6) % len(sh_big)) if i % 6 == 0 else 1 + (i * 7 + i // 3) % len(sh_small)]
open(OUT + 'route_shaymin_petals.bin', 'wb').write(bytes(pet))
open(OUT + 'route_shaymin_carpet.bin', 'wb').write(bytes(
    (SH_CARPET0 + (x * 7 + y * 11 + (x * y) % 5) % len(sh_carpet_tiles)) | (((x + y) & 1) << 6) for y in range(20) for x in range(30)))
print('  Shaymin: %d klein, %d groot, %d tapijt' % (len(sh_small), len(sh_big), len(sh_carpet_tiles)))
print('  paletten klein:', [p for t, p in sh_small], 'groot:', [p for f, p in sh_big])

# ------------------------------------------------------------------ Genesect: scanlijnen, een rood vizier dat zijn doel zoekt, Techno Blast
# 1 scanlijnen, 2 scanbalk, 3-66 vizier (8x8), 67.. "LOCKED ON" (GTW x GTH), daarna straal: rand boven, kern, rand onder
GEN = pad([(0, 0, 0), (6, 0, 2), (20, 2, 4), (31, 6, 6), (31, 18, 16), (31, 31, 31), (2, 2, 4), (12, 4, 16)])
gen = [tile(lambda x, y: 6 if y % 4 == 0 else 0), tile(lambda x, y: 3 if y % 2 == 0 else 4)]
def reticle(x, y):
    dx, dy = x - 31.5, y - 31.5
    r = math.hypot(dx, dy)
    if r < 2.5:
        return 5
    if 25 <= r <= 28:
        return 3
    if 24 <= r < 25 or 28 < r <= 29.2:
        return 1
    if (abs(dx) < 1.5 or abs(dy) < 1.5) and 7 < r < 32:
        return 3
    if (abs(dx) < 2.5 or abs(dy) < 2.5) and 7 < r < 32:
        return 1
    if 14 <= r <= 15.5 and int((math.atan2(dy, dx) + math.pi) * 8 / math.pi) % 2 == 0:
        return 2
    near = min(x, 63 - x), min(y, 63 - y)
    if (near[0] < 2 and near[1] < 12) or (near[1] < 2 and near[0] < 12):
        return 4
    return 0
gen += blocks(reticle, 8, 8)
tm = text_mask('LOCKED ON', 12)
GTW, GTH = (tm.size[0] + 9) // 8, (tm.size[1] + 9) // 8
def gtext(x, y):
    on = lambda a, b: 0 <= a - 1 < tm.size[0] and 0 <= b - 1 < tm.size[1] and tm.getpixel((a - 1, b - 1))
    if on(x, y):
        return 3
    if any(on(x + a, y + b) for a in (-1, 0, 1) for b in (-1, 0, 1)):
        return 6
    return 0
gen += blocks(gtext, GTW, GTH)
BEAM = [6, 1, 2, 3, 4, 5, 5, 5]
gen += [tile(lambda x, y: BEAM[y]), tile(lambda x, y: 5 if (x + y) % 3 else 4), tile(lambda x, y: BEAM[7 - y])]
save('genesect', gen, [GEN])
print('  LOCKED ON', GTW, 'x', GTH, 'tiles, straal vanaf', 3 + 64 + GTW * GTH)

# ------------------------------------------------------------------ Mewtwo: het lab op Cinnabar Island. In een gloeiende kweektank zweeft
# Mewtwo's silhouet (de FRLG-sprite), het dagboek uit de Pokémon Mansion verschijnt regel voor regel ("Diary: Feb. 6
# Mew gave birth. We named the newborn MEWTWO." / "Diary: Sept. 1 MEWTWO is far too powerful. We have failed to curb
# its vicious tendencies..."), dan gaan de ogen open, barst het glas en spat de tank uiteen in een psychische schokgolf.
# route_mewtwo.png: tiles 1-3 rand van de schokgolf (buiten, fel, binnen), 4-7 glasscherven, daarna de ontdubbelde
# tiles van de beelden. Tilemaps (u16, 30 breed, tile-indexen zonder palet): _lab.bin (30x20), _crack.bin (3 x 30x20,
# barsten 1-3), _page.bin (2 x 30x4: dagboek, rij 16-19), _burst.bin (30x20: psychisch veld met Mewtwo).
# Paletten (9 x 16): 0-2 rustig (belletjes stijgen), 3-5 ontwaakt (ogen gloeien, vloeistof flakkert), 6-8 schokgolf.
# Kleuren: 1 zwart, 2 donker staal / tekstschaduw, 3 staal, 4 glans / barst, 5-7 vloeistof (donker-fel), 8-10 belletjes,
# lampjes en ringen (kleurcyclus), 11 ogen, 12 tekst / scherm, 13-14 silhouet (schaduw / licht)
import re
MW_BLACK, MW_STEEL_D, MW_STEEL, MW_GLINT, MW_LIQ_D, MW_LIQ, MW_LIQ_L = 1, 2, 3, 4, 5, 6, 7
MW_PHASE, MW_EYE, MW_TEXT, MW_SIL_D, MW_SIL_L, MW_GLOW = 8, 11, 12, 13, 14, 15
def mw_pal(liq, bub_on, bub_off, eye, glow, phase):
    p = [(0, 0, 0), (1, 2, 3), (4, 6, 8), (10, 13, 15), (22, 27, 27), liq[0], liq[1], liq[2]]
    for k in range(3):
        p.append(bub_on if (k + phase) % 3 == 0 else bub_off)
    return p + [eye, (20, 31, 20), (0, 3, 2), (3, 8, 6), glow]
MW_LIQ_CALM = ((2, 9, 6), (5, 17, 10), (13, 27, 15))
mw_pals = []
for f in range(3):                                      # rustig: belletjes stijgen
    mw_pals.append(mw_pal(MW_LIQ_CALM, (24, 31, 24), MW_LIQ_CALM[1], (3, 8, 6), (3, 8, 6), f))
for f in range(3):                                      # ontwaakt: de vloeistof flakkert paars, de ogen gloeien
    liq = [((2, 9, 6), (8, 4, 12), (4, 6, 10))[f], ((5, 17, 10), (16, 8, 22), (10, 12, 18))[f],
           ((13, 27, 15), (26, 16, 31), (20, 24, 28))[f]]
    mw_pals.append(mw_pal(liq, (31, 31, 31), liq[1], ((31, 31, 31), (28, 22, 31), (31, 28, 31))[f],
                         ((20, 8, 28), (24, 12, 31), (16, 6, 24))[f], f))
for f in range(3):                                      # schokgolf: paars veld, ringen golven naar buiten
    ring = [(12, 4, 20), (20, 9, 28), (28, 18, 31)]
    p = [(0, 0, 0), (2, 0, 4), (6, 2, 10), (14, 8, 22), (31, 28, 31), (6, 2, 12), (12, 4, 20), (24, 14, 31)]
    for k in range(3):
        p.append(ring[(k - f) % 3])
    mw_pals.append(p + [(31, 31, 31), (31, 26, 31), (2, 0, 5), (8, 3, 14), (26, 14, 31)])

def mw_scale3x(img):
    """Scale3x op een P-beeld (zie guest_trainer_pics.py); daarna halveren geeft een nette 1,5x"""
    W, H = img.size
    p = img.load()
    out = Image.new('P', (W * 3, H * 3))
    q = out.load()
    g = lambda x, y: p[min(max(x, 0), W - 1), min(max(y, 0), H - 1)]
    for y in range(H):
        for x in range(W):
            A, B, C, D, E, F, G, Hh, I = [g(x + dx, y + dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
            e = [E] * 9
            if B != Hh and D != F:
                e[0] = D if D == B else E
                e[1] = B if (D == B and E != C) or (B == F and E != A) else E
                e[2] = F if B == F else E
                e[3] = D if (D == B and E != G) or (D == Hh and E != A) else E
                e[5] = F if (B == F and E != I) or (Hh == F and E != C) else E
                e[6] = D if D == Hh else E
                e[7] = Hh if (D == Hh and E != I) or (Hh == F and E != G) else E
                e[8] = F if Hh == F else E
            for i in range(9):
                q[x * 3 + i % 3, y * 3 + i // 3] = e[i]
    return out
# Mewtwo-silhouet uit de FRLG-frontsprite: 1 schaduw, 2 licht, 3 oog (gloeit als de ogen opengaan)
mw_spr = Image.open('graphics/pokemon/mewtwo/anim_front_gba.png').crop((0, 0, 64, 64))
mw_sp = mw_spr.getpalette()
mw_sil = Image.new('P', (64, 64), 0)
for y in range(64):
    for x in range(64):
        v = mw_spr.getpixel((x, y))
        if v == 0:
            continue
        if 35 <= x <= 39 and 15 <= y <= 18 and v in (5, 6, 7, 8):
            mw_sil.putpixel((x, y), 3)
        else:
            mw_sil.putpixel((x, y), 2 if sum(mw_sp[v * 3:v * 3 + 3]) > 450 and v != 14 else 1)
mw_big = mw_scale3x(mw_sil).resize((96, 96), Image.NEAREST)
mw_eye = [(x, y) for y in range(96) for x in range(96) if mw_big.getpixel((x, y)) == 3]
for (x, y) in mw_eye:                                   # gloed rond het oog (kleur 15), binnen het silhouet
    for a in range(-2, 3):
        for b in range(-1, 2):
            if abs(a) + abs(b) <= 2 and mw_big.getpixel((x + a, y + b)) in (1, 2):
                mw_big.putpixel((x + a, y + b), 4)
MW_CX = 120
mbx0, mby0, mbx1, mby1 = mw_big.getbbox()
MW_OX, MW_OY = MW_CX - (mbx0 + mbx1) // 2, 17 - mby0
def mw_paste(im, rim=None):
    px = mw_big.load()
    if rim is not None:
        for y in range(96):
            for x in range(96):
                if px[x, y] == 0 and any(0 <= x + a < 96 and 0 <= y + b < 96 and px[x + a, y + b]
                                         for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    im.putpixel((MW_OX + x, MW_OY + y), rim)
    for y in range(96):
        for x in range(96):
            if px[x, y]:
                im.putpixel((MW_OX + x, MW_OY + y), (MW_SIL_D, MW_SIL_L, MW_EYE, MW_GLOW)[px[x, y] - 1])

MTX0, MTX1, MTY0, MTY1 = 64, 176, 14, 112               # glas van de tank
def mw_lab():
    im = Image.new('P', (240, 160), MW_BLACK)
    d = ImageDraw.Draw(im)
    for x in range(0, 240, 40):                         # wandpanelen
        d.line(((x, 0), (x, 111)), fill=MW_STEEL_D)
    for y in (40, 88):
        d.line(((0, y), (239, y)), fill=MW_STEEL_D)
    d.rectangle((0, 112, 239, 127), fill=MW_STEEL_D)    # vloer met roosters
    for x in range(0, 240, 8):
        d.line(((x, 113), (x, 127)), fill=MW_BLACK)
    d.line(((0, 112), (239, 112)), fill=MW_STEEL)
    for (x0, x1) in ((0, MTX0), (MTX1, 239)):           # leidingen van de tankkap naar de zijkanten en omlaag
        d.rectangle((x0, 3, x1, 9), fill=MW_STEEL)
        d.line(((x0, 4), (x1, 4)), fill=MW_GLINT)
        d.line(((x0, 9), (x1, 9)), fill=MW_STEEL_D)
    for x in (24, 216):
        d.rectangle((x - 3, 6, x + 3, 56), fill=MW_STEEL)
        d.line(((x - 2, 6), (x - 2, 56)), fill=MW_GLINT)
        d.line(((x + 3, 6), (x + 3, 56)), fill=MW_STEEL_D)
        for y in (20, 40):
            d.rectangle((x - 4, y, x + 4, y + 2), fill=MW_STEEL_D)
    # consoles: links een DNA-streng, rechts een hartslag; de lampjes knipperen (fasekleuren)
    for (cx, kind) in ((24, 'dna'), (216, 'ecg')):
        x0, x1 = cx - 20, cx + 19
        d.rectangle((x0, 58, x1, 111), fill=MW_STEEL)
        d.line(((x0, 58), (x1, 58)), fill=MW_GLINT)
        d.line(((x0, 58), (x0, 111)), fill=MW_GLINT)
        d.line(((x1, 58), (x1, 111)), fill=MW_STEEL_D)
        d.rectangle((x0 + 4, 62, x1 - 4, 88), fill=MW_BLACK)
        if kind == 'dna':
            for y in range(64, 87):
                a = (y - 64) * 0.5
                xa, xb = cx + int(round(9 * math.sin(a))), cx + int(round(9 * math.sin(a + math.pi)))
                if (y - 64) % 3 == 1 and abs(xa - xb) > 3:
                    d.line(((min(xa, xb) + 1, y), (max(xa, xb) - 1, y)), fill=MW_LIQ_D)
                d.point((xb, y), fill=MW_LIQ)
                d.point((xa, y), fill=MW_TEXT)
        else:
            pts = []
            for x in range(x0 + 5, x1 - 4):
                u = (x - x0 - 5) % 15
                pts.append((x, 76 - {4: 2, 6: 9, 7: -5}.get(u, 0)))
            d.line(pts, fill=MW_TEXT)
            for x in range(x0 + 5, x1 - 4, 4):
                d.point((x, 86), fill=MW_LIQ_D)
        for k in range(4):
            d.rectangle((x0 + 6 + k * 8, 94, x0 + 8 + k * 8, 96), fill=MW_PHASE + (k + (cx > 100)) % 3)
        for k in range(3):
            d.line(((x0 + 6, 101 + k * 3), (x1 - 6, 101 + k * 3)), fill=MW_STEEL_D)
    # de tank: kap, glas met vloeistof (cilinder: fel in het midden), belletjes, sokkel
    d.rectangle((MTX0 - 6, 0, MTX1 + 6, MTY0 - 1), fill=MW_STEEL)
    d.line(((MTX0 - 6, MTY0 - 1), (MTX1 + 6, MTY0 - 1)), fill=MW_STEEL_D)
    d.line(((MTX0 - 6, 1), (MTX1 + 6, 1)), fill=MW_GLINT)
    for x in range(MTX0, MTX1, 12):
        d.rectangle((x + 2, 4, x + 5, 9), fill=MW_STEEL_D)
    for y in range(MTY0, MTY1):
        for x in range(MTX0, MTX1):
            c = abs((x - MTX0) / (MTX1 - MTX0 - 1) - 0.5) * 2
            v = MW_LIQ_L if c < 0.32 else (MW_LIQ if c < 0.78 else MW_LIQ_D)
            if (0.26 < c < 0.38 or 0.72 < c < 0.84) and (x + y) % 2:
                v = MW_LIQ if c < 0.5 else MW_LIQ_D
            im.putpixel((x, y), v)
    for x in (MTX0 + 8, MTX0 + 9, MTX0 + 14):
        d.line(((x, MTY0 + 2), (x, MTY1 - 3)), fill=MW_GLINT)
    d.line(((MTX1 - 9, MTY0 + 4), (MTX1 - 9, MTY1 - 5)), fill=MW_GLINT)
    br = random.Random(150)
    for col in range(8):                                # belletjes: elke stip heeft een fase per hoogte (stijgen)
        x = MTX0 + 18 + col * 11 + br.randint(-3, 3)
        for y in range(MTY1 - 4, MTY0 + 2, -6):
            if br.random() < 0.75:
                ph = MW_PHASE + (y // 6) % 3
                if br.random() < 0.3:
                    d.rectangle((x - 1, y - 1, x, y), fill=ph)
                else:
                    d.point((x, y), fill=ph)
            x += br.choice((-1, 0, 0, 1))
    d.rectangle((MTX0 - 2, MTY0, MTX0 - 1, MTY1), fill=MW_STEEL)
    d.rectangle((MTX1, MTY0, MTX1 + 1, MTY1), fill=MW_STEEL)
    d.rectangle((MTX0 - 8, MTY1, MTX1 + 8, 126), fill=MW_STEEL)
    d.line(((MTX0 - 8, MTY1), (MTX1 + 8, MTY1)), fill=MW_GLINT)
    d.line(((MTX0 - 8, 126), (MTX1 + 8, 126)), fill=MW_STEEL_D)
    for k in range(5):
        d.rectangle((MTX0 + 4 + k * 22, MTY1 + 5, MTX0 + 9 + k * 22, MTY1 + 7), fill=MW_PHASE + k % 3)
    mw_paste(im)
    d.rectangle((0, 128, 239, 159), fill=MW_BLACK)      # dagboekbalk
    d.line(((0, 128), (239, 128)), fill=MW_STEEL)
    return im
mw_lab_im = mw_lab()

# barsten in het glas (3 stadia) vanaf de plek waar Mewtwo's hand tegen het glas drukt
mw_segs = []
mcr = random.Random(2)
def mw_crack(x, y, ang, n, t0, depth):
    for i in range(n):
        ang += mcr.uniform(-0.5, 0.5)
        nx, ny = x + math.cos(ang) * 7, y + math.sin(ang) * 7
        mw_segs.append(((x, y), (nx, ny), t0 + i))
        x, y = nx, ny
        if depth < 1 and mcr.random() < 0.3:
            mw_crack(x, y, ang + mcr.choice((-1, 1)) * mcr.uniform(0.7, 1.2), n // 2, t0 + i, depth + 1)
MW_CRX, MW_CRY = MW_CX + 6, 60
for k in range(6):
    mw_crack(MW_CRX, MW_CRY, k * 2 * math.pi / 6 + 0.3, 9, 0, 0)
mw_cracks = []
for lim in (2, 5, 99):
    im = mw_lab_im.copy()
    d = ImageDraw.Draw(im)
    for (p, q, t0) in mw_segs:
        if t0 <= lim:
            d.line((p, q), fill=MW_GLINT)
    if lim == 99:
        d.ellipse((MW_CRX - 3, MW_CRY - 3, MW_CRX + 3, MW_CRY + 3), outline=MW_GLINT)
    for y in range(160):                                # alleen op het glas
        for x in range(240):
            if not (MTX0 <= x < MTX1 and MTY0 <= y < MTY1):
                im.putpixel((x, y), mw_lab_im.getpixel((x, y)))
    mw_cracks.append(im)

# het dagboek in het lettertype van de game (latin_narrow; 1 = letter, 2 = schaduw)
MW_CM = {}
for line in open('charmap.txt', encoding='utf-8'):
    m = re.match(r"^'(.|…)'\s*=\s*([0-9A-F]{2})\s*(@.*)?$", line.strip())
    if m and m.group(1) not in MW_CM:
        MW_CM[m.group(1)] = int(m.group(2), 16)
MW_W = [int(v, 0) for v in re.findall(r'0x[0-9A-Fa-f]+|\d+',
        open('src/fonts.c').read().split('const u8 gFontNarrowLatinGlyphWidths[] = {')[1].split('};')[0])]
mw_font = Image.open('graphics/fonts/latin_narrow.png')
def mw_text(im, x, y, text):
    for ch in text:
        g = MW_CM[ch]
        gx, gy = (g % 16) * 16, (g // 16) * 16
        for yy in range(16):
            for xx in range(MW_W[g]):
                v = mw_font.getpixel((gx + xx, gy + yy))
                if v in (1, 2) and 0 <= y + yy < im.height:
                    im.putpixel((x + xx, y + yy), MW_TEXT if v == 1 else MW_STEEL_D)
        x += MW_W[g]
    return x
mw_pages = []
for (head, l1, l2) in (('Diary: Feb. 6', 'Mew gave birth.', 'We named the newborn MEWTWO.'),
                       ('Diary: Sept. 1', 'MEWTWO is far too powerful.', 'We have failed to curb its vicious tendencies…')):
    im = Image.new('P', (240, 32), MW_BLACK)
    ImageDraw.Draw(im).line(((0, 0), (239, 0)), fill=MW_STEEL)
    mw_text(im, 10, 13, l2)
    mw_text(im, mw_text(im, 10, -1, head) + 6, -1, l1)
    mw_pages.append(im)

# schokgolf: psychisch veld in ringen rond Mewtwo (fasekleuren golven naar buiten), spiegelsymmetrisch rond het midden
# (x 120, y 64 liggen op een tilegrens) zodat de kwarten dezelfde (gespiegelde) tiles delen; Mewtwo zwart met een felle
# rand en witte ogen
def mw_burst():
    im = Image.new('P', (240, 160), 0)
    for y in range(160):
        for x in range(240):
            dx, dy = abs(x + 0.5 - MW_CX), abs(y + 0.5 - 64) * 1.25
            r = math.hypot(dx, dy)
            w = (r + 4 * math.cos(4 * math.atan2(dy, dx))) / 9
            v = MW_PHASE + int(w) % 3
            if w - int(w) > 0.8:
                v = MW_LIQ_D if r > 30 else MW_PHASE + (int(w) + 1) % 3
            im.putpixel((x, y), v)
    mw_paste(im, rim=MW_GLINT)
    return im
mw_burst_im = mw_burst()

mw_tiles = [[MW_GLINT if (x + y) % 2 else MW_BLACK for y in range(8) for x in range(8)],
            [MW_GLINT] * 64,
            [MW_LIQ_L if (x + y) % 2 else MW_GLINT for y in range(8) for x in range(8)]]
for k in range(4):                                      # glasscherven
    sr = random.Random(30 + k)
    im = Image.new('P', (8, 8), MW_BLACK)
    pts = [(sr.randint(0, 3), sr.randint(0, 3)), (sr.randint(4, 7), sr.randint(1, 5)), (sr.randint(1, 5), sr.randint(5, 7))]
    ImageDraw.Draw(im).polygon(pts, fill=MW_LIQ_L, outline=MW_GLINT)
    mw_tiles.append([im.getpixel((x, y)) for y in range(8) for x in range(8)])
mw_idx = {}
def mw_map(im, h):
    """ontdubbelt ook gespiegelde tiles (bit 10/11 = horizontaal/verticaal spiegelen in de tilemap)"""
    out = []
    for ty in range(h):
        for tx in range(30):
            px = [[im.getpixel((tx * 8 + x, ty * 8 + y)) for x in range(8)] for y in range(8)]
            for flip in range(4):
                rows = px[::-1] if flip & 2 else px
                t = tuple(v for row in rows for v in (row[::-1] if flip & 1 else row))
                if t in mw_idx:
                    out.append(mw_idx[t] | (flip << 10))
                    break
            else:
                t = tuple(v for row in px for v in row)
                mw_idx[t] = len(mw_tiles) + 1
                mw_tiles.append(list(t))
                out.append(mw_idx[t])
    return out
mw_lab_tm = mw_map(mw_lab_im, 20)
mw_crack_tm = sum((mw_map(im, 20) for im in mw_cracks), [])
mw_page_tm = sum((mw_map(im, 4) for im in mw_pages), [])
mw_burst_tm = mw_map(mw_burst_im, 20)
save('mewtwo', mw_tiles, mw_pals)
for (nm, tm) in (('lab', mw_lab_tm), ('crack', mw_crack_tm), ('page', mw_page_tm), ('burst', mw_burst_tm)):
    open(OUT + 'route_mewtwo_%s.bin' % nm, 'wb').write(struct.pack('<%dH' % len(tm), *tm))
# ------------------------------------------------------------------ Giratina: het scherm scheurt, de wereld klapt
# ondersteboven de Distortion World in en de zes schaduwvleugels (Origin Forme) sluiten het beeld af.
# route_giratina.png (tiles), _crack.bin (30x20 tilemap van de scheuren) + _crack_t.bin (u8: frame waarop een vak
# zichtbaar wordt, 255 = nooit), _wing.bin (30x20 tilemap van de linkervleugels; de rechter = 180 graden gedraaid)
GPAL2 = pad([(0, 0, 0), (1, 0, 2), (7, 6, 9), (28, 3, 5), (16, 1, 3), (27, 21, 6), (17, 5, 24), (27, 17, 31), (31, 31, 31)])
gtiles, gidx = [], {}
def gtmap(im, w=30, h=20):
    out = []
    for ty in range(h):
        for tx in range(w):
            t = tuple(im.getpixel((tx * 8 + x, ty * 8 + y)) for y in range(8) for x in range(8))
            if not any(t):
                out.append(0); continue
            if t not in gidx:
                gidx[t] = len(gtiles) + 1; gtiles.append(list(t))
            out.append(gidx[t])
    return out
# scheuren: vier gekartelde breuklijnen vanuit punten aan de rand, met zijtakken; zwart met paarse gloed
gr = random.Random(487)
crack = Image.new('P', (240, 160), 0)
cd = ImageDraw.Draw(crack)
ctime = [[255] * 30 for _ in range(20)]
segs = []
def crack_line(x, y, ang, length, width, t0, depth):
    pts = [(x, y)]
    for i in range(length):
        ang += gr.uniform(-0.5, 0.5)
        x += math.cos(ang) * 9; y += math.sin(ang) * 9
        pts.append((x, y))
        segs.append((pts[-2], pts[-1], max(1, width - i * width / (length + 2)), t0 + i * 2))
        if depth < 2 and gr.random() < 0.22:
            crack_line(x, y, ang + gr.choice((-1, 1)) * gr.uniform(0.6, 1.1), length // 2, max(1, width * 0.5), t0 + i * 2, depth + 1)
for (sx, sy, a) in [(120, 74, -2.6), (120, 74, 0.4), (120, 74, 2.0), (120, 74, -0.9)]:
    crack_line(sx, sy, a, 16, 5, 0, 0)
for glow in (True, False):
    for (p, q, w, t) in segs:
        if glow:
            cd.line((p, q), fill=6, width=int(w + 4))
        else:
            cd.line((p, q), fill=1, width=int(w))
for (p, q, w, t) in segs:
    for k in range(5):
        px = p[0] + (q[0] - p[0]) * k / 4; py = p[1] + (q[1] - p[1]) * k / 4
        tx, ty = int(px) // 8, int(py) // 8
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if 0 <= tx + dx < 30 and 0 <= ty + dy < 20:
                    ctime[ty + dy][tx + dx] = min(ctime[ty + dy][tx + dx], t)
for y in range(160):                                    # lichte rand langs de gloed
    for x in range(240):
        if crack.getpixel((x, y)) == 6 and any(0 <= x + dx < 240 and 0 <= y + dy < 160 and crack.getpixel((x + dx, y + dy)) == 0
                                               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) and (x + y) % 3:
            crack.putpixel((x, y), 7)
ctm = gtmap(crack)
ct = [ctime[r][c] if ctm[r * 30 + c] else 255 for r in range(20) for c in range(30)]
# linkervleugels: drie zwarte tentakels vanaf de linkerrand, taps toelopend, met rode stekels en een rode punt
wing = Image.new('P', (240, 160), 0)
wd = ImageDraw.Draw(wing)
for (cy, ln, ph) in [(14, 106, 0.0), (66, 112, 1.7), (118, 104, 3.1)]:
    pts = []
    for i in range(60):
        t = i / 59
        x = -6 + t * ln
        y = cy + math.sin(t * 3.0 + ph) * 6 - t * t * 5
        r = 21 * (1 - t) ** 0.7 + 1.5
        pts.append((x, y, r))
    for (x, y, r) in pts:                               # zwart lijf
        wd.ellipse((x - r, y - r, x + r, y + r), fill=1)
    for k, (x, y, r) in enumerate(pts):                 # grijze glans aan de bovenkant
        if r > 3:
            wd.arc((x - r + 1, y - r + 1, x + r - 1, y + r - 1), 200, 300, fill=2)
    for k in range(5, 50, 8):                           # rode stekels aan de bovenkant, naar achteren gericht
        x, y, r = pts[k]
        wd.polygon([(x - 2, y - r + 1), (x + 5, y - r + 1), (x - 6, y - r - 9)], fill=3)
        wd.line(((x + 4, y - r + 1), (x - 6, y - r - 9)), fill=4)
    for k in range(10, 52, 12):                         # en kleinere aan de onderkant
        x, y, r = pts[k]
        wd.polygon([(x - 2, y + r - 1), (x + 4, y + r - 1), (x - 5, y + r + 6)], fill=4)
    for (x, y, r) in pts[-6:]:                          # rode punt
        wd.ellipse((x - r - 1, y - r - 1, x + r + 1, y + r + 1), fill=3)
    x, y, r = pts[-1]
    wd.polygon([(x, y - 3), (x + 12, y), (x, y + 3)], fill=3)
    for k in range(4, 40, 13):                          # gouden ringen (zoals op Giratina's vleugels)
        x, y, r = pts[k]
        wd.line(((x, y - r + 3), (x + 2, y + r - 3)), fill=5, width=2)
# de linkervleugels blijven in de linkerhelft (x < 120); de rechter (180 graden gedraaid) in de rechterhelft, zodat
# ze elkaars tiles nooit afkappen
for y in range(160):
    for x in range(120, 240):
        wing.putpixel((x, y), 0)
wtm = gtmap(wing)
save('giratina', gtiles, [GPAL2])
open(OUT + 'route_giratina_crack.bin', 'wb').write(struct.pack('<600H', *ctm))
open(OUT + 'route_giratina_crack_t.bin', 'wb').write(bytes(min(255, v) for v in ct))
open(OUT + 'route_giratina_wing.bin', 'wb').write(struct.pack('<600H', *wtm))
# ------------------------------------------------------------------ Victini: een grote V in vuur (V-create)
# 1-3 vuurmassa (kleurcyclus), 4-5 vlammentongen (bovenrand van het vuur), 6 vonken; daarna de V zelf
# (240x144, tiles ontdubbeld, tilemap 30x18 in route_victini_v.bin, indexen al opgehoogd)
VPAL = pad([(0, 0, 0), (9, 1, 1), (20, 3, 2), (28, 8, 2), (31, 15, 3), (31, 22, 6), (31, 28, 12), (31, 31, 24),
            (31, 31, 31), (15, 2, 3)])
def fire_px(x, y, v):
    s = math.sin(x * 0.85 + y * 0.5 + v * 2.3) + math.sin(y * 1.1 - x * 0.4 + v * 1.7)
    return 3 + int((s + 2) / 4 * 3.99)          # 3..6
vtiles = [tile(lambda x, y, v=v: fire_px(x, y, v)) for v in range(3)]
def tongue(v):
    def f(x, y):
        top = 7 - int(7 * abs(math.sin(x * 0.55 + v * 1.9)) ** 0.7)
        if y < top:
            return 0
        if y == top:
            return 2
        return min(6, fire_px(x, y, v) + (1 if y > 5 else 0)) if y > top + 1 else 4
    return tile(f)
vtiles += [tongue(0), tongue(1)]
vr = random.Random(494)
vtiles.append(tile(lambda x, y: (7 if vr.random() < 0.5 else 6) if vr.random() < 0.08 else 0))
NFIRE = len(vtiles)

def v_art():
    W_, H_ = 240, 144
    im = Image.new('P', (W_, H_), 0)
    px = im.load()
    rr = random.Random(4940)
    noise = [rr.uniform(-1, 1) for _ in range(512)]
    def nz(k):
        i = int(k) % 511
        f = k - int(k)
        return noise[i] * (1 - f) + noise[i + 1] * f
    segs = [((38, 24), (120, 138), 0), ((202, 24), (120, 138), 1)]
    for y in range(H_):
        for x in range(W_):
            best = None
            for (ax, ay), (bx, by), side in segs:
                dx, dy = bx - ax, by - ay
                L2 = dx * dx + dy * dy
                t = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L2))
                cx, cy = ax + t * dx, ay + t * dy
                d = math.hypot(x - cx, y - cy)
                # buitenkant (weg van het midden): vlammige rand
                outer = (x < cx) if side == 0 else (x > cx)
                w = 21 * (1 - t) + 7
                if outer:
                    w += 5 * (nz(y * 0.35 + side * 200) + 0.6) * (1 - 0.5 * t)
                if t <= 0.0 and y < ay:
                    # bovenkant: vlammentongen omhoog
                    w *= max(0.0, 1 - (ay - y) / (14 + 12 * abs(nz(x * 0.45 + side * 77))))
                rel = d / max(w, 1)
                if best is None or rel < best:
                    best = rel
            if best is None:
                continue
            if best < 0.22:
                c = 8
            elif best < 0.40:
                c = 7
            elif best < 0.60:
                c = 6
            elif best < 0.74:
                c = 5
            elif best < 0.86:
                c = 4
            elif best < 0.95:
                c = 3
            elif best < 1.0:
                c = 2
            elif best < 1.12:
                c = 1
            else:
                continue
            px[x, y] = c
    return im
vim = v_art()
vidx, vmap = {}, []
for ty in range(vim.height // 8):
    for tx in range(30):
        t = tuple(vim.getpixel((tx * 8 + x, ty * 8 + y)) for y in range(8) for x in range(8))
        if not any(t):
            vmap.append(0); continue
        if t not in vidx:
            vidx[t] = len(vtiles) + 1; vtiles.append(list(t))
        vmap.append(vidx[t])
save('victini', vtiles, cycle(VPAL, 4, amp=2))
open(OUT + 'route_victini_v.bin', 'wb').write(struct.pack('<%dH' % len(vmap), *vmap))
print('victini: vuur-tiles', NFIRE, 'V-tiles', len(vtiles) - NFIRE)
# ------------------------------------------------------------------ Jirachi: een wensster tuimelt fladderend over het
# beeld en laat een spoor van fonkelingen achter; dan duikt hij draaiend naar het midden en alles kleurt goudwit.
# BG-tiles: 1-4 fonkelingen (klein/middel/groot/kruis), kleurcyclus = twinkelen. Sprite: de ster met drie wenslabels.
JPAL = [(0, 0, 0), (31, 31, 31), (31, 30, 18), (31, 26, 8), (26, 20, 4), (14, 20, 31), (8, 12, 26)]
def twinkle(size, cross):
    def f(x, y):
        dx, dy = abs(x - 3.5), abs(y - 3.5)
        if dx < 1 and dy < 1:
            return 1
        if cross and dx + dy < size * 0.6 and (dx < 1 or dy < 1):
            return 2
        if (dx < 1 and dy < size) or (dy < 1 and dx < size):
            return 2 if max(dx, dy) < size - 1.2 else 3
        return 0
    return tile(f)
jtiles = [twinkle(2.2, False), twinkle(3.2, False), twinkle(4.1, False), twinkle(4.1, True)]
JCYC = []
for f in range(4):
    p = list(JPAL)
    p[1] = [(31, 31, 31), (31, 31, 24), (28, 28, 31), (31, 31, 28)][f]
    p[2] = [(31, 30, 18), (31, 31, 26), (31, 27, 12), (30, 30, 31)][f]
    p[3] = [(31, 26, 8), (28, 22, 6), (31, 29, 16), (24, 24, 31)][f]
    JCYC.append(pad(p))
save('jirachi', jtiles, JCYC)

# ster-sprite: vijfpuntige gele ster (Jirachi's kop), oranje rand, witte glans, drie blauwe wenslabels aan de bovenste punten
SPAL_J = pad([(0, 0, 0), (31, 31, 31), (31, 30, 14), (31, 25, 4), (24, 14, 2), (12, 6, 2), (14, 20, 31), (8, 12, 26), (20, 26, 31)])
si = Image.new('P', (64, 64), 0)
sd = ImageDraw.Draw(si)
def star_pts(cx, cy, ro, ri, rot=-90):
    pts = []
    for k in range(10):
        a = math.radians(rot + k * 36)
        r_ = ro if k % 2 == 0 else ri
        pts.append((cx + r_ * math.cos(a), cy + r_ * math.sin(a)))
    return pts
# wenslabels: drie korte strookjes die van de bovenste drie punten afhangen
for k in (0, 1, 4):
    a = math.radians(-90 + k * 72)
    px, py = 32 + 20 * math.cos(a), 33 + 20 * math.sin(a)
    sd.polygon([(px - 3, py), (px + 3, py), (px + 4 - 2 * (k == 1), py + 9), (px - 2 - 2 * (k == 4), py + 10)], fill=7)
    sd.polygon([(px - 2, py + 1), (px + 2, py + 1), (px + 2 - 2 * (k == 1), py + 8), (px - 1 - 2 * (k == 4), py + 8)], fill=6)
sd.polygon(star_pts(32, 33, 25, 11), fill=5)
sd.polygon(star_pts(32, 33, 23, 10), fill=4)
sd.polygon(star_pts(32, 33, 21, 9), fill=3)
sd.polygon(star_pts(31, 32, 15, 7), fill=2)
sd.ellipse((25, 24, 31, 30), fill=1)
sd.point([(23, 22), (24, 21)], fill=1)
save_sprite('jirachi_star', si, SPAL_J)

# ------------------------------------------------------------------ Darkrai: nachtmerrierook kruipt van boven en onder
# dicht (als oogleden die zwaar worden), het beeld zakt weg in het donker; dan gaat midden in het zwart één blauw oog
# open boven een rode, gepunte kraag. BG-tiles: 1 zwart, 2-4 rookrand (onder), 5-7 rookrand (boven), 8-9 losse slierten.
DPAL = [(0, 0, 0), (1, 0, 3), (5, 2, 9), (10, 4, 16), (16, 8, 22), (3, 1, 6)]
dr = random.Random(491)
def smoke_edge(up, seed):
    rr = random.Random(seed)
    ph = rr.random() * 6
    def f(x, y):
        yy = 7 - y if up else y                       # afstand vanaf de open kant
        top = 3 + int(2.2 * math.sin(x * 0.85 + ph)) + (1 if rr.random() < 0.15 else 0)
        if yy < top - 1:
            return 0
        if yy == top - 1:
            return 4 if rr.random() < 0.5 else 3
        if yy == top:
            return 3
        return 2 if yy < top + 2 else 1
    return tile(f)
def wisp(seed):
    rr = random.Random(seed)
    def f(x, y):
        d = abs(y - 4 - 1.8 * math.sin(x * 0.9 + seed))
        return 3 if d < 0.8 else (2 if d < 1.6 and rr.random() < 0.7 else 0)
    return tile(f)
dtiles = [tile(lambda x, y: 1)] + [smoke_edge(False, 10 + k) for k in range(3)] + \
         [smoke_edge(True, 20 + k) for k in range(3)] + [wisp(3), wisp(7)]
DCYC = []
for f in range(4):
    p = list(DPAL)
    p[3] = [(10, 4, 16), (12, 5, 18), (11, 4, 17), (9, 3, 15)][f]
    p[4] = [(16, 8, 22), (19, 10, 25), (14, 7, 20), (17, 9, 24)][f]
    DCYC.append(pad(p))
save('darkrai', dtiles, DCYC)

# oog-sprite: amandelvormig blauw oog met spleetpupil onder een witte haarpluk, met daaronder de rode kraag
EPAL = pad([(0, 0, 0), (2, 1, 4), (31, 31, 31), (20, 22, 26), (6, 24, 31), (2, 14, 24), (30, 4, 6), (18, 1, 3), (31, 14, 12), (1, 1, 1)])
ei = Image.new('P', (64, 64), 0)
ed = ImageDraw.Draw(ei)
# rode kraag: een waaier van punten onder het oog
for k in range(-3, 4):
    a = math.radians(90 + k * 22)
    tx, ty = 32 + 30 * math.cos(a) * 1.05, 34 + 26 * math.sin(a)
    bx = 32 + 12 * math.cos(a)
    by = 34 + 10 * math.sin(a)
    perp = (math.cos(a + math.pi / 2) * 6, math.sin(a + math.pi / 2) * 6)
    ed.polygon([(bx - perp[0], by - perp[1]), (tx, ty), (bx + perp[0], by + perp[1])], fill=7)
    ed.polygon([(bx - perp[0] * 0.6, by - perp[1] * 0.6), (tx - math.cos(a) * 3, ty - math.sin(a) * 3), (bx + perp[0] * 0.4, by + perp[1] * 0.4)], fill=6)
ed.ellipse((12, 20, 52, 46), fill=1)                         # zwarte kop achter het oog
# witte haarpluk die vanaf de kruin schuin naar rechtsboven waait
ed.polygon([(12, 30), (16, 20), (28, 13), (44, 9), (62, 2), (54, 14), (40, 20), (24, 24)], fill=3)
ed.polygon([(15, 28), (19, 20), (29, 15), (44, 11), (57, 5), (51, 13), (39, 18), (24, 22)], fill=2)
# oog
eye = [(18, 34), (24, 29), (32, 27), (40, 29), (46, 33), (40, 38), (32, 40), (24, 38)]
ed.polygon(eye, fill=9)
ed.polygon([(20, 34), (25, 30), (32, 28), (39, 30), (44, 33), (39, 37), (32, 38), (25, 37)], fill=5)
ed.ellipse((25, 29, 39, 38), fill=4)
ed.rectangle((31, 29, 33, 38), fill=9)                       # spleetpupil
ed.point([(28, 31), (29, 31), (28, 32)], fill=2)             # glinstering
save_sprite('darkrai_eye', ei, EPAL)


# ------------------------------------------------------------------ Team Rocket: zwarte balken schuiven dicht met een
# rode voorrand, rode snelheidsstrepen schieten over het zwart, en een grote rode R zoomt in en stempelt met een klap.
# BG-tiles: 1 zwart, 2 rode voorrand (balk van links), 3 idem van rechts, 4 streep-lijf, 5 streep-kop, 6 streep-staart
RPAL = pad([(0, 0, 0), (2, 0, 1), (31, 4, 4), (18, 1, 2), (8, 0, 1), (31, 22, 20)])
def rocket_edge(x, y, right):
    d = (7 - x) if right else x                      # 0 = kant van het zwart, 7 = kant van de wereld
    if d <= 3:
        return 1
    return 3 if d == 4 else 2 if d < 7 else 5
def rocket_streak(x, y, part):
    if y in (3, 4):
        if part == 'head':
            return 5 if x >= 5 else 2
        if part == 'tail':
            return 4 if x < 4 else 3
        return 2 if y == 3 else 3
    if y in (2, 5) and part == 'body' and (x + y) % 3 == 0:
        return 4
    return 1
rtiles = [tile(lambda x, y: 1), tile(lambda x, y: rocket_edge(x, y, False)), tile(lambda x, y: rocket_edge(x, y, True)),
          tile(lambda x, y: rocket_streak(x, y, 'body')), tile(lambda x, y: rocket_streak(x, y, 'head')),
          tile(lambda x, y: rocket_streak(x, y, 'tail'))]
save('rocket', rtiles, [RPAL])

# de R (64x64-sprite, in het spel 2x geschaald): rood met lichte bovenrand, donkere schaduwrand en zwarte omlijning
RSPAL = pad([(0, 0, 0), (2, 0, 1), (16, 0, 2), (29, 3, 4), (31, 14, 12), (31, 31, 31)])
SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
font = ImageFont.truetype(SERIF, 64)
x0, y0, x1, y1 = font.getbbox('R')
rm = Image.new('1', (64, 64), 0)
ImageDraw.Draw(rm).text(((64 - (x1 - x0)) // 2 - x0, (64 - (y1 - y0)) // 2 - y0), 'R', font=font, fill=1)
assert rm.getbbox()[0] >= 3 and rm.getbbox()[1] >= 3 and rm.getbbox()[2] <= 61 and rm.getbbox()[3] <= 61, rm.getbbox()
ri = Image.new('P', (64, 64), 0)
inR = lambda x, y: 0 <= x < 64 and 0 <= y < 64 and rm.getpixel((x, y))
for y in range(64):
    for x in range(64):
        if inR(x, y):
            if not inR(x + 2, y + 2) or not inR(x + 1, y + 1):
                c = 2                                 # schaduwrand rechtsonder
            elif not inR(x - 1, y - 1) or not inR(x - 2, y):
                c = 4                                 # lichtrand linksboven
            else:
                c = 3
            ri.putpixel((x, y), c)
        elif any(inR(x + dx, y + dy) for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)):
            ri.putpixel((x, y), 1)
save_sprite('rocket_r', ri, RSPAL)


# ------------------------------------------------------------------ Zarude: de jungle groeit dicht, lianen zwiepen naar
# beneden, drie klauwkrassen (op de taiko-slagen van "Battle! Zarude") en dan Zarude's silhouet met rode ogen.
# BG-tiles (palet ZRPAL): 1-4 dicht bladerdek (vol), 5-7 bladrand (met gaten), 8-9 liaan, 10 liaantip,
# daarna de klauwkrassen (3 x 30x20 tilemaps in route_zarude_claws.bin, ontdubbeld) en de dieptekaart
# route_zarude_depth.bin (30x20 u8: hoe ver een vak van de rand ligt; het bladerdek groeit van de rand naar binnen).
ZRPAL = pad([(0, 0, 0), (1, 3, 1), (2, 6, 2), (3, 10, 3), (5, 14, 4), (8, 19, 5), (13, 24, 7), (4, 3, 1), (9, 6, 3),
             (14, 10, 5), (0, 1, 0), (10, 26, 6), (22, 31, 12), (6, 18, 8)])
zr = random.Random(893)


def zleaf_layer(img, n, seed, opaque):
    """Overlappende bladeren (ellipsen met nerf) op een 8x8-tile; opaque = de hele tile gevuld (donkere ondergrond)."""
    rr = random.Random(seed)
    if opaque:
        for y in range(8):
            for x in range(8):
                img[y][x] = 1 if rr.random() < 0.6 else 2
    for _ in range(n):
        cx, cy = rr.uniform(-1, 9), rr.uniform(-1, 9)
        a = rr.uniform(0, math.pi)
        L, Wd = rr.uniform(3.0, 4.6), rr.uniform(1.3, 2.0)
        ca, sa = math.cos(a), math.sin(a)
        shade = rr.choice((3, 4, 4, 5))
        for y in range(8):
            for x in range(8):
                u = (x - cx) * ca + (y - cy) * sa
                v = -(x - cx) * sa + (y - cy) * ca
                if (u / L) ** 2 + (v / Wd) ** 2 <= 1:
                    c = shade
                    if abs(v) < 0.5:
                        c = 13 if shade >= 4 else 2              # nerf
                    elif v < -0.6 and shade < 6:
                        c = shade + 1                            # licht van boven
                    img[y][x] = c
    return img


def ztile(n, seed, opaque):
    img = zleaf_layer([[0] * 8 for _ in range(8)], n, seed, opaque)
    return [img[y][x] for y in range(8) for x in range(8)]


zr_tiles = [ztile(5, 10 + k, True) for k in range(4)] + [ztile(3, 30 + k, False) for k in range(3)]


def zvine(x, y, seed):
    rr = random.Random(seed)
    sx = 3 + int(round(1.2 * math.sin(y * 0.8 + seed)))
    if x in (sx, sx + 1):
        return 8 if x == sx else 7
    if (y + seed) % 4 == 0 and x in (sx + 2, sx + 3, sx + 4):
        return 6 if x != sx + 4 else 5                          # blaadje rechts
    if (y + seed) % 4 == 2 and x in (sx - 1, sx - 2, sx - 3):
        return 5 if x != sx - 3 else 4                          # blaadje links
    return 0


zr_tiles += [tile(lambda x, y: zvine(x, y, 1)), tile(lambda x, y: zvine(x, y, 3)),
             tile(lambda x, y: (zvine(x, y, 1) if y < 4 else (5 if 2 <= x <= 5 and y < 7 and abs(x - 3.5) < 7 - y else 0)))]
NZ = len(zr_tiles)                                               # 10: de klauwtiles beginnen bij 11

# dieptekaart: 0 = hoek, ~240 = midden, met wat ruis zodat de bladrand rafelig binnenkomt
zdepth = []
for r in range(20):
    for c in range(30):
        dx, dy = (c + 0.5 - 15) / 15, (r + 0.5 - 10) / 10
        d = (1.45 - math.sqrt(dx * dx + dy * dy)) * 168 + zr.uniform(-14, 14)
        zdepth.append(max(0, min(250, int(d))))
open(OUT + 'route_zarude_depth.bin', 'wb').write(bytes(zdepth))


def zclaw(direction, cx, cy, length, bend):
    """Drie evenwijdige, licht gebogen klauwkrassen (240x160): zwarte scheur met een smalle, giftig groene gloed.
    direction 1 = van rechtsboven naar linksonder, -1 = van linksboven naar rechtsonder; (cx, cy) = midden."""
    im = Image.new('P', (240, 160), 0)
    d = ImageDraw.Draw(im)
    ux, uy = (-0.80, 0.60) if direction > 0 else (0.80, 0.60)       # richting van de kras
    nx, ny = -uy, ux                                                # dwars
    for k in (-1, 0, 1):
        pts = []
        L = length * (0.86 if k else 1.0)
        for i in range(161):
            s = i / 160 - 0.5
            off = k * 17 + bend * (s * s * 4 - 1) * 6
            x = cx + ux * s * L + nx * off + (k * 6 if k else 0) * ux
            y = cy + uy * s * L + ny * off + (k * 6 if k else 0) * uy
            w = 9.0 * math.sin(math.pi * (s + 0.5)) ** 0.7 + 0.6
            pts.append((x, y, w))
        for col, extra in ((11, 1.6), (12, 0.7), (10, 0)):
            for x, y, w in pts:
                rr2 = max(0.5, w / 2 + extra - (0 if col == 10 else 0.6))
                d.ellipse((x - rr2, y - rr2, x + rr2, y + rr2), fill=col)
    return im


zc_idx = {}
zc_maps = []
for direction, cx, cy, length, bend in ((1, 170, 62, 150, 1), (-1, 74, 96, 150, -1), (1, 118, 82, 230, 1)):
    im = zclaw(direction, cx, cy, length, bend)
    m = []
    for ty in range(20):
        for tx in range(30):
            t = tuple(im.getpixel((tx * 8 + x, ty * 8 + y)) for y in range(8) for x in range(8))
            if not any(t):
                m.append(0)
                continue
            if t not in zc_idx:
                zc_idx[t] = NZ + 1 + len(zc_idx)
                zr_tiles.append(list(t))
            m.append(zc_idx[t])
    zc_maps += m
open(OUT + 'route_zarude_claws.bin', 'wb').write(struct.pack('<%dH' % len(zc_maps), *zc_maps))
assert len(zr_tiles) < 760, len(zr_tiles)
save('zarude', zr_tiles, [ZRPAL])

# silhouet-sprite: de front-sprite van Zarude, alles bijna zwart met een donkergroene glans en twee rode ogen
zs = Image.open('graphics/pokemon/zarude/front.png')
zsil = Image.new('P', (64, 64), 0)
for y in range(64):
    for x in range(64):
        zsil.putpixel((x, y), zs.getpixel((x, y)) & 15)
ZSPAL = [(0, 0, 0)] + [(1, 2, 1)] * 15
for i in (7, 9, 13):                                            # groene delen: een vleugje groen in het donker
    ZSPAL[i] = (2, 6, 2)
for i in (14, 15, 2):
    ZSPAL[i] = (0, 0, 0)
ZSPAL[8] = (31, 4, 2)                                           # ogen
ZSPAL[12] = (6, 6, 5)                                           # tanden
save_sprite('zarude_silhouette', zsil, ZSPAL)


# ------------------------------------------------------------------ Loyal Three (Okidogi, Munkidori, Fezandipiti): de
# Poison Chain. Paarse, gloeiende ovale schakels, om en om plat en op hun kant, haken in elkaar en vormen een ketting
# die in een boog over het (donker-paarse) beeld loopt; de schakels komen kort na elkaar op en blijven dan staan.
# route_poisonchain.png (tiles) + route_poisonchain_map.bin: per stap k (1..PC_N) een 30x20 tilemap (u16, met
# flip-bits) met de eerste k schakels. Tiles ook gespiegeld ontdubbeld. 4 paletten: de gloed pulseert licht.
import numpy as np
from scipy import ndimage
from PIL import Image
PC_BASE = [(0, 0, 0), (3, 0, 6), (6, 0, 10), (11, 1, 17), (17, 3, 24), (9, 1, 15), (15, 3, 22), (21, 5, 28),
           (26, 9, 31), (29, 16, 31), (31, 25, 31)]
PC_SS = 3                                                     # supersampling


def pc_curve(s):
    """kwadratische bezier: linksonder buiten beeld -> boog -> rechtsboven buiten beeld"""
    p0, p1, p2 = np.array((-35.0, 170.0)), np.array((75.0, 40.0)), np.array((280.0, 5.0))
    return (1 - s) ** 2 * p0 + 2 * (1 - s) * s * p1 + s * s * p2


ss = np.linspace(0, 1, 4001)
pts = np.array([pc_curve(s) for s in ss])
arc = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(pts, axis=0).T))])
PC_PITCH, PC_LEN, PC_WID, PC_TH = 40.0, 60.0, 36.0, 8.0
links = []
d = 8.0
while d < arc[-1] - 4:
    i = np.searchsorted(arc, d)
    a, b = pts[max(0, i - 3)], pts[min(len(pts) - 1, i + 3)]
    t = (b - a) / np.hypot(*(b - a))
    links.append((pts[i], t))
    d += PC_PITCH
PC_N = len(links)

H, W = 160 * PC_SS, 240 * PC_SS
yy, xx = np.mgrid[0:H, 0:W]
X, Y = (xx + 0.5) / PC_SS, (yy + 0.5) / PC_SS
LIGHT = np.array((-0.6, -0.8))                                 # licht van linksboven


def pc_link(k):
    """(masker, helderheid 0..1, omlijning) van schakel k op supersample-resolutie"""
    (cx, cy), (tx, ty) = links[k]
    u = (X - cx) * tx + (Y - cy) * ty                          # langs de ketting
    v = -(X - cx) * ty + (Y - cy) * tx                         # dwars
    if k % 2 == 0:
        # plat: ovale ring (stadionvorm), buis van dikte PC_TH
        b = PC_WID / 2
        r = b - PC_TH / 2
        half = PC_LEN / 2 - b
        du = np.clip(np.abs(u) - half, 0, None)
        dist = np.hypot(du, v)
        q = dist - r
        inside = np.abs(q) <= PC_TH / 2
        prof = q / (PC_TH / 2)
        w = PC_TH / 2
    else:
        # op zijn kant: smal en langwerpig, met een donkere spleet tussen de twee draden
        w = PC_TH * 0.95
        half = PC_LEN / 2 - w
        du = np.clip(np.abs(u) - half, 0, None)
        dist = np.hypot(du, v)
        inside = dist <= w
        q = dist
        prof = dist / w
    nx = (np.sign(u) * du * tx - v * ty) / np.maximum(dist, 1e-6)
    ny = (np.sign(u) * du * ty + v * tx) / np.maximum(dist, 1e-6)
    lam = (nx * LIGHT[0] + ny * LIGHT[1]) * np.clip(prof, -1, 1)
    bright = 0.3 + 0.45 * lam + 0.35 * np.sqrt(np.clip(1 - prof ** 2, 0, 1))
    if k % 2 == 1:
        slot = (np.abs(u) < half - 1) & (np.abs(v) < 0.9)
        bright = np.where(slot, 0.1, bright)
        outline = dist <= w + 1.2
    else:
        outline = np.abs(q) <= w + 1.2
    return inside, np.clip(bright, 0, 1), outline


PC_LINKS = [pc_link(k) for k in range(PC_N)]


def pc_render(n):
    """beeld (160x240, paletindex) met de eerste n schakels"""
    body = np.zeros((H, W), bool)
    br = np.zeros((H, W))
    ol = np.zeros((H, W), bool)
    # platte ringen eerst, de schakels op hun kant eroverheen (die haken door de ringen)
    for k in [k for k in range(n) if k % 2 == 0] + [k for k in range(n) if k % 2 == 1]:
        ins, b, o = PC_LINKS[k]
        body &= ~(o & ~ins)                                    # rand van de bovenste schakel snijdt de onderste
        ol |= o & ~ins
        br = np.where(ins, b, br)
        body |= ins
        ol &= ~body

    def down(m):
        return m.reshape(160, PC_SS, 240, PC_SS).mean(axis=(1, 3))
    bodyf = down(body.astype(float))
    brf = down(np.where(body, br, 0)) / np.maximum(bodyf, 1e-6)
    olf = down(ol.astype(float))
    img = np.zeros((160, 240), np.uint8)
    solid = bodyf >= 0.5
    edge = (~solid) & (olf >= 0.3)
    dist = ndimage.distance_transform_edt(~(solid | edge))
    img[(dist > 0) & (dist <= 9)] = 2
    img[(dist > 0) & (dist <= 5.5)] = 3
    img[(dist > 0) & (dist <= 2.5)] = 4
    img[edge] = 1
    lv = np.clip((brf * 6).astype(int), 0, 5)
    img[solid] = 5 + lv[solid]
    return img


pc_tiles, pc_idx, pc_maps = [], {}, []


def pc_tile_id(t):
    """tile-index met flip-bits (bit 10 = h, bit 11 = v); 0 = leeg"""
    if not any(t):
        return 0
    a = np.array(t, np.uint8).reshape(8, 8)
    for flip, var in ((0, a), (0x400, a[:, ::-1]), (0x800, a[::-1, :]), (0xC00, a[::-1, ::-1])):
        key = var.tobytes()
        if key in pc_idx:
            return pc_idx[key] | flip
    pc_tiles.append([int(v) for v in t])
    pc_idx[a.tobytes()] = len(pc_tiles)
    return len(pc_tiles)


for n in range(1, PC_N + 1):
    im = pc_render(n)
    for ty in range(20):
        for tx in range(30):
            pc_maps.append(pc_tile_id(tuple(im[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].flatten())))
assert len(pc_tiles) < 760, len(pc_tiles)
open(OUT + 'route_poisonchain_map.bin', 'wb').write(struct.pack('<%dH' % len(pc_maps), *pc_maps))
pc_pals = []
for f in range(4):
    g = [0, 1, 2, 1][f]                                         # gloed: dof, half, fel, half
    pal = list(PC_BASE)
    pal[2] = (6 + g, 0, 10 + 2 * g)
    pal[3] = (11 + 2 * g, 1 + g // 2, 17 + 2 * g)
    pal[4] = (17 + 2 * g, 3 + g, 24 + 2 * g)
    pal[10] = (31, 25 + g * 2, 31)
    pc_pals.append(pad(pal))
save('poisonchain', pc_tiles, pc_pals)
print('poisonchain', PC_N, 'schakels')
