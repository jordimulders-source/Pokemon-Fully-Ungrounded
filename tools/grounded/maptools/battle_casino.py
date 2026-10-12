#!/usr/bin/env python3
"""Project Grounded: Battle Casino op het Battle Frontier-eiland (oostkant).

- BattleFrontier_OutsideEast: een kopie van het lounge-huisje (Lounge1, x 3-5, y 41-44) op het plein
  tussen het water en het bloembed (x 12-14, y 35-38), deur op (13, 38).
- BattleFrontier_BattleCasino (gMapGroup_Grounded) op de vanilla layout van de Game Corner van Mauville.
- Scripts: data/maps/BattleFrontier_BattleCasino/scripts.inc (croupier + sfeer-NPC's), de logica zit in
  src/battle_casino.c. Idempotent: opnieuw draaien verandert niets.
"""
import json
import os
import re
import struct

LAY = 'data/layouts/BattleFrontier_OutsideEast/map.bin'
W = 72
SRC = (3, 41)       # linksboven van het lounge-huisje
DST = (12, 35)
HOUSE_W, HOUSE_H = 3, 4
DOOR = (13, 38)
MAP = 'BattleFrontier_BattleCasino'
MAPDIR = 'data/maps/' + MAP


def patch_outside():
    data = bytearray(open(LAY, 'rb').read())
    v = list(struct.unpack('<%dH' % (len(data) // 2), data))
    # grasvak onder en boven het huisje (de dak- en deurtegels hebben gras op de achtergrond);
    # x 11 is de muur, x 15 de rand van het bloembed
    for y in range(DST[1] - 1, DST[1] + HOUSE_H):
        for x in range(DST[0], DST[0] + HOUSE_W):
            v[y * W + x] = 0x001
    for dy in range(HOUSE_H):
        for dx in range(HOUSE_W):
            v[(DST[1] + dy) * W + DST[0] + dx] = v[(SRC[1] + dy) * W + SRC[0] + dx]
    open(LAY, 'wb').write(struct.pack('<%dH' % len(v), *v))

    p = 'data/maps/BattleFrontier_OutsideEast/map.json'
    s = open(p).read()
    d = json.loads(s)
    if any(w['dest_map'] == 'MAP_BATTLE_FRONTIER_BATTLE_CASINO' for w in d['warp_events']):
        return len([w for w in d['warp_events']]) - 1
    idx = len(d['warp_events'])
    # tekstueel achteraan warp_events (bestaande warp-id's blijven gelijk)
    m = re.search(r'("warp_events": \[\n)(.*?)(\n  \])', s, re.S)
    body = m.group(2)
    new = body + ',\n    {\n      "x": %d,\n      "y": %d,\n      "elevation": 0,\n      "dest_map": "MAP_BATTLE_FRONTIER_BATTLE_CASINO",\n      "dest_warp_id": "0"\n    }' % DOOR
    s = s[:m.start(2)] + new + s[m.end(2):]
    json.loads(s)
    open(p, 'w').write(s)
    return idx


def obj(gfx, x, y, mv, script, lid=None):
    o = {}
    if lid:
        o['local_id'] = lid
    o.update({'graphics_id': gfx, 'x': x, 'y': y, 'elevation': 3, 'movement_type': mv,
              'movement_range_x': 1, 'movement_range_y': 1, 'trainer_type': 'TRAINER_TYPE_NONE',
              'trainer_sight_or_berry_tree_id': '0', 'script': script, 'flag': '0'})
    return o


def sign(x, y, face, script):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': face, 'script': script}


def make_map(warp_idx):
    os.makedirs(MAPDIR, exist_ok=True)
    pre = 'BattleCasino_EventScript_'
    objs = [
        obj('OBJ_EVENT_GFX_BEAUTY', 12, 2, 'MOVEMENT_TYPE_FACE_DOWN', pre + 'Croupier', 'LOCALID_CASINO_CROUPIER'),
        obj('OBJ_EVENT_GFX_MAN_3', 1, 7, 'MOVEMENT_TYPE_FACE_RIGHT', pre + 'Broke'),
        obj('OBJ_EVENT_GFX_MANIAC', 9, 8, 'MOVEMENT_TYPE_FACE_LEFT', pre + 'Conspiracy'),
        obj('OBJ_EVENT_GFX_GENTLEMAN', 16, 5, 'MOVEMENT_TYPE_FACE_DOWN', pre + 'Underdog'),
        obj('OBJ_EVENT_GFX_OLD_MAN', 20, 8, 'MOVEMENT_TYPE_FACE_LEFT', pre + 'OldMan'),
        obj('OBJ_EVENT_GFX_COOK', 6, 8, 'MOVEMENT_TYPE_FACE_RIGHT', pre + 'Buffet'),
        obj('OBJ_EVENT_GFX_WOMAN_5', 4, 6, 'MOVEMENT_TYPE_FACE_LEFT', pre + 'Wurmple'),
        # bookies (Jordi, v0.9.214): de tipgever kijkt naar de huidige kaart (Casino_GetTip)
        obj('OBJ_EVENT_GFX_MAN_5', 17, 3, 'MOVEMENT_TYPE_FACE_LEFT', pre + 'BookieTip'),
        obj('OBJ_EVENT_GFX_EXPERT_M', 5, 4, 'MOVEMENT_TYPE_FACE_DOWN', pre + 'BookieOdds'),
        obj('OBJ_EVENT_GFX_HEX_MANIAC', 20, 4, 'MOVEMENT_TYPE_FACE_DOWN', pre + 'BookieSpirits'),
    ]
    signs = []
    for (x, y, face) in [(2, 6, 'EAST'), (2, 8, 'EAST'), (2, 9, 'EAST'), (3, 7, 'WEST'), (3, 8, 'WEST'), (3, 9, 'WEST'),
                         (7, 6, 'EAST'), (7, 7, 'EAST'), (7, 9, 'EAST'), (8, 6, 'WEST'), (8, 7, 'WEST'), (8, 9, 'WEST')]:
        signs.append(sign(x, y, 'BG_EVENT_PLAYER_FACING_' + face, pre + 'Slots'))
    for x0 in (14, 18):
        for y in (6, 7, 8):
            for x in (x0, x0 + 1):
                signs.append(sign(x, y, 'BG_EVENT_PLAYER_FACING_ANY', pre + 'Roulette'))
    d = {
        'id': 'MAP_BATTLE_FRONTIER_BATTLE_CASINO',
        'name': MAP,
        'layout': 'LAYOUT_MAUVILLE_CITY_GAME_CORNER',
        'music': 'MUS_GAME_CORNER',
        'region_map_section': 'MAPSEC_BATTLE_FRONTIER',
        'requires_flash': False,
        'weather': 'WEATHER_NONE',
        'map_type': 'MAP_TYPE_INDOOR',
        'allow_cycling': False,
        'allow_escaping': False,
        'allow_running': False,
        'show_map_name': False,
        'battle_scene': 'MAP_BATTLE_SCENE_NORMAL',
        'connections': None,
        'object_events': objs,
        'warp_events': [
            {'x': 11, 'y': 10, 'elevation': 3, 'dest_map': 'MAP_BATTLE_FRONTIER_OUTSIDE_EAST', 'dest_warp_id': str(warp_idx)},
            {'x': 12, 'y': 10, 'elevation': 3, 'dest_map': 'MAP_BATTLE_FRONTIER_OUTSIDE_EAST', 'dest_warp_id': str(warp_idx)},
        ],
        'coord_events': [],
        'bg_events': signs,
    }
    open(MAPDIR + '/map.json', 'w').write(json.dumps(d, indent=2) + '\n')


def register():
    p = 'data/maps/map_groups.json'
    s = open(p).read()
    if '"%s"' % MAP not in s:
        m = re.search(r'("gMapGroup_Grounded": \[\n)(.*?)(\n  \])', s, re.S)
        s = s[:m.end(2)] + ',\n    "%s"' % MAP + s[m.end(2):]
        json.loads(s)
        open(p, 'w').write(s)
    p = 'data/event_scripts.s'
    s = open(p).read()
    line = '\t.include "data/maps/%s/scripts.inc"\n' % MAP
    if line not in s:
        anchor = '\t.include "data/maps/BattleFrontier_StadiumArena/scripts.inc"\n'
        s = s.replace(anchor, anchor + line)
        open(p, 'w').write(s)


if __name__ == '__main__':
    w = patch_outside()
    make_map(w)
    register()
    print('warp-id deur:', w)
