"""Project Grounded: The Spire op het Battle Frontier-eiland (BattleFrontier_OutsideWest).

- De kaart wordt N rijen hoger (bovenaan zee); alle events schuiven N rijen mee, de verbinding met
  OutsideEast krijgt offset N/-N en de veerboot-warps (19, 67) worden (19, 67+N).
- Op de noordrand van het Dome-plein (x 26-40, de oude hekrij) staat The Spire in Frontier-stijl:
  de gevel van de Battle Tower (wit glas, baksteenrood, blauwe ruiten, crème pilaren, leien luifel
  met glazen schuifdeur) uit gTileset_BattleFrontierOutsideEast, 15 breed. Hij loopt in vier
  trappen (15 -> 11 -> 7 -> 3 breed) omhoog; elke trap eindigt in een dakrand met oranje sierlijst,
  bovenop staat een antennenaald met rood baken. De voet staat op het plein (onderste rij =
  pleinvloer), de schacht rijst boven zee uit, net als het huisje rechts ervan.
- Tiles en metatiles van de Battle Tower worden gekopieerd naar vrije plekken van
  gTileset_BattleFrontierOutsideWest (alleen deze kaart gebruikt die tileset). Paletten 0 (General),
  9 en 10 zijn in East en West identiek, dus de kleuren blijven exact die van de Battle Tower.
- Deur (33, 26): metatile 0x329 met MB_ANIMATED_DOOR, net als de Battle Tower; field_door.c zoekt de
  animatie op metatile-nummer, dus de deur schuift open met de Battle Tower-animatie.
  Warp naar BattleFrontier_SpireLobby.

Idempotent: leest de oorspronkelijke kaart/tileset uit git (commit ORIG) en bouwt alles opnieuw.
Gebruik: python3 tools/grounded/maptools/spire_tower.py [voorbeeld.png]
"""
import io, json, re, struct, subprocess, sys
from PIL import Image

ORIG = '6744d697'           # commit vóór The Spire-toren
N = 24                      # extra rijen bovenaan
W, H0 = 56, 72
H = H0 + N
TS = 'data/tilesets/secondary/battle_frontier_outside_west/'
EAST = 'data/tilesets/secondary/battle_frontier_outside_east/'
GEN = 'data/tilesets/primary/general/'
LAY = 'data/layouts/BattleFrontier_OutsideWest/'
EAST_MAP = 'data/layouts/BattleFrontier_OutsideEast/map.bin'
MAPJ = 'data/maps/BattleFrontier_OutsideWest/map.json'
X0 = 26                     # linkerkolom van de toren
BASE = N + 3                # onderste rij (oude hekrij, ligt op het plein)
DOOR = (33, N + 2)
DOOR_MT = 0x329             # = METATILE_BattleFrontierOutsideEast_Door_BattleTower (deuranimatie)
LOBBY = 'MAP_BATTLE_FRONTIER_SPIRE_LOBBY'
MB_ANIMATED_DOOR = 0x69
FLAG_ANIM_TILES = range(218, 224)
NUM_TILES = 508             # -num_tiles in graphics_file_rules.mk
DOOR_LABELS = {0x3FC, 0x28A, 0x263, 0x396}

# Battle Tower in OutsideEast: kolommen x 8..24 (17 breed), schacht rij 0-11, voet rij 12-15.
# Kolom-indexen: 0 wit glas, 1-2 baksteen, 3-4 schuin glas, 5 pilaar, 6 schuin glas, 7-9 middenglas,
# 10 schuin glas, 11 pilaar, 12-13 schuin glas, 14-15 baksteen, 16 wit glas.
BT_X = 8
S1 = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16]     # 15 breed (voet + onderste trap)
S2 = [0, 1, 2, 6, 7, 8, 9, 10, 14, 15, 16]                 # 11
S3 = [0, 6, 7, 8, 9, 10, 16]                               # 7
S4 = [0, 8, 16]                                            # 3
# (eerste rij, laatste rij) van elke trap; de rij erboven is de dakrand
SECTIONS = [(S1, 14, BASE - 4), (S2, 9, 12), (S3, 5, 7), (S4, 3, 3)]
NEEDLE_ROWS = (0, 1)
TW = len(S1)


def git(path):
    return subprocess.check_output(['git', 'show', '%s:%s' % (ORIG, path)])


def read_pal(data):
    return [tuple(map(int, l.split())) for l in data.decode().replace('\r', '').split('\n')[3:19]]


# ---------------------------------------------------------------- Battle Tower-pixels uit East
class East:
    def __init__(self):
        self.map = struct.unpack('<%dH' % (72 * 72), open(EAST_MAP, 'rb').read())
        self.mts = open(EAST + 'metatiles.bin', 'rb').read()
        self.attrs = open(EAST + 'metatile_attributes.bin', 'rb').read()
        self.tiles = Image.open(EAST + 'tiles.png').load()

    def entries(self, mid):
        return list(struct.unpack_from('<8H', self.mts, (mid - 512) * 16))

    def tile_px(self, e):
        """8x8 (pal, kleur) van een tile-entry (secondary tile), 0 = doorzichtig."""
        t = (e & 0x3FF) - 512
        hf, vf, pal = (e >> 10) & 1, (e >> 11) & 1, e >> 12
        tx, ty = (t % 16) * 8, (t // 16) * 8
        out = []
        for y in range(8):
            for x in range(8):
                c = self.tiles[tx + (7 - x if hf else x), ty + (7 - y if vf else y)] if t >= 0 else 0
                out.append((pal, c) if c else None)
        return out

    def top(self, col, row):
        """Bovenlaag van Battle Tower-metatile (kolom-index, rij) als 16x16 (pal, kleur)/None."""
        mid = self.map[row * 72 + BT_X + col] & 0x3FF
        e = self.entries(mid)
        px = [[None] * 16 for _ in range(16)]
        for q in range(4):
            if (e[4 + q] & 0x3FF) == 0:
                continue
            assert (e[4 + q] & 0x3FF) >= 512, hex(mid)
            d = self.tile_px(e[4 + q])
            for i, v in enumerate(d):
                px[(q // 2) * 8 + i // 8][(q % 2) * 8 + i % 8] = v
        return px


# ---------------------------------------------------------------- eigen stukken (palet 9)
P9 = 9
NAVY, WHITE, LBLUE, GRAY, SLATE, DARK, LAV = 0, 1, 4, 5, 6, 7, 8
SKY, GLASS, GLASS2, ORANGE, RED, BRICK, BRICK2 = 9, 10, 11, 12, 13, 14, 15


def roof_band(width):
    """Dakrand (16 px hoog) over `width` metatiles: plat dak van boven gezien + oranje sierlijst."""
    w = width * 16
    rows = [
        [DARK] * w,                                   # achterrand
        [GRAY] * w,
        [LAV] * w, [LAV] * w, [LAV] * w, [LAV] * w,   # dakvlak
        [GRAY] * w,                                   # schaduw tegen de lijst
        [DARK] * w,
        [WHITE] * w,                                  # bovenkant sierlijst
        [ORANGE] * w, [ORANGE] * w,
        [RED] * w, [RED] * w,
        [BRICK] * w,
        [BRICK2] * w,
        [NAVY] * w,                                   # schaduwlijn op de gevel eronder
    ]
    # dakvlak: zachte tegelvoegen elke 16 px, licht van linksboven
    for x in range(w):
        if x % 16 == 15:
            for y in (3, 4):
                rows[y][x] = GRAY
        if x % 16 == 0:
            rows[2][x] = WHITE
    # zijkanten: omlijning, links licht, rechts schaduw
    for y in range(16):
        rows[y][0] = DARK
        rows[y][w - 1] = DARK
        if 1 <= y <= 14:
            rows[y][w - 2] = BRICK2 if y >= 9 else GRAY
            rows[y][1] = WHITE if y >= 8 else rows[y][1]
    rows[0][0] = rows[0][w - 1] = None
    return [[(P9, c) if c is not None else None for c in r] for r in rows]


def needle():
    """Antennenaald (2 metatiles hoog, 1 breed) met rood baken bovenaan."""
    h = 32
    px = [[None] * 16 for _ in range(h)]
    for y in range(h):
        if y < 4:                                     # baken
            hw = [1.0, 2.0, 2.5, 2.5][y]
        elif y < 6:
            hw = 1.0                                  # dun steeltje onder het baken
        else:
            hw = 1.5 + 4.5 * ((y - 6) / (h - 7)) ** 1.3
        for x in range(16):
            d = x + 0.5 - 8
            if abs(d) >= hw:
                continue
            e = hw - abs(d)
            if y < 4:
                c = WHITE if (y == 1 and d < 0 and d > -1.5) else ORANGE if y < 2 else RED
                if e < 1:
                    c = BRICK2
            else:
                c = LAV if d < -0.5 else GRAY if d < 1.5 else SLATE
                if d < 0 and d > -1.5 and hw > 2:
                    c = WHITE
                if e < 1:
                    c = DARK
            px[y][x] = c
    # ringen (oranje sierlijsten) op de naald
    for ry in (14, 24):
        hw = 1.5 + 4.5 * ((ry - 6) / (h - 7)) ** 1.3 + 1
        for x in range(16):
            d = x + 0.5 - 8
            if abs(d) < hw:
                px[ry][x] = DARK if hw - abs(d) < 1 else ORANGE
                px[ry + 1][x] = DARK if hw - abs(d) < 1 else RED
    # voet van de naald: breed blokje dat op het dak staat
    for y in range(h - 3, h):
        for x in range(3, 13):
            px[y][x] = DARK if x in (3, 12) or y == h - 1 else (LAV if x < 6 else GRAY if x < 10 else SLATE)
    return [[(P9, c) if c is not None else None for c in r] for r in px]


def tower_pixels(east):
    """Pixels van de hele toren: kolom X0.., rij 0..BASE."""
    w, h = TW * 16, (BASE + 1) * 16
    img = [[None] * w for _ in range(h)]

    def paste(px, mx, my):
        for y, r in enumerate(px):
            for x, v in enumerate(r):
                if v is not None:
                    img[my * 16 + y][mx * 16 + x] = v

    for cols, r0, r1 in SECTIONS:
        off = (TW - len(cols)) // 2
        for r in range(r0, r1 + 1):
            erow = 11 - ((BASE - 4 - r) % 2)          # baksteen wisselt per rij, sluit aan op de voet
            for i, c in enumerate(cols):
                paste(east.top(c, erow), off + i, r)
        band = roof_band(len(cols))
        for y in range(16):
            for x in range(len(cols) * 16):
                img[(r0 - 1) * 16 + y][off * 16 + x] = band[y][x]
    for r in range(4):                                 # voet: Battle Tower rij 12-15
        for i, c in enumerate(S1):
            paste(east.top(c, 12 + r), i, BASE - 3 + r)
    nd = needle()
    for y in range(32):
        for x in range(16):
            if nd[y][x] is not None:
                img[NEEDLE_ROWS[0] * 16 + y][(TW // 2) * 16 + x] = nd[y][x]
    return img


# ---------------------------------------------------------------- tiles en metatiles
def build():
    east = East()
    orig_map = list(struct.unpack('<%dH' % (W * H0), git(LAY + 'map.bin')))
    mts = bytearray(git(TS + 'metatiles.bin'))
    attrs = bytearray(git(TS + 'metatile_attributes.bin'))
    tiles_img = Image.open(io.BytesIO(git(TS + 'tiles.png')))
    tiles_img.load()
    border = struct.unpack('<4H', git(LAY + 'border.bin'))
    gen_mts = open(GEN + 'metatiles.bin', 'rb').read()

    # paletten 9 en 10 moeten gelijk zijn aan die van East (dan kloppen de kleuren exact)
    for p in (9, 10):
        assert read_pal(git(TS + 'palettes/%02d.pal' % p)) == read_pal(open(EAST + 'palettes/%02d.pal' % p, 'rb').read()), p

    # vrije metatiles: niet op de kaart/rand, geen deurlabel; daarna de lege plekken achteraan
    used = set(v & 0x3FF for v in orig_map) | set(b & 0x3FF for b in border)
    nmt = len(mts) // 16
    reserved = used | DOOR_LABELS | {DOOR_MT}
    free_mt = [512 + i for i in range(nmt) if 512 + i not in reserved]
    free_mt += list(range(512 + nmt, 1024))
    if DOOR_MT in used:
        # 0x329 is in West een gewone metatile op de kaart: verhuizen naar een vrije plek,
        # zodat 0x329 de Battle Tower-deur kan worden (deuranimatie gaat op metatile-nummer)
        assert DOOR_MT not in set(b & 0x3FF for b in border)
        mv = free_mt.pop(0)
        mts[(mv - 512) * 16:(mv - 511) * 16] = mts[(DOOR_MT - 512) * 16:(DOOR_MT - 511) * 16]
        attrs[(mv - 512) * 2:(mv - 511) * 2] = attrs[(DOOR_MT - 512) * 2:(DOOR_MT - 511) * 2]
        orig_map = [(v & ~0x3FF) | mv if (v & 0x3FF) == DOOR_MT else v for v in orig_map]
        used = (used - {DOOR_MT}) | {mv}
    ref = set()
    for i in range(nmt):
        if 512 + i in used or 512 + i in DOOR_LABELS:
            for k in range(8):
                t = struct.unpack_from('<H', mts, i * 16 + k * 2)[0] & 0x3FF
                if t >= 512:
                    ref.add(t - 512)
    free_tiles = [t for t in range(1, NUM_TILES) if t not in ref and t not in FLAG_ANIM_TILES]

    # nieuwe kaart: N rijen zee erboven
    water = orig_map[0]
    grid = [[water] * W for _ in range(N)] + [orig_map[y * W:(y + 1) * W] for y in range(H0)]
    # vlaggen achter de toren weg (oude rij 1-2, x 27..40)
    for oy in (1, 2):
        for x in range(X0, X0 + TW):
            if (grid[N + oy][x] & 0x3FF) != (water & 0x3FF):
                grid[N + oy][x] = water
    # een paar rotsen in zee (2x2, zoals op de rest van de kaart)
    rock = [orig_map[0 * W + 5], orig_map[0 * W + 6], orig_map[1 * W + 5], orig_map[1 * W + 6]]
    for rx, ry in ((6, 6), (19, 13), (47, 4), (20, 20), (46, 16), (11, 19)):
        grid[ry][rx], grid[ry][rx + 1], grid[ry + 1][rx], grid[ry + 1][rx + 1] = rock

    # rots die tegen de rechterwand van de toren lag (oude rij 0-1) weg
    for y in (N, N + 1):
        for x in range(X0 + TW, X0 + TW + 3):
            if (grid[y][x] & 0x3FF) in (0x150, 0x151, 0x158, 0x159):
                grid[y][x] = water

    pix = tower_pixels(east)
    tiles_px = tiles_img.load()
    tile_index = {}           # (pal, pixels) -> (tile, hflip, vflip)
    out_tiles = {}

    def get_tile(block):
        if all(v is None for v in block):
            return 0
        pals = set(v[0] for v in block if v)
        assert len(pals) == 1, 'tile met meerdere paletten: %s' % pals
        pal = pals.pop()
        data = tuple(v[1] if v else 0 for v in block)
        for hf in (0, 1):
            for vf in (0, 1):
                d = tuple(data[(7 - r if vf else r) * 8 + (7 - c if hf else c)] for r in range(8) for c in range(8))
                if (pal, d) in tile_index:
                    return (512 + tile_index[(pal, d)]) | (hf << 10) | (vf << 11) | (pal << 12)
        t = free_tiles.pop(0)
        tile_index[(pal, data)] = t
        out_tiles[t] = data
        return (512 + t) | (pal << 12)

    def bottom(mid):
        src = mts if mid >= 512 else gen_mts
        e = list(struct.unpack_from('<8H', src, (mid - 512 if mid >= 512 else mid) * 16))
        return e[:4]

    mt_index = {}
    new_mt = 0
    for my in range(BASE + 1):
        for cx in range(TW):
            mx = X0 + cx
            block = [[pix[my * 16 + y][cx * 16 + x] for x in range(16)] for y in range(16)]
            filled = any(v for r in block for v in r)
            if (mx, my) == DOOR:
                top = [get_tile([block[(q // 2) * 8 + i // 8][(q % 2) * 8 + i % 8] for i in range(64)]) for q in range(4)]
                bot = bottom(orig_map[(my + 2 - N) * W + mx] & 0x3FF)
                struct.pack_into('<8H', mts, (DOOR_MT - 512) * 16, *(bot + top))
                struct.pack_into('<H', attrs, (DOOR_MT - 512) * 2, MB_ANIMATED_DOOR | (1 << 12))
                grid[my][mx] = DOOR_MT
                continue
            if not filled and my != BASE:
                continue
            if my == BASE or (my == BASE - 1 and 0 < cx < TW - 1):
                # de voet staat op het plein: vloer van twee rijen lager (zelfde patroon);
                # de buitenste kolommen van de rij erboven houden water (rechte kustlijn)
                bgid = orig_map[(my + 2 - N) * W + mx] & 0x3FF
            else:
                bgid = water & 0x3FF
            bot = bottom(bgid)
            top = [get_tile([block[(q // 2) * 8 + i // 8][(q % 2) * 8 + i % 8] for i in range(64)]) for q in range(4)]
            key = (tuple(bot), tuple(top))
            if key not in mt_index:
                m = free_mt.pop(0)
                mt_index[key] = m
                new_mt += 1
                if m - 512 >= len(mts) // 16:
                    mts += b'\0' * ((m - 512 + 1) * 16 - len(mts))
                    attrs += b'\0' * ((m - 512 + 1) * 2 - len(attrs))
                struct.pack_into('<8H', mts, (m - 512) * 16, *(bot + top))
                struct.pack_into('<H', attrs, (m - 512) * 2, 1 << 12)     # LAYER_COVERED
            m = mt_index[key]
            if my == BASE:
                # onderste rij: alleen waar de gevel tot onderaan komt is het muur
                coll = 1 if any(block[y][x] for y in range(8, 16) for x in range(16)) or abs(mx - DOOR[0]) > 1 else 0
            else:
                coll = 1
            grid[my][mx] = m | (coll << 10)
    for t, data in out_tiles.items():
        tx, ty = (t % 16) * 8, (t // 16) * 8
        for i, c in enumerate(data):
            tiles_px[tx + i % 8, ty + i // 8] = c
    print('spire: %d metatiles, %d tiles (vrij over: %d metatiles, %d tiles)'
          % (new_mt + 1, len(out_tiles), len(free_mt), len(free_tiles)))

    open(LAY + 'map.bin', 'wb').write(b''.join(struct.pack('<H', grid[y][x]) for y in range(H) for x in range(W)))
    open(TS + 'metatiles.bin', 'wb').write(bytes(mts))
    open(TS + 'metatile_attributes.bin', 'wb').write(bytes(attrs))
    tiles_img.save(TS + 'tiles.png')
    # palet 10 terug naar het origineel (de vorige versie had er een eigen obsidiaanpalet in)
    open(TS + 'palettes/10.pal', 'wb').write(git(TS + 'palettes/10.pal'))
    return pix


def metadata():
    # layouts.json: hoogte
    lj = open('data/layouts/layouts.json').read()
    i = lj.index('"id": "LAYOUT_BATTLE_FRONTIER_OUTSIDE_WEST"')
    j = lj.index('}', i)
    lj = lj[:i] + re.sub(r'"height": \d+', '"height": %d' % H, lj[i:j], 1) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)

    # map.json OutsideWest: alles N rijen omlaag, verbinding, Spire-warp
    m = json.loads(git(MAPJ))
    for key in ('object_events', 'warp_events', 'coord_events', 'bg_events'):
        for ev in m.get(key) or []:
            ev['y'] += N
    m['connections'][0]['offset'] = N
    m['warp_events'].append({'x': DOOR[0], 'y': DOOR[1], 'elevation': 0, 'dest_map': LOBBY, 'dest_warp_id': '0'})
    open(MAPJ, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    warp_id = len(m['warp_events']) - 1

    e = 'data/maps/BattleFrontier_OutsideEast/map.json'
    s = open(e).read()
    s = re.sub(r'("map": "MAP_BATTLE_FRONTIER_OUTSIDE_WEST",\s*"offset": )-?\d+', r'\g<1>%d' % -N, s)
    open(e, 'w').write(s)

    # veerboot: aankomst op (19, 67) van de oude kaart
    for f in ('data/maps/SlateportCity_Harbor/scripts.inc', 'data/maps/LilycoveCity_Harbor/scripts.inc'):
        s = open(f).read()
        s = re.sub(r'warp MAP_BATTLE_FRONTIER_OUTSIDE_WEST, 19, \d+', 'warp MAP_BATTLE_FRONTIER_OUTSIDE_WEST, 19, %d' % (67 + N), s)
        open(f, 'w').write(s)
    return warp_id


def lobby(warp_id):
    NAME, CONST = 'BattleFrontier_SpireLobby', 'BATTLE_FRONTIER_SPIRE_LOBBY'
    import os, shutil
    os.makedirs('data/layouts/' + NAME, exist_ok=True)
    for f in ('map.bin', 'border.bin'):
        shutil.copy('data/layouts/BattleFrontier_BattlePikeLobby/' + f, 'data/layouts/%s/%s' % (NAME, f))
    lj = open('data/layouts/layouts.json').read()
    if '"LAYOUT_%s"' % CONST not in lj:
        i = lj.index('"id": "LAYOUT_BATTLE_FRONTIER_BATTLE_PIKE_LOBBY"'); j = lj.index('},', i) + 2
        lj = lj[:j] + '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": 11,
      "height": 13,
      "primary_tileset": "gTileset_Building",
      "secondary_tileset": "gTileset_BattlePike",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (CONST, NAME, NAME, NAME) + lj[j:]
        open('data/layouts/layouts.json', 'w').write(lj)

    base = json.load(open('data/maps/BattleFrontier_BattlePikeLobby/map.json'))
    m = {k: base[k] for k in base}
    m.update({'id': 'MAP_' + CONST, 'name': NAME, 'layout': 'LAYOUT_' + CONST, 'music': 'MUS_B_PYRAMID'})
    obj = lambda gfx, x, y, mv, script, lid=None: dict(
        ([('local_id', lid)] if lid else []) + [
            ('graphics_id', gfx), ('x', x), ('y', y), ('elevation', 3), ('movement_type', mv),
            ('movement_range_x', 1), ('movement_range_y', 1), ('trainer_type', 'TRAINER_TYPE_NONE'),
            ('trainer_sight_or_berry_tree_id', '0'), ('script', script), ('flag', '0')])
    m['object_events'] = [
        obj('OBJ_EVENT_GFX_LINK_RECEPTIONIST', 5, 5, 'MOVEMENT_TYPE_FACE_DOWN', NAME + '_EventScript_Attendant',
            'LOCALID_SPIRE_LOBBY_ATTENDANT'),
        obj('OBJ_EVENT_GFX_EXPERT_M', 9, 9, 'MOVEMENT_TYPE_FACE_UP', NAME + '_EventScript_Veteran'),
    ]
    m['warp_events'] = [{'x': x, 'y': 12, 'elevation': 0, 'dest_map': 'MAP_BATTLE_FRONTIER_OUTSIDE_WEST',
                         'dest_warp_id': str(warp_id)} for x in (5, 4, 6)]
    m['coord_events'] = []
    m['bg_events'] = [{'type': 'sign', 'x': 1, 'y': 3, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
                       'script': NAME + '_EventScript_RulesBoard'}]
    os.makedirs('data/maps/' + NAME, exist_ok=True)
    open('data/maps/%s/map.json' % NAME, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

    g = open('data/maps/map_groups.json').read()
    if '"%s"' % NAME not in g:
        g = g.replace('    "TrainerHill_Elevator"\n', '    "TrainerHill_Elevator",\n    "%s"\n' % NAME, 1)
        open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
    if inc not in es:
        anchor = '\t.include "data/maps/BattleFrontier_BattlePikeLobby/scripts.inc"\n'
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def preview(out):
    """Kaart rond de toren (rij 0 .. N+14) met rasternummers."""
    subprocess.check_call(['python3', 'tools/grounded/maptools/render_map.py', 'BattleFrontier_OutsideWest', out, '0', str(N + 16)])


if __name__ == '__main__':
    build()
    wid = metadata()
    lobby(wid)
    print('klaar: kaart %dx%d, Spire-warp id %d' % (W, H, wid))
    if len(sys.argv) > 1:
        subprocess.check_call(['make', TS + 'tiles.4bpp'])
        preview(sys.argv[1])
