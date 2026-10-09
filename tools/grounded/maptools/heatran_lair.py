"""Project Grounded: Heatran-grot onder Fiery Path (post-game).
Layout = Magma Hideout 4F zonder de machines van Team Magma (metatiles 0x35C-0x3A1 vervangen door de
dichtstbijzijnde horizontale buur), Heatran aan de onderrand van de lavapoel (16,20).
Ingang: na de Hall of Fame een grotopening in de bovenwand van Fiery Path linksboven (8,0-1).
Idempotent. Gebruik: python3 tools/grounded/maptools/heatran_lair.py"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, shutil, struct

NAME, CONST = 'FieryPath_HeatranLair', 'FIERY_PATH_HEATRAN_LAIR'
W, H = 59, 28
os.makedirs('data/layouts/' + NAME, exist_ok=True)
shutil.copy('data/layouts/MagmaHideout_4F/border.bin', 'data/layouts/%s/border.bin' % NAME)
b = open('data/layouts/MagmaHideout_4F/map.bin', 'rb').read()
v = [[struct.unpack_from('<H', b, (y * W + x) * 2)[0] for x in range(W)] for y in range(H)]
machine = lambda val: 0x35C <= (val & 0x3FF) <= 0x3A1
out = [row[:] for row in v]
for y in range(H):
    for x in range(W):
        if machine(v[y][x]):
            for d in range(1, W):
                cand = [xx for xx in (x - d, x + d) if 0 <= xx < W and not machine(v[y][xx])]
                if cand:
                    out[y][x] = v[y][cand[0]]
                    break
open('data/layouts/%s/map.bin' % NAME, 'wb').write(b''.join(struct.pack('<H', out[y][x]) for y in range(H) for x in range(W)))

lj = open('data/layouts/layouts.json').read()
if '"LAYOUT_%s"' % CONST not in lj:
    i = lj.index('"id": "LAYOUT_MAGMA_HIDEOUT_4F"'); j = lj.index('},', i) + 2
    lj = lj[:j] + '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_Lavaridge",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (CONST, NAME, W, H, NAME, NAME) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)

# Fiery Path: aankomstpunt voor de grotopening
fp = json.load(open('data/maps/FieryPath/map.json'))
if not any(w['dest_map'] == 'MAP_' + CONST for w in fp['warp_events']):
    fp['warp_events'].append({'x': 8, 'y': 1, 'elevation': 0, 'dest_map': 'MAP_' + CONST, 'dest_warp_id': '0'})
    open('data/maps/FieryPath/map.json', 'w').write(json.dumps(fp, indent=2, ensure_ascii=False) + '\n')
fpw = [i for i, w in enumerate(fp['warp_events']) if w['dest_map'] == 'MAP_' + CONST][0]

base = json.load(open('data/maps/MagmaHideout_4F/map.json'))
m = {k: base[k] for k in base}
m.update({'id': 'MAP_' + CONST, 'name': NAME, 'layout': 'LAYOUT_' + CONST, 'region_map_section': 'MAPSEC_FIERY_PATH',
          'music': 'MUS_PETALBURG_WOODS', 'show_map_name': False})
m['object_events'] = [{'local_id': 'LOCALID_HEATRAN_LAIR_HEATRAN', 'graphics_id': 'OBJ_EVENT_GFX_SPECIES(HEATRAN)',
                       'x': 16, 'y': 20, 'elevation': 3, 'movement_type': 'MOVEMENT_TYPE_FACE_DOWN',
                       'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE',
                       'trainer_sight_or_berry_tree_id': '0', 'script': NAME + '_EventScript_Heatran',
                       'flag': 'FLAG_HIDE_FIERY_PATH_HEATRAN'}]
m['warp_events'] = [{'x': 46, 'y': 7, 'elevation': 0, 'dest_map': 'MAP_FIERY_PATH', 'dest_warp_id': str(fpw)},
                    {'x': 20, 'y': 21, 'elevation': 0, 'dest_map': 'MAP_FIERY_PATH', 'dest_warp_id': str(fpw)}]
m['coord_events'] = []
m['bg_events'] = []
os.makedirs('data/maps/' + NAME, exist_ok=True)
open('data/maps/%s/map.json' % NAME, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

g = open('data/maps/map_groups.json').read()
if '"%s"' % NAME not in g:
    g = g.replace('    "RegigigasTemple"', '    "RegigigasTemple",\n    "%s"' % NAME, 1)
    open('data/maps/map_groups.json', 'w').write(g)
es = open('data/event_scripts.s').read()
inc = '\t.include "data/maps/%s/scripts.inc"\n' % NAME
if inc not in es:
    es = es.replace('\t.include "data/maps/RegigigasTemple/scripts.inc"\n', '\t.include "data/maps/RegigigasTemple/scripts.inc"\n' + inc, 1)
    open('data/event_scripts.s', 'w').write(es)
print('klaar, Fiery Path-warp', fpw)
