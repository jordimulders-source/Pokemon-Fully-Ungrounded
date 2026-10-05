#!/usr/bin/env python3
"""Project Grounded: reuzen-Wailord als grappig obstakel op zee (Jordi, 5 okt). Het zijaanzicht uit de follower-sprite
(graphics/pokemon/wailord/overworld.png, frame 4) 4x vergroot met Scale2x (twee keer, gladde randen), de buik onder de
waterlijn weggeknipt en een schuimrand erbij. Uitvoer: 192x96, 9 blokken van 64x32 (spritesheet-regel -mwidth 8
-mheight 4), eigen palet. Gebruik: python3 tools/grounded/giant_wailord.py [voorbeeld.png]"""
import sys
import numpy as np
from PIL import Image

SRC = 'graphics/pokemon/wailord/overworld.png'
OUT = 'graphics/object_events/pics/misc/giant_wailord.png'
PAL = 'graphics/object_events/palettes/giant_wailord.pal'
W, H = 192, 96
WATERLINE = 0.72          # deel van de hoogte boven water
FOAM = 9                  # lichtste paletkleur (216,232,248)


def scale2x(a):
    h, w = a.shape
    p = np.pad(a, 1, mode='edge')
    B, D, F, Hh, E = p[:-2, 1:-1], p[1:-1, :-2], p[1:-1, 2:], p[2:, 1:-1], a
    out = np.zeros((h * 2, w * 2), a.dtype)
    out[0::2, 0::2] = np.where((D == B) & (B != F) & (D != Hh), D, E)
    out[0::2, 1::2] = np.where((B == F) & (B != D) & (F != Hh), F, E)
    out[1::2, 0::2] = np.where((D == Hh) & (D != B) & (Hh != F), D, E)
    out[1::2, 1::2] = np.where((Hh == F) & (D != Hh) & (B != F), F, E)
    return out


def main():
    im = Image.open(SRC)
    a = np.array(im.crop((256, 0, 320, 64)))
    ys, xs = np.where(a != 0)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    a = scale2x(scale2x(a))                                   # 4x
    cut = int(a.shape[0] * WATERLINE)
    body = a[:cut]
    canvas = np.zeros((H, W), np.uint8)
    x0 = (W - body.shape[1]) // 2
    y0 = H - 6 - body.shape[0]
    canvas[y0:y0 + body.shape[0], x0:x0 + body.shape[1]] = body
    # schuimrand: waterlijn over de breedte van het lijf (+2 px), golvend, en een paar spatten
    row = canvas[y0 + body.shape[0] - 1]
    cols = np.where(row != 0)[0]
    lo, hi = cols.min() - 3, cols.max() + 3
    for x in range(lo, hi + 1):
        wob = (x // 3) % 3
        for dy in range(2 + (wob == 1)):
            canvas[y0 + body.shape[0] - 1 + dy, x] = FOAM if (x + dy) % 5 else 7
    for x in range(lo - 6, hi + 7, 9):
        canvas[H - 3, x:x + 4] = FOAM
    out = Image.fromarray(canvas, 'P')
    pal = (im.getpalette() + [0] * 48)[:48]
    out.putpalette(pal + [0] * (768 - len(pal)))
    out.save(OUT)
    with open(PAL, 'w') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for i in range(16):
            f.write('%d %d %d\n' % tuple(pal[i * 3:i * 3 + 3]))
    print(OUT, body.shape, 'waterlijn op y', y0 + body.shape[0])
    if len(sys.argv) > 1:
        prev = Image.new('RGB', (W * 2, H * 2), (48, 120, 200))
        rgba = out.convert('RGBA'); px = np.array(rgba); px[canvas == 0, 3] = 0
        prev.paste(Image.fromarray(px).resize((W * 2, H * 2), Image.NEAREST), (0, 0), Image.fromarray(px).resize((W * 2, H * 2), Image.NEAREST))
        prev.save(sys.argv[1])


if __name__ == '__main__':
    main()
