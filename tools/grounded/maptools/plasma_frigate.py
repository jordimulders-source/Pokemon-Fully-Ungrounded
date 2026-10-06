"""Project Grounded: Nothing Island en de Plasma Frigate (post-game Genesect-sidequest, Neo Team Plasma).

Vier kaarten (alle in gMapGroup_Grounded):
- NothingIsland (44x40, General + Dewford, mist): zandeiland uit Route 105 (x 9-19, y 40-63) met rotsruggen en
  zeerotsen, een steiger (Dewford-steiger) naar de aangemeerde Plasma Frigate (S.S. Tidal-sprite met een eigen palet,
  OBJ_EVENT_GFX_PLASMA_FRIGATE). Verbonden met de westrand van Route 105 (zelfde tilesets: General + Dewford). Aan
  boord gaan = coord-trigger aan het eind van de steiger (warp naar de gang).
- PlasmaFrigate_Corridor (kopie SSTidalCorridor): 4 onderste hutdeuren (kleurdeuren, bewakers), 4 bovenste,
  trap naar het ruim (Shadow Triad), trap terug naar het eiland (linksonder).
- PlasmaFrigate_Cabins (kopie SSTidalRooms): 8 hutten; de onderste 4 hebben elk een terminal met de volgende kleurcode.
- PlasmaFrigate_Hold (kopie SSTidalLowerDeck, middelste kratten weg): het ruim/vrieslab met Zinzolin, Rood en Genesect.
Idempotent. Controleert bereikbaarheid (lopen + surfen) van alle objecten, warps en triggers.
Scripts staan met de hand in data/maps/<kaart>/scripts.inc.
Gebruik: python3 tools/grounded/maptools/plasma_frigate.py [rendermap]"""
import json, os, random, struct, subprocess, sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)
LAY = {l['name']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}


def load(name):
    l = LAY[name + '_Layout']
    w, h = l['width'], l['height']
    v = struct.unpack('<%dH' % (w * h), open(l['blockdata_filepath'], 'rb').read())
    return [list(v[y * w:(y + 1) * w]) for y in range(h)]


def mt(v):
    return v & 0x3FF


def solid(v):
    return (v >> 10) & 3


COL = 1 << 10
WATER = 0x170

# ====================================================================== Nothing Island
W, H = 44, 40
isl = [[WATER] * W for _ in range(H)]
r105 = load('Route105')
# zandeiland met bomen uit Route 105 (x 9-19, y 40-63); alleen de niet-watertegels
IX, IY = 13, 6                     # plek op de nieuwe kaart
for y in range(40, 64):
    for x in range(9, 20):
        t = r105[y][x]
        if mt(t) != WATER and not 0x150 <= mt(t) <= 0x17e:     # zeerotsen aan de rand van het stuk niet meenemen
            isl[IY + y - 40][IX + x - 9] = t
# rotsrug uit Route 105 (x 29-34, y 8-25) aan de westkant
for (sx0, sy0, sx1, sy1, dx, dy) in ((29, 8, 34, 25, 3, 9),):
    for y in range(sy0, sy1 + 1):
        for x in range(sx0, sx1 + 1):
            t = r105[y][x]
            if mt(t) != WATER:
                isl[dy + y - sy0][dx + x - sx0] = t

# steiger (Dewford): rij R, vanaf de oostoever van het eiland 5 tegels de zee in
R = IY + 9                          # rij op de nieuwe kaart
xe = max(x for x in range(W) if mt(isl[R][x]) in (0x124, 0x125, 0x13e, 0x11c, 0x146) and x < 30)
assert mt(isl[R][xe]) == 0x125, hex(isl[R][xe])    # oostoever (water met zandrand)
DOCK = list(range(xe, xe + 5))
for i, x in enumerate(DOCK):
    isl[R][x] = 0x228 if i == 0 else 0x229
    isl[R + 1][x] = (0x230 if i == 0 else 0x231) | COL
DOCK_END = (DOCK[-1], R)
# de Frigate: S.S. Tidal-sprite (96x40), linkerrand half over de laatste steigertegel
SHIP = (DOCK_END[0] + 3, R + 1)
for y in range(R - 1, R + 3):
    for x in range(DOCK_END[0] + 1, DOCK_END[0] + 7):
        assert mt(isl[y][x]) == WATER, (x, y)
        isl[y][x] = WATER | COL
# losse zeerotsen (2x2), vaste seed, niet op de vaarroute naar de steiger
rnd = random.Random(451)
ROCK = ((0x150, 0x151), (0x158, 0x159))
SMALL = ((0x175, 0x176), (0x17d, 0x17e))
placed = 0
while placed < 14:
    x, y = rnd.randint(1, W - 4), rnd.randint(1, H - 3)
    if R - 4 <= y <= R + 5 and x >= DOCK[0] - 1:
        continue                    # vaarroute en schip vrij
    if x >= W - 6:
        continue                    # rand bij Route 105 open houden
    if any(mt(isl[yy][xx]) != WATER for yy in range(y - 1, y + 3) for xx in range(x - 1, x + 3)
           if 0 <= yy < H and 0 <= xx < W):
        continue
    pat = rnd.choice((ROCK, SMALL))
    for dy in range(2):
        for dx in range(2):
            isl[y + dy][x + dx] = pat[dy][dx] | COL
    placed += 1

# objecten op het eiland (posities)
LOOKOUT = (IX + 5, IY + 1)          # noordpunt (uitkijkpost)
GUARD = (IX + 4, IY + 18)           # zuidkant
NIGEL = (xe - 1, R)                 # voor de steiger
NIGEL_ASIDE = (xe - 1, R - 1)        # of (xe - 1, R + 1) als de speler boven hem staat
ISL_WARP = (DOCK_END[0] - 1, R)     # aankomst vanaf het schip
for (x, y) in (LOOKOUT, GUARD, NIGEL, NIGEL_ASIDE, (xe - 1, R + 1), ISL_WARP):
    assert not solid(isl[y][x]), ('object op een blokkade', x, y, hex(isl[y][x]))

# ====================================================================== Frigate
corr = load('SSTidalCorridor')
cab = load('SSTidalRooms')
hold = load('SSTidalLowerDeck')
FLOOR_H = 0x20d
for y in range(5, 9):               # middelste kratten (en hun schaduw op x 14) weg: ruimte voor het vrieslab
    for x in range(1, 15):
        hold[y][x] = FLOOR_H
MAPS = {'NothingIsland': isl, 'PlasmaFrigate_Corridor': corr, 'PlasmaFrigate_Cabins': cab,
        'PlasmaFrigate_Hold': hold}
C = {'NothingIsland': 'MAP_NOTHING_ISLAND', 'PlasmaFrigate_Corridor': 'MAP_PLASMA_FRIGATE_CORRIDOR',
     'PlasmaFrigate_Cabins': 'MAP_PLASMA_FRIGATE_CABINS', 'PlasmaFrigate_Hold': 'MAP_PLASMA_FRIGATE_HOLD'}


def warp(x, y, dest, wid, elev=0):
    return {"x": x, "y": y, "elevation": elev, "dest_map": C[dest], "dest_warp_id": str(wid)}


WARPS = {
    'NothingIsland': [warp(*ISL_WARP, 'PlasmaFrigate_Corridor', 8)],
    'PlasmaFrigate_Corridor': [warp(4, 9, 'PlasmaFrigate_Cabins', 0), warp(7, 9, 'PlasmaFrigate_Cabins', 2),
                               warp(10, 9, 'PlasmaFrigate_Cabins', 4), warp(13, 9, 'PlasmaFrigate_Cabins', 6),
                               warp(4, 3, 'PlasmaFrigate_Cabins', 8), warp(7, 3, 'PlasmaFrigate_Cabins', 9),
                               warp(10, 3, 'PlasmaFrigate_Cabins', 10), warp(13, 3, 'PlasmaFrigate_Cabins', 11),
                               warp(1, 11, 'NothingIsland', 0), warp(16, 2, 'PlasmaFrigate_Hold', 0)],
    'PlasmaFrigate_Cabins': [warp(4, 16, 'PlasmaFrigate_Corridor', 0), warp(5, 16, 'PlasmaFrigate_Corridor', 0),
                             warp(13, 16, 'PlasmaFrigate_Corridor', 1), warp(14, 16, 'PlasmaFrigate_Corridor', 1),
                             warp(22, 16, 'PlasmaFrigate_Corridor', 2), warp(23, 16, 'PlasmaFrigate_Corridor', 2),
                             warp(31, 16, 'PlasmaFrigate_Corridor', 3), warp(32, 16, 'PlasmaFrigate_Corridor', 3),
                             warp(4, 1, 'PlasmaFrigate_Corridor', 4), warp(13, 1, 'PlasmaFrigate_Corridor', 5),
                             warp(22, 1, 'PlasmaFrigate_Corridor', 6), warp(31, 1, 'PlasmaFrigate_Corridor', 7)],
    'PlasmaFrigate_Hold': [warp(15, 2, 'PlasmaFrigate_Corridor', 9)],
}


def obj(gfx, x, y, move, script, flag='0', ttype='TRAINER_TYPE_NONE', sight=0, item=None, lid=None, elev=3):
    o = {"graphics_id": gfx, "x": x, "y": y, "elevation": elev, "movement_type": move, "movement_range_x": 0,
         "movement_range_y": 0, "trainer_type": ttype,
         "trainer_sight_or_berry_tree_id": item if item else str(sight), "script": script, "flag": flag}
    if lid:
        o = dict([('local_id', lid)] + list(o.items()))
    return o


GM, GF = 'OBJ_EVENT_GFX_NEO_PLASMA_GRUNT_M', 'OBJ_EVENT_GFX_NEO_PLASMA_GRUNT_F'
CREW = 'FLAG_HIDE_PLASMA_ISLAND_CREW'
P = 'PlasmaFrigate_'
OBJS = {
    'NothingIsland': [
        obj('OBJ_EVENT_GFX_PLASMA_FRIGATE', *SHIP, 'MOVEMENT_TYPE_FACE_RIGHT', '0x0', lid='LOCALID_PLASMA_FRIGATE', elev=1),
        obj(GM, *LOOKOUT, 'MOVEMENT_TYPE_FACE_UP', 'NothingIsland_EventScript_Lookout', CREW, 'TRAINER_TYPE_NORMAL', 3),
        obj(GF, *GUARD, 'MOVEMENT_TYPE_LOOK_AROUND', 'NothingIsland_EventScript_Guard', CREW, 'TRAINER_TYPE_NORMAL', 4),
        obj(GM, *NIGEL, 'MOVEMENT_TYPE_FACE_DOWN_AND_UP', 'NothingIsland_EventScript_Nigel', CREW, 'TRAINER_TYPE_NORMAL', 3,
            lid='LOCALID_PLASMA_NIGEL'),
    ],
    'PlasmaFrigate_Corridor': [
        obj(GM, 7, 10, 'MOVEMENT_TYPE_FACE_DOWN', P + 'Corridor_EventScript_GuardRed', lid='LOCALID_PLASMA_GUARD_RED'),
        obj(GF, 10, 10, 'MOVEMENT_TYPE_FACE_DOWN', P + 'Corridor_EventScript_GuardBlue', lid='LOCALID_PLASMA_GUARD_BLUE'),
        obj(GM, 13, 10, 'MOVEMENT_TYPE_FACE_DOWN', P + 'Corridor_EventScript_GuardWhite', lid='LOCALID_PLASMA_GUARD_WHITE'),
        obj('OBJ_EVENT_GFX_SHADOW_TRIAD', 15, 2, 'MOVEMENT_TYPE_FACE_DOWN', P + 'Corridor_EventScript_Triad',
            'FLAG_HIDE_PLASMA_TRIAD', lid='LOCALID_PLASMA_TRIAD'),
    ],
    'PlasmaFrigate_Cabins': [
        obj(GM, 3, 5, 'MOVEMENT_TYPE_FACE_DOWN', P + 'Cabins_EventScript_Sleeper'),
        obj('OBJ_EVENT_GFX_ITEM_BALL', 15, 4, 'MOVEMENT_TYPE_LOOK_AROUND', 'Common_EventScript_FindItem',
            'FLAG_ITEM_PLASMA_FRIGATE_PP_MAX', item='ITEM_PP_MAX'),
        obj(GF, 23, 4, 'MOVEMENT_TYPE_FACE_LEFT', P + 'Cabins_EventScript_Gossip'),
        obj('OBJ_EVENT_GFX_ITEM_BALL', 29, 6, 'MOVEMENT_TYPE_LOOK_AROUND', 'Common_EventScript_FindItem',
            'FLAG_ITEM_PLASMA_FRIGATE_MAX_REVIVE', item='ITEM_MAX_REVIVE'),
    ],
    'PlasmaFrigate_Hold': [
        obj('OBJ_EVENT_GFX_SPECIES(GENESECT)', 7, 5, 'MOVEMENT_TYPE_FACE_DOWN', P + 'Hold_EventScript_Genesect',
            'FLAG_HIDE_NEW_MAUVILLE_GENESECT', lid='LOCALID_PLASMA_GENESECT'),
        obj('OBJ_EVENT_GFX_ZINZOLIN', 6, 7, 'MOVEMENT_TYPE_FACE_DOWN', P + 'Hold_EventScript_Bosses',
            'FLAG_HIDE_PLASMA_BOSSES', lid='LOCALID_PLASMA_ZINZOLIN'),
        obj('OBJ_EVENT_GFX_ROOD', 8, 7, 'MOVEMENT_TYPE_FACE_DOWN', P + 'Hold_EventScript_Bosses',
            'FLAG_HIDE_PLASMA_BOSSES', lid='LOCALID_PLASMA_ROOD'),
    ],
}


def sign(x, y, script):
    return {"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
            "script": script}


def signs(cells, script):
    return [sign(x, y, script) for (x, y) in cells]


BGS = {
    'NothingIsland': [],
    'PlasmaFrigate_Corridor': [],
    'PlasmaFrigate_Cabins': (signs([(2, 11), (2, 12)], P + 'Cabins_EventScript_TerminalRed')
                             + signs([(11, 12), (12, 12), (11, 13), (12, 13)], P + 'Cabins_EventScript_TerminalBlue')
                             + signs([(19, 11), (20, 11), (19, 12), (20, 12)], P + 'Cabins_EventScript_TerminalWhite')
                             + signs([(x, y) for x in range(31, 35) for y in (12, 13)], P + 'Cabins_EventScript_TerminalYellow')),
    'PlasmaFrigate_Hold': signs([(10, 3), (11, 3), (12, 3)], P + 'Hold_EventScript_Console'),
}
COORDS = {
    'NothingIsland': [{"type": "trigger", "x": DOCK_END[0], "y": R, "elevation": 0, "var": "VAR_TEMP_1",
                       "var_value": "0", "script": "NothingIsland_EventScript_Gangway"}],
}
for name, objs in OBJS.items():
    for o in objs:
        assert 'FRIGATE' in o['graphics_id'] or not solid(MAPS[name][o['y']][o['x']]), ('object op blokkade', name, o)
for b in BGS['PlasmaFrigate_Cabins'] + BGS['PlasmaFrigate_Hold']:
    g = MAPS['PlasmaFrigate_Cabins' if 'Cabins' in b['script'] else 'PlasmaFrigate_Hold']
    assert solid(g[b['y']][b['x']]), ('terminal niet op meubel', b)

# ---------------------------------------------------------------- bereikbaarheid
# wie na zijn gevecht opzij stapt (of verdwijnt): telt niet als blokkade; de 'opzij'-plek moet vrij zijn
MOVES = {'LOCALID_PLASMA_NIGEL': ('NothingIsland', NIGEL_ASIDE), 'LOCALID_PLASMA_GUARD_RED': ('PlasmaFrigate_Corridor', (8, 10)),
         'LOCALID_PLASMA_GUARD_BLUE': ('PlasmaFrigate_Corridor', (11, 10)),
         'LOCALID_PLASMA_GUARD_WHITE': ('PlasmaFrigate_Corridor', (14, 10)),
         'LOCALID_PLASMA_TRIAD': None, 'LOCALID_PLASMA_ZINZOLIN': None, 'LOCALID_PLASMA_ROOD': None,
         'LOCALID_PLASMA_GENESECT': None}
for lid, v in MOVES.items():
    if v:
        assert not solid(MAPS[v[0]][v[1][1]][v[1][0]]), ('opzij-plek bezet', lid)
SURF_OK = {WATER, 0x123, 0x125, 0x11b, 0x11d, 0x12b, 0x12c, 0x12d}


def passable(name, x, y, surf):
    g = MAPS[name]
    if not (0 <= y < len(g) and 0 <= x < len(g[0])):
        return False
    v = g[y][x]
    if solid(v):
        return False
    if any(o['x'] == x and o['y'] == y and o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL'
           and o.get('local_id') not in MOVES for o in OBJS[name]):
        return False
    return True


# eiland: vanaf de oostrand (Route 105) surfend; land en water lopen allebei (surfen op/af kan overal aan de rand)
seen = set()
todo = [('NothingIsland', W - 1, y) for y in range(H) if passable('NothingIsland', W - 1, y, True)]
seen.update(todo)
MAPID = {v: k for k, v in C.items()}
while todo:
    name, x, y = todo.pop()
    nxt = []
    for w in WARPS[name]:
        door = solid(MAPS[name][w['y']][w['x']]) and abs(w['x'] - x) + abs(w['y'] - y) == 1   # deur: ertegenaan lopen
        if (w['x'], w['y']) == (x, y) or door:
            seen.add((name, w['x'], w['y']))
            d = WARPS[MAPID[w['dest_map']]][int(w['dest_warp_id'])]
            nxt.append((MAPID[w['dest_map']], d['x'], d['y']))
    for c in COORDS.get(name, []):
        if (c['x'], c['y']) == (x, y):           # steiger -> schip
            d = WARPS['PlasmaFrigate_Corridor'][8]
            nxt.append(('PlasmaFrigate_Corridor', d['x'], d['y']))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if passable(name, x + dx, y + dy, True):
            nxt.append((name, x + dx, y + dy))
    for n in nxt:
        if n not in seen:
            seen.add(n)
            todo.append(n)
for name, objs in OBJS.items():
    for o in objs:
        if 'FRIGATE' in o['graphics_id']:
            continue
        assert any((name, o['x'] + dx, o['y'] + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), \
            ('onbereikbaar', name, o['script'], o['x'], o['y'])
for name, ws in WARPS.items():
    for w in ws:
        assert (name, w['x'], w['y']) in seen, ('warp onbereikbaar', name, w)
for name, bs in BGS.items():
    for scr in {b['script'] for b in bs}:
        assert any((name, b['x'] + dx, b['y'] + dy) in seen for b in bs if b['script'] == scr
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), ('terminal onbereikbaar', name, scr)
print('bereikbaar:', len(seen), 'vakken; steiger', DOCK, 'rij', R, 'schip', SHIP)

# ---------------------------------------------------------------- schrijven
TILESETS = {'NothingIsland': ('gTileset_General', 'gTileset_Dewford')}
MUSIC = {'NothingIsland': 'MUS_ABANDONED_SHIP'}
lj = open('data/layouts/layouts.json').read()
grp = open('data/maps/map_groups.json').read()
es = open('data/event_scripts.s').read()
prev = 'RocketHideout_B2F'
for name, grid in MAPS.items():
    h, w = len(grid), len(grid[0])
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', v) for r in grid for v in r))
    border = [WATER | COL] * 4 if name == 'NothingIsland' else [0x201 | COL] * 4
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *border))
    lid = 'LAYOUT_' + C[name][4:]
    pts, sts = TILESETS.get(name, ('gTileset_General', 'gTileset_InsideShip'))
    if '"%s"' % lid not in lj:
        i = lj.rindex('    }\n  ]')
        j = i + len('    }')
        lj = lj[:j] + ''',
    {
      "id": "%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "%s",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (lid, name, w, h, pts, sts, name, name) + lj[j:]
    island = name == 'NothingIsland'
    mj = {
        "id": C[name], "name": name, "layout": lid, "music": MUSIC.get(name, 'MUS_AQUA_MAGMA_HIDEOUT'),
        "region_map_section": "MAPSEC_NOTHING_ISLAND", "requires_flash": False,
        "weather": "WEATHER_FOG_HORIZONTAL" if island else "WEATHER_NONE",
        "map_type": "MAP_TYPE_OCEAN_ROUTE" if island else "MAP_TYPE_INDOOR", "allow_cycling": island,
        "allow_escaping": False, "allow_running": True, "show_map_name": island,
        "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
        "connections": [{"map": "MAP_ROUTE105", "offset": 0, "direction": "right"}] if island else None,
        "object_events": OBJS[name], "warp_events": WARPS[name], "coord_events": COORDS.get(name, []),
        "bg_events": BGS[name],
    }
    os.makedirs('data/maps/' + name, exist_ok=True)
    with open('data/maps/%s/map.json' % name, 'w') as fp:
        json.dump(mj, fp, indent=2, ensure_ascii=False)
        fp.write('\n')
    if '"%s"' % name not in grp:
        i = grp.index('"gMapGroup_Grounded": [')
        j = grp.index('\n  ]', i)
        grp = grp[:j] + ',\n    "%s"' % name + grp[j:]
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/%s/scripts.inc"\n' % prev
        assert anchor in es
        es = es.replace(anchor, anchor + inc, 1)
    prev = name
open('data/layouts/layouts.json', 'w').write(lj)
open('data/maps/map_groups.json', 'w').write(grp)
open('data/event_scripts.s', 'w').write(es)

# Route 105: verbinding naar het westen (tekstueel, de rest van het bestand blijft zoals het is)
p = 'data/maps/Route105/map.json'
r = open(p).read()
if 'MAP_NOTHING_ISLAND' not in r:
    anchor = '"connections": ['
    assert anchor in r
    r = r.replace(anchor, anchor + '\n    {\n      "map": "MAP_NOTHING_ISLAND",\n      "offset": 0,\n'
                  '      "direction": "left"\n    },', 1)
    open(p, 'w').write(r)
    json.loads(r)
print({n: (len(m[0]), len(m)) for n, m in MAPS.items()})

if len(sys.argv) > 1:
    for name, grid in MAPS.items():
        subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', name,
                        os.path.join(sys.argv[1], name + '.png'), '0', str(len(grid))], check=True)
print('klaar')
