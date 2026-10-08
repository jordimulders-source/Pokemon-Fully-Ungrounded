"""Project Grounded: de Regigigas-tempel onder de iglo van Ashfrost.
- Tileset data/tilesets/secondary/snow_temple uit de sneeuwtempel-sheet van Ekat99
  (graphics/grounded/tilesets/ekat99_sneeuwtempel.png, 16x16-raster), via emit() uit snow_tileset.py.
- Layout data/layouts/RegigigasTemple (15x14): gevel met pilaren en de donkere trap in de achterwand,
  ijsvloer, een paar ijsbrokken, uitgang onderin.
- Layout data/layouts/RegigigasTemple_Sealed: dezelfde zaal met een ijsmuur (rijen 8-10) voor Regigigas;
  de kaart kiest die zolang FLAG_REGIGIGAS_TEMPLE_OPEN niet gezet is (de iglo is altijd open).
Gebruik: python3 tools/grounded/regigigas_temple.py"""
import os, struct
import numpy as np
from PIL import Image

# emit() en hulpfuncties uit snow_tileset.py halen zonder dat script te draaien
src = open('tools/grounded/snow_tileset.py').read()
ns = {'np': np, 'Image': Image, 'struct': struct, 'os': os, 'LAYER_COVERED': 1}
exec(src[src.index('def to5('):src.rindex('\nif TOWN:')], ns)
emit = ns['emit']

OUT = 'data/tilesets/secondary/snow_temple'
LAY = 'data/layouts/RegigigasTemple'
sheet = Image.open('graphics/grounded/tilesets/ekat99_sneeuwtempel.png').convert('RGBA')
NORMAL, SOUTH_EXIT = 0x00, 0x65


def cell(c, r):
    return sheet.crop((c * 16, r * 16, c * 16 + 16, r * 16 + 16))


def over(base, top):
    out = base.copy()
    out.alpha_composite(top)
    return out


metatiles, names = [], {}
def add(name, img, beh=NORMAL):
    names[name] = 0x200 + len(metatiles)
    metatiles.append((name, img, None, beh))

for r in range(25, 29):
    add('wall_%d' % r, cell(4, r))
for dy in (0, 1):
    for dx in (0, 1):
        add('floor_%d%d' % (dx, dy), cell(4 + dx, 32 + dy))
add('exit', cell(4, 32), SOUTH_EXIT)
for r in range(25, 32):
    for c in range(8):
        add('facade_%d_%d' % (c, r), over(cell(4, r if r < 29 else 27), cell(c, r)))
for (c, r) in [(1, 35), (2, 35), (3, 35), (1, 36), (2, 36)]:
    add('ice_%d_%d' % (c, r), over(cell(4, 32), cell(c, r)))
# ijsmuur (alleen in de verzegelde versie): grote ijsblokken (3x3) en een ijskristal (1x2)
for r in range(21, 24):
    for c in range(5, 8):
        add('iceblock_%d_%d' % (c, r), over(cell(4, 32), cell(c, r)))
for r in (21, 22):
    for c in (3, 4):
        add('icecrys_%d_%d' % (c, r), over(cell(4, 32), cell(c, r)))

res = emit(metatiles, OUT, 512, 6, 7)

W, H = 15, 14
grid = [[None] * W for _ in range(H)]
block = [[True] * W for _ in range(H)]
for y in range(H):
    for x in range(W):
        if y < 4:
            grid[y][x] = 'facade_%d_%d' % (x - 3, 25 + y) if 3 <= x <= 10 else 'wall_%d' % (25 + y)
        elif y < 7:
            grid[y][x] = 'facade_%d_%d' % (x - 3, 25 + y) if 3 <= x <= 10 else 'wall_27'
        elif y < 13 and 0 < x < W - 1:
            grid[y][x] = 'floor_%d%d' % (x % 2, y % 2)
            block[y][x] = False
        else:
            grid[y][x] = 'wall_25'
grid[13][7] = 'exit'; block[13][7] = False
for x in (6, 7, 8):          # de trap voor de donkere ingang
    block[6][x] = False
for (x, y), n in {(2, 9): 'ice_1_35', (12, 10): 'ice_2_35', (3, 11): 'ice_1_36', (11, 8): 'ice_2_36'}.items():
    grid[y][x] = n; block[y][x] = True

os.makedirs(LAY, exist_ok=True)
data = b''.join(struct.pack('<H', names[grid[y][x]] | ((1 if block[y][x] else 0) << 10) | (3 << 12))
                for y in range(H) for x in range(W))
open(LAY + '/map.bin', 'wb').write(data)
open(LAY + '/border.bin', 'wb').write(struct.pack('<4H', *([names['wall_26'] | (1 << 10)] * 4)))
print('klaar:', LAY)

# verzegelde versie (LAYOUT_REGIGIGAS_TEMPLE_SEALED, via setmaplayoutindex zolang niet alle vijf Regi's gevangen zijn):
# een ijsmuur over de hele breedte van de zaal (rijen 8-10), Regigigas zit erachter
SEALED = 'data/layouts/RegigigasTemple_Sealed'
# 13 breed: ijskristal (2) + drie ijsblokken (3x3) + ijskristal (2); de onderste blokrij is schaduw (begaanbaar)
for y in range(8, 11):
    for k in range(3):
        for dx in range(3):
            grid[y][3 + 3 * k + dx] = 'iceblock_%d_%d' % (5 + dx, 21 + y - 8)
            block[y][3 + 3 * k + dx] = y < 10
for y in (8, 9):
    for x0 in (1, 12):
        for dx in (0, 1):
            grid[y][x0 + dx] = 'icecrys_%d_%d' % (3 + dx, 21 + y - 8)
            block[y][x0 + dx] = True
os.makedirs(SEALED, exist_ok=True)
data = b''.join(struct.pack('<H', names[grid[y][x]] | ((1 if block[y][x] else 0) << 10) | (3 << 12))
                for y in range(H) for x in range(W))
open(SEALED + '/map.bin', 'wb').write(data)
open(SEALED + '/border.bin', 'wb').write(struct.pack('<4H', *([names['wall_26'] | (1 << 10)] * 4)))
print('klaar:', SEALED)
