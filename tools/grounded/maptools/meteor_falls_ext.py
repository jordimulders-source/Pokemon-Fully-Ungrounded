"""Project Grounded: uitbreiding van Meteor Falls ("de diepte").

Bouwt (vaste seed, idempotent):
- MeteorFalls_B1F_2R  (vergroot): de Bagon-kamer naar beneden. Ingang (vanaf B1F_1R, Surf) onderin. Een laag terras
  met trap, een hoge klif met een brede waterval (Waterfall) naar een bovenmeer, meteorietbrokken en een
  Strength-puzzel naar het TM-plateau (Dragon Claw). Verborgen: een grotgat naast de waterval (alleen surfend
  bereikbaar: "achter de waterval") en een scheur in de muur achter een brokkelrots (Rock Smash).
- MeteorFalls_HiddenFalls   : grot achter de waterval (Dragon Scale, Max Elixir).
- MeteorFalls_Tunnels       : de Draconid-gangen, een doolhof met trainers dat drie kamers verbindt. Onder een
  brokkelrots zit een verborgen gat in de vloer (vallen naar de Sterrenvalgrot).
- MeteorFalls_StarCore      : de meteorietkern, Minior-wolk + vaste Salamence.
- MeteorFalls_DraconidShrine: oude Draconid-schrijn met de Draconid-oudere (gesprek, gevecht, Dragon Fang).
- MeteorFalls_EchoChamber   : echokamer; de echo verraadt het gat onder de zingende steen.
- MeteorFalls_StarfallGrotto: waar je na het gat landt (Comet Shard, Star Piece); trap terug naar de gangen.

Stijl zoals vanilla Meteor Falls 1F: uitgehakte kamers in rots (rotsrand 234/23c, onderrand 236, noordwand met
stalactieten 244 onder een rand 23e), terrassen (23e + 219 met trap 202), klif 23e/219/244x3, waterval uit 1F.
Gebruik: python3 tools/grounded/maptools/meteor_falls_ext.py [rendermap]"""
import json, os, shutil, struct, random, sys
from collections import deque

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)

# ---------------------------------------------------------------------------------------------------- metatiles
ROCK, FLOOR = 0x201, 0x201
EDGE_E, EDGE_W = 0x234, 0x23c          # rotsrand met de vloer rechts / links ervan
LIP_N, LIP_S = 0x23e, 0x236            # rand boven een noordwand / onderrand van een kamer
LIP_NW, LIP_NE = 0x23f, 0x23d          # hoeken van de bovenrand
LIP_S1, LIP_S2 = 0x286, 0x286          # zuidrand (ring 1 en 2)
STAL, STAL_L, STAL_R = 0x244, 0x22f, 0x22e   # stalactietenwand, met linker- en rechterrand
FACE = 0x219                           # lage klifwand (terras)
STAIRS = 0x202
CAVE_HOLE = [(0x245, 0x246, 0x247), (0x24d, 0x24e, 0x24f)]   # grotgat in een stalactietenwand (warp op 24e)
EXIT_S = (0x27d, 0x27e, 0x27f)         # uitgang in de onderrand
EXIT_MAT = 0x207                       # vloer met zuidpijl-warp
LADDER = 0x20d
HOLE = 0x206                           # gat in de vloer (MB_CRACKED_FLOOR_HOLE)
RUBBLE = (0x20e, 0x20f, 0x21f)         # losse steentjes (decor, blokkeert)
CRATER = ((0x282, 0x283), (0x28a, 0x28b))
PILLAR = ((0x264, 0x265), (0x26c, 0x26d), (0x274, 0x275))          # zuil in een stalactietenwand (3 hoog)
PILLAR4 = ((0x266, 0x267), (0x26e, 0x26f), (0x26e, 0x26f), (0x276, 0x277))
W_C, W_N, W_NW, W_NE, W_W, W_E, W_SHORE = 0x170, 0x189, 0x180, 0x181, 0x190, 0x192, 0x21e
W_INNER_NW, W_INNER_NE = 0x198, 0x19a     # binnenhoeken (land linksboven / rechtsboven)
# waterval (uit MeteorFalls_1F_1R, 8 breed): rand 23e-rij, valtop, val, voet, schuim
WF_EDGE = (0x237, 0x179, 0x178, 0x235)
WF_TOP, WF_TOP_L, WF_TOP_R, WF_MID, WF_FOOT, WF_FOAM = 0xb3, 0xbb, 0xbc, 0xb9, 0x4c, 0x54

E_FLOOR, E_WATER = 3, 1


def cell(mt, coll, elev):
    return mt | (coll << 10) | (elev << 12)


class Map:
    """Raster met klassen: 'R' rots, 'F' vloer, 'W' water. Na build() staan de metatiles in .g; overrides daarna."""

    def __init__(self, w, h):
        self.W, self.H = w, h
        self.k = [['R'] * w for _ in range(h)]
        self.over = {}            # (x,y) -> (metatile, collision, elevation) na het autotilen
        self.bands = []           # terrassen/kliffen

    def room(self, x0, y0, x1, y1, kind='F'):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.k[y][x] = kind

    def water(self, x0, y0, x1, y1):
        self.room(x0, y0, x1, y1, 'W')

    def isF(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H and self.k[y][x] in 'FW'

    def set(self, x, y, mt, coll=0, elev=E_FLOOR):
        self.over[(x, y)] = (mt, coll, elev)

    def build(self):
        g = [[cell(ROCK, 1, 0)] * self.W for _ in range(self.H)]
        for y in range(self.H):
            for x in range(self.W):
                c = self.k[y][x]
                if c == 'F':
                    above_w = y > 0 and self.k[y - 1][x] == 'W'
                    g[y][x] = cell(W_SHORE if above_w else FLOOR, 0, E_FLOOR)
                elif c == 'W':
                    g[y][x] = cell(self.water_tile(x, y), 0, E_WATER)
                else:
                    g[y][x] = cell(self.rock_tile(x, y), 1, 0)
        for (x, y), (mt, coll, elev) in self.over.items():
            g[y][x] = cell(mt, coll, elev)
        self.g = g
        return g

    def water_tile(self, x, y):
        isw = lambda xx, yy: 0 <= xx < self.W and 0 <= yy < self.H and self.k[yy][xx] == 'W'
        n, w, e = isw(x, y - 1), isw(x - 1, y), isw(x + 1, y)
        if not n and not w:
            return W_NW
        if not n and not e:
            return W_NE
        if not n:
            return W_N
        if not w:
            return W_W
        if not e:
            return W_E
        if not isw(x - 1, y - 1):
            return W_INNER_NW
        if not isw(x + 1, y - 1):
            return W_INNER_NE
        return W_C

    def rock_tile(self, x, y):
        """Ringen rond de vloer (Chebyshev-afstand 1-3), zoals MeteorFalls_B1F_2R: noordwand 231/231/23e,
        westwand 212/22a/234, oostwand 210/228/23c, zuidrand 286; diagonale hoeken 213/214."""
        for r in (1, 2, 3):
            types = set()
            for b in range(-r, r + 1):
                for a in range(-r, r + 1):
                    if max(abs(a), abs(b)) != r or not self.isF(x + a, y + b):
                        continue
                    if b > 0 and abs(a) < b:
                        types.add('N')
                    elif b > 0 and a == b:
                        types.add('NW')
                    elif b > 0 and -a == b:
                        types.add('NE')
                    elif a > 0 and a > abs(b):
                        types.add('W')
                    elif a < 0 and -a > abs(b):
                        types.add('E')
                    else:
                        types.add('S')
            if not types:
                continue
            if r == 3:
                if 'N' in types:
                    return LIP_N
                if 'W' in types and 'S' not in types:
                    return EDGE_E
                if 'E' in types and 'S' not in types:
                    return EDGE_W
                return ROCK
            if 'N' in types:
                if 'W' in types:
                    return 0x232
                if 'E' in types:
                    return 0x230
                return 0x231
            if 'W' in types:
                return 0x212 if r == 1 else 0x22a
            if 'E' in types:
                return 0x210 if r == 1 else 0x228
            if 'NW' in types and 'NE' not in types:
                return 0x213
            if 'NE' in types and 'NW' not in types:
                return 0x214
            if 'NW' in types:
                return 0x231
            return LIP_S2 if r == 2 else LIP_S1
        return ROCK

    # ---------------------------------------------------------------- stempels (na build, als overrides)
    def step(self, x0, x1, y, stairs=()):
        """Laag terras: rij y = bovenrand (beloopbaar, hoort bij het hoge deel), rij y+1 = wand met trappen."""
        for x in range(x0, x1 + 1):
            self.set(x, y, LIP_N)
            self.set(x, y + 1, STAIRS if x in stairs else FACE, 0 if x in stairs else 1)

    def cliff(self, x0, x1, y, stairs=(), pillars=()):
        """Hoge klif: 23e (beloopbaar), 219, 244 x3 (geblokkeerd). Vloer weer vanaf y+5."""
        for x in range(x0, x1 + 1):
            self.set(x, y, LIP_N)
            self.set(x, y + 1, FACE, 1)
            for i in (2, 3, 4):
                self.set(x, y + i, STAL, 1)
        for px in pillars:
            for i, row in enumerate(PILLAR):
                self.set(px, y + 2 + i, row[0], 1); self.set(px + 1, y + 2 + i, row[1], 1)

    def waterfall(self, x0, y):
        """Waterval van 8 breed (x0..x0+7) in een hoge klif die op rij y begint; bovenmeer eindigt op y-1, ondermeer
        begint op y+5 (schuimrij). Randtegels op x0-1 en x0+8."""
        self.set(x0 - 1, y, WF_EDGE[0], 1); self.set(x0 + 8, y, WF_EDGE[3], 1)
        self.set(x0, y, WF_EDGE[1], 0, E_WATER); self.set(x0 + 7, y, WF_EDGE[2], 0, E_WATER)
        for x in range(x0 + 1, x0 + 7):
            self.set(x, y, W_C, 0, E_WATER)
        for i in (1, 2, 3, 4):
            self.set(x0 - 1, y + i, STAL_L, 1); self.set(x0 + 8, y + i, STAL_R, 1)
        for x in range(x0, x0 + 8):
            self.set(x, y + 1, WF_TOP_L if x == x0 else WF_TOP_R if x == x0 + 7 else WF_TOP, 0, E_WATER)
            self.set(x, y + 2, WF_MID, 0, E_WATER); self.set(x, y + 3, WF_MID, 0, E_WATER)
            self.set(x, y + 4, WF_FOOT, 0, E_WATER)
            self.set(x, y + 5, WF_FOAM, 0, E_WATER)

    def stal_wall(self, x0, x1, y0, pillars=()):
        """Noordwand van een kamer (vloer begint op y0) als hoge stalactietenwand: 23e + 244 x3, zuilen."""
        for x in range(x0, x1 + 1):
            self.set(x, y0 - 4, LIP_N, 1)
            for i in (1, 2, 3):
                self.set(x, y0 - i, STAL_L if x == x0 else STAL_R if x == x1 else STAL, 1)
        for px in pillars:
            for i, row in enumerate(PILLAR):
                self.set(px, y0 - 3 + i, row[0], 1); self.set(px + 1, y0 - 3 + i, row[1], 1)

    def cave_hole(self, x, y):
        """Grotgat in een stalactietenwand; (x,y) = de warptegel (onderste rij, midden)."""
        for dy, row in enumerate(CAVE_HOLE):
            for dx, mt in enumerate(row):
                self.set(x - 1 + dx, y - 1 + dy, mt, 0 if (dx == 1 and dy == 1) else 1)

    def exit_south(self, x, y):
        """Uitgang onderaan: (x,y) = vloertegel met de warp; de onderrand eronder krijgt de opening."""
        self.set(x, y, EXIT_MAT)
        for dx, mt in enumerate(EXIT_S):
            self.set(x - 1 + dx, y + 1, mt, 1)

    def crater(self, x, y):
        for dy in range(2):
            for dx in range(2):
                self.set(x + dx, y + dy, CRATER[dy][dx], 1)

    def rubble(self, rnd, n, area, avoid):
        x0, y0, x1, y1 = area
        tries = 0
        while n and tries < 500:
            tries += 1
            x, y = rnd.randint(x0, x1), rnd.randint(y0, y1)
            if self.k[y][x] != 'F' or (x, y) in self.over or (x, y) in avoid:
                continue
            if any((x + dx, y + dy) in avoid for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                continue
            self.set(x, y, rnd.choice(RUBBLE), 1); n -= 1


# ---------------------------------------------------------------------------------------------------- hulp
def reachable(g, start, blocked=(), allow_water=False, extra=()):
    """Botsing + hoogte zoals de engine. Water (hoogte 1) alleen met allow_water (Surf); waterval-tegels tellen
    dan ook mee. 'extra' = cellen die toch beloopbaar zijn (bijv. weggeslagen brokkelrots)."""
    H, W = len(g), len(g[0])
    seen = {start}; q = deque([start])
    while q:
        x, y = q.popleft(); e0 = g[y][x] >> 12
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in seen or (nx, ny) in blocked:
                continue
            v = g[ny][nx]; e = v >> 12
            if (v >> 10) & 3 and (nx, ny) not in extra:
                continue
            if e == 1 or e0 == 1:
                if not allow_water:
                    continue
            elif not (e == e0 or e in (0, 15) or e0 in (0, 15)):
                continue
            seen.add((nx, ny)); q.append((nx, ny))
    return seen


def next_to(r, x, y):
    return any((x + dx, y + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def save_layout(name, g):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', t) for r in g for t in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *([cell(ROCK, 1, 0)] * 4)))


def add_layout(name, const, w, h, after):
    lj = open('data/layouts/layouts.json').read()
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"name": "%s_Layout"' % name)
        j = lj.index('}', i)
        blk = lj[i:j]
        import re
        nb = re.sub(r'"width": \d+', '"width": %d' % w, blk)
        nb = re.sub(r'"height": \d+', '"height": %d' % h, nb)
        lj = lj[:i] + nb + lj[j:]
        open('data/layouts/layouts.json', 'w').write(lj)
        return
    i = lj.index('"name": "%s"' % after); j = lj.index('},', i) + 2
    lj = lj[:j] + '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_MeteorFalls",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (const, name, w, h, name, name) + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)


def add_to_grounded_group(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name in g:
        return
    i = g.index('"gMapGroup_Grounded": [')
    j = g.index(']', i)
    body = g[i:j].rstrip()
    g = g[:i] + body + ',\n    "%s"\n  ' % name + g[j:]
    open('data/maps/map_groups.json', 'w').write(g)


def add_include(name, after):
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        a = '\t.include "data/maps/%s/scripts.inc"\n' % after
        assert a in es, after
        es = es.replace(a, a + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def write_json(path, d):
    open(path, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')


def obj(gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', sight='0', lid=None, ttype='TRAINER_TYPE_NONE',
        elev=3, rx=0, ry=0):
    o = {}
    if lid:
        o['local_id'] = lid
    o.update({'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
              'movement_range_x': rx, 'movement_range_y': ry, 'trainer_type': ttype,
              'trainer_sight_or_berry_tree_id': sight, 'script': script, 'flag': flag})
    return o


def item(x, y, it, flag):
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', flag, 'MOVEMENT_TYPE_LOOK_AROUND', it)


def trainer(gfx, x, y, script, face, sight):
    return obj(gfx, x, y, script, '0', 'MOVEMENT_TYPE_FACE_' + face, str(sight), ttype='TRAINER_TYPE_NORMAL')


def rocksmash(x, y):
    return obj('OBJ_EVENT_GFX_BREAKABLE_ROCK', x, y, 'EventScript_RockSmash', '0', 'MOVEMENT_TYPE_LOOK_AROUND')


def boulder(x, y):
    return obj('OBJ_EVENT_GFX_PUSHABLE_BOULDER', x, y, 'EventScript_StrengthBoulder', '0', 'MOVEMENT_TYPE_LOOK_AROUND')


def meteorite(x, y, script):
    return obj('OBJ_EVENT_GFX_DEOXYS_TRIANGLE', x, y, script, '0', 'MOVEMENT_TYPE_LOOK_AROUND')


def sign(x, y, script, facing='BG_EVENT_PLAYER_FACING_ANY'):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': facing, 'script': script}


def warp(x, y, elev, dest, wid):
    return {'x': x, 'y': y, 'elevation': elev, 'dest_map': 'MAP_' + dest, 'dest_warp_id': str(wid)}


def map_json(const, name, music, objs, warps, signs, coords=()):
    return {'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + const, 'music': music,
            'region_map_section': 'MAPSEC_METEOR_FALLS', 'requires_flash': False, 'weather': 'WEATHER_NONE',
            'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': True,
            'allow_running': True, 'show_map_name': False, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL',
            'connections': None, 'object_events': list(objs), 'warp_events': list(warps),
            'coord_events': list(coords), 'bg_events': list(signs)}


# ==================================================================================================== kaarten
B2R, B2R_C = 'MeteorFalls_B1F_2R', 'METEOR_FALLS_B1F_2R'
TUN, TUN_C = 'MeteorFalls_Tunnels', 'METEOR_FALLS_TUNNELS'
CORE, CORE_C = 'MeteorFalls_StarCore', 'METEOR_FALLS_STAR_CORE'
SHR, SHR_C = 'MeteorFalls_DraconidShrine', 'METEOR_FALLS_DRACONID_SHRINE'
ECHO, ECHO_C = 'MeteorFalls_EchoChamber', 'METEOR_FALLS_ECHO_CHAMBER'
GROT, GROT_C = 'MeteorFalls_StarfallGrotto', 'METEOR_FALLS_STARFALL_GROTTO'
HFALL, HFALL_C = 'MeteorFalls_HiddenFalls', 'METEOR_FALLS_HIDDEN_FALLS'
MUSIC = 'MUS_CAVE_OF_ORIGIN'
MAPS = {}      # naam -> (Map, grid)


def build_b1f_2r():
    """De Bagon-kamer, nu een diep bekken in drie lagen. Onder: ingangshal (uitgang naar B1F_1R) met een
    Strength-nis; trap omhoog naar de middenlaag met het ondermeer; via de waterval (Waterfall) naar de bovenlaag
    met het bovenmeer, de Dragon Claw en de brokkelrots voor de scheur naar de Draconid-gangen. Naast de waterval
    een grotgat dat je alleen surfend haalt (HiddenFalls)."""
    m = Map(40, 50)
    m.room(4, 5, 35, 32)                  # boven- en middenlaag (+ terrasrand)
    m.room(17, 33, 35, 47)                # ingangshal
    m.room(4, 36, 9, 40)                  # de nis
    m.room(10, 38, 16, 38)                # smalle gang met het rotsblok (Strength)
    m.water(21, 8, 30, 13)                # bovenmeer
    m.water(18, 19, 29, 28)               # ondermeer (onder de waterval)
    m.water(30, 20, 35, 28)
    m.build()
    m.cliff(4, 35, 14, pillars=(7, 13, 33))
    m.waterfall(22, 14)
    m.cave_hole(32, 18)                   # "achter de waterval"
    m.step(17, 35, 31, stairs=(26, 27))
    for x in range(4, 17):                # links geen terras: de middenlaag houdt hier op
        m.k[31][x] = m.k[32][x] = 'R'
    m.cave_hole(12, 4)                    # scheur naar de gangen (brokkelrots ervoor op 12,5)
    m.exit_south(20, 47)
    m.crater(28, 41); m.crater(6, 22); m.crater(32, 9)
    rnd = random.Random(6315)
    keep = {(12, 5), (12, 6), (20, 46), (20, 45), (26, 30), (27, 30), (26, 33), (27, 33), (16, 38), (17, 38), (15, 38),
            (32, 19), (6, 6), (5, 37), (7, 39), (11, 10), (17, 36), (29, 36), (24, 44), (10, 24), (8, 9)}
    m.rubble(rnd, 7, (4, 33, 35, 46), keep)
    m.rubble(rnd, 5, (4, 19, 17, 30), keep)
    m.rubble(rnd, 4, (4, 5, 20, 13), keep)
    g = m.build()
    return m, g


# ---------------------------------------------------------------------------------------------------- gangen
NODE = lambda i, j: (4 + 9 * i, 6 + 9 * j)          # linkerbovenhoek van een 3x3-knooppunt
TUN_EDGES = [((2, 3), (1, 3)), ((1, 3), (0, 3)), ((0, 3), (0, 2)), ((0, 2), (1, 2)), ((1, 2), (1, 1)),
             ((1, 1), (0, 1)), ((0, 1), (0, 0)), ((1, 1), (2, 1)), ((2, 1), (2, 0)), ((2, 0), (1, 0)),
             ((2, 3), (3, 3)), ((3, 3), (4, 3)), ((4, 3), (4, 2)), ((4, 2), (3, 2)), ((3, 2), (2, 2)),
             ((4, 2), (4, 1)), ((4, 1), (3, 1)), ((3, 1), (3, 0)), ((3, 0), (4, 0)), ((2, 1), (3, 1))]
TUN_HOLE = (23, 25)            # verborgen gat onder een brokkelrots (knooppunt 2,2: doodlopend)
TUN_GROTTO_EXIT = (23, 37)     # aankomst vanuit de Sterrenvalgrot


def build_tunnels():
    """De Draconid-gangen: een doolhof van 5x4 knooppunten met gangen van 3 breed (6 rots ertussen, zodat de
    wanden niet in elkaar lopen). Ingang onderin (vanaf B1F_2R), grotgaten bovenin naar de schrijn (links),
    de meteorietkern (midden) en de echokamer (rechts)."""
    m = Map(47, 44)
    for i in range(5):
        for j in range(4):
            x, y = NODE(i, j); m.room(x, y, x + 2, y + 2)
    for (a, b) in TUN_EDGES:
        (x0, y0), (x1, y1) = NODE(*a), NODE(*b)
        m.room(min(x0, x1), min(y0, y1), max(x0, x1) + 2, max(y0, y1) + 2)
    m.room(22, 36, 24, 40)                     # naar de uitgang
    m.build()
    m.exit_south(23, 40)
    m.cave_hole(5, 5); m.cave_hole(23, 5); m.cave_hole(41, 5)
    m.set(*TUN_HOLE, HOLE)
    rnd = random.Random(1983)
    keep = {(5, 6), (23, 6), (41, 6), (22, 25), (24, 25), (23, 24), (23, 26), TUN_GROTTO_EXIT, (23, 38), (23, 39),
            (8, 34), (14, 15), (41, 24), (37, 7), (14, 7), (4, 35), (42, 35)}
    for (a, b) in TUN_EDGES:
        (x0, y0), (x1, y1) = NODE(*a), NODE(*b)
        if rnd.random() < 0.45:
            xa, ya = (min(x0, x1), min(y0, y1))
            xb, yb = (max(x0, x1) + 2, max(y0, y1) + 2)
            # alleen in de rand van de gang, nooit in het midden (de gang blijft begaanbaar)
            if ya == yb - 2:
                xx = rnd.randint(xa + 3, xb - 3); yy = rnd.choice((ya, yb))
            else:
                yy = rnd.randint(ya + 3, yb - 3); xx = rnd.choice((xa, xb))
            if (xx, yy) not in keep and (xx, yy) not in m.over:
                m.set(xx, yy, rnd.choice(RUBBLE), 1)
    g = m.build()
    return m, g


def simple_room(w, h, x0, y0, x1, y1, exit_xy):
    m = Map(w, h)
    m.room(x0, y0, x1, y1)
    return m


def build_core():
    """De meteorietkern: een ronde kamer rond een krater, Minior-wolk en een vaste Salamence."""
    m = Map(26, 24)
    m.room(4, 5, 21, 19)
    m.build()
    m.stal_wall(4, 21, 5, pillars=(6, 10, 15, 19))
    m.exit_south(12, 19)
    m.crater(12, 11); m.crater(7, 9); m.crater(17, 14)
    rnd = random.Random(774)
    m.rubble(rnd, 6, (4, 5, 21, 18), set(CORE_KEEP))
    return m, m.build()


CORE_SALAMENCE = (12, 9)
CORE_MINIOR = [(6, 13), (18, 8), (9, 16), (16, 11), (14, 15)]
CORE_ROCKS = [(10, 11), (15, 12), (11, 14)]
CORE_ITEM = (20, 18)
CORE_KEEP = [CORE_SALAMENCE, CORE_ITEM, (12, 18), (12, 17), (12, 10)] + CORE_MINIOR + CORE_ROCKS


def build_shrine():
    """Oude Draconid-schrijn: hal met twee zuilen in de achterwand, een meteoriet als altaar en de oudere."""
    m = Map(22, 20)
    m.room(4, 5, 17, 15)
    m.build()
    m.stal_wall(4, 17, 5, pillars=(5, 8, 12, 15))
    m.exit_south(10, 15)
    m.crater(5, 12); m.crater(15, 12)
    return m, m.build()


SHR_ELDER = (10, 9)
SHR_ALTAR = (10, 7)
SHR_TABLETS = [(7, 4), (13, 4)]


def build_echo():
    """Echokamer: hoog, leeg en hol. Roep in het donker en de grot antwoordt (te veel)."""
    m = Map(20, 18)
    m.room(4, 5, 15, 13)
    m.room(4, 5, 4, 6, 'R'); m.room(15, 5, 15, 6, 'R')
    m.build()
    m.exit_south(9, 13)
    rnd = random.Random(404)
    m.rubble(rnd, 4, (4, 5, 15, 12), {(9, 12), (9, 11), (9, 6), (14, 7), (8, 6), (10, 6)})
    return m, m.build()


ECHO_SPOT = (9, 4)
ECHO_ITEM = (14, 7)


def build_grotto():
    """Sterrenvalgrot: hier land je als je door het gat in de gangen valt (zelfde x,y als het gat)."""
    m = Map(47, 44)
    m.room(17, 19, 29, 30)
    m.build()
    m.exit_south(23, 30)
    m.crater(19, 27); m.crater(26, 22)
    return m, m.build()


GROT_ITEMS = [(18, 20), (28, 28)]


def build_hidden_falls():
    """Grot achter de waterval: druipend, met een poel die door de waterval gevoed wordt."""
    m = Map(20, 16)
    m.room(4, 5, 15, 11)
    m.water(9, 5, 14, 8)
    m.build()
    m.exit_south(6, 11)
    return m, m.build()


HFALL_ITEMS = [(4, 6), (15, 10)]


# ---------------------------------------------------------------------------------------------------- objecten
B2R_ROCK = (12, 5)
B2R_BOULDER = (16, 38)
B2R_ITEMS = {(6, 7): ('ITEM_TM_DRAGON_CLAW', 'FLAG_ITEM_METEOR_FALLS_B1F_2R_TM_DRAGON_CLAW'),
             (5, 37): ('ITEM_RARE_CANDY', 'FLAG_ITEM_METEOR_FALLS_B1F_2R_RARE_CANDY'),
             (33, 45): ('ITEM_STAR_PIECE', 'FLAG_ITEM_METEOR_FALLS_B1F_2R_STAR_PIECE')}
B2R_METEORITES = [(8, 26), (30, 36), (19, 43)]
B2R_TAMER = (15, 10)


def objects():
    o = {}
    b = [item(x, y, it, fl) for (x, y), (it, fl) in B2R_ITEMS.items()]
    b += [rocksmash(*B2R_ROCK), boulder(*B2R_BOULDER)]
    b += [meteorite(x, y, B2R + '_EventScript_Meteorite') for (x, y) in B2R_METEORITES]
    b += [trainer('OBJ_EVENT_GFX_MAN_3', *B2R_TAMER, B2R + '_EventScript_Drake', 'RIGHT', 5)]
    o[B2R] = b
    o[TUN] = [rocksmash(*TUN_HOLE),
              trainer('OBJ_EVENT_GFX_HIKER', 8, 34, TUN + '_EventScript_Boulderman', 'RIGHT', 4),
              trainer('OBJ_EVENT_GFX_PSYCHIC_M', 14, 15, TUN + '_EventScript_Orion', 'DOWN', 5),
              trainer('OBJ_EVENT_GFX_MAN_3', 41, 24, TUN + '_EventScript_Vesper', 'DOWN', 5),
              trainer('OBJ_EVENT_GFX_WOMAN_5', 37, 7, TUN + '_EventScript_Nova', 'LEFT', 4),
              item(14, 7, 'ITEM_DRAGON_FANG', 'FLAG_ITEM_METEOR_FALLS_TUNNELS_DRAGON_FANG'),
              item(4, 35, 'ITEM_FULL_RESTORE', 'FLAG_ITEM_METEOR_FALLS_TUNNELS_FULL_RESTORE'),
              item(42, 35, 'ITEM_STARDUST', 'FLAG_ITEM_METEOR_FALLS_TUNNELS_STARDUST')]
    c = [obj('OBJ_EVENT_GFX_SPECIES(SALAMENCE)', *CORE_SALAMENCE, CORE + '_EventScript_Salamence',
             'FLAG_HIDE_METEOR_FALLS_SALAMENCE', lid='LOCALID_STAR_CORE_SALAMENCE')]
    for k, (x, y) in enumerate(CORE_MINIOR):
        c.append(obj('OBJ_EVENT_GFX_SPECIES(MINIOR_METEOR)', x, y, CORE + '_EventScript_Minior%d' % (k + 1),
                     'FLAG_TEMP_%d' % (k + 1), 'MOVEMENT_TYPE_WANDER_AROUND', lid='LOCALID_STAR_CORE_MINIOR_%d' % (k + 1),
                     rx=1, ry=1))
    c += [meteorite(x, y, CORE + '_EventScript_Meteorite') for (x, y) in CORE_ROCKS]
    c.append(item(*CORE_ITEM, 'ITEM_COMET_SHARD', 'FLAG_ITEM_METEOR_FALLS_STAR_CORE_COMET_SHARD'))
    o[CORE] = c
    o[SHR] = [obj('OBJ_EVENT_GFX_OLD_WOMAN', *SHR_ELDER, SHR + '_EventScript_Elder', lid='LOCALID_DRACONID_ELDER'),
              meteorite(*SHR_ALTAR, SHR + '_EventScript_Altar')]
    o[ECHO] = [item(*ECHO_ITEM, 'ITEM_MAX_ETHER', 'FLAG_ITEM_METEOR_FALLS_ECHO_CHAMBER_MAX_ETHER')]
    o[GROT] = [item(*GROT_ITEMS[0], 'ITEM_COMET_SHARD', 'FLAG_ITEM_METEOR_FALLS_STARFALL_COMET_SHARD'),
               item(*GROT_ITEMS[1], 'ITEM_STAR_PIECE', 'FLAG_ITEM_METEOR_FALLS_STARFALL_STAR_PIECE')]
    o[HFALL] = [item(*HFALL_ITEMS[0], 'ITEM_DRAGON_SCALE', 'FLAG_ITEM_METEOR_FALLS_HIDDEN_FALLS_DRAGON_SCALE'),
                item(*HFALL_ITEMS[1], 'ITEM_MAX_ELIXIR', 'FLAG_ITEM_METEOR_FALLS_HIDDEN_FALLS_MAX_ELIXIR')]
    return o


WARPS = {
    B2R: [warp(20, 47, 3, 'METEOR_FALLS_B1F_1R', 3), warp(12, 4, 3, TUN_C, 0), warp(32, 18, 3, HFALL_C, 0)],
    TUN: [warp(23, 40, 3, B2R_C, 1), warp(5, 5, 3, SHR_C, 0), warp(23, 5, 3, CORE_C, 0), warp(41, 5, 3, ECHO_C, 0),
          warp(*TUN_GROTTO_EXIT, 3, GROT_C, 0)],
    SHR: [warp(10, 15, 3, TUN_C, 1)],
    CORE: [warp(12, 19, 3, TUN_C, 2)],
    ECHO: [warp(9, 13, 3, TUN_C, 3)],
    GROT: [warp(23, 30, 3, TUN_C, 4)],
    HFALL: [warp(6, 11, 3, B2R_C, 2)],
}
SIGNS = {
    SHR: [sign(x, y, SHR + '_EventScript_Tablet%d' % (k + 1), 'BG_EVENT_PLAYER_FACING_NORTH')
          for k, (x, y) in enumerate(SHR_TABLETS)],
    ECHO: [sign(*ECHO_SPOT, ECHO + '_EventScript_Shout', 'BG_EVENT_PLAYER_FACING_NORTH')],
}
CONSTS = {B2R: B2R_C, TUN: TUN_C, CORE: CORE_C, SHR: SHR_C, ECHO: ECHO_C, GROT: GROT_C, HFALL: HFALL_C}
MUSICS = {SHR: 'MUS_SEALED_CHAMBER', CORE: 'MUS_SEALED_CHAMBER'}


def check(name, start, targets, surf=False, blocked=(), extra=()):
    g = MAPS[name][1]
    r = reachable(g, start, set(blocked), surf, set(extra))
    for t in targets:
        assert t in r or next_to(r, *t), '%s: %s onbereikbaar' % (name, t)
    return r


def checks(objs):
    blocked = lambda n, skip=(): {(o['x'], o['y']) for o in objs[n] if (o['x'], o['y']) not in skip}
    # B1F_2R: te voet alleen de hal en de middenlaag; de nis pas met Strength; de rest met Surf/Waterfall
    b = blocked(B2R)
    r = check(B2R, (20, 46), [(26, 33), (8, 26)], blocked=b)
    assert (5, 37) not in r and (32, 19) not in r and (12, 6) not in r, 'B1F_2R: poort lekt'
    check(B2R, (17, 38), [(5, 37)], blocked=blocked(B2R, {B2R_BOULDER}) | {(8, 38)})   # rotsblok de nis in geduwd
    r = check(B2R, (20, 46), [(32, 18), (6, 7), B2R_ROCK, B2R_TAMER, (33, 45)], surf=True, blocked=b)
    assert (12, 4) not in r, 'B1F_2R: scheur zonder Rock Smash bereikbaar'
    check(B2R, (20, 46), [(12, 4)], surf=True, blocked=blocked(B2R, {B2R_ROCK}))
    # gangen: alles vanaf de ingang (de brokkelrots op het gat telt als weggeslagen)
    t = blocked(TUN, {TUN_HOLE})
    check(TUN, (23, 39), [(5, 5), (23, 5), (41, 5), TUN_HOLE, TUN_GROTTO_EXIT] +
          [(o['x'], o['y']) for o in objs[TUN]], blocked=t)
    for n, start in ((CORE, (12, 18)), (SHR, (10, 14)), (ECHO, (9, 12)), (GROT, TUN_HOLE), (HFALL, (6, 10))):
        check(n, start, [(o['x'], o['y']) for o in objs[n]] + [(w['x'], w['y']) for w in WARPS[n]],
              blocked=blocked(n))
    assert MAPS[GROT][1][TUN_HOLE[1]][TUN_HOLE[0]] >> 10 & 3 == 0, 'landingsplek in de grot is geen vloer'
    for n, ws in WARPS.items():
        g = MAPS[n][1]
        for w in ws:
            v = g[w['y']][w['x']]
            assert v >> 12 == w['elevation'], (n, w)


def register(objs):
    prev = 'MeteorFalls_StevensCave'
    for n, c in CONSTS.items():
        m, g = MAPS[n]
        save_layout(n, g)
        add_layout(n, c, m.W, m.H, 'MeteorFalls_StevensCave_Layout')
        os.makedirs('data/maps/' + n, exist_ok=True)
        if n == B2R:
            d = json.load(open('data/maps/%s/map.json' % n))
            d['object_events'] = objs[n]; d['warp_events'] = WARPS[n]; d['bg_events'] = []
            write_json('data/maps/%s/map.json' % n, d)
            continue
        write_json('data/maps/%s/map.json' % n,
                   map_json(c, n, MUSICS.get(n, MUSIC), objs[n], WARPS[n], SIGNS.get(n, [])))
        add_to_grounded_group(n)
        add_include(n, prev)
        prev = n


def main():
    MAPS[B2R] = build_b1f_2r()
    MAPS[TUN] = build_tunnels()
    MAPS[CORE] = build_core()
    MAPS[SHR] = build_shrine()
    MAPS[ECHO] = build_echo()
    MAPS[GROT] = build_grotto()
    MAPS[HFALL] = build_hidden_falls()
    objs = objects()
    checks(objs)
    register(objs)
    print('klaar:', ', '.join('%s %dx%d' % (n, m.W, m.H) for n, (m, g) in MAPS.items()))
    if len(sys.argv) > 1:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from gridrender import render
        for n, (mm, gg) in MAPS.items():
            render(gg, 'general', 'meteor_falls', 2).save(os.path.join(sys.argv[1], n + '.png'))


if __name__ == '__main__':
    main()
