"""Project Grounded: de Spacetime Cave (post-game hub bij Mossdeep) + deel 1 van de warps.

  SpacetimeCave        Hub (Cave-tileset violet getint, spacetime_tiles.py): rotsheuvel op een eilandje in
                       Route 125 (45,28); de grotopening verschijnt pas na de Hall of Fame (ON_LOAD). Binnen zes
                       scheuren (2x2): LAVENDER TOWN en CERULEAN CAVE werken (teleporttegel), de rest is open maar
                       nog zonder overkant (bord-tekst): National Park/Ilex, Chargestone Cave, Glimwood Tangle,
                       Area Zero. Daaronder de gang naar ?????, de meren en Mt. Coronet (zie S2).
  LavenderTown         FRLG-indeling 1-op-1 (24x20), Emerald-grond/bomen/PC/Mart, Petalburg-huizen met paars dak,
                       de FRLG-toren; terugscheur bij de zuiduitgang. PC (+2F, heal location), Mart, drie huizen.
  PokemonTower_1F-5F   FRLG 1F-4F + de FRLG-7F als 5F (ingekort: 5F/6F weggelaten). Reskin met Ekat's Revamp.
                       Channelers (Hex Maniac-klasse, lv 65-69), wilde ghosts op 3F-5F, bovenin een beloning.
  CeruleanCave_1F/2F/B1F  FRLG 1-op-1 met Emerald-grotaankleding; wilde Pokemon lv 60-70; MEWTWO lv 70 in B1F
                       (vlag FLAG_HIDE_METEOR_FALLS_MEWTWO: er blijft maar een Mewtwo; de oude grot achter Meteor
                       Falls krijgt een kras in de rots i.p.v. Mewtwo). Terugscheur bij de oude uitgang van 1F.
S1 (Jordi, 9 okt): groter eiland met rotsheuvel op Route 125; eerste bezoek: Dialga + Palkia openen de scheuren
  (behalve ????? en Coronet), quest-poort Spacetime_AllSidequestsDone (lijst SIDEQUESTS); Lavender als spookstad
  (eigen paletten, graven, dode bomen, kwade geesten, bezeten Channelers, baas Agatha op 5F) en na de bevrijding
  layout LavenderTown_Calm; Cerulean Cave: Rocket-grunts, Giovanni voor Mewtwo, Mewtwo healt en vecht (lv 75).
S2 (Jordi, 9 okt): Route 125-ingang met vanilla rotsheuvel (Route 111 + SkyPillar_Outside); hoofdzaal alleen de
  zes sidequest-scheuren; onder de hoofdzaal (zelfde kaart, 27x68) een gang met poorten: gevouwen wand (open na
  Spacetime_AllSidequestsDone) -> ?????-kamer -> gevouwen wand (FLAG_SPACETIME_YOSHI_DONE) -> meren-kamer (Dialga +
  Palkia, Acuity/Valor/Verity) -> doodlopend met Giratina-inscriptie (open als Giratina gevangen is) -> Mt. Coronet.
  Portalen nog zonder warp. Lavender: Silph Scope van de oud-verkoper in het PC; zonder scope Gen 1-GHOST
  (src/gen1_ghost.c, tools/grounded/gen1_ghost_sprites.py).
Kaartgroep gMapGroup_Spacetime (nieuw, achteraan). Mapsec MAPSEC_SPACETIME_CAVE (Town Map 26,4); de Kanto-kaarten
gebruiken MAPSEC_LAVENDER_TOWN / MAPSEC_POKEMON_TOWER / MAPSEC_CERULEAN_CAVE.
Flags FLAG_GROUNDED 560-619 (blok 'spacetime_cave' in flags.h; 560-582 in gebruik), trainers 1159-1169 en 1195-1199.
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
    # S1: eerste bezoek, quest-poorten en de Lavender-quest
    (574, 'FLAG_SPACETIME_RIFTS_OPENED', 'Spacetime Cave: Dialga en Palkia hebben de scheuren geopend'),
    (575, 'FLAG_SPACETIME_LAVENDER_DONE', 'Spacetime-sidequest klaar: Lavender bevrijd (Agatha verslagen)'),
    (576, 'FLAG_SPACETIME_CERULEAN_DONE', 'Spacetime-sidequest klaar: Mewtwo gevangen/verslagen'),
    (577, 'FLAG_HIDE_LAVENDER_GHOST_GENGAR', 'Lavender Town: kwade geest voor de toren verdreven'),
    (578, 'FLAG_HIDE_LAVENDER_GHOST_DUSKNOIR', 'Lavender Town: kwade geest bij de noorduitgang verdreven'),
    (579, 'FLAG_HIDE_LAVENDER_GHOST_BANETTE', 'Lavender Town: kwade geest bij de westuitgang verdreven'),
    # S2: de gang onder de hoofdzaal en de Silph Scope
    (580, 'FLAG_SPACETIME_YOSHI_DONE', "Spacetime: Yoshi's Island gefixt (opent de gang naar de meren; nog nooit gezet)"),
    (581, 'FLAG_SPACETIME_LAKES_SCENE', 'Spacetime: Dialga en Palkia hebben de meren-portalen geopend'),
    (582, 'FLAG_RECEIVED_SILPH_SCOPE', 'Lavender Town: Silph Scope van de oud-verkoper in het PC'),
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
# S2 (Jordi, 9 okt): in de hoofdzaal alleen de zes sidequest-scheuren. Onderin loopt een gang naar het zuiden
# (een lange kaart met poorten): instabiele wand (open na Spacetime_AllSidequestsDone) -> ?????-kamer ->
# instabiele wand (open na FLAG_SPACETIME_YOSHI_DONE) -> meren-kamer (Dialga + Palkia, drie portalen) ->
# doodlopend stuk met een Giratina-inscriptie (open als Giratina gevangen is) -> Mt. Coronet-portaal.
HUB = 'SpacetimeCave'
HUB_DOOR = (13, 2)
RIFTS = [  # (sleutel, linksboven, bestemming of None, naam op het bord)
    ('Lavender', (4, 5), 'LAVENDER', None),
    ('Cerulean', (4, 10), 'CERULEAN', None),
    ('Park', (4, 14), None, 'a park shaped like a POKé BALL, and a forest behind it that hums'),
    ('Chargestone', (21, 5), 'CHARGESTONE', None),
    ('Glimwood', (21, 10), None, 'glowing mushrooms and a forest that is far too pleased with itself'),
    ('AreaZero', (21, 14), None, 'a crater that keeps going down long after it should have stopped'),
]
# S1: eerste bezoek (Dialga + Palkia openen de scheuren) en quest-poorten.
# Toestand per scheur na de scene: 'warp' (werkt), 'open' (open maar de overkant bestaat nog niet).
RIFT_STATE = {'Lavender': 'warp', 'Cerulean': 'warp', 'Park': 'open', 'Chargestone': 'warp', 'Glimwood': 'open',
              'AreaZero': 'open'}
# Sidequests die meetellen voor de gang naar ?????. Een nieuwe locatie: haar klaar-flag hier toevoegen (en opnieuw
# draaien). Nog niet gebouwde locaties (National Park/Ilex, Chargestone Cave, Glimwood Tangle, Area Zero) tellen pas
# mee zodra hun flag hier staat; tot dan telt alleen wat bestaat. De meren-kamer ligt na ????? en telt niet mee.
SIDEQUESTS = [('FLAG_SPACETIME_LAVENDER_DONE', 'Lavender Town: de kwade geesten verdreven'),
              ('FLAG_SPACETIME_CERULEAN_DONE', 'Cerulean Cave: Mewtwo gevangen of verslagen'),
              ('FLAG_SPACETIME_CHARGESTONE_DONE', 'Chargestone Cave: Zeraora gevangen of verslagen')]
HUB_DIALGA, HUB_PALKIA, HUB_RESEARCHER = (10, 7), (16, 7), (18, 4)
# de diepte (zelfde kaart, onder de hoofdzaal); de gang is 2 breed (x 13-14)
CX = 13
DEEP_ROOMS = {'Unknown': (6, 26, 20, 31), 'Lakes': (4, 40, 22, 48), 'Coronet': (8, 60, 18, 65)}
GATE_UNKNOWN, GATE_YOSHI = (CX, 19), (CX, 34)       # instabiele wand (2x2, linksboven)
DEAD_END = 54                                        # rij van de doodlopende rand (dicht tot Giratina gevangen is)
PORTALS = [  # (sleutel, linksboven, kamer)
    ('Unknown', (9, 28), 'Unknown'),
    ('Valor', (CX, 42), 'Lakes'), ('Acuity', (7, 45), 'Lakes'), ('Verity', (18, 45), 'Lakes'),
    ('Coronet', (CX, 62), 'Coronet'),
]
LAKES_DIALGA, LAKES_PALKIA = (10, 42), (17, 42)
HUB_W, HUB_H = 27, 68


def hub_grid(ids):
    """Raster van de hele kaart, alle poorten open (de dichte toestand zet het kaartscript / hub())."""
    vre = importlib.import_module('victory_road_ext')
    g = vre.blank(HUB_W, HUB_H)
    F3 = vre.F
    vre.room(g, 2, 3, 24, 17)
    vre.door(g, HUB_DOOR[0], HUB_DOOR[1])
    for (x, y) in ((2, 3), (24, 3), (2, 17), (24, 17), (10, 3), (16, 3), (2, 8), (24, 8)):
        vre.rock(g, x, y)
    # kristallen (Cave 0x3a5-0x3a7) in een kring in het midden: de 'kern' van de scheuren
    for i, (x, y) in enumerate(((11, 8), (15, 8), (10, 10), (16, 10), (11, 12), (15, 12), (13, 10))):
        g[y][x] = T((0x3a6, 0x3a7)[i % 2] if i < 6 else 0x3a5, True)
    for (x0, y0, x1, y1) in DEEP_ROOMS.values():
        vre.room(g, x0, y0, x1, y1)
    for (x0, y0, x1, y1) in DEEP_ROOMS.values():
        for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            if abs(x - CX) > 3:
                vre.rock(g, x, y)

    def corridor(ya, yb):
        """gang x CX..CX+1 van rij ya (de onderrand van de kamer erboven) tot yb (de bovenwand van de kamer eronder)."""
        for y in range(ya, yb + 1):
            g[y][CX - 1], g[y][CX + 2] = T(0x212, True), T(0x210, True)
            g[y][CX] = g[y][CX + 1] = F3
        # aansluiting op de onderrand erboven (GraniteCave_B1F: 20a links, 208 rechts)
        g[ya][CX - 1], g[ya][CX + 2] = T(0x20a, True), T(0x208, True)
        # aansluiting op de bovenwand eronder (AlteringCave/Shoal Cave: 21a links, 218 rechts; tweede rij 219)
        g[yb - 1][CX - 1], g[yb - 1][CX + 2] = T(0x21a, True), T(0x218, True)
        g[yb][CX - 1], g[yb][CX + 2] = T(0x219, True), T(0x219, True)
    corridor(18, 25)
    corridor(32, 39)
    corridor(49, 59)
    # wat kristallen in de diepere kamers
    for (x, y) in ((16, 27), (18, 29), (7, 30), (5, 41), (21, 41), (11, 47), (16, 47), (10, 61), (16, 61)):
        g[y][x] = T((0x3a6, 0x3a7)[(x + y) % 2], True)
    for key, (x0, y0), room in PORTALS:
        for q in range(4):
            g[y0 + q // 2][x0 + q % 2] = T(ids[(0, q)], True)
    return g


def hub_closed_cells(ids, g):
    """De dichte toestand per poort: {poort: [(x, y, metatile, col)]}."""
    out = {}
    for key, (gx, gy) in (('Unknown', GATE_UNKNOWN), ('Yoshi', GATE_YOSHI)):
        out[key] = [(gx + q % 2, gy + q // 2, ids[(2, q)], True) for q in range(4)]
    # Giratina: de gang eindigt in een onderrand; daaronder rots, en de bovenwand van de Coronet-kamer dicht
    y = DEAD_END
    cells = [(CX - 1, y, 0x224, True), (CX, y, 0x221, True), (CX + 1, y, 0x221, True), (CX + 2, y, 0x224, True)]
    top = DEEP_ROOMS['Coronet'][1] - 2
    for yy in range(y + 1, top):
        cells += [(x, yy, 0x211, True) for x in range(CX - 1, CX + 3)]
    cells += [(x, yy, 0x219, True) for yy in (top, top + 1) for x in range(CX - 1, CX + 3)]
    out['Giratina'] = cells
    return out


def hub_reach(g, start):
    seen, q = {start}, [start]
    while q:
        x, y = q.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if 0 <= p[0] < HUB_W and 0 <= p[1] < HUB_H and p not in seen and not g[p[1]][p[0]] & 0xC00:
                seen.add(p); q.append(p)
    return seen


def hub(lav_rift_warp, cc_rift_warp):
    os.chdir(st.REPO)
    ids = HUB_IDS
    g = hub_grid(ids)
    closed = hub_closed_cells(ids, g)
    # controle (alles open): elk portaal bereikbaar vanaf de deur
    r = hub_reach(g, (HUB_DOOR[0], HUB_DOOR[1] + 1))
    for key, (x0, y0), room in PORTALS:
        assert any((x0 + dx + ex, y0 + dy + ey) in r for dx in (0, 1) for dy in (0, 1)
                   for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1))), ('portaal onbereikbaar', key)
    # map.bin = alle poorten dicht (zo ziet de speler het eerst)
    gc = [row[:] for row in g]
    for cells in closed.values():
        for x, y, m, col in cells:
            gc[y][x] = T(m, col)
    warps = [warp(HUB_DOOR[0], HUB_DOOR[1], 'ROUTE125', ROUTE125_WARP, elev=3)]
    bgs, P, T_ = [], HUB + '_EventScript_', HUB + '_Text_'
    head = ('@ Project Grounded: SpacetimeCave (tools/grounded/maptools/spacetime_cave.py)\n'
            'SpacetimeCave_MapScripts::\n'
            '\tmap_script MAP_SCRIPT_ON_LOAD, SpacetimeCave_OnLoad\n'
            '\tmap_script MAP_SCRIPT_ON_TRANSITION, SpacetimeCave_OnTransition\n'
            '\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, SpacetimeCave_OnFrame\n\t.byte 0\n')
    S = Scr(HUB, head)
    hide, opened = [], []          # setmetatile-regels: scheuren voor/na de eerste scene
    for key, (x0, y0), dest, desc in RIFTS:
        state = RIFT_STATE[key]
        for q in range(4):
            x, y = x0 + q % 2, y0 + q // 2
            floor = g[y][x] & 0x3FF
            if state == 'warp':             # bovenste rij = warp (beloopbaar), onderste rij = lijf (dicht)
                m, col = ids[(0, q)], q >= 2
                if q < 2:
                    # Chargestone (chargestone.py) heeft één aankomstwarp (index 0) voor beide vakken
                    wid = {'LAVENDER': lav_rift_warp + q, 'CERULEAN': cc_rift_warp + q, 'CHARGESTONE': 0}[dest]
                    warps.append(warp(x, y, {'LAVENDER': 'LAVENDER_TOWN', 'CERULEAN': 'CERULEAN_CAVE_1F',
                                             'CHARGESTONE': 'CHARGESTONE_CAVE_1F'}[dest], wid, elev=3))
            else:                           # open (actief beeld), nog geen overkant: massief + bordje
                m, col = ids[(0, q)], True
                bgs.append(sign(x, y, P + 'Rift' + key))
            g[y][x] = gc[y][x] = T(m, col)
            hide.append('\tsetmetatile %d, %d, 0x%03X, FALSE\n' % (x, y, floor))
            opened.append('\tsetmetatile %d, %d, 0x%03X, %s\n' % (x, y, m, 'TRUE' if col else 'FALSE'))
        if state == 'open':
            S.npc('Rift' + key, "The rift is wide open. Through it you can just make out %s.\n\n"
                  "The other side hasn't finished existing yet, though. Spacetime is still loading." % desc,
                  'MSGBOX_SIGN')

    def setm(cells):
        return ''.join('\tsetmetatile %d, %d, 0x%03X, %s\n' % (x, y, m & 0x3FF, 'TRUE' if col else 'FALSE')
                       for x, y, m, col in cells)

    def open_cells(key):
        return [(x, y, g[y][x] & 0x3FF, bool(g[y][x] & 0xC00)) for x, y, m, col in closed[key]]
    lake_floor = [(x0 + q % 2, y0 + q // 2, 0x201, False) for key, (x0, y0), room in PORTALS if room == 'Lakes'
                  for q in range(4)]
    lake_open = [(x0 + q % 2, y0 + q // 2, ids[(0, q)], True) for key, (x0, y0), room in PORTALS if room == 'Lakes'
                 for q in range(4)]
    # quest-poort (uitbreidbaar): VAR_RESULT = TRUE als alles klaar is, VAR_0x8005 = aantal open sidequests
    code = ('@ Spacetime_AllSidequestsDone: VAR_RESULT = TRUE als alle Spacetime-sidequests klaar zijn, VAR_0x8005 = het\n'
            '@ aantal dat nog openstaat. Uitbreiden: de klaar-flag van een nieuwe locatie in SIDEQUESTS (spacetime_cave.py)\n'
            '@ zetten. Nog niet gebouwde locaties (National Park/Ilex, Chargestone Cave, Glimwood Tangle, Area Zero) tellen\n'
            '@ pas mee als hun flag in de lijst staat; tot dan telt alleen wat bestaat.\n'
            'Spacetime_AllSidequestsDone::\n\tsetvar VAR_0x8005, 0\n')
    for fl, why in SIDEQUESTS:
        code += '\tcall_if_unset %s, Spacetime_EventScript_CountOpen @ %s\n' % (fl, why)
    code += ('\tsetvar VAR_RESULT, FALSE\n\tcall_if_eq VAR_0x8005, 0, Spacetime_EventScript_AllDone\n\treturn\n\n'
             'Spacetime_EventScript_CountOpen:\n\taddvar VAR_0x8005, 1\n\treturn\n\n'
             'Spacetime_EventScript_AllDone:\n\tsetvar VAR_RESULT, TRUE\n\treturn\n')
    S.raw(code)
    # kaartscripts: lege grot tot de scene; poorten open volgens hun flags
    S.raw('SpacetimeCave_OnLoad:\n'
          '\tcall_if_unset FLAG_SPACETIME_RIFTS_OPENED, SpacetimeCave_EventScript_HideRifts\n'
          '\tcall_if_unset FLAG_SPACETIME_LAKES_SCENE, SpacetimeCave_EventScript_HideLakes\n'
          '\tcall Spacetime_AllSidequestsDone\n'
          '\tcall_if_eq VAR_RESULT, TRUE, SpacetimeCave_EventScript_OpenGateUnknown\n'
          '\tcall_if_set FLAG_SPACETIME_YOSHI_DONE, SpacetimeCave_EventScript_OpenGateYoshi\n'
          '\tgetcaughtmon SPECIES_GIRATINA\n'
          '\tcall_if_ne VAR_RESULT, 0, SpacetimeCave_EventScript_OpenGateGiratina\n'
          '\tend\n\n'
          'SpacetimeCave_OnTransition:\n'
          '\tcall_if_unset FLAG_SPACETIME_RIFTS_OPENED, SpacetimeCave_EventScript_ArmScene\n'
          '\tcall_if_set FLAG_SPACETIME_LAKES_SCENE, SpacetimeCave_EventScript_DisarmLakes\n\tend\n\n'
          'SpacetimeCave_EventScript_ArmScene:\n\tsetvar VAR_TEMP_1, 1\n\treturn\n\n'
          'SpacetimeCave_EventScript_DisarmLakes:\n\tsetvar VAR_TEMP_2, 1\n\treturn\n\n'
          'SpacetimeCave_OnFrame:\n\tmap_script_2 VAR_TEMP_1, 1, SpacetimeCave_EventScript_FirstVisit\n\t.2byte 0\n\n'
          'SpacetimeCave_EventScript_HideRifts:\n' + ''.join(hide) + '\treturn\n\n'
          'SpacetimeCave_EventScript_OpenRifts:\n' + ''.join(opened) + '\treturn\n\n'
          'SpacetimeCave_EventScript_HideLakes:\n' + setm(lake_floor) + '\treturn\n\n'
          'SpacetimeCave_EventScript_OpenLakes:\n' + setm(lake_open) + '\treturn\n\n'
          'SpacetimeCave_EventScript_OpenGateUnknown:\n' + setm(open_cells('Unknown')) + '\treturn\n\n'
          'SpacetimeCave_EventScript_OpenGateYoshi:\n' + setm(open_cells('Yoshi')) + '\treturn\n\n'
          'SpacetimeCave_EventScript_OpenGateGiratina:\n' + setm(open_cells('Giratina')) + '\treturn\n')
    # de scene van het eerste bezoek
    S.raw(f'''{P}FirstVisit::
	lockall
	setvar VAR_TEMP_1, 0
	applymovement OBJ_EVENT_ID_PLAYER, {P}Movement_PlayerIn
	waitmovement 0
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox {T_}Dialga1, MSGBOX_DEFAULT
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox {T_}Palkia1, MSGBOX_DEFAULT
	msgbox {T_}Dialga2, MSGBOX_DEFAULT
	msgbox {T_}Palkia2, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	waitmoncry
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 4
	special ShakeCamera
	waitstate
	waitmoncry
	playse SE_M_DETECT
	fadescreenspeed FADE_TO_WHITE, 2
	call SpacetimeCave_EventScript_OpenRifts
	special DrawWholeMapView
	removeobject LOCALID_SPACETIME_DIALGA
	removeobject LOCALID_SPACETIME_PALKIA
	setflag FLAG_SPACETIME_RIFTS_OPENED
	delay 20
	fadescreenspeed FADE_FROM_WHITE, 4
	playse SE_M_TELEPORT
	msgbox {T_}RiftsOpen, MSGBOX_DEFAULT
	releaseall
	end

{P}Movement_PlayerIn:
	walk_down
	walk_down
	walk_down
	step_end
''', [('Dialga1', "DIALGA: ...Finally.\n\nDo you know how long we have been waiting for you? I do. Exactly. "
                  "Down to the nanosecond. I am time. It's a whole thing."),
      ('Palkia1', "PALKIA: Don't mind him. He counts.\n\nWelcome to the space between spaces. Mind the "
                  "edges. They're sharp, and some of them are Tuesdays."),
      ('Dialga2', "DIALGA: Every tear in this cave leads to a place that went wrong. Another dimension. "
                  "Another time. Usually both.\n\nGo and fix them. We would do it ourselves, but we are "
                  "very large and very busy."),
      ('Palkia2', "PALKIA: The passage to the south stays shut until every one of these is fixed.\n\n"
                  "What's down there? Ask again later. Ideally much later. Ideally never."),
      ('RiftsOpen', "The cave tore open in six places at once!\n\nDIALGA and PALKIA are gone. The passage "
                    "to the south is still a wall of folded spacetime.")])
    # de poorten (bordjes op de instabiele wanden en de doodlopende rand)
    for key, (gx, gy) in (('Unknown', GATE_UNKNOWN), ('Yoshi', GATE_YOSHI)):
        for q in range(4):
            bgs.append(sign(gx + q % 2, gy + q // 2, P + 'Gate' + key))
    S.raw(f'''{P}GateUnknown::
	lockall
	call Spacetime_AllSidequestsDone
	goto_if_eq VAR_RESULT, TRUE, {P}GateEnd
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox {T_}GateUnknown, MSGBOX_DEFAULT
	releaseall
	end

{P}GateYoshi::
	lockall
	goto_if_set FLAG_SPACETIME_YOSHI_DONE, {P}GateEnd
	msgbox {T_}GateYoshi, MSGBOX_DEFAULT
	releaseall
	end

{P}GateEnd::
	releaseall
	end

{P}Inscription::
	lockall
	getcaughtmon SPECIES_GIRATINA
	goto_if_ne VAR_RESULT, 0, {P}GateEnd
	msgbox {T_}Inscription, MSGBOX_DEFAULT
	releaseall
	end
''', [('GateUnknown', "The passage is blocked by a wall of folded spacetime. It flickers between 'rock', "
                      "'not rock' and 'error'.\n\nIt won't settle until the rifts upstairs are fixed. "
                      "{STR_VAR_1} to go."),
      ('GateYoshi', "Another fold in spacetime. This one smells faintly of fruit and is humming a jaunty "
                    "tune.\n\nWhatever went wrong behind the ????? rift has to be put right first."),
      ('Inscription', "Words are carved into the dead end, upside down and back to front:\n\n"
                      "'WHERE THE SKY PILLAR STANDS ON ITS HEAD, THE ONE WHO WAS BANISHED HOLDS THE DOOR. "
                      "BRING IT ALONG, AND THE WALL WILL REMEMBER IT WAS NEVER A WALL.'")])
    for x in (CX, CX + 1):
        bgs.append(sign(x, DEAD_END, P + 'Inscription'))
    # de portalen in de diepte (nog geen warp)
    for key, (x0, y0), room in PORTALS:
        for q in range(4):
            bgs.append(sign(x0 + q % 2, y0 + q // 2, P + 'Portal' + key))
    S.raw(f'''{P}PortalUnknown::
	lockall
	playse SE_M_TELEPORT
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 1
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	msgbox {T_}PortalUnknown, MSGBOX_DEFAULT
	releaseall
	end
''', [('PortalUnknown', "You reach into the ????? rift...\n\nSomething grabs your sleeve. A small hand. "
                        "In a mask. It pulls, the rift hiccups, and spits you straight back out.\n\n"
                        "Something went wrong. Spacetime says: island not found. Try again in a later version "
                        "of reality.")])
    S.npc('PortalAcuity', "Snow blows out of this portal, and the cold has a voice. It is thinking about you. "
          "It knows things.\n\nLAKE ACUITY. The ice on the other side is still being installed.", 'MSGBOX_SIGN')
    S.npc('PortalValor', "Behind this portal: a calm lake, and a cave in the middle of it, and something in "
          "the cave that is very brave from a safe distance.\n\nLAKE VALOR. Not open yet.", 'MSGBOX_SIGN')
    S.npc('PortalVerity', "A lake, warm and still. Someone over there is feeling a lot of feelings, on your "
          "behalf.\n\nLAKE VERITY. Under construction. The feelings are not.", 'MSGBOX_SIGN')
    S.npc('PortalCoronet', "The last portal. Behind it, a mountain climbs out of the top of the world.\n\n"
          "MT. CORONET. You can hear it breathing. It isn't ready for you. Possibly the other way round.",
          'MSGBOX_SIGN')
    # meren-kamer: Dialga en Palkia channelen weer
    S.raw(f'''{P}LakesScene::
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, {P}Movement_LakesIn
	waitmovement 0
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox {T_}LakesPalkia1, MSGBOX_DEFAULT
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox {T_}LakesDialga1, MSGBOX_DEFAULT
	msgbox {T_}LakesPalkia2, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	waitmoncry
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 4
	special ShakeCamera
	waitstate
	waitmoncry
	playse SE_M_DETECT
	fadescreenspeed FADE_TO_WHITE, 2
	call SpacetimeCave_EventScript_OpenLakes
	special DrawWholeMapView
	removeobject LOCALID_SPACETIME_LAKES_DIALGA
	removeobject LOCALID_SPACETIME_LAKES_PALKIA
	setflag FLAG_SPACETIME_LAKES_SCENE
	setvar VAR_TEMP_2, 1
	delay 20
	fadescreenspeed FADE_FROM_WHITE, 4
	playse SE_M_TELEPORT
	msgbox {T_}LakesOpen, MSGBOX_DEFAULT
	releaseall
	end

{P}Movement_LakesIn:
	walk_down
	step_end
''', [('LakesPalkia1', "PALKIA: You again. Good. We were starting to think the island ate you.\n\n"
                       "It does that. It's very round and very hungry."),
      ('LakesDialga1', "DIALGA: Listen. Something is coming. Not today. Not in any time I'd call 'soon'. "
                       "But it is coming, in every dimension at once.\n\nWe cannot stop it. We are space and "
                       "time. It is the kind of problem that needs a brain, a heart and a spine."),
      ('LakesPalkia2', "PALKIA: Three of them. KNOWLEDGE, EMOTION, WILLPOWER. They sleep in three lakes.\n\n"
                       "Go wake them up. Be polite. The last person who wasn't lost their memory, their "
                       "feelings, and their car keys."),
      ('LakesOpen', "Three portals tore open: LAKE ACUITY, LAKE VALOR and LAKE VERITY!\n\nDIALGA and PALKIA "
                    "are gone again. They really do love an exit.")])
    coords = [{'type': 'trigger', 'x': x, 'y': DEEP_ROOMS['Lakes'][1], 'elevation': 3, 'var': 'VAR_TEMP_2',
               'var_value': '0', 'script': P + 'LakesScene'} for x in (CX, CX + 1)]
    # bordje en de onderzoeker (telt mee met de quest-poort)
    bgs.append(sign(10, 3, P + 'Plaque'))
    S.npc('Plaque', "SPACETIME CAVE\n\nWhere places that no longer exist, never existed, or are in another "
          "cartridge go to wait.\n\nPlease do not feed the timelines.", 'MSGBOX_SIGN')
    objs = [obj('OBJ_EVENT_GFX_SCIENTIST_1', HUB_RESEARCHER[0], HUB_RESEARCHER[1], P + 'Researcher',
                move='MOVEMENT_TYPE_FACE_DOWN'),
            obj('OBJ_EVENT_GFX_SPECIES(DIALGA)', HUB_DIALGA[0], HUB_DIALGA[1], '0x0', 'FLAG_SPACETIME_RIFTS_OPENED',
                move='MOVEMENT_TYPE_FACE_UP', local_id='LOCALID_SPACETIME_DIALGA'),
            obj('OBJ_EVENT_GFX_SPECIES(PALKIA)', HUB_PALKIA[0], HUB_PALKIA[1], '0x0', 'FLAG_SPACETIME_RIFTS_OPENED',
                move='MOVEMENT_TYPE_FACE_UP', local_id='LOCALID_SPACETIME_PALKIA'),
            obj('OBJ_EVENT_GFX_SPECIES(DIALGA)', LAKES_DIALGA[0], LAKES_DIALGA[1], '0x0', 'FLAG_SPACETIME_LAKES_SCENE',
                move='MOVEMENT_TYPE_FACE_UP', local_id='LOCALID_SPACETIME_LAKES_DIALGA'),
            obj('OBJ_EVENT_GFX_SPECIES(PALKIA)', LAKES_PALKIA[0], LAKES_PALKIA[1], '0x0', 'FLAG_SPACETIME_LAKES_SCENE',
                move='MOVEMENT_TYPE_FACE_UP', local_id='LOCALID_SPACETIME_LAKES_PALKIA')]
    S.raw(f'''{P}Researcher::
	lock
	faceplayer
	call Spacetime_AllSidequestsDone
	goto_if_eq VAR_RESULT, TRUE, {P}ResearcherDone
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox {T_}Researcher, MSGBOX_DEFAULT
	release
	end

{P}ResearcherDone::
	msgbox {T_}ResearcherDone, MSGBOX_DEFAULT
	release
	end
''', [('Researcher', "Did you SEE that? Two gods, one cave, zero safety briefings.\n\nI study the rifts. "
                     "The far left one leads to a haunted town. The one below it smells like a very angry "
                     "clone.\n\nMy instruments say {STR_VAR_1} of the working rifts still need you before the "
                     "passage to the south unfolds."),
      ('ResearcherDone', "Every working rift is quiet. You did that.\n\nThe passage to the south has "
                         "unfolded. Something down there is humming. I liked the screaming better. You knew "
                         "where you stood.")])
    S.write()
    cells = [c for row in gc for c in row]
    lay = save_layout(HUB, HUB_W, HUB_H, cells, [T(0x211, True, 0)] * 4, 'gTileset_SpacetimeGeneral',
                      'gTileset_SpacetimeCave')
    write_map(HUB, lay, objs, warps, bgs, coords, music='MUS_RG_SEVII_DUNGEON',
              region_map_section='MAPSEC_SPACETIME_CAVE')
    return g, gc


# ====================================================================== 2. Route 125: eilandje met grotopening
ROUTE125_DOOR = (45, 28)
ROUTE125_WARP = None


ISLE = dict(ring=(39, 22, 51, 31), sand=(40, 23, 50, 30), rock=(42, 25))
# S2 (Jordi: opening leek bovenaan afgekapt): rotsheuvel met grot exact uit vanilla overgenomen, geen eigen hoeken.
# Rij 0 = de top van Route 111 (080 081 0a4, ook op zand), rij 1-3 = de rots met grotopening van SkyPillar_Outside
# (17,13); daar staat rechtsboven een Pacifidlog-tegel (2b8), hier 0a4 zoals in Route 111 (0a4 rechts van 075 en
# boven 08a). None = zand. De opening (064 boven 0a7) is dicht tot de Hall of Fame: 07c boven 0a9.
ROCK_HILL = [[None, 0x080, 0x081, 0x081, 0x081, 0x0a4, None],
             [0x080, 0x073, 0x071, 0x071, 0x071, 0x075, 0x0a4],
             [0x088, 0x07b, 0x07c, 0x064, 0x07c, 0x07d, 0x08a],
             [0x090, 0x0a9, 0x0a9, 0x0a7, 0x0a9, 0x0a9, 0x092]]
ROCK_CLOSED = {(3, 2): 0x07c, (3, 3): 0x0a9}
ROCK_OPEN = {(3, 2): 0x064, (3, 3): 0x0a7}


def route125_island():
    """Eilandje met rotsheuvel (General-tegels op zand): ondiepe rand -> strand -> zand -> rots met grotopening."""
    p = 'data/layouts/Route125/map.bin'
    W, H = 80, 40
    v = list(struct.unpack('<%dH' % (W * H), open(p, 'rb').read()))

    def put(x, y, m, col=False, elev=3):
        v[y * W + x] = T(m, col, elev)

    def rect(box, nine, col=False, elev=3):
        x0, y0, x1, y1 = box
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                r = 0 if y == y0 else 2 if y == y1 else 1
                c = 0 if x == x0 else 2 if x == x1 else 1
                put(x, y, nine[r][c], col, elev)
    rect(ISLE['ring'], [[0x1ad, 0x1ae, 0x1af], [0x1b5, 0x19e, 0x1b7], [0x1bd, 0x1be, 0x1bf]], elev=1)
    rect(ISLE['sand'], [[0x195, 0x196, 0x197], [0x19d, 0x124, 0x19f], [0x1a5, 0x1a6, 0x1a7]])
    rx, ry = ISLE['rock']
    for dy, row in enumerate(ROCK_HILL):
        for dx, m in enumerate(row):
            if m is not None:
                m = ROCK_CLOSED.get((dx, dy), m)
                put(rx + dx, ry + dy, m, True)
    assert ROUTE125_DOOR == (rx + 3, ry + 3)
    open(p, 'wb').write(struct.pack('<%dH' % len(v), *v))


def route125():
    global ROUTE125_WARP
    route125_island()
    p = 'data/maps/Route125/map.json'
    m = json.load(open(p))
    dm = 'MAP_' + const(HUB)
    if not any(w['dest_map'] == dm for w in m['warp_events']):
        m['warp_events'].append({'x': ROUTE125_DOOR[0], 'y': ROUTE125_DOOR[1], 'elevation': 3, 'dest_map': dm,
                                 'dest_warp_id': '0'})
    for w in m['warp_events']:
        if w['dest_map'] == dm:
            w['x'], w['y'] = ROUTE125_DOOR
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    ROUTE125_WARP = [i for i, w in enumerate(m['warp_events']) if w['dest_map'] == dm][0]
    s = open('data/maps/Route125/scripts.inc').read()
    line = '\tcall_if_set FLAG_SYS_GAME_CLEAR, Route125_EventScript_OpenSpacetimeCave\n'
    if line not in s:
        s = s.replace('Route125_OnLoad:\n', 'Route125_OnLoad:\n' + line, 1)
    blk = ('@ --- spacetime_cave (tools/grounded/maptools/spacetime_cave.py) ---\n'
           '@ Project Grounded: na de Hall of Fame een grotopening in het rotsje op het eilandje (Spacetime Cave)\n'
           'Route125_EventScript_OpenSpacetimeCave::\n'
           + ''.join('\tsetmetatile %d, %d, 0x%03X, %s\n' % (ISLE['rock'][0] + dx, ISLE['rock'][1] + dy, m,
                                                             'FALSE' if m == 0x0A7 else 'TRUE')
                     for (dx, dy), m in sorted(ROCK_OPEN.items()))
           + '\treturn\n@ --- einde spacetime_cave ---')
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
    # gaten tussen de gebouwen (FRLG-huizen waren 5 breed): bloemen (na de bevrijding) of graven (spookstad)
    FLOWERS = [(x, y) for (x, y) in ((8, 8), (8, 9), (8, 10), (8, 11), (3, 13), (8, 13), (8, 14), (8, 15), (3, 14),
                                     (4, 1), (4, 2), (4, 3), (4, 4), (4, 5)) if kind[(x, y)] == 'grass']
    gH = [row[:] for row in g]                     # spookstad
    gC = [row[:] for row in g]                     # na de bevrijding
    grave = lambda i: T(names[('grave_orange', 'grave_gray')[i % 2]], True)
    for i, (x, y) in enumerate(FLOWERS):
        gC[y][x] = T(0x004)
        gH[y][x] = grave(i) if i % 2 == 0 else T(0x001)
    for i, (x, y) in enumerate(LAV_GRAVES):        # graven blijven: dit is nog steeds de stad van de doden
        assert kind[(x, y)] == 'grass', (x, y)
        gH[y][x] = gC[y][x] = grave(i + 1)
    for (x, y, t, keep) in LAV_DEADTREES:          # dode bomen (1x2); 'keep' = ook na de bevrijding (uitgangen dicht)
        assert kind[(x, y)] == kind[(x, y + 1)] == 'grass', (x, y)
        for r in range(2):
            gH[y + r][x] = T(names[('deadtree', t, r)], True)
            gC[y + r][x] = gH[y + r][x] if keep else T((0x001, 0x004)[r])
    border = [T(0x1d4, True, 0), T(0x1d5, True, 0), T(0x1dc, True, 0), T(0x1dd, True, 0)]
    lay = save_layout(LAV, W, H, [c for row in gH for c in row], border, 'gTileset_LavenderHauntGeneral',
                      'gTileset_LavenderHaunt')
    save_layout(LAV_CALM, W, H, [c for row in gC for c in row], border, 'gTileset_LavenderCalmGeneral',
                'gTileset_LavenderCalm')
    warps = [warp(x, y, const(dest), 0, elev=3) for x, y, dest in LAV_DOORS]
    warps[2]['dest_warp_id'] = '1'                 # torendeur -> de mat in 1F (FRLG: warp 1)
    first_rift = len(warps)
    for q in range(2):
        warps.append(warp(LAV_RIFT[0] + q, LAV_RIFT[1], const(HUB), 1 + q, elev=3))
    head = ('@ Project Grounded: LavenderTown (tools/grounded/maptools/spacetime_cave.py)\n'
            '@ Spookstad (eigen paletten, bewolkt) tot FLAG_SPACETIME_LAVENDER_DONE; daarna layout LavenderTown_Calm.\n'
            'LavenderTown_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, LavenderTown_OnTransition\n\t.byte 0\n\n'
            'LavenderTown_OnTransition:\n\tcall_if_set FLAG_SPACETIME_LAVENDER_DONE, LavenderTown_EventScript_Calm\n\tend\n\n'
            'LavenderTown_EventScript_Calm:\n\tsetmaplayoutindex LAYOUT_%s\n\tsetweather WEATHER_NONE\n' % const(LAV_CALM)
            + ''.join('\tsetflag FLAG_HIDE_LAVENDER_GHOST_%s\n' % g[0] for g in LAV_GHOSTS) + '\treturn\n')
    S = Scr(LAV, head)
    P = S.P
    objs = [
        obj('OBJ_EVENT_GFX_LITTLE_GIRL', 19, 10, P + 'LittleGirl', move='MOVEMENT_TYPE_WANDER_AROUND', rx=1, ry=1),
        obj('OBJ_EVENT_GFX_MAN_1', 12, 12, P + 'Worker', move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_BOY_1', 10, 6, P + 'Boy', move='MOVEMENT_TYPE_WANDER_UP_AND_DOWN', ry=1),
    ]

    def two(key, before, after):
        S.raw(f'{P}{key}::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_SPACETIME_LAVENDER_DONE, {P}{key}After\n'
              f'\tmsgbox {S.T}{key}, MSGBOX_DEFAULT\n\trelease\n\tend\n\n'
              f'{P}{key}After::\n\tmsgbox {S.T}{key}After, MSGBOX_DEFAULT\n\trelease\n\tend\n',
              [(key, before), (key + 'After', after)])
    two('LittleGirl', "Do you believe in ghosts?\n\nMy mom says they're just POKéMON. My dad says they're just "
        "POKéMON with unfinished business.\n\nThe one in front of the TOWER has a LOT of unfinished business.",
        "The bad ghosts are gone! Now it's just the regular ghosts.\n\nThe regular ghosts are fine. They do "
        "the dishes. Badly. But they do them.")
    two('Worker', "We were going to renovate the TOWER. Then the fog rolled in and Kanto just... stopped "
        "updating.\n\nI've been on lunch break for twenty-five years. The CHANNELERS went up to pray and came "
        "down wrong.",
        "The fog's gone. I can see the TOWER again.\n\nI suppose this means my lunch break is over. "
        "...I'll start tomorrow. Tomorrows work again here, apparently.")
    two('Boy', "You came out of the purple hole! Cool!\n\nThe last person who came out of it was a grumpy kid "
        "with spiky hair. He saw the fog, said 'smell ya never' and went straight back in.",
        "You beat the evil ghost! Cool!\n\nWhen the grumpy kid comes back, I'm telling him it was me.")
    # kwade geesten in de stad (wild gevecht; gewonnen of gevangen = weg)
    for gk, species, lvl, (gx, gy), face, txt in LAV_GHOSTS:
        flag = 'FLAG_HIDE_LAVENDER_GHOST_' + gk
        lid = 'LOCALID_LAVENDER_GHOST_' + gk
        # S2: in de overworld het Gen 1-GHOST; zonder Silph Scope ook in het gevecht (src/gen1_ghost.c)
        objs.append(obj('OBJ_EVENT_GFX_GEN1_GHOST', gx, gy, P + 'Ghost' + gk.title(), flag,
                        move='MOVEMENT_TYPE_FACE_' + face, local_id=lid))
        S.raw(f'''{P}Ghost{gk.title()}::
	lock
	faceplayer
	playmoncry SPECIES_{gk}, CRY_MODE_ENCOUNTER
	checkitem ITEM_SILPH_SCOPE
	goto_if_eq VAR_RESULT, FALSE, {P}Ghost{gk.title()}NoScope
	msgbox {S.T}Ghost{gk.title()}, MSGBOX_DEFAULT
	goto {P}Ghost{gk.title()}Fight

{P}Ghost{gk.title()}NoScope::
	msgbox {S.T}GhostNoScope, MSGBOX_DEFAULT
{P}Ghost{gk.title()}Fight::
	waitmoncry
	closemessage
	setwildbattle SPECIES_{species}, {lvl}
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}Ghost{gk.title()}Gone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}Ghost{gk.title()}Gone
	release
	end

{P}Ghost{gk.title()}Gone::
	removeobject {lid}
	msgbox {S.T}GhostGone, MSGBOX_DEFAULT
	release
	end
''', [('Ghost' + gk.title(), txt)])
    S.raw('', [('GhostGone', "The shadow dissolved into the fog.\n\nSomewhere, a door creaks shut. "
                             "Probably for the better."),
               ('GhostNoScope', "A GHOST! A grinning shadow with too many opinions about you.\n\nDarn! "
                                "The GHOST can't be ID'd. Somebody in this town used to sell SILPH SCOPES.")])
    bgs = [sign(15, 11, P + 'TownSign'), sign(21, 7, P + 'TowerSign'), sign(7, 11, P + 'HouseSign'),
           sign(12, 4, P + 'Notice')]
    S.npc('TownSign', "LAVENDER TOWN\nThe Noble Purple Town\n\n(Population: fluctuating. Please count "
          "yourself twice to be sure.)", 'MSGBOX_SIGN')
    S.npc('TowerSign', "POKéMON TOWER\nBecalm the spirits of POKéMON\n\nNo running. No flash photography. "
          "No asking the CHANNELERS if they're okay. They are not.", 'MSGBOX_SIGN')
    S.npc('HouseSign', "VOLUNTEER POKéMON HOUSE\n\nAll POKéMON welcome. Ghosts by appointment.", 'MSGBOX_SIGN')
    S.npc('Notice', "NOTICE\n\nSILPH SCOPES are sold out. Until further notice, assume every shadow is a "
          "GHOST, and every GHOST is in a mood.", 'MSGBOX_SIGN')
    S.write()
    write_map(LAV, lay, objs, warps, bgs, music='MUS_RG_LAVENDER', region_map_section='MAPSEC_LAVENDER_TOWN',
              map_type='MAP_TYPE_TOWN', weather=LAV_WEATHER, allow_cycling=True, allow_escaping=False)
    return first_rift, kind


LAV_WEATHER = 'WEATHER_SHADE'   # mist (horizontaal of diagonaal) maakte de donkere paletten melkwit
LAV_CALM = 'LavenderTown_Calm'
LAV_GRAVES = [(14, 13), (16, 13), (14, 15), (2, 6), (2, 8), (8, 0), (10, 0), (12, 0), (0, 9), (0, 10), (0, 11)]
LAV_DEADTREES = [(9, 0, 0, True), (11, 0, 1, True), (1, 5, 1, False), (21, 9, 0, False), (13, 13, 1, False),
                 (1, 14, 0, False)]
LAV_GHOSTS = [  # (soort-/sleutel, gevecht, level, plek, kijkrichting, tekst met Silph Scope)
    ('GENGAR', 'GENGAR', 67, (18, 7), 'DOWN', "A GHOST is blocking the TOWER door.\n\nThrough the SILPH SCOPE "
     "it's a GENGAR, and its grin is about three teeth too wide."),
    ('DUSKNOIR', 'DUSKNOIR', 66, (10, 1), 'DOWN', "The road north is gone. There's only fog, and a GHOST in the "
     "fog.\n\nThe SILPH SCOPE says DUSKNOIR. The DUSKNOIR says nothing. It just keeps looking."),
    ('BANETTE', 'BANETTE', 66, (2, 10), 'RIGHT', "A GHOST at the edge of town. Through the SILPH SCOPE: a "
     "BANETTE, zipping and unzipping its mouth.\n\nIt seems to be waiting for its old trainer. You'll do.")]


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
        # S1: geen Protip Oracle (Hoenn-gag) in een andere dimensie: een Kanto-verkoper van Silph Scopes
        'Text_ProtipMaster': "I used to sell SILPH SCOPES. Lovely things. You look through one and the ghosts "
                             "stop pretending.\n\nThen the fog came and nobody bought anything ever again. "
                             "Here. Last one. Take it before it starts haunting me too.",
    }, lambda o: [dict(x, graphics_id='OBJ_EVENT_GFX_GENTLEMAN') if 'Protip' in x['script'] else x for x in o])
    # S2: hij geeft je zijn laatste Silph Scope (zonder scope zijn de geesten in Lavender/de toren een Gen 1-GHOST)
    n = 'LavenderTown_PokemonCenter_1F'
    p = 'data/maps/%s/scripts.inc' % n
    sc = open(p).read()
    old = ('%s_EventScript_Protipmaster::\n\tlock\n\tfaceplayer\n\tmsgbox %s_Text_ProtipMaster, MSGBOX_NPC\n'
           '\trelease\n\tend\n' % (n, n))
    assert old in sc
    sc = sc.replace(old, f'''{n}_EventScript_Protipmaster::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_SILPH_SCOPE, {n}_EventScript_ScopeAfter
	msgbox {n}_Text_ProtipMaster, MSGBOX_DEFAULT
	giveitem ITEM_SILPH_SCOPE
	setflag FLAG_RECEIVED_SILPH_SCOPE
	msgbox {n}_Text_ScopeGiven, MSGBOX_DEFAULT
	release
	end

{n}_EventScript_ScopeAfter::
	msgbox {n}_Text_ScopeAfter, MSGBOX_DEFAULT
	release
	end
''')
    sc = sc.rstrip('\n') + '\n\n' + text(n + '_Text_ScopeGiven', "Look at a GHOST through it and you'll see what "
                                           "it really is.\n\nUsually something with too many teeth. No refunds. "
                                           "There's no shop left to refund it at.") + '\n' + \
        text(n + '_Text_ScopeAfter', "How's the SCOPE? Seen anything you can't unsee?\n\nGood. That means it works.")
    open(p, 'w').write(sc.rstrip('\n') + '\n')
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


TRAINERS = [  # S1: de Channelers zijn bezeten; teams: Ghost, Dark, Psychic en ander mysterieus spul (geen dubbele soort)
    ('TOWER_MAYA', 'PokemonTower_2F', 16, 5, 'LEFT', 3, 'MAYA', [
        mon('Mismagius', 65, ['Shadow Ball', 'Mystical Fire', 'Dazzling Gleam', 'Nasty Plot']),
        mon('Umbreon', 65, ['Foul Play', 'Moonlight', 'Toxic', 'Wish']),
        mon('Hypno', 65, ['Psychic', 'Hypnosis', 'Dream Eater', 'Focus Blast'])],
     "Hey! You're not dead! How refreshing.\n\nThe voice in my head says I should fix that. It's very "
     "persuasive. It has a podcast.",
     "The voice... stopped? Oh, thank goodness. It never let me pick the music.",
     "Something up there is wearing people like coats. I was a coat. Zero stars."),
    ('TOWER_PATRICIA', 'PokemonTower_3F', None, None, None, None, 'PATRICIA', [
        mon('Banette', 65, ['Shadow Claw', 'Gunk Shot', 'Knock Off', 'Shadow Sneak']),
        mon('Absol', 65, ['Night Slash', 'Psycho Cut', 'Sucker Punch', 'Swords Dance']),
        mon('Xatu', 65, ['Psychic', 'Air Slash', 'Roost', 'Confuse Ray'])],
     "Kekeke... ke... sorry. That's not my laugh. I don't know whose laugh that is.",
     "Kek. ...That one was mine. I think I'm back.",
     "The spirits say you'll go far. They said that about the last guy. He's in the third row."),
    ('TOWER_CARLY', 'PokemonTower_3F', None, None, None, None, 'CARLY', [
        mon('Dusclops', 65, ['Night Shade', 'Will-O-Wisp', 'Pain Split', 'Shadow Sneak']),
        mon('Mr. Mime', 65, ['Psychic', 'Dazzling Gleam', 'Reflect', 'Light Screen']),
        mon('Mandibuzz', 65, ['Foul Play', 'Roost', 'Brave Bird', 'Toxic'])],
     "Be gone... living... thing... You're warm. Stop being warm. It's rude.",
     "Ugh. I'm cold again. Normal cold. Human cold.",
     "I wear this robe because it's warm. The chanting was the ghost's idea."),
    ('TOWER_HOPE', 'PokemonTower_3F', None, None, None, None, 'HOPE', [
        mon('Chandelure', 66, ['Shadow Ball', 'Flamethrower', 'Energy Ball', 'Will-O-Wisp']),
        mon('Sableye', 66, ['Knock Off', 'Shadow Claw', 'Will-O-Wisp', 'Recover']),
        mon('Sigilyph', 66, ['Psychic', 'Air Slash', 'Cosmic Power', 'Roost'])],
     "My name is HOPE. The thing inside me finds that hilarious.",
     "And there it goes. Out through the ears, I think.",
     "Every grave here has a name on it. Except the ones that have two."),
    ('TOWER_LAUREL', 'PokemonTower_4F', None, None, None, None, 'LAUREL', [
        mon('Cofagrigus', 66, ['Shadow Ball', 'Will-O-Wisp', 'Trick Room', 'Nasty Plot']),
        mon('Malamar', 66, ['Psycho Cut', 'Knock Off', 'Superpower', 'Topsy-Turvy']),
        mon('Froslass', 66, ['Shadow Ball', 'Ice Beam', 'Spikes', 'Thunderbolt'])],
     "GHOST! Oh. No. That's my reflection. It's been doing things without me.",
     "My reflection is back to copying me. As it should.",
     "The tower used to be quiet. Then the fog came, and something moved into the top floor."),
    ('TOWER_JODY', 'PokemonTower_4F', None, None, None, None, 'JODY', [
        mon('Trevenant', 67, ['Wood Hammer', 'Shadow Claw', 'Horn Leech', 'Will-O-Wisp']),
        mon('Bronzong', 67, ['Gyro Ball', 'Psychic', 'Trick Room', 'Stealth Rock']),
        mon('Honchkrow', 67, ['Night Slash', 'Brave Bird', 'Sucker Punch', 'Heat Wave']),
        mon('Houndstone', 67, ['Shadow Claw', 'Play Rough', 'Body Press', 'Crunch'])],
     "I can see five spirits behind you. One of them is rolling its eyes. One of them is me.",
     "The eye-roller says 'told you so'. The me says 'sorry'.",
     "My HOUNDSTONE is a good boy. Was a good boy. Remains, technically, a good boy."),
    ('TOWER_PAULA', 'PokemonTower_4F', None, None, None, None, 'PAULA', [
        mon('Gourgeist', 66, ['Shadow Sneak', 'Seed Bomb', 'Will-O-Wisp', 'Leech Seed']),
        mon('Musharna', 66, ['Psychic', 'Moonblast', 'Yawn', 'Calm Mind']),
        mon('Grimmsnarl', 66, ['Spirit Break', 'Darkest Lariat', 'Thunder Wave', 'Bulk Up'])],
     "Shhh. You'll wake them. You'll wake ME. I'm not the one talking right now.",
     "...I'm awake. Thanks. I think.",
     "Please walk softly. Some of them are light sleepers. All of them are heavy grudge-holders."),
    ('TOWER_RUTH', 'PokemonTower_5F', None, None, None, None, 'RUTH', [
        mon('Polteageist', 68, ['Shadow Ball', 'Giga Drain', 'Shell Smash', 'Stored Power']),
        mon('Dhelmise', 68, ['Power Whip', 'Anchor Shot', 'Shadow Claw', 'Earthquake']),
        mon('Beheeyem', 68, ['Psychic', 'Shadow Ball', 'Thunderbolt', 'Trick Room']),
        mon('Zoroark-Hisui', 68, ['Shadow Ball', 'Hyper Voice', 'Nasty Plot', 'Flamethrower'])],
     "We are the CHOIR of the top floor. We sing for HER now.\n\nYou may join. Briefly. Permanently.",
     "That note was flat. And it was mine. I'm free!",
     "We don't actually sing. The acoustics up here are terrible. SHE made us."),
    ('TOWER_TAMMY', 'PokemonTower_5F', None, None, None, None, 'TAMMY', [
        mon('Dusknoir', 68, ['Shadow Punch', 'Earthquake', 'Ice Punch', 'Will-O-Wisp']),
        mon('Jellicent', 68, ['Scald', 'Shadow Ball', 'Recover', 'Will-O-Wisp']),
        mon('Alakazam', 68, ['Psychic', 'Shadow Ball', 'Focus Blast', 'Calm Mind']),
        mon('Spiritomb', 68, ['Sucker Punch', 'Shadow Sneak', 'Foul Play', 'Will-O-Wisp'])],
     "A hundred and eight spirits live in my SPIRITOMB. A hundred and nine live in me. It gets crowded. "
     "They vote on everything.",
     "The vote was unanimous. You win, and the hundred and ninth gets evicted.",
     "Upstairs is AGATHA. Or something that used to be AGATHA. She brought the fog."),
    ('TOWER_KARINA', 'PokemonTower_5F', None, None, None, None, 'KARINA', [
        mon('Gengar', 69, ['Shadow Ball', 'Sludge Bomb', 'Focus Blast', 'Hypnosis']),
        mon('Aegislash', 69, ["King's Shield", 'Shadow Ball', 'Flash Cannon', 'Sacred Sword']),
        mon('Mimikyu', 69, ['Play Rough', 'Shadow Claw', 'Swords Dance', 'Shadow Sneak']),
        mon('Marowak-Alola', 69, ['Shadow Bone', 'Flare Blitz', 'Bonemerang', 'Will-O-Wisp'])],
     "I lead the CHOIR. Or the thing behind my eyes does. It has terrible taste in hymns.",
     "...It's gone. My MAROWAK is staring at me like it knew all along.",
     "AGATHA is just ahead. The real one is still in there somewhere. Hit the other one first."),
]
# S1: extra trainers (eigen klasse/foto) met de id's uit de opdracht (1169, 1195-1199)
EXTRA = [  # (sleutel, id, kaart, naam, klasse, foto, geslacht, muziek, AI, mugshot, items, team, omschrijving)
    ('TOWER_AGATHA', 1169, 'PokemonTower_5F', 'AGATHA', 'Elite Four', 'Agatha', 'Female', 'Suspicious', bd.AI_BOSS,
     None, 'Full Restore / Full Restore', [
        mon('Crobat', 70, ['Cross Poison', 'Brave Bird', 'U-turn', 'Roost']),
        mon('Arbok', 70, ['Gunk Shot', 'Sucker Punch', 'Glare', 'Earthquake']),
        mon('Annihilape', 70, ['Rage Fist', 'Drain Punch', 'Bulk Up', 'Ice Punch']),
        mon('Typhlosion-Hisui', 70, ['Infernal Parade', 'Eruption', 'Focus Blast', 'Will-O-Wisp']),
        mon('Dragapult', 70, ['Dragon Darts', 'Phantom Force', 'U-turn', 'Will-O-Wisp']),
        mon('Gengar @ Life Orb', 71, ['Shadow Ball', 'Sludge Wave', 'Focus Blast', 'Nasty Plot'])],
     'Pokemon Tower 5F: bezeten Agatha (Lavender-quest)'),
    ('CC_GRUNT_ARLO', 1195, 'CeruleanCave_1F', 'ARLO', 'Team Rocket', 'Rocket Grunt M', 'Male', 'Rocket', bd.AI, None,
     None, [mon('Crobat', 66, ['Cross Poison', 'Air Slash', 'U-turn', 'Taunt']),
            mon('Weezing-Galar', 66, ['Strange Steam', 'Sludge Bomb', 'Will-O-Wisp', 'Defog']),
            mon('Houndoom', 66, ['Dark Pulse', 'Flamethrower', 'Sludge Bomb', 'Nasty Plot'])],
     'Cerulean Cave 1F: Rocket die Mewtwo zoekt'),
    ('CC_GRUNT_VERA', 1196, 'CeruleanCave_2F', 'VERA', 'Team Rocket', 'Rocket Grunt F', 'Female', 'Rocket', bd.AI, None,
     None, [mon('Arbok', 67, ['Gunk Shot', 'Crunch', 'Coil', 'Earthquake']),
            mon('Persian-Alola', 67, ['Foul Play', 'Power Gem', 'Nasty Plot', 'Dark Pulse']),
            mon('Toxicroak', 67, ['Poison Jab', 'Drain Punch', 'Sucker Punch', 'Swords Dance']),
            mon('Skuntank', 67, ['Crunch', 'Poison Jab', 'Fire Blast', 'Sucker Punch'])],
     'Cerulean Cave 2F: Rocket die Mewtwo zoekt'),
    ('CC_GRUNT_DUNCAN', 1197, 'CeruleanCave_2F', 'DUNCAN', 'Team Rocket', 'Rocket Grunt M', 'Male', 'Rocket', bd.AI,
     None, None, [mon('Scizor', 68, ['Bullet Punch', 'X-Scissor', 'Knock Off', 'Swords Dance']),
                  mon('Magnezone', 68, ['Thunderbolt', 'Flash Cannon', 'Volt Switch', 'Thunder Wave']),
                  mon('Drapion', 68, ['Knock Off', 'Poison Jab', 'Earthquake', 'Swords Dance'])],
     'Cerulean Cave 2F: Rocket die Mewtwo zoekt'),
    ('CC_GRUNT_MAXINE', 1198, 'CeruleanCave_B1F', 'MAXINE', 'Team Rocket', 'Rocket Grunt F', 'Female', 'Rocket', bd.AI,
     None, None, [mon('Porygon-Z', 69, ['Tri Attack', 'Thunderbolt', 'Ice Beam', 'Nasty Plot']),
                  mon('Muk', 69, ['Gunk Shot', 'Knock Off', 'Drain Punch', 'Curse']),
                  mon('Electivire', 69, ['Wild Charge', 'Ice Punch', 'Cross Chop', 'Earthquake']),
                  mon('Kingambit', 70, ['Kowtow Cleave', 'Iron Head', 'Sucker Punch', 'Swords Dance'])],
     'Cerulean Cave B1F: Rocket die Mewtwo zoekt'),
    ('CC_GIOVANNI', 1199, 'CeruleanCave_B1F', 'GIOVANNI', 'Boss', 'Giovanni', 'Male', 'Rocket', bd.AI_BOSS, 'Purple',
     'Full Restore / Full Restore', [
        mon('Honchkrow', 73, ['Night Slash', 'Brave Bird', 'Sucker Punch', 'Superpower']),
        mon('Dugtrio', 73, ['Earthquake', 'Stone Edge', 'Sucker Punch', 'Swords Dance']),
        mon('Kangaskhan', 73, ['Fake Out', 'Double-Edge', 'Sucker Punch', 'Earthquake']),
        mon('Nidoqueen', 74, ['Earth Power', 'Sludge Wave', 'Ice Beam', 'Flamethrower']),
        mon('Rhyperior @ Weakness Policy', 74, ['Rock Wrecker', 'High Horsepower', 'Megahorn', 'Rock Polish']),
        mon('Nidoking @ Life Orb', 75, ['Earth Power', 'Sludge Wave', 'Ice Beam', 'Thunderbolt'])],
     'Cerulean Cave B1F: Giovanni, vlak voor Mewtwo'),
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
            objs.append(obj('OBJ_EVENT_GFX_AGATHA', 11, 5, P + 'Agatha', move='MOVEMENT_TYPE_FACE_DOWN'))
            # S1: de baas van de Lavender-quest: de kwade geest in Agatha; daarna is Lavender bevrijd
            S.raw(f'''{P}Agatha::
	lock
	faceplayer
	goto_if_set FLAG_SPACETIME_LAVENDER_DONE, {P}AgathaFreed
	playse SE_M_NIGHTMARE
	msgbox {S.T}AgathaIntro, MSGBOX_DEFAULT
	trainerbattle_single TRAINER_TOWER_AGATHA, {S.T}AgathaBattle, {S.T}AgathaDefeat, {P}AgathaDefeated
{P}AgathaFreed::
	msgbox {S.T}AgathaFreed, MSGBOX_DEFAULT
	release
	end

{P}AgathaDefeated::
	msgbox {S.T}AgathaLeaves, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TELEPORT
	fadescreenspeed FADE_TO_WHITE, 4
	setflag FLAG_SPACETIME_LAVENDER_DONE
	setflag FLAG_HIDE_LAVENDER_GHOST_GENGAR
	setflag FLAG_HIDE_LAVENDER_GHOST_DUSKNOIR
	setflag FLAG_HIDE_LAVENDER_GHOST_BANETTE
	delay 30
	fadescreenspeed FADE_FROM_WHITE, 4
	msgbox {S.T}AgathaThanks, MSGBOX_DEFAULT
	msgbox {S.T}LavenderFreed, MSGBOX_DEFAULT
	release
	end
''', [('AgathaIntro', "AGATHA stands perfectly still. Her eyes are the wrong color.\n\n\"Oh, a visitor. How "
                      "lovely. This old body has a lot of fight left in it. I'm borrowing it.\""),
      ('AgathaBattle', "\"I made the fog. I made the CHANNELERS sing. I'll make you a GRAVE. A nice one. "
                       "Near the window.\""),
      ('AgathaDefeat', "\"Fine! FINE! There are other towns! Other dimensions!\""),
      ('AgathaLeaves', "Something black and screaming pours out of AGATHA and through the floor.\n\n"
                       "The whole TOWER sighs."),
      ('AgathaThanks', "AGATHA: ...Hm. Fifty years of training GHOSTS and one finally trains me.\n\n"
                       "Thank you, child. Now go away before I get sentimental. It's bad for my image."),
      ('LavenderFreed', "Far below, the fog over LAVENDER TOWN starts to lift."),
      ('AgathaFreed', "AGATHA: The town is quiet again. Quiet-quiet, not haunted-quiet.\n\n"
                      "If you see an old woman in a dimension that isn't this one, don't tell her about the "
                      "possession. She'd never let me hear the end of it.")])
            S.raw(f'''{P}Caretaker::
	lock
	faceplayer
	goto_if_unset FLAG_SPACETIME_LAVENDER_DONE, {P}CaretakerScared
	goto_if_set FLAG_RECEIVED_POKEMON_TOWER_LIFE_ORB, {P}CaretakerDone
	msgbox {S.T}CaretakerGift, MSGBOX_DEFAULT
	giveitem ITEM_LIFE_ORB
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_POKEMON_TOWER_LIFE_ORB
{P}CaretakerDone::
	msgbox {S.T}CaretakerDone, MSGBOX_DEFAULT
	release
	end

{P}CaretakerScared::
	msgbox {S.T}CaretakerScared, MSGBOX_DEFAULT
	release
	end
''', [('CaretakerScared', "Psst. Don't look at her. That's AGATHA. Was AGATHA.\n\nShe came up to deal "
                          "with the ghosts and the ghosts dealt with her. Now she's the reason for the fog."),
      ('CaretakerGift', "You climbed all the way up here? With the CHOIR and everything? And you got the thing "
                        "out of AGATHA?\n\nI'm the caretaker. MR. FUJI left me in charge when he went to find "
                        "himself. Twenty-five years ago.\n\nHere. Someone left this on a grave. It glows. "
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
MEWTWO_LVL = 75
GIOVANNI = (7, 14)      # S1: vlak voor Mewtwo, in de enige doorgang van het eilandje
CC_GRUNT_MAP = {'CC_GRUNT_ARLO': 'CeruleanCave_1F', 'CC_GRUNT_VERA': 'CeruleanCave_2F',
                'CC_GRUNT_DUNCAN': 'CeruleanCave_2F', 'CC_GRUNT_MAXINE': 'CeruleanCave_B1F'}
CC_GRUNTS = [  # (sleutel, x, y, kijkrichting, zicht, gfx, intro, verlies, na afloop)
    ('CC_GRUNT_ARLO', 33, 15, 'DOWN', 4, 'OBJ_EVENT_GFX_ROCKET_GRUNT_M',
     "Halt! This cave is property of TEAM ROCKET. Well. It will be. We're filling in the forms.",
     "The forms! You've ruined the forms!",
     "The BOSS says there's a POKéMON down here worth more than all of Kanto. I'm just here for the dental plan."),
    ('CC_GRUNT_VERA', 8, 6, 'LEFT', 4, 'OBJ_EVENT_GFX_ROCKET_GRUNT_F',
     "Another tourist from the purple hole? We already have a tourist. We put him in the lake.",
     "Okay, okay! You can stay out of the lake.",
     "We've been searching this cave for weeks. Every tunnel looks the same. I think the cave does it on purpose."),
    ('CC_GRUNT_DUNCAN', 6, 8, 'RIGHT', 5, 'OBJ_EVENT_GFX_ROCKET_GRUNT_M',
     "Shh! I'm listening for MEWTWO. It's psychic, so I'm trying very hard not to think.",
     "I thought about losing. And then I lost. It works!",
     "The BOSS is down below. He doesn't need us. He just likes an audience."),
    ('CC_GRUNT_MAXINE', 9, 5, 'RIGHT', 5, 'OBJ_EVENT_GFX_ROCKET_GRUNT_F',
     "I'm TEAM ROCKET's head of research. Our research says: you shouldn't be here.",
     "Peer review is brutal.",
     "We cloned it once. We can't even find it twice. Science is humbling."),
]


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
        # S1: Team Rocket zoekt Mewtwo
        for key, gx, gy, face, sight, gfx, intro, defeat, post in CC_GRUNTS:
            if CC_GRUNT_MAP[key] == name:
                objs.append(tr(gfx, gx, gy, S.trainer(key.split('_')[-1].title(), key, intro, defeat, post), face,
                               sight))
        if name == 'CeruleanCave_B1F':
            objs.insert(0, obj('OBJ_EVENT_GFX_SPECIES(MEWTWO)', MEWTWO[0], MEWTWO[1], P + 'Mewtwo',
                               'FLAG_HIDE_METEOR_FALLS_MEWTWO', local_id='LOCALID_CERULEAN_CAVE_MEWTWO'))
            gio = tr('OBJ_EVENT_GFX_GIOVANNI', GIOVANNI[0], GIOVANNI[1], P + 'Giovanni', 'DOWN', 1)
            gio['flag'] = 'TRAINER_FLAGS_START+TRAINER_CC_GIOVANNI'
            gio['local_id'] = 'LOCALID_CERULEAN_CAVE_GIOVANNI'
            objs.append(gio)
            S.raw(f"""{P}Giovanni::
	trainerbattle_single TRAINER_CC_GIOVANNI, {S.T}GiovanniIntro, {S.T}GiovanniDefeat, {P}GiovanniDefeated
	end

{P}GiovanniDefeated::
	msgbox {S.T}GiovanniLeaves, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_CERULEAN_CAVE_GIOVANNI
	fadescreen FADE_FROM_BLACK
	goto {P}MewtwoHeal

{P}Mewtwo::
	lock
	faceplayer
	goto {P}MewtwoHeal

{P}MewtwoHeal::
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	msgbox {S.T}Mewtwo, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	playse SE_M_PSYBEAM
	fadescreenspeed FADE_TO_WHITE, 4
	special HealPlayerParty
	fadescreenspeed FADE_FROM_WHITE, 4
	playfanfare MUS_HEAL
	waitfanfare
	msgbox {S.T}MewtwoHealed, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_MEWTWO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MEWTWO, {MEWTWO_LVL}
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}MewtwoStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}MewtwoStays
	removeobject LOCALID_CERULEAN_CAVE_MEWTWO
	setflag FLAG_HIDE_METEOR_FALLS_MEWTWO
	setflag FLAG_SPACETIME_CERULEAN_DONE
{P}MewtwoStays::
	release
	end
""", [('GiovanniIntro', "GIOVANNI: So. The child from the hole in the sky.\n\nIn this world, TEAM ROCKET "
                        "never fell. We simply ran out of things to steal. Then the cave started whispering "
                        "a name.\n\nMEWTWO was made by my people. I'm only collecting what's mine."),
      ('GiovanniDefeat', "...Impressive. Annoyingly so."),
      ('GiovanniLeaves', "GIOVANNI: Keep it, then. Every dimension has a GIOVANNI, and every GIOVANNI "
                         "learns to lose with dignity.\n\nMost of them. I'm one of the good ones.\n\n"
                         "TEAM ROCKET! We're leaving. Somebody fetch the van."),
      ('Mewtwo', "A voice echoes inside your head.\n\n\"He was right about one thing. I was made. I was not "
                 "made to be owned.\"\n\n\"You fought him for me, and your team is exhausted. I will not fight "
                 "an exhausted opponent. Where is the honor in that? Where is the CHALLENGE?\""),
      ('MewtwoHealed', "MEWTWO restored your POKéMON to full health!\n\n\"Now. Show me what you are worth.\"")])
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
    blk = '// spacetime_cave { (tools/grounded/maptools/spacetime_cave.py; id 1159-1169, 1195-1199)\n'
    ids = []
    for i, t in enumerate(TRAINERS):
        blk += '#define TRAINER_%-28s%d // Project Grounded: Pokemon Tower (Spacetime Cave), %s\n' % (t[0], FIRST_ID + i, t[6])
        ids.append(FIRST_ID + i)
    for key, n, mp, *_, why in EXTRA:
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (key, n, why)
        ids.append(n)
    blk += '// }'
    if '// spacetime_cave {' in s:
        i = s.index('// spacetime_cave {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for n in ids:
        hits = re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)
        assert len(hits) == 1, ('trainer-id dubbel', n, hits)
        assert n < 1200
    cnt = int(re.search(r'^#define TRAINERS_COUNT\s+(\d+)', s, re.M).group(1))
    if max(ids) + 1 > cnt:
        s = re.sub(r'^#define TRAINERS_COUNT\s+\d+', '#define TRAINERS_COUNT                      %d' % (max(ids) + 1),
                   s, flags=re.M)
    open(p, 'w').write(s)
    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- spacetime_cave (tools/grounded/maptools/spacetime_cave.py) --- */\n\n'
    for key, mp, x, y, face, sight, nm, team, *_ in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: Hex Maniac', 'Pic: Hex Maniac', 'Gender: Female', 'Music: Suspicious',
               'Double Battle: No', bd.AI]
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (key, '\n'.join(hdr), '\n\n'.join(team))
    for key, n, mp, nm, cls, pic, gender, music, ai, mug, items, team, why in EXTRA:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music]
        if items:
            hdr.append('Items: ' + items)
        hdr += ['Double Battle: No', ai]
        if mug:
            hdr.append('Mugshot: ' + mug)
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
    line2 = ('- **Dode bomen in Lavender Town** (spookstad): **Ekat99**, *Haunted Woods (Normal Pallet)* uit Ekat\'s Public '
             'Tiles (`graphics/grounded/tilesets/ekat/haunted_woods_deadtrees.png`); graven: Mt. Pyre (Emerald, Facility).\n')
    if 'Dode bomen in Lavender Town' not in s:
        anchor = '- **N** (trainerfoto en overworld)'
        s = s.replace(anchor, line2 + anchor, 1)
    open(p, 'w').write(s)


# ====================================================================== controles
def check():
    sys.modules.pop('landlib', None)
    ll = importlib.import_module('landlib')
    problems = []

    def reach_all(name, start, surf=False):
        k = ll.Kaart(name)
        solid = {(o['x'], o['y']) for o in k.d['object_events'] if 'BREAKABLE_ROCK' not in o['graphics_id']
                 and 'Ghost' not in o['script'] and 'Giovanni' not in o['script']} - {start}
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
