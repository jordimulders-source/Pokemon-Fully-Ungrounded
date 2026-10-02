"""Project Grounded: genereert de gevechtstransities van Regidrago en Regieleki.
De stip komt uit de vanilla Regi-tiles (regis.4bpp + regice.bin); de stippen worden
in het gezichtspatroon van de Regi op een 240x160-beeld gezet en in tiles ontdubbeld.
Schrijft graphics/battle_transitions/<naam>.png (tiles), .bin (tilemap 32x32, palet 15) en .pal.
Gebruik: python3 tools/grounded/regi_transition.py"""
import struct
from PIL import Image

B = 'graphics/battle_transitions/'
W, H = 240, 160

def vanilla_dot():
    d = open(B + 'regis.4bpp', 'rb').read()
    tiles = [d[i:i + 32] for i in range(0, len(d), 32)]
    m = struct.unpack('<1024H', open(B + 'regice.bin', 'rb').read())
    img = [[0] * 256 for _ in range(160)]
    for ty in range(20):
        for tx in range(32):
            e = m[ty * 32 + tx]; t = e & 0x3ff
            hf, vf = e >> 10 & 1, e >> 11 & 1
            for y in range(8):
                for x in range(8):
                    c = (tiles[t][y * 4 + x // 2] >> ((x & 1) * 4)) & 15
                    img[ty * 8 + (7 - y if vf else y)][tx * 8 + (7 - x if hf else x)] = c
    # eerste stip: kleinste omhullende rond de eerste gekleurde pixel
    pts = [(x, y) for y in range(160) for x in range(256) if img[y][x]]
    x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts if p[0] < min(q[0] for q in pts) + 40)
    x0 = min(p[0] for p in pts if y0 <= p[1] < y0 + 40)
    blk = [[img[y][x] for x in range(x0, x0 + 40)] for y in range(y0, y0 + 40)]
    ys = [y for y in range(40) if any(blk[y][:36])]
    xs = [x for x in range(40) if any(blk[y][x] for y in ys)]
    # alleen de eerste stip: kap af op de eerste lege kolom
    end = xs[0]
    while end + 1 in xs: end += 1
    return [row[xs[0]:end + 1] for row in blk[ys[0]:ys[-1] + 1]]

def build(name, coords, scale, colors):
    dot = vanilla_dot(); dh, dw = len(dot), len(dot[0])
    cx = [x * scale for x, y in coords]; cy = [y * scale for x, y in coords]
    ox = (W - (max(cx) - min(cx))) / 2 - min(cx); oy = (H - (max(cy) - min(cy))) / 2 - min(cy)
    img = [[0] * W for _ in range(H)]
    for x, y in zip(cx, cy):
        px, py = int(round(x + ox - dw / 2)), int(round(y + oy - dh / 2))
        for j in range(dh):
            for i in range(dw):
                if dot[j][i]: img[py + j][px + i] = dot[j][i]
    tiles, index, tilemap = [], {}, [0] * 1024
    blank = tuple([0] * 64); tiles.append(blank); index[blank] = 0
    for ty in range(H // 8):
        for tx in range(W // 8):
            t = tuple(img[ty * 8 + py][tx * 8 + px] for py in range(8) for px in range(8))
            if t not in index: index[t] = len(tiles); tiles.append(t)
            tilemap[ty * 32 + tx] = index[t] | (15 << 12)
    rows = (len(tiles) + 15) // 16
    out = Image.new('P', (128, rows * 8))
    for n, t in enumerate(tiles):
        for p, v in enumerate(t):
            out.putpixel(((n % 16) * 8 + p % 8, (n // 16) * 8 + p // 8), v)
    out.putpalette([v for c in colors for v in c] + [0] * (768 - 48))
    out.save(B + name + '.png')
    open(B + name + '.bin', 'wb').write(struct.pack('<1024H', *tilemap))
    with open(B + name + '.pal', 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n')
        for c in colors: fp.write('%d %d %d\n' % c)
    print(name, 'tiles:', len(tiles))

BLACK = [(0, 0, 0)] * 8
# Regidrago: blauwe stippen in een vork/Y-patroon (gezicht op de rode bol)
build('regidrago', [(140, 57), (335, 57), (240, 93), (165, 143), (313, 143), (240, 197), (240, 298)], 0.5,
      BLACK + [(16, 140, 224), (8, 40, 90), (16, 70, 140), (24, 100, 190), (40, 170, 240), (90, 200, 248), (170, 228, 255), (255, 255, 255)])
# Regieleki: roze/oranje stippen in zijn glimlachpatroon
build('regieleki', [(126, 215), (180, 287), (105, 335), (265, 305), (352, 325), (438, 278), (410, 400)], 0.55,
      BLACK + [(240, 140, 150), (110, 40, 40), (170, 70, 70), (215, 110, 100), (248, 150, 130), (255, 180, 160), (255, 215, 200), (255, 255, 255)])
