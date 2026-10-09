"""Project Grounded: Chargestone Cave (Spacetime Cave-sidequest; Unova in een andere tijd).

Drie kaarten (gMapGroup_Spacetime, achteraan), Meteor Falls-vormen met een donkerblauwe tint en zwevende
magneetstenen (chargestone_tiles.py):
  ChargestoneCave_1F   Ingang (warp 0 = terug naar de Spacetime Cave; hier komt de hub-scheur uit), grote hal,
                       oostkamer met de ladder naar B1F, zijgrot achter een duwsteen (Strength).
  ChargestoneCave_B1F  Grote grot; de ladder naar B2F staat achter een hek van zwevende stenen: twee duwstenen
                       (licht puzzelpad, door dit script met een Sokoban-BFS gecontroleerd).
  ChargestoneCave_B2F  Colress' lab: zijn machine tapt de stroom van ZERAORA af. Verslaat je hem, dan gaat de
                       machine uit en verschijnt ZERAORA achterin (lv 70, legendary-gevecht).
Quest: vier Neo Plasma-assistenten (lv 66-70) + COLRESS (andere dimensie: kent je niet, is hier wél evil, lv 72-75).
Klaar-flag: FLAG_SPACETIME_CHARGESTONE_DONE (Zeraora gevangen of verslagen).
Extra: mapsec MAPSEC_CHARGESTONE_CAVE is een magnetisch veld: Magneton -> Magnezone, Charjabug -> Vikavolt.
Flags FLAG_GROUNDED 760-799, trainers 1124-1128.
Teksten zijn placeholders (Jordi herschrijft ze).
Gebruik: python3 tools/grounded/maptools/chargestone.py [render-uitmap]"""
import json, os, random, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import meteor_falls_ext as mf          # werkmap = repo-root
import victory_road_ext as vre
import beacon_dragon as bd
import chargestone_tiles as ct

os.chdir(ct.REPO)
Scr, text = bd.Scr, bd.text
cell = mf.cell
E = mf.E_FLOOR
ID = ct.ids()
PRIM, SEC = 'gTileset_ChargestoneGeneral', 'gTileset_Chargestone'
GROUP = 'gMapGroup_Spacetime'
F1, B1, B2 = 'ChargestoneCave_1F', 'ChargestoneCave_B1F', 'ChargestoneCave_B2F'
MUSIC = 'MUS_RG_SEVII_CAVE'

# ====================================================================== flags (FLAG_GROUNDED 760-799)
FLAGS = [
    (760, 'FLAG_SPACETIME_CHARGESTONE_DONE', 'Chargestone Cave: ZERAORA gevangen of verslagen (klaar-flag sidequest)'),
    (761, 'FLAG_HIDE_CHARGESTONE_ZERAORA', 'Chargestone Cave B2F: ZERAORA verborgen (voor Colress verslagen is of na het gevecht)'),
    (762, 'FLAG_HIDE_CHARGESTONE_COLRESS', 'Chargestone Cave B2F: Colress weg (na ZERAORA)'),
    (763, 'FLAG_ITEM_CHARGESTONE_1F_THUNDER_STONE', 'Chargestone Cave 1F: Thunder Stone'),
    (764, 'FLAG_ITEM_CHARGESTONE_1F_MAX_REVIVE', 'Chargestone Cave 1F: Max Revive (zijgrot achter de duwsteen)'),
    (765, 'FLAG_ITEM_CHARGESTONE_B1F_MAGNET', 'Chargestone Cave B1F: Magnet'),
    (766, 'FLAG_ITEM_CHARGESTONE_B1F_METAL_COAT', 'Chargestone Cave B1F: Metal Coat'),
    (767, 'FLAG_ITEM_CHARGESTONE_B2F_ELECTIRIZER', 'Chargestone Cave B2F: Electirizer'),
    (768, 'FLAG_ITEM_CHARGESTONE_B2F_PP_MAX', 'Chargestone Cave B2F: PP Max'),
    (769, 'FLAG_HIDDEN_ITEM_CHARGESTONE_1F_CELL_BATTERY', 'Chargestone Cave 1F: verborgen Cell Battery'),
    (770, 'FLAG_HIDDEN_ITEM_CHARGESTONE_B1F_BIG_NUGGET', 'Chargestone Cave B1F: verborgen Big Nugget'),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// chargestone { (tools/grounded/maptools/chargestone.py; FLAG_GROUNDED 760-799, 771-799 nog vrij)\n'
    for n, name, why in FLAGS:
        assert 760 <= n <= 799
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// chargestone {' in s:
        i = s.index('// chargestone {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// mega_forest {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    s = s.replace('620-659 Mega Forest (mega_forest.py), 660+ vrij.',
                  '620-659 Mega Forest (mega_forest.py), 760-799 Chargestone Cave (chargestone.py), 660+ vrij '
                  '(behalve 760-799).')
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== kaarten
def const(name):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper().replace('CAVE_1_F', 'CAVE_1F')


CONST = {F1: 'CHARGESTONE_CAVE_1F', B1: 'CHARGESTONE_CAVE_B1F', B2: 'CHARGESTONE_CAVE_B2F'}


class Cave(mf.Map):
    """Meteor Falls-autotiler + zwevende stenen (2x2, 'S'), scherven en vonkjes (na build als overrides)."""

    def __init__(self, w, h, seed):
        super().__init__(w, h)
        self.rnd = random.Random(seed)
        self.stones = []

    def stone(self, x, y, kind=None):
        kind = kind or self.rnd.choice(('stoneA', 'stoneA_f', 'stoneB', 'stoneB_f'))
        for i, m in enumerate(ID[kind]):
            self.set(x + i % 2, y + i // 2, m, 1)
        self.stones.append((x, y))

    def shard(self, x, y):
        self.set(x, y, ID['shard'][0], 1)

    def sparks(self, n, area, keep):
        x0, y0, x1, y1 = area
        tries = 0
        while n and tries < 400:
            tries += 1
            x, y = self.rnd.randint(x0, x1), self.rnd.randint(y0, y1)
            if self.k[y][x] != 'F' or (x, y) in self.over or (x, y) in keep:
                continue
            self.set(x, y, ID[self.rnd.choice(('spark1', 'spark2'))][0], 0); n -= 1

    def build(self):
        g = super().build()
        dark = {mf.LIP_N: 'lipD', mf.EDGE_E: 'edgeED', mf.EDGE_W: 'edgeWD'}
        for y in range(self.H):
            for x in range(self.W):
                if self.k[y][x] != 'R' or (x, y) in self.over:
                    continue
                v = g[y][x] & 0x3FF
                if v in dark:
                    g[y][x] = cell(ID[dark[v]][0], 1, 0)
                elif v == mf.ROCK:
                    g[y][x] = cell(ID['rockD'][0], 1, 0)
                elif v == mf.LIP_S1:
                    up = y > 0 and self.k[y - 1][x] in 'FW'
                    g[y][x] = cell(ID['rimSD' if up else 'rockD'][0], 1, 0)
        # rots die verder dan 3 van elke vloer ligt = donkere leegte (zoals de echte Chargestone Cave)
        for y in range(self.H):
            for x in range(self.W):
                if self.k[y][x] == 'R' and (x, y) not in self.over and not any(
                        self.isF(x + a, y + b) for a in range(-3, 4) for b in range(-3, 4)):
                    g[y][x] = cell(ID['rockD'][0], 1, 0)
        return g

    def ladder(self, x, y):
        self.set(x, y, mf.LADDER, 0)


def stones_ok(m, keep):
    for (x, y) in m.stones:
        for dx in (0, 1):
            for dy in (0, 1):
                assert m.k[y + dy][x + dx] == 'F', ('steen op rots', x, y)
                assert (x + dx, y + dy) not in keep, ('steen op een event', x, y)


# --------------------------------------------------------------------- 1F
F1_EXIT = (11, 34)           # zuiduitgang = terug naar de Spacetime Cave (warp 0)
F1_LADDER = (42, 30)         # ladder naar B1F (warp 1)
F1_BOULDER = (21, 30)
F1_TRAINER = (16, 12)
F1_TRAINER2 = (39, 9)
F1_ITEMS = [((6, 7), 'THUNDER_STONE', 'FLAG_ITEM_CHARGESTONE_1F_THUNDER_STONE'),
            ((28, 32), 'MAX_REVIVE', 'FLAG_ITEM_CHARGESTONE_1F_MAX_REVIVE')]
F1_HIDDEN = ((44, 6), 'CELL_BATTERY', 'FLAG_HIDDEN_ITEM_CHARGESTONE_1F_CELL_BATTERY')
F1_SIGN = (12, 26)


def build_1f():
    m = Cave(50, 40, 7101)
    m.room(5, 27, 18, 34)          # ingangshal
    m.room(8, 19, 10, 26)          # gang omhoog
    m.room(5, 6, 27, 18)           # grote hal
    m.room(12, 4, 21, 5)           # inham noord
    m.room(28, 11, 34, 13)         # gang oost
    m.room(35, 5, 45, 17)          # oostkamer boven
    m.room(39, 18, 41, 22)         # gang omlaag
    m.room(35, 23, 45, 31)         # oostkamer onder (ladder)
    m.room(19, 29, 24, 31)         # gang naar de zijgrot (scherven + duwsteen)
    m.room(25, 26, 29, 33)         # zijgrot
    m.build()
    m.exit_south(*F1_EXIT)
    m.ladder(*F1_LADDER)
    keep = {F1_EXIT, (11, 33), (11, 32), F1_LADDER, (42, 29), (41, 30), F1_BOULDER, (20, 30), (22, 30), (23, 30),
            F1_TRAINER, F1_TRAINER2, F1_SIGN, (12, 27), F1_HIDDEN[0]} | {p for p, *_ in F1_ITEMS}
    for x in range(8, 11):
        keep |= {(x, 18), (x, 17), (x, 27)}
    for y in range(11, 14):
        keep |= {(27, y), (35, y)}
    for x in range(39, 42):
        keep |= {(x, 17), (x, 23)}
    # sight lines
    keep |= {(16, y) for y in range(13, 17)} | {(x, 9) for x in range(36, 39)}
    for (x, y) in [(7, 9), (20, 8), (24, 14), (13, 15), (6, 15), (22, 10), (37, 14), (43, 12), (36, 25), (44, 24),
                   (15, 29), (6, 30), (26, 27)]:
        m.stone(x, y)
    for (x, y) in [(12, 8), (18, 16), (26, 7), (44, 16), (38, 28), (17, 33), (35, 6), (21, 29), (21, 31)]:
        m.shard(x, y)
    m.sparks(28, (5, 5, 45, 34), keep)
    stones_ok(m, keep)
    return m, m.build()


# --------------------------------------------------------------------- B1F
B1_ARRIVE = (12, 36)         # ladder omhoog (warp 0) = waar je vanuit 1F aankomt
B1_LADDER = (12, 8)          # ladder naar B2F (warp 1), achter het stenenhek
B1_FENCE_Y = 13              # hek: stenen op rij 12-13, gaten met duwstenen
B1_BOULDERS = [(9, 13), (17, 13)]
B1_TRAINERS = [(19, 18), (44, 30)]   # westhal (kijkt naar links), grote grot
B1_TRAINER_N = (40, 9)               # noordkamer: geen trainer, wel de Magnet
B1_ITEMS = [((46, 6), 'MAGNET', 'FLAG_ITEM_CHARGESTONE_B1F_MAGNET'),
            ((6, 6), 'METAL_COAT', 'FLAG_ITEM_CHARGESTONE_B1F_METAL_COAT')]
B1_HIDDEN = ((38, 40), 'BIG_NUGGET', 'FLAG_HIDDEN_ITEM_CHARGESTONE_B1F_BIG_NUGGET')


def build_b1f():
    m = Cave(54, 46, 7202)
    m.room(5, 30, 20, 40)          # aankomsthal
    m.room(14, 23, 16, 29)         # gang omhoog naar de westhal
    m.room(21, 33, 29, 35)         # gang oost
    m.room(30, 24, 48, 41)         # grote grot
    m.room(32, 22, 37, 23)         # inham noord
    m.room(42, 15, 44, 23)         # gang omhoog
    m.room(28, 5, 48, 14)          # noordkamer
    m.room(5, 5, 22, 22)           # westhal met het hek
    m.room(9, 3, 17, 4)            # inham achter het hek
    m.build()
    m.ladder(*B1_ARRIVE)
    m.ladder(*B1_LADDER)
    # hek van zwevende stenen (rij 12-13) over de hele westhal, met twee gaten (duwstenen)
    gaps = {x for x, _ in B1_BOULDERS}
    x = 5
    while x <= 22:
        if x in gaps:
            x += 1
            continue
        if x + 1 <= 22 and x + 1 not in gaps:
            m.stone(x, B1_FENCE_Y - 1); x += 2
        else:
            m.shard(x, B1_FENCE_Y); m.shard(x, B1_FENCE_Y - 1); x += 1
    keep = {B1_ARRIVE, (12, 35), (12, 37), B1_LADDER, (12, 9), (12, 7)} | set(B1_TRAINERS) | {p for p, *_ in B1_ITEMS}
    keep |= {B1_HIDDEN[0]}
    for (bx, by) in B1_BOULDERS:
        keep |= {(bx, by + 1), (bx, by - 1), (bx, by - 2), (bx, by - 3), (bx, by + 2)}
    keep |= {(x, 9) for x in range(28, 40)} | {(44, y) for y in range(31, 35)} | {(x, 18) for x in range(15, 19)}
    for y in range(33, 36):
        keep |= {(20, y), (21, y), (29, y), (30, y)}
    for x in range(42, 45):
        keep |= {(x, 14), (x, 15), (x, 23), (x, 24)}
    for x in range(14, 17):
        keep |= {(x, 22), (x, 23), (x, 29), (x, 30)}
    for (x, y) in [(7, 31), (17, 38), (6, 37), (33, 26), (46, 27), (32, 38), (45, 37), (31, 7), (36, 11), (47, 11),
                   (7, 17), (20, 20), (10, 20), (19, 6), (8, 7), (37, 31), (40, 35)]:
        m.stone(x, y)
    for (x, y) in [(17, 32), (35, 28), (47, 39), (34, 12), (6, 21), (21, 15), (15, 6)]:
        m.shard(x, y)
    m.sparks(32, (5, 5, 48, 40), keep | {(x, y) for x in range(5, 23) for y in range(11, 15)})
    stones_ok(m, keep)
    return m, m.build()


# --------------------------------------------------------------------- B2F
B2_ARRIVE = (10, 33)         # ladder omhoog (warp 0)
B2_COLRESS = (25, 10)
B2_MACHINE = (24, 7)         # 2x2 'machine' = een zwevende steen met een bord (sign)
B2_ZERAORA = (25, 5)         # verschijnt achter de machine, achterin de hal
B2_TRAINERS = [(30, 27), (33, 17)]
B2_ITEMS = [((38, 33), 'ELECTIRIZER', 'FLAG_ITEM_CHARGESTONE_B2F_ELECTIRIZER'),
            ((11, 6), 'PP_MAX', 'FLAG_ITEM_CHARGESTONE_B2F_PP_MAX')]


def build_b2f():
    m = Cave(46, 40, 7303)
    m.room(6, 28, 18, 35)          # aankomst
    m.room(19, 30, 26, 32)         # gang
    m.room(27, 20, 40, 35)         # middenkamer
    m.room(32, 14, 34, 19)         # gang omhoog
    m.room(9, 4, 40, 13)           # Colress' hal
    m.room(18, 3, 32, 3)           # achterwand iets dieper (ZERAORA)
    m.build()
    m.ladder(*B2_ARRIVE)
    keep = {B2_ARRIVE, (10, 32), (10, 34), B2_COLRESS, (25, 11), (25, 12), (25, 9), (24, 9), (26, 9)} | set(B2_TRAINERS)
    keep |= {p for p, *_ in B2_ITEMS} | {(25, 5), (25, 4), (26, 5), (24, 5)}
    keep |= {(30, y) for y in range(22, 27)} | {(33, y) for y in range(18, 20)} | {(x, 17) for x in range(32, 35)}
    for y in range(30, 33):
        keep |= {(18, y), (19, y), (26, y), (27, y)}
    for x in range(32, 35):
        keep |= {(x, 13), (x, 14), (x, 19), (x, 20)}
    # de machine: drie stenen in een boog rond Colress' werkplek
    m.stone(21, 7, 'stoneA'); m.stone(28, 7, 'stoneA_f'); m.stone(24, 7, 'stoneB')
    for (x, y) in [(7, 29), (15, 33), (29, 33), (38, 22), (36, 30), (12, 9), (36, 5), (17, 5), (31, 10)]:
        m.stone(x, y)
    for (x, y) in [(20, 9), (30, 9), (14, 12), (39, 12), (28, 21), (17, 29)]:
        m.shard(x, y)
    m.sparks(26, (6, 4, 40, 35), keep)
    stones_ok(m, keep)
    return m, m.build()


# ====================================================================== registratie
def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"%s": [' % GROUP); j = g.index('\n  ]', i)
        body = g[i:j]
        sep = ',' if body.rstrip().endswith('"') else ''
        g = g[:j] + sep + '\n    "%s"' % name + g[j:]
    d = json.loads(g)
    assert len(d[GROUP]) <= 128
    open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/SpacetimeCave/scripts.inc"\n'
        if anchor not in es:
            anchor = '\t.include "data/maps/MangroveMire/scripts.inc"\n'
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def save(name, g):
    W, H = len(g[0]), len(g)
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', t) for r in g for t in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack("<4H", *([cell(ID["rockD"][0], 1, 0)] * 4)))
    bd.register_layout(name, CONST[name], W, H, PRIM, SEC)


def write_map(name, objs, warps, bgs, coords=(), head=None):
    m = {'id': 'MAP_' + CONST[name], 'name': name, 'layout': 'LAYOUT_' + CONST[name], 'music': MUSIC,
         'region_map_section': 'MAPSEC_CHARGESTONE_CAVE', 'requires_flash': False, 'weather': 'WEATHER_NONE',
         'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': True, 'allow_running': True,
         'show_map_name': name == F1, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
         'object_events': objs, 'warp_events': warps, 'coord_events': list(coords), 'bg_events': bgs}
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    register_map(name)


warp, obj, tr, ball, sign = bd.warp, bd.obj, bd.tr, bd.ball, bd.sign


def hidden(xy, it, flag):
    return {'type': 'hidden_item', 'x': xy[0], 'y': xy[1], 'elevation': 3, 'item': 'ITEM_' + it, 'flag': flag}


def boulder(x, y):
    return obj('OBJ_EVENT_GFX_PUSHABLE_BOULDER', x, y, 'EventScript_StrengthBoulder', '0', 'MOVEMENT_TYPE_LOOK_AROUND')


def render(name, out):
    H = len(MAPS[name][1])
    subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', name, out, '0', str(H)], check=True)


MAPS = {}


def build_maps():
    for name, fn in ((F1, build_1f), (B1, build_b1f), (B2, build_b2f)):
        m, g = fn()
        MAPS[name] = (m, g)
        save(name, g)


# ====================================================================== trainers (1124-1128)
mon, AI, AI_BOSS = bd.mon, bd.AI, bd.AI_BOSS
TRAINERS = [  # (sleutel, id, naam, klasse, pic, gender, music, ai, mugshot, team, waarom)
    ('CHARGESTONE_GRUNT_1F', 1124, 'GRUNT', 'Neo Plasma', 'Neo Plasma Grunt M', 'Male', 'Suspicious', AI, None, [
        mon('Klinklang', 66, ['Gear Grind', 'Wild Charge', 'Shift Gear', 'Screech']),
        mon('Eelektross', 66, ['Wild Charge', 'Crunch', 'Drain Punch', 'Flamethrower']),
        mon('Galvantula', 66, ['Thunder', 'Bug Buzz', 'Sticky Web', 'Energy Ball'])],
     'Chargestone Cave 1F, Colress-assistent'),
    ('CHARGESTONE_GRUNT_B1F_1', 1125, 'GRUNT', 'Neo Plasma', 'Neo Plasma Grunt F', 'Female', 'Suspicious', AI, None, [
        mon('Rotom_Wash', 67, ['Hydro Pump', 'Thunderbolt', 'Will-O-Wisp', 'Volt Switch']),
        mon('Heliolisk', 67, ['Parabolic Charge', 'Grass Knot', 'Surf', 'Volt Switch']),
        mon('Ferrothorn', 67, ['Power Whip', 'Gyro Ball', 'Leech Seed', 'Spikes'])],
     'Chargestone Cave B1F, Colress-assistent bij het stenenhek'),
    ('CHARGESTONE_GRUNT_B1F_2', 1126, 'GRUNT', 'Neo Plasma', 'Neo Plasma Grunt M', 'Male', 'Suspicious', AI, None, [
        mon('Kingambit', 68, ['Kowtow Cleave', 'Iron Head', 'Sucker Punch', 'Swords Dance']),
        mon('Magnezone', 68, ['Thunderbolt', 'Flash Cannon', 'Volt Switch', 'Mirror Coat']),
        mon('Golurk', 68, ['Earthquake', 'Shadow Punch', 'Dynamic Punch', 'Ice Punch'])],
     'Chargestone Cave B1F, Colress-assistent in de grote grot'),
    ('CHARGESTONE_GRUNT_B2F', 1127, 'GRUNT', 'Neo Plasma', 'Neo Plasma Grunt F', 'Female', 'Suspicious', AI, None, [
        mon('Electivire', 69, ['Wild Charge', 'Ice Punch', 'Cross Chop', 'Earthquake']),
        mon('Probopass', 69, ['Power Gem', 'Flash Cannon', 'Earth Power', 'Thunder Wave']),
        mon('Bronzong', 69, ['Gyro Ball', 'Earthquake', 'Trick Room', 'Psychic']),
        mon('Vikavolt', 70, ['Bug Buzz', 'Thunderbolt', 'Energy Ball', 'Sticky Web'])],
     'Chargestone Cave B2F, Colress-assistent voor het lab'),
    ('CHARGESTONE_COLRESS', 1128, 'COLRESS', 'Scientist', 'Colress', 'Male', 'Intense', AI_BOSS, 'Blue', [
        mon('Rotom_Heat', 72, ['Overheat', 'Thunderbolt', 'Will-O-Wisp', 'Volt Switch']),
        mon('Porygon_Z', 73, ['Tri Attack', 'Thunderbolt', 'Ice Beam', 'Nasty Plot']),
        mon('Metagross', 73, ['Meteor Mash', 'Zen Headbutt', 'Earthquake', 'Bullet Punch']),
        mon('Copperajah', 73, ['Iron Head', 'Heavy Slam', 'Earthquake', 'Play Rough']),
        mon('Archaludon', 74, ['Electro Shot', 'Flash Cannon', 'Draco Meteor', 'Body Press']),
        mon('Genesect @ Shock Drive', 75, ['Techno Blast', 'U-turn', 'Iron Head', 'Shift Gear'])],
     'Chargestone Cave B2F, COLRESS uit een andere dimensie (hier wel evil)'),
]


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = '// chargestone { (tools/grounded/maptools/chargestone.py; id 1124-1128)\n'
    for key, n, *_, why in TRAINERS:
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (key, n, why)
    blk += '// }'
    if '// chargestone {' in s:
        i = s.index('// chargestone {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for key, n, *_ in TRAINERS:
        hits = re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)
        assert len(hits) == 1, ('trainer-id dubbel', n, hits)
    open(p, 'w').write(s)
    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- chargestone (tools/grounded/maptools/chargestone.py) --- */\n\n'
    for key, n, nm, cls, pic, gender, music, ai, mug, team, why in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music,
               'Double Battle: No', ai] + (['Mugshot: ' + mug] if mug else [])
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (key, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde chargestone --- */'
    s = bd.replace_block(s, '/* --- chargestone', '/* --- einde chargestone --- */', blk)
    open(p, 'w').write(s)


# ====================================================================== wilde Pokemon
WILD = {
    'CHARGESTONE_CAVE_1F': dict(land=(8, [
        ('GALVANTULA', 60, 62), ('BOLDORE', 60, 62), ('KLINKLANG', 60, 62), ('EELEKTRIK', 60, 62),
        ('FERROTHORN', 60, 62), ('MAGNETON', 60, 62), ('DURANT', 61, 63), ('ZEBSTRIKA', 61, 63),
        ('EMOLGA', 61, 63), ('BRONZONG', 61, 63), ('PROBOPASS', 62, 63), ('ROTOM', 62, 63)])),
    'CHARGESTONE_CAVE_B1F': dict(land=(8, [
        ('GALVANTULA', 62, 64), ('GIGALITH', 62, 64), ('EELEKTRIK', 62, 64), ('KLINKLANG', 62, 64),
        ('MAGNETON', 62, 64), ('HELIOLISK', 62, 64), ('CARBINK', 63, 65), ('EXCADRILL', 63, 65),
        ('ESCAVALIER', 63, 65), ('FERROTHORN', 63, 65), ('EELEKTROSS', 64, 65), ('TOGEDEMARU', 64, 65)])),
    'CHARGESTONE_CAVE_B2F': dict(land=(8, [
        ('GALVANTULA', 64, 66), ('GIGALITH', 64, 66), ('EELEKTRIK', 64, 66), ('MAGNETON', 64, 66),
        ('BRONZONG', 64, 66), ('EXCADRILL', 64, 66), ('BISHARP', 65, 67), ('PROBOPASS', 65, 67),
        ('VIKAVOLT', 65, 67), ('GOLURK', 65, 67), ('EELEKTROSS', 66, 67), ('ROTOM', 66, 67)])),
}


def wild():
    for mp, tabs in WILD.items():
        assert len({x[0] for x in tabs['land'][1]}) == 12, mp
    bd.WILD = WILD
    bd.wild()


# ====================================================================== mapsec, evolutie, gevechtsstart
def mapsecs():
    bd.MAPSECS[:] = [('MAPSEC_CHARGESTONE_CAVE', 'CHARGESTONE CAVE', 26, 4, 1, 1, 'MAPPOPUP_THEME_STONE',
                      'Chargestone Cave (Spacetime)')]
    bd.mapsecs()


EVOS = [('src/data/pokemon/species_info/gen_1_families.h', 'SPECIES_MAGNEZONE'),
        ('src/data/pokemon/species_info/gen_7_families.h', 'SPECIES_VIKAVOLT')]


def evolutions():
    """Magnetisch veld: Magneton en Charjabug evolueren ook door een level-up in Chargestone Cave.
    (Nosepass evolueert in dit project al gewoon op lv 30.)"""
    for p, sp in EVOS:
        s = open(p).read()
        old = '{EVO_LEVEL, 0, %s, CONDITIONS({IF_IN_MAPSEC, MAPSEC_NEW_MAUVILLE})},' % sp
        add = ('\n                                {EVO_LEVEL, 0, %s, CONDITIONS({IF_IN_MAPSEC, MAPSEC_CHARGESTONE_CAVE})}, '
               '// Project Grounded: magnetisch veld (chargestone.py)' % sp)
        assert old in s
        if old + add not in s:
            s = s.replace(old, old + add, 1)
        open(p, 'w').write(s)


def battle_setup():
    p = 'src/battle_setup.c'
    s = open(p).read()
    if 'case SPECIES_ZERAORA' not in s:
        a = '    case SPECIES_VOLCANION:'
        assert a in s
        s = s.replace(a, '    case SPECIES_ZERAORA: // Project Grounded: Chargestone Cave (placeholder: Kanto-legendary-thema, '
                         'bestaande transitie)\n        CreateBattleStartTask(B_TRANSITION_ANGLED_WIPES, MUS_RG_VS_LEGEND);\n'
                         '        break;\n' + a, 1)
        open(p, 'w').write(s)


# ====================================================================== events en scripts
def tr_obj(gfx, xy, face, sight, script):
    return bd.tr(gfx, xy[0], xy[1], script, face, sight)


def head(name, scripts=()):
    h = '@ Project Grounded: %s (tools/grounded/maptools/chargestone.py)\n%s_MapScripts::\n' % (name, name)
    for kind, lbl in scripts:
        h += '\tmap_script %s, %s\n' % (kind, lbl)
    return h + '\t.byte 0\n'


HUB_DEST = ('SPACETIME_CAVE', 0)   # bij het samenvoegen: de warp-index van de Chargestone-scheur in de hub


def events():
    # ---------------------------------------------------------------- 1F
    S = Scr(F1, head(F1))
    g1 = S.trainer('Grunt', 'CHARGESTONE_GRUNT_1F',
                   "Halt! This cave is property of TEAM PLASMA's research division.\n\n"
                   "Which is one man. And us. We're the division's legs.",
                   "My legs have been defeated.",
                   "COLRESS? Nice? Who told you that?\n\nThe man once fired an intern for saying 'good morning' "
                   "without a hypothesis.")
    S.npc('Plaque', "CHARGESTONE CAVE\n\nThe stones float because of magnetism. Do not lick the stones.\n\n"
          "Someone has added in marker: 'the stones float because of ZERAORA. Lick at own risk.'", 'MSGBOX_SIGN')
    S.write()
    objs = [tr_obj('OBJ_EVENT_GFX_NEO_PLASMA_GRUNT_M', F1_TRAINER, 'DOWN', 4, g1)]
    objs += [ball(xy[0], xy[1], 'ITEM_' + it, fl) for xy, it, fl in F1_ITEMS]
    objs += [boulder(*F1_BOULDER)]
    warps = [warp(F1_EXIT[0], F1_EXIT[1], HUB_DEST[0], HUB_DEST[1], elev=3),
             warp(F1_LADDER[0], F1_LADDER[1], CONST[B1], 0, elev=3)]
    bgs = [sign(F1_SIGN[0], F1_SIGN[1], S.P + 'Plaque', 'BG_EVENT_PLAYER_FACING_NORTH'), hidden(*F1_HIDDEN)]
    write_map(F1, objs, warps, bgs)
    # ---------------------------------------------------------------- B1F
    S = Scr(B1, head(B1))
    a = S.trainer('GruntFence', 'CHARGESTONE_GRUNT_B1F_1',
                  "You found the fence! We built it out of floating rocks. Very modern.\n\n"
                  "It's also the only fence in the world you can push over. We're working on that.",
                  "The fence was a metaphor anyway.",
                  "Push the stones in the gaps. Or don't. I'm not your supervisor. My supervisor is evil.")
    b = S.trainer('GruntCavern', 'CHARGESTONE_GRUNT_B1F_2',
                  "Every rock in here hums at fifty hertz. So do I, after three weeks of overtime.",
                  "Bzzt. That's me, short-circuiting emotionally.",
                  "COLRESS says the cave runs on a ZERAORA now. I asked what it ran on before.\n\n"
                  "He said 'ignorance' and docked my pay.")
    S.write()
    objs = [tr_obj('OBJ_EVENT_GFX_NEO_PLASMA_GRUNT_F', B1_TRAINERS[0], 'LEFT', 4, a),
            tr_obj('OBJ_EVENT_GFX_NEO_PLASMA_GRUNT_M', B1_TRAINERS[1], 'DOWN', 4, b)]
    objs += [ball(xy[0], xy[1], 'ITEM_' + it, fl) for xy, it, fl in B1_ITEMS]
    objs += [boulder(*xy) for xy in B1_BOULDERS]
    warps = [warp(B1_ARRIVE[0], B1_ARRIVE[1], CONST[F1], 1, elev=3),
             warp(B1_LADDER[0], B1_LADDER[1], CONST[B2], 0, elev=3)]
    write_map(B1, objs, warps, [hidden(*B1_HIDDEN)])
    # ---------------------------------------------------------------- B2F
    S = Scr(B2, head(B2, [('MAP_SCRIPT_ON_TRANSITION', B2 + '_OnTransition')]))
    P, T = S.P, S.T
    c = S.trainer('Grunt', 'CHARGESTONE_GRUNT_B2F',
                  "The lab is through here. Please wipe your feet. The floor is load-bearing AND current-bearing.",
                  "My shoes are smoking. That's new.",
                  "When the machine is on, ZERAORA screams at a frequency only POKéMON can hear.\n\n"
                  "We wear earplugs anyway. Solidarity.")
    S.npc('Machine', "A floating stone wired to a laptop. The screen reads:\n\n"
          "ZERAORA OUTPUT: 98%.\nZERAORA MOOD: no.\nETHICS MODULE: not found.", 'MSGBOX_SIGN')
    S.raw(f"""{B2}_OnTransition:
	setflag FLAG_HIDE_CHARGESTONE_ZERAORA
	goto_if_set FLAG_SPACETIME_CHARGESTONE_DONE, {P}OnTransitionEnd
	goto_if_not_defeated TRAINER_CHARGESTONE_COLRESS, {P}OnTransitionEnd
	clearflag FLAG_HIDE_CHARGESTONE_ZERAORA
{P}OnTransitionEnd:
	end

{P}Colress::
	lock
	faceplayer
	goto_if_defeated TRAINER_CHARGESTONE_COLRESS, {P}ColressAfter
	msgbox {T}ColressIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_CHARGESTONE_COLRESS, {T}ColressDefeat
	msgbox {T}ColressShutdown, MSGBOX_DEFAULT
	closemessage
	playse SE_THUNDER
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 10
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	special SpawnCameraObject
	applymovement OBJ_EVENT_ID_CAMERA, {P}Movement_CameraUp
	waitmovement 0
	clearflag FLAG_HIDE_CHARGESTONE_ZERAORA
	addobject LOCALID_CHARGESTONE_ZERAORA
	playse SE_M_THUNDERBOLT
	playmoncry SPECIES_ZERAORA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox {T}ZeraoraFree, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_CAMERA, {P}Movement_CameraDown
	waitmovement 0
	special RemoveCameraObject
	release
	end

{P}Movement_CameraUp:
	walk_slow_up
	walk_slow_up
	walk_slow_up
	step_end

{P}Movement_CameraDown:
	walk_down
	walk_down
	walk_down
	step_end

{P}ColressAfter::
	goto_if_set FLAG_SPACETIME_CHARGESTONE_DONE, {P}ColressDone
	msgbox {T}ColressAfter, MSGBOX_DEFAULT
	release
	end

{P}ColressDone::
	msgbox {T}ColressDone, MSGBOX_DEFAULT
	release
	end

{P}Zeraora::
	lock
	faceplayer
	playmoncry SPECIES_ZERAORA, CRY_MODE_ENCOUNTER
	msgbox {T}Zeraora, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_ZERAORA, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}ZeraoraStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}ZeraoraStays
	removeobject LOCALID_CHARGESTONE_ZERAORA
	setflag FLAG_HIDE_CHARGESTONE_ZERAORA
	setflag FLAG_SPACETIME_CHARGESTONE_DONE
	msgbox {T}CaveCalm, MSGBOX_DEFAULT
{P}ZeraoraStays::
	release
	end
""", [('ColressIntro', "COLRESS: ...Why are you looking at me like that? Do I know you?\n\n"
                           "...I'm not evil? Where on earth did you hear that?\n\n"
                           "Parallel dimensions. While I do not dispute the possibility, it doesn't change my "
                           "current standing.\n\n"
                           "Here, I am evil, and I am very good at it. My machine drains ZERAORA's current into "
                           "the cave. The rocks float. The lights stay on. ZERAORA has some notes.\n\n"
                           "You came all this way to switch it off? Wonderful. A control group!"),
          ('ColressDefeat', "Fascinating. You reduced my output by exactly one hundred percent."),
          ('ColressShutdown', "COLRESS: The machine is overloading. It appears it relied on my POKéMON "
                              "not losing.\n\nA design flaw. I'll fix it in the next dimension.\n\n"
                              "Ah. And there goes the battery."),
          ('ZeraoraFree', "The floating stones drop a few inches all at once.\n\n"
                          "Something at the back of the lab stretches, crackles, and turns to look at you."),
          ('ColressAfter', "COLRESS: Go on, then. It's free, it's furious, and it is standing right behind my "
                           "machine.\n\nI'd love the data. Try not to become part of it."),
          ('ColressDone', "COLRESS: The cave runs on plain old magnetism again. Dreadfully natural.\n\n"
                          "In your dimension I'm the nice one? Tell him he's wasting his potential."),
          ('Zeraora', "ZERAORA: Grrrah!\n\nIts fur is standing on end. So is yours."),
          ('CaveCalm', "The hum in the walls fades to a gentle buzz.\n\nCHARGESTONE CAVE runs on its own "
                       "again.")])
    S.write()
    objs = [tr_obj('OBJ_EVENT_GFX_NEO_PLASMA_GRUNT_F', B2_TRAINERS[0], 'DOWN', 4, c),
            obj('OBJ_EVENT_GFX_COLRESS', B2_COLRESS[0], B2_COLRESS[1], P + 'Colress', 'FLAG_HIDE_CHARGESTONE_COLRESS',
                move='MOVEMENT_TYPE_FACE_UP', local_id='LOCALID_CHARGESTONE_COLRESS'),
            obj('OBJ_EVENT_GFX_SPECIES(ZERAORA)', B2_ZERAORA[0], B2_ZERAORA[1], P + 'Zeraora',
                'FLAG_HIDE_CHARGESTONE_ZERAORA', move='MOVEMENT_TYPE_FACE_DOWN', local_id='LOCALID_CHARGESTONE_ZERAORA')]
    objs += [ball(xy[0], xy[1], 'ITEM_' + it, fl) for xy, it, fl in B2_ITEMS]
    warps = [warp(B2_ARRIVE[0], B2_ARRIVE[1], CONST[B1], 1, elev=3)]
    bgs = [sign(B2_MACHINE[0] + dx, B2_MACHINE[1] + 1, P + 'Machine', 'BG_EVENT_PLAYER_FACING_NORTH') for dx in (0, 1)]
    write_map(B2, objs, warps, bgs)


# ====================================================================== controles
FACE = {'DOWN': (0, 1), 'UP': (0, -1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}


def checks():
    for name in MAPS:
        g = MAPS[name][1]
        d = json.load(open('data/maps/%s/map.json' % name))
        objs = d['object_events']
        start = (d['warp_events'][0]['x'], d['warp_events'][0]['y'])
        solid = {(o['x'], o['y']) for o in objs} - {start}
        boulders = {(o['x'], o['y']) for o in objs if 'BOULDER' in o['graphics_id']}
        r_all = mf.reachable(g, start, solid - boulders)          # duwstenen weg = na het duwen
        for o in objs:
            p = (o['x'], o['y'])
            assert mf.next_to(r_all, *p) or p in r_all, (name, 'object onbereikbaar', o['script'], p)
            if o['trainer_type'] == 'TRAINER_TYPE_NORMAL':
                dx, dy = FACE[o['movement_type'].split('_')[-1]]
                for k in range(1, int(o['trainer_sight_or_berry_tree_id']) + 1):
                    assert (o['x'] + dx * k, o['y'] + dy * k) in r_all, (name, 'zichtlijn', o['script'], k)
        for w in d['warp_events']:
            assert (w['x'], w['y']) in r_all or (w['x'], w['y']) == start, (name, 'warp onbereikbaar', w)
        for b in d['bg_events']:
            p = (b['x'], b['y'])
            assert p in r_all or mf.next_to(r_all, *p), (name, 'bg onbereikbaar', p)
        print(name, 'bereikbaar:', len(r_all), 'tegels')
    # B1F: het hek houdt de ladder dicht; één duw omhoog in een gat opent hem (licht puzzelpad)
    g = MAPS[B1][1]
    d = json.load(open('data/maps/%s/map.json' % B1))
    solid = {(o['x'], o['y']) for o in d['object_events']} - {B1_ARRIVE}
    assert B1_LADDER not in mf.reachable(g, B1_ARRIVE, solid), 'B1F: hek lekt'
    for bx, by in B1_BOULDERS:
        assert (bx, by + 1) in mf.reachable(g, B1_ARRIVE, solid - {(bx, by)}), ('B1F: duwplek', bx)
        moved = (solid - {(bx, by)}) | {(bx, by - 3)}           # drie keer omhoog geduwd
        assert B1_LADDER in mf.reachable(g, B1_ARRIVE, moved), ('B1F: ladder na het duwen', bx)
    g = MAPS[F1][1]
    d = json.load(open('data/maps/%s/map.json' % F1))
    solid = {(o['x'], o['y']) for o in d['object_events']} - {F1_EXIT}
    assert not mf.next_to(mf.reachable(g, F1_EXIT, solid), *F1_ITEMS[1][0]), '1F: zijgrot lekt'


def overview(dirn):
    from PIL import Image
    ims = [Image.open(os.path.join(dirn, n + '.png')) for n in (F1, B1, B2)]
    o = Image.new('RGB', (sum(i.width for i in ims) + 32, max(i.height for i in ims)), (10, 14, 32))
    x = 0
    for i in ims:
        o.paste(i, (x, 0)); x += i.width + 16
    o.save(os.path.join(dirn, 'overzicht.png'))


def main():
    flags()
    build_maps()
    mapsecs()
    events()
    trainers()
    wild()
    evolutions()
    battle_setup()
    checks()
    if len(sys.argv) > 1:
        for name in MAPS:
            render(name, os.path.join(sys.argv[1], name + '.png'))
        overview(sys.argv[1])


if __name__ == '__main__':
    main()
