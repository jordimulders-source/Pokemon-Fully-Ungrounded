"""Project Grounded: de Hoopa-quest (Mirage Bazaar). Deterministisch en idempotent.

  MirageBazaar        Een bazaar op een zandeiland in een luchtspiegeling (water dat er niet is), General + Slateport:
                      de marktkramen van Slateport (blauwe tenten, oranje luifel, parasols, manden, potten, kratten)
                      op zand. Kopieën met een zand-onderlaag staan achteraan de Slateport-tileset (op inhoud gezocht,
                      vanilla-nummers blijven gelijk). Ingang: een ring van Hoopa die post-game in de zandstorm van
                      Route 111 hangt (object, OBJ_EVENT_GFX_HOOPA_RING). Je komt binnen bij de ring onderaan.
  MirageBazaar_Vault  Hoopa's schatkamer: de hal van de Battle Pyramid-lobby (Building + BattlePyramid) verbreed en
                      met een lange benedenhal vol gestolen Hoenn-spullen, rondom leegte. Hoopa Unbound bovenaan de
                      trap.
Route 111: de ring in de woestijn (object achteraan, zichtbaar via het map-script alleen na de Hall of Fame).
Controleert de bereikbaarheid van alle objecten en tekens.

Gebruik: python3 tools/grounded/maptools/mirage_bazaar.py [rendermap]"""
import collections, json, os, struct, sys

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


WATER, SAND = 0x170, 0x124

# ====================================================================== zand-kopieën van de marktkramen
SANDED = {}
GOODS = (0x20b, 0x20c, 0x213, 0x214, 0x21b, 0x21c, 0x223, 0x224, 0x22b, 0x344,          # manden, potten
         0x32e, 0x336, 0x32f, 0x337, 0x33e, 0x33f,                                       # kratten (2 hoog)
         0x270, 0x271, 0x272, 0x278, 0x279, 0x27a, 0x263, 0x264,                         # oranje luifel + palen
         0x225, 0x20d, 0x20e, 0x20f, 0x227, 0x22d, 0x2f8, 0x2f9, 0x2fa, 0x22f, 0x23d, 0x26c)  # blauwe tent


def sand_copies():
    gm = open('data/tilesets/primary/general/metatiles.bin', 'rb').read()
    sand = struct.unpack_from('<8H', gm, SAND * 16)
    for m_ in GOODS:
        e, attr = sms._mt('slateport', m_)
        n = sms.ensure_metatile('slateport', struct.pack('<8H', *(sand[:4] + e[4:])), attr)
        SANDED[m_] = n
        REF[n] = REF[m_]


def S(m_, col=None):
    return t(SANDED[m_], col)


# ====================================================================== de bazaar
W, H = 30, 27
SPANS = {2: (6, 23), 3: (4, 25), 23: (4, 25), 24: (6, 23)}
for _y in range(4, 23):
    SPANS[_y] = (3, 26)
ARRIVE = (14, 20)               # hier zet de ring uit de woestijn je neer (kijkt omhoog)
EXIT_RING = (14, 22)
HOOPA = (14, 7)                 # onder de luifel van Salim; daarna de ring naar de schatkamer
SALIM = (12, 8)
SIGN = (16, 21)


def is_sand(x, y):
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
    return SAND


def put(g, x, y, v):
    assert mt(g[y][x]) == SAND, ('decor op de rand of op decor', x, y, hex(mt(g[y][x])))
    g[y][x] = v


def tent(g, x, y, goods):
    rows = [(0x225, 0x20d, 0x20e, 0x20f, 0x227), (0x22d, 0x2f8, 0x2f9, 0x2fa, 0x22f), (0x23d,) + goods + (0x26c,)]
    for j, r in enumerate(rows):
        for i, m_ in enumerate(r):
            put(g, x + i, y + j, S(m_, True))


def canopy(g, x, y, goods):
    rows = [(0x270, 0x271, 0x271, 0x271, 0x272), (0x278, 0x279, 0x279, 0x279, 0x27a)]
    for j, r in enumerate(rows):
        for i, m_ in enumerate(r):
            put(g, x + i, y + j, S(m_, True))
    put(g, x, y + 2, S(0x263, True))
    put(g, x + 4, y + 2, S(0x264, True))
    for i, m_ in enumerate(goods):
        if m_:
            put(g, x + 1 + i, y + 2, S(m_, True))


def umbrella(g, x, y, kind):
    ids = {'orange': (0x2e4, 0x2e5, 0x2ec, 0x2ed, 0x2f4, 0x2f5), 'blue': (0x2e2, 0x2e3, 0x2ea, 0x2eb, 0x2f2, 0x2f3),
           'green': (0x2e6, 0x2e7, 0x2ee, 0x2ef, 0x2f6, 0x2f7)}[kind]
    for k, (i, j) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2))):
        put(g, x + i, y + j, t(ids[k]))


def crate(g, x, y, top=0x32f, bot=0x337):
    put(g, x, y, S(top, True))
    put(g, x, y + 1, S(bot, True))


B = 'MirageBazaar_EventScript_'


def bazaar():
    name, const = 'MirageBazaar', 'MIRAGE_BAZAAR'
    g = [[t(WATER, False, 1) for _ in range(W)] for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if is_sand(x, y):
                g[y][x] = t(sand_tile(x, y), False, 3)
    # Salims luifel (midden boven): pot, plek van Hoopa, sinaasappels
    canopy(g, 12, 5, (0x20c, None, 0x22b))
    put(g, 10, 6, S(0x213, True)); put(g, 18, 6, S(0x214, True))
    crate(g, 9, 5, 0x33e, 0x336); crate(g, 19, 5, 0x32e, 0x336)
    # blauwe tenten links en rechts
    tent(g, 4, 6, (0x21b, 0x21c, 0x21b))
    tent(g, 4, 13, (0x223, 0x224, 0x223))
    tent(g, 21, 6, (0x20b, 0x344, 0x20b))
    tent(g, 21, 13, (0x22b, 0x20c, 0x22b))
    # parasolkramen met waar ernaast
    umbrella(g, 10, 12, 'orange'); put(g, 12, 14, S(0x21c, True)); put(g, 9, 14, S(0x344, True))
    umbrella(g, 17, 12, 'green'); put(g, 19, 14, S(0x223, True)); put(g, 16, 14, S(0x20c, True))
    umbrella(g, 6, 19, 'blue'); put(g, 8, 21, S(0x214, True))
    umbrella(g, 22, 19, 'orange'); put(g, 21, 21, S(0x22b, True))
    crate(g, 4, 18); crate(g, 25, 9, 0x33e, 0x336); crate(g, 4, 10, 0x32e, 0x336)
    for x, y, m_ in ((11, 17, 0x20c), (18, 17, 0x20c), (25, 17, 0x21b), (13, 3, 0x20b), (16, 3, 0x213)):
        put(g, x, y, S(m_, True))
    put(g, SIGN[0], SIGN[1], t(0x294))

    O = sms.obj
    objs = [
        O('OBJ_EVENT_GFX_HOOPA_RING', EXIT_RING[0], EXIT_RING[1], B + 'ExitRing', local_id='LOCALID_MIRAGE_BAZAAR_EXIT_RING'),
        O('OBJ_EVENT_GFX_EXPERT_M', SALIM[0], SALIM[1], B + 'Salim', 'FLAG_HIDE_MIRAGE_BAZAAR_SALIM',
          local_id='LOCALID_MIRAGE_BAZAAR_SALIM'),
        O('OBJ_EVENT_GFX_SPECIES(HOOPA_CONFINED)', HOOPA[0], HOOPA[1], B + 'Hoopa', 'FLAG_HIDE_MIRAGE_BAZAAR_HOOPA',
          local_id='LOCALID_MIRAGE_BAZAAR_HOOPA'),
        O('OBJ_EVENT_GFX_HOOPA_RING', HOOPA[0], HOOPA[1], B + 'VaultRing', 'FLAG_HIDE_MIRAGE_BAZAAR_VAULT_RING',
          local_id='LOCALID_MIRAGE_BAZAAR_VAULT_RING'),
        O('OBJ_EVENT_GFX_MART_EMPLOYEE', 6, 9, B + 'Mart'),
        O('OBJ_EVENT_GFX_OLD_MAN', 6, 16, B + 'RugSeller'),
        O('OBJ_EVENT_GFX_HEX_MANIAC', 23, 9, B + 'FortuneTeller'),
        O('OBJ_EVENT_GFX_RICH_BOY', 23, 16, B + 'Refunds'),
        O('OBJ_EVENT_GFX_SPECIES(HIPPOWDON)', 19, 21, B + 'Hippowdon', move='MOVEMENT_TYPE_FACE_LEFT'),
        O('OBJ_EVENT_GFX_BOY_2', 14, 15, B + 'Kid', move='MOVEMENT_TYPE_WANDER_AROUND', rx=2, ry=1),
        O('OBJ_EVENT_GFX_POKEFAN_F', 11, 15, B + 'Shopper', move='MOVEMENT_TYPE_FACE_UP'),
        O('OBJ_EVENT_GFX_FISHERMAN', 26, 21, B + 'MirageFisher', move='MOVEMENT_TYPE_FACE_RIGHT'),
    ]
    assert len(objs) <= 15
    bgs = [sms.sign(SIGN[0], SIGN[1], B + 'Sign', 'BG_EVENT_PLAYER_FACING_ANY')]
    # controles: alles bereikbaar vanaf de aankomst (te voet: geen water)
    r = foot_reach(g, [ARRIVE])
    for o in objs:
        assert any(n in r for n in around(o['x'], o['y'])), ('object onbereikbaar', o['script'])
        assert cx.walkable(g[o['y']][o['x']]), ('object op decor', o['script'], o['x'], o['y'])
    assert any(n in r for n in around(*SIGN))
    assert (HOOPA[0], HOOPA[1] + 1) in r, 'Hoopa niet van voren aan te spreken'
    sms.save(g, name)
    sms.border(name, t(WATER, True, 1))
    oq.register_layout(name, const, W, H, 'gTileset_Slateport')
    sms.write_map(name, const, objs, [], [], bgs, music='MUS_RG_CELADON', map_type='MAP_TYPE_TOWN',
                  region_map_section='MAPSEC_ROUTE_111', allow_escaping=False, allow_cycling=False,
                  show_map_name=False, weather='WEATHER_SUNNY')
    oq.register_map(name)
    return name, g


def around(x, y):
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def foot_reach(g, starts):
    seen, st = set(starts), list(starts)
    while st:
        x, y = st.pop()
        for n in around(x, y):
            if 0 <= n[0] < len(g[0]) and 0 <= n[1] < len(g) and n not in seen:
                v = g[n[1]][n[0]]
                if cx.walkable(v) and mt(v) != WATER:
                    seen.add(n); st.append(n)
    return seen


# ====================================================================== de schatkamer
VW, VH = 23, 23
LX = 4                           # kolom van de Pyramid-lobby (15 breed) in de schatkamer
V_ARRIVE = (11, 19)
V_EXIT = (11, 21)
V_HOOPA = (11, 5)
V = 'MirageBazaar_Vault_EventScript_'


def vault():
    name, const = 'MirageBazaar_Vault', 'MIRAGE_BAZAAR_VAULT'
    lob = oq.read_layout('data/layouts/BattleFrontier_BattlePyramidLobby/map.bin', 15, 18)
    void = lob[0][0]
    floor = lob[14][0]
    g = [[floor] * VW for _ in range(VH)]
    for y in range(14):
        for x in range(VW):
            g[y][x] = lob[y][x - LX] if LX <= x < LX + 15 else lob[y][14]
    for y in range(VH):
        g[y][0] = g[y][VW - 1] = void
    for x in range(VW):
        g[VH - 1][x] = void
    # de blauwe tegel van de lobby (opgang naar de top) is Hoopa's troon: dicht
    assert mt(g[4][LX + 7]) == 0x20d
    g[4][LX + 7] |= 0x400
    O = cx.obj
    objs = [
        O('OBJ_EVENT_GFX_HOOPA_RING', V_EXIT[0], V_EXIT[1], V + 'ExitRing', local_id='LOCALID_HOOPA_VAULT_EXIT_RING'),
        O('OBJ_EVENT_GFX_SPECIES(HOOPA_UNBOUND)', V_HOOPA[0], V_HOOPA[1], V + 'Hoopa', 'FLAG_HIDE_HOOPA_VAULT_HOOPA',
          local_id='LOCALID_HOOPA_VAULT_HOOPA'),
        O('OBJ_EVENT_GFX_EXPERT_M', 13, 18, V + 'Salim', 'FLAG_HIDE_HOOPA_VAULT_SALIM',
          local_id='LOCALID_HOOPA_VAULT_SALIM', move='MOVEMENT_TYPE_FACE_LEFT'),
        # de buit
        O('OBJ_EVENT_GFX_BIRCHS_BAG', 3, 15, V + 'BirchsBag'),
        O('OBJ_EVENT_GFX_TRUCK', 5, 18, V + 'Truck'),
        O('OBJ_EVENT_GFX_MR_BRINEYS_BOAT', 17, 18, V + 'Boat'),
        O('OBJ_EVENT_GFX_CABLE_CAR', 19, 15, V + 'CableCar'),
        O('OBJ_EVENT_GFX_WINGULL', 8, 15, V + 'Peeko', move='MOVEMENT_TYPE_FACE_RIGHT'),
        O('OBJ_EVENT_GFX_POOCHYENA', 15, 15, V + 'Poochyena', move='MOVEMENT_TYPE_FACE_LEFT'),
        O('OBJ_EVENT_GFX_FOSSIL', 2, 8, V + 'Fossil'),
        O('OBJ_EVENT_GFX_MOVING_BOX', 20, 8, V + 'Box'),
        cx.item(2, 19, 'ITEM_RELIC_CROWN', 'FLAG_ITEM_HOOPA_VAULT_1'),
        cx.item(20, 20, 'ITEM_COMET_SHARD', 'FLAG_ITEM_HOOPA_VAULT_2'),
        cx.item(11, 15, 'ITEM_RELIC_GOLD', 'FLAG_ITEM_HOOPA_VAULT_3'),
    ]
    assert len(objs) <= 15
    for o in objs:
        o['elevation'] = 4                  # vloer van de Pyramid-lobby
    bgs = [cx.sign(LX + 1, 12, V + 'StolenPC'), cx.sign(LX + 13, 12, V + 'StolenMachine'),
           cx.sign(LX + 5, 4, V + 'Statue'), cx.sign(LX + 9, 4, V + 'Statue')]
    r = cx.reach(g, [V_ARRIVE])
    big = {'OBJ_EVENT_GFX_TRUCK', 'OBJ_EVENT_GFX_MR_BRINEYS_BOAT', 'OBJ_EVENT_GFX_CABLE_CAR'}
    for o in objs:
        assert cx.walkable(g[o['y']][o['x']]), ('object op een muur', o['script'], o['x'], o['y'])
        assert any(n in r for n in around(o['x'], o['y'])), ('object onbereikbaar', o['script'])
    assert (V_HOOPA[0], V_HOOPA[1] + 1) in r, 'Hoopa niet bereikbaar via de trap'
    for b in bgs:
        assert any(n in r for n in around(b['x'], b['y'])), ('teken onbereikbaar', b['script'])
    # grote sprites (vrachtwagen, boot, kabelbaan) mogen de doorgang naar de trap niet versperren
    blocked = {(o['x'], o['y']) for o in objs}
    r2 = cx.reach(g, [V_ARRIVE], blocked=blocked)
    assert (V_HOOPA[0], V_HOOPA[1] + 1) in r2, 'objecten versperren de weg naar Hoopa'
    os.makedirs('data/layouts/' + name, exist_ok=True)
    cx.save_grid(g, 'data/layouts/%s/map.bin' % name)
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', void, void, void, void))
    register_building_layout(name, const, VW, VH)
    oq.write_map(name, const, 'BattleFrontier_BattlePyramidLobby', const, objs, [],
                 music='MUS_B_PYRAMID_TOP', region_map_section='MAPSEC_ROUTE_111', bg_events=bgs,
                 map_type='MAP_TYPE_INDOOR', allow_escaping=False, show_map_name=False)
    oq.register_map(name)
    return name, g


def register_building_layout(name, const, W_, H_):
    oq.register_layout(name, const, W_, H_, 'gTileset_BattlePyramid')
    lj = open('data/layouts/layouts.json').read()
    i = lj.index('"id": "LAYOUT_%s"' % const)
    j = lj.index('"primary_tileset": "gTileset_General"', i)
    assert j < lj.index('}', i)
    lj = lj[:j] + '"primary_tileset": "gTileset_Building"' + lj[j + len('"primary_tileset": "gTileset_General"'):]
    open('data/layouts/layouts.json', 'w').write(lj)
    json.loads(lj)


# ====================================================================== Route 111: de ring in de zandstorm
R111_RING = (33, 57)


def route111():
    def fn(m):
        for o in m['object_events']:
            if o.get('local_id') == 'LOCALID_ROUTE111_HOOPA_RING':
                o.update({'x': R111_RING[0], 'y': R111_RING[1]})
                return
        m['object_events'].append(cx.obj('OBJ_EVENT_GFX_HOOPA_RING', R111_RING[0], R111_RING[1],
                                         'Route111_EventScript_HoopaRing', 'FLAG_HIDE_ROUTE111_HOOPA_RING',
                                         local_id='LOCALID_ROUTE111_HOOPA_RING'))
    oq.edit_map('Route111', fn)
    g, _ = cx.load_layout('LAYOUT_ROUTE111')
    r = cx.reach(g, [(19, 59)])
    assert cx.walkable(g[R111_RING[1]][R111_RING[0]]) and (R111_RING[0], R111_RING[1] + 1) in r, 'ring niet bereikbaar'


if __name__ == '__main__':
    sand_copies()
    names = [bazaar()[0], vault()[0]]
    route111()
    if len(sys.argv) > 1:
        import subprocess
        for n, h in zip(names, (H, VH)):
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', str(h)], check=True)
    print('klaar:', ', '.join(names))
