"""Project Grounded: Scorched Slab als kleine zonnetempel-dungeon.

Bouwt (deterministisch, idempotent):
- tileset `scorched_slab` (secondary): de Cave-tiles (gedeeld, geen nieuwe tiles) met eigen paletten en metatiles.
  Palet 6 warmer ("gebakken" rots), palet 12 = zonlicht. Achteraan: 0x3AA zonneglyph in een lichtstraal (doel van de
  puzzel, METATILE_ScorchedSlab_SunLight) en 0x3AB-0x3B9 vloer met deels zonlicht (per 8x8-kwart, voor ronde
  lichtvlekken).
- ScorchedSlab (vanilla ingang, nu met de warme tileset): grotopening in de noordwand (7,2) naar de Zonnezaal.
- ScorchedSlab_SunHall    (Zonnezaal): tempelzaal (Regi-kamerstijl) met drie lichtschachten en drie zonnestenen
  (Strength). Staan alle drie de stenen tegelijk in het licht, dan gaat de zonnedeur in de noordwand open
  (hook in PushBoulder_End -> ScorchedSlab_SunHall_EventScript_StoneInLight). Kindler Ray, Sun Stone,
  ladder omlaag naar de bron.
- ScorchedSlab_Spring     (Koele bron): meer onder de zonnezaal (Surf), verdwaalde duiker Marco, Damp Rock op een
  oever die je alleen surfend bereikt, diep water (Dive, na badge 7).
- Underwater_ScorchedSlab : kleine onderwatergrot onder de bron (verborgen Big Nugget).
- ScorchedSlab_Sanctum    (Zonnesanctum): achter de zonnedeur. Hogepriesteres Helia, Volcarona lv 42 in een grote
  lichtvlek, Heat Rock en TM59 Weather Ball.

Controleert de bereikbaarheid (HM-poorten), lost de blokpuzzel op (BFS op duwen: oplosbaar, minimaal aantal duwen,
uitgangen blijven bereikbaar) en dat de puzzel-coordinaten kloppen met de lichtschachten.
Gebruik: python3 tools/grounded/maptools/scorched_slab_ext.py [voorbeeld.png]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, shutil, struct, sys
from collections import deque

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)

COL = 0x400
def T(mt, col=False, elev=0):
    return mt | (COL if col else 0) | (elev << 12)
def walkable(t):
    return not t & 0xc00

FLOOR = T(0x201, elev=3)
ROCKS = (0x202, 0x203)

# ---------------------------------------------------------------------------------------------------- tileset
CAVE = 'data/tilesets/secondary/cave'
TS = 'data/tilesets/secondary/scorched_slab'
N_CAVE = 426
SUN_TARGET = 0x200 + N_CAVE          # 0x3AA: zonneglyph in de lichtstraal (doel)
GLOW0 = SUN_TARGET + 1               # 0x3AB + (masker - 1): vloer met zonlicht per kwart (bit 0 LB, 1 RB, 2 LO, 3 RO)
FLOOR_SUB = (0x203, 0x204, 0x213, 0x214)
SUN_SUB = (0x3bd, 0x3be, 0x3bf, 0x3c0)
PAL_ROCK, PAL_SUN = 6, 12

WARM6 = [(255, 131, 123), (255, 224, 150), (240, 192, 128), (220, 162, 106), (192, 128, 88), (162, 96, 70),
         (124, 62, 46), (86, 34, 36)]
LIT12 = [(255, 131, 123), (255, 252, 210), (255, 238, 172), (255, 216, 140), (240, 186, 112), (214, 150, 90),
         (172, 106, 64), (124, 66, 44)]

def read_pal(p):
    lines = open(p).read().split('\n')[3:19]
    return [tuple(map(int, l.split())) for l in lines]
def write_pal(p, cols):
    open(p, 'w', newline='\r\n').write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in cols))

def build_tileset():
    os.makedirs(TS + '/palettes', exist_ok=True)
    mts = open(CAVE + '/metatiles.bin', 'rb').read()
    att = open(CAVE + '/metatile_attributes.bin', 'rb').read()
    # Cave groeide na dit script (v0.9.179+); de Scorched Slab houdt de eerste N_CAVE metatiles,
    # zodat de zonne-metatiles (en METATILE_ScorchedSlab_SunLight) op hun plek blijven.
    assert len(mts) >= N_CAVE * 16 and len(att) >= N_CAVE * 2, 'Cave-tileset is kleiner geworden'
    mts, att = mts[:N_CAVE * 16], att[:N_CAVE * 2]
    floor_attr = att[(0x201 - 0x200) * 2:(0x201 - 0x200) * 2 + 2]
    sun_attr = att[(0x3a9 - 0x200) * 2:(0x3a9 - 0x200) * 2 + 2]
    new = struct.pack('<8H', *[s | (PAL_SUN << 12) for s in SUN_SUB], 0, 0, 0, 0)
    natt = sun_attr
    for mask in range(1, 16):
        new += struct.pack('<8H', *[s | ((PAL_SUN if mask >> i & 1 else PAL_ROCK) << 12) for i, s in enumerate(FLOOR_SUB)], 0, 0, 0, 0)
        natt += floor_attr
    open(TS + '/metatiles.bin', 'wb').write(mts + new)
    open(TS + '/metatile_attributes.bin', 'wb').write(att + natt)
    for i in range(16):
        src = CAVE + '/palettes/%02d.pal' % i
        cols = read_pal(src)
        if i == PAL_ROCK:
            cols = WARM6 + cols[8:]
        elif i == PAL_SUN:
            cols = LIT12 + read_pal(CAVE + '/palettes/%02d.pal' % PAL_ROCK)[8:]
        write_pal(TS + '/palettes/%02d.pal' % i, cols)
    open(TS + '/TILES', 'w').write('cave\n')   # voor render_map.py/gridrender.py
    register_tileset()

def register_tileset():
    hdr = 'src/data/tilesets/headers.h'
    s = open(hdr).read()
    if 'gTileset_ScorchedSlab' not in s:
        s += '''
const struct Tileset gTileset_ScorchedSlab = // Project Grounded: Scorched Slab (Cave-tiles, warme paletten, lichtvlekken)
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Cave,
    .palettes = gTilesetPalettes_ScorchedSlab,
    .metatiles = gMetatiles_ScorchedSlab,
    .metatileAttributes = gMetatileAttributes_ScorchedSlab,
    .callback = InitTilesetAnim_Cave,
};
'''
        open(hdr, 'w').write(s)
    gfx = 'src/data/tilesets/graphics.h'
    s = open(gfx).read()
    if 'gTilesetPalettes_ScorchedSlab' not in s:
        s += '\nconst u16 gTilesetPalettes_ScorchedSlab[][16] = // Project Grounded: Scorched Slab\n{\n' + \
             ''.join('    INCBIN_U16("data/tilesets/secondary/scorched_slab/palettes/%02d.gbapal"),\n' % i for i in range(16)) + '};\n'
        open(gfx, 'w').write(s)
    mt = 'src/data/tilesets/metatiles.h'
    s = open(mt).read()
    if 'gMetatiles_ScorchedSlab' not in s:
        s += '\nconst u16 gMetatiles_ScorchedSlab[] = INCBIN_U16("data/tilesets/secondary/scorched_slab/metatiles.bin"); // Project Grounded: Scorched Slab\n' + \
             'const u16 gMetatileAttributes_ScorchedSlab[] = INCBIN_U16("data/tilesets/secondary/scorched_slab/metatile_attributes.bin");\n'
        open(mt, 'w').write(s)
    lab = 'include/constants/metatile_labels.h'
    s = open(lab).read()
    if 'METATILE_ScorchedSlab_SunLight' not in s:
        s = s.replace('// gTileset_Cave\n', '// gTileset_ScorchedSlab (Project Grounded; verder dezelfde nummers als gTileset_Cave)\n'
                      '#define METATILE_ScorchedSlab_SunLight                   0x%03X\n\n// gTileset_Cave\n' % SUN_TARGET, 1)
        open(lab, 'w').write(s)

# ---------------------------------------------------------------------------------------------------- bestanden
L = {l['id']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'id' in l}
def load_layout(lid):
    l = L[lid]
    W, H = l['width'], l['height']
    v = list(struct.unpack('<%dH' % (W * H), open(l['blockdata_filepath'], 'rb').read()))
    return [v[y * W:(y + 1) * W] for y in range(H)], l['blockdata_filepath']

def save_grid(g, path):
    open(path, 'wb').write(struct.pack('<%dH' % (len(g) * len(g[0])), *[t for r in g for t in r]))

# ---------------------------------------------------------------------------------------------------- tempelkamer
# Sjabloon: de Regi-kamer van Island Cave (rij 18-32, 17x15): gevel met zegeldeur bovenin, uitgang onderin.
# Bovenin "plain" = rij 0-2 van dezelfde kaart (zelfde kamer zonder gevel). Uitrekken: kolom 4 (links van de gevel),
# kolom 12 (rechts) en rij 25 (midden van het brede deel).
IC, _ = load_layout('LAYOUT_ISLAND_CAVE')
def chamber(addL, addR, addH, top='facade', bottom='exit'):
    rows = [list(IC[18 + r]) for r in range(15)]
    if top == 'plain':
        rows[0:3] = [list(IC[r]) for r in range(3)]
    for r in rows:
        for x, t in enumerate(r):
            if t & 0x3ff == 0x3a8: r[x] = FLOOR          # Regi-stippen weg
    if bottom == 'plain':
        rows[11][8] = rows[11][7]; rows[12][7:10] = [rows[12][6]] * 3
    rows = [r[:5] + [r[4]] * addL + r[5:12] + [r[12]] * addR + r[12:] for r in rows]
    rows = rows[:8] + [list(rows[7]) for _ in range(addH)] + rows[8:]
    return rows

def rock(g, x, y):
    g[y][x] = T(ROCKS[(x * 7 + y * 3) % 2], True)

def carpet(g, x0, y0, x1, y1):
    """Zandvloer (heet zand): 298/299/29a, 2a0/2a1/2a2, 2a8/2a9/2aa."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            r = 0 if y == y0 else 2 if y == y1 else 1
            c = 0 if x == x0 else 2 if x == x1 else 1
            g[y][x] = T([[0x298, 0x299, 0x29a], [0x2a0, 0x2a1, 0x2a2], [0x2a8, 0x2a9, 0x2aa]][r][c], elev=3)

def glow(g, cx, cy, radius, target=True):
    """Ronde lichtvlek: per 8x8-kwart van een vloertegel licht als het midden binnen `radius` (tegels) ligt."""
    R = int(radius) + 1
    for y in range(cy - R, cy + R + 1):
        for x in range(cx - R, cx + R + 1):
            if not (0 <= y < len(g) and 0 <= x < len(g[0])): continue
            if (x, y) == (cx, cy):
                g[y][x] = T(SUN_TARGET if target else GLOW0 + 14, elev=3); continue
            if g[y][x] != FLOOR: continue
            mask = 0
            for i, (sx, sy) in enumerate(((0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75))):
                if ((x + sx - cx - 0.5) ** 2 + (y + sy - cy - 0.5) ** 2) ** 0.5 <= radius: mask |= 1 << i
            if mask: g[y][x] = T(GLOW0 + mask - 1, elev=3)

def door(g, x, ydoor, elev=3):
    """Grotopening: 20b/20c/20d boven, 213/214/215 op de deurrij (214 = deur, warp)."""
    g[ydoor - 1][x - 1:x + 2] = [T(0x20b, True), T(0x20c, True), T(0x20d, True)]
    g[ydoor][x - 1:x + 2] = [T(0x213, True), T(0x214, elev=elev), T(0x215, True)]

def obj(gfx, x, y, script, flag='0', ttype='TRAINER_TYPE_NONE', sight='0', move='MOVEMENT_TYPE_FACE_DOWN', local_id=None, elev=3):
    o = {}
    if local_id: o['local_id'] = local_id
    o.update({'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
              'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': ttype,
              'trainer_sight_or_berry_tree_id': sight, 'script': script, 'flag': flag})
    return o
def item(x, y, it, flag):
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', flag, sight=it, move='MOVEMENT_TYPE_LOOK_AROUND')
def boulder(x, y, flag):
    return obj('OBJ_EVENT_GFX_PUSHABLE_BOULDER', x, y, 'EventScript_StrengthBoulder', flag, move='MOVEMENT_TYPE_LOOK_AROUND')
def sign(x, y, script, elev=0):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': elev, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY', 'script': script}
def hidden(x, y, it, flag, elev=3):
    return {'type': 'hidden_item', 'x': x, 'y': y, 'elevation': elev, 'item': it, 'flag': flag}

# ---------------------------------------------------------------------------------------------------- Sokoban
D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
def solve(free_cells, boulders, targets, start, exits, cap=400000):
    """BFS op duwen. Geeft (minimaal aantal duwen tot alle doelen tegelijk bedekt zijn, of None; val?; toestanden).
    Val = een bereikbare stand van waaruit je (ook met verder duwen) nooit meer bij elke uitgang komt."""
    free = lambda c: c in free_cells
    def region(p, bs):
        seen = {p}; st = [p]
        while st:
            x, y = st.pop()
            for dx, dy in D4:
                n = (x + dx, y + dy)
                if n not in seen and free(n) and n not in bs:
                    seen.add(n); st.append(n)
        return seen
    b0 = frozenset(boulders); Tg = frozenset(targets)
    k0 = (min(region(start, b0)), b0)
    q = deque([(start, b0, 0, k0)]); seen = {k0}
    best = None; succ = {}; good = {}
    while q:
        p, bs, d, key = q.popleft()
        reg = region(p, bs)
        good[key] = frozenset(e for e in exits if e in reg)
        if best is None and Tg <= bs: best = d
        nxt = succ.setdefault(key, [])
        for b in bs:
            for dx, dy in D4:
                pc = (b[0] - dx, b[1] - dy); tc = (b[0] + dx, b[1] + dy)
                if pc in reg and free(tc) and tc not in bs:
                    nb = (bs - {b}) | {tc}
                    k = (min(region(b, nb)), nb)
                    nxt.append(k)
                    if k not in seen:
                        seen.add(k); q.append((b, nb, d + 1, k))
                        if len(seen) > cap: raise SystemExit('puzzel: te veel toestanden')
    # per uitgang: toestanden van waaruit die uitgang nog te bereiken is (achterwaarts propageren)
    pred = {}
    for k, ns in succ.items():
        for n in ns: pred.setdefault(n, []).append(k)
    trap = False
    for e in exits:
        ok = {k for k, g in good.items() if e in g}; st = list(ok)
        while st:
            k = st.pop()
            for pk in pred.get(k, ()):
                if pk not in ok: ok.add(pk); st.append(pk)
        bad = [k for k in seen if k not in ok]
        if bad:
            trap = True
            if os.environ.get('SLABDEBUG'): print('val:', e, bad[0])
    return best, trap, len(seen)

def reach(g, start, blocked=(), surf=False):
    """Bereikbaarheid met hoogteregels (0/15 = elke hoogte; water = hoogte 1, alleen met Surf)."""
    W, H = len(g[0]), len(g)
    el = lambda t: t >> 12
    def ok(a, b):
        ea, eb = el(a), el(b)
        if ea in (0, 15) or eb in (0, 15) or ea == eb: return True
        return surf and {ea, eb} == {1, 3}
    seen = {start}; st = [start]
    while st:
        x, y = st.pop()
        for dx, dy in D4:
            n = (x + dx, y + dy)
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and n not in blocked:
                t = g[n[1]][n[0]]
                if walkable(t) and ok(g[y][x], t) and (surf or el(t) != 1):
                    seen.add(n); st.append(n)
    return seen

def adj(reg, x, y):
    return any((x + dx, y + dy) in reg for dx, dy in D4)

# ---------------------------------------------------------------------------------------------------- Zonnezaal
# Kolommen x3..23 (breed deel rij 5-15), smal (x4..22) rij 3-4 en 16-17. Zegeldeur (13,2), uitgang (13,17).
# Drie kapellen: west (x3-8, rij 6-12, ingang (5,13)), middenpad (x10-16, rij 5-13) en oost (x18-23, ingang (21,13)).
# Elke kapel heeft een zonnesteen (B) en een lichtschacht (T). Gevonden met tools-zoeker en hier gecontroleerd.
WEST = ['#.....',
        '##B#.#',
        '......',
        'T.#...',
        '......',
        '..###.',
        '#.....']
AISLE = ['#.....#',
         '#...#..',
         '#......',
         '....#..',
         '..###..',
         '....#B.',
         '...#..#',
         '.....##',
         '.....T.']
EAST = ['...##.',
        '.B....',
        '...#.#',
        '.....#',
        '.##...',
        '##..#.',
        '.#...T']
SH_DOOR, SH_EXIT, SH_LADDER = (13, 2), (13, 17), (21, 16)

def sun_hall():
    g = chamber(5, 5, 6, top='facade', bottom='exit')
    W, H = len(g[0]), len(g)
    assert g[SH_DOOR[1]][SH_DOOR[0]] & 0x3ff == 0x233 and g[SH_EXIT[1]][SH_EXIT[0]] & 0x3ff == 0x207
    boulders, targets = [], []
    def put(pattern, x0, y0):
        for dy, row in enumerate(pattern):
            for dx, c in enumerate(row):
                x, y = x0 + dx, y0 + dy
                if c == '#': rock(g, x, y)
                elif c == 'B': boulders.append((x, y))
                elif c == 'T': targets.append((x, y))
    # scheidingen: rij 5 boven de kapellen, kolommen 9 en 17, rij 13 onder de kapellen (met ingang)
    for x in list(range(3, 10)) + list(range(17, 24)): rock(g, x, 5)
    for y in range(5, 14): rock(g, 9, y); rock(g, 17, y)
    for x in list(range(3, 9)) + list(range(18, 24)):
        if x not in (5, 21): rock(g, x, 13)
    put(WEST, 3, 6); put(AISLE, 10, 5); put(EAST, 18, 6)
    # heet zand op de aanloop naar de kapellen, zonneglyfen (onverlicht) in het voorportaal
    carpet(g, 10, 14, 16, 16)
    for x in (6, 9, 17, 20): g[3][x] = T(0x3a8, elev=3)
    for (x, y) in targets: glow(g, x, y, 1.4)
    g[SH_LADDER[1]][SH_LADDER[0]] = T(0x205, elev=3)
    objs = [
        obj('OBJ_EVENT_GFX_MAN_5', 8, 15, 'ScorchedSlab_SunHall_EventScript_Ray', ttype='TRAINER_TYPE_NORMAL', sight='5', move='MOVEMENT_TYPE_FACE_RIGHT'),
        item(4, 16, 'ITEM_SUN_STONE', 'FLAG_ITEM_SCORCHED_SLAB_SUN_STONE'),
    ]
    objs += [boulder(x, y, 'FLAG_TEMP_%X' % (0x11 + i)) for i, (x, y) in enumerate(boulders)]
    bgs = [sign(12, 2, 'ScorchedSlab_SunHall_EventScript_SunDoor'), sign(13, 2, 'ScorchedSlab_SunHall_EventScript_SunDoor'),
           sign(14, 2, 'ScorchedSlab_SunHall_EventScript_SunDoor')]
    # --- controle
    static = {(o['x'], o['y']) for o in objs if o['graphics_id'] != 'OBJ_EVENT_GFX_PUSHABLE_BOULDER'}
    cells = reach(g, SH_EXIT, blocked=static)
    assert SH_LADDER in cells and (13, 3) in cells, 'zonnezaal: ladder/deur onbereikbaar'
    # Per kapel oplossen (de andere stenen liggen stil; een opgeloste steen blijft op zijn doel liggen), in volgorde.
    # Een gezamenlijke BFS over alle drie de stenen is te groot (het zuiddeel is open).
    placed = []; total = 0
    for b, t in zip(boulders, targets):
        others = [o for o in boulders if o != b and o not in [p[0] for p in placed]] + [p[1] for p in placed]
        best, trap, n = solve(cells - set(others), [b], [t], SH_EXIT, [SH_EXIT, (13, 3), SH_LADDER])
        assert best is not None and not trap, 'zonnezaal: kapel %s -> %s klopt niet (%s, val=%s)' % (b, t, best, trap)
        placed.append((b, t)); total += best
    print('zonnezaal: puzzel %d duwen in totaal, doelen %s' % (total, targets))
    for o in objs:
        if o['graphics_id'] in ('OBJ_EVENT_GFX_PUSHABLE_BOULDER',): continue
        assert adj(cells, o['x'], o['y']), 'zonnezaal: %s onbereikbaar' % o['script']
    return g, objs, bgs, targets

# ---------------------------------------------------------------------------------------------------- Koele bron
SP_LADDER, SP_DIVE = (6, 3), (14, 10)
def spring():
    g = chamber(4, 4, 4, top='plain', bottom='plain')
    W, H = len(g[0]), len(g)
    g[SP_LADDER[1] - 1][SP_LADDER[0]] = T(0x20f, True); g[SP_LADDER[1]][SP_LADDER[0]] = T(0x216, elev=3)
    x0, x1, y0, y1 = 7, 18, 6, 12
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if y == y0: mt = 0x180 if x == x0 else 0x181 if x == x1 else 0x189
            else: mt = 0x190 if x == x0 else 0x192 if x == x1 else 0x27b
            g[y][x] = T(mt, elev=1)
        pass
    for x in range(x0, x1 + 1): g[y1 + 1][x] = T(0x357, elev=3)
    for (x, y) in ((SP_DIVE[0], SP_DIVE[1]), (SP_DIVE[0] + 1, SP_DIVE[1]), (SP_DIVE[0], SP_DIVE[1] + 1), (SP_DIVE[0] + 1, SP_DIVE[1] + 1)):
        g[y][x] = T(0x14e if (x + y) % 2 else 0x14f, elev=1)
    # oostoever alleen surfend bereikbaar: ingestorte rotsen boven en onder
    for x in (19, 20, 21): rock(g, x, 5); rock(g, x, 13)
    rock(g, 3, 5); rock(g, 3, 13); rock(g, 21, 6); rock(g, 21, 12)
    for y in (6, 9, 12): g[y][4] = T(0x3a8, elev=3)
    objs = [
        obj('OBJ_EVENT_GFX_SWIMMER_M', 11, 9, 'ScorchedSlab_Spring_EventScript_Marco', ttype='TRAINER_TYPE_NORMAL', sight='4',
            move='MOVEMENT_TYPE_FACE_LEFT', elev=1),
        item(20, 9, 'ITEM_DAMP_ROCK', 'FLAG_ITEM_SCORCHED_SLAB_DAMP_ROCK'),
    ]
    bgs = [sign(9, 2, 'ScorchedSlab_Spring_EventScript_Plaque')]
    blocked = {(o['x'], o['y']) for o in objs}
    land = reach(g, SP_LADDER, blocked)
    wet = reach(g, SP_LADDER, blocked, surf=True)
    assert not adj(land, 20, 9), 'bron: Damp Rock hoort Surf te vereisen'
    assert adj(wet, 20, 9) and SP_DIVE in wet and adj(wet, 11, 9), 'bron: iets onbereikbaar met Surf'
    assert (9, 3) in land
    return g, objs, bgs

# ---------------------------------------------------------------------------------------------------- Zonnesanctum
SA_EXIT, SA_VOLC = (11, 16), (11, 7)
def sanctum():
    g = chamber(3, 3, 5, top='plain', bottom='exit')
    assert g[SA_EXIT[1]][SA_EXIT[0]] & 0x3ff == 0x207
    for y in range(9, 15, 2):
        g[y][8] = T(0x3a8, elev=3); g[y][14] = T(0x3a8, elev=3)
    for (x, y) in ((3, 5), (19, 5), (3, 14), (19, 14), (4, 15), (18, 15)): rock(g, x, y)
    glow(g, SA_VOLC[0], SA_VOLC[1], 2.4)
    objs = [
        obj('OBJ_EVENT_GFX_SPECIES(VOLCARONA)', SA_VOLC[0], SA_VOLC[1], 'ScorchedSlab_Sanctum_EventScript_Volcarona',
            'FLAG_HIDE_SCORCHED_SLAB_VOLCARONA', local_id='LOCALID_SCORCHED_SLAB_VOLCARONA'),
        obj('OBJ_EVENT_GFX_HEX_MANIAC', 11, 11, 'ScorchedSlab_Sanctum_EventScript_Helia', ttype='TRAINER_TYPE_NORMAL', sight='4'),
        item(4, 4, 'ITEM_HEAT_ROCK', 'FLAG_ITEM_SCORCHED_SLAB_HEAT_ROCK'),
        item(18, 4, 'ITEM_TM_WEATHER_BALL', 'FLAG_ITEM_SCORCHED_SLAB_TM_WEATHER_BALL'),
    ]
    bgs = [sign(11, 2, 'ScorchedSlab_Sanctum_EventScript_Mural')]
    blocked = {(o['x'], o['y']) for o in objs}
    r = reach(g, SA_EXIT, blocked)
    for o in objs:
        assert adj(r, o['x'], o['y']), 'sanctum: %s onbereikbaar' % o['script']
    assert (11, 3) in r
    return g, objs, bgs

# ---------------------------------------------------------------------------------------------------- onderwater
UW_ARRIVE, UW_ITEM = (8, 6), (5, 6)
def underwater():
    g, _ = load_layout('LAYOUT_UNDERWATER_ROUTE134')
    g = [list(r) for r in g]
    # zwemgat dicht (geen warp hier): vloer en een gewone onderrand
    g[8][8] = g[8][7]
    g[9][7:10] = [g[9][6]] * 3
    r = reach(g, UW_ARRIVE)
    assert UW_ITEM in r
    return g

# ---------------------------------------------------------------------------------------------------- registratie
NEW = [('ScorchedSlab_SunHall', 'SCORCHED_SLAB_SUN_HALL', 'gTileset_ScorchedSlab'),
       ('ScorchedSlab_Spring', 'SCORCHED_SLAB_SPRING', 'gTileset_ScorchedSlab'),
       ('ScorchedSlab_Sanctum', 'SCORCHED_SLAB_SANCTUM', 'gTileset_ScorchedSlab'),
       ('Underwater_ScorchedSlab', 'UNDERWATER_SCORCHED_SLAB', 'gTileset_Underwater')]

def register_layout(name, const, W, H, sec):
    lj = open('data/layouts/layouts.json').read()
    entry = '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (const, name, W, H, sec, name, name)
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"id": "LAYOUT_%s"' % const); s = lj.rindex('{', 0, i); e = lj.index('},', i) + 2
        lj = lj[:s - 5] + entry + lj[e:]
    else:
        i = lj.index('"id": "LAYOUT_SCORCHED_SLAB"'); j = lj.index('},', i) + 2
        lj = lj[:j] + entry + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)

def set_layout_tileset(const, sec):
    lj = open('data/layouts/layouts.json').read()
    i = lj.index('"id": "LAYOUT_%s"' % const); e = lj.index('},', i)
    block = lj[i:e]
    nb = block.replace('"secondary_tileset": "gTileset_Cave"', '"secondary_tileset": "%s"' % sec)
    open('data/layouts/layouts.json', 'w').write(lj[:i] + nb + lj[e:])

def write_map(name, const, objs, warps, bgs, underwater=False, music='MUS_SEALED_CHAMBER'):
    base = json.load(open('data/maps/%s/map.json' % ('Underwater_MarineCave' if underwater else 'ScorchedSlab')))
    m = dict(base)
    m.update({'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + const, 'music': music,
              'region_map_section': 'MAPSEC_SCORCHED_SLAB', 'show_map_name': False, 'connections': None,
              'object_events': objs, 'warp_events': warps, 'coord_events': [], 'bg_events': bgs})
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"gMapGroup_Grounded": ['); j = g.index(']', i)
        body = g[i:j].rstrip()
        g = g[:i] + body + ',\n    "%s"\n  ' % name + g[j:]
        open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/ScorchedSlab/scripts.inc"\n'
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)

def wr(path, m):
    open(path, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

def check_script_targets(targets):
    """De puzzel telt stenen op METATILE_ScorchedSlab_SunLight; het script noemt het aantal doelen."""
    s = open('data/maps/ScorchedSlab_SunHall/scripts.inc').read()
    assert 'goto_if_eq VAR_RESULT, %d,' % len(targets) in s, 'scripts.inc: aantal lichtschachten klopt niet'

def main():
    build_tileset()
    sh, sh_objs, sh_bgs, targets = sun_hall()
    sp, sp_objs, sp_bgs = spring()
    sa, sa_objs, sa_bgs = sanctum()
    uw = underwater()

    # --- de vanilla ingang: warme tileset, grotopening in de noordwand (7,2), inscriptie ernaast
    slab, slab_path = load_layout('LAYOUT_SCORCHED_SLAB')
    door(slab, 7, 2)
    save_grid(slab, slab_path)
    set_layout_tileset('SCORCHED_SLAB', 'gTileset_ScorchedSlab')
    ms = json.load(open('data/maps/ScorchedSlab/map.json'))
    ms['warp_events'] = [w for w in ms['warp_events'] if w['dest_map'] == 'MAP_ROUTE120']
    ms['warp_events'].append({'x': 7, 'y': 2, 'elevation': 3, 'dest_map': 'MAP_SCORCHED_SLAB_SUN_HALL', 'dest_warp_id': '0'})
    ms['bg_events'] = [sign(5, 2, 'ScorchedSlab_EventScript_Inscription')]
    wr('data/maps/ScorchedSlab/map.json', ms)
    assert (7, 3) in reach(slab, (7, 4)) and (7, 2) in reach(slab, (7, 4))

    warps = {
        'ScorchedSlab_SunHall': [
            {'x': SH_EXIT[0], 'y': SH_EXIT[1], 'elevation': 3, 'dest_map': 'MAP_SCORCHED_SLAB', 'dest_warp_id': '1'},
            {'x': SH_DOOR[0], 'y': SH_DOOR[1], 'elevation': 0, 'dest_map': 'MAP_SCORCHED_SLAB_SANCTUM', 'dest_warp_id': '0'},
            {'x': SH_LADDER[0], 'y': SH_LADDER[1], 'elevation': 3, 'dest_map': 'MAP_SCORCHED_SLAB_SPRING', 'dest_warp_id': '0'}],
        'ScorchedSlab_Spring': [
            {'x': SP_LADDER[0], 'y': SP_LADDER[1], 'elevation': 3, 'dest_map': 'MAP_SCORCHED_SLAB_SUN_HALL', 'dest_warp_id': '2'}],
        'ScorchedSlab_Sanctum': [
            {'x': SA_EXIT[0], 'y': SA_EXIT[1], 'elevation': 3, 'dest_map': 'MAP_SCORCHED_SLAB_SUN_HALL', 'dest_warp_id': '1'}],
        'Underwater_ScorchedSlab': [],
    }
    data = {'ScorchedSlab_SunHall': (sh, sh_objs, sh_bgs), 'ScorchedSlab_Spring': (sp, sp_objs, sp_bgs),
            'ScorchedSlab_Sanctum': (sa, sa_objs, sa_bgs),
            'Underwater_ScorchedSlab': (uw, [], [hidden(UW_ITEM[0], UW_ITEM[1], 'ITEM_BIG_NUGGET', 'FLAG_HIDDEN_ITEM_SCORCHED_SLAB_BIG_NUGGET')])}
    for name, const, sec in NEW:
        g, objs, bgs = data[name]
        os.makedirs('data/layouts/' + name, exist_ok=True)
        save_grid(g, 'data/layouts/%s/map.bin' % name)
        if name.startswith('Underwater'):
            shutil.copy('data/layouts/Underwater_Route134/border.bin', 'data/layouts/%s/border.bin' % name)
        else:
            shutil.copy('data/layouts/IslandCave/border.bin', 'data/layouts/%s/border.bin' % name)
        register_layout(name, const, len(g[0]), len(g), sec)
        uw_ = name.startswith('Underwater')
        write_map(name, const, objs, warps[name], bgs, underwater=uw_, music='MUS_UNDERWATER' if uw_ else 'MUS_SEALED_CHAMBER')
        register_map(name)
    if os.path.exists('data/maps/ScorchedSlab_SunHall/scripts.inc'):
        check_script_targets(targets)
    if len(sys.argv) > 1:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from gridrender import render
        from PIL import Image, ImageDraw
        ims = []
        for g, objs in ((slab, ms['object_events']), (sh, sh_objs), (sp, sp_objs), (sa, sa_objs)):
            im = render(g, 'general', 'scorched_slab'); d = ImageDraw.Draw(im)
            for o in objs:
                c = (255, 255, 0) if 'BOULDER' in o['graphics_id'] else (255, 0, 0)
                d.rectangle([o['x'] * 16 + 3, o['y'] * 16 + 3, o['x'] * 16 + 12, o['y'] * 16 + 12], outline=c)
            ims.append(im)
        ims.append(render(uw, 'general', 'underwater'))
        out = Image.new('RGB', (sum(i.width for i in ims) + 16 * len(ims), max(i.height for i in ims)), 'black')
        x = 0
        for i in ims: out.paste(i, (x, 0)); x += i.width + 16
        out.save(sys.argv[1])
    print('klaar')

if __name__ == '__main__':
    main()
