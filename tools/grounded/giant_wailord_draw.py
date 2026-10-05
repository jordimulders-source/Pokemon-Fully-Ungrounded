#!/usr/bin/env python3
"""Project Grounded: reuzen-Wailord v3 (Jordi, 5 okt: 'zoals het HGSS-sprite opgeblazen tot ware grootte, maar dan de
omlijning wat minder dik'). Het zijaanzicht uit de follower-sprite (graphics/pokemon/wailord/overworld.png, frame 4,
= het HGSS-overworldsprite) wordt met hele pixels (nearest) 4x vergroot, zodat het de pixel-art-look houdt. Alleen de
buitenrand wordt dun: van elk randblok (zwart of donkerblauw) blijft 1 px aan de buitenkant over, de rest krijgt de kleur van
het lijf ernaast. Binnenlijnen en het oog blijven zoals ze zijn. Het onderste deel ligt onder water, met een schuimlijn.
Uitvoer: 192x96 (giant_wailord.png + .pal). Gebruik: python3 tools/grounded/giant_wailord_draw.py [voorbeeld.png]"""
import sys
import numpy as np
from PIL import Image

SRC = 'graphics/pokemon/wailord/overworld.png'
OUT = 'graphics/object_events/pics/misc/giant_wailord.png'
PAL = 'graphics/object_events/palettes/giant_wailord.pal'
W, H = 192, 96
SCALE = 4
LINE = SCALE              # randdikte: Jordi, 5 okt: "houd het maar gewoon dik, is humor" (1 = dun)
SUBMERGED = 3             # zoveel bronrijen (onderkant) liggen onder water
OUTLINE = 1
FOAM = 9


def main():
    im = Image.open(SRC)
    src = np.array(im.crop((256, 0, 320, 64)))
    ys, xs = np.where(src != 0)
    src = src[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    src = src[:src.shape[0] - SUBMERGED]
    h, w = src.shape
    big = np.kron(src, np.ones((SCALE, SCALE), np.uint8))
    pad = np.pad(src, 1)
    for y in range(h):
        for x in range(w):
            if src[y, x] == 0:
                continue
            col = src[y, x]
            nb = {(-1, 0): pad[y, x + 1], (1, 0): pad[y + 2, x + 1], (0, -1): pad[y + 1, x], (0, 1): pad[y + 1, x + 2]}
            outside = [d for d, v in nb.items() if v == 0]
            if not outside:
                continue                                  # binnenlijn of oog: laten staan
            inner = [v for v in nb.values() if v not in (0, OUTLINE, col)] or [v for v in nb.values() if v not in (0, col)]
            if not inner:                                 # alleen tussen rand en leegte: hele blok laten
                continue
            fill = max(set(inner), key=inner.count)
            blk = np.full((SCALE, SCALE), fill, np.uint8)
            for dy, dx in outside:
                if dy == -1: blk[:LINE, :] = col
                if dy == 1: blk[-LINE:, :] = col
                if dx == -1: blk[:, :LINE] = col
                if dx == 1: blk[:, -LINE:] = col
            big[y * SCALE:(y + 1) * SCALE, x * SCALE:(x + 1) * SCALE] = blk
    # diagonale hoekblokken (rand alleen schuin naar buiten): ook dunnen
    canvas = np.zeros((H, W), np.uint8)
    x0 = (W - big.shape[1]) // 2
    y0 = H - 5 - big.shape[0]
    canvas[y0:y0 + big.shape[0], x0:x0 + big.shape[1]] = big
    wl = y0 + big.shape[0]
    cols = np.where(canvas[wl - 1] != 0)[0]
    lo, hi = cols.min() - 4, cols.max() + 4
    canvas[wl - 1, lo:hi + 1] = np.where(canvas[wl - 1, lo:hi + 1] == 0, FOAM, canvas[wl - 1, lo:hi + 1])
    for x in range(lo, hi + 1):
        if (x // 4) % 3 != 2:
            canvas[wl, x] = FOAM
    for x in range(lo - 8, hi + 9, 12):
        canvas[wl + 2, x:x + 4] = FOAM
    out = Image.fromarray(canvas, 'P')
    pal = (im.getpalette() + [0] * 48)[:48]
    out.putpalette(pal + [0] * (768 - len(pal)))
    out.save(OUT)
    with open(PAL, 'w') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for i in range(16):
            f.write('%d %d %d\n' % tuple(pal[i * 3:i * 3 + 3]))
    print(OUT, big.shape)
    if len(sys.argv) > 1:
        rgb = np.array(out.convert('RGB')); rgb[canvas == 0] = (48, 120, 200)
        Image.fromarray(rgb).resize((W * 3, H * 3), Image.NEAREST).save(sys.argv[1])


if __name__ == '__main__':
    main()
