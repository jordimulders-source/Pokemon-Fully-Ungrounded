#!/usr/bin/env python3
"""Andes-primary (ronde 2): een omgebouwde kopie van de General-primary.

Zelfde tegelnummers, metatiles, gedrag en animaties (water, bloemen, watervallen) als General, zodat alles wat al
werkt blijft werken en Hoenn-secondaries erop passen. Anders:
- paletten omgekleurd: gras -> goudgele puna, Hoenn-zand -> lichte onverharde weg, mauve rotsbergen -> rode klei,
  bomen iets olijfgroener; de vaste 'grasindex' 15 van elk palet wordt de puna-grond;
- hoog gras -> ichu: alleen via het palet (de grastegel gebruikt de grondindexen);
- in ongebruikte General-metatiles (nergens op een kaart en niet in metatile_labels.h): een verre bergketen,
  lantaarn, bank en kantuta-bloemen (Bolivia's nationale bloem) in vrije tegels.

Gebruik: python3 tools/concept/tiles/andes_primary.py  ->  tilesets/eigen/andes_primary/
Andere scripts: `from andes_primary import build` geeft een r2lib.Pair met de primary al ingevuld.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from r2lib import load_set, recolor, Pair, Canvas
from tilelib import ellipse_mask

OUT = 'tilesets/eigen/andes_primary'
GRASS = (115, 197, 164)
PUNA = [(248, 232, 160), (216, 192, 112), (192, 160, 80), (168, 128, 48)]   # licht, basis, donker, donkerst
CLAY = [(248, 208, 176), (232, 168, 128), (200, 128, 96), (168, 96, 72), (128, 64, 56), (88, 48, 48)]
ROAD = [(248, 232, 192), (232, 208, 160), (208, 176, 128), (184, 144, 104)]
GREEN = [(192, 232, 128), (136, 184, 88), (64, 128, 56), (72, 64, 16)]
MTN = [(152, 152, 184), (112, 112, 152), (80, 80, 120)]

# vrije metatile-slots in General: nergens gebruikt en niet in metatile_labels.h
FREE_MTS = [0x0c, 0x23, 0x2a, 0x2e, 0x2f, 0x35, 0x46, 0x5c, 0x7e, 0x7f, 0x97, 0x9d, 0x9e, 0xa5, 0xa6, 0xad, 0xae,
            0xb5, 0xb7, 0xbd, 0xc5, 0xcd, 0xd7, 0xdb, 0xdc, 0xdd, 0xde, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0x10e, 0x10f,
            0x116, 0x117, 0x11e, 0x11f, 0x126, 0x127, 0x12e, 0x12f, 0x135, 0x136, 0x137, 0x13b, 0x13c, 0x13f, 0x143,
            0x144, 0x160, 0x161, 0x17f, 0x183, 0x187, 0x18b, 0x18c, 0x199, 0x1a2, 0x1b6, 0x1e3, 0x1ea, 0x1eb,
            0x1f8, 0x1f9]
TALL_GRASS = 0x0D


def palettes(g):
    P = [list(map(tuple, map(lambda c: tuple(int(v) for v in c), g['pals'][i]))) for i in range(6)]
    P = [recolor(p, {GRASS: PUNA[1]}) for p in P]
    P[2] = recolor(P[2], {1: GREEN[0], 2: GREEN[1], 3: GREEN[2], 4: GREEN[3],
                          12: PUNA[0], 13: PUNA[1], 14: PUNA[2], 15: PUNA[3]})
    P[3] = recolor(P[3], {6: PUNA[2], 7: PUNA[0], 9: CLAY[0], 10: CLAY[1], 11: CLAY[2], 12: CLAY[3], 13: CLAY[4],
                          14: CLAY[5]})
    P[4] = recolor(P[4], {3: MTN[0], 4: MTN[1], 5: MTN[2]})
    P[5] = recolor(P[5], {11: ROAD[0], 12: ROAD[1], 13: ROAD[2], 14: ROAD[3]})
    return P


def far_range(pair):
    """Verre besneeuwde keten (4 x 3), naadloos; kleuren uit palet 4 (sneeuw, ijsblauw, rotsgrijs)."""
    P4 = pair.pals[4]
    SN, SN2, SH = P4[1], P4[2], P4[3 + 8] if False else P4[11]
    RK = [MTN[0], MTN[1], MTN[2]]
    OL = P4[0]
    W_, H_ = 64, 48
    c = Canvas(W_, H_)
    peaks = [(16, 6), (44, 14)]
    for x in range(W_):
        def dist(p):
            return min(abs(x - p[0]), W_ - abs(x - p[0]))
        px_, py = min(peaks, key=lambda p: p[1] + dist(p))
        top = py + dist((px_, py))
        left = ((x - px_) % W_) >= W_ // 2
        for y in range(H_):
            if y < top:
                col = P4[11]  # heiige lucht/gletsjer achter de keten
            elif y == top:
                col = OL
            elif y < top + 9 + ((x // 3) % 3):
                col = SN if left else SN2
                if not left and (x + y) % 6 == 0:
                    col = SH
            else:
                col = RK[0] if left else RK[1]
                if (x - y) % 8 == 0 or ((x + 2 * y) % 13 == 0):
                    col = RK[1] if left else RK[2]
            if y > 44:
                col = None
            elif y == 44:
                col = OL
            if col is not None:
                c.px(x, y, col)
    return c


def lamp():
    c = Canvas(16, 32)
    gr = [(131, 131, 139), (98, 98, 123), (65, 74, 106), (41, 49, 90)]
    c.rect(5, 2, 10, 6, (255, 189, 131)); c.box(4, 1, 11, 7, gr[2]); c.hline(5, 10, 2, (255, 255, 255))
    c.hline(3, 12, 0, gr[2]); c.hline(4, 11, 0, gr[1])
    c.vline(7, 8, 28, gr[0]); c.vline(8, 8, 28, gr[1]); c.vline(6, 8, 28, gr[2]); c.vline(9, 8, 28, gr[2])
    c.rect(5, 27, 10, 30, gr[1]); c.box(4, 27, 11, 31, gr[2]); c.hline(5, 10, 28, gr[0])
    return c


def bench():
    c = Canvas(16, 16)
    w = [(222, 148, 115), (164, 98, 90), (106, 90, 90), (65, 57, 49)]
    c.rect(1, 4, 14, 6, w[0]); c.hline(1, 14, 6, w[1]); c.box(0, 3, 15, 7, w[3])
    c.rect(1, 9, 14, 10, w[0]); c.hline(1, 14, 11, w[1]); c.box(0, 8, 15, 12, w[3])
    for x in (2, 13):
        c.vline(x, 13, 14, w[3])
    return c


def kantuta():
    """Kantuta: hangende rood-gele kelkbloemen op een struikje (Bolivia's nationale bloem)."""
    c = Canvas(16, 16)
    g = GREEN
    c.mask_fill(ellipse_mask(8, 10, 6, 4), g[2])
    c.mask_fill(ellipse_mask(7, 9, 4, 2.5), g[1])
    for x, y in ((4, 9), (8, 7), (11, 10), (6, 12), (10, 13)):
        c.px(x, y, (205, 65, 82)); c.px(x, y + 1, (222, 106, 98)); c.px(x, y + 2, (255, 197, 148))
    c.outline(g[3])
    return c


def build():
    g = load_set('primary', 'general')
    pair = Pair(g['tiles'], g['mts'], g['attrs'], palettes(g))
    used = {int(e) & 0x3FF for e in g['mts'].flatten()}
    pair.free_prim = [t for t in range(1, 512) if t not in used]
    # ichu: de tegels van het hoge gras naar de goudtinten van palet 2 (grond)
    # hoog gras = ichu: de Hoenn-grastegel gebruikt al de grondindexen (12 licht, 13 basis, 15 sprieten) en 4
    # (omlijning); met het puna-palet wordt het vanzelf een goudgele pol. Geen pixelwijziging nodig.
    free = list(FREE_MTS)
    grass_ents = list(pair.pm[0x01][:4])  # gewone grond
    # verre bergketen (4 x 3)
    fr = far_range(pair)
    for my in range(3):
        for mx in range(4):
            s = fr.sub(mx * 16, my * 16, 16, 16)
            nm = f'andes_range_{mx}_{my}'
            if s.a[:, :, 3].all():
                pair.add_drawn(nm, s, pals=(4,), target='P', slot=free.pop(0))
            else:
                pair.add_drawn(nm, None, s, pals=(4,), target='P', slot=free.pop(0), bottom_ents=grass_ents)
    lp = lamp()
    pair.add_drawn('andes_lamp_0', None, lp.sub(0, 0, 16, 16), pals=(0, 1), layer='normal', target='P',
                   slot=free.pop(0), bottom_ents=grass_ents)
    pair.add_drawn('andes_lamp_1', None, lp.sub(0, 16, 16, 16), pals=(0, 1), target='P', slot=free.pop(0),
                   bottom_ents=grass_ents)
    pair.add_drawn('andes_bench', None, bench(), pals=(2,), target='P', slot=free.pop(0), bottom_ents=grass_ents)
    pair.add_drawn('andes_kantuta', None, kantuta(), pals=(2,), target='P', slot=free.pop(0), bottom_ents=grass_ents)
    pair.free_mts = free
    return pair


if __name__ == '__main__':
    from tilelib import render_repo_map  # noqa
    pair = build()
    pair.write(OUT, 'P')
    pair.sheet(list(range(512)), OUT + '/sheet.png')
    pair.palette_strip(range(6), OUT + '/paletten.png')
    print('vrije tegels over:', len(pair.free_prim), ' vrije metatiles over:', len(pair.free_mts))
    print('nieuw:', {k: hex(v) for k, v in pair.pnames.items()})
