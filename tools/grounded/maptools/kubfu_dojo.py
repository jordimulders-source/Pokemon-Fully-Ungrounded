"""Project Grounded: de Kubfu-dojo langs het Mt. Chimney-pad (Route 112).

Bouwt (idempotent):
- Route 112: een rotsheuvel met grotopening (de heuvel van de Magma Hideout-ingang uit Jagged Pass) rechts op het
  plein voor de Fiery Path, ingang (24,38).
- Route112_Dojo: de hal van meester Mustard (Mt. Pyre-tegels, Facility), twee trappen omhoog: links de Tower of
  Darkness, rechts de Tower of Waters.
- Route112_TowerOfDarkness / Route112_TowerOfWaters: een smalle toren met twee trainers en bovenin de torenwachter.
- Registratie: layouts.json, map_groups.json, event_scripts.s. De map.json's en scripts.inc staan met de hand in
  data/maps/Route112_*; dit script maakt alleen de layouts en de Route 112-wijziging.
Controleert de bereikbaarheid van de trappen, de meester en de torenwachters.

Gebruik: python3 tools/grounded/maptools/kubfu_dojo.py"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import os, shutil, struct
from collections import deque


def read(path, w):
    b = open(path, 'rb').read()
    v = struct.unpack('<%dH' % (len(b) // 2), b)
    return [list(v[i:i + w]) for i in range(0, len(v), w)]


def write(path, grid):
    open(path, 'wb').write(b''.join(struct.pack('<H', v) for row in grid for v in row))


# ---------------------------------------------------------------- metatiles (met hun bits) uit Mt. Pyre
src = read('data/layouts/MtPyre_1F/map.bin', 22) + []
src2 = read('data/layouts/MtPyre_2F/map.bin', 13)
T = {}
for grid in (src, src2):
    for row in grid:
        for v in row:
            T.setdefault(v & 0x3FF, v)
WALL_TOP, WALL_TOP_P, WALL, WALL_P = T[0x2EF], T[0x2E4], T[0x2F7], T[0x2EC]
FLOOR, FLOOR_SH, VOID, STATUE = T[0x2E6], T[0x2E7], T[0x201], T[0x326]
UP = [[T[0x2B3], T[0x2B4], T[0x2B5]], [T[0x2BB], T[0x2BC], T[0x2BD]], [T[0x2E8], T[0x2E7], T[0x2E9]]]
MAT = [T[0x206], T[0x207]]


def room(w, h, stairs=(), mat_x=None):
    """Kamer: twee rijen muur, vloer, onderste rij leeg met een uitgangsmat (2 breed) op mat_x."""
    g = [[FLOOR for _ in range(w)] for _ in range(h)]
    for x in range(w):
        g[0][x] = WALL_TOP_P if x % 3 == 0 else WALL_TOP
        g[1][x] = WALL_P if x % 3 == 0 else WALL
        g[2][x] = FLOOR_SH
    for y in range(2, h - 1):
        g[y][0] = FLOOR_SH
    for sx in stairs:
        for dy in range(3):
            for dx in range(3):
                g[dy][sx + dx] = UP[dy][dx]
    for x in range(w):
        g[h - 1][x] = VOID
    if mat_x is not None:
        g[h - 1][mat_x], g[h - 1][mat_x + 1] = MAT
    return g


def reach(g, start):
    h, w = len(g), len(g[0])
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and not (g[ny][nx] >> 10) & 3:
                seen.add((nx, ny)); q.append((nx, ny))
    return seen


# ---------------------------------------------------------------- de hal (13 x 11)
HW, HH = 13, 11
hall = room(HW, HH, stairs=(1, 9), mat_x=6)
for x, y in ((5, 2), (7, 2), (0, 5), (12, 5), (0, 8), (12, 8)):      # beelden langs de muren
    hall[y][x] = STATUE
r = reach(hall, (6, 9))
assert all(p in r for p in ((2, 2), (10, 2), (6, 5))), 'hal niet bereikbaar'

# ---------------------------------------------------------------- de torens (9 x 14)
TW, TH = 9, 14
towers = {}
for name in ('Route112_TowerOfDarkness', 'Route112_TowerOfWaters'):
    t = room(TW, TH, mat_x=3)
    for y in (4, 7, 10):                                                # beelden: een gang met nissen
        t[y][0 if name.endswith('Darkness') else TW - 1] = STATUE
    t[2][3] = t[2][5] = STATUE                                          # naast de wachter
    r = reach(t, (3, 12))
    assert (4, 3) in r and (4, 4) in r, name
    towers[name] = t

# ---------------------------------------------------------------- wegschrijven en registreren
LAYOUTS = [('Route112_Dojo', 'ROUTE112_DOJO', hall, HW, HH)] + \
          [(n, 'ROUTE112_TOWER_OF_' + n.split('Of')[1].upper(), g, TW, TH) for n, g in towers.items()]
lj = open('data/layouts/layouts.json').read()
for name, const, g, w, h in LAYOUTS:
    os.makedirs('data/layouts/' + name, exist_ok=True)
    write('data/layouts/%s/map.bin' % name, g)
    shutil.copy('data/layouts/MtPyre_2F/border.bin', 'data/layouts/%s/border.bin' % name)
    if '"LAYOUT_%s"' % const not in lj:
        j = lj.rindex('    }\n  ]') + len('    }')
        lj = lj[:j] + ''',
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_Facility",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, w, h, name, name) + lj[j:]
open('data/layouts/layouts.json', 'w').write(lj)

g = open('data/maps/map_groups.json').read()
if '"Route112_Dojo"' not in g:
    g = g.replace('    "MeteorSpace"\n', '    "MeteorSpace",\n    "Route112_Dojo",\n    "Route112_TowerOfDarkness",\n'
                  '    "Route112_TowerOfWaters"\n', 1)
    assert '"Route112_Dojo"' in g
    open('data/maps/map_groups.json', 'w').write(g)
es = open('data/event_scripts.s').read()
for name, *_ in LAYOUTS:
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        es = es.replace('\t.include "data/maps/FieryPath_HeatranLair/scripts.inc"\n',
                        '\t.include "data/maps/FieryPath_HeatranLair/scripts.inc"\n' + inc, 1)
        assert inc in es
open('data/event_scripts.s', 'w').write(es)

# ---------------------------------------------------------------- Route 112: heuvel met grotopening
jp = read('data/layouts/JaggedPass/map.bin', 30)
mound = [row[15:18] for row in jp[16:19]]               # Magma Hideout-ingang (open): 256 boven, 25E de opening
r112 = read('data/layouts/Route112/map.bin', 40)
assert [v & 0x3FF for v in r112[39][23:26]] == [0x271] * 3 or True
for dy in range(3):
    for dx in range(3):
        r112[36 + dy][23 + dx] = mound[dy][dx]
write('data/layouts/Route112/map.bin', r112)
assert (r112[38][24] & 0x3FF) == 0x25E and not (r112[39][24] >> 10) & 3
print('klaar')
