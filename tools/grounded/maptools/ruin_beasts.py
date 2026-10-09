"""Project Grounded: de vier Beasts of Ruin, elk verzegeld in een schrijn (post-game).
- Vier kleine tilesets (data/tilesets/secondary/ruin_{fire,earth,moss,ice}) uit Ekat99's Volcano Set
  (graphics/grounded/tilesets/ekat99_lava_rotsen.png, 16x16-raster), per thema getint; primary = SnowTownBase
  (zoals de Regigigas-tempel), emit() uit snow_tileset.py.
- Kaarten (gMapGroup_Grounded):
  JaggedPass_RuinChamber  kamer met inscriptie, ingang = grotopening bovenin Jagged Pass (11,6), leidt naar
  JaggedPass_RuinCaldera  lavaveld met Chi-Yu (beads)
  DesertUnderpass_RuinShrine  Ting-Lu (vessels), opening in de zuidwand van de Desert Underpass (61,13)
  PetalburgWoods_RuinShrine   Wo-Chien (tablets), verborgen boomgat (zoals naar Toadstool Hollow) in de zuidoosthoek van Petalburg Woods (43,36)
  Route135_RuinShrine         Chien-Pao (sword), grot in de klif van Route 135 (51,21)
- Mechaniek: aanspreken zet de zegelvlag (FLAG_RUIN_SEAL_*); na de Hall of Fame breken de zegels pas als alle
  vier de schrijnen bezocht zijn (bezoeken vóór de HoF tellen mee). Dan lv 70, MUS_RG_VS_LEGEND (placeholder).
Idempotent (outdoor-kaarten worden alleen gewijzigd als ze nog de oude tegels hebben).
Gebruik: python3 tools/grounded/maptools/ruin_beasts.py"""
import json, os, random, struct
from collections import deque
import numpy as np
from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)
src = open('tools/grounded/snow_tileset.py').read()
ns = {'np': np, 'Image': Image, 'struct': struct, 'os': os, 'LAYER_COVERED': 1}
exec(src[src.index('def to5('):src.rindex('\nif TOWN:')], ns)
emit = ns['emit']

SHEET = np.array(Image.open('graphics/grounded/tilesets/ekat99_lava_rotsen.png').convert('RGBA')).astype(float)
SOUTH, NORTH = 0x65, 0x64


def tint(theme):
    a = SHEET.copy(); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    if theme == 'earth':
        a[..., 0], a[..., 1], a[..., 2] = r * 1.05 + 14, g * 1.0 + 8, b * 0.72
    elif theme == 'moss':
        a[..., 0], a[..., 1], a[..., 2] = r * 0.80, g * 0.95 + 14, b * 0.70 + 2
    elif theme == 'ice':
        L = 0.3 * r + 0.59 * g + 0.11 * b
        a[..., 0], a[..., 1], a[..., 2] = L * 0.80 + 26, L * 0.95 + 40, L * 1.05 + 66
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


FLOORS = [(6, 18), (7, 18), (6, 19), (7, 19), (1, 3)]
LAVA = [(0, 18), (1, 18), (2, 18)]
POOL = {'NW': (3, 14), 'N': (5, 13), 'NE': (7, 14), 'W': (3, 15), 'E': (7, 15), 'S': (5, 17)}


class Map:
    def __init__(s, W, H, seed):
        s.W, s.H = W, H
        s.rnd = random.Random(seed)
        s.floor = set(); s.lava = set(); s.cell = {}; s.block = set(); s.beh = {}
        s.fv = {(x, y): s.rnd.choice((0, 0, 1, 1, 2, 3, 4)) for x in range(W) for y in range(H)}

    def rect(s, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.floor.add((x, y))

    def pool(s, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                k = 'N' if y == y0 else None
                if x == x0: k = 'NW' if y == y0 else 'W'
                elif x == x1: k = 'NE' if y == y0 else 'E'
                s.cell[(x, y)] = ('c', POOL[k] if k else LAVA[(x + y) % 3], 0)
                s.block.add((x, y)); s.lava.add((x, y))
        for x in range(x0, x1 + 1):
            if (x, y1 + 1) in s.floor and (x, y1 + 1) not in s.lava:
                s.cell[(x, y1 + 1)] = ('c', POOL['S'], 0)

    def bridge(s, x, y0, y1):
        for y in range(y0, y1 + 1):
            s.cell[(x, y)] = ('c', (1, 24 + (y % 2)), 0); s.block.discard((x, y)); s.lava.discard((x, y))

    def stake(s, x, y):  # rotspilaar van 1x2 als zegelstaak
        s.cell[(x, y)] = ('o', (4, 6)); s.cell[(x, y + 1)] = ('o', (4, 7)); s.block |= {(x, y), (x, y + 1)}

    def exit(s, x, y, beh):
        s.floor.add((x, y)); s.beh[(x, y)] = beh

    def decor(s, n, cells, avoid, blocking=False, opaque=False):
        free = [p for p in sorted(s.floor) if p not in s.cell and p not in avoid and p not in s.beh
                and 1 <= p[1] < s.H - 1]
        for p in s.rnd.sample(free, min(n, len(free))):
            c = s.rnd.choice(cells)
            s.cell[p] = ('c', c, 0) if opaque else ('o', c)
            if blocking: s.block.add(p)

    def keys(s):
        """grid van metatile-sleutels + botsing"""
        F = s.floor
        out = []
        for y in range(s.H):
            row = []
            for x in range(s.W):
                p = (x, y); fv = s.fv[p]
                if p in s.cell:
                    k = s.cell[p]
                    k = ('o', k[1], fv) if k[0] == 'o' else k
                    row.append((k, p in s.block)); continue
                if p in F:
                    row.append((('x', fv, s.beh[p]) if p in s.beh else ('f', fv), False)); continue
                if (x, y + 1) in F: c = (x % 2, 8)
                elif (x + 1, y) in F: c = (0, 3)
                elif (x - 1, y) in F: c = (2, 3)
                elif (x, y - 1) in F: c = (x % 2, 9)
                else: c = (x % 2, 6 + (y % 2))
                row.append((('c', c, 0), True))
            out.append(row)
        return out

    def reach(s, start):
        seen = {start}; q = deque([start])
        while q:
            x, y = q.popleft()
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + d[0], y + d[1])
                if n in s.floor and n not in s.block and n not in seen:
                    seen.add(n); q.append(n)
        return seen


def shrine(seed, north_exit=False):
    """13x11: zaal x 2-10 / y 2-8, gang naar de uitgang onderin (6,10), beest op (6,3), vier staken."""
    m = Map(13, 11, seed)
    m.rect(2, 2, 10, 8); m.rect(6, 9, 6, 9); m.exit(6, 10, SOUTH)
    if north_exit:
        m.rect(6, 1, 6, 1); m.exit(6, 0, NORTH)
    for (x, y) in ((3, 2), (9, 2), (3, 6), (9, 6)):
        m.stake(x, y)
    return m


def caldera(seed):
    """20x18: lavaband met brug, twee lavapoelen naast het altaar, Chi-Yu bovenin (9,4)."""
    m = Map(20, 18, seed)
    m.rect(2, 2, 17, 15); m.rect(9, 16, 9, 16); m.exit(9, 17, SOUTH)
    m.pool(2, 9, 17, 11); m.bridge(9, 9, 11)
    m.pool(3, 3, 5, 6); m.pool(14, 3, 16, 6)
    for (x, y) in ((7, 3), (11, 3), (7, 6), (11, 6)):
        m.stake(x, y)
    return m


AVOID_SHRINE = {(x, y) for x in range(5, 8) for y in range(2, 11)} | {(4, 8), (8, 8), (3, 8), (9, 8)}
MAPS = {}
# kamer bovenin Jagged Pass (geen beest): lavavlekken
m = shrine(531, north_exit=True); m.decor(7, [(4, 1), (5, 1), (6, 1), (7, 1)], AVOID_SHRINE | {(6, 2), (6, 1)}, opaque=True)
MAPS['JaggedPass_RuinChamber'] = ('fire', m)
m = caldera(532); m.decor(12, [(4, 1), (5, 1), (6, 1), (7, 1)], {(9, y) for y in range(2, 18)} | {(8, 4), (10, 4), (9, 5)}, opaque=True)
MAPS['JaggedPass_RuinCaldera'] = ('fire', m)
m = shrine(533); m.decor(4, [(1, 1), (3, 1)], AVOID_SHRINE); m.decor(2, [(2, 1)], AVOID_SHRINE, blocking=True)
MAPS['DesertUnderpass_RuinShrine'] = ('earth', m)
m = shrine(534); m.decor(5, [(1, 1)], AVOID_SHRINE); m.decor(4, [(0, 1)], AVOID_SHRINE, blocking=True)
MAPS['PetalburgWoods_RuinShrine'] = ('moss', m)
m = shrine(535); m.decor(4, [(2, 1)], AVOID_SHRINE, blocking=True); m.decor(3, [(3, 1)], AVOID_SHRINE)
MAPS['Route135_RuinShrine'] = ('ice', m)

THEMES = {'fire': 'RuinFire', 'earth': 'RuinEarth', 'moss': 'RuinMoss', 'ice': 'RuinIce'}
layouts = {}
for theme, sym in THEMES.items():
    sheet = tint(theme)
    cell = lambda c: sheet.crop((c[0] * 16, c[1] * 16, c[0] * 16 + 16, c[1] * 16 + 16))
    floor = lambda i: cell(FLOORS[i])
    used = []
    grids = {}
    for name, (th, m) in MAPS.items():
        if th != theme: continue
        g = m.keys(); grids[name] = g
        for row in g:
            for k, _ in row:
                if k not in used: used.append(k)
    used.insert(0, ('c', (0, 6), 0))  # randtegel
    mts = []
    for k in dict.fromkeys(used):
        if k[0] == 'f':
            mts.append((k, floor(k[1]), None, 0))
        elif k[0] == 'x':
            mts.append((k, floor(k[1]), None, k[2]))
        elif k[0] == 'c':
            b = floor(k[2]).copy(); b.alpha_composite(cell(k[1])); mts.append((k, b, None, 0))
        elif k[0] == 'o':
            mts.append((k, floor(k[2]), cell(k[1]), 0))
    res = emit(mts, 'data/tilesets/secondary/ruin_' + theme, 512, 6, 7)
    ids = res['names']
    for name, g in grids.items():
        m = MAPS[name][1]
        os.makedirs('data/layouts/' + name, exist_ok=True)
        data = b''.join(struct.pack('<H', ids[k] | ((1 if bl else 0) << 10) | (3 << 12)) for row in g for k, bl in row)
        open('data/layouts/%s/map.bin' % name, 'wb').write(data)
        open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *([ids[('c', (0, 6), 0)] | (1 << 10) | (3 << 12)] * 4)))
        layouts[name] = (m.W, m.H, sym)

# ---------------------------------------------------------------- bereikbaarheid
for name, (th, m) in MAPS.items():
    starts = [p for p, b in m.beh.items()]
    r = m.reach(starts[0])
    assert all(p in r for p in starts), name + ': uitgangen niet verbonden'
    if name != 'JaggedPass_RuinChamber':
        bx, by = (9, 4) if 'Caldera' in name else (6, 3)
        assert (bx, by + 1) in r, name + ': beest niet bereikbaar'
print('bereikbaarheid ok')

# ---------------------------------------------------------------- tileset-registratie
gh = open('src/data/tilesets/graphics.h').read()
mh = open('src/data/tilesets/metatiles.h').read()
hh = open('src/data/tilesets/headers.h').read()
for theme, sym in THEMES.items():
    d = 'data/tilesets/secondary/ruin_' + theme
    if 'gTilesetTiles_%s[]' % sym not in gh:
        gh += ('\n// Project Grounded: Beasts of Ruin (%s; Volcano Set van Ekat99, ruin_beasts.py)\n'
               'const u32 gTilesetTiles_%s[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n\n'
               'const u16 gTilesetPalettes_%s[][16] =\n{\n' % (theme, sym, d, sym)
               + ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (d, i) for i in range(16)) + '};\n')
    if 'gMetatiles_%s[]' % sym not in mh:
        mh += ('\nconst u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin"); // Project Grounded: Beasts of Ruin\n'
               'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % (sym, d, sym, d))
    if 'gTileset_%s =' % sym not in hh:
        hh += ('\nconst struct Tileset gTileset_%s = // Project Grounded: Beasts of Ruin (%s)\n{\n'
               '    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_%s,\n'
               '    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n'
               '    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = NULL,\n};\n' % (sym, theme, sym, sym, sym, sym))
open('src/data/tilesets/graphics.h', 'w').write(gh)
open('src/data/tilesets/metatiles.h', 'w').write(mh)
open('src/data/tilesets/headers.h', 'w').write(hh)


def const(name):
    import re
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper()


lj = open('data/layouts/layouts.json').read()
anchor = lj.index('"id": "LAYOUT_REGIGIGAS_TEMPLE_SEALED"'); j = lj.index('},', anchor) + 2
add = ''
for name, (W, H, sym) in layouts.items():
    if '"LAYOUT_%s"' % const(name) in lj: continue
    add += ('\n    {\n      "id": "LAYOUT_%s",\n      "name": "%s_Layout",\n      "width": %d,\n      "height": %d,\n'
            '      "primary_tileset": "gTileset_SnowTownBase",\n      "secondary_tileset": "gTileset_%s",\n'
            '      "border_filepath": "data/layouts/%s/border.bin",\n      "blockdata_filepath": "data/layouts/%s/map.bin"\n    },'
            % (const(name), name, W, H, sym, name, name))
if add:
    open('data/layouts/layouts.json', 'w').write(lj[:j] + add + lj[j:])

# ---------------------------------------------------------------- buitenkaarten: openingen + warps
def lay(name):
    L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('name') == name + '_Layout'][0]
    W = L['width']; p = L['blockdata_filepath']
    v = list(struct.unpack('<%dH' % (W * L['height']), open(p, 'rb').read()))
    return W, p, v

# (buitenkaart, layout, [(x, y, bron-x, bron-y)], warp (x, y), schrijn)
OUTDOOR = [
    ('JaggedPass', [(11, 5, 16, 5), (11, 6, 16, 6)], (11, 6), 'JaggedPass_RuinChamber'),
    ('DesertUnderpass', [(61, 13, 10, 12), (60, 14, 9, 13), (61, 14, 10, 13), (62, 14, 11, 13)], (61, 13), 'DesertUnderpass_RuinShrine'),
    ('PetalburgWoods', [(42, 35, 46, 9), (43, 35, 47, 9), (42, 36, 46, 10), (43, 36, 47, 10)], (43, 36), 'PetalburgWoods_RuinShrine'),
    ('Route135', [(50 + dx, 20 + dy, 5 + dx, 10 + dy) for dy in (0, 1) for dx in range(3)], (51, 21), 'Route135_RuinShrine'),
]
back = {}
for mapname, tiles, (wx, wy), dst in OUTDOOR:
    mj = json.load(open('data/maps/%s/map.json' % mapname))
    W, p, v = lay(mapname)
    for x, y, sx, sy in tiles:
        v[y * W + x] = v[sy * W + sx]
    open(p, 'wb').write(struct.pack('<%dH' % len(v), *v))
    if not any(w['dest_map'] == 'MAP_' + const(dst) for w in mj['warp_events']):
        mj['warp_events'].append({'x': wx, 'y': wy, 'elevation': 0, 'dest_map': 'MAP_' + const(dst), 'dest_warp_id': '0'})
        open('data/maps/%s/map.json' % mapname, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')
    back[dst] = ('MAP_' + const(mapname), [i for i, w in enumerate(mj['warp_events']) if w['dest_map'] == 'MAP_' + const(dst)][0])

# ---------------------------------------------------------------- kaarten
BEASTS = {  # kaart: (soort, gfx, vlag-suffix, beest-x, beest-y, mapsec)
    'JaggedPass_RuinCaldera': ('CHI_YU', 'CHI_YU', 9, 4, 'MAPSEC_JAGGED_PASS'),
    'DesertUnderpass_RuinShrine': ('TING_LU', 'TING_LU', 6, 3, 'MAPSEC_DESERT_UNDERPASS'),
    'PetalburgWoods_RuinShrine': ('WO_CHIEN', 'WO_CHIEN', 6, 3, 'MAPSEC_PETALBURG_WOODS'),
    'Route135_RuinShrine': ('CHIEN_PAO', 'CHIEN_PAO', 6, 3, 'MAPSEC_ROUTE_135'),
}
base = json.load(open('data/maps/RegigigasTemple/map.json'))
for name, (th, m) in MAPS.items():
    mj = {k: base[k] for k in base}
    mj.update({'id': 'MAP_' + const(name), 'name': name, 'layout': 'LAYOUT_' + const(name), 'music': 'MUS_SEALED_CHAMBER',
               'map_type': 'MAP_TYPE_UNDERGROUND', 'show_map_name': False,
               'region_map_section': BEASTS[name][4] if name in BEASTS else 'MAPSEC_JAGGED_PASS'})
    mj['object_events'] = []; mj['coord_events'] = []; mj['bg_events'] = []
    if name in BEASTS:
        sp, gfx, bx, by, _ = BEASTS[name]
        mj['object_events'].append({'local_id': 'LOCALID_RUIN_' + sp, 'graphics_id': 'OBJ_EVENT_GFX_SPECIES(%s)' % gfx,
                                    'x': bx, 'y': by, 'elevation': 3, 'movement_type': 'MOVEMENT_TYPE_FACE_DOWN',
                                    'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE',
                                    'trainer_sight_or_berry_tree_id': '0', 'script': 'RuinBeasts_EventScript_' + sp,
                                    'flag': 'FLAG_HIDE_RUIN_' + sp})
    # inscriptie op de linkeronderstaak (onderste tegel), te lezen van rechts (4,7)
    sx, sy = (7, 7) if 'Caldera' in name else (3, 7)
    mj['bg_events'].append({'type': 'sign', 'x': sx, 'y': sy, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
                            'script': name + '_EventScript_Stake'})
    ex = [p for p, b in m.beh.items() if b == SOUTH][0]
    if name == 'JaggedPass_RuinCaldera':
        warps = [{'x': ex[0], 'y': ex[1], 'elevation': 0, 'dest_map': 'MAP_JAGGED_PASS_RUIN_CHAMBER', 'dest_warp_id': '1'}]
    else:
        dm, di = back[name]
        warps = [{'x': ex[0], 'y': ex[1], 'elevation': 0, 'dest_map': dm, 'dest_warp_id': str(di)}]
        if name == 'JaggedPass_RuinChamber':
            nx = [p for p, b in m.beh.items() if b == NORTH][0]
            warps.append({'x': nx[0], 'y': nx[1], 'elevation': 0, 'dest_map': 'MAP_JAGGED_PASS_RUIN_CALDERA', 'dest_warp_id': '0'})
    mj['warp_events'] = warps
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')

g = open('data/maps/map_groups.json').read()
for name in MAPS:
    if '"%s"' % name not in g:
        i = g.index('"gMapGroup_Grounded": ['); j = g.index('\n  ]', i)
        g = g[:j] + ',\n    "%s"' % name + g[j:]
open('data/maps/map_groups.json', 'w').write(g)
es = open('data/event_scripts.s').read()
for name in MAPS:
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        es = es.replace('\t.include "data/maps/Route126_SilentCrater/scripts.inc"\n',
                        '\t.include "data/maps/Route126_SilentCrater/scripts.inc"\n' + inc, 1)
open('data/event_scripts.s', 'w').write(es)
print('klaar')
