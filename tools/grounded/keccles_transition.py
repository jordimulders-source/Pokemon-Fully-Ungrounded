#!/usr/bin/env python3
"""Project Grounded: B_TRANSITION_KECCLES (Keccles de Kecleon, een droge, echt wijze denker; ook in het Stadium).

De humor zit in wie het zegt (een Kecleon met een academische carrière), niet in gekke zinnen: wat op de borden staat
klopt echt (waarneming, camouflage, geduld). Een verlaten lab bij nacht: schoolborden vol krijt. De camera zoekt (drie
shots, handheld): het lege lab ("EYES SEE EDGES, NOT THINGS."), een bord met aantekeningen ("COLOR = CONTEXT",
"SELF = CONTEXT ?", "FREE WILL ?", "HASTE < PATIENCE"), dan het bord met THE PLAN (OBSERVE, WAIT, ADAPT, ACT ONCE) en
jouw gezicht omcirkeld. Op dat bord hangt een rode zigzag in de lucht (de enige streep die een Kecleon niet kan
camoufleren), dan gaat er een oog open in het krijt. De camouflage golft van boven naar beneden weg en Keccles staat
ervoor (echte Kecleon-sprite). Hij grijnst; naast hem schrijft het krijt "WE SEE WHAT WE EXPECT." (lang genoeg om te
lezen). Wit, gevecht.

Film (zie film.py): tiles/tilemaps/paletten naar graphics/battle_transitions/film_keccles*.
Gebruik: python3 tools/grounded/keccles_transition.py [voorbeeldmap]
"""
import math, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
import film_art as fa
from film import W, H, text35, text35_width

# ------------------------------------------------------------------ tijdlijn (zie KECCLES_* in battle_transition.c)
T_IN = 8
T_FADE = 18
T_SHOT2 = 54      # cut: formules
T_SHOT3 = 98      # cut: THE PLAN
T_EYE = 126       # het oog gaat open
T_RIPPLE = 148    # de camouflage golft weg
T_RIPPLE_END = 176
T_GRIN = 188      # bek open
T_QUOTE = 194     # het krijt schrijft de les (QUOTE_SPEED frames per letter), daarna leestijd
QUOTE = ('WE SEE WHAT', 'WE EXPECT.')
QUOTE_SPEED = 1
T_WHITE = T_QUOTE + sum(len(q) for q in QUOTE) * QUOTE_SPEED + 100     # ±1,7 s leestijd voor 5 woorden
T_END = T_WHITE + 12

BLACK = (0, 0, 0)
WHITE = (248, 248, 248)
CHALK = (216, 224, 208)
CHALK2 = (128, 150, 128)        # uitgeveegd krijt
RED = (232, 96, 88)
BOARD = [(22, 52, 38), (30, 64, 46), (40, 78, 56)]
FRAME = [(62, 38, 22), (104, 66, 34), (148, 100, 52)]
WALL = [(40, 44, 52), (54, 60, 70), (70, 78, 88)]
DESK = [(56, 40, 30), (92, 66, 44), (128, 96, 64)]
GLASS = [(96, 160, 176), (160, 216, 224), (120, 224, 120)]


def chalk_text(a, x, y, s, scale=1, col=CHALK):
    return text35(lambda u, v: a.__setitem__((v, u), col) if 0 <= u < W and 0 <= v < H else None, x, y, s, scale)


def chalk_line(a, x0, y0, x1, y1, col=CHALK, w=1):
    n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    for i in range(n):
        u = i / max(1, n - 1)
        x, y = int(round(x0 + (x1 - x0) * u)), int(round(y0 + (y1 - y0) * u))
        fa.rect(a, x, y, x + w, y + w, col)


def chalk_circle(a, cx, cy, rx, ry, col=CHALK, w=1, a0=0.0, a1=2 * math.pi, wobble=0.0):
    n = int((rx + ry) * 4)
    pts = []
    for i in range(n + 1):
        t = a0 + (a1 - a0) * i / n
        r = 1 + wobble * math.sin(t * 3)
        pts.append((cx + rx * r * math.cos(t), cy + ry * r * math.sin(t)))
    for p, q in zip(pts, pts[1:]):
        chalk_line(a, p[0], p[1], q[0], q[1], col, w)


def board(a, x0, y0, x1, y1, smudge=0):
    fa.rect(a, x0 - 4, y0 - 4, x1 + 4, y1 + 4, FRAME[1])
    fa.rect(a, x0 - 4, y0 - 4, x1 + 4, y0 - 3, FRAME[2])
    fa.rect(a, x0 - 4, y1 + 3, x1 + 4, y1 + 4, FRAME[0])
    fa.rect(a, x0, y0, x1, y1, BOARD[1])
    # uitgeveegde wolken (vast patroon per bord)
    rng = np.random.RandomState(smudge + 3)
    ys, xs = np.mgrid[0:H, 0:W]
    for _ in range(4):
        cx, cy = rng.uniform(x0, x1), rng.uniform(y0, y1)
        m = (((xs - cx) / 26.0) ** 2 + ((ys - cy) / 9.0) ** 2 < 1) & (xs >= x0) & (xs < x1) & (ys >= y0) & (ys < y1)
        fa.dither(a, m, BOARD[2], 0.3)
    fa.rect(a, x0 - 2, y1 + 4, x1 + 2, y1 + 7, FRAME[0])           # krijtgoot
    fa.rect(a, x0 + 10, y1 + 3, x0 + 16, y1 + 5, CHALK)


def wall():
    a = fa.canvas(WALL[1])
    # behang: ruitjes van 16 px
    ys, xs = np.mgrid[0:H, 0:W]
    m = ((np.abs((xs % 16) - 8) + np.abs((ys % 16) - 8)) == 6)
    a[m] = WALL[2]
    a[((xs % 16) == 8) & ((ys % 16) == 8)] = WALL[0]
    return a


def shot1():
    """Wijd: het lege lab, twee borden, een bureau met glaswerk, een hanglamp."""
    a = wall()
    board(a, 14, 22, 112, 92, 1)
    board(a, 130, 22, 228, 92, 2)
    for i, s in enumerate(('UNSEEN IS NOT', 'ABSENT.', 'SEEN IS NOT', 'UNDERSTOOD.')):
        chalk_text(a, 20, 28 + i * 9, s)
    chalk_circle(a, 92, 74, 12, 10)
    chalk_line(a, 22, 84, 76, 62)
    for i, s in enumerate(('ON PERCEPTION:', 'EYES SEE EDGES,', 'NOT THINGS.', 'BLUR THE EDGE.')):
        chalk_text(a, 136, 28 + i * 9, s)
    chalk_circle(a, 208, 76, 10, 9, RED)
    # bureau
    fa.rect(a, 0, 112, W, H, (30, 32, 38))
    fa.rect(a, 40, 104, 200, 112, DESK[2])
    fa.rect(a, 40, 112, 200, 116, DESK[0])
    fa.rect(a, 48, 116, 54, H, DESK[1])
    fa.rect(a, 186, 116, 192, H, DESK[1])
    for i, x in enumerate((60, 74, 88)):                     # reageerbuisjes in een rekje
        fa.rect(a, x, 86, x + 5, 104, GLASS[0])
        fa.rect(a, x + 1, 94 + i * 2, x + 4, 103, GLASS[2] if i != 1 else RED)
    fa.rect(a, 56, 98, 96, 101, DESK[0])
    fa.rect(a, 140, 92, 160, 104, GLASS[1])                  # kolf
    fa.rect(a, 146, 84, 154, 92, GLASS[1])
    fa.rect(a, 142, 98, 158, 104, GLASS[2])
    fa.rect(a, 104, 96, 132, 104, (120, 40, 40))              # boek
    fa.rect(a, 104, 96, 132, 98, (170, 70, 60))
    # hanglamp
    fa.rect(a, 119, 0, 121, 8, (20, 20, 24))
    fa.rect(a, 110, 8, 130, 13, (90, 96, 104))
    fa.rect(a, 114, 13, 126, 15, (248, 232, 160))
    return a


def shot2():
    """Close-up van een bord met formules."""
    a = fa.canvas(FRAME[1])
    fa.rect(a, 0, 0, W, H, BOARD[1])
    rng = np.random.RandomState(9)
    ys, xs = np.mgrid[0:H, 0:W]
    for _ in range(6):
        cx, cy = rng.uniform(0, W), rng.uniform(0, H)
        m = (((xs - cx) / 40.0) ** 2 + ((ys - cy) / 14.0) ** 2 < 1)
        fa.dither(a, m, BOARD[2], 0.3)
    chalk_text(a, 12, 14, 'COLOR = CONTEXT', 2)
    chalk_text(a, 12, 34, 'SELF = CONTEXT ?', 2)
    chalk_text(a, 12, 62, 'FREE WILL ?', 2)
    chalk_text(a, 12, 92, 'HASTE < PATIENCE', 2)
    chalk_line(a, 10, 106, 208, 106, CHALK, 1)
    # grafiek rechtsboven: hoeveel je ziet tegen hoe lang je kijkt
    chalk_line(a, 168, 18, 168, 72)
    chalk_line(a, 168, 72, 228, 72)
    for i in range(12):
        x = 170 + i * 5
        chalk_line(a, x, 70 - i * i * 0.35, x + 5, 70 - (i + 1) ** 2 * 0.35)
    chalk_text(a, 172, 76, 'TIME LOOKING', 1)
    chalk_text(a, 150, 18, 'SEEN', 1)
    chalk_text(a, 120, 124, 'EVERYONE WEARS', 1)
    chalk_text(a, 120, 132, 'A COLOR FOR OTHERS.', 1)
    chalk_text(a, 12, 124, 'SEE ALSO: ME', 1)
    return a


# ------------------------------------------------------------------ shot 3: THE PLAN + Keccles
KEC = [fa.scale(fa.mon('kecleon', frame=k), 2) for k in (0, 1)]
KIDX = np.kron(np.array(Image.open(os.path.join(film.ROOT, 'graphics/pokemon/kecleon/anim_front_gba.png')))[:64],
               np.ones((2, 2), np.uint8))
KX, KY = 118, 38                      # linkerbovenhoek van de 2x-sprite


def plan_bg():
    a = wall()
    board(a, 6, 8, 234, 130, 5)
    chalk_text(a, 14, 14, 'THE PLAN', 2)
    chalk_line(a, 14, 26, 74, 26)
    for i, s in enumerate(('1. OBSERVE', '2. WAIT', '3. ADAPT', '4. ACT ONCE')):
        chalk_text(a, 14, 34 + i * 9, s)
    chalk_line(a, 52, 52, 66, 52, RED)        # bij ADAPT een pijl van het gezicht (hij past zich aan jou aan)
    # het gezicht van de speler (krijtpoppetje met pet), rood omcirkeld
    cx, cy = 44, 100
    chalk_circle(a, cx, cy, 10, 10)
    chalk_line(a, cx - 12, cy - 8, cx + 8, cy - 12)
    chalk_line(a, cx - 11, cy - 9, cx + 12, cy - 9, CHALK, 2)
    fa.rect(a, cx - 4, cy - 1, cx - 2, cy + 1, CHALK)
    fa.rect(a, cx + 3, cy - 1, cx + 5, cy + 1, CHALK)
    chalk_circle(a, cx, cy + 3, 4, 3, CHALK, 1, 0.3, math.pi - 0.3)
    chalk_circle(a, cx, cy - 1, 19, 17, RED, 2, wobble=0.04)
    chalk_text(a, cx + 24, cy - 2, 'YOU', 2, RED)
    chalk_line(a, cx + 10, cy - 18, 60, 54, RED)
    chalk_text(a, 14, 124, 'PATIENCE IS ALSO A COLOR.', 1, CHALK2)
    return a


def kec_masks():
    s = np.array(KEC[0])
    hh, ww = s.shape[:2]
    pm = np.zeros((H + hh, W + ww), bool)
    pi = np.zeros((H + hh, W + ww), np.uint8)
    pm[KY:KY + hh, KX:KX + ww] = s[..., 3] > 0
    pi[KY:KY + hh, KX:KX + ww] = KIDX
    m, idx = pm[:H, :W], pi[:H, :W]
    ys, xs = np.mgrid[0:H, 0:W]
    ly, lx = (ys - KY) // 2, (xs - KX) // 2
    eye = m & ((ly - 22.5) ** 2 + (lx - 34) ** 2 <= 13)
    red = m & np.isin(idx, [7, 8, 9])
    return m, eye, red


MASK, EYE_M, RED_M = kec_masks()


def edge_of(m):
    e = np.zeros_like(m)
    e[1:, :] |= m[1:, :] & ~m[:-1, :]
    e[:-1, :] |= m[:-1, :] & ~m[1:, :]
    e[:, 1:] |= m[:, 1:] & ~m[:, :-1]
    e[:, :-1] |= m[:, :-1] & ~m[:, 1:]
    return e


EDGE = edge_of(MASK)


def kec_full(frame=0):
    a = plan_bg()
    fa.blit(a, KEC[frame], KX, KY)
    return a


def camo(eye=0, shimmer=0, edge=0.8):
    """Gecamoufleerd: het bord zelf, met een vage rand (verspringt een pixel: shimmer), de rode zigzag en eventueel het
    oog (0 dicht, 1 half, 2 open)."""
    a = plan_bg()
    full = kec_full()
    e = np.roll(EDGE, shimmer, axis=1)
    if edge < 1:
        a[e] = (a[e].astype(np.int32) * edge).astype(np.uint8)
    a[RED_M] = full[RED_M]
    if eye:
        ys = np.nonzero(EYE_M.any(1))[0]
        if eye == 1:
            mid = (ys.min() + ys.max()) // 2
            em = EYE_M & (np.arange(H)[:, None] >= mid - 2) & (np.arange(H)[:, None] <= mid + 2)
        else:
            em = EYE_M
        a[em] = full[em]
    return a


def ripple(front):
    """De camouflage golft weg: boven de golf Keccles, in de golf een horizontale zinusgolf, eronder nog camouflage."""
    cam = camo(2)
    full = kec_full()
    a = cam.copy()
    for y in range(H):
        d = y - front
        if d < -10:
            row = full[y]
            a[y][MASK[y]] = row[MASK[y]]
        elif d < 8:
            sh = int(round(4 * math.sin(y * 0.9 + front * 0.5) * (1 - abs(d + 1) / 10)))
            src = np.roll(full[y] if d < -2 else cam[y], sh, axis=0)
            a[y][MASK[y]] = src[MASK[y]]
    return a


QX, QY = 128, 12      # de les rechtsboven op het bord, boven Keccles


def quote(a, n=99):
    """De les, de eerste n letters (het krijt schrijft)."""
    for i, q in enumerate(QUOTE):
        chalk_text(a, QX, QY + i * 14, q[:max(0, n)], 2)
        n -= len(q)
    return a


# ------------------------------------------------------------------ film
def build(preview=None):
    f = film.Film('keccles')
    s1, s2, s3 = shot1(), shot2(), plan_bg()
    k0, k1 = kec_full(0), quote(kec_full(1))
    p = film.auto_palettes([s1, s2, s3, k0, k1], [BLACK, CHALK, RED], n_free=12)
    pal = [x[:15] for x in p]

    def ps(k=1.0, white=0.0):
        return f.palset(*[[fa.mix(fa.shade(c, k), WHITE, white) for c in q] for q in pal])

    f.ref = ps()
    for t in range(T_IN):
        f.add(None, ps(0.0))
    for t in range(T_IN, T_FADE):
        f.add(s1, ps((t - T_IN + 1) / (T_FADE - T_IN)))
    f.add(s1, f.ref, T_SHOT2 - T_FADE)
    f.add(s2, f.ref, T_SHOT3 - T_SHOT2)
    f.add(camo(0, 0, 1.0), f.ref, T_EYE - T_SHOT3)
    eyes = [camo(1), camo(2)]
    f.add(eyes[0], f.ref, 3)
    f.add(eyes[1], f.ref, 8)
    f.add(eyes[0], f.ref, 2)                 # knipper
    f.add(eyes[1], f.ref, T_RIPPLE - T_EYE - 13)
    ys = np.nonzero(MASK.any(1))[0]
    top, bot = ys.min(), ys.max()
    for t in range(T_RIPPLE, T_RIPPLE_END, 2):
        u = (t - T_RIPPLE) / (T_RIPPLE_END - T_RIPPLE - 2)
        f.add(ripple(int(top - 10 + (bot - top + 22) * u)), f.ref, 2)
    f.add(k0, f.ref, T_GRIN - T_RIPPLE_END)
    f.add(kec_full(1), f.ref, T_QUOTE - T_GRIN)
    nq = sum(len(q) for q in QUOTE)
    for n in range(1, nq):
        if QUOTE[0][:n].endswith(' ') or (n > len(QUOTE[0]) and QUOTE[1][:n - len(QUOTE[0])].endswith(' ')):
            continue        # spaties: geen eigen beeld
        f.add(quote(kec_full(1), n), f.ref, QUOTE_SPEED)
    while len(f.frames) < T_QUOTE + nq * QUOTE_SPEED:
        f.add(k1, f.ref)
    for t in range(T_QUOTE + nq * QUOTE_SPEED, T_END):
        w = max(0.0, (t - T_WHITE + 1) / (T_END - T_WHITE))
        f.add(k1, ps(1.0, min(1.0, w)))
    f.encode(preview)
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    f = build(d)
    if d:
        print('KECCLES: T_QUOTE %d, T_WHITE %d, T_END %d' % (T_QUOTE, T_WHITE, T_END))
        film.sheet(f.preview_frames, [30, 70, 110, 128, 140, 152, 168, 190, 200, 210, 260, T_WHITE - 2],
                   os.path.join(d, 'keccles_keys.png'))
