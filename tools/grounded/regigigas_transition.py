"""Project Grounded: genereert de gevechtstransitie van Regigigas (B_TRANSITION_REGIGIGAS).
Zelfde stip als de vanilla Regi's (regis.4bpp, via regi_transition.vanilla_dot), maar per oog
in een eigen kleur met een witte kern en kleine 'oortjes', in het oogpatroon van Regigigas:
3 rijen van 2 (rood het breedst, dan blauw, dan wit/grijs iets smaller).
Tiles worden ontdubbeld, ook horizontaal gespiegeld (het patroon is symmetrisch).
Schrijft graphics/battle_transitions/regigigas.png, .bin (32x32, palet 15) en .pal.
Gebruik: python3 tools/grounded/regigigas_transition.py (eerst make graphics/battle_transitions/regis.4bpp)"""
import os, struct, sys
from PIL import Image

# alleen de hulpfuncties van regi_transition.py (dat script bouwt bij import ook Regidrago/Regieleki)
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'regi_transition.py')).read()
exec(_src.split('BLACK = ')[0])

OUTLINE, WHITE = 1, 15
# per oogkleur: (donker, kleur, licht)
RED, CYAN, GREY = (2, 3, 4), (5, 6, 7), (8, 9, 10)
PAL = [(0, 0, 0), (16, 12, 24),
       (120, 16, 24), (232, 48, 40), (255, 128, 104),
       (16, 88, 128), (56, 196, 240), (168, 236, 255),
       (88, 96, 112), (184, 190, 200), (228, 232, 240),
       (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 255, 255)]

ROW_DY = 40            # ~1,3x de oogdiameter (31 px)
ROWS = [(-ROW_DY, 37, RED), (0, 32, CYAN), (ROW_DY, 28, GREY)]  # (dy, halve afstand, kleuren)

def eye(colors):
    dot = vanilla_dot(); n = len(dot); c = (n - 1) / 2
    dark, mid, light = colors
    out = []
    for y in range(n):
        row = []
        for x in range(n):
            v = dot[y][x]
            r2 = (x - c) ** 2 + (y - c) ** 2
            if v == 0: row.append(0)
            elif v == 10: row.append(OUTLINE)
            elif v == 11: row.append(dark)
            elif r2 <= 3.2 ** 2: row.append(WHITE)
            elif r2 <= 6.0 ** 2: row.append(light)
            else: row.append(mid)
        out.append(row)
    return out

def build():
    img = [[0] * W for _ in range(H)]
    cx0, cy0 = W // 2, H // 2
    for dy, half, colors in ROWS:
        e = eye(colors); n = len(e)
        for sx in (-1, 1):
            ex, ey = cx0 + sx * half, cy0 + dy
            px, py = ex - n // 2, ey - n // 2
            for j in range(n):
                for i in range(n):
                    if e[j][i]: img[py + j][px + i] = e[j][i]
            # oortjes: kort streepje links en rechts van het oog
            for side in (-1, 1):
                x0 = ex + side * (n // 2 + 1)
                for k in range(4):
                    x = x0 + side * k
                    for yy in range(ey - 2, ey + 3):
                        edge = yy in (ey - 2, ey + 2) or k == 3
                        img[yy][x] = OUTLINE if edge else colors[0]
    # spiegel de linkerhelft naar rechts, zodat het patroon exact symmetrisch is
    for y in range(H):
        for x in range(W // 2):
            img[y][W - 1 - x] = img[y][x]
    tiles, index, tilemap = [], {}, [0] * 1024
    blank = tuple([0] * 64); tiles.append(blank); index[blank] = (0, 0)
    for ty in range(H // 8):
        for tx in range(W // 8):
            t = tuple(img[ty * 8 + py][tx * 8 + px] for py in range(8) for px in range(8))
            tf = tuple(t[py * 8 + 7 - px] for py in range(8) for px in range(8))
            if t in index: num, hf = index[t]
            elif tf in index: num, hf = index[tf][0], 1 - index[tf][1]
            else: num, hf = len(tiles), 0; tiles.append(t); index[t] = (num, 0)
            tilemap[ty * 32 + tx] = num | (hf << 10) | (15 << 12)
    rows = (len(tiles) + 15) // 16
    out = Image.new('P', (128, rows * 8))
    for n, t in enumerate(tiles):
        for p, v in enumerate(t):
            out.putpixel(((n % 16) * 8 + p % 8, (n // 16) * 8 + p // 8), v)
    out.putpalette([v for c in PAL for v in c] + [0] * (768 - 48))
    out.save(B + 'regigigas.png')
    open(B + 'regigigas.bin', 'wb').write(struct.pack('<1024H', *tilemap))
    with open(B + 'regigigas.pal', 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n')
        for c in PAL: fp.write('%d %d %d\n' % c)
    print('regigigas tiles:', len(tiles))
    return img

if __name__ == '__main__':
    img = build()
    if len(sys.argv) > 1:  # voorbeeldbeeld (2x) naar het opgegeven pad
        p = Image.new('RGB', (W, H))
        for y in range(H):
            for x in range(W):
                p.putpixel((x, y), PAL[img[y][x]] if img[y][x] else (40, 40, 48))
        p.resize((W * 2, H * 2), Image.NEAREST).save(sys.argv[1])
