#!/usr/bin/env python3
"""Project Grounded: gevechtsintro van Wario (Yoshi's Island-fort en Battle Stadium). Jordi: "een stuk knoflook dat
opgegeten wordt en een grote geel-paars omlijnde W die in beeld komt, daarna Wario in diverse poses, met de W die
terugkomt en het beeld overneemt."

BG0 (paletten 13-15, gym_intro_lib.Encoder): een draaiende stralenkrans in geel en paars (index 1-8 van elk palet is
een fase, C laat ze rondgaan), daarop de knoflook (palet 14, drie hapstadia) en de W (palet 15, in drie maten: de W
komt terug en neemt het beeld over). Wario zelf is echte art: de drie GBA-poses (wario_bron, _flex_bron, _side_bron)
met Scale3x (3x) als groot object van 128 x 128 (vier 64x64-sprites, zoals het zwaard in legend_intros2.h).

Uitvoer: graphics/battle_transitions/wario_intro.png/.pal/_maps.bin en wario_poses.png/.pal.
Gebruik: python3 tools/grounded/wario_intro.py [voorbeeldmap]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import Encoder, preview_strip, OUT, KEY, gba, ROOT

PREVIEW = sys.argv[1] if len(sys.argv) > 1 else None

# fasen van de stralenkrans: index 1-8 in alle drie de paletten (codekleuren; C zet de echte kleuren)
PHASES = [(8 + i * 24, 200, 16 + i * 8) for i in range(8)]
GARLIC = [(248, 240, 216), (248, 248, 248), (208, 184, 224), (152, 112, 184), (200, 168, 112), (64, 32, 80),
          (232, 216, 176)]
WCOL = [(248, 224, 48), (248, 248, 160), (224, 160, 24), (128, 48, 168), (72, 16, 104), (32, 8, 40), (248, 248, 248)]
SECTORS = 16


def burst():
    """Fase per pixel: 16 sectoren rond het midden (fase = sector % 8), 4-voudig symmetrisch (gespiegelde tiles)."""
    yy, xx = np.mgrid[0:160, 0:240]
    ang = np.arctan2(yy - 79.5, xx - 119.5)
    sec = ((ang / (2 * math.pi) + 1) * SECTORS).astype(int) % SECTORS
    ph = sec % 8
    # spiegelen zodat linksboven de bron is
    ph[:, 120:] = ph[:, :120][:, ::-1]
    ph[80:] = ph[:80][::-1]
    a = np.zeros((160, 240, 3), np.uint8)
    for i in range(8):
        a[ph == i] = PHASES[i]
    return a


def garlic(im, bites):
    """Een knoflookbol (knoflook is geen Pokémon: met de hand getekend) met 0-3 happen eruit."""
    W, H = 240, 160
    mask = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(mask)
    cx, cy = 120, 84
    d.ellipse((cx - 44, cy - 34, cx + 44, cy + 40), fill=255)
    d.polygon([(cx - 22, cy - 26), (cx, cy - 58), (cx + 22, cy - 26)], fill=255)
    m = np.array(mask) > 0
    # happen: een cirkel met een kartelrand (tanden)
    bite_pos = [(cx + 40, cy - 26, 24), (cx - 44, cy + 6, 26), (cx + 12, cy + 2, 34)]
    yy, xx = np.mgrid[0:H, 0:W]
    eaten = np.zeros_like(m)
    for k in range(bites):
        bx, by, r = bite_pos[k]
        ang = np.arctan2(yy - by, xx - bx)
        rr = r + 3 * np.cos(ang * 9)          # tandafdrukken
        eaten |= (xx - bx) ** 2 + (yy - by) ** 2 < rr ** 2
    body = m & ~eaten
    a = im.copy()
    # kleur: crème met paarse teenlijnen
    a[body] = GARLIC[0]
    for x0 in (-26, -10, 8, 24):
        line = body & (np.abs(xx - (cx + x0 + (yy - cy) * 0.12 * np.sign(x0))) < 1.2) & (yy > cy - 30)
        a[line] = GARLIC[3]
    hl = body & ((xx - (cx - 18)) ** 2 / 100 + (yy - (cy - 12)) ** 2 / 300 < 1)
    a[hl] = GARLIC[1]
    shade = body & ((xx - cx) ** 2 / 44 ** 2 + (yy - cy - 18) ** 2 / 22 ** 2 > 1) & (yy > cy + 10)
    a[shade] = GARLIC[2]
    # binnenkant van de hap (het witte vruchtvlees langs de tandafdrukken)
    def grow(mm, n):
        g = mm.copy()
        for _ in range(n):
            g = g | np.roll(g, 1, 0) | np.roll(g, -1, 0) | np.roll(g, 1, 1) | np.roll(g, -1, 1)
        return g
    rim = body & grow(eaten, 2)
    a[rim] = GARLIC[6]
    a[body & grow(eaten, 1)] = GARLIC[1]
    # wortels (alleen zolang de onderkant er nog is)
    d2 = Image.fromarray(a)
    dd = ImageDraw.Draw(d2)
    for k in range(-3, 4):
        if body[cy + 38, cx + k * 6]:
            dd.line([(cx + k * 6, cy + 40), (cx + k * 8, cy + 50 + abs(k))], fill=GARLIC[4], width=1)
    a = np.array(d2)
    roots = (a == np.array(GARLIC[4])).all(2)
    solid = body | roots
    a[grow(solid, 1) & ~solid] = GARLIC[5]
    return a


def w_letter(im, scale, cy=80):
    """Wario's W: geel met een dikke paarse rand (en een zwarte buitenrand), geschaald rond het midden."""
    pts = [(-70, -42), (-38, -42), (-24, 10), (-10, -42), (10, -42), (24, 10), (38, -42), (70, -42), (40, 46),
           (12, 46), (0, 6), (-12, 46), (-40, 46)]
    P = [(120 + x * scale, cy + y * scale) for x, y in pts]
    img = Image.fromarray(im)
    d = ImageDraw.Draw(img)
    big = Image.new('L', (240, 160), 0)
    ImageDraw.Draw(big).polygon(P, fill=255)
    m = np.array(big) > 0
    a = np.array(img)

    def grow(mm, n):
        g = mm.copy()
        for _ in range(n):
            g = g | np.roll(g, 1, 0) | np.roll(g, -1, 0) | np.roll(g, 1, 1) | np.roll(g, -1, 1)
        return g
    o = max(2, int(5 * scale))
    a[grow(m, o + 2) & ~grow(m, o)] = WCOL[5]
    a[grow(m, o) & ~m] = WCOL[3]
    a[grow(m, max(1, o // 2)) & ~m] = WCOL[4] if scale > 3 else WCOL[3]
    a[m] = WCOL[0]
    # glans boven, schaduw onder
    yy, xx = np.mgrid[0:160, 0:240]
    top = m & (yy < cy + (-42 + 14) * scale) & ~np.roll(m, -int(3 * scale) - 1, 0)
    a[m & (yy < cy - 30 * scale)] = WCOL[1]
    a[m & (yy > cy + 34 * scale)] = WCOL[2]
    return a


def poses():
    """De drie GBA-poses met Scale3x (3x) in een 128x128-object; één palet van 15 kleuren."""
    from legend_intros2 import write_pal
    from guest_trainer_pics import scale3x
    srcs = ['wario_bron', 'wario_flex_bron', 'wario_side_bron']
    cols = []
    ims = []
    for n in srcs:
        a = np.array(Image.open(os.path.join(ROOT, 'graphics/grounded/trainers/guests/%s.png' % n)).convert('RGBA'))
        ims.append(a)
        for c in map(tuple, (a[a[:, :, 3] > 0][:, :3] >> 3 << 3)):
            if c not in cols:
                cols.append(c)
    assert len(cols) <= 15, len(cols)
    sheets = []
    for a in ims:
        idx = np.zeros(a.shape[:2], int)
        rgb = a[:, :, :3] >> 3 << 3
        for i, c in enumerate(cols):
            idx[(rgb == np.array(c)).all(2) & (a[:, :, 3] > 0)] = i + 1
        rgba = np.stack([idx, idx * 0, idx * 0, idx * 0 + 255], 2).astype(np.uint8)
        big = np.array(scale3x(Image.fromarray(rgba, 'RGBA')))[:, :, 0].astype(int)   # 3x, schuine randen netjes
        cols_used = np.where(big.any(0))[0]
        big = big[:, cols_used[0]:cols_used[-1] + 1]
        if big.shape[1] > 128:                                                          # de biceps: 129 breed
            big = big[:, (big.shape[1] - 128) // 2:(big.shape[1] - 128) // 2 + 128]
        canvas = np.zeros((128, 128), int)
        h, w = big.shape
        canvas[128 - h - 2:128 - 2, 64 - w // 2:64 - w // 2 + w] = big   # voeten onderaan
        sheets.append(np.concatenate([canvas[:64, :64], canvas[:64, 64:], canvas[64:, :64], canvas[64:, 64:]], 0))
    sheet = np.concatenate(sheets, 0).astype(np.uint8)
    im = Image.fromarray(sheet, 'P')
    pal = [(0, 0, 0)] + [tuple(int(v) for v in c) for c in cols] + [(0, 0, 0)] * (15 - len(cols))
    im.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    im.save(OUT + 'wario_poses.png')
    write_pal(OUT + 'wario_poses.pal', pal)
    return [np.array(pal, np.uint8)[s.reshape(-1, 64)] for s in sheets]


def main():
    b = burst()
    scenes = [('krans', b)]
    for k in range(4):
        scenes.append(('knoflook%d' % k, garlic(b, k)))
    for sc, lbl in ((1.0, 'w'), (2.2, 'w_groot'), (5.0, 'w_reus')):
        scenes.append((lbl, w_letter(b, sc)))
    enc = Encoder('intro', [PHASES, PHASES + GARLIC, PHASES + WCOL], prefix='wario_')
    imgs = []
    for lbl, a in scenes:
        im = Image.fromarray(a)
        enc.add(im, None, lbl)
        imgs.append(im)
    enc.save()
    p = poses()
    if PREVIEW:
        preview_strip(imgs, os.path.join(PREVIEW, 'wario_intro.png'), k=2, cols=4)


if __name__ == '__main__':
    main()
