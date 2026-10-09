"""Project Grounded: het scheepswrakkenkerkhof (Shipwreck Shoals) onder Route 131 + het spookschip S.S. AGAVE.

Bouwt (idempotent, vaste seed):
- tileset shipwreck_shoals via shipwreck_art.py (spookschip = Route 108-wrak met spookpaletten, wrakdecor).
- data/layouts/ShipwreckShoals (42x58, General + ShipwreckShoals): open zee met ondieptes (grijs, autotile op een
  hoekpuntenraster zoals Route 108), zandbanken, rotsen, masten, spanten, een gekapseisde romp, een boeg, tonnen en
  kisten. Verbonden met de zuidrand van Route 131 (offset 18): de bovenste rijen bevatten alleen General-tiles, dus
  de naad tekent goed met de Pacifidlog-tileset van Route 131.
  Het spookschip ligt 's nachts op de ondiepte in het midden (SHIP_X/SHIP_Y): het map-script zet de 19 metatiles
  met setmetatile (overdag is daar alleen een verdacht scheepsvormig stuk ondiepte). De ingang (MB_STAIRS_OUTSIDE_
  ABANDONED_SHIP) werkt alleen als de tile er ligt.
- Spookschip binnen: kopieen van de Abandoned Ship-layouts (Deck, Corridors_1F, Rooms_1F, CaptainsOffice) in eigen
  layoutmappen; in de gang zijn de trap naar B1F en de twee deuren naar Rooms2_1F dichtgemaakt.
- Registratie: layouts.json, map_groups.json (gMapGroup_Grounded), event_scripts.s, connection in Route131/map.json.
De map.json's en scripts.inc's staan met de hand in data/maps/ShipwreckShoals en data/maps/GhostShip_*; dit script
schrijft alleen de layouts en controleert de bereikbaarheid (objecten/borden/warps uit de map.json's).

Gebruik: python3 tools/grounded/maptools/shipwreck_shoals.py [rendermap]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, random, re, shutil, struct, sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shipwreck_art

W, H = 42, 58
SEED = 592  # Frillish
rng = random.Random(SEED)
SHIP_X, SHIP_Y = 18, 33          # linkerbovenhoek van het 6x4-schip
SHIP = [[0, 0x351, 0x352, 0x353, 0x354, 0], [0x358, 0x359, 0x35a, 0x35b, 0x35c, 0x35d],
        [0x360, 0x361, 0x362, 0x363, 0x364, 0x365], [0, 0x369, 0x36a, 0x36b, 0, 0]]
# botsing per schiptile zoals op Route 108 (de bovenrij en de trap/romp onderaan zijn beloopbaar)
SHIP_COLL = {0x351: 0, 0x352: 0, 0x353: 0, 0x354: 0, 0x369: 0, 0x36a: 0, 0x36b: 0}

names, ntiles = shipwreck_art.build()
print('tileset: %d tiles, %d metatiles' % (ntiles, len(names)))

# ---------------------------------------------------------------- gedrag
BEH = [re.match(r'\s*(MB_\w+)', l).group(1) for l in open('include/constants/metatile_behaviors.h')
       if re.match(r'\s*MB_\w+', l)]


def attrs(path):
    a = open(path, 'rb').read()
    return [struct.unpack_from('<H', a, i * 2)[0] for i in range(len(a) // 2)]


GEN = attrs('data/tilesets/primary/general/metatile_attributes.bin')
SEC = attrs(shipwreck_art.TS + '/metatile_attributes.bin')


def beh(mt):
    a = GEN[mt] if mt < 0x200 else SEC[mt - 0x200]
    return BEH[a & 0xFF]


SURF = {'MB_OCEAN_WATER', 'MB_DEEP_WATER', 'MB_POND_WATER'}

# ---------------------------------------------------------------- ondieptes en zandbanken (hoekpuntenraster)
V = [[0] * (W + 1) for _ in range(H + 1)]    # 1 = ondiepte
S = [[0] * (W + 1) for _ in range(H + 1)]    # 1 = zand


def vrect(G, x0, y0, x1, y1, v=1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            G[y][x] = v


# A: zandbank west (visser)
vrect(V, 3, 12, 13, 21); vrect(V, 3, 12, 4, 12, 0); vrect(V, 3, 13, 3, 13, 0); vrect(V, 12, 20, 13, 21, 0); vrect(V, 9, 21, 13, 21, 0)
vrect(S, 5, 14, 10, 18)
# B: ondiepte van het spookschip
vrect(V, SHIP_X - 1, SHIP_Y - 1, SHIP_X + 7, SHIP_Y + 4); vrect(V, SHIP_X - 1, SHIP_Y - 1, SHIP_X, SHIP_Y - 1, 0)
# C: zandbank zuidoost (eenzame mast + schat)
vrect(V, 27, 45, 38, 55); vrect(V, 27, 45, 29, 46, 0); vrect(V, 36, 54, 38, 55, 0)
vrect(S, 29, 48, 34, 53)
# D: kleine ondiepte noordoost (item)
vrect(V, 28, 14, 35, 19); vrect(V, 34, 14, 35, 15, 0)
# E: smalle ondiepte west (verborgen item)
vrect(V, 4, 40, 11, 44); vrect(V, 4, 44, 6, 44, 0)

SHOAL_MS = {(1, 1, 1, 1): 0x19e, (0, 1, 1, 1): 0x19b, (1, 0, 1, 1): 0x19c, (1, 1, 1, 0): 0x1a4, (1, 1, 0, 1): 0x1a3,
            (0, 0, 1, 1): 0x1ae, (1, 1, 0, 0): 0x1be, (0, 1, 0, 1): 0x1b5, (1, 0, 1, 0): 0x1b7,
            (0, 0, 0, 1): 0x1ad, (0, 0, 1, 0): 0x1af, (0, 1, 0, 0): 0x1bd, (1, 0, 0, 0): 0x1bf, (0, 0, 0, 0): 0x170}
SAND_MS = {(1, 1, 1, 1): 0x124, (0, 0, 0, 1): 0x195, (0, 0, 1, 1): 0x196, (0, 0, 1, 0): 0x197, (0, 1, 0, 1): 0x19d,
           (1, 0, 1, 0): 0x19f, (0, 1, 0, 0): 0x1a5, (1, 1, 0, 0): 0x1a6, (1, 0, 0, 0): 0x1a7,
           (0, 1, 1, 1): 0x185, (1, 0, 1, 1): 0x186, (1, 1, 0, 1): 0x18d, (1, 1, 1, 0): 0x18e}


def quad(G, x, y):
    return (G[y][x], G[y][x + 1], G[y + 1][x], G[y + 1][x + 1])


M = [[0x170] * W for _ in range(H)]
COLL = [[0] * W for _ in range(H)]
for y in range(H):
    for x in range(W):
        q = quad(V, x, y)
        if q not in SHOAL_MS:
            raise SystemExit('diagonale ondiepte op (%d,%d)' % (x, y))
        M[y][x] = SHOAL_MS[q]
        s = quad(S, x, y)
        if any(s):
            if q != (1, 1, 1, 1):
                raise SystemExit('zand tegen de rand van de ondiepte op (%d,%d)' % (x, y))
            if s not in SAND_MS:
                raise SystemExit('diagonaal zand op (%d,%d)' % (x, y))
            M[y][x] = SAND_MS[s]


def is_sea(x, y):
    return 0 <= x < W and 0 <= y < H and M[y][x] == 0x170 and not COLL[y][x]


def is_shoal(x, y):
    return 0 <= x < W and 0 <= y < H and M[y][x] == 0x19e and not COLL[y][x]


def stamp(piece, base, x0, y0, w, h):
    ok = is_sea if base == 'sea' else is_shoal
    for dy in range(h):
        for dx in range(w):
            if not ok(x0 + dx, y0 + dy):
                raise SystemExit('%s past niet op (%d,%d)' % (piece, x0 + dx, y0 + dy))
    for dy in range(h):
        for dx in range(w):
            M[y0 + dy][x0 + dx] = names['%s_%s_%d_%d' % (piece, base, dx, dy)]
            COLL[y0 + dy][x0 + dx] = 1


# vrij te houden: spookschip + ingang, events (uit de map.json), randen van de verbinding
KEEP = set()
for dy in range(-1, 6):
    for dx in range(-1, 7):
        KEEP.add((SHIP_X + dx, SHIP_Y + dy))
KEEP |= {(SHIP_X + 2, SHIP_Y + 4), (SHIP_X + 2, SHIP_Y + 5), (SHIP_X + 1, SHIP_Y + 5), (SHIP_X + 3, SHIP_Y + 5)}
MAPJ = json.load(open('data/maps/ShipwreckShoals/map.json'))
EVENTS = [(o['x'], o['y']) for o in MAPJ['object_events']] + [(b['x'], b['y']) for b in MAPJ['bg_events']]
for (ex, ey) in EVENTS:
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            KEEP.add((ex + dx, ey + dy))

# wrakken (vaste plekken)
# Groepjes: masten op een rij + spanten/boeg = een gezonken schip; los drijvend wrakhout ertussen.
WRECKS = [
    # bij de ingang: twee masten van een schip dat net niet de haven haalde
    ('mast', 'sea', 22, 9, 1, 3), ('mast', 'sea', 25, 10, 1, 3), ('crate', 'sea', 12, 8, 1, 1),
    ('barrel', 'sea', 26, 12, 1, 1),
    # westelijke zandbank: mast op de ondiepte
    ('mast', 'shoal', 12, 14, 1, 3), ('barrel', 'sea', 15, 20, 1, 1),
    # noordoost: boeg + mast naast de kleine ondiepte
    ('bow', 'sea', 37, 11, 2, 2), ('mast', 'sea', 39, 14, 1, 3), ('barrel', 'shoal', 33, 17, 1, 1),
    # midden-west: gekapseisde romp met wrakhout
    ('hull', 'sea', 4, 27, 3, 2), ('crate', 'sea', 8, 26, 1, 1), ('barrel', 'sea', 3, 31, 1, 1),
    # midden: geraamte met twee masten
    ('ribs', 'sea', 13, 25, 3, 2), ('mast', 'sea', 17, 22, 1, 3), ('mast', 'sea', 19, 23, 1, 3),
    ('crate', 'sea', 22, 27, 1, 1),
    # oost: geraamte, drie masten op een rij (een driemaster die rechtop zonk)
    ('ribs', 'sea', 28, 27, 3, 2), ('mast', 'sea', 32, 23, 1, 3), ('mast', 'sea', 34, 24, 1, 3),
    ('mast', 'sea', 36, 25, 1, 3), ('barrel', 'sea', 39, 24, 1, 1), ('crate', 'sea', 38, 29, 1, 1),
    # rond het spookschip: alleen wat wrakhout
    ('mast', 'sea', 10, 32, 1, 3), ('mast', 'sea', 31, 33, 1, 3), ('barrel', 'sea', 27, 37, 1, 1),
    ('mast', 'sea', 37, 35, 1, 3),
    # zuidwest: tweede romp, boeg en masten
    ('hull', 'sea', 19, 42, 3, 2), ('barrel', 'sea', 23, 41, 1, 1), ('crate', 'shoal', 9, 41, 1, 1),
    ('bow', 'sea', 13, 47, 2, 2), ('mast', 'sea', 10, 47, 1, 3), ('mast', 'sea', 8, 48, 1, 3),
    ('mast', 'sea', 2, 49, 1, 3), ('barrel', 'sea', 4, 54, 1, 1), ('crate', 'sea', 17, 54, 1, 1),
    ('ribs', 'sea', 19, 50, 3, 2), ('mast', 'sea', 24, 50, 1, 3),
    # zuidelijke zandbank: de eenzame mast (schat aan zijn voet) en wat wrakhout
    ('mast', 'shoal', 35, 46, 1, 3), ('crate', 'shoal', 30, 46, 1, 1), ('barrel', 'sea', 33, 41, 1, 1),
]
for piece, base, x0, y0, w, h in WRECKS:
    stamp(piece, base, x0, y0, w, h)

# rotsen: 2x2 in zee (General 175/176/17d/17e), kleine rotsjes op de ondiepte (194)
ROCK2 = (0x175, 0x176, 0x17d, 0x17e)
placed = 0
tries = 0
while placed < 13 and tries < 5000:
    tries += 1
    x, y = rng.randrange(1, W - 2), rng.randrange(6, H - 2)
    cells = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
    ring = [(x + dx, y + dy) for dx in range(-1, 3) for dy in range(-1, 3)]
    if all(is_sea(*c) for c in ring if 0 <= c[0] < W and 0 <= c[1] < H) and not any(c in KEEP for c in ring):
        for (cx, cy), m in zip(cells, ROCK2):
            M[cy][cx] = m
            COLL[cy][cx] = 1
        placed += 1
# een paar rotsen in de bovenste rijen zoals de zuidrand van Route 131 (alleen General-tiles)
for (x, y) in [(3, 2), (30, 1), (14, 4)]:
    for (cx, cy), m in zip([(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)], ROCK2):
        assert M[cy][cx] == 0x170
        M[cy][cx] = m
        COLL[cy][cx] = 1
for (x, y) in [(6, 19), (8, 13), (31, 19), (36, 50), (28, 52), (19, 32), (25, 36), (10, 43)]:
    if is_shoal(x, y) and (x, y) not in KEEP:
        M[y][x] = 0x194
        COLL[y][x] = 1

# bovenste 8 rijen: alleen General (de naad met Route 131 tekent met de Pacifidlog-tileset)
for y in range(8):
    for x in range(W):
        assert M[y][x] < 0x200, (x, y)


def val(m, coll):
    b = beh(m)
    if coll:
        return m | (1 << 10)
    if b in SURF:
        return m | (1 << 12)
    return m | (3 << 12)


os.makedirs('data/layouts/ShipwreckShoals', exist_ok=True)
with open('data/layouts/ShipwreckShoals/map.bin', 'wb') as f:
    for y in range(H):
        for x in range(W):
            f.write(struct.pack('<H', val(M[y][x], COLL[y][x])))
with open('data/layouts/ShipwreckShoals/border.bin', 'wb') as f:
    f.write(struct.pack('<4H', *([0x170 | (1 << 12)] * 4)))

# schip-tabel voor het map-script (setmetatile) en de render
SHIP_SET = []
for dy, row in enumerate(SHIP):
    for dx, m in enumerate(row):
        if m:
            SHIP_SET.append((SHIP_X + dx, SHIP_Y + dy, names['ship_%03x' % m], 1 if SHIP_COLL.get(m, 1) else 0))
for (x, y, m, c) in SHIP_SET:
    assert M[y][x] == 0x19e and not COLL[y][x], (x, y)


def ship_script():
    out = ['ShipwreckShoals_EventScript_PlaceGhostShip::  @ gegenereerd door shipwreck_shoals.py']
    for (x, y, m, c) in SHIP_SET:
        out.append('\tsetmetatile %d, %d, 0x%03X, %s' % (x, y, m, 'TRUE' if c else 'FALSE'))
    out.append('\treturn')
    return '\n'.join(out) + '\n'


sp = 'data/maps/ShipwreckShoals/scripts.inc'
s = open(sp).read()
begin, end = '@ --- schip (gegenereerd) ---\n', '@ --- einde schip ---\n'
s = s[:s.index(begin) + len(begin)] + ship_script() + s[s.index(end):]
open(sp, 'w').write(s)

# ---------------------------------------------------------------- spookschip binnen (kopieen)
INTERIOR = {'GhostShip_Deck': 'AbandonedShip_Deck', 'GhostShip_Corridors': 'AbandonedShip_Corridors_1F',
            'GhostShip_Cabins': 'AbandonedShip_Rooms_1F', 'GhostShip_CaptainsOffice': 'AbandonedShip_CaptainsOffice'}
for dst, src in INTERIOR.items():
    os.makedirs('data/layouts/' + dst, exist_ok=True)
    shutil.copy('data/layouts/%s/border.bin' % src, 'data/layouts/%s/border.bin' % dst)
    shutil.copy('data/layouts/%s/map.bin' % src, 'data/layouts/%s/map.bin' % dst)
cor = bytearray(open('data/layouts/GhostShip_Corridors/map.bin', 'rb').read())


def cset(x, y, v):
    struct.pack_into('<H', cor, (y * 18 + x) * 2, v)


cset(5, 2, 0x203 | (3 << 12)); cset(16, 2, 0x203 | (3 << 12))      # trap naar B1F: vloer
cset(3, 3, 0x21b | (1 << 10)); cset(3, 8, 0x624 | (1 << 10)); cset(3, 9, 0x62c | (1 << 10))  # deuren naar Rooms2_1F: wand
open('data/layouts/GhostShip_Corridors/map.bin', 'wb').write(cor)

# ---------------------------------------------------------------- registratie
LAYOUTS = [('LAYOUT_SHIPWRECK_SHOALS', 'ShipwreckShoals', W, H, 'gTileset_ShipwreckShoals')]
ref = {l['id']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'id' in l}
IDS = {'GhostShip_Deck': ('LAYOUT_GHOST_SHIP_DECK', 'LAYOUT_ABANDONED_SHIP_DECK'),
       'GhostShip_Corridors': ('LAYOUT_GHOST_SHIP_CORRIDORS', 'LAYOUT_ABANDONED_SHIP_CORRIDORS_1F'),
       'GhostShip_Cabins': ('LAYOUT_GHOST_SHIP_CABINS', 'LAYOUT_ABANDONED_SHIP_ROOMS_1F'),
       'GhostShip_CaptainsOffice': ('LAYOUT_GHOST_SHIP_CAPTAINS_OFFICE', 'LAYOUT_ABANDONED_SHIP_CAPTAINS_OFFICE')}
for dst in INTERIOR:
    lid, rid = IDS[dst]
    r = ref[rid]
    LAYOUTS.append((lid, dst, r['width'], r['height'], r['secondary_tileset']))
lj = open('data/layouts/layouts.json').read()
for lid, d, w, h, sec in LAYOUTS:
    if '"%s"' % lid in lj:
        continue
    entry = ('    },\n    {\n      "id": "%s",\n      "name": "%s_Layout",\n      "width": %d,\n      "height": %d,\n'
             '      "primary_tileset": "gTileset_General",\n      "secondary_tileset": "%s",\n'
             '      "border_filepath": "data/layouts/%s/border.bin",\n      "blockdata_filepath": "data/layouts/%s/map.bin"\n'
             '    }\n  ]\n}' % (lid, d, w, h, sec, d, d))
    i = lj.rstrip().rindex('    }\n  ]\n}')
    lj = lj[:i] + entry + '\n'
open('data/layouts/layouts.json', 'w').write(lj)
json.load(open('data/layouts/layouts.json'))

MAPS = ['ShipwreckShoals'] + list(INTERIOR)
mg = open('data/maps/map_groups.json').read()
for m in MAPS:
    if '"%s"' % m not in mg:
        i = mg.index('"gMapGroup_Grounded": [')
        j = mg.index(']', i)
        k = mg.rindex('"', i, j) + 1
        mg = mg[:k] + ',\n    "%s"' % m + mg[k:]
open('data/maps/map_groups.json', 'w').write(mg)
grp = json.load(open('data/maps/map_groups.json'))['gMapGroup_Grounded']
assert len(grp) <= 128, len(grp)
es = open('data/event_scripts.s').read()
for m in MAPS:
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % m
    if inc not in es:
        anchor = '\t.include "data/maps/MangroveMire/scripts.inc"\n'
        es = es.replace(anchor, anchor + inc, 1)
open('data/event_scripts.s', 'w').write(es)
r131 = open('data/maps/Route131/map.json').read()
if 'MAP_SHIPWRECK_SHOALS' not in r131:
    r131 = r131.replace('"connections": [\n', '"connections": [\n    {\n      "map": "MAP_SHIPWRECK_SHOALS",\n'
                        '      "offset": 18,\n      "direction": "down"\n    },\n', 1)
    open('data/maps/Route131/map.json', 'w').write(r131)
assert any(c['map'] == 'MAP_SHIPWRECK_SHOALS' for c in json.load(open('data/maps/Route131/map.json'))['connections'])

# ---------------------------------------------------------------- bereikbaarheid
def walk_ok(x, y):
    return 0 <= x < W and 0 <= y < H and not COLL[y][x]


blocked = {(o['x'], o['y']) for o in MAPJ['object_events']}
seen = set()
dq = deque((x, 0) for x in range(W) if not COLL[0][x])
seen |= set(dq)
while dq:
    x, y = dq.popleft()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        n = (x + dx, y + dy)
        if n not in seen and walk_ok(*n) and n not in blocked:
            seen.add(n)
            dq.append(n)
bad = []
for o in MAPJ['object_events']:
    if not any((o['x'] + dx, o['y'] + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        bad.append(('object', o['script'], o['x'], o['y']))
for b in MAPJ['bg_events']:
    pos = (b['x'], b['y'])
    ok = pos in seen if not COLL[b['y']][b['x']] else False
    if b['type'] != 'hidden_item':
        ok = any((b['x'] + dx, b['y'] + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    if not ok:
        bad.append(('bg', b.get('script', b.get('item')), b['x'], b['y']))
door = (SHIP_X + 2, SHIP_Y + 3)
if (door[0], door[1] + 1) not in seen or beh(M[door[1] + 1][door[0]]) not in SURF:
    bad.append(('schipingang', door))
for w in MAPJ['warp_events']:
    if (w['x'], w['y']) != door:
        bad.append(('warp niet op de deur', w['x'], w['y']))
if bad:
    raise SystemExit('niet bereikbaar: %s' % bad)
print('bereikbaar: %d vakken; alle events en de schipingang ok' % len(seen))

if len(sys.argv) > 1:
    from gridrender import render
    grid = [row[:] for row in M]
    for (x, y, m, c) in SHIP_SET:
        grid[y][x] = m
    img = render(grid, 'general', 'shipwreck_shoals', 1)
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    for (ex, ey) in EVENTS:
        d.rectangle([ex * 16 + 3, ey * 16 + 3, ex * 16 + 12, ey * 16 + 12], outline=(255, 0, 0))
    img.save(sys.argv[1])
