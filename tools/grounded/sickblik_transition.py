#!/usr/bin/env python3
"""Project Grounded: graphics voor B_TRANSITION_SICKBLIK (Jordi's eigen gevecht: hotpot wordt Poké Ball).

Idee van Jordi: een grote tafel met een Chinese yin-yang-hotpot (rode mala-bouillon en witte bouillon), borden vol
ingrediënten en biertjes; je kijkt erop alsof je er zelf aan zit. Dan switcht de camera naar een bovenaanzicht en de
hotpot verandert langzaam in een Poké Ball (de kleuren kloppen al): de S-scheiding trekt recht tot de zwarte band, de
pan-rand wordt de zwarte buitenrand, de ingrediënten zinken weg en een blokje tofu drijft naar het midden en wordt de knop.

Twee beelden op BG0, drie BG-paletten (13, 14, 15; per tile één palet, automatisch gekozen):
- Beeld 1 (aan tafel): één tileset (<= 767 tiles) en één tilemap. Stoom en bubbels zijn kleuren die per stap van een
  korte kleurcyclus (SB_CYCLE paletsets) wisselen.
- Beeld 2 (bovenaanzicht): SB_KEYS sleutelbeelden van de morph. Tiles die in alle sleutelbeelden gelijk zijn (de tafel en
  borden eromheen) staan vast in VRAM; de rest (de pan) wordt per sleutelbeeld in één van twee buffers geladen (om en om,
  zodat nooit een buffer wordt overschreven die nog in beeld is). Per sleutelbeeld ook een eigen paletset: het metaal
  wordt zwart, de bouillon Poké Ball-rood/wit en de tafel eromheen dimt. Geen rekenwerk in de game: alles staat in tabellen.

Uitvoer:
- graphics/battle_transitions/sickblik_*.bin (ruwe 4bpp-tiles, tilemaps, BGR555-paletten)
- src/data/sickblik_transition.h (aantallen en de tabel met dynamische tiles per sleutelbeeld)
Gebruik: python3 tools/grounded/sickblik_transition.py [voorbeeldmap]   (voorbeeldmap: vergrote PNG's)
"""
import math, os, random, struct, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT = os.path.join(ROOT, 'graphics/battle_transitions/')
HDR = os.path.join(ROOT, 'src/data/sickblik_transition.h')
W, H = 240, 160
SB_CYCLE = 3          # stappen in de kleurcyclus van beeld 1 (stoom stijgt, bubbels)
SB_KEYS = 30          # sleutelbeelden van de morph (beeld 2)
MAX_TILES = 767       # BG0-tiles die vrij zijn (lessen: ±767)

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0 + 1 / 32.0

# ---------------------------------------------------------------- kleuren (8-bit RGB; worden 5-bit in de game)
C = {
    'out': (40, 22, 18),
    # kamer
    'wall_d': (78, 18, 20), 'wall': (112, 28, 26), 'paper': (236, 190, 112), 'gold': (232, 176, 56),
    'lan': (214, 42, 32), 'lan_d': (140, 22, 22), 'shine': (250, 246, 236),
    # tafel
    'wdd': (80, 42, 24), 'wd': (118, 64, 34), 'wm': (154, 90, 48), 'wl': (186, 120, 66),
    # pan
    'md': (72, 76, 86), 'mm': (138, 144, 156), 'ml': (204, 210, 218),
    'rd': (126, 20, 16), 'rm': (194, 40, 24), 'rl': (240, 104, 44),
    'cream_d': (204, 188, 156), 'cream': (238, 228, 202), 'white': (252, 252, 246),
    'green': (72, 152, 56), 'pink': (232, 128, 124),
    # eten en bier
    'porc': (190, 204, 220), 'blue': (52, 92, 176), 'meat': (220, 92, 98), 'meat_d': (156, 42, 54),
    'orange': (248, 138, 62), 'g_d': (26, 86, 46), 'g_m': (62, 146, 66), 'g_l': (150, 210, 98),
    'amber': (236, 172, 40), 'tofu': (246, 236, 204),
}
# kleuren met een cyclus (beeld 1): per stap een eigen RGB
WALL = C['wall']


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


STEAM_LV = [0.80, 0.55, 0.32]          # helder, half, vaag; de band schuift elke stap een plek omhoog
ANIM = {}
for k in range(3):
    ANIM['s%d' % k] = [mix(WALL, (255, 238, 232), STEAM_LV[(k + f) % 3]) for f in range(SB_CYCLE)]
ANIM['rbubA'] = [(255, 172, 120), C['rl'], C['rm']]
ANIM['rbubB'] = [C['rm'], (255, 172, 120), C['rl']]
ANIM['wbub'] = [C['white'], C['cream_d'], C['cream']]
for k, v in ANIM.items():
    C[k] = v[0]

# paletten van beeld 1 (index 1..15; index 0 ongebruikt)
PAL1 = {
    13: ['out', 'wall_d', 'wall', 'paper', 'gold', 'lan', 'lan_d', 'wdd', 'wd', 'wm', 'wl', 'shine', 's0', 's1', 's2'],
    14: ['out', 'wd', 'wm', 'wl', 'white', 'porc', 'blue', 'meat', 'meat_d', 'orange', 'tofu', 'g_d', 'g_m', 'g_l', 'amber'],
    15: ['out', 'wd', 'wm', 'md', 'mm', 'ml', 'rd', 'rm', 'rl', 'cream_d', 'cream', 'white', 'rbubA', 'rbubB', 'wbub'],
}
# paletten van beeld 2
PAL2 = {
    13: ['out', 'wd', 'wm', 'wl', 'white', 'porc', 'blue', 'meat', 'meat_d', 'orange', 'tofu', 'wdd', 'amber', 'g_m', 'cream'],
    14: ['out', 'wd', 'wm', 'wl', 'white', 'porc', 'blue', 'g_d', 'g_m', 'g_l', 'tofu', 'amber', 'gold', 'cream_d', 'meat_d'],
    15: ['out', 'wd', 'wm', 'wl', 'md', 'mm', 'ml', 'rd', 'rm', 'rl', 'cream_d', 'cream', 'white', 'green', 'pink'],
}
NAMES = sorted(C)
ID = {n: i for i, n in enumerate(NAMES)}


def gba(c):
    return tuple((v >> 3) << 3 for v in c)


def bgr555(c):
    return (c[0] >> 3) | ((c[1] >> 3) << 5) | ((c[2] >> 3) << 10)


# ---------------------------------------------------------------- tekenhulpjes
YY, XX = np.mgrid[:H, :W]
PX, PY = XX + 0.5, YY + 0.5


class Canvas:
    def __init__(self, color):
        self.a = np.full((H, W), ID[color], np.int16)

    def put(self, mask, color):
        self.a[mask] = ID[color]

    def get(self, name):
        return self.a == ID[name]


def ell(cx, cy, rx, ry):
    return ((PX - cx) / rx) ** 2 + ((PY - cy) / ry) ** 2 <= 1.0


def draw_mask(fn):
    im = Image.new('L', (W, H), 0)
    fn(ImageDraw.Draw(im))
    return np.array(im) > 0


def edge(mask):
    return mask & ~nd.binary_erosion(mask)


def outlined(cv, mask, color, line='out'):
    cv.put(mask, color)
    cv.put(edge(mask), line)


# ---------------------------------------------------------------- beeld 1: aan tafel
def lantern(cv, cx):
    cv.put((np.abs(PX - cx) < 1) & (PY < 6), 'out')
    cv.put((np.abs(PX - cx) < 6) & (PY >= 6) & (PY < 9), 'gold')
    body = ell(cx, 19, 12, 10)
    outlined(cv, body, 'lan', 'lan_d')
    for off in (-7, 0, 7):                           # ribben
        rib = body & (np.abs(PX - (cx + off * np.sqrt(np.clip(1 - ((PY - 19) / 10) ** 2, 0, 1)))) < 0.6)
        cv.put(rib, 'lan_d')
    cv.put(ell(cx - 5, 15, 2.5, 3.5) & body, 'shine')
    cv.put((np.abs(PX - cx) < 6) & (PY >= 28) & (PY < 31), 'gold')
    for dx in (-2, 0, 2):                            # kwastje
        cv.put((np.abs(PX - (cx + dx)) < 0.6) & (PY >= 31) & (PY < 40 - abs(dx)), 'gold')


def lattice(cv, x0, x1, y0, y1):
    box = (PX > x0) & (PX < x1) & (PY > y0) & (PY < y1)
    cv.put(box, 'wdd')
    inner = (PX > x0 + 2) & (PX < x1 - 2) & (PY > y0 + 2) & (PY < y1 - 2)
    cv.put(inner, 'paper')
    grid = inner & ((XX % 8 == 0) | (YY % 8 == 0))
    cv.put(grid, 'wdd')
    # klassiek Chinees raam: kleine kruisjes in elk vak
    cv.put(inner & (XX % 8 == 4) & (YY % 8 == 4), 'gold')
    cv.put(edge(box), 'out')


def plate(cv, cx, cy, rx, ry):
    cv.put(ell(cx + 1, cy + 3, rx, ry), 'wd')             # schaduw
    m = ell(cx, cy, rx, ry)
    cv.put(m, 'white')
    cv.put(m & ~ell(cx, cy + 1, rx - 3, ry - 2), 'porc')
    cv.put(edge(m), 'blue')
    cv.put(m & ~ell(cx, cy, rx - 1, ry - 1) & (PY > cy), 'out')


def beef_plate(cv, cx, cy):
    plate(cv, cx, cy, 32, 13)
    for r, (oy, n) in enumerate(((-6, 4), (-1, 5), (5, 4))):
        for i in range(n):
            x = cx - (n - 1) * 6 + i * 12 + (r % 2)
            y = cy + oy
            m = ell(x, y, 6, 3.4)
            outlined(cv, m, 'meat', 'meat_d')
            # vetmarmer: twee witte streepjes
            cv.put(m & (np.abs((PY - y) - 0.5 * np.sin((PX - x) * 1.1)) < 0.5) & (np.abs(PX - x) < 4), 'white')
            cv.put(m & (np.abs(PX - x - 2 - (PY - y)) < 0.5), 'tofu')


def shrimp_plate(cv, cx, cy):
    plate(cv, cx, cy, 32, 13)
    for i, (dx, dy) in enumerate(((-18, -5), (-6, -6), (6, -5), (18, -6), (-12, 4), (0, 4), (12, 4))):
        x, y = cx + dx, cy + dy
        d = np.hypot((PX - x) / 1.25, PY - y)
        ring = (d < 5.2) & (d > 1.8) & ~((PX > x + 1) & (PY > y - 1))      # C-vorm
        cv.put(ring, 'orange')
        cv.put(edge(ring), 'meat_d')
        cv.put(ring & (np.abs(np.arctan2(PY - y, PX - x) * 3 % 1.0 - 0.5) < 0.12), 'tofu')   # segmenten
        cv.put(ell(x + 4, y + 2, 1.6, 1.2), 'meat_d')                       # staartje


def tofu_plate(cv, cx, cy):
    plate(cv, cx, cy, 22, 9)
    for dx, dy in ((-11, -2), (-4, -3), (3, -2), (-8, 3)):
        x, y = cx + dx, cy + dy
        top = (np.abs(PX - x) < 3) & (PY > y - 2) & (PY < y + 1)
        side = (np.abs(PX - x) < 3) & (PY >= y + 1) & (PY < y + 3)
        cv.put(top, 'white'); cv.put(side, 'tofu'); cv.put(edge(top | side), 'porc')
    for dx, dy in ((10, -1), (15, 2), (7, 3)):                              # shiitake
        x, y = cx + dx, cy + dy
        cap = ell(x, y, 4, 2.6)
        outlined(cv, cap, 'wd', 'out')
        cv.put(cap & (np.abs(PX - x) < 0.6) & (np.abs(PY - y) < 1.5), 'wl')


def greens_plate(cv, cx, cy):
    plate(cv, cx, cy, 22, 9)
    for dx, dy, a in ((-12, 0, -0.5), (-5, -2, -0.2), (3, -2, 0.2), (10, 0, 0.5), (-2, 2, 0)):
        x, y = cx + dx, cy + dy
        leaf = ((((PX - x) * np.cos(a) + (PY - y) * np.sin(a)) / 5.5) ** 2 + ((-(PX - x) * np.sin(a) + (PY - y) * np.cos(a)) / 3) ** 2) <= 1
        outlined(cv, leaf, 'g_m', 'g_d')
        cv.put(leaf & (np.abs((PY - y) - (PX - x) * np.tan(a)) < 0.5) & (np.abs(PX - x) < 4), 'g_l')
    # bundeltje enoki
    for i in range(5):
        cv.put((np.abs(PX - (cx + 14 + i)) < 0.5) & (PY > cy - 6 + (i % 2)) & (PY < cy + 2), 'tofu')
        cv.put(ell(cx + 14 + i, cy - 6 + (i % 2), 0.8, 0.8), 'white')


def bottle(cv, cx, top):
    neck = (np.abs(PX - cx) < 3) & (PY > top + 3) & (PY < top + 24)
    shoulder = draw_mask(lambda d: d.polygon([(cx - 3, top + 22), (cx + 3, top + 22), (cx + 7, top + 34), (cx - 7, top + 34)], fill=1))
    body = (np.abs(PX - cx) < 7) & (PY >= top + 33)
    m = neck | shoulder | body
    outlined(cv, m, 'g_m', 'g_d')
    cv.put(m & (np.abs(PX - (cx - 3)) < 0.6) & (PY > top + 6), 'g_l')      # glans
    cv.put(m & (PX > cx + 3) & (PY > top + 30), 'g_d')
    cv.put((np.abs(PX - cx) < 4) & (PY > top) & (PY <= top + 3), 'amber')   # dop
    cv.put(edge((np.abs(PX - cx) < 4) & (PY > top) & (PY <= top + 3)), 'out')
    lab = (np.abs(PX - cx) < 6) & (PY > top + 46) & (PY < top + 60)
    cv.put(lab, 'white')
    cv.put(lab & (PY > top + 51) & (PY < top + 55), 'meat_d')               # rood bandje, geen merk
    cv.put(lab & (np.abs(PX - cx) < 2) & (np.abs(PY - (top + 49)) < 1), 'amber')
    cv.put(edge(lab), 'g_d')


def glass(cv, x0, y0, x1, y1):
    m = draw_mask(lambda d: d.polygon([(x0, y0), (x1, y0), (x1 - 1, y1), (x0 + 1, y1)], fill=1))
    cv.put(m, 'amber')
    cv.put(m & (PY < y0 + 5), 'white')                                       # schuimkraag
    cv.put(m & (PY >= y0 + 5) & (PY < y0 + 6), 'tofu')
    cv.put(m & (np.abs(PX - (x0 + 2.5)) < 0.6) & (PY > y0 + 7), 'tofu')      # glans
    cv.put(m & (PX > x1 - 3) & (PY > y0 + 6), 'orange')
    cv.put(edge(m), 'out')
    rng = random.Random(x0)
    for _ in range(4):                                                       # belletjes
        bx, by = rng.uniform(x0 + 3, x1 - 3), rng.uniform(y0 + 8, y1 - 3)
        cv.put(ell(bx, by, 0.7, 0.7) & m, 'tofu')


def pot_side(cv, cx, cy, rx, ry, depth):
    lower = cy + ry * np.sqrt(np.clip(1 - ((PX - cx) / rx) ** 2, 0, 1))
    body = (np.abs(PX - cx) < rx) & (PY >= cy) & (PY < lower + depth)
    cv.put(body, 'mm')
    u = (PX - cx) / rx
    cv.put(body & (u > 0.45), 'md')
    cv.put(body & (u < -0.55) & (u > -0.75), 'ml')
    cv.put(body & (PY > lower + depth - 2), 'md')
    cv.put(edge(body), 'out')
    return body


def yinyang_boundary(u, a=1.0):
    """S-grens (genormaliseerd, straal 1): links bolt omhoog, rechts omlaag; rood ligt erboven."""
    left = u < 0
    out = np.where(left, -np.sqrt(np.clip(0.25 - (u + 0.5) ** 2, 0, None)), np.sqrt(np.clip(0.25 - (u - 0.5) ** 2, 0, None)))
    return out * a


def pot_perspective(cv):
    cx, cy, rx, ry = 120, 86, 62, 25
    cv.put(ell(cx + 2, cy + 18, rx + 4, ry + 4) & (PY > cy + 8), 'wdd')     # schaduw op tafel
    pot_side(cv, cx, cy, rx, ry, 11)
    # oortjes
    for s in (-1, 1):
        h = ell(cx + s * (rx + 3), cy + 6, 4, 3) & ~ell(cx + s * (rx + 3), cy + 6, 2, 1.4)
        cv.put(h, 'mm'); cv.put(edge(h), 'out')
    rim = ell(cx, cy, rx, ry)
    cv.put(rim, 'ml')
    cv.put(rim & (PY > cy + ry - 3), 'mm')
    cv.put(edge(rim), 'out')
    cv.put(ell(cx, cy, rx - 4, ry - 3), 'md')                                # binnenwand achter
    bx, by, brx, bry = cx, cy + 3, rx - 5, ry - 6
    broth = ell(bx, by, brx, bry) & ell(cx, cy, rx - 4, ry - 3)
    u = (PX - bx) / brx
    v = (PY - by) / bry
    f = yinyang_boundary(u)
    # afstand tot de S in genormaliseerde ruimte (benadering: verticaal, met helling gecorrigeerd)
    red = broth & (v < f)
    white = broth & ~red
    cv.put(red, 'rm')
    cv.put(white, 'cream')
    rng = np.random.default_rng(7)
    noise = nd.gaussian_filter(rng.random((H, W)), 2.2)
    cv.put(red & (noise < np.percentile(noise, 22)), 'rd')
    oil = nd.gaussian_filter(rng.random((H, W)), 1.0)
    cv.put(red & (oil > np.percentile(oil, 91)), 'rl')
    cv.put(white & (noise > np.percentile(noise, 80)), 'cream_d')
    # scheiding: een metalen wandje langs de S (bovenrand licht, eronder donker)
    sampled = []
    for t in np.linspace(-1, 1, 400):
        sampled.append((bx + t * brx, by + float(yinyang_boundary(np.array([t]))[0]) * bry))
    sampled = np.array(sampled)
    d = np.full((H, W), 99.0)
    for sx, sy in sampled[::2]:
        d = np.minimum(d, np.hypot(PX - sx, (PY - sy) * 1.6))
    wall = broth & (d < 1.9)
    cv.put(wall, 'ml')
    cv.put(wall & (PY > np.interp(PX, sampled[:, 0], sampled[:, 1]) + 0.3), 'mm')
    # ingrediënten
    R = random.Random(11)
    for _ in range(9):                                                       # pepers
        x, y = R.uniform(bx - 50, bx + 50), R.uniform(by - 15, by + 12)
        m = ell(x, y, 3.2, 1.2) & red & (d > 3)
        cv.put(m, 'rl'); cv.put(m & (PY > y + 0.3), 'rd')
    for _ in range(14):                                                      # Sichuan-peper
        x, y = R.uniform(bx - 50, bx + 50), R.uniform(by - 15, by + 12)
        cv.put(ell(x, y, 0.9, 0.7) & red & (d > 3), 'out')
    for _ in range(3):                                                       # vlees
        x, y = R.uniform(bx - 6, bx + 40), R.uniform(by - 14, by - 4)
        m = ell(x, y, 5, 2) & red & (d > 3)
        cv.put(m, 'cream_d'); cv.put(m & (np.abs(PY - y) < 0.5), 'cream')
    for x, y in ((bx - 34, by + 6), (bx - 18, by + 10), (bx + 4, by + 9), (bx - 42, by - 1)):   # tofu
        top = (np.abs(PX - x) < 3) & (PY > y - 2) & (PY < y + 0.5) & white & (d > 3)
        side = (np.abs(PX - x) < 3) & (PY >= y + 0.5) & (PY < y + 2) & white & (d > 3)
        cv.put(top, 'white'); cv.put(side, 'cream_d')
    for x, y in ((bx - 26, by + 3), (bx + 18, by + 11), (bx - 8, by + 12)):    # paddenstoelen
        m = ell(x, y, 3.5, 1.8) & white & (d > 3)
        cv.put(m, 'wm'); cv.put(edge(m), 'wd')
    for _ in range(6):                                                       # goji
        x, y = R.uniform(bx - 46, bx + 30), R.uniform(by + 2, by + 13)
        cv.put(ell(x, y, 0.9, 0.7) & white & (d > 3), 'rl')
    # bubbels (kleurcyclus)
    for i in range(10):
        x, y = R.uniform(bx - 48, bx + 48), R.uniform(by - 14, by + 12)
        ring = ell(x, y, 2.2, 1.3) & ~ell(x, y, 1.0, 0.6)
        cv.put(ring & red & (d > 3), 'rbubA' if i % 2 else 'rbubB')
        cv.put(ring & white & (d > 3), 'wbub')
    return broth


def steam(cv):
    """Drie stoomslierten die uitwaaieren; de kleurcyclus laat de lichte banden omhoog schuiven."""
    for k, (x0, ph, amp) in enumerate(((103, 0.0, 4.0), (121, 2.1, 5.5), (139, 4.0, 4.0))):
        h = (55 - PY)                                   # hoogte boven de pan
        cxs = x0 + amp * np.sin(PY / 9.0 + ph) + (k - 1) * h * 0.12
        width = 1.8 + h / 8.0
        core = np.abs(PX - cxs) / width
        m = (core < 1) & (PY < 55) & (PY > 2 + k * 4)
        # rand en bovenkant uitdunnen (dither)
        fade = np.clip(core * 0.9 + h / 70.0, 0, 1)
        m &= BAYER[YY % 4, XX % 4] > fade - 0.25
        band = ((YY // 3) + k) % 3
        for b in range(3):
            cv.put(m & (band == b), 's%d' % b)


def scene_table():
    cv = Canvas('wall')
    cv.put((YY >= 42) & (YY < 52), 'wdd')                                    # lambrisering
    cv.put(YY == 42, 'wd')
    cv.put((YY >= 43) & (YY < 52) & (XX % 16 == 0), 'out')
    lattice(cv, 7, 57, 7, 37)
    lattice(cv, 183, 233, 7, 37)
    lantern(cv, 76)
    lantern(cv, 164)
    # tafel: planken, in perspectief steeds breder
    cv.put(YY >= 52, 'wm')
    cv.put(YY == 52, 'wl')
    cv.put(YY == 53, 'wl')
    seams = [59, 67, 77, 89, 103, 119, 137, 157]
    prev = 54
    for i, s in enumerate(seams):
        cv.put(YY == s, 'wd')
        cv.put(YY == s + 1, 'wl')
        mid = (prev + s) // 2
        cv.put((YY == mid) & (((XX + i * 5) % 16) < 6), 'wd')                # nerf
        cv.put((YY == mid + 2) & (((XX + i * 9 + 8) % 16) < 3) & (YY < s), 'wl')
        prev = s + 2
    steam(cv)
    # borden en bier
    tofu_plate(cv, 40, 71)
    greens_plate(cv, 200, 71)
    pot_perspective(cv)
    beef_plate(cv, 54, 141)
    shrimp_plate(cv, 186, 141)
    glass(cv, 87, 130, 98, 153)
    glass(cv, 142, 130, 153, 153)
    # eigen kommetje met sesamsaus en eetstokjes
    bowl = ell(120, 147, 18, 7)
    cv.put(bowl, 'white'); cv.put(ell(120, 146, 15, 4.5), 'wm')
    cv.put(ell(120, 146, 15, 4.5) & (BAYER[YY % 4, XX % 4] > 0.88), 'g_m')
    cv.put(edge(bowl), 'blue')
    for y in (155.5, 158.5):
        sticks = (np.abs(PY - y) < 1.0) & (PX > 92) & (PX < 150)
        cv.put(sticks, 'out'); cv.put(sticks & (PY < y), 'meat_d')       # zwart gelakt, rode punt
        cv.put(sticks & (PX < 99), 'amber')
    bottle(cv, 9, 70)
    bottle(cv, 231, 70)
    return cv


# ---------------------------------------------------------------- beeld 2: bovenaanzicht + morph
CX2, CY2, R2 = 120, 80, 60


def smooth(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def top_static():
    cv = Canvas('wm')
    for i, s in enumerate((4, 28, 52, 76, 100, 124, 148)):
        cv.put(YY == s, 'wd')
        cv.put(YY == s + 1, 'wl')
        cv.put((YY == s + 9) & (((XX + i * 7) % 16) < 6), 'wd')
        cv.put((YY == s + 16) & (((XX + i * 11) % 16) < 4), 'wl')

    def tplate(cx, cy, r):
        cv.put(np.hypot(PX - cx - 2, PY - cy - 3) < r, 'wd')
        m = np.hypot(PX - cx, PY - cy) < r
        cv.put(m, 'white')
        cv.put(m & (np.hypot(PX - cx, PY - cy) > r - 6), 'porc')
        cv.put(edge(m), 'blue')
        return m
    R = random.Random(3)
    # linksonder: rundvlees (bij de speler), rechtsonder: garnalen, boven: tofu/paddenstoel en groente
    m = tplate(20, 146, 40)
    for i in range(12):
        x, y = R.uniform(0, 46), R.uniform(118, 160)
        s = ell(x, y, 7, 4) & m
        outlined(cv, s, 'meat', 'meat_d')
        cv.put(s & (np.abs(PY - y - 0.6 * np.sin(PX - x)) < 0.5), 'white')
    m = tplate(220, 146, 40)
    for i in range(10):
        x, y = R.uniform(194, 240), R.uniform(118, 160)
        d = np.hypot(PX - x, PY - y)
        ring = (d < 5) & (d > 2) & ~((PX > x) & (PY < y)) & m
        cv.put(ring, 'orange'); cv.put(edge(ring), 'meat_d')
    m = tplate(18, 14, 36)
    for i in range(7):
        x, y = R.uniform(0, 42), R.uniform(0, 38)
        sq = (np.abs(PX - x) < 4) & (np.abs(PY - y) < 4) & m
        cv.put(sq, 'tofu'); cv.put(edge(sq), 'porc')
    for i in range(4):
        x, y = R.uniform(4, 40), R.uniform(2, 36)
        c = np.hypot(PX - x, PY - y) < 4.5
        cv.put(c & m, 'wd'); cv.put(c & m & ((np.abs(PX - x) < 0.6) | (np.abs(PY - y) < 0.6)), 'wl')
    m = tplate(222, 14, 36)
    for i in range(8):
        x, y = R.uniform(198, 240), R.uniform(0, 38)
        a = R.uniform(0, math.pi)
        leaf = ((((PX - x) * math.cos(a) + (PY - y) * math.sin(a)) / 7) ** 2 + ((-(PX - x) * math.sin(a) + (PY - y) * math.cos(a)) / 3.5) ** 2) <= 1
        outlined(cv, leaf & m, 'g_m', 'g_d')
    # bierglas (bovenaanzicht: schuimkraag) en flesje (dop)
    g = np.hypot(PX - 22, PY - 82) < 11
    cv.put(g, 'amber'); cv.put(g & (np.hypot(PX - 22, PY - 82) < 8.5), 'white')
    cv.put(g & (np.hypot(PX - 20, PY - 80) < 3), 'tofu'); cv.put(edge(g), 'out')
    b = np.hypot(PX - 218, PY - 82) < 9
    cv.put(b, 'g_m'); cv.put(b & (np.hypot(PX - 218, PY - 82) < 5), 'gold')
    cv.put(b & (np.hypot(PX - 216, PY - 80) < 1.5), 'g_l'); cv.put(edge(b), 'g_d')
    # eetstokjes onderaan rechts van de pan
    for y in (151.5, 154.5):
        s = (np.abs(PY - y) < 1.0) & (PX > 150) & (PX < 192)
        cv.put(s, 'wl'); cv.put(s & (PY > y), 'wd'); cv.put(s & (PX > 186), 'meat_d')
    return cv


def make_ingredients():
    R = random.Random(21)
    ing = []
    Ri = R2 - 6
    while len(ing) < 46:
        x, y = R.uniform(-Ri, Ri), R.uniform(-Ri, Ri)
        if math.hypot(x, y) > Ri - 6:
            continue
        f = float(yinyang_boundary(np.array([x / Ri]))[0]) * Ri
        if abs(y - f) < 7:
            continue
        red = y < f
        kind = R.choice(['chili', 'chili', 'pepper', 'pepper', 'meat']) if red else R.choice(['tofu', 'mush', 'goji', 'goji', 'scallion', 'enoki'])
        ing.append(dict(x=x, y=y, red=red, kind=kind, start=R.uniform(0.0, 0.32), a=R.uniform(0, math.pi)))
    return ing


INGREDIENTS = make_ingredients()


def draw_ingredient(cv, g, s, inside):
    """s = 0 (drijft) .. 1 (gezonken). Zinken = kleiner worden en via dither verdwijnen."""
    if s >= 1:
        return
    x, y = CX2 + g['x'], CY2 + g['y']
    k = 1 - 0.45 * s
    vis = inside & (BAYER[YY % 4, XX % 4] > s * 1.05)
    a = g['a']
    rot = lambda rx, ry: ((((PX - x) * math.cos(a) + (PY - y) * math.sin(a)) / rx) ** 2 + ((-(PX - x) * math.sin(a) + (PY - y) * math.cos(a)) / ry) ** 2) <= 1
    if g['kind'] == 'chili':
        m = rot(6 * k, 2.2 * k) & vis
        cv.put(m, 'rl'); cv.put(edge(m), 'rd')
        cv.put(m & (np.hypot(PX - x - 5 * k * math.cos(a), PY - y - 5 * k * math.sin(a)) < 1.5), 'green')
    elif g['kind'] == 'pepper':
        cv.put((np.hypot(PX - x, PY - y) < 1.6 * k) & vis, 'out')
    elif g['kind'] == 'meat':
        m = rot(8 * k, 4 * k) & vis
        cv.put(m, 'pink'); cv.put(m & (np.abs((PX - x) * math.sin(a) - (PY - y) * math.cos(a)) < 0.6), 'cream')
        cv.put(edge(m), 'rd')
    elif g['kind'] == 'tofu':
        m = (np.abs(PX - x) < 5 * k) & (np.abs(PY - y) < 5 * k) & vis
        cv.put(m, 'white'); cv.put(m & ((PX - x > 3 * k) | (PY - y > 3 * k)), 'cream_d')
    elif g['kind'] == 'mush':
        m = (np.hypot(PX - x, PY - y) < 5 * k) & vis
        cv.put(m, 'wd'); cv.put(m & (np.hypot(PX - x + 1, PY - y + 1) < 3 * k), 'wm')
        cv.put(m & ((np.abs(PX - x) < 0.6) | (np.abs(PY - y) < 0.6)), 'wl')
    elif g['kind'] == 'goji':
        m = rot(2.2 * k, 1.4 * k) & vis
        cv.put(m, 'rm'); cv.put(m & (np.hypot(PX - x + 0.6, PY - y + 0.6) < 0.8), 'rl')
    elif g['kind'] == 'scallion':
        d = np.hypot(PX - x, PY - y)
        cv.put((d < 2.6 * k) & (d > 1.2 * k) & vis, 'green')
    elif g['kind'] == 'enoki':
        m = rot(7 * k, 1.0) & vis
        cv.put(m, 'cream'); cv.put(rot(1.6 * k, 1.6 * k) & vis, 'white')


def top_key(p, static):
    """Sleutelbeeld van de morph; p = 0 (hotpot) .. 1 (Poké Ball)."""
    cv = Canvas('wm')
    cv.a[:] = static.a
    e = smooth(p)
    dx, dy = PX - CX2, PY - CY2
    r = np.hypot(dx, dy)
    # oortjes (verdwijnen in de eerste helft)
    L = 9 * (1 - smooth(p / 0.5))
    if L > 0.8:
        for s in (-1, 1):
            hm = (np.abs(dy) < 6) & (s * dx > R2 - 3) & (s * dx < R2 + L)
            cv.put(hm, 'mm'); cv.put(hm & (dy < -3), 'ml'); cv.put(hm & (dy > 3), 'md'); cv.put(edge(hm), 'out')
    rimw = 6 - 2.6 * e
    pot = r < R2
    cv.put(pot, 'mm')
    ang = np.arctan2(dy, dx)
    lit = np.cos(ang + 2.36)                       # licht van linksboven
    cv.put(pot & (lit > 0.45), 'ml')
    cv.put(pot & (lit < -0.45), 'md')
    cv.put(pot & (r > R2 - 1.2), 'out')
    Ri = R2 - rimw
    inside = r < Ri
    cv.put(pot & ~inside & (r < Ri + 1.0), 'md')   # binnenkant van de rand
    # S-grens -> rechte band
    a = 1 - e
    xs = np.linspace(-Ri, Ri, 600)
    ys = yinyang_boundary(xs / Ri, a) * Ri
    bnd = np.interp(dx, xs, ys)
    d = np.full((H, W), 99.0)
    box = (np.abs(dx) < R2 + 1) & (np.abs(dy) < R2 + 1)
    for sx, sy in zip(xs[::3], ys[::3]):
        d = np.minimum(d, np.where(box, np.hypot(dx - sx, dy - sy), 99.0))
    half = 1.6 + (4.6 - 1.6) * e
    red = inside & (dy < bnd)
    white = inside & ~red
    cv.put(red, 'rm')
    cv.put(white, 'cream')
    rng = np.random.default_rng(5)
    blot = nd.gaussian_filter(rng.random((H, W)), 2.4)
    oil = nd.gaussian_filter(rng.random((H, W)), 1.1)
    tex = 1 - smooth((p - 0.1) / 0.6)              # textuur verdwijnt
    if tex > 0:
        cv.put(red & (blot < np.percentile(blot, 24 * tex)), 'rd')
        cv.put(red & (oil > np.percentile(oil, 100 - 9 * tex)), 'rl')
        cv.put(white & (blot > np.percentile(blot, 100 - 18 * tex)), 'cream_d')
    # Poké Ball-schaduw en glans komen erbij
    sh = smooth((p - 0.55) / 0.4)
    if sh > 0:
        dith = BAYER[YY % 4, XX % 4] < sh
        cv.put(red & dith & (r > Ri - 7) & (dx + dy * 0.3 > 12), 'rd')
        cv.put(white & dith & (r > Ri - 7) & (dx + dy > 18), 'cream_d')
        hl = (np.hypot(dx + 26, dy + 30) < 11) & ~(np.hypot(dx + 21, dy + 25) < 10)
        cv.put(red & dith & hl, 'rl')
        cv.put(red & dith & (np.hypot(dx + 30, dy + 33) < 2.6), 'white')
    # ingrediënten en bubbels
    R = random.Random(int(p * 1000) + 9)
    nb = int(round(12 * (1 - smooth(p / 0.75))))
    for i in range(nb):
        x, y = R.uniform(-Ri + 6, Ri - 6), R.uniform(-Ri + 6, Ri - 6)
        rb = R.choice((1.6, 2.2, 2.8))
        ring = (np.hypot(dx - x, dy - y) < rb) & (np.hypot(dx - x, dy - y) > rb - 1.1) & inside & (d > half + 1)
        cv.put(ring & red, 'rl'); cv.put(ring & white, 'white')
    for g in INGREDIENTS:
        s = smooth((p - g['start']) / 0.34)
        f = np.interp(g['x'], xs, ys)
        if (g['y'] < f) != g['red'] or abs(g['y'] - f) < half + 4:
            s = max(s, 0.85)                       # de scheiding haalt hem in: weg ermee
        draw_ingredient(cv, g, s, (red if g['red'] else white) & (d > half + 1))
    # scheiding: metalen wandje, wordt de band
    div = inside & (d < half)
    cv.put(div, 'mm')
    cv.put(div & (dy < bnd - half * 0.4), 'ml')
    cv.put(div & (dy > bnd + half * 0.4), 'md')
    # tofu drijft naar het midden en wordt de knop
    q = smooth(p / 0.5)
    tx, ty = 15 * (1 - q), 24 * (1 - q)
    m2 = smooth((p - 0.45) / 0.4)                  # vierkant -> rond
    n = 8 - 6 * m2
    sz = 6 + 1.6 * m2
    ax, ay = np.abs(dx - tx) / sz, np.abs(dy - ty) / sz
    tofu = (ax ** n + ay ** n) <= 1
    ringw = 3.6 * smooth((p - 0.5) / 0.38)
    if ringw > 0.3:
        rr = np.hypot(dx - tx, dy - ty)
        cv.put((rr < sz + ringw) & ~tofu & (rr > sz - 0.5), 'md')
    cv.put(tofu, 'white')
    cv.put(tofu & (((dx - tx) > sz * 0.45) | ((dy - ty) > sz * 0.45)) & (m2 < 0.6), 'cream_d')
    if m2 > 0.6:
        rr = np.hypot(dx - tx, dy - ty)
        cv.put(tofu & (rr > 3.6) & (rr < 4.7) & (BAYER[YY % 4, XX % 4] < (m2 - 0.6) * 2.5), 'cream_d')
    return cv


def pot_first(r, c):
    """Tiles over de pan (incl. oortjes) eerst in palet 15 (dat wordt Poké Ball), de rest eerst 13/14 (dimt)."""
    x, y = c * 8 + 4, r * 8 + 4
    if abs(x - CX2) < R2 + 14 and abs(y - CY2) < R2 + 4 and math.hypot(max(abs(x - CX2) - 10, 0), y - CY2) < R2 + 8:
        return (15, 13, 14)
    return (13, 14, 15)


def key_palettes(p):
    """Paletset per sleutelbeeld: metaal -> zwart, bouillon -> Poké Ball-kleuren, tafel dimt."""
    e = smooth(p)
    mt = smooth((p - 0.2) / 0.6)
    ball = smooth((p - 0.25) / 0.65)
    dim = 0.55 * e
    target = {'md': (16, 16, 20), 'mm': (16, 16, 20), 'ml': (16, 16, 20), 'out': (16, 16, 20),
              'rd': (156, 24, 32), 'rm': (232, 44, 44), 'rl': (255, 140, 128),
              'cream_d': (178, 180, 190), 'cream': (248, 248, 248), 'white': (255, 255, 255)}
    pals = {}
    for n, names in PAL2.items():
        pal = []
        for name in names:
            c = C[name]
            if name in ('md', 'mm', 'ml'):
                c = mix(c, target[name], mt)
            elif name == 'out':
                c = mix(c, target['out'], e)
            elif name in target and n == 15:
                c = mix(c, target[name], ball)
            if n != 15 or name in ('wd', 'wm', 'wl'):
                c = mix(c, (8, 4, 4), dim)
            pal.append(c)
        pals[n] = pal
    return pals


# ---------------------------------------------------------------- tiles, paletten, tilemaps
def assign(cv, pals, prefer=(13, 14, 15)):
    """Per tile een palet kiezen; geeft (palnr, 8x8 indexen) per tile en het aantal benaderde pixels."""
    sets = {n: [ID[x] for x in names] for n, names in pals.items()}
    out, missed = [], 0
    for r in range(20):
        for c in range(30):
            t = cv.a[r * 8:(r + 1) * 8, c * 8:(c + 1) * 8]
            u = set(np.unique(t).tolist())
            best, bm = None, 1e9
            for n in (prefer(r, c) if callable(prefer) else prefer):
                m = len(u - set(sets[n]))
                if m < bm:
                    best, bm = n, m
            idx = np.zeros((8, 8), np.uint8)
            for y in range(8):
                for x in range(8):
                    cid = t[y, x]
                    if cid in sets[best]:
                        idx[y, x] = sets[best].index(cid) + 1
                    else:
                        rgb = C[NAMES[cid]]
                        dd = [sum((a - b) ** 2 for a, b in zip(rgb, C[NAMES[s]])) for s in sets[best]]
                        idx[y, x] = int(np.argmin(dd)) + 1
                        missed += 1
            out.append((best, idx))
    return out, missed


def variants(idx):
    return ((0, idx), (1, idx[:, ::-1]), (2, idx[::-1, :]), (3, idx[::-1, ::-1]))


class TileSet:
    def __init__(self, first):
        self.first = first
        self.tiles = []
        self.lookup = {}

    def find(self, pal, idx):
        return self.lookup.get((pal, idx.tobytes()))

    def add(self, pal, idx):
        hit = self.find(pal, idx)
        if hit is not None:
            return hit
        n = self.first + len(self.tiles)
        self.tiles.append(idx.copy())
        for f, v in variants(idx):
            self.lookup.setdefault((pal, np.ascontiguousarray(v).tobytes()), (n, f))
        # een tile mag in elk palet: de indexen zijn hetzelfde
        for p2 in (13, 14, 15):
            for f, v in variants(idx):
                self.lookup.setdefault((p2, np.ascontiguousarray(v).tobytes()), (n, f))
        return (n, 0)


def pack4(tiles):
    b = bytearray()
    for t in tiles:
        for y in range(8):
            for x in range(0, 8, 2):
                b.append(int(t[y, x]) | (int(t[y, x + 1]) << 4))
    return bytes(b)


def entry(n, f, pal):
    return n | (f << 10) | (pal << 12)


def pal_bytes(pals):
    words = []
    for n in (13, 14, 15):
        cols = [pals[n][0]] + list(pals[n])
        words += [bgr555(c) for c in cols]
    return struct.pack('<%dH' % len(words), *words)


def cycle_pal1(f):
    pals = {}
    for n, names in PAL1.items():
        pals[n] = [ANIM[x][f] if x in ANIM else C[x] for x in names]
    return pals


def render(assigned, palsets):
    """Hoe het in de game eruitziet (voor voorbeelden)."""
    img = np.zeros((H, W, 3), np.uint8)
    for i, (pal, idx) in enumerate(assigned):
        r, c = divmod(i, 30)
        lut = np.array([(0, 0, 0)] + [gba(x) for x in palsets[pal]], np.uint8)
        img[r * 8:(r + 1) * 8, c * 8:(c + 1) * 8] = lut[idx]
    return Image.fromarray(img)


def build():
    # beeld 1
    table = scene_table()
    a1, miss1 = assign(table, PAL1)
    ts1 = TileSet(1)
    map1 = []
    for pal, idx in a1:
        n, f = ts1.add(pal, idx)
        map1.append(entry(n, f, pal))
    assert len(ts1.tiles) <= MAX_TILES, len(ts1.tiles)

    # beeld 2
    static = top_static()
    ps = [i / (SB_KEYS - 1) for i in range(SB_KEYS)]
    keys = [top_key(p, static) for p in ps]
    assigned = [assign(k, PAL2, prefer=pot_first)[0] for k in keys]
    n_pos = 600
    fixed = [all(assigned[k][i][0] == assigned[0][i][0] and np.array_equal(assigned[k][i][1], assigned[0][i][1])
                 for k in range(SB_KEYS)) for i in range(n_pos)]
    st = TileSet(1)
    for i in range(n_pos):
        if fixed[i]:
            st.add(*assigned[0][i])
    ns = len(st.tiles)
    dyn = []
    for k in range(SB_KEYS):
        loc = []
        lk = {}
        for i in range(n_pos):
            if fixed[i]:
                continue
            pal, idx = assigned[k][i]
            if st.find(pal, idx) is None and (pal, idx.tobytes()) not in lk:
                j = len(loc)
                loc.append(idx.copy())
                for f, v in variants(idx):
                    for p2 in (13, 14, 15):
                        lk.setdefault((p2, np.ascontiguousarray(v).tobytes()), (j, f))
        dyn.append((loc, lk))
    dmax = max(len(l) for l, _ in dyn)
    base = [1 + ns, 1 + ns + dmax]
    assert ns + 1 + 2 * dmax <= MAX_TILES, (ns, dmax)
    maps2 = []
    for k in range(SB_KEYS):
        loc, lk = dyn[k]
        tm = []
        for i in range(n_pos):
            pal, idx = assigned[k][i]
            hit = st.find(pal, idx)
            if hit is None:
                j, f = lk[(pal, idx.tobytes())]
                hit = (base[k & 1] + j, f)
            tm.append(entry(hit[0], hit[1], pal))
        maps2.append(tm)
    pals2 = [key_palettes(p) for p in ps]
    return dict(table=table, a1=a1, miss1=miss1, ts1=ts1, map1=map1, keys=keys, assigned=assigned, st=st, dyn=dyn,
                dmax=dmax, maps2=maps2, pals2=pals2)


def save(b):
    ts1, st, dyn = b['ts1'], b['st'], b['dyn']
    w = lambda name, data: open(OUT + name, 'wb').write(data)
    w('sickblik_table_tiles.bin', pack4([np.zeros((8, 8), np.uint8)] + ts1.tiles))   # tile 0 leeg (de runner kopieert vanaf tile 0)
    w('sickblik_table_map.bin', struct.pack('<600H', *b['map1']))
    w('sickblik_table_pals.bin', b''.join(pal_bytes(cycle_pal1(f)) for f in range(SB_CYCLE)))
    w('sickblik_top_static.bin', pack4(st.tiles))
    alltiles, offs = [], []
    for loc, _ in dyn:
        offs.append((len(alltiles), len(loc)))
        alltiles += loc
    w('sickblik_top_dyn.bin', pack4(alltiles))
    w('sickblik_top_maps.bin', b''.join(struct.pack('<600H', *m) for m in b['maps2']))
    w('sickblik_top_pals.bin', b''.join(pal_bytes(p) for p in b['pals2']))
    with open(HDR, 'w') as fp:
        fp.write('// Gegenereerd door tools/grounded/sickblik_transition.py; niet met de hand bewerken.\n')
        fp.write('#define SB_CYCLE %d\n#define SB_KEYS %d\n#define SB_TOP_STATIC %d\n#define SB_TOP_DMAX %d\n\n'
                 % (SB_CYCLE, SB_KEYS, len(st.tiles), b['dmax']))
        fp.write('// per sleutelbeeld: eerste tile in sSickBlik_TopDyn en het aantal tiles\n')
        fp.write('static const u16 sSickBlik_KeyTiles[SB_KEYS][2] =\n{\n')
        for o, n in offs:
            fp.write('    {%d, %d},\n' % (o, n))
        fp.write('};\n')
    print('sickblik: beeld 1 %d tiles (%d pixels benaderd), beeld 2 %d vaste tiles + 2 x %d, %d sleutelbeelden, %d KB'
          % (len(ts1.tiles), b['miss1'], len(st.tiles), b['dmax'], SB_KEYS, len(alltiles) * 32 // 1024))


def preview(b, d):
    os.makedirs(d, exist_ok=True)
    big = lambda im, s=3: im.resize((W * s, H * s), Image.NEAREST)
    t1 = [render(b['a1'], cycle_pal1(f)) for f in range(SB_CYCLE)]
    big(t1[0]).save(os.path.join(d, 'sb_beeld1_tafel.png'))
    tops = [render(b['assigned'][k], b['pals2'][k]) for k in range(SB_KEYS)]
    big(tops[0]).save(os.path.join(d, 'sb_beeld2_bovenaanzicht.png'))
    big(tops[-1]).save(os.path.join(d, 'sb_beeld2_pokeball.png'))
    pick = [0, 6, 11, 16, 21, 29]
    sheet = Image.new('RGB', (W * 3 * 2 + 8, H * 3 * 4 + 24), (24, 24, 24))
    sheet.paste(big(t1[0]), (0, 0))
    sheet.paste(big(tops[0]), (W * 3 + 8, 0))
    for i, k in enumerate(pick[1:5]):
        sheet.paste(big(tops[k]), ((i % 2) * (W * 3 + 8), (1 + i // 2) * (H * 3 + 8)))
    sheet.paste(big(tops[-1]), (0, 3 * (H * 3 + 8)))
    sheet.paste(big(tops[25]), (W * 3 + 8, 3 * (H * 3 + 8)))
    sheet.save(os.path.join(d, 'sb_overzicht.png'))


if __name__ == '__main__':
    b = build()
    save(b)
    if len(sys.argv) > 1:
        preview(b, sys.argv[1])
