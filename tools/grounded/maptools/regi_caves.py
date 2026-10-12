"""Project Grounded: Regi-grotten met de stippenpuzzel.
- Zet de stippen (metatile 0x3A8) + coord-triggers in de voorkamers van Desert Ruins, Island Cave en Ancient Tomb.
- Maakt RegielekiCave (luik in de pijler van de Cycling Road, Route 110) en RegidragoCave (eilandje op Route 130)
  als kopie van de Ancient Tomb.
Idempotent: kan opnieuw draaien. Stippen staan in src/regi_dots.c (zelfde lijst als hier).
Gebruik: python3 tools/grounded/maptools/regi_caves.py"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, re, shutil, struct

DOTS = {
    'DesertRuins': [(6, 22), (6, 24), (6, 26), (8, 24), (10, 22), (10, 24), (10, 26)],
    'IslandCave': [(7, 22), (9, 22), (10, 24), (9, 26), (7, 26), (6, 24), (8, 24)],
    'AncientTomb': [(6, 22), (7, 23), (8, 24), (9, 25), (10, 26), (10, 22), (9, 23), (7, 25), (6, 26)],
    'RegielekiCave': [(5, 22), (6, 24), (5, 25), (8, 24), (11, 25), (10, 24), (11, 22)],
    'RegidragoCave': [(6, 22), (10, 22), (8, 23), (7, 24), (9, 24), (8, 25), (8, 27)],
}
DOT_OFF = 0x3A8
W = 17


def load_json(p):
    return json.load(open(p))


def save_json(p, d):
    open(p, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')


def set_block(path, width, x, y, metatile, keep_collision=True):
    b = bytearray(open(path, 'rb').read())
    v = struct.unpack_from('<H', b, (y * width + x) * 2)[0]
    nv = (v & 0xFC00 if keep_collision else v & 0xF000) | metatile
    struct.pack_into('<H', b, (y * width + x) * 2, nv)
    open(path, 'wb').write(bytes(b))


def get_block(path, width, x, y):
    return struct.unpack_from('<H', open(path, 'rb').read(), (y * width + x) * 2)[0]


def add_dots(name):
    m = load_json('data/maps/%s/map.json' % name)
    lay = 'data/layouts/%s/map.bin' % name
    coord = [c for c in (m.get('coord_events') or []) if c.get('script') != 'Common_EventScript_RegiDotStep']
    for x, y in DOTS[name]:
        set_block(lay, W, x, y, DOT_OFF)
        coord.append({'type': 'trigger', 'x': x, 'y': y, 'elevation': get_block(lay, W, x, y) >> 12,
                      'var': 'VAR_TEMP_0', 'var_value': '0', 'script': 'Common_EventScript_RegiDotStep'})
    m['coord_events'] = coord
    save_json('data/maps/%s/map.json' % name, m)


def make_cave(name, const, mon, route_map, route_warp, mapsec):
    os.makedirs('data/layouts/%s' % name, exist_ok=True)
    for f in ('map.bin', 'border.bin'):
        shutil.copy('data/layouts/AncientTomb/%s' % f, 'data/layouts/%s/%s' % (name, f))
    # de vanilla Ancient Tomb-layout heeft de stippen van Registeel al als die eerder draaide: opnieuw vanaf schoon
    for x, y in DOTS['AncientTomb']:
        set_block('data/layouts/%s/map.bin' % name, W, x, y, 0x201)
    m = load_json('data/maps/AncientTomb/map.json')
    up = mon.upper()
    m.update({'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + const, 'region_map_section': mapsec})
    m['object_events'] = [{
        'local_id': 'LOCALID_%s_%s' % (const, up), 'graphics_id': 'OBJ_EVENT_GFX_SPECIES(%s)' % up,
        'x': 8, 'y': 7, 'elevation': 3, 'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 0,
        'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': '0',
        'script': '%s_EventScript_%s' % (name, mon), 'flag': 'FLAG_HIDE_' + up}]
    m['warp_events'][0].update({'dest_map': route_map, 'dest_warp_id': str(route_warp)})
    m['warp_events'][1]['dest_map'] = 'MAP_' + const
    m['warp_events'][2]['dest_map'] = 'MAP_' + const
    for b in m['bg_events']:
        b['script'] = 'Common_EventScript_RegiDotsMural'
    m['coord_events'] = []
    os.makedirs('data/maps/%s' % name, exist_ok=True)
    save_json('data/maps/%s/map.json' % name, m)
    open('data/maps/%s/scripts.inc' % name, 'w').write(f'''{name}_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, {name}_OnResume
	map_script MAP_SCRIPT_ON_LOAD, {name}_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, {name}_OnTransition
	.byte 0

@ Project Grounded: {mon} (stippenpuzzel, zie src/regi_dots.c en tools/grounded/maptools/regi_caves.py)
{name}_OnResume:
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, {name}_EventScript_TryRemove{mon}
	end

{name}_EventScript_TryRemove{mon}::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject VAR_LAST_TALKED
	return

{name}_OnTransition:
	setflag FLAG_HIDE_{up}
	call_if_unset FLAG_DEFEATED_{up}, {name}_EventScript_Show{mon}
	end

{name}_EventScript_Show{mon}::
	clearflag FLAG_HIDE_{up}
	return

{name}_OnLoad:
	special RegiDots_OnLoad
	call_if_unset FLAG_SYS_{up}_PUZZLE_COMPLETED, {name}_EventScript_HideRegiEntrance
	end

{name}_EventScript_HideRegiEntrance::
	setmetatile 7, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 8, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 9, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 7, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 8, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 9, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	return

{name}_EventScript_{mon}::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_{up}, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setwildbattle SPECIES_{up}, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special StartRegiBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Common_EventScript_RegiCrumbled
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {name}_EventScript_RanFrom{mon}
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {name}_EventScript_RanFrom{mon}
	setflag FLAG_DEFEATED_{up}
	call Common_EventScript_CheckRegigigasTemple
	release
	end

{name}_EventScript_RanFrom{mon}::
	setvar VAR_0x8004, SPECIES_{up}
	goto Common_EventScript_LegendaryFlewAway
	end
''')
    add_dots(name)
    # map_groups.json: achter AncientTomb's groep (tekstueel)
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"AncientTomb"')
        j = g.index(']', i)
        k = g.rindex('"', 0, j) + 1
        g = g[:k] + ',\n    "%s"' % name + g[k:]
        open('data/maps/map_groups.json', 'w').write(g)
    lj = open('data/layouts/layouts.json').read()
    if '"LAYOUT_%s"' % const not in lj:
        i = lj.index('"id": "LAYOUT_ANCIENT_TOMB"')
        j = lj.index('},', i) + 2
        lj = lj[:j] + '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": 17,
      "height": 33,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_Cave",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (const, name, name, name) + lj[j:]
        open('data/layouts/layouts.json', 'w').write(lj)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        es = es.replace('\t.include "data/maps/AncientTomb/scripts.inc"\n', '\t.include "data/maps/AncientTomb/scripts.inc"\n' + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def add_route_warp(route, x, y, elevation, dest, dest_warp=0):
    p = 'data/maps/%s/map.json' % route
    m = load_json(p)
    warps = m.get('warp_events') or []
    for i, w in enumerate(warps):
        if w['dest_map'] == dest:
            return i
    warps.append({'x': x, 'y': y, 'elevation': elevation, 'dest_map': dest, 'dest_warp_id': str(dest_warp)})
    m['warp_events'] = warps
    save_json(p, m)
    return len(warps) - 1


for n in ('DesertRuins', 'IslandCave', 'AncientTomb'):
    add_dots(n)

# Regieleki: luik in de pijler van de Cycling Road (Route 110, pijler op 15,72; je staat er onder de brug voor)
w110 = add_route_warp('Route110', 15, 71, 3, 'MAP_REGIELEKI_CAVE')
m = load_json('data/maps/Route110/map.json')
if not any(b.get('script') == 'Route110_EventScript_PillarHatch' for b in m['bg_events']):
    m['bg_events'].append({'type': 'sign', 'x': 15, 'y': 72, 'elevation': 3,
                           'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
                           'script': 'Route110_EventScript_PillarHatch'})
    save_json('data/maps/Route110/map.json', m)
make_cave('RegielekiCave', 'REGIELEKI_CAVE', 'Regieleki', 'MAP_ROUTE110', w110, 'MAPSEC_ROUTE_110')

# Regidrago: het eilandje van de Island Cave (Route 105) op Route 130, deur op (18,25)
R105 = 'data/layouts/Route105/map.bin'
R130 = 'data/layouts/Route130/map.bin'
b130 = bytearray(open(R130, 'rb').read())
for dy in range(7):
    for dx in range(7):
        v = get_block(R105, 40, 6 + dx, 17 + dy)
        mt = v & 0x3FF
        if mt == 0x341: v = (v & 0xFC00) | 0x073   # Dewford-tegels -> General
        if mt == 0x342: v = (v & 0xFC00) | 0x075
        struct.pack_into('<H', b130, ((22 + dy) * 80 + 15 + dx) * 2, v)
# de rotsjes in de hoeken onderaan zijn de helft van een tweedelige rots: water ervan maken
water = struct.unpack_from('<H', b130, (28 * 80 + 14) * 2)[0]
for x in (15, 21):
    struct.pack_into('<H', b130, (28 * 80 + x) * 2, water)
open(R130, 'wb').write(bytes(b130))
w130 = add_route_warp('Route130', 18, 25, 0, 'MAP_REGIDRAGO_CAVE')
make_cave('RegidragoCave', 'REGIDRAGO_CAVE', 'Regidrago', 'MAP_ROUTE130', w130, 'MAPSEC_ROUTE_130')
print('klaar')
