"""Project Grounded: de diepzeetrog onder Route 127 als onderwatersnelweg (Jordi, 9 okt).

Underwater_Route127_Trench (40x101): de schacht (rij 0-49, 22 breed) komt uit zee_vulling_4.py (kopie van de Sealed
Chamber-trog) en blijft zoals hij is. Het rotsblok in de oude onderste kamer ('grot zonder ingang') is weg: onder de
schacht kronkelt nu een zigzaggebied van vijf kommen (A-E) met nissen, en in de noordwand van de diepste kom (E) zit
een tweede zwemgat naar de Sea Temple-kom van onderwater Route 128 (warp 1 <-> Underwater_Route128). Bovenkomen in de
zuidelijke helft brengt je naar Route 128 (boven die kom), in de noordhelft naar Route 127 (zoals eerst).
Tegels: klassenraster (R rots / F zwemruimte), ge-autotiled met tegels uit dezelfde 3x3-omgeving in de Sealed
Chamber-stijl (Underwater_SealedChamber, Underwater_SeaTemple, Underwater_Route136 en de schacht zelf).
Items: de bestaande trogvondsten (Deep Sea Scale/Tooth, verborgen Relic Crown; flags uit zee_vulling_4.py) verhuizen
naar de nieuwe kommen, plus items die nergens anders liggen (nieuwe_items.py). De Sea Shard (coral_cathedral.py)
ligt in de schacht: draai coral_cathedral.py daarna opnieuw.
Deterministisch en idempotent. Gebruik: python3 tools/grounded/maptools/trog127.py [render.png]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, math, os, random, struct, subprocess, sys
from collections import Counter, defaultdict, deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
os.chdir(REPO)
import nieuwe_items as ni

NAME, CONST = 'Underwater_Route127_Trench', 'UNDERWATER_ROUTE127_TRENCH'
UW128 = 'Underwater_Route128'
SHAFT_W, KEEP_ROWS = 22, 49            # rijen 0-48 van de schacht blijven ongemoeid (rij 49 sluit aan)
W, H = 40, 101
LAYOUT_DIR = 'data/layouts/' + NAME
COL = 0x400
HOLE_TOP, HOLE_BOT = (0x265, 0x266, 0x267), (0x26D, 0x26E, 0x26F)
HOLE_MTS = set(HOLE_TOP) | set(HOLE_BOT) | {0x270}
ROCK_V = 0x0613                         # massieve rots (213, botsing)
FLOOR_MT, WEED_MT = 0x2D3, 0x281        # trogbodem en zeewier (MB_SEAWEED_NO_SURFACING: encounters)
UW128_HOLE = (69, 16)                   # bovenrij van het nieuwe zwemgat in onderwater 128 (warp op 69,17)
SURFACE_N = ('MAP_ROUTE127', 24, 14)
SURFACE_S = ('MAP_ROUTE128', 69, 18)
SURFACE_SPLIT = 60                      # bovenkomen vanaf deze rij = Route 128

LAYOUTS = {l['id']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'id' in l}


def read_grid(name):
    d = json.load(open('data/maps/%s/map.json' % name))
    L = LAYOUTS[d['layout']]
    w, h = L['width'], L['height']
    b = open(L['blockdata_filepath'], 'rb').read()
    return [list(struct.unpack_from('<%dH' % w, b, y * w * 2)) for y in range(h)], L


def klass(t):
    if (t & 0x3FF) in HOLE_MTS:
        return 'X'
    return 'R' if t & 0xC00 else 'F'


def norm(t):
    """Zeewier en schachtstrepen tellen als gewone trogbodem."""
    m = t & 0x3FF
    if m == WEED_MT or (0x2D0 <= m <= 0x2DF and not t & 0xC00):
        return (t & 0xF000) | FLOOR_MT
    return t


# ---------------------------------------------------------------------------------------------- 3x3-patronen leren
N8 = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
PAT8 = defaultdict(Counter)


def learn(g, y1=None):
    h, w = len(g), len(g[0])
    C = [[klass(t) for t in r] for r in g]
    for y in range(h if y1 is None else y1):
        for x in range(w):
            c = C[y][x]
            if c == 'X':
                continue
            nb = tuple(C[y + dy][x + dx] if 0 <= x + dx < w and 0 <= y + dy < h else c for dx, dy in N8)
            if 'X' in nb:
                continue
            PAT8[(c, nb)][norm(g[y][x])] += 1


def autotile_cell(C, x, y):
    c = C[y][x]
    nb = tuple(C[y + dy][x + dx] if 0 <= x + dx < W and 0 <= y + dy < H else c for dx, dy in N8)
    if c == 'F' and all(n == 'F' for n in nb):
        return 0x3000 | FLOOR_MT, 0
    if c == 'R' and all(n == 'R' for n in nb):
        return ROCK_V, 0
    if (c, nb) in PAT8:
        return PAT8[(c, nb)].most_common(1)[0][0], 0
    best = None
    for (pc, pn), cnt in PAT8.items():
        if pc != c:
            continue
        d = sum((2 if i in (1, 3, 4, 6) else 1) for i in range(8) if pn[i] != nb[i])
        key = (d, -sum(cnt.values()))
        if best is None or key < best[0]:
            best = (key, cnt)
    return best[1].most_common(1)[0][0], best[0][0]


# ---------------------------------------------------------------------------------------------- vormen
def blob(C, cx, cy, rx, ry, seed):
    rnd = random.Random(seed)
    noise = [rnd.uniform(-0.22, 0.22) for _ in range(10)]
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            a = math.atan2((y - cy) / ry, (x - cx) / rx)
            k = (a + math.pi) / (2 * math.pi) * 10
            i = int(k) % 10
            f = k - int(k)
            n = noise[i] * (1 - f) + noise[(i + 1) % 10] * f
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= (1 + n) ** 2:
                C[y][x] = 'F'


def path(C, pts, r=1.8):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
        for i in range(n + 1):
            px, py = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n
            for y in range(int(py - r) - 1, int(py + r) + 2):
                for x in range(int(px - r) - 1, int(px + r) + 2):
                    if (x - px) ** 2 + (y - py) ** 2 <= r * r:
                        C[y][x] = 'F'


def cleanup(C, y0):
    """Geen dunne rotsribbels (<3), geen 1-brede zwemgangen, geen diagonale aanrakingen (alleen rij >= y0)."""
    for _ in range(30):
        ch = 0
        for y in range(y0, H):
            for x in range(W):
                if C[y][x] != 'R' or x < 2 or x >= W - 2 or y >= H - 3:
                    continue
                for dx, dy in ((1, 0), (0, 1)):
                    # rotsloop tussen twee zwemvlakken korter dan 3 -> open
                    a = 1
                    while 0 <= x - dx * a < W and 0 <= y - dy * a < H and C[y - dy * a][x - dx * a] == 'R' and a < 4:
                        a += 1
                    b = 1
                    while 0 <= x + dx * b < W and 0 <= y + dy * b < H and C[y + dy * b][x + dx * b] == 'R' and b < 4:
                        b += 1
                    if a + b - 1 < (4 if dy else 3) and C[y - dy * a][x - dx * a] == 'F' and C[y + dy * b][x + dx * b] == 'F':
                        C[y][x] = 'F'; ch += 1
                        break
        for y in range(y0, H - 1):
            for x in range(W - 1):
                q = [C[y][x], C[y][x + 1], C[y + 1][x], C[y + 1][x + 1]]
                if q in (['F', 'R', 'R', 'F'], ['R', 'F', 'F', 'R']):
                    C[y][x] = C[y][x + 1] = C[y + 1][x] = C[y + 1][x + 1] = 'F'; ch += 1
        for c, n in (('F', 3), ('R', 3)):
            # bodem: elke cel in een vrij 3x3-vak (geen 1-2 brede uitstulpingen); rots: in een 2x2-vak
            rng = range(-(n - 1), 1)
            for y in range(max(y0, 2), H - 2):
                for x in range(2, W - 2):
                    if C[y][x] != c:
                        continue
                    if not any(all(C[y + b][x + a] == c for a in range(sx, sx + n) for b in range(sy, sy + n))
                               for sx in rng for sy in rng):
                        C[y][x] = 'R' if c == 'F' else 'F'; ch += 1
        if not ch:
            return
    raise SystemExit('cleanup convergeert niet')


# ---------------------------------------------------------------------------------------------- het zigzaggebied
CHAMBERS = [  # (sleutel, cx, cy, rx, ry): elke kom = een paar overlappende lobben
    ('A', 12, 55, 6.5, 3.6), ('A2', 8, 57.5, 3.5, 2.5), ('A3', 16, 53.5, 3, 2.2),
    ('B', 32.5, 62, 4.2, 3.8), ('B2', 30.5, 58.5, 3.4, 2.4), ('B3', 34, 65, 3, 2),
    ('C', 8.5, 73, 4.6, 3.2), ('C2', 11, 70.5, 3.2, 2), ('C3', 6.5, 76, 2.6, 2),
    ('D', 31.5, 83.5, 5, 3.2), ('D2', 28, 81.5, 3.2, 2.2), ('D3', 34.5, 86.5, 3, 2),
    ('E', 11.5, 95, 5.5, 2.6), ('E2', 8, 92.5, 2.8, 2.4), ('E3', 16.5, 96, 3.6, 2)]
PATHS = [  # gangen (kronkelend) en nissen
    [(11, 47), (11, 52)],                                        # schacht -> A
    [(17, 57), (21, 59), (25, 57.5), (29, 59)],                  # A -> B
    [(30, 65.5), (26, 68.5), (21, 67), (16, 69), (12, 71)],     # B -> C
    [(11, 75.5), (15, 78.5), (20, 77.5), (25, 79.5), (28, 81)], # C -> D
    [(28, 86), (23, 88.5), (18, 87.5), (14, 90), (13, 91.5)],   # D -> E
]
NICHES = [  # (sleutel, gang, nis): kleine kom aan een gang
    ('A1', [(7, 57.5), (4.5, 60)], (4.5, 61, 2.2, 2.0)),
    ('B1', [(35, 59), (36, 55.5)], (36, 54.5, 2.0, 2.0)),
    ('C1', [(5, 75), (4.5, 79)], (4.5, 80, 2.2, 2.0)),
    ('D1', [(35.5, 86), (35.5, 90)], (35.5, 91, 2.0, 2.0)),
]


def design(old):
    C = [['R'] * W for _ in range(H)]
    for y in range(KEEP_ROWS + 1):
        for x in range(SHAFT_W):
            C[y][x] = 'R' if old[y][x] & 0xC00 else 'F'
    for i, (k, cx, cy, rx, ry) in enumerate(CHAMBERS):
        blob(C, cx, cy, rx, ry, 'trog127-' + k)
    for p in PATHS:
        path(C, p)
    for k, p, (cx, cy, rx, ry) in NICHES:
        path(C, p, 1.9)
        blob(C, cx, cy, rx, ry, 'trog127-' + k)
    # op een raster van 2x2: elke bocht en uitstulping is minstens 2 tegels (geen trapjes van 1 tegel)
    y0 = KEEP_ROWS + 1
    for by in range(y0, H - 1, 2):
        for bx in range(0, W - 1, 2):
            f = sum(C[by + b][bx + a] == 'F' for a in (0, 1) for b in (0, 1)) >= 2
            for a in (0, 1):
                for b in (0, 1):
                    C[by + b][bx + a] = 'F' if f else 'R'
    for y in range(KEEP_ROWS + 1):          # de schacht zelf verandert niet
        for x in range(SHAFT_W):
            C[y][x] = 'R' if old[y][x] & 0xC00 else 'F'
    cleanup(C, KEEP_ROWS + 1)
    for y in range(H):                      # rand van 2 rots
        for x in range(W):
            if x < 2 or x >= W - 2 or y >= H - 3:
                assert C[y][x] == 'R' or y <= KEEP_ROWS, ('rand', x, y)
    return C


def build():
    old, L = read_grid(NAME)
    if L['width'] != SHAFT_W:                # al eerder omgebouwd: neem de schacht uit de huidige kaart
        old = [r[:SHAFT_W] for r in old]
    for src in ('Underwater_SealedChamber', 'Underwater_SeaTemple', 'Underwater_Route136'):
        learn(read_grid(src)[0])
    learn(old, KEEP_ROWS)
    C = design(old)
    g = [[ROCK_V] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if y < KEEP_ROWS and x < SHAFT_W:
                g[y][x] = old[y][x]
    far = Counter()
    for y in range(KEEP_ROWS, H):
        for x in range(W):
            g[y][x], d = autotile_cell(C, x, y)
            if d:
                far[d] += 1
    if far:
        print('trog: patronen zonder exact voorbeeld (afstand: aantal):', dict(sorted(far.items())))
    return C, g


def hole(C, g):
    """Zwemgat in de noordwand van kom E: de onderste rij van het gat staat in de wandrij boven de bodem.
    Plek: de 3 cellen onder het gat zijn bodem, erboven minstens 4 rijen rots; liefst met bodem ernaast."""
    best = None
    for yf in range(88, H - 3):
        for ex in range(4, W - 4):
            if not all(C[yf][ex + d] == 'F' for d in (-1, 0, 1)) or not all(C[yf - 1][ex + d] == 'R' for d in (-1, 0, 1)):
                continue
            if not all(C[y][ex + d] == 'R' for y in range(yf - 5, yf) for d in (-1, 0, 1)):
                continue
            score = sum(C[yf][ex + d] == 'F' for d in (-2, 2)) * 10 + sum(C[yf - 1][ex + d] == 'R' for d in (-2, 2)) * 5 - ex
            if best is None or score > best[0]:
                best = (score, ex, yf)
    assert best, 'geen plek voor het zwemgat'
    _, ex, yf = best
    for i in range(3):
        g[yf - 2][ex - 1 + i] = HOLE_TOP[i] | COL
        g[yf - 1][ex - 1 + i] = HOLE_BOT[i] | (0 if i == 1 else COL)
    return (ex, yf - 1)


def seaweed(C, g, keep):
    rnd = random.Random('trog127-zeewier')
    n = 0
    for (cx, cy, rx, ry) in [(9, 54, 4, 2.2), (15, 56, 3, 1.8), (33, 63, 3, 2.5), (7, 73, 3, 2), (31, 84, 4, 2),
                             (13, 95, 5, 2), (21, 67.5, 3, 1.2), (24, 79, 3, 1.2)]:
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if (x, y) in keep or not (0 <= y < H and 0 <= x < W):
                    continue
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1 and rnd.random() < 0.85 \
                        and g[y][x] & 0x3FF == FLOOR_MT and not g[y][x] & COL:
                    g[y][x] = (g[y][x] & 0xF000) | WEED_MT; n += 1
    return n


# ---------------------------------------------------------------------------------------------- events
def reach(g, start, solid=()):
    seen = {start}; q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if 0 <= p[0] < W and 0 <= p[1] < H and p not in seen and not g[p[1]][p[0]] & COL and p not in solid:
                seen.add(p); q.append(p)
    return seen


def adj(r, p):
    return any((p[0] + dx, p[1] + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def nearest_floor(C, p, taken):
    x0, y0 = p
    best = None
    for y in range(H):
        for x in range(W):
            if C[y][x] == 'F' and (x, y) not in taken and all(C[y + b][x + a] == 'F' for a in (-1, 0, 1) for b in (-1, 0, 1)):
                d = (x - x0) ** 2 + (y - y0) ** 2
                if best is None or d < best[0]:
                    best = (d, (x, y))
    return best[1]


def ball(x, y, item, flag, qty=1):
    return {'graphics_id': 'OBJ_EVENT_GFX_ITEM_BALL', 'x': x, 'y': y, 'elevation': 3,
            'movement_type': 'MOVEMENT_TYPE_LOOK_AROUND', 'movement_range_x': qty if qty > 1 else 0,
            'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': item,
            'script': 'Common_EventScript_FindItem', 'flag': flag}


def hidden(x, y, item, flag, qty=1):
    h = {'type': 'hidden_item', 'x': x, 'y': y, 'elevation': 3, 'item': item, 'flag': flag}
    if qty > 1:
        h['quantity'] = qty
    return h


# (doelplek, item, flag, aantal, verborgen): de plek wordt de dichtstbijzijnde open plek (3x3 vrij)
OLD_ITEMS = [((4, 60), 'ITEM_DEEP_SEA_TOOTH', 'FLAG_ITEM_ZV4_TRENCH_DEEP_SEA_TOOTH', 1, False),
             ((34, 85), 'ITEM_DEEP_SEA_SCALE', 'FLAG_ITEM_ZV4_TRENCH_DEEP_SEA_SCALE', 1, False),
             ((18, 96), 'ITEM_RELIC_CROWN', 'FLAG_HIDDEN_ITEM_ZV4_TRENCH_RELIC_CROWN', 1, True)]
NEW_SPOTS = {'ITEM_LURE_BALL': (36, 54), 'ITEM_HEAVY_BALL': (35, 65), 'ITEM_BINDING_BAND': (4, 80),
             'ITEM_EJECT_BUTTON': (8, 71), 'ITEM_POWER_ANKLET': (35, 91), 'ITEM_EXP_CANDY_L': (5, 95),
             'ITEM_RELIC_VASE': (28, 84)}
SIGN_X = 13          # bord 'diepste punt' in de noordwand van kom E


def events(C, g, hole_xy):
    p = 'data/maps/%s/map.json' % NAME
    m = json.load(open(p))
    old_flags = {f for _, _, f, _, _ in OLD_ITEMS}
    new = ni.items(NAME)
    new_flags = {f for f, *_ in new}
    keep_o = [o for o in m['object_events'] if o['flag'] not in old_flags | new_flags]
    keep_b = [b for b in m['bg_events'] if b.get('flag') not in old_flags | new_flags and 'ZV4Bottom' not in b.get('script', '')]
    for e in keep_o + keep_b:
        assert e['y'] < KEEP_ROWS, ('event in het nieuwe deel', e)
    taken = {(e['x'], e['y']) for e in keep_o + keep_b}
    objs, bgs = [], []
    for spot, it, fl, q, hid in OLD_ITEMS + [(NEW_SPOTS[it], it, fl, q, hid) for fl, it, q, hid in new]:
        x, y = nearest_floor(C, spot, taken)
        taken.add((x, y))
        (bgs if hid else objs).append((hidden if hid else ball)(x, y, it, fl, q))
    # bord: wandtegel boven de bodem van kom E
    yb = min(y for y in range(88, H) if C[y][SIGN_X] == 'F') - 1
    assert C[yb][SIGN_X] == 'R'
    bgs.append({'type': 'sign', 'x': SIGN_X, 'y': yb, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
                'script': NAME + '_EventScript_ZV4Bottom'})
    m['object_events'] = keep_o + objs
    m['bg_events'] = keep_b + bgs
    m['warp_events'] = [m['warp_events'][0]] + [{'x': hole_xy[0], 'y': hole_xy[1], 'elevation': 0,
                                                 'dest_map': 'MAP_UNDERWATER_ROUTE128', 'dest_warp_id': 'UW128_WARP'}]
    return m


def uw128(trench_warp):
    """Zwemgat in de noordwand van de Sea Temple-kom (onderwater 128) + warp naar de trog."""
    g, L = read_grid(UW128)
    x, y = UW128_HOLE
    src_top = [g[18][75 + i] for i in range(3)]          # het vanilla zwemgat naar de Sea Temple (75-77, 18-19)
    src_bot = [g[19][75 + i] for i in range(3)]
    assert [t & 0x3FF for t in src_top] == list(HOLE_TOP) and [t & 0x3FF for t in src_bot] == list(HOLE_BOT)
    for i in range(3):
        cur = (g[y][x - 1 + i] & 0x3FF, g[y + 1][x - 1 + i] & 0x3FF)
        assert cur[0] in (0x21E, HOLE_TOP[i]) and cur[1] in (0x240, 0x243, 0x241, HOLE_BOT[i]), ('UW128-plek', cur)
        g[y][x - 1 + i] = src_top[i]
        g[y + 1][x - 1 + i] = src_bot[i]
    assert not g[y + 2][x] & COL, 'onder het zwemgat geen zwemruimte'
    open(L['blockdata_filepath'], 'wb').write(b''.join(struct.pack('<%dH' % len(r), *r) for r in g))
    p = 'data/maps/%s/map.json' % UW128
    m = json.load(open(p))
    w = {'x': x, 'y': y + 1, 'elevation': 0, 'dest_map': 'MAP_' + CONST, 'dest_warp_id': str(trench_warp)}
    idx = [i for i, e in enumerate(m['warp_events']) if e['dest_map'] == 'MAP_' + CONST]
    if idx:
        m['warp_events'][idx[0]] = w; i = idx[0]
    else:
        m['warp_events'].append(w); i = len(m['warp_events']) - 1
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    return i


def scripts():
    sp = 'data/maps/%s/scripts.inc' % NAME
    s = open(sp).read()
    mark = '@ --- zee_vulling_4'
    tail = s[s.index(mark):] if mark in s else ''
    head = '''@ Project Grounded: de diepzeetrog onder Route 127 (zwemgat in de kop van de centrale trog van onderwater 127,
@ 24,13), een onderwatersnelweg: onderin een zigzaggebied met een tweede zwemgat naar de Sea Temple-kom van
@ onderwater Route 128. Bovenkomen: noordhelft = Route 127, zuidhelft (rij %d+) = Route 128.
@ Schacht: tools/grounded/maptools/zee_vulling_4.py; zigzaggebied, items en warps: tools/grounded/maptools/trog127.py
%s_MapScripts::
	map_script MAP_SCRIPT_ON_DIVE_WARP, %s_OnDive
	.byte 0

%s_OnDive:
	getplayerxy VAR_TEMP_0, VAR_TEMP_1
	goto_if_ge VAR_TEMP_1, %d, %s_OnDiveSouth
	setdivewarp %s, %d, %d
	end

%s_OnDiveSouth:
	setdivewarp %s, %d, %d
	end
''' % (SURFACE_SPLIT, NAME, NAME, NAME, SURFACE_SPLIT, NAME, SURFACE_N[0], SURFACE_N[1], SURFACE_N[2], NAME,
       SURFACE_S[0], SURFACE_S[1], SURFACE_S[2])
    open(sp, 'w').write(head + ('\n' + tail if tail else ''))


def set_layout_size():
    p = 'data/layouts/layouts.json'
    s = open(p).read()
    i = s.index('"id": "LAYOUT_%s"' % CONST)
    j = s.index('}', i)
    blk = s[i:j]
    import re
    blk2 = re.sub(r'"width": \d+', '"width": %d' % W, blk)
    blk2 = re.sub(r'"height": \d+', '"height": %d' % H, blk2)
    s = s[:i] + blk2 + s[j:]
    json.loads(s)
    open(p, 'w').write(s)


def main():
    C, g = build()
    hole_xy = hole(C, g)
    m = events(C, g, hole_xy)
    keep = {(o['x'], o['y']) for o in m['object_events'] + m['bg_events']} | {hole_xy, (hole_xy[0], hole_xy[1] + 1)}
    n = seaweed(C, g, keep)
    print('trog: %d zeewiertegels in het zigzaggebied' % n)
    # bereikbaarheid: alles vanaf het bovenste zwemgat
    w0 = m['warp_events'][0]
    solid = {(o['x'], o['y']) for o in m['object_events'] if o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL'}
    r = reach(g, (w0['x'], w0['y']), solid)
    probs = []
    for o in m['object_events']:
        if not adj(r, (o['x'], o['y'])) and (o['x'], o['y']) not in r:
            probs.append(('object', o['flag'], o['x'], o['y']))
    for b in m['bg_events']:
        ok = (b['x'], b['y']) in r if b['type'] == 'hidden_item' else adj(r, (b['x'], b['y']))
        if not ok:
            probs.append(('bg', b.get('flag') or b.get('script'), b['x'], b['y']))
    if hole_xy not in r:
        probs.append(('tweede zwemgat onbereikbaar', hole_xy))
    assert not probs, probs
    print('trog: %d zwemtegels bereikbaar, beide zwemgaten verbonden' % len(r))
    os.makedirs(LAYOUT_DIR, exist_ok=True)
    open(LAYOUT_DIR + '/map.bin', 'wb').write(b''.join(struct.pack('<%dH' % W, *row) for row in g))
    set_layout_size()
    wi = uw128(1)
    m['warp_events'][1]['dest_warp_id'] = str(wi)
    open('data/maps/%s/map.json' % NAME, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    scripts()
    ni.flags()
    if os.path.exists('build/emerald/data/maps.o'):
        os.remove('build/emerald/data/maps.o')
    if len(sys.argv) > 1:
        subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), NAME, sys.argv[1], '0', str(H)], check=True)
    print('klaar')


if __name__ == '__main__':
    main()
