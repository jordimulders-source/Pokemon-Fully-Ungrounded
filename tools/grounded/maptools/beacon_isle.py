"""Project Grounded: Beacon Isle (vuurtoreneiland onder Route 133), de galerij bovenin de vuurtoren en het
Lichteiland met de grot van TALLOW. Deterministisch en idempotent (vaste seeds; draai opnieuw na een wijziging).
Afgesplitst uit beacon_dragon.py (dat doet nog de vuurtoren-tileset, vuurtoren 1F/2F, de Beacon-trainers, de wilde
tabel BEACON_ISLE en de mapsec; dit script gebruikt die hulpjes).

  BeaconIsle             32x48, General + Dewford. Onregelmatig eiland: een westlob met een baai en een houten
                         steiger (aanleggen vanaf het noorden), de vuurtoren op een rotspunt aan de oostkant, een
                         lobbige zuidkust. Onder het eiland een rif over de hele breedte (rij 33-34) met daarachter
                         het Lichteiland (het eilandje met de grot van Route 105, Island Cave).
                         Het rif heeft één vaste plek (x 14-15) die opengaat zodra de speler 's nachts de lamp
                         (LANTURN) bovenin de vuurtoren aanspreekt: FLAG_BEACON_LIGHT_ISLE_FOUND. Daarna blijft de
                         doorgang open (setmetatile in ON_LOAD); twee lichtjes markeren hem 's nachts.
  BeaconIsle_Lighthouse_Top
                         Galerij (kopie van het dak van het Lilycove-warenhuis), WICK en LANTURN.
  BeaconIsle_Grotto      De grot op het Lichteiland: de layout van Steven's kamer in Granite Cave, gedeeld (geen kopie).
                         Zeldzame wilde soorten (ONDERVERTEGENWOORDIGD.md) en de geest van de eerste vuurtorenwachter,
                         TALLOW (sterk gevecht, Battle Stadium-pool).

Teksten zijn placeholders in de huisstijl (Jordi herschrijft ze).
Gebruik: python3 tools/grounded/maptools/beacon_isle.py [rendermap]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, random, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beacon_dragon as bd          # zet ook de werkmap op de repo-root

sms, cx, oq, tc = bd.sms, bd.cx, bd.oq, bd.tc
t, mt, WATER, reach, val = bd.t, bd.mt, bd.WATER, bd.reach, bd.val
Scr, obj, tr, ball, light, sign, hidden, warp = bd.Scr, bd.obj, bd.tr, bd.ball, bd.light, bd.sign, bd.hidden, bd.warp
LH_DOOR, LW, LH = bd.LH_DOOR, bd.LW, bd.LH
DEBUG = os.environ.get('BD_DEBUG')

# ====================================================================== flags (FLAG_GROUNDED 400-429 = dit script)
FLAGS = [
    (400, 'FLAG_BEACON_LIGHT_ISLE_FOUND', "Beacon Isle: 's nachts de lamp aangesproken, rif naar het Lichteiland open"),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// beacon_isle { (tools/grounded/maptools/beacon_isle.py; FLAG_GROUNDED 400-429)\n'
    for n, name, why in FLAGS:
        assert 400 <= n <= 429
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// beacon_isle {' in s:
        i = s.index('// beacon_isle {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('\n', s.index('// Verdeling (houd bij!)')) + 1
        s = s[:anchor] + blk + '\n' + s[anchor:]
    open(p, 'w').write(s)


# ====================================================================== Beacon Isle
BW, BH = 32, 48
BEACON_OFFSET = 48                  # x van het eiland op Route 133
LX, LY = 24, 12                     # linkerbovenhoek van de vuurtoren (3x8 metatiles)
DOOR = (LX + LH_DOOR[0], LY + LH_DOOR[1])
SAFE_TOP = 9                        # bovenste rijen alleen primary (grens met Route 133, andere secondary)
REEF_GAP133 = (60, 61)              # geul in het rif onderaan Route 133 (lokaal x 12-13)
REEF_Y = 33                         # rif over de hele breedte (rijen 33-34), rotsen van 2x2
REEF_GAP = 14                       # rots x 14-15 gaat open
ISLET = (12, 38)                    # linkerbovenhoek van het Lichteiland (7x7, uit Route 105 x 6-12, y 17-23)
ISLET_SRC = ('Route105', 6, 17)
ISLET_DOOR = (ISLET[0] + 3, ISLET[1] + 3)
LH_GRID = []
PIER = (13, 17, 14)                 # steiger x 13-17 op rij 14 (palen op rij 15), vast aan de westlob

# landvormen per rij: (x0, x1) incl., meerdere stukken per rij mogelijk. Westlob + baai + rotspunt (oost) + zuidkust.
ROWS = {
    9: [(23, 27)],
    10: [(22, 28)],
    11: [(5, 9), (21, 29)],
    12: [(4, 11), (21, 29)],
    13: [(3, 12), (21, 30)],
    14: [(3, 12), (21, 30)],
    15: [(2, 12), (21, 30)],
    16: [(2, 12), (21, 29)],
    17: [(2, 13), (21, 29)],
    18: [(2, 29)],
    19: [(1, 28)],
    20: [(1, 28)],
    21: [(1, 28)],
    22: [(2, 27)],
    23: [(2, 26)],
    24: [(3, 26)],
    25: [(3, 24)],
    26: [(4, 17), (20, 23)],
    27: [(5, 16), (20, 22)],
    28: [(6, 15)],
    29: [(8, 13)],
}
TREES = [(6, 22), (10, 19), (15, 21), (19, 21), (4, 18)]
GRASS_PATCHES = [(6.5, 14.5, 2.4), (10, 25, 2.6)]


def open_reef133():
    """Route 133 heeft onderaan een rif; één zeerots (60-61, 36-37) gaat weg (vaargeul naar Beacon Isle)."""
    g = sms.read('Route133', 80, 40)
    x0, y0 = REEF_GAP133[0], 36
    rock = [mt(g[y0 + dy][x0 + dx]) for dy in (0, 1) for dx in (0, 1)]
    if rock == [WATER] * 4:
        return
    assert rock == [0x150, 0x151, 0x158, 0x159], [hex(m) for m in rock]
    water = g[35][x0]
    assert mt(water) == WATER and cx.walkable(water)
    for dy in (0, 1):
        for dx in (0, 1):
            g[y0 + dy][x0 + dx] = water
    sms.save(g, 'Route133')


def islet_cells():
    """Het eilandje met de grot van Route 105 (Island Cave): 7x7 cellen, de losse zeerotsen eromheen worden water."""
    src, sx, sy = ISLET_SRC
    L = bd.layout_of(src)
    g = oq.read_layout(L['blockdata_filepath'], L['width'], L['height'])
    out = {}
    for dy in range(7):
        for dx in range(7):
            v = g[sy + dy][sx + dx]
            if mt(v) in (0x175, 0x176, 0x17d, 0x17e):
                v = t(WATER, False, 1)
            out[(ISLET[0] + dx, ISLET[1] + dy)] = v
    assert mt(out[ISLET_DOOR]) == 0x0A7, 'deur van het eilandje niet gevonden'
    return out


def reef_cells():
    return {(x, y) for x in range(BW) for y in (REEF_Y, REEF_Y + 1)}


def beacon_isle():
    name, const = 'BeaconIsle', 'BEACON_ISLE'
    rng = random.Random(171)                        # nationaal dexnummer van Lanturn
    land = [[False] * BW for _ in range(BH)]
    for y, segs in ROWS.items():
        for x0, x1 in segs:
            for x in range(x0, x1 + 1):
                land[y][x] = True
    tc.smooth(land, 6)
    d = tc.dist_to_water(land)
    C = tc.Chars(BW, BH, '~')
    for y in range(BH):
        for x in range(BW):
            if land[y][x]:
                C.c[y][x] = 'S' if d[y][x] <= (2 if y >= 24 else 1) else 'g'   # brede zuidkust, smalle oevers
    # grasveld rond de vuurtoren (de onderlaag van de vuurtoren-metatiles is gras)
    for y in range(LY - 1, DOOR[1] + 2):
        for x in range(LX - 1, LX + LW + 1):
            assert land[y][x] and d[y][x] >= 2, ('vuurtoren te dicht bij het water', x, y)
            C.c[y][x] = 'g'
    for my in range(LH):
        for mx in range(LW):
            C.c[LY + my][LX + mx] = 'H'
    for cx_, cy_, r in GRASS_PATCHES:
        C.disc(cx_, cy_, r, 'L', only='g')
    for x, y in TREES:
        if all(C.c[y + dy][x + dx] == 'g' for dx in (0, 1) for dy in (0, 1)) and C.c[y - 1][x] == 'g' and C.c[y - 1][x + 1] == 'g':
            for dx in (0, 1):
                for dy in (0, 1):
                    C.c[y + dy][x + dx] = 'T'
        else:
            print('boom past niet op %s' % ((x, y),)) if DEBUG else None
            if not DEBUG: raise SystemExit('boom past niet op %s' % ((x, y),))
    for y in range(BH):
        for x in range(BW):
            if C.c[y][x] == 'g' and 2.5 <= ((x - DOOR[0]) ** 2 + ((y - DOOR[1]) * 1.2) ** 2) ** .5 <= 4.2 \
                    and rng.random() < 0.3 and y > DOOR[1]:
                C.c[y][x] = 'f'
    if DEBUG:
        print('\n'.join('%2d ' % y + ''.join(r) for y, r in enumerate(C.c)))

    g = [[0] * BW for _ in range(BH)]
    for y in range(BH):
        for x in range(BW):
            k = C.c[y][x]
            below = C.get(x, y + 1, '~')
            if k == '~':
                g[y][x] = t(WATER, False, 1)
            elif k == 'S':
                g[y][x] = tc.sand_tile(land, x, y)
            elif k == 'H':
                m_ = LH_GRID[y - LY][x - LX]
                g[y][x] = val(m_, 0 if (x, y) == DOOR else 1, 3 if (x, y) == DOOR else 0)
            elif k == 'T':
                g[y][x] = val(rng.choice(tc.TRUNK if below != 'T' else tc.FOREST), 1, 0)
            elif k == 'L':
                g[y][x] = val(0x00D, 0, 3)
            elif below == 'T':
                g[y][x] = val(rng.choice(tc.CANOPY), 0, 3)
            elif k == 'f':
                g[y][x] = val(tc.FLOWER, 0, 3)
            else:
                g[y][x] = val(tc.GRASS, 0, 3)
    # houten steiger (zoals Dewford: 0x228 begin, 0x229 planken, palen 0x230/0x231 eronder)
    x0, x1, py = PIER
    assert land[py][x0 - 1] and not any(land[py][x] or land[py + 1][x] or land[py - 1][x] for x in range(x0, x1 + 1))
    for x in range(x0, x1 + 1):
        g[py][x] = 0x3228 if x == x0 else 0x3229
        g[py + 1][x] = 0x0630 if x == x0 else 0x0631
    # rif over de hele breedte
    rr = random.Random(172)
    for x in range(0, BW, 2):
        r = rr.choice(tc.ROCKS)
        for k, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
            g[REEF_Y + dy][x + dx] = t(r[k], True, 1)
    gap_rock = [mt(g[REEF_Y + dy][REEF_GAP + dx]) for dy in (0, 1) for dx in (0, 1)]
    # het Lichteiland
    for (x, y), v in islet_cells().items():
        g[y][x] = v
    # losse zeerotsen: rond de rotspunt (de vuurtoren staat op de rotsen) en een paar elders, weg van de vaarroutes
    tc.place_rocks(g, 5, 173, lambda x, y: x >= 26 and 2 <= y <= 26)
    tc.place_rocks(g, 4, 174, lambda x, y: (x <= 8 and 5 <= y <= 30) or (y >= 37 and (x <= 8 or x >= 21)))

    S = Scr(name, '''@ Project Grounded: Beacon Isle, het vuurtoreneiland onder Route 133 (ZEE_PLAN.md).
@ Kaart en scripts: tools/grounded/maptools/beacon_isle.py. 's Nachts: CHINCHOU in het water (FLAG_TEMP_11
@ verbergt ze overdag) en het licht van de vuurtoren (lichtobjecten). Het rif onderaan (rij 33-34) gaat op x 14-15
@ open zodra de speler 's nachts de lamp bovenin heeft aangesproken (FLAG_BEACON_LIGHT_ISLE_FOUND); daarachter het
@ Lichteiland met de grot van TALLOW. Teksten zijn placeholders.
BeaconIsle_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, BeaconIsle_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, BeaconIsle_OnTransition
	.byte 0

BeaconIsle_OnLoad:
	goto_if_unset FLAG_BEACON_LIGHT_ISLE_FOUND, BeaconIsle_EventScript_End
	setmetatile %d, %d, METATILE_General_CalmWater, FALSE
	setmetatile %d, %d, METATILE_General_CalmWater, FALSE
	setmetatile %d, %d, METATILE_General_CalmWater, FALSE
	setmetatile %d, %d, METATILE_General_CalmWater, FALSE
BeaconIsle_EventScript_End:
	end

BeaconIsle_OnTransition:
	call_if_unset FLAG_BEACON_LIGHT_ISLE_FOUND, BeaconIsle_EventScript_HideGuideLights
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, TRUE, BeaconIsle_EventScript_End
	setflag FLAG_TEMP_11
	end

BeaconIsle_EventScript_HideGuideLights::
	setflag FLAG_TEMP_12
	return
''' % (REEF_GAP, REEF_Y, REEF_GAP + 1, REEF_Y, REEF_GAP, REEF_Y + 1, REEF_GAP + 1, REEF_Y + 1))
    P = S.P
    S.trainer('Roald', 'BEACON_ROALD',
              "Ahoy! I sailed three days to see the famous BEACON ISLE LIGHTHOUSE.\n\n"
              "Turns out it's a fish in a tower. I want a refund. I'll take it out on you.",
              "Fine. The fish wins too.",
              "Ships used to crash here every week. Now they crash every other week.\n\n"
              "That's a 50% improvement. Thank you, LANTURN.")
    S.trainer('Lux', 'BEACON_LUX',
              "Shh! VOLBEAT and ILLUMISE are on a date. Nature's own lighthouse!\n\n...You're ruining the mood.",
              "The mood is ruined.",
              "Moths fly into the lighthouse every night. Not my bugs, though. My bugs have standards.")
    S.npc('Fisherman',
          "At night the CHINCHOU come up to stare at the light.\n\nThey think it's their mother.\n\n"
          "I haven't told them. You don't tell a fish something like that.")
    S.npc('Chinchou', "CHINCHOU is gazing at the lighthouse with its whole face.\n\n"
          "It's the only light it has ever loved.", 'MSGBOX_DEFAULT')
    S.npc('Plaque', "BEACON ISLE LIGHTHOUSE\nEst. 1952. Lamp broken since 1953.\n\n"
          "Ships are kindly requested to follow the fish.", 'MSGBOX_SIGN')
    S.npc('Reef', "A reef of sharp rocks. The waves foam white over every gap.\n\n"
          "Behind it, a tiny island. You'd need a very good light to find the way through.", 'MSGBOX_SIGN')

    gap = (REEF_GAP, REEF_Y)
    objs = [
        tr('OBJ_EVENT_GFX_SAILOR', 24, 23, P + 'Roald', 'LEFT', 4),
        tr('OBJ_EVENT_GFX_MANIAC', 7, 12, P + 'Lux', 'DOWN', 3),
        obj('OBJ_EVENT_GFX_FISHERMAN', PIER[1], PIER[2], P + 'Fisherman', move='MOVEMENT_TYPE_FACE_RIGHT'),
        ball(28, 15, 'ITEM_CELL_BATTERY', 'FLAG_ITEM_BEACON_ISLE_CELL_BATTERY'),
        light(DOOR[0], LY + 1, 'LIGHT_TYPE_BALL'),
        light(DOOR[0], LY + 2, 'LIGHT_TYPE_LIGHTHOUSE_BEAM'),
    ]
    GUIDE = [(REEF_GAP - 1, REEF_Y), (REEF_GAP + 2, REEF_Y)]      # lichtjes op de rotsen naast de doorgang
    for x, y in GUIDE:
        o = light(x, y, 'LIGHT_TYPE_BALL')
        o['flag'] = 'FLAG_TEMP_12'
        objs.append(o)
    CHIN = [(16, 11), (30, 6), (5, 31), (26, 30)]
    for x, y in CHIN:
        objs.append(obj('OBJ_EVENT_GFX_SPECIES(CHINCHOU)', x, y, P + 'Chinchou', 'FLAG_TEMP_11',
                        move='MOVEMENT_TYPE_WANDER_AROUND', elev=1, rx=1, ry=1))
    bgs = [sign(DOOR[0] - 1, DOOR[1], P + 'Plaque', 'BG_EVENT_PLAYER_FACING_NORTH'),
           sign(REEF_GAP, REEF_Y, P + 'Reef', 'BG_EVENT_PLAYER_FACING_SOUTH'),
           hidden(3, 20, 'ITEM_BIG_PEARL', 'FLAG_HIDDEN_ITEM_BEACON_ISLE_BIG_PEARL'),
           hidden(21, 26, 'ITEM_PEARL_STRING', 'FLAG_HIDDEN_ITEM_BEACON_ISLE_PEARL_STRING'),
           hidden(ISLET_DOOR[0] - 2, ISLET_DOOR[1] + 2, 'ITEM_STAR_PIECE', 'FLAG_HIDDEN_ITEM_LIGHT_ISLE_STAR_PIECE')]
    REEF_SIGN = bgs[1]                              # bord op de rots in het rif (aanspreken vanaf het water)
    warps = [warp(DOOR[0], DOOR[1], 'BEACON_ISLE_LIGHTHOUSE_1F', 0),
             warp(ISLET_DOOR[0], ISLET_DOOR[1], 'BEACON_ISLE_GROTTO', 0)]

    # ---- controles
    starts = [(x, 0) for x in range(BW) if mt(g[0][x]) == WATER]
    surf = reach(g, starts)
    opened = [row[:] for row in g]
    for dy in (0, 1):
        for dx in (0, 1):
            opened[REEF_Y + dy][REEF_GAP + dx] = t(WATER, False, 1)
    surf_open = reach(opened, starts)
    assert not any(y > REEF_Y + 1 for x, y in surf), 'het rif is lek: Lichteiland overdag bereikbaar'
    assert (ISLET_DOOR[0], ISLET_DOOR[1] + 2) not in surf
    islet_walk = reach(opened, [(ISLET_DOOR[0], ISLET_DOOR[1] + 1)])
    assert islet_walk & surf_open, 'Lichteiland niet bereikbaar door de doorgang'
    assert gap_rock[0] in (0x150, 0x175)
    landc = {(x, y) for y in range(BH) for x in range(BW) if C.c[y][x] in 'SgLf' and cx.walkable(g[y][x])}
    blocked = {(o['x'], o['y']) for o in objs if o['graphics_id'] != 'OBJ_EVENT_GFX_LIGHT_SPRITE' and o['elevation'] != 1}
    walk = reach(g, [(DOOR[0], DOOR[1] + 1)], blocked=blocked)
    assert walk >= landc - blocked, ('afgesloten stukjes', sorted(landc - blocked - walk)[:10])
    assert walk & surf, 'eiland niet bereikbaar vanaf zee'
    assert (PIER[1], PIER[2]) not in walk and (PIER[1] - 1, PIER[2]) in walk, 'steiger niet vast aan het eiland'
    for o in objs:
        c = (o['x'], o['y'])
        if o['graphics_id'] == 'OBJ_EVENT_GFX_LIGHT_SPRITE':
            assert C.c[o['y']][o['x']] == 'H' or tuple(c) in GUIDE
        elif o['elevation'] == 1:
            assert mt(g[o['y']][o['x']]) == WATER and c in surf, ('CHINCHOU niet in open water', c)
        else:
            assert cx.next_to(c, walk), ('object onbereikbaar', o['script'])
            for s_ in bd.sight_cells(o):
                assert s_ in walk or not cx.walkable(g[s_[1]][s_[0]]), ('zichtlijn over water', o['script'])
    for b in bgs:
        c = (b['x'], b['y'])
        if b['type'] == 'hidden_item':
            assert c in walk or c in islet_walk, ('verborgen item onbereikbaar', b)
        elif b is REEF_SIGN:
            assert (c[0], c[1] - 1) in surf
        else:
            assert cx.next_to(c, walk), ('bord onbereikbaar', b)
    assert (DOOR[0], DOOR[1] + 1) in walk and mt(g[DOOR[1]][DOOR[0]]) == LH_GRID[LH_DOOR[1]][LH_DOOR[0]]
    assert sms.primary_only(g, range(0, SAFE_TOP)), 'bovenste rijen moeten primary zijn (grens met Route 133)'
    r133 = sms.read('Route133', 80, 40)
    assert sms.primary_only([row[BEACON_OFFSET:BEACON_OFFSET + BW] for row in r133], range(32, 40)), \
        'Route 133 onderaan niet primary'
    open_reef133()
    r133 = sms.read('Route133', 80, 40)
    for y in range(32, 40):
        for x in REEF_GAP133:
            assert mt(r133[y][x]) == WATER and cx.walkable(r133[y][x]), ('geul Route 133 dicht', x, y)
    assert all(mt(g[y][x - BEACON_OFFSET]) == WATER for y in range(0, 4) for x in REEF_GAP133)
    assert all((x - BEACON_OFFSET, 3) in surf for x in REEF_GAP133)

    sms.save(g, name)
    sms.border(name, t(WATER, False, 1))
    bd.register_layout(name, const, BW, BH, 'gTileset_General', 'gTileset_Dewford')
    sms.write_map(name, const, objs, warps, [], bgs, music='MUS_DEWFORD', weather='WEATHER_SUNNY',
                  region_map_section='MAPSEC_BEACON_ISLE',
                  connections=[{'map': 'MAP_ROUTE133', 'offset': -BEACON_OFFSET, 'direction': 'up'}])
    oq.register_map(name)
    sms.set_connection('Route133', 'MAP_BEACON_ISLE', 'down', BEACON_OFFSET)
    S.write()
    return name


# ====================================================================== galerij bovenin
def lighthouse_top():
    name, const = 'BeaconIsle_Lighthouse_Top', 'BEACON_ISLE_LIGHTHOUSE_TOP'
    g, W, H, prim, sec = bd.copy_layout('LilycoveCity_DepartmentStoreRooftop', name)
    for x in (9, 10):                                   # automaten weg: reling en vloer
        assert mt(g[0][x]) == 0x26f and mt(g[1][x]) == 0x277
        g[0][x] = g[0][8]
        g[1][x] = g[1][8]
    sms.save(g, name)
    bd.register_layout(name, const, W, H, prim, sec)
    S = Scr(name, '''@ Project Grounded: de galerij bovenin de vuurtoren van Beacon Isle (kopie van het dak van het Lilycove-warenhuis).
@ Vuurtorenwachter WICK en zijn LANTURN, die al 40 jaar de lamp is. 's Nachts LANTURN aanspreken: haar licht vindt het
@ Lichteiland achter het rif (FLAG_BEACON_LIGHT_ISLE_FOUND). Kaart en scripts: beacon_isle.py.
BeaconIsle_Lighthouse_Top_MapScripts::
	.byte 0
''')
    P = S.P
    S.trainer('Wick', 'WICK',
              "Up all those stairs just to look at a fish? Well. She is quite a fish.\n\n"
              "Forty years I've kept this light. The lamp broke in the first week. Since then: LANTURN.\n\n"
              "She works nights. I pay her in pilchards. Want to see what she can do?",
              "...She's still shining. That's what counts.",
              "Some ships still crash. But they crash in a lovely, steady glow.\n\n"
              "The keeper before me, old TALLOW, broke the lamp. Then he rowed off to the little island behind "
              "the reef. Never came back.\n\nHe still sends a postcard every Christmas. Blank. Smells of candles.",
              gift='ITEM_ZOOM_LENS',
              gift_text="Here. The old lens of the lighthouse.\n\n"
                        "Turns out it was a camera lens all along. No wonder the light never reached the ships.")
    S.raw('''%(P)sLanturn::
	lock
	faceplayer
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, FALSE, %(P)sLanturnDay
	goto_if_set FLAG_BEACON_LIGHT_ISLE_FOUND, %(P)sLanturnKnown
	msgbox %(T)sLanturnNight, MSGBOX_DEFAULT
	closemessage
	playse SE_M_REFLECT
	setflag FLAG_BEACON_LIGHT_ISLE_FOUND
	msgbox %(T)sLanturnReveal, MSGBOX_DEFAULT
	release
	end

%(P)sLanturnDay::
	msgbox %(T)sLanturnDay, MSGBOX_DEFAULT
	release
	end

%(P)sLanturnKnown::
	msgbox %(T)sLanturnKnown, MSGBOX_DEFAULT
	release
	end
''' % dict(P=P, T=S.T), [
        ('LanturnDay', "LANTURN is glowing at roughly forty thousand lumens.\n\nIt looks extremely proud of itself.\n\n"
                       "By day, nobody notices. LANTURN is saving her best work for the night shift."),
        ('LanturnNight', "LANTURN swings her light out over the sea, slowly, like she's looking for her keys."),
        ('LanturnReveal', "...There! Behind the reef, a tiny island lights up. A gap in the rocks glows white.\n\n"
                          "It was there all along. It just never got the light.\n\n"
                          "The gap in the reef is marked now. Ships may follow it. Ships may also not."),
        ('LanturnKnown', "LANTURN keeps her beam on the gap in the reef.\n\nShe has never been more professional."),
    ])
    S.npc('View', "The whole sea, all the way to PACIFIDLOG.\n\nSomewhere out there, a ship is about to make a mistake.",
          'MSGBOX_SIGN')
    objs = [tr('OBJ_EVENT_GFX_EXPERT_M', 6, 4, P + 'Wick', 'RIGHT', 1),
            obj('OBJ_EVENT_GFX_SPECIES(LANTURN)', 8, 3, P + 'Lanturn', move='MOVEMENT_TYPE_FACE_DOWN')]
    bgs = [sign(5, 0, P + 'View', 'BG_EVENT_PLAYER_FACING_NORTH')]
    warps = [warp(13, 3, 'BEACON_ISLE_LIGHTHOUSE_2F', 1)]
    walk = reach(g, [(13, 4)], blocked={(o['x'], o['y']) for o in objs})
    for o in objs:
        assert cx.next_to((o['x'], o['y']), walk), o['script']
    assert (5, 1) in walk
    sms.write_map(name, const, objs, warps, [], bgs, music='MUS_OCEANIC_MUSEUM', region_map_section='MAPSEC_BEACON_ISLE',
                  **bd.indoor())
    oq.register_map(name)
    S.write()
    return name


# ====================================================================== de grot op het Lichteiland
GROTTO_LAYOUT = 'LAYOUT_GRANITE_CAVE_STEVENS_ROOM'      # gedeeld, niet gekopieerd
GROTTO_DOOR = (7, 3)
TALLOW = (7, 8)


def grotto():
    name, const = 'BeaconIsle_Grotto', 'BEACON_ISLE_GROTTO'
    L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == GROTTO_LAYOUT][0]
    g = oq.read_layout(L['blockdata_filepath'], L['width'], L['height'])
    S = Scr(name, '''@ Project Grounded: de grot op het Lichteiland achter het rif van Beacon Isle (layout: Steven's kamer in
@ Granite Cave, gedeeld). TALLOW, de geest van de eerste vuurtorenwachter (1952-1953), en zeldzame wilde soorten.
@ Kaart en scripts: tools/grounded/maptools/beacon_isle.py. Teksten zijn placeholders.
BeaconIsle_Grotto_MapScripts::
	.byte 0
''')
    P = S.P
    S.trainer('Tallow', 'TALLOW',
              "...Oh! A visitor. Forgive me, I'm a little transparent today.\n\n"
              "I am TALLOW, first keeper of the BEACON ISLE LIGHT. 1952 to 1953. Mostly 1953.\n\n"
              "I broke the lamp. I was trying to make it brighter. I made it a candle.\n\n"
              "Seventy years I've practised in this cave. Let me show you real light!",
              "...Even a ghost can be outshone. How embarrassing.",
              "Tell WICK the fish is doing a better job than I ever did.\n\n"
              "Don't tell him I said that. Tell him I'm haunting him. Professionally.",
              gift='ITEM_DUSK_STONE',
              gift_text="Take this. Hold it up to a LAMPENT and something wonderful happens.\n\n"
                        "Hold it up to a lighthouse and nothing happens. I've checked. For seventy years.")
    S.npc('Candles', "Hundreds of melted candles, in neat rows.\n\nEvery one has a little label: “BRIGHTER?”", 'MSGBOX_SIGN')
    objs = [tr('OBJ_EVENT_GFX_PSYCHIC_M', TALLOW[0], TALLOW[1], P + 'Tallow', 'UP', 0),
            ball(10, 10, 'ITEM_MIND_PLATE', 'FLAG_ITEM_LIGHT_ISLE_MIND_PLATE')]
    bgs = [sign(5, 9, P + 'Candles')]
    warps = [warp(GROTTO_DOOR[0], GROTTO_DOOR[1], 'BEACON_ISLE', 1)]
    start = (GROTTO_DOOR[0], GROTTO_DOOR[1] + 1)
    walk = reach(g, [start], blocked={(o['x'], o['y']) for o in objs})
    for o in objs:
        assert cx.next_to((o['x'], o['y']), walk), ('grot: object onbereikbaar', o['script'])
    for b in bgs:
        assert cx.next_to((b['x'], b['y']), walk) and not cx.walkable(g[b['y']][b['x']]), ('grot: bord', b)
    sms.write_map(name, const, objs, warps, [], bgs, music='MUS_SEALED_CHAMBER', weather='WEATHER_NONE',
                  map_type='MAP_TYPE_UNDERGROUND', region_map_section='MAPSEC_BEACON_ISLE', show_map_name=False,
                  allow_cycling=False, allow_escaping=True, layout=GROTTO_LAYOUT)
    oq.register_map(name)
    S.write()
    return name


# ====================================================================== wilde Pokemon (grot)
WILD = {
    'BEACON_ISLE_GROTTO': dict(
        land=(10, [('SHIINOTIC', 42, 45), ('LAMPENT', 42, 45), ('PERSIAN_ALOLA', 42, 45), ('VOLTORB_HISUI', 42, 45),
                   ('KLEFKI', 42, 45), ('CHIMECHO', 42, 45), ('ESPATHRA', 43, 45), ('ACCELGOR', 43, 45),
                   ('PALOSSAND', 43, 46), ('UNOWN', 42, 44), ('INDEEDEE', 45, 46), ('ELECTRODE_HISUI', 46, 46)])),
}


# ====================================================================== trainer (vaste id's: 1048; 1049 en 1055-1059 vrij)
TRAINERS = [
    (1048, 'TALLOW', 'Beacon Isle, Lichteiland: geest van de eerste vuurtorenwachter (Battle Stadium)', 'TALLOW', 'Sage',
     'Psychic M', 'Male', 'Suspicious', bd.AI_BOSS, 'Hyper Potion / Hyper Potion', [
         bd.mon('Drifblim', 52, ['Shadow Ball', 'Air Slash', 'Will-O-Wisp', 'Calm Mind']),
         bd.mon('Dusknoir', 52, ['Shadow Punch', 'Earthquake', 'Ice Punch', 'Will-O-Wisp']),
         bd.mon('Mismagius', 52, ['Shadow Ball', 'Dazzling Gleam', 'Thunderbolt', 'Nasty Plot']),
         bd.mon('Jellicent', 52, ['Scald', 'Shadow Ball', 'Recover', 'Will-O-Wisp']),
         bd.mon('Chandelure @ Life Orb', 54, ['Shadow Ball', 'Flamethrower', 'Energy Ball', 'Trick Room'])]),
]


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = '// beacon_isle { (tools/grounded/maptools/beacon_isle.py; vaste id\'s)\n'
    for n, const, why, *_ in TRAINERS:
        assert n in (1048, 1049, 1055, 1056, 1057, 1058, 1059)
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (const, n, why)
    blk += '// }'
    if '// beacon_isle {' in s:
        i = s.index('// beacon_isle {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for n, *_ in TRAINERS:
        assert len(re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)) == 1, ('trainer-id dubbel', n)
    open(p, 'w').write(s)

    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- beacon_isle (tools/grounded/maptools/beacon_isle.py) --- */\n\n'
    for n, const, why, nm, cls, pic, gender, music, ai, items, team in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music]
        if items:
            hdr.append('Items: ' + items)
        hdr += ['Double Battle: No', ai]
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (const, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde beacon_isle --- */'
    s = bd.replace_block(s, '/* --- beacon_isle', '/* --- einde beacon_isle --- */', blk)
    open(p, 'w').write(s)


STADIUM = [('TALLOW', 'TALLOW', 'PSYCHIC_M', "TALLOW! Lighthouse keeper, 1952 to 1953. Mostly 1953. Mostly dead.")]


# ====================================================================== main
if __name__ == '__main__':
    flags()
    bd.beam_graphics()
    LH_GRID.extend(bd.lighthouse_tileset())
    names = [beacon_isle(), lighthouse_top(), grotto()]
    bd.WILD = WILD
    bd.wild()
    trainers()
    if not os.environ.get('BD_NO_STADIUM'):
        bd.STADIUM = STADIUM
        bd.stadium()
    if len(sys.argv) > 1:
        subprocess.run(['make', 'data/tilesets/secondary/dewford/tiles.4bpp'], check=True, capture_output=True)
        for n in names:
            L = bd.layout_of(n)
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', str(L['height'])], check=True)
    print('klaar:', ', '.join(names))
