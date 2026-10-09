"""Project Grounded: Mt. Coronet + Spear Pillar (Spacetime Cave, het laatste portaal; Jordi 9 okt).

DPPt als inspiratie, niet nagebouwd. Je begint al hoog in de berg:
  MtCoronet_4F_Room1    Grote grotkamer met een waterval in het midden (bovenmeer -> ondermeer) en trappen aan beide
                        kanten. Warp 0 (zuiduitgang) = aankomst uit de Spacetime Cave (HUB_DEST terug); bovenaan de
                        lichte opening naar buiten.
  MtCoronet_4F_Outside  Sneeuwhelling rond de top (coronet_snow): een rotsmassief in terrassen in het midden, een beek
                        uit een waterval in de noordwand met twee bruggetjes, hoog gras, rotsen. Om de berg heen (west of
                        oost) naar de grot in de noordwand (kamer 3); kamer 2 via een trap op het massief.
  MtCoronet_4F_Room2    Kleine kamer: twee items en een rots.
  MtCoronet_4F_Room3    L-vormige gang naar de ladder naar 5F.
  MtCoronet_5F          Trapsgewijze grotkamer; een hek van puin met twee duwstenen (Strength) naar de bovenste laag.
  MtCoronet_6F          Smalle kamer, twee trappen omhoog, twee zuilen, bovenaan de lichte uitgang naar Spear Pillar.
  SpearPillar           De ruine op de top: platform met speerpilaren en twee altaren. Het diamant-altaar roept
                        DIALGA op, het parel-altaar PALKIA (lv 100); de speler kiest de volgorde. Na beide (gevangen of
                        verslagen) teleporteer je terug naar de Spacetime Cave: FLAG_SPACETIME_CORONET_DONE.
Trainers: projecties van Dialga en Palkia (bestaande klassen, lv 95-98), id 1057-1059, 1068, 1069, 1082-1088.
Flags FLAG_GROUNDED 1160-1219 (nieuwe items in nieuwe_items.py met nummers uit dit bereik).
Tilesets: coronet_tiles.py. Teksten zijn placeholders (Jordi herschrijft ze).
Gebruik: python3 tools/grounded/maptools/coronet.py [render-uitmap]"""
import json, math, os, random, re, struct, subprocess, sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import meteor_falls_ext as mf
import beacon_dragon as bd
import chargestone as cs
import coronet_tiles as ctt
import snowlib as sl

os.chdir(ctt.REPO)
Scr = bd.Scr
cell = mf.cell
CID = ctt.cave_ids()
cs.ID = CID                     # Cave.build() donkert de verre rots met onze tegels
sl.use_tileset('coronet_snow')
sl.FRONT_B = lambda: 'cliff_b'  # cliff_front_b heeft een grotopening (zwarte boog): niet als gewone klifvoet
N = sl.N
GROUP = 'gMapGroup_Spacetime'
PRIM = 'gTileset_General'
SEC_CAVE, SEC_SNOW = 'gTileset_CoronetCave', 'gTileset_CoronetSnow'
R1, OUT, R2, R3, F5, F6, SP = ('MtCoronet_4F_Room1', 'MtCoronet_4F_Outside', 'MtCoronet_4F_Room2',
                               'MtCoronet_4F_Room3', 'MtCoronet_5F', 'MtCoronet_6F', 'SpearPillar')
ORDER = [R1, OUT, R2, R3, F5, F6, SP]
CONST = {R1: 'MT_CORONET_4F_ROOM1', OUT: 'MT_CORONET_4F_OUTSIDE', R2: 'MT_CORONET_4F_ROOM2',
         R3: 'MT_CORONET_4F_ROOM3', F5: 'MT_CORONET_5F', F6: 'MT_CORONET_6F', SP: 'SPEAR_PILLAR'}
HUB_DEST = ('SPACETIME_CAVE', 0)   # terugwarp naar de hub (de hub koppelt zijn Coronet-portaal aan R1 warp 0)
MUSIC = {R1: 'MUS_CAVE_OF_ORIGIN', OUT: 'MUS_ROUTE120', R2: 'MUS_CAVE_OF_ORIGIN', R3: 'MUS_CAVE_OF_ORIGIN',
         F5: 'MUS_CAVE_OF_ORIGIN', F6: 'MUS_CAVE_OF_ORIGIN', SP: 'MUS_SEALED_CHAMBER'}

# ====================================================================== flags (FLAG_GROUNDED 1160-1219)
FLAGS = [
    (1160, 'FLAG_SPACETIME_CORONET_DONE', 'Mt. Coronet: Dialga en Palkia allebei gevangen of verslagen (klaar-flag; Arceus-scene in de hub)'),
    (1161, 'FLAG_CORONET_DIALGA_DONE', 'Spear Pillar: DIALGA gevangen of verslagen'),
    (1162, 'FLAG_CORONET_PALKIA_DONE', 'Spear Pillar: PALKIA gevangen of verslagen'),
    (1163, 'FLAG_HIDE_CORONET_DIALGA', 'Spear Pillar: DIALGA verborgen (verschijnt alleen via het altaar)'),
    (1164, 'FLAG_HIDE_CORONET_PALKIA', 'Spear Pillar: PALKIA verborgen (verschijnt alleen via het altaar)'),
    (1165, 'FLAG_ITEM_CORONET_4F_ROOM1_MAX_REVIVE', 'Mt. Coronet 4F kamer 1: Max Revive'),
    (1166, 'FLAG_HIDDEN_ITEM_CORONET_4F_ROOM1_ULTRA_BALL', 'Mt. Coronet 4F kamer 1: verborgen Ultra Balls'),
    (1167, 'FLAG_ITEM_CORONET_4F_OUTSIDE_MAX_ELIXIR', 'Mt. Coronet 4F buiten: Max Elixir (op het massief)'),
    (1168, 'FLAG_ITEM_CORONET_4F_OUTSIDE_PP_MAX', 'Mt. Coronet 4F buiten: PP Max'),
    (1169, 'FLAG_ITEM_CORONET_4F_ROOM3_RARE_CANDY', 'Mt. Coronet 4F kamer 3: Rare Candy'),
    (1170, 'FLAG_ITEM_CORONET_5F_MAX_POTION', 'Mt. Coronet 5F: Max Potion'),
    (1171, 'FLAG_HIDDEN_ITEM_CORONET_5F_STAR_PIECE', 'Mt. Coronet 5F: verborgen Star Piece'),
    (1172, 'FLAG_ITEM_CORONET_6F_PP_UP', 'Mt. Coronet 6F: PP Up'),
]
# 1180-1199: nieuwe items (nieuwe_items.py); 1173-1179 en 1200-1219 nog vrij


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = ('// coronet { (tools/grounded/maptools/coronet.py; FLAG_GROUNDED 1160-1219: 1180-1186 nieuwe items '
           '(blok nieuwe_items), 1173-1179 en 1187-1219 nog vrij)\n')
    for n, name, why in FLAGS:
        assert 1160 <= n <= 1219
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// coronet {' in s:
        i = s.index('// coronet {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// yoshis_island {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== nieuwe items (nergens anders te krijgen)
NEW_ITEMS = [  # (n, kaart, item, aantal, verborgen, omschrijving)
    (1180, R2, 'ITEM_ADAMANT_CRYSTAL', 1, False, 'Mt. Coronet 4F kamer 2: Adamant Crystal (Dialga Origin)'),
    (1181, R2, 'ITEM_ODD_KEYSTONE', 1, False, 'Mt. Coronet 4F kamer 2: Odd Keystone'),
    (1182, OUT, 'ITEM_LUSTROUS_GLOBE', 1, True, 'Mt. Coronet 4F buiten: verborgen Lustrous Globe (Palkia Origin)'),
    (1183, F5, 'ITEM_IRON_BALL', 1, False, 'Mt. Coronet 5F: Iron Ball'),
    (1184, SP, 'ITEM_ADAMANT_ORB', 1, False, 'Spear Pillar: Adamant Orb (bij het altaar van Dialga)'),
    (1185, SP, 'ITEM_LUSTROUS_ORB', 1, False, 'Spear Pillar: Lustrous Orb (bij het altaar van Palkia)'),
]


def new_items():
    """Voegt de items toe aan nieuwe_items.py (één lijst voor de hele game) en laat dat script zijn flagblok schrijven."""
    p = os.path.join(HERE, 'nieuwe_items.py')
    s = open(p).read()
    rows = ''.join("    (%d, '%s', '%s', %d, %s, '%s'),\n" % r for r in NEW_ITEMS)
    blk = '    # Mt. Coronet + Spear Pillar (coronet.py; flags uit het eigen blok FLAG_GROUNDED 1160-1219)\n' + rows
    if '# Mt. Coronet + Spear Pillar' in s:
        i = s.index('    # Mt. Coronet + Spear Pillar'); j = s.index('\n]\n', i) + 1
        s = s[:i] + blk + s[j:]
    else:
        i = s.index('\n]\nFIRST, LAST')
        s = s[:i + 1] + blk + s[i + 1:]
    if '(1160, 1219)' not in s:
        s = s.replace('EXTRA_RANGES = [(920, 999)]', 'EXTRA_RANGES = [(920, 999), (1160, 1219)]')
    assert '(1160, 1219)' in s
    open(p, 'w').write(s)
    import importlib
    import nieuwe_items as ni
    importlib.reload(ni)
    ni.flags()
    return ni


def item_list(ni, name):
    return [(fl, it, q, hid) for fl, it, q, hid in ni.items(name)]


# ====================================================================== kaart-hulpjes
def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"%s": [' % GROUP); j = g.index('\n  ]', i)
        body = g[i:j]
        sep = ',' if body.rstrip().endswith('"') else ''
        g = g[:j] + sep + '\n    "%s"' % name + g[j:]
    d = json.loads(g)
    assert len(d[GROUP]) <= 128, len(d[GROUP])
    open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/SpacetimeCave/scripts.inc"\n'
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def save(name, g, sec, border):
    W, H = len(g[0]), len(g)
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', t) for r in g for t in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *border))
    bd.register_layout(name, CONST[name], W, H, PRIM, sec)


def write_map(name, objs, warps, bgs, coords=(), head_scripts=None, **kw):
    m = {'id': 'MAP_' + CONST[name], 'name': name, 'layout': 'LAYOUT_' + CONST[name], 'music': MUSIC[name],
         'region_map_section': 'MAPSEC_SPEAR_PILLAR' if name == SP else 'MAPSEC_MT_CORONET',
         'requires_flash': False, 'weather': 'WEATHER_NONE', 'map_type': 'MAP_TYPE_UNDERGROUND',
         'allow_cycling': False, 'allow_escaping': False, 'allow_running': True,
         'show_map_name': name in (R1, OUT, SP), 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
         'object_events': objs, 'warp_events': warps, 'coord_events': list(coords), 'bg_events': bgs}
    m.update(kw)
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    register_map(name)


warp, obj, tr, ball = bd.warp, bd.obj, bd.tr, bd.ball


def hidden(xy, it, flag, q=1):
    return cs.hidden(xy, it, flag, q)


def head(name, scripts=()):
    os.makedirs('data/maps/' + name, exist_ok=True)
    h = '@ Project Grounded: %s (tools/grounded/maptools/coronet.py)\n%s_MapScripts::\n' % (name, name)
    for kind, lbl in scripts:
        h += '\tmap_script %s, %s\n' % (kind, lbl)
    return h + '\t.byte 0\n'


MAPS = {}        # naam -> raster (g)
EV = {}          # naam -> {'items': [((x,y), item, flag, aantal, verborgen)], ...}


# ====================================================================== grotten (Meteor Falls-autotiler, coronet_cave)
class Cave(cs.Cave):
    def lighthole(self, x, y):
        """Lichte opening in een stalactietenwand; (x,y) = de warptegel (onderste rij, midden)."""
        h = CID['lighthole']
        for dy in range(2):
            for dx in range(3):
                self.set(x - 1 + dx, y - 1 + dy, h[dy * 3 + dx], 0 if (dx == 1 and dy == 1) else 1)

    def craters(self, rnd, n, area, avoid):
        x0, y0, x1, y1 = area
        tries = 0
        while n and tries < 400:
            tries += 1
            x, y = rnd.randint(x0, x1 - 1), rnd.randint(y0, y1 - 1)
            cells = [(x + a, y + b) for a in (0, 1) for b in (0, 1)]
            if any(self.k[cy][cx] != 'F' or (cx, cy) in self.over or (cx, cy) in avoid for cx, cy in cells):
                continue
            if any((cx + a, cy + b) in self.over for cx, cy in cells for a in (-1, 0, 1) for b in (-1, 0, 1)):
                continue
            self.crater(x, y); n -= 1


def cave_decor(m, g, pts, extra, seed, rubble, craters=1):
    keep = cs.keep_paths(g, pts, extra)
    rnd = random.Random(seed)
    m.craters(rnd, craters, (0, 0, m.W - 1, m.H - 1), keep)
    m.rubble(rnd, rubble, (0, 0, m.W - 1, m.H - 1), keep)
    return m.build()


def cave_items(name, g, wanted):
    out = []
    for p, it, fl, q, hid in wanted:
        x, y = p
        assert not g[y][x] & 0xC00, (name, 'item op een muur', p, it)
        out.append((p, it, fl, q, hid))
    EV.setdefault(name, {})['items'] = out
    return {p for p, *_ in out}


def items_ev(name):
    objs, bgs = [], []
    for p, it, fl, q, hid in EV.get(name, {}).get('items', []):
        if hid:
            bgs.append(hidden(p, it, fl, q))
        else:
            o = ball(p[0], p[1], it, fl)
            if q > 1:
                o['movement_range_x'] = q
            objs.append(o)
    return objs, bgs


# --------------------------------------------------------------------- 4F kamer 1 (waterval)
R1_ENTRY = (8, 31)            # zuiduitgang = aankomst uit de hub (warp 0)
R1_HOLE = (30, 5)             # lichte opening naar buiten (warp 1)
R1_TRAINERS = {'TICK': ((30, 26), 'LEFT', 4), 'PARALLAX': ((11, 7), 'RIGHT', 4)}


def spots(m, g, wanted, taken):
    """wanted: [(doel, item, flag, aantal, verborgen)] -> dichtstbijzijnde vrije vloertegels."""
    out = []
    for tgt, it, fl, q, hid in wanted:
        p = cs.item_spot(m, g, tgt, taken)
        taken |= {p}
        out.append((p, it, fl, q, hid))
    return out


def build_r1(ni):
    m = Cave(40, 36, 4401)
    m.lobes(4, 4, 35, 15, 'up', 9)
    m.lobes(4, 21, 35, 31, 'low', 9)
    m.freeze(4, 15, 35, 21, 'F')                          # klifband met waterval en trappen over de volle breedte
    m.freeze(14, 8, 25, 15, 'F'); m.freeze(12, 21, 27, 28, 'F')     # meren met oever
    m.freeze(27, 6, 33, 8, 'F'); m.freeze(26, 0, 34, 5, 'R')        # rechte wand bij de lichte opening
    m.freeze(4, 28, 35, 31, 'F'); m.freeze(4, 32, 35, 35, 'R')      # rechte onderwand met de zuiduitgang
    m.freeze(4, 12, 35, 14, 'F'); m.freeze(4, 22, 35, 23, 'F')      # zalen even breed als de klifband
    m.freeze(30, 21, 35, 31, 'F')
    m.freeze(25, 25, 31, 27, 'F'); m.freeze(10, 6, 16, 8, 'F')      # trainers
    m.shape()
    m.water(16, 9, 23, 15)                    # bovenmeer
    m.water(14, 21, 25, 26)                   # ondermeer onder de waterval
    m.build()
    m.stal_wall(27, 33, 6)
    m.cliff(10, 29, 16)
    for y in (18, 19, 20):                    # randen van de stalactietenwand naast de trappen
        m.set(10, y, mf.STAL_L, 1); m.set(29, y, mf.STAL_R, 1)
    m.step(4, 9, 16, stairs=(6, 7))
    m.step(30, 35, 16, stairs=(32, 33))
    m.waterfall(16, 16)
    m.lighthole(*R1_HOLE)
    m.exit_south(*R1_ENTRY)
    g = m.build()
    taken = {R1_ENTRY, R1_HOLE} | {p for p, _, _ in R1_TRAINERS.values()}
    EV[R1] = {'items': spots(m, g, [((5, 6), 'ITEM_MAX_REVIVE', 'FLAG_ITEM_CORONET_4F_ROOM1_MAX_REVIVE', 1, False),
                                    ((34, 29), 'ITEM_ULTRA_BALL', 'FLAG_HIDDEN_ITEM_CORONET_4F_ROOM1_ULTRA_BALL', 3,
                                     True)], taken)}
    ip = {p for p, *_ in EV[R1]['items']}
    pts = [(R1_ENTRY[0], R1_ENTRY[1] - 1), (R1_HOLE[0], R1_HOLE[1] + 1), (6, 15), (32, 15), (6, 18), (32, 18)]
    pts += [p for p, _, _ in R1_TRAINERS.values()] + sorted(ip)
    extra = set().union(*[cs.sight(p, f, n) for p, f, n in R1_TRAINERS.values()]) | ip
    return m, cave_decor(m, g, pts, extra, 4402, 16, 3)


# --------------------------------------------------------------------- 4F kamer 2 (klein: twee items, een rots)
R2_ENTRY = (8, 11)
R2_ROCK = (8, 7)


def build_r2(ni):
    m = Cave(18, 16, 4421)
    m.lobes(4, 4, 13, 11, 'r2', 6)
    m.freeze(4, 8, 13, 11, 'F'); m.freeze(3, 12, 14, 15, 'R')
    m.freeze(6, 6, 10, 9, 'F')
    m.shape()
    m.build()
    m.exit_south(*R2_ENTRY)
    g = m.build()
    new = item_list(ni, R2)
    EV[R2] = {'items': spots(m, g, [((4, 5), new[0][1], new[0][0], 1, False),
                                    ((13, 5), new[1][1], new[1][0], 1, False)], {R2_ENTRY, R2_ROCK})}
    ip = {p for p, *_ in EV[R2]['items']}
    pts = [(R2_ENTRY[0], R2_ENTRY[1] - 1)] + sorted(ip) + [(R2_ROCK[0], R2_ROCK[1] + 1)]
    return m, cave_decor(m, g, pts, ip | {R2_ROCK}, 4422, 3, 0)


# --------------------------------------------------------------------- 4F kamer 3 (L-gang)
R3_ENTRY = (6, 17)            # zuiduitgang = vanaf buiten (warp 0)
R3_LADDER = (35, 12)          # ladder naar 5F (warp 1)
R3_TRAINERS = {'VERTEX': ((22, 13), 'LEFT', 4)}


def build_r3(ni):
    m = Cave(42, 22, 4431)
    m.path([(6.5, 16), (6, 11), (7, 6)], 2.1)              # verticale poot
    m.path([(6.5, 13), (13, 12.5), (30, 12.5), (35, 12.5)], 2.0)   # lange gang
    m.lobes(3, 4, 10, 9, 'r3', 5)
    m.freeze(5, 16, 7, 17, 'F'); m.freeze(3, 18, 9, 21, 'R')
    m.freeze(32, 10, 37, 14, 'F')
    m.shape()
    m.build()
    m.exit_south(*R3_ENTRY)
    m.ladder(*R3_LADDER)
    g = m.build()
    taken = {R3_ENTRY, R3_LADDER} | {p for p, _, _ in R3_TRAINERS.values()}
    EV[R3] = {'items': spots(m, g, [((5, 3), 'ITEM_RARE_CANDY', 'FLAG_ITEM_CORONET_4F_ROOM3_RARE_CANDY', 1, False)],
                             taken)}
    ip = {p for p, *_ in EV[R3]['items']}
    pts = [(R3_ENTRY[0], R3_ENTRY[1] - 1), (R3_LADDER[0], R3_LADDER[1] + 1)] + sorted(ip)
    pts += [p for p, _, _ in R3_TRAINERS.values()]
    extra = set().union(*[cs.sight(p, f, n) for p, f, n in R3_TRAINERS.values()]) | ip
    return m, cave_decor(m, g, pts, extra, 4432, 8, 1)


# --------------------------------------------------------------------- 5F (terrassen + duwstenen)
F5_ARRIVE = (6, 29)           # ladder omlaag naar kamer 3 (warp 0)
F5_LADDER = (29, 6)           # ladder naar 6F (warp 1)
F5_FENCE_Y = 17
F5_BOULDERS = [(12, 17), (24, 17)]
F5_TRAINERS = {'DEJAVU': ((21, 27), 'LEFT', 4), 'NEBULA': ((16, 7), 'DOWN', 3)}


def build_5f(ni):
    m = Cave(36, 34, 4501)
    m.lobes(4, 4, 31, 12, 'top', 8)
    m.lobes(4, 23, 31, 29, 'bot', 8)
    m.freeze(4, 16, 31, 18, 'F')
    for bx, _ in F5_BOULDERS:
        m.freeze(bx - 1, 14, bx + 1, 19, 'F')
    m.freeze(4, 26, 31, 29, 'F'); m.freeze(28, 5, 30, 7, 'F')
    m.freeze(16, 26, 22, 28, 'F'); m.freeze(15, 6, 17, 11, 'F')
    m.terrace(4, 31, 22, 28)
    m.terrace(4, 31, 13, 6)
    m.shape()
    m.build()
    m.steps()
    for x in range(m.W):                      # puinhek op de middenlaag, twee gaten met een duwsteen
        if m.k[F5_FENCE_Y][x] == 'F' and x not in [b[0] for b in F5_BOULDERS]:
            m.set(x, F5_FENCE_Y, mf.RUBBLE[x % 3], 1)
    m.ladder(*F5_ARRIVE)
    m.ladder(*F5_LADDER)
    g = m.build()
    new = item_list(ni, F5)
    taken = {F5_ARRIVE, F5_LADDER} | {p for p, _, _ in F5_TRAINERS.values()} | set(F5_BOULDERS)
    taken |= {(x, y) for x, _ in F5_BOULDERS for y in range(14, 19)}
    EV[F5] = {'items': spots(m, g, [((31, 26), 'ITEM_MAX_POTION', 'FLAG_ITEM_CORONET_5F_MAX_POTION', 1, False),
                                    ((4, 19), 'ITEM_STAR_PIECE', 'FLAG_HIDDEN_ITEM_CORONET_5F_STAR_PIECE', 1, True),
                                    ((4, 6), new[0][1], new[0][0], 1, False)], taken)}
    ip = {p for p, *_ in EV[F5]['items']}
    pts = [(F5_ARRIVE[0], F5_ARRIVE[1] - 1), (F5_LADDER[0], F5_LADDER[1] + 1), (28, 21), (6, 12)]
    pts += [p for p, _, _ in F5_TRAINERS.values()] + sorted(ip - {EV[F5]['items'][2][0]})
    extra = set().union(*[cs.sight(p, f, n) for p, f, n in F5_TRAINERS.values()]) | ip
    extra |= {(x, y) for x, _ in F5_BOULDERS for y in range(14, 20)} | {(x, y) for x in range(m.W) for y in (16, 17, 18)}
    top = cs.keep_paths(g, [(6, 12), EV[F5]['items'][2][0], (F5_LADDER[0], F5_LADDER[1] + 1)])
    return m, cave_decor(m, g, pts, extra | top, 4502, 14, 2)


# --------------------------------------------------------------------- 6F (smal, twee trappen, twee zuilen)
F6_ARRIVE = (12, 25)          # ladder omlaag naar 5F (warp 0)
F6_HOLE = (12, 5)             # lichte uitgang naar Spear Pillar (warp 1)
F6_TRAINERS = {'CHRONOS': ((15, 15), 'LEFT', 5), 'SPATIA': ((8, 9), 'RIGHT', 5)}


def build_6f(ni):
    m = Cave(24, 30, 4601)
    m.room(6, 6, 17, 25)                      # smalle, rechte kamer (zoals in DPPt)
    m.terrace(6, 17, 12, 15)
    m.terrace(6, 17, 19, 7)
    m.build()
    m.steps()
    m.stal_wall(8, 16, 6, pillars=(9, 14))
    m.lighthole(*F6_HOLE)
    m.ladder(*F6_ARRIVE)
    g = m.build()
    taken = {F6_ARRIVE, F6_HOLE} | {p for p, _, _ in F6_TRAINERS.values()}
    EV[F6] = {'items': spots(m, g, [((18, 24), 'ITEM_PP_UP', 'FLAG_ITEM_CORONET_6F_PP_UP', 1, False)], taken)}
    ip = {p for p, *_ in EV[F6]['items']}
    pts = [(F6_ARRIVE[0], F6_ARRIVE[1] - 1), (F6_HOLE[0], F6_HOLE[1] + 1)] + sorted(ip)
    pts += [p for p, _, _ in F6_TRAINERS.values()]
    extra = set().union(*[cs.sight(p, f, n) for p, f, n in F6_TRAINERS.values()]) | ip
    return m, cave_decor(m, g, pts, extra, 4602, 7, 1)


# ====================================================================== sneeuw (snowlib, coronet_snow)
STL, STR = 175, 207           # Hoenn-stenen trap (General)
BLOCK = ['rock_snow', 'rock_snow2', 'rock_cluster', 'rock_snow3', 'rock_snow4', 'ice_rock', 'ice_rock2', 'ice_chunks',
         'ice_crystal', 'ice_crystal2', 'snowball']
SOFT = ['tuft2', 'tuft4', 'tuft6', 'tuft7', 'tuft8', 'tuft9', 'snow_deep', 'snow_deep2', 'snow_dots', 'snow_light']


def rect(x0, y0, x1, y1):
    return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}


def snow_g(m):
    return [[(m.g[y][x] & 0x3ff) | (m.col[y][x] << 10) | (m.elev[y][x] << 12) for x in range(m.W)] for y in range(m.H)]


def stairs(m, x0, y0, h=2):
    for y in range(y0, y0 + h):
        m.put(x0, y, STL, 0, 3); m.put(x0 + 1, y, STR, 0, 3)


def door(m, x0, y):
    """Grotingang in een klifwand van 2 rijen (y = bovenste rij); warp op (x0+1, y+1)."""
    for x, n in zip((x0, x0 + 1, x0 + 2), ('cliff_front_a', 'cliff_front_b', 'cliff_front_c')):
        m.put(x, y, n, 1)
    for x, n in zip((x0, x0 + 1, x0 + 2), ('cave_l', 'cave_door', 'cave_r')):
        m.put(x, y + 1, n, 1)
    m.put(x0 + 1, y + 1, 'cave_door', 0, 0)
    return (x0 + 1, y + 1)


def raised_field(m, W, H, face_n=3):
    """Hoge noordwand (de top) over de volle breedte; daaronder het veld als terras dat naar het westen, oosten en
    zuiden afloopt (de border is lagere sneeuw). Buiten de kaart telt mee, zodat er geen losse hoeken ontstaan."""
    field = {(x, y) for x in range(1, W - 1) for y in range(-6, H - 2)}
    before = [row[:] for row in m.g]
    sl.terrace(m, field, face=2)
    for y in range(H):                     # het veld zelf is gewone sneeuw (met de strooisels van daarvoor)
        for x in range(W):
            if m.g[y][x] == N['cliff_c']:
                m.g[y][x] = before[y][x]
    north = {(x, y) for x in range(-6, W + 6) for y in range(-6, 4)}
    sl.terrace(m, north, face=face_n)


def snow_reach(m, start, blocked=()):
    return mf.reachable(snow_g(m), start, set(blocked))


def snow_keep(m, pts, extra=()):
    return cs.keep_paths(snow_g(m), pts, extra)


def snow_decor(m, rnd, keep, avoid_tiles, p_block=0.06, p_soft=0.12, area=None):
    W, H = m.W, m.H
    sp = {N[k] for k in N if k.startswith(('cliff', 'cave', 'bridge', 'pillar', 'altar', 'path_stone', 'shore'))}

    def free(x, y):
        return 0 <= x < W and 0 <= y < H and m.col[y][x] == 0 and m.elev[y][x] == 3 and \
            m.g[y][x] in (N['snow'], N['cliff_c'])

    def clear(x, y, r):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                c = (x + dx, y + dy)
                if c in keep:
                    return False
                if 0 <= c[0] < W and 0 <= c[1] < H and (m.g[c[1]][c[0]] in avoid_tiles or m.g[c[1]][c[0]] in sp
                                                        or m.g[c[1]][c[0]] in (STL, STR) or m.elev[c[1]][c[0]] == 1):
                    return False
        return True
    cands = [(x, y) for y in range(H) for x in range(W) if free(x, y) and (x, y) not in keep
             and (area is None or (x, y) in area)]
    rnd.shuffle(cands)
    for (x, y) in cands:
        if not free(x, y):
            continue
        r = rnd.random()
        if r < p_block and clear(x, y, 1):
            m.put(x, y, rnd.choice(BLOCK), 1)
        elif r < p_block + p_soft and clear(x, y, 0):
            m.put(x, y, rnd.choice(SOFT), 0)


# --------------------------------------------------------------------- 4F buiten
OW, OH = 56, 46
OUT_TRAINERS = {'AEON': ((31, 34), 'LEFT', 4), 'VOIDA': ((43, 22), 'DOWN', 4), 'MOMENTUM': ((7, 18), 'DOWN', 4),
                'ORBIT': ((37, 6), 'RIGHT', 3), 'EPOCH': ((19, 8), 'DOWN', 3)}
OUT_DOORS = {}                # 'r1', 'r2', 'r3' -> warptegel


def build_out(ni):
    m = sl.M(OW, OH)
    sl.use_tileset('coronet_snow')
    rnd = random.Random(4004)
    for y in range(OH):
        for x in range(OW):
            if rnd.random() < 0.05:
                m.put(x, y, rnd.choice(['snow_dots', 'tuft0', 'tuft1', 'tuft3', 'snow_light', 'tuft5']))
    raised_field(m, OW, OH)
    # het massief in terrassen rond de (onbereikbare) top
    M1, M2, M3 = rect(14, 13, 41, 31), rect(17, 15, 38, 26), rect(20, 17, 35, 22)
    sl.terrace(m, M1, face=2); sl.terrace(m, M2, face=2); sl.terrace(m, M3, face=2)
    for hill in (rect(4, 29, 9, 32), rect(4, 11, 8, 13), rect(21, 36, 25, 39)):   # rotsheuvels op de helling
        sl.terrace(m, hill, face=2)
    for (px, py) in ((24, 17), (29, 18)):                 # rotspieken op de top
        for dx in (0, 1):
            for dy in (0, 1):
                m.put(px + dx, py + dy, 'peak_%d%d' % (dx, dy), 1)
    # beek: waterval uit de noordwand, omlaag, langs het massief naar het oosten, dan zuidwaarts naar een vijver
    sl.fall(m, 33, 1, 3, w=3)
    # onderaan stort de beek als waterval over de zuidrand naar de lagere helling
    brook = rect(33, 5, 35, 12) | rect(36, 10, 47, 12) | rect(46, 13, 47, OH - 5)
    pond2 = set(sl.blob(7, 37.5, 3.4, 2.4, seed=8))
    foam = rect(33, 4, 35, 4)
    sl.fall(m, 46, OH - 4, OH - 3, w=2)
    low = rect(45, OH - 2, 48, OH - 1)
    m.water(brook, extra=foam | rect(46, OH - 4, 47, OH - 2))
    m.water(low - rect(46, OH - 2, 47, OH - 2), extra=rect(46, OH - 2, 47, OH - 2) | rect(44, OH, 49, OH + 2))
    m.water(pond2)
    for x in (33, 34, 35):                                # bruggetje 1 (oost-west) over de beek in de noordband
        for y in (6, 7):
            m.put(x, y, 'bridge_h', 0, 3)
    for x in (43, 44):                                    # bruggetje 2 (noord-zuid) over de beek langs het massief
        for y in (10, 11, 12):
            m.put(x, y, 'bridge_v', 0, 3)
    OUT_DOORS['r1'] = door(m, 17, 30)                    # uit kamer 1 (in de zuidwand van het massief)
    OUT_DOORS['r2'] = door(m, 33, 25)                    # naar kamer 2 (in de wand van de tweede laag)
    OUT_DOORS['r3'] = door(m, 39, 2)                     # naar kamer 3 (in de noordwand)
    stairs(m, 28, 30)                                     # trap op het massief (naar kamer 2)
    # hoog gras
    grass = set()
    for c, sd in (((34, 36, 5, 2.2), 11), ((8, 22, 2.6, 4.5), 12), ((13, 7.5, 5, 2), 13), ((50.5, 30, 1.8, 3.2), 14),
                  ((44, 29, 1.6, 3), 15), ((26, 8.5, 3, 1.6), 16)):
        grass |= set(sl.blob(*c, seed=sd))
    keyp = [(OUT_DOORS['r1'][0], OUT_DOORS['r1'][1] + 1), (OUT_DOORS['r2'][0], OUT_DOORS['r2'][1] + 1),
            (OUT_DOORS['r3'][0], OUT_DOORS['r3'][1] + 1), (28, 32), (29, 29), (32, 7), (36, 7), (43, 9), (43, 13)]
    keyp += [p for p, _, _ in OUT_TRAINERS.values()]
    new = item_list(ni, OUT)
    wanted = [((30, 28), 'ITEM_MAX_ELIXIR', 'FLAG_ITEM_CORONET_4F_OUTSIDE_MAX_ELIXIR', 1, False),
              ((3, 5), 'ITEM_PP_MAX', 'FLAG_ITEM_CORONET_4F_OUTSIDE_PP_MAX', 1, False),
              ((52, 33), new[0][1], new[0][0], 1, True)]
    ip = {p for p, *_ in wanted}
    keyp += sorted(ip)
    sight = set().union(*[cs.sight(p, f, n) for p, f, n in OUT_TRAINERS.values()])
    for (x, y) in grass:
        if 0 <= x < OW and 0 <= y < OH and m.col[y][x] == 0 and m.elev[y][x] == 3 and (x, y) not in ip \
                and m.g[y][x] not in (N['cave_door'], STL, STR, N['bridge_h'], N['bridge_v']) \
                and not any(0 <= x + a < OW and 0 <= y + b < OH and m.col[y + b][x + a] for a in (-1, 0, 1) for b in (-1, 0, 1)
                            if (x + a, y + b) not in grass and m.g[y + b][x + a] in (N['cave_door'],)):
            if m.g[y][x] == N['cliff_c'] or (x, y) in {p for p, _, _ in OUT_TRAINERS.values()}:
                continue
            m.put(x, y, 'grass_snow', 0)
    keep = snow_keep(m, keyp, sight | ip)
    for (x, y) in ((4, 4), (9, 4), (25, 4), (51, 5), (3, 13), (11, 14), (51, 14), (2, 39), (12, 38), (38, 38),
                   (49, 36), (27, 30), (34, 13)):          # besneeuwde dennen langs de wanden
        cells = [(x + a, y + b) for a in (0, 1) for b in (0, 1, 2)]
        if all(0 <= cx < OW and 0 <= cy < OH and m.col[cy][cx] == 0 and m.elev[cy][cx] == 3 and (cx, cy) not in keep
               and m.g[cy][cx] in (N['snow'], N['cliff_c']) or m.g[cy][cx] in {N[k] for k in N if k.startswith('tuft')}
               for cx, cy in cells):
            m.pine(x, y, green=rnd.random() < 0.3)
    snow_decor(m, rnd, keep, {N['grass_snow']}, p_block=0.08, p_soft=0.16)
    EV[OUT] = {'items': wanted}
    return m, snow_g(m)


# --------------------------------------------------------------------- Spear Pillar
SW, SH = 30, 34
SP_ENTRY = [(14, 31), (15, 31)]       # trap omlaag naar 6F (warps 0 en 1)
SP_ALTARS = {'DIALGA': (9, 9), 'PALKIA': (19, 9)}
SP_MON = {'DIALGA': (10, 10), 'PALKIA': (20, 10)}


def build_sp(ni):
    m = sl.M(SW, SH)
    sl.use_tileset('coronet_snow')
    rnd = random.Random(4777)
    for y in range(SH):
        for x in range(SW):
            if rnd.random() < 0.05:
                m.put(x, y, rnd.choice(['snow_dots', 'snow_light', 'tuft0', 'tuft3']))
    raised_field(m, SW, SH)
    plat = rect(6, 8, 23, 26)
    sl.terrace(m, plat, face=2)
    sl.autopath(m, rect(7, 9, 22, 24), 'path_stone')
    stairs(m, 14, 25)                                     # trap op het platform
    stairs(m, 14, SH - 4)                                 # trap door de zuidrand (omlaag naar 6F)
    for x, k in ((14, 'stairs_s_l'), (15, 'stairs_s_r')):
        m.put(x, SH - 3, k, 0, 3)
    for kind, (x, y) in SP_ALTARS.items():
        for dx in (0, 1):
            for dy in (0, 1):
                m.put(x + dx, y + dy, 'altar_%s_%d%d' % (kind.lower(), dx, dy), 1)
    br = ctt.blocked_rows()

    def put_art(key, x, y, cols, rows):
        for dx in range(cols):
            for dy in range(rows):
                m.put(x + dx, y + dy, '%s_%d%d' % (key, dx, dy), 1 if dy in br[key] else 0)
    for (x, y) in ((7, 13), (21, 13), (7, 19)):
        put_art('pillar', x, y, 2, 4)
    for (x, y) in ((21, 20), (11, 18), (17, 14)):
        put_art('pillar_broken', x, y, 2, 3)
    EV[SP] = {'items': [((7, 10), 'ITEM_ADAMANT_ORB', item_list(ni, SP)[0][0], 1, False),
                        ((22, 10), 'ITEM_LUSTROUS_ORB', item_list(ni, SP)[1][0], 1, False)]}
    keyp = [(14, 29), (14, 24), (9, 11), (10, 11), (19, 11), (20, 11), (7, 11), (22, 11)]
    keep = snow_keep(m, keyp, rect(7, 9, 22, 24))
    for (x, y) in ((3, 5), (25, 5), (3, 27), (25, 28)):   # rotspieken in de hoeken van de top
        for dx in (0, 1):
            for dy in (0, 1):
                m.put(x + dx, y + dy, 'peak_%d%d' % (dx, dy), 1)
    snow_decor(m, rnd, keep, set(), p_block=0.08, p_soft=0.12)
    return m, snow_g(m)


# ====================================================================== bouwen
BUILD = {R1: (build_r1, 'cave'), R2: (build_r2, 'cave'), R3: (build_r3, 'cave'), F5: (build_5f, 'cave'),
         F6: (build_6f, 'cave'), OUT: (build_out, 'snow'), SP: (build_sp, 'snow')}


def build_maps(ni):
    for name in ORDER:
        fn, kind = BUILD[name]
        m, g = fn(ni)
        MAPS[name] = g
        if kind == 'cave':
            save(name, g, SEC_CAVE, [cell(CID['rockD'][0], 1, 0)] * 4)
        else:
            save(name, g, SEC_SNOW, [N['snow'] | (3 << 12)] * 4)


# ====================================================================== trainers
mon, AI, AI_BOSS = bd.mon, bd.AI, bd.AI_BOSS
TRAINERS = [  # (sleutel, id, naam, klasse, pic, gender, music, ai, gfx, team, waarom)
    ('CORONET_TICK', 1057, 'TICK', 'Expert', 'Expert M', 'Male', 'Intense', AI, 'OBJ_EVENT_GFX_EXPERT_M', [
        mon('Bronzong', 95, ['Gyro Ball', 'Earthquake', 'Psychic', 'Trick Room']),
        mon('Corviknight', 95, ['Brave Bird', 'Iron Head', 'Bulk Up', 'Roost']),
        mon('Kingambit', 95, ['Kowtow Cleave', 'Iron Head', 'Sucker Punch', 'Swords Dance']),
        mon('Excadrill', 95, ['Earthquake', 'Iron Head', 'Rock Slide', 'Swords Dance'])],
     'Mt. Coronet 4F kamer 1, projectie van Dialga'),
    ('CORONET_PARALLAX', 1058, 'PARALLAX', 'Cooltrainer', 'Cooltrainer F', 'Female', 'Cool', AI,
     'OBJ_EVENT_GFX_WOMAN_5', [
        mon('Starmie', 95, ['Hydro Pump', 'Psychic', 'Thunderbolt', 'Ice Beam']),
        mon('Kingdra', 95, ['Draco Meteor', 'Hydro Pump', 'Ice Beam', 'Rain Dance']),
        mon('Beheeyem', 95, ['Psychic', 'Shadow Ball', 'Thunderbolt', 'Trick Room']),
        mon('Primarina', 95, ['Moonblast', 'Sparkling Aria', 'Psychic', 'Ice Beam'])],
     'Mt. Coronet 4F kamer 1, projectie van Palkia'),
    ('CORONET_AEON', 1059, 'AEON', 'Cooltrainer', 'Cooltrainer M', 'Male', 'Cool', AI, 'OBJ_EVENT_GFX_MAN_3', [
        mon('Magnezone', 95, ['Thunderbolt', 'Flash Cannon', 'Volt Switch', 'Body Press']),
        mon('Slowking', 95, ['Psychic', 'Scald', 'Slack Off', 'Trick Room']),
        mon('Hydreigon', 95, ['Dark Pulse', 'Draco Meteor', 'Flamethrower', 'Earth Power']),
        mon('Duraludon', 95, ['Flash Cannon', 'Draco Meteor', 'Thunderbolt', 'Body Press']),
        mon('Dragapult', 96, ['Dragon Darts', 'Phantom Force', 'U-turn', 'Will-O-Wisp'])],
     'Mt. Coronet 4F buiten, projectie van Dialga'),
    ('CORONET_VOIDA', 1068, 'VOIDA', 'Hex Maniac', 'Hex Maniac', 'Female', 'Suspicious', AI,
     'OBJ_EVENT_GFX_HEX_MANIAC', [
        mon('Chandelure', 95, ['Shadow Ball', 'Flamethrower', 'Energy Ball', 'Will-O-Wisp']),
        mon('Gengar', 95, ['Shadow Ball', 'Sludge Bomb', 'Focus Blast', 'Hypnosis']),
        mon('Sigilyph', 95, ['Psychic', 'Air Slash', 'Heat Wave', 'Cosmic Power']),
        mon('Reuniclus', 95, ['Psychic', 'Focus Blast', 'Shadow Ball', 'Calm Mind']),
        mon('Mimikyu', 96, ['Play Rough', 'Shadow Claw', 'Swords Dance', 'Shadow Sneak'])],
     'Mt. Coronet 4F buiten, projectie van Palkia'),
    ('CORONET_MOMENTUM', 1069, 'MOMENTUM', 'Black Belt', 'Black Belt', 'Male', 'Intense', AI,
     'OBJ_EVENT_GFX_BLACK_BELT', [
        mon('Lucario', 96, ['Aura Sphere', 'Flash Cannon', 'Close Combat', 'Extreme Speed']),
        mon('Conkeldurr', 96, ['Drain Punch', 'Mach Punch', 'Knock Off', 'Ice Punch']),
        mon('Hawlucha', 96, ['Close Combat', 'Brave Bird', 'Swords Dance', 'Roost']),
        mon('Machamp', 96, ['Dynamic Punch', 'Stone Edge', 'Knock Off', 'Bullet Punch'])],
     'Mt. Coronet 4F buiten, projectie van Dialga'),
    ('CORONET_ORBIT', 1082, 'ORBIT', 'Psychic', 'Psychic M', 'Male', 'Intense', AI, 'OBJ_EVENT_GFX_PSYCHIC_M', [
        mon('Lunatone', 96, ['Psychic', 'Moonblast', 'Earth Power', 'Rock Polish']),
        mon('Solrock', 96, ['Psychic', 'Flare Blitz', 'Stone Edge', 'Morning Sun']),
        mon('Clefable', 96, ['Moonblast', 'Moonlight', 'Thunderbolt', 'Cosmic Power']),
        mon('Gardevoir', 96, ['Moonblast', 'Psychic', 'Focus Blast', 'Calm Mind']),
        mon('Orbeetle', 96, ['Bug Buzz', 'Psychic', 'Sticky Web', 'Light Screen'])],
     'Mt. Coronet 4F buiten, projectie van Palkia'),
    ('CORONET_EPOCH', 1083, 'EPOCH', 'Expert', 'Expert F', 'Female', 'Intense', AI, 'OBJ_EVENT_GFX_EXPERT_F', [
        mon('Aerodactyl', 96, ['Stone Edge', 'Earthquake', 'Crunch', 'Dual Wingbeat']),
        mon('Tyrantrum', 96, ['Head Smash', 'Dragon Claw', 'Earthquake', 'Crunch']),
        mon('Armaldo', 96, ['X-Scissor', 'Stone Edge', 'Earthquake', 'Swords Dance']),
        mon('Bastiodon', 96, ['Iron Head', 'Body Press', 'Stealth Rock', 'Metal Burst']),
        mon('Aurorus', 96, ['Freeze-Dry', 'Earth Power', 'Thunderbolt', 'Ancient Power'])],
     'Mt. Coronet 4F buiten, projectie van Dialga (fossielen: tijd)'),
    ('CORONET_VERTEX', 1084, 'VERTEX', 'Dragon Tamer', 'Dragon Tamer', 'Male', 'Intense', AI, 'OBJ_EVENT_GFX_MAN_3', [
        mon('Dragonite', 97, ['Extreme Speed', 'Dragon Claw', 'Earthquake', 'Dragon Dance']),
        mon('Goodra', 97, ['Draco Meteor', 'Fire Blast', 'Thunderbolt', 'Sludge Bomb']),
        mon('Salamence', 97, ['Draco Meteor', 'Fire Blast', 'Hydro Pump', 'Roost']),
        mon('Haxorus', 97, ['Outrage', 'Earthquake', 'Poison Jab', 'Dragon Dance']),
        mon('Garchomp', 97, ['Earthquake', 'Dragon Claw', 'Stone Edge', 'Swords Dance'])],
     'Mt. Coronet 4F kamer 3, projectie van Palkia'),
    ('CORONET_DEJAVU', 1085, 'DEJA VU', 'Cooltrainer', 'Cooltrainer M', 'Male', 'Cool', AI, 'OBJ_EVENT_GFX_MAN_3', [
        mon('Ditto', 97, ['Transform']),
        mon('Slowbro', 97, ['Psychic', 'Scald', 'Slack Off', 'Trick Room']),
        mon('Alakazam', 97, ['Psychic', 'Shadow Ball', 'Focus Blast', 'Recover']),
        mon('Metagross', 97, ['Meteor Mash', 'Zen Headbutt', 'Earthquake', 'Bullet Punch']),
        mon('Scizor', 97, ['Bullet Punch', 'U-turn', 'Swords Dance', 'Close Combat'])],
     'Mt. Coronet 5F, projectie van Dialga'),
    ('CORONET_NEBULA', 1086, 'NEBULA', 'Cooltrainer', 'Cooltrainer F', 'Female', 'Cool', AI,
     'OBJ_EVENT_GFX_WOMAN_5', [
        mon('Milotic', 97, ['Scald', 'Ice Beam', 'Recover', 'Dragon Pulse']),
        mon('Lapras', 97, ['Freeze-Dry', 'Surf', 'Thunderbolt', 'Psychic']),
        mon('Gyarados', 97, ['Waterfall', 'Earthquake', 'Dragon Dance', 'Crunch']),
        mon('Jellicent', 97, ['Scald', 'Shadow Ball', 'Recover', 'Will-O-Wisp']),
        mon('Walrein', 97, ['Surf', 'Ice Beam', 'Earth Power', 'Yawn'])],
     'Mt. Coronet 5F, projectie van Palkia'),
    ('CORONET_CHRONOS', 1087, 'CHRONOS', 'Expert', 'Expert M', 'Male', 'Intense', AI_BOSS, 'OBJ_EVENT_GFX_EXPERT_M', [
        mon('Archaludon', 98, ['Electro Shot', 'Draco Meteor', 'Flash Cannon', 'Body Press']),
        mon('Tyranitar', 98, ['Stone Edge', 'Crunch', 'Earthquake', 'Dragon Dance']),
        mon('Gholdengo', 98, ['Make It Rain', 'Shadow Ball', 'Nasty Plot', 'Recover']),
        mon('Hatterene', 98, ['Psychic', 'Dazzling Gleam', 'Mystical Fire', 'Trick Room']),
        mon('Espathra', 98, ['Lumina Crash', 'Dazzling Gleam', 'Calm Mind', 'Stored Power']),
        mon('Skarmory', 98, ['Brave Bird', 'Iron Head', 'Spikes', 'Roost'])],
     'Mt. Coronet 6F, de laatste projectie van Dialga'),
    ('CORONET_SPATIA', 1088, 'SPATIA', 'Expert', 'Expert F', 'Female', 'Intense', AI_BOSS, 'OBJ_EVENT_GFX_EXPERT_F', [
        mon('Baxcalibur', 98, ['Glaive Rush', 'Icicle Crash', 'Earthquake', 'Dragon Dance']),
        mon('Greninja', 98, ['Hydro Pump', 'Dark Pulse', 'Ice Beam', 'U-turn']),
        mon('Kingdra', 98, ['Draco Meteor', 'Surf', 'Ice Beam', 'Focus Energy']),
        mon('Toxapex', 98, ['Scald', 'Toxic', 'Recover', 'Haze']),
        mon('Sylveon', 98, ['Hyper Voice', 'Psyshock', 'Calm Mind', 'Wish']),
        mon('Swampert', 98, ['Earthquake', 'Waterfall', 'Ice Punch', 'Stealth Rock'])],
     'Mt. Coronet 6F, de laatste projectie van Palkia'),
]
TR = {t[0].split('_', 1)[1].replace('DEJAVU', 'DEJAVU'): t for t in TRAINERS}


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = '// coronet { (tools/grounded/maptools/coronet.py; id 1057-1059, 1068, 1069, 1082-1088)\n'
    for key, n, *_, why in TRAINERS:
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (key, n, why)
    blk += '// }'
    if '// coronet {' in s:
        i = s.index('// coronet {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for key, n, *_ in TRAINERS:
        hits = re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)
        assert len(hits) == 1, ('trainer-id dubbel', n, hits)
    open(p, 'w').write(s)
    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- coronet (tools/grounded/maptools/coronet.py) --- */\n\n'
    for key, n, nm, cls, pic, gender, music, ai, gfx, team, why in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music,
               'Double Battle: No', ai]
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (key, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde coronet --- */'
    s = bd.replace_block(s, '/* --- coronet', '/* --- einde coronet --- */', blk)
    open(p, 'w').write(s)


# ====================================================================== wilde Pokemon (lv 91-94)
CAVE_A = [('GOLEM', 91, 93), ('MACHAMP', 91, 93), ('PROBOPASS', 91, 93), ('BRONZONG', 91, 93), ('CHIMECHO', 91, 93),
          ('MEDICHAM', 91, 93), ('CROBAT', 92, 93), ('CLEFABLE', 92, 93), ('LUNATONE', 92, 94), ('SOLROCK', 92, 94),
          ('LUCARIO', 93, 94), ('GARCHOMP', 93, 94)]
CAVE_B = [('GOLEM', 92, 93), ('BRONZONG', 92, 93), ('MACHAMP', 92, 93), ('CROBAT', 92, 93), ('PROBOPASS', 92, 93),
          ('CHIMECHO', 92, 93), ('CLEFABLE', 92, 94), ('MEDICHAM', 92, 94), ('NOSEPASS', 92, 94), ('ABSOL', 92, 94),
          ('GABITE', 93, 94), ('SPIRITOMB', 93, 94)]
WILD = {
    CONST[R1]: dict(land=(9, CAVE_A),
                    water=(4, [('WHISCASH', 91, 93), ('GOLDUCK', 91, 93), ('QUAGSIRE', 91, 93), ('GYARADOS', 92, 94),
                               ('MILOTIC', 93, 94)])),
    CONST[R2]: dict(land=(9, CAVE_A)),
    CONST[R3]: dict(land=(9, CAVE_B)),
    CONST[F5]: dict(land=(9, CAVE_B)),
    CONST[F6]: dict(land=(8, [('GOLEM', 93, 94), ('BRONZONG', 93, 94), ('CROBAT', 93, 94), ('PROBOPASS', 93, 94),
                              ('CLEFABLE', 93, 94), ('MEDICHAM', 93, 94), ('CHIMECHO', 93, 94), ('LUCARIO', 93, 94),
                              ('LUNATONE', 93, 94), ('SOLROCK', 93, 94), ('GARCHOMP', 94, 94), ('ABSOL', 94, 94)])),
    CONST[OUT]: dict(land=(20, [('ABOMASNOW', 91, 93), ('WEAVILE', 91, 93), ('MAMOSWINE', 91, 93),
                                ('FROSLASS', 91, 93), ('GLALIE', 91, 93), ('MEDICHAM', 91, 93), ('ALTARIA', 92, 93),
                                ('NOCTOWL', 92, 93), ('ABSOL', 92, 94), ('CLEFABLE', 92, 94), ('LUCARIO', 93, 94),
                                ('GARCHOMP', 93, 94)]),
                     water=(4, [('WHISCASH', 91, 93), ('FLOATZEL', 91, 93), ('QUAGSIRE', 91, 93), ('GYARADOS', 92, 94),
                                ('MILOTIC', 93, 94)]),
                     fishing=(30, [('FEEBAS', 30, 35), ('BARBOACH', 30, 35), ('SEAKING', 60, 70), ('WHISCASH', 60, 70),
                                   ('GYARADOS', 70, 80), ('LUMINEON', 88, 92), ('FLOATZEL', 88, 92),
                                   ('QUAGSIRE', 90, 93), ('LAPRAS', 91, 94), ('MILOTIC', 92, 94)])),
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
                assert len(spec) == {'land': 12, 'water': 5, 'fishing': 10}[kind], (mp, kind)
                assert len({x[0] for x in spec}) == len(spec), ('dubbele soort', mp, kind)
                e[kind + '_mons'] = {'encounter_rate': rate, 'mons': bd.mons(spec)}
        blob = json.dumps(e, indent=2)
        blob = '\n'.join('        ' + ln for ln in blob.split('\n'))
        key = '"map": "MAP_%s"' % mp
        if key in s:
            i = s.index(key); a = s.rindex('{', 0, i)
            depth, j = 0, a
            while True:
                if s[j] == '{': depth += 1
                elif s[j] == '}':
                    depth -= 1
                    if depth == 0: break
                j += 1
            s = s[:a] + blob.lstrip() + s[j + 1:]
        else:                                   # achteraan de lijst van gWildMonHeaders
            end = s.index('"label": "gBattlePyramidWildMonHeaders"')
            j = s.rindex('\n      ]\n    },', 0, end)
            s = s[:j] + ',\n' + blob + s[j:]
    json.loads(s)
    open(p, 'w').write(s)


# ====================================================================== mapsec en gevechtsstart
MAPSECS = [('MAPSEC_MT_CORONET', 'MT. CORONET', 'MAPPOPUP_THEME_STONE', 'Mt. Coronet (Spacetime)'),
           ('MAPSEC_SPEAR_PILLAR', 'SPEAR PILLAR', 'MAPPOPUP_THEME_MARBLE', 'Spear Pillar (Spacetime)')]


def mapsecs():
    p = 'src/data/region_map/region_map_sections.json'
    s = open(p).read()
    for mid, nm, *_ in MAPSECS:
        if '"%s"' % mid not in s:
            i = s.rindex('    }\n  ]')
            s = s[:i + 5] + ',\n    {\n      "id": "%s",\n      "name": "%s"\n    }' % (mid, nm) + s[i + 5:]
    json.loads(s)
    open(p, 'w').write(s)
    p = 'src/map_name_popup.c'
    s = open(p).read()
    a = '    [MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_STONE, // Project Grounded: Spacetime Cave\n'
    b = '    [MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: Spacetime Cave\n'
    assert a in s and b in s
    for mid, nm, theme, why in MAPSECS:
        if '[%s - KANTO' % mid not in s:
            s = s.replace(a, a + '    [%s - KANTO_MAPSEC_COUNT] = %s, // Project Grounded: %s\n' % (mid, theme, why), 1)
            s = s.replace(b, b + '    [%s - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: %s\n'
                          % (mid, why), 1)
    open(p, 'w').write(s)


def battle_setup():
    p = 'src/battle_setup.c'
    s = open(p).read()
    if 'case SPECIES_DIALGA' not in s:
        a = '    case SPECIES_ZERAORA:'
        assert a in s
        s = s.replace(a, '    case SPECIES_DIALGA: // Project Grounded: Spear Pillar (placeholder: Kanto-legendary-thema, '
                         'de klok draait rond)\n    case SPECIES_DIALGA_ORIGIN:\n'
                         '        CreateBattleStartTask(B_TRANSITION_CLOCKWISE_WIPE, MUS_RG_VS_LEGEND);\n        break;\n'
                         '    case SPECIES_PALKIA: // Project Grounded: Spear Pillar (placeholder: Kanto-legendary-thema, '
                         'de ruimte rimpelt)\n    case SPECIES_PALKIA_ORIGIN:\n'
                         '        CreateBattleStartTask(B_TRANSITION_RIPPLE, MUS_RG_VS_LEGEND);\n        break;\n' + a, 1)
        open(p, 'w').write(s)


# ====================================================================== events en scripts
TEXTS = {  # sleutel -> (intro, verloren, daarna)
    'TICK': ("I am a projection of DIALGA. Technically I'm a trainer who hasn't been born yet.\n\n"
             "Don't worry about it. I don't.",
             "Ah. So that's how this ends. I always wondered.",
             "Time is a flat circle. Mostly it's just flat. Like my team, apparently."),
    'PARALLAX': ("Hi! I'm a projection of PALKIA. From over there, I look closer than I am.\n\n"
                 "From over here too, actually. Space is weird.",
                 "Objects in defeat are smaller than they appear.",
                 "PALKIA projects us so nobody walks up to Spear Pillar unannounced. We're the doorbell."),
    'AEON': ("I've waited here for an aeon. That's DIALGA's little joke.\n\nIt has been eleven minutes.",
             "Eleven minutes and one loss. A productive day.",
             "Every time someone beats me, DIALGA rewinds me. I've lost this fight four hundred times.\n\n"
             "You're the first who said 'oops'."),
    'VOIDA': ("The void between dimensions is cold, dark and full of my ex.\n\nPALKIA projected me out of it. "
              "I owe it one fight.",
              "Back to the void. At least it doesn't judge my GHOST types.",
              "If you hear whispering on this mountain, it's not me. It's the other me. Two dimensions over."),
    'MOMENTUM': ("A body in motion stays in motion! That's physics! I'm a projection, so it's also my entire "
                 "personality!",
                 "An unstoppable force met an immovable object. The object was you.",
                 "DIALGA says I'm 'temporally unstable'. My doctor said the same about my knees."),
    'ORBIT': ("I orbit this cave entrance at a distance of exactly three tiles.\n\nCross my orbit and gravity "
              "takes over. Gravity is me.",
              "My orbit decayed. That's the polite word for it.",
              "PALKIA folds space so the cave is bigger inside. That's why the rent is so high."),
    'EPOCH': ("Every fossil on my team was alive yesterday. Not your yesterday. DIALGA's.",
              "Extinct again. They're used to it.",
              "Time is just very slow archaeology."),
    'VERTEX': ("Every DRAGON you see is a point in space where PALKIA got bored.\n\nI am the tip of the spear. "
               "Literally. Look up.",
               "Pointless. Which is ironic, for a vertex.",
               "Up the ladder it gets narrower. Space does that up here. So does my patience."),
    'DEJAVU': ("Have we done this before? We've done this before. I'm sure we've done this before.",
               "...We've definitely done this before. You won then too.",
               "Next time, I'm doing something different. I said that last time."),
    'NEBULA': ("A nebula is where stars are born. I'm where trainers come to lose. Close enough!",
               "A star is born. It's you. I hate it.",
               "Above us is SPEAR PILLAR. Above that is space. PALKIA owns both. No visitors after midnight."),
    'CHRONOS': ("I am the last of DIALGA's projections. DIALGA has watched every possible version of this "
                "battle.\n\nIn most of them you brought more Revives.",
                "Interesting. That was one of the rare timelines.",
                "Go on. DIALGA waits at the top. It already knows how this ends. It just likes to watch."),
    'SPATIA': ("I am the last of PALKIA's projections. Between you and SPEAR PILLAR lies exactly one trainer "
               "and an unreasonable amount of space.",
               "The space between us has been... resolved.",
               "The light at the top is SPEAR PILLAR. Don't touch the pearl unless you mean it. Same for the "
               "diamond. Same for most things."),
}


def tr_obj(key, xy, face, sight, script):
    gfx = TR[key][8]
    return tr(gfx, xy[0], xy[1], script, face, sight)


def trainers_on(S, table):
    objs = []
    for key, (xy, face, n) in table.items():
        k = 'CORONET_' + key
        script = S.trainer(key.title(), k, *TEXTS[key])
        objs.append(tr_obj(key, xy, face, n, script))
    return objs


def events():
    # ---------------------------------------------------------------- 4F kamer 1
    S = Scr(R1, head(R1))
    objs = trainers_on(S, R1_TRAINERS)
    S.write()
    io, ib = items_ev(R1)
    write_map(R1, objs + io, [warp(R1_ENTRY[0], R1_ENTRY[1], HUB_DEST[0], HUB_DEST[1], elev=3),
                              warp(R1_HOLE[0], R1_HOLE[1], CONST[OUT], 0, elev=3)], ib)
    # ---------------------------------------------------------------- 4F buiten
    S = Scr(OUT, head(OUT))
    objs = trainers_on(S, OUT_TRAINERS)
    S.npc('Sign', "MT. CORONET, 4F (exterior)\n\nThe summit is up. Everything is up, eventually.\n\n"
          "Do not feed the projections.", 'MSGBOX_SIGN')
    S.write()
    io, ib = items_ev(OUT)
    d1, d2, d3 = OUT_DOORS['r1'], OUT_DOORS['r2'], OUT_DOORS['r3']
    warps = [warp(d1[0], d1[1], CONST[R1], 1), warp(d2[0], d2[1], CONST[R2], 0), warp(d3[0], d3[1], CONST[R3], 0)]
    bgs = [bd.sign(d1[0] + 2, d1[1] + 2, S.P + 'Sign')] + ib
    write_map(OUT, objs + io, warps, bgs, weather='WEATHER_SNOW', map_type='MAP_TYPE_ROUTE')
    # ---------------------------------------------------------------- 4F kamer 2
    S = Scr(R2, head(R2))
    S.write()
    io, ib = items_ev(R2)
    rock = obj('OBJ_EVENT_GFX_BREAKABLE_ROCK', R2_ROCK[0], R2_ROCK[1], 'EventScript_RockSmash', '0',
               'MOVEMENT_TYPE_LOOK_AROUND')
    write_map(R2, io + [rock], [warp(R2_ENTRY[0], R2_ENTRY[1], CONST[OUT], 1, elev=3)], ib)
    # ---------------------------------------------------------------- 4F kamer 3
    S = Scr(R3, head(R3))
    objs = trainers_on(S, R3_TRAINERS)
    S.write()
    io, ib = items_ev(R3)
    write_map(R3, objs + io, [warp(R3_ENTRY[0], R3_ENTRY[1], CONST[OUT], 2, elev=3),
                              warp(R3_LADDER[0], R3_LADDER[1], CONST[F5], 0, elev=3)], ib)
    # ---------------------------------------------------------------- 5F
    S = Scr(F5, head(F5))
    objs = trainers_on(S, F5_TRAINERS)
    S.write()
    io, ib = items_ev(F5)
    objs += io + [cs.boulder(*xy) for xy in F5_BOULDERS]
    write_map(F5, objs, [warp(F5_ARRIVE[0], F5_ARRIVE[1], CONST[R3], 1, elev=3),
                         warp(F5_LADDER[0], F5_LADDER[1], CONST[F6], 0, elev=3)], ib)
    # ---------------------------------------------------------------- 6F
    S = Scr(F6, head(F6))
    objs = trainers_on(S, F6_TRAINERS)
    S.write()
    io, ib = items_ev(F6)
    write_map(F6, objs + io, [warp(F6_ARRIVE[0], F6_ARRIVE[1], CONST[F5], 1, elev=3),
                              warp(F6_HOLE[0], F6_HOLE[1], CONST[SP], 0, elev=3)], ib)
    # ---------------------------------------------------------------- Spear Pillar
    S = Scr(SP, head(SP, [('MAP_SCRIPT_ON_TRANSITION', SP + '_OnTransition')]))
    P, T = S.P, S.T
    code = f"""{SP}_OnTransition:
	setflag FLAG_HIDE_CORONET_DIALGA
	setflag FLAG_HIDE_CORONET_PALKIA
	end
"""
    texts = []
    for kind, other in (('DIALGA', 'PALKIA'), ('PALKIA', 'DIALGA')):
        K = kind.title()
        code += f"""
{P}{K}Altar::
	lock
	goto_if_set FLAG_CORONET_{kind}_DONE, {P}{K}Empty
	msgbox {T}{K}Altar, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	clearflag FLAG_HIDE_CORONET_{kind}
	addobject LOCALID_CORONET_{kind}
	playmoncry SPECIES_{kind}, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox {T}{K}Appears, MSGBOX_DEFAULT
	closemessage
	setwildbattle SPECIES_{kind}, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	removeobject LOCALID_CORONET_{kind}
	setflag FLAG_HIDE_CORONET_{kind}
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}{K}Fled
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}{K}Fled
	setflag FLAG_CORONET_{kind}_DONE
	goto_if_set FLAG_CORONET_{other}_DONE, {P}BothDone
	msgbox {T}{K}Done, MSGBOX_DEFAULT
	release
	end

{P}{K}Fled::
	msgbox {T}{K}Fled, MSGBOX_DEFAULT
	release
	end

{P}{K}Empty::
	msgbox {T}{K}Empty, MSGBOX_DEFAULT
	release
	end
"""
    code += f"""
{P}BothDone::
	msgbox {T}BothDone, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_SPACETIME_CORONET_DONE
	setvar VAR_0x8004, 3
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 16
	setvar VAR_0x8007, 2
	special ShakeCamera
	waitstate
	playse SE_M_TELEPORT
	waitse
	warp MAP_{HUB_DEST[0]}, {HUB_DEST[1]}
	waitstate
	release
	end
"""
    texts = [
        ('DialgaAltar', "A diamond floats above the altar, ticking.\n\nNot like a clock. Like a clock that's "
                        "annoyed with you specifically."),
        ('DialgaAppears', "DIALGA: Gyaaahn!\n\nThe seconds stop counting. One of them looks at you."),
        ('DialgaDone', "The diamond goes quiet. Somewhere a clock gets the time right for the first time "
                       "in centuries.\n\nOn the other altar, the pearl starts to glow."),
        ('DialgaFled', "DIALGA rewinds itself to before you showed up.\n\nThe diamond ticks again. It's very "
                       "smug about it."),
        ('DialgaEmpty', "The diamond is still. It's just a very expensive rock now."),
        ('PalkiaAltar', "A pearl hangs over the altar. The air around it bends, as if the pearl takes up more "
                        "room than it should."),
        ('PalkiaAppears', "PALKIA: Graaaah!\n\nThe mountain folds in on itself. You are now standing much "
                          "closer to PALKIA than you agreed to."),
        ('PalkiaDone', "The pearl settles. Space unfolds and puts itself back roughly where it was.\n\n"
                       "On the other altar, the diamond starts ticking."),
        ('PalkiaFled', "PALKIA steps sideways into a dimension you weren't invited to.\n\nThe pearl is still "
                       "glowing. Second date?"),
        ('PalkiaEmpty', "The pearl is still. Space here is perfectly normal. It's unsettling."),
        ('BothDone', "Time and space both stop to look at you.\n\nThat's never a good sign.\n\n"
                     "SPEAR PILLAR folds up like a pop-up book, and you are the part that doesn't fit."),
    ]
    S.raw(code, texts)
    S.write()
    io, ib = items_ev(SP)
    objs = io
    for kind in ('DIALGA', 'PALKIA'):
        x, y = SP_MON[kind]
        objs.append(obj('OBJ_EVENT_GFX_SPECIES(%s)' % kind, x, y, '0x0', 'FLAG_HIDE_CORONET_' + kind,
                        move='MOVEMENT_TYPE_FACE_DOWN', local_id='LOCALID_CORONET_' + kind))
    bgs = ib
    for kind, (x, y) in SP_ALTARS.items():
        for dx in (0, 1):
            bgs.append(bd.sign(x + dx, y + 1, P + kind.title() + 'Altar', 'BG_EVENT_PLAYER_FACING_NORTH'))
    write_map(SP, objs, [warp(SP_ENTRY[0][0], SP_ENTRY[0][1], CONST[F6], 1, elev=3),
                         warp(SP_ENTRY[1][0], SP_ENTRY[1][1], CONST[F6], 1, elev=3)], bgs,
              map_type='MAP_TYPE_ROUTE')


# ====================================================================== controles
FACE = {'DOWN': (0, 1), 'UP': (0, -1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}


def checks():
    for name in ORDER:
        g = MAPS[name]
        d = json.load(open('data/maps/%s/map.json' % name))
        objs = [o for o in d['object_events'] if 'SPECIES(' not in o['graphics_id']]
        start = (d['warp_events'][0]['x'], d['warp_events'][0]['y'])
        solid = {(o['x'], o['y']) for o in objs} - {start}
        movable = {(o['x'], o['y']) for o in objs if 'BOULDER' in o['graphics_id'] or 'BREAKABLE' in o['graphics_id']}
        r_all = mf.reachable(g, start, solid - movable)
        for o in objs:
            p = (o['x'], o['y'])
            assert not g[p[1]][p[0]] & 0xC00 or 'BOULDER' in o['graphics_id'], (name, 'object op een muur', o['script'], p)
            assert mf.next_to(r_all, *p) or p in r_all, (name, 'object onbereikbaar', o['script'], p)
            if o['trainer_type'] == 'TRAINER_TYPE_NORMAL':
                dx, dy = FACE[o['movement_type'].split('_')[-1]]
                for k in range(1, int(o['trainer_sight_or_berry_tree_id']) + 1):
                    assert (o['x'] + dx * k, o['y'] + dy * k) in r_all, (name, 'zichtlijn', o['script'], k)
        for w in d['warp_events']:
            assert (w['x'], w['y']) in r_all or (w['x'], w['y']) == start, (name, 'warp onbereikbaar', w)
        for b in d['bg_events']:
            p = (b['x'], b['y'])
            assert p in r_all if b['type'] == 'hidden_item' else mf.next_to(r_all, *p), (name, 'bg onbereikbaar', p)
        print('%-22s bereikbaar: %d tegels' % (name, len(r_all)))
    # 5F: het puinhek houdt de bovenste laag dicht; een duwsteen twee keer omhoog opent hem
    g = MAPS[F5]
    d = json.load(open('data/maps/%s/map.json' % F5))
    solid = {(o['x'], o['y']) for o in d['object_events']} - {F5_ARRIVE}
    assert F5_LADDER not in mf.reachable(g, F5_ARRIVE, solid), '5F: hek lekt'
    for bx, by in F5_BOULDERS:
        assert (bx, by + 1) in mf.reachable(g, F5_ARRIVE, solid - {(bx, by)}), ('5F: duwplek', bx)
        moved = (solid - {(bx, by)}) | {(bx, by - 2)}
        assert F5_LADDER in mf.reachable(g, F5_ARRIVE, moved), ('5F: ladder na het duwen', bx)
    # buiten: kamer 3 alleen over een bruggetje; beide routes om de berg (west en oost) komen er
    g = [row[:] for row in MAPS[OUT]]
    start = OUT_DOORS['r1']
    for (x, y) in rect(33, 6, 35, 7) | rect(43, 10, 44, 12):
        g[y][x] |= 0x400
    assert not mf.next_to(mf.reachable(g, start), *OUT_DOORS['r3']), 'buiten: kamer 3 zonder brug bereikbaar'
    g = [row[:] for row in MAPS[OUT]]
    for (x, y) in rect(43, 10, 44, 12):
        g[y][x] |= 0x400
    assert OUT_DOORS['r3'] in mf.reachable(g, start), 'buiten: westroute (brug 1) werkt niet'
    g = [row[:] for row in MAPS[OUT]]
    for (x, y) in rect(33, 6, 35, 7):
        g[y][x] |= 0x400
    assert OUT_DOORS['r3'] in mf.reachable(g, start), 'buiten: oostroute (brug 2) werkt niet'


def render(name, out):
    H = len(MAPS[name])
    subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', name, out, '0', str(H)], check=True,
                   capture_output=True)
    from PIL import Image
    im = Image.open(out).convert('RGB')
    W = len(MAPS[name][0])
    im.crop((0, 0, W * 16, H * 16)).save(out)


def overview(dirn):
    from PIL import Image
    ims = {n: Image.open(os.path.join(dirn, n + '.png')) for n in ORDER}
    col1 = [R1, R2, R3]
    col2 = [OUT]
    col3 = [F5, F6]
    col4 = [SP]
    cols = [col1, col2, col3, col4]
    W = sum(max(ims[n].width for n in c) for c in cols) + 16 * (len(cols) + 1)
    H = max(sum(ims[n].height + 16 for n in c) for c in cols) + 16
    o = Image.new('RGB', (W, H), (16, 16, 24))
    x = 16
    for c in cols:
        y = 16
        for n in c:
            o.paste(ims[n], (x, y)); y += ims[n].height + 16
        x += max(ims[n].width for n in c) + 16
    o.save(os.path.join(dirn, 'overzicht.png'))


def main():
    flags()
    ni = new_items()
    build_maps(ni)
    mapsecs()
    events()
    trainers()
    wild()
    battle_setup()
    checks()
    if len(sys.argv) > 1:
        for name in ORDER:
            render(name, os.path.join(sys.argv[1], name + '.png'))
        overview(sys.argv[1])


if __name__ == '__main__':
    main()
