#!/usr/bin/env python3
"""Project Grounded: het eerste deel van B_TRANSITION_DAVE (vóór de penalty): de tribune.

Een volle stadiontribune bij avond onder de lichtmasten. Een wave loopt over de onderste ring van links naar rechts,
gaat via de bocht over de bovenste ring terug, en op de laatste noot van de eerste riff gaat in het midden een groot
spandoek "DP PENNINGS" omhoog (vast op de klap). Op de volgende klap: close-up van het spandoek, dat wappert; op de
eerste noot van de tweede riff flitsen de camera's, dan zwart en de bestaande penalty (route_dave*, ongewijzigd).

De penalty loopt op de tweede riff (klok 192 = 225 frames na de eerste), dus deze film duurt precies DAVE_STADIUM (225)
frames. Muziek-ijkpunten (transitieframe t = muziekframe - DAVE_MUSIC_OFS): riffnoten t = 9, 31, 52, 80 (riff 1) en
206 (riff 2), klappen t = 9, 65, 122, 178.
Film (zie film.py): graphics/battle_transitions/film_dave_stadium*.
Gebruik: python3 tools/grounded/dave_stadium.py [voorbeeldmap] (dave_transition.py roept hem ook aan)
"""
import math, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
import film_art as fa
from film import W, H, text35, text35_width

LEN = 225
T_IN = 8
T_WAVE1 = 14      # onderste ring, links -> rechts
T_WAVE2 = 60      # bovenste ring, rechts -> links
T_WAVE_END = 112
T_BANNER = 80     # riffnoot 5: het spandoek gaat omhoog
T_UP = 122        # klap: helemaal op
T_CLOSE = 178     # klap: close-up
T_FLASH = 206     # riff 2, noot 1: flitsen
T_BLACK = 218     # zwart (de penalty-tiles worden geladen), penalty vanaf LEN

BLACK = (0, 0, 0)
WHITE = (248, 248, 248)
SKY = [(10, 14, 40), (18, 26, 64)]
STEEL = [(40, 44, 60), (86, 92, 110), (150, 156, 170)]
LIGHT = (255, 248, 200)
SKIN = [(248, 200, 160), (200, 140, 96), (120, 76, 48)]
HAIR = [(40, 28, 20), (200, 160, 60), (120, 60, 30)]
SHIRT = [(208, 40, 40), (40, 80, 200), (248, 208, 40), (240, 240, 240), (248, 128, 24), (40, 150, 70)]
SEAT = [(30, 34, 52), (50, 56, 80)]
GRASS = [(40, 120, 48), (56, 148, 60)]
CLOTH = [(248, 248, 240), (200, 200, 196)]
INK = (200, 24, 32)
AD = [(24, 32, 96), (248, 224, 40)]

LOW_Y = [70, 84, 98, 112]      # bovenkant van de rijen in de onderste ring (14 px per rij)
UP_Y = [28, 36, 44, 52]        # bovenste ring (8 px per rij)


def fan_low(a, x, y, k, stand):
    """Supporter onderste ring, 8 px breed. stand 0 zittend, 1 half, 2 staand met de armen omhoog."""
    shirt = SHIRT[(k * 7 + (k // 5)) % len(SHIRT)]
    skin = SKIN[(k * 3) % 3 if k % 4 else 1]
    hair = HAIR[(k * 5) % 3]
    dy = -3 * stand
    fa.rect(a, x + 1, y + 6 + dy, x + 7, y + 14, shirt)            # lijf
    fa.rect(a, x + 2, y + 1 + dy, x + 6, y + 6 + dy, skin)         # hoofd
    fa.rect(a, x + 2, y + 1 + dy, x + 6, y + 2 + dy, hair)
    fa.rect(a, x + 3, y + 3 + dy, x + 4, y + 4 + dy, BLACK)
    fa.rect(a, x + 5, y + 3 + dy, x + 6, y + 4 + dy, BLACK)
    if stand == 2:
        fa.rect(a, x + 0, y - 3 + dy, x + 1, y + 7 + dy, skin)     # armen omhoog
        fa.rect(a, x + 7, y - 3 + dy, x + 8, y + 7 + dy, skin)
    elif stand == 1:
        fa.rect(a, x + 0, y + 3 + dy, x + 1, y + 8 + dy, skin)
        fa.rect(a, x + 7, y + 3 + dy, x + 8, y + 8 + dy, skin)


def fan_up(a, x, y, k, stand):
    """Supporter bovenste ring, 4 px breed, 8 px hoog."""
    shirt = SHIRT[(k * 5 + 1) % len(SHIRT)]
    skin = SKIN[k % 3]
    dy = -2 * stand
    fa.rect(a, x, y + 4 + dy, x + 4, y + 8, shirt)
    fa.rect(a, x + 1, y + 1 + dy, x + 3, y + 4 + dy, skin)
    if stand == 2:
        fa.rect(a, x, y - 1 + dy, x + 1, y + 3 + dy, skin)
        fa.rect(a, x + 3, y - 1 + dy, x + 4, y + 3 + dy, skin)


def stand_of(d):
    d = abs(d)
    return 2 if d < 10 else (1 if d < 22 else 0)


def stadium(wave_low=None, wave_up=None, banner=0.0, flashes=()):
    a = fa.canvas(SKY[0])
    fa.rect(a, 0, 12, W, 26, SKY[1])
    # lichtmasten links en rechts
    for x0 in (14, 196):
        fa.rect(a, x0 + 13, 10, x0 + 17, 30, STEEL[1])
        fa.rect(a, x0, 0, x0 + 30, 12, STEEL[0])
        for i in range(4):
            for j in range(2):
                fa.rect(a, x0 + 2 + i * 7, 2 + j * 5, x0 + 7 + i * 7, 6 + j * 5, LIGHT)
    # dak / rand van de bovenste ring
    fa.rect(a, 0, 24, W, 27, STEEL[2])
    # bovenste ring
    fa.rect(a, 0, 27, W, 62, SEAT[0])
    for r, y in enumerate(UP_Y):
        for i in range(60):
            x = i * 4
            fan_up(a, x, y, i + r * 13, stand_of(x + 2 - wave_up) if wave_up is not None else 0)
    # reclameborden (geen echte merken)
    fa.rect(a, 0, 60, W, 70, AD[0])
    fa.rect(a, 0, 60, W, 61, STEEL[2])
    x = 4
    for s in ('TOP BINS', 'WINKELHAAK BV', 'TOP BINS', 'ROOF OF THE NET'):
        text35(lambda u, v: a.__setitem__((v, u), AD[1]) if 0 <= u < W else None, x, 63, s)
        x += text35_width(s) + 14
    # onderste ring
    fa.rect(a, 0, 70, W, 128, SEAT[1])
    for r, y in enumerate(LOW_Y):
        for i in range(30):
            x = i * 8
            fan_low(a, x, y, i * 3 + r * 11, stand_of(x + 4 - wave_low) if wave_low is not None else 0)
    if banner > 0:
        draw_banner(a, banner)
    # hek en veld
    fa.rect(a, 0, 126, W, 132, STEEL[1])
    for x in range(0, W, 6):
        fa.rect(a, x, 126, x + 1, 132, STEEL[2])
    fa.rect(a, 0, 132, W, H, GRASS[1])
    for x in range(0, W, 32):
        fa.rect(a, x, 132, x + 16, H, GRASS[0])
    for (fx, fy) in flashes:
        fa.rect(a, fx - 1, fy, fx + 2, fy + 1, WHITE)
        fa.rect(a, fx, fy - 1, fx + 1, fy + 2, WHITE)
    return a


BANNER_TXT = 'DP PENNINGS'


def draw_banner(a, up):
    """Spandoek tussen twee stokken; up = 0 (achter het hek) .. 1 (helemaal omhoog)."""
    bw = text35_width(BANNER_TXT, 3) + 16
    x0 = (W - bw) // 2
    top = int(round(128 - up * 54))
    h = 26
    for x in (x0 - 2, x0 + bw):                                   # stokken
        fa.rect(a, x, top - 4, x + 2, 132, STEEL[2])
    fa.rect(a, x0, top, x0 + bw, top + h, CLOTH[0])
    for x in range(x0 + 10, x0 + bw, 20):                         # plooien
        fa.rect(a, x, top, x + 2, top + h, CLOTH[1])
    fa.rect(a, x0, top + h - 2, x0 + bw, top + h, CLOTH[1])
    text35(lambda u, v: a.__setitem__((v, u), INK) if 0 <= v < H else None, x0 + 8, top + 6, BANNER_TXT, 3)
    # handen aan de stokken
    for x in (x0 - 4, x0 + bw - 2):
        fa.rect(a, x, top + h + 2, x + 6, top + h + 6, SKIN[1])


def closeup(phase, flash=False):
    """Close-up: het spandoek groot, wapperend (zinus per kolom), met de hoofden van de supporters eronder."""
    a = fa.canvas(SEAT[1])
    # vage menigte op de achtergrond (grote hoofden, 2x)
    for r, y in enumerate((8, 36)):
        for i in range(16):
            x = i * 16 - (8 if r else 0)
            k = i * 3 + r * 7
            fa.rect(a, x + 2, y + 12, x + 14, y + 28, SHIRT[(k * 7) % 6])
            fa.rect(a, x + 4, y + 2, x + 12, y + 12, SKIN[k % 3])
            fa.rect(a, x + 4, y + 2, x + 12, y + 4, HAIR[k % 3])
            fa.rect(a, x + 5, y + 6, x + 7, y + 8, BLACK)
            fa.rect(a, x + 9, y + 6, x + 11, y + 8, BLACK)
    sc = 5
    tw = text35_width(BANNER_TXT, sc)
    x0, y0, bw, bh = (W - tw) // 2 - 6, 44, tw + 12, 44
    cloth = fa.canvas(CLOTH[0])[:bh, :bw].copy()
    for x in range(8, bw, 26):
        cloth[:, x:x + 3] = CLOTH[1]
    text35(lambda u, v: cloth.__setitem__((v, u), INK), 6, 9, BANNER_TXT, sc)
    cloth[bh - 3:] = CLOTH[1]
    # wapperen: elke kolom een paar pixels op en neer (in stapjes van 2 px, dat ontdubbelt beter)
    for x in range(bw):
        dy = int(round(3 * math.sin(x * 0.045 + phase))) * 2
        col = cloth[:, x]
        for y in range(bh):
            yy = y0 + y + dy
            if 0 <= yy < H and 0 <= x0 + x < W:
                a[yy, x0 + x] = col[y]
    for x in (x0 - 4, x0 + bw):
        fa.rect(a, x, y0 - 8, x + 4, H, STEEL[2])
    # voorste rij hoofden die het spandoek vasthouden (3x)
    for i in range(6):
        x = 6 + i * 40
        k = i * 5 + 2
        fa.rect(a, x, 118, x + 30, H, SHIRT[(k * 7) % 6])
        fa.rect(a, x + 5, 96, x + 25, 120, SKIN[k % 3])
        fa.rect(a, x + 5, 96, x + 25, 102, HAIR[k % 3])
        fa.rect(a, x + 9, 106, x + 12, 109, BLACK)
        fa.rect(a, x + 18, 106, x + 21, 109, BLACK)
        fa.rect(a, x + 11, 112, x + 19, 117, (90, 20, 20))      # juichende mond
    if flash:
        rng = np.random.RandomState(int(phase * 10))
        for _ in range(10):
            fx, fy = rng.randint(4, W - 4), rng.randint(4, 40)
            fa.rect(a, fx - 2, fy, fx + 3, fy + 1, WHITE)
            fa.rect(a, fx, fy - 2, fx + 1, fy + 3, WHITE)
    return a


def build(preview=None):
    f = film.Film('dave_stadium')
    keys = [stadium(), stadium(100, 100, 1.0), closeup(0.0), closeup(1.0, True)]
    p = film.auto_palettes(keys, [BLACK, WHITE, INK], n_free=12)
    pal = [x[:15] for x in p]

    def ps(k=1.0, white=0.0):
        return f.palset(*[[fa.mix(fa.shade(c, k), WHITE, white) for c in q] for q in pal])

    f.ref = ps()
    rng = np.random.RandomState(12)
    still = keys[0]
    for t in range(T_IN):
        f.add(None, ps(0.0))
    for t in range(T_IN, T_WAVE1):
        f.add(still, ps((t - T_IN + 1) / (T_WAVE1 - T_IN)))
    STEP = 3
    for t in range(T_WAVE1, T_CLOSE, STEP):
        wl = wu = None
        if t < T_WAVE2 + 4:
            wl = -24 + (W + 48) * (t - T_WAVE1) / (T_WAVE2 + 4 - T_WAVE1)
        if T_WAVE2 - 4 <= t < T_WAVE_END:
            wu = W + 24 - (W + 48) * (t - T_WAVE2 + 4) / (T_WAVE_END - T_WAVE2 + 4)
        up = 0.0
        if t >= T_BANNER:
            u = min(1.0, (t - T_BANNER + 1) / (T_UP - T_BANNER))
            up = 1 - (1 - u) ** 2
        fl = ()
        # camera's flitsen op de klappen (t = 65, 122) en als het spandoek boven is
        if t in (65, 122, 149):
            fl = [(rng.randint(4, W - 4), rng.randint(30, 120)) for _ in range(8)]
        f.add(stadium(wl, wu, up, fl), f.ref, min(STEP, T_CLOSE - t))
    for t in range(T_CLOSE, T_BLACK, 4):
        fl = T_FLASH <= t < T_FLASH + 4
        f.add(closeup((t - T_CLOSE) * 0.5, fl), ps(1.0, 0.35 if fl else 0.0), min(4, T_BLACK - t))
    for t in range(T_BLACK, LEN):
        f.add(None, ps(0.0))
    assert len(f.frames) == LEN, len(f.frames)
    f.encode(preview)
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    f = build(d)
    if d:
        film.sheet(f.preview_frames, [12, 30, 50, 70, 90, 104, 124, 160, 180, 196, 207, 216],
                   os.path.join(d, 'dave_stadium_keys.png'))
