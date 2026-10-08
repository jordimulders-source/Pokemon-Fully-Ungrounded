"""Project Grounded: het vuurtoreneiland (Beacon Isle) en het drakeneiland (Dragonspine Isle). Deterministisch en
idempotent (vaste seeds; draai opnieuw na een wijziging).

  BeaconIsle             Eilandje onder Route 133 (verbinding, x 48-79 van Route 133; Town Map x 14, y 11), General +
                         Dewford. De vuurtoren uit tools/grounded/lighthouse_art.py staat als 3x8 metatiles achteraan
                         de Dewford-tileset (tiles na de laatste gebruikte, palet 6 = lighthouse.pal met .pla: glas en
                         lens gloeien 's nachts). 's Nachts: lichtbol + draaiende lichtbundel (LIGHT_TYPE_LIGHTHOUSE_BEAM,
                         src/event_object_movement.c) en CHINCHOU in het water die naar het licht staren.
  BeaconIsle_Lighthouse_1F / _2F / _Top
                         Binnenkant: kopieen van de Space Center (1F zeekaarten, 2F machines, met een extra trap omhoog)
                         en het dak van het Lilycove-warenhuis (de galerij, automaten weg). Bovenin vuurtorenwachter
                         WICK en zijn LANTURN: de lamp is al 40 jaar kapot, zij is het licht.
  DragonspineIsle        Rotsig drakeneiland rechts van Route 129 (verbinding; Town Map x 26-27, y 10), General +
                         Lavaridge (terras-autotiler van chimney_ext.py), zandstrand met de General-zand-autotiler.
                         De linker kolommen zijn alleen water/zand (andere secondary dan Route 129; het script
                         controleert het). Grot in de bergwand naar de Dragon's Den.
  DragonspineIsle_Den    Meteor Falls-stijl (Map-klasse van meteor_falls_ext.py): onderhal met meer, een hoge klif met
                         waterval (Waterfall = badge 8) naar de bovenhal met de drakenwachter GERALD.

Ook: trainers (opponents.h- en trainers.party-blok 'beacon_dragon'), wilde Pokemon, mapsecs + popups, flags, de
Battle Stadium-pool (WICK, GERALD; pool.py en announcer.py) en de verbindingen in Route 133 en Route 129.
Teksten zijn placeholders in de huisstijl (Jordi herschrijft ze); ze worden automatisch afgebroken
(tools/dialogen/import.py).

Gebruik: python3 tools/grounded/maptools/beacon_dragon.py [rendermap]"""
import importlib.util, json, math, os, random, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chimney_ext as cx            # zet ook de werkmap op de repo-root
import ogerpon_quest as oq
import sea_market_steam as sms
import tapu_cresselia as tc
import meteor_falls_ext as mf
from PIL import Image

t, mt, WATER, reach, val = sms.t, sms.mt, sms.WATER, cx.reach, tc.val
DEBUG = os.environ.get('BD_DEBUG')

_spec = importlib.util.spec_from_file_location('dialogen_import', 'tools/dialogen/import.py')
dimp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dimp)


# ====================================================================== tekst-hulpjes (scripts.inc)
def text(label, s):
    out = '%s:\n' % label
    for part in dimp.to_strings(s):
        out += '\t.string "%s"\n' % part
    return out + '\n'


class Scr:
    """Verzamelt scripts en teksten van één kaart."""

    def __init__(self, name, header):
        self.name, self.P = name, name + '_EventScript_'
        self.T = name + '_Text_'
        self.head, self.code, self.texts = header, [], []

    def npc(self, key, s, kind='MSGBOX_NPC'):
        self.code.append('%s%s::\n\tmsgbox %s%s, %s\n\tend\n' % (self.P, key, self.T, key, kind))
        self.texts.append(text(self.T + key, s))
        return self.P + key

    def trainer(self, key, const, intro, defeat, post, gift=None, gift_text=None):
        P, T = self.P + key, self.T + key
        if gift:
            self.code.append(
                f'{P}::\n\ttrainerbattle_single TRAINER_{const}, {T}Intro, {T}Defeat, {P}Defeated\n'
                f'\tmsgbox {T}Post, MSGBOX_AUTOCLOSE\n\tend\n\n'
                f'{P}Defeated::\n\tmsgbox {T}Gift, MSGBOX_DEFAULT\n\tgiveitem {gift}\n'
                f'\tmsgbox {T}Post, MSGBOX_DEFAULT\n\trelease\n\tend\n')
            self.texts.append(text(T + 'Gift', gift_text))
        else:
            self.code.append(f'{P}::\n\ttrainerbattle_single TRAINER_{const}, {T}Intro, {T}Defeat\n'
                             f'\tmsgbox {T}Post, MSGBOX_AUTOCLOSE\n\tend\n')
        for k, s in (('Intro', intro), ('Defeat', defeat), ('Post', post)):
            self.texts.append(text(T + k, s))
        return P

    def raw(self, code, texts=()):
        self.code.append(code)
        for label, s in texts:
            self.texts.append(text(self.T + label, s))

    def write(self):
        s = self.head.rstrip('\n') + '\n\n' + '\n'.join(self.code) + \
            '\n@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)\n' + \
            ''.join(self.texts)
        open('data/maps/%s/scripts.inc' % self.name, 'w').write(s.rstrip('\n') + '\n')


# ====================================================================== registratie-hulpjes
def register_layout(name, const, W, H, primary, secondary):
    lj = open('data/layouts/layouts.json').read()
    entry = '''    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "%s",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, W, H, primary, secondary, name, name)
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"id": "LAYOUT_%s"' % const); s = lj.rindex('    {', 0, i); e = lj.index('    }', i) + 5
        lj = lj[:s] + entry + lj[e:]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    json.loads(lj)
    open('data/layouts/layouts.json', 'w').write(lj)


def layout_of(mapname):
    m = json.load(open('data/maps/%s/map.json' % mapname))
    return [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == m['layout']][0]


def copy_layout(src_map, name):
    L = layout_of(src_map)
    W, H = L['width'], L['height']
    g = oq.read_layout(L['blockdata_filepath'], W, H)
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/border.bin' % name, 'wb').write(open(L['border_filepath'], 'rb').read())
    return g, W, H, L['primary_tileset'], L['secondary_tileset']


def indoor(**kw):
    d = dict(map_type='MAP_TYPE_INDOOR', weather='WEATHER_NONE', allow_cycling=False, allow_escaping=False,
             allow_running=True, show_map_name=False, battle_scene='MAP_BATTLE_SCENE_NORMAL')
    d.update(kw)
    return d


def warp(x, y, dest, wid, elev=0):
    return {'x': x, 'y': y, 'elevation': elev, 'dest_map': 'MAP_' + dest, 'dest_warp_id': str(wid)}


def obj(gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', local_id=None, elev=3, rx=0, ry=0, sight='0'):
    o = sms.obj(gfx, x, y, script, flag, move=move, local_id=local_id, elev=elev, rx=rx, ry=ry)
    o['trainer_sight_or_berry_tree_id'] = sight
    return o


def tr(gfx, x, y, script, face, sight, elev=3):
    o = obj(gfx, x, y, script, move='MOVEMENT_TYPE_FACE_' + face, elev=elev, sight=str(sight))
    o['trainer_type'] = 'TRAINER_TYPE_NORMAL'
    return o


def ball(x, y, it, flag, elev=3):
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', flag, 'MOVEMENT_TYPE_LOOK_AROUND',
               elev=elev, sight=it)


def light(x, y, kind):
    return obj('OBJ_EVENT_GFX_LIGHT_SPRITE', x, y, '0x0', sight=kind, move='MOVEMENT_TYPE_NONE')


def sign(x, y, script, facing='BG_EVENT_PLAYER_FACING_ANY'):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': facing, 'script': script}


def hidden(x, y, it, flag):
    return cx.hidden(x, y, it, flag)


def sight_cells(o):
    return cx.sight(o)


# ====================================================================== flags (FLAG_GROUNDED 100-149 = dit script)
FLAGS = [
    # (n in FLAG_GROUNDED(n), naam, commentaar)
    (100, 'FLAG_HIDDEN_ITEM_BEACON_ISLE_BIG_PEARL', 'Beacon Isle: verborgen Big Pearl'),
    (101, 'FLAG_HIDDEN_ITEM_BEACON_ISLE_PEARL_STRING', 'Beacon Isle: verborgen Pearl String'),
    (102, 'FLAG_ITEM_BEACON_ISLE_CELL_BATTERY', 'Beacon Isle: Cell Battery'),
    (103, 'FLAG_ITEM_BEACON_LIGHTHOUSE_THUNDER_STONE', 'vuurtoren 1F: Thunder Stone'),
    (104, 'FLAG_ITEM_BEACON_LIGHTHOUSE_ELECTIRIZER', 'vuurtoren 2F: Electirizer'),
    (105, 'FLAG_HIDDEN_ITEM_DRAGONSPINE_DRAGON_SCALE', 'Dragonspine Isle: verborgen Dragon Scale'),
    (106, 'FLAG_HIDDEN_ITEM_DRAGONSPINE_STAR_PIECE', 'Dragonspine Isle: verborgen Star Piece'),
    (107, 'FLAG_ITEM_DRAGONSPINE_MAX_REVIVE', 'Dragonspine Isle: Max Revive'),
    (108, 'FLAG_ITEM_DRAGONSPINE_DEN_PP_UP', "Dragon's Den: PP Up"),
    (109, 'FLAG_ITEM_DRAGONSPINE_DEN_MAX_ELIXIR', "Dragon's Den: Max Elixir"),
    (110, 'FLAG_HIDDEN_ITEM_DRAGONSPINE_DEN_BIG_NUGGET', "Dragon's Den: verborgen Big Nugget"),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// beacon_dragon { (tools/grounded/maptools/beacon_dragon.py; FLAG_GROUNDED 100-149)\n'
    for n, name, why in FLAGS:
        assert 100 <= n <= 149
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// beacon_dragon {' in s:
        i = s.index('// beacon_dragon {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('\n', s.index('// Verdeling (houd bij!)')) + 1
        s = s[:anchor] + blk + '\n' + s[anchor:]
    open(p, 'w').write(s)


# ====================================================================== vuurtoren in de Dewford-tileset
DEW = 'data/tilesets/secondary/dewford'
LH_DIR = 'graphics/grounded/lighthouse'
LH_PAL = 6
GRASS_BOTTOM = struct.unpack_from('<4H', open('data/tilesets/primary/general/metatiles.bin', 'rb').read(), 1 * 16)
MB_NON_ANIMATED_DOOR = 0x60
LW, LH = 3, 8                       # vuurtoren in metatiles
LH_DOOR = (1, 7)                    # deur: middelste metatile van de onderste rij


def lighthouse_tileset():
    """Zet de vuurtoren (48x128) als 3x8 metatiles achteraan Dewford; geeft het raster met metatile-id's terug."""
    lh = Image.open(LH_DIR + '/lighthouse.png')
    assert lh.mode == 'P' and lh.size == (48, 128)
    lp = lh.load()
    tim = Image.open(DEW + '/tiles.png')
    assert tim.mode == 'P' and tim.size == (128, 256)
    tp = tim.load()
    mts = open(DEW + '/metatiles.bin', 'rb').read()
    ents = struct.unpack('<%dH' % (len(mts) // 2), mts)

    def tile(n):
        return tuple(tuple(tp[(n % 16) * 8 + x, (n // 16) * 8 + y] for x in range(8)) for y in range(8))

    def flips(tl):
        h = tuple(tuple(reversed(r)) for r in tl)
        return [(tl, 0), (h, 1), (tuple(reversed(tl)), 2), (tuple(reversed(h)), 3)]

    lh_tiles = []
    for ty in range(16):
        for tx in range(6):
            lh_tiles.append(tuple(tuple(lp[tx * 8 + x, ty * 8 + y] for x in range(8)) for y in range(8)))
    vanilla_used = max((e & 0x3ff) - 512 for e in ents if (e & 0x3ff) >= 512 and (e >> 12) != LH_PAL)
    index = {}
    for n in range(512):
        tl = tile(n)
        if any(any(r) for r in tl):
            for f, fl in flips(tl):
                index.setdefault(f, (n, fl))
    free = [n for n in range(vanilla_used + 1, 512) if not any(any(r) for r in tile(n))]
    entries = {}
    for i, tl in enumerate(lh_tiles):
        if not any(any(r) for r in tl):
            entries[i] = 0
            continue
        if tl not in index:
            n = free.pop(0)
            for y in range(8):
                for x in range(8):
                    tp[(n % 16) * 8 + x, (n // 16) * 8 + y] = tl[y][x]
            for f, fl in flips(tl):
                index.setdefault(f, (n, fl))
        n, fl = index[tl]
        entries[i] = (512 + n) | (fl << 10) | (LH_PAL << 12)
    tim.save(DEW + '/tiles.png')
    # palet 6 (Dewford gebruikt het niet) + lichtkleuren voor de dag/nacht-cyclus
    for ext in ('pal', 'pla'):
        src = open('%s/lighthouse.%s' % (LH_DIR, ext), 'rb').read()
        dst = '%s/palettes/%02d.%s' % (DEW, LH_PAL, ext)
        if not os.path.exists(dst) or open(dst, 'rb').read() != src:
            open(dst, 'wb').write(src)
            if os.path.exists('%s/palettes/%02d.gbapal' % (DEW, LH_PAL)):
                os.remove('%s/palettes/%02d.gbapal' % (DEW, LH_PAL))
    grid = []
    for my in range(LH):
        row = []
        for mx in range(LW):
            k = lambda dx, dy: entries[(my * 2 + dy) * 6 + mx * 2 + dx]
            top = (k(0, 0), k(1, 0), k(0, 1), k(1, 1))
            beh = MB_NON_ANIMATED_DOOR if (mx, my) == LH_DOOR else 0
            row.append(sms.ensure_metatile('dewford', struct.pack('<8H', *(GRASS_BOTTOM + top)), struct.pack('<H', beh)))
        grid.append(row)
    return grid


def beam_graphics():
    """Lichtbundel als object (64x32) op de kleuren van de lichtbol (light.pal: 15 = helderst)."""
    src = Image.open(LH_DIR + '/lighthouse_beam.png')
    assert src.size == (64, 32)
    remap = {0: 0, 1: 15, 2: 12, 3: 9}
    out = Image.new('P', (64, 32))
    pal = []
    for line in open('graphics/object_events/palettes/light.pal').read().split('\n')[3:19]:
        pal += [int(v) for v in line.split()]
    out.putpalette(pal + [0] * (768 - len(pal)))
    out.putdata([remap[v] for v in src.getdata()])
    dst = 'graphics/object_events/pics/misc/lighthouse_beam.png'
    out.save(dst)


# ====================================================================== Beacon Isle
BW, BH = 32, 36
BEACON_OFFSET = 48                  # x van het eiland op Route 133
LX, LY = 15, 11                     # linkerbovenhoek van de vuurtoren
DOOR = (LX + LH_DOOR[0], LY + LH_DOOR[1])
SAFE_TOP = 9                        # bovenste rijen alleen primary (grens met Route 133, andere secondary)
LH_GRID = []


REEF_GAP133 = (60, 61)              # Route 133 heeft onderaan een rif; één zeerots (60-61, 36-37) gaat weg


def open_reef133():
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


def beacon_isle():
    name, const = 'BeaconIsle', 'BEACON_ISLE'
    rng = random.Random(171)                        # nationaal dexnummer van Lanturn
    land = [[False] * BW for _ in range(BH)]
    ph = [rng.random() * 6.28 for _ in range(3)]
    for y in range(BH):
        for x in range(BW):
            a = math.atan2(y - 25, x - 16)
            r = 1 + 0.05 * math.sin(3 * a + ph[0]) + 0.04 * math.sin(5 * a + ph[1])
            body = ((x - 16) / 12.5) ** 2 + ((y - 25) / 8.3) ** 2 <= r * r
            cape = (x - 16) ** 2 + ((y - 15.5) * 1.05) ** 2 <= 6.6 ** 2
            land[y][x] = body or cape
    tc.smooth(land, 6)
    d = tc.dist_to_water(land)
    C = tc.Chars(BW, BH, '~')
    for y in range(BH):
        for x in range(BW):
            if land[y][x]:
                C.c[y][x] = 'S' if d[y][x] <= 2 else 'g'
    # grasveld rond de vuurtoren (de onderlaag van de vuurtoren-metatiles is gras)
    for y in range(LY - 1, DOOR[1] + 2):
        for x in range(LX - 1, LX + LW + 1):
            assert land[y][x], ('vuurtoren niet op het eiland', x, y)
            C.c[y][x] = 'g'
    for my in range(LH):
        for mx in range(LW):
            C.c[LY + my][LX + mx] = 'H'
    # hoog gras (twee plukken), bomen, bloemen
    for cx_, cy_, r in ((8.5, 25, 2.6), (23.5, 25.5, 2.4)):
        C.disc(cx_, cy_, r, 'L', only='g')
    trees = [(5, 21), (25, 21), (12, 28), (20, 29)]
    for x, y in trees:
        if all(C.c[y + dy][x + dx] == 'g' for dx in (0, 1) for dy in (0, 1)) and C.c[y - 1][x] == 'g' and C.c[y - 1][x + 1] == 'g':
            for dx in (0, 1):
                for dy in (0, 1):
                    C.c[y + dy][x + dx] = 'T'
    for y in range(BH):
        for x in range(BW):
            if C.c[y][x] == 'g' and 2.5 <= math.hypot(x - DOOR[0], (y - DOOR[1]) * 1.2) <= 4.2 and rng.random() < 0.3 \
                    and y > DOOR[1]:
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
    tc.place_rocks(g, 8, 172, lambda x, y: y >= SAFE_TOP + 2 or (x < 8 or x > 23))

    S = Scr(name, '''@ Project Grounded: Beacon Isle, het vuurtoreneiland onder Route 133 (ZEE_PLAN.md).
@ Kaart: tools/grounded/maptools/beacon_dragon.py (ook deze scripts). 's Nachts: CHINCHOU in het water (FLAG_TEMP_11
@ verbergt ze overdag) en het licht van de vuurtoren (lichtobjecten). Teksten zijn placeholders.
BeaconIsle_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, BeaconIsle_OnTransition
	.byte 0

BeaconIsle_OnTransition:
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, TRUE, BeaconIsle_EventScript_Night
	setflag FLAG_TEMP_11
BeaconIsle_EventScript_Night:
	end
''')
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

    objs = [
        tr('OBJ_EVENT_GFX_SAILOR', 24, 27, P + 'Roald', 'LEFT', 4),
        tr('OBJ_EVENT_GFX_MANIAC', 7, 22, P + 'Lux', 'DOWN', 3),
        obj('OBJ_EVENT_GFX_FISHERMAN', 16, 32, P + 'Fisherman', move='MOVEMENT_TYPE_FACE_DOWN'),
        ball(26, 22, 'ITEM_CELL_BATTERY', 'FLAG_ITEM_BEACON_ISLE_CELL_BATTERY'),
        light(DOOR[0], LY + 1, 'LIGHT_TYPE_BALL'),
        light(DOOR[0], LY + 2, 'LIGHT_TYPE_LIGHTHOUSE_BEAM'),
    ]
    CHIN = [(5, 13), (27, 15), (9, 7), (24, 6)]
    for i, (x, y) in enumerate(CHIN):
        objs.append(obj('OBJ_EVENT_GFX_SPECIES(CHINCHOU)', x, y, P + 'Chinchou', 'FLAG_TEMP_11',
                        move='MOVEMENT_TYPE_WANDER_AROUND', elev=1, rx=1, ry=1))
    bgs = [sign(DOOR[0] - 1, DOOR[1], P + 'Plaque', 'BG_EVENT_PLAYER_FACING_NORTH'),
           hidden(5, 26, 'ITEM_BIG_PEARL', 'FLAG_HIDDEN_ITEM_BEACON_ISLE_BIG_PEARL'),
           hidden(27, 29, 'ITEM_PEARL_STRING', 'FLAG_HIDDEN_ITEM_BEACON_ISLE_PEARL_STRING')]
    warps = [warp(DOOR[0], DOOR[1], 'BEACON_ISLE_LIGHTHOUSE_1F', 0)]

    # ---- controles
    starts = [(x, 0) for x in range(BW) if mt(g[0][x]) == WATER]
    surf = reach(g, starts)
    landc = {(x, y) for y in range(BH) for x in range(BW) if C.c[y][x] in 'SgLf' and cx.walkable(g[y][x])}
    blocked = {(o['x'], o['y']) for o in objs if o['graphics_id'] != 'OBJ_EVENT_GFX_LIGHT_SPRITE' and o['elevation'] != 1}
    walk = reach(g, [(DOOR[0], DOOR[1] + 1)], blocked=blocked)
    assert walk >= landc - blocked, ('afgesloten stukjes', sorted(landc - blocked - walk)[:10])
    assert walk & surf, 'eiland niet bereikbaar vanaf zee'
    for o in objs:
        if o['graphics_id'] == 'OBJ_EVENT_GFX_LIGHT_SPRITE':
            assert C.c[o['y']][o['x']] == 'H'
        elif o['elevation'] == 1:
            assert mt(g[o['y']][o['x']]) == WATER, ('CHINCHOU niet in het water', o['x'], o['y'])
        else:
            assert cx.next_to((o['x'], o['y']), walk), ('object onbereikbaar', o['script'])
            for c in sight_cells(o):
                assert c in walk or not cx.walkable(g[c[1]][c[0]]), ('zichtlijn over water', o['script'])
    for b in bgs:
        c = (b['x'], b['y'])
        assert (c in walk) if b['type'] == 'hidden_item' else cx.next_to(c, walk), ('bg onbereikbaar', b)
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

    sms.save(g, name)
    sms.border(name, t(WATER, False, 1))
    register_layout(name, const, BW, BH, 'gTileset_General', 'gTileset_Dewford')
    sms.write_map(name, const, objs, warps, [], bgs, music='MUS_DEWFORD', weather='WEATHER_SUNNY',
                  region_map_section='MAPSEC_BEACON_ISLE',
                  connections=[{'map': 'MAP_ROUTE133', 'offset': -BEACON_OFFSET, 'direction': 'up'}])
    oq.register_map(name)
    sms.set_connection('Route133', 'MAP_BEACON_ISLE', 'down', BEACON_OFFSET)
    S.write()
    return name


# ====================================================================== vuurtoren binnen
def lighthouse_1f():
    name, const = 'BeaconIsle_Lighthouse_1F', 'BEACON_ISLE_LIGHTHOUSE_1F'
    g, W, H, prim, sec = copy_layout('MossdeepCity_SpaceCenter_1F', name)
    sms.save(g, name)
    register_layout(name, const, W, H, prim, sec)
    S = Scr(name, '''@ Project Grounded: vuurtoren op Beacon Isle, begane grond (kopie van de Space Center 1F: tafels = zeekaarten).
@ Kaart en scripts: tools/grounded/maptools/beacon_dragon.py. Teksten zijn placeholders.
BeaconIsle_Lighthouse_1F_MapScripts::
	.byte 0
''')
    P = S.P
    S.trainer('Dylan', 'BEACON_DYLAN',
              "I'm the foghorn of this lighthouse. Unpaid. Self-appointed.\n\nHONNNNK! Let's battle!",
              "That was my last note.",
              "The keeper says I'm “not a foghorn” and “not allowed in.”\n\nAnd yet here I am. In.")
    S.npc('Logbook', "KEEPER'S LOG.\nDay 1: Lamp broken.\nDay 2: Lamp still broken.\n\n"
          "Day 3: Found a LANTURN.\nDays 4 to 14,600: LANTURN.", 'MSGBOX_SIGN')
    S.npc('Charts', "Sea charts. Someone circled every rock around the island and wrote “NOT AGAIN.”", 'MSGBOX_SIGN')
    S.npc('Window', "You can see the ocean. The ocean can see you. Neither of you blinks.", 'MSGBOX_SIGN')
    objs = [tr('OBJ_EVENT_GFX_MAN_5', 8, 4, P + 'Dylan', 'DOWN', 3),
            ball(1, 8, 'ITEM_THUNDER_STONE', 'FLAG_ITEM_BEACON_LIGHTHOUSE_THUNDER_STONE')]
    bgs = [sign(3, 5, P + 'Logbook'), sign(11, 7, P + 'Charts'), sign(6, 1, P + 'Window', 'BG_EVENT_PLAYER_FACING_NORTH')]
    warps = [warp(7, 9, 'BEACON_ISLE', 0), warp(8, 9, 'BEACON_ISLE', 0), warp(13, 1, 'BEACON_ISLE_LIGHTHOUSE_2F', 0)]
    walk = reach(g, [(7, 8)], blocked={(o['x'], o['y']) for o in objs})
    for o in objs:
        assert cx.next_to((o['x'], o['y']), walk), o['script']
    assert (13, 1) in walk or cx.next_to((13, 1), walk)
    sms.write_map(name, const, objs, warps, [], bgs, music='MUS_OCEANIC_MUSEUM', region_map_section='MAPSEC_BEACON_ISLE',
                  **indoor())
    oq.register_map(name)
    S.write()
    return name


def lighthouse_2f():
    name, const = 'BeaconIsle_Lighthouse_2F', 'BEACON_ISLE_LIGHTHOUSE_2F'
    g, W, H, prim, sec = copy_layout('MossdeepCity_SpaceCenter_2F', name)
    up, _, _, _, _ = copy_layout('MossdeepCity_SpaceCenter_1F', name)      # trap omhoog uit 1F (x 12-14, y 0-2)
    for y in range(3):
        for x in range(3):
            g[y][4 + x] = up[y][12 + x]
    sms.save(g, name)
    open('data/layouts/%s/border.bin' % name, 'wb').write(open(layout_of('MossdeepCity_SpaceCenter_2F')['border_filepath'], 'rb').read())
    register_layout(name, const, W, H, prim, sec)
    S = Scr(name, '''@ Project Grounded: vuurtoren op Beacon Isle, eerste verdieping (kopie van de Space Center 2F + trap omhoog).
@ Kaart en scripts: tools/grounded/maptools/beacon_dragon.py. Teksten zijn placeholders.
BeaconIsle_Lighthouse_2F_MapScripts::
	.byte 0
''')
    P = S.P
    S.trainer('Keiko', 'BEACON_KEIKO',
              "I climb these stairs a hundred times a day. Leg day is every day.\n\nToday, it's YOUR day.",
              "My legs gave up before I did.",
              "The keeper climbs these stairs every night. He's 91.\n\nHe says the secret is spite.")
    S.trainer('Pemberton', 'BEACON_PEMBERTON',
              "I've come to purchase this lighthouse. The keeper refuses to sell.\n\nPerhaps I can buy YOU instead?",
              "Priceless. How annoying.",
              "I offered the keeper a fortune for his LANTURN.\n\n"
              "He said she isn't for sale. She's for “shining.” Unbelievable.")
    S.npc('Machine', "A huge machine labeled LAMP CONTROL. It's unplugged.\n\n"
          "Someone has taped a picture of a fish over the switch.", 'MSGBOX_SIGN')
    objs = [tr('OBJ_EVENT_GFX_GIRL_3', 2, 7, P + 'Keiko', 'RIGHT', 4),
            tr('OBJ_EVENT_GFX_GENTLEMAN', 10, 3, P + 'Pemberton', 'LEFT', 3),
            ball(14, 9, 'ITEM_ELECTIRIZER', 'FLAG_ITEM_BEACON_LIGHTHOUSE_ELECTIRIZER')]
    bgs = [sign(8, 7, P + 'Machine')]
    warps = [warp(13, 1, 'BEACON_ISLE_LIGHTHOUSE_1F', 2), warp(5, 1, 'BEACON_ISLE_LIGHTHOUSE_TOP', 0)]
    walk = reach(g, [(13, 2)], blocked={(o['x'], o['y']) for o in objs})
    for o in objs:
        assert cx.next_to((o['x'], o['y']), walk), o['script']
    assert cx.next_to((5, 1), walk) and (5, 2) in walk
    sms.write_map(name, const, objs, warps, [], bgs, music='MUS_OCEANIC_MUSEUM', region_map_section='MAPSEC_BEACON_ISLE',
                  **indoor())
    oq.register_map(name)
    S.write()
    return name


def lighthouse_top():
    name, const = 'BeaconIsle_Lighthouse_Top', 'BEACON_ISLE_LIGHTHOUSE_TOP'
    g, W, H, prim, sec = copy_layout('LilycoveCity_DepartmentStoreRooftop', name)
    for x in (9, 10):                                   # automaten weg: reling en vloer
        assert mt(g[0][x]) == 0x26f and mt(g[1][x]) == 0x277
        g[0][x] = g[0][8]
        g[1][x] = g[1][8]
    sms.save(g, name)
    register_layout(name, const, W, H, prim, sec)
    S = Scr(name, '''@ Project Grounded: de galerij bovenin de vuurtoren van Beacon Isle (kopie van het dak van het Lilycove-warenhuis).
@ Vuurtorenwachter WICK en zijn LANTURN, die al 40 jaar de lamp is. Kaart en scripts: beacon_dragon.py.
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
              "A man on ROUTE 134 wants to build his own lighthouse. He asked me what one looks like.\n\n"
              "I said “a fish.” He wrote it down.",
              gift='ITEM_ZOOM_LENS',
              gift_text="Here. The old lens of the lighthouse.\n\n"
                        "Turns out it was a camera lens all along. No wonder the light never reached the ships.")
    S.npc('Lanturn', "LANTURN is glowing at roughly forty thousand lumens.\n\nIt looks extremely proud of itself.",
          'MSGBOX_DEFAULT')
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
                  **indoor())
    oq.register_map(name)
    S.write()
    return name


# ====================================================================== Dragonspine Isle
DW, DH = 42, 42
PLATEAU = (15, 9, 34, 31)
MOUNT = (18, 11, 31, 22)
SPINE = (20, 12, 29, 15)
STAIRS1 = [(23, 31), (24, 31)]
STAIRS2 = [(28, 22), (29, 22)]
CAVE = (21, 22)
SAFE_LEFT = 9                       # linker kolommen alleen primary (grens met Route 129)


def dragon_hmap():
    m = [['0'] * DW for _ in range(DH)]

    def fill(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                m[y][x] = c
    fill(*PLATEAU, '1')
    fill(*MOUNT, '2')
    # (geen losse bergkam: de RIDGE-tegels lazen als losse wandstukjes)
    return [''.join(r) for r in m]


def dragonspine_isle():
    name, const = 'DragonspineIsle', 'DRAGONSPINE_ISLE'
    random.seed(149)                                 # nationaal dexnummer van Dragonite
    rng = random.Random(148)
    hm = dragon_hmap()
    land = [[False] * DW for _ in range(DH)]
    ph = [rng.random() * 6.28 for _ in range(3)]
    for y in range(DH):
        for x in range(DW):
            a = math.atan2(y - 21, x - 25)
            r = 1 + 0.07 * math.sin(3 * a + ph[0]) + 0.05 * math.sin(5 * a + ph[1]) + 0.03 * math.sin(7 * a + ph[2])
            blob = abs((x - 25) / 15.5) ** 2.3 + abs((y - 21) / 17.0) ** 2.3 <= r ** 2.3
            near = PLATEAU[0] - 2 <= x <= PLATEAU[2] + 2 and PLATEAU[1] - 2 <= y <= PLATEAU[3] + 2
            land[y][x] = blob or near
    tc.smooth(land, 6)
    for y in range(PLATEAU[1] - 2, PLATEAU[3] + 3):
        for x in range(PLATEAU[0] - 2, PLATEAU[2] + 3):
            assert land[y][x], ('plateau te dicht bij het water', x, y)
    g = cx.terrace_tiles(hm)
    for y in range(DH):
        for x in range(DW):
            if hm[y][x] != '0':
                continue
            g[y][x] = tc.sand_tile(land, x, y) if land[y][x] else t(WATER, False, 1)
    cx.stairs(g, STAIRS1)
    cx.stairs(g, STAIRS2)
    cx.cave_door(g, *CAVE)
    tc.place_rocks(g, 10, 150, lambda x, y: x >= SAFE_LEFT + 1 or y < 6 or y > 34)

    S = Scr(name, '''@ Project Grounded: Dragonspine Isle, het drakeneiland rechts van Route 129 (ZEE_PLAN.md idee 6).
@ Kaart en scripts: tools/grounded/maptools/beacon_dragon.py. In de bergwand de Dragon's Den (drakenwachter GERALD,
@ achter een waterval). Teksten zijn placeholders.
DragonspineIsle_MapScripts::
	.byte 0
''')
    P = S.P
    S.trainer('Vernon', 'DRAGONSPINE_VERNON',
              "Welcome to DRAGONSPINE ISLE! The dragons here are wild, free and incredibly bitey.",
              "Bitten. Again.",
              "I've been bitten 412 times. I keep count. It keeps me humble.")
    S.trainer('Saela', 'DRAGONSPINE_SAELA',
              "I came here to train with dragons. Mostly I've been training my running.",
              "Running away it is.",
              "The cave? The warden lives in there. GERALD.\n\n"
              "He has a clipboard. Even the dragons are afraid of the clipboard.")
    S.npc('Adjuster',
          "I'm the island's insurance adjuster.\n\n"
          "Claims this week: fourteen scorched tents, three eaten canoes and one man who “just wanted to pet it.”\n\n"
          "All denied. Dragons count as an act of God.")
    objs = [tr('OBJ_EVENT_GFX_MAN_5', 17, 26, P + 'Vernon', 'RIGHT', 4),
            tr('OBJ_EVENT_GFX_WOMAN_5', 24, 17, P + 'Saela', 'DOWN', 3),
            obj('OBJ_EVENT_GFX_MAN_1', 17, 34, P + 'Adjuster', move='MOVEMENT_TYPE_LOOK_AROUND'),
            ball(19, 20, 'ITEM_MAX_REVIVE', 'FLAG_ITEM_DRAGONSPINE_MAX_REVIVE')]
    bgs = [hidden(31, 33, 'ITEM_DRAGON_SCALE', 'FLAG_HIDDEN_ITEM_DRAGONSPINE_DRAGON_SCALE'),
           hidden(32, 10, 'ITEM_STAR_PIECE', 'FLAG_HIDDEN_ITEM_DRAGONSPINE_STAR_PIECE')]
    warps = [warp(CAVE[0], CAVE[1], 'DRAGONSPINE_ISLE_DEN', 0)]
    starts = [(CAVE[0], CAVE[1] + 1)]
    keep = cx.keep_cells(objs, bgs, cx.area(STAIRS1 + STAIRS2 + [CAVE]) | cx.area([(x, y + 1) for x, y in STAIRS1 + STAIRS2])
                         | cx.area([(x, y - 1) for x, y in STAIRS1 + STAIRS2]) | cx.area([(CAVE[0], CAVE[1] + 1)]))
    high = {(x, y) for y in range(DH) for x in range(DW) if hm[y][x] in 'X'}
    used = set()
    grass = cx.ash_grass(g, keep | high, rng, 6)
    cx.decorate(g, 0x271, 'ground', keep | grass, starts, [
        ('boulder', 3, 'open'), ('rock', 6, 'muur'), ('basalt', 3, 'vrij'), ('crack_a', 3, 'vrij'),
        ('crack_b', 3, 'vrij'), ('deadtree', 3, 'muur')], rng, used)
    if DEBUG:
        for y in range(DH):
            print('%2d ' % y + ''.join('~' if mt(v) == WATER else ('s' if mt(v) < 0x200 and cx.walkable(v) else
                                       ('"' if mt(v) == 0x207 else ('.' if cx.walkable(v) else '#'))) for v in g[y]))
    # ---- controles
    blocked = {(o['x'], o['y']) for o in objs}
    walk = reach(g, starts, blocked=blocked)
    surf = reach(g, [(0, y) for y in range(DH)])
    assert any(cx.next_to(c, surf) for c in walk), 'eiland niet bereikbaar vanaf zee'
    for o in objs:
        assert cx.next_to((o['x'], o['y']), walk), ('object onbereikbaar', o['script'])
        for c in sight_cells(o):
            assert c in walk or not cx.walkable(g[c[1]][c[0]]), ('zichtlijn over water', o['script'])
    for b in bgs:
        assert (b['x'], b['y']) in walk, ('verborgen item onbereikbaar', b)
    assert grass and all(c in walk for c in grass), 'as-gras onbereikbaar'
    lvl2 = {(x, y) for x in range(MOUNT[0] + 1, MOUNT[2]) for y in range(MOUNT[1] + 1, MOUNT[3]) if cx.walkable(g[y][x])}
    assert lvl2 and lvl2 - blocked <= walk, 'bergterras onbereikbaar'
    assert all(mt(g[y][x]) < 0x200 for y in range(DH) for x in range(SAFE_LEFT)), 'linker kolommen niet primary'
    r129 = sms.read('Route129', 80, 40)
    assert all(mt(r129[y][x]) < 0x200 for y in range(40) for x in range(80 - SAFE_LEFT, 80)), 'Route 129 rechts niet primary'
    sms.save(g, name)
    sms.border(name, t(WATER, False, 1))
    register_layout(name, const, DW, DH, 'gTileset_General', 'gTileset_Lavaridge')
    sms.write_map(name, const, objs, warps, [], bgs, music='MUS_ROUTE120', weather='WEATHER_SHADE',
                  region_map_section='MAPSEC_DRAGONSPINE_ISLE',
                  connections=[{'map': 'MAP_ROUTE129', 'offset': 0, 'direction': 'left'}])
    oq.register_map(name)
    sms.set_connection('Route129', 'MAP_DRAGONSPINE_ISLE', 'right', 0)
    S.write()
    return name


# ====================================================================== Dragon's Den
NW, NH = 36, 40
DEN_EXIT = (17, 34)
GERALD = (26, 9)


def dragon_den():
    name, const = 'DragonspineIsle_Den', 'DRAGONSPINE_ISLE_DEN'
    m = mf.Map(NW, NH)
    m.room(4, 5, 31, 16)                 # bovenhal
    m.room(4, 22, 31, 34)                # onderhal
    m.water(12, 10, 23, 16)              # bovenmeer
    m.water(9, 22, 26, 27)               # ondermeer (onder de waterval)
    m.build()
    m.cliff(4, 31, 17, pillars=(6, 27))
    m.waterfall(14, 17)
    m.stal_wall(4, 31, 5, pillars=(7, 26))
    m.exit_south(*DEN_EXIT)
    m.crater(27, 6)                      # het nest achter GERALD
    m.crater(5, 31)
    rnd = random.Random(1491)
    keep = {DEN_EXIT, (17, 33), (17, 32), GERALD, (26, 10), (8, 8), (9, 8), (8, 30), (9, 30), (10, 30), (11, 30),
            (28, 29), (27, 29), (26, 29), (29, 29), (5, 23), (30, 33), (5, 15), (6, 15), (29, 9), (30, 9), (24, 8), (10, 6), (10, 7),
            (11, 8), (12, 8)}
    for x in range(4, 32):
        keep |= {(x, 21), (x, 16)}
    m.rubble(rnd, 6, (4, 23, 31, 33), keep)
    m.rubble(rnd, 4, (4, 6, 31, 15), keep)
    g = m.build()

    S = Scr(name, '''@ Project Grounded: de Dragon's Den in Dragonspine Isle. Kaart en scripts: tools/grounded/maptools/beacon_dragon.py.
@ Onderhal met meer; de waterval (Waterfall, badge 8) leidt naar de bovenhal met drakenwachter GERALD.
@ Teksten zijn placeholders.
DragonspineIsle_Den_MapScripts::
	.byte 0
''')
    P = S.P
    S.trainer('Osric', 'DRAGONSPINE_OSRIC',
              "Halt! This den is for DRAGON TAMERS only!\n\nDo you have a permit? ...Nobody has a permit.",
              "Fine. You may stay. Unofficially.",
              "The waterfall leads to the warden. Climbing it is the easy part.\n\nFilling in his forms is the hard part.")
    S.trainer('Mira', 'DRAGONSPINE_MIRA',
              "Shh. The dragons are sleeping. Let's fight very, very quietly.",
              "...That was not quiet.",
              "Something big is snoring up there. I hope it's a DRAGONITE.\n\nI really hope it's not GERALD.")
    S.trainer('Talon', 'DRAGONSPINE_TALON',
              "You climbed the waterfall? Impressive. I took the stairs.\n\n...There are no stairs. That's how good I am.",
              "There really are no stairs.",
              "GERALD has guarded this den for thirty years. Nobody knows what he's guarding it from.\n\nPossibly from us.")
    S.trainer('Gerald', 'GERALD_WARDEN',
              "Ah. A visitor. I am GERALD, Warden of the Dragon's Den.\n\n"
              "Have you filled in form D-7, “Intent to Battle a Dragon Warden”?\n\n"
              "...No? Then I shall have to process you manually.",
              "Request... approved.",
              "Dragons used to rule these islands. These days they're mostly retired.\n\n"
              "I make sure nobody disturbs their pension.",
              gift='ITEM_EXPERT_BELT',
              gift_text="Your paperwork is in order. Take this EXPERT BELT.\n\n"
                        "Standard issue for people who keep winning. Sign here. And here. And here.")
    S.npc('Dragonite', "DRAGONITE is asleep on a stack of paperwork.\n\nIt is snoring in triplicate.", 'MSGBOX_DEFAULT')
    objs = [tr('OBJ_EVENT_GFX_MAN_5', 8, 30, P + 'Osric', 'RIGHT', 4),
            tr('OBJ_EVENT_GFX_WOMAN_5', 29, 29, P + 'Mira', 'LEFT', 3),
            tr('OBJ_EVENT_GFX_MAN_3', 9, 7, P + 'Talon', 'DOWN', 3),
            tr('OBJ_EVENT_GFX_MAN_5', GERALD[0], GERALD[1], P + 'Gerald', 'DOWN', 1),
            obj('OBJ_EVENT_GFX_SPECIES(DRAGONITE)', 29, 9, P + 'Dragonite', move='MOVEMENT_TYPE_FACE_LEFT'),
            ball(5, 23, 'ITEM_PP_UP', 'FLAG_ITEM_DRAGONSPINE_DEN_PP_UP'),
            ball(5, 15, 'ITEM_MAX_ELIXIR', 'FLAG_ITEM_DRAGONSPINE_DEN_MAX_ELIXIR')]
    bgs = [hidden(30, 33, 'ITEM_BIG_NUGGET', 'FLAG_HIDDEN_ITEM_DRAGONSPINE_DEN_BIG_NUGGET')]
    warps = [warp(DEN_EXIT[0], DEN_EXIT[1], 'DRAGONSPINE_ISLE', 0)]
    # ---- controles: onderhal te voet, bovenhal alleen via het meer + de waterval
    blocked = {(o['x'], o['y']) for o in objs}
    start = (DEN_EXIT[0], DEN_EXIT[1] - 1)
    walk = mf.reachable(g, start, blocked=blocked)
    surf = mf.reachable(g, start, blocked=blocked, allow_water=True)
    upper = {(x, y) for x in range(4, 32) for y in range(5, 17) if (x, y) in surf and g[y][x] >> 12 != 1}
    assert upper and not (upper & walk), 'bovenhal hoort alleen via de waterval bereikbaar te zijn'
    for o in objs:
        c = (o['x'], o['y'])
        if c[1] >= 22:
            assert mf.next_to(walk, *c), ('onderhal: object onbereikbaar', o['script'])
        else:
            assert mf.next_to(upper, *c), ('bovenhal: object onbereikbaar', o['script'])
        for s in sight_cells(o):
            assert s in walk | upper or (g[s[1]][s[0]] >> 10) & 3, ('zichtlijn over water', o['script'])
    assert (30, 33) in walk
    mf.save_layout(name, g)
    register_layout(name, const, NW, NH, 'gTileset_General', 'gTileset_MeteorFalls')
    sms.write_map(name, const, objs, warps, [], bgs, music='MUS_SEALED_CHAMBER', weather='WEATHER_NONE',
                  map_type='MAP_TYPE_UNDERGROUND', region_map_section='MAPSEC_DRAGONSPINE_ISLE', show_map_name=False,
                  allow_cycling=False, allow_escaping=True, battle_scene='MAP_BATTLE_SCENE_NORMAL')
    oq.register_map(name)
    S.write()
    return name


# ====================================================================== mapsecs, popups
MAPSECS = [('MAPSEC_BEACON_ISLE', 'BEACON ISLE', 14, 11, 1, 1, 'MAPPOPUP_THEME_MARBLE', 'vuurtoreneiland'),
           ('MAPSEC_DRAGONSPINE_ISLE', 'DRAGONSPINE ISLE', 26, 10, 2, 1, 'MAPPOPUP_THEME_STONE', 'drakeneiland')]


def mapsecs():
    p = 'src/data/region_map/region_map_sections.json'
    s = open(p).read()
    for mid, nm, x, y, w, h, theme, why in MAPSECS:
        if '"%s"' % mid not in s:
            i = s.rindex('    }\n  ]')
            s = s[:i + 5] + ',\n    {\n      "id": "%s",\n      "name": "%s",\n      "x": %d,\n      "y": %d,\n' \
                '      "width": %d,\n      "height": %d\n    }' % (mid, nm, x, y, w, h) + s[i + 5:]
    json.loads(s)
    open(p, 'w').write(s)
    p = 'src/map_name_popup.c'
    s = open(p).read()
    for mid, nm, x, y, w, h, theme, why in MAPSECS:
        if mid in s:
            continue
        a = '    [MAPSEC_STEAM_ISLAND - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_STONE, // Project Grounded: stoomeiland\n'
        b = '    [MAPSEC_STEAM_ISLAND - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: stoomeiland\n'
        assert a in s and b in s
        s = s.replace(a, a + '    [%s - KANTO_MAPSEC_COUNT] = %s, // Project Grounded: %s\n' % (mid, theme, why), 1)
        s = s.replace(b, b + '    [%s - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: %s\n' % (mid, why), 1)
    open(p, 'w').write(s)


# ====================================================================== wilde Pokemon
def mons(spec):
    return [{'min_level': a, 'max_level': b, 'species': 'SPECIES_' + s} for s, a, b in spec]


LAND_RATES = (20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1)
WILD = {
    'BEACON_ISLE': dict(
        land=(20, [('KILOWATTREL', 38, 41), ('HELIOPTILE', 38, 41), ('VOLBEAT', 38, 41), ('ILLUMISE', 38, 41),
                   ('CRABRAWLER', 38, 41), ('SQUAWKABILLY', 38, 41), ('PINCURCHIN', 38, 41), ('MANECTRIC', 38, 41),
                   ('GALVANTULA', 38, 41), ('TOGEDEMARU', 38, 41), ('BOLTUND', 39, 41), ('AMPHAROS', 40, 42)]),
        water=(4, [('LANTURN', 38, 41), ('EELEKTRIK', 38, 41), ('MANTINE', 38, 41), ('PELIPPER', 38, 41),
                   ('LUMINEON', 40, 42)]),
        fishing=(30, [('FINNEON', 28, 30), ('WISHIWASHI', 28, 30), ('LANTURN', 32, 36), ('LUMINEON', 32, 36),
                      ('EELEKTRIK', 32, 36), ('CLAWITZER', 38, 42), ('BRUXISH', 38, 42), ('MANTINE', 40, 44),
                      ('KINGLER', 40, 44), ('EELEKTROSS', 42, 45)])),
    'DRAGONSPINE_ISLE': dict(
        land=(20, [('ALTARIA', 44, 47), ('CYCLIZAR', 44, 47), ('FLYGON', 44, 47), ('HAXORUS', 44, 47),
                   ('TYRANTRUM', 45, 48), ('DRUDDIGON', 44, 47), ('KOMMO_O', 45, 48), ('DRAMPA', 45, 48),
                   ('NOIVERN', 45, 48), ('SLIGGOO', 44, 47), ('DURALUDON', 47, 48), ('GARCHOMP', 48, 48)]),
        water=(4, [('SEADRA', 44, 47), ('DRAGALGE', 48, 48), ('DRAGONAIR', 45, 48), ('TATSUGIRI', 45, 48),
                   ('KINGDRA', 48, 48)]),
        fishing=(30, [('HORSEA', 28, 31), ('SKRELP', 28, 31), ('SEADRA', 33, 37), ('DRAGONAIR', 33, 37),
                      ('TATSUGIRI', 33, 37), ('KINGDRA', 42, 46), ('DRACOVISH', 42, 46), ('ARCTOVISH', 42, 46),
                      ('DRAGALGE', 48, 50), ('DRAGONITE', 51, 52)])),
    'DRAGONSPINE_ISLE_DEN': dict(
        land=(10, [('GABITE', 46, 47), ('ZWEILOUS', 46, 50), ('SHELGON', 46, 49), ('ARCTIBAX', 46, 50),
                   ('DRACOZOLT', 46, 50), ('ARCTOZOLT', 46, 50), ('DRAKLOAK', 46, 49), ('TURTONATOR', 46, 50),
                   ('DURALUDON', 47, 50), ('SLIGGOO', 46, 49), ('SALAMENCE', 50, 50), ('DRAGAPULT', 50, 50)]),
        water=(4, [('DRAGONAIR', 46, 50), ('SEADRA', 46, 50), ('DRACOVISH', 48, 50), ('ARCTOVISH', 48, 50),
                   ('KINGDRA', 50, 50)])),
}


def wild():
    p = 'src/data/wild_encounters.json'
    s = open(p).read()
    for mp, tabs in WILD.items():
        lbl = 'g' + ''.join(w.title() for w in mp.split('_'))
        e = {'map': 'MAP_' + mp, 'base_label': lbl}
        for kind in ('land', 'water', 'fishing'):
            if kind in tabs:
                rate, spec = tabs[kind]
                assert len(spec) == {'land': 12, 'water': 5, 'fishing': 10}[kind]
                assert len({x[0] for x in spec}) == len(spec), ('dubbele soort', mp, kind)
                e[kind + '_mons'] = {'encounter_rate': rate, 'mons': mons(spec)}
        blob = json.dumps(e, indent=2)
        blob = '\n'.join('        ' + ln for ln in blob.split('\n'))
        key = '"map": "MAP_%s"' % mp
        if key in s:                                    # vervangen
            i = s.index(key); a = s.rindex('{', 0, i)
            depth, j = 0, a
            while True:
                if s[j] == '{': depth += 1
                elif s[j] == '}':
                    depth -= 1
                    if depth == 0: break
                j += 1
            s = s[:a] + blob.lstrip() + s[j + 1:]
        else:
            i = s.index('"base_label": "gSteamIsland"'); a = s.rindex('{', 0, i)
            depth, j = 0, a
            while True:
                if s[j] == '{': depth += 1
                elif s[j] == '}':
                    depth -= 1
                    if depth == 0: break
                j += 1
            s = s[:j + 1] + ',\n' + blob + s[j + 1:]
    json.loads(s)
    open(p, 'w').write(s)


# ====================================================================== trainers
IV = 'IVs: 25 HP / 25 Atk / 25 Def / 25 SpA / 25 SpD / 25 Spe'
AI = 'AI: Check Bad Move / Try To Faint / Check Viability'
AI_BOSS = 'AI: Check Bad Move / Try To Faint / Check Viability / Smart Switching / Smart Mon Choices'


def mon(head, lvl, moves, ability=None, iv=IV):
    out = [head, 'Level: %d' % lvl] + (['Ability: ' + ability] if ability else []) + [iv] + ['- ' + m for m in moves]
    return '\n'.join(out)


TRAINERS = [
    ('BEACON_ROALD', 'Beacon Isle, toerist die zijn geld terug wil', 'ROALD', 'Sailor', 'Sailor', 'Male', 'Male', AI, None, [
        mon('Bewear', 41, ['Hammer Arm', 'Double-Edge', 'Payback', 'Bulk Up']),
        mon('Passimian', 41, ['Brick Break', 'Rock Slide', 'Knock Off', 'U-turn']),
        mon('Kilowattrel', 41, ['Discharge', 'Air Slash', 'Volt Switch', 'Roost'])]),
    ('BEACON_LUX', 'Beacon Isle, vuurvliegjesman', 'LUX', 'Bug Maniac', 'Bug Maniac', 'Male', 'Suspicious', AI, None, [
        mon('Volbeat', 41, ['Tail Glow', 'Bug Buzz', 'Thunderbolt', 'Encore'], 'Prankster'),
        mon('Illumise', 41, ['Bug Buzz', 'Wish', 'Encore', 'Thunder Wave'], 'Prankster'),
        mon('Galvantula', 41, ['Electroweb', 'Bug Buzz', 'Sticky Web', 'Thunder']),
        mon('Vikavolt', 42, ['Bug Buzz', 'Thunderbolt', 'Energy Ball', 'Air Slash'])]),
    ('BEACON_DYLAN', 'Beacon Isle, vuurtoren 1F: zelfbenoemde misthoorn', 'DYLAN', 'Guitarist', 'Guitarist', 'Male', 'Intense', AI, None, [
        mon('Boltund', 42, ['Wild Charge', 'Crunch', 'Play Rough', 'Roar']),
        mon('Heliolisk', 42, ['Parabolic Charge', 'Grass Knot', 'Surf', 'Volt Switch']),
        mon('Bellibolt', 42, ['Discharge', 'Muddy Water', 'Slack Off', 'Toxic'])]),
    ('BEACON_KEIKO', 'Beacon Isle, vuurtoren 2F: traplopen', 'KEIKO', 'Battle Girl', 'Battle Girl', 'Female', 'Intense', AI, None, [
        mon('Annihilape', 42, ['Rage Fist', 'Close Combat', 'Bulk Up', 'Rock Slide']),
        mon('Breloom', 42, ['Spore', 'Mach Punch', 'Seed Bomb', 'Rock Tomb']),
        mon('Toxicroak', 42, ['Poison Jab', 'Sucker Punch', 'Drain Punch', 'Swords Dance']),
        mon('Scrafty', 42, ['Drain Punch', 'Crunch', 'Bulk Up', 'Fake Out'])]),
    ('BEACON_PEMBERTON', 'Beacon Isle, vuurtoren 2F: wil de vuurtoren kopen', 'PEMBERTON', 'Gentleman', 'Gentleman', 'Male', 'Rich', AI, None, [
        mon('Kangaskhan', 42, ['Fake Out', 'Body Slam', 'Sucker Punch', 'Earthquake']),
        mon('Oinkologne', 42, ['Body Slam', 'Stomping Tantrum', 'Yawn', 'Belch']),
        mon('Ursaring', 42, ['Crunch', 'Hammer Arm', 'Swords Dance', 'Facade']),
        mon('Miltank', 42, ['Milk Drink', 'Rollout', 'Thunder Wave', 'Double-Edge'])]),
    ('WICK', 'Beacon Isle, vuurtorenwachter (Battle Stadium)', 'WICK', 'Expert', 'Expert M', 'Male', 'Intense', AI_BOSS,
     'Super Potion / Super Potion', [
        mon('Ampharos @ Sitrus Berry', 45, ['Thunderbolt', 'Dragon Pulse', 'Power Gem', 'Thunder Wave']),
        mon('Magnezone', 45, ['Flash Cannon', 'Thunderbolt', 'Mirror Coat', 'Light Screen']),
        mon('Eelektross', 45, ['Wild Charge', 'Crunch', 'Drain Punch', 'Coil'], 'Levitate'),
        mon('Lumineon', 45, ['Scald', 'U-turn', 'Ice Beam', 'Rain Dance']),
        mon('Lanturn @ Leftovers', 47, ['Discharge', 'Scald', 'Ice Beam', 'Confuse Ray'], 'Volt Absorb')]),
    ('DRAGONSPINE_VERNON', 'Dragonspine Isle, 412 keer gebeten', 'VERNON', 'Dragon Tamer', 'Dragon Tamer', 'Male', 'Intense', AI, None, [
        mon('Altaria', 46, ['Dragon Pulse', 'Air Slash', 'Cotton Guard', 'Roost']),
        mon('Flygon', 46, ['Earthquake', 'Dragon Claw', 'U-turn', 'Fire Punch']),
        mon('Drampa', 46, ['Dragon Pulse', 'Hyper Voice', 'Flamethrower', 'Glare'])]),
    ('DRAGONSPINE_SAELA', 'Dragonspine Isle, traint vooral rennen', 'SAELA', 'Cooltrainer', 'Cooltrainer F', 'Female', 'Cool', AI, None, [
        mon('Noivern', 46, ['Air Slash', 'Dragon Pulse', 'Super Fang', 'Roost']),
        mon('Cyclizar', 46, ['Double-Edge', 'Dragon Claw', 'U-turn', 'Shed Tail']),
        mon('Tyrantrum', 46, ['Rock Slide', 'Dragon Claw', 'Crunch', 'Dragon Dance'])]),
    ('DRAGONSPINE_OSRIC', "Dragon's Den onderhal, vergunningencontrole", 'OSRIC', 'Dragon Tamer', 'Dragon Tamer', 'Male', 'Intense', AI, None, [
        mon('Kommo-o', 49, ['Clanging Scales', 'Drain Punch', 'Iron Defense', 'Dragon Claw']),
        mon('Druddigon', 49, ['Dragon Claw', 'Rock Slide', 'Superpower', 'Glare']),
        mon('Dracozolt', 49, ['Bolt Beak', 'Dragon Claw', 'Stomping Tantrum', 'Rock Slide'])]),
    ('DRAGONSPINE_MIRA', "Dragon's Den onderhal, heel zacht vechten", 'MIRA', 'Cooltrainer', 'Cooltrainer F', 'Female', 'Cool', AI, None, [
        mon('Goodra', 49, ['Dragon Pulse', 'Sludge Bomb', 'Thunderbolt', 'Fire Blast']),
        mon('Duraludon', 49, ['Flash Cannon', 'Dragon Pulse', 'Thunderbolt', 'Stealth Rock']),
        mon('Tatsugiri', 49, ['Dragon Pulse', 'Muddy Water', 'Rapid Spin', 'Icy Wind']),
        mon('Appletun', 49, ['Apple Acid', 'Dragon Pulse', 'Recover', 'Leech Seed'])]),
    ('DRAGONSPINE_TALON', "Dragon's Den bovenhal, nam de trap", 'TALON', 'Cooltrainer', 'Cooltrainer M', 'Male', 'Cool', AI_BOSS, None, [
        mon('Garchomp', 52, ['Earthquake', 'Dragon Claw', 'Swords Dance', 'Stone Edge']),
        mon('Dragapult', 52, ['Dragon Darts', 'Phantom Force', 'U-turn', 'Will-O-Wisp']),
        mon('Haxorus', 52, ['Dragon Dance', 'Dragon Claw', 'Earthquake', 'Poison Jab']),
        mon('Hydreigon', 53, ['Dark Pulse', 'Dragon Pulse', 'Flamethrower', 'Nasty Plot'])]),
    ('GERALD_WARDEN', "Dragon's Den, drakenwachter met klembord (Battle Stadium)", 'GERALD', 'Dragon Tamer', 'Dragon Tamer', 'Male', 'Intense',
     AI_BOSS, 'Hyper Potion / Hyper Potion', [
        mon('Exeggutor_Alola', 55, ['Dragon Hammer', 'Wood Hammer', 'Flamethrower', 'Trick Room']),
        mon('Kingdra', 55, ['Rain Dance', 'Surf', 'Dragon Pulse', 'Ice Beam']),
        mon('Goodra_Hisui', 55, ['Heavy Slam', 'Dragon Pulse', 'Sludge Bomb', 'Thunderbolt']),
        mon('Baxcalibur', 55, ['Glaive Rush', 'Icicle Crash', 'Earthquake', 'Dragon Dance']),
        mon('Archaludon', 55, ['Electro Shot', 'Flash Cannon', 'Dragon Pulse', 'Body Press']),
        mon('Dragonite @ Lum Berry', 57, ['Dragon Dance', 'Extreme Speed', 'Earthquake', 'Fire Punch'], 'Multiscale')]),
]


def replace_block(text_, start, end, new):
    if start in text_:
        i = text_.index(start)
        j = text_.index(end, i) + len(end)
        return text_[:i] + new + text_[j:]
    return text_.rstrip('\n') + '\n\n' + new + '\n'


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    if '// beacon_dragon {' in s:
        first = int(re.search(r'// beacon_dragon \{[^\n]*\n#define TRAINER_\w+\s+(\d+)', s).group(1))
    else:
        first = int(re.search(r'^#define TRAINERS_COUNT\s+(\d+)', s, re.M).group(1))
    blk = '// beacon_dragon { (tools/grounded/maptools/beacon_dragon.py)\n'
    for i, tr_ in enumerate(TRAINERS):
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (tr_[0], first + i, tr_[1])
    blk += '// }'
    if '// beacon_dragon {' in s:
        i = s.index('// beacon_dragon {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    top = max(int(m.group(2)) for m in re.finditer(r'^#define (TRAINER_\w+)\s+(\d+)', s, re.M)
              if m.group(1) not in ('TRAINERS_COUNT', 'MAX_TRAINERS_COUNT'))
    s = re.sub(r'^#define TRAINERS_COUNT\s+\d+', '#define TRAINERS_COUNT                      %d' % (top + 1), s, flags=re.M)
    open(p, 'w').write(s)

    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- beacon_dragon (tools/grounded/maptools/beacon_dragon.py) --- */\n\n'
    for const, why, nm, cls, pic, gender, music, ai, items, team in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music]
        if items:
            hdr.append('Items: ' + items)
        hdr += ['Double Battle: No', ai]
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (const, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde beacon_dragon --- */'
    s = replace_block(s, '/* --- beacon_dragon', '/* --- einde beacon_dragon --- */', blk)
    open(p, 'w').write(s)


# ====================================================================== Battle Stadium-pool
# (trainer zonder TRAINER_, sleutel in GFX (pool.py zoekt op voorvoegsel), overworld, omroepzin).
# TRAINER_GERALD bestaat al in vanilla (een Cooltrainer): de drakenwachter heet GERALD_WARDEN.
STADIUM = [('WICK', 'WICK', 'EXPERT_M', "WICK! Forty years a lighthouse keeper. His lamp is a fish. It works."),
           ('GERALD_WARDEN', 'GERALD', 'MAN_5', "GERALD, Warden of the Dragon's Den! Did you fill in form D-7? Too late now.")]


def stadium():
    p = 'tools/grounded/stadium/pool.py'
    s = open(p).read()
    for key, gkey, gfx, line in STADIUM:
        if "'%s'," % key not in s.split('RIVALS =')[0]:
            i = s.index('\n]', s.index('POOL = ['))
            if '# eilanden: vuurtorenwachter' not in s:
                s = s[:i] + "\n    # eilanden: vuurtorenwachter (Beacon Isle), drakenwachter (Dragonspine Isle)" + s[i:]
                i = s.index('\n]', s.index('POOL = ['))
            s = s[:i] + "\n    '%s'," % key + s[i:]
        if "'%s': '" % gkey not in s.split('def gfx_for')[0].split('GFX = {')[1]:
            j = s.index("    'GRIMSBY': 'SAILOR',\n") + len("    'GRIMSBY': 'SAILOR',\n")
            s = s[:j] + "    '%s': '%s',\n" % (gkey, gfx) + s[j:]
    open(p, 'w').write(s)
    p = 'tools/grounded/stadium/announcer.py'
    s = open(p).read()
    for key, gkey, gfx, line in STADIUM:
        if "    '%s': " % key not in s:
            a = s.index("    'GRIMSBY': ")
            a = s.index('\n', a) + 1
            s = s[:a] + '    %r: %s,\n' % (key, json.dumps(line, ensure_ascii=False)) + s[a:]
    open(p, 'w').write(s)
    subprocess.run([sys.executable, 'tools/grounded/stadium/pool.py'], check=True)
    subprocess.run([sys.executable, 'tools/grounded/stadium/announcer.py'], check=True)


# ====================================================================== main
if __name__ == '__main__':
    flags()
    beam_graphics()
    LH_GRID.extend(lighthouse_tileset())
    names = [beacon_isle(), lighthouse_1f(), lighthouse_2f(), lighthouse_top(), dragonspine_isle(), dragon_den()]
    mapsecs()
    wild()
    trainers()
    if not os.environ.get('BD_NO_STADIUM'):
        stadium()
    if len(sys.argv) > 1:
        subprocess.run(['make', 'data/tilesets/secondary/dewford/tiles.4bpp'], check=True, capture_output=True)
        for n in names:
            L = layout_of(n)
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', str(L['height'])], check=True)
    print('klaar:', ', '.join(names))
