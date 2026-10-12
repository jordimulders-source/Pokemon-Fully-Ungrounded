#!/usr/bin/env python3
"""Project Grounded: het Gen 1-GHOST (Pokemon Tower zonder Silph Scope) als Gen 3-sprites.

Bron: graphics/enfofgjfdzwd1.jpg (Jordi, kleurversie; staat op origin/master: zo nodig eerst
`git show origin/master:graphics/enfofgjfdzwd1.jpg > bron.jpg` en het pad meegeven).
Het raster van de GB-pixels (21.9 px) wordt 1:1 overgenomen: 49x49 in een 64x64-frontsprite (zwart, paars, perzik,
wit voor ogen/mond; cream aan de rand en kleine cream-vlekjes in de rafelrand = transparant), plus een verkleinde
32x32-overworld met hetzelfde palet. Gebruikt door src/gen1_ghost.c en OBJ_EVENT_GFX_GEN1_GHOST.
Gebruik: python3 tools/grounded/gen1_ghost_sprites.py [bron.jpg] [voorbeeld_8x.png]"""
import os, sys
import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'graphics/enfofgjfdzwd1.jpg')
PREVIEW = sys.argv[2] if len(sys.argv) > 2 else None
os.chdir(ROOT)
OUT = 'graphics/grounded/gen1_ghost'
OW = 'graphics/object_events/pics/misc/gen1_ghost.png'
OWPAL = 'graphics/object_events/palettes/gen1_ghost.pal'

a = np.asarray(Image.open(SRC).convert('RGB')).astype(float)
P, ox, oy = 21.9, 5.0, 5.0          # pixelmaat en verschuiving van het GB-raster in de bron
n = 49
cells = np.zeros((n, n, 3))
for j in range(n):
    for i in range(n):
        x0, y0 = int(ox + i * P + P * 0.3), int(oy + j * P + P * 0.3)
        x1, y1 = int(ox + i * P + P * 0.7), int(oy + j * P + P * 0.7)
        cells[j, i] = np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0)
REF = {'black': (35, 22, 30), 'purple': (130, 112, 165), 'peach': (240, 178, 136), 'cream': (252, 250, 236)}
names = list(REF)
ref = np.array([REF[k] for k in names], float)
cls = ((cells[:, :, None, :] - ref[None, None]) ** 2).sum(3).argmin(2)
CREAM = names.index('cream')


def flood(starts, mask):
    st = list(starts)
    comp = []
    while st:
        y, x = st.pop()
        if 0 <= y < n and 0 <= x < n and not mask[y, x] and cls[y, x] == CREAM:
            mask[y, x] = True
            comp.append((y, x))
            st += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    return comp


# cream die aan de rand vastzit = transparant; kleine ingesloten vlekjes ook; ogen en mond (grote vlakken) = wit
outside = np.zeros((n, n), bool)
flood([(0, i) for i in range(n)] + [(n - 1, i) for i in range(n)] + [(i, 0) for i in range(n)]
      + [(i, n - 1) for i in range(n)], outside)
seen = outside.copy()
for sy in range(n):
    for sx in range(n):
        if cls[sy, sx] == CREAM and not seen[sy, sx]:
            comp = flood([(sy, sx)], seen)
            if len(comp) < 6:
                for y, x in comp:
                    outside[y, x] = True
# Gen 3-palet: 0 transparant, 1 zwart, 2 paars, 3 perzik, 4 wit
pal = [(152, 208, 160), (16, 8, 16), (120, 96, 160), (240, 176, 136), (248, 248, 232)] + [(0, 0, 0)] * 11
m = {names.index('black'): 1, names.index('purple'): 2, names.index('peach'): 3, CREAM: 4}
lab = np.zeros((n, n), np.int32)
for y in range(n):
    for x in range(n):
        lab[y, x] = 0 if outside[y, x] else m[cls[y, x]]


def save(idx, path, palpath, preview, scale):
    im = Image.fromarray(idx, 'P')
    im.putpalette([c for p in pal for c in p] + [0] * (768 - 48))
    im.save(path)
    with open(palpath, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in pal))
    if preview:
        rgb = np.array(pal, np.uint8)[idx]
        rgb[idx == 0] = (255, 255, 255)
        Image.fromarray(rgb).resize((idx.shape[1] * scale, idx.shape[0] * scale), Image.NEAREST).save(preview)


# ---------------------------------------------------------------- frontsprite 64x64 (1:1)
front = np.zeros((64, 64), np.uint8)
X0, Y0 = (64 - n) // 2 + 1, 64 - n - 2          # midden, onderkant 2 px boven de rand
front[Y0:Y0 + n, X0:X0 + n] = lab
os.makedirs(OUT, exist_ok=True)
save(front, OUT + '/front.png', OUT + '/front.pal', PREVIEW, 8)

# ---------------------------------------------------------------- overworld 32x32 (verkleind, zelfde palet)
L = np.where(lab == 0, -1, lab)
S = 30
ow = np.zeros((32, 32), np.uint8)
f = n / S
for ty in range(S):
    for tx in range(S):
        blk = L[int(ty * f):max(int(ty * f) + 1, int((ty + 1) * f)), int(tx * f):max(int(tx * f) + 1, int((tx + 1) * f))]
        fr = {k: (blk == k).mean() for k in (-1, 1, 2, 3, 4)}
        body = fr[1] + fr[2] + fr[4]
        if fr[4] >= 0.2 and body > 0.6:
            v = 4
        elif body >= 0.5:
            v = 2 if fr[2] > 0.45 else 1
        elif fr[3] + fr[2] >= 0.35 and (tx + ty) % 2 == 0:
            v = 3                                   # rafelrand als dither
        else:
            v = 0
        ow[32 - S - 1 + ty, 1 + tx] = v
o2 = ow.copy()                                      # omlijning: zwart lijf naast niet-lijf wordt paars
for y in range(32):
    for x in range(32):
        if ow[y, x] == 1 and any(not (0 <= y + dy < 32 and 0 <= x + dx < 32) or ow[y + dy, x + dx] in (0, 3)
                                 for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            o2[y, x] = 2
save(o2, OW, OWPAL, PREVIEW.replace('.png', '_ow8x.png') if PREVIEW else None, 8)
print('klaar:', OUT + '/front.png', OW)
