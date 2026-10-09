"""Project Grounded: Jagged Pass ondergronds + Mt. Chimney nog hoger.

Bouwt twee nieuwe kaarten (General + Lavaridge, dezelfde stijl als Jagged Pass / Magma Hideout) en past de
ingangen in JaggedPass en MtChimney aan. Deterministisch (vaste seed) en idempotent.

  JaggedPass_LavaTube  Lavabuis onder Jagged Pass. Ingang A: grotopening in de klif vlak onder Mt. Chimney
                       (Jagged Pass (16,6)), dicht met een Rock Smash-rots. Uitgang B: grotopening op het grote
                       plateau halverwege (Jagged Pass (10,18), naast de Magma Hideout). Drie magmapoelen,
                       drie trainers, een Strength-blok (Heat Badge) voor de nis met TM Fire Blast.
  MtChimney_Summit     De echte top boven de krater. Trap in de bergkam aan de noordoostkant van Mt. Chimney
                       (31-32,4 na de aanpassing: (30,4)/(31,4)); tot badge 5 houdt een vulkanoloog je tegen.
                       Drie terrassen met trappen in rechte wanden, drie sterke trainers, bovenin een kratermeer
                       met een vaste Volcarona (lv 40) en de vulkanoloog.

Muren worden automatisch gelegd: in de grot als "kuil" (308-vloer met de 30x-randen van de Magma Hideout),
buiten als terrassen (271-grond met de randen van Jagged Pass/Mt. Chimney). Het script controleert de
bereikbaarheid (Rock Smash/Strength als poorten), dat elke rand een bekende vorm heeft en dat trappen in een
rechte wand liggen.
Gebruik: python3 tools/grounded/maptools/chimney_ext.py [voorbeeld.png]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, random, struct, sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)
random.seed(1136)

COL = 0x400
def T(mt, col=False, elev=0):
    return mt | (COL if col else 0) | (elev << 12)
def walkable(t):
    return not t & 0xc00

L = {l['id']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'id' in l}
def load_layout(lid):
    l = L[lid]; W, H = l['width'], l['height']
    v = list(struct.unpack('<%dH' % (W * H), open(l['blockdata_filepath'], 'rb').read()))
    return [v[y * W:(y + 1) * W] for y in range(H)], l['blockdata_filepath']
def save_grid(g, path):
    open(path, 'wb').write(struct.pack('<%dH' % (len(g) * len(g[0])), *[t for r in g for t in r]))

# ---------------------------------------------------------------- lava
LAVA = (0x2bd, 0x2bd, 0x2bd, 0x21c, 0x333)
def lava_tile():
    return T(random.choice(LAVA), True)

# ---------------------------------------------------------------- grot: kuil-autotiler (308-vloer)
FLOOR = 0x308
FLOOR_VAR = (0x310, 0x311)
def cave_tiles(mask):
    """mask: lijst strings; '#' vloer, 'L' lava, al het andere rots. Geeft een metatile-raster terug."""
    H, W = len(mask), len(mask[0])
    m = lambda x, y: mask[y][x] if 0 <= x < W and 0 <= y < H else '.'
    open_ = lambda x, y: m(x, y) in '#L'
    g = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            c = m(x, y)
            if c == '#':
                g[y][x] = T(random.choice(FLOOR_VAR) if random.random() < 0.05 else FLOOR, elev=3)
                continue
            if c == 'L':
                g[y][x] = lava_tile(); continue
            n, s, e, w = open_(x, y - 1), open_(x, y + 1), open_(x + 1, y), open_(x - 1, y)
            # lavarand: rotskolom naast de poel, wand erboven
            if m(x, y + 1) == 'L': t = 0x347
            elif m(x + 1, y) == 'L': t = 0x346
            elif m(x - 1, y) == 'L': t = 0x289
            else:
                assert not (n and s) and not (e and w), 'grot: te dunne rots op (%d,%d)' % (x, y)
                if s and e: t = 0x30f
                elif s and w: t = 0x30e
                elif n and w: t = 0x30a
                elif n and e: t = 0x30b
                elif s: t = 0x323 if random.random() < 0.08 else 0x274
                elif n: t = 0x30c
                elif e: t = 0x307
                elif w: t = 0x306
                elif open_(x + 1, y + 1): t = 0x27b
                elif open_(x - 1, y + 1): t = 0x27c
                elif open_(x + 1, y - 1): t = 0x27f
                elif open_(x - 1, y - 1): t = 0x27e
                else: t = 0x271
            g[y][x] = T(t, True)
    # oevers onder de lava
    for y in range(H):
        for x in range(W):
            if m(x, y) == '#' and m(x, y - 1) == 'L':
                g[y][x] = T(0x3a3, elev=3)
            elif m(x, y) == '#' and m(x, y - 1) not in '#L' and (m(x - 1, y - 1) == 'L' or m(x + 1, y - 1) == 'L'):
                g[y][x] = T(0x3a4, elev=3)
    return g

def cave_door(g, x, y):
    """Grotopening in een noordwand: 256 erboven, 25e (warp) op de wandrij."""
    assert (g[y][x] & 0x3ff) in (0x274, 0x323), 'deur (%d,%d) staat niet in een rechte noordwand' % (x, y)
    g[y - 1][x] = T(0x256, True); g[y][x] = T(0x25e)

# ---------------------------------------------------------------- buiten: terras-autotiler (271-grond)
RIDGE = (0x270, 0x270, 0x271, 0x272, 0x271, 0x270, 0x271, 0x272, 0x272, 0x271)
def terrace_tiles(hmap, lava=()):
    """hmap: lijst strings met niveaus '0'-'8' (beloopbaar) en 'X' (berg, 9). Elke cel die aan een lager
    niveau grenst wordt een rand van zijn eigen terras (zuid = wand 274, noord = rand 269, zijkanten 270/272).
    lava: set cellen (x,y) die lava zijn (horen bij een kuil in de berg)."""
    H, W = len(hmap), len(hmap[0])
    lv = lambda x, y: (9 if hmap[y][x] == 'X' else int(hmap[y][x])) if 0 <= x < W and 0 <= y < H else 9
    lav = set(lava)
    g = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if (x, y) in lav:
                g[y][x] = lava_tile(); continue
            h = lv(x, y)
            low = lambda xx, yy: (xx, yy) in lav or lv(xx, yy) < h
            n, s, e, w = low(x, y - 1), low(x, y + 1), low(x + 1, y), low(x - 1, y)
            if (x, y + 1) in lav: t = 0x347
            elif (x + 1, y) in lav: t = 0x346
            elif (x - 1, y) in lav: t = 0x289
            elif not (n or s or e or w or low(x + 1, y + 1) or low(x - 1, y + 1) or low(x + 1, y - 1) or low(x - 1, y - 1)):
                if h == 9:
                    t = RIDGE[(x * 3 + (y // 7) * 5) % len(RIDGE)]
                    g[y][x] = T(t, True); continue
                g[y][x] = T(0x271, elev=3); continue
            else:
                assert not (n and s) and not (e and w), 'terras: te smalle rand op (%d,%d)' % (x, y)
                if s and e: t = 0x27a
                elif s and w: t = 0x278
                elif n and w: t = 0x268
                elif n and e: t = 0x26a
                elif s: t = 0x274
                elif n: t = 0x269
                elif e: t = 0x272
                elif w: t = 0x270
                elif low(x + 1, y + 1): t = 0x27b
                elif low(x - 1, y + 1): t = 0x27c
                elif low(x + 1, y - 1): t = 0x27f
                else: t = 0x27e
            g[y][x] = T(t, True)
    for y in range(H):
        for x in range(W):
            if (x, y - 1) in lav and (x, y) not in lav:
                g[y][x] = T(0x3a3, elev=3)
            elif (x, y) not in lav and walkable(g[y][x]) and ((x - 1, y - 1) in lav or (x + 1, y - 1) in lav):
                g[y][x] = T(0x3a4, elev=3)
    return g

def stairs(g, cells):
    """Trap (2af) in een zuidwand: links/rechts ook wand, erboven en eronder beloopbaar."""
    for x, y in cells:
        assert (g[y][x] & 0x3ff) == 0x274, 'trap (%d,%d) niet in een rechte wand: %03x' % (x, y, g[y][x] & 0x3ff)
    for x, y in cells:
        g[y][x] = T(0x2af, elev=3)
    for x, y in cells:
        assert walkable(g[y - 1][x]) and walkable(g[y + 1][x]), 'trap (%d,%d) loopt dood' % (x, y)
        for nx in (x - 1, x + 1):
            if (nx, y) not in cells:
                assert (g[y][nx] & 0x3ff) in (0x274, 0x278, 0x27a), 'trap (%d,%d) niet midden in een wand' % (x, y)

# ---------------------------------------------------------------- events
def obj(gfx, x, y, script, flag='0', ttype='TRAINER_TYPE_NONE', sight='0', move='MOVEMENT_TYPE_FACE_DOWN', local_id=None, elev=3):
    o = {}
    if local_id: o['local_id'] = local_id
    o.update({'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
              'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': ttype,
              'trainer_sight_or_berry_tree_id': sight, 'script': script, 'flag': flag})
    return o
def item(x, y, it, flag):
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', flag, sight=it, move='MOVEMENT_TYPE_LOOK_AROUND')
def trainer(gfx, x, y, script, sight, move):
    return obj(gfx, x, y, script, ttype='TRAINER_TYPE_NORMAL', sight=str(sight), move=move)
def sign(x, y, script):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY', 'script': script}
def hidden(x, y, it, flag):
    return {'type': 'hidden_item', 'x': x, 'y': y, 'elevation': 3, 'item': it, 'flag': flag}

# ---------------------------------------------------------------- decor (tools/grounded/lavaridge_decor.py)
DECOR = json.load(open('data/tilesets/secondary/lavaridge/decor.json'))
def area(cells, r=1):
    return {(x + dx, y + dy) for x, y in cells for dx in range(-r, r + 1) for dy in range(-r, r + 1)}
def sight(o):
    if o['trainer_type'] != 'TRAINER_TYPE_NORMAL': return set()
    d = {'MOVEMENT_TYPE_FACE_LEFT': (-1, 0), 'MOVEMENT_TYPE_FACE_RIGHT': (1, 0),
         'MOVEMENT_TYPE_FACE_UP': (0, -1), 'MOVEMENT_TYPE_FACE_DOWN': (0, 1)}[o['movement_type']]
    return {(o['x'] + d[0] * i, o['y'] + d[1] * i) for i in range(1, int(o['trainer_sight_or_berry_tree_id']) + 1)}
def keep_cells(objs, bgs, extra=()):
    k = set(extra)
    for o in objs:
        k |= area([(o['x'], o['y'])]) | sight(o)
    for b in bgs:
        k |= area([(b['x'], b['y'])])
    return k

def place(g, name, x, y, kind):
    info = DECOR['%s_%s' % (name, kind)]
    for j, row in enumerate(info['ids']):
        for i, mt in enumerate(row):
            g[y + j][x + i] = T(mt, True) if info['collision'] else T(mt, elev=3)

def decorate(g, floor, kind, keep, starts, rules, rng, used=None):
    """Strooit decor over vloercellen (metatile `floor`, beloopbaar). Decor met botsing mag het bereikbare
    gebied alleen met zijn eigen cellen verkleinen (geen afgesloten hoekjes). rules: (naam, aantal, plek)
    met plek 'muur' (naast een rand), 'open' (niet naast een rand) of 'vrij'."""
    H, W = len(g), len(g[0])
    used = set() if used is None else used
    base = reach(g, starts)
    def wallside(c):
        return any(not walkable(g[c[1] + dy][c[0] + dx]) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if 0 <= c[0] + dx < W and 0 <= c[1] + dy < H)
    for name, count, where in rules:
        info = DECOR['%s_%s' % (name, kind)]
        h, w = len(info['ids']), len(info['ids'][0])
        placed = tries = 0
        while placed < count and tries < count * 200:
            tries += 1
            x, y = rng.randrange(1, W - w), rng.randrange(1, H - h)
            cells = [(x + i, y + j) for j in range(h) for i in range(w)]
            if any((g[cy][cx] & 0x3ff) != floor or not walkable(g[cy][cx]) or (cx, cy) in keep or (cx, cy) in used
                   or (cx, cy) not in base for cx, cy in cells):
                continue
            if any(c in used for c in area(cells) - set(cells)): continue
            ws = any(wallside(c) for c in cells)
            if where == 'muur' and not ws: continue
            if where == 'open' and ws: continue
            if info['collision']:
                after = reach(g, starts, blocked=set(cells))
                if after != base - set(cells): continue
                base = after
            place(g, name, x, y, kind)
            used |= set(cells); placed += 1
    return used

def ash_grass(g, keep, rng, n):
    """As-gras (Lavaridge 0x207) in grillige plukken op vlakke grond (0x271)."""
    H, W = len(g), len(g[0])
    flat = [(x, y) for y in range(H) for x in range(W) if (g[y][x] & 0x3ff) == 0x271 and walkable(g[y][x]) and (x, y) not in keep]
    done = set()
    for _ in range(n):
        cx, cy = rng.choice(flat)
        rx, ry = rng.uniform(1.5, 3.2), rng.uniform(1.0, 2.0)
        for y in range(cy - 3, cy + 4):
            for x in range(cx - 4, cx + 5):
                if 0 <= x < W and 0 <= y < H and (x, y) in set(flat) and ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 + rng.uniform(-0.3, 0.2):
                    g[y][x] = T(0x207, elev=3); done.add((x, y))
    return done

# ---------------------------------------------------------------- 1. Lavabuis
NICHES = [(21, 3), (37, 5), (3, 16), (3, 17), (7, 28), (8, 28)]
TW, TH = 40, 30
def tunnel_mask():
    m = [['.'] * TW for _ in range(TH)]
    def carve(x0, y0, x1, y1, c='#'):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                m[y][x] = c
    carve(29, 4, 36, 7)            # aankomst A
    carve(22, 5, 28, 6)            # gang west
    carve(10, 4, 22, 9)            # lavakamer
    carve(13, 4, 19, 5, '.'); carve(14, 4, 18, 5, 'L')
    carve(11, 10, 12, 12)          # gang zuid
    carve(4, 13, 27, 20)           # grote grot
    carve(4, 13, 6, 14, '.')       # afgeronde hoek
    carve(23, 19, 27, 20, '.')
    carve(15, 16, 17, 17, '.')     # rotspilaar midden in de grot
    carve(19, 13, 26, 14, '.'); carve(20, 13, 25, 14, 'L')
    carve(28, 17, 29, 17)          # doorgang naar de nis (Strength-blok op (28,17))
    carve(30, 15, 35, 19)          # nis
    carve(30, 15, 30, 15, '.'); carve(35, 15, 35, 15, '.')
    carve(8, 21, 9, 22)            # gang zuid
    carve(3, 23, 24, 27)           # benedenkamer
    carve(11, 23, 15, 24, '.'); carve(12, 23, 14, 24, 'L')
    carve(21, 26, 24, 27, '.')
    for x, y in NICHES: m[y][x] = '#'
    return [''.join(r) for r in m]

DOOR_A = (33, 3)     # -> Jagged Pass (16,6)
DOOR_B = (23, 22)    # -> Jagged Pass (10,18)
BOULDER = (28, 17)
def lava_tube():
    mask = tunnel_mask()
    g = cave_tiles(mask)
    cave_door(g, *DOOR_A); cave_door(g, *DOOR_B)
    objs = [
        trainer('OBJ_EVENT_GFX_HIKER', 21, 8, 'JaggedPass_LavaTube_EventScript_Hank', 4, 'MOVEMENT_TYPE_FACE_LEFT'),
        trainer('OBJ_EVENT_GFX_MAN_5', 8, 16, 'JaggedPass_LavaTube_EventScript_Ignace', 5, 'MOVEMENT_TYPE_FACE_RIGHT'),
        trainer('OBJ_EVENT_GFX_PICNICKER', 4, 25, 'JaggedPass_LavaTube_EventScript_Daisy', 3, 'MOVEMENT_TYPE_FACE_RIGHT'),
        item(5, 19, 'ITEM_CHARCOAL', 'FLAG_ITEM_LAVA_TUBE_CHARCOAL'),
        item(23, 25, 'ITEM_FIRE_STONE', 'FLAG_ITEM_LAVA_TUBE_FIRE_STONE'),
        item(34, 16, 'ITEM_FIRE_MEMORY', 'FLAG_ITEM_LAVA_TUBE_TM_FIRE_BLAST'),
        item(34, 19, 'ITEM_HEAT_ROCK', 'FLAG_ITEM_LAVA_TUBE_HEAT_ROCK'),
        obj('OBJ_EVENT_GFX_PUSHABLE_BOULDER', BOULDER[0], BOULDER[1], 'EventScript_StrengthBoulder', 'FLAG_TEMP_11', move='MOVEMENT_TYPE_LOOK_AROUND'),
    ]
    bgs = [hidden(3, 27, 'ITEM_LAVA_COOKIE', 'FLAG_HIDDEN_ITEM_LAVA_TUBE_LAVA_COOKIE'),
           sign(16, 16, 'JaggedPass_LavaTube_EventScript_Pillar')]
    rng = random.Random(77)
    starts = [(DOOR_A[0], DOOR_A[1] + 1), (DOOR_B[0], DOOR_B[1] + 1)]
    keep = keep_cells(objs, bgs, area(starts) | {(x, 17) for x in range(26, 33)} | {BOULDER})
    used = set()
    for i, (x, y) in enumerate(NICHES):            # zwavel in de nissen
        place(g, ('sulfur_a', 'sulfur_b')[i % 2], x, y, 'cave'); used.add((x, y))
    decorate(g, FLOOR, 'cave', keep, starts, [
        ('basalt', 3, 'vrij'), ('boulder', 3, 'open'), ('sulfur_a', 4, 'muur'), ('sulfur_b', 4, 'muur'),
        ('rock', 7, 'muur'), ('ash_a', 5, 'vrij'), ('ash_b', 5, 'vrij'), ('crack_a', 9, 'vrij'), ('crack_b', 9, 'vrij'),
    ], rng, used)
    return g, objs, bgs, mask

# ---------------------------------------------------------------- 2. De top
SW, SH = 36, 40
def summit_hmap():
    m = [['X'] * SW for _ in range(SH)]
    def fill(x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                m[y][x] = c
    fill(8, 7, 27, 12, '3')        # top (kraterrand)
    fill(10, 6, 25, 6, '3')        # oever onder het kratermeer (rij 6 = 3a3/3a4)
    fill(4, 13, 31, 21, '2')       # terras 2
    fill(4, 13, 6, 14, 'X'); fill(29, 13, 31, 14, 'X')
    fill(19, 16, 21, 17, 'X')      # rotsblok midden op terras 2
    fill(3, 22, 32, 29, '1')       # terras 1
    fill(3, 26, 5, 29, 'X'); fill(13, 25, 15, 26, 'X')
    fill(6, 30, 29, 37, '0')       # terras 0 (aankomst)
    fill(6, 34, 9, 37, 'X'); fill(26, 35, 29, 37, 'X')
    fill(32, 17, 33, 19, '2')      # nis oost op terras 2 (Magmarizer-hoekje)
    fill(1, 22, 2, 24, '1')        # nis west op terras 1
    fill(30, 32, 31, 34, '0')      # nis oost op terras 0
    fill(28, 23, 30, 24, 'X')      # rotspartij terras 1
    fill(20, 32, 22, 33, 'X')      # rotspartij terras 0
    fill(24, 7, 27, 8, '3'); fill(26, 7, 27, 7, 'X')   # uitkijkhoek naast het kratermeer
    return [''.join(r) for r in m]
CRATER = [(x, y) for x in range(12, 24) for y in range(2, 6)]
SUMMIT_ARRIVE = [(17, 38), (18, 38)]
SUMMIT_STAIRS = [(17, 12), (18, 12), (8, 21), (9, 21), (26, 29), (27, 29)]
def summit():
    hm = summit_hmap()
    g = terrace_tiles(hm, CRATER)
    stairs(g, SUMMIT_STAIRS)
    # aankomst: trap met zuidpijl, het pad loopt onder de kaartrand door
    for x, y in SUMMIT_ARRIVE:
        g[y][x] = T(0x216, elev=3); g[y + 1][x] = T(0x314, True)
        assert walkable(g[y - 1][x]), 'aankomst (%d,%d) loopt dood' % (x, y)
    for y in (38, 39):
        g[y][16] = T(0x272, True); g[y][19] = T(0x270, True)
    objs = [
        trainer('OBJ_EVENT_GFX_HIKER', 11, 33, 'MtChimney_Summit_EventScript_Grant', 4, 'MOVEMENT_TYPE_FACE_RIGHT'),
        trainer('OBJ_EVENT_GFX_MAN_5', 24, 24, 'MtChimney_Summit_EventScript_Pyro', 5, 'MOVEMENT_TYPE_FACE_LEFT'),
        trainer('OBJ_EVENT_GFX_EXPERT_F', 10, 15, 'MtChimney_Summit_EventScript_Vera', 5, 'MOVEMENT_TYPE_FACE_RIGHT'),
        item(30, 20, 'ITEM_MAGMARIZER', 'FLAG_ITEM_MT_CHIMNEY_SUMMIT_MAGMARIZER'),
        obj('OBJ_EVENT_GFX_SPECIES(VOLCARONA)', 17, 7, 'MtChimney_Summit_EventScript_Volcarona', 'FLAG_HIDE_MT_CHIMNEY_SUMMIT_VOLCARONA',
            local_id='LOCALID_SUMMIT_VOLCARONA'),
        obj('OBJ_EVENT_GFX_SCIENTIST_1', 23, 9, 'MtChimney_Summit_EventScript_Volcanologist', move='MOVEMENT_TYPE_FACE_LEFT'),
    ]
    bgs = [hidden(4, 25, 'ITEM_STAR_PIECE', 'FLAG_HIDDEN_ITEM_MT_CHIMNEY_SUMMIT_STAR_PIECE'),
           sign(28, 9, 'MtChimney_Summit_EventScript_SummitSign')]
    rng = random.Random(1137)
    starts = [(17, 37)]
    stair_keep = area([(x, y + d) for x, y in SUMMIT_STAIRS for d in (-1, 0, 1)])
    keep = keep_cells(objs, bgs, stair_keep | area(SUMMIT_ARRIVE + [(17, 37), (18, 37)]) | {(x, 6) for x in range(8, 28)})
    # gestolde lavastroom vanaf de krater + zwavel langs de kraterrand
    used = set()
    for x, y in ((11, 8), (12, 10), (21, 14), (25, 15)):
        place(g, 'basalt', x, y, 'ground'); used |= {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
    for (x, y), nm in (((9, 7), 'sulfur_a'), ((26, 8), 'sulfur_b'), ((32, 17), 'sulfur_b'), ((1, 22), 'sulfur_a'), ((31, 32), 'sulfur_a')):
        place(g, nm, x, y, 'ground'); used.add((x, y))
    grass = ash_grass(g, keep | area(used), rng, 9)
    decorate(g, 0x271, 'ground', keep | grass, starts, [
        ('deadtree', 5, 'muur'), ('stump', 5, 'vrij'), ('boulder', 3, 'open'), ('rock', 7, 'muur'),
        ('sulfur_a', 2, 'muur'), ('ash_a', 6, 'vrij'), ('ash_b', 6, 'vrij'), ('crack_a', 7, 'vrij'), ('crack_b', 7, 'vrij'),
    ], rng, used)
    # stoom uit de grond (vanilla 0x312/0x313, geanimeerd)
    flat = [(x, y) for y in range(SH) for x in range(SW) if (g[y][x] & 0x3ff) == 0x271 and walkable(g[y][x]) and (x, y) not in keep]
    for x, y in rng.sample(flat, 10):
        g[y][x] = T(rng.choice((0x312, 0x313)), elev=3)
    return g, objs, bgs, hm

# ---------------------------------------------------------------- bereikbaarheid
def reach(g, starts, blocked=(), passable=()):
    W, H = len(g[0]), len(g)
    seen = set(starts); st = list(starts)
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and n not in blocked and (walkable(g[n[1]][n[0]]) or n in passable):
                seen.add(n); st.append(n)
    return seen
def next_to(c, reg):
    return any((c[0] + dx, c[1] + dy) in reg for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))

# ---------------------------------------------------------------- registratie
def register_layout(name, const, W, H, anchor):
    lj = open('data/layouts/layouts.json').read()
    entry = '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_Lavaridge",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (const, name, W, H, name, name)
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"id": "LAYOUT_%s"' % const); s = lj.rindex('{', 0, i); e = lj.index('},', i) + 2
        lj = lj[:s - 5] + entry + lj[e:]
    else:
        i = lj.index('"id": "%s"' % anchor); j = lj.index('},', i) + 2
        lj = lj[:j] + entry + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)

def write_map(name, const, base, objs, warps, coords, bgs, **kw):
    b = json.load(open('data/maps/%s/map.json' % base))
    m = {k: b[k] for k in b}
    m.update({'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + const, 'connections': None,
              'object_events': objs, 'warp_events': warps, 'coord_events': coords, 'bg_events': bgs})
    m.update(kw)
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

def register_map(name, anchor_inc):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"gMapGroup_Grounded": ['); j = g.index(']', i)
        body = g[i:j].rstrip()
        g = g[:i] + body + ',\n    "%s"\n  ' % name + g[j:]
        open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/%s/scripts.inc"\n' % anchor_inc
        assert anchor in es
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)

def set_warp(m, x, y, elev, dest, dest_id):
    for i, w in enumerate(m['warp_events']):
        if w['x'] == x and w['y'] == y:
            w.update({'elevation': elev, 'dest_map': dest, 'dest_warp_id': str(dest_id)}); return i
    m['warp_events'].append({'x': x, 'y': y, 'elevation': elev, 'dest_map': dest, 'dest_warp_id': str(dest_id)})
    return len(m['warp_events']) - 1

def set_obj(m, o):
    for e in m['object_events']:
        if e['x'] == o['x'] and e['y'] == o['y'] and e['script'] == o['script']:
            e.clear(); e.update(o); return
    m['object_events'].append(o)

def set_coord(m, c):
    for e in m['coord_events']:
        if e['x'] == c['x'] and e['y'] == c['y'] and e.get('script') == c['script']:
            e.clear(); e.update(c); return
    m['coord_events'].append(c)

# ---------------------------------------------------------------- Jagged Pass / Mt. Chimney zelf
JP_A = (16, 6)      # opening in de klif vlak onder de trap naar Mt. Chimney
JP_B = (10, 18)     # opening in de wand van het plateau halverwege
MC_STAIRS = [(30, 4), (31, 4)]

def main():
    tg, tobjs, tbgs, tmask = lava_tube()
    sg, sobjs, sbgs, shm = summit()

    # --- Jagged Pass: twee grotopeningen (bovenste dicht met een Rock Smash-rots, vaste flag)
    jm = json.load(open('data/maps/JaggedPass/map.json'))
    jg, jp = load_layout('LAYOUT_JAGGED_PASS')
    for x, y in (JP_A, JP_B):
        if (jg[y][x] & 0x3ff) != 0x25e:
            assert (jg[y][x] & 0x3ff) == 0x274 and (jg[y - 1][x] & 0x3ff) == 0x271, 'Jagged Pass (%d,%d): geen wand onder grond' % (x, y)
        jg[y - 1][x] = T(0x256, True); jg[y][x] = T(0x25e)
    wa = set_warp(jm, JP_A[0], JP_A[1], 0, 'MAP_JAGGED_PASS_LAVA_TUBE', 0)
    wb = set_warp(jm, JP_B[0], JP_B[1], 0, 'MAP_JAGGED_PASS_LAVA_TUBE', 1)
    set_obj(jm, obj('OBJ_EVENT_GFX_BREAKABLE_ROCK', JP_A[0], JP_A[1], 'EventScript_RockSmash', 'FLAG_JAGGED_PASS_LAVA_TUBE_ROCK',
                    move='MOVEMENT_TYPE_LOOK_AROUND', elev=0))
    # bereikbaarheid vanaf de trap van Mt. Chimney (13,6) bergaf: de bovenste opening ligt aan het pad
    r = reach(jg, [(13, 6)])
    assert (JP_A[0], JP_A[1] + 1) in r, 'Jagged Pass: opening A onbereikbaar'
    rb = reach(jg, [(13, 19)])
    assert (JP_B[0], JP_B[1] + 1) in rb, 'Jagged Pass: opening B onbereikbaar'

    # --- Mt. Chimney: trap in de bergkam aan de noordoostkant
    mm = json.load(open('data/maps/MtChimney/map.json'))
    mg, mp = load_layout('LAYOUT_MT_CHIMNEY')
    for y in range(0, 4):
        mg[y][29] = T(0x270, True); mg[y][30] = T(0x271, True); mg[y][31] = T(0x271, True); mg[y][32] = T(0x272, True)
    for x, y in MC_STAIRS:
        mg[y][x] = T(0x217, elev=3)
    mg[4][29] = T(0x270, True); mg[4][32] = T(0x272, True)
    for x, y in MC_STAIRS:
        assert walkable(mg[y + 1][x]), 'Mt. Chimney: trap (%d,%d) loopt dood' % (x, y)
    r = reach(mg, [(30, 7)])
    assert all(c in r for c in MC_STAIRS), 'Mt. Chimney: trap onbereikbaar'
    mw = [set_warp(mm, x, y, 3, 'MAP_MT_CHIMNEY_SUMMIT', i) for i, (x, y) in enumerate(MC_STAIRS)]
    set_obj(mm, obj('OBJ_EVENT_GFX_SCIENTIST_1', 32, 6, 'MtChimney_EventScript_TrailGuard', 'FLAG_HIDE_MT_CHIMNEY_TRAIL_GUARD',
                    move='MOVEMENT_TYPE_FACE_LEFT', local_id='LOCALID_MT_CHIMNEY_TRAIL_GUARD'))
    for x, y in MC_STAIRS:
        set_coord(mm, {'type': 'trigger', 'x': x, 'y': y + 1, 'elevation': 3, 'var': 'VAR_TEMP_1', 'var_value': '0',
                       'script': 'MtChimney_EventScript_TrailClosed'})

    # --- Lavabuis: bereikbaarheid
    ta = (DOOR_A[0], DOOR_A[1] + 1); tb = (DOOR_B[0], DOOR_B[1] + 1)
    tobj_cells = {(o['x'], o['y']) for o in tobjs if o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL'}
    no_str = reach(tg, [ta], blocked=tobj_cells)
    assert tb in no_str, 'Lavabuis: A en B niet verbonden'
    for o in tobjs:
        if o['graphics_id'] in ('OBJ_EVENT_GFX_PUSHABLE_BOULDER',): continue
        c = (o['x'], o['y'])
        strength_item = o['flag'] in ('FLAG_ITEM_LAVA_TUBE_TM_FIRE_BLAST', 'FLAG_ITEM_LAVA_TUBE_HEAT_ROCK')
        if strength_item:
            assert not next_to(c, no_str), 'Lavabuis: %s is zonder Strength te pakken' % o['flag']
            with_str = reach(tg, [ta], blocked=tobj_cells - {BOULDER} - {c})
            assert next_to(c, with_str) or c in with_str, 'Lavabuis: %s onbereikbaar met Strength' % o['flag']
        else:
            assert next_to(c, no_str), 'Lavabuis: %s op %s onbereikbaar' % (o['script'], c)
    # het blok kun je twee keer naar rechts duwen (de nis in) zonder hem vast te zetten
    assert walkable(tg[BOULDER[1]][BOULDER[0] - 1]) and walkable(tg[BOULDER[1]][BOULDER[0] + 1]) and walkable(tg[BOULDER[1]][BOULDER[0] + 2])
    for b in tbgs:
        if b['type'] == 'hidden_item':
            assert (b['x'], b['y']) in no_str, 'Lavabuis: verborgen item onbereikbaar'

    # --- Top: bereikbaarheid
    sobj_cells = {(o['x'], o['y']) for o in sobjs if o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL'}
    rs = reach(sg, [(17, 37)], blocked=sobj_cells)
    for o in sobjs:
        assert next_to((o['x'], o['y']), rs), 'Top: %s op (%d,%d) onbereikbaar' % (o['script'], o['x'], o['y'])
    for b in sbgs:
        if b['type'] == 'hidden_item': assert (b['x'], b['y']) in rs, 'Top: verborgen item onbereikbaar'
        else: assert next_to((b['x'], b['y']), rs), 'Top: bord onbereikbaar'

    # --- wegschrijven
    save_grid(jg, jp); save_grid(mg, mp)
    open('data/maps/JaggedPass/map.json', 'w').write(json.dumps(jm, indent=2, ensure_ascii=False) + '\n')
    open('data/maps/MtChimney/map.json', 'w').write(json.dumps(mm, indent=2, ensure_ascii=False) + '\n')

    rock = T(0x271, True)
    for name, const, g, anchor in (('JaggedPass_LavaTube', 'JAGGED_PASS_LAVA_TUBE', tg, 'LAYOUT_JAGGED_PASS'),
                                   ('MtChimney_Summit', 'MT_CHIMNEY_SUMMIT', sg, 'LAYOUT_MT_CHIMNEY')):
        os.makedirs('data/layouts/' + name, exist_ok=True)
        save_grid(g, 'data/layouts/%s/map.bin' % name)
        save_grid([[rock, rock], [rock, rock]], 'data/layouts/%s/border.bin' % name)
        register_layout(name, const, len(g[0]), len(g), anchor)

    write_map('JaggedPass_LavaTube', 'JAGGED_PASS_LAVA_TUBE', 'FieryPath', tobjs,
              [{'x': DOOR_A[0], 'y': DOOR_A[1], 'elevation': 0, 'dest_map': 'MAP_JAGGED_PASS', 'dest_warp_id': str(wa)},
               {'x': DOOR_B[0], 'y': DOOR_B[1], 'elevation': 0, 'dest_map': 'MAP_JAGGED_PASS', 'dest_warp_id': str(wb)}],
              [], tbgs, region_map_section='MAPSEC_JAGGED_PASS', show_map_name=False)
    write_map('MtChimney_Summit', 'MT_CHIMNEY_SUMMIT', 'MtChimney', sobjs,
              [{'x': x, 'y': y, 'elevation': 3, 'dest_map': 'MAP_MT_CHIMNEY', 'dest_warp_id': str(mw[i])}
               for i, (x, y) in enumerate(SUMMIT_ARRIVE)],
              [], sbgs, show_map_name=False)
    register_map('JaggedPass_LavaTube', 'JaggedPass')
    register_map('MtChimney_Summit', 'MtChimney')

    if len(sys.argv) > 1:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from gridrender import render
        from PIL import Image
        ims = [render(tg, 'general', 'lavaridge'), render(sg, 'general', 'lavaridge')]
        out = Image.new('RGB', (sum(i.width for i in ims) + 16, max(i.height for i in ims)), 'black')
        x = 0
        for i in ims: out.paste(i, (x, 0)); x += i.width + 16
        out.save(sys.argv[1])
    print('klaar; Jagged Pass-warps %d/%d, Mt. Chimney-warps %s' % (wa, wb, mw))

if __name__ == '__main__':
    main()
