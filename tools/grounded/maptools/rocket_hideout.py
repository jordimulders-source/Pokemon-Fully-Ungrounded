"""Project Grounded: de Rocket-hideout onder Fortree Jungle (Safari-sidequest).

Drie kaarten, gebouwd uit stukken van de Aqua Hideout (Facility-metatiles) met een eigen Rocket-kleur:
- RocketHideout_1F (opslag, 15x17): AquaHideout_B2F x 0-14, y 0-14 + onderwand. Trap omhoog = holle reuzenpalm in
  Fortree Jungle; twee teleportvlakken verbinden de opslag, de gang en de computerkamer; trap omlaag naar B1F.
- RocketHideout_B1F (labo/kazerne, 51x24): kopie van AquaHideout_B1F met een nieuw teleportdoolhof (alle vlakken
  opnieuw gekoppeld, een extra vlak in de kamer met de trap naar B2F). Oplossing: aankomstkamer -> rechtervlak ->
  rasterkamer (45,5) -> rij 13 -> (48,13) -> grote zaal (2 grunts) -> rond het bad naar (3,15) -> trapkamer.
- RocketHideout_B2F (kantoor van executive Petrel, 20x15): AquaHideout_B2F x 14-33, y 0-12 + onderwand, met een
  nooduitgang (teleportvlak) terug naar de jungle.
Tilesets rocket_general / rocket_facility hebben alleen eigen paletten (BASE-bestand: tiles en metatiles van
General / Facility): blauwgrijs wordt koud antraciet, het groen/turkoois van de vloeren donker bordeauxrood. Water blijft
blauw. Registreert layouts, kaarten, map_groups (gMapGroup_Grounded), event_scripts.s en de tilesets.
De scripts.inc staan met de hand in data/maps/RocketHideout_*.
Gebruik: python3 tools/grounded/maptools/rocket_hideout.py [rendermap]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import colorsys, json, os, struct, subprocess, sys

# ---------------------------------------------------------------- paletten


def rocketize(c, primary):
    r, g, b = c
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    deg = h * 360
    if s > 0.35 and (deg < 40 or deg > 330):           # al rood/oranje: laten (Rocket-rood, waarschuwingslampjes)
        return c
    if primary:
        if 190 <= deg <= 225 and s > 0.6 and l < 0.75:  # water en lucht in General blijven blauw
            return c
        nl = l * 0.86
        return tuple(int(v * 255) for v in colorsys.hls_to_rgb(0.0, nl, min(s, 0.05)))
    if 190 <= deg <= 230 and s > 0.4:                  # water blijft blauw
        return c
    if 130 <= deg < 190 and s > 0.15:                  # turkoois (zeshoektegels in labo's) -> bordeaux
        return tuple(int(v * 255) for v in colorsys.hls_to_rgb(0.985, l * 0.70, min(0.50, s + 0.10)))
    return tuple(int(v * 255) for v in colorsys.hls_to_rgb(0.0, l * 0.80, min(s, 0.06)))  # rest -> koud antraciet


def convert(src, dst, base, primary):
    os.makedirs(dst + '/palettes', exist_ok=True)
    open(dst + '/BASE', 'w').write(base + '\n')
    for i in range(16):
        lines = open(f'{src}/palettes/{i:02}.pal').read().split('\n')
        cols = [tuple(map(int, l.split())) for l in lines[3:19]]
        if not (primary and i == 4):                   # General-palet 4 = water: blijft blauw
            cols = [cols[0]] + [rocketize(c, primary) for c in cols[1:]]
        with open(f'{dst}/palettes/{i:02}.pal', 'w', newline='\r\n') as fp:
            fp.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % tuple((v >> 3) << 3 for v in c) for c in cols))


convert('data/tilesets/primary/general', 'data/tilesets/primary/rocket_general', 'general', True)
convert('data/tilesets/secondary/facility', 'data/tilesets/secondary/rocket_facility', 'facility', False)

hdr = open('src/data/tilesets/headers.h').read()
if 'gTileset_RocketGeneral' not in hdr:
    hdr += '''
// Project Grounded: Rocket-hideout onder Fortree Jungle. Tiles/metatiles van General en Facility, eigen (Rocket-)paletten
// (tools/grounded/maptools/rocket_hideout.py)
const struct Tileset gTileset_RocketGeneral =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_General,
    .palettes = gTilesetPalettes_RocketGeneral,
    .metatiles = gMetatiles_General,
    .metatileAttributes = gMetatileAttributes_General,
    .callback = InitTilesetAnim_General,
};

const struct Tileset gTileset_RocketFacility =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Facility,
    .palettes = gTilesetPalettes_RocketFacility,
    .metatiles = gMetatiles_Facility,
    .metatileAttributes = gMetatileAttributes_Facility,
    .callback = NULL,
};
'''
    open('src/data/tilesets/headers.h', 'w').write(hdr)
gfx = open('src/data/tilesets/graphics.h').read()
if 'gTilesetPalettes_RocketGeneral' not in gfx:
    for name, d in (('RocketGeneral', 'primary/rocket_general'), ('RocketFacility', 'secondary/rocket_facility')):
        gfx += '\nconst u16 gTilesetPalettes_%s[][16] = // Project Grounded: Rocket-hideout\n{\n' % name
        gfx += ''.join('    INCBIN_U16("data/tilesets/%s/palettes/%02d.gbapal"),\n' % (d, i) for i in range(16)) + '};\n'
    open('src/data/tilesets/graphics.h', 'w').write(gfx)

# ---------------------------------------------------------------- kaarten


def load(name, w):
    v = struct.unpack('<%dH' % (len(open('data/layouts/%s/map.bin' % name, 'rb').read()) // 2),
                      open('data/layouts/%s/map.bin' % name, 'rb').read())
    return [list(v[y * w:(y + 1) * w]) for y in range(len(v) // w)]


B1 = load('AquaHideout_B1F', 51)
B2 = load('AquaHideout_B2F', 34)
WALL_V = B2[11][0]            # 0x20a verticale wand
PAD = B2[8][5]                # 0x2df teleportvlak
CAP_END, FACE_END = B1[22][0], B1[23][0]       # 0x210 / 0x220: wandkolom die onderaan de kaart eindigt
CAP, FACE = B1[22][1], B1[23][1]               # 0x2e0 / 0x221: onderwand
FLOOR_BOTTOM, FLOOR_BOTTOM_L = B2[9][2], B2[9][1]   # 0x259 / 0x20b: vloer vlak boven een wand


def mt(v):
    return v & 0x3FF


def cut(src, x0, y0, x1, y1):
    return [row[x0:x1 + 1] for row in src[y0:y1 + 1]]


def close_bottom(g):
    """Laatste rij wordt 'vloer boven wand', daaronder een onderwand (kap + wandvlak) zoals onderaan Aqua B2F."""
    last = g[-1]
    walls = [mt(v) in (0x20a, 0x209, 0x210, 0x211, 0x213, 0x220) for v in last]
    for x, v in enumerate(last):
        if not walls[x]:
            last[x] = FLOOR_BOTTOM_L if (x > 0 and walls[x - 1]) else FLOOR_BOTTOM
        else:
            last[x] = WALL_V
    g.append([CAP_END if w else CAP for w in walls])
    g.append([FACE_END if w else FACE for w in walls])
    return g


# 1F: opslag
F1 = cut(B2, 0, 0, 14, 14)
for y in (12, 13, 14):
    F1[y][14] = WALL_V
F1[13][2] = PAD
F1 = close_bottom(F1)
# B1F: kopie, extra teleportvlak in de trapkamer
FB1 = [row[:] for row in B1]
FB1[10][11] = PAD
# B2F: kantoor
F2 = cut(B2, 14, 0, 33, 12)
F2[12][19] = F2[9][0] = F2[10][0] = WALL_V
for x in range(1, 19):
    if mt(F2[12][x]) in (0x21f, 0x227, 0x22f):
        F2[12][x] = B2[12][16]    # krat onderaan weg: gewone vloer
F2 = close_bottom(F2)

MAPS = {
    'RocketHideout_1F': F1,
    'RocketHideout_B1F': FB1,
    'RocketHideout_B2F': F2,
}


def warp(x, y, dest, wid):
    return {"x": x, "y": y, "elevation": 3, "dest_map": dest, "dest_warp_id": str(wid)}


def pads(pairs, first):
    """Koppel teleportvlakken paarsgewijs: [(a, b), ...] -> warps vanaf index first."""
    out, idx = [], {}
    flat = [p for pr in pairs for p in pr]
    for i, p in enumerate(flat):
        idx[p] = first + i
    for a, b in pairs:
        out.append((a, idx[b]))
        out.append((b, idx[a]))
    return sorted(out, key=lambda t: idx[t[0]])


H1, HB1, HB2 = 'MAP_ROCKET_HIDEOUT_1F', 'MAP_ROCKET_HIDEOUT_B1F', 'MAP_ROCKET_HIDEOUT_B2F'
W1F = [warp(3, 3, 'MAP_FORTREE_JUNGLE', 0), warp(12, 1, HB1, 0)]
W1F += [warp(x, y, H1, d) for (x, y), d in pads([((5, 8), (12, 13)), ((2, 13), (8, 8))], 2)]
WB1F = [warp(29, 1, H1, 1), warp(18, 1, H1, 1), warp(12, 1, H1, 1), warp(3, 3, HB2, 0)]
B1_PAIRS = [((31, 4), (45, 3)), ((27, 4), (23, 10)), ((42, 5), (27, 12)), ((45, 5), (42, 13)), ((48, 5), (45, 9)),
            ((42, 9), (48, 17)), ((48, 9), (20, 4)), ((45, 13), (42, 17)), ((48, 13), (32, 19)), ((45, 17), (3, 20)),
            ((3, 15), (11, 10))]
WB1F += [warp(x, y, HB1, d) for (x, y), d in pads(B1_PAIRS, 4)]
WB2F = [warp(4, 1, HB1, 3), warp(17, 8, 'MAP_FORTREE_JUNGLE', 0)]
for name, ws in (('RocketHideout_1F', W1F), ('RocketHideout_B1F', WB1F), ('RocketHideout_B2F', WB2F)):
    g = MAPS[name]
    for w in ws:
        assert mt(g[w['y']][w['x']]) in (0x2df, 0x2bc, 0x2cc), (name, w, hex(g[w['y']][w['x']]))
    pad_cells = {(x, y) for y in range(len(g)) for x in range(len(g[0])) if mt(g[y][x]) == 0x2df}
    assert pad_cells <= {(w['x'], w['y']) for w in ws}, (name, 'teleportvlak zonder warp', pad_cells)


def obj(gfx, x, y, move, script, flag='0', ttype='TRAINER_TYPE_NONE', sight=0, item=None):
    return {"graphics_id": gfx, "x": x, "y": y, "elevation": 3, "movement_type": move, "movement_range_x": 0,
            "movement_range_y": 0, "trainer_type": ttype,
            "trainer_sight_or_berry_tree_id": item if item else str(sight), "script": script, "flag": flag}


def grunt(gfx, x, y, face, sight, script):
    return obj(gfx, x, y, 'MOVEMENT_TYPE_FACE_' + face, script, 'FLAG_HIDE_ROCKET_HIDEOUT_GRUNTS',
               'TRAINER_TYPE_NORMAL', sight)


def item(x, y, it, flag):
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'MOVEMENT_TYPE_LOOK_AROUND', 'Common_EventScript_FindItem', flag,
               item=it)


M_, F_ = 'OBJ_EVENT_GFX_ROCKET_GRUNT_M', 'OBJ_EVENT_GFX_ROCKET_GRUNT_F'
OBJS = {
    'RocketHideout_1F': [
        grunt(M_, 7, 14, 'UP', 2, 'RocketHideout_1F_EventScript_Smuggler'),
        grunt(F_, 9, 3, 'DOWN', 6, 'RocketHideout_1F_EventScript_Recruiter'),
        item(2, 5, 'ITEM_FULL_HEAL', 'FLAG_ITEM_ROCKET_HIDEOUT_FULL_HEAL'),
    ],
    'RocketHideout_B1F': [
        grunt(M_, 28, 20, 'RIGHT', 3, 'RocketHideout_B1F_EventScript_Scientist'),
        grunt(F_, 7, 14, 'DOWN', 1, 'RocketHideout_B1F_EventScript_Thief'),
        item(16, 10, 'ITEM_MAX_POTION', 'FLAG_ITEM_ROCKET_HIDEOUT_MAX_POTION'),
        item(28, 11, 'ITEM_PP_UP', 'FLAG_ITEM_ROCKET_HIDEOUT_PP_UP'),
        item(17, 3, 'ITEM_NUGGET', 'FLAG_ITEM_ROCKET_HIDEOUT_NUGGET'),
    ],
    'RocketHideout_B2F': [
        obj('OBJ_EVENT_GFX_PETREL', 10, 5, 'MOVEMENT_TYPE_FACE_DOWN', 'RocketHideout_B2F_EventScript_Petrel',
            'FLAG_HIDE_ROCKET_EXEC', 'TRAINER_TYPE_NORMAL', 4),
        obj(M_, 12, 5, 'MOVEMENT_TYPE_FACE_LEFT', 'RocketHideout_B2F_EventScript_Runner', 'FLAG_HIDE_ROCKET_EXEC'),
    ],
}
for name, objs in OBJS.items():
    g = MAPS[name]
    for o in objs:
        v = g[o['y']][o['x']]
        assert (v >> 10) & 3 == 0, (name, o['script'], o['x'], o['y'], hex(v))
    for o in objs:
        o['local_id'] = None
for o in OBJS['RocketHideout_B2F']:
    o['local_id'] = 'LOCALID_ROCKET_PETREL' if o['graphics_id'] == 'OBJ_EVENT_GFX_PETREL' else 'LOCALID_ROCKET_RUNNER'

# bereikbaarheid (lopend + teleport): elke trainer/item/warp bereikbaar vanaf de ingang, en B2F vanaf 1F
WARPS = {'RocketHideout_1F': W1F, 'RocketHideout_B1F': WB1F, 'RocketHideout_B2F': WB2F}
MAPID = {H1: 'RocketHideout_1F', HB1: 'RocketHideout_B1F', HB2: 'RocketHideout_B2F'}


def walkable(name, x, y):
    g = MAPS[name]
    if not (0 <= y < len(g) and 0 <= x < len(g[0])):
        return False
    v = g[y][x]
    return (v >> 10) & 3 == 0 and not any(o['x'] == x and o['y'] == y and o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL'
                                          and 'Runner' not in o['script'] for o in OBJS[name])


seen, todo = {('RocketHideout_1F', 3, 3)}, [('RocketHideout_1F', 3, 3)]
while todo:
    name, x, y = todo.pop()
    nxt = []
    for w in WARPS[name]:
        if (w['x'], w['y']) == (x, y) and w['dest_map'] in MAPID:
            d = WARPS[MAPID[w['dest_map']]][int(w['dest_warp_id'])]
            nxt.append((MAPID[w['dest_map']], d['x'], d['y']))
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if walkable(name, x + dx, y + dy):
            nxt.append((name, x + dx, y + dy))
    for n in nxt:
        if n not in seen:
            seen.add(n)
            todo.append(n)
for name, objs in OBJS.items():
    for o in objs:
        assert any((name, o['x'] + dx, o['y'] + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), \
            ('onbereikbaar', name, o['script'], o['x'], o['y'])
for name, ws in WARPS.items():
    for w in ws:
        assert (name, w['x'], w['y']) in seen or w['dest_map'] == 'MAP_FORTREE_JUNGLE' and name == 'RocketHideout_B2F', \
            ('warp onbereikbaar', name, w)
print('bereikbaar:', len(seen), 'vakken')

# ---------------------------------------------------------------- schrijven
lj = open('data/layouts/layouts.json').read()
g = open('data/maps/map_groups.json').read()
es = open('data/event_scripts.s').read()
for name, grid in MAPS.items():
    h, w = len(grid), len(grid[0])
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', v) for r in grid for v in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *([0x601 | 0x400] * 4)))
    lid = 'LAYOUT_' + name.upper().replace('ROCKETHIDEOUT', 'ROCKET_HIDEOUT')
    mid = 'MAP_' + name.upper().replace('ROCKETHIDEOUT', 'ROCKET_HIDEOUT')
    if '"%s"' % lid not in lj:
        i = lj.rindex('    }\n  ]')
        j = i + len('    }')
        lj = lj[:j] + ''',
    {
      "id": "%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_RocketGeneral",
      "secondary_tileset": "gTileset_RocketFacility",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (lid, name, w, h, name, name) + lj[j:]
    mj = {
        "id": mid, "name": name, "layout": lid, "music": "MUS_RG_ROCKET_HIDEOUT",
        "region_map_section": "MAPSEC_FORTREE_JUNGLE", "requires_flash": False, "weather": "WEATHER_NONE",
        "map_type": "MAP_TYPE_INDOOR", "allow_cycling": False, "allow_escaping": True, "allow_running": True,
        "show_map_name": False, "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": None,
        "object_events": [{k: v for k, v in o.items() if not (k == 'local_id' and v is None)} for o in OBJS[name]],
        "warp_events": WARPS[name], "coord_events": [], "bg_events": [],
    }
    for o in mj['object_events']:
        if 'local_id' in o:
            lid_ = o.pop('local_id')
            mj['object_events'][mj['object_events'].index(o)] = dict([('local_id', lid_)] + list(o.items()))
    os.makedirs('data/maps/' + name, exist_ok=True)
    with open('data/maps/%s/map.json' % name, 'w') as fp:
        json.dump(mj, fp, indent=2, ensure_ascii=False)
        fp.write('\n')
    if '"%s"' % name not in g:
        i = g.index('"gMapGroup_Grounded": [')
        j = g.index('\n  ]', i)
        g = g[:j] + ',\n    "%s"' % name + g[j:]
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/FortreeJungle/scripts.inc"\n'
        assert anchor in es
        es = es.replace(anchor, anchor + inc, 1)
open('data/layouts/layouts.json', 'w').write(lj)
open('data/maps/map_groups.json', 'w').write(g)
open('data/event_scripts.s', 'w').write(es)
print({n: (len(m[0]), len(m)) for n, m in MAPS.items()})

if len(sys.argv) > 1:
    for name, grid in MAPS.items():
        subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', name,
                        os.path.join(sys.argv[1], name + '.png'), '0', str(len(grid))], check=True)
print('klaar')
