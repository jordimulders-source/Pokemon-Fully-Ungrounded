"""Project Grounded: voegt de Regi-stippen toe aan de Cave-tileset (eenmalig, idempotent).
Metatile 0x3A8 = stip uit (uitgesleten kuiltje in de grotvloer), 0x3A9 = stip aan (gloeit goud).
Gloedkleuren in de lege plekken 12-14 van palet 6 (de vloerkleur); tiles achteraan tiles.png (vanaf 441).
Gebruik: python3 tools/grounded/regi_dots_tiles.py"""
import math, struct
from PIL import Image

T = 'data/tilesets/secondary/cave/'
FIRST_NEW_TILE = 441
METATILE_COUNT_BEFORE = 424  # 0x200 + 424 = 0x3A8

meta = open(T + 'metatiles.bin', 'rb').read()
if len(meta) // 16 != METATILE_COUNT_BEFORE:
    print('metatiles staan er al (%d)' % (len(meta) // 16)); raise SystemExit

# palet 6: gloedkleuren
pal = open(T + 'palettes/06.pal').read().replace('\r', '').split('\n')
head, cols = pal[:3], pal[3:19]
cols[12], cols[13], cols[14] = '255 238 98', '246 172 41', '255 255 214'
open(T + 'palettes/06.pal', 'w', newline='\r\n').write('\n'.join(head + cols) + '\n')

im = Image.open(T + 'tiles.png')
def tile_px(i):
    return [[im.getpixel(((i % 16) * 8 + x, (i // 16) * 8 + y)) for x in range(8)] for y in range(8)]
# vloer = metatile 0x201: tiles 3, 4, 19, 20 (palet 6, niet gespiegeld)
floor = [[0] * 16 for _ in range(16)]
for k, t in enumerate((3, 4, 19, 20)):
    px = tile_px(t)
    for y in range(8):
        for x in range(8):
            floor[(k // 2) * 8 + y][(k % 2) * 8 + x] = px[y][x]

def dot(lit):
    g = [row[:] for row in floor]
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - 7.5, y - 7.5)
            if lit:
                if d < 2.2: g[y][x] = 14
                elif d < 4.2: g[y][x] = 12
                elif d < 5.6: g[y][x] = 13
                elif d < 6.6 and (x + y) % 2 == 0: g[y][x] = 13
            else:
                if 4.3 <= d < 5.6: g[y][x] = 7
                elif d < 4.3: g[y][x] = 6 if (x - 7.5) + (y - 7.5) > -2 else 5
    return g

new = []
for lit in (False, True):
    g = dot(lit)
    for k in range(4):
        new.append([[g[(k // 2) * 8 + y][(k % 2) * 8 + x] for x in range(8)] for y in range(8)])

need_rows = (FIRST_NEW_TILE + len(new) + 15) // 16
out = Image.new('P', (128, max(im.height, need_rows * 8)), 0)
out.putpalette(im.getpalette())
out.paste(im, (0, 0))
for n, t in enumerate(new):
    i = FIRST_NEW_TILE + n
    for y in range(8):
        for x in range(8):
            out.putpixel(((i % 16) * 8 + x, (i // 16) * 8 + y), t[y][x])
out.save(T + 'tiles.png')

entries = b''
for base in (FIRST_NEW_TILE, FIRST_NEW_TILE + 4):
    bottom = [0x200 + base + k | (6 << 12) for k in range(4)]
    top = [0] * 4
    entries += struct.pack('<8H', *(bottom + top))
open(T + 'metatiles.bin', 'wb').write(meta + entries)
attr = open(T + 'metatile_attributes.bin', 'rb').read()
floor_attr = struct.unpack_from('<H', attr, 1 * 2)[0]  # 0x201
open(T + 'metatile_attributes.bin', 'wb').write(attr + struct.pack('<2H', floor_attr, floor_attr))
print('klaar: metatiles 0x3A8/0x3A9, tiles %d-%d, num_tiles moet %d zijn' % (FIRST_NEW_TILE, FIRST_NEW_TILE + 7, FIRST_NEW_TILE + 8))
