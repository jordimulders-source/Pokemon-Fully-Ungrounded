#!/usr/bin/env python3
"""Project Grounded: B_TRANSITION_KYOGRE_MURAL en B_TRANSITION_GROUDON_MURAL (Marine Cave / Terra Cave).

Een oude stenen muurschildering in de grot van hun strijd, in de stijl van de Hoenn-ruïnes: Groudon (land, bergen) en
Kyogre (zee, golven) uitgehakt in zandsteen, met een braillerand ("DONT WAKE THEM"). Fakkellicht flikkert. Dan lopen er
barsten door de schildering, vanuit de borst van degene die je komt wekken; door de barsten stroomt water (Kyogre) of
lava (Groudon) tot het beeld vol is. In de vloeistof gaan de gloeiende markeringen van zijn Primal-vorm aan
(silhouet uit de echte Primal-sprite), witte flits, gevecht.

De beelden in de muur zijn de echte front-sprites (1,5x via Scale3x), omgezet naar reliëf; de markeringen komen uit de
Primal-front-sprites (2x via Scale2x). Vloeistof als tile-periodieke textuur (ontdubbelt goed).
Gebruik: python3 tools/grounded/primal_mural_transition.py [voorbeeldmap]
"""
import math, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
import gbagfx_render as gr
from film import W, H
from guest_trainer_pics import scale3x
from wally_transition import scale2x

# tijden (gameframes); zie ook battle_transition.c (geluiden)
T_IN = 8          # de muur komt uit het donker
T_CRACK = 40      # eerste barst
T_LEAK = 78       # het eerste straaltje
T_POOL = 92       # de vloeistof begint te stijgen
T_FULL = 168      # het beeld is vol
T_MARK = 176      # de markeringen gaan aan
T_FLASH = 222     # witte flits
T_END = 232
STEP = 3          # gameframes per beeld (20 beelden per seconde)

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
YS, XS = np.mgrid[0:H, 0:W]
BY = BAYER[YS % 4, XS % 4]

# zandsteen in fakkellicht (0 = diepste groef ... 5 = hoogste licht)
STONE = [(26, 18, 14), (56, 40, 30), (92, 68, 48), (128, 98, 68), (166, 132, 92), (206, 172, 124)]
WATER = [(6, 18, 56), (14, 40, 104), (28, 80, 164), (64, 136, 216), (150, 214, 248), (236, 250, 255)]
LAVA = [(64, 10, 6), (140, 26, 8), (210, 72, 12), (248, 150, 32), (255, 220, 110), (255, 250, 210)]


def mix(a, b, k):
    return tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))


def sprite(path, frame=0, flip=False, pal=None):
    im = gr.sprite(path, pal, frame)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im


def x15(im):
    big = scale3x(im)
    return big.resize((big.width // 2, big.height // 2), Image.NEAREST)


def trim(im):
    bb = im.getbbox()
    return im.crop(bb)


# ------------------------------------------------------------------ de muur (niveaukaart 0..5)
def wall_levels():
    """Zandsteenblokken (32x16, halfsteens verband) met voegen: tile-periodiek (32x32)."""
    lv = np.full((H, W), 3, np.int8)
    for y in range(H):
        row = y // 16
        off = 16 if row % 2 else 0
        for x in range(W):
            bx = (x + off) % 32
            by = y % 16
            if by == 0 or bx == 0:
                lv[y, x] = 1
            elif by == 1 or bx == 1:
                lv[y, x] = 4
            elif by == 15 or bx == 31:
                lv[y, x] = 2
            elif ((bx * 7 + by * 13) % 23) == 0:
                lv[y, x] = 2
    return lv


PX0, PY0, PX1, PY1 = 12, 12, 228, 148     # paneel (verzonken vlak)


def panel(lv):
    lv[PY0:PY1, PX0:PX1] = 3
    # 16x16-periodieke spikkels op het vlak
    m = (((XS % 8) * 5 + (YS % 8) * 3) % 13 == 0) & (YS >= PY0) & (YS < PY1) & (XS >= PX0) & (XS < PX1)
    lv[m] = 2
    # rand: buiten licht, binnen schaduw (verzonken)
    lv[PY0 - 2:PY0, PX0 - 2:PX1 + 2] = 5
    lv[PY0 - 2:PY1 + 2, PX0 - 2:PX0] = 5
    lv[PY1:PY1 + 2, PX0 - 2:PX1 + 2] = 1
    lv[PY0 - 2:PY1 + 2, PX1:PX1 + 2] = 1
    lv[PY0:PY0 + 2, PX0:PX1] = 1
    lv[PY0:PY1, PX0:PX0 + 2] = 1
    lv[PY1 - 1, PX0:PX1] = 4
    lv[PY0:PY1, PX1 - 1] = 4


def carve(lv, spr, x0, y0):
    """Zet een sprite (RGBA) om naar reliëf: helderheid -> 2..4, donkere lijnen -> groef (1), rand linksboven licht (5),
    rechtsonder schaduw (0) met een slagschaduw op het vlak."""
    a = np.array(spr)
    op = a[..., 3] > 0
    lum = a[..., :3].astype(np.float64) @ np.array([0.3, 0.59, 0.11])
    h, w = op.shape
    lvl = np.where(lum < 56, 1, np.where(lum < 120, 2, np.where(lum < 185, 3, 4)))
    pad = np.zeros((h + 2, w + 2), bool)
    pad[1:-1, 1:-1] = op
    ul = pad[:-2, :-2] & pad[:-2, 1:-1] & pad[1:-1, :-2]
    dr = pad[2:, 2:] & pad[2:, 1:-1] & pad[1:-1, 2:]
    lvl = np.where(op & ~ul, 5, lvl)
    lvl = np.where(op & ~dr, 0, lvl)
    for yy in range(h + 1):
        for xx in range(w + 1):
            X, Y = x0 + xx, y0 + yy
            if not (0 <= X < W and 0 <= Y < H):
                continue
            inside = yy < h and xx < w and op[yy, xx]
            if inside:
                lv[Y, X] = lvl[yy, xx]
            elif yy > 0 and xx > 0 and op[yy - 1, xx - 1]:
                lv[Y, X] = 1      # slagschaduw


def groove(lv, pts, hi=True):
    """Uitgehakte lijn: groef (0) met een lichte rand eronder."""
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        n = int(max(abs(xb - xa), abs(yb - ya))) + 1
        for i in range(n + 1):
            x = int(round(xa + (xb - xa) * i / n))
            y = int(round(ya + (yb - ya) * i / n))
            if 0 <= x < W and 0 <= y < H:
                lv[y, x] = 1
                if hi and y + 1 < H and lv[y + 1, x] != 1:
                    lv[y + 1, x] = 5


BRAILLE = {'a': '1', 'b': '12', 'c': '14', 'd': '145', 'e': '15', 'f': '124', 'g': '1245', 'h': '125', 'i': '24',
           'j': '245', 'k': '13', 'l': '123', 'm': '134', 'n': '1345', 'o': '135', 'p': '1234', 'q': '12345',
           'r': '1235', 's': '234', 't': '2345', 'u': '136', 'v': '1236', 'w': '2456', 'x': '1346', 'y': '13456',
           'z': '1356'}


def braille(lv, x, y, text):
    """Hoenn-braille: per letter een cel van 2x3 bolletjes (2x2 px, licht linksboven, schaduw rechtsonder)."""
    for ch in text:
        if ch != ' ':
            for d in BRAILLE[ch]:
                k = int(d) - 1
                cx = x + (k // 3) * 4
                cy = y + (k % 3) * 4
                lv[cy, cx] = 5
                lv[cy, cx + 1] = 4
                lv[cy + 1, cx] = 4
                lv[cy + 1, cx + 1] = 1
        x += 10


def mural():
    lv = wall_levels()
    panel(lv)
    # Groudon (links, gespiegeld zodat hij naar rechts kijkt) en Kyogre (rechts)
    gro = trim(x15(sprite('graphics/pokemon/groudon/anim_front.png', 0, flip=True)))
    kyo = trim(x15(sprite('graphics/pokemon/kyogre/anim_front.png', 0)))
    gx, gy = 22, PY1 - 12 - gro.height
    kx, ky = PX1 - 12 - kyo.width, 52
    # land: bergen onder/achter Groudon
    pts = [(PX0 + 4, 124)]
    for i, xx in enumerate(range(PX0 + 12, 118, 12)):
        pts.append((xx, 112 if i % 2 == 0 else 126))
    groove(lv, pts)
    groove(lv, [(PX0 + 4, 134), (118, 134)])
    # zee: golven onder Kyogre
    for row, yy in enumerate((118, 128, 138)):
        ph = row * 6
        pts = [(xx, yy + 3 * math.sin((xx + ph) / 5.0)) for xx in range(122, PX1 - 4, 2)]
        groove(lv, pts)
    carve(lv, gro, gx, gy)
    carve(lv, kyo, kx, ky)
    # braille (bovenrand van het paneel) en een midden-scheiding
    braille(lv, 50, PY0 + 6, 'dont wake them')
    groove(lv, [(120, 44), (120, 60)], hi=False)
    centers = {'groudon': (gx + gro.width * 0.45, gy + gro.height * 0.45),
               'kyogre': (kx + kyo.width * 0.42, ky + kyo.height * 0.5)}
    return lv, centers


# ------------------------------------------------------------------ barsten
def cracks(origin, seed):
    """Vertakkende barsten vanuit origin: lijst (x, y, geboortetijd, dikte)."""
    rng = np.random.RandomState(seed)
    out = []
    todo = []
    for k in range(6):
        a = k * math.pi / 3 + rng.uniform(-0.4, 0.4)
        todo.append((origin[0], origin[1], a, T_CRACK + k * 2, 2, 120 + rng.randint(80)))
    while todo:
        x, y, a, t, th, n = todo.pop()
        a0 = a
        for i in range(n):
            a += rng.uniform(-0.5, 0.5)
            a += (a0 - a) * 0.25
            x += math.cos(a) * 0.8
            y += math.sin(a) * 0.8
            t += 0.21
            if not (0 <= x < W and 0 <= y < H):
                break
            out.append((x, y, t, th))
            if rng.rand() < 0.018 and len(out) < 4800:
                todo.append((x, y, a + rng.choice([-1, 1]) * rng.uniform(0.6, 1.1), t, 1, int(n * 0.5)))
    # aaneengesloten: tussenpunten zodat er geen gaten in de lijn zitten
    return out


# ------------------------------------------------------------------ vloeistof
def liquid_tex(kind):
    """Periodieke vloeistoftextuur (64x64): een kaustieknet (water) of korstplaten met gloeiende naden (lava), met
    niveaus 0..5. Verschuift hij over het scherm, dan blijft het beeld periodiek: max. 64 verschillende tiles."""
    rng = np.random.RandomState(4 if kind == 'kyogre' else 9)
    N = 64
    yy, xx = np.mgrid[0:N, 0:N]
    pts = rng.rand(12 if kind == 'kyogre' else 6, 2) * N
    d1 = np.full((N, N), 1e9)
    d2 = np.full((N, N), 1e9)
    for px, py in pts:
        for ox in (-N, 0, N):
            for oy in (-N, 0, N):
                d = np.hypot(xx - px - ox, yy - py - oy)
                nd1 = np.minimum(d1, d)
                d2 = np.where(d < d1, d1, np.minimum(d2, d))
                d1 = nd1
    edge = d2 - d1                      # klein = naad tussen twee cellen
    if kind == 'kyogre':
        # dunne lichtlijnen op middenblauw, met een Bayer-overgang
        by = BAYER[yy % 4, xx % 4]
        return np.where(edge < 0.9, 3, np.where((edge < 2.0) & (by < 0.5), 3, 2))
    # lava: donkere korstplaten (midden het donkerst), gloeiende naden
    by = BAYER[yy % 4, xx % 4]
    return np.where(edge < 0.9, 5, np.where(edge < 2.0, 4, np.where(edge < 3.4 + by * 2, 3,
                    np.where(edge < 7 + by * 3, 2, np.where(d1 > 9 + by * 4, 0, 1)))))


TEX = {k: liquid_tex(k) for k in ('kyogre', 'groudon')}


def tex_at(kind, t):
    """De textuur over het hele scherm, verschoven met de tijd (water: stroomt; lava: kruipt)."""
    T = TEX[kind]
    # in stapjes (water 4 px per 9 frames, lava 2 px per 12 frames): weinig verschillende standen = weinig tiles laden
    sx = (t // 9) * 4 if kind == 'kyogre' else (t // 12) * 2
    return T[YS % 64, (XS + sx) % 64]


def surface(t, level):
    x = np.arange(W)
    return level + 2.0 * np.sin(x / 9.0 + t / 4.0) + 1.5 * np.sin(x / 23.0 - t / 7.0)


def draw_liquid(img, kind, t, level, streams):
    """Plas tot 'level' (y van het oppervlak) en de straaltjes [(x, y0, t0, w)]."""
    LQ = WATER if kind == 'kyogre' else LAVA
    for (x0, y0, t0, w) in streams:
        if t < t0:
            continue
        dt = t - t0
        yh = y0 + 0.06 * dt * dt + 1.5 * dt
        x0i = int(x0)
        for y in range(int(y0), int(min(yh, H))):
            wob = int(round(math.sin(y / 6.0 + t / 3.0) * 0.8 * (y - y0) / 40.0))
            ww = w + (1 if y - y0 > 30 else 0)
            for dx in range(-ww // 2, ww - ww // 2):
                X = x0i + dx + wob
                if 0 <= X < W:
                    img[y, X] = LQ[4] if dx == -ww // 2 else LQ[3]
        # spat bij het oppervlak
        if yh >= level - 2 and level < H:
            for k in range(-3, 4):
                X = x0i + k * 2
                Y = int(level - 3 - (3 - abs(k)) * (1 + (t % 4 == 0)))
                if 0 <= X < W and 0 <= Y < H:
                    img[Y, X] = LQ[5]
    if level >= H:
        return
    surf = surface(t, level)
    d = YS - surf[None, :]
    lvl = tex_at(kind, t).astype(np.int16)
    if kind == 'kyogre':
        # dieper = donkerder (het net dooft uit), vlak onder het oppervlak lichter
        k = BY * 8
        lvl = np.where(d > 24 + k, lvl - 1, lvl)
        lvl = np.clip(lvl, 0, 4)
    else:
        # lava: vlak onder het oppervlak alles gloeiend
        lvl = np.where(d <= 8, np.maximum(lvl, 3), lvl)
    lvl = np.where(d <= 4, np.maximum(lvl, 3), lvl)
    lvl = np.where(d <= 1.5, 4, lvl)
    lvl = np.where(d <= 0.6, 5, lvl)
    col = np.array(LQ, np.uint8)[lvl]
    m = d >= 0
    img[m] = col[m]


# ------------------------------------------------------------------ Primal-markeringen
def primal(kind):
    """Primal-front-sprite (2x): masker van het silhouet en van de markeringen (de lichte lijnkleuren)."""
    path = 'graphics/pokemon/%s/primal/front.png' % kind
    im = Image.open(os.path.join(film.ROOT, path))
    a = np.array(im)
    big = scale2x(sprite(path))
    b = np.array(big)
    # markeringen: Kyogre index 5 (lichtgeel) en 9 (lichtblauw), Groudon 5 (lichtgeel) en 6 (oranje)
    idx = Image.fromarray(a).resize((128, 128), Image.NEAREST)
    ia = np.array(idx)
    marks = np.isin(ia, [5, 9] if kind == 'kyogre' else [5, 7, 8])
    sil = b[..., 3] > 0
    marks &= sil
    # ogen: het lichtste stukje kop (Kyogre: 2 = wit, Groudon: 13 = wit)
    eyes = np.isin(ia, [2] if kind == 'kyogre' else [13]) & sil
    lit = (b[..., :3].astype(np.float64) @ np.array([0.3, 0.59, 0.11])) > 110   # lichte delen van het lijf
    return sil, marks, eyes, lit


def build(kind, preview=None):
    other = 'groudon' if kind == 'kyogre' else 'kyogre'
    f = film.Film('mural_' + kind)
    lv, centers = mural()
    LQ = WATER if kind == 'kyogre' else LAVA
    stone_rgb = np.array(STONE, np.uint8)[lv]
    crk = cracks(centers[kind], 7 if kind == 'kyogre' else 11)
    glow = LQ[4]
    # straaltjes: vanaf barstpunten verspreid over de breedte
    rng = np.random.RandomState(3)
    streams = []
    cands = [c for c in crk if c[2] < T_LEAK + 30 and c[1] < 110]
    for k, xs in enumerate(range(18, 230, 26)):
        near = [c for c in cands if abs(c[0] - xs) < 10]
        if near:
            c = near[rng.randint(len(near))]
            streams.append((c[0], c[1], max(T_LEAK + (k * 5) % 22, int(c[2]) + 8), 2 + (k % 2)))

    def frame(t):
        img = stone_rgb.copy()
        for (x, y, tb, th) in crk:
            if tb > t:
                continue
            X, Y = int(x), int(y)
            lit = t > tb + 14
            c = glow if lit else STONE[0]
            img[Y, X] = c
            if th == 2 and X + 1 < W:
                img[Y, X + 1] = LQ[3] if lit else STONE[0]
            if Y + 1 < H and lv[min(Y + 1, H - 1), X] > 1 and not lit:
                img[Y + 1, X] = STONE[5]
        if t >= T_POOL:
            u = min(1.0, (t - T_POOL) / float(T_FULL - T_POOL))
            level = H + 6 - (H + 14) * (u ** 1.35)
        else:
            level = H + 10
        draw_liquid(img, kind, t, level, streams)
        return img

    def final(t, on):
        """Vol beeld vloeistof met het Primal-silhouet; on = 0..1 hoe ver de markeringen aan zijn."""
        img = np.zeros((H, W, 3), np.uint8)
        draw_liquid(img, kind, t, -12, [])
        sil, marks, eyes, lit = PRIMAL
        x0, y0 = 56, 18
        reveal = min(1.0, (t - T_FULL + 3) / 12.0)
        sub = BY[y0:y0 + 128, x0:x0 + 128]
        dark = LQ[0]
        m = sil & (sub < reveal)
        reg = img[y0:y0 + 128, x0:x0 + 128]
        reg[m] = dark
        reg[m & lit] = LQ[1]      # de vorm van het lijf blijft net zichtbaar
        # randlicht: de rand van het silhouet vangt het licht van boven
        rim = sil & ~np.roll(sil, 1, 0) | sil & ~np.roll(sil, 1, 1) | sil & ~np.roll(sil, -1, 1)
        reg[rim & (sub < reveal * 1.4)] = LQ[3] if kind == 'kyogre' else LQ[5]
        if on > 0:
            mm = marks & (sub < on)
            reg[mm] = LQ[5] if (t // 4) % 2 == 0 else LQ[4]
            # gloed rond de markeringen
            g = np.zeros_like(mm)
            g[1:] |= mm[:-1]; g[:-1] |= mm[1:]; g[:, 1:] |= mm[:, :-1]; g[:, :-1] |= mm[:, 1:]
            reg[g & ~mm & sil] = LQ[3]
        if on >= 1.0:
            reg[eyes] = LQ[5]
        return img

    global PRIMAL
    PRIMAL = primal(kind)

    # beelden: elke 2 frames een nieuw beeld (fakkel en vloeistof); paletten automatisch per deel
    seg_a = {t: frame(t) for t in range(T_IN, T_FULL, STEP)}
    seg_b = {t: final(t, min(1.0, max(0.0, (t - T_MARK + 3) / 15.0))) for t in range(T_FULL, T_END, STEP)}
    fixed = [STONE[0], STONE[3], LQ[3]]
    pa = film.auto_palettes([seg_a[t] for t in list(seg_a)[::5]] + [seg_a[max(seg_a)]], fixed)
    pb = film.auto_palettes([seg_b[t] for t in list(seg_b)[::4]], [LQ[0], LQ[2], LQ[5]])
    pa = [p[:15] for p in pa]
    pb = [p[:15] for p in pb]

    def tinted(p, fade=1.0, white=0.0, torch=0.0):
        out = []
        for pal in p:
            q = []
            for c in pal:
                c2 = mix((0, 0, 0), c, fade * (1.0 - torch))
                q.append(mix(c2, (255, 255, 255), white))
            out.append(q)
        return f.palset(*out)

    qa = tinted(pa)
    qb = tinted(pb)
    blank = f.palset([(0, 0, 0)], [(0, 0, 0)], [(0, 0, 0)])
    for t in range(T_IN):
        f.add(None, blank)
    torch = [0.0, 0.06, 0.02, 0.1, 0.04, 0.0, 0.08, 0.03]
    for t in range(T_IN, T_FULL):
        img = seg_a[t - (t - T_IN) % STEP]
        fade = min(1.0, (t - T_IN + 1) / 16.0)
        # fakkellicht: flikkert tot de vloeistof het licht overneemt
        tr = torch[(t // 5) % 8] if t < T_POOL + 30 else 0.0
        f.add(img, tinted(pa, fade, torch=tr), q=qa)
    for t in range(T_FULL, T_END):
        img = seg_b[t - (t - T_FULL) % STEP]
        wh = 0.0
        if t >= T_FLASH:
            wh = min(1.0, (t - T_FLASH + 1) / 8.0)
        elif T_MARK + 20 <= t < T_MARK + 24:
            wh = 0.25          # de ogen gaan open: korte lichtflits
        f.add(img, tinted(pb, white=wh), q=qb)
    f.encode(preview)
    print('%s: %d frames (%.1f s)' % (kind, len(f.frames), len(f.frames) / 60.0))
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    for kind in ('kyogre', 'groudon'):
        f = build(kind, d)
        if d:
            film.sheet(f.preview_frames, [24, 44, 60, 76, 90, 104, 120, 140, 160, 180, 200, 226],
                       os.path.join(d, 'mural_%s_keys.png' % kind))
