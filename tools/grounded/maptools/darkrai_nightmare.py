"""Project Grounded: bouwt de nachtmerrie van Darkrai (MtPyre_Nightmare): de top van Mt. Pyre als droom, uitgesneden
uit MtPyre_Summit (het heiligdom met de ommuurde grasvlakte), zonder uitgang, met grafstenen, en met eigen paarse,
donkere paletten. De tilesets nightmare_general / nightmare_facility lenen tiles en metatiles van General / Facility
(zie src/data/tilesets/headers.h, en het BASE-bestand voor render_map.py) en hebben alleen eigen paletten.
Gebruik: python3 tools/grounded/maptools/darkrai_nightmare.py [voorbeeld.png]"""
import os, struct, sys


def darken(rgb):
    """Kleur -> nachtmerrie: helderheid met meer contrast (machtsfunctie) op een paars-blauwe schaal, een vleugje
    van de oorspronkelijke kleur erdoor."""
    r, g, b = rgb
    L = ((0.30 * r + 0.59 * g + 0.11 * b) / 248) ** 1.6
    out = (6 + L * 120 + r * 0.08, L * 60 + g * 0.06, 16 + L * 160 + b * 0.08)
    return tuple(max(0, min(248, int(v) // 8 * 8)) for v in out)


def convert(src, dst, base, black_backdrop=False):
    os.makedirs(dst + '/palettes', exist_ok=True)
    open(dst + '/BASE', 'w').write(base + '\n')
    for i in range(16):
        lines = open(f'{src}/palettes/{i:02}.pal').read().split('\n')
        cols = [darken(tuple(map(int, l.split()))) for l in lines[3:19]]
        if black_backdrop and i == 0:
            cols[0] = (0, 0, 0)
        with open(f'{dst}/palettes/{i:02}.pal', 'w', newline='\r\n') as fp:
            fp.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in cols))


convert('data/tilesets/primary/general', 'data/tilesets/primary/nightmare_general', 'general', True)
convert('data/tilesets/secondary/facility', 'data/tilesets/secondary/nightmare_facility', 'facility')

# kaart: MtPyre_Summit x 15..31, y 0..10 (17 x 11); de trap naar beneden (rij 10) wordt klifwand
SW = 50
src = struct.unpack('<%dH' % (SW * 37), open('data/layouts/MtPyre_Summit/map.bin', 'rb').read())
W, H, X0 = 17, 11, 15
grid = [[src[y * SW + X0 + x] for x in range(W)] for y in range(H)]
for x in range(7, 10):
    grid[10][x] = grid[10][6]                       # klifwand in plaats van de trap: geen uitgang
VOID = 0x601                                        # Facility-metatile 0x201: effen (bijna) zwart, niet beloopbaar
for y in range(H):
    grid[y][0] = grid[y][W - 1] = VOID              # buiten de muren: zwarte leegte
    for x in range(W):
        if grid[y][x] & 0x3FF in (0x0A1, 0x341, 0x342, 0x343):  # losse bergtoppen buiten de ring ook
            grid[y][x] = VOID
GRAVE = 0x725
for x, y in [(4, 3), (5, 5), (4, 6), (12, 3), (11, 5), (12, 6), (6, 2), (10, 2)]:
    assert grid[y][x] & 0x3FF == 0x001, (x, y, hex(grid[y][x]))
    grid[y][x] = GRAVE
for (x, y) in [(8, 5), (8, 9)]:                     # Darkrai, aankomst
    assert grid[y][x] & 0xC00 == 0, (x, y)
# bereikbaarheid: van de aankomst naar het vak voor Darkrai
seen, todo = {(8, 9)}, [(8, 9)]
while todo:
    x, y = todo.pop()
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and grid[ny][nx] & 0xC00 == 0 and (nx, ny) != (8, 5):
            seen.add((nx, ny))
            todo.append((nx, ny))
assert (8, 6) in seen, 'Darkrai niet bereikbaar'
# rondom aanvullen met zwarte leegte, zodat de camera nooit buiten de kaart kijkt (de rand zou dan getekend worden)
PX, PT, PB = 7, 5, 6
grid = [[VOID] * (W + 2 * PX) for _ in range(PT)] + [[VOID] * PX + row + [VOID] * PX for row in grid] + \
       [[VOID] * (W + 2 * PX) for _ in range(PB)]
W, H = W + 2 * PX, H + PT + PB
print('Darkrai op (%d, %d), aankomst op (%d, %d)' % (8 + PX, 5 + PT, 8 + PX, 9 + PT))
os.makedirs('data/layouts/MtPyre_Nightmare', exist_ok=True)
open('data/layouts/MtPyre_Nightmare/map.bin', 'wb').write(struct.pack('<%dH' % (W * H), *[v for row in grid for v in row]))
open('data/layouts/MtPyre_Nightmare/border.bin', 'wb').write(struct.pack('<4H', *[VOID] * 4))
print('MtPyre_Nightmare %dx%d, %d vakken bereikbaar' % (W, H, len(seen)))
if len(sys.argv) > 1:
    import subprocess
    subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', 'MtPyre_Nightmare', sys.argv[1], '0', str(H)], check=True)
