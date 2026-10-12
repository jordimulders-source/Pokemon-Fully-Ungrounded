#!/usr/bin/env python3
"""Project Grounded: B_TRANSITION_MIMI (Mimi de Mimikyu, Mimic Circle op Route 119, ook in het Battle Stadium).

Een donkere kinderkamer bij nacht: maanlicht door het raam, speelgoedblokken die "HELP" spellen, een bed. In het midden
een poppenkast ("THE PIKACHU SHOW"). Het doek gaat open; in het lamplicht staat de Pikachu-pop (Mimikyu, echte
sprite). Hij draait heel langzaam zijn kop opzij... tot het nekje knakt (de busted-vorm). Het licht flikkert, gaat uit,
en onder het doek gaan twee ogen open. Gevecht.

Film (zie film.py): tiles/tilemaps/paletten naar graphics/battle_transitions/film_mimi*.
Gebruik: python3 tools/grounded/mimi_transition.py [voorbeeldmap]
"""
import math, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
import film_art as fa
from film import W, H, text35, text35_width

# ------------------------------------------------------------------ tijdlijn (gameframes; zie MIMI_* in battle_transition.c)
T_IN = 8          # 0-7 leeg (de wereld wordt zwart)
T_HOLD = 20
T_OPEN = 30       # het doek gaat open (SE_CONTEST_CURTAIN_RISE)
T_OPEN_END = 58
T_TURN = 74       # de kop begint te draaien
T_SNAP = 150      # krak: busted
T_FLICK = 166     # het licht flikkert
T_OUT = 192       # uit
T_EYES = 200      # twee ogen onder het doek
T_END = 224

# ------------------------------------------------------------------ kleuren
BLACK = (0, 0, 0)
EYE = (112, 248, 224)
NIGHT = [(14, 12, 30), (24, 22, 48), (36, 34, 66), (52, 50, 90)]          # muur/vloer, donker -> licht
MOON = [(120, 136, 184), (184, 196, 232)]
WOOD = [(46, 26, 18), (80, 46, 26), (120, 74, 38), (164, 112, 60)]
CURT = [(70, 10, 22), (120, 20, 36), (168, 40, 50), (206, 78, 74)]
GOLD = [(150, 112, 40), (224, 186, 88)]
STAGE = [(10, 8, 20), (24, 20, 34), (40, 34, 46), (60, 52, 58)]         # binnenkant poppenkast + lampkegel
BLOCK = [(152, 48, 48), (48, 96, 160), (56, 136, 72), (200, 168, 56)]

# poppenkast
TX0, TX1 = 56, 184         # buitenkant
OX0, OX1 = 68, 172         # opening
OY0, OY1 = 30, 124
LEDGE0, LEDGE1 = 124, 136


def room():
    a = fa.canvas(NIGHT[1])
    # behang: verticale banen (twee tinten), vloer met planken
    for x in range(0, W, 16):
        fa.rect(a, x, 0, x + 8, 112, NIGHT[2])
    fa.rect(a, 0, 108, W, 112, NIGHT[0])                      # plint
    fa.rect(a, 0, 112, W, H, NIGHT[0])
    for y in (120, 132, 146):
        fa.rect(a, 0, y, W, y + 1, NIGHT[1])
    for i, y in enumerate((112, 120, 132, 146)):
        for x in range((i * 24) % 40, W, 40):
            fa.rect(a, x, y, x + 1, y + (8, 12, 14, 14)[i], NIGHT[1])
    # raam links met maan
    fa.rect(a, 6, 16, 46, 72, WOOD[1])
    fa.rect(a, 9, 19, 43, 69, (8, 12, 34))
    ys, xs = np.mgrid[0:H, 0:W]
    moon = (xs - 32) ** 2 + (ys - 32) ** 2 <= 49
    a[moon] = MOON[1]
    a[((xs - 34) ** 2 + (ys - 31) ** 2 <= 30) & moon] = MOON[0]
    fa.rect(a, 25, 19, 27, 69, WOOD[1])
    fa.rect(a, 9, 43, 43, 45, WOOD[1])
    # maanlicht op de vloer (gedithered parallellogram)
    m = np.zeros((H, W), bool)
    for y in range(112, H):
        k = (y - 112) * 0.6
        m[y, int(10 + k):int(44 + k)] = True
    fa.dither(a, m, NIGHT[3], 0.4)
    # speelgoedblokken: H E L P
    for i, (ch, col) in enumerate(zip('HELP', BLOCK)):
        x, y = 4 + i * 12, 138 - (i % 2)
        fa.rect(a, x, y, x + 10, y + 10, fa.shade(col, 0.55))
        fa.rect(a, x + 1, y + 1, x + 9, y + 9, fa.shade(col, 0.8))
        text35(lambda u, v: a.__setitem__((v, u), (230, 222, 200)), x + 4, y + 3, ch)
    # bed rechts
    fa.rect(a, 196, 92, 240, 140, WOOD[0])
    fa.rect(a, 198, 86, 240, 100, (70, 80, 120))            # deken
    fa.rect(a, 198, 100, 240, 128, (54, 62, 100))
    fa.rect(a, 200, 80, 222, 90, (150, 150, 170))           # kussen
    fa.rect(a, 192, 70, 196, 140, WOOD[1])                  # bedstijl
    return a


def theater(curtain):
    """Poppenkast; curtain = 0 (dicht) .. 1 (open)."""
    a = room()
    # kast
    fa.rect(a, TX0, 4, TX1, H, WOOD[1])
    fa.rect(a, TX0 + 2, 4, TX1 - 2, H, WOOD[2])
    for x in range(TX0 + 6, TX1 - 4, 12):
        fa.rect(a, x, LEDGE1 + 2, x + 1, H, WOOD[1])
    # bord bovenaan
    fa.rect(a, TX0 - 4, 2, TX1 + 4, 26, WOOD[0])
    fa.rect(a, TX0 - 2, 4, TX1 + 2, 24, GOLD[0])
    fa.rect(a, TX0, 6, TX1, 22, CURT[1])
    t1 = 'THE PIKACHU SHOW'
    text35(lambda u, v: a.__setitem__((v, u), GOLD[1]), (W - text35_width(t1, 1)) // 2, 9, t1)
    t2 = '(NOT A GHOST)'
    text35(lambda u, v: a.__setitem__((v, u), GOLD[0]), (W - text35_width(t2, 1)) // 2, 16, t2)
    # opening: donker decor met lampkegel
    fa.rect(a, OX0, OY0, OX1, OY1, STAGE[0])
    ys, xs = np.mgrid[0:H, 0:W]
    for lvl, (wid, lev) in enumerate(((52, 1.0), (40, 1.0), (28, 1.0))):
        cone = (ys >= OY0) & (ys < OY1) & (np.abs(xs - 120) < 10 + (ys - OY0) * wid / (OY1 - OY0))
        fa.dither(a, cone, STAGE[1 + lvl], 0.5 if lvl else 0.75)
    # lampje boven in de opening
    fa.rect(a, 114, OY0, 126, OY0 + 3, GOLD[0])
    fa.rect(a, 116, OY0 + 3, 124, OY0 + 5, GOLD[1])
    return a, ys, xs


def curtains(a, ys, xs, curtain):
    """Twee gordijnhelften (plooien = verticale banen), open = opgebonden aan de zijkanten."""
    half = (OX1 - OX0) // 2
    w = int(round(half - (half - 12) * curtain))
    for side in (0, 1):
        x0 = OX0 if side == 0 else OX1 - w
        for x in range(x0, x0 + w):
            u = (x - x0) / max(1, w)
            ph = (x - x0) * (6.0 / max(1, w)) * math.pi * (1.0 if curtain < 1 else 1.0)
            v = 0.5 + 0.5 * math.sin(ph * (half / max(w, 12)) * 0.9 + side)
            col = CURT[min(3, int(v * 3.99))]
            if curtain > 0:
                # opgebonden: onderkant loopt schuin naar de zijkant
                edge = (u if side == 0 else 1 - u)
                ybot = int(OY1 - (OY1 - OY0 - 18) * curtain * edge ** 1.5)
            else:
                ybot = OY1
            a[OY0:ybot, x] = col
            if curtain > 0 and ybot < OY1:
                a[ybot:ybot + 1, x] = CURT[0]
    # valance (strook stof bovenaan)
    fa.rect(a, OX0 - 2, OY0 - 4, OX1 + 2, OY0 + 6, CURT[2])
    for x in range(OX0 - 2, OX1 + 2, 8):
        fa.rect(a, x, OY0 + 6, x + 4, OY0 + 8, CURT[2])
    fa.rect(a, OX0 - 2, OY0 - 4, OX1 + 2, OY0 - 3, GOLD[0])


def ledge(a):
    fa.rect(a, TX0 - 2, LEDGE0, TX1 + 2, LEDGE1, WOOD[3])
    fa.rect(a, TX0 - 2, LEDGE1 - 3, TX1 + 2, LEDGE1, WOOD[1])
    fa.rect(a, TX0 - 2, LEDGE0, TX1 + 2, LEDGE0 + 1, GOLD[1])


# ------------------------------------------------------------------ Mimikyu
NORMAL1 = fa.mon('mimikyu', 'front.png', pal='normal.pal')
NORMAL = fa.scale(NORMAL1, 2)
BUSTED = fa.scale(fa.mon('mimikyu', 'busted/front.png', pal='busted/normal.pal'), 2)
PIVOT = (30, 36)            # nekje (in de 64x64-sprite)
MX, MY = 48, 27             # linkerbovenhoek van de 2x-sprite (onderkant achter de rand)


def head_turned(deg):
    """De normale sprite met de kop (alles boven het nekje, zonder de staart) deg graden met de klok mee gedraaid om
    het nekje. Draaien op 2x (NEAREST) zodat de randen niet rafelen."""
    s = np.array(NORMAL1)
    ys, xs = np.mgrid[0:64, 0:64]
    head = (ys <= 35) & ((ys < 29) | (xs <= 40))
    hd = s.copy()
    hd[~head] = 0
    body = s.copy()
    body[head] = 0
    big_h = fa.scale(Image.fromarray(hd, 'RGBA'), 2)
    big_b = fa.scale(Image.fromarray(body, 'RGBA'), 2)
    if deg:
        big_h = big_h.rotate(-deg, resample=Image.NEAREST, center=(PIVOT[0] * 2, PIVOT[1] * 2))
    out = Image.new('RGBA', (128, 128))
    out.alpha_composite(big_b)
    out.alpha_composite(big_h)
    return out


def scene(curtain=1.0, mon=None, eyes=0):
    a, ys, xs = theater(curtain)
    if mon is not None:
        fa.blit(a, mon, MX, MY)
    ledge(a)
    curtains(a, ys, xs, curtain)
    return a


def dark(eyes):
    """Licht uit: alles zwart, alleen twee ogen in de kier onder het doek (eyes: 0 dicht .. 3 open)."""
    a = fa.canvas(BLACK)
    if eyes:
        h = (0, 1, 3, 4)[eyes]
        for ex in (106, 128):
            fa.rect(a, ex, 112 - h // 2, ex + 6, 112 - h // 2 + h, EYE)
            if h >= 3:
                fa.rect(a, ex + 1, 112 - h // 2 - 1, ex + 5, 112 - h // 2 + h + 1, EYE)
    return a


# ------------------------------------------------------------------ film
def build(preview=None):
    f = film.Film('mimi')
    closed = scene(0.0)
    keys = [closed, scene(1.0, NORMAL), scene(1.0, BUSTED)]
    p = film.auto_palettes(keys, [BLACK, EYE], n_free=13)
    pal = [x[:15] for x in p]

    def ps(k=1.0, keep_eye=True):
        def tr(c):
            if keep_eye and tuple(film.gba(c)) == tuple(film.gba(EYE)):
                return c
            return fa.shade(c, k)
        return f.palset(*[[tr(c) for c in q] for q in pal])

    f.ref = ps(1.0)
    for t in range(T_IN):
        f.add(None, ps(0.0))
    for t in range(T_IN, T_HOLD):
        f.add(closed, ps((t - T_IN + 1) / (T_HOLD - T_IN)))
    for t in range(T_HOLD, T_OPEN):
        f.add(closed, f.ref)
    cache = {}
    for t in range(T_OPEN, T_OPEN_END, 2):
        u = (t - T_OPEN + 2) / (T_OPEN_END - T_OPEN)
        u = u * u * (3 - 2 * u)
        f.add(scene(u, NORMAL), f.ref, 2)
    still = keys[1]
    for t in range(T_OPEN_END, T_TURN):
        f.add(still, f.ref)
    # de kop draait heel langzaam (en steeds iets sneller), per 4 frames een stapje
    for t in range(T_TURN, T_SNAP, 4):
        u = (t - T_TURN) / (T_SNAP - T_TURN)
        deg = int(round(62 * u ** 1.6))
        if deg not in cache:
            cache[deg] = scene(1.0, head_turned(deg))
        f.add(cache[deg], f.ref, min(4, T_SNAP - t))
    busted = keys[2]
    for t in range(T_SNAP, T_FLICK):
        f.add(busted, f.ref)
    # flikkeren: aan/uit in een onregelmatig ritme, steeds donkerder
    flick = [0.25, 1, 1, 0.15, 0.15, 0.7, 0.1, 1, 0.9, 0.1, 0.1, 0.1, 0.5, 0.08, 0.08, 0.6, 0.05, 0.05, 0.05, 0.3,
             0.04, 0.04, 0.04, 0.04, 0.15, 0.02]
    for i, t in enumerate(range(T_FLICK, T_OUT)):
        f.add(busted, ps(flick[i % len(flick)]))
    for t in range(T_OUT, T_EYES):
        f.add(dark(0), f.ref)
    eyes = [dark(1), dark(2), dark(3)]
    for t in range(T_EYES, T_END):
        k = t - T_EYES
        e = eyes[min(2, k // 2)]
        if 14 <= k < 16:              # één keer knipperen
            e = eyes[0] if k == 14 else eyes[1]
        f.add(e, f.ref)
    f.encode(preview)
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    f = build(d)
    if d:
        film.sheet(f.preview_frames, [24, 44, 66, 100, 128, 146, 154, 170, 186, 196, 206, 222],
                   os.path.join(d, 'mimi_keys.png'))
