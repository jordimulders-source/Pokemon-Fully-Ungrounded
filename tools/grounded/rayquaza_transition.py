#!/usr/bin/env python3
"""Project Grounded: B_TRANSITION_RAYQUAZA_PILLAR (Rayquaza op de Sky Pillar, ook de shiny/Delta Episode).

Je kijkt omhoog langs de Sky Pillar, door de wolken. Een groene streep cirkelt om de top, steeds sneller en langer, tot
hij een gesloten, gloeiende ring is. Uit de ring breekt het silhouet van Rayquaza recht op de camera af: kop eerst,
de lange hoornvinnen naar achteren, het lijf in een S achter hem aan tot in de ring, de gele markeringen (ogen, bek,
vinnen, de ringen om het lijf) gloeien. De kop vult het beeld, groene flits, wit, gevecht.

Film (zie film.py): film_rayquaza*. Gebruik: python3 tools/grounded/rayquaza_transition.py [voorbeeldmap]
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
from film import W, H

# ------------------------------------------------------------------ tijdlijn
T_IN = 8
T_STREAK = 22      # de streep verschijnt
T_RING = 104       # de streep is een gesloten ring
T_BURST = 124      # Rayquaza breekt eruit
T_FILL = 166       # de kop vult het beeld
T_END = 180

# ------------------------------------------------------------------ kleuren
SKY = [(8, 12, 44), (14, 26, 74), (26, 46, 110), (42, 76, 150), (70, 112, 190)]
CLOUD = [(232, 238, 250), (178, 194, 226), (124, 142, 192), (80, 96, 150)]
STONE = [(26, 32, 34), (50, 58, 58), (82, 92, 88), (120, 130, 122), (166, 174, 158)]
MOSS = [(36, 66, 38), (66, 104, 56)]
K = (4, 6, 14)
RING = [(18, 84, 40), (40, 164, 72), (120, 230, 120), (220, 255, 210)]
RAY = [(6, 18, 12), (14, 40, 28), (34, 96, 58)]           # silhouet: zwartgroen, donkergroen, randlicht
GOLD = [(140, 88, 10), (232, 176, 32), (255, 242, 120)]
WH = (250, 252, 250)


def mix(a, b, k):
    return tuple(a[i] + (b[i] - a[i]) * k for i in range(3))


def palset(f, fade=1.0, dim=0.0, glow=0.0, white=0.0, green=0.0):
    """fade: uit het zwart; dim: de wereld donkerder; glow: ring en markeringen feller; white/green: flitsen."""
    def tr(c, world):
        if world:
            c = mix(c, (0, 0, 0), dim * 0.6)
        else:
            c = mix(c, (255, 255, 255), glow * 0.25)
        c = mix((0, 0, 0), c, fade)
        c = mix(c, (60, 255, 120), green)
        return mix(c, (255, 255, 255), white)
    p15 = [tr(K, True)] + [tr(c, True) for c in SKY + CLOUD]
    p14 = [tr(K, True)] + [tr(c, True) for c in STONE + MOSS + SKY[:4]] + [tr(c, True) for c in CLOUD[:2]]
    p13 = [tr(c, False) for c in RING + [WH]] + [tr(c, True) for c in RAY] + [tr(c, False) for c in GOLD] + \
          [tr(c, True) for c in SKY[1:4]]
    return f.palset(p13, p14, p15)


BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
YS, XS = np.mgrid[0:H, 0:W]
BY = BAYER[YS % 4, XS % 4]

TOP = 30           # bovenkant van de pilaar (y)
RC = (120.0, 36.0) # midden van de ring (om de top)
RX, RY = 84.0, 17.0


def hw(y):
    return 22 + (y - TOP) * 0.42


def ramp(img, mask, level, cols):
    """Kleurt mask met een dithered verloop: level (0..len-1, float per pixel)."""
    lv = np.clip(np.floor(level + BY - 0.5 + 0.5).astype(int), 0, len(cols) - 1)
    for i, c in enumerate(cols):
        img[mask & (lv == i)] = c


def sky():
    img = np.zeros((H, W, 3), np.uint8)
    lev = (YS / 160.0) * 4.2
    ramp(img, np.ones((H, W), bool), lev, SKY)
    # een paar sterren boven in de lucht (zo hoog is het al bijna ruimte)
    rng = np.random.RandomState(4)
    for _ in range(18):
        x, y = rng.randint(0, W), rng.randint(0, 40)
        img[y, x] = CLOUD[1]
    return img


def pillar(img):
    """De Sky Pillar van onderen gezien: een ronde toren die naar boven smaller wordt, stenen blokken, mos, ramen."""
    cx = 120
    y = YS.astype(np.float64)
    h = hw(y)
    with np.errstate(all='ignore'):
        u = np.where(YS >= TOP, (XS - cx) / np.maximum(h, 1), 9.0)
    m = (YS >= TOP) & (np.abs(u) <= 1)
    # bolling: licht van links
    shade = 2.9 - 1.9 * u - 0.6 * u * u
    # rijen stenen (perspectief: dichter op elkaar naar boven)
    v = 900.0 / np.maximum(y - TOP + 30, 1)
    course = np.floor(v)
    fv = v - course
    phi = np.arcsin(np.clip(np.nan_to_num(u), -1, 1))
    col = (phi * 5 + course * 0.5) % 1.0
    joint = m & ((fv < 0.09 * (1 + (YS - TOP) / 60.0)) | (col < 0.05))
    shade = shade - joint * 1.4
    # brede banden (verdiepingen) met donkere boogramen
    band = (course % 6 == 0)
    shade = shade - (band * 0.7)
    win = m & (course % 6 == 3) & (np.abs(((phi * 3 / math.pi) % 1.0) - 0.5) < 0.12) & (fv > 0.25)
    shade = np.where(win, -1, shade)
    ramp(img, m, np.clip(shade, 0, 4.4), STONE)
    img[win] = K
    # mos: vlekken onderaan de banden
    rng = np.random.RandomState(8)
    noise = rng.rand(H // 4 + 1, W // 4 + 1)
    nz = np.kron(noise, np.ones((4, 4)))[:H, :W]
    moss = m & ~win & ((course % 6 == 1) | (course % 6 == 5)) & (nz > 0.62) & (u < 0.5)
    img[moss & (BY < 0.5)] = MOSS[1]
    img[moss & (BY >= 0.5)] = MOSS[0]
    # kantelen op de top
    for k in range(-3, 4):
        x0 = cx + k * 7 - 2
        img[TOP - 4:TOP, x0:x0 + 4] = STONE[2] if k < 0 else STONE[1]
        img[TOP - 4, x0:x0 + 4] = STONE[3] if k < 1 else STONE[2]
    return img


def cloud_layer(img, clouds, ofs=0.0):
    """Wolken als bollen: lichte bovenkant, donkere onderkant (van onderen gezien)."""
    pil = Image.fromarray(img)
    d = ImageDraw.Draw(pil)
    for (x, y, r) in clouds:
        x = x + ofs
        d.ellipse([x - r, y - r * 0.62, x + r, y + r * 0.62], fill=CLOUD[3])
    for (x, y, r) in clouds:
        x = x + ofs
        d.ellipse([x - r * 0.92, y - r * 0.62, x + r * 0.92, y + r * 0.38], fill=CLOUD[2])
    for (x, y, r) in clouds:
        x = x + ofs
        d.ellipse([x - r * 0.8, y - r * 0.6, x + r * 0.7, y + r * 0.12], fill=CLOUD[1])
    for (x, y, r) in clouds:
        x = x + ofs
        d.ellipse([x - r * 0.55, y - r * 0.56, x + r * 0.3, y - r * 0.18], fill=CLOUD[0])
    return np.array(pil)


def cloud_set(seed, n, y0, y1, r0, r1):
    rng = np.random.RandomState(seed)
    out = []
    for _ in range(n):
        cx, cy = rng.uniform(-20, 260), rng.uniform(y0, y1)
        for k in range(rng.randint(3, 6)):
            out.append((cx + rng.uniform(-r1, r1), cy + rng.uniform(-r0 * 0.3, r0 * 0.3), rng.uniform(r0, r1)))
    return out


FAR = cloud_set(1, 4, 58, 84, 7, 13)
NEAR = cloud_set(2, 5, 128, 158, 14, 26)


def background(dx_far=0.0, dx_near=0.0):
    img = sky()
    img = cloud_layer(img, FAR, dx_far)
    img = pillar(img)
    img = cloud_layer(img, NEAR, dx_near)
    return img


# ------------------------------------------------------------------ de groene streep / ring
def ring_pt(a, r=1.0):
    return RC[0] + RX * r * math.cos(a), RC[1] + RY * r * math.sin(a)


def behind(a):
    """Achter de pilaar: de bovenste helft van de ellips (sin < 0) binnen de breedte van de pilaar."""
    x, y = ring_pt(a)
    return math.sin(a) < 0 and abs(x - 120) < hw(max(y, TOP)) + 2


def draw_arc(img, a_head, length, thick, front_only=None, glow=1.0):
    """Tekent de streep: kop op hoek a_head, staart length radialen terug. Dikker en feller bij de kop."""
    pil = Image.fromarray(img)
    d = ImageDraw.Draw(pil)
    n = max(4, int(length * 40))
    pts = []
    for i in range(n + 1):
        a = a_head - length * i / n
        pts.append((a, i / n))
    for layer, col, wmul in ((0, RING[0], 1.0), (1, RING[1], 0.66), (2, RING[2], 0.38), (3, RING[3], 0.16)):
        for (a0, f0), (a1, f1) in zip(pts, pts[1:]):
            if front_only is not None and behind(a0) != (not front_only):
                continue
            w = thick * wmul * (1.0 - 0.75 * f0) * glow
            if w < 0.6:
                continue
            p0, p1 = ring_pt(a0), ring_pt(a1)
            d.line([p0, p1], fill=col, width=max(1, int(round(w))))
    return np.array(pil)


def streak_frame(base, t, sparks=True):
    """Fase 1: de streep draait om de top, steeds sneller en langer, tot een ring."""
    u = (t - T_STREAK) / float(T_RING - T_STREAK)
    a = 0.0
    # hoek = integraal van een versnellende hoeksnelheid
    a = -math.pi / 2 + 2 * math.pi * (1.6 * u * u + 1.4 * u ** 4) * 1.0
    length = min(2 * math.pi, 0.5 + 5.9 * u ** 1.6)
    thick = 4 + 6 * u
    img = draw_arc(base, a, length, thick, front_only=False)      # achter de pilaar (eerst)
    img = redraw_pillar_front(img, base)
    img = draw_arc(img, a, length, thick, front_only=True)
    if sparks:
        rng = np.random.RandomState(t)
        hx, hy = ring_pt(a)
        for _ in range(4 + int(8 * u)):
            sx, sy = hx + rng.uniform(-10, 10), hy + rng.uniform(-6, 6)
            if 0 <= sx < W and 0 <= sy < H:
                img[int(sy), int(sx)] = RING[3]
    return img


PILLAR_MASK = None


def redraw_pillar_front(img, base):
    """De pilaar opnieuw over het achterste deel van de streep (de wolken ervoor ook)."""
    global PILLAR_MASK
    if PILLAR_MASK is None:
        y = YS.astype(np.float64)
        PILLAR_MASK = ((YS >= TOP - 4) & (np.abs(XS - 120) <= hw(np.maximum(y, TOP))))
    out = img.copy()
    out[PILLAR_MASK] = base[PILLAR_MASK]
    return out


def ring_frame(base, t):
    """Fase 2: de gesloten ring draait en zwelt aan, lichtstralen."""
    u = (t - T_RING) / float(T_BURST - T_RING)
    a = t * 0.9
    thick = 10 + 5 * u + 2 * math.sin(t * 0.9)
    img = draw_arc(base, a, 2 * math.pi, thick, front_only=False)
    img = redraw_pillar_front(img, base)
    img = draw_arc(img, a, 2 * math.pi, thick, front_only=True)
    # vonken rond de ring
    rng = np.random.RandomState(t)
    for _ in range(26):
        aa = rng.uniform(0, 2 * math.pi)
        x, y = ring_pt(aa, rng.uniform(0.85, 1.25))
        if 0 <= x < W and 0 <= y < H:
            img[int(y), int(x)] = RING[3]
    return img


# ------------------------------------------------------------------ Rayquaza
# kop van voren (iets van onderen): breed plat voorhoofd, smalle snuit, open bek met tanden (hij brult je toe),
# twee lange hoorns die schuin naar achteren/buiten steken, kleinere vinnen bij de kaak. Eenheid = breedte van de kop.
SKULL = [(-0.5, -0.32), (-0.2, -0.46), (0.2, -0.46), (0.5, -0.32), (0.44, -0.06), (0.24, 0.16), (0.16, 0.24),
         (-0.16, 0.24), (-0.24, 0.16), (-0.44, -0.06)]
JAW = [(-0.3, 0.3), (0.3, 0.3), (0.2, 0.6), (0.08, 0.68), (-0.08, 0.68), (-0.2, 0.6)]
MAW = [(-0.2, 0.2), (0.2, 0.2), (0.25, 0.34), (-0.25, 0.34)]                  # donkere bek tussen de kaken
HORN = [(-0.3, -0.36), (-0.62, -0.62), (-1.55, -0.98), (-0.9, -0.5), (-0.46, -0.2)]
HORN2 = [(-0.44, -0.12), (-0.86, -0.18), (-1.3, -0.08), (-0.82, -0.02), (-0.44, 0.02)]
JAWFIN = [(-0.22, 0.42), (-0.58, 0.66), (-0.16, 0.56)]
EYE = [(-0.42, -0.2), (-0.16, -0.27), (-0.12, -0.2), (-0.34, -0.13)]
PUPIL = [(-0.27, -0.25), (-0.24, -0.25), (-0.23, -0.16), (-0.26, -0.16)]
HORN_LINE = [(-0.42, -0.38), (-0.7, -0.6), (-1.36, -0.92)]
HORN2_LINE = [(-0.52, -0.08), (-0.9, -0.11), (-1.18, -0.08)]
LIP = [(-0.22, 0.17), (-0.1, 0.22), (0.1, 0.22), (0.22, 0.17)]
FANGS = [[(-0.18, 0.2), (-0.13, 0.2), (-0.155, 0.29)], [(0.13, 0.2), (0.18, 0.2), (0.155, 0.29)],
         [(-0.12, 0.34), (-0.07, 0.34), (-0.095, 0.27)], [(0.07, 0.34), (0.12, 0.34), (0.095, 0.27)]]
SNOUT_MARK = [(-0.07, -0.42), (0.0, -0.1), (0.07, -0.42)]


def mirror(pts):
    return [(-x, y) for x, y in pts]


def draw_rayquaza(img, cx, cy, s, glow, shake=(0, 0)):
    """Silhouet met gloeiende markeringen. s = breedte van de kop in pixels; (cx, cy) = midden van de kop.
    Het lijf loopt in een S van de kop terug naar het midden van de ring (perspectief), met gele ringen."""
    pil = Image.fromarray(img)
    d = ImageDraw.Draw(pil)
    ox, oy = shake
    gold = GOLD[2] if glow > 0.5 else GOLD[1]

    def P(pts, x0=cx, y0=cy, sc=1.0):
        return [(x0 + ox + x * s * sc, y0 + oy + y * s * sc) for x, y in pts]
    # lijf: van de ring (ver, klein) naar de kop (dichtbij, groot)
    n = 22
    for i in range(n, 0, -1):
        f = i / float(n)                               # 1 = bij de ring, 0 = bij de kop
        k = 1.0 / (1.0 + 7.0 * f)                      # perspectief
        bx = cx + (RC[0] - cx) * f ** 0.8 + math.sin(f * 7.0) * s * 0.55 * k
        by = cy + (RC[1] - cy) * f ** 0.8 + math.cos(f * 5.0) * s * 0.2 * k - s * 0.15 * k
        r = 0.34 * s * k
        if r < 0.7:
            continue
        d.ellipse([bx + ox - r, by + oy - r, bx + ox + r, by + oy + r], fill=RAY[0], outline=RAY[2])
        if i % 3 == 0 and r > 2:
            rr = r * 0.78
            d.ellipse([bx + ox - rr, by + oy - rr * 0.45, bx + ox + rr, by + oy + rr * 0.45], outline=gold,
                      width=max(1, int(r * 0.14)))
    lw = max(1, int(round(s * 0.03)))
    for poly in (HORN, mirror(HORN), HORN2, mirror(HORN2), JAWFIN, mirror(JAWFIN)):
        d.polygon(P(poly), fill=RAY[0], outline=RAY[2])
    for line in (HORN_LINE, mirror(HORN_LINE), HORN2_LINE, mirror(HORN2_LINE)):
        d.line(P(line), fill=GOLD[1], width=lw)
    d.polygon(P(JAW), fill=RAY[0], outline=RAY[2])
    d.polygon(P([(-0.3, 0.3), (0.0, 0.3), (0.0, 0.68), (-0.08, 0.68), (-0.2, 0.6)]), fill=RAY[1])
    d.polygon(P(MAW), fill=K)
    if s > 40:
        for fang in FANGS:
            d.polygon(P(fang), fill=WH)
    d.polygon(P(SKULL), fill=RAY[1], outline=RAY[2])
    # rechterhelft in de schaduw (licht van de ring linksboven), een lichte rand over het midden
    d.polygon(P([(0.02, -0.46), (0.2, -0.46), (0.5, -0.32), (0.44, -0.06), (0.24, 0.16), (0.16, 0.24), (0.02, 0.24)]),
              fill=RAY[0])
    d.line(P([(0.0, -0.44), (0.0, 0.2)]), fill=RAY[2], width=lw)
    d.line(P(LIP), fill=gold, width=lw)
    d.line(P(mirror(LIP)), fill=gold, width=lw)
    for eye, pupil in ((EYE, PUPIL), (mirror(EYE), mirror(PUPIL))):
        if s > 24:
            d.polygon(P([(x * 1.12 - 0.01 * (1 if x < 0 else -1), y * 1.08) for x, y in eye]), fill=GOLD[0])
        d.polygon(P(eye), fill=GOLD[2] if glow > 0.3 else GOLD[1])
        if s > 60:
            d.polygon(P(pupil), fill=K)
    return np.array(pil)


def burst_frame(base, t):
    u = (t - T_BURST) / float(T_FILL - T_BURST)
    s = 6 * math.exp(math.log(420 / 6.0) * u ** 1.25)         # kopbreedte 6 -> 420 px
    cx = RC[0]
    cy = RC[1] + (74 - RC[1]) * min(1.0, u * 1.3)
    img = base.copy()
    # de ring (al uiteenvallend) achter Rayquaza
    if u < 0.6:
        img = draw_arc(img, t * 0.9, 2 * math.pi, 12 * (1 - u / 0.6) + 1, front_only=None)
    rng = np.random.RandomState(t)
    sh = (rng.randint(-2, 3), rng.randint(-2, 3)) if u > 0.3 else (0, 0)
    glow = 0.5 + 0.5 * math.sin(t * 0.8)
    img = draw_rayquaza(img, cx, cy, s, glow, sh)
    return img


# ------------------------------------------------------------------ film
def build(preview=None):
    f = film.Film('rayquaza')
    f.ref = palset(f)
    base = background()
    dim_bg = base
    for t in range(T_IN):
        f.add(None, palset(f, fade=0))
    for t in range(T_IN, T_STREAK):
        f.add(base, palset(f, fade=(t - T_IN + 1) / float(T_STREAK - T_IN)))
    cur = None
    for t in range(T_STREAK, T_RING):
        if (t - T_STREAK) % 2 == 0:
            cur = streak_frame(base, t)
        u = (t - T_STREAK) / float(T_RING - T_STREAK)
        f.add(cur, palset(f, dim=0.4 * u, glow=0.5 * u))
    for t in range(T_RING, T_BURST):
        if (t - T_RING) % 2 == 0:
            cur = ring_frame(base, t)
        u = (t - T_RING) / float(T_BURST - T_RING)
        f.add(cur, palset(f, dim=0.4 + 0.3 * u, glow=0.5 + 0.5 * math.sin(t * 0.5) ** 2,
                          green=0.35 * max(0, (t - T_BURST + 4) / 4.0)))
    for t in range(T_BURST, T_FILL):
        if (t - T_BURST) % 2 == 0:
            cur = burst_frame(base, t)
        f.add(cur, palset(f, dim=0.7, glow=0.6 + 0.4 * math.sin(t * 0.8) ** 2,
                          green=0.3 * max(0.0, 1 - (t - T_BURST) / 6.0)))
    last = cur
    for t in range(T_FILL, T_END):
        k = (t - T_FILL + 1) / float(T_END - T_FILL)
        f.add(last, palset(f, dim=0.7, glow=1.0, green=min(1.0, k * 1.6) * 0.6, white=max(0.0, k * 1.4 - 0.4)))
    f.encode(preview)
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    f = build(d)
    if d:
        fr = f.preview_frames
        film.sheet(fr, [18, 40, 60, 80, 96, 110, 126, 136, 146, 154, 162, 174], os.path.join(d, 'rayquaza_keys.png'))
