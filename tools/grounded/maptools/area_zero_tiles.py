"""Project Grounded: tilesets van Area Zero (Spacetime Cave-sidequest, Paldea in een andere tijd).

Eén set tiles/metatiles (secondary `area_zero`) en zes paletversies, zodat de krater per laag 'verder ontspoort'
zonder extra tiles:
  area_zero          krater-rand: weelderig groen gras op de plateaus, grijze rotswanden, bleke kristallen
  area_zero_deep     dieper: het groen wordt blauwgroen, de rots lila, de kristallen cyaan/violet
  area_zero_crystal  kristalgrot: indigo vloer, violette wanden, regenboogkristallen
  area_zero_future   toekomst: staalblauw en neon (cyaan/magenta)
  area_zero_past     verleden: rode aarde, oker rots, de kristallen worden barnsteen
  area_zero_tera     Tera-grot: bleek prisma-wit, blauwe en gouden facetten
Primary per versie: area_zero_general[_deep/...] = General met dezelfde kleurtransformatie (alleen paletten; gras,
hoog gras en boompjes van General sluiten zo naadloos aan op de vloer).

Secondary = kopie van Meteor Falls (zelfde metatile-nummers, dus meteor_falls_ext/chargestone.Cave werkt) met
achteraan eigen metatiles (procedureel getekend, behalve de bomen):
  palet 9  (CR) kristallen (1x1, 2x2, 3x3, zuil 1x2), glinsteringen en gloeiende aders (beloopbaar), het portaal
                (beloopbaar, MB_AQUA_HIDEOUT_WARP: draaiend teleporteren), circuitsporen (beloopbaar), de Tera-kern (3x3),
                een kristalprop voor het verzegelde grotgat
  palet 10 (DARK) rotsbovenkant buiten de wanden (zoals Chargestone)
  palet 11 (OB) onderzoeksstation (3x2), beveiligingsterminal (2x2), poortframe (3x2), zwevende metalen kubussen,
                fossielbotten
  palet 12 (FL) bomen uit Ekat's *Floating Cliffs* (twee slanke boompjes 1x2, een ronde boom 3x3) en varens
Gebruik: python3 tools/grounded/maptools/area_zero_tiles.py (area_zero.py roept build() zelf aan)."""
import colorsys, math, os, random, struct, zlib
import numpy as np
from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)

SRC = 'data/tilesets/secondary/meteor_falls'
DST = 'data/tilesets/secondary/area_zero'
GEN = 'data/tilesets/primary/general'
TREES_PNG = 'graphics/grounded/tilesets/ekat/floating_cliffs_trees.png'
EKAT_SHEET = os.environ.get('EKAT_FLOATING', '')     # alleen nodig om TREES_PNG opnieuw uit te knippen
P_CR, P_DARK, P_OB, P_FL = 9, 10, 11, 12
FLOOR_MT = 0x201
NT_SRC = 460
VARIANTS = ['rim', 'deep', 'crystal', 'future', 'past', 'tera']
SUFFIX = {'rim': '', 'deep': '_deep', 'crystal': '_crystal', 'future': '_future', 'past': '_past', 'tera': '_tera'}
MB_AQUA_HIDEOUT_WARP = 0x67


def jasc(path):
    L = open(path).read().replace('\r', '').split('\n')[3:19]
    return [tuple(int(v) for v in l.split()) for l in L]


def write_pal(path, cols):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % tuple(int(v) for v in c) for c in cols))


def q8(c):
    return tuple(int(max(0, min(248, round(v / 8.0) * 8))) for v in c)


# ====================================================================== kleuren
# Rand-basis: Area Zero-groen (helder geelgroen in plaats van Hoenn-blauwgroen) en grijze steen.
GRASS = [(176, 232, 128), (128, 200, 88), (80, 160, 72), (48, 120, 64)]       # licht, midden, donker, diep
STONE = [(196, 196, 188), (156, 156, 156), (112, 114, 124), (72, 74, 92)]       # MF-index 4-7 (licht -> donker)


def mood(v):
    """Kleurtransformatie per laag: (tintkleur, tintsterkte, tintdraaiing in graden, verzadiging, helderheid)."""
    return {'rim': None,
            'deep': ((80, 150, 190), 0.30, 38, 0.95, 0.86),
            'crystal': ((96, 72, 200), 0.42, 120, 1.10, 0.60),
            'future': ((70, 150, 200), 0.55, 90, 0.45, 0.52),
            'past': ((180, 70, 40), 0.42, -75, 1.05, 0.62),
            'tera': ((210, 210, 255), 0.45, 100, 0.55, 1.05)}[v]


def tf(v, c):
    m = mood(v)
    if m is None:
        return q8(c)
    tint, k, rot, sat, val = m
    h, s, vv = colorsys.rgb_to_hsv(*(x / 255.0 for x in c))
    h = (h + rot / 360.0) % 1.0
    s = min(1.0, s * sat)
    vv = min(1.0, vv * val)
    r, g, b = colorsys.hsv_to_rgb(h, s, vv)
    L = 0.30 * r + 0.59 * g + 0.11 * b
    out = [(1 - k) * a * 255 + k * L * t * 1.25 for a, t in zip((r, g, b), tint)]
    return q8(out)


# kristalpalet per laag: 1 omlijning, 2-6 tint A (donker -> licht), 7-9 tint B, 10 wit, 11 gloedkern, 12 zachte gloed,
# 13 diepe schaduw, 14 middentint, 15 accent
def ramp(a, b, n):
    return [tuple(a[i] + (b[i] - a[i]) * t / (n - 1) for i in range(3)) for t in range(n)]


CR = {
    'rim': [(0, 0, 0), (24, 48, 72)] + ramp((40, 104, 136), (208, 248, 248), 5) + ramp((136, 72, 136), (248, 208, 240), 3) +
           [(255, 255, 255), (224, 255, 255), (160, 232, 224), (20, 40, 56), (112, 184, 200), (255, 240, 160)],
    'deep': [(0, 0, 0), (16, 24, 56)] + ramp((24, 88, 128), (168, 248, 248), 5) + ramp((88, 48, 152), (224, 176, 255), 3) +
            [(255, 255, 255), (200, 255, 248), (112, 200, 216), (12, 20, 44), (96, 152, 200), (255, 176, 232)],
    'crystal': [(0, 0, 0), (16, 8, 40)] + ramp((64, 32, 136), (224, 200, 255), 5) + ramp((32, 128, 176), (184, 255, 248), 3) +
               [(255, 255, 255), (255, 216, 248), (200, 120, 232), (12, 8, 32), (136, 104, 216), (255, 144, 200)],
    'future': [(0, 0, 0), (0, 16, 32)] + ramp((0, 72, 104), (176, 255, 255), 5) + ramp((96, 0, 112), (255, 136, 248), 3) +
              [(255, 255, 255), (200, 255, 255), (0, 200, 232), (0, 8, 20), (40, 140, 180), (255, 72, 200)],
    'past': [(0, 0, 0), (40, 12, 0)] + ramp((112, 48, 8), (255, 224, 128), 5) + ramp((112, 24, 16), (255, 136, 88), 3) +
            [(255, 248, 216), (255, 232, 120), (232, 136, 40), (32, 8, 0), (200, 120, 40), (255, 80, 32)],
    'tera': [(0, 0, 0), (24, 32, 80)] + ramp((40, 96, 184), (232, 248, 255), 5) + ramp((152, 104, 16), (255, 240, 160), 3) +
            [(255, 255, 255), (255, 255, 224), (176, 216, 255), (16, 20, 56), (120, 168, 232), (255, 120, 200)],
}
OB = [(0, 0, 0), (24, 24, 32), (248, 248, 248), (216, 220, 228), (168, 172, 184), (120, 124, 140), (72, 76, 92),
      (44, 46, 60), (64, 200, 232), (176, 248, 255), (208, 40, 48), (255, 140, 120), (152, 88, 24), (240, 184, 72),
      (232, 216, 176), (176, 152, 112)]


# ====================================================================== tekenen (index-afbeeldingen, 0 = transparant)
def outline(img, col=1):
    body = img > 0
    out = img.copy()
    h, w = img.shape
    for y in range(h):
        for x in range(w):
            if body[y, x]:
                continue
            if any(0 <= y + dy < h and 0 <= x + dx < w and body[y + dy, x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y, x] = col
    return out


def spikes(w, h, specs, glow=True, seed=0):
    """Kristalspiesen (prisma's): specs = [(x, voet-y, hoogte, halve breedte, scheefheid)], achterste eerst.
    Linkerfacet licht (6/5), rechterfacet donker (4/3), iriserende banden in tint B, witte punt."""
    rnd = random.Random(seed)
    img = np.zeros((h, w), np.uint8)
    for (bx, by, hgt, wid, lean) in specs:
        band = rnd.randint(0, 6)
        for t in range(int(hgt)):
            yy = int(by - t)
            frac = t / hgt
            half = wid * (1 - frac ** 1.5) + 0.35
            xc = bx + lean * t
            for xx in range(int(math.floor(xc - half)), int(math.ceil(xc + half)) + 1):
                if not (0 <= yy < h and 0 <= xx < w) or abs(xx - xc) > half:
                    continue
                rel = (xx - xc) / max(half, 0.5)
                if t >= hgt - 2:
                    v = 10
                elif rel < -0.45:
                    v = 6
                elif rel < 0.05:
                    v = 5
                elif rel < 0.55:
                    v = 4
                else:
                    v = 3
                if (t + band) % 7 in (0, 1) and v in (4, 5):
                    v = 8 if v == 5 else 7
                if (t + band) % 7 == 0 and v == 6:
                    v = 9
                img[yy, xx] = v
    out = outline(img)
    if glow:
        base = max(int(s[1]) for s in specs)
        for y in range(base + 1, min(h, base + 3)):
            for x in range(w):
                if not out[y, x] and (x + y) % 2 == 0 and any(abs(x - s[0]) < s[3] + 3 for s in specs):
                    out[y, x] = 12 if y > base + 1 else 11
    return out


def crystal_small(seed):
    r = random.Random(seed)
    n = r.randint(2, 3)
    specs = sorted([(r.uniform(4.5, 11.5), r.randint(11, 13), r.randint(6, 11), r.uniform(1.6, 2.6), r.uniform(-0.25, 0.25))
                    for _ in range(n)], key=lambda s: -s[2])
    return spikes(16, 16, specs, seed=seed)


def crystal_med(seed):
    r = random.Random(seed)
    specs = [(16 + r.uniform(-2, 2), 26, r.randint(19, 23), 4.2, r.uniform(-0.08, 0.08))]
    for _ in range(5):
        x = r.uniform(6, 26)
        specs.append((x, r.randint(25, 28), r.randint(8, 15), r.uniform(2.0, 3.0), (x - 16) / 40.0))
    specs.sort(key=lambda s: -s[2])
    return spikes(32, 32, specs, seed=seed)


def crystal_large(seed):
    r = random.Random(seed)
    specs = [(24, 40, 36, 6.0, 0.0), (15, 41, 26, 4.5, -0.10), (33, 41, 28, 4.8, 0.10)]
    for _ in range(8):
        x = r.uniform(6, 42)
        specs.append((x, r.randint(40, 44), r.randint(9, 18), r.uniform(2.0, 3.4), (x - 24) / 50.0))
    specs.sort(key=lambda s: -s[2])
    return spikes(48, 48, specs, seed=seed)


def crystal_pillar(seed):
    r = random.Random(seed)
    specs = [(8, 28, 27, 3.6, r.uniform(-0.04, 0.04)), (4, 29, 10, 2.0, -0.12), (12, 29, 12, 2.2, 0.12)]
    return spikes(16, 32, specs, seed=seed)


def sparkle(seed):
    r = random.Random(seed)
    img = np.zeros((16, 16), np.uint8)
    for _ in range(2):
        x, y = r.randint(3, 12), r.randint(3, 12)
        img[y, x] = 10
        for d in (1, 2):
            for dx, dy in ((d, 0), (-d, 0), (0, d), (0, -d)):
                img[y + dy, x + dx] = 11 if d == 1 else 12
    for _ in range(3):
        x, y = r.randint(1, 14), r.randint(1, 14)
        if not img[y, x]:
            img[y, x] = 9
    return img


def vein(seed):
    """Gloeiende ader in de vloer (beloopbaar)."""
    r = random.Random(seed)
    img = np.zeros((16, 16), np.uint8)
    x, y = 0.0, r.uniform(4, 11)
    core = []
    while x < 16:
        core.append((int(x), int(round(y))))
        x += r.uniform(0.6, 1.3); y = min(13.5, max(2.5, y + r.uniform(-1.2, 1.2)))
    if r.random() < 0.7:
        bx, by = core[len(core) // 2]
        d = r.choice((-1, 1))
        for i in range(1, r.randint(3, 6)):
            core.append((bx + i // 2, by + d * i))
    cs = set(core)
    for (cx, cy) in cs:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                xx, yy = cx + dx, cy + dy
                if 0 <= xx < 16 and 0 <= yy < 16 and (xx, yy) not in cs and (xx + yy) % 2 == 0:
                    img[yy, xx] = 12
    for (cx, cy) in cs:
        if 0 <= cx < 16 and 0 <= cy < 16:
            img[cy, cx] = 11 if r.random() < 0.35 else 6
    return img


def circuit(seed):
    """Toekomstvloer (beloopbaar): metalen paneel met neonnaden; naast elkaar vormen ze een raster.
    seed 2: kale plaat, 9: plaat met een chip, 21: plaat met datastromen."""
    img = np.zeros((16, 16), np.uint8)
    img[0, :] = 4; img[:, 0] = 4
    img[15, :] = 3; img[:, 15] = 3
    for k in (0, 15):
        img[k, k] = 10
    img[0, 15] = img[15, 0] = 6
    if seed == 9:
        img[5:11, 5:11] = 14
        img[5, 5:11] = img[10, 5:11] = 6
        img[5:11, 5] = img[5:11, 10] = 6
        for t in range(6, 10, 2):
            img[3:5, t] = 5; img[11:13, t] = 5; img[t, 3:5] = 5; img[t, 11:13] = 5
        img[7:9, 7:9] = 11
    elif seed == 21:
        for y in (4, 8, 12):
            for x in range(2, 14):
                if (x + y // 4 * 3) % 5 != 0:
                    img[y, x] = 5 if x % 3 else 9
        img[8, 13] = 10
    else:
        img[2:14:11, 2:14:11] = 13
    return img


def portal_pad():
    """Draaikolk van licht (beloopbaar, warp)."""
    img = np.zeros((16, 16), np.uint8)
    for y in range(16):
        for x in range(16):
            dx, dy = x - 7.5, (y - 7.5) * 1.25
            r = math.hypot(dx, dy)
            if r > 7.6:
                continue
            a = math.atan2(dy, dx)
            s = (a / (2 * math.pi) * 3 + r / 3.2) % 1.0
            if r > 6.6:
                v = 1
            elif r < 1.6:
                v = 10
            elif s < 0.33:
                v = 6 if r < 4 else 5
            elif s < 0.66:
                v = 9 if r < 4 else 8
            else:
                v = 11 if r < 3 else 3
            img[y, x] = v
    return img


def tera_core(seed=5):
    """Grote Tera-kristal (3x3): zeshoek met driehoekige facetten in beide tinten, witte glinsteringen."""
    img = np.zeros((48, 48), np.uint8)
    cx, cy, R = 23.5, 21.0, 19.5
    pts = [(cx + R * math.cos(math.radians(90 + 60 * i)) * 0.95, cy - R * math.sin(math.radians(90 + 60 * i))) for i in range(6)]
    cols = [6, 9, 4, 8, 5, 7]
    for y in range(48):
        for x in range(48):
            px, py = x + 0.5, y + 0.5
            # binnen de zeshoek?
            inside = True
            for i in range(6):
                (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % 6]
                if (x1 - x0) * (py - y0) - (y1 - y0) * (px - x0) > 0:
                    inside = False
                    break
            if not inside:
                continue
            a = (math.degrees(math.atan2(-(py - cy), px - cx)) - 90) % 360
            k = int(a // 60)
            r = math.hypot(px - cx, py - cy) / R
            v = cols[k]
            if r < 0.42:
                v = [10, 6, 9, 5, 8, 6][k]
            if abs(((a % 60) - 30)) > 28.5 and r > 0.15:
                v = 3
            img[y, x] = v
    for (gx, gy) in ((17, 10), (29, 15), (21, 27), (14, 20)):
        img[gy, gx] = 10
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            img[gy + dy, gx + dx] = 11
    base = spikes(48, 48, [(6, 44, 12, 2.4, -0.15), (11, 45, 8, 2.0, -0.05), (40, 44, 13, 2.6, 0.15),
                           (35, 45, 9, 2.0, 0.05), (24, 46, 6, 3.0, 0.0)], seed=seed)
    out = outline(img)
    mask = base > 0
    out[mask & (out == 0)] = base[mask & (out == 0)]
    for y in range(41, 48):
        for x in range(48):
            if not out[y, x] and (x + y) % 2 == 0 and abs(x - 24) < 20:
                out[y, x] = 12
    return out


def plug(seed=3):
    """Kristalprop in een grotgat (verzegelde Tera-grot)."""
    return spikes(16, 16, [(8, 14, 13, 3.4, 0.0), (4, 15, 9, 2.4, -0.12), (12, 15, 10, 2.4, 0.12)], seed=seed)


# --- objecten (palet OB)
def shade_box(img, x0, y0, w, h, top, front, side, depth=4):
    """Witte module in vogelvlucht: bovenvlak (top), voorvlak (front, onderste depth rijen) en rechterzijkant."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if y >= y0 + h - depth:
                img[y, x] = front
            elif x >= x0 + w - 2:
                img[y, x] = side
            else:
                img[y, x] = top


def lab_station():
    """Onderzoeksstation (3x2): drie witte modules zoals in Area Zero, met naden, ramen en een antenne."""
    img = np.zeros((32, 48), np.uint8)
    shade_box(img, 2, 8, 16, 20, 2, 4, 3, 7)
    shade_box(img, 18, 5, 14, 23, 3, 5, 4, 8)
    shade_box(img, 32, 10, 14, 18, 2, 4, 3, 6)
    for x in range(2, 46):                     # naden en een groene streep zoals op de echte stations
        if img[24, x]:
            img[24, x] = 6
    for (x0, y0) in ((6, 23), (22, 21), (36, 24)):
        img[y0:y0 + 2, x0:x0 + 5] = 8
        img[y0, x0:x0 + 5] = 9
    for y in range(0, 6):
        img[y, 25] = 6
    img[0, 24:27] = 10
    img[1, 25] = 11
    for x in range(2, 46):
        for y in range(28, 31):
            if (x + y) % 2 == 0 and img[y - 3, x]:
                img[y, x] = 7
    return outline(img)


def terminal():
    """Beveiligingsterminal (2x2): monitor met cyaan scherm en een rood oog, sokkel met lampjes."""
    img = np.zeros((32, 32), np.uint8)
    img[3:19, 3:29] = 6
    img[4:18, 4:28] = 5
    img[6:16, 6:26] = 8
    for y in range(6, 16):
        for x in range(6, 26):
            if (y % 3 == 0) and x % 2:
                img[y, x] = 9
    for y in range(8, 14):
        for x in range(12, 20):
            if (x - 15.5) ** 2 / 14 + (y - 10.5) ** 2 / 6 <= 1:
                img[y, x] = 10
    img[10:12, 15:17] = 11
    img[19:22, 12:20] = 6
    img[22:30, 6:26] = 4
    img[22, 6:26] = 3
    img[27:30, 6:26] = 6
    for x in (9, 13, 17, 21):
        img[24:26, x:x + 2] = 10 if x == 21 else 9
    return outline(img)


def gate_frame():
    """Poortframe (3x2): twee metalen pylonen met cyaan lichtstrips en een boog; het midden van de onderste rij blijft
    leeg (daar komt de draaikolk)."""
    img = np.zeros((32, 48), np.uint8)
    for (x0, x1) in ((3, 13), (35, 45)):
        img[6:31, x0:x1] = 5
        img[6:31, x0] = 4
        img[6:31, x1 - 1] = 6
        img[8:29, (x0 + x1) // 2] = 8
        img[9:28:4, (x0 + x1) // 2] = 9
        img[28:31, x0 - 1:x1 + 1] = 6
        img[28, x0 - 1:x1 + 1] = 4
    for x in range(3, 45):
        yy = int(7 - 5 * math.sin(math.pi * (x - 3) / 41))
        img[yy:yy + 3, x] = 4
        img[yy, x] = 3
        img[yy + 3, x] = 6
    img[1:4, 22:26] = 10
    img[2, 23:25] = 11
    out = outline(img)
    out[16:32, 16:32] = 0                       # plek van de draaikolk
    return out


def cube(seed, size=16):
    """Zwevende metalen kubus (toekomst) met cyaan naden en een schaduw eronder."""
    img = np.zeros((size, size), np.uint8)
    s = size - 6 if size == 16 else size - 10
    x0, y0 = (size - s) // 2, 1
    for y in range(y0, y0 + s):
        for x in range(x0, x0 + s):
            img[y, x] = 3 if y < y0 + s * 0.45 else 6 if x > x0 + s * 0.6 else 5
    img[y0 + int(s * 0.45), x0:x0 + s] = 9
    img[y0:y0 + s, x0 + int(s * 0.6)] = 8
    out = outline(img)
    for y in range(size - 3, size):
        for x in range(2, size - 2):
            if (x + y) % 2 == 0 and abs(x - size / 2) < size * 0.32:
                out[y, x] = 7
    return out


def bones():
    """Fossiel skelet (2x1): schedel en ruggengraat met ribben."""
    img = np.zeros((16, 32), np.uint8)
    for x in range(8, 30):
        y = int(8 + 1.5 * math.sin(x / 4.0))
        img[y:y + 2, x] = 14
        if x % 3 == 0 and x < 27:
            img[y - 4:y, x] = 15
            img[y + 2:y + 6, x] = 15
    for y in range(4, 12):
        for x in range(1, 10):
            if ((x - 5) / 4.5) ** 2 + ((y - 8) / 4) ** 2 <= 1:
                img[y, x] = 14
    img[7, 3:5] = 1
    img[10, 2:8:2] = 15
    return outline(img)


# --- flora (Ekat, palet FL)
def cut_trees():
    """Knipt de bomen uit Ekat's Floating Cliffs (bron: EKAT_FLOATING) naar TREES_PNG (RGBA, 112x48):
    x 0-47 ronde boom (kruin 2 rijen + stam met struikrok, het gras eromheen transparant), x 48-79 twee slanke boompjes."""
    src = Image.open(EKAT_SHEET).convert('RGBA')
    a = np.array(src).copy()
    out = np.zeros((48, 112, 4), np.uint8)
    out[0:48, 0:48] = a[256:304, 0:48]
    out[0:32, 48:80] = a[256:288, 48:80]
    # gras rond de stam (rij 288-303) weg: kleuren die in de kruin niet voorkomen en lichtgroen-turkoois zijn
    blk = out[32:48, 0:48]
    for y in range(16):
        for x in range(48):
            r, g, b, al = blk[y, x]
            if al and g > 150 and b > 120 and r < 160:
                blk[y, x] = (0, 0, 0, 0)
    Image.fromarray(out, 'RGBA').save(TREES_PNG)


def flora():
    """Bomen + varens als index-afbeeldingen op één palet van max. 15 kleuren."""
    a = np.array(Image.open(TREES_PNG).convert('RGBA'))
    cols = sorted({tuple(p[:3]) for row in a for p in row if p[3]})
    # varens (eigen tekening) in de bladkleuren van de bomen
    greens = sorted([c for c in cols if c[1] > c[0] and c[1] > c[2]], key=lambda c: int(c[0]) + int(c[1]) + int(c[2]))
    assert len(cols) <= 15, ('te veel boomkleuren', len(cols))
    pal = [(0, 0, 0)] + cols + [(0, 0, 0)] * (15 - len(cols))
    lut = {c: i + 1 for i, c in enumerate(cols)}
    idx = np.zeros(a.shape[:2], np.uint8)
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if a[y, x, 3]:
                idx[y, x] = lut[tuple(a[y, x, :3])]
    big = idx[0:48, 0:48]
    slim1, slim2 = idx[0:32, 48:64], idx[0:32, 64:80]
    dark, mid, light = lut[greens[0]], lut[greens[len(greens) // 2]], lut[greens[-1]]

    def fern(seed):
        r = random.Random(seed)
        img = np.zeros((16, 16), np.uint8)
        for k in range(r.randint(5, 7)):
            ang = math.radians(r.uniform(200, 340))
            L = r.uniform(5, 7.5)
            for t in np.linspace(0, 1, 16):
                x = 8 + math.cos(ang) * L * t
                y = 13 + math.sin(ang) * L * t + 2.2 * t * t
                xi, yi = int(round(x)), int(round(y))
                if 0 <= xi < 16 and 0 <= yi < 16:
                    img[yi, xi] = mid if t < 0.7 else light
                    if 0.2 < t < 0.9 and 0 <= yi + 1 < 16:
                        img[yi + 1, xi] = img[yi + 1, xi] or dark
        return outline(img, dark)
    return pal, big, slim1, slim2, fern(11), fern(23)


# ====================================================================== tileset
def tiles_of(png):
    idx = np.array(Image.open(png))
    n = idx.shape[0] // 8 * 16
    return [idx[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] for i in range(n)]


def rim_pal6(src):
    """MF-palet 6/7 naar de rand-basis: index 1-3 gras (vloer en plateaus), 4-7 grijze steen (wanden), rest grijs."""
    out = list(src)
    out[1], out[2], out[3] = GRASS[0], GRASS[1], GRASS[2]
    out[4:8] = STONE
    for i in range(8, 16):
        c = src[i]
        L = 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]
        out[i] = (L * 0.92 + 8, L * 0.94 + 8, L * 0.96 + 14) if i != 8 else (248, 248, 240)
    return [q8(c) for c in out]


def build():
    """Schrijft tiles.png, metatiles en alle paletversies; geeft {naam: [metatile-nummers]} terug."""
    os.makedirs(DST + '/palettes', exist_ok=True)
    tiles = tiles_of(SRC + '/tiles.png')[:NT_SRC]
    mt = bytearray(open(SRC + '/metatiles.bin', 'rb').read())
    at = bytearray(open(SRC + '/metatile_attributes.bin', 'rb').read())
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
        if not t.any():
            return 0, 0
        for fl, v in ((0, t), (1, t[:, ::-1]), (2, t[::-1]), (3, t[::-1, ::-1])):
            k = v.tobytes()
            if k in cache:
                return cache[k], fl
        tiles.append(t.copy())
        cache[t.tobytes()] = len(tiles) - 1
        return len(tiles) - 1, 0

    def ent(t, pal):
        n, fl = tile(t)
        if n == 0:
            return 0
        return (512 + n) | (fl << 10) | (pal << 12)

    out = {}

    def add(key, art, pal, blocked, walk=False, beh=None, low=None, flip=False):
        """art = index-afbeelding (veelvoud van 16); per 16x16 een metatile met de vloer als onderlaag (of `low`)."""
        rows, cols = art.shape[0] // 16, art.shape[1] // 16
        if flip:
            art = art[:, ::-1]
        ids = []
        for r in range(rows):
            for c in range(cols):
                q = art[r * 16:r * 16 + 16, c * 16:c * 16 + 16]
                top = [ent(q[sy:sy + 8, sx:sx + 8], pal) for sy in (0, 8) for sx in (0, 8)]
                mt.extend(struct.pack('<8H', *(low or floor), *top))
                if beh is not None:
                    a = 0x1000 | beh
                elif blocked:
                    a = 0x1000
                elif walk:
                    a = 0x1000 | (floor_attr & 0xFF)
                else:
                    a = floor_attr
                at.extend(struct.pack('<H', a))
                ids.append(len(mt) // 16 - 1 + 512)
        out[key] = ids

    # donkere rotsbovenkant buiten de wanden (Cave.build van chargestone.py verwacht deze namen)
    for key, src_mt, which in (('rockD', FLOOR_MT, range(4)), ('lipD', 0x23e, range(4)), ('edgeED', 0x234, range(4)),
                               ('edgeWD', 0x23c, range(4)), ('rimSD', 0x286, (2, 3))):
        e = list(struct.unpack_from('<8H', mt, (src_mt - 512) * 16))
        for i in which:
            if e[i] >> 12 == 6:
                e[i] = (e[i] & 0x0FFF) | (P_DARK << 12)
        if key == 'rockD':
            e[4:] = [0x1000] * 4
        mt.extend(struct.pack('<8H', *e))
        at.extend(struct.pack('<H', 0))
        out[key] = [len(mt) // 16 - 1 + 512]
    # kristallen
    for i, sd in enumerate((5, 17, 31)):
        add('crysS%d' % (i + 1), crystal_small(sd), P_CR, True)
    add('crysM1', crystal_med(7), P_CR, True)
    add('crysM2', crystal_med(41), P_CR, True, flip=True)
    add('crysL', crystal_large(13), P_CR, True)
    add('crysP', crystal_pillar(19), P_CR, True)
    for i, sd in enumerate((5, 11)):
        add('spark%d' % (i + 1), sparkle(sd), P_CR, False, walk=True)
    for i, sd in enumerate((3, 14, 27)):
        add('vein%d' % (i + 1), vein(sd), P_CR, False, walk=True)
    for i, sd in enumerate((2, 9, 21)):
        add('circ%d' % (i + 1), circuit(sd), P_CR, False, walk=True)
    add('pad', portal_pad(), P_CR, False, beh=MB_AQUA_HIDEOUT_WARP)
    add('tera', tera_core(), P_CR, True)
    hole = struct.unpack_from('<4H', mt, (0x24e - 512) * 16)
    add('plug', plug(), P_CR, True, low=hole)
    # objecten
    add('station', lab_station(), P_OB, True)
    add('terminal', terminal(), P_OB, True)
    add('gate', gate_frame(), P_OB, True)
    add('cube', cube(1), P_OB, True)
    add('cubeL', cube(2, 32), P_OB, True)
    add('bones', bones(), P_OB, True)
    # flora
    flpal, big, s1, s2, f1, f2 = flora()
    add('treeL', big, P_FL, True)
    add('treeS1', s1, P_FL, True)
    add('treeS2', s2, P_FL, True)
    add('fern1', f1, P_FL, True)
    add('fern2', f2, P_FL, True)
    assert len(tiles) <= 512, ('te veel tiles', len(tiles))
    assert len(mt) // 16 <= 512
    n = (len(tiles) + 15) // 16 * 16
    img = np.zeros((n // 16 * 8, 128), np.uint8)
    for i, t in enumerate(tiles):
        img[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = t
    im = Image.fromarray(img, 'P')
    im.putpalette([v for c in OB for v in c] + [0] * (768 - 48))
    im.save(DST + '/tiles.png')
    import subprocess
    subprocess.run(['tools/gbagfx/gbagfx', DST + '/tiles.png', DST + '/tiles.4bpp'], check=True)
    open(DST + '/metatiles.bin', 'wb').write(bytes(mt))
    open(DST + '/metatile_attributes.bin', 'wb').write(bytes(at))
    # paletten per laag
    mf = {i: jasc(SRC + '/palettes/%02d.pal' % i) for i in range(16)}
    base6, base7 = rim_pal6(mf[6]), rim_pal6(mf[7])
    base8 = rim_pal6(mf[8])
    for v in VARIANTS:
        d = DST + SUFFIX[v]
        os.makedirs(d + '/palettes', exist_ok=True)
        if v != 'rim':
            open(d + '/BASE', 'w').write('area_zero\n')
        for i in range(16):
            if i == 6:
                p = [base6[0]] + [tf(v, c) for c in base6[1:]]
            elif i == 7:
                p = [base7[0]] + [tf(v, c) for c in base7[1:]]
            elif i == 8:
                p = [base8[0]] + [tf(v, c) for c in base8[1:]]
            elif i == P_DARK:
                p6 = [base6[0]] + [tf(v, c) for c in base6[1:]]
                k = 0.80 if v in ('rim', 'deep', 'tera') else 0.55
                p = [p6[0]] + [q8(tuple(x * k for x in c)) for c in p6[1:]]
            elif i == P_CR:
                p = [q8(c) for c in CR[v]]
            elif i == P_OB:
                p = [q8(c) for c in OB]
            elif i == P_FL:
                def fl(c):
                    if v == 'past':
                        return q8((c[0] * 0.8, c[1] * 0.95, c[2] * 0.6))
                    t = tf(v, c)
                    return q8(tuple(0.6 * a + 0.4 * b for a, b in zip(c, t)))
                p = [flpal[0]] + [fl(c) for c in flpal[1:]]
            else:
                p = mf[i]
            write_pal('%s/palettes/%02d.pal' % (d, i), p)
        g = 'data/tilesets/primary/area_zero_general' + SUFFIX[v]
        os.makedirs(g + '/palettes', exist_ok=True)
        open(g + '/BASE', 'w').write('general\n')
        for i in range(16):
            p = jasc(GEN + '/palettes/%02d.pal' % i)
            if i == 2:
                p = list(p)
                p[12], p[13], p[14], p[15] = GRASS[0], GRASS[1], GRASS[2], GRASS[3]
            if i < 6:
                p = [p[0]] + [tf(v, c) for c in p[1:]]
            write_pal('%s/palettes/%02d.pal' % (g, i), p)
    print(DST, len(tiles), 'tiles,', len(mt) // 16, 'metatiles')
    return out


# ====================================================================== trainerfoto's (beveiligings-/alarmsysteem)
def security_pic(path, alarm=False):
    """64x64 trainerfoto: een zwevende beveiligingsdrone van het Zero Lab (achthoekige romp, één grote lens, twee
    armen met sensoren, een antenne). Beveiliging: cyaan lens; alarm: rode lens en waarschuwingsstrepen."""
    pal = [(0, 0, 0), (16, 18, 28), (236, 240, 248), (196, 204, 216), (150, 158, 176), (104, 112, 132), (64, 70, 90),
           (36, 40, 56), (24, 120, 168), (64, 200, 240), (200, 248, 255), (176, 32, 40), (248, 96, 80), (255, 216, 200),
           (240, 200, 56), (40, 44, 52)]
    if alarm:
        pal[8], pal[9], pal[10] = (120, 16, 24), (232, 56, 48), (255, 200, 176)
    img = np.zeros((64, 64), np.uint8)
    cx, cy = 31.5, 27.0
    # romp: achthoek, belicht van linksboven
    for y in range(64):
        for x in range(64):
            dx, dy = x - cx, y - cy
            if max(abs(dx), abs(dy) * 1.15, (abs(dx) + abs(dy) * 1.15) / 1.38) <= 19:
                s = -0.6 * dx / 19 - 0.8 * dy / 22
                img[y, x] = 2 if s > 0.55 else 3 if s > 0.1 else 4 if s > -0.35 else 5
    # paneelnaden
    for y in range(64):
        for x in range(64):
            if img[y, x] and (abs(y - (cy + 9)) < 0.6 or abs(x - cx) < 0.6 and y > cy + 9):
                img[y, x] = 6
    # lens (ring + iris + pupil + glans)
    for y in range(64):
        for x in range(64):
            r = math.hypot(x - cx, (y - cy + 1) * 1.05)
            if r <= 11.5:
                img[y, x] = 7 if r > 10.2 else 6 if r > 8.8 else 8 if r > 5.5 else 9 if r > 2.6 else 10
    for (x, y) in ((27, 21), (28, 21), (27, 22)):
        img[y, x] = 10
    # armen met sensorbollen
    for side in (-1, 1):
        for t in range(8):
            x = int(cx + side * (18 + t))
            y = int(cy + 4 + t * 0.55)
            img[y - 1:y + 2, x] = 5 if t % 4 else 6
        bx, by = int(cx + side * 26.5), int(cy + 10)
        for y in range(by - 4, by + 5):
            for x in range(bx - 4, bx + 5):
                if 0 <= x < 64 and (x - bx) ** 2 + (y - by) ** 2 <= 16:
                    img[y, x] = 9 if (x - bx) ** 2 + (y - by) ** 2 <= 4 else 5
    # antenne + lampje
    for y in range(2, 9):
        img[y, 31:33] = 5
    img[1:3, 30:34] = 11 if alarm else 9
    img[0, 31:33] = 12 if alarm else 10
    # onderkant: stuwer met gloed (zweeft)
    for y in range(int(cy + 19), int(cy + 24)):
        img[y, 25:39] = 6
        img[y, 25] = img[y, 38] = 7
    for y in range(int(cy + 24), 60):
        for x in range(22, 42):
            if (x + y) % 2 == 0 and abs(x - 31.5) < 10 - (y - cy - 24) * 0.9:
                img[y, x] = 9 if y < cy + 28 else 8
    if alarm:                                     # waarschuwingsstrepen op de romp
        for y in range(64):
            for x in range(64):
                if img[y, x] in (2, 3, 4, 5) and y > cy + 10 and ((x + y) // 3) % 2 == 0:
                    img[y, x] = 14
    out = outline(img)
    im = Image.fromarray(out, 'P')
    im.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    im.save(path)


def sym(v, prim=False):
    return 'AreaZero' + ('General' if prim else '') + {'rim': '', 'deep': 'Deep', 'crystal': 'Crystal', 'future': 'Future',
                                                         'past': 'Past', 'tera': 'Tera'}[v]


def register():
    gh = open('src/data/tilesets/graphics.h').read()
    mh = open('src/data/tilesets/metatiles.h').read()
    hh = open('src/data/tilesets/headers.h').read()
    tag = '// Project Grounded: Area Zero (tools/grounded/maptools/area_zero_tiles.py)\n'
    if 'gTilesetTiles_AreaZero[]' not in gh:
        gh = gh.rstrip('\n') + '\n\n' + tag + 'const u32 gTilesetTiles_AreaZero[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n' % DST
    if 'gMetatiles_AreaZero[]' not in mh:
        mh = mh.rstrip('\n') + '\n\n' + tag + 'const u16 gMetatiles_AreaZero[] = INCBIN_U16("%s/metatiles.bin");\n' % DST + \
             'const u16 gMetatileAttributes_AreaZero[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % DST
    for v in VARIANTS:
        for prim in (False, True):
            s = sym(v, prim)
            d = ('data/tilesets/primary/area_zero_general' if prim else DST) + SUFFIX[v]
            if 'gTilesetPalettes_%s[]' % s not in gh:
                gh = gh.rstrip('\n') + '\n\n' + tag + 'const u16 gTilesetPalettes_%s[][16] =\n{\n' % s + \
                     ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (d, i) for i in range(16)) + '};\n'
            if 'gTileset_%s =' % s not in hh:
                tl, mts, cb = ('General', 'General', 'InitTilesetAnim_General') if prim else ('AreaZero', 'AreaZero', 'NULL')
                hh = hh.rstrip('\n') + '\n\n' + tag + 'const struct Tileset gTileset_%s =\n{\n' \
                     '    .isCompressed = TRUE,\n    .isSecondary = %s,\n    .tiles = gTilesetTiles_%s,\n' \
                     '    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n' \
                     '    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = %s,\n};\n' % (
                         s, 'FALSE' if prim else 'TRUE', tl, s, mts, mts, cb)
    open('src/data/tilesets/graphics.h', 'w').write(gh)
    open('src/data/tilesets/metatiles.h', 'w').write(mh)
    open('src/data/tilesets/headers.h', 'w').write(hh)


if __name__ == '__main__':
    if EKAT_SHEET:
        cut_trees()
    ids = build()
    register()
    security_pic('graphics/trainers/front_pics/zero_security.png')
    security_pic('graphics/trainers/front_pics/zero_alarm.png', alarm=True)
    print({k: [hex(x) for x in v] for k, v in ids.items()})
