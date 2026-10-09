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


# ============================================================================ registratie
TILESETS = [  # (symbool, map, tiles-symbool (None = eigen), omschrijving)
    ('CoronetCave', 'secondary/coronet_cave', 'MeteorFalls', 'Mt. Coronet: Meteor Falls-tiles, grijsbruin + lichte opening'),
    ('CoronetSnow', 'secondary/coronet_snow', None, 'Mt. Coronet: sneeuwset + bruggetjes, speerpilaren, altaren'),
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
    register()
    if len(sys.argv) > 1:
        preview(prev, sys.argv[1])
    print('klaar')


if __name__ == '__main__':
    main()
