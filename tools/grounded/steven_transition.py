#!/usr/bin/env python3
"""Project Grounded: B_TRANSITION_STEVEN (kampioen Steven, ook post-game en in het Battle Stadium).

Stevens verzamelkast: edelstenen op donker fluweel in vakjes met messing randen, elk met een plaatje ("ROCK",
"ALSO ROCK", ... en in het midden "THE ROCK"). De middelste steen begint te gloeien, de rest van de kast wordt donker,
de camera zoomt in op de facetten, en in de acht kite-facetten rond het tafelvlak verschijnen een voor een de acht
badges (gespiegeld in de kleur van de steen). Dan barst de steen en spat hij uiteen, wit, gevecht.

Film (zie film.py): per gameframe een beeld; tiles/tilemaps/paletten naar graphics/battle_transitions/film_steven*.
Gebruik: python3 tools/grounded/steven_transition.py [voorbeeldmap]
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
from film import W, H, text35, text35_width

ROOT = film.ROOT

# ------------------------------------------------------------------ tijdlijn (gameframes)
T_IN = 8          # 0-7 leeg (de wereld wordt zwart), dan de kast uit het zwart
T_HOLD = 24
T_GLOW = 56       # de middelste steen gaat gloeien
T_ZOOM = 96
T_CLOSE = 140     # close-up van de facetten
T_BADGE = 146     # eerste badge (nog in de blauwe kleur van de steen), daarna elke BADGE_GAP frames
BADGE_GAP = 4
T_LIGHT = 182     # de badges lichten een voor een op in hun echte kleur, elk met een klap (LIGHT_GAP frames per badge)
LIGHT_GAP = 8
T_CRACK = T_LIGHT + 8 * LIGHT_GAP + 10    # barsten op T_CRACK, +6, +12 (eerst even alle acht verlicht)
T_SHATTER = T_CRACK + 18
T_END = T_SHATTER + 26

# ------------------------------------------------------------------ kleuren
V = [(18, 8, 34), (30, 14, 54), (44, 22, 74), (60, 32, 96)]        # fluweel, donker -> licht
B = [(70, 44, 18), (122, 86, 34), (182, 140, 60), (232, 198, 110)]  # messing
K = (6, 2, 10)
TXT = (34, 20, 8)
WH = (248, 248, 248)
HERO = [(14, 28, 64), (34, 70, 138), (66, 126, 202), (128, 188, 240), (200, 236, 255)]
GLOW = [(46, 70, 124), (96, 150, 214)]
RUBY = [(112, 10, 34), (198, 34, 66), (250, 120, 140)]
EMER = [(10, 76, 44), (30, 156, 84), (130, 226, 160)]
AMET = [(70, 28, 110), (140, 72, 200), (204, 156, 250)]


def mix(a, b, k):
    return tuple(a[i] + (b[i] - a[i]) * k for i in range(3))


def palset(f, fade=1.0, dim=0.0, glow=0.0, shimmer=None, white=0.0, badges=False):
    """fade: 0 = zwart, 1 = normaal; dim: de kast (fluweel, messing, kleine stenen) donkerder; glow: de middelste
    steen en zijn gloed; shimmer: fase van het glinsteren (per tint een eigen golf); white: naar wit."""
    def tr(c, case):
        if case:
            c = mix(c, (0, 0, 0), dim * 0.55)
        c = mix((0, 0, 0), c, fade)
        return mix(c, (255, 255, 255), white)
    hero = []
    for i, c in enumerate(HERO):
        k = glow * 0.12
        if shimmer is not None:
            k += 0.14 * max(0.0, math.sin(shimmer + i * 1.9))
        hero.append(mix(c, (255, 255, 255), min(k, 0.8)))
    g = [mix(V[2], GLOW[0], glow), mix(V[3], GLOW[1], glow)]
    p13 = [tr(c, True) for c in V] + [tr(c, False) for c in g] + [tr(c, False) for c in hero] + [tr(WH, False)] + \
          [tr(c, True) for c in B[1:]]
    p14 = [tr(c, True) for c in V] + [tr(c, True) for c in RUBY + EMER + AMET] + [tr(WH, True)]
    p15 = [tr(K, True)] + [tr(c, True) for c in V] + [tr(c, True) for c in B] + [tr(WH, True), tr(TXT, True)]
    if badges:
        # close-up met verlichte badges: BG 14/15 = de steen (zelfde tinten als BG 13) + de echte badgekleuren (de
        # kast is dan niet in beeld)
        p14 = [tr(c, False) for c in hero] + [tr(WH, False)] + [tr(c, False) for k in (0, 2, 4, 6) for c in BADGE_REAL[k]]
        p15 = [tr(c, False) for c in hero] + [tr(WH, False)] + [tr(c, False) for k in (1, 3, 5, 7) for c in BADGE_REAL[k]]
    return f.palset(p13, p14, p15)


# ------------------------------------------------------------------ camera
GEM = (120.0, 70.0)
RH = 30.0
S_CLOSE = 78.0 / RH


class Cam:
    def __init__(self, s=1.0, cx=120.0, cy=80.0):
        self.s, self.cx, self.cy = s, cx, cy

    def p(self, x, y):
        return (120 + (x - self.cx) * self.s, 80 + (y - self.cy) * self.s)


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def zoom_cam(u):
    e = ease(u)
    # schaal exponentieel (gelijkmatig gevoel), midden schuift naar de steen
    s = math.exp(math.log(S_CLOSE) * e)
    return Cam(s, 120 + (GEM[0] - 120) * e, 80 + (GEM[1] - 80) * e)


# ------------------------------------------------------------------ tekenen
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


def velvet(cam, light=0.0):
    """Fluweel met een vignet rond de steen. Het niveau wordt per tile bepaald (niet per pixel) en tussenstanden zijn een
    vast Bayer-patroon: zo blijven er maar een handvol verschillende fluweeltiles over, ook tijdens het zoomen."""
    ty, tx = np.mgrid[0:20, 0:30].astype(np.float64)
    wx = (tx * 8 + 4 - 120) / cam.s + cam.cx
    wy = (ty * 8 + 4 - 80) / cam.s + cam.cy
    d = np.hypot(wx - GEM[0], (wy - GEM[1]) * 1.2)
    L = np.clip(3.3 - d / 30.0 + light, 0, 3.0)
    L = np.round(L * 4) / 4.0                      # kwart-stappen
    lo = np.floor(L).astype(int)
    fr = L - lo
    big_lo = np.kron(lo, np.ones((8, 8), int))
    big_fr = np.kron(fr, np.ones((8, 8)))
    ys, xs = np.mgrid[0:H, 0:W]
    lv = np.minimum(big_lo + (BAYER[ys % 4, xs % 4] < big_fr - 1e-9), 3)
    img = np.zeros((H, W, 3), np.uint8)
    for i in range(4):
        img[lv == i] = V[i]
    return img


def rect(dr, cam, x0, y0, x1, y1, col):
    a = cam.p(x0, y0)
    b = cam.p(x1, y1)
    x0, y0, x1, y1 = round(a[0]), round(a[1]), round(b[0]) - 1, round(b[1]) - 1
    if x1 >= x0 and y1 >= y0:
        dr.rectangle([x0, y0, x1, y1], fill=col)


def bar(dr, cam, x0, y0, x1, y1, vertical):
    """Messing lat met afschuining (licht links/boven, donker rechts/onder)."""
    n = 4
    for i in range(n):
        col = B[3 - i]
        if vertical:
            rect(dr, cam, x0 + (x1 - x0) * i / n, y0, x0 + (x1 - x0) * (i + 1) / n, y1, col)
        else:
            rect(dr, cam, x0, y0 + (y1 - y0) * i / n, x1, y0 + (y1 - y0) * (i + 1) / n, col)


COMPARTMENTS = [(5, 5, 74, 77), (5, 80, 74, 155), (77, 5, 163, 155), (166, 5, 235, 77), (166, 80, 235, 155)]


def case(dr, cam):
    # binnenschaduw van elk vak (fluweel ligt dieper)
    for (x0, y0, x1, y1) in COMPARTMENTS:
        rect(dr, cam, x0, y0, x1, y0 + 3, V[0])
        rect(dr, cam, x0, y0, x0 + 3, y1, V[0])
    # buitenrand
    bar(dr, cam, 0, 0, 240, 5, False)
    bar(dr, cam, 0, 155, 240, 160, False)
    bar(dr, cam, 0, 0, 5, 160, True)
    bar(dr, cam, 235, 0, 240, 160, True)
    for x in (74, 163):
        bar(dr, cam, x, 5, x + 3, 155, True)
    for (x0, x1) in ((5, 74), (166, 235)):
        bar(dr, cam, x0, 77, x1, 80, False)


def brilliant_facets(cx, cy, rx, ry, square=0.0, rot=0.0):
    """Facetten van een briljant (bovenaanzicht): (polygoon, soort, hoek). Soorten: table, star, kite, girdle."""
    def pt(r, a):
        # squircle-achtige rand voor cushion-stenen
        c, s = math.cos(a), math.sin(a)
        if square:
            n = 2 + 4 * square
            k = (abs(c) ** n + abs(s) ** n) ** (-1.0 / n)
            k = 1 + (k - 1) * min(r, 1.0)
        else:
            k = 1
        return (cx + rx * r * c * k, cy + ry * r * s * k)
    d = math.pi / 8
    out = []
    T = [pt(0.5, rot + 2 * d * k - math.pi / 2) for k in range(8)]
    P = [pt(0.78, rot + 2 * d * k + d - math.pi / 2) for k in range(8)]
    G = [pt(1.0, rot + d * k - math.pi / 2) for k in range(16)]
    out.append((T, 'table', 0.0))
    for k in range(8):
        a = rot + 2 * d * k + d - math.pi / 2
        out.append(([T[k], T[(k + 1) % 8], P[k]], 'star', a))
    for k in range(8):
        a = rot + 2 * d * k - math.pi / 2
        out.append(([T[k], P[(k - 1) % 8], G[2 * k], P[k]], 'kite', a))
    for k in range(8):
        a = rot + 2 * d * k + d - math.pi / 2
        out.append(([P[k], G[2 * k], G[2 * k + 1]], 'girdle', a - d / 2))
        out.append(([P[k], G[2 * k + 1], G[(2 * k + 2) % 16]], 'girdle', a + d / 2))
    return out, G


LIGHT = -3 * math.pi / 4   # licht van linksboven


def facet_tone(kind, a, n):
    """Tint 0..n-1 per facet (n = aantal tinten in de kleurenreeks)."""
    lit = math.cos(a - LIGHT)
    if kind == 'table':
        t = 0.62
    elif kind == 'star':
        t = 0.45 + 0.3 * lit
    elif kind == 'kite':
        t = 0.5 + 0.45 * lit
    else:
        t = 0.3 + 0.45 * lit
    return int(round(min(max(t, 0), 1) * (n - 1)))


def draw_brilliant(dr, cam, cx, cy, rx, ry, ramp, square=0.0, glint=True, skip=()):
    facets, G = brilliant_facets(cx, cy, rx, ry, square)
    polys = []
    for i, (poly, kind, a) in enumerate(facets):
        sp = [cam.p(*q) for q in poly]
        polys.append((sp, kind, a))
        if i in skip:
            continue
        tone = facet_tone(kind, a, len(ramp))
        col = ramp[tone]
        # glinsters: het tafelvlak linksboven en twee facetten krijgen wit
        if glint and kind == 'kite' and abs(math.cos(a - LIGHT) - 1) < 0.05:
            col = WH
        dr.polygon(sp, fill=col)
    # facetranden in de donkerste tint (1 px), rand rondom
    for (sp, kind, a) in polys:
        dr.line(sp + [sp[0]], fill=ramp[0], width=1)
    return polys


def draw_emerald_cut(dr, cam, cx, cy, w, h, ramp):
    """Smaragdslijpsel: rechthoek met afgeschuinde hoeken, drie trappen naar het tafelvlak."""
    def octa(sw, sh, c):
        return [(cx - sw + c, cy - sh), (cx + sw - c, cy - sh), (cx + sw, cy - sh + c), (cx + sw, cy + sh - c),
                (cx + sw - c, cy + sh), (cx - sw + c, cy + sh), (cx - sw, cy + sh - c), (cx - sw, cy - sh + c)]
    rings = [octa(w / 2 * f, h / 2 * f, 4 * f) for f in (1.0, 0.78, 0.56, 0.36)]
    side_tone = [2, 2, 1, 0, 0, 0, 1, 2]     # per zijde (boven, rb, rechts, ...) licht van linksboven
    for r in range(3):
        o, i = rings[r], rings[r + 1]
        for k in range(8):
            q = [o[k], o[(k + 1) % 8], i[(k + 1) % 8], i[k]]
            t = min(2, max(0, side_tone[k] - (1 if r == 1 else 0) + (1 if r == 2 else 0)))
            dr.polygon([cam.p(*p) for p in q], fill=ramp[t])
    dr.polygon([cam.p(*p) for p in rings[3]], fill=ramp[1])
    for ring in rings:
        sp = [cam.p(*p) for p in ring]
        dr.line(sp + [sp[0]], fill=ramp[0], width=1)
    # glinster
    a = cam.p(cx - w / 2 * 0.62, cy - h / 2 * 0.55)
    dr.rectangle([a[0], a[1], a[0] + max(1, cam.s) - 1, a[1] + max(1, cam.s) - 1], fill=WH)


def plaque_img(text):
    w = text35_width(text) + 6
    im = Image.new('RGB', (w, 9), B[2])
    d = ImageDraw.Draw(im)
    d.line([(0, 0), (w - 1, 0)], fill=B[3])
    d.line([(0, 8), (w - 1, 8)], fill=B[0])
    d.line([(0, 0), (0, 8)], fill=B[3])
    d.line([(w - 1, 0), (w - 1, 8)], fill=B[0])
    text35(lambda x, y: im.putpixel((x, y), TXT), 3, 2, text)
    return im


PLAQUES = [((40, 63), 'ROCK'), ((40, 140), 'ROCK (WET)'), ((200, 63), 'NICE ROCK'), ((200, 140), 'ALSO ROCK'),
           ((120, 128), 'THE ROCK')]
PLAQUE_IMGS = [(c, plaque_img(t)) for c, t in PLAQUES]


def paste_scaled(img, cam, pim, wx, wy):
    """Plakt een 1x-plaatje (gecentreerd op wereldpunt wx, wy) geschaald met de camera."""
    w, h = pim.size
    sw, sh = max(1, int(round(w * cam.s))), max(1, int(round(h * cam.s)))
    big = pim.resize((sw, sh), Image.NEAREST)
    x, y = cam.p(wx - w / 2, wy - h / 2)
    img.paste(big, (int(round(x)), int(round(y))))


def scene(cam, glow_level=0, twinkle=0):
    img = Image.fromarray(velvet(cam))
    dr = ImageDraw.Draw(img)
    case(dr, cam)
    # gloed rond de middelste steen (in het eigen vak)
    if glow_level:
        arr = np.array(img)
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float64)
        wx = (xs - 120) / cam.s + cam.cx
        wy = (ys - 80) / cam.s + cam.cy
        inside = (wx > 78) & (wx < 162) & (wy > 6) & (wy < 154)
        b = BAYER[ys.astype(int) % 4, xs.astype(int) % 4]
        # sterkte per tile (afstand van het midden van de tile, in kwarten): weinig verschillende tiles
        ty, tx = np.mgrid[0:20, 0:30].astype(np.float64)
        dt = np.hypot((tx * 8 + 4 - 120) / cam.s + cam.cx - GEM[0], (ty * 8 + 4 - 80) / cam.s + cam.cy - GEM[1])
        outer = RH + 2 + 2.6 * glow_level
        inner = RH + 1 + 1.6 * glow_level
        f0 = np.kron(np.round(np.clip((outer - dt) / 6.0, 0, 1) * 4) / 4, np.ones((8, 8)))
        f1 = np.kron(np.round(np.clip((inner - dt) / 4.0, 0, 1) * 4) / 4, np.ones((8, 8)))
        m0 = inside & (b < f0 - 1e-9)
        m1 = inside & (b < f1 - 1e-9)
        arr[m0] = GLOW[0]
        arr[m1] = GLOW[1]
        img = Image.fromarray(arr)
        dr = ImageDraw.Draw(img)
    draw_brilliant(dr, cam, 40, 36, 13, 13, RUBY + [WH])
    draw_emerald_cut(dr, cam, 40, 110, 28, 20, EMER)
    draw_brilliant(dr, cam, 200, 36, 10, 14, AMET + [WH])
    draw_brilliant(dr, cam, 200, 110, 13, 13, B[1:] + [WH], square=0.7)
    draw_brilliant(dr, cam, GEM[0], GEM[1], RH, RH, HERO)
    for (c, pim) in PLAQUE_IMGS:
        paste_scaled(img, cam, pim, *c)
    if twinkle:
        x, y = cam.p(GEM[0] - 13, GEM[1] - 14)
        L = 2 + twinkle * 2
        dr.line([(x - L, y), (x + L, y)], fill=WH)
        dr.line([(x, y - L), (x, y + L)], fill=WH)
        dr.line([(x - L // 2, y - L // 2), (x + L // 2, y + L // 2)], fill=HERO[4])
        dr.line([(x - L // 2, y + L // 2), (x + L // 2, y - L // 2)], fill=HERO[4])
        dr.point([(x, y)], fill=WH)
    return img


# ------------------------------------------------------------------ badges in de facetten
BADGES = Image.open(os.path.join(ROOT, 'graphics/trainer_card/badges.png'))
BADGE_TONE = {15: 0, 4: 2, 3: 3, 2: 4, 1: 4}
# de echte kleuren (donker, licht) van Stone, Knuckle, Dynamo, Heat, Balance, Feather, Mind, Rain; de grijze
# trainerkaart-badges (index 1 wit, 2 licht, 3/4 donker, 15 rand) worden daarmee gekleurd
BADGE_REAL = [
    [(120, 104, 96), (192, 176, 160)],     # Stone: steengrijs
    [(208, 88, 32), (248, 168, 80)],       # Knuckle: oranje
    [(208, 152, 16), (248, 224, 80)],      # Dynamo: goud/geel
    [(200, 32, 24), (248, 112, 64)],       # Heat: vuurrood
    [(168, 96, 48), (232, 168, 112)],      # Balance: koper
    [(120, 64, 176), (200, 152, 240)],     # Feather: paars
    [(208, 56, 136), (248, 152, 200)],     # Mind: roze
    [(16, 120, 200), (120, 208, 248)],     # Rain: blauw
]


def badge_rgba(k, scale=2, real=False, hot=False):
    """Badge k (16x16, vergroot). real: in zijn echte kleuren (anders in de tinten van de steen); hot: lichter (de
    klap bij het oplichten)."""
    a = np.array(BADGES)[:, k * 16:(k + 1) * 16]
    im = np.zeros((16, 16, 4), np.uint8)
    for v, t in BADGE_TONE.items():
        if real:
            col = {15: HERO[0], 4: BADGE_REAL[k][0], 3: BADGE_REAL[k][0], 2: BADGE_REAL[k][1], 1: WH}[v]
            if hot and v in (3, 4):
                col = BADGE_REAL[k][1]
            if hot and v == 2:
                col = WH
        else:
            col = HERO[t]
        im[a == v, :3] = col
        im[a == v, 3] = 255
    out = Image.fromarray(im, 'RGBA')
    return out.resize((int(16 * scale), int(16 * scale)), Image.NEAREST)


CLOSE = Cam(S_CLOSE, GEM[0], GEM[1])


def kite_polys(cam):
    facets, _ = brilliant_facets(GEM[0], GEM[1], RH, RH)
    return [[cam.p(*q) for q in poly] for poly, kind, a in facets if kind == 'kite']


def closeup(nbadges, flash=-1, crack=0, lit=0, pop=-1):
    """nbadges: zoveel badges staan in de facetten; lit: de eerste lit daarvan in hun echte kleur; pop: deze badge
    springt even groot en licht uit zijn facet (de klap bij het oplichten)."""
    img = scene(CLOSE, glow_level=4)
    kites = kite_polys(CLOSE)
    for k in range(8):
        poly = kites[k]
        if k == flash:
            ImageDraw.Draw(img).polygon(poly, fill=WH)
            continue
        if k < nbadges:
            cx = sum(p[0] for p in poly) / 4
            cy = sum(p[1] for p in poly) / 4
            b = badge_rgba(k, real=k < lit)
            mask = Image.new('L', img.size, 0)
            ImageDraw.Draw(mask).polygon(poly, fill=255)
            layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
            layer.paste(b, (int(round(cx - 16)), int(round(cy - 16))))
            al = np.minimum(np.array(layer)[:, :, 3], np.array(mask))
            arr = np.array(img)
            arr[al > 0] = np.array(layer)[:, :, :3][al > 0]
            img = Image.fromarray(arr)
    # de facetranden er weer over (de badge ligt "in" het facet)
    dr = ImageDraw.Draw(img)
    for poly in kites:
        dr.line(poly + [poly[0]], fill=HERO[0], width=1)
    if pop >= 0:
        # de klap: de badge 1,5x zo groot en licht, over de facetrand heen
        poly = kites[pop]
        cx = sum(p[0] for p in poly) / 4
        cy = sum(p[1] for p in poly) / 4
        b = badge_rgba(pop, scale=3, real=True, hot=True)
        img.paste(b, (int(round(cx - 24)), int(round(cy - 24))), b)
    if crack:
        draw_cracks(dr, crack)
    return img


def crack_paths():
    rng = np.random.RandomState(7)
    paths = []
    for k in range(7):
        a = k * 2 * math.pi / 7 + rng.uniform(-0.3, 0.3)
        pts = [(120.0, 80.0)]
        r = 0.0
        while r < 120:
            r += rng.uniform(9, 16)
            aa = a + rng.uniform(-0.28, 0.28)
            pts.append((120 + r * math.cos(aa), 80 + r * math.sin(aa) * 0.95))
        paths.append(pts)
    return paths


CRACKS = crack_paths()


def draw_cracks(dr, stage):
    lim = [0, 34, 70, 140][stage]
    for pts in CRACKS:
        acc = 0
        for a, b in zip(pts, pts[1:]):
            l = math.hypot(b[0] - a[0], b[1] - a[1])
            if acc >= lim:
                break
            if acc + l > lim:
                f = (lim - acc) / l
                b = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
            dr.line([a, b], fill=HERO[0], width=3)
            dr.line([a, b], fill=WH, width=1)
            acc += l


# ------------------------------------------------------------------ uiteenspatten
def shards_from(img):
    """Knipt elk facet uit het close-upbeeld als losse scherf (RGBA + middelpunt)."""
    facets, _ = brilliant_facets(GEM[0], GEM[1], RH, RH)
    out = []
    arr = np.array(img)
    pieces = []
    for poly, kind, a in facets:
        if kind == 'table':
            for k in range(8):
                pieces.append(([GEM, poly[k], poly[(k + 1) % 8]], 'table'))
        else:
            pieces.append((poly, kind))
    for poly, kind in pieces:
        sp = [CLOSE.p(*q) for q in poly]
        xs = [p[0] for p in sp]
        ys = [p[1] for p in sp]
        x0, y0, x1, y1 = int(min(xs)) - 1, int(min(ys)) - 1, int(max(xs)) + 2, int(max(ys)) + 2
        mask = Image.new('L', img.size, 0)
        ImageDraw.Draw(mask).polygon(sp, fill=255, outline=255)
        m = np.array(mask) > 0
        rgba = np.zeros((H, W, 4), np.uint8)
        rgba[..., :3] = arr
        rgba[..., 3] = m * 255
        x0c, y0c, x1c, y1c = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
        if x1c <= x0c or y1c <= y0c:
            continue
        piece = Image.fromarray(rgba[y0c:y1c, x0c:x1c], 'RGBA')
        cx, cy = (x0c + x1c) / 2, (y0c + y1c) / 2
        out.append((piece, cx, cy, kind))
    return out


def shatter(base_bg, shards, tau):
    img = base_bg.copy()
    rng = np.random.RandomState(3)
    # witte kern die groeit
    dr = ImageDraw.Draw(img)
    r = 6 + tau * 7
    for rr, col in ((r + 6, HERO[3]), (r + 3, HERO[4]), (r, WH)):
        dr.ellipse([120 - rr, 80 - rr * 0.9, 120 + rr, 80 + rr * 0.9], fill=col)
    for i, (piece, cx, cy, kind) in enumerate(shards):
        dx, dy = cx - 120, cy - 80
        dist = math.hypot(dx, dy) or 1
        sp = 4.5 + rng.uniform(0, 3)
        ox = dx / dist * sp * tau * (1 + tau * 0.12)
        oy = dy / dist * sp * tau * (1 + tau * 0.12) + 0.08 * tau * tau
        ang = rng.uniform(-14, 14) * tau
        sc = 1 + 0.05 * tau
        p = piece
        if sc != 1:
            p = p.resize((max(1, int(p.width * sc)), max(1, int(p.height * sc))), Image.NEAREST)
        p = p.rotate(ang, resample=Image.NEAREST, expand=True)
        img.paste(p, (int(round(cx + ox - p.width / 2)), int(round(cy + oy - p.height / 2))), p)
    return img


# ------------------------------------------------------------------ film opbouwen
def build(preview=None):
    f = film.Film('steven')
    f.ref = palset(f)
    arr = lambda im: np.array(im.convert('RGB'))

    base = arr(scene(Cam()))
    for t in range(T_IN):
        f.add(None, palset(f, fade=0))
    for t in range(T_IN, T_HOLD):
        f.add(base, palset(f, fade=(t - T_IN + 1) / (T_HOLD - T_IN)))
    for t in range(T_HOLD, T_GLOW):
        f.add(base, palset(f))
    glow_imgs = {}
    for t in range(T_GLOW, T_ZOOM):
        u = (t - T_GLOW) / (T_ZOOM - T_GLOW)
        lvl = min(4, 1 + int(u * 5))
        tw = 0
        if t >= T_GLOW + 22:
            tw = [1, 2, 3, 2, 1, 2, 3, 3][min(7, (t - T_GLOW - 22) // 2)]
        key = (lvl, tw)
        if key not in glow_imgs:
            glow_imgs[key] = arr(scene(Cam(), glow_level=lvl, twinkle=tw))
        f.add(glow_imgs[key], palset(f, dim=u, glow=u, shimmer=t * 0.25))
    zimg = None
    for t in range(T_ZOOM, T_CLOSE):
        if (t - T_ZOOM) % 2 == 0:
            u = min(1.0, (t - T_ZOOM + 2) / (T_CLOSE - T_ZOOM - 2))
            zimg = arr(scene(zoom_cam(u), glow_level=4))
        f.add(zimg, palset(f, dim=1, glow=1, shimmer=t * 0.25))
    cache = {}
    for t in range(T_CLOSE, T_LIGHT):
        nb = 0 if t < T_BADGE else min(8, (t - T_BADGE) // BADGE_GAP + 1)
        flash = -1
        if T_BADGE <= t < T_BADGE + 8 * BADGE_GAP and (t - T_BADGE) % BADGE_GAP < 2:
            flash = nb - 1
            nb -= 1
        key = (nb, flash)
        if key not in cache:
            cache[key] = arr(closeup(nb, flash))
        f.add(cache[key], palset(f, dim=1, glow=1, shimmer=t * 0.3))
    # oplichten: per badge 2 frames wit facet, 2 frames groot en licht (de klap), dan in zijn echte kleur
    qb = palset(f, badges=True)
    for t in range(T_LIGHT, T_CRACK):
        u = t - T_LIGHT
        k, ph = u // LIGHT_GAP, u % LIGHT_GAP
        if k >= 8:
            key = ('lit', 8, -1, -1)
        elif ph < 2:
            key = ('lit', k, k, -1)
        elif ph < 4:
            key = ('lit', k + 1, -1, k)
        else:
            key = ('lit', k + 1, -1, -1)
        if key not in cache:
            _, lit, fl, pop = key
            cache[key] = arr(closeup(8, flash=fl, lit=lit, pop=pop))
        f.add(cache[key], palset(f, dim=1, glow=1, shimmer=t * 0.3, badges=True), q=qb)
    for t in range(T_CRACK, T_SHATTER):
        st = 1 + min(2, (t - T_CRACK) // 6)
        key = ('c', st)
        if key not in cache:
            cache[key] = arr(closeup(8, crack=st, lit=8))
        f.add(cache[key], palset(f, dim=1, glow=1 + 0.0, shimmer=t * 0.6, badges=True), q=qb)
    whole = closeup(8, lit=8)
    shards = shards_from(whole)
    bg = Image.fromarray(velvet(CLOSE))
    simg = None
    for t in range(T_SHATTER, T_END):
        tau = t - T_SHATTER
        if tau % 2 == 0:
            simg = arr(shatter(bg, shards, tau + 1))
        w = max(0.0, (tau - 14) / (T_END - T_SHATTER - 15))
        f.add(simg, palset(f, dim=1, glow=1, white=min(1.0, w), badges=True), q=qb)
    f.encode(preview)
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    f = build(d)
    if d:
        fr = f.preview_frames
        film.sheet(fr, [70, 150, 178, 183, 185, 188, 209, 213, 230, 246, T_CRACK + 14, T_SHATTER + 8],
                   os.path.join(d, 'steven_keys.png'))
        print('#define STEVEN_BADGE %d / BADGE_GAP %d / LIGHT %d / LIGHT_GAP %d / CRACK %d / SHATTER %d / END %d' %
              (T_BADGE, BADGE_GAP, T_LIGHT, LIGHT_GAP, T_CRACK, T_SHATTER, T_END))
