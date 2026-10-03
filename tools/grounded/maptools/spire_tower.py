"""Project Grounded: The Spire op het Battle Frontier-eiland (BattleFrontier_OutsideWest).

- De kaart wordt N rijen hoger (bovenaan zee); alle events schuiven N rijen mee, de verbinding met
  OutsideEast krijgt offset N/-N en de veerboot-warps (19, 67) worden (19, 67+N).
- Achter het noordhek van het Dome-plein (x 32-36, oude rij 0-3) rijst The Spire uit zee: een
  obsidiaanzwarte stekel met karmozijnrode aders, gewervelde schacht en een gloeiend hart bovenin.
  De punt staat op rij 0; in het spel zie je hem nooit eindigen.
- Graphics: rotstextuur uit General (metatile 0x073, de bruine klifwand), opnieuw ingekleurd met een
  eigen palet (slot 10, ongebruikt in deze tileset). Het silhouet is symmetrisch, zodat rechts de
  gespiegelde tiles van links gebruikt. Metatiles en tiles komen op ongebruikte plekken van
  gTileset_BattleFrontierOutsideWest (de tileset zat vol: 510/512 metatiles, alleen deze kaart gebruikt hem).
- Deur onderaan in het midden (34, N+3): MB_NON_ANIMATED_DOOR, warp naar BattleFrontier_SpireLobby.

Idempotent: leest de oorspronkelijke kaart/tileset uit git (commit ORIG) en bouwt alles opnieuw.
Gebruik: python3 tools/grounded/maptools/spire_tower.py [voorbeeld.png]
"""
import io, json, math, re, struct, subprocess, sys
from PIL import Image

ORIG = '6744d697'           # commit vóór The Spire-toren
N = 24                      # extra rijen bovenaan
W, H0 = 56, 72
H = H0 + N
TS = 'data/tilesets/secondary/battle_frontier_outside_west/'
LAY = 'data/layouts/BattleFrontier_OutsideWest/'
MAPJ = 'data/maps/BattleFrontier_OutsideWest/map.json'
COL0, COLS = 32, 5          # spire-kolommen x 32..36, as in het midden van x 34
ROWS = N + 4                # rij 0 .. N+3 (N+3 = oude hekrij)
DOOR = (34, N + 3)
PAL = 10
LOBBY = 'MAP_BATTLE_FRONTIER_SPIRE_LOBBY'
MB_NON_ANIMATED_DOOR = 0x60
LAYER_COVERED = 1
FLAG_ANIM_TILES = range(218, 224)
NUM_TILES = 508             # -num_tiles in graphics_file_rules.mk
DOOR_LABELS = {0x3FC, 0x28A, 0x263, 0x396}


def git(path):
    return subprocess.check_output(['git', 'show', '%s:%s' % (ORIG, path)])


# ---------------------------------------------------------------- palet
COLORS = [
    (255, 0, 255),   # 0 transparant
    (8, 5, 12),      # 1 omlijning
    (18, 12, 24),    # 2 obsidiaan
    (30, 20, 38),    # 3
    (44, 30, 54),    # 4
    (62, 44, 74),    # 5 glans
    (92, 70, 104),   # 6 hoogste glans
    (58, 8, 18),     # 7 bloedrood donker
    (110, 14, 28),   # 8 karmozijn
    (168, 24, 36),   # 9 rood
    (222, 52, 44),   # 10 helrood
    (255, 120, 64),  # 11 oranje gloed
    (255, 204, 112), # 12 gele gloed
    (255, 246, 214), # 13 witheet
    (40, 12, 22),    # 14 donker kastanje (gloed op obsidiaan)
    (0, 0, 0),       # 15 zwart (deuropening)
]

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def dither(v, x, y):
    return v + (BAYER[y & 3][x & 3] / 16.0 - 0.5) * 0.5


# ---------------------------------------------------------------- textuur uit General 0x073
def general_texture():
    im =Image.open('data/tilesets/primary/general/tiles.png')
    px = im.load()
    pal = [tuple(map(int, l.split())) for l in open('data/tilesets/primary/general/palettes/03.pal').read().split('\n')[3:19]]
    mt = open('data/tilesets/primary/general/metatiles.bin', 'rb').read()
    ent = struct.unpack_from('<4H', mt, 0x073 * 16)
    tex = [[0.0] * 16 for _ in range(16)]
    for k, e in enumerate(ent):
        t = e & 0x3FF; hf = (e >> 10) & 1; vf = (e >> 11) & 1
        tx, ty = (t % 16) * 8, (t // 16) * 8
        for y in range(8):
            for x in range(8):
                c = px[tx + (7 - x if hf else x), ty + (7 - y if vf else y)]
                r, g, b = pal[c]
                tex[(k // 2) * 8 + y][(k % 2) * 8 + x] = (0.3 * r + 0.59 * g + 0.11 * b) / 255.0
    flat = [v for row in tex for v in row]
    lo, hi = min(flat), max(flat)
    return [[(v - lo) / (hi - lo) - 0.5 for v in row] for row in tex]


TEX = general_texture()

# ---------------------------------------------------------------- silhouet
YC, RY = 112, 46            # hart: middelpunt en halve hoogte (rij 4-9)
GROUPS = [11, 14, 17]       # schacht rij 10-21: drie groepen van 2 wervels (elk 2 rijen)
SH0 = 160


def vert(y):
    """(groepsbreedte, positie 0..1 in de wervel) of None buiten de schacht."""
    if SH0 <= y < SH0 + 192:
        return GROUPS[(y - SH0) // 64], ((y - SH0) % 32) / 32.0
    return None


def halfwidth(y):
    if y < 6:
        return 0.0
    if y < 64:                                   # naald
        return 0.6 + 7.0 * ((y - 6) / 58.0) ** 1.5
    if y < SH0:                                  # hart
        k = 1 - ((y - YC) / RY) ** 2
        return 8.0 + 14.0 * max(0.0, k) ** 0.55
    v = vert(y)
    if v:                                        # gewervelde schacht
        base, t = v
        return base * (1 - 0.10 * math.sin(math.pi * t)) + (2.0 if t < 0.1 else 0.0)
    rough = 1.6 * math.sin(y * 0.9) + 1.0 * math.sin(y * 2.3) if y >= 384 else 0.0
    if y < 416:                                  # uitwaaieren (rij 22-25)
        f = (y - 352) / 64.0
        return 19 + 13 * f ** 1.6 + rough
    f = (y - 416) / 32.0                          # voet (rij 26-27), ruwe rots
    return min(39.5, 32 + 8 * f ** 0.6 + rough)


def root_gap(d, y):
    """Inkepingen tussen de wortels onderaan."""
    if y < 428:
        return False
    g = (y - 428) / 20.0
    for c in (22.0, 33.5):
        if abs(d - c) < 0.4 + 3.2 * g:
            return True
    return False


def spire_pixels():
    w, h = COLS * 16, ROWS * 16
    img = [[0] * w for _ in range(h)]
    for y in range(h):
        hw = halfwidth(y)
        v = vert(y)
        for x in range(w):
            d = abs(x + 0.5 - 40)
            if d >= hw or root_gap(d, y):
                continue
            e = hw - d                                       # afstand tot de rand
            u = int(d) % 16
            tex = TEX[y % 16][u]
            rel = d / max(hw, 1)
            amp = 0.75 if y >= 384 else 0.55             # voet: meer rots
            tone = 0.22 + amp * tex + 0.42 * max(0.0, 1 - rel * rel) ** 1.5
            c = 2 + max(0, min(4, int(dither(tone, int(d), y) * 4.5)))   # 2..6
            if c == 6 and (int(d) + y) % 2:
                c = 5
            # aders: twee kronkelende karmozijnrode lijnen per kant
            for k, ph in ((0.55, 0.0), (0.28, 1.7)):
                pos = hw * (k + 0.06 * math.sin(2 * math.pi * (y % 32) / 32.0 + ph))
                if abs(d - pos) < 0.55 and hw > 5:
                    c = 8
            if d < 1.0 and hw > 3:                           # rugnaad
                c = 2
            # wervelring
            if v:
                base, t = v
                ty = (y - SH0) % 32
                tc = ty - int(3.0 * max(0.0, 1 - rel * rel))     # ring buigt naar voren (midden lager)
                if ty == 0 and d > base * 0.9 - 4:
                    c = 1
                elif tc == 0 and e > 1.2:
                    c = 1
                elif tc in (1, 2) and e > 1.2:
                    c = 6 if (tc == 1 and rel < 0.6) else 5
                elif tc == 3 and e > 1.2:
                    c = 4
                elif tc in (4, 5) and e > 1.2:
                    c = 2 if tc == 4 else 1 if rel > 0.5 else 3
            # rand
            if e < 1.2:
                c = 1
            elif e < 2.2:
                c = 7
            img[y][x] = c
    heart(img)
    base_glow(img)
    despeckle(img)
    door(img)
    return img


def despeckle(img):
    """Losse pixels (minder dan 3 buren) weghalen; de rand eromheen opnieuw omlijnen."""
    h, w = len(img), len(img[0])
    for _ in range(2):
        kill = [(x, y) for y in range(h) for x in range(w) if img[y][x] and sum(
            1 for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx or dy) and 0 <= x + dx < w and 0 <= y + dy < h
            and img[y + dy][x + dx]) < 3]
        for x, y in kill:
            img[y][x] = 0


def heart(img):
    rx, ry = 12.0, 26.0
    for y in range(YC - 34, YC + 34):
        hw = halfwidth(y)
        for x in range(COLS * 16):
            d = abs(x + 0.5 - 40)
            if not img[y][x]:
                continue
            dy = y - YC
            r = math.hypot(d / rx, dy / ry)
            e = hw - d
            if r < 1.0:
                g = dither(1.0 - r, int(d), y)
                c = 13 if g > 0.80 else 12 if g > 0.62 else 11 if g > 0.42 else 10 if g > 0.22 else 9
                # ribben over het hart (gekooid)
                for off in (-15, -5, 5, 15):
                    if abs(dy - off - 2.5 * (d / rx) ** 2) < 1.0:
                        c = 1 if abs(off) > 10 else 7
                if d < 1.0 and abs(dy) > 8:
                    c = 7
                img[y][x] = c
            elif r < 1.35 and e > 2.2:
                if img[y][x] in (3, 4, 5, 6):
                    img[y][x] = 14 if (int(d) + y) % 2 else 7
                elif img[y][x] == 2:
                    img[y][x] = 14
            elif r < 1.9 and img[y][x] == 8 and e > 2.2:
                img[y][x] = 9          # aders gloeien bij het hart


def base_glow(img):
    """Rode barsten in de voet rond de deur."""
    cx, cy = 39.5, ROWS * 16 - 6
    for y in range(400, ROWS * 16):
        for x in range(COLS * 16):
            c = img[y][x]
            if c in (3, 4, 5, 6):
                dist = math.hypot(x + 0.5 - 40, (y - cy) * 1.4)
                if dist < 26 and (int(abs(x + 0.5 - 40)) * 3 + y * 2) % 11 == 0:
                    img[y][x] = 9 if dist < 16 else 8


def door(img):
    oy = DOOR[1] * 16
    for y in range(oy, oy + 16):
        for x in range(32, 48):
            d = abs(x + 0.5 - 40)
            top = oy + 3 + 6 * (1 - math.sqrt(max(0.0, 1 - (d / 6.0) ** 2)))
            if d < 6.0 and y >= top:
                ry = y - oy
                c = 15
                if ry >= 12:
                    c = 9 if (x + y) % 2 else 8
                if ry >= 14:
                    c = 10
                img[y][x] = c
            elif d < 7.5 and y >= top - 1.5:
                img[y][x] = 8 if d < 7 else 1


# ---------------------------------------------------------------- tiles en metatiles
def build():
    orig_map = list(struct.unpack('<%dH' % (W * H0), git(LAY + 'map.bin')))
    mts = bytearray(git(TS + 'metatiles.bin'))
    attrs = bytearray(git(TS + 'metatile_attributes.bin'))
    tiles_img = Image.open(io.BytesIO(git(TS + 'tiles.png')))
    tiles_img.load()
    border = struct.unpack('<4H', git(LAY + 'border.bin'))

    # vrije metatiles: niet op de kaart/rand, geen deurlabel; daarna de 2 lege plekken achteraan
    used = set(v & 0x3FF for v in orig_map) | set(b & 0x3FF for b in border)
    nmt = len(mts) // 16
    free_mt = [512 + i for i in range(nmt) if 512 + i not in used and 512 + i not in DOOR_LABELS]
    free_mt += list(range(512 + nmt, 1024))
    # vrije tiles: niet gebruikt door een metatile die op de kaart staat
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
    # vlaggen met paal op x 33 en 36 (oude rij 1-2) weg: daar staat de voet
    for oy in (1, 2):
        for x in (33, 34, 36, 37):
            grid[N + oy][x] = water
    for x in (33, 36):      # hekpaal (0x3D6/0x3D7) -> gewoon hek (0x26C/0x26D)
        v = grid[N + 3][x]
        grid[N + 3][x] = (v & ~0x3FF) | {0x3D6: 0x26C, 0x3D7: 0x26D}[v & 0x3FF]
    # een paar rotsen in zee (2x2, zoals op de rest van de kaart)
    rock = [orig_map[0 * W + 5], orig_map[0 * W + 6], orig_map[1 * W + 5], orig_map[1 * W + 6]]
    for rx, ry in ((6, 6), (19, 13), (47, 4), (25, 20), (44, 17), (11, 19)):
        grid[ry][rx], grid[ry][rx + 1], grid[ry + 1][rx], grid[ry + 1][rx + 1] = rock

    pix = spire_pixels()
    tile_index = {}           # pixeldata -> (tile, hflip)
    out_tiles = {}
    tiles_px = tiles_img.load()

    def get_tile(data):
        if not any(data):
            return 0, 0
        if data in tile_index:
            return tile_index[data]
        mir = tuple(data[r * 8 + (7 - c)] for r in range(8) for c in range(8))
        if mir in tile_index:
            t, f = tile_index[mir]
            return t, f ^ 1
        t = free_tiles.pop(0)
        tile_index[data] = (t, 0)
        out_tiles[t] = data
        return t, 0

    mt_index = {}
    mt_count = 0
    for r in range(ROWS):
        for cx in range(COLS):
            x0, y0 = cx * 16, r * 16
            block = [pix[y0 + y][x0 + x] for y in range(16) for x in range(16)]
            mx, my = COL0 + cx, r
            if not any(block) and (mx, my) != DOOR:
                continue
            bg = grid[my][mx]
            bgid = bg & 0x3FF
            src = mts if bgid >= 512 else open('data/tilesets/primary/general/metatiles.bin', 'rb').read()
            bgent = list(struct.unpack_from('<8H', src, (bgid - 512 if bgid >= 512 else bgid) * 16))
            assert all((e & 0x3FF) == 0 for e in bgent[4:]), 'achtergrond met bovenlaag op %d,%d' % (mx, my)
            top = []
            for q in range(4):
                qx, qy = (q % 2) * 8, (q // 2) * 8
                data = tuple(pix[y0 + qy + y][x0 + qx + x] for y in range(8) for x in range(8))
                t, f = get_tile(data)
                top.append(((512 + t) | (f << 10) | (PAL << 12)) if t else 0)
            key = (tuple(bgent[:4]), tuple(top), (mx, my) == DOOR)
            if key not in mt_index:
                m = free_mt.pop(0)
                mt_index[key] = m
                mt_count += 1
                struct.pack_into('<8H', mts, (m - 512) * 16, *(bgent[:4] + top))
                beh = MB_NON_ANIMATED_DOOR if (mx, my) == DOOR else 0
                struct.pack_into('<H', attrs, (m - 512) * 2, beh | (LAYER_COVERED << 12))
            m = mt_index[key]
            coll = 0 if (mx, my) == DOOR else 1
            grid[my][mx] = m | (coll << 10) | (bg & 0xF000)
    for t, data in out_tiles.items():
        tx, ty = (t % 16) * 8, (t // 16) * 8
        for i, c in enumerate(data):
            tiles_px[tx + i % 8, ty + i // 8] = c
    if len(mts) < 512 * 16:
        pass
    print('spire: %d metatiles, %d tiles (vrij over: %d metatiles, %d tiles)'
          % (mt_count, len(out_tiles), len(free_mt), len(free_tiles)))

    open(LAY + 'map.bin', 'wb').write(b''.join(struct.pack('<H', grid[y][x]) for y in range(H) for x in range(W)))
    # metatiles.bin moet even groot blijven als het aantal gebruikte plekken
    last = max(mt_index.values()) - 512 + 1
    n_out = max(nmt, last)
    open(TS + 'metatiles.bin', 'wb').write(bytes(mts[:n_out * 16]) + b'\0' * max(0, n_out * 16 - len(mts)))
    open(TS + 'metatile_attributes.bin', 'wb').write(bytes(attrs[:n_out * 2]) + b'\0' * max(0, n_out * 2 - len(attrs)))
    tiles_img.save(TS + 'tiles.png')
    with open(TS + 'palettes/%02d.pal' % PAL, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in COLORS))
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
