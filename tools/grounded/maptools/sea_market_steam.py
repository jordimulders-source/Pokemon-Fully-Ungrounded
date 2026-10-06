"""Project Grounded: de drijvende markt en het stoomeiland (ZEE_PLAN.md). Deterministisch en idempotent.

  FloatingMarket    Vlotten aan elkaar (Pacifidlog-tileset) ten noorden van Route 133 (verbinding, x 16-51 van
                    Route 133). Een groot marktvlot met de rondreizende handelaar (dagelijks wisselend assortiment,
                    src/floating_market.c), twee hutten (visboer, vlotverhuurder; deuren dicht) en een visvlot,
                    met elkaar verbonden door drijvende boomstammen. Nieuwe metatile 0x2D8 in de Pacifidlog-
                    tileset: de rechte bovenrand van een vlot (zonder hut), uit tile 0x301 van de hoekstukken.
  SteamIsland       Vulkanisch eilandje ten noorden van Route 131 (verbinding, x 20-59 van Route 131), General +
                    Lavaridge. Zandstrand rondom (General), een plateau (terras-autotiler van chimney_ext.py) met
                    stomende grond, as-gras, de hete bron uit Lavaridge (badgast healt je team zodra je erin
                    stapt) en een vulkaan met een grotopening die pas na de Hall of Fame open is.
                    Alleen de onderste rijen grenzen aan Route 131 (andere secondary tileset): daar liggen alleen
                    primary-tiles (water/zand), en Route 131 heeft bovenaan ook alleen primary-tiles; het script
                    controleert dat.
  SteamIsland_Cave  Stoomgrot met Volcanion (lv 70, post-game).

Gebruik: python3 tools/grounded/maptools/sea_market_steam.py [rendermap]"""
import json, os, random, struct, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chimney_ext as cx            # zet ook de werkmap op de repo-root
import ogerpon_quest as oq

T, walkable, reach = cx.T, cx.walkable, cx.reach


def mt(v):
    return v & 0x3ff


# standaard botsing/hoogte per metatile, afgeleid uit vanilla-kaarten
REF = collections.defaultdict(collections.Counter)
_LAY = {l['name']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}
for name in ('Route105', 'Route131', 'PacifidlogTown', 'LavaridgeTown', 'MtChimney', 'Route109'):
    l = _LAY[name + '_Layout']
    for v in struct.unpack('<%dH' % (l['width'] * l['height']), open(l['blockdata_filepath'], 'rb').read()):
        REF[v & 0x3ff][v & ~0x3ff] += 1


def t(m, col=None, elev=None):
    """metatile m met de botsing/hoogte die vanilla er meestal bij gebruikt (of expliciet)."""
    base = REF[m].most_common(1)[0][0] if REF[m] else 0x3000
    c = (base >> 10) & 3 if col is None else (1 if col else 0)
    e = base >> 12 if elev is None else elev
    return m | (c << 10) | (e << 12)


WATER = 0x170


def grid(W, H, v):
    return [[v] * W for _ in range(H)]


def read(name, W, H):
    return oq.read_layout('data/layouts/%s/map.bin' % name, W, H)


def save(g, name):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    cx.save_grid(g, 'data/layouts/%s/map.bin' % name)


def border(name, v):
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', v, v, v, v))


def obj(gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', local_id=None, elev=3, rx=0, ry=0):
    o = cx.obj(gfx, x, y, script, flag, move=move, local_id=local_id, elev=elev)
    o['movement_range_x'], o['movement_range_y'] = rx, ry
    return o


def coord(x, y, script, elev=3):
    return {'type': 'trigger', 'x': x, 'y': y, 'elevation': elev, 'var': 'VAR_TEMP_1', 'var_value': '0',
            'script': script}


def sign(x, y, script, facing='BG_EVENT_PLAYER_FACING_NORTH'):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': facing, 'script': script}


def write_map(name, const, objs, warps, coords, bgs, **kw):
    m = {'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + const, 'music': 'MUS_ROUTE119',
         'region_map_section': 'MAPSEC_NONE', 'requires_flash': False, 'weather': 'WEATHER_SUNNY',
         'map_type': 'MAP_TYPE_OCEAN_ROUTE', 'allow_cycling': True, 'allow_escaping': False, 'allow_running': True,
         'show_map_name': True, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
         'object_events': objs, 'warp_events': warps, 'coord_events': coords, 'bg_events': bgs}
    m.update(kw)
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')


def set_connection(mapname, dest, direction, offset):
    """Voegt (tekstueel, rest van het bestand blijft gelijk) een verbinding toe of werkt hem bij."""
    p = 'data/maps/%s/map.json' % mapname
    s = open(p).read()
    m = json.loads(s)
    conns = m['connections'] or []
    for c in conns:
        if c['map'] == dest:
            if c['direction'] == direction and c['offset'] == offset:
                return
            raise SystemExit('verbinding %s -> %s bestaat al anders' % (mapname, dest))
    entry = '    {\n      "map": "%s",\n      "offset": %d,\n      "direction": "%s"\n    }' % (dest, offset, direction)
    i = s.index('"connections": [') + len('"connections": [')
    s = s[:i] + '\n' + entry + (',' if conns else '') + s[i:]
    json.loads(s)
    open(p, 'w').write(s)


def primary_only(g, rows):
    return all(mt(g[y][x]) < 0x200 for y in rows for x in range(len(g[0])))


# ====================================================================== nieuwe metatiles (achteraan, op inhoud gezocht)
# Ze worden op inhoud teruggevonden of achteraan toegevoegd; na een merge-conflict in metatiles.bin: de andere
# versie nemen en dit script opnieuw draaien (dan schuiven de nummers mee in map.bin).
def ensure_metatile(sec, entry, attr):
    p = 'data/tilesets/secondary/%s/metatiles.bin' % sec
    a = 'data/tilesets/secondary/%s/metatile_attributes.bin' % sec
    mts, attrs = bytearray(open(p, 'rb').read()), bytearray(open(a, 'rb').read())
    assert len(mts) // 16 == len(attrs) // 2
    for i in range(len(mts) // 16):
        if mts[i * 16:i * 16 + 16] == entry and attrs[i * 2:i * 2 + 2] == attr:
            return 0x200 + i
    assert len(mts) // 16 < 512
    mts += entry
    attrs += attr
    open(p, 'wb').write(mts)
    open(a, 'wb').write(attrs)
    return 0x200 + len(mts) // 16 - 1


def _mt(sec, i):
    m = open('data/tilesets/secondary/%s/metatiles.bin' % sec, 'rb').read()
    a = open('data/tilesets/secondary/%s/metatile_attributes.bin' % sec, 'rb').read()
    j = i - 0x200
    return struct.unpack_from('<8H', m, j * 16), a[j * 2:j * 2 + 2]


def raft_top():
    """Pacifidlog: rechte bovenrand van een vlot zonder hut (onderlaag water, onder 2x tile 0x301)."""
    corner, attr = _mt('pacifidlog', 0x208)
    assert corner[7] & 0x3ff == 0x301 and not corner[7] & 0xc00, hex(corner[7])
    return ensure_metatile('pacifidlog', struct.pack('<8H', *(corner[:4] + (0, 0, corner[7], corner[7]))), attr)


def sand_right_column():
    """Lavaridge: de rechterkolom van de hete bron (2a5/2ad/2b5) met zand eronder i.p.v. gras (zoals links)."""
    left, _ = _mt('lavaridge', 0x2a1)
    out = {}
    for m_ in (0x2a5, 0x2ad, 0x2b5):
        e, attr = _mt('lavaridge', m_)
        out[m_] = ensure_metatile('lavaridge', struct.pack('<8H', *(left[:4] + e[4:])), attr)
    return out


# ====================================================================== drijvende markt
MW, MH = 36, 26
RAFT_TOP = []
POOL_RIGHT = {}
MARKET_OFFSET = 16                  # x van de markt op Route 133
LAND = 3


def raft(g, x0, y0, w, h, steps=()):
    """Vlot zonder hut, w x h (bovenste rij = water met rand, onderste rij = water met onderkant)."""
    assert w >= 3 and h >= 4
    RT = RAFT_TOP[0]
    for x in range(x0, x0 + w):
        first, last = x == x0, x == x0 + w - 1
        g[y0][x] = t(0x208 if first else 0x20c if last else RT, False, 1)
        g[y0 + 1][x] = t(0x210 if first else 0x214 if last else 0x221, False, LAND)
        for y in range(y0 + 2, y0 + h - 2):
            g[y][x] = t(0x218 if first else 0x21c if last else 0x221, False, LAND)
        g[y0 + h - 2][x] = t(0x220 if first else 0x224 if last else 0x221, False, LAND)
        if x in steps:
            g[y0 + h - 1][x] = t(0x22a, False, LAND)
        else:
            g[y0 + h - 1][x] = t(0x228 if first else 0x22c if last else 0x229, False, 1)


PAC = read('PacifidlogTown', 20, 40)


def hut(g, x0, y0):
    """Hut op een vlot uit Pacifidlog (x 0-4, y 9-15): spits, dak, deur (rij 3), dek, onderkant met trapje (x0+3)."""
    for j in range(7):
        for i in range(5):
            v = PAC[9 + j][i]
            if j == 0 and mt(v) != 0x202:
                continue                            # alleen de spits
            g[y0 + j][x0 + i] = v
    assert mt(g[y0 + 3][x0 + 2]) == 0x21a and mt(g[y0 + 6][x0 + 3]) == 0x22a
    return (x0 + 2, y0 + 3), (x0 + 3, y0 + 6)       # deur, trapje


def hlog(g, x0, x1, y):
    assert (x1 - x0 + 1) % 2 == 0
    for x in range(x0, x1 + 1):
        assert mt(g[y][x]) == WATER, ('stam op iets anders', x, y)
        g[y][x] = t(0x250 if (x - x0) % 2 == 0 else 0x251, False, LAND)


def vlog(g, x, y0, y1):
    assert (y1 - y0 + 1) % 2 == 0
    for y in range(y0, y1 + 1):
        assert mt(g[y][x]) == WATER, ('stam op iets anders', x, y)
        g[y][x] = t(0x258 if (y - y0) % 2 == 0 else 0x260, False, LAND)


def market():
    name, const = 'FloatingMarket', 'FLOATING_MARKET'
    g = grid(MW, MH, t(WATER, False, 1))
    raft(g, 11, 10, 14, 7, steps=(17, 18))          # marktvlot: dek x 11-24, y 11-15
    door_a, step_a = hut(g, 3, 2)                   # hut van de visboer
    door_b, step_b = hut(g, 28, 2)                  # hut van de vlotverhuurder
    raft(g, 2, 13, 7, 5)                            # visvlot: dek x 2-8, y 14-16
    door_c, step_c = hut(g, 15, 4)                  # hut van de handelaar, trapje (18,10) op het marktvlot
    vlog(g, step_a[0], step_a[1] + 1, step_a[1] + 4)            # (6, 9-12)
    hlog(g, step_a[0] + 1, 10, step_a[1] + 4)                   # (7-10, 12) -> marktvlot
    vlog(g, step_b[0], step_b[1] + 1, step_b[1] + 4)            # (30, 9-12)
    hlog(g, 25, step_b[0] - 1, step_b[1] + 4)                   # (25-29, 12)
    hlog(g, 9, 10, 15)                                          # visvlot -> marktvlot
    # zeerotsen (2x2, primary) langs de randen, vaste seed, niet op de vaarroute naar Route 133
    rnd = random.Random(1330)
    ROCKS = ((0x150, 0x151, 0x158, 0x159), (0x175, 0x176, 0x17d, 0x17e))
    placed = 0
    while placed < 9:
        x, y = rnd.randint(0, MW - 2), rnd.randint(0, MH - 2)
        if 9 <= x <= 27 and y >= 15:
            continue
        if any(mt(g[yy][xx]) != WATER for yy in range(y - 1, y + 3) for xx in range(x - 1, x + 3)
               if 0 <= yy < MH and 0 <= xx < MW):
            continue
        r = rnd.choice(ROCKS)
        for k, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
            g[y + dy][x + dx] = t(r[k], True, 1)
        placed += 1

    P = name + '_EventScript_'
    objs = [
        obj('OBJ_EVENT_GFX_ROOFTOP_SALE_WOMAN', 17, 12, P + 'Merchant', local_id='LOCALID_FLOATING_MARKET_MERCHANT'),
        obj('OBJ_EVENT_GFX_MOVING_BOX', 16, 12, P + 'Crate'),
        obj('OBJ_EVENT_GFX_MOVING_BOX', 18, 12, P + 'Crate'),
        obj('OBJ_EVENT_GFX_POKEFAN_F', 20, 13, P + 'Haggler', move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_FISHERMAN', 5, 14, P + 'Fishmonger'),
        obj('OBJ_EVENT_GFX_MOVING_BOX', 4, 14, P + 'FishCrate'),
        obj('OBJ_EVENT_GFX_OLD_MAN', 2, 15, P + 'OldFisher', move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_SAILOR', 23, 14, P + 'RaftRenter', move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_WINGULL', 14, 14, P + 'Wingull', move='MOVEMENT_TYPE_WANDER_AROUND', rx=2, ry=1,
            local_id='LOCALID_FLOATING_MARKET_WINGULL'),
        obj('OBJ_EVENT_GFX_TUBER_M', 13, 11, P + 'Tuber', move='MOVEMENT_TYPE_WANDER_AROUND', rx=1, ry=1),
    ]
    bgs = [sign(door_a[0], door_a[1], P + 'FishmongerDoor'), sign(door_b[0], door_b[1], P + 'RenterDoor'),
           sign(door_c[0], door_c[1], P + 'MerchantDoor')]
    # bereikbaarheid: alles vanaf het dek van het marktvlot
    r = reach(g, [(17, 15)])
    for o in objs:
        assert (o['x'], o['y']) in r, ('object niet op het dek', o['script'])
    for d in (door_a, door_b, door_c):
        assert (d[0], d[1] + 1) in r, ('deur onbereikbaar', d)
    assert (2, 15) in r and (6, 9) in r and (31, 9) in r
    # aankomst vanaf Route 133: water in de onderste rijen open
    assert all(mt(g[y][x]) == WATER for y in range(19, MH) for x in range(10, 28))
    save(g, name)
    border(name, t(WATER, False, 1))
    oq.register_layout(name, const, MW, MH, 'gTileset_Pacifidlog')
    write_map(name, const, objs, [], [], bgs, music='MUS_SLATEPORT', region_map_section='MAPSEC_FLOATING_MARKET',
              connections=[{'map': 'MAP_ROUTE133', 'offset': -MARKET_OFFSET, 'direction': 'down'}])
    oq.register_map(name)
    set_connection('Route133', 'MAP_FLOATING_MARKET', 'up', MARKET_OFFSET)
    return name


# ====================================================================== stoomeiland
SW, SH = 40, 34
STEAM_OFFSET = 20                   # x van het eiland op Route 131
BEACH = (5, 4, 34, 27)              # zandring (x0, y0, x1, y1), de buitenste ring is de waterrand
PLATEAU = (8, 7, 31, 23)            # terras 1
VOLCANO = (13, 9, 26, 16)           # vulkaan: terras 2, met de grotopening in de zuidwand
SUMMIT = (16, 9, 23, 13)            # terras 3 met de krater
CRATER = [(x, y) for x in range(18, 22) for y in range(10, 12)]
CAVE_DOOR = (20, 16)
STAIRS = [(19, 23), (20, 23)]
POOL = (24, 17)                     # hete bron (6x5, uit Lavaridge x 2-7, y 2-6)
LAVA = read('LavaridgeTown', 20, 20)


def steam_hmap():
    m = [['0'] * SW for _ in range(SH)]
    def fill(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                m[y][x] = c
    fill(*PLATEAU, '1')
    fill(*VOLCANO, '2')
    fill(*SUMMIT, '3')
    return [''.join(r) for r in m]


def steam_island():
    name, const = 'SteamIsland', 'STEAM_ISLAND'
    random.seed(1310)
    hm = steam_hmap()
    g = cx.terrace_tiles(hm, CRATER)
    bx0, by0, bx1, by1 = BEACH
    for y in range(SH):
        for x in range(SW):
            if hm[y][x] != '0' or (x, y) in CRATER:
                continue
            if not (bx0 <= x <= bx1 and by0 <= y <= by1):
                g[y][x] = t(WATER, False, 1); continue
            top, bot, left, right = y == by0, y == by1, x == bx0, x == bx1
            if top:
                m_ = 0x11b if left else 0x11d if right else 0x11c
            elif bot:
                m_ = 0x12b if left else 0x12d if right else 0x12c
            else:
                m_ = 0x123 if left else 0x125 if right else 0x124
            g[y][x] = t(m_)
    cx.stairs(g, STAIRS)
    # hete bron uit Lavaridge
    px, py = POOL
    for j in range(5):
        for i in range(6):
            v = LAVA[2 + j][2 + i]
            if i == 5 and mt(v) in POOL_RIGHT:
                v = (v & ~0x3ff) | POOL_RIGHT[mt(v)]
            g[py + j][px + i] = v
    # zandrand rond de bron (links, rechts, onder)
    for j in range(1, 6):
        for i in (-1, 6):
            g[py + j][px + i] = t(0x2a8, False, 3)
    for i in range(-1, 7):
        g[py + 5][px + i] = t(0x2a8, False, 3)
    assert mt(g[py][px + 4]) == 0x29c and walkable(g[py][px + 4])     # enige ingang (zoals in Lavaridge)
    SOAK = [(px + 4, py + 1)]
    SEATS = [(px + 2, py + 2), (px + 3, py + 2)]
    # grotopening: de wand blijft dicht tot na de Hall of Fame (setmetatile in ON_LOAD)
    assert mt(g[CAVE_DOOR[1]][CAVE_DOOR[0]]) in (0x274, 0x323) and walkable(g[CAVE_DOOR[1] + 1][CAVE_DOOR[0]])
    g[CAVE_DOOR[1]][CAVE_DOOR[0]] = T(0x274, True)
    # zeerotsen rondom (primary), niet in de aanloop vanaf Route 131 (onderkant x 14-26)
    rnd = random.Random(1311)
    ROCKS = ((0x150, 0x151, 0x158, 0x159), (0x175, 0x176, 0x17d, 0x17e))
    placed = 0
    while placed < 12:
        x, y = rnd.randint(0, SW - 2), rnd.randint(0, SH - 2)
        if 12 <= x <= 28 and y >= 27:
            continue
        if any(mt(g[yy][xx]) != WATER for yy in range(y - 1, y + 3) for xx in range(x - 1, x + 3)
               if 0 <= yy < SH and 0 <= xx < SW):
            continue
        r = rnd.choice(ROCKS)
        for k, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
            g[y + dy][x + dx] = t(r[k], True, 1)
        placed += 1

    P = name + '_EventScript_'
    objs = [
        obj('OBJ_EVENT_GFX_HOT_SPRINGS_OLD_WOMAN', *SEATS[0], P + 'Bather', elev=3),
        obj('OBJ_EVENT_GFX_HOT_SPRINGS_OLD_WOMAN', *SEATS[1], P + 'Bather2', elev=3),
        obj('OBJ_EVENT_GFX_SCIENTIST_1', CAVE_DOOR[0] + 2, CAVE_DOOR[1] + 1, P + 'Volcanologist',
            move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_EXPERT_M', 12, 25, P + 'Tourist', move='MOVEMENT_TYPE_WANDER_AROUND', rx=2, ry=1),
        obj('OBJ_EVENT_GFX_SWIMMER_F', 36, 18, P + 'Swimmer', move='MOVEMENT_TYPE_FACE_LEFT', elev=1),
    ]
    coords = [coord(x, y, P + 'Soak') for x, y in SOAK]
    starts = [(19, 25)]
    keep = cx.keep_cells(objs, []) | cx.area(STAIRS + [(x, y + 1) for x, y in STAIRS] + [(x, y - 1) for x, y in STAIRS])
    keep |= cx.area([(px + i, py + j) for i in range(6) for j in range(5)]) | cx.area([CAVE_DOOR, (CAVE_DOOR[0], CAVE_DOOR[1] + 1)])
    keep |= cx.area([(px + 4, py - 1)])
    rng = random.Random(1312)
    used = set()
    high = {(x, y) for y in range(SH) for x in range(SW) if hm[y][x] in '23'}
    grass = cx.ash_grass(g, keep | high, rng, 7)
    cx.decorate(g, 0x271, 'ground', keep | grass, starts, [
        ('boulder', 2, 'open'), ('rock', 5, 'muur'), ('sulfur_a', 2, 'muur'), ('sulfur_b', 2, 'muur'),
        ('basalt', 3, 'vrij'), ('crack_a', 4, 'vrij'), ('crack_b', 4, 'vrij'), ('ash_a', 3, 'vrij'), ('deadtree', 2, 'muur'),
    ], rng, used)
    flat = [(x, y) for y in range(SH) for x in range(SW) if mt(g[y][x]) == 0x271 and walkable(g[y][x])
            and (x, y) not in keep and (x, y) not in grass]
    for x, y in rng.sample(flat, 16):                            # stoom uit de grond (geanimeerd)
        g[y][x] = T(rng.choice((0x312, 0x313)), elev=3)
    # controles
    r = reach(g, starts)
    for o in objs[2:4]:
        assert (o['x'], o['y']) in r, ('object onbereikbaar', o['script'])
    assert mt(g[18][36]) == WATER
    for c in SOAK:
        assert c in reach(g, starts, passable=set()) or cx.next_to(c, r)
    assert (px + 4, py - 1) in r and (CAVE_DOOR[0], CAVE_DOOR[1] + 1) in r
    assert grass and all(c in r for c in grass), 'as-gras onbereikbaar'
    assert primary_only(g, range(SH - 8, SH)), 'onderste rijen moeten primary zijn (grens met Route 131)'
    r131 = read('Route131', 60, 40)
    assert primary_only([row[STEAM_OFFSET:STEAM_OFFSET + SW] for row in r131], range(0, 8)), 'Route 131 boven niet primary'
    assert all(mt(g[y][x]) == WATER for y in range(28, SH) for x in range(14, 27)), 'aanloop vanaf Route 131 dicht'
    inc = open('data/maps/SteamIsland/scripts.inc').read()
    assert 'setmetatile %d, %d, METATILE_Lavaridge_CaveEntrance_Bottom' % CAVE_DOOR in inc, 'ON_LOAD-deur klopt niet'
    save(g, name)
    border(name, t(WATER, False, 1))
    oq.register_layout(name, const, SW, SH, 'gTileset_Lavaridge')
    write_map(name, const, objs,
              [{'x': CAVE_DOOR[0], 'y': CAVE_DOOR[1], 'elevation': 0, 'dest_map': 'MAP_STEAM_ISLAND_CAVE', 'dest_warp_id': '0'}],
              coords, [], music='MUS_OLDALE', weather='WEATHER_FOG_HORIZONTAL', region_map_section='MAPSEC_STEAM_ISLAND',
              connections=[{'map': 'MAP_ROUTE131', 'offset': -STEAM_OFFSET, 'direction': 'down'}])
    oq.register_map(name)
    set_connection('Route131', 'MAP_STEAM_ISLAND', 'up', STEAM_OFFSET)
    return name


# ====================================================================== stoomgrot (Volcanion)
CW, CH = 17, 13
CDOOR = (8, 2)
VOLCANION = (8, 8)


def cave():
    name, const = 'SteamIsland_Cave', 'STEAM_ISLAND_CAVE'
    random.seed(1313)
    m = [['.'] * CW for _ in range(CH)]
    def carve(x0, y0, x1, y1, c='#'):
        for yy in range(y0, y1 + 1):
            for xx in range(x0, x1 + 1):
                m[yy][xx] = c
    carve(2, 3, 14, 10)
    for c in ((2, 3), (14, 3), (2, 10), (14, 10), (3, 10), (13, 10)):
        m[c[1]][c[0]] = '.'
    carve(2, 3, 4, 4, '.'); carve(12, 3, 14, 4, '.')
    carve(3, 7, 4, 8, 'L'); carve(12, 6, 13, 8, 'L')          # magmapoeltjes (de stoom komt ergens vandaan)
    mask = [''.join(r) for r in m]
    g = cx.cave_tiles(mask)
    cx.cave_door(g, *CDOOR)
    start = (CDOOR[0], CDOOR[1] + 1)
    o = obj('OBJ_EVENT_GFX_SPECIES(VOLCANION)', VOLCANION[0], VOLCANION[1], name + '_EventScript_Volcanion',
            'FLAG_DEFEATED_VOLCANION', local_id='LOCALID_STEAM_CAVE_VOLCANION')
    keep = cx.keep_cells([o], [], cx.area([start]) | cx.area([VOLCANION], 2))
    cx.decorate(g, cx.FLOOR, 'cave', keep, [start], [
        ('sulfur_a', 2, 'muur'), ('sulfur_b', 2, 'muur'), ('rock', 2, 'muur'), ('crack_a', 3, 'vrij'),
        ('crack_b', 2, 'vrij'), ('ash_a', 2, 'vrij')], random.Random(1314))
    assert VOLCANION in reach(g, [start]), 'Volcanion onbereikbaar'
    save(g, name)
    open('data/layouts/%s/border.bin' % name, 'wb').write(open('data/layouts/FieryPath_HeatranLair/border.bin', 'rb').read())
    oq.register_layout(name, const, CW, CH, 'gTileset_Lavaridge')
    write_map(name, const, [o],
              [{'x': CDOOR[0], 'y': CDOOR[1], 'elevation': 0, 'dest_map': 'MAP_STEAM_ISLAND', 'dest_warp_id': '0'}],
              [], [], music='MUS_SEALED_CHAMBER', weather='WEATHER_FOG_HORIZONTAL', map_type='MAP_TYPE_UNDERGROUND',
              region_map_section='MAPSEC_STEAM_ISLAND', show_map_name=False, allow_cycling=False, allow_escaping=True,
              battle_scene='MAP_BATTLE_SCENE_NORMAL')
    oq.register_map(name)
    return name


if __name__ == '__main__':
    RAFT_TOP.append(raft_top())
    POOL_RIGHT.update(sand_right_column())
    names = [market(), steam_island(), cave()]
    if len(sys.argv) > 1:
        import subprocess
        for n in names:
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', '40'], check=True)
    print('klaar:', ', '.join(names))
