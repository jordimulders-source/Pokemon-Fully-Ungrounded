"""Project Grounded: het strandresort PARADISO RESORT (ZEE_PLAN.md, Jordi's besluiten). Deterministisch en idempotent.

  ParadisoResort           Zandeiland ten zuiden van Route 129 (verbinding, offset 20; was eerst onder Route 109, maar
                           Jordi wilde het verder oostwaarts, uit het zicht van Mr. Briney's boot). General + Slateport;
                           Route 129 is General + Mossdeep, maar de rijen langs de rand zijn aan beide kanten alleen
                           primary (open zee), dus naadloos. Groot all-in hotel (het havengebouw van Slateport, verbreed tot 15 en een
                           verdieping hoger), strandbar (het Seashore House van Route 109), parasols, ligstoelen,
                           een "infinity pool" (een lagune: het is gewoon de zee), Birch met een drol, Misty, Erika,
                           de rivaal (post-game) en dronken fans.
  ParadisoResort_Lobby     Lobby met receptie (inchecken = gratis heal, zonder ja/nee); layout van de Contest Lobby
                           (gedeeld, kost geen ROM). Cynthia zit hier. De twee deuren achter de balie: de wijnzaal.
  ParadisoResort_WineHall  Wallace' wijnproeverij in de grote zaal (layout van de Contest Hall, gedeeld): Wallace op het
                           podium, sommeliers, fans en oude mannen die in emmers spugen.
  ParadisoResort_Bar       Strandbar (layout van het Seashore House, gedeeld) met Lorelei.

Gebruik: python3 tools/grounded/maptools/paradiso_resort.py [rendermap]"""
import collections, json, os, random, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chimney_ext as cx            # zet ook de werkmap op de repo-root
import ogerpon_quest as oq
import sea_market_steam as sms


def mt(v):
    return v & 0x3ff


REF = collections.defaultdict(collections.Counter)
_LAY = {l['name']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}
for _n in ('Route109', 'SlateportCity'):
    _l = _LAY[_n + '_Layout']
    for _v in struct.unpack('<%dH' % (_l['width'] * _l['height']), open(_l['blockdata_filepath'], 'rb').read()):
        REF[_v & 0x3ff][_v & ~0x3ff] += 1


def t(m, col=None, elev=None):
    base = REF[m].most_common(1)[0][0] if REF[m] else 0x3000
    c = (base >> 10) & 3 if col is None else (1 if col else 0)
    e = base >> 12 if elev is None else elev
    return m | (c << 10) | (e << 12)


WATER = 0x170
R109 = oq.read_layout('data/layouts/Route109/map.bin', 40, 63)
SLATE = oq.read_layout('data/layouts/SlateportCity/map.bin', 40, 60)

W, H = 40, 46
SPANS = {6: (14, 25), 7: (11, 28), 8: (9, 30), 9: (7, 32), 39: (7, 32), 40: (9, 30), 41: (12, 27)}
for _y in range(10, 39):
    SPANS[_y] = (6, 33)
LAGOON = {(x, y) for x in range(26, 32) for y in range(21, 26)}
HOTEL = (9, 11)                     # linksboven, 15 x 8
HOTEL_DOOR = (16, 18)
BAR = (25, 30)                      # Seashore House-stempel 5 x 4 (deur op (27,33))
BAR_DOOR = (27, 33)
SIGN = (19, 19)


def is_sand(x, y):
    if (x, y) in LAGOON:
        return False
    s = SPANS.get(y)
    return bool(s) and s[0] <= x <= s[1]


def sand_tile(x, y):
    n, s, w, e = (not is_sand(x, y - 1)), (not is_sand(x, y + 1)), (not is_sand(x - 1, y)), (not is_sand(x + 1, y))
    assert not (n and s) and not (w and e), ('te smal zand', x, y)
    if n and w: return 0x11b
    if n and e: return 0x11d
    if s and w: return 0x12b
    if s and e: return 0x12d
    if n: return 0x11c
    if s: return 0x12c
    if w: return 0x123
    if e: return 0x125
    if not is_sand(x - 1, y - 1): return 0x13d
    if not is_sand(x + 1, y - 1): return 0x13e
    if not is_sand(x - 1, y + 1): return 0x145
    if not is_sand(x + 1, y + 1): return 0x146
    return 0x124


def hotel(g):
    """Havengebouw van Slateport (x 25-31, y 7-12) verbreed tot 15 kolommen en met een extra raamrij."""
    x0, y0 = HOTEL
    WD = 15
    mid = WD // 2

    def row(left, middle, right):
        return [left] + [middle] * (WD - 2) + [right]
    rows = [row(0x295, 0x296, 0x297), row(0x29d, 0x29e, 0x29f), row(0x29d, 0x29e, 0x29f), row(0x29d, 0x29e, 0x29f),
            row(0x2a5, 0x2a6, 0x2a7)]
    # ronde ramen = 268 (linkerhelft) + 269 (rechterhelft); naast de deur vormen 268/2bd en 2bf/269 het raam
    win = [0x2ad] + [(0x2ae, 0x268, 0x269)[(i - 1) % 3] for i in range(1, WD - 1)] + [0x2af]
    rows.append(list(win))
    top = list(win)
    top[mid - 2:mid + 3] = [0x268, 0x2bd, 0x2be, 0x2bf, 0x269]
    top[mid - 3], top[mid + 3] = 0x2ae, 0x2ae
    rows.append(top)
    bot = row(0x2b5, 0x2b6, 0x2b7)
    bot[mid - 1:mid + 2] = [0x2c5, 0x2c6, 0x2d7]
    rows.append(bot)
    for j, r in enumerate(rows):
        for i, m_ in enumerate(r):
            g[y0 + j][x0 + i] = t(SANDED.get(m_, m_), m_ != 0x2c6)
    assert (x0 + mid, y0 + len(rows) - 1) == HOTEL_DOOR


SANDED = {}
BUILDING = (0x295, 0x296, 0x297, 0x29d, 0x29e, 0x29f, 0x2a5, 0x2a6, 0x2a7, 0x2ad, 0x2ae, 0x2af, 0x268, 0x269,
            0x2bd, 0x2be, 0x2bf, 0x2b5, 0x2b6, 0x2b7, 0x2c5, 0x2d7)


def building_on_sand():
    """Slateport: het havengebouw staat op gras; tegels waarvan de onderlaag gras/boom is (palet 2) krijgen een kopie
    met zand eronder (achteraan de tileset, vanilla-nummers blijven gelijk)."""
    gm = open('data/tilesets/primary/general/metatiles.bin', 'rb').read()
    sand = struct.unpack_from('<8H', gm, 0x124 * 16)
    for m_ in BUILDING:
        e, attr = sms._mt('slateport', m_)
        if any(v >> 12 == 2 for v in e[:4]):
            n = sms.ensure_metatile('slateport', struct.pack('<8H', *(sand[:4] + e[4:])), attr)
            SANDED[m_] = n
            REF[n] = REF[m_]


def stamp(g, src, sx, sy, w, h, dx, dy):
    for j in range(h):
        for i in range(w):
            g[dy + j][dx + i] = src[sy + j][sx + i]


UMB = {'orange': (0x2e4, 0x2e5, 0x2ec, 0x2ed, 0x2f4, 0x2f5), 'blue': (0x2e2, 0x2e3, 0x2ea, 0x2eb, 0x2f2, 0x2f3),
       'green': (0x2e6, 0x2e7, 0x2ee, 0x2ef, 0x2f6, 0x2f7)}


def umbrella(g, x, y, kind):
    ids = UMB[kind]
    for k, (i, j) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2))):
        assert mt(g[y + j][x + i]) == 0x124, ('parasol op de rand', x, y)
        g[y + j][x + i] = t(ids[k])


def column(g, x, y, ids):
    for j, m_ in enumerate(ids):
        assert mt(g[y + j][x]) == 0x124, ('decor op de rand', x, y)
        g[y + j][x] = t(m_)


def chair(g, x, y):
    column(g, x, y, (0x2e1, 0x2e9, 0x2f1))


def buoy(g, x, y):
    column(g, x, y, (0x2e0, 0x2e8, 0x2f0))


def foot_reach(g, starts):
    """Te voet: geen botsing en geen water."""
    seen, st = set(starts), list(starts)
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen:
                v = g[n[1]][n[0]]
                if cx.walkable(v) and mt(v) != WATER:
                    seen.add(n); st.append(n)
    return seen


P = 'ParadisoResort_EventScript_'


def exterior():
    name, const = 'ParadisoResort', 'PARADISO_RESORT'
    g = [[t(WATER, False, 1) for _ in range(W)] for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if is_sand(x, y):
                g[y][x] = t(sand_tile(x, y))
    hotel(g)
    stamp(g, R109, 10, 2, 5, 4, *BAR)                         # Seashore House van Route 109 = strandbar
    assert mt(g[BAR_DOOR[1]][BAR_DOOR[0]]) == 0x2db
    g[SIGN[1]][SIGN[0]] = t(0x294)
    # parasols, ligstoelen, zwembanden
    for x, y, k in ((12, 8, 'blue'), (25, 8, 'orange'), (7, 21, 'green'), (15, 33, 'orange'), (20, 35, 'blue'),
                    (9, 32, 'green'), (30, 16, 'orange')):
        umbrella(g, x, y, k)
    for x, y in ((27, 8), (14, 8), (17, 33), (18, 33), (22, 35), (11, 32)):
        chair(g, x, y)
    for x, y in ((24, 22), (32, 27)):
        buoy(g, x, y)
    # zeerotsen (primary), vaste seed; niet in de aanloop vanaf Route 109 (bovenste 10 rijen)
    rnd = random.Random(1090)
    ROCKS = ((0x150, 0x151, 0x158, 0x159), (0x175, 0x176, 0x17d, 0x17e))
    placed = 0
    while placed < 10:
        x, y = rnd.randint(0, W - 2), rnd.randint(10, H - 2)
        if any(mt(g[yy][xx]) != WATER for yy in range(y - 1, y + 3) for xx in range(x - 1, x + 3)
               if 0 <= yy < H and 0 <= xx < W):
            continue
        r = rnd.choice(ROCKS)
        for k, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
            g[y + dy][x + dx] = t(r[k], True, 1)
        placed += 1

    O = sms.obj
    objs = [
        O('OBJ_EVENT_GFX_PROF_BIRCH', 12, 36, P + 'Birch', move='MOVEMENT_TYPE_FACE_RIGHT', local_id='LOCALID_RESORT_BIRCH'),
        O('OBJ_EVENT_GFX_TURD', 13, 36, P + 'Turd'),
        O('OBJ_EVENT_GFX_VAR_0', 27, 9, P + 'Rival', 'FLAG_HIDE_RESORT_RIVAL', local_id='LOCALID_RESORT_RIVAL'),
        O('OBJ_EVENT_GFX_MISTY', 25, 23, P + 'Misty', move='MOVEMENT_TYPE_FACE_RIGHT'),
        O('OBJ_EVENT_GFX_SWIMMER_M', 28, 23, P + 'PoolSwimmer', move='MOVEMENT_TYPE_WANDER_AROUND', elev=1, rx=1, ry=1),
        O('OBJ_EVENT_GFX_SAILOR', 32, 22, P + 'Lifeguard', move='MOVEMENT_TYPE_FACE_LEFT'),
        O('OBJ_EVENT_GFX_ERIKA', 9, 23, P + 'Erika', move='MOVEMENT_TYPE_FACE_DOWN'),
        O('OBJ_EVENT_GFX_HIKER', 15, 22, P + 'DrunkHiker', move='MOVEMENT_TYPE_WANDER_AROUND', rx=2, ry=2),
        O('OBJ_EVENT_GFX_BEAUTY', 21, 25, P + 'DrunkBeauty', move='MOVEMENT_TYPE_WANDER_AROUND', rx=2, ry=1),
        O('OBJ_EVENT_GFX_FAT_MAN', 16, 29, P + 'DrunkFatMan', move='MOVEMENT_TYPE_FACE_RIGHT'),
        O('OBJ_EVENT_GFX_POKEFAN_M', 29, 37, P + 'DrunkFan', move='MOVEMENT_TYPE_WANDER_AROUND', rx=2, ry=1),
        O('OBJ_EVENT_GFX_MAN_3', 7, 13, P + 'Sunburn', move='MOVEMENT_TYPE_FACE_RIGHT'),
        O('OBJ_EVENT_GFX_OLD_WOMAN', 23, 38, P + 'Collector', move='MOVEMENT_TYPE_FACE_UP'),
        # Dave (post-game, met pensioen) op de ligstoel naast de oranje parasol; zelfde flag als de rivaal
        O('OBJ_EVENT_GFX_MAN_3', 18, 34, P + 'Dave', 'FLAG_HIDE_RESORT_RIVAL', move='MOVEMENT_TYPE_FACE_DOWN'),
    ]
    assert len(objs) <= 15
    bgs = [sms.sign(SIGN[0], SIGN[1], P + 'Sign', 'BG_EVENT_PLAYER_FACING_ANY'),
           sms.sign(30, 24, P + 'PoolSign', 'BG_EVENT_PLAYER_FACING_ANY')]
    warps = [{'x': HOTEL_DOOR[0], 'y': HOTEL_DOOR[1], 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT_LOBBY', 'dest_warp_id': '0'},
             {'x': BAR_DOOR[0], 'y': BAR_DOOR[1], 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT_BAR', 'dest_warp_id': '0'}]
    # controles
    start = [(20, 6)]
    r = foot_reach(g, start)
    for o in objs:
        if o['elevation'] == 1:
            assert (o['x'], o['y']) in LAGOON, o['script']
            continue
        assert (o['x'], o['y']) in r, ('object onbereikbaar', o['script'], o['x'], o['y'])
    for d in (HOTEL_DOOR, BAR_DOOR):
        assert (d[0], d[1] + 1) in r, ('deur onbereikbaar', d)
    assert (SIGN[0], SIGN[1] + 1) in r and (30, 26) in r
    assert sms.primary_only(g, range(0, 6)), 'bovenste rijen moeten primary zijn'
    assert all(mt(g[0][x]) == WATER for x in range(W)), 'aanloop vanaf Route 129 dicht'
    sms.save(g, name)
    sms.border(name, t(WATER, False, 1))
    oq.register_layout(name, const, W, H, 'gTileset_Slateport')
    sms.write_map(name, const, objs, warps, [], bgs, music='MUS_LILYCOVE', map_type='MAP_TYPE_TOWN',
                  region_map_section='MAPSEC_PARADISO_RESORT', allow_escaping=False,
                  connections=[{'map': 'MAP_ROUTE129', 'offset': -20, 'direction': 'up'}])
    oq.register_map(name)
    sms.set_connection('Route129', 'MAP_PARADISO_RESORT', 'down', 20)
    return name, g


def layout_grid(lid):
    g, _ = cx.load_layout(lid)
    return g


def check_spots(lid, objs, starts):
    g = layout_grid(lid)
    r = cx.reach(g, starts)
    for o in objs:
        if o.get('_behind'):
            continue
        assert (o['x'], o['y']) in r, ('object op een muur/onbereikbaar', lid, o['script'], o['x'], o['y'])
    for o in objs:
        o.pop('_behind', None)


def interior(name, const, base, layout, objs, warps, starts, **kw):
    check_spots('LAYOUT_' + layout, objs, starts)
    oq.write_map(name, const, base, layout, objs, warps, region_map_section='MAPSEC_PARADISO_RESORT', **kw)
    oq.register_map(name)


def lobby():
    L = 'ParadisoResort_Lobby_EventScript_'
    O = sms.obj
    objs = [
        O('OBJ_EVENT_GFX_TEALA', 14, 2, L + 'Receptionist'),
        O('OBJ_EVENT_GFX_TEALA', 15, 2, L + 'Concierge'),
        O('OBJ_EVENT_GFX_CYNTHIA', 26, 7, L + 'Cynthia', move='MOVEMENT_TYPE_FACE_LEFT'),
        O('OBJ_EVENT_GFX_GENTLEMAN', 6, 6, L + 'Bellhop', move='MOVEMENT_TYPE_FACE_RIGHT'),
        O('OBJ_EVENT_GFX_FAT_MAN', 4, 9, L + 'DrunkGuest', move='MOVEMENT_TYPE_FACE_UP'),
        O('OBJ_EVENT_GFX_WOMAN_2', 22, 9, L + 'DrunkWoman', move='MOVEMENT_TYPE_WANDER_AROUND', rx=1, ry=1),
        O('OBJ_EVENT_GFX_MAN_4', 28, 9, L + 'Complainer', move='MOVEMENT_TYPE_FACE_LEFT'),
        O('OBJ_EVENT_GFX_POKEFAN_F', 9, 3, L + 'WallaceFan', move='MOVEMENT_TYPE_FACE_UP'),
        O('OBJ_EVENT_GFX_BOY_1', 18, 7, L + 'Kid', move='MOVEMENT_TYPE_WANDER_AROUND', rx=2, ry=1),
    ]
    objs[0]['_behind'] = objs[1]['_behind'] = True
    warps = [{'x': 14, 'y': 11, 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT', 'dest_warp_id': '0'},
             {'x': 15, 'y': 11, 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT', 'dest_warp_id': '0'},
             {'x': 9, 'y': 1, 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT_WINE_HALL', 'dest_warp_id': '0'},
             {'x': 21, 'y': 1, 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT_WINE_HALL', 'dest_warp_id': '2'}]
    interior('ParadisoResort_Lobby', 'PARADISO_RESORT_LOBBY', 'LilycoveCity_ContestLobby', 'LILYCOVE_CITY_CONTEST_LOBBY',
             objs, warps, [(14, 10)], music='MUS_RG_SS_ANNE')


def wine_hall():
    L = 'ParadisoResort_WineHall_EventScript_'
    O = sms.obj
    objs = [
        O('OBJ_EVENT_GFX_WALLACE', 25, 11, L + 'Wallace', local_id='LOCALID_RESORT_WALLACE'),
        O('OBJ_EVENT_GFX_GENTLEMAN', 23, 12, L + 'Sommelier', move='MOVEMENT_TYPE_FACE_RIGHT'),
        O('OBJ_EVENT_GFX_BEAUTY', 22, 17, L + 'Fan1', move='MOVEMENT_TYPE_FACE_UP'),
        O('OBJ_EVENT_GFX_LASS', 28, 17, L + 'Fan2', move='MOVEMENT_TYPE_FACE_UP'),
        O('OBJ_EVENT_GFX_POKEFAN_F', 25, 18, L + 'Fan3', move='MOVEMENT_TYPE_FACE_UP'),
        O('OBJ_EVENT_GFX_OLD_MAN', 11, 23, L + 'Spitter1', move='MOVEMENT_TYPE_FACE_DOWN'),
        O('OBJ_EVENT_GFX_OLD_MAN', 13, 23, L + 'Spitter2', move='MOVEMENT_TYPE_FACE_DOWN'),
        O('OBJ_EVENT_GFX_OLD_MAN', 15, 23, L + 'Spitter3', move='MOVEMENT_TYPE_FACE_DOWN'),
        O('OBJ_EVENT_GFX_MOVING_BOX', 12, 24, L + 'Bucket'),
        O('OBJ_EVENT_GFX_EXPERT_F', 36, 23, L + 'Drinker1', move='MOVEMENT_TYPE_FACE_RIGHT'),
        O('OBJ_EVENT_GFX_MAN_5', 38, 23, L + 'Drinker2', move='MOVEMENT_TYPE_FACE_LEFT'),
        O('OBJ_EVENT_GFX_GENTLEMAN', 37, 25, L + 'Critic', move='MOVEMENT_TYPE_FACE_UP'),
        O('OBJ_EVENT_GFX_WOMAN_5', 8, 13, L + 'Lightweight', move='MOVEMENT_TYPE_FACE_DOWN'),
    ]
    assert len(objs) <= 15
    warps = [{'x': 19, 'y': 32, 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT_LOBBY', 'dest_warp_id': '2'},
             {'x': 20, 'y': 32, 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT_LOBBY', 'dest_warp_id': '2'},
             {'x': 30, 'y': 32, 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT_LOBBY', 'dest_warp_id': '3'},
             {'x': 31, 'y': 32, 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT_LOBBY', 'dest_warp_id': '3'}]
    interior('ParadisoResort_WineHall', 'PARADISO_RESORT_WINE_HALL', 'LilycoveCity_ContestHall', 'LILYCOVE_CITY_CONTEST_HALL',
             objs, warps, [(19, 31)], music='MUS_LILYCOVE_MUSEUM')


def bar():
    L = 'ParadisoResort_Bar_EventScript_'
    O = sms.obj
    objs = [
        O('OBJ_EVENT_GFX_POKEFAN_M', 6, 2, L + 'Bartender'),
        O('OBJ_EVENT_GFX_LORELEI', 10, 5, L + 'Lorelei', move='MOVEMENT_TYPE_FACE_LEFT'),
        O('OBJ_EVENT_GFX_SAILOR', 2, 3, L + 'DrunkSailor', move='MOVEMENT_TYPE_FACE_RIGHT'),
        O('OBJ_EVENT_GFX_TUBER_M', 12, 8, L + 'Tuber', move='MOVEMENT_TYPE_FACE_LEFT'),
    ]
    warps = [{'x': 6, 'y': 9, 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT', 'dest_warp_id': '1'},
             {'x': 7, 'y': 9, 'elevation': 0, 'dest_map': 'MAP_PARADISO_RESORT', 'dest_warp_id': '1'}]
    interior('ParadisoResort_Bar', 'PARADISO_RESORT_BAR', 'Route109_SeashoreHouse', 'ROUTE109_SEASHORE_HOUSE',
             objs, warps, [(6, 8)], music='MUS_RG_SS_ANNE')


if __name__ == '__main__':
    building_on_sand()
    name, _ = exterior()
    lobby()
    wine_hall()
    bar()
    if len(sys.argv) > 1:
        import subprocess
        for n, y1 in ((name, H), ('ParadisoResort_Lobby', 12), ('ParadisoResort_WineHall', 33), ('ParadisoResort_Bar', 10)):
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', str(y1)], check=True)
    print('klaar: PARADISO RESORT')
