"""Project Grounded: genereert de tiles en paletten voor de route-transities (gevechtsovergangen per gebied).
Per transitie: graphics/battle_transitions/route_<naam>.png (tiles, index 0 = leeg) en route_<naam>.pal
(1 of meer paletten van 16 kleuren). De tilemaps bouwt de code in src/battle_transition.c zelf op.
Gebruik: python3 tools/grounded/route_transitions.py"""
import math, random, struct
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
# ghost van 8x8 tiles (64x64) naar de Lavender Town-sprite: gebochelde zwarte gestalte, boze schuine ogen, brede grijns,
# klauwhandjes met witte vingerlijnen, korrelige grijze aura eromheen; tiles 1-64
PYRE = pad([(0, 0, 0), (1, 1, 2), (8, 8, 9), (16, 16, 17), (31, 31, 31)])
from PIL import ImageDraw, ImageFilter
G = 64
body = Image.new('L', (G, G), 0)
d = ImageDraw.Draw(body)
d.ellipse((11, 3, 53, 43), fill=255)                                    # kop/romp
d.polygon([(13, 26), (51, 26), (55, 52), (48, 58), (40, 54), (32, 60), (24, 54), (16, 58), (9, 52)], fill=255)  # lijf met slierten
d.ellipse((3, 30, 23, 50), fill=255)                                    # linkerhand
d.ellipse((41, 30, 61, 50), fill=255)                                   # rechterhand
face = Image.new('L', (G, G), 0)
f = ImageDraw.Draw(face)
f.polygon([(17, 15), (29, 20), (28, 23), (18, 19)], fill=255)          # linkeroog, schuin naar het midden
f.polygon([(47, 15), (35, 20), (36, 23), (46, 19)], fill=255)          # rechteroog
f.chord((21, 20, 43, 36), 10, 170, fill=255)                            # grijns
f.arc((6, 34, 14, 46), 270, 90, fill=255); f.arc((10, 33, 18, 45), 270, 90, fill=255)   # vingers links
f.arc((50, 34, 58, 46), 90, 270, fill=255); f.arc((46, 33, 54, 45), 90, 270, fill=255)  # vingers rechts
near = body.filter(ImageFilter.MaxFilter(5))
far = body.filter(ImageFilter.MaxFilter(11))
def ghost(x, y):
    if face.getpixel((x, y)) and body.getpixel((x, y)):
        return 4
    if body.getpixel((x, y)):
        return 1
    if near.getpixel((x, y)):
        return 2 if (x + y) % 2 == 0 else 3
    if far.getpixel((x, y)):
        return 3 if (x + y) % 2 == 0 and (x // 2 + y) % 3 else 0
    return 0
pyre = blocks(ghost, 8, 8)
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
# MissingNo: L-vorm (linksboven leeg), blokjes in lila, lichtroze, perzik en zwart; tiles 8-91
SHORT[6:9] = [(16, 13, 19), (30, 28, 30), (29, 21, 15)]
MW, MH = 6 * 8, 14 * 8
rr = random.Random(136)
cells = [[rr.choice((6, 6, 7, 7, 7, 8, 1)) for _ in range(MW // 4)] for _ in range(MH // 4)]
for cy in range(0, MH // 4, 3):              # typische streepjes met stippen
    if rr.random() < 0.5:
        x0 = rr.randint(0, 6)
        for cx in range(x0, min(MW // 4, x0 + 6)):
            cells[cy][cx] = 8 if cx % 2 else 1
def missingno(x, y):
    if x < 16 and y < 56:
        return 0
    return cells[y // 4][x // 4]
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
