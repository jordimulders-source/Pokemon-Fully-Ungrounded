"""Capykart r8 -> r9: nieuwe paletindeling (coördinator): hout oranje en los van de vacht.
Uitgangspunt r8; alleen tinttoewijzing + palet. Silhouet en bevroren gezicht diff 0."""
import os, json, sys
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
R8 = os.path.join(D, '../r8/capykart.png')
im = Image.open(R8); W, H = im.size
o = [[im.getpixel((x, y)) for x in range(W)] for y in range(H)]
g = [r[:] for r in o]
w8 = json.load(open(os.path.join(D, '../r8/wijzigingen.json')))
zone8 = {tuple(map(int, k.split(','))): v[2] for k, v in w8.items()}

# nieuwe indices
K, FL, FM, DK = 1, 2, 3, 4          # zwart, vacht licht, vacht midden, gedeeld donker (vacht-donker = hout-donkerst = rood-schaduw)
HH, HB, HS = 5, 6, 13               # hout hooglicht, hout basis, hout midden-schaduw
RDK, BG, WT, BL, DG, RD, YE, GN = 7, 8, 9, 10, 11, 12, 14, 15   # 7 = rood-donker (lichtgrijs vervalt)
PAL = {0: (0, 0, 0), 1: (32, 20, 28), 2: (216, 158, 116), 3: (180, 122, 88), 4: (140, 72, 52),
       5: (252, 186, 98), 6: (238, 140, 64), 13: (198, 98, 50),
       7: (178, 44, 56), 8: (88, 96, 128), 9: (255, 255, 255), 10: (100, 156, 232), 11: (60, 140, 72),
       12: (240, 92, 84), 14: (248, 212, 72), 15: (96, 180, 84)}
if len(sys.argv) > 1: PAL.update(json.loads(sys.argv[1]))

def isfur(x, y):  # kop, oren, nek, schouder (zie log)
    if y <= 29 and x <= 42: return True
    if 30 <= y <= 32 and 23 <= x <= 44: return True
    if y == 33 and (24 <= x <= 27 or 31 <= x <= 46): return True
    if 34 <= y <= 37 and 31 <= x <= 47 and o[y][x] in (2, 3): return True
    if y == 35 and 30 <= x <= 47: return True
    return False
def block(x, y): return x >= 42 and y <= 31 and not isfur(x, y)

side_panels = lambda x, y: ((44 <= y <= 53 and 34 <= x <= 47) or (36 <= y <= 43 and 52 <= x <= 61)
                            or (44 <= y <= 55 and 19 <= x <= 23))
def hood_blob(x, y):
    return ((y == 39 and 7 <= x <= 15) or (y == 40 and 5 <= x <= 12) or (y == 41 and 4 <= x <= 9)
            or (42 <= y <= 44 and x <= 4))
hood_top = lambda x, y: 38 <= y <= 44 and x <= 25
hood_back = lambda x, y: 39 <= y <= 43 and 17 <= x <= 25
WHY = {}
def put(x, y, v, why):
    if g[y][x] != v: WHY[(x, y)] = why
    g[y][x] = v
for y in range(H):
    for x in range(W):
        v = o[y][x]
        if v == 7: put(x, y, BG, 'lichtgrijs vervalt: hoepel/tandschaduw -> blauwgrijs'); continue
        if v in (0, 1, 8, 9, 10, 11, 12, 14, 15): continue
        if block(x, y):
            if v == 13: put(x, y, RDK, 'rood zijvlak/onderbevel -> rood-donker (eigen; gedeeld donker las bruin)')
            elif v == 6: put(x, y, HB, 'gele zijkant = hout-basis')
            elif v == 5: put(x, y, HH, 'bevel geel/rood = hout-hooglicht')
            continue
        if isfur(x, y):
            if v == 5: put(x, y, FL, 'vacht: hooglicht uit r8 terug naar vacht-licht (vacht heeft 3 tinten)')
            elif v == 6: put(x, y, HB, 'hout dat tussen kop en nek uitsteekt')
            continue
        # ---- hout ----
        z = zone8.get((x, y), '')
        black_adj = any(0 <= x+dx < W and 0 <= y+dy < H and o[y+dy][x+dx] in (0, 1) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)))
        if v == 5:
            if hood_top(x, y) and not hood_blob(x, y): put(x, y, HB, 'motorkap: basis, hooglicht alleen linksboven (bolling)')
            else: put(x, y, HH, 'hout licht -> hooglicht')
        elif v == 6:
            if hood_back(x, y): put(x, y, HS, 'motorkap achter/rechts draait weg van het licht')
            elif side_panels(x, y): put(x, y, HS, 'zijkant: midden-schaduw (neus lichter dan zijkant)')
            else: put(x, y, HB, 'hout basis')
        elif v == 2:
            put(x, y, HB if hood_blob(x, y) else HS, 'nerf op licht vlak: een houttint donkerder')
        elif v == 3:
            put(x, y, DK if side_panels(x, y) else HS, 'nerf: een houttint donkerder dan het vlak')
        elif v == 4:
            if z in ('kart neus sikkel', 'voorwiel', 'achterwiel', 'kart midden') and not black_adj and not side_panels(x, y):
                put(x, y, HS, 'sikkel: overgang basis -> donker')
            else: put(x, y, DK, 'hout donkerst / outline base (gedeeld donker)')
pal = []
for i in range(16): pal += list(PAL.get(i, (0, 0, 0)))
out = Image.new('P', (W, H)); out.putpalette(pal + [0]*(768-48)); out.putdata([v for r in g for v in r])
out.save(os.path.join(D, 'capykart.png'), transparency=0)
out.convert('RGBA').resize((W*8, H*8), Image.NEAREST).save(os.path.join(D, 'capykart_8x.png'))
json.dump({f'{x},{y}': [o[y][x], g[y][x], w] for (x, y), w in WHY.items()}, open(os.path.join(D, 'wijzigingen.json'), 'w'), ensure_ascii=False)
print('gewijzigd t.o.v. r8 (index):', len(WHY))
