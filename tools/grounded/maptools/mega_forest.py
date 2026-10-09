"""Project Grounded: het Mega Forest achter het Mini Forest (Route 102), met Zacian en Zamazenta (post-game).

Bouwt (idempotent, vaste seed):
- Route102_MiniForest: een opening van 1 breed in de noordrand (4, 0-1). Daarin ligt een omgevallen reuzenboom
  (object GIANT_LOG, verdwijnt na de Hall of Fame), met links het roestige zwaard (3,2) en rechts het roestige schild
  (5,2): "zwaard en schild met een boomstam in het midden" (sprites: tools/grounded/mega_forest_sprites.py).
  Na de HoF kun je het zwaard en het schild oppakken (ITEM_RUSTED_SWORD/SHIELD, Crowned-vormen in gevechten).
  Connection omhoog naar het Mega Forest (offset -10).
- MegaForest (48x56, General + Petalburg, zelfde tilesets als het Mini Forest, dus naadloos): Hoenn-bosbomen op een
  2x2-raster uit een grof plan (PLAN hieronder, 1 teken = 2x2 tegels), paden, hoog gras, een vijver, bloemen.
  Achterin een open plek met Zacian en Zamazenta (lv 70) en een bordje.
- Registratie: layouts.json, map_groups.json (gMapGroup_Grounded), event_scripts.s.
map.json wordt hier geschreven; scripts.inc van MegaForest en het Mini Forest-blok staan met de hand in data/maps.
Controleert de bereikbaarheid van alle events.
Gebruik: python3 tools/grounded/maptools/mega_forest.py"""
import json, os, random, struct
from collections import deque

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)
SEED = 888  # nationaal dexnummer van Zacian
rng = random.Random(SEED)
NAME, CONST = 'MegaForest', 'MEGA_FOREST'
OFFSET = 10                       # mega x = mini x + OFFSET
GAP_MINI = 4                      # opening in de noordrand van het Mini Forest

PLAN = [
    "TTTTTTTTTTTTTTTTTTTTTTTT",
    "TTTTTTTTT......TTTTTTTTT",
    "TTTTTTT..........TTTTTTT",
    "TTTTTTT..........TTTTTTT",
    "TTTTTTTT........TTTTTTTT",
    "TTTTTTTTTTT..TTTTTTTTTTT",
    "TTTTLLLTTTT..TTTTT...TTT",
    "TTT.LLLL..........LL.TTT",
    "TTT..LL..TTTTT.TT.LL.TTT",
    "TT...TTTTTTTTT.TT....TTT",
    "TT.L.TT......T.TTTT.TTTT",
    "TT.LL.T.www..T..LLL..TTT",
    "TT.LL...www..TT.LLL..TTT",
    "TT..TT.......TT..TTT.TTT",
    "TTT.TTTT.LL.TTT..TTT..TT",
    "TTT..TTT.LL......LL...TT",
    "TTTT...T..TTTTT..LL.T.TT",
    "TTTTT..TT.TTTTT.TTT.T.TT",
    "TT....LLL.TT......T...TT",
    "TT.TT.LLL.TT.LLL..TTT.TT",
    "TT.TT.....TT.LLL.....TTT",
    "TT.TTTTT.TTT.TTTTTTT.TTT",
    "TT...LL..TTT....LL...TTT",
    "TTTT.LL.TTTTTT..LL.TTTTT",
    "TTTT....TTTTTTT....TTTTT",
    "TTTTTT.TTTTTTTTTTTTTTTTT",
    "TTTTTT.......TTTTTTTTTTT",
    "TTTTTTT.TTTTTTTTTTTTTTTT",
]
CW, CH = len(PLAN[0]), len(PLAN)
assert all(len(r) == CW for r in PLAN)
W, H = CW * 2, CH * 2
ENTRY = (GAP_MINI + OFFSET, H - 1)
assert PLAN[-1][ENTRY[0] // 2] == '.' and ENTRY[0] % 2 == 0


def cell(cx, cy):
    if not (0 <= cx < CW and 0 <= cy < CH):
        return 'T'
    return PLAN[cy][cx]


def kind(x, y):
    return cell(x // 2, y // 2)


# ---------------------------------------------------------------- metatiles (General + Petalburg)
GRASS, TALL, FLOWER, BANK, SIGN = 0x001, 0x00D, 0x004, 0x002, 0x01B


def val(mt, coll, elev):
    return mt | (coll << 10) | (elev << 12)


M = [[val(GRASS, 0, 3) for _ in range(W)] for _ in range(H)]
for y in range(H):
    for x in range(W):
        k = kind(x, y)
        if k == 'L':
            M[y][x] = val(TALL, 0, 3)
        elif k == 'w':
            up, lf, rt = kind(x, y - 1) != 'w', kind(x - 1, y) != 'w', kind(x + 1, y) != 'w'
            ul, ur = kind(x - 1, y - 1) != 'w', kind(x + 1, y - 1) != 'w'
            assert kind(x, y + 1) != 'T', 'vijver tegen bomen'
            mt = (0xB0 if lf else 0xB2 if rt else 0xB1) if up else 0xB8 if lf else 0xBA if rt else \
                0xC0 if ul else 0xC2 if ur else 0xA1
            M[y][x] = val(mt, 0, 1)
        elif kind(x, y - 1) == 'w':
            M[y][x] = val(BANK, 0, 3)
# Hoenn-bosbomen: per boomcel een 2x2-boom; buiten de kaart telt als bos, behalve onder de kaart (daar begint
# het Mini Forest met kleine boompjes, dus de onderste rij krijgt stammen).
for cy in range(CH):
    for cx in range(CW):
        if cell(cx, cy) != 'T':
            continue
        x, y = cx * 2, cy * 2
        Lf, R = cell(cx - 1, cy) == 'T', cell(cx + 1, cy) == 'T'
        B = cy + 1 < CH and cell(cx, cy + 1) == 'T'
        M[y][x] = val(0x1D4 if Lf else 0x1D6, 1, 0); M[y][x + 1] = val(0x1D5 if R else 0x1D7, 1, 0)
        if B:
            M[y + 1][x] = val(0x1DC, 1, 0); M[y + 1][x + 1] = val(0x1DD, 1, 0)
        else:
            M[y + 1][x] = val(0x1E4 if Lf else 0x1E6, 1, 0); M[y + 1][x + 1] = val(0x1E5 if R else 0x1E7, 1, 0)
        if cy > 0 and cell(cx, cy - 1) != 'T':            # kruin over de onderste rij van de open cel erboven
            assert cell(cx, cy - 1) != 'w'
            M[y - 1][x] = val(0x1CE, 0, 3); M[y - 1][x + 1] = val(0x1CF, 0, 3)
CANOPY = {(x, y) for y in range(H) for x in range(W) if M[y][x] & 0x3FF in (0x1CE, 0x1CF)}

# ---------------------------------------------------------------- events
LEGENDS = [('LOCALID_MEGA_FOREST_ZACIAN', 'ZACIAN', 20, 5, 'FLAG_HIDE_MEGA_FOREST_ZACIAN'),
           ('LOCALID_MEGA_FOREST_ZAMAZENTA', 'ZAMAZENTA', 27, 5, 'FLAG_HIDE_MEGA_FOREST_ZAMAZENTA')]
SIGN_XY = (23, 3)
# (x, y, trainer, gfx, script, richting, zicht)
TRAINERS = [(28, 15, 'TRAINER_MEGA_FOREST_PERCIVAL', 'OBJ_EVENT_GFX_CAMPER', 'MegaForest_EventScript_Percival', 'LEFT', 4),
            (6, 30, 'TRAINER_MEGA_FOREST_MORGANA', 'OBJ_EVENT_GFX_HEX_MANIAC', 'MegaForest_EventScript_Morgana', 'DOWN', 4),
            (34, 40, 'TRAINER_MEGA_FOREST_GWEN', 'OBJ_EVENT_GFX_PICNICKER', 'MegaForest_EventScript_Gwen', 'LEFT', 4)]
ITEMS = [(6, 19, 'ITEM_SWEET_APPLE', 'FLAG_ITEM_MEGA_FOREST_SWEET_APPLE'),
         (40, 13, 'ITEM_TART_APPLE', 'FLAG_ITEM_MEGA_FOREST_TART_APPLE'),
         (5, 44, 'ITEM_MAX_REVIVE', 'FLAG_ITEM_MEGA_FOREST_MAX_REVIVE'),
         (42, 30, 'ITEM_PP_MAX', 'FLAG_ITEM_MEGA_FOREST_PP_MAX')]
HIDDEN = [(24, 22, 'ITEM_STAR_PIECE', 'FLAG_HIDDEN_ITEM_MEGA_FOREST_STAR_PIECE'),
          (4, 36, 'ITEM_BIG_NUGGET', 'FLAG_HIDDEN_ITEM_MEGA_FOREST_BIG_NUGGET')]
EVENTS = [(x, y) for _, _, x, y, _ in LEGENDS] + [SIGN_XY] + [(x, y) for x, y, *_ in TRAINERS + ITEMS]
for x, y in EVENTS + [(x, y) for x, y, *_ in HIDDEN]:
    assert kind(x, y) in '.L' and (x, y) not in CANOPY, ('event niet op open grond', x, y)
M[SIGN_XY[1]][SIGN_XY[0]] = val(SIGN, 1, 3)

# bloemenkrans rond de helden en losse bloemen
for (x, y) in [(19, 4), (21, 4), (19, 6), (21, 6), (26, 4), (28, 4), (26, 6), (28, 6), (22, 3), (24, 3), (23, 4)]:
    M[y][x] = val(FLOWER, 0, 3)
KEEP = set(EVENTS) | {(x, y) for x, y, *_ in HIDDEN} | {(x + dx, y + dy) for x, y in EVENTS for dx, dy in
                                                          ((1, 0), (-1, 0), (0, 1), (0, -1))}
for y in range(H):
    for x in range(W):
        if M[y][x] & 0x3FF == GRASS and (x, y) not in KEEP and (x, y) not in CANOPY and rng.random() < 0.07:
            M[y][x] = val(FLOWER, 0, 3)


# ---------------------------------------------------------------- bereikbaarheid
def bfs(start, blocked):
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and n not in blocked:
                v = M[n[1]][n[0]]
                if (v >> 10) & 3 == 0 and v >> 12 == 3:
                    seen.add(n); q.append(n)
    return seen


walk = bfs(ENTRY, set(EVENTS))
near = lambda x, y: any((x + dx, y + dy) in walk for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
for x, y in EVENTS:
    assert near(x, y), ('onbereikbaar', x, y)
for x, y, *_ in HIDDEN:
    assert (x, y) in walk, ('verborgen item onbereikbaar', x, y)
# trainers mogen geen doorgang afsluiten: alles wat zonder hen bereikbaar is, blijft het met hen
free = bfs(ENTRY, set())
lost = {p for p in free - walk if p not in EVENTS}
assert not lost, ('afgesloten door een event', sorted(lost)[:5])
print('Mega Forest: %d begaanbare tegels' % len(walk))

# ---------------------------------------------------------------- schrijven
os.makedirs('data/layouts/' + NAME, exist_ok=True)
open('data/layouts/%s/map.bin' % NAME, 'wb').write(b''.join(struct.pack('<H', v) for r in M for v in r))
open('data/layouts/%s/border.bin' % NAME, 'wb').write(struct.pack('<4H', *(val(m, 1, 0) for m in (0x1D4, 0x1D5, 0x1DC, 0x1DD))))


def obj(gfx, x, y, script, flag, move='MOVEMENT_TYPE_FACE_DOWN', ttype='TRAINER_TYPE_NONE', sight='0', lid=None):
    o = {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': 3, 'movement_type': move, 'movement_range_x': 0,
         'movement_range_y': 0, 'trainer_type': ttype, 'trainer_sight_or_berry_tree_id': sight, 'script': script,
         'flag': flag}
    return dict(local_id=lid, **o) if lid else o


objs = [obj('OBJ_EVENT_GFX_SPECIES(%s)' % sp, x, y, 'MegaForest_EventScript_%s' % sp.title(), f, lid=lid)
        for lid, sp, x, y, f in LEGENDS]
objs += [obj(g, x, y, s, '0', 'MOVEMENT_TYPE_FACE_' + d, 'TRAINER_TYPE_NORMAL', str(r)) for x, y, _, g, s, d, r in TRAINERS]
objs += [obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', f, sight=i) for x, y, i, f in ITEMS]
bgs = [{'type': 'sign', 'x': SIGN_XY[0], 'y': SIGN_XY[1], 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
        'script': 'MegaForest_EventScript_Plaque'}]
bgs += [{'type': 'hidden_item', 'x': x, 'y': y, 'elevation': 3, 'item': i, 'flag': f} for x, y, i, f in HIDDEN]
mj = {'id': 'MAP_' + CONST, 'name': NAME, 'layout': 'LAYOUT_' + CONST, 'music': 'MUS_RG_VIRIDIAN_FOREST',
      'region_map_section': 'MAPSEC_ROUTE_102', 'requires_flash': False, 'weather': 'WEATHER_SHADE',
      'map_type': 'MAP_TYPE_ROUTE', 'allow_cycling': True, 'allow_escaping': False, 'allow_running': True,
      'show_map_name': True, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL',
      'connections': [{'map': 'MAP_ROUTE102_MINI_FOREST', 'offset': OFFSET, 'direction': 'down'}],
      'object_events': objs, 'warp_events': [], 'coord_events': [], 'bg_events': bgs}
os.makedirs('data/maps/' + NAME, exist_ok=True)
open('data/maps/%s/map.json' % NAME, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')

# Mini Forest: opening in de noordrand + objecten + connection omhoog
MINI = 'data/layouts/Route102_MiniForest/map.bin'
mv = list(struct.unpack('<572H', open(MINI, 'rb').read()))
for y in (0, 1):
    mv[y * 26 + GAP_MINI] = val(GRASS, 0, 3)
open(MINI, 'wb').write(struct.pack('<572H', *mv))
mp = 'data/maps/Route102_MiniForest/map.json'
md = json.load(open(mp))
if not any(c['map'] == 'MAP_MEGA_FOREST' for c in md['connections']):
    md['connections'].append({'map': 'MAP_MEGA_FOREST', 'offset': -OFFSET, 'direction': 'up'})
md['object_events'] = [o for o in md['object_events'] if 'MegaForest' not in o['script'] and 'MiniForest_EventScript' not in o['script']]
md['object_events'] += [
    obj('OBJ_EVENT_GFX_GIANT_LOG', GAP_MINI, 1, 'Route102_MiniForest_EventScript_GiantLog', 'FLAG_HIDE_MINI_FOREST_GIANT_LOG'),
    obj('OBJ_EVENT_GFX_RUSTED_SWORD_OW', GAP_MINI - 1, 2, 'Route102_MiniForest_EventScript_RustedSword', 'FLAG_RECEIVED_RUSTED_SWORD',
        lid='LOCALID_MINI_FOREST_RUSTED_SWORD'),
    obj('OBJ_EVENT_GFX_RUSTED_SHIELD_OW', GAP_MINI + 1, 2, 'Route102_MiniForest_EventScript_RustedShield', 'FLAG_RECEIVED_RUSTED_SHIELD',
        lid='LOCALID_MINI_FOREST_RUSTED_SHIELD')]
open(mp, 'w').write(json.dumps(md, indent=2, ensure_ascii=False) + '\n')

# registratie
lj = open('data/layouts/layouts.json').read()
if '"LAYOUT_%s"' % CONST not in lj:
    i = lj.index('"name": "Route102_MiniForest_Layout"'); j = lj.index('},', i) + 2
    lj = lj[:j] + '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_Petalburg",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (CONST, NAME, W, H, NAME, NAME) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)
g = open('data/maps/map_groups.json').read()
if '"%s"' % NAME not in g:
    i = g.index('"gMapGroup_Grounded": ['); j = g.index(']', i)
    k = g.rindex('"', i, j) + 1
    g = g[:k] + ',\n    "%s"' % NAME + g[k:]
    open('data/maps/map_groups.json', 'w').write(g)
es = open('data/event_scripts.s').read()
inc = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
if inc not in es:
    a = '\t.include "data/maps/Route102_MiniForest/scripts.inc"\n'
    es = es.replace(a, a + inc, 1)
    open('data/event_scripts.s', 'w').write(es)
print('klaar')
