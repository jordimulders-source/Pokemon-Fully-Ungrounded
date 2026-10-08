#!/usr/bin/env python3
"""Project Grounded: B_TRANSITION_WEATHER_SERVICE (Archie en Maxie, werkstraf in het Weather Institute).

Het prikbord in de pauzeruimte van het Weather Institute: het werkstrafrooster ("DISHES: MAXIE / MOPPING: ARCHIE",
"RULE 1: NO DROUGHTS. RULE 2: NO FLOODS."), plakbriefjes met passief-agressieve vragen, een rode en een blauwe punaise.
Er valt een druppel koffie op het rooster. De vlek loopt uit tot de vorm van Groudon, en kruipt dan verder tot Kyogre
(het silhouet van de echte front-sprites, met de donkere rand die koffievlekken hebben). Dan scheurt het rooster
doormidden: de linkerhelft vliegt in brand (Magma), de rechterhelft wordt doorweekt en zakt weg (Aqua). Eronder hangt
"VOLUNTEER OF THE MONTH" met Maxie en Archie samen erop ("(DISPUTED)"). Flits, gevecht.
Gebruik: python3 tools/grounded/service_transition.py [voorbeeldmap]
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
import gbagfx_render as gr
from film import W, H, text35, text35_width
from guest_trainer_pics import scale3x

T_IN = 8
T_DRIP = 22       # de druppel valt
T_SPLAT = 38      # plets
T_GROUDON = 70    # de vlek is Groudon
T_MORPH = 84      # de vlek kruipt verder
T_KYOGRE = 112    # de vlek is Kyogre
T_TEAR = 124      # het rooster scheurt
T_SPLIT = 140     # de helften gaan uit elkaar: brand en water
T_FLASH = 206
T_END = 216
STEP = 2

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
YS, XS = np.mgrid[0:H, 0:W]
BY = BAYER[YS % 4, XS % 4]

CORK = [(118, 78, 44), (146, 100, 58), (172, 124, 74), (96, 62, 34)]
FRAME = [(64, 40, 24), (100, 66, 38), (138, 96, 56)]
PAPER = [(240, 236, 224), (214, 208, 196)]
INK = (40, 40, 52)
COFFEE = [(176, 128, 82), (142, 96, 56), (96, 60, 32)]
FIRE = [(120, 20, 8), (216, 56, 16), (248, 140, 32), (255, 232, 120)]
SOAK = [(132, 156, 196), (84, 112, 168), (40, 64, 128)]
MAGMA_RED = (200, 40, 40)
AQUA_BLUE = (40, 96, 200)


def mix(a, b, k):
    return tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))


def x15(im):
    big = scale3x(im)
    return big.resize((big.width // 2, big.height // 2), Image.NEAREST)


def put_text(a, x, y, s, col=INK, font='small'):
    return gr.text(a, x, y, s, col, None, font)


def tiny(a, x, y, s, col=INK):
    def px(u, v):
        if 0 <= u < a.shape[1] and 0 <= v < a.shape[0]:
            a[v, u] = col
    return text35(px, x, y, s)


# ------------------------------------------------------------------ het prikbord
def board():
    a = np.zeros((H, W, 3), np.uint8)
    # kurk: 16x16-periodieke spikkels (ontdubbelt goed)
    a[:] = CORK[1]
    yy, xx = YS % 16, XS % 16
    a[((xx * 7 + yy * 5) % 11 == 0)] = CORK[2]
    a[((xx * 3 + yy * 13) % 17 == 0)] = CORK[0]
    a[((xx * 11 + yy * 3) % 29 == 0)] = CORK[3]
    # houten lijst
    a[:6] = FRAME[1]; a[-6:] = FRAME[1]; a[:, :6] = FRAME[1]; a[:, -6:] = FRAME[1]
    a[5] = FRAME[0]; a[-6] = FRAME[2]; a[:, 5] = FRAME[0]; a[:, -6] = FRAME[2]
    a[0] = FRAME[2]; a[:, 0] = FRAME[2]; a[-1] = FRAME[0]; a[:, -1] = FRAME[0]
    return a


def note(a, x0, y0, w, h, col, lines, pin):
    a[y0 + 2:y0 + h + 2, x0 + 2:x0 + w + 2] = mix(CORK[3], (0, 0, 0), 0.3)       # schaduw
    a[y0:y0 + h, x0:x0 + w] = col
    a[y0 + h - 1, x0:x0 + w] = mix(col, (0, 0, 0), 0.15)
    for i, l in enumerate(lines):
        tiny(a, x0 + 3, y0 + 8 + i * 7, l)
    pushpin(a, x0 + w // 2, y0 + 2, pin)


def pushpin(a, x, y, col):
    dark = mix(col, (0, 0, 0), 0.45)
    lite = mix(col, (255, 255, 255), 0.5)
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if dx * dx + dy * dy <= 5:
                a[y + dy, x + dx] = col
    a[y + 1:y + 3, x + 1:x + 3] = dark
    a[y - 1, x - 1] = lite
    a[y + 3, x + 2] = (40, 30, 30)


def poster():
    """VOLUNTEER OF THE MONTH (onder het rooster): Maxie en Archie samen, (DISPUTED)."""
    p = np.zeros((H, W, 4), np.uint8)
    x0, y0, x1, y1 = 28, 14, 170, 146
    p[y0:y1, x0:x1, :3] = (248, 232, 176)
    p[y0:y1, x0:x1, 3] = 255
    rgb = p[..., :3]
    rgb[y0:y0 + 3, x0:x1] = (216, 172, 64)
    rgb[y1 - 3:y1, x0:x1] = (216, 172, 64)
    s = 'VOLUNTEER OF THE MONTH'
    w = gr.text(np.zeros((16, 400, 3), np.uint8), 0, 0, s, INK, None, 'normal')
    put_text(rgb, 99 - w // 2, y0 + 4, s, INK, 'normal')
    for k, (path, col, nm) in enumerate((('magma_leader_maxie', MAGMA_RED, 'MAXIE'),
                                         ('aqua_leader_archie', AQUA_BLUE, 'ARCHIE'))):
        px = 32 + k * 70
        rgb[34:108, px - 2:px + 66] = (252, 252, 248)
        rgb[36:104, px:px + 64] = mix(col, (255, 255, 255), 0.55)
        spr = gr.sprite('graphics/trainers/front_pics/%s.png' % path)
        if k == 0:
            spr = spr.transpose(Image.FLIP_LEFT_RIGHT)      # ze kijken elkaar aan
        im = Image.fromarray(rgb)
        im.paste(spr.crop((0, 0, 64, 68)), (px, 38), spr.crop((0, 0, 64, 68)))
        rgb[:] = np.array(im)
        rgb[104:108, px - 2:px + 66] = (252, 252, 248)
        w = text35_width(nm, 1)
        tiny(rgb, px + 32 - w // 2, 112, nm)
    s = '(DISPUTED)'
    w = text35_width(s, 2)
    text35(lambda u, v: rgb.__setitem__((v, u), MAGMA_RED if u < 99 else AQUA_BLUE), 99 - w // 2, 124, s, 2)
    return p


def rota():
    """Het werkstrafrooster als RGBA-laag (wit papier met tekst), plus het masker van het papier."""
    p = np.zeros((H, W, 4), np.uint8)
    x0, y0, x1, y1 = 22, 10, 176, 150
    p[y0:y1, x0:x1, :3] = PAPER[0]
    p[y0:y1, x0:x1, 3] = 255
    rgb = p[..., :3]
    # lijntjes
    for y in range(y0 + 34, y1 - 8, 12):
        rgb[y, x0 + 4:x1 - 4] = PAPER[1]
    put_text(rgb, x0 + 8, y0 + 2, 'COMMUNITY SERVICE', INK, 'normal')
    tiny(rgb, x0 + 8, y0 + 20, 'WEATHER INSTITUTE - BREAKROOM ROTA')
    rows = [('DISHES', 'MAXIE'), ('MOPPING', 'ARCHIE'), ('DEHUMIDIFIER', 'MAXIE'), ('SUNSCREEN', 'ARCHIE'),
            ('HOURS LEFT', '600'), ('RULE 1', 'NO DROUGHTS.'), ('RULE 2', 'NO FLOODS.')]
    for i, (a_, b_) in enumerate(rows):
        y = y0 + 25 + i * 12
        put_text(rgb, x0 + 8, y, a_ + ':', INK, 'small')
        col = MAGMA_RED if b_ == 'MAXIE' else AQUA_BLUE if b_ == 'ARCHIE' else INK
        put_text(rgb, x0 + 82, y, b_, col, 'small')
    return p, (x0, y0, x1, y1)


# ------------------------------------------------------------------ de koffievlek
def silhouette(path, flip=False):
    im = gr.sprite(path)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    im = x15(im)
    a = np.array(im)[..., 3] > 0
    a = ndimage.binary_closing(a, iterations=1)
    a = ndimage.binary_fill_holes(a)
    return a


def place(mask, cx, cy):
    out = np.zeros((H, W), bool)
    h, w = mask.shape
    ys, xs = np.nonzero(mask)
    oy = int(cy - h / 2)
    ox = int(cx - w / 2)
    Y, X = ys + oy, xs + ox
    ok = (Y >= 0) & (Y < H) & (X >= 0) & (X < W)
    out[Y[ok], X[ok]] = True
    return out


def sdf(m):
    return ndimage.distance_transform_edt(~m) - ndimage.distance_transform_edt(m)


STAIN_C = (99, 86)
GRO = place(silhouette('graphics/pokemon/groudon/anim_front.png', flip=True), *STAIN_C)
KYO = place(silhouette('graphics/pokemon/kyogre/anim_front.png'), STAIN_C[0], STAIN_C[1] + 4)
SD_G, SD_K = sdf(GRO), sdf(KYO)
DIST = np.hypot(XS - STAIN_C[0], YS - (STAIN_C[1] - 6))


def stain_mask(t):
    if t < T_SPLAT:
        return np.zeros((H, W), bool)
    if t < T_MORPH:
        r = 4 + (t - T_SPLAT) * 2.1           # loopt uit vanaf de plets, binnen de vorm van Groudon
        return (SD_G <= 0) & (DIST < r + BY * 3) | (DIST < min(r, 6))
    u = min(1.0, (t - T_MORPH) / float(T_KYOGRE - T_MORPH))
    u = u * u * (3 - 2 * u)
    return (SD_G * (1 - u) + SD_K * u) <= (BY - 0.5) * 0.8


def draw_stain(rgb, m, t):
    """Koffie: lichter midden, donkere rand (het koffievlek-effect), een paar spatjes rond de plets."""
    edge = m & ~ndimage.binary_erosion(m, iterations=2)
    inner = m & ~edge
    rgb[inner] = COFFEE[0]
    rgb[inner & (BY < 0.25)] = COFFEE[1]
    rgb[edge] = COFFEE[2]
    if t >= T_SPLAT:
        rng = np.random.RandomState(8)
        for _ in range(9):
            a = rng.uniform(0, 2 * math.pi)
            r = rng.uniform(14, 30)
            x, y = int(STAIN_C[0] + math.cos(a) * r), int(STAIN_C[1] - 6 + math.sin(a) * r * 0.7)
            rgb[y:y + 2, x:x + 2] = COFFEE[2]


# ------------------------------------------------------------------ scheuren, brand, water
TEAR_X = np.array([STAIN_C[0] + 4 + 5 * math.sin(y * 0.7) + 3 * math.sin(y * 0.23) + (2 if (y // 3) % 2 else -2)
                   for y in range(H)])


def flames(a, edge_y, x0, x1, t, rng):
    """Vlammen boven een brandrand (edge_y per kolom)."""
    for x in range(x0, x1):
        ey = edge_y[x]
        if ey is None:
            continue
        h = 6 + 5 * math.sin(x * 0.9 + t * 0.7) + 3 * math.sin(x * 0.37 - t * 0.45)
        for k in range(int(h)):
            y = int(ey - k)
            if 0 <= y < H:
                v = k / max(1.0, h)
                if v > 0.8 and BAYER[y % 4, x % 4] < 0.5:
                    continue
                a[y, x] = FIRE[3] if v < 0.2 else FIRE[2] if v < 0.5 else FIRE[1]
        if 0 <= int(ey) + 1 < H:
            a[int(ey) + 1, x] = FIRE[0]


def build(preview=None):
    f = film.Film('service')
    base = board()
    note(base, 178, 16, 54, 42, (248, 236, 120), ['WHO KEEPS', 'MAKING IT', 'RAIN IN THE', 'FRIDGE?'], AQUA_BLUE)
    note(base, 180, 84, 52, 42, (156, 208, 240), ['WHO KEEPS', 'PUTTING', 'LAVA IN THE', 'KETTLE?'], MAGMA_RED)
    post = poster()
    paper, (px0, py0, px1, py1) = rota()
    left = XS < TEAR_X[YS]
    frames = {}

    def compose(t):
        a = base.copy()
        # poster eronder (al zichtbaar door de scheur)
        pm = post[..., 3] > 0
        a[pm] = post[..., :3][pm]
        p = paper[..., :3].copy()
        pa = paper[..., 3] > 0
        m = stain_mask(t)
        draw_stain(p, m & pa, t)
        if t < T_TEAR:
            a[pa] = p[pa]
            pushpin(a, 30, 16, MAGMA_RED)
            pushpin(a, 168, 16, AQUA_BLUE)
            if T_DRIP <= t < T_SPLAT:
                # de druppel valt van boven het beeld
                k = (t - T_DRIP) / float(T_SPLAT - T_DRIP)
                y = int(-6 + (STAIN_C[1] - 6 + 6) * k * k)
                x = STAIN_C[0]
                for dy in range(-4, 3):
                    w = 1 if dy < -2 else 2
                    if 0 <= y + dy < H:
                        a[y + dy, x - w + 1:x + w] = COFFEE[2]
                if 0 <= y - 2 < H:
                    a[y - 1, x] = COFFEE[0]
            return a
        # het scheuren: de scheur loopt van boven naar beneden
        tear_y = H if t >= T_SPLIT else int((t - T_TEAR) / float(T_SPLIT - T_TEAR) * (py1 - py0)) + py0
        u = max(0, t - T_SPLIT)
        # linkerhelft: brandt van onderen en vanaf de scheur, schuift iets naar links
        Lm = pa & left
        Rm = pa & ~left
        if u > 0:
            burn = (H - 1 - YS) * 0.9 + (TEAR_X[YS] - XS) * 0.6 < u * 3.2 + BY * 4 - 10
            charred = (H - 1 - YS) * 0.9 + (TEAR_X[YS] - XS) * 0.6 < u * 3.2 + BY * 4 - 4
        else:
            burn = charred = np.zeros((H, W), bool)
        dxl = -min(14, u // 2)
        dyl = 0
        # rechterhelft: doorweekt (blauw kruipt vanaf de scheur), zakt weg naar rechtsonder
        dxr = min(10, u // 3)
        dyr = int(0.045 * u * u)
        soak = (XS - TEAR_X[YS]) * 1.0 + (YS - py0) * 0.2 < u * 2.6 + BY * 6
        # samenstellen: eerst de rechterhelft (zakt), dan de linker
        Rs = np.roll(np.roll(Rm, dyr, 0), dxr, 1)
        Rp = np.roll(np.roll(p, dyr, 0), dxr, 1)
        Sk = np.roll(np.roll(soak, dyr, 0), dxr, 1)
        if dyr:
            Rs[:dyr] = False
        Rp2 = Rp.copy()
        wet = Rs & Sk
        lum = Rp.astype(np.int32).sum(2)
        Rp2[wet & (lum > 500)] = SOAK[0]
        Rp2[wet & (lum <= 500) & (lum > 300)] = SOAK[1]
        Rp2[wet & (lum <= 300)] = SOAK[2]
        # natte rand
        rim = wet & ~np.roll(wet, 2, 1)
        Rp2[rim & Rs] = SOAK[1]
        a[Rs] = Rp2[Rs]
        if dyr < 3:
            pushpin(a, 168 + dxr, 16, AQUA_BLUE)
        # druppels uit de natte helft
        if u > 6:
            rng = np.random.RandomState(u // 4)
            for k in range(6):
                x = int(TEAR_X[120] + 8 + k * 11 + dxr)
                y = min(H - 1, py1 + dyr + ((u * 3 + k * 17) % 40))
                if 0 <= x < W and 0 <= y < H - 2:
                    a[y:y + 3, x] = SOAK[1]
        Ls = np.roll(Lm, dxl, 1) & ~np.roll(burn, dxl, 1)
        Lp = np.roll(p, dxl, 1)
        Lc = np.roll(charred & ~burn, dxl, 1) & Ls
        a[Ls] = Lp[Ls]
        a[Lc] = (24, 18, 16)
        if Ls[14:19, max(0, 26 + dxl):35 + dxl].any():
            pushpin(a, 30 + dxl, 16, MAGMA_RED)
        if u > 0:
            # vlammen op de brandrand
            edge = [None] * W
            Lsb = Ls
            ys = np.argmax(Lsb, axis=0)
            for x in range(W):
                col = Lsb[:, x]
                if col.any():
                    edge[x] = int(np.nonzero(col)[0].max()) if not Lc[:, x].any() else int(np.nonzero(Lc[:, x])[0].min())
            flames(a, edge, 0, W, u, None)
        # de scheur zelf: rafelrand
        for y in range(py0, min(tear_y, py1)):
            x = int(TEAR_X[y])
            if t < T_SPLIT:
                a[y, x] = PAPER[1]
                a[y, x + 1] = (200, 196, 186)
        return a

    for t in range(T_IN, T_END, STEP):
        frames[t] = compose(t)
    pals = film.auto_palettes([frames[t] for t in sorted(frames)][::3], [(0, 0, 0), INK, PAPER[0]])
    pals = [p[:15] for p in pals]

    def tinted(fade=1.0, white=0.0):
        return f.palset(*[[mix(mix((0, 0, 0), c, fade), (255, 255, 255), white) for c in pal] for pal in pals])

    q = tinted()
    blank = f.palset([(0, 0, 0)], [(0, 0, 0)], [(0, 0, 0)])
    for t in range(T_IN):
        f.add(None, blank)
    for t in range(T_IN, T_END):
        img = frames[t - (t - T_IN) % STEP]
        fade = min(1.0, (t - T_IN + 1) / 14.0)
        wh = 0.0
        if t >= T_FLASH:
            wh = min(1.0, (t - T_FLASH + 1) / 8.0)
        elif T_SPLIT <= t < T_SPLIT + 3:
            wh = 0.35
        f.add(img, tinted(fade, wh), q=q)
    f.encode(preview)
    print('service: %d frames (%.1f s)' % (len(f.frames), len(f.frames) / 60.0))
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    f = build(d)
    if d:
        film.sheet(f.preview_frames, [24, 36, 50, 74, 92, 104, 116, 132, 148, 164, 184, 200],
                   os.path.join(d, 'service_keys.png'))
