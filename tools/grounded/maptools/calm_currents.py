"""Project Grounded: zeestroming op Route 132-134 minder straffend (Jordi: "erg frustrerend"). Deterministisch en
idempotent.

Vanilla heeft één grote westwaartse stroom (±1200 tegels per route) met noord/zuid-wervels: wie oost wil, wordt
steeds teruggeduwd. Nu:
  - alle noord-, zuid- en oostwaartse stroomtegels worden rustig water (geen wervels die je de rotsen in duwen);
  - van de westwaartse stroom blijven alleen korte stroomgeulen over: banden van 2 rijen hoog (elke 6 rijen),
    elk opgeknipt in stukken van 6 tegels met 6 rustige tegels ertussen (per band verspringend). Een geul duwt je
    hoogstens 6 tegels naar het westen; daaromheen ligt overal rustig water, dus een rustige omweg is er altijd.
  - het script controleert met een simulatie van de stroming (glijden tot een niet-stroomtegel of een obstakel) dat
    vanaf elke ingang alle trainers, items, borden, verborgen items en uitgangen bereikbaar zijn, in beide
    richtingen.
Rustig water = General 0x170 (oceaan, zelfde als de rest van de zee), met de elevation/collision van de oude tegel.
Route132_LowTide (eb, tides_juan.py) krijgt dezelfde behandeling.

Gebruik: python3 tools/grounded/maptools/calm_currents.py"""
import json, os, struct, sys
from collections import deque

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))

CALM = 0x170
BAND_PERIOD, BAND_ROWS = 6, 2
SEG_PERIOD, SEG_LEN = 12, 6


def attrs(p):
    d = open(p, 'rb').read()
    return struct.unpack('<%dH' % (len(d) // 2), d)


PRIM = attrs('data/tilesets/primary/general/metatile_attributes.bin')
SEC = attrs('data/tilesets/secondary/pacifidlog/metatile_attributes.bin')
DIRS = {0x50: (1, 0), 0x51: (-1, 0), 0x52: (0, -1), 0x53: (0, 1)}


def beh(v):
    m = v & 0x3ff
    a = PRIM[m] if m < 0x200 else SEC[m - 0x200]
    return a & 0xff


def keep(x, y):
    if y % BAND_PERIOD >= BAND_ROWS:
        return False
    band = y // BAND_PERIOD
    return (x + band * 5) % SEG_PERIOD < SEG_LEN


OPENINGS = {
    # Route 133, noordrand: de verbinding met de drijvende markt (x 16-51) lag achter een rij zeerotsen; twee
    # rotsen (2x2) weg geeft een vaargeul op x 28-31 (de markt is daar onderaan open water).
    'Route133_Layout': [(x, y) for x in range(28, 32) for y in range(0, 2)],
}


def transform(grid, w, h, name=None):
    out = list(grid)
    for x, y in OPENINGS.get(name, ()):
        out[y * w + x] = CALM | (1 << 12)
    for y in range(h):
        for x in range(w):
            v = grid[y * w + x]
            b = beh(v)
            if b not in DIRS:
                continue
            if b == 0x51 and keep(x, y):
                continue
            out[y * w + x] = CALM | (v & ~0x3ff)
    return out


def reach(grid, w, h, blocked, starts):
    """Bereikbare tegels met stroming: op een stroomtegel glijd je door tot het niet verder kan."""
    def free(x, y):
        return 0 <= x < w and 0 <= y < h and (grid[y * w + x] >> 10) & 3 == 0 and (x, y) not in blocked

    def slide(x, y):
        seen = set()
        while True:
            d = DIRS.get(beh(grid[y * w + x]))
            if not d or (x, y) in seen:
                return x, y
            seen.add((x, y))
            nx, ny = x + d[0], y + d[1]
            if not free(nx, ny):
                return x, y          # tegen een obstakel: je kunt weer zelf sturen
            x, y = nx, ny

    seen, q = set(), deque()
    for s in starts:
        if free(*s):
            p = slide(*s)
            if p not in seen:
                seen.add(p)
                q.append(p)
    while q:
        x, y = q.popleft()
        d = DIRS.get(beh(grid[y * w + x]))
        if d and free(x + d[0], y + d[1]):
            continue                 # nog in beweging (komt niet voor na slide)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if free(nx, ny):
                p = slide(nx, ny)
                if p not in seen:
                    seen.add(p)
                    q.append(p)
    return seen


def edge_cells(grid, w, h, mp):
    m = json.load(open('data/maps/%s/map.json' % mp))
    cells = {}
    for c in m['connections'] or []:
        d = c['direction']
        if d == 'left':
            cells[c['map']] = [(0, y) for y in range(h)]
        elif d == 'right':
            cells[c['map']] = [(w - 1, y) for y in range(h)]
        elif d == 'up':
            cells[c['map']] = [(x, 0) for x in range(max(0, c['offset']), w)]
        elif d == 'down':
            cells[c['map']] = [(x, h - 1) for x in range(max(0, c['offset']), w)]
    return m, cells


def check(mp, grid, w, h):
    m, edges = edge_cells(grid, w, h, mp)
    blocked = {(o['x'], o['y']) for o in m['object_events']}
    targets = [('obj ' + o['script'], o['x'], o['y']) for o in m['object_events']]
    targets += [('bg ' + b['type'], b['x'], b['y']) for b in m['bg_events']]

    def free(x, y):
        return 0 <= x < w and 0 <= y < h and (grid[y * w + x] >> 10) & 3 == 0 and (x, y) not in blocked
    for name, cells in edges.items():
        r = reach(grid, w, h, blocked, [c for c in cells if free(*c)])
        for t, x, y in targets:
            if t.startswith('bg hidden'):
                ok = (x, y) in r
            else:
                ok = any((x + dx, y + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            assert ok, (mp, 'vanaf', name, 'onbereikbaar', t, x, y)
        for other, oc in edges.items():
            assert any(c in r for c in oc), (mp, 'vanaf', name, 'geen weg naar', other)


def run(layout_name, mapname):
    L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('name') == layout_name][0]
    w, h, p = L['width'], L['height'], L['blockdata_filepath']
    grid = struct.unpack('<%dH' % (w * h), open(p, 'rb').read())
    new = transform(grid, w, h, layout_name)
    check(mapname, new, w, h)
    before = sum(1 for v in grid if beh(v) in DIRS)
    after = sum(1 for v in new if beh(v) in DIRS)
    open(p, 'wb').write(struct.pack('<%dH' % (w * h), *new))
    print('%s: stroomtegels %d -> %d' % (layout_name, before, after))


if __name__ == '__main__':
    for lay, mp in (('Route132_Layout', 'Route132'), ('Route132_LowTide_Layout', 'Route132'),
                    ('Route133_Layout', 'Route133'), ('Route134_Layout', 'Route134')):
        run(lay, mp)
