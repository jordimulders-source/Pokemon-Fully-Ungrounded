"""Project Grounded: twee kratereilanden in Sootopolis-stijl rond Sootopolis (Route 126). Deterministisch en idempotent.

  Route126_HermitCrater   Bewoond kratertje: kluizenaar-schilder (oud-lid van de Sootopolis-familie), twee trainers,
                          items, wilde Pokemon in het kratermeer (surf + vissen) en op de grasrichels (12 unieke slots).
  Route126_SilentCrater   Verlaten kratertje: een verzegelde 'tweelingpoort' van de Cave of Origin (uit de Sootopolis-
                          kaart gestempeld), een stenen tablet met Primal-lore, een zeldzaam item, eigen encounters.

Bereikbaar via zwemgaten (MB_WATER_DOOR) in Underwater_Route126; je komt surfend boven in het kratermeer. Terug =
duiken in het donkere water (MB_SOOTOPOLIS_DEEP_WATER, setdivewarp naar onder het zwemgat).

Tegels: de kaart wordt eerst als klassenraster ontworpen (W wit gesteente, P roze klif, F begaanbare roze vloer,
G gras, A water, D diep duikwater) en dan ge-autotiled met tegels die in SootopolisCity in precies dezelfde
3x3-klassenomgeving voorkomen (zelfde tileset: gTileset_General + gTileset_Sootopolis). Ontbrekende patronen worden
gemeld (val terug op de 4-buren).

Flags: FLAG_GROUNDED 500-529. Trainers: 1074-1085.
Gebruik: python3 tools/grounded/maptools/sootopolis_craters.py [rendermap]"""
import json, os, random, re, struct, subprocess, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beacon_dragon as bd          # zet ook de werkmap op de repo-root
from landlib import Kaart

sms, cx, oq = bd.sms, bd.cx, bd.oq
Scr, ball, sign, hidden, warp, obj, tr = bd.Scr, bd.ball, bd.sign, bd.hidden, bd.warp, bd.obj, bd.tr

# ====================================================================== klassen in SootopolisCity leren
SOOT = Kaart('SootopolisCity')
COL = 0x400
TREE = {0x1ce, 0x1cf, 0x1d4, 0x1d5, 0x1d6, 0x1d7, 0x1dc, 0x1dd, 0x1e4, 0x1e5, 0x1e6, 0x1e7}
PINK = set(range(0x068, 0x0b0)) - {0x098, 0x09a} | {0x0be, 0x0bf, 0x089, 0x0a0, 0x1b3, 0x269, 0x28a, 0x28b, 0x28c,
                                                    0x2de, 0x2df, 0x2eb, 0x2ed, 0x27c, 0x27d, 0x260}
WHITE = {0x2cd, 0x2ce, 0x2d0, 0x2d1, 0x2d2, 0x2d3, 0x2d4, 0x2d6, 0x2d8, 0x2d9, 0x2da, 0x2db, 0x2dc, 0x2e0, 0x2e1,
         0x2e2, 0x2ec, 0x2f3, 0x2fb, 0x2fd}


def klass(t, beh):
    m = t & 0x3ff
    if m == 0x28e:
        return 'D'
    if 0x280 <= m <= 0x284:             # zandrand van het gymeiland
        return 'X'
    if beh == 'MB_POND_WATER' and not t & 0xc00:
        return 'A'
    if m == 0x001 or m in TREE or m in (0x0d3, 0x0d4):
        return 'G'
    if m in PINK:
        return 'P'                      # begaanbare roze vloer (F) heeft dezelfde tegel; botsing zet autotile()
    if m in WHITE:
        return 'W'
    return 'X'


SC = [[klass(SOOT.c(x, y), SOOT.beh(x, y)) for x in range(SOOT.w)] for y in range(SOOT.h)]
N8 = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
N4 = [(0, -1), (-1, 0), (1, 0), (0, 1)]
PAT8, PAT4, PAT0 = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter)
for y in range(SOOT.h):
    for x in range(SOOT.w):
        c = SC[y][x]
        t = SOOT.c(x, y)
        if c == 'X' or (t & 0x3ff) in TREE:
            continue
        nb = [SC[y + dy][x + dx] if 0 <= x + dx < SOOT.w and 0 <= y + dy < SOOT.h else c for dx, dy in N8]
        if 'X' in nb:
            continue
        PAT8[(c, tuple(nb))][t] += 1
        PAT4[(c, tuple(nb[i] for i in (1, 3, 4, 6)))][t] += 1
        PAT0[c][t] += 1


def autotile(cls, tag):
    """cls: lijst strings (klassen). Geeft het metatile-raster terug; meldt ontbrekende 3x3-patronen."""
    H, W = len(cls), len(cls[0])
    walk = [[c == 'F' for c in r] for r in cls]
    cls = [[('P' if c == 'F' else c) for c in r] for r in cls]
    g = [[0] * W for _ in range(H)]
    miss = Counter()
    for y in range(H):
        for x in range(W):
            c = cls[y][x]
            nb = [cls[y + dy][x + dx] if 0 <= x + dx < W and 0 <= y + dy < H else c for dx, dy in N8]
            k8 = (c, tuple(nb))
            k4 = (c, tuple(nb[i] for i in (1, 3, 4, 6)))
            if k8 in PAT8:
                t = PAT8[k8].most_common(1)[0][0]
            else:                       # dichtstbijzijnde voorbeeld (rechte buren tellen dubbel)
                best = None
                for (pc, pn), cnt in PAT8.items():
                    if pc != c:
                        continue
                    d = sum((2 if i in (1, 3, 4, 6) else 1) for i in range(8) if pn[i] != nb[i])
                    key = (d, -sum(cnt.values()))
                    if best is None or key < best[0]:
                        best = (key, cnt)
                t = best[1].most_common(1)[0][0]
                miss[(x, y, c, ''.join(nb), best[0][0], '%03x' % (t & 0x3ff))] += 1
            if c in 'WP' and not walk[y][x]:
                t |= COL
            elif c == 'G' or walk[y][x]:
                t = (t & ~0xc00 & 0x0fff) | (3 << 12)
            g[y][x] = t
    if miss:
        print(tag, 'patronen zonder 3x3-voorbeeld:', len(miss))
        for k in sorted(miss)[:40]:
            print('   ', k)
    return g


def canvas(W, H, fill='W'):
    return [[fill] * W for _ in range(H)]


def rect(cv, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            cv[y][x] = c


def rows(cv):
    return [''.join(r) for r in cv]


def tree(g, x, y):
    """2x2-boom met linkerboven op (x,y), tegels uit SootopolisCity (1d6/1d7 boven, 1e6/1e7 onder)."""
    for dy, row in enumerate(((0x1d6, 0x1d7), (0x1e6, 0x1e7))):
        for dx, m in enumerate(row):
            g[y + dy][x + dx] = m | COL | (3 << 12)


def render(name, out, H):
    subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), name, out, '0', str(H)], check=True)


def preview(g, out):
    import gridrender
    gridrender.render(g, 'general', 'sootopolis', 1).save(out)


DOME = [''.join('D' if SC[y][x] == 'D' else 'A' for x in range(23, 36)) for y in range(52, 56)]   # het duikwater van Sootopolis


def stamp_classes(cv, x0, y0, block):
    for dy, row in enumerate(block):
        for dx, c in enumerate(row):
            cv[y0 + dy][x0 + dx] = c


# ====================================================================== 1. bewoond kratertje (klassen)
def chamfer(cv, x0, y0, x1, y1, n, c='W', corners='NW NE SW SE'):
    """Trapsgewijs afgeschuinde hoeken van het bekken (n treden per hoek)."""
    for i in range(n):
        for j in range(n - i):
            pts = {'NW': (x0 + j, y0 + i), 'NE': (x1 - j, y0 + i), 'SW': (x0 + j, y1 - i), 'SE': (x1 - j, y1 - i)}
            for k in corners.split():
                x, y = pts[k]
                cv[y][x] = c


def hermit_classes():
    W, H = 30, 26
    cv = canvas(W, H)
    rect(cv, 5, 4, 24, 21, 'A')          # kratermeer
    rect(cv, 5, 6, 8, 17, 'G')           # westelijke grasrichel (de kluizenaar)
    rect(cv, 6, 4, 8, 5, 'G')
    rect(cv, 20, 4, 24, 12, 'G')         # oostelijke richel
    rect(cv, 22, 13, 24, 14, 'G')
    chamfer(cv, 5, 4, 24, 21, 2, corners='NW NE')
    stamp_classes(cv, 7, 18, DOME)       # duikwater tegen de zuidwand
    # Hoeken waar gras, klif en water samenkomen hebben in Sootopolis geen kusttegel (Jordi: hoekjes zonder
    # kustrand): daar loopt de klif een vakje door.
    for x in range(9, 20):                # het meer reikt een rij hoger dan de grasrichels (zoals Sootopolis)
        cv[3][x] = 'A'
    return cv


def ring(cv, kw=1, kg=2, ks=2):
    """Klif (P) rond het bekken: kw breed langs water, kg langs gras, ks onder het bekken (zuidwand); de rest wit."""
    H, W = len(cv), len(cv[0])
    out = [r[:] for r in cv]

    def near(x, y, kinds, kx, ky_up, ky_down):
        return any(cv[yy][xx] in kinds for yy in range(max(0, y - ky_up), min(H, y + ky_down + 1))
                   for xx in range(max(0, x - kx), min(W, x + kx + 1)))
    for y in range(H):
        for x in range(W):
            if cv[y][x] in 'AGDF':
                continue
            p = near(x, y, 'AD', kw, ks, kw) or near(x, y, 'G', kg, kg, kg)
            out[y][x] = 'P' if p else 'W'
    return out


# ====================================================================== 2. verlaten kratertje (klassen)
GATE_SRC = (28, 15, 7, 6)          # x, y, w, h in SootopolisCity: de poort van de Cave of Origin + voorplein
GATE_AT = (10, 3)                  # linkerboven in Route126_SilentCrater
STAIRS = (13, 10)                  # witte trap (244/245, zoals in Sootopolis) van het voorplein naar de grasrand


def silent_classes():
    W, H = 28, 25
    cv = canvas(W, H)
    rect(cv, 4, 13, 23, 21, 'A')          # kratermeer
    rect(cv, 4, 12, 7, 13, 'W')
    rect(cv, 20, 12, 23, 13, 'W')
    rect(cv, 9, 11, 18, 12, 'G')          # smalle grasrand onder het voorplein
    rect(cv, 8, 8, 19, 9, 'F')            # voorplein (begaanbaar roze gesteente)
    rect(cv, 20, 16, 23, 18, 'G')         # grasrichel tegen de oostwand (los eilandje kan niet: gras heeft
    rect(cv, 20, 13, 23, 15, 'W')         # in Sootopolis geen noordkust-tegel), klif erboven
    sx, sy, sw, sh = GATE_SRC
    gx, gy = GATE_AT
    for dy in range(sh):
        for dx in range(sw):
            c = SC[sy + dy][sx + dx]
            cv[gy + dy][gx + dx] = 'F' if (dy >= 2 and 0 < dx < sw - 1) or dy == sh - 1 else 'W'
    chamfer(cv, 4, 13, 23, 21, 2, 'W', 'NW NE')
    stamp_classes(cv, 7, 18, DOME)
    return cv


def wall_fix(g):
    """Oostwand naast water: in Sootopolis staat 073 naast 0ba/0c4 (0a0 heeft een randje water).
    Klif boven gras zonder plantjes (Jordi: 2de/2df zien er onaf uit): 079."""
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] & 0x3ff in (0x2de, 0x2df):
                g[y][x] = (g[y][x] & ~0x3ff) | 0x079
        for x in range(1, len(g[0])):
            if g[y][x] & 0x3ff == 0x0a0 and g[y][x - 1] & 0x3ff in (0x0ba, 0x0c4):
                g[y][x] = (g[y][x] & ~0x3ff) | 0x073
    return g


def silent_tiles(cv):
    g = autotile(ring(cv, 2, 2, 2), 'SilentCrater')
    sx, sy, sw, sh = GATE_SRC
    gx, gy = GATE_AT
    for dy in range(sh):
        for dx in range(sw):
            g[gy + dy][gx + dx] = SOOT.c(sx + dx, sy + dy)
    # rechtsonder de grasrichel: waterhoek tegen de wand (zoals Sootopolis 36,24), het water eronder loopt door
    for x, y, m in ((23, 19, 0x0c4), (22, 20, 0x279), (23, 20, 0x0ba)):
        g[y][x] = (g[y][x] & ~0x3ff) | m
    x, y = STAIRS
    g[y][x] = 0x244 | (3 << 12)
    g[y][x + 1] = 0x245 | (3 << 12)
    return wall_fix(g)


# ====================================================================== flags
FLAGS = [
    (500, 'FLAG_ITEM_HERMIT_CRATER_WIDE_LENS', 'kluizenaarskrater: Wide Lens'),
    (501, 'FLAG_HIDDEN_ITEM_HERMIT_CRATER_PEARL_STRING', 'kluizenaarskrater: verborgen Pearl String'),
    (502, 'FLAG_ITEM_SILENT_CRATER_GOLD_BOTTLE_CAP', 'stille krater: Gold Bottle Cap (grasrichel)'),
    (503, 'FLAG_HIDDEN_ITEM_SILENT_CRATER_EARTH_PLATE', 'stille krater: verborgen Earth Plate (voorplein)'),
    (504, 'FLAG_HIDDEN_ITEM_SILENT_CRATER_SPLASH_PLATE', 'stille krater: verborgen Splash Plate (grasrand)'),
]
F = {name: name for _, name, _ in FLAGS}


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// sootopolis_craters { (tools/grounded/maptools/sootopolis_craters.py; FLAG_GROUNDED 500-529)\n'
    for n, name, why in FLAGS:
        assert 500 <= n <= 529
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// sootopolis_craters {' in s:
        i = s.index('// sootopolis_craters {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        i = s.index('// dungeon_extra {')
        s = s[:i] + blk + '\n' + s[i:]
    s = s.replace('470-499 extra dungeons (dungeon_extra.py), 500+ vrij.',
                  '470-499 extra dungeons (dungeon_extra.py), 500-529 kratereilanden (sootopolis_craters.py), 530+ vrij.')
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== trainers (id's 1074-1085)
mon, AI, AI_BOSS = bd.mon, bd.AI, bd.AI_BOSS
TRAINERS = [
    (1074, 'LAVIS', 'kluizenaarskrater: schilder, oud-lid van de Sootopolis-familie (Battle Stadium)', 'LAVIS',
     'Expert', 'Expert M', 'Male', 'Intense', AI_BOSS, 'Hyper Potion / Hyper Potion', [
        mon('Grafaiai', 48, ['Gunk Shot', 'Knock Off', 'U-turn', 'Super Fang']),
        mon('Kingdra', 48, ['Hydro Pump', 'Draco Meteor', 'Flash Cannon', 'Agility']),
        mon('Milotic @ Leftovers', 49, ['Scald', 'Recover', 'Ice Beam', 'Toxic']),
        mon('Smeargle @ Focus Sash', 50, ['Spore', 'Shell Smash', 'Stored Power', 'Hydro Pump'])]),
    (1075, 'SWIMMER_MARGOT', 'kluizenaarskrater: zwemt baantjes in het kratermeer', 'MARGOT',
     'Swimmer F', 'Swimmer F', 'Female', 'Swimmer', AI, None, [
        mon('Barraskewda', 46, ['Liquidation', 'Close Combat', 'Psychic Fangs', 'Aqua Jet']),
        mon('Palafin', 46, ['Wave Crash', 'Jet Punch', 'Zen Headbutt', 'Bulk Up']),
        mon('Tatsugiri', 46, ['Muddy Water', 'Dragon Pulse', 'Icy Wind', 'Nasty Plot'])]),
    (1076, 'AROMA_LADY_FENNA', 'kluizenaarskrater: kwam voor de stilte, nam een speaker mee', 'FENNA',
     'Aroma Lady', 'Aroma Lady', 'Female', 'Female', AI, None, [
        mon('Comfey', 46, ['Draining Kiss', 'Giga Drain', 'Synthesis', 'Calm Mind']),
        mon('Tsareena', 46, ['Trop Kick', 'High Jump Kick', 'Triple Axel', 'Rapid Spin']),
        mon('Lilligant', 46, ['Petal Dance', 'Quiver Dance', 'Sleep Powder', 'Pollen Puff'])]),
]


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = "// sootopolis_craters { (tools/grounded/maptools/sootopolis_craters.py; id's 1074-1085)\n"
    for n, const, why, *_ in TRAINERS:
        assert 1074 <= n <= 1085
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (const, n, why)
    blk += '// }'
    if '// sootopolis_craters {' in s:
        i = s.index('// sootopolis_craters {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for n, *_ in TRAINERS:
        assert len(re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)) == 1, ('trainer-id dubbel', n)
    open(p, 'w').write(s)

    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- sootopolis_craters (tools/grounded/maptools/sootopolis_craters.py) --- */\n\n'
    for n, const, why, nm, cls, pic, gender, music, ai, items, team in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music]
        if items:
            hdr.append('Items: ' + items)
        hdr += ['Double Battle: No', ai]
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (const, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde sootopolis_craters --- */'
    s = bd.replace_block(s, '/* --- sootopolis_craters', '/* --- einde sootopolis_craters --- */', blk)
    open(p, 'w').write(s)


# ====================================================================== zwemgaten in Underwater_Route126
UW = 'Underwater_Route126'
UW_SRC = (45, 65)                   # bestaand zwemgat naar Underwater_SootopolisCity
HOLES = {'Route126_HermitCrater': (24, 14), 'Route126_SilentCrater': (37, 9)}


def const_of(name):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper()


def uw_hole(name):
    L = bd.layout_of(UW)
    uw = oq.read_layout(L['blockdata_filepath'], L['width'], L['height'])
    sx, sy = UW_SRC
    x, y = HOLES[name]
    src = [[uw[sy - 1 + r][sx - 1 + c] for c in range(3)] for r in range(2)]
    assert [[t & 0x3ff for t in row] for row in src] == [[0x265, 0x266, 0x267], [0x26d, 0x26e, 0x26f]], src
    for r in range(2):
        for c in range(3):
            cur = uw[y - 1 + r][x - 1 + c] & 0x3ff
            assert cur in (0x21b, 0x216, 0x265, 0x266, 0x267, 0x26d, 0x26e, 0x26f), ('zwemgat-plek', name, hex(cur))
            uw[y - 1 + r][x - 1 + c] = src[r][c]
    assert cx.walkable(uw[y + 1][x]), 'onder het zwemgat ligt geen zeebodem'
    cx.save_grid(uw, L['blockdata_filepath'])
    return oq.edit_map(UW, lambda m: oq.warp_to(m, x, y, 'MAP_' + const_of(name)))


# ====================================================================== controle en registratie
def check(g, start, objs, bgs, tag):
    blocked = {(o['x'], o['y']) for o in objs}
    walk = cx.reach(g, [start], blocked=blocked)
    for o in objs:
        assert cx.next_to((o['x'], o['y']), walk), (tag, 'object onbereikbaar', o['x'], o['y'], o['script'])
    for b in bgs:
        if b['type'] == 'hidden_item':
            assert (b['x'], b['y']) in walk, (tag, 'verborgen item onbereikbaar', b)
        else:
            assert cx.next_to((b['x'], b['y']), walk), (tag, 'bord onbereikbaar', b)
    return walk


def write_layout(name, g):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    cx.save_grid(g, 'data/layouts/%s/map.bin' % name)
    wt = 0x2d9 | COL                                  # wit gesteente als rand
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', wt, wt, wt, wt))
    bd.register_layout(name, const_of(name), len(g[0]), len(g), 'gTileset_General', 'gTileset_Sootopolis')


def header(name, text):
    x, y = HOLES[name]
    return '''@ Project Grounded: %s
@ Kaart en scripts: tools/grounded/maptools/sootopolis_craters.py (niet met de hand bewerken).
%s_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, %s_OnResume
	.byte 0

%s_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE126, %d, %d
	setescapewarp MAP_UNDERWATER_ROUTE126, %d, %d
	end
''' % (text, name, name, name, x, y + 1, x, y + 1)


def arrival(g):
    """Eerste diep-duikwatercel (28e) bovenin de koepel: daar kom je boven."""
    for y in range(len(g)):
        for x in range(len(g[0])):
            if (g[y][x] & 0x3ff) == 0x28e:
                return x + 1, y + 1


def finish(name, g, objs, bgs, S, music):
    start = arrival(g)
    check(g, start, objs, bgs, name)
    write_layout(name, g)
    wid = uw_hole(name)
    sms.write_map(name, const_of(name), objs, [warp(start[0], start[1], 'UNDERWATER_ROUTE126', wid)], [], bgs,
                  music=music, weather='WEATHER_SUNNY', map_type='MAP_TYPE_ROUTE',
                  region_map_section='MAPSEC_ROUTE_126', show_map_name=True, allow_cycling=False,
                  allow_escaping=False, allow_running=True, battle_scene='MAP_BATTLE_SCENE_NORMAL')
    oq.register_map(name)
    S.write()
    return name


# ====================================================================== 1. bewoond kratertje
TALL = 0x00d | (3 << 12)
HERMIT_TREES = [(5, 8), (5, 14), (22, 5), (23, 8)]
HERMIT_TALL = [(7, 6), (8, 6), (7, 7), (8, 7), (20, 9), (21, 9), (20, 10), (21, 10), (20, 11), (21, 11)]


def hermit():
    name = 'Route126_HermitCrater'
    cv = hermit_classes()
    g = autotile(ring(cv, 2, 2, 2), name)
    # onderhoeken van de grasrichels tegen de wand: waterhoektegels zoals in Sootopolis (36,24 en 16,46)
    for x, y, m in ((24, 15, 0x0c4), (5, 18, 0x0b0)):
        g[y][x] = (g[y][x] & ~0x3ff) | m
    # bovenhoeken van de grasrichels: exact de tegels van Sootopolis (21-24,34-36 en 38-40,35-37)
    water = lambda x, y, m: g[y].__setitem__(x, m | (3 << 12))
    cliff = lambda x, y, m: g[y].__setitem__(x, m | COL)
    for x in range(10, 18):
        water(x, 3, 0x0b1); cliff(x, 2, 0x07c)
    cliff(8, 3, 0x07a); water(9, 3, 0x0c3); cliff(9, 2, 0x07d)
    water(18, 3, 0x0c4); water(18, 4, 0x0c2); water(19, 4, 0x0b2); cliff(19, 3, 0x07b); cliff(19, 2, 0x07c)
    g = wall_fix(g)
    for x, y in HERMIT_TREES:
        assert all(cv[y + dy][x + dx] == 'G' for dx in (0, 1) for dy in (0, 1)), ('boom niet op gras', x, y)
        tree(g, x, y)
    for x, y in HERMIT_TALL:
        assert cv[y][x] == 'G' and not g[y][x] & 0xc00
        g[y][x] = TALL
    S = Scr(name, header(name, 'bewoond kratertje bij Sootopolis (Route 126). Ingang: zwemgat in '
                               'Underwater_Route126 %d,%d; terug = duiken in het donkere water.' % HOLES[name]))
    P = S.P
    S.trainer('Lavis', 'LAVIS',
              "Don't. Move.\n\nI have been painting this lake for thirty-one years. You are now IN it. "
              "Do you know what that does to a composition?",
              "Fine. You're in the painting. Small. In the corner. Drowning, but tastefully.",
              "My family guarded the SOOTOPOLIS crater for generations. I guard this one. It's smaller. "
              "Like my pension.\n\nWALLACE got the GYM. I got 'creative freedom'. It is mostly freedom to be alone "
              "with a lake that refuses to hold still.")
    S.trainer('Margot', 'SWIMMER_MARGOT',
              "Lap four thousand and twelve! The crater has no lanes, so I AM the lane.",
              "You broke my rhythm. And my team. Mostly the rhythm.",
              "Every lap I touch the wall and whisper 'nearly'.\n\nNearly what? Unclear. "
              "'Nearly' is the whole point.")
    S.trainer('Fenna', 'AROMA_LADY_FENNA',
              "I came here for absolute silence. Then I brought a speaker. For the silence. So it's louder.",
              "Okay. That was loud.",
              "The painter says my COMFEY ruins his composition.\n\nMy COMFEY says nothing. "
              "My COMFEY IS the composition.")
    S.npc('Canvas', "A canvas is nailed to the tree. It shows this lake, very accurately.\n\n"
                    "In the corner, a tiny figure is drowning. The paint is still wet.", 'MSGBOX_SIGN')
    objs = [obj('OBJ_EVENT_GFX_ARTIST', 7, 11, P + 'Lavis', move='MOVEMENT_TYPE_FACE_RIGHT'),
            tr('OBJ_EVENT_GFX_SWIMMER_F', 14, 9, P + 'Margot', 'DOWN', 3, elev=1),
            tr('OBJ_EVENT_GFX_WOMAN_2', 21, 7, P + 'Fenna', 'LEFT', 2),
            ball(24, 12, 'ITEM_WIDE_LENS', F['FLAG_ITEM_HERMIT_CRATER_WIDE_LENS'])]
    bgs = [sign(5, 15, P + 'Canvas'),
           hidden(8, 17, 'ITEM_PEARL_STRING', F['FLAG_HIDDEN_ITEM_HERMIT_CRATER_PEARL_STRING'])]
    return finish(name, g, objs, bgs, S, 'MUS_SOOTOPOLIS')


# ====================================================================== 2. verlaten kratertje
def silent():
    name = 'Route126_SilentCrater'
    cv = silent_classes()
    g = silent_tiles(cv)
    gx, gy = GATE_AT
    door = (gx + 3, gy + 1)
    assert (g[door[1]][door[0]] & 0x3ff) == 0x221, 'poortdeur'
    g[door[1]][door[0]] |= COL                       # verzegeld: geen warp, alleen een bord
    statues = [(gx + 2, gy + 4), (gx + 4, gy + 4)]
    for x, y in statues:
        assert (g[y][x] & 0x3ff) == 0x280, ('beeld', x, y)
    S = Scr(name, header(name, 'verlaten kratertje bij Sootopolis (Route 126) met een verzegelde tweelingpoort van '
                               'de Cave of Origin. Ingang: zwemgat in Underwater_Route126 %d,%d.' % HOLES[name]))
    P = S.P
    S.npc('Gate', "A sealed gate, the twin of the one in SOOTOPOLIS. This door was never meant to open.\n\n"
                  "Carved above it:\n'THE SKY CAME DOWN TO PART THEM. THEN IT WENT BACK UP. "
                  "IT DID NOT ENJOY THE VISIT.'", 'MSGBOX_SIGN')
    S.npc('Sea', "A worn statue of a whale. Its markings glow faintly when nobody is looking.\n\n"
                 "The plaque:\n'SHE WANTED MORE SEA. THERE IS NEVER ENOUGH SEA. ASK THE SEA.'", 'MSGBOX_SIGN')
    S.npc('Land', "A statue with claws, half melted.\n\nThe plaque:\n'HE WANTED MORE LAND. HE GOT A VOLCANO. "
                  "HE SULKED FOR AN AGE.'\n\nScratched underneath, much newer:\n'REVERSION IS NOT A PHASE, MOM.'",
          'MSGBOX_SIGN')
    objs = [ball(21, 17, 'ITEM_GOLD_BOTTLE_CAP', F['FLAG_ITEM_SILENT_CRATER_GOLD_BOTTLE_CAP'])]
    bgs = [sign(door[0], door[1], P + 'Gate', 'BG_EVENT_PLAYER_FACING_NORTH'),
           sign(statues[0][0], statues[0][1], P + 'Sea'), sign(statues[1][0], statues[1][1], P + 'Land'),
           hidden(9, 9, 'ITEM_EARTH_PLATE', F['FLAG_HIDDEN_ITEM_SILENT_CRATER_EARTH_PLATE']),
           hidden(18, 12, 'ITEM_SPLASH_PLATE', F['FLAG_HIDDEN_ITEM_SILENT_CRATER_SPLASH_PLATE'])]
    return finish(name, g, objs, bgs, S, 'MUS_SEALED_CHAMBER')


# ====================================================================== wilde Pokemon
WILD = {
    'ROUTE126_HERMIT_CRATER': dict(
        land=(15, [('VIVILLON', 44, 47), ('CHATOT', 44, 47), ('ORICORIO', 44, 47), ('BELLOSSOM', 44, 47),
                   ('RIBOMBEE', 44, 47), ('TROPIUS', 44, 47), ('COMFEY', 45, 47), ('CASTFORM', 45, 47),
                   ('FLORGES', 46, 48), ('XATU', 46, 48), ('SMEARGLE', 47, 49), ('ALTARIA', 47, 49)]),
        water=(4, [('PELIPPER', 44, 47), ('GOLDUCK', 44, 47), ('AZUMARILL', 44, 47), ('SWANNA', 45, 48),
                   ('MILOTIC', 46, 48)]),
        fishing=(30, [('GOLDEEN', 20, 25), ('FEEBAS', 20, 25), ('FINNEON', 30, 35), ('LUVDISC', 30, 35),
                      ('CHINCHOU', 30, 35), ('SEAKING', 40, 45), ('LUMINEON', 40, 45), ('WHISCASH', 40, 45),
                      ('LANTURN', 42, 46), ('MILOTIC', 44, 48)])),
    'ROUTE126_SILENT_CRATER': dict(
        water=(4, [('TENTACRUEL', 44, 47), ('JELLICENT', 44, 47), ('GASTRODON', 44, 47), ('DHELMISE', 45, 48),
                   ('RELICANTH', 46, 48)]),
        fishing=(30, [('FRILLISH', 20, 25), ('SHELLOS', 20, 25), ('SKRELP', 30, 35), ('CORSOLA_GALAR', 30, 35),
                      ('SHELLDER', 30, 35), ('CURSOLA', 40, 45), ('CLOYSTER', 40, 45), ('DRAGALGE', 40, 45),
                      ('OVERQWIL', 42, 46), ('RELICANTH', 44, 48)])),
}
STADIUM = [('LAVIS', 'LAVIS', 'ARTIST',
            "LAVIS! Thirty-one years painting one lake. Today: you, small, in the corner.")]


# ====================================================================== main
if __name__ == '__main__':
    flags()
    trainers()
    names = [hermit(), silent()]
    bd.WILD = WILD
    bd.wild()
    bd.STADIUM = STADIUM
    bd.stadium()
    if len(sys.argv) > 1:
        for n in names:
            L = bd.layout_of(n)
            render(n, os.path.join(sys.argv[1], n + '.png'), L['height'])
    print('klaar:', ', '.join(names))
