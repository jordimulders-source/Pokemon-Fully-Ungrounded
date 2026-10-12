"""Project Grounded: het vuurtoreneiland (Beacon Isle). Deterministisch en
idempotent (vaste seeds; draai opnieuw na een wijziging).

  BeaconIsle             (nu in beacon_isle.py) Eilandje onder Route 133 (verbinding, x 48-79 van Route 133; Town Map x 14, y 11), General +
                         Dewford. De vuurtoren uit tools/grounded/lighthouse_art.py staat als 3x8 metatiles achteraan
                         de Dewford-tileset (tiles na de laatste gebruikte, palet 6 = lighthouse.pal met .pla: glas en
                         lens gloeien 's nachts). 's Nachts: lichtbol + draaiende lichtbundel (LIGHT_TYPE_LIGHTHOUSE_BEAM,
                         src/event_object_movement.c) en CHINCHOU in het water die naar het licht staren.
  BeaconIsle_Lighthouse_1F / _2F / _Top
                         Binnenkant: kopieen van de Space Center (1F zeekaarten, 2F machines, met een extra trap omhoog)
                         en het dak van het Lilycove-warenhuis (de galerij, automaten weg). Bovenin vuurtorenwachter
                         WICK en zijn LANTURN: de lamp is al 40 jaar kapot, zij is het licht.
  (Dragonspine Isle en de Dragon's Den zijn het Tao-eiland geworden: tools/grounded/maptools/tao_island.py.)

Ook: trainers (opponents.h- en trainers.party-blok 'beacon_dragon'), wilde Pokemon, mapsecs + popups, flags, de
Battle Stadium-pool (WICK; pool.py en announcer.py) en de verbinding in Route 133.
Teksten zijn placeholders in de huisstijl (Jordi herschrijft ze); ze worden automatisch afgebroken
(tools/dialogen/import.py).

Gebruik: python3 tools/grounded/maptools/beacon_dragon.py [rendermap]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
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
# Het eiland zelf (en de galerij bovenin de vuurtoren) staan sinds v0.9.16x in beacon_isle.py (nieuwe vorm,
# Lichteiland); dit script levert nog de vuurtoren-tileset, 1F/2F, de trainers, de wilde tabel en de mapsec.


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




# ====================================================================== mapsecs, popups
MAPSECS = [('MAPSEC_BEACON_ISLE', 'BEACON ISLE', 14, 11, 1, 1, 'MAPPOPUP_THEME_MARBLE', 'vuurtoreneiland')]


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
STADIUM = [('WICK', 'WICK', 'EXPERT_M', "WICK! Forty years a lighthouse keeper. His lamp is a fish. It works.")]


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
    check_levels.restore()  # levels eerst terug, pool.py leest trainers.party
    subprocess.run([sys.executable, 'tools/grounded/stadium/pool.py'], check=True)
    subprocess.run([sys.executable, 'tools/grounded/stadium/announcer.py'], check=True)


# ====================================================================== main
if __name__ == '__main__':
    flags()
    beam_graphics()
    lighthouse_tileset()
    names = [lighthouse_1f(), lighthouse_2f()]  # Beacon Isle: beacon_isle.py; Tao-eiland: tao_island.py
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
