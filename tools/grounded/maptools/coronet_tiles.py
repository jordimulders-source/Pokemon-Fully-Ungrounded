"""Project Grounded: tilesets van Mt. Coronet + Spear Pillar (Spacetime Cave, laatste portaal).

  coronet_cave  (secondary) Meteor Falls-tiles (gedeeld, TILES-bestand) met eigen metatiles en paletten: warm grijsbruin
                als de grotten van Mt. Coronet. Achteraan: donkere rotsbovenkant (zoals Chargestone, palet 10) en een
                lichte grotopening (het grotgat in de stalactietenwand op palet 9, de donkere kleuren licht: de
                uitgang naar Spear Pillar).
  coronet_snow  (secondary) Kopie van de sneeuwset (Route 135/136, zelfde metatile-nummers, dus snowlib werkt) zonder
                de huistegels; achteraan getekend (procedureel, op de bestaande paletten 7/8/11): houten bruggetjes
                (oost-west en noord-zuid, water eronder), stenen speerpilaren (2x4, heel en gebroken 2x3) en twee
                altaren (diamant voor Dialga, parel voor Palkia).
Gebruik: python3 tools/grounded/maptools/coronet_tiles.py [voorbeeld.png]   (daarna make)"""
import json, os, random, struct, sys
import numpy as np
from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)

MF = 'data/tilesets/secondary/meteor_falls'
CAVE = 'data/tilesets/secondary/coronet_cave'
SNOW = 'data/tilesets/secondary/snow'
CSNOW = 'data/tilesets/secondary/coronet_snow'
DARK, LIGHT = 10, 9
NAMES = json.load(open(SNOW + '/metatile_names.json'))


def jasc(path):
    L = open(path).read().replace('\r', '').split('\n')[3:19]
    return [tuple(int(v) for v in l.split()) for l in L]


def write_pal(path, cols):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % tuple(c) for c in cols))


def lum(c):
    return 0.30 * c[0] + 0.55 * c[1] + 0.15 * c[2]


def tint(c):
    """Lila Meteor Falls -> warm grijsbruin gesteente (Mt. Coronet)."""
    L = lum(c)
    t = (L * 0.90 + 22, L * 0.78 + 14, L * 0.62 + 8)
    return tuple(int(min(248, max(0, 0.12 * a + 0.88 * b))) for a, b in zip(c, t))


def _tiles_of(png):
    idx = np.array(Image.open(png))
    n = idx.shape[0] // 8 * 16
    return [idx[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8].copy() for i in range(n)]


def _save_tiles(tiles, path, pal_src):
    n = (len(tiles) + 15) // 16 * 16
    img = np.zeros((n // 16 * 8, 128), np.uint8)
    for i, t in enumerate(tiles):
        img[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = t
    im = Image.fromarray(img, 'P')
    im.putpalette(Image.open(pal_src).getpalette())
    im.save(path)


# ============================================================================ coronet_cave
CAVE_HOLE = [(0x245, 0x246, 0x247), (0x24d, 0x24e, 0x24f)]


def build_cave():
    os.makedirs(CAVE + '/palettes', exist_ok=True)
    open(CAVE + '/TILES', 'w').write('meteor_falls\n')
    pals = [jasc(MF + '/palettes/%02d.pal' % i) for i in range(16)]
    out = []
    for i in range(16):
        cols = pals[i]
        if 6 <= i <= 12:
            cols = [cols[0]] + [tint(c) for c in cols[1:]]
        out.append(cols)
    p6 = out[6]
    out[DARK] = [p6[0]] + [tuple(int(v * 0.40) for v in c) for c in p6[1:]]
    # licht palet: het gat zelf is index 15 (alleen in de grotgat-tiles); dat wordt daglicht (warm wit)
    light = list(p6)
    light[15] = (248, 244, 224)
    out[LIGHT] = light
    for i in range(16):
        write_pal(CAVE + '/palettes/%02d.pal' % i, out[i])
    mt = bytearray(open(MF + '/metatiles.bin', 'rb').read())
    at = bytearray(open(MF + '/metatile_attributes.bin', 'rb').read())
    ids = {}
    for key, src_mt, which in (('rockD', 0x201, range(4)), ('lipD', 0x23e, range(4)), ('edgeED', 0x234, range(4)),
                               ('edgeWD', 0x23c, range(4)), ('rimSD', 0x286, (2, 3))):
        e = list(struct.unpack_from('<8H', mt, (src_mt - 512) * 16))
        for i in which:
            if e[i] >> 12 == 6:
                e[i] = (e[i] & 0x0FFF) | (DARK << 12)
        if key == 'rockD':
            e[4:] = [0x1000] * 4
        mt.extend(struct.pack('<8H', *e))
        at.extend(struct.pack('<H', 0))
        ids[key] = [len(mt) // 16 - 1 + 512]
    # lichte grotopening: zelfde tiles, palet 6 -> LIGHT; gedrag van het origineel
    hole = []
    for row in CAVE_HOLE:
        for src_mt in row:
            e = list(struct.unpack_from('<8H', mt, (src_mt - 512) * 16))
            e = [(v & 0x0FFF) | (LIGHT << 12) if v >> 12 == 6 else v for v in e]
            mt.extend(struct.pack('<8H', *e))
            at.extend(struct.pack('<H', struct.unpack_from('<H', at, (src_mt - 512) * 2)[0]))
            hole.append(len(mt) // 16 - 1 + 512)
    ids['lighthole'] = hole
    open(CAVE + '/metatiles.bin', 'wb').write(bytes(mt))
    open(CAVE + '/metatile_attributes.bin', 'wb').write(bytes(at))
    return ids


def cave_ids():
    first = 512 + 159
    out, n = {}, first
    for k, c in (('rockD', 1), ('lipD', 1), ('edgeED', 1), ('edgeWD', 1), ('rimSD', 1), ('lighthole', 6)):
        out[k] = list(range(n, n + c)); n += c
    return out


# ============================================================================ coronet_snow: tekeningen
# palet 8 (kliffen/keien/trappen): 1 b0d0e8, 2 907068, 3 704048, 4 c8e0f0, 6 503040, 8 90a8d8, 10 d8e8f8,
# 11 c8a080, 12 a0b8c8, 13 585860, 14 383028, 15 88a0b0
W_, SN_D, SN_M, SN_L, SN_B = 0, 1, 4, 10, 8
BR, BR_D, BR_DD, TAN = 2, 3, 6, 11
ST_HI, ST_M, ST_D, OUT = 12, 15, 13, 14


def _outline(img, col=OUT):
    out = img.copy()
    h, w = img.shape
    body = img > 0
    for y in range(h):
        for x in range(w):
            if body[y, x]:
                continue
            if any(0 <= y + dy < h and 0 <= x + dx < w and body[y + dy, x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y, x] = col
    return out


def _shade(rel):
    return SN_M if rel < 0.10 else ST_HI if rel < 0.34 else ST_M if rel < 0.72 else ST_D


def _plinth(img, y0, rnd):
    h, w = img.shape
    for y in range(y0, y0 + 12):
        for x in range(3, 29):
            if y < y0 + 3:
                img[y, x] = ST_HI if x < 20 else ST_M
            else:
                img[y, x] = ST_M if y < y0 + 8 else ST_D
                if x in (3, 28):
                    img[y, x] = ST_D
    for x in range(4, 28):                               # sneeuw op de sokkel
        if rnd.random() < 0.7:
            img[y0, x] = SN_L
            if rnd.random() < 0.5:
                img[y0 + 1, x] = SN_M
    for x in range(6, 27, 5):                            # voegen
        for y in range(y0 + 4, y0 + 11):
            img[y, x] = ST_D


def _shaft(img, y0, y1, rnd, top=None):
    for y in range(y0, y1):
        for x in range(9, 23):
            if top is not None and y < top[x - 9]:
                continue
            rel = (x - 9) / 13.0
            v = _shade(rel)
            if x in (12, 16, 20) and v != SN_L:              # cannelures
                v = {ST_HI: ST_M, ST_M: ST_D, ST_D: ST_D}[v]
            img[y, x] = v
    for yb in (y1 - 5, y0 + 4):                              # banden
        for x in range(9, 23):
            if top is None or yb >= top[x - 9]:
                img[yb, x] = TAN if x < 18 else BR
                img[yb + 1, x] = BR if x < 18 else BR_D
    for _ in range(3):                                       # scheurtjes
        x, y = rnd.randint(11, 20), rnd.randint(y0 + 6, y1 - 8)
        for _ in range(rnd.randint(3, 6)):
            if top is None or y >= top[x - 9]:
                img[y, x] = ST_D
            x += rnd.choice((-1, 0, 1)); y += 1


def pillar(seed=1):
    rnd = random.Random(seed)
    img = np.zeros((64, 32), np.uint8)
    for y in range(1, 15):                                   # speerpunt
        half = (y - 1) / 13.0 * 7.0
        for x in range(32):
            d = x - 15.5
            if abs(d) <= half + 0.3:
                img[y, x] = SN_L if d < -half * 0.4 else ST_HI if d < 0 else ST_M if d < half * 0.6 else ST_D
    _shaft(img, 14, 50, rnd)
    _plinth(img, 50, rnd)
    img = _outline(img)
    for x in range(4, 29):                                   # schaduw op de vloer
        if x % 2 == 0:
            img[63, x] = ST_D
    return img


def broken(seed=2):
    rnd = random.Random(seed)
    img = np.zeros((48, 32), np.uint8)
    top = []
    y = 6
    for i in range(14):
        y = max(3, min(11, y + rnd.choice((-2, -1, 0, 1, 2))))
        top.append(y)
    _shaft(img, 3, 34, rnd, top)
    for i, t in enumerate(top):                              # sneeuw op de breuk
        img[t, 9 + i] = SN_L
        if rnd.random() < 0.6:
            img[t + 1, 9 + i] = SN_M
    _plinth(img, 34, rnd)
    img = _outline(img)
    for x in range(4, 29):
        if x % 2 == 0:
            img[47, x] = ST_D
    return img


# palet 7 (blauw, Dialga): 1 80a0e0, 3 5860d0, 4 b0c8e8, 6 506080, 8 70b8f0, 9 6078a8, 10 d8e8f0, 12 7088c8,
#   13 606078, 14 404868, 15 5898c0
# palet 11 (roze, Palkia): 3 808088, 4 c8a8b0, 5 404868, 7 505878, 10 788898, 11 d0e8f0, 13 f8b0b8, 15 a8b8d8
def altar(kind):
    img = np.zeros((32, 32), np.uint8)
    if kind == 'dialga':
        hi, mid, dk, out, g1, g2, g3, gw = 4, 13, 14, 14, 8, 1, 3, 10
    else:
        hi, mid, dk, out, g1, g2, g3, gw = 15, 10, 7, 5, 13, 4, 3, 11
    for y in range(20, 30):                                  # onderste trede
        for x in range(2, 30):
            img[y, x] = hi if y < 22 else mid if y < 27 else dk
    for y in range(13, 20):                                  # bovenste trede
        for x in range(7, 25):
            img[y, x] = hi if y < 15 else mid if y < 18 else dk
    for x in range(9, 23, 4):
        img[16, x] = dk
    if kind == 'dialga':                                     # diamant (ruit)
        for y in range(0, 14):
            half = 6.5 * (1 - abs(y - 6.0) / 7.0)
            for x in range(32):
                d = x - 15.5
                if abs(d) <= half:
                    up = y < 6
                    img[y, x] = gw if (up and d < -half * 0.3) else g1 if up else g2 if d < 0 else g3
        img[3, 13] = img[4, 14] = gw
    else:                                                    # parel
        for y in range(1, 14):
            for x in range(32):
                dx, dy = x - 15.5, y - 7.0
                r = (dx * dx + dy * dy) ** 0.5
                if r <= 5.8:
                    s = -0.6 * dx - 0.8 * dy
                    img[y, x] = gw if s > 2.6 else g1 if s > -1.0 else g2 if s > -3.5 else g3
    img = _outline(img, out)
    for x, y in ((5, 6), (26, 5), (4, 12), (27, 11)):         # glinstering
        img[y, x] = gw
    return img


def bridge(vertical=False):
    img = np.zeros((16, 16), np.uint8)
    for y in range(16):
        for x in range(16):
            if y in (0, 15):
                continue
            if y in (1, 14):
                img[y, x] = OUT
            elif y in (2, 13):
                img[y, x] = BR_D
            else:
                k = x % 4
                img[y, x] = BR_DD if k == 0 else TAN if k == 1 else BR
                if y == 12 and k:
                    img[y, x] = BR_D
    for x in (2, 6, 10, 14):                                 # spijkers
        img[4, x] = ST_HI; img[11, x] = ST_HI
    return img.T.copy() if vertical else img


ART = [  # (naam, tekening, kolommen, rijen, palet, onderlaag (snow-naam), geblokkeerde rijen, bedekt)
    ('bridge_h', lambda: bridge(False), 1, 1, 8, 'water', (), False),
    ('bridge_v', lambda: bridge(True), 1, 1, 8, 'water', (), False),
    ('pillar', pillar, 2, 4, 8, 'path_stone_c', (1, 2, 3), True),
    ('pillar_broken', broken, 2, 3, 8, 'path_stone_c', (1, 2), True),
    ('altar_dialga', lambda: altar('dialga'), 2, 2, 7, 'path_stone_c', (0, 1), True),
    ('altar_palkia', lambda: altar('palkia'), 2, 2, 11, 'path_stone_c', (0, 1), True),
]
DROP = ('house_blue_',)


def build_snow():
    os.makedirs(CSNOW + '/palettes', exist_ok=True)
    for i in range(16):
        write_pal(CSNOW + '/palettes/%02d.pal' % i, jasc(SNOW + '/palettes/%02d.pal' % i))
    tiles = _tiles_of(SNOW + '/tiles.png')
    mt = bytearray(open(SNOW + '/metatiles.bin', 'rb').read())
    at = bytearray(open(SNOW + '/metatile_attributes.bin', 'rb').read())
    nmt = len(mt) // 16
    ents = list(struct.unpack('<%dH' % (len(mt) // 2), mt))
    drop_mt = {NAMES[k] - 512 for k in NAMES if k.startswith(DROP)}
    for m in drop_mt:                                        # huizen eruit (Coronet heeft geen huizen)
        for i in range(8):
            ents[m * 8 + i] = 0
    used = sorted({(e & 0x3FF) - 512 for e in ents if (e & 0x3FF) >= 512} | {0})
    remap = {o: n for n, o in enumerate(used)}
    tiles = [tiles[o] for o in used]
    for i, e in enumerate(ents):
        if (e & 0x3FF) >= 512:
            ents[i] = (e & 0xFC00) | (512 + remap[(e & 0x3FF) - 512])
    mt = bytearray(struct.pack('<%dH' % len(ents), *ents))
    cache = {}
    for i, t in enumerate(tiles):
        cache.setdefault(t.tobytes(), i)

    def tile(t):
        if not t.any():
            return 0, 0
        for fl, v in ((0, t), (1, t[:, ::-1]), (2, t[::-1]), (3, t[::-1, ::-1])):
            if v.tobytes() in cache:
                return cache[v.tobytes()], fl
        tiles.append(t.copy())
        cache[t.tobytes()] = len(tiles) - 1
        return len(tiles) - 1, 0

    names = dict(NAMES)
    for k in list(names):
        if k.startswith(DROP):
            del names[k]
    prev = []
    for key, fn, cols, rows, pal, under, blocked_rows, covered in ART:
        art = fn()
        prev.append((key, art, pal))
        base = struct.unpack_from('<4H', mt, (NAMES[under] - 512) * 16)
        battr = struct.unpack_from('<H', at, (NAMES[under] - 512) * 2)[0]
        for r in range(rows):
            for c in range(cols):
                q = art[r * 16:r * 16 + 16, c * 16:c * 16 + 16]
                top = []
                for sy in (0, 8):
                    for sx in (0, 8):
                        n, fl = tile(q[sy:sy + 8, sx:sx + 8])
                        top.append(0 if n == 0 else ((512 + n) | (fl << 10) | (pal << 12)))
                mt.extend(struct.pack('<8H', *base, *top))
                # COVERED (0x1000): alles onder de speler (brug, sokkels: geen afgekapte hoofden); de bovenste,
                # beloopbare rij van een pilaar is NORMAL, zodat de speler erachter langs loopt
                if key.startswith('bridge'):
                    a = 0x1000                               # gewone grond (loopbaar, geen water)
                else:
                    a = (0x1000 if r in blocked_rows else 0) | (battr & 0xFF)
                at.extend(struct.pack('<H', a))
                names['%s_%d%d' % (key, c, r) if cols * rows > 1 else key] = len(mt) // 16 - 1 + 512
    # stenen Hoenn-trap (General 175/207) met zuidpijl-warp (0x65): de trap van Spear Pillar omlaag naar 6F
    pm = open('data/tilesets/primary/general/metatiles.bin', 'rb').read()
    pa = open('data/tilesets/primary/general/metatile_attributes.bin', 'rb').read()
    for key, src in (('stairs_s_l', 175), ('stairs_s_r', 207)):
        mt.extend(pm[src * 16:src * 16 + 16])
        a = struct.unpack_from('<H', pa, src * 2)[0]
        at.extend(struct.pack('<H', (a & 0xFF00) | 0x65))
        names[key] = len(mt) // 16 - 1 + 512
    assert len(tiles) <= 512, ('te veel tiles', len(tiles))
    assert len(mt) // 16 <= 512
    _save_tiles(tiles, CSNOW + '/tiles.png', SNOW + '/tiles.png')
    open(CSNOW + '/metatiles.bin', 'wb').write(bytes(mt))
    open(CSNOW + '/metatile_attributes.bin', 'wb').write(bytes(at))
    open(CSNOW + '/metatile_names.json', 'w').write(json.dumps(names, indent=1) + '\n')
    print(CSNOW, len(tiles), 'tiles,', len(mt) // 16, 'metatiles')
    return prev


def blocked_rows():
    """{naam: geblokkeerde rijen} voor de kaartscripts."""
    return {k: set(b) for k, _, c, r, _, _, b, _ in ART}


# ============================================================================ spear_pillar (Spear Pillar + Hall of Origin)
# Eigen secondary (Jordi 9 okt: "voller, meer een Gen 3-versie van het origineel"): de sneeuwset van coronet_snow
# (zelfde metatile-nummers, snowlib werkt) zonder bomen/water/paden/huizen, zodat er tiles vrijkomen; paletten 9 en 11
# worden RUIN (zandsteen + grijsgroene pilaren + sneeuw) en LITE (licht, goud, wolken; Hall of Origin, trap van licht).
SPEAR = 'data/tilesets/secondary/spear_pillar'
RUIN, LITE = 9, 11
RUIN_PAL = [(255, 0, 255), (56, 48, 40), (98, 88, 66), (136, 126, 96), (172, 162, 124), (202, 194, 154),
            (230, 224, 192), (76, 80, 72), (116, 120, 104), (158, 162, 144), (204, 208, 190), (232, 240, 248),
            (176, 204, 232), (66, 60, 50), (152, 144, 110), (118, 100, 80)]
RO, RSH, RD, RM, RL, RHI, PD, PM, PL, PHI, SW, SS, PIT, RMD, RBR = range(1, 16)
LITE_PAL = [(255, 0, 255), (72, 80, 128), (136, 168, 224), (184, 208, 248), (226, 236, 250), (248, 248, 248),
            (168, 120, 40), (224, 176, 64), (248, 224, 136), (204, 212, 240), (160, 176, 224), (240, 168, 192),
            (192, 112, 152), (96, 128, 208), (156, 164, 192), (104, 112, 144)]
LO, LSKY, LPALE, LNW, LW, GD, GM, GL, CS, CD, PK, PKD, LDB, LST, LSTD = range(1, 16)
SPEAR_DROP = ('house_blue_', 'pine', 'thinpine', 'htree_', 'water', 'shore_', 'deep_', 'path_pink_', 'path_stone_',
              'flowers_', 'grass_', 'snowman', 'bunny_', 'log', 'bush_', 'stump', 'ice_floor', 'tuft6', 'cave_',
              'cliff_front_fall')
MB_N_ARROW, MB_S_ARROW = 0x64, 0x65


def _hash(*a):
    h = 2166136261
    for v in a:
        h = ((h ^ (v & 0xFFFF)) * 16777619) & 0xFFFFFFFF
    return h


def _brick(gx, gy):
    """Zandstenen bestrating (16x8, verspringend): 'm' voeg, 'h' licht randje, 'b' steen; plus steen-id."""
    band = gy // 8
    off = 8 if band % 2 else 0
    bx, yy = (gx + off) % 16, gy % 8
    bid = (band, (gx + off) // 16)
    if yy == 7 or bx == 15:
        return 'm', bid
    if yy == 0 or bx == 0:
        return 'h', bid
    return 'b', bid


def rfloor(var=0):
    img = np.zeros((16, 16), np.uint8)
    rnd = random.Random(500 + var)
    for y in range(16):
        for x in range(16):
            k, bid = _brick(x, y)
            body = RL
            if var == 1 and bid[0] == 0:
                body = RM                                    # donkerder steen
            if var == 4 and bid[0] == 1:
                body = RMD
            img[y, x] = RD if k == 'm' else RHI if k == 'h' else body
    if var == 2:                                             # scheur
        x, y = 4, 9
        while y < 15 and 0 < x < 15:
            img[y, x] = RD
            x += rnd.choice((0, 1, 1)); y += 1
        img[3, 10] = img[4, 11] = img[4, 12] = RD
    if var == 3:                                             # stippen
        for _ in range(6):
            x, y = rnd.randint(2, 13), rnd.randint(1, 14)
            if img[y, x] == RL:
                img[y, x] = RM
    if var == 5:                                             # sneeuwstof in een hoek
        for y in range(16):
            for x in range(16):
                d = ((x - 3) ** 2 + (y - 12) ** 2) ** 0.5 + rnd.random() * 2.2
                if d < 4.2:
                    img[y, x] = SW
                elif d < 5.6:
                    img[y, x] = SS
    if var == 6:                                             # afgebrokkelde hoek
        for y in range(9, 15):
            for x in range(1, 15 - (y - 9)):
                if x < 6 - (y - 9) // 2:
                    img[y, x] = RSH if y > 9 else RD
    return img


def lfloor(var=0):
    """Hall of Origin: vloer van wit glas met een fijn raster (zoals het platform van Arceus in Platinum)."""
    img = np.full((16, 16), LW, np.uint8)
    for y in range(16):
        for x in range(16):
            if x in (0, 15) or y in (0, 15):
                img[y, x] = LPALE
            elif x in (1, 14) or y in (1, 14):
                img[y, x] = LNW
    if var == 1:
        for (x, y) in ((5, 5), (6, 6), (4, 6), (5, 7), (6, 4)):
            img[y, x] = LNW
        img[5, 5] = LPALE
    if var == 2:
        for i in range(3, 12):
            img[i, i] = LNW
    return img


def lrunner(side):
    """Loper van licht over het glas (gouden rand aan de buitenkant), 1 breed; side 'l' of 'r'."""
    img = lfloor(0)
    for y in range(16):
        for x in range(16):
            if x in (2, 3):
                img[y, x] = GM if x == 2 else GL
            elif x > 3:
                img[y, x] = LPALE if (y % 8) else LNW
            if x > 3 and y % 8 == 4 and x % 4 == 2:
                img[y, x] = LW
    return img if side == 'l' else img[:, ::-1].copy()


def cloud_canvas():
    """32x32, naadloos herhaalbaar: lichtblauwe leegte met wolken (rond de Hall of Origin)."""
    img = np.full((32, 32), LPALE, np.uint8)
    puffs = [(8, 10, 7, 4), (22, 6, 6, 3), (26, 22, 8, 4), (6, 26, 5, 3), (15, 18, 4, 2)]
    for y in range(32):
        for x in range(32):
            best = 9
            for cx, cy, rx, ry in puffs:
                for wx in (-32, 0, 32):
                    for wy in (-32, 0, 32):
                        dx, dy = (x - cx - wx) / rx, (y - cy - wy) / ry
                        d = dx * dx + dy * dy
                        if d < 1:
                            sh = dy + 0.35 * dx                  # licht van linksboven
                            best = min(best, 0 if sh < -0.25 else 1 if sh < 0.45 else 2)
            if best < 9:
                img[y, x] = (LW, LNW, CS)[best]
    for (x, y) in ((3, 3), (17, 28), (29, 13), (12, 2)):    # sterretjes
        img[y, x] = LW
    return img


def _ellipse(img, cx, cy, rx, ry, col_fn):
    h, w = img.shape
    for y in range(h):
        for x in range(w):
            dx, dy = (x - cx) / rx, (y - cy) / ry
            if dx * dx + dy * dy <= 1.0:
                c = col_fn(x, y, dx, dy)
                if c:
                    img[y, x] = c


def _outline_col(img, col):
    return _outline(img, col)


def column(kind='whole', h=4, style='ruin', seed=1):
    """Speerpilaar (2 breed, h hoog). kind: whole (speerpunt), broken (afgebroken), short (stomp)."""
    rnd = random.Random(seed)
    H = 16 * h
    img = np.zeros((H, 32), np.uint8)
    if style == 'ruin':
        f = (PHI, PL, PM, PD); band = (RMD, RD); base = (RHI, RL, RM, RD); snow = (SW, SS); brk = (RHI, RL, RM)
        out = RO
    else:
        f = (LW, LNW, LPALE, LSKY); band = (GL, GM); base = (LW, LNW, LPALE, LST); snow = (LW, LNW); brk = (LW, LNW, LPALE)
        out = LO
    by = H - 9                                                   # midden van de sokkel
    # sokkel: twee ringen (ellips), schaduw eronder
    _ellipse(img, 15.5, by + 2, 14, 5, lambda x, y, dx, dy: base[3] if dy > 0.2 else base[2])
    _ellipse(img, 15.5, by, 12.5, 4.5, lambda x, y, dx, dy: base[0] if dy < -0.35 and dx < 0.3 else base[1]
             if dy < 0.25 else base[2])
    # schacht
    if kind == 'whole':
        top = [14] * 14
    elif kind == 'broken':
        top, y = [], rnd.randint(8, 12)
        for i in range(14):
            y = max(4, min(16, y + rnd.choice((-3, -2, -1, 0, 1, 2, 3))))
            top.append(y)
    else:
        top, y = [], H - 30
        for i in range(14):
            y = max(H - 34, min(H - 24, y + rnd.choice((-2, -1, 0, 1, 2))))
            top.append(y)
    for x in range(9, 23):
        for y in range(top[x - 9], by):
            r = x - 9
            img[y, x] = f[0] if r < 3 else f[1] if r < 7 else f[2] if r < 11 else f[3]
    for yb in (by - 6, top[0] + 5 if kind == 'whole' else by - 14):   # banden
        if yb < by:
            for x in range(9, 23):
                if yb >= top[x - 9]:
                    img[yb, x] = band[0] if x < 17 else band[1]
                    if yb + 1 < by:
                        img[yb + 1, x] = band[1]
    if kind == 'whole':                                          # speerpunt met vier facetten
        for y in range(1, 15):
            half = (y - 1) / 13.0 * 7.0
            for x in range(32):
                d = x - 15.5
                if abs(d) <= half + 0.3:
                    img[y, x] = snow[0] if (y < 4 and d < 0) else f[0] if d < -half * 0.45 else f[1] if d < 0 \
                        else f[2] if d < half * 0.55 else f[3]
    else:                                                        # breukvlak + sneeuw
        for i, t in enumerate(top):
            x = 9 + i
            img[t, x] = snow[0] if rnd.random() < 0.7 else brk[0]
            if t + 1 < by:
                img[t + 1, x] = brk[1] if rnd.random() < 0.6 else snow[1]
            if t + 2 < by and rnd.random() < 0.4:
                img[t + 2, x] = brk[2]
        if kind == 'broken':                                     # brokstuk aan de voet
            for (x, y) in ((25, by - 1), (26, by - 1), (25, by), (26, by), (27, by)):
                img[y, x] = brk[1]
    for _ in range(2 if kind != 'short' else 1):                 # scheurtjes
        x, y = rnd.randint(11, 20), rnd.randint(max(top) + 4, by - 6)
        for _ in range(rnd.randint(3, 6)):
            if y < by and y > top[x - 9]:
                img[y, x] = f[3]
            x = max(9, min(22, x + rnd.choice((-1, 0, 1)))); y += 1
    img = _outline(img, out)
    for x in range(3, 30):                                        # slagschaduw
        if x % 2 == 0 and img[H - 2, x] == 0:
            img[H - 2, x] = RD if style == 'ruin' else LPALE
    return img


def platform_canvas(style):
    """8x6 metatiles: verhoogd platform met afgeschuinde rand, voorkant, trap (kolom 3-4) en bordes eronder.
    Uitsnedes: zie PLATFORM_CUTS."""
    W, H = 128, 96
    img = np.zeros((H, W), np.uint8)
    x0, x1, y0, y1, fy1 = 2, 125, 2, 63, 75
    gx0, gx1 = 48, 79                                             # trapgat
    ruin = style == 'ruin'
    for y in range(H):
        for x in range(W):
            if not (x0 <= x <= x1 and y0 <= y <= fy1):
                continue
            dl, dr, dt, db = x - x0, x1 - x, y - y0, y1 - y
            if y <= y1 and (dl + dt < 3 or dr + dt < 3 or dl + db < 3 or dr + db < 3):
                continue                                          # afgeschuinde hoek
            if gx0 <= x <= gx1 and y >= y1 - 9:
                continue                                          # trapgat (apart getekend)
            if y > y1:                                            # voorkant
                if dl + (y - y1) < 3 or dr + (y - y1) < 3:
                    continue
                yy = y - y1 - 1
                if ruin:
                    row = yy // 6
                    seam = (x + (8 if row % 2 else 0)) % 16 == 0
                    c = RO if yy == 0 else RD if yy % 6 == 5 or seam else RHI if yy % 6 == 0 else RM
                    if x in (gx0 - 1, gx1 + 1) or dl == 0 or dr == 0:
                        c = RO
                else:
                    c = LPALE if yy < 3 else LSKY if yy < 7 else CD if (x + yy) % 2 else LSKY
                    if yy == 0:
                        c = GD
                img[y, x] = c
                continue
            d = min(dl, dr, dt, db)
            side = 'l' if d == dl else 'r' if d == dr else 't' if d == dt else 'b'
            lit = side in ('l', 't')
            if gx0 - 2 <= x < gx0 and y >= y1 - 9 or gx1 < x <= gx1 + 2 and y >= y1 - 9:
                img[y, x] = RO if ruin else GD                    # zijwang naast de trap
                continue
            if d < 10:
                if ruin:
                    if d == 0:
                        c = RO
                    elif d <= 2:
                        c = RHI if lit else RM
                    elif d <= 7:
                        along = y if side in ('l', 'r') else x
                        c = RD if along % 16 == 7 and d in (3, 4, 5, 6, 7) else RL
                    elif d == 8:
                        c = RD if lit else RHI
                    else:
                        c = RSH if lit else RL
                else:
                    if d == 0:
                        c = LO
                    elif d <= 2:
                        c = GL if lit else GM
                    elif d <= 7:
                        along = y if side in ('l', 'r') else x
                        c = LPALE if along % 16 == 7 else LNW
                    elif d == 8:
                        c = GM
                    else:
                        c = GD if lit else GL
                img[y, x] = c
            else:
                if ruin:
                    k, _ = _brick(x, y)
                    img[y, x] = RD if k == 'm' else RHI if k == 'h' else RL
                else:
                    img[y, x] = lfloor(0)[y % 16, x % 16]
    if ruin:                                                      # stenen trap + bordes
        for y in range(y1 - 9, fy1 + 1):
            for x in range(gx0, gx1 + 1):
                k = (y - (y1 - 9)) % 5
                c = RHI if k == 0 else RL if k < 3 else RM if k == 3 else RD
                if x in (gx0, gx1):
                    c = RO
                elif x in (gx0 + 1, gx1 - 1):
                    c = RD
                img[y, x] = c
        for y in range(fy1 + 1, 93):
            for x in range(gx0 + 1, gx1):
                c = RHI if y == fy1 + 1 or x == gx0 + 1 else RD if y == 92 or x == gx1 - 1 else RM
                if y in (84, 88) and gx0 + 6 <= x <= gx1 - 6:
                    c = RD if y == 84 else RHI
                img[y, x] = c
            img[y, gx0] = img[y, gx1] = RO
        for x in range(gx0 + 1, gx1):
            img[93, x] = RO
            if x % 2:
                img[94, x] = SS
        for y in range(fy1 + 1, 76):
            for x in range(x0 + 2, x1 - 1):
                if not (gx0 <= x <= gx1) and img[y, x] == 0 and (x + y) % 2:
                    img[y, x] = SS
    else:
        st = light_stair('mid')
        for y in range(y1 - 9, H):
            for x in range(gx0, gx1 + 1):
                img[y, x] = st[y % 16, x - gx0]
    return img


PLATFORM_CUTS = {'tl': (0, 0), 't': (1, 0), 'tr': (7, 0), 'l': (0, 1), 'r': (7, 1), 'bl': (0, 3), 'b': (1, 3),
                 'bgl': (2, 3), 'stl0': (3, 3), 'str0': (4, 3), 'bgr': (5, 3), 'br': (7, 3), 'fl': (0, 4),
                 'f': (1, 4), 'fgl': (2, 4), 'stl1': (3, 4), 'str1': (4, 4), 'fgr': (5, 4), 'fr': (7, 4),
                 'land_l': (3, 5), 'land_r': (4, 5)}


def light_stair(part='mid'):
    """Trap van licht, 2 breed: gouden leuningen, treden van licht. part: mid, top (gloed), bot (vervaagt)."""
    img = np.zeros((16, 32), np.uint8)
    for y in range(16):
        k = y % 8
        for x in range(32):
            if x in (0, 31):
                c = LO
            elif x in (1, 30):
                c = GD
            elif x in (2, 29):
                c = GM if y % 4 else GL
            else:
                c = LW if k == 0 else LNW if k < 5 else LPALE if k < 7 else LSKY
                if k in (1, 2) and x in (3, 28):
                    c = LPALE
            img[y, x] = c
    if part == 'top':
        for y in range(10):
            for x in range(3, 29):
                d = abs(x - 15.5) / 13.0 + y / 10.0
                if d < 0.8 or (d < 1.05 and (x + y) % 2):
                    img[y, x] = LW
        for x in (8, 15, 16, 23):
            for y in range(0, 6):
                img[y, x] = GL
    if part == 'bot':
        for y in range(9, 16):
            for x in range(3, 29):
                if (x + y) % 2 and y > 11:
                    img[y, x] = LPALE
    return img


def pit_canvas():
    """3x3 metatiles: verzonken stuk vloer (donker), noordwand zichtbaar, lichte rand onderaan."""
    img = np.zeros((48, 48), np.uint8)
    for y in range(48):
        for x in range(48):
            k, _ = _brick(x, y)
            c = RSH if k == 'm' else RMD if k == 'h' else RD
            if y < 6:
                c = (RO, RSH, RD, RD, RSH, RSH)[y] if x % 8 else RO     # noordwand met voegen
            elif x < 2:
                c = RO if x == 0 else RSH
            elif x > 45:
                c = RO if x == 47 else RM
            elif y > 45:
                c = RO if y == 47 else RHI
            elif y < 9 and c != RSH:
                c = PIT if (x + y) % 2 else RSH                          # schaduw van de wand
            img[y, x] = c
    return img


def emblem():
    """2x2: plaquette met de speerpunt (driehoek) in het midden van het plein; de groef loopt erdoor."""
    img = rfloor_canvas(32, 32)
    for y in range(32):
        for x in range(32):
            if y in (7, 8, 9, 10) and (x < 3 or x > 28):
                img[y, x] = (RSH, RD, RMD, RHI)[y - 7]
    for y in range(2, 30):
        for x in range(3, 29):
            e = x in (3, 28) or y in (2, 29)
            img[y, x] = RO if e else RHI if (x == 4 or y == 3) else RD if (x == 27 or y == 28) else RM
    for y in range(7, 25):                                         # driehoek in reliëf
        half = (y - 7) / 17.0 * 10.0
        for x in range(32):
            d = x - 15.5
            if abs(d) <= half:
                inner = abs(d) <= half - 3 and y < 22
                if not inner:
                    img[y, x] = RHI if d < 0 else RD
                elif abs(d) <= half - 4.5 and y < 20:
                    img[y, x] = RL
    return img


def rfloor_canvas(w, h):
    img = np.zeros((h, w), np.uint8)
    for y in range(h):
        for x in range(w):
            k, _ = _brick(x, y)
            img[y, x] = RD if k == 'm' else RHI if k == 'h' else RL
    return img


def groove():
    img = rfloor(0)
    for x in range(16):
        img[7, x], img[8, x], img[9, x], img[10, x] = RSH, RD, RMD, RHI
    return img


def block(seed=3):
    """2x2: ingestort blok zandsteen (zoals de brokken in het zuiden van Spear Pillar)."""
    rnd = random.Random(seed)
    img = np.zeros((32, 32), np.uint8)
    for y in range(3, 30):
        for x in range(2, 30):
            if x - 2 + (y - 3) < 4 or (29 - x) + (y - 3) < 7:
                continue                                           # afgebroken hoeken
            if y < 14:
                c = SW if y < 5 and rnd.random() < 0.7 else RHI if x < 12 else RL
            else:
                c = RM if x < 20 else RD
                if (y - 14) % 7 == 6 or x == 19:
                    c = RSH
            img[y, x] = c
    x, y = 12, 4                                                   # scheur over het blok
    while y < 28:
        img[y, x] = RSH if y >= 14 else RD
        x += rnd.choice((-1, 0, 1)); y += 1
    img = _outline(img, RO)
    for x in range(4, 31):
        if x % 2 and img[31, x] == 0:
            img[31, x] = RSH
    return img


def rubble(seed):
    rnd = random.Random(seed)
    img = np.zeros((16, 16), np.uint8)
    cx, cy, rx, ry = 7.5 + rnd.random(), 9.5, 5.5 + rnd.random(), 4.0
    _ellipse(img, cx, cy, rx, ry, lambda x, y, dx, dy: SW if dy < -0.6 and dx < 0.2 else RHI if dy < -0.2
             else RBR if dy < 0.45 else RD)
    img = _outline(img, RO)
    for x in range(3, 14):
        if x % 2 and img[14, x] == 0:
            img[14, x] = RSH
    return img


def fallen():
    """2x1: omgevallen stuk pilaar."""
    img = np.zeros((16, 32), np.uint8)
    for y in range(3, 14):
        for x in range(2, 30):
            r = y - 3
            img[y, x] = PHI if r < 2 else PL if r < 5 else PM if r < 8 else PD
    for y in range(3, 14):                                         # breukvlakken
        img[y, 2] = img[y, 3] = RL
        img[y, 29] = RHI if y % 3 else RL
    for x in (10, 20):
        for y in range(3, 14):
            img[y, x] = RMD
    img = _outline(img, RO)
    for x in range(3, 31):
        if x % 2 and img[15, x] == 0:
            img[15, x] = RSH
    return img


def dais():
    """4x4: gouden wiel van Arceus in de vloer (symmetrisch, zodat de tiles gespiegeld hergebruikt worden)."""
    img = np.zeros((64, 64), np.uint8)
    for y in range(64):
        for x in range(64):
            img[y, x] = lfloor(0)[y % 16, x % 16]
    c = 31.5
    for y in range(64):
        for x in range(64):
            dx, dy = x - c, y - c
            r = (dx * dx + dy * dy) ** 0.5
            if 26 <= r <= 30.5:
                img[y, x] = GD if r > 29.5 or r < 27 else GM if r > 28.2 else GL
            elif r < 26:
                img[y, x] = LNW if r > 22 else LW
            spoke = (abs(dx) < 3 or abs(dy) < 3) and 8 < r < 27
            if spoke:
                img[y, x] = GD if (abs(dx) > 2 and abs(dy) > 2) or min(abs(dx), abs(dy)) > 2.2 else GM
            if 8 <= r <= 10:
                img[y, x] = GM if r < 9.2 else GD
            if r < 8:
                img[y, x] = LSKY if r > 6 else LPALE if r > 3.5 else LW
    return img


def fountain():
    img = lfloor(0)
    _ellipse(img, 7.5, 8, 7, 6, lambda x, y, dx, dy: GD if dx * dx + dy * dy > 0.7 else LSKY if dy > 0.1 else
             LPALE if dx * dx + dy * dy > 0.15 else LW)
    img[5, 6] = img[6, 7] = LW
    return img


def altar_lite(kind):
    """Altaar (2x2) van wit gesteente met de diamant (Dialga) of parel (Palkia), op palet LITE (bovenlaag)."""
    art = np.zeros((32, 32), np.uint8)
    hi, mid, dk = LW, LST, LSTD
    for y in range(20, 30):
        for x in range(2, 30):
            art[y, x] = hi if y < 22 else mid if y < 27 else dk
    for y in range(13, 20):
        for x in range(7, 25):
            art[y, x] = hi if y < 15 else mid if y < 18 else dk
    for x in range(9, 23, 4):
        art[16, x] = dk
    for x in range(4, 28, 3):
        art[24, x] = GM
    if kind == 'dialga':
        for y in range(0, 14):
            half = 6.5 * (1 - abs(y - 6.0) / 7.0)
            for x in range(32):
                d = x - 15.5
                if abs(d) <= half:
                    up = y < 6
                    art[y, x] = LW if (up and d < -half * 0.3) else LPALE if up else LSKY if d < 0 else LDB
    else:
        for y in range(1, 14):
            for x in range(32):
                dx, dy = x - 15.5, y - 7.0
                if (dx * dx + dy * dy) ** 0.5 <= 5.8:
                    s = -0.6 * dx - 0.8 * dy
                    art[y, x] = LW if s > 2.6 else PK if s > -1.0 else PKD if s > -3.5 else LSTD
    art = _outline(art, LO)
    for x, y in ((5, 6), (26, 5), (4, 12), (27, 11)):
        art[y, x] = GL
    return art


def _full(fn):
    """Volledig getekende tegel (geen onderlaag)."""
    return fn


SPEAR_ART = None


def spear_art():
    """[(naam, tekening, kolommen, rijen, palet, onderlaag (naam of None), loop-achter-rijen, geblokkeerde rijen,
    gedrag)] in volgorde (een onderlaag moet al bestaan). Kolommen/rijen > 1: namen naam_cr."""
    pc = platform_canvas('ruin')
    lc = platform_canvas('lite')
    pit = pit_canvas()
    cl = cloud_canvas()

    def cut(c, col, row, w=1, h=1):
        return lambda: c[row * 16:(row + h) * 16, col * 16:(col + w) * 16].copy()
    art = []
    for v in range(7):
        art.append(('rfloor%d' % v, (lambda v=v: rfloor(v)), 1, 1, RUIN, None, (), (), 0))
    art.append(('rgroove', groove, 1, 1, RUIN, None, (), (), 0))
    for v in range(3):
        art.append(('lfloor%d' % v, (lambda v=v: lfloor(v)), 1, 1, LITE, None, (), (), 0))
    art.append(('cloud', lambda: cl.copy(), 2, 2, LITE, None, (), (0, 1), 0))
    art.append(('lrun_l', lambda: lrunner('l'), 1, 1, LITE, None, (), (), 0))
    art.append(('lrun_r', lambda: lrunner('r'), 1, 1, LITE, None, (), (), 0))
    for k, (c, r) in PLATFORM_CUTS.items():
        walk = k.startswith(('st', 'land'))
        art.append(('rim_' + k, cut(pc, c, r), 1, 1, RUIN, 'snow', (), () if walk else (0,), 0))
        if k != 'land_l' and k != 'land_r':
            art.append(('lrim_' + k, cut(lc, c, r), 1, 1, LITE, 'cloud_00', (), () if walk else (0,), 0))
    for k, (c, r) in {'tl': (0, 0), 't': (1, 0), 'tr': (2, 0), 'l': (0, 1), 'c': (1, 1), 'r': (2, 1),
                      'bl': (0, 2), 'b': (1, 2), 'br': (2, 2)}.items():
        art.append(('pit_' + k, cut(pit, c, r), 1, 1, RUIN, None, (), (), 0))
    art.append(('emblem', emblem, 2, 2, RUIN, None, (), (), 0))
    for part, beh in (('mid', 0), ('top', MB_N_ARROW), ('bot', MB_S_ARROW)):
        st = light_stair(part)
        for c in (0, 1):
            art.append(('lstair_%s_%s' % (part, 'lr'[c]), (lambda st=st, c=c: st[:, c * 16:c * 16 + 16].copy()), 1, 1,
                        LITE, None, (), (), beh))
    art += [
        ('rpillar', lambda: column('whole', 4, 'ruin', 11), 2, 4, RUIN, 'rfloor0', (0,), (1, 2, 3), 0),
        ('rpillar_tall', lambda: column('whole', 5, 'ruin', 12), 2, 5, RUIN, 'rfloor0', (0, 1), (2, 3, 4), 0),
        ('rbroken', lambda: column('broken', 4, 'ruin', 13), 2, 4, RUIN, 'rfloor0', (0,), (1, 2, 3), 0),
        ('rbroken_s', lambda: column('broken', 3, 'ruin', 14), 2, 3, RUIN, 'rfloor0', (0,), (1, 2), 0),
        ('rstump', lambda: column('short', 2, 'ruin', 15), 2, 2, RUIN, 'rfloor0', (), (0, 1), 0),
        ('rpillar_s', lambda: column('whole', 4, 'ruin', 11), 2, 4, RUIN, 'snow', (0,), (1, 2, 3), 0),
        ('rbroken_sn', lambda: column('broken', 3, 'ruin', 14), 2, 3, RUIN, 'snow', (0,), (1, 2), 0),
        ('block', block, 2, 2, RUIN, 'rfloor0', (), (0, 1), 0),
        ('rubble0', lambda: rubble(1), 1, 1, RUIN, 'rfloor0', (), (0,), 0),
        ('rubble1', lambda: rubble(2), 1, 1, RUIN, 'rfloor3', (), (0,), 0),
        ('rubble_s', lambda: rubble(3), 1, 1, RUIN, 'snow', (), (0,), 0),
        ('fallen', fallen, 2, 1, RUIN, 'rfloor0', (), (0,), 0),
        ('mpillar', lambda: column('whole', 4, 'lite', 21), 2, 4, LITE, 'lfloor0', (0,), (1, 2, 3), 0),
        ('mbroken', lambda: column('broken', 3, 'lite', 22), 2, 3, LITE, 'lfloor0', (0,), (1, 2), 0),
        ('dais', dais, 4, 4, LITE, None, (), (), 0),
        ('fountain', fountain, 1, 1, LITE, None, (), (0,), 0),
    ]
    for kind in ('dialga', 'palkia'):
        art.append(('altar_r_' + kind, (lambda k=kind: altar_lite(k)), 2, 2, LITE, 'rfloor0', (), (0, 1), 0))
        art.append(('altar_l_' + kind, (lambda k=kind: altar_lite(k)), 2, 2, LITE, 'lfloor0', (), (0, 1), 0))
    return art


def spear_blocked():
    """{naam: geblokkeerde rijen} en {naam: (kolommen, rijen)} voor de kaartscripts."""
    a = spear_art()
    return {k: set(b) for k, _, c, r, _, _, _, b, _ in a}, {k: (c, r) for k, _, c, r, *_ in a}


def build_spear():
    os.makedirs(SPEAR + '/palettes', exist_ok=True)
    for i in range(16):
        cols = jasc(SNOW + '/palettes/%02d.pal' % i)
        if i == RUIN:
            cols = RUIN_PAL
        if i == LITE:
            cols = LITE_PAL
        write_pal(SPEAR + '/palettes/%02d.pal' % i, cols)
    tiles = _tiles_of(SNOW + '/tiles.png')
    mt = bytearray(open(SNOW + '/metatiles.bin', 'rb').read())
    at = bytearray(open(SNOW + '/metatile_attributes.bin', 'rb').read())
    ents = list(struct.unpack('<%dH' % (len(mt) // 2), mt))
    drop_mt = {NAMES[k] - 512 for k in NAMES if k.startswith(SPEAR_DROP)}
    for m in drop_mt:
        for i in range(8):
            ents[m * 8 + i] = 0
    for e in ents:
        if (e & 0x3FF) and e >> 12 in (RUIN, LITE):
            raise SystemExit('spear_pillar: palet %d nog in gebruik' % (e >> 12))
    used = sorted({(e & 0x3FF) - 512 for e in ents if (e & 0x3FF) >= 512} | {0})
    remap = {o: n for n, o in enumerate(used)}
    tiles = [tiles[o] for o in used]
    for i, e in enumerate(ents):
        if (e & 0x3FF) >= 512:
            ents[i] = (e & 0xFC00) | (512 + remap[(e & 0x3FF) - 512])
    mt = bytearray(struct.pack('<%dH' % len(ents), *ents))
    cache = {}
    for i, t in enumerate(tiles):
        cache.setdefault(t.tobytes(), i)

    def tile(t):
        if not t.any():
            return 0, 0
        for fl, v in ((0, t), (1, t[:, ::-1]), (2, t[::-1]), (3, t[::-1, ::-1])):
            if v.tobytes() in cache:
                return cache[v.tobytes()], fl
        tiles.append(t.copy())
        cache[t.tobytes()] = len(tiles) - 1
        return len(tiles) - 1, 0

    names = {k: v for k, v in NAMES.items() if not k.startswith(SPEAR_DROP)}
    names = {k: v for k, v in names.items() if v < 0x2b8}         # coronet-tekeningen (brug, oude pilaren) niet
    prev = []
    for key, fn, cols, rows, pal, under, behind, blocked, beh in spear_art():
        art = fn()
        prev.append((key, art, pal))
        _n0 = len(tiles)
        if under is None:
            base = None
        else:
            base = struct.unpack_from('<4H', mt, (names[under] - 512) * 16)
        for r in range(rows):
            for c in range(cols):
                q = art[r * 16:r * 16 + 16, c * 16:c * 16 + 16]
                lay = []
                for sy in (0, 8):
                    for sx in (0, 8):
                        n, fl = tile(q[sy:sy + 8, sx:sx + 8])
                        lay.append(0 if n == 0 else ((512 + n) | (fl << 10) | (pal << 12)))
                if base is None:
                    mt.extend(struct.pack('<8H', *lay, 0, 0, 0, 0))
                else:
                    mt.extend(struct.pack('<8H', *base, *lay))
                layer = 0 if r in behind else 1                    # NORMAL (loop erachter langs) / COVERED
                at.extend(struct.pack('<H', (layer << 12) | beh))
                names['%s_%d%d' % (key, c, r) if cols * rows > 1 else key] = len(mt) // 16 - 1 + 512
        if os.environ.get('SPEAR_DEBUG'):
            print('  %-16s +%d tiles' % (key, len(tiles) - _n0))
    pm = open('data/tilesets/primary/general/metatiles.bin', 'rb').read()   # Hoenn-trap met zuidpijl (naar 6F)
    pa = open('data/tilesets/primary/general/metatile_attributes.bin', 'rb').read()
    for key, src in (('stairs_s_l', 175), ('stairs_s_r', 207)):
        mt.extend(pm[src * 16:src * 16 + 16])
        a = struct.unpack_from('<H', pa, src * 2)[0]
        at.extend(struct.pack('<H', (a & 0xFF00) | MB_S_ARROW))
        names[key] = len(mt) // 16 - 1 + 512
    assert len(tiles) <= 512, ('spear_pillar: te veel tiles', len(tiles))
    assert len(mt) // 16 <= 512, len(mt) // 16
    _save_tiles(tiles, SPEAR + '/tiles.png', SNOW + '/tiles.png')
    open(SPEAR + '/metatiles.bin', 'wb').write(bytes(mt))
    open(SPEAR + '/metatile_attributes.bin', 'wb').write(bytes(at))
    open(SPEAR + '/metatile_names.json', 'w').write(json.dumps(names, indent=1) + '\n')
    print(SPEAR, len(tiles), 'tiles,', len(mt) // 16, 'metatiles')
    return prev


def spear_preview(out):
    """Alle nieuwe metatiles van spear_pillar (met onderlaag) op een vel."""
    import subprocess
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from PIL import Image
    pals = {}
    for i in range(16):
        pals[i] = jasc(SPEAR + '/palettes/%02d.pal' % i)
    prim = 'data/tilesets/primary/general'
    for i in range(6):
        pals[i] = jasc(prim + '/palettes/%02d.pal' % i)
    st = _tiles_of(SPEAR + '/tiles.png')
    mt = open(SPEAR + '/metatiles.bin', 'rb').read()
    names = json.load(open(SPEAR + '/metatile_names.json'))
    first = min(v for k, v in names.items() if k.startswith('rfloor'))
    n = len(mt) // 16
    ids = list(range(first, n + 512))
    cols = 16
    im = Image.new('RGB', (cols * 18, ((len(ids) + cols - 1) // cols) * 18), (40, 40, 60))
    for i, m in enumerate(ids):
        e = struct.unpack_from('<8H', mt, (m - 512) * 16)
        px = np.zeros((16, 16, 3), np.uint8)
        for layer in (0, 1):
            for q in range(4):
                v = e[layer * 4 + q]
                t = v & 0x3FF
                if t < 512:
                    if layer or t == 0:
                        continue
                    continue
                tl = st[t - 512]
                if v & 0x400:
                    tl = tl[:, ::-1]
                if v & 0x800:
                    tl = tl[::-1]
                pal = pals[v >> 12]
                oy, ox = (q // 2) * 8, (q % 2) * 8
                for y in range(8):
                    for x in range(8):
                        if tl[y, x] or layer == 0:
                            px[oy + y, ox + x] = pal[tl[y, x]] if tl[y, x] else (px[oy + y, ox + x] if layer else pal[0] if False else (200, 220, 240))
        im.paste(Image.fromarray(px), ((i % cols) * 18, (i // cols) * 18))
    im.resize((im.width * 3, im.height * 3), Image.NEAREST).save(out)


# ============================================================================ registratie
TILESETS = [  # (symbool, map, tiles-symbool (None = eigen), omschrijving)
    ('CoronetCave', 'secondary/coronet_cave', 'MeteorFalls', 'Mt. Coronet: Meteor Falls-tiles, grijsbruin + lichte opening'),
    ('CoronetSnow', 'secondary/coronet_snow', None, 'Mt. Coronet: sneeuwset + bruggetjes, speerpilaren, altaren'),
    ('SpearPillar', 'secondary/spear_pillar', None, 'Spear Pillar + Hall of Origin: ruine, pilaren, trap van licht, wolken'),
]


def register():
    gh = open('src/data/tilesets/graphics.h').read()
    mh = open('src/data/tilesets/metatiles.h').read()
    hh = open('src/data/tilesets/headers.h').read()
    for sym, d, tiles_sym, why in TILESETS:
        D = 'data/tilesets/' + d
        tsym = tiles_sym or sym
        if tiles_sym is None and 'gTilesetTiles_%s[]' % sym not in gh:
            gh += '\n// Project Grounded: %s (coronet_tiles.py)\nconst u32 gTilesetTiles_%s[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n' % (why, sym, D)
        if 'gTilesetPalettes_%s[]' % sym not in gh:
            gh += ('\n// Project Grounded: %s (paletten, coronet_tiles.py)\nconst u16 gTilesetPalettes_%s[][16] =\n{\n' % (why, sym)
                   + ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (D, i) for i in range(16)) + '};\n')
        if 'gMetatiles_%s[]' % sym not in mh:
            mh += ('\nconst u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin"); // Project Grounded: %s\n'
                   'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % (sym, D, why, sym, D))
        if 'gTileset_%s =' % sym not in hh:
            hh += ('\nconst struct Tileset gTileset_%s = // Project Grounded: %s (coronet_tiles.py)\n{\n'
                   '    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_%s,\n'
                   '    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n'
                   '    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = NULL,\n};\n'
                   % (sym, why, tsym, sym, sym, sym))
    open('src/data/tilesets/graphics.h', 'w').write(gh)
    open('src/data/tilesets/metatiles.h', 'w').write(mh)
    open('src/data/tilesets/headers.h', 'w').write(hh)


def preview(prev, out):
    pals = {i: jasc(CSNOW + '/palettes/%02d.pal' % i) for i in (7, 8, 11)}
    W = sum(a.shape[1] + 4 for _, a, _ in prev)
    H = max(a.shape[0] for _, a, _ in prev)
    im = Image.new('RGB', (W, H), (60, 70, 90))
    x = 0
    for _, a, p in prev:
        rgb = np.array([[pals[p][v] if v else (60, 70, 90) for v in row] for row in a], np.uint8)
        im.paste(Image.fromarray(rgb), (x, 0)); x += a.shape[1] + 4
    im.resize((W * 4, H * 4), Image.NEAREST).save(out)


def main():
    ids = build_cave()
    assert ids == cave_ids(), (ids, cave_ids())
    prev = build_snow()
    prev_sp = build_spear()
    register()
    if len(sys.argv) > 1:
        preview(prev, sys.argv[1])
        spear_preview(sys.argv[1].replace('.png', '_spear.png'))
    print('klaar')


if __name__ == '__main__':
    main()
