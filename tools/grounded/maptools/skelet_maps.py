"""Fully Ungrounded: bouwt de skeletkaarten in gMapGroup_FullyUngrounded (stap 1 van PLAN_HOENN_ERUIT.md).

- StartTown: kopie van Oldale Town (pc, mart, twee huizen), noord- en zuiduitgang dicht met bomen; west sluit aan op
  de TestMap.
- StartTown_PokemonCenter_1F/2F en StartTown_Mart: de Oldale-kaarten, alleen hernoemd.
- Stock_*: per bewaarde huislayout één kaart (zie skelet_keep.py).
- TestMap: Route 102 (gras, vijver, bessenbomen) met onderaan een pleintje met vier huizen naar de stock-kaarten,
  Keccles als trainer en een PC.

De bronnen komen uit git (commit BASE), dus het script werkt ook nadat de Hoenn-kaarten weg zijn. Idempotent:
draait het opnieuw, dan worden de kaarten overschreven en de registraties niet dubbel gezet.
Gebruik: python3 tools/grounded/maptools/skelet_maps.py
"""
import json, os, re, struct, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skelet_keep import GROUP, MAPS, STOCK_HOUSES  # noqa: E402

BASE = 'a64c32e28d'  # laatste commit met de volledige Hoenn-wereld


def git(path, binary=False):
    out = subprocess.run(['git', 'show', '%s:%s' % (BASE, path)], capture_output=True, check=True).stdout
    return out if binary else out.decode()


def grid(path, w, h):
    return list(struct.unpack('<%dH' % (w * h), git(path, True)))


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = 'wb' if isinstance(data, bytes) else 'w'
    with open(path, mode) as f:
        f.write(data)


def pack(v):
    return struct.pack('<%dH' % len(v), *v)


def obj(gfx, x, y, script, move='MOVEMENT_TYPE_FACE_DOWN', trainer='TRAINER_TYPE_NONE', sight='0', flag='0',
        local_id=None, elev=3):
    o = {}
    if local_id:
        o['local_id'] = local_id
    o.update({'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
              'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': trainer,
              'trainer_sight_or_berry_tree_id': sight, 'script': script, 'flag': flag})
    return o


def warp(x, y, dest, wid, elev=0):
    return {'x': x, 'y': y, 'elevation': elev, 'dest_map': dest, 'dest_warp_id': str(wid)}


def sign(x, y, script, facing='BG_EVENT_PLAYER_FACING_ANY'):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': facing, 'script': script}


def map_json(name, layout, music, mtype, objs, warps, bgs, conns=None, weather='WEATHER_NONE', show=False,
             cycling=False, running=False, escaping=False):
    mid = 'MAP_' + re.sub(r'(?<=[a-z])(?=[A-Z])', '_', name).upper().replace('__', '_')
    return {
        'id': mid, 'name': name, 'layout': layout, 'music': music, 'region_map_section': 'MAPSEC_START_TOWN',
        'requires_flash': False, 'weather': weather, 'map_type': mtype, 'allow_cycling': cycling,
        'allow_escaping': escaping, 'allow_running': running, 'show_map_name': show,
        'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': conns, 'object_events': objs,
        'warp_events': warps, 'coord_events': [], 'bg_events': bgs,
    }


def dump(d):
    return json.dumps(d, indent=2, ensure_ascii=False) + '\n'


def map_id(name):
    return map_json(name, '', '', '', [], [], [])['id']


# ---------------------------------------------------------------- metatiles (ruwe waarden incl. botsing/hoogte)
OLD = grid('data/layouts/OldaleTown/map.bin', 20, 20)
R102 = grid('data/layouts/Route102/map.bin', 50, 20)


def o(x, y):
    return OLD[y * 20 + x]


def r(x, y):
    return R102[y * 50 + x]


GRASS = o(4, 2)                       # 001
TREE_T = (r(0, 0), r(1, 0))           # 1d4 1d5: bovenkant boom
TREE_B = (r(0, 1), r(1, 1))           # 1dc 1dd: onderkant boom, open eronder
TREE_BB = (r(8, 1), r(9, 1))          # 1e4 1e5: onderkant boom met de kruin van de boom eronder
CROWN = (r(0, 9), r(1, 9))            # 1ce 1cf: open cel boven een boom
HOUSE = [[o(14 + dx, 13 + dy) for dx in range(4)] for dy in range(4)]   # Oldale-huis, deur op (1, 3)
PATH_BOTTOM = (o(3, 11), o(4, 11), o(4, 11), o(17, 11))  # 1e0 1e1 1e1 1e2


# ---------------------------------------------------------------- StartTown (20x20)
def build_start_town():
    v = OLD[:]
    W = 20

    def put(x, y, m):
        v[y * W + x] = m
    # noorduitgang dicht (x 8-11, rij 0-1)
    for x in range(8, 12):
        put(x, 0, TREE_T[x % 2])
        put(x, 1, TREE_B[x % 2])
    # zuiduitgang dicht: bomen op rij 18-19 (x 4-15), kruinen op rij 17, pad stopt netjes op rij 16
    for x in range(4, 16):
        put(x, 18, TREE_T[x % 2])
        put(x, 19, TREE_B[x % 2])
        put(x, 17, CROWN[x % 2])
    for i, x in enumerate(range(9, 13)):
        put(x, 16, PATH_BOTTOM[i])
    write('data/layouts/StartTown/map.bin', pack(v))
    write('data/layouts/StartTown/border.bin', git('data/layouts/OldaleTown/border.bin', True))

    warps = [
        warp(5, 7, 'MAP_STOCK_HOUSE1', 0),
        warp(15, 16, 'MAP_STOCK_HOUSE2', 0),
        warp(6, 16, 'MAP_START_TOWN_POKEMON_CENTER_1F', 0),
        warp(14, 6, 'MAP_START_TOWN_MART', 0),
    ]
    bgs = [
        sign(11, 9, 'StartTown_EventScript_TownSign'),
        sign(7, 16, 'Common_EventScript_ShowPokemonCenterSign', 'BG_EVENT_PLAYER_FACING_NORTH'),
        sign(15, 6, 'Common_EventScript_ShowPokemartSign', 'BG_EVENT_PLAYER_FACING_NORTH'),
        sign(8, 16, 'Common_EventScript_ShowPokemonCenterSign', 'BG_EVENT_PLAYER_FACING_NORTH'),
        sign(16, 6, 'Common_EventScript_ShowPokemartSign', 'BG_EVENT_PLAYER_FACING_NORTH'),
    ]
    objs = [
        obj('OBJ_EVENT_GFX_MART_EMPLOYEE', 13, 7, 'StartTown_EventScript_MartEmployee',
            move='MOVEMENT_TYPE_FACE_DOWN'),
    ]
    conns = [{'map': 'MAP_TEST_MAP', 'offset': 0, 'direction': 'left'}]
    d = map_json('StartTown', 'LAYOUT_START_TOWN', 'MUS_LITTLEROOT', 'MAP_TYPE_TOWN', objs, warps, bgs, conns,
                 weather='WEATHER_SUNNY', show=True, cycling=True, running=True, escaping=False)
    write('data/maps/StartTown/map.json', dump(d))
    write('data/maps/StartTown/scripts.inc', '''StartTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, StartTown_OnTransition
	.byte 0

StartTown_OnTransition:
	setflag FLAG_VISITED_LITTLEROOT_TOWN
	end

StartTown_EventScript_TownSign::
	msgbox StartTown_Text_TownSign, MSGBOX_SIGN
	end

StartTown_EventScript_MartEmployee::
	msgbox StartTown_Text_MartEmployee, MSGBOX_NPC
	end

StartTown_Text_TownSign:
	.string "START TOWN\\n"
	.string "A placeholder with a POKéMON CENTER.$"

StartTown_Text_MartEmployee:
	.string "The real town is still being drawn.\\p"
	.string "Until then, this one is load-bearing.\\n"
	.string "Please don't lean on the houses.$"
''')


# ---------------------------------------------------------------- Pokémon Center en Mart (Oldale, hernoemd)
def renamed(text):
    for a, b in [('OldaleTown_PokemonCenter', 'StartTown_PokemonCenter'), ('OldaleTown_Mart', 'StartTown_Mart'),
                 ('MAP_OLDALE_TOWN', 'MAP_START_TOWN'), ('MAPSEC_OLDALE_TOWN', 'MAPSEC_START_TOWN'),
                 ('LOCALID_OLDALE_', 'LOCALID_START_TOWN_'), ('HEAL_LOCATION_OLDALE_TOWN', 'HEAL_LOCATION_START_TOWN')]:
        text = text.replace(a, b)
    return text


def build_pc_mart():
    for src in ['OldaleTown_PokemonCenter_1F', 'OldaleTown_PokemonCenter_2F', 'OldaleTown_Mart']:
        dst = src.replace('OldaleTown', 'StartTown')
        d = json.loads(renamed(git('data/maps/%s/map.json' % src)))
        # warps naar kaarten buiten de groep (Union Room, Trade Center) vallen weg
        ids = {map_id(m) for m in MAPS}
        d['warp_events'] = [w for w in d['warp_events'] if w['dest_map'] in ids]
        write('data/maps/%s/map.json' % dst, dump(d))
        scripts = renamed(git('data/maps/%s/scripts.inc' % src))
        # stap 7: de Briney-administratie (Hoenn) is weg
        scripts = scripts.replace('\tcall Common_EventScript_UpdateBrineyLocation\n', '')
        write('data/maps/%s/scripts.inc' % dst, scripts)


# ---------------------------------------------------------------- stock-huizen
# (layout -> uitgangswarps (x, y, hoogte) in die layout, overgenomen uit de vanilla-kaarten)
EXITS = {
    'LAYOUT_HOUSE1': [(3, 8), (4, 8)],
    'LAYOUT_HOUSE2': [(3, 7), (4, 7)],
    'LAYOUT_HOUSE_WITH_BED': [(3, 7), (4, 7)],
    'LAYOUT_FORTREE_CITY_HOUSE1': [(3, 5), (4, 5)],
    'LAYOUT_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F': [(8, 8), (9, 8)],
    'LAYOUT_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB': [(6, 12), (7, 12)],
}
# kaart -> (buitenkaart, warp-id daar)
OUTSIDE = {
    'Stock_House1': ('MAP_START_TOWN', 0),
    'Stock_House2': ('MAP_START_TOWN', 1),
    'Stock_HouseWithBed': ('MAP_TEST_MAP', 0),
    'Stock_SmallHouse': ('MAP_TEST_MAP', 1),
    'Stock_TwoStory_1F': ('MAP_TEST_MAP', 2),
    'Stock_Lab': ('MAP_TEST_MAP', 3),
}


def build_stock():
    for name, (layout, _desc) in STOCK_HOUSES.items():
        if name == 'Stock_TwoStory_2F':
            warps = [warp(7, 1, 'MAP_STOCK_TWO_STORY_1F', 2)]
        else:
            dest, wid = OUTSIDE[name]
            warps = [warp(x, y, dest, wid) for x, y in EXITS[layout]]
            if name == 'Stock_TwoStory_1F':
                warps.append(warp(8, 2, 'MAP_STOCK_TWO_STORY_2F', 0))
        objs, bgs = [], []
        if name == 'Stock_TwoStory_1F':
            # stap 7: Mom (players_house.inc: standaardtekst, PokéNav-registratie, healen)
            objs = [obj('OBJ_EVENT_GFX_MOM', 2, 6, 'PlayersHouse_1F_EventScript_Mom', move='MOVEMENT_TYPE_FACE_RIGHT',
                        local_id='LOCALID_STOCK_TWO_STORY_1F_MOM')]
        if name == 'Stock_TwoStory_2F':
            # stap 7: PC op de slaapkamer en de wandklok (players_house.inc)
            bgs = [sign(0, 1, 'PlayersHouse_2F_EventScript_PC', 'BG_EVENT_PLAYER_FACING_NORTH'),
                   sign(5, 1, 'PlayersHouse_2F_EventScript_WallClock')]
        d = map_json(name, layout, 'MUS_LITTLEROOT', 'MAP_TYPE_INDOOR', objs, warps, bgs)
        write('data/maps/%s/map.json' % name, dump(d))
        write('data/maps/%s/scripts.inc' % name, '%s_MapScripts::\n\t.byte 0\n' % name)


# ---------------------------------------------------------------- TestMap (Route 102 + pleintje, 50x32)
TW, TH = 50, 32
PLAZA_X = range(16, 36)
PLAZA_Y = range(20, 30)
HOUSES_X = [17, 22, 27, 32]   # linkerkolom van elk huis; deur op x+1, rij 27
HOUSE_Y = 24


def build_test_map():
    v = [0] * (TW * TH)
    for y in range(20):
        for x in range(TW):
            v[y * TW + x] = r(x, y)

    def put(x, y, m):
        v[y * TW + x] = m
    # bossen onder de route: bomen op even x, paren van rijen
    for y in range(20, TH):
        for x in range(TW):
            if x in PLAZA_X and y in PLAZA_Y:
                put(x, y, CROWN[x % 2] if y == PLAZA_Y[-1] else GRASS)
                continue
            if y % 2 == 0:
                put(x, y, TREE_T[x % 2])
            else:
                below_tree = y + 1 < TH and not (x in PLAZA_X and (y + 1) in PLAZA_Y)
                put(x, y, (TREE_BB if below_tree else TREE_B)[x % 2])
    # rij 19: de opening (x 24-31) wordt gras; boomonderkanten boven nieuwe bomen krijgen de kruin eronder
    for x in range(TW):
        if 24 <= x < 32:
            put(x, 19, GRASS)
        elif x not in PLAZA_X:
            put(x, 19, TREE_BB[x % 2])
    # huizen
    for hx in HOUSES_X:
        for dy in range(4):
            for dx in range(4):
                put(hx + dx, HOUSE_Y + dy, HOUSE[dy][dx])
    write('data/layouts/TestMap/map.bin', pack(v))
    write('data/layouts/TestMap/border.bin', git('data/layouts/Route102/border.bin', True))

    door_y = HOUSE_Y + 3
    warps = [
        warp(HOUSES_X[0] + 1, door_y, 'MAP_STOCK_HOUSE_WITH_BED', 0),
        warp(HOUSES_X[1] + 1, door_y, 'MAP_STOCK_SMALL_HOUSE', 0),
        warp(HOUSES_X[2] + 1, door_y, 'MAP_STOCK_TWO_STORY_1F', 0),
        warp(HOUSES_X[3] + 1, door_y, 'MAP_STOCK_LAB', 0),
    ]
    objs = [
        obj('OBJ_EVENT_GFX_KECLEON', 33, 14, 'TestMap_EventScript_Keccles', move='MOVEMENT_TYPE_FACE_LEFT',
            local_id='LOCALID_TEST_MAP_KECCLES'),
        obj('OBJ_EVENT_GFX_BERRY_TREE', 24, 2, 'BerryTreeScript', move='MOVEMENT_TYPE_BERRY_TREE_GROWTH',
            sight='BERRY_TREE_ROUTE_102_ORAN'),
        obj('OBJ_EVENT_GFX_BERRY_TREE', 25, 2, 'BerryTreeScript', move='MOVEMENT_TYPE_BERRY_TREE_GROWTH',
            sight='BERRY_TREE_ROUTE_102_PECHA'),
    ]
    bgs = [
        sign(17, 2, 'TestMap_EventScript_PC'),
        sign(40, 9, 'TestMap_EventScript_Sign'),
    ]
    conns = [{'map': 'MAP_START_TOWN', 'offset': 0, 'direction': 'right'}]
    d = map_json('TestMap', 'LAYOUT_TEST_MAP', 'MUS_ROUTE101', 'MAP_TYPE_ROUTE', objs, warps, bgs, conns,
                 weather='WEATHER_SUNNY', show=True, cycling=True, running=True, escaping=False)
    write('data/maps/TestMap/map.json', dump(d))
    write('data/maps/TestMap/scripts.inc', '''TestMap_MapScripts::
	.byte 0

@ Keccles blijft te bevechten: na elk gevecht gaat zijn trainerflag weer uit.
TestMap_EventScript_Keccles::
	lock
	faceplayer
	msgbox TestMap_Text_KecclesIntro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, TestMap_EventScript_KecclesDeclined
	trainerbattle_no_intro TRAINER_KECCLES_1, TestMap_Text_KecclesDefeat
	cleartrainerflag TRAINER_KECCLES_1
	msgbox TestMap_Text_KecclesPostBattle, MSGBOX_DEFAULT
	release
	end

TestMap_EventScript_KecclesDeclined::
	msgbox TestMap_Text_KecclesDeclined, MSGBOX_DEFAULT
	release
	end

TestMap_EventScript_PC::
	goto EventScript_PC
	end

TestMap_EventScript_Sign::
	msgbox TestMap_Text_Sign, MSGBOX_SIGN
	end

TestMap_Text_KecclesIntro:
	.string "KECCLES: Ah. The test map.\\p"
	.string "Everything here gets tested.\\n"
	.string "Including me, apparently.\\p"
	.string "Battle? For science?$"

TestMap_Text_KecclesDeclined:
	.string "KECCLES: A control group. Sensible.$"

TestMap_Text_KecclesDefeat:
	.string "Results inconclusive.$"

TestMap_Text_KecclesPostBattle:
	.string "KECCLES: Same time tomorrow.\\n"
	.string "Or in five seconds. I'll be here.$"

TestMap_Text_Sign:
	.string "TEST MAP\\n"
	.string "Everything new gets tried here first.$"
''')


# ---------------------------------------------------------------- registraties
def register_layouts():
    p = 'data/layouts/layouts.json'
    t = open(p).read()
    add = ''
    for lid, name, w, h in [('LAYOUT_START_TOWN', 'StartTown', 20, 20), ('LAYOUT_TEST_MAP', 'TestMap', TW, TH)]:
        if '"%s"' % lid in t:
            t = re.sub(r'("id": "%s",\s*"name": "[^"]+",\s*"width": )\d+(,\s*"height": )\d+' % lid,
                       lambda m: m.group(1) + str(w) + m.group(2) + str(h), t)
            continue
        add += (',\n    {\n      "id": "%s",\n      "name": "%s_Layout",\n      "width": %d,\n      "height": %d,\n'
                '      "primary_tileset": "gTileset_General",\n      "secondary_tileset": "gTileset_Petalburg",\n'
                '      "border_filepath": "data/layouts/%s/border.bin",\n'
                '      "blockdata_filepath": "data/layouts/%s/map.bin"\n    }') % (lid, name, w, h, name, name)
    if add:
        i = t.rstrip().rfind(']')
        j = t.rstrip()[:i].rstrip().rfind('}') + 1
        t = t[:j] + add + t[j:]
    open(p, 'w').write(t)
    json.load(open(p))


def register_group():
    p = 'data/maps/map_groups.json'
    t = open(p).read()
    if '"%s"' % GROUP not in t:
        # achteraan group_order
        m = re.search(r'"group_order": \[(.*?)\n  \]', t, re.S)
        t = t[:m.end(1)] + ',\n    "%s"' % GROUP + t[m.end(1):]
        # als laatste sleutel
        i = t.rstrip().rfind('}')
        body = ',\n  "%s": [\n%s\n  ]\n' % (GROUP, ',\n'.join('    "%s"' % n for n in MAPS))
        t = t[:i].rstrip() + body + t[i:]
    else:
        t = re.sub(r'("%s": \[)(.*?)(\n  \])' % GROUP,
                   lambda m: m.group(1) + '\n' + ',\n'.join('    "%s"' % n for n in MAPS) + m.group(3), t, flags=re.S)
    open(p, 'w').write(t)
    d = json.load(open(p))
    assert d['group_order'][-1] == GROUP and list(d)[-1] == GROUP


def register_scripts():
    p = 'data/event_scripts.s'
    lines = open(p).read().split('\n')
    have = set(lines)
    last = max(i for i, l in enumerate(lines) if l.startswith('\t.include "data/maps/'))
    new = ['\t.include "data/maps/%s/scripts.inc"' % n for n in MAPS]
    new = [l for l in new if l not in have]
    lines[last + 1:last + 1] = new
    open(p, 'w').write('\n'.join(lines))


def register_heal():
    p = 'src/data/heal_locations.json'
    t = open(p).read()
    if 'HEAL_LOCATION_START_TOWN' in t:
        return
    entry = (',\n    {\n      "id": "HEAL_LOCATION_START_TOWN",\n      "map": "MAP_START_TOWN",\n      "x": 6,\n'
             '      "y": 17,\n      "respawn_map": "MAP_START_TOWN_POKEMON_CENTER_1F",\n'
             '      "respawn_npc": "LOCALID_START_TOWN_NURSE"\n    }')
    i = t.rstrip().rfind(']')
    j = t[:i].rstrip().rfind('}') + 1
    t = t[:j] + entry + t[j:]
    open(p, 'w').write(t)
    json.load(open(p))


def register_wild():
    """TestMap krijgt de tabellen van Route 102 (12 unieke landsoorten, water, vissen)."""
    p = 'src/data/wild_encounters.json'
    t = open(p).read()
    if '"MAP_TEST_MAP"' in t:
        return
    src = json.loads(git(p))
    e = next(x for x in src['wild_encounter_groups'][0]['encounters'] if x['map'] == 'MAP_ROUTE102')
    e = dict(e, map='MAP_TEST_MAP', base_label='gTestMap')
    land = [m['species'] for m in e['land_mons']['mons']]
    assert len(land) == 12 and len(set(land)) == 12, land
    block = json.dumps(e, indent=2).replace('\n', '\n        ')
    m = re.search(r'"encounters": \[\n', t)
    t = t[:m.end()] + '        ' + block + ',\n' + t[m.end():]
    open(p, 'w').write(t)
    json.load(open(p))


def main():
    build_start_town()
    build_pc_mart()
    build_stock()
    build_test_map()
    register_layouts()
    register_group()
    register_scripts()
    register_heal()
    register_wild()
    print('skeletkaarten gebouwd:', ', '.join(MAPS))


if __name__ == '__main__':
    main()
