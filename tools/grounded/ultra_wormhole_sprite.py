"""Project Grounded: overworld-object van een Ultra Wormhole (Ultra Space, achterin Altering Cave).

Een staande, ovale scheur van 32x32: een witte kern met spiraalarmen, een prismarand (geel, roze, cyaan) en een
donkere omlijning. Stilstaand object (OBJ_EVENT_GFX_ULTRA_WORMHOLE): de ingang in Altering Cave, het grote portaal in
de hub en de terugweg op elke Ultra Beast-plek. Schrijft graphics/object_events/pics/misc/ultra_wormhole.png +
palettes/ultra_wormhole.pal.

Gebruik: python3 tools/grounded/ultra_wormhole_sprite.py"""
import math
import os
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
PAL = [(0, 0, 0),                                   # 0 transparant
       (24, 16, 48), (72, 40, 120), (136, 72, 184),  # 1-3 omlijning, paars
       (248, 104, 200), (248, 168, 232),             # 4-5 roze
       (248, 224, 96), (248, 248, 176),              # 6-7 geel
       (80, 208, 248), (168, 240, 248),              # 8-9 cyaan
       (232, 240, 255), (255, 255, 255),             # 10-11 wit
       (200, 184, 248), (120, 104, 216),             # 12-13 lila (spiraal)
       (0, 0, 0), (0, 0, 0)]
W = H = 32
CX, CY, RX, RY = 15.5, 17.0, 11.0, 14.0
px = [[0] * W for _ in range(H)]
for y in range(H):
    for x in range(W):
        dx, dy = (x + 0.5 - CX) / RX, (y + 0.5 - CY) / RY
        r = math.hypot(dx, dy)
        a = math.atan2(dy, dx)
        wob = 0.05 * math.sin(a * 6)
        if r > 1.0 + wob + 0.12:
            continue
        if r > 1.0 + wob:
            px[y][x] = 1
            continue
        if r > 0.86 + wob:                              # prismarand: kleur draait rond
            k = int(((a + math.pi) / (2 * math.pi)) * 6) % 3
            px[y][x] = (4, 6, 8)[k] if r < 0.94 + wob else (5, 7, 9)[k]
            continue
        s = math.sin(a * 3 + r * 9.0)                   # drie spiraalarmen naar binnen
        if r < 0.22:
            px[y][x] = 11
        elif s > 0.55:
            px[y][x] = 10 if r < 0.5 else 12
        elif s > -0.2:
            px[y][x] = 12 if r < 0.6 else 13
        else:
            px[y][x] = 13 if r < 0.7 else 2
# kleine vonken rondom
for (x, y) in ((3, 6), (28, 9), (2, 24), (29, 27), (15, 1)):
    if px[y][x] == 0:
        px[y][x] = 11
im = Image.new('P', (W, H))
flat = []
for c in PAL:
    flat += list(c)
im.putpalette(flat + [0] * (768 - len(flat)))
im.putdata([v for row in px for v in row])
im.save(os.path.join(ROOT, 'graphics/object_events/pics/misc/ultra_wormhole.png'))
with open(os.path.join(ROOT, 'graphics/object_events/palettes/ultra_wormhole.pal'), 'w', newline='\r\n') as f:
    f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in PAL))
print('klaar: ultra_wormhole.png + ultra_wormhole.pal')
