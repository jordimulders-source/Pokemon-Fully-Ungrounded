#!/usr/bin/env python3
"""Project Grounded: reuzen-Wailord v2, hertekend i.p.v. uitgerekt (Jordi: 'te dikke lijnen, lijkt niet meer op een
Pokémon-sprite'). De vorm komt uit het zijaanzicht van de follower-sprite (graphics/pokemon/wailord/overworld.png),
maar wordt op ware grootte opnieuw getekend zoals een Gen 3-sprite: gladde contour, omlijning van 1 px, kleurvlakken
met 1-px-grenzen, schaduwbanden, een klein oog, rugvlekken als nette ovaaltjes en buikgroeven. Uitvoer: zelfde formaat
als v1 (192x96, giant_wailord.png + .pal). Gebruik: python3 tools/grounded/giant_wailord_draw.py [voorbeeld.png]"""
import sys
import numpy as np
from PIL import Image, ImageFilter

SRC = 'graphics/pokemon/wailord/overworld.png'
OUT = 'graphics/object_events/pics/misc/giant_wailord.png'
PAL = 'graphics/object_events/palettes/giant_wailord.pal'
W, H = 192, 96
SCALE = 4
WATERLINE = 0.72
# palet: 0 transparant, 1 omlijning, 2 donkerblauw (schaduw), 3 blauw, 4 lichtblauw, 5 highlight,
# 6 buik schaduw, 7 buik, 8 buik licht, 9 schuim, 10 oogwit, 11 vlek, 12 vlekrand
COLS = [(152, 208, 160), (24, 32, 56), (40, 88, 144), (64, 128, 192), (104, 160, 224), (160, 200, 240),
        (136, 160, 176), (184, 200, 216), (216, 232, 248), (240, 248, 255), (255, 255, 255), (200, 224, 248),
        (120, 168, 216), (0, 0, 0), (0, 0, 0), (0, 0, 0)]


def smooth_mask(m, scale, blur):
    im = Image.fromarray((m * 255).astype(np.uint8)).resize((m.shape[1] * scale, m.shape[0] * scale), Image.BILINEAR)
    im = im.filter(ImageFilter.GaussianBlur(blur))
    return np.array(im) > 127


def outline_of(mask):
    p = np.pad(mask, 1)
    inner = p[1:-1, 1:-1] & p[:-2, 1:-1] & p[2:, 1:-1] & p[1:-1, :-2] & p[1:-1, 2:]
    return mask & ~inner


def main():
    src = np.array(Image.open(SRC).crop((256, 0, 320, 64)))
    ys, xs = np.where(src != 0)
    src = src[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    body = smooth_mask(src != 0, SCALE, 3.4)
    h, w = body.shape
    yy, xx = np.mgrid[0:h, 0:w]
    top = np.where(body.any(0), body.argmax(0), h)
    bottom = np.where(body.any(0), h - 1 - body[::-1].argmax(0), 0)
    # buik: de onderste ±40% van het lijf, met een golvende bovenrand die naar de staart toe smaller wordt
    frac = 0.42 - 0.22 * np.clip((xx - w * 0.15) / (w * 0.6), 0, 1)
    belly = body & (yy >= bottom[None, :] - (bottom - top)[None, :] * frac) & (xx < w * 0.8)
    belly = smooth_mask(belly, 1, 1.2) & body
    cut = int(h * WATERLINE)
    a = np.zeros((h, w), np.uint8)
    # rug: banden van boven naar beneden (highlight smalle band bovenaan, dan licht, midden, schaduw onderaan)
    depth = yy - top[None, :]
    a[body] = 3
    a[body & (depth < 10)] = 4
    a[body & (depth < 4)] = 5
    a[body & (yy > cut - 14)] = 2
    a[belly] = 7
    a[belly & (yy > cut - 8)] = 6
    a[belly & (depth < 6)] = 8
    # buikgroeven: dunne lijnen schuin naar achteren
    for k in range(6):
        x0 = int(w * 0.12) + k * 9
        for t in range(14):
            x, y = x0 + t // 2, cut - 4 - t
            if 0 <= y < h and 0 <= x < w and belly[y, x]:
                a[y, x] = 6
    # grens rug/buik: 1 px donkerder
    a[outline_of(belly) & body & ~outline_of(body)] = 2
    # rugvlekken: kleine ovalen langs de rug
    for cx in np.linspace(w * 0.34, w * 0.70, 5):
        cx = int(cx); cy = int(top[cx]) + 8
        e = ((xx - cx) / 4.6) ** 2 + ((yy - cy) / 3.2) ** 2
        spot = (e <= 1) & body
        a[spot] = 11
        a[outline_of(spot) & body] = 12
    # oog: 4x3 donker met 1 px wit, en een wenkbrauwboogje
    ex = int(w * 0.17); ey = int(top[ex]) + 15
    a[ey:ey + 3, ex:ex + 4] = 1
    a[ey, ex + 2] = 10
    # bek: een licht gebogen lijn van de snuit naar achteren, net boven de buik
    for x in range(int(w * 0.03), int(w * 0.30)):
        t = (x - w * 0.03) / (w * 0.27)
        y = int(cut - 15 + 5 * t * t)
        if body[y, x]:
            a[y, x] = 2
    # borstvin: kleine driehoek die boven de waterlijn uitsteekt
    fx = int(w * 0.40)
    fin = (yy >= cut - 9) & (yy < cut) & (np.abs(xx - fx - (yy - (cut - 9)) * 1.4) <= (yy - (cut - 9)) * 0.9 + 1)
    a[fin & body] = 3
    a[outline_of(fin) & body] = 1
    # omlijning 1 px
    a[outline_of(body)] = 1
    a = a[:cut]
    canvas = np.zeros((H, W), np.uint8)
    x0 = (W - a.shape[1]) // 2
    y0 = H - 6 - a.shape[0]
    canvas[y0:y0 + a.shape[0], x0:x0 + a.shape[1]] = a
    # waterlijn: schuim van 1-2 px, licht golvend, iets breder dan het lijf
    row = canvas[y0 + a.shape[0] - 1]
    cols = np.where(row != 0)[0]
    lo, hi = cols.min() - 4, cols.max() + 4
    wl = y0 + a.shape[0]
    for x in range(lo, hi + 1):
        canvas[wl - 1, x] = 9
        if (x // 4) % 3 == 0:
            canvas[wl, x] = 9
    for x in range(lo - 8, hi + 9, 11):
        canvas[wl + 2, x:x + 3] = 9
    out = Image.fromarray(canvas, 'P')
    flat = [c for col in COLS for c in col]
    out.putpalette(flat + [0] * (768 - len(flat)))
    out.save(OUT)
    with open(PAL, 'w') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in COLS:
            f.write('%d %d %d\n' % c)
    print(OUT, a.shape)
    if len(sys.argv) > 1:
        rgb = np.array(out.convert('RGB')); rgb[canvas == 0] = (48, 120, 200)
        Image.fromarray(rgb).resize((W * 3, H * 3), Image.NEAREST).save(sys.argv[1])


if __name__ == '__main__':
    main()
