#!/usr/bin/env python3
"""Project Grounded: B_TRANSITION_RAYQUAZA_PILLAR (Rayquaza op de Sky Pillar, ook de shiny/Delta Episode).

Je kijkt omhoog langs de Sky Pillar, door de wolken. Een groene streep cirkelt om de top, steeds sneller en langer, tot
hij een gesloten, gloeiende ring is: groene flits. De camera kantelt weg van de toren, omhoog naar het wolkendek, en
dan volgt de echte Emerald-cutscene (src/rayquaza_scene.c, graphics/rayquaza_scene/): een lichtbundel valt door het
gat in de wolken en Rayquaza duikt erdoor naar beneden ('descends'), dan stormt hij tussen de snelheidsstrepen op de
camera af ('charges'): trillen, terugdeinzen, naar voren schieten tot hij het beeld vult. Groen, wit, gevecht.

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
T_RING = 100       # de streep is een gesloten ring
T_FLASH = 116      # groene flits; de camera kantelt omhoog
T_PAN = 142        # het wolkendek (scene 3) staat in beeld
T_S3 = 194         # Rayquaza is door de wolken gedoken: snede naar de aanval (scene 4)
T_S4 = 244         # Rayquaza vult het beeld
T_END = 252

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
    u = (t - T_RING) / float(T_FLASH - T_RING)
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


# ------------------------------------------------------------------ de vanilla-cutscene (src/rayquaza_scene.c)
# Na de flits kijkt de camera omhoog, weg van de toren, naar het wolkendek ('Rayquaza descends', scene 3): een lichtbundel
# valt door het gat in de wolken en Rayquaza duikt erdoor naar beneden. Dan de aanval op de camera ('Rayquaza charges',
# scene 4): de grote Rayquaza tussen de snelheidsstrepen, hij trilt, deinst terug en schiet naar voren tot hij het beeld
# vult. Alle art komt uit graphics/rayquaza_scene/ (tiles + tilemaps + paletten), samengesteld zoals de GBA dat doet.
RS = os.path.join(film.ROOT, 'graphics/rayquaza_scene')
BAR = 24                                   # zwarte balken boven/onder (scene 3 in de tilemap, scene 4 met WIN0)


def _jasc(p):
    v = open(p).read().split()
    n = int(v[2])
    a = list(map(int, v[3:3 + 3 * n]))
    return [tuple(a[i * 3:i * 3 + 3]) for i in range(n)]


def _pngpal(p, n=16):
    v = Image.open(p).getpalette()[:3 * n]
    return [tuple(v[i * 3:i * 3 + 3]) for i in range(n)]


def layer(binf, pngf, pal):
    """Tilemap (32x32, 4bpp) -> (rgb 256x256x3, ondoorzichtig 256x256): index 0 van elk palet is doorzichtig."""
    t = np.array(Image.open(os.path.join(RS, pngf)))
    raw = open(os.path.join(RS, binf), 'rb').read()
    m = np.frombuffer(raw, '<u2')
    tw = t.shape[1] // 8
    P = np.array(list(pal) + [(0, 0, 0)] * (64 - len(pal)), np.uint8)
    rgb = np.zeros((256, 256, 3), np.uint8)
    op = np.zeros((256, 256), bool)
    for i, v in enumerate(m):
        r, c = divmod(i, 32)
        ty, tx = divmod(int(v) & 0x3FF, tw)
        if ty * 8 >= t.shape[0]:
            continue
        b = t[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
        if v & 0x400:
            b = b[:, ::-1]
        if v & 0x800:
            b = b[::-1]
        rgb[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = P[b.astype(int) + (int(v) >> 12) * 16]
        op[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = b != 0
    return rgb, op


def sprite_sheet(pngf, pal):
    a = np.array(Image.open(os.path.join(RS, pngf)))
    return np.array(pal, np.uint8)[a], a != 0


def blit(img, src, op, x0, y0):
    """Plakt src (met ondoorzichtig-masker) met linksboven op (x0, y0), afgekapt op het scherm."""
    h, w = op.shape
    x0, y0 = int(round(x0)), int(round(y0))
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    w2, h2 = min(w - sx0, W - dx0), min(h - sy0, H - dy0)
    if w2 <= 0 or h2 <= 0:
        return
    m = op[sy0:sy0 + h2, sx0:sx0 + w2]
    img[dy0:dy0 + h2, dx0:dx0 + w2][m] = src[sy0:sy0 + h2, sx0:sx0 + w2][m]


def scroll(rgb, op, sx, sy):
    """Een BG van 256x256 zoals de GBA hem toont met scroll (sx, sy): de 240x160 linksboven, met wrap."""
    ys = (np.arange(H) + int(sy)) % 256
    xs = (np.arange(W) + int(sx)) % 256
    return rgb[ys][:, xs], op[ys][:, xs]


def bars(img, b):
    b = int(round(b))
    if b > 0:
        img[:b] = 0
        img[H - b:] = 0
    return img


# --- scene 3: Rayquaza daalt door het wolkendek
P3 = _jasc(os.path.join(RS, 'scene_3/bg.pal'))
RAYPAL = _pngpal(os.path.join(RS, 'scene_2/rayquaza.png'))       # 'takes flight'-palet, ook voor de sprite in scene 3
S3_BG, S3_BGOP = layer('scene_3/bg.bin', 'scene_3/bg.png', P3)
S3_LIGHT, S3_LIGHTOP = layer('scene_3/light.bin', 'scene_3/light.png', P3)
S3_RAY, S3_RAYOP = sprite_sheet('scene_3/rayquaza.png', RAYPAL)            # 64x128: twee beelden van 64x64
S3_TAIL, S3_TAILOP = sprite_sheet('scene_3/rayquaza_tail.png', RAYPAL)     # 16x128: beelden van 16x32
WHITE = (255, 255, 255)                                                    # de achtergrondkleur (BG-palet 0 = wit)


def s3_frame(t, reveal, rx, ry, anim):
    """Scene 3 zoals rayquaza_scene.c hem samenstelt: BG3 (wolken), de sprite (prioriteit 3), BG1 (bovenste 8 rijen
    wolken, vóór de sprite: hij komt door het gat), BG0 = de lichtbundel, alfa 8/16 over 13/16, tot regel 24+reveal."""
    img = np.empty((H, W, 3), np.uint8)
    img[:] = WHITE
    bg, op = S3_BG[:H, :W], S3_BGOP[:H, :W]
    img[op] = bg[op]
    front = op.copy()
    front[64:] = False                                  # BG1 = alleen de rijen 0..7
    # de lichtbundel
    lo, lop = S3_LIGHT[:H, :W], S3_LIGHTOP[:H, :W].copy()
    lop[:24] = False
    lop[24 + int(reveal) + 1:] = False
    below_bd = lop & ~op                                 # boven de achtergrondkleur: geen tweede doel, dus niet gemengd
    mixm = lop & ~below_bd
    a = lo.astype(np.int32) * 8 // 16 + img.astype(np.int32) * 13 // 16
    img[mixm] = np.minimum(a, 255).astype(np.uint8)[mixm]
    img[below_bd] = lo[below_bd]
    # Rayquaza zelf: in de cutscene mengt de bundel ook over hem heen (dan is hij een bleek spookje); hier vóór het licht,
    # zodat je hem echt ziet, maar nog wel achter het bovenste wolkendek (BG1)
    f = anim & 1
    blit(img, S3_RAY[f * 64:f * 64 + 64], S3_RAYOP[f * 64:f * 64 + 64], rx - 32, ry - 32)
    blit(img, S3_TAIL[f * 32:f * 32 + 32], S3_TAILOP[f * 32:f * 32 + 32], rx + 24 - 8, ry - 48 - 16)
    img[front] = bg[front]
    return img


# --- scene 4: Rayquaza valt aan
P4 = _jasc(os.path.join(RS, 'scene_4/bg.pal'))
S4_BG, S4_BGOP = layer('scene_4/bg.bin', 'scene_4/bg.png', P4)
S4_RAY, S4_RAYOP = layer('scene_4/rayquaza.bin', 'scene_4/rayquaza.png', P4)
S4_STREAK, S4_STREAKOP = layer('scene_4/streaks.bin', 'scene_4/streaks.png', P4)
S4_ORB, S4_ORBOP = layer('scene_4/orbs.bin', 'scene_4/streaks.png', P4)
HEAD = (88, 92)            # ongeveer het midden van de kop in de Rayquaza-tilemap (laagcoördinaten)


def s4_frame(t, rdx, rdy, zoom=1.0, hx=None, hy=None):
    """Scene 4: BG3 verloop, BG2 strepen (8 px/frame), BG1 Rayquaza (verschoven met rdx/rdy, of ingezoomd rond zijn kop
    met de kop op (hx, hy); zonder wrap), BG0 gele lichtjes (4 px/frame), balken via WIN0 (achtergrond zwart)."""
    if hx is None:
        hx, hy = HEAD[0] + rdx, HEAD[1] + rdy
    img = np.zeros((H, W, 3), np.uint8)
    bg, op = scroll(S4_BG, S4_BGOP, 0, 0)
    img[op] = bg[op]
    s, o = scroll(S4_STREAK, S4_STREAKOP, -8 * t, 8 * t)
    img[o] = s[o]
    ys = np.floor((np.arange(H) - hy) / zoom + HEAD[1]).astype(int)
    xs = np.floor((np.arange(W) - hx) / zoom + HEAD[0]).astype(int)
    ok = ((ys >= 0) & (ys < 232))[:, None] & ((xs >= 0) & (xs < 256))[None, :]   # rij 29+ = losse staartpunt (wrap)
    yc, xc = np.clip(ys, 0, 255), np.clip(xs, 0, 255)
    r, o = S4_RAY[yc][:, xc], S4_RAYOP[yc][:, xc] & ok
    img[o] = r[o]
    s, o = scroll(S4_ORB, S4_ORBOP, -4 * t, 4 * t)
    img[o] = s[o]
    return bars(img, BAR)


def edge_palette(imgs, pa, pb, n=15):
    """Derde palet: k-means op de pixels van tiles die met palet A en B allebei slecht te tekenen zijn."""
    wts = np.array([3.0, 6.0, 2.0])
    A = np.array([film.gba(c) for c in pa], np.float64)
    B = np.array([film.gba(c) for c in pb], np.float64)
    px = []
    for img in imgs:
        t = img.reshape(20, 8, 30, 8, 3).transpose(0, 2, 1, 3, 4).reshape(600, 64, 3).astype(np.float64)
        ea = (((t[:, :, None] - A[None, None]) ** 2) * wts).sum(3).min(2).sum(1)
        eb = (((t[:, :, None] - B[None, None]) ** 2) * wts).sum(3).min(2).sum(1)
        bad = np.minimum(ea, eb) > 64 * 60
        px.append(t[bad].reshape(-1, 3))
    px = np.concatenate(px) if px else np.zeros((0, 3))
    if len(px) < n:
        return list(pa[:n])
    keys, inv = np.unique(px.astype(np.int64) @ np.array([1, 256, 65536]), return_inverse=True)
    cols = np.stack([keys % 256, (keys // 256) % 256, keys // 65536], 1).astype(np.float64)
    cw = np.bincount(inv)
    c = cols[np.argsort(-cw)[:n]].copy()
    rng = np.random.RandomState(3)
    for _ in range(16):
        d = (((cols[:, None] - c[None]) ** 2) * wts).sum(2)
        a = d.argmin(1)
        for j in range(len(c)):
            m = a == j
            if m.any():
                c[j] = np.average(cols[m], axis=0, weights=cw[m])
            else:
                c[j] = cols[rng.randint(len(cols))]
    return [tuple(int(v) for v in x) for x in c]


def tint(f, pals, fade=1.0, green=0.0, white=0.0):
    def tr(c):
        c = mix((0, 0, 0), c, fade)
        c = mix(c, (60, 255, 120), green)
        return mix(c, (255, 255, 255), white)
    return f.palset(*[[tr(c) for c in p] for p in pals])


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ film
def build(preview=None):
    f = film.Film('rayquaza')
    f.ref = palset(f)
    base = background()
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
    for t in range(T_RING, T_FLASH):
        if (t - T_RING) % 2 == 0:
            cur = ring_frame(base, t)
        u = (t - T_RING) / float(T_FLASH - T_RING)
        f.add(cur, palset(f, dim=0.4 + 0.3 * u, glow=0.5 + 0.5 * math.sin(t * 0.5) ** 2,
                          green=0.85 * max(0, (t - T_FLASH + 6) / 6.0) ** 1.5))

    # --- de camera kantelt omhoog: de toren zakt weg, het wolkendek van scene 3 komt van boven in beeld
    s3_top = S3_BG[BAR:H - BAR, :W].copy()                     # de 112 rijen wolken en lucht zonder balken
    s3_top[~S3_BGOP[BAR:H - BAR, :W]] = WHITE                  # het gat in de wolken: de (witte) achtergrondkleur
    band = 64
    tall = np.zeros((s3_top.shape[0] + band + H, W, 3), np.uint8)
    tall[:s3_top.shape[0]] = s3_top
    grad = [tuple(int(v) for v in s3_top[-1, 0])] + SKY[::-1]       # van de lucht onder het wolkendek naar de nacht
    lv = (np.arange(band)[:, None] + 0.5) / band * (len(grad) - 1) + np.zeros((1, W))
    by = BAYER[np.arange(band)[:, None] % 4, np.arange(W)[None] % 4]
    li = np.clip(np.floor(lv + by), 0, len(grad) - 1).astype(int)
    tall[s3_top.shape[0]:s3_top.shape[0] + band] = np.array(grad, np.uint8)[li]
    tall[s3_top.shape[0] + band:] = base
    y_from = s3_top.shape[0] + band                           # toren in beeld
    y_to = -BAR                                               # het wolkendek met de balken van scene 3
    p3_world = [c for c in P3[2:16]] + [WHITE]           # wolkendek
    pan_pals = [p3_world, [K] + STONE + MOSS + SKY[:4] + CLOUD[:2], [K] + SKY + CLOUD]
    n_pan = T_PAN - T_FLASH
    for i in range(n_pan):
        if i % 2 == 0:
            u = ease((i + 2) / float(n_pan))
            y = int(round(y_from + (y_to - y_from) * u))
            img = np.zeros((H, W, 3), np.uint8)
            lo, hi = max(0, y), min(tall.shape[0], y + H)
            img[lo - y:hi - y] = tall[lo:hi]
            img = bars(img, BAR * u)
        q = tint(f, pan_pals)
        f.add(img, tint(f, pan_pals, green=0.85 * max(0.0, 1 - i / 10.0) ** 1.5), q=q)

    # --- scene 3: de lichtbundel en Rayquaza die erdoor naar beneden duikt
    n3 = T_S3 - T_PAN
    s3 = []
    for i in range(0, n3, 2):
        reveal = min(112, i * 5)
        u = max(0.0, (i - 6) / float(n3 - 6))
        # zoals in de cutscene schuin naar linksonder (dx:dy = 2:3) en steeds sneller, maar verder: tot midden in beeld
        k = u ** 1.6
        rx = 162 - 66 * k
        ry = 4 + 100 * k
        s3.append(s3_frame(i, reveal, rx, ry, (i // 8) & 1))
    ray15 = RAYPAL[1:16]
    p3_15 = [c for c in P3[2:16]] + [WHITE]
    p3_pals = [ray15, p3_15, edge_palette(s3, ray15, p3_15)]
    for i in range(n3):
        img = s3[i // 2]
        q = tint(f, p3_pals)
        f.add(img, q, q=q)

    # --- scene 4: de aanval
    n4 = T_S4 - T_S3
    T_BACK, T_LAUNCH = 16, 24                                 # trillen 0..16, terugdeinzen 16..26, dan naar voren
    rng = np.random.RandomState(7)
    s4 = []
    shx = shy = 0
    bx = by = 0.0
    ofs = 6
    for i in range(n4):
        if i < T_BACK:
            if i % 4 == 0:
                shx, shy = rng.randint(-4, 4), rng.randint(-4, 4)
            img = s4_frame(i, shx, shy) if i % 2 == 0 else s4[-1][0]
        elif i < T_LAUNCH:
            bx += ofs
            by -= ofs
            ofs = max(1, ofs - 1)
            img = s4_frame(i, bx, by) if i % 2 == 0 else s4[-1][0]
        else:
            u = (i - T_LAUNCH + 1) / float(n4 - T_LAUNCH)
            z = 1.0 + 1.9 * u ** 1.6
            # de kop schiet van zijn plek (teruggedeinsd) naar het midden en komt op de camera af
            hx0, hy0 = HEAD[0] + bx, HEAD[1] + by
            hx = hx0 + (122 - hx0) * ease(u * 1.3)
            hy = hy0 + (86 - hy0) * ease(u * 1.3)
            img = s4_frame(i, 0, 0, z, hx, hy) if i % 2 == 0 else s4[-1][0]
        s4.append((img, i))
    ray4 = P4[1:16]
    bg4 = P4[17:23] + [(0, 0, 0)] + [P4[33], P4[34], P4[35], P4[50], P4[51]]
    p4_pals = [ray4, bg4, edge_palette([x[0] for x in s4[::4]], ray4, bg4)]
    for img, i in s4:
        q = tint(f, p4_pals)
        f.add(img, q, q=q)
    last = s4[-1][0]
    for t in range(T_S4, T_END):
        k = (t - T_S4 + 1) / float(T_END - T_S4)
        q = tint(f, p4_pals)
        f.add(last, tint(f, p4_pals, green=min(1.0, k * 2) * 0.5, white=max(0.0, k * 1.5 - 0.5)), q=q)
    f.encode(preview)
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    f = build(d)
    if d:
        fr = f.preview_frames
        film.sheet(fr, [40, 80, 104, 116, 124, 132, 140, 150, 162, 174, 186, 196, 204, 214, 222, 232, 240, 248],
                   os.path.join(d, 'rayquaza_keys.png'), cols=3)
