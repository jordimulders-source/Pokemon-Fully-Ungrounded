"""Project Grounded: kaarten voor de post-game legendary-events Genesect en Mewtwo.
- NewMauville_ServerVault (was Genesect lv 70; sinds v0.9.110 leeg, met de vrachtbrief naar Nothing Island): serverkluis achter de Raikou-grot onder New Mauville. Stijl en bouwstenen
  zoals NewMauville_ThunderCave (beasts_maps.py): rotswanden uit NewMauville_Entrance, tanks en computers uit
  AquaHideout_B2F. Ingang: kluisdeur in de bovenwand van de Raikou-grot (x 6-8), verschijnt na de herstart via de
  terminal (FLAG_NEW_MAUVILLE_VAULT_OPEN, scripts in NewMauville_ThunderCave/scripts.inc).
- MeteorFalls_UnknownCave_1F / _B1F (Mewtwo lv 70): Cerulean Cave-hommage. 1F = kopie van Altering Cave met een
  ladder naar beneden op het verhoogde plateau (27,10); B1F = kopie van de ongebruikte Ruby/Sapphire-kaart
  CaveOfOrigin_UnusedRubySapphireMap3 (een spiraal die nooit in een game te zien was), Mewtwo op de plek van het gat.
  Ingang: na de Hall of Fame een grotopening in Meteor Falls 1F (12,25-26).
Idempotent. Controleert de bereikbaarheid van warps, items en de legendaries.
Gebruik: python3 tools/grounded/maptools/legend_maps.py"""
import json, os, shutil, struct, random
from collections import deque

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)
LAYOUTS = {l['name']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}


def load(n):
    l = LAYOUTS[n + '_Layout']; W = l['width']
    v = list(struct.unpack('<%dH' % (W * l['height']), open(l['blockdata_filepath'], 'rb').read()))
    return [v[y * W:(y + 1) * W] for y in range(l['height'])]


def save_layout(name, g, border_from):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', t) for r in g for t in r))
    shutil.copy('data/layouts/%s/border.bin' % border_from, 'data/layouts/%s/border.bin' % name)


def add_layout(name, const, w, h, secondary, after='MeteorSpace_Layout'):
    lj = open('data/layouts/layouts.json').read()
    if '"LAYOUT_%s"' % const in lj:
        return
    i = lj.index('"name": "%s"' % after); j = lj.index('},', i) + 2
    lj = lj[:j] + '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (const, name, w, h, secondary, name, name) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)


def add_to_groups(name, after):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        g = g.replace('    "%s"\n' % after, '    "%s",\n    "%s"\n' % (after, name), 1)
        assert '"%s"' % name in g, name
        open('data/maps/map_groups.json', 'w').write(g)


def add_include(name, after):
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        a = '\t.include "data/maps/%s/scripts.inc"\n' % after
        es = es.replace(a, a + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def write_json(path, d):
    open(path, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')


def obj(lid, gfx, x, y, script, flag, move='MOVEMENT_TYPE_FACE_DOWN', sight='0'):
    return {'local_id': lid, 'graphics_id': gfx, 'x': x, 'y': y, 'elevation': 3, 'movement_type': move,
            'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE',
            'trainer_sight_or_berry_tree_id': sight, 'script': script, 'flag': flag}


def sign(x, y, script):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_NORTH',
            'script': script}


def map_json(const, name, layout_const, music, mapsec, objs, warps, signs, weather='WEATHER_NONE'):
    return {'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + layout_const, 'music': music,
            'region_map_section': mapsec, 'requires_flash': False, 'weather': weather,
            'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': True,
            'allow_running': True, 'show_map_name': False, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL',
            'connections': None, 'object_events': objs, 'warp_events': warps, 'coord_events': [], 'bg_events': signs}


def reachable(g, start, blocked=()):
    """Botsing + hoogte (0/15 = overal) zoals in de engine; objecten in 'blocked' tellen als muur."""
    H, W = len(g), len(g[0])
    seen = {start}; q = deque([start])
    while q:
        x, y = q.popleft(); e0 = g[y][x] >> 12
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in seen or (nx, ny) in blocked:
                continue
            v = g[ny][nx]; e = v >> 12
            if (v >> 10) & 3 or not (e == e0 or e in (0, 15) or e0 in (0, 15)):
                continue
            seen.add((nx, ny)); q.append((nx, ny))
    return seen


def next_to(r, x, y):
    return any((x + dx, y + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


# ====================================================================== Genesect: serverkluis
VAULT, VAULT_C = 'NewMauville_ServerVault', 'NEW_MAUVILLE_SERVER_VAULT'
ent = load('NewMauville_Entrance'); aqua = load('AquaHideout_B2F')
W, H = 15, 14
FLOOR = 0x3d0 | (3 << 12)
g = [[FLOOR] * W for _ in range(H)]
for y in range(H):
    g[y][0] = ent[3][0]; g[y][1] = ent[3][1]; g[y][W - 2] = ent[3][7]; g[y][W - 1] = ent[3][8]
for x in range(1, W - 1):
    g[0][x] = ent[0][1]; g[1][x] = ent[1][2]
    if 2 <= x < W - 2:
        g[H - 2][x] = ent[7][2]
    g[H - 1][x] = ent[8][1]
g[0][0] = ent[0][0]; g[0][W - 1] = ent[0][8]; g[1][0] = ent[1][0]; g[1][1] = ent[1][1]; g[1][W - 2] = ent[1][7]
g[1][W - 1] = ent[1][8]; g[H - 2][1] = ent[7][1]; g[H - 2][W - 2] = ent[7][7]; g[H - 1][0] = ent[8][0]
g[H - 1][W - 1] = ent[8][8]
for dy in range(2):                       # deur bovenin (x 6-8), dezelfde als die van de Raikou-grot
    for dx in range(3):
        g[dy][6 + dx] = ent[dy][3 + dx]
rnd = random.Random(649)
for _ in range(6):
    x, y = rnd.randint(2, W - 3), rnd.randint(7, H - 4)
    g[y][x] = rnd.choice((ent[2][3], ent[2][5], ent[6][4]))


def paste(sx, sy, w, h, dx, dy):
    for yy in range(h):
        for xx in range(w):
            t = aqua[sy + yy][sx + xx]
            if (t & 0x3ff) in (0x228, 0x2a1, 0x2a9, 0x22a, 0x230, 0x238, 0x232, 0x23a):
                continue
            g[dy + yy][dx + xx] = t


paste(20, 0, 4, 7, 2, 0); paste(26, 0, 4, 7, 9, 0)          # twee tanks naast de deur
for (dx, dy) in ((2, 8), (10, 8)):                            # serverkasten (scherm, kast, kast, schaduw)
    paste(17, 6, 3, 4, dx, dy)
save_layout(VAULT, g, 'NewMauville_Entrance')
add_layout(VAULT, VAULT_C, W, H, 'gTileset_Facility')
# sinds v0.9.110 is Genesect weg (Neo Plasma, Plasma Frigate bij Nothing Island): lege capsules + printer met de vrachtbrief
r = reachable(g, (7, 2), set())
for sx, sy in ((2, 10), (3, 10), (10, 10), (11, 10), (3, 6), (4, 6), (10, 6), (11, 6)):
    assert (sx, sy + 1) in r, ('server/capsule', sx, sy)

# Raikou-grot: warp naar de kluis (alleen bereikbaar als de deur er is)
tc = json.load(open('data/maps/NewMauville_ThunderCave/map.json'))
if not any(w['dest_map'] == 'MAP_' + VAULT_C for w in tc['warp_events']):
    tc['warp_events'].append({'x': 7, 'y': 1, 'elevation': 0, 'dest_map': 'MAP_' + VAULT_C, 'dest_warp_id': '0'})
    write_json('data/maps/NewMauville_ThunderCave/map.json', tc)
tcw = [i for i, w in enumerate(tc['warp_events']) if w['dest_map'] == 'MAP_' + VAULT_C][0]

os.makedirs('data/maps/' + VAULT, exist_ok=True)
write_json('data/maps/%s/map.json' % VAULT, map_json(
    VAULT_C, VAULT, VAULT_C, 'MUS_RG_SILPH', 'MAPSEC_NEW_MAUVILLE',
    [],
    [{'x': 7, 'y': 1, 'elevation': 0, 'dest_map': 'MAP_NEW_MAUVILLE_THUNDER_CAVE', 'dest_warp_id': str(tcw)}],
    [sign(2, 10, VAULT + '_EventScript_Server1'), sign(3, 10, VAULT + '_EventScript_Server1'),
     sign(10, 10, VAULT + '_EventScript_Printer'), sign(11, 10, VAULT + '_EventScript_Printer')]
    + [sign(x, 6, VAULT + '_EventScript_Capsule') for x in (3, 4, 10, 11)]))
add_to_groups(VAULT, 'MeteorSpace')
add_include(VAULT, 'MeteorSpace')

# ====================================================================== Mewtwo: verborgen grot achter Meteor Falls
# (Mewtwo staat sinds v0.9.171 in de echte Cerulean Cave achter de Spacetime Cave: draai na dit script ook
#  tools/grounded/maptools/spacetime_cave.py, dat Mewtwo hier weghaalt en een kras in de rots zet.)
C1, C1_C = 'MeteorFalls_UnknownCave_1F', 'METEOR_FALLS_UNKNOWN_CAVE_1F'
C2, C2_C = 'MeteorFalls_UnknownCave_B1F', 'METEOR_FALLS_UNKNOWN_CAVE_B1F'
g1 = load('AlteringCave')
HOLE = (27, 10)
g1[HOLE[1]][HOLE[0]] = (g1[HOLE[1]][HOLE[0]] & 0xF000) | 0x33d   # ladder naar beneden (gat), hoogte van het plateau
g2 = load('CaveOfOrigin_UnusedRubySapphireMap3')
assert g2[6][12] & 0x3ff == 0x33d
g2[6][12] = g2[6][11]                     # gat naar beneden dicht: hier staat Mewtwo
save_layout(C1, g1, 'AlteringCave')
save_layout(C2, g2, 'CaveOfOrigin_UnusedRubySapphireMap3')
add_layout(C1, C1_C, len(g1[0]), len(g1), 'gTileset_Cave', VAULT + '_Layout')
add_layout(C2, C2_C, len(g2[0]), len(g2), 'gTileset_Cave', C1 + '_Layout')

MEWTWO = (12, 6)
ITEM1, ITEM2 = (6, 2), (7, 12)
r1 = reachable(g1, (18, 21), {ITEM1})
assert HOLE in r1 and next_to(r1, *ITEM1), 'grot 1F'
r2 = reachable(g2, (7, 14), {MEWTWO, ITEM2})
assert next_to(r2, *MEWTWO) and next_to(r2, *ITEM2), 'grot B1F'

# Meteor Falls 1F: aankomstpunt voor de grotopening (12,26)
mf = json.load(open('data/maps/MeteorFalls_1F_1R/map.json'))
if not any(w['dest_map'] == 'MAP_' + C1_C for w in mf['warp_events']):
    mf['warp_events'].append({'x': 12, 'y': 26, 'elevation': 3, 'dest_map': 'MAP_' + C1_C, 'dest_warp_id': '0'})
    write_json('data/maps/MeteorFalls_1F_1R/map.json', mf)
mfw = [i for i, w in enumerate(mf['warp_events']) if w['dest_map'] == 'MAP_' + C1_C][0]
mfg = load('MeteorFalls_1F_1R')
assert (12, 27) in reachable(mfg, (27, 19)), 'grotopening in Meteor Falls onbereikbaar'

for n in (C1, C2):
    os.makedirs('data/maps/' + n, exist_ok=True)
write_json('data/maps/%s/map.json' % C1, map_json(
    C1_C, C1, C1_C, 'MUS_RG_SEVII_DUNGEON', 'MAPSEC_METEOR_FALLS',
    [obj('LOCALID_UNKNOWN_CAVE_1F_ITEM', 'OBJ_EVENT_GFX_ITEM_BALL', ITEM1[0], ITEM1[1], 'Common_EventScript_FindItem',
         'FLAG_ITEM_UNKNOWN_CAVE_1F_MAX_REVIVE', 'MOVEMENT_TYPE_LOOK_AROUND', 'ITEM_MAX_REVIVE')],
    [{'x': 18, 'y': 22, 'elevation': 0, 'dest_map': 'MAP_METEOR_FALLS_1F_1R', 'dest_warp_id': str(mfw)},
     {'x': HOLE[0], 'y': HOLE[1], 'elevation': g1[HOLE[1]][HOLE[0]] >> 12, 'dest_map': 'MAP_' + C2_C, 'dest_warp_id': '0'}], []))
write_json('data/maps/%s/map.json' % C2, map_json(
    C2_C, C2, C2_C, 'MUS_RG_SEVII_DUNGEON', 'MAPSEC_METEOR_FALLS',
    [obj('LOCALID_UNKNOWN_CAVE_MEWTWO', 'OBJ_EVENT_GFX_SPECIES(MEWTWO)', MEWTWO[0], MEWTWO[1],
         C2 + '_EventScript_Mewtwo', 'FLAG_HIDE_METEOR_FALLS_MEWTWO', 'MOVEMENT_TYPE_FACE_DOWN'),
     obj('LOCALID_UNKNOWN_CAVE_B1F_ITEM', 'OBJ_EVENT_GFX_ITEM_BALL', ITEM2[0], ITEM2[1], 'Common_EventScript_FindItem',
         'FLAG_ITEM_UNKNOWN_CAVE_B1F_MAX_ELIXIR', 'MOVEMENT_TYPE_LOOK_AROUND', 'ITEM_MAX_ELIXIR')],
    [{'x': 7, 'y': 14, 'elevation': 3, 'dest_map': 'MAP_' + C1_C, 'dest_warp_id': '1'}], []))
add_to_groups(C1, VAULT)
add_to_groups(C2, C1)
add_include(C1, VAULT)
add_include(C2, C1)
print('klaar; Raikou-grot warp', tcw, '- Meteor Falls warp', mfw)
