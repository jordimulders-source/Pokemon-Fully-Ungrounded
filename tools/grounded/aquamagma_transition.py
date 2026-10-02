"""Project Grounded: genereert de gevechtstransitie voor Archie + Maxie samen (Sootopolis):
het Aqua- en het Magma-logo naast elkaar (vanilla graphics, verkleind), met het vanilla evil_team-palet.
Schrijft graphics/battle_transitions/aqua_magma.png (tiles) en aqua_magma.bin (tilemap 32x32, palet 15).
Gebruik: python3 tools/grounded/aquamagma_transition.py"""
import struct
from PIL import Image

B = 'graphics/battle_transitions/'
W, H = 240, 160

def render(name):
    d = open(B + name + '.4bpp', 'rb').read()
    tiles = [d[i:i + 32] for i in range(0, len(d), 32)]
    m = struct.unpack('<1024H', open(B + name + '.bin', 'rb').read())
    img = [[0] * W for _ in range(H)]
    for ty in range(20):
        for tx in range(30):
            e = m[ty * 32 + tx]; t = e & 0x3ff
            hf, vf = e >> 10 & 1, e >> 11 & 1
            if t >= len(tiles): continue
            for y in range(8):
                for x in range(8):
                    c = (tiles[t][y * 4 + x // 2] >> ((x & 1) * 4)) & 15
                    img[ty * 8 + (7 - y if vf else y)][tx * 8 + (7 - x if hf else x)] = c
    xs = [x for y in range(H) for x in range(W) if img[y][x]]
    ys = [y for y in range(H) for x in range(W) if img[y][x]]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    return [row[x0:x1 + 1] for row in img[y0:y1 + 1]]

def scale(img, f):
    h, w = len(img), len(img[0])
    nh, nw = int(h * f), int(w * f)
    return [[img[min(h - 1, int(y / f))][min(w - 1, int(x / f))] for x in range(nw)] for y in range(nh)]

aqua, magma = render('team_aqua'), render('team_magma')
# beide logo's in een vak van 112x150, zelfde schaal
f = min(112 / max(len(aqua[0]), len(magma[0])), 150 / max(len(aqua), len(magma)), 1.0)
aqua, magma = scale(aqua, f), scale(magma, f)
img = [[0] * W for _ in range(H)]
for logo, cx in ((aqua, 60), (magma, 180)):
    h, w = len(logo), len(logo[0])
    ox, oy = cx - w // 2, (H - h) // 2
    for y in range(h):
        for x in range(w):
            if logo[y][x]: img[oy + y][ox + x] = logo[y][x]

tiles, index, tilemap = [], {}, [0] * 1024
blank = tuple([0] * 64); tiles.append(blank); index[blank] = 0
for ty in range(H // 8):
    for tx in range(W // 8):
        t = tuple(img[ty * 8 + py][tx * 8 + px] for py in range(8) for px in range(8))
        if t not in index: index[t] = len(tiles); tiles.append(t)
        tilemap[ty * 32 + tx] = index[t] | (15 << 12)
out = Image.new('P', (128, ((len(tiles) + 15) // 16) * 8))
for n, t in enumerate(tiles):
    for p, v in enumerate(t):
        out.putpixel(((n % 16) * 8 + p % 8, (n // 16) * 8 + p // 8), v)
pal = [tuple(map(int, l.split())) for l in open(B + 'evil_team.pal').read().split('\n')[3:19]]
out.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
out.save(B + 'aqua_magma.png')
open(B + 'aqua_magma.bin', 'wb').write(struct.pack('<1024H', *tilemap))
print('schaal %.2f, tiles %d' % (f, len(tiles)))
