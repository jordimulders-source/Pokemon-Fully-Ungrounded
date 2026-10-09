"""Project Grounded: de Spacetime Cave (post-game hub bij Mossdeep) + deel 1 van de warps.

  SpacetimeCave        Hub (27x20, Cave-tileset violet getint, spacetime_tiles.py): rotsje op een eilandje in
                       Route 125 (46,28); de grotopening verschijnt pas na de Hall of Fame (ON_LOAD). Binnen negen
                       scheuren (2x2): LAVENDER TOWN en CERULEAN CAVE werken (teleporttegel), de rest is instabiel
                       (bord-tekst, nog geen warp): National Park/Ilex, Gen 4-meren, Chargestone Cave, Glimwood
                       Tangle, Area Zero, ?????, en onderaan midden Mt. Coronet (als laatste).
  LavenderTown         FRLG-indeling 1-op-1 (24x20), Emerald-grond/bomen/PC/Mart, Petalburg-huizen met paars dak,
                       de FRLG-toren; terugscheur bij de zuiduitgang. PC (+2F, heal location), Mart, drie huizen.
  PokemonTower_1F-5F   FRLG 1F-4F + de FRLG-7F als 5F (ingekort: 5F/6F weggelaten). Reskin met Ekat's Revamp.
                       Channelers (Hex Maniac-klasse, lv 65-69), wilde ghosts op 3F-5F, bovenin een beloning.
  CeruleanCave_1F/2F/B1F  FRLG 1-op-1 met Emerald-grotaankleding; wilde Pokemon lv 60-70; MEWTWO lv 70 in B1F
                       (vlag FLAG_HIDE_METEOR_FALLS_MEWTWO: er blijft maar een Mewtwo; de oude grot achter Meteor
                       Falls krijgt een kras in de rots i.p.v. Mewtwo). Terugscheur bij de oude uitgang van 1F.
Kaartgroep gMapGroup_Spacetime (nieuw, achteraan). Mapsec MAPSEC_SPACETIME_CAVE (Town Map 26,4); de Kanto-kaarten
gebruiken MAPSEC_LAVENDER_TOWN / MAPSEC_POKEMON_TOWER / MAPSEC_CERULEAN_CAVE.
Flags FLAG_GROUNDED 560-619 (blok 'spacetime_cave' in flags.h), trainers 1159-1168.
Teksten zijn placeholders (Jordi herschrijft ze).
Gebruik: python3 tools/grounded/maptools/spacetime_cave.py [rendermap]"""
import importlib, json, os, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beacon_dragon as bd          # werkmap = repo-root
import spacetime_tiles as st

Scr, text, register_layout = bd.Scr, bd.text, bd.register_layout
COL = 0x400


def T(m, col=False, elev=3):
    return m | (COL if col else 0) | (elev << 12)


# ====================================================================== flags (FLAG_GROUNDED 560-619)
FLAGS = [
    (560, 'FLAG_ITEM_POKEMON_TOWER_3F_MAX_REVIVE', 'Pokemon Tower 3F: Max Revive'),
    (561, 'FLAG_ITEM_POKEMON_TOWER_4F_MAX_ELIXIR', 'Pokemon Tower 4F: Max Elixir'),
    (562, 'FLAG_ITEM_POKEMON_TOWER_4F_DUSK_STONE', 'Pokemon Tower 4F: Dusk Stone'),
    (563, 'FLAG_ITEM_POKEMON_TOWER_4F_DUSK_BALL', 'Pokemon Tower 4F: Dusk Ball'),
    (564, 'FLAG_RECEIVED_POKEMON_TOWER_LIFE_ORB', 'Pokemon Tower 5F: Life Orb van de conciërge'),
    (565, 'FLAG_ITEM_CERULEAN_CAVE_1F_BIG_NUGGET', 'Cerulean Cave 1F: Big Nugget'),
    (566, 'FLAG_ITEM_CERULEAN_CAVE_1F_FULL_RESTORE', 'Cerulean Cave 1F: Full Restore'),
    (567, 'FLAG_ITEM_CERULEAN_CAVE_1F_MAX_ELIXIR', 'Cerulean Cave 1F: Max Elixir'),
    (568, 'FLAG_HIDDEN_ITEM_CERULEAN_CAVE_1F_PP_MAX', 'Cerulean Cave 1F: verborgen PP Max'),
    (569, 'FLAG_ITEM_CERULEAN_CAVE_2F_PP_UP', 'Cerulean Cave 2F: PP Up'),
    (570, 'FLAG_ITEM_CERULEAN_CAVE_2F_RARE_CANDY', 'Cerulean Cave 2F: Rare Candy'),
    (571, 'FLAG_ITEM_CERULEAN_CAVE_2F_FULL_RESTORE', 'Cerulean Cave 2F: Full Restore'),
    (572, 'FLAG_ITEM_CERULEAN_CAVE_B1F_ULTRA_BALL', 'Cerulean Cave B1F: Ultra Ball'),
    (573, 'FLAG_ITEM_CERULEAN_CAVE_B1F_MAX_REVIVE', 'Cerulean Cave B1F: Max Revive'),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// spacetime_cave { (tools/grounded/maptools/spacetime_cave.py; FLAG_GROUNDED 560-619)\n'
    for n, name, why in FLAGS:
        assert 560 <= n <= 619
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// spacetime_cave {' in s:
        i = s.index('// spacetime_cave {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// ruin_beasts {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    s = s.replace('530-559 Beasts of Ruin (ruin_beasts.py), 560+ vrij.',
                  '530-559 Beasts of Ruin (ruin_beasts.py), 560-619 Spacetime Cave deel 1 (spacetime_cave.py), 620+ vrij.')
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== registratie
GROUP = 'gMapGroup_Spacetime'


def const(name):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', '_', name).upper()


def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % GROUP not in g:
        i = g.index('    "gMapGroup_Grounded"\n  ]')
        g = g[:i] + '    "gMapGroup_Grounded",\n    "%s"\n  ]' % GROUP + g[i + len('    "gMapGroup_Grounded"\n  ]'):]
        j = g.rindex('\n  ]\n}')
        g = g[:j] + '\n  ],\n  "%s": [\n  ]\n}' % GROUP + g[j + len('\n  ]\n}'):]
    if '"%s"' % name not in g:
        i = g.index('"%s": [' % GROUP); j = g.index('\n  ]', i)
        body = g[i:j]
        sep = ',' if body.rstrip().endswith('"') else ''
        g = g[:j] + sep + '\n    "%s"' % name + g[j:]
    d = json.loads(g)
    assert len(d[GROUP]) <= 128 and d['group_order'][-1] == GROUP
    open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/MangroveMire/scripts.inc"\n'
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def write_map(name, layout, objs, warps, bgs, coords=(), **kw):
    m = {'id': 'MAP_' + const(name), 'name': name, 'layout': layout, 'music': 'MUS_RG_SEVII_DUNGEON',
         'region_map_section': 'MAPSEC_SPACETIME_CAVE', 'requires_flash': False, 'weather': 'WEATHER_NONE',
         'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': True, 'allow_running': True,
         'show_map_name': True, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
         'object_events': objs, 'warp_events': warps, 'coord_events': list(coords), 'bg_events': bgs}
    m.update(kw)
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    register_map(name)


def save_layout(name, W, H, cells, border, prim, sec):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(struct.pack('<%dH' % len(cells), *cells))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *border))
    register_layout(name, const(name), W, H, prim, sec)
    return 'LAYOUT_' + const(name)


warp, obj, tr, ball, sign, hidden = bd.warp, bd.obj, bd.tr, bd.ball, bd.sign, bd.hidden


def scr(name):
    os.makedirs('data/maps/' + name, exist_ok=True)
    return Scr(name, '@ Project Grounded: %s (tools/grounded/maptools/spacetime_cave.py)\n%s_MapScripts::\n\t.byte 0\n'
               % (name, name))


# ====================================================================== 1. de hub
HUB = 'SpacetimeCave'
HUB_DOOR = (13, 2)
RIFTS = [  # (sleutel, linksboven, bestemming of None, naam op het bord)
    ('Lavender', (4, 5), 'LAVENDER', None),
    ('Cerulean', (4, 10), 'CERULEAN', None),
    ('Park', (4, 14), None, 'a park shaped like a POKé BALL, and a forest behind it that hums'),
    ('Lakes', (21, 5), None, 'three lakes, and three pairs of eyes that are definitely watching'),
    ('Chargestone', (21, 10), None, 'floating rocks and enough static to restyle your hair'),
    ('Glimwood', (21, 14), None, 'glowing mushrooms and a forest that is far too pleased with itself'),
    ('AreaZero', (8, 15), None, 'a crater that keeps going down long after it should have stopped'),
    ('Unknown', (17, 15), None, '?????'),
    ('Coronet', (12, 15), None, 'a mountain at the top of the world, and something enormous breathing behind it'),
]


def hub(lav_rift_warp, cc_rift_warp):
    vre = importlib.import_module('victory_road_ext')
    os.chdir(st.REPO)
    W, H = 27, 20
    g = vre.blank(W, H)
    vre.room(g, 2, 3, 24, 17)
    vre.door(g, HUB_DOOR[0], HUB_DOOR[1])
    for (x, y) in ((2, 3), (24, 3), (2, 17), (24, 17), (10, 3), (16, 3), (2, 8), (24, 8)):
        vre.rock(g, x, y)
    # kristallen (Cave 0x3a5-0x3a7) in een kring in het midden: de 'kern' van de scheuren
    for i, (x, y) in enumerate(((11, 8), (15, 8), (10, 10), (16, 10), (11, 12), (15, 12), (13, 10))):
        g[y][x] = T((0x3a6, 0x3a7)[i % 2] if i < 6 else 0x3a5, True)
    ids = HUB_IDS
    warps = [warp(HUB_DOOR[0], HUB_DOOR[1], 'ROUTE125', ROUTE125_WARP, elev=3)]
    bgs, P, T_ = [], HUB + '_EventScript_', HUB + '_Text_'
    S = scr(HUB)
    for key, (x0, y0), dest, desc in RIFTS:
        for q in range(4):
            x, y = x0 + q % 2, y0 + q // 2
            if dest:                        # bovenste rij = warp (beloopbaar), onderste rij = lijf (dicht)
                g[y][x] = T(ids[(0, q)], q >= 2)
                if q < 2:
                    wid = {'LAVENDER': lav_rift_warp, 'CERULEAN': cc_rift_warp}[dest] + q
                    warps.append(warp(x, y, {'LAVENDER': 'LAVENDER_TOWN', 'CERULEAN': 'CERULEAN_CAVE_1F'}[dest], wid,
                                      elev=3))
            else:
                g[y][x] = T(ids[(1, q)], True)
                bgs.append(sign(x, y, P + 'Rift' + key))
        if not dest:
            S.npc('Rift' + key, "The rift flickers. Through it you can just make out %s.\n\n"
                  "It isn't stable yet. Spacetime is still loading." % desc if desc != '?????' else
                  "The rift shows... nothing. A silhouette of a green dinosaur. Then static.\n\n"
                  "It isn't stable yet. Something in there is very, very round.", 'MSGBOX_SIGN')
    # bordjes en een onderzoeker
    bgs.append(sign(10, 3, P + 'Plaque'))
    S.npc('Plaque', "SPACETIME CAVE\n\nWhere places that no longer exist, never existed, or are in another "
          "cartridge go to wait.\n\nPlease do not feed the timelines.", 'MSGBOX_SIGN')
    objs = [obj('OBJ_EVENT_GFX_SCIENTIST_1', 15, 5, P + 'Researcher', move='MOVEMENT_TYPE_FACE_DOWN')]
    S.npc('Researcher', "Ah, a visitor! I study the rifts. Mostly I study why they won't hold still.\n\n"
          "The one on the far left leads to a town that plays the same sad song on loop. "
          "The one below it smells like a very angry clone.\n\n"
          "The others? Unstable. Give them a few patches.")
    S.write()
    cells = [c for row in g for c in row]
    lay = save_layout(HUB, W, H, cells, [T(0x211, True, 0)] * 4, 'gTileset_SpacetimeGeneral', 'gTileset_SpacetimeCave')
    write_map(HUB, lay, objs, warps, bgs, music='MUS_RG_SEVII_DUNGEON', region_map_section='MAPSEC_SPACETIME_CAVE')
    return g


# ====================================================================== 2. Route 125: eilandje met grotopening
ROUTE125_DOOR = (46, 28)
ROUTE125_WARP = None


def route125():
    global ROUTE125_WARP
    p = 'data/maps/Route125/map.json'
    m = json.load(open(p))
    dm = 'MAP_' + const(HUB)
    if not any(w['dest_map'] == dm for w in m['warp_events']):
        m['warp_events'].append({'x': ROUTE125_DOOR[0], 'y': ROUTE125_DOOR[1], 'elevation': 3, 'dest_map': dm,
                                 'dest_warp_id': '0'})
        open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    ROUTE125_WARP = [i for i, w in enumerate(m['warp_events']) if w['dest_map'] == dm][0]
    s = open('data/maps/Route125/scripts.inc').read()
    line = '\tcall_if_set FLAG_SYS_GAME_CLEAR, Route125_EventScript_OpenSpacetimeCave\n'
    if line not in s:
        s = s.replace('Route125_OnLoad:\n', 'Route125_OnLoad:\n' + line, 1)
    blk = ('@ --- spacetime_cave (tools/grounded/maptools/spacetime_cave.py) ---\n'
           '@ Project Grounded: na de Hall of Fame een grotopening in het rotsje op het eilandje (Spacetime Cave)\n'
           'Route125_EventScript_OpenSpacetimeCave::\n'
           '\tsetmetatile %d, %d, 0x0A7, FALSE\n\treturn\n@ --- einde spacetime_cave ---' % ROUTE125_DOOR)
    s = bd.replace_block(s, '@ --- spacetime_cave', '@ --- einde spacetime_cave ---', blk)
    open('data/maps/Route125/scripts.inc', 'w').write(s.rstrip('\n') + '\n')


# ====================================================================== 3. Lavender Town
LAV = 'LavenderTown'
LAV_RIFT = (11, 18)
ROCK = {0x068, 0x069, 0x06a, 0x070, 0x071, 0x072, 0x073, 0x075, 0x078, 0x079, 0x07a, 0x07b, 0x07d, 0x0b2, 0x0b3,
        0x0ba, 0x0bb, 0x0e7}
PATH = {0x162, 0x163, 0x164, 0x172, 0x173, 0x174}
PC = [[(0x048, 0), (0x049, 0), ('pc_tr1', 0), ('pc_tr2', 0)], [(0x050, 1), (0x051, 1), (0x052, 1), (0x053, 1)],
      [(0x058, 1), (0x059, 1), (0x05a, 1), (0x05b, 1)], [(0x060, 1), (0x061, 1), (0x062, 1), (0x063, 1)]]
MART = [[(0x028, 0), (0x029, 0), (0x029, 0), ('mart_tr', 1)], [(0x030, 1), (0x031, 1), (0x032, 1), (0x033, 1)],
        [(0x038, 1), (0x039, 1), (0x03a, 1), (0x03b, 1)], [(0x060, 1), (0x041, 1), (0x042, 1), (0x043, 1)]]
HOUSE_COL = [[0, 0, 0, 0], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
BUILDINGS = [('PC', 5, 2), ('MART', 18, 12), ('HOUSE', 9, 8), ('HOUSE', 4, 13), ('HOUSE', 9, 13)]
LAV_DOORS = [  # (x, y, kaart) in warp-volgorde
    (6, 5, 'LavenderTown_PokemonCenter_1F'), (19, 15, 'LavenderTown_Mart'), (18, 6, 'PokemonTower_1F'),
    (10, 11, 'LavenderTown_VolunteerHouse'), (5, 16, 'LavenderTown_House1'), (10, 16, 'LavenderTown_House2')]


def lavender(names):
    W, H, v = st.frlg_layout('LavenderTown')
    fid = lambda x, y: v[y * W + x] & 0x3FF
    kind = {}
    for y in range(H):
        for x in range(W):
            m = fid(x, y)
            kind[(x, y)] = 'rock' if m in ROCK else 'path' if m in PATH else 'sign' if m == 0x002 else 'grass'
    rift = {(LAV_RIFT[0] + dx, LAV_RIFT[1] + dy) for dx in (0, 1) for dy in (0, 1)}
    for c in rift:
        kind[c] = 'rift'
    g = [[T(0x001) for _ in range(W)] for _ in range(H)]
    isF = lambda x, y: (x < 0 or y < 0 or x >= W or y >= H) or kind[(x, y)] == 'rock'
    for y in range(H):
        for x in range(W):
            k = kind[(x, y)]
            if k == 'rock':
                px = x % 2
                if not isF(x, y + 1):
                    t = (0x1e4, 0x1e5)[px]
                elif y % 2 == 0:
                    t = (0x1d4, 0x1d5)[px]
                else:
                    t = (0x1dc, 0x1dd)[px]
                g[y][x] = T(t, True)
            elif k == 'sign':
                g[y][x] = T(0x003, True)
            elif k == 'grass' and isF(x, y + 1) and y + 1 < H and (y + 1) % 2 == 0:
                g[y][x] = T((0x1ce, 0x1cf)[x % 2])        # boomkruin steekt in het gras
    for y in range(H):
        for x in range(W):
            if kind[(x, y)] != 'path':
                continue
            P = lambda a, b: kind.get((a, b)) == 'path'
            r = 0 if not P(x, y - 1) else 2 if not P(x, y + 1) else 1
            c = 0 if not P(x - 1, y) else 2 if not P(x + 1, y) else 1
            g[y][x] = T([[0x1d0, 0x1d1, 0x1d2], [0x1d8, 0x1d9, 0x1da], [0x1e0, 0x1e1, 0x1e2]][r][c])
    # toren (FRLG, 7x7) en de scheur
    for dy in range(7):
        for dx in range(7):
            x, y = st.TOWER_X0 + dx, st.TOWER_Y0 + dy
            g[y][x] = T(names[('tower', dx, dy)], bool(v[y * W + x] & 0xC00))
    for q in range(4):
        g[LAV_RIFT[1] + q // 2][LAV_RIFT[0] + q % 2] = T(names[('rift', q)], q >= 2)
    # gebouwen (Emerald)
    for kind_, x0, y0 in BUILDINGS:
        for r in range(4):
            for c in range(4):
                if kind_ == 'HOUSE':
                    m, col = names[('house', r, c)], HOUSE_COL[r][c]
                else:
                    m, col = (PC if kind_ == 'PC' else MART)[r][c]
                    m = names[m] if isinstance(m, str) else m
                g[y0 + r][x0 + c] = T(m, bool(col))
    # gaten tussen de gebouwen (FRLG-huizen waren 5 breed): bloemen
    for (x, y) in ((8, 8), (8, 9), (8, 10), (8, 11), (3, 13), (8, 13), (8, 14), (8, 15), (3, 14), (4, 1), (4, 2),
                   (4, 3), (4, 4), (4, 5)):
        if kind[(x, y)] == 'grass':
            g[y][x] = T(0x004)
    cells = [c for row in g for c in row]
    border = [T(0x1d4, True, 0), T(0x1d5, True, 0), T(0x1dc, True, 0), T(0x1dd, True, 0)]
    lay = save_layout(LAV, W, H, cells, border, 'gTileset_General', 'gTileset_LavenderTown')
    warps = [warp(x, y, const(dest), 0, elev=3) for x, y, dest in LAV_DOORS]
    warps[2]['dest_warp_id'] = '1'                 # torendeur -> de mat in 1F (FRLG: warp 1)
    first_rift = len(warps)
    for q in range(2):
        warps.append(warp(LAV_RIFT[0] + q, LAV_RIFT[1], const(HUB), 1 + q, elev=3))
    S = scr(LAV)
    P = S.P
    objs = [
        obj('OBJ_EVENT_GFX_LITTLE_GIRL', 19, 10, P + 'LittleGirl', move='MOVEMENT_TYPE_WANDER_AROUND', rx=1, ry=1),
        obj('OBJ_EVENT_GFX_MAN_1', 12, 12, P + 'Worker', move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_BOY_1', 10, 6, P + 'Boy', move='MOVEMENT_TYPE_WANDER_UP_AND_DOWN', ry=1),
    ]
    S.npc('LittleGirl', "Do you believe in ghosts?\n\nMy mom says they're just POKéMON. My dad says they're "
          "just POKéMON with unfinished business.\n\nMy dad has a lot of unfinished business.")
    S.npc('Worker', "We were going to renovate the TOWER. Then the rift opened and Kanto just... stopped "
          "updating.\n\nI've been on lunch break for twenty-five years.")
    S.npc('Boy', "You came out of the purple hole! Cool!\n\nThe last person who came out of it was a "
          "grumpy kid with spiky hair. He said 'smell ya later' and went back in.")
    bgs = [sign(15, 11, P + 'TownSign'), sign(21, 7, P + 'TowerSign'), sign(7, 11, P + 'HouseSign'),
           sign(12, 4, P + 'Notice')]
    S.npc('TownSign', "LAVENDER TOWN\nThe Noble Purple Town\n\n(Population: fluctuating. Please count "
          "yourself twice to be sure.)", 'MSGBOX_SIGN')
    S.npc('TowerSign', "POKéMON TOWER\nBecalm the spirits of POKéMON\n\nNo running. No flash photography. "
          "No asking the CHANNELERS if they're okay.", 'MSGBOX_SIGN')
    S.npc('HouseSign', "VOLUNTEER POKéMON HOUSE\n\nAll POKéMON welcome. Ghosts by appointment.", 'MSGBOX_SIGN')
    S.npc('Notice', "NOTICE\n\nSilph Scopes are no longer required. The ghosts have unionized and now "
          "identify themselves voluntarily.", 'MSGBOX_SIGN')
    S.write()
    write_map(LAV, lay, objs, warps, bgs, music='MUS_RG_LAVENDER', region_map_section='MAPSEC_LAVENDER_TOWN',
              map_type='MAP_TYPE_TOWN', weather='WEATHER_NONE', allow_cycling=True, allow_escaping=False)
    return first_rift, kind


# ---------------------------------------------------------------- interieurs (vanilla layouts, Ashfrost als sjabloon)
def interior_from(template, name, door_warp, replace_texts, objs=None):
    """Kopieert een Ashfrost-interieur (map.json + scripts.inc) en vervangt AshfrostTown door de nieuwe naam."""
    old = 'AshfrostTown_' + template
    s = open('data/maps/%s/scripts.inc' % old).read().replace(old, name)
    s = s.replace('HEAL_LOCATION_ASHFROST_TOWN', 'HEAL_LOCATION_LAVENDER_TOWN').replace('LOCALID_ASHFROST_NURSE',
                                                                                         'LOCALID_LAVENDER_NURSE')
    for label, txt in replace_texts.items():
        lbl = name + '_' + label
        m = re.search(r'(?m)^%s:\n((?:\t\.string ".*"\n?)+)' % re.escape(lbl), s)
        assert m, (name, lbl)
        s = s[:m.start()] + text(lbl, txt).rstrip('\n') + '\n' + s[m.end():]
    s = '@ Project Grounded: %s (kopie van %s, tools/grounded/maptools/spacetime_cave.py)\n' % (name, old) + s
    m = json.load(open('data/maps/%s/map.json' % old))
    m['id'], m['name'] = 'MAP_' + const(name), name
    m['region_map_section'] = 'MAPSEC_LAVENDER_TOWN'
    if m['music'] == 'MUS_GROUNDED_ASHFROST':
        m['music'] = 'MUS_RG_LAVENDER'
    js = json.dumps(m, ensure_ascii=False).replace(old, name).replace('LOCALID_ASHFROST_NURSE', 'LOCALID_LAVENDER_NURSE')
    js = js.replace('MAP_ASHFROST_TOWN_', 'MAP_LAVENDER_TOWN_')
    m = json.loads(js)
    for w in m['warp_events']:
        if w['dest_map'] == 'MAP_ASHFROST_TOWN':
            w['dest_map'], w['dest_warp_id'] = 'MAP_LAVENDER_TOWN', str(door_warp)
    if objs is not None:
        m['object_events'] = objs(m['object_events'])
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/scripts.inc' % name, 'w').write(s)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    register_map(name)


def lavender_interiors():
    interior_from('PokemonCenter_1F', 'LavenderTown_PokemonCenter_1F', 0, {
        'EventScript_ExpertM_Text': "I come here to talk to the NURSE. She's the only one in town who answers "
                                    "when you speak to her.\n\nWell. The only one who's alive.",
    })
    interior_from('PokemonCenter_2F', 'LavenderTown_PokemonCenter_2F', 0, {})
    interior_from('Mart', 'LavenderTown_Mart', 1, {})
    houses = [('LavenderTown_VolunteerHouse', 3, 'OBJ_EVENT_GFX_OLD_MAN',
               "MR. FUJI? He went up the TOWER to pray a while ago.\n\nWhich while? That's the thing about this "
               "town. Every while is the same while."),
              ('LavenderTown_House1', 4, 'OBJ_EVENT_GFX_WOMAN_2',
               "My CUBONE wears its mother's skull. My therapist says that's 'a lot to unpack'.\n\n"
               "My CUBONE says nothing. It has never said anything. It just stares."),
              ('LavenderTown_House2', 5, 'OBJ_EVENT_GFX_MAN_2',
               "I'm the NAME RATER. Well, I was. Now everybody names their POKéMON after "
               "rappers and I've lost the will to rate.\n\nYour POKéMON's name? Fine. It's fine. Everything is fine.")]
    for name, door, gfx, txt in houses:
        def objs(o, gfx=gfx, name=name):
            o[0]['graphics_id'] = gfx
            return o
        interior_from('House1', name, door, {'EventScript_Resident_Text': txt}, objs)


def heal_location():
    p = 'src/data/heal_locations.json'
    s = open(p).read()
    if 'HEAL_LOCATION_LAVENDER_TOWN' in s:
        return
    i = s.rindex('    }\n  ]')
    s = s[:i + 5] + (',\n    {\n      "id": "HEAL_LOCATION_LAVENDER_TOWN",\n      "map": "MAP_LAVENDER_TOWN",\n'
                     '      "x": 6,\n      "y": 6,\n      "respawn_map": "MAP_LAVENDER_TOWN_POKEMON_CENTER_1F",\n'
                     '      "respawn_npc": "LOCALID_LAVENDER_NURSE"\n    }') + s[i + 5:]
    json.loads(s)
    open(p, 'w').write(s)


# ====================================================================== 4. Pokemon Tower
TOWER = [('PokemonTower_1F', 'PokemonTower_1F'), ('PokemonTower_2F', 'PokemonTower_2F'),
         ('PokemonTower_3F', 'PokemonTower_3F'), ('PokemonTower_4F', 'PokemonTower_4F'),
         ('PokemonTower_5F', 'PokemonTower_7F')]                # (onze kaart, FRLG-bron)
TOWER_DEST = {'MAP_POKEMON_TOWER_5F': 'MAP_POKEMON_TOWER_5F', 'MAP_POKEMON_TOWER_6F': None,
              'MAP_POKEMON_TOWER_7F': 'MAP_POKEMON_TOWER_5F'}
# trainers: (id-sleutel, kaart, x, y, naam, klas-tekst, team)
IV = 'IVs: 28 HP / 28 Atk / 28 Def / 28 SpA / 28 SpD / 28 Spe'


def mon(head, lvl, moves):
    return bd.mon(head, lvl, moves, iv=IV)


TRAINERS = [
    ('TOWER_MAYA', 'PokemonTower_2F', 16, 5, 'LEFT', 3, 'MAYA', [
        mon('Mismagius', 65, ['Shadow Ball', 'Mystical Fire', 'Dazzling Gleam', 'Nasty Plot']),
        mon('Hypno', 65, ['Psychic', 'Hypnosis', 'Dream Eater', 'Focus Blast']),
        mon('Drifblim', 65, ['Shadow Ball', 'Air Slash', 'Thunderbolt', 'Will-O-Wisp'])],
     "Hey! You're not dead! How refreshing.\n\nI'll fix that. Spiritually.",
     "Okay, okay, you're very alive. I get it.",
     "I used to channel the dead. Now I mostly channel my frustration."),
    ('TOWER_PATRICIA', 'PokemonTower_3F', None, None, None, None, 'PATRICIA', [
        mon('Banette', 65, ['Shadow Claw', 'Gunk Shot', 'Knock Off', 'Shadow Sneak']),
        mon('Golurk', 65, ['Earthquake', 'Shadow Punch', 'Ice Punch', 'Dynamic Punch']),
        mon('Xatu', 65, ['Psychic', 'Air Slash', 'Roost', 'Confuse Ray'])],
     "Kekeke... ke... sorry, I've had this cough since 1996.",
     "Kek. That's the sound of me losing.",
     "The spirits say you'll go far. They also said that about the last guy. He's in the third row."),
    ('TOWER_CARLY', 'PokemonTower_3F', None, None, None, None, 'CARLY', [
        mon('Dusclops', 65, ['Night Shade', 'Will-O-Wisp', 'Pain Split', 'Shadow Sneak']),
        mon('Mr. Mime', 65, ['Psychic', 'Dazzling Gleam', 'Reflect', 'Light Screen']),
        mon('Lampent', 65, ['Shadow Ball', 'Flamethrower', 'Energy Ball', 'Will-O-Wisp'])],
     "Be gone... evil... spirit... oh, it's a kid. Same procedure.",
     "Fine! You may pass, evil kid.",
     "I wear this robe because it's warm. The chanting is optional."),
    ('TOWER_HOPE', 'PokemonTower_3F', None, None, None, None, 'HOPE', [
        mon('Chandelure', 66, ['Shadow Ball', 'Flamethrower', 'Energy Ball', 'Will-O-Wisp']),
        mon('Sableye', 66, ['Knock Off', 'Shadow Claw', 'Will-O-Wisp', 'Recover']),
        mon('Exeggutor', 66, ['Psychic', 'Giga Drain', 'Sleep Powder', 'Leaf Storm'])],
     "My name is HOPE. In this tower that's practically a joke.",
     "And there it goes.",
     "Every grave here has a name on it. Except the ones that have two."),
    ('TOWER_LAUREL', 'PokemonTower_4F', None, None, None, None, 'LAUREL', [
        mon('Cofagrigus', 66, ['Shadow Ball', 'Will-O-Wisp', 'Trick Room', 'Nasty Plot']),
        mon('Slowking', 66, ['Psychic', 'Scald', 'Slack Off', 'Ice Beam']),
        mon('Froslass', 66, ['Shadow Ball', 'Ice Beam', 'Spikes', 'Thunderbolt'])],
     "GHOST! Oh. No. That's my reflection. Long night.",
     "I need a nap. In a coffin, ideally.",
     "The tower used to be quiet. Then that hole in spacetime opened and now we get tourists."),
    ('TOWER_JODY', 'PokemonTower_4F', None, None, None, None, 'JODY', [
        mon('Trevenant', 67, ['Wood Hammer', 'Shadow Claw', 'Horn Leech', 'Will-O-Wisp']),
        mon('Bronzong', 67, ['Gyro Ball', 'Psychic', 'Trick Room', 'Stealth Rock']),
        mon('Houndstone', 67, ['Shadow Claw', 'Play Rough', 'Body Press', 'Crunch'])],
     "I can see five spirits behind you. One of them is rolling its eyes.",
     "The eye-roller says 'told you so'.",
     "My HOUNDSTONE is a good boy. Was a good boy. Remains, technically, a good boy."),
    ('TOWER_PAULA', 'PokemonTower_4F', None, None, None, None, 'PAULA', [
        mon('Gourgeist', 66, ['Shadow Sneak', 'Seed Bomb', 'Will-O-Wisp', 'Leech Seed']),
        mon('Palossand', 66, ['Shadow Ball', 'Earth Power', 'Shore Up', 'Giga Drain']),
        mon('Musharna', 66, ['Psychic', 'Moonblast', 'Yawn', 'Calm Mind'])],
     "Shhh. You'll wake them. And they are SO cranky in the morning.",
     "...They're awake. Thanks.",
     "Please walk softly. Some of them are light sleepers. All of them are heavy grudge-holders."),
    ('TOWER_RUTH', 'PokemonTower_5F', None, None, None, None, 'RUTH', [
        mon('Polteageist', 68, ['Shadow Ball', 'Giga Drain', 'Shell Smash', 'Stored Power']),
        mon('Dhelmise', 68, ['Power Whip', 'Anchor Shot', 'Shadow Claw', 'Earthquake']),
        mon('Gardevoir', 68, ['Psychic', 'Moonblast', 'Calm Mind', 'Mystical Fire'])],
     "We are the CHOIR of the top floor. We sing for the departed.\n\nYou may join. Briefly. Permanently.",
     "That note was flat. Like my team.",
     "We don't actually sing. The acoustics up here are terrible."),
    ('TOWER_TAMMY', 'PokemonTower_5F', None, None, None, None, 'TAMMY', [
        mon('Dusknoir', 68, ['Shadow Punch', 'Earthquake', 'Ice Punch', 'Will-O-Wisp']),
        mon('Jellicent', 68, ['Scald', 'Shadow Ball', 'Recover', 'Will-O-Wisp']),
        mon('Alakazam', 68, ['Psychic', 'Shadow Ball', 'Focus Blast', 'Calm Mind']),
        mon('Spiritomb', 68, ['Sucker Punch', 'Shadow Sneak', 'Foul Play', 'Will-O-Wisp'])],
     "A hundred and eight spirits live in my SPIRITOMB. It gets crowded. They vote on everything.",
     "The vote was unanimous. You win.",
     "Upstairs is the caretaker. He's nice. Tips well. Mostly in items."),
    ('TOWER_KARINA', 'PokemonTower_5F', None, None, None, None, 'KARINA', [
        mon('Gengar', 69, ['Shadow Ball', 'Sludge Bomb', 'Focus Blast', 'Hypnosis']),
        mon('Aegislash', 69, ["King's Shield", 'Shadow Ball', 'Flash Cannon', 'Sacred Sword']),
        mon('Mimikyu', 69, ['Play Rough', 'Shadow Claw', 'Swords Dance', 'Shadow Sneak']),
        mon('Marowak-Alola', 69, ['Shadow Bone', 'Flare Blitz', 'Bonemerang', 'Will-O-Wisp'])],
     "I lead the CHOIR. The MAROWAK in my party has been waiting a very long time for someone to "
     "finally fight it fair.",
     "...It's at peace. Or it's sulking. Hard to tell with skulls.",
     "Go on. The caretaker is waiting. He has been waiting since before the rift."),
]
FIRST_ID = 1159
TRAINER_POS = {   # FRLG-posities (Channelers in 3F/4F, grunts in 7F = onze 5F)
    'TOWER_PATRICIA': (10, 14), 'TOWER_CARLY': (9, 9), 'TOWER_HOPE': (12, 4),
    'TOWER_LAUREL': (17, 7), 'TOWER_JODY': (15, 13), 'TOWER_PAULA': (4, 12),
    'TOWER_RUTH': (9, 10), 'TOWER_TAMMY': (13, 8), 'TOWER_KARINA': (9, 6),
}


def tower(tower_grids, lav_tower_warp):
    out = []
    for name, src_name in TOWER:
        W, H, cells = tower_grids[src_name]
        lay = save_layout(name, W, H, cells, [T(cells[0] & 0x3FF, True, 0)] * 4, 'gTileset_Building',
                          'gTileset_PokemonTower')
        fm = st.frlg_map(src_name)
        warps = []
        for w in fm['warp_events']:
            d = w['dest_map']
            if d == 'MAP_LAVENDER_TOWN':
                d, wid = 'MAP_LAVENDER_TOWN', lav_tower_warp
            elif src_name == 'PokemonTower_7F':
                d, wid = 'MAP_POKEMON_TOWER_4F', 0
            else:
                d = TOWER_DEST.get(d, d)
                wid = int(w['dest_warp_id'])
                if src_name == 'PokemonTower_4F' and w['dest_map'] == 'MAP_POKEMON_TOWER_5F':
                    wid = 0
            warps.append({'x': w['x'], 'y': w['y'], 'elevation': w['elevation'], 'dest_map': d,
                          'dest_warp_id': str(wid)})
        S = scr(name)
        P = S.P
        objs, bgs = [], []
        fobj = {(o['x'], o['y']): o for o in fm['object_events']}
        for key, mp, x, y, face, sight, nm, team, intro, defeat, post in TRAINERS:
            if mp != name:
                continue
            if x is None:
                x, y = TRAINER_POS[key]
                fo = fobj[(x, y)]
                face = fo['movement_type'].replace('MOVEMENT_TYPE_FACE_', '').replace('MOVEMENT_TYPE_LOOK_AROUND', 'DOWN')
                if face not in ('UP', 'DOWN', 'LEFT', 'RIGHT'):
                    face = 'DOWN'
                sight = int(fo['trainer_sight_or_berry_tree_id'])
            objs.append(tr('OBJ_EVENT_GFX_HEX_MANIAC', x, y, S.trainer(key.split('_')[1].title(), key, intro, defeat, post),
                           face, sight))
        if name == 'PokemonTower_1F':
            objs.append(obj('OBJ_EVENT_GFX_NURSE', 18, 13, P + 'Receptionist', move='MOVEMENT_TYPE_FACE_DOWN'))
            S.npc('Receptionist', "Welcome to POKéMON TOWER. Visiting hours are from dusk till dusk.\n\n"
                  "Wild ghosts haunt the upper floors. They're harmless. Mostly. Legally speaking, entirely.")
            objs.append(obj('OBJ_EVENT_GFX_WOMAN_2', 15, 6, P + 'Mourner', move='MOVEMENT_TYPE_FACE_UP'))
            S.npc('Mourner', "I come here every day to visit my CLEFAIRY.\n\nShe isn't buried here. She just "
                  "likes it here. She's around the back, judging the décor.")
            objs.append(obj('OBJ_EVENT_GFX_OLD_MAN', 8, 12, P + 'OldMan', move='MOVEMENT_TYPE_FACE_RIGHT'))
            S.npc('OldMan', "I've been coming here since this was all FRLG.\n\nThe floor used to be green. "
                  "Can you imagine? A green floor. In a graveyard.")
        if name == 'PokemonTower_2F':
            objs.append(obj('OBJ_EVENT_GFX_HEX_MANIAC', 3, 7, P + 'Channeler', elev=0, move='MOVEMENT_TYPE_FACE_RIGHT'))
            S.npc('Channeler', "The upper floors are full of ghosts. Real ones, this time.\n\n"
                  "The real ghosts are nicer than the fake ones. Fewer opinions.")
        if name == 'PokemonTower_3F':
            objs.append(ball(13, 2, 'ITEM_MAX_REVIVE', 'FLAG_ITEM_POKEMON_TOWER_3F_MAX_REVIVE'))
        if name == 'PokemonTower_4F':
            objs += [ball(12, 11, 'ITEM_MAX_ELIXIR', 'FLAG_ITEM_POKEMON_TOWER_4F_MAX_ELIXIR'),
                     ball(8, 11, 'ITEM_DUSK_STONE', 'FLAG_ITEM_POKEMON_TOWER_4F_DUSK_STONE'),
                     ball(11, 16, 'ITEM_DUSK_BALL', 'FLAG_ITEM_POKEMON_TOWER_4F_DUSK_BALL')]
        if name == 'PokemonTower_5F':
            objs.append(obj('OBJ_EVENT_GFX_OLD_MAN', 11, 4, P + 'Caretaker', move='MOVEMENT_TYPE_FACE_DOWN'))
            S.raw(f'''{P}Caretaker::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_POKEMON_TOWER_LIFE_ORB, {P}CaretakerDone
	msgbox {S.T}CaretakerGift, MSGBOX_DEFAULT
	giveitem ITEM_LIFE_ORB
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_POKEMON_TOWER_LIFE_ORB
{P}CaretakerDone::
	msgbox {S.T}CaretakerDone, MSGBOX_DEFAULT
	release
	end
''', [('CaretakerGift', "You climbed all the way up here? With the CHOIR and everything?\n\n"
                        "I'm the caretaker. MR. FUJI left me in charge when he went to find himself. "
                        "Twenty-five years ago.\n\nHere. Someone left this on a grave. It glows. "
                        "I think it's a LIFE ORB, or a very determined nightlight."),
      ('CaretakerDone', "Every soul up here had a trainer once.\n\nTake good care of yours. "
                        "The paperwork for ghosts is unbelievable.")])
        S.write()
        write_map(name, lay, objs, warps, bgs, music='MUS_RG_POKE_TOWER', region_map_section='MAPSEC_POKEMON_TOWER',
                  map_type='MAP_TYPE_INDOOR', allow_escaping=True, show_map_name=(name == 'PokemonTower_1F'))
        out.append(name)
    return out


# ====================================================================== 5. Cerulean Cave
CC = ['CeruleanCave_1F', 'CeruleanCave_2F', 'CeruleanCave_B1F']
CC_RIFT = (32, 20)
CC_ITEMS = {
    'CeruleanCave_1F': [(7, 3, 3, 'ITEM_BIG_NUGGET', 'FLAG_ITEM_CERULEAN_CAVE_1F_BIG_NUGGET'),
                        (11, 16, 3, 'ITEM_FULL_RESTORE', 'FLAG_ITEM_CERULEAN_CAVE_1F_FULL_RESTORE'),
                        (25, 5, 4, 'ITEM_MAX_ELIXIR', 'FLAG_ITEM_CERULEAN_CAVE_1F_MAX_ELIXIR')],
    'CeruleanCave_2F': [(9, 18, 3, 'ITEM_PP_UP', 'FLAG_ITEM_CERULEAN_CAVE_2F_PP_UP'),
                        (29, 16, 3, 'ITEM_RARE_CANDY', 'FLAG_ITEM_CERULEAN_CAVE_2F_RARE_CANDY'),
                        (33, 12, 3, 'ITEM_FULL_RESTORE', 'FLAG_ITEM_CERULEAN_CAVE_2F_FULL_RESTORE')],
    'CeruleanCave_B1F': [(31, 9, 4, 'ITEM_ULTRA_BALL', 'FLAG_ITEM_CERULEAN_CAVE_B1F_ULTRA_BALL'),
                         (32, 2, 3, 'ITEM_MAX_REVIVE', 'FLAG_ITEM_CERULEAN_CAVE_B1F_MAX_REVIVE')],
}
MEWTWO = (7, 12)


def cerulean(cave_grids):
    out = []
    for name in CC:
        W, H, cells = cave_grids[name]
        lay = save_layout(name, W, H, cells, [T(cells[0] & 0x3FF, True, 0)] * 4, 'gTileset_General',
                          'gTileset_CeruleanCave')
        fm = st.frlg_map(name)
        warps = []
        for w in fm['warp_events']:
            if w['dest_map'] == 'MAP_CERULEAN_CITY':
                continue                    # de oude uitgang is nu de scheur
            warps.append({'x': w['x'], 'y': w['y'], 'elevation': w['elevation'], 'dest_map': w['dest_map'],
                          'dest_warp_id': w['dest_warp_id']})
        if name == 'CeruleanCave_1F':
            for q in range(2):
                warps.append(warp(CC_RIFT[0] + q, CC_RIFT[1], const(HUB), 3 + q, elev=3))
        S = scr(name)
        P = S.P
        objs = [obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', fl, 'MOVEMENT_TYPE_LOOK_AROUND',
                    elev=e, sight=it) for x, y, e, it, fl in CC_ITEMS[name]]
        tmp = 0x12
        for o in fm['object_events']:
            if o['graphics_id'] == 'OBJ_EVENT_GFX_ROCK_SMASH_ROCK':
                objs.append(obj('OBJ_EVENT_GFX_BREAKABLE_ROCK', o['x'], o['y'], 'EventScript_RockSmash',
                                'FLAG_TEMP_%X' % tmp, 'MOVEMENT_TYPE_LOOK_AROUND', elev=o['elevation']))
                tmp += 1
        bgs = []
        if name == 'CeruleanCave_1F':
            bgs.append(hidden(12, 2, 'ITEM_PP_MAX', 'FLAG_HIDDEN_ITEM_CERULEAN_CAVE_1F_PP_MAX'))
        if name == 'CeruleanCave_B1F':
            objs.insert(0, obj('OBJ_EVENT_GFX_SPECIES(MEWTWO)', MEWTWO[0], MEWTWO[1], P + 'Mewtwo',
                               'FLAG_HIDE_METEOR_FALLS_MEWTWO', local_id='LOCALID_CERULEAN_CAVE_MEWTWO'))
            S.raw(f'''{P}Mewtwo::
	lock
	faceplayer
	msgbox {S.T}Mewtwo, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MEWTWO, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}MewtwoStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}MewtwoStays
	removeobject LOCALID_CERULEAN_CAVE_MEWTWO
	setflag FLAG_HIDE_METEOR_FALLS_MEWTWO
{P}MewtwoStays::
	release
	end
''', [('Mewtwo', "A voice echoes inside your head.\n\n\"So. You found the real cave. The one in Hoenn was a "
                 "sublet.\"\n\n\"I was cloned in a lab, abandoned by my makers, and left in a cave for "
                 "twenty-five years.\"\n\n\"You are the first visitor who didn't bring a camera crew. Let us begin.\"")])
        S.write()
        write_map(name, lay, objs, warps, bgs, music='MUS_RG_ROCKET_HIDEOUT', region_map_section='MAPSEC_CERULEAN_CAVE',
                  map_type='MAP_TYPE_UNDERGROUND', show_map_name=(name == 'CeruleanCave_1F'))
        out.append(name)
    return out


def fix_cerulean_warp_ids():
    """FRLG-warp 0 van 1F (uitgang) is weg: verwijzingen naar 1F-warp n worden n-1."""
    p = 'data/maps/CeruleanCave_2F/map.json'
    m = json.load(open(p))
    for w in m['warp_events']:
        if w['dest_map'] == 'MAP_CERULEAN_CAVE_1F' and not w.get('_fixed'):
            w['dest_warp_id'] = str(int(w['dest_warp_id']) - 1)
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    p = 'data/maps/CeruleanCave_B1F/map.json'
    m = json.load(open(p))
    for w in m['warp_events']:
        if w['dest_map'] == 'MAP_CERULEAN_CAVE_1F':
            w['dest_warp_id'] = str(int(w['dest_warp_id']) - 1)
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')


# ====================================================================== 6. de oude Mewtwo-grot
def old_mewtwo_cave():
    p = 'data/maps/MeteorFalls_UnknownCave_B1F/map.json'
    m = json.load(open(p))
    m['object_events'] = [o for o in m['object_events'] if 'MEWTWO' not in o['graphics_id']]
    if not any(b.get('script') == 'MeteorFalls_UnknownCave_B1F_EventScript_Scratches' for b in m['bg_events']):
        m['bg_events'].append(sign(13, 5, 'MeteorFalls_UnknownCave_B1F_EventScript_Scratches'))
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    s = ('MeteorFalls_UnknownCave_B1F_MapScripts::\n\t.byte 0\n\n'
         '@ Project Grounded: Mewtwo is verhuisd naar de echte Cerulean Cave (Spacetime Cave, '
         'tools/grounded/maptools/spacetime_cave.py)\n'
         'MeteorFalls_UnknownCave_B1F_EventScript_Scratches::\n'
         '\tmsgbox MeteorFalls_UnknownCave_B1F_Text_Scratches, MSGBOX_SIGN\n\tend\n\n'
         + text('MeteorFalls_UnknownCave_B1F_Text_Scratches',
                "Words have been scratched into the rock by something with no hands.\n\n"
                "\"THIS WAS A REPLICA. I HAVE RETURNED TO THE ORIGINAL. EAST OF THE CITY OF ROCKETS, "
                "THROUGH THE TEAR. DO NOT BRING A MASTER BALL. I WILL KNOW.\""))
    open('data/maps/MeteorFalls_UnknownCave_B1F/scripts.inc', 'w').write(s.rstrip('\n') + '\n')


# ====================================================================== 7. mapsec, wild, trainers
def mapsecs():
    bd.MAPSECS[:] = [('MAPSEC_SPACETIME_CAVE', 'SPACETIME CAVE', 26, 4, 1, 1, 'MAPPOPUP_THEME_STONE', 'Spacetime Cave')]
    bd.mapsecs()


LAND = lambda spec, rate=8: (rate, spec)
WILD = {
    'POKEMON_TOWER_3F': dict(land=(10, [('HAUNTER', 60, 62), ('BANETTE', 60, 62), ('DUSCLOPS', 60, 62),
                                        ('DRIFBLIM', 60, 62), ('LAMPENT', 60, 62), ('GOLURK', 60, 62),
                                        ('DOUBLADE', 61, 63), ('COFAGRIGUS', 61, 63), ('HOUNDSTONE', 61, 63),
                                        ('MISDREAVUS', 61, 63), ('SPIRITOMB', 62, 63), ('MIMIKYU', 62, 63)])),
    'POKEMON_TOWER_4F': dict(land=(10, [('HAUNTER', 62, 64), ('DUSCLOPS', 62, 64), ('TREVENANT', 62, 64),
                                        ('GOURGEIST', 62, 64), ('PALOSSAND', 62, 64), ('BANETTE', 62, 64),
                                        ('SABLEYE', 63, 65), ('ROTOM', 63, 65), ('POLTEAGEIST', 63, 65),
                                        ('DRIFBLIM', 63, 65), ('FROSLASS', 64, 65), ('GENGAR', 64, 65)])),
    'POKEMON_TOWER_5F': dict(land=(10, [('HAUNTER', 64, 66), ('MISMAGIUS', 64, 66), ('DUSCLOPS', 64, 66),
                                        ('CHANDELURE', 64, 66), ('GOLURK', 64, 66), ('RUNERIGUS', 64, 66),
                                        ('AEGISLASH', 65, 67), ('GOURGEIST', 65, 67), ('DHELMISE', 65, 67),
                                        ('SPIRITOMB', 65, 67), ('DRAGAPULT', 66, 68), ('MAROWAK_ALOLA', 66, 68)])),
    'CERULEAN_CAVE_1F': dict(
        land=(7, [('CROBAT', 60, 62), ('PARASECT', 60, 62), ('ALAKAZAM', 60, 62), ('ELECTRODE', 60, 62),
                  ('MAGNETON', 60, 62), ('RHYDON', 61, 63), ('MACHOKE', 61, 63), ('SANDSLASH', 61, 63),
                  ('WOBBUFFET', 61, 63), ('DITTO', 61, 63), ('BLISSEY', 63, 64), ('CLEFABLE', 63, 64)]),
        water=(4, [('GOLDUCK', 60, 63), ('SEAKING', 60, 63), ('SLOWBRO', 60, 63), ('POLIWHIRL', 61, 63),
                   ('DEWGONG', 62, 64)]),
        fishing=(20, [('GOLDEEN', 30, 34), ('POLIWAG', 30, 34), ('SEAKING', 50, 54), ('POLIWHIRL', 50, 54),
                      ('KINGLER', 50, 54), ('KINGLER', 60, 63), ('SEAKING', 60, 63), ('GYARADOS', 60, 63),
                      ('SLOWBRO', 62, 64), ('DRAGONAIR', 62, 64)])),
    'CERULEAN_CAVE_2F': dict(
        land=(7, [('CROBAT', 62, 64), ('VENOMOTH', 62, 64), ('PRIMEAPE', 62, 64), ('RAICHU', 62, 64),
                  ('HYPNO', 62, 64), ('DUGTRIO', 62, 64), ('MAROWAK', 63, 65), ('MAGNETON', 63, 65),
                  ('KANGASKHAN', 63, 65), ('DITTO', 63, 65), ('LICKITUNG', 64, 66), ('SNORLAX', 64, 66)]),
        water=(4, [('GOLDUCK', 62, 65), ('SEAKING', 62, 65), ('STARMIE', 62, 65), ('CLOYSTER', 63, 65),
                   ('LAPRAS', 64, 66)]),
        fishing=(20, [('GOLDEEN', 30, 34), ('KRABBY', 30, 34), ('SEAKING', 50, 54), ('POLIWHIRL', 50, 54),
                      ('STARYU', 50, 54), ('KINGLER', 62, 65), ('SEAKING', 62, 65), ('GYARADOS', 62, 65),
                      ('STARMIE', 63, 65), ('DRAGONAIR', 64, 66)])),
    'CERULEAN_CAVE_B1F': dict(
        land=(7, [('CROBAT', 65, 67), ('RHYDON', 65, 67), ('ELECTRODE', 65, 67), ('ALAKAZAM', 65, 67),
                  ('MACHOKE', 65, 67), ('MAGNETON', 65, 67), ('WOBBUFFET', 66, 68), ('DITTO', 66, 68),
                  ('KANGASKHAN', 66, 68), ('BLISSEY', 66, 68), ('SNORLAX', 68, 70), ('PORYGON2', 68, 70)]),
        water=(4, [('GOLDUCK', 65, 68), ('SLOWBRO', 65, 68), ('SEAKING', 65, 68), ('DEWGONG', 66, 68),
                   ('LAPRAS', 68, 70)]),
        fishing=(20, [('GOLDEEN', 30, 34), ('POLIWAG', 30, 34), ('SEAKING', 52, 56), ('POLIWHIRL', 52, 56),
                      ('KRABBY', 52, 56), ('KINGLER', 65, 68), ('SEAKING', 65, 68), ('GYARADOS', 65, 68),
                      ('SLOWBRO', 66, 68), ('DRAGONITE', 68, 70)])),
}
SPECIES_ALIAS = {'GOURGEIST': 'GOURGEIST_AVERAGE', 'POLTEAGEIST': 'POLTEAGEIST_PHONY', 'MIMIKYU': 'MIMIKYU_DISGUISED',
                 'AEGISLASH': 'AEGISLASH_SHIELD'}


def wild():
    for mp, tabs in WILD.items():
        for k, (rate, spec) in tabs.items():
            if k == 'land':
                assert len({s for s, a, b in spec}) == 12, (mp, 'niet 12 uniek')
            tabs[k] = (rate, [(SPECIES_ALIAS.get(s, s), a, b) for s, a, b in spec])
    # fishing heeft per hengel eigen slots: dubbele soorten tussen hengels zijn normaal (beacon_dragon telt alleen uniek)
    src = open(os.path.join(HERE, 'beacon_dragon.py')).read()
    f = src[src.index('def wild():'):src.index('# ====================================================================== trainers')]
    a = "assert len({x[0] for x in spec}) == len(spec), ('dubbele soort', mp, kind)"
    assert a in f
    f = f.replace(a, "assert kind == 'fishing' or len({x[0] for x in spec}) == len(spec), ('dubbele soort', mp, kind)")
    ns = dict(bd.__dict__)
    ns['WILD'] = WILD
    exec(f, ns)
    ns['wild']()


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = '// spacetime_cave { (tools/grounded/maptools/spacetime_cave.py; id 1159-1168)\n'
    for i, t in enumerate(TRAINERS):
        blk += '#define TRAINER_%-28s%d // Project Grounded: Pokemon Tower (Spacetime Cave), %s\n' % (t[0], FIRST_ID + i, t[6])
    blk += '// }'
    if '// spacetime_cave {' in s:
        i = s.index('// spacetime_cave {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for n in range(FIRST_ID, FIRST_ID + len(TRAINERS)):
        hits = re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)
        assert len(hits) == 1, ('trainer-id dubbel', n, hits)
    open(p, 'w').write(s)
    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- spacetime_cave (tools/grounded/maptools/spacetime_cave.py) --- */\n\n'
    for key, mp, x, y, face, sight, nm, team, *_ in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: Hex Maniac', 'Pic: Hex Maniac', 'Gender: Female', 'Music: Suspicious',
               'Double Battle: No', bd.AI]
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (key, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde spacetime_cave --- */'
    s = bd.replace_block(s, '/* --- spacetime_cave', '/* --- einde spacetime_cave --- */', blk)
    open(p, 'w').write(s)


def credits():
    p = 'CREDITS.md'
    s = open(p).read()
    line = ('- **Pokémon Tower-interieur** (vloer, graven): **Ekat99**, sheet "Pokémon Tower Interior (Revamp)" uit '
            "Ekat's Public Tiles (`graphics/grounded/tilesets/ekat/pokemon_tower_interior_revamp.png`; Credits.txt van de "
            'zip noemt voor deze sheet geen extra makers). Indeling en overige tegels van Lavender Town, Pokémon Tower en '
            'Cerulean Cave: Pokémon FireRed / LeafGreen via **pret/pokefirered** (omgezet met '
            '`tools/grounded/maptools/spacetime_tiles.py`).\n')
    if 'Pokémon Tower-interieur' not in s:
        anchor = '- **N** (trainerfoto en overworld)'
        s = s.replace(anchor, line + anchor, 1)
        open(p, 'w').write(s)


# ====================================================================== controles
def check():
    sys.modules.pop('landlib', None)
    ll = importlib.import_module('landlib')
    problems = []

    def reach_all(name, start, surf=False):
        k = ll.Kaart(name)
        solid = {(o['x'], o['y']) for o in k.d['object_events'] if 'BREAKABLE_ROCK' not in o['graphics_id']} - {start}
        seen = {start: k.elev(*start)}
        q = [start]
        while q:
            x, y = q.pop()
            ze = seen[(x, y)]
            wz = k.beh(x, y) in ll.WATER
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (x + dx, y + dy)
                if p in seen or not (0 <= p[0] < k.w and 0 <= p[1] < k.h) or k.blocked(*p) or p in solid:
                    continue
                b = k.beh(*p)
                if b in ll.LEDGE or (b in ll.WATER and not surf):
                    continue
                e = k.elev(*p)
                if not (b in ll.WATER or wz or e in (0, 15) or ze in (0, 15) or e == ze):
                    continue
                seen[p] = ze if e == 15 else e
                q.append(p)
        return k, seen

    def adj(r, x, y):
        return any((x + dx, y + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))

    # hub: alle scheuren en het bord bereikbaar vanaf de deur
    k, r = reach_all(HUB, (HUB_DOOR[0], HUB_DOOR[1] + 1))
    for key, (x0, y0), dest, desc in RIFTS:
        ok = any(adj(r, x0 + q % 2, y0 + q // 2) or (x0 + q % 2, y0 + q // 2) in r for q in range(4))
        if not ok: problems.append('hub: scheur %s onbereikbaar' % key)
    # Lavender: alle deuren en de scheur vanaf de scheur
    k, r = reach_all(LAV, (LAV_RIFT[0], LAV_RIFT[1] - 1))
    for x, y, dest in LAV_DOORS:
        if not (adj(r, x, y) or (x, y) in r): problems.append('Lavender: deur %s onbereikbaar' % dest)
    for o in k.d['object_events']:
        if not adj(r, o['x'], o['y']): problems.append('Lavender: NPC %s' % o['script'])
    # toren: elke verdieping vanaf de trap omlaag naar de trap omhoog
    for name, _ in TOWER:
        k = ll.Kaart(name)
        w0 = k.d['warp_events']
        start = [(w['x'], w['y']) for w in w0][-1 if name != 'PokemonTower_1F' else 1]
        k, r = reach_all(name, start)
        for w in w0:
            if not (adj(r, w['x'], w['y']) or (w['x'], w['y']) in r): problems.append('%s: warp %s' % (name, w))
        for o in k.d['object_events']:
            if not adj(r, o['x'], o['y']) and 'Receptionist' not in o['script']: problems.append('%s: object %s' % (name, o['script']))
    # Cerulean Cave: alles vanaf de scheur in 1F, over de ladders heen (met surf)
    seen = {}
    todo = [('CeruleanCave_1F', (CC_RIFT[0], CC_RIFT[1] - 1))]
    while todo:
        name, start = todo.pop()
        k, r = reach_all(name, start, surf=True)
        seen.setdefault(name, set()).update(r)
        for w in k.d['warp_events']:
            if (w['x'], w['y']) in r and w['dest_map'].startswith('MAP_CERULEAN_CAVE'):
                dn = {'MAP_CERULEAN_CAVE_1F': 'CeruleanCave_1F', 'MAP_CERULEAN_CAVE_2F': 'CeruleanCave_2F',
                      'MAP_CERULEAN_CAVE_B1F': 'CeruleanCave_B1F'}[w['dest_map']]
                dw = ll.Kaart(dn).d['warp_events'][int(w['dest_warp_id'])]
                if (dw['x'], dw['y']) not in seen.get(dn, set()):
                    todo.append((dn, (dw['x'], dw['y'])))
    for name in CC:
        k = ll.Kaart(name)
        for o in k.d['object_events']:
            if 'BREAKABLE' in o['graphics_id']: continue
            if not adj(seen.get(name, set()), o['x'], o['y']): problems.append('%s: object %s %s' % (name, o['x'], o['y']))
    print('controles:', 'ok' if not problems else '\n  ' + '\n  '.join(problems))
    return problems


# ====================================================================== main
def main():
    flags()
    tower_grids = st.tower_tileset()
    lav_names = st.lavender_tileset()
    global HUB_IDS
    HUB_IDS = st.spacetime_tilesets()
    cave_grids = st.cave_tileset({'CeruleanCave_1F': CC_RIFT})
    st.register()
    route125()
    lav_rift, _ = lavender(lav_names)
    lavender_interiors()
    heal_location()
    names = tower(tower_grids, 2)
    names += cerulean(cave_grids)
    fix_cerulean_warp_ids()
    cc_rift = len(json.load(open('data/maps/CeruleanCave_1F/map.json'))['warp_events']) - 2
    hub(lav_rift, cc_rift)
    old_mewtwo_cave()
    mapsecs()
    wild()
    trainers()
    credits()
    subprocess.run(['make', '-j4'] + ['data/tilesets/secondary/%s/tiles.4bpp' % d for d in
                                      ('pokemon_tower', 'cerulean_cave', 'lavender_town', 'spacetime_cave')],
                   check=True, capture_output=True)
    probs = check()
    if len(sys.argv) > 1:
        for n in [HUB, LAV, 'LavenderTown_PokemonCenter_1F'] + names:
            m = json.load(open('data/maps/%s/map.json' % n))
            L = bd.layout_of(n)
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', str(L['height'])], check=True)
    print('klaar')
    return probs


HUB_IDS = None
if __name__ == '__main__':
    main()
