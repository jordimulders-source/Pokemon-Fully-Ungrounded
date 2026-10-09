"""Project Grounded: Flower Paradise, het bloemeneiland van Shaymin (post-game, Bloom Ticket via de veerboot in Lilycove).

Bouwt (idempotent, vaste seed):
- Tileset data/tilesets/secondary/flower_paradise: kopie van Fortree plus drie Gracidea-metatiles (roze/witte bloemen
  op gras, palet 6, dat Fortree niet gebruikt). Nieuwe tiles komen in de laatste rij van tiles.png (496-511).
- FlowerParadise_Shore: aanlegsteiger (layout van Southern Island, Rustboro), pad naar het bos.
- FlowerParadise_Meadow: de open plek uit Faraway Island (binnen), het hoge gras wordt een Gracidea-veld; Shaymin in
  het midden.
- Registratie: layouts.json, map_groups.json, event_scripts.s, headers.h/graphics.h/metatiles.h (tileset).
De map.json's en scripts.inc staan met de hand in data/maps/FlowerParadise_*.

Gebruik: python3 tools/grounded/maptools/flower_paradise.py [voorbeeld.png]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import math, os, random, shutil, struct, sys
from PIL import Image

SRC, TS = 'data/tilesets/secondary/fortree', 'data/tilesets/secondary/flower_paradise'
SEED = 492  # nationaal dexnummer van Shaymin

# ---------------------------------------------------------------- tileset
os.makedirs(TS + '/palettes', exist_ok=True)
for f in ('metatiles.bin', 'metatile_attributes.bin'):
    shutil.copy('%s/%s' % (SRC, f), '%s/%s' % (TS, f))
for i in range(16):
    shutil.copy('%s/palettes/%02d.pal' % (SRC, i), '%s/palettes/%02d.pal' % (TS, i))

GPAL = [(0, 0, 0), (31, 20, 26), (29, 11, 20), (21, 5, 13), (31, 31, 31), (26, 24, 28), (31, 27, 8),
        (10, 22, 8), (5, 13, 5)]
GPAL += [(0, 0, 0)] * (16 - len(GPAL))
with open(TS + '/palettes/06.pal', 'w', newline='\r\n') as fp:
    fp.write('JASC-PAL\n0100\n16\n')
    for c in GPAL:
        fp.write('%d %d %d\n' % tuple(v * 8 for v in c))


def flower(px, cx, cy, white, r=3.4):
    """Gracidea: vijf bloemblaadjes rond een geel hart; wit = witte punten met een roze hart."""
    for y in range(16):
        for x in range(16):
            dx, dy = x - cx, y - cy
            d = math.hypot(dx, dy)
            if d > r + 0.5:
                continue
            if d < 0.9:
                px[y][x] = 6
                continue
            a = math.atan2(dy, dx)
            lobe = abs(math.cos(2.5 * (a + 0.4)))
            if d > 1.3 + (r - 1.3) * lobe:
                continue
            if white:
                px[y][x] = 2 if d < 1.7 else (4 if d < r - 0.9 else 5)
            else:
                px[y][x] = 3 if d < 1.4 else (2 if d < r - 1.2 else 1)


def leaf(px, cx, cy, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    for y in range(16):
        for x in range(16):
            if px[y][x]:
                continue
            u = (x - cx) * ca + (y - cy) * sa
            v = -(x - cx) * sa + (y - cy) * ca
            if 0 <= u <= 3.2 and abs(v) <= 1.1 * math.sin(math.pi * u / 3.2) + 0.2:
                px[y][x] = 8 if v > 0.3 else 7


VARIANTS = [
    # (bloemen (x, y, wit), bladeren (x, y, hoek))
    ([(4.5, 4.5, False), (11.5, 10.5, True)], [(6.5, 7.5, 1.0), (9.5, 8.5, 3.6), (2.5, 12.5, 5.0)]),
    ([(10.5, 4.0, False), (4.0, 11.0, False), (12.5, 12.5, True)], [(7.0, 6.5, 2.4), (6.5, 13.5, 0.2)]),
    ([(7.5, 7.5, True), (13.0, 2.5, False)], [(3.5, 10.5, 5.4), (10.5, 12.0, 0.6), (2.0, 3.0, 0.9)]),
]
newtiles, tidx, metas = [], {}, []
for flowers, leaves in VARIANTS:
    px = [[0] * 16 for _ in range(16)]
    for fx, fy, w in flowers:
        flower(px, fx, fy, w)
    for lx, ly, la in leaves:
        leaf(px, lx, ly, la)
    ent = []
    for k in range(4):
        ox, oy = (k % 2) * 8, (k // 2) * 8
        t = tuple(px[oy + y][ox + x] for y in range(8) for x in range(8))
        if t not in tidx:
            tidx[t] = 496 + len(newtiles)
            newtiles.append(t)
        ent.append(0x6000 | (512 + tidx[t]))
    metas.append(ent)
assert len(newtiles) <= 16, len(newtiles)

im = Image.open(SRC + '/tiles.png')
out = Image.new('P', (128, 256), 0)
out.putpalette(im.getpalette())
out.paste(im, (0, 0))
for i, t in enumerate(newtiles):
    n = 496 + i
    ox, oy = (n % 16) * 8, (n // 16) * 8
    for p, v in enumerate(t):
        out.putpixel((ox + p % 8, oy + p // 8), v)
out.save(TS + '/tiles.png')

mts = bytearray(open(SRC + '/metatiles.bin', 'rb').read())
attrs = bytearray(open(SRC + '/metatile_attributes.bin', 'rb').read())
FIRST = 512 + len(mts) // 16                     # eerste Gracidea-metatile
for ent in metas:
    mts += struct.pack('<8H', 0x2002, 0x2003, 0x2003, 0x2002, *ent)   # onder: gras (General 1)
    attrs += struct.pack('<H', 0x1000)                                   # zoals de bloemen van General: covered
open(TS + '/metatiles.bin', 'wb').write(mts)
open(TS + '/metatile_attributes.bin', 'wb').write(attrs)
GRAC = [FIRST + i for i in range(len(metas))]
print('Gracidea-metatiles', [hex(g) for g in GRAC], len(newtiles), 'nieuwe tiles')

# registratie van de tileset
hdr = open('src/data/tilesets/headers.h').read()
if 'gTileset_FlowerParadise' not in hdr:
    hdr += '''
const struct Tileset gTileset_FlowerParadise = // Project Grounded: Flower Paradise (Shaymin), Fortree + Gracidea, flower_paradise.py
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_FlowerParadise,
    .palettes = gTilesetPalettes_FlowerParadise,
    .metatiles = gMetatiles_FlowerParadise,
    .metatileAttributes = gMetatileAttributes_FlowerParadise,
    .callback = InitTilesetAnim_Fortree,
};
'''
    open('src/data/tilesets/headers.h', 'w').write(hdr)
gfx = open('src/data/tilesets/graphics.h').read()
if 'gTilesetTiles_FlowerParadise' not in gfx:
    gfx += '\nconst u32 gTilesetTiles_FlowerParadise[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n\n' % TS
    gfx += 'const u16 gTilesetPalettes_FlowerParadise[][16] =\n{\n'
    gfx += ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (TS, i) for i in range(16)) + '};\n'
    open('src/data/tilesets/graphics.h', 'w').write(gfx)
mh = open('src/data/tilesets/metatiles.h').read()
if 'gMetatiles_FlowerParadise' not in mh:
    mh += '\nconst u16 gMetatiles_FlowerParadise[] = INCBIN_U16("%s/metatiles.bin");\n' % TS
    mh += 'const u16 gMetatileAttributes_FlowerParadise[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % TS
    open('src/data/tilesets/metatiles.h', 'w').write(mh)


# ---------------------------------------------------------------- kaarten
def read(path, w, h):
    return [list(r) for r in zip(*[iter(struct.unpack('<%dH' % (w * h), open(path, 'rb').read()))] * w)]


def write(path, grid):
    open(path, 'wb').write(b''.join(struct.pack('<H', v) for row in grid for v in row))


# kust: Southern Island buiten, ongewijzigd (steiger + pad naar het bos)
os.makedirs('data/layouts/FlowerParadise_Shore', exist_ok=True)
shutil.copy('data/layouts/SouthernIsland_Exterior/map.bin', 'data/layouts/FlowerParadise_Shore/map.bin')
shutil.copy('data/layouts/SouthernIsland_Exterior/border.bin', 'data/layouts/FlowerParadise_Shore/border.bin')

# open plek: het hoge gras (0x15 en Fortree 0x208) en de rotsen (0xE0) worden Gracidea; een grasstrook als pad
W, H = 29, 26
rng = random.Random(SEED)
m = read('data/layouts/FarawayIsland_Interior/map.bin', W, H)
PATH = {(12, 18), (13, 18), (12, 17), (13, 17), (13, 16), (13, 15), (13, 14), (14, 14), (14, 13), (14, 12)}
for y in range(H):
    for x in range(W):
        mid, hi = m[y][x] & 0x3FF, m[y][x] & 0xFC00
        if mid in (0x15, 0x208, 0xE0):
            if (x, y) in PATH:
                m[y][x] = hi | 0x001
            else:
                m[y][x] = hi | rng.choice(GRAC)
            if mid == 0xE0:                     # rots weg: begaanbaar
                m[y][x] &= ~0x0C00
        elif mid == 0x004 and rng.random() < 0.7:   # de rode bloemen van General worden ook Gracidea
            m[y][x] = hi | rng.choice(GRAC)
os.makedirs('data/layouts/FlowerParadise_Meadow', exist_ok=True)
write('data/layouts/FlowerParadise_Meadow/map.bin', m)
shutil.copy('data/layouts/FarawayIsland_Interior/border.bin', 'data/layouts/FlowerParadise_Meadow/border.bin')

lj = open('data/layouts/layouts.json').read()
for name, w, h, sec in (('FlowerParadise_Shore', 33, 30, 'gTileset_Rustboro'),
                        ('FlowerParadise_Meadow', W, H, 'gTileset_FlowerParadise')):
    const = 'LAYOUT_FLOWER_PARADISE_' + name.split('_')[1].upper()
    if '"%s"' % const in lj:
        continue
    i = lj.rindex('    }\n  ]')
    j = i + len('    }')
    lj = lj[:j] + ''',
    {
      "id": "%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, w, h, sec, name, name) + lj[j:]
open('data/layouts/layouts.json', 'w').write(lj)

g = open('data/maps/map_groups.json').read()
if '"FlowerParadise_Shore"' not in g:
    g = g.replace('    "BattleFrontier_StadiumArena"\n', '    "BattleFrontier_StadiumArena",\n    "FlowerParadise_Shore",\n    "FlowerParadise_Meadow"\n', 1)
    assert '"FlowerParadise_Shore"' in g
    open('data/maps/map_groups.json', 'w').write(g)
es = open('data/event_scripts.s').read()
for name in ('FlowerParadise_Shore', 'FlowerParadise_Meadow'):
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        es = es.replace('\t.include "data/maps/FieryPath_HeatranLair/scripts.inc"\n',
                        '\t.include "data/maps/FieryPath_HeatranLair/scripts.inc"\n' + inc, 1)
        assert inc in es
open('data/event_scripts.s', 'w').write(es)

# bereikbaarheid op de open plek: van de ingang (12,18) naar Shaymin (13,10)
from collections import deque
seen, q = {(12, 18)}, deque([(12, 18)])
while q:
    x, y = q.popleft()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and not (m[ny][nx] >> 10) & 3:
            seen.add((nx, ny)); q.append((nx, ny))
assert (13, 11) in seen, 'Shaymin onbereikbaar'
print('klaar')
