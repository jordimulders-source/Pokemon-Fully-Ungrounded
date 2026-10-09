"""Project Grounded: tiles voor national_park.py (aangeroepen vanuit main(); niet los draaien).

park_burnt_rustboro  Eigen secondary voor NationalPark_Ruined: de tiles van Rustboro (zelfde nummers, dus dezelfde
                     metatiles) met in een vrij stuk (tiles FIRE_SLOT..) geanimeerd vuur uit de Gen 3-gevechtsanimatie
                     graphics/battle_anims/sprites/fire.png (8 frames, palet 6 = het vuurpalet + houtskool):
                     grote vuurhaarden (2x2), kleine vlammen (1x1) en vlammen op boomkruinen, elk in twee fasen zodat
                     niet alles tegelijk flakkert. src/tileset_anims.c: InitTilesetAnim_ParkBurnt (Rustboro + vuur).
ilex_forest          Eigen secondary voor IlexForest (primary IlexGeneral): zie build_ilex_tiles().
"""
import os, re, struct
from PIL import Image
import jungle_tileset as J

RUST = 'data/tilesets/secondary/rustboro'
BURNT = 'data/tilesets/secondary/park_burnt_rustboro'
GEN = 'data/tilesets/primary/general'
FIRE_PAL = 6
FIRE_SLOT = 320                                  # vrij in Rustboro voor het park (park gebruikt <= 280 en 448+)
FIRE_FRAMES = 8
# groepen in het geanimeerde blok (aaneengesloten): naam -> (eerste tile t.o.v. FIRE_SLOT, breedte, hoogte in tiles)
FIRE_GROUPS = [('big_a', 0, 4, 4), ('big_b', 16, 4, 4), ('small_a', 32, 2, 2), ('small_b', 36, 2, 2),
               ('tree_a', 40, 4, 2), ('tree_b', 48, 4, 2)]
FIRE_TILES = 56
COVERED = 0x1000

GEN_MT = open(GEN + '/metatiles.bin', 'rb').read()


def gen_entry(m):
    return list(struct.unpack_from('<8H', GEN_MT, m * 16))


def fire_palette():
    im = Image.open('graphics/battle_anims/sprites/fire.png')
    p = im.getpalette()[:48]
    cols = [tuple(p[i * 3:i * 3 + 3]) for i in range(16)]
    cols[13:16] = [(48, 40, 40), (88, 80, 72), (136, 128, 120)]          # houtskool / rook
    return [J.q(c) for c in cols]


def fire_frames():
    """8 frames van 32x32 (indexen in het vuurpalet). De witte kern wordt lichtgeel (minder 'lamp')."""
    im = Image.open('graphics/battle_anims/sprites/fire.png')
    px = im.load()
    out = []
    for f in range(FIRE_FRAMES):
        out.append([[{1: 2}.get(px[x, f * 32 + y], px[x, f * 32 + y]) for x in range(32)] for y in range(32)])
    return out


def shrink(fr):
    """32x32 -> 16x16: een pixel als minstens twee van de vier gevuld zijn, de 'koelste' daarvan (rand blijft rood)."""
    o = [[0] * 16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            v = [fr[y * 2 + j][x * 2 + i] for j in (0, 1) for i in (0, 1)]
            v = sorted(c for c in v if c)
            if len(v) >= 2:
                o[y][x] = v[len(v) // 2]
    return o


BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def crown_mask():
    """32x16: welke pixels van de bovenste rij van een losse Hoenn-boom (General 0x1D6/0x1D7) bladerkruin zijn."""
    gt, _ = J.png_tiles(GEN + '/tiles.png')
    m = [[False] * 32 for _ in range(16)]
    for half, mt in ((0, 0x1D6), (1, 0x1D7)):
        e = gen_entry(mt)
        for k in range(4):
            t = gt[e[k] & 0x3FF]
            for y in range(8):
                for x in range(8):
                    sx = 7 - x if e[k] & 0x400 else x
                    sy = 7 - y if e[k] & 0x800 else y
                    m[(k // 2) * 8 + y][half * 16 + (k % 2) * 8 + x] = t[sy][sx] not in (0, 12, 13, 14)
    return m


CROWN = None


def tongues(fa, fb):
    """Vlammen op een boomkruin (32x16): twee kleine vlammen naast elkaar (verschillende frames), binnen het
    silhouet van de kruin en onderaan geditherd uitlopend, zodat de kruin eronder zichtbaar blijft."""
    global CROWN
    CROWN = CROWN or crown_mask()
    a, b = shrink(fa), shrink(fb)
    o = [[0] * 32 for _ in range(16)]
    for y in range(16):
        for x in range(32):
            c = a[y][x] if x < 16 else b[y][x - 16]
            if not c or not CROWN[y][x]:
                continue
            yb = 10 + (0, 2, 1, 3, 2, 0, 1, 3)[(x * 5 + 3) % 8]  # grillige onderrand: de vlam zakt in de kruin
            if y > yb:
                continue
            if y >= yb - 1:
                c = 10 if y == yb - 1 else 11
            o[y][x] = c
    return o


def scorch(fr):
    """Verkoolde grond onder een vuurhaard: lege pixels in een ovaal onderaan worden houtskool (13/14)."""
    o = [r[:] for r in fr]
    h, w = len(fr), len(fr[0])
    for y in range(h):
        for x in range(w):
            if o[y][x]:
                continue
            d = ((x - (w - 1) / 2) / (w * 0.46)) ** 2 + ((y - (h - 2.5)) / (h * 0.16)) ** 2
            if d < 0.55:
                o[y][x] = 13
            elif d < 1.0 and BAYER[y & 3][x & 3] < 8:
                o[y][x] = 14
    return o


def cut(pix, w, h):
    """pixelraster -> lijst van tiles (8x8), rij voor rij."""
    return [[[pix[ty * 8 + y][tx * 8 + x] for x in range(8)] for y in range(8)] for ty in range(h) for tx in range(w)]


def save_png(path, tiles, per_row, pngpal):
    rows = (len(tiles) + per_row - 1) // per_row
    im = Image.new('P', (per_row * 8, rows * 8), 0)
    im.putpalette(pngpal)
    px = im.load()
    for n, t in enumerate(tiles):
        for y in range(8):
            for x in range(8):
                px[(n % per_row) * 8 + x, (n // per_row) * 8 + y] = t[y][x]
    im.save(path)


def write_pal(path, cols):
    J.write_pal(path, cols)


def burnt_tiles(rust_mt_count):
    """Bouwt park_burnt_rustboro (tiles, anim, metatiles, palet 6). Geeft {naam: metatile-id} terug."""
    frames = fire_frames()
    # per frame het hele geanimeerde blok (56 tiles)
    blocks = []
    for f in range(FIRE_FRAMES):
        g = {'big_a': scorch(frames[f]), 'big_b': scorch(frames[(f + 4) % 8]),
             'small_a': scorch(shrink(frames[(f + 2) % 8])), 'small_b': scorch(shrink(frames[(f + 6) % 8])),
             'tree_a': tongues(frames[(f + 1) % 8], frames[(f + 4) % 8]),
             'tree_b': tongues(frames[(f + 5) % 8], frames[(f + 7) % 8])}
        blk = []
        for name, off, w, h in FIRE_GROUPS:
            assert len(blk) == off
            blk += cut(g[name], w, h)
        assert len(blk) == FIRE_TILES
        blocks.append(blk)
    tiles, pngpal = J.png_tiles(RUST + '/tiles.png')
    assert len(tiles) == 512
    # de vrije plek mag door geen enkele Rustboro-metatile die het park gebruikt worden aangeraakt (zie national_park.py)
    for i in range(FIRE_TILES):
        tiles[FIRE_SLOT + i] = blocks[0][i]
    os.makedirs(BURNT + '/anim/fire', exist_ok=True)
    save_png(BURNT + '/tiles.png', tiles, 16, pngpal)
    for f, blk in enumerate(blocks):
        save_png('%s/anim/fire/%d.png' % (BURNT, f), blk, 8, pngpal)
    write_pal('%s/palettes/%02d.pal' % (BURNT, FIRE_PAL), fire_palette())
    if os.path.exists(BURNT + '/BASE'):
        os.remove(BURNT + '/BASE')

    # metatiles: Rustboro (incl. de aanvullingen van national_park.py) + vuur
    mts = bytearray(open(RUST + '/metatiles.bin', 'rb').read())
    att = bytearray(open(RUST + '/metatile_attributes.bin', 'rb').read())
    assert len(mts) // 16 == rust_mt_count
    ids = {}

    def ftile(name, k):
        off = [g for g in FIRE_GROUPS if g[0] == name][0][1]
        return (512 + FIRE_SLOT + off + k) | (FIRE_PAL << 12)

    def add(key, ent, attr):
        ids[key] = 0x200 + len(mts) // 16
        mts.extend(struct.pack('<8H', *ent))
        att.extend(struct.pack('<H', attr))

    dark = list(struct.unpack_from('<8H', mts, (0x363 - 0x200) * 16))
    grounds = {'grass': gen_entry(0x001)[:4], 'tall': gen_entry(0x00D)[:4], 'lawn': dark[:4]}
    for gname, low in grounds.items():
        for ph in 'ab':
            for j in range(2):
                for i in range(2):
                    top = [ftile('big_' + ph, (j * 2 + ty) * 4 + i * 2 + tx) for ty in (0, 1) for tx in (0, 1)]
                    add(('big', gname, ph, i, j), low + top, COVERED)
            add(('small', gname, ph), low + [ftile('small_' + ph, k) for k in range(4)], COVERED)
    # brandende boomkruinen: bovenste rij van een Hoenn-boom (General 0x1D4-0x1D7), vlammen op de bovenlaag
    for m, half in ((0x1D4, 0), (0x1D6, 0), (0x1D5, 1), (0x1D7, 1)):
        low = gen_entry(m)[:4]
        for ph in 'ab':
            top = [ftile('tree_' + ph, ty * 4 + half * 2 + tx) for ty in (0, 1) for tx in (0, 1)]
            add(('tree', m, ph), low + top, 0)
    open(BURNT + '/metatiles.bin', 'wb').write(mts)
    open(BURNT + '/metatile_attributes.bin', 'wb').write(att)
    return ids


# ====================================================================== registratie (headers, graphics, anim)
def set_tileset(sym, ts_dir, callback, metatiles=True):
    """Laat gTileset_<sym> naar eigen tiles (en metatiles) in ts_dir wijzen."""
    gh = open('src/data/tilesets/graphics.h').read()
    if 'gTilesetTiles_%s[]' % sym not in gh:
        i = gh.index('const u16 gTilesetPalettes_%s[][16]' % sym)
        gh = gh[:i] + 'const u32 gTilesetTiles_%s[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n' % (sym, ts_dir) + gh[i:]
        open('src/data/tilesets/graphics.h', 'w').write(gh)
    if metatiles:
        mh = open('src/data/tilesets/metatiles.h').read()
        if 'gMetatiles_%s[]' % sym not in mh:
            mh = mh.rstrip('\n') + '\n\n// Project Grounded: tools/grounded/maptools/national_park_tiles.py\n' \
                 'const u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin");\n' \
                 'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % (sym, ts_dir, sym, ts_dir)
            open('src/data/tilesets/metatiles.h', 'w').write(mh)
    hh = open('src/data/tilesets/headers.h').read()
    m = re.search(r'const struct Tileset gTileset_%s =\s*\{(.*?)\};' % sym, hh, re.S)
    body = m.group(1)
    nb = re.sub(r'\.tiles = \w+', '.tiles = gTilesetTiles_%s' % sym, body)
    if metatiles:
        nb = re.sub(r'\.metatiles = \w+', '.metatiles = gMetatiles_%s' % sym, nb)
        nb = re.sub(r'\.metatileAttributes = \w+', '.metatileAttributes = gMetatileAttributes_%s' % sym, nb)
    nb = re.sub(r'\.callback = \w+', '.callback = %s' % callback, nb)
    hh = hh[:m.start(1)] + nb + hh[m.end(1):]
    open('src/data/tilesets/headers.h', 'w').write(hh)


ANIM_C = '''
// Project Grounded: brandend National Park (tools/grounded/maptools/national_park_tiles.py): Rustboro (fontein) +
// vuur in tiles %d-%d van de secondary, elke 8 frames een stap
static void TilesetAnim_ParkBurnt(u16 timer)
{
    TilesetAnim_Rustboro(timer);
    if (timer %% 8 == 1)
        AppendTilesetAnimToBuffer(gTilesetAnims_ParkBurnt_Fire[(timer / 8) %% ARRAY_COUNT(gTilesetAnims_ParkBurnt_Fire)],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + %d)), %d * TILE_SIZE_4BPP);
}

void InitTilesetAnim_ParkBurnt(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;
    sSecondaryTilesetAnimCallback = TilesetAnim_ParkBurnt;
}
''' % (FIRE_SLOT, FIRE_SLOT + FIRE_TILES - 1, FIRE_SLOT, FIRE_TILES)


def register_anim():
    h = open('include/tileset_anims.h').read()
    if 'InitTilesetAnim_ParkBurnt' not in h:
        h = h.replace('void InitTilesetAnim_Sootopolis(void);\n',
                      'void InitTilesetAnim_Sootopolis(void);\nvoid InitTilesetAnim_ParkBurnt(void); // Project Grounded\n', 1)
        open('include/tileset_anims.h', 'w').write(h)
    c = open('src/tileset_anims.c').read()
    if 'InitTilesetAnim_ParkBurnt' not in c:
        frames = ''.join('const u16 gTilesetAnims_ParkBurnt_Fire_Frame%d[] = INCBIN_U16("%s/anim/fire/%d.4bpp");\n'
                         % (i, BURNT, i) for i in range(FIRE_FRAMES))
        table = 'const u16 *const gTilesetAnims_ParkBurnt_Fire[] = {\n' + ''.join(
            '    gTilesetAnims_ParkBurnt_Fire_Frame%d,\n' % i for i in range(FIRE_FRAMES)) + '};\n'
        anchor = 'const u16 *const gTilesetAnims_Sootopolis_StormyWater[] = {'
        i = c.index(anchor)
        c = c[:i] + '// Project Grounded: vuur in het brandende National Park (national_park_tiles.py)\n' + \
            frames + table + '\n' + c[i:]
        c = c.rstrip('\n') + '\n' + ANIM_C
        open('src/tileset_anims.c', 'w').write(c)


def register_burnt():
    set_tileset('ParkBurntRustboro', BURNT, 'InitTilesetAnim_ParkBurnt')
    register_anim()


# ====================================================================== Ilex Forest: eigen secondary ilex_forest
ILEX_TS = 'data/tilesets/secondary/ilex_forest'
EKAT = 'graphics/grounded/tilesets/ekat/'
FAIRY, HAUNTED = EKAT + 'fairy_woods_ilex.png', EKAT + 'haunted_woods_ilex.png'
# uitsneden (Ekat99: Fairy Woods / Haunted Woods): naam -> (bestand, x, breedte, hoogte); y is altijd 0
DECOR = {
    'big_tree': (FAIRY, 0, 48, 48), 'willow': (FAIRY, 48, 48, 48), 'bush': (FAIRY, 96, 48, 32),
    'bush_pink': (FAIRY, 144, 48, 32), 'bush_blue': (FAIRY, 192, 48, 32), 'small_pine': (FAIRY, 240, 16, 32),
    'flower_pink': (FAIRY, 256, 16, 16), 'flower_blue': (FAIRY, 272, 16, 16), 'flower_mix': (FAIRY, 288, 16, 16),
    'petals_pink': (FAIRY, 304, 16, 16), 'petals_blue': (FAIRY, 320, 16, 16), 'sprout_a': (FAIRY, 336, 16, 16),
    'sprout_b': (FAIRY, 352, 16, 16), 'stump_a': (FAIRY, 368, 16, 16), 'fern_clump': (FAIRY, 384, 16, 16),
    'log_h': (HAUNTED, 0, 48, 16), 'log_v': (HAUNTED, 48, 16, 48), 'stump_b': (HAUNTED, 64, 16, 16),
    'stump_c': (HAUNTED, 80, 16, 16), 'mush_big': (HAUNTED, 96, 16, 16), 'mush_one': (HAUNTED, 112, 16, 16),
    'mush_pair': (HAUNTED, 128, 16, 16), 'mush_sprouts': (HAUNTED, 144, 16, 16),
}
P_SHRINE, P_LIGHT = 6, 11
PAL_GROUPS = {   # palet -> uitsneden die het delen (15 kleuren, median cut)
    7: ['big_tree', 'willow'],
    8: ['bush', 'bush_pink', 'bush_blue', 'small_pine', 'fern_clump', 'sprout_a', 'sprout_b'],
    9: ['log_h', 'log_v', 'stump_a', 'stump_b', 'stump_c', 'mush_big', 'mush_one', 'mush_pair', 'mush_sprouts'],
    10: ['flower_pink', 'flower_blue', 'flower_mix', 'petals_pink', 'petals_blue'],
    12: ['lily'],
}
SHRINE_PAL = [(0, 0, 0), (24, 20, 28), (48, 56, 80), (80, 88, 112), (120, 128, 152),          # 1 omlijning, 2-4 dak
              (80, 44, 28), (128, 76, 44), (176, 116, 68), (216, 164, 104),                    # 5-8 hout
              (64, 64, 72), (112, 112, 120), (168, 168, 168),                                  # 9-11 steen
              (240, 240, 232), (208, 176, 96), (192, 48, 40), (80, 112, 56)]                   # papier, touw, rood, mos


def lily():
    """Twee waterlelieblaadjes en een bloempje (16x16, RGBA)."""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    px = im.load()
    D, M, L, F, W = (32, 88, 48, 255), (64, 136, 64, 255), (112, 184, 88, 255), (232, 136, 176, 255), (248, 224, 232, 255)
    for cx, cy, rx, ry, notch in ((5.5, 10.5, 4.6, 3.2, 1), (11.5, 5.5, 3.6, 2.6, -1)):
        for y in range(16):
            for x in range(16):
                dx, dy = (x - cx) / rx, (y - cy) / ry
                if dx * dx + dy * dy > 1:
                    continue
                if abs(y - cy) < 0.8 and (x - cx) * notch > 0.5:          # inkeping
                    continue
                edge = dx * dx + dy * dy > 0.6
                px[x, y] = D if edge and dy > 0 else (L if dy < -0.3 and dx < 0.2 else M)
    for x, y, c in ((11, 5, F), (12, 5, F), (11, 4, W), (12, 6, F), (10, 5, F)):
        px[x, y] = c
    return im


def shrine():
    """Houten schrijn (GSC/HGSS) op een stenen voet, 32x48, palet SHRINE_PAL (indexen)."""
    W, H = 32, 48
    p = [[0] * W for _ in range(H)]

    def s(x, y, c):
        if 0 <= x < W and 0 <= y < H:
            p[y][x] = c
    # nok met omhoogstekende uiteinden
    for x in range(7, 25):
        s(x, 1, 1); s(x, 2, 4); s(x, 3, 3)
    for x0 in (5, 25):
        for y in range(0, 3):
            s(x0, y, 5); s(x0 + 1, y, 5)
        s(x0, 0, 1); s(x0 + 1, 0, 1)
    # dakvlak (dakpannen), breder naar onderen
    for y in range(4, 15):
        hw = 9 + (y - 4) * 7 // 10
        for x in range(16 - hw, 16 + hw):
            line = (y - 4) % 3 == 2
            seam = (x + ((y - 4) // 3) * 2) % 4 == 0
            c = 2 if line or seam else 3
            if not line and y < 7 and x < 16:
                c = 4 if not seam else 3
            s(x, y, c)
        s(16 - hw - 1, y, 1); s(16 + hw, y, 1)
    for x in range(0, 32):
        s(x, 15, 1)
    for x in range(1, 31):
        s(x, 16, 5)
    s(0, 16, 1); s(31, 16, 1)
    for x in range(3, 29):
        s(x, 17, 1)
    # kastje met deurtjes
    for y in range(18, 34):
        s(6, y, 1); s(25, y, 1)
        for x in range(7, 25):
            if x in (7, 8):
                c = 8 if x == 7 else 7
            elif x in (23, 24):
                c = 6 if x == 23 else 5
            elif x in (15, 16):
                c = 1 if x == 16 else 5
            elif y in (18, 22, 26, 30, 33) or x in (11, 20):
                c = 5
            else:
                c = 6 if (x + y) % 5 else 7
            s(x, y, c)
    # shimenawa (touw) met papieren zigzagjes
    for x in range(7, 25):
        s(x, 19, 13 if x % 2 else 7); s(x, 20, 7 if x % 2 else 13)
    for x0 in (10, 15, 20):
        for i, y in enumerate(range(21, 26)):
            s(x0 + (i % 2), y, 12)
    # stenen voet: plaat, blokken, trede
    for x in range(2, 30):
        s(x, 34, 11); s(x, 35, 10); s(x, 36, 9)
    for y in (34, 35, 36):
        s(2, y, 1); s(29, y, 1)
    for y in range(37, 43):
        s(4, y, 1); s(27, y, 1)
        for x in range(5, 27):
            c = 11 if y == 37 else 10
            if y in (39, 42) or (y < 39 and x in (11, 20)) or (y > 39 and x in (8, 16, 23)):
                c = 9
            s(x, y, c)
    for x in range(1, 31):
        s(x, 43, 11); s(x, 44, 10); s(x, 45, 10); s(x, 46, 9); s(x, 47, 1)
    for y in range(43, 47):
        s(0, y, 1); s(31, y, 1)
    for x, y in ((3, 35), (4, 35), (4, 34), (28, 35), (27, 36), (5, 38), (5, 37), (26, 41), (2, 44), (3, 44),
                 (3, 43), (29, 44), (28, 45), (12, 46), (13, 45)):
        s(x, y, 15)
    # offers: een rode appel en een boterham (zie de tekst)
    for x, y, c in ((10, 33, 14), (11, 33, 14), (10, 34, 14), (11, 34, 14), (11, 32, 15),
                    (19, 33, 8), (20, 33, 8), (21, 33, 8), (19, 34, 15), (20, 34, 8), (21, 34, 15), (20, 32, 8)):
        s(x, y, c)
    return p


def lantern():
    """Stenen lantaarn (toro), 16x32, palet SHRINE_PAL."""
    p = [[0] * 16 for _ in range(32)]

    def row(y, x0, x1, c, edge=1):
        for x in range(x0, x1 + 1):
            p[y][x] = c
        p[y][x0 - 1] = edge
        p[y][x1 + 1] = edge
    p[0][7] = p[0][8] = 1
    row(1, 7, 8, 11)
    row(2, 5, 10, 11)
    row(3, 3, 12, 10)
    row(4, 2, 13, 10)
    row(5, 2, 13, 9)
    for y in range(6, 12):
        row(y, 4, 11, 10)
        for x in range(6, 10):
            p[y][x] = 12 if (y in (8, 9) and x in (7, 8)) else 13
    p[6][6:10] = [9] * 4
    row(12, 3, 12, 10)
    row(13, 3, 12, 9)
    for y in range(14, 25):
        row(y, 6, 9, 10)
        p[y][6] = 11
        p[y][9] = 9
    row(25, 4, 11, 10)
    row(26, 4, 11, 10)
    row(27, 3, 12, 9)
    for x in range(2, 14):
        p[28][x] = 1
    p[26][5] = p[25][10] = 15
    return p


def quantize(imgs, n=15):
    """Gezamenlijk palet (n kleuren + transparant) voor een groep RGBA-plaatjes; geeft (palet, [indexrasters])."""
    pix = [im.getpixel((x, y))[:3] for im in imgs for y in range(im.height) for x in range(im.width)
           if im.getpixel((x, y))[3] >= 128]
    strip = Image.new('RGB', (len(pix), 1))
    strip.putdata(pix)
    q = strip.quantize(colors=n, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:n * 3]
    cols = [tuple(pal[i * 3:i * 3 + 3]) for i in range(len(pal) // 3)]
    out = []
    for im in imgs:
        g = []
        for y in range(im.height):
            r = []
            for x in range(im.width):
                c = im.getpixel((x, y))
                if c[3] < 128:
                    r.append(0)
                else:
                    r.append(1 + min(range(len(cols)), key=lambda i: sum((a - b) ** 2 for a, b in zip(cols[i], c[:3]))))
            g.append(r)
        out.append(g)
    return [(0, 0, 0)] + cols + [(0, 0, 0)] * (15 - len(cols)), out


class IlexTiles:
    """Tiles en metatiles van ilex_forest; decor wordt op aanvraag gemaakt en ontdubbeld."""

    def __init__(self, transform):
        self.tiles = [[[0] * 8 for _ in range(8)] for _ in range(512)]
        self.next = 1
        self.tidx, self.midx, self.mts, self.attrs = {}, {}, bytearray(), bytearray()
        self.cache = {}
        self.pals = {i: [(0, 0, 0)] * 16 for i in range(16)}
        self.pals[P_SHRINE] = [J.q(c) for c in SHRINE_PAL]
        self.raster = {'shrine': (P_SHRINE, shrine()), 'lantern': (P_SHRINE, lantern())}
        for pal, names in PAL_GROUPS.items():
            imgs = []
            for nm in names:
                if nm == 'lily':
                    imgs.append(lily())
                else:
                    f, x, w, h = DECOR[nm]
                    imgs.append(Image.open(f).convert('RGBA').crop((x, 0, x + w, h)))
            cols, rasters = quantize(imgs)
            self.pals[pal] = [J.q(c) for c in cols]
            for nm, r in zip(names, rasters):
                self.raster[nm] = (pal, r)
        for i in list(self.pals):
            if i in PAL_GROUPS:
                self.pals[i] = [self.pals[i][0]] + [transform(c) for c in self.pals[i][1:]]
            elif i == P_SHRINE:   # het schrijn iets minder somber dan de rest (het moet opvallen), zelfde sfeer
                self.pals[i] = [self.pals[i][0]] + [tuple((a + b) // 2 // 8 * 8 for a, b in zip(c, transform(c)))
                                                    for c in self.pals[i][1:]]
        # lichtvlekken: General-palet 2 (Ilex) met lichtere grastinten op 3-5
        g2 = J.read_pal('data/tilesets/primary/ilex_general/palettes/02.pal')
        lp = list(g2)
        for src, dst in ((12, 3), (13, 4), (14, 5)):
            lp[dst] = J.q(tuple(min(248, int(v * 1.1 + w)) for v, w in zip(g2[src], (22, 26, 8))))
        self.pals[P_LIGHT] = lp
        self.grass = gen_entry(0x001)[:4]
        self.water = gen_entry(0x0A1)[:4]
        self.gtiles, _ = J.png_tiles(GEN + '/tiles.png')
        # 0x200: gras + noordpijl-warp (terug naar het park)
        self.mt(self.grass, [0, 0, 0, 0], 0x64)

    def tile(self, pix):
        t = tuple(tuple(r) for r in pix)
        if not any(any(r) for r in t):
            return 0
        for hf in (0, 1):
            for vf in (0, 1):
                v = tuple(tuple(r[::-1] if hf else r) for r in (t[::-1] if vf else t))
                if v in self.tidx:
                    return self.tidx[v] | (hf << 10) | (vf << 11)
        slot = self.next
        self.next += 1
        assert slot < 512, 'ilex_forest: tiles op'
        self.tiles[slot] = [list(r) for r in t]
        self.tidx[t] = 512 + slot
        return 512 + slot

    def mt(self, bottom, top, attr):
        key = (tuple(bottom), tuple(top), attr)
        if key not in self.midx:
            self.midx[key] = 0x200 + len(self.mts) // 16
            assert self.midx[key] < 0x400
            self.mts += struct.pack('<8H', *(list(bottom) + list(top)))
            self.attrs += struct.pack('<H', attr)
        return self.midx[key]

    def decor(self, name, water=False):
        """Metatile-raster [rij][kolom] voor een uitsnede op gras (of water: waterlelie). None = leeg vak."""
        key = (name, water)
        if key in self.cache:
            return self.cache[key]
        pal, r = self.raster[name]
        h, w = len(r) // 16, len(r[0]) // 16
        grid = []
        for cy in range(h):
            row = []
            for cx in range(w):
                top = []
                for k in range(4):
                    x0, y0 = cx * 16 + (k % 2) * 8, cy * 16 + (k // 2) * 8
                    t = self.tile([[r[y0 + y][x0 + x] for x in range(8)] for y in range(8)])
                    top.append(0 if t == 0 else t | (pal << 12))
                if not any(top):
                    row.append(None)
                    continue
                row.append(self.mt(self.water if water else self.grass, top, (0x10 if water else 0) | COVERED))
            grid.append(row)
        self.cache[key] = grid
        return grid

    def light(self, mask):
        """Gras met een lichtvlek: mask[y][x] (16x16) True = licht."""
        ent = []
        for k in range(4):
            e = self.grass[k]
            src = self.gtiles[e & 0x3FF]
            pix = [[src[y][x] for x in range(8)] for y in range(8)]
            if e & 0x400:
                pix = [r[::-1] for r in pix]
            if e & 0x800:
                pix = pix[::-1]
            x0, y0 = (k % 2) * 8, (k // 2) * 8
            pix = [[{12: 3, 13: 4, 14: 5}.get(c, c) if mask[y0 + y][x0 + x] else c for x, c in enumerate(r)]
                   for y, r in enumerate(pix)]
            ent.append(self.tile(pix) | (P_LIGHT << 12))
        return self.mt(ent, [0, 0, 0, 0], 0)

    def save(self):
        os.makedirs(ILEX_TS + '/palettes', exist_ok=True)
        pngpal = Image.open(GEN + '/tiles.png').getpalette()
        save_png(ILEX_TS + '/tiles.png', self.tiles[:(self.next + 15) // 16 * 16], 16, pngpal)
        for i in range(16):
            write_pal('%s/palettes/%02d.pal' % (ILEX_TS, i), self.pals[i])
        open(ILEX_TS + '/metatiles.bin', 'wb').write(self.mts)
        open(ILEX_TS + '/metatile_attributes.bin', 'wb').write(self.attrs)
        return self.next, len(self.mts) // 16


def register_ilex():
    """Eenmalige omzetting IlexPetalburg (Petalburg-tiles, eigen paletten) -> IlexForest (alles eigen)."""
    for f in ('src/data/tilesets/headers.h', 'src/data/tilesets/graphics.h'):
        s = open(f).read()
        n = s.replace('secondary/ilex_petalburg/', 'secondary/ilex_forest/').replace('IlexPetalburg', 'IlexForest')
        if n != s:
            open(f, 'w').write(n)
    if os.path.isdir('data/tilesets/secondary/ilex_petalburg'):
        import shutil
        shutil.rmtree('data/tilesets/secondary/ilex_petalburg')
    set_tileset('IlexForest', ILEX_TS, 'NULL')
