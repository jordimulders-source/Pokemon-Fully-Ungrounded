#!/usr/bin/env python3
"""Project Grounded: B_TRANSITION_OGERPON (het einde van de Ogerpon-quest, Fortree Jungle).

Een maskerfestival 's nachts: een slinger papieren lantaarns, de silhouetten van kraampjes en een torii, en een
maskerkraam met vijf haken. Er hangen vier maskers (Wellspring, Hearthflame, Teal, Cornerstone) met prijskaartjes;
één haak is leeg ("STOLEN", de Loyal Three). Op het Teal-masker staat "NOT FOR SALE". De camera schuift en zoomt naar
het Teal-masker; de lantaarns gaan een voor een uit, de ogen van het masker gaan branden: het is geen masker. Ogerpon
springt op de camera af in een wolk bladeren, groene flits, gevecht.

De maskers zijn uitsneden uit de echte Ogerpon-front-sprites (elke vorm draagt zijn masker); Ogerpon zelf is de
Teal-front-sprite (2x via Scale2x).
Gebruik: python3 tools/grounded/ogerpon_transition.py [voorbeeldmap]
"""
import math, os, sys
from collections import deque
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
import gbagfx_render as gr
from film import W, H, text35, text35_width
from wally_transition import scale2x

T_IN = 8
T_OUT = 30        # de lantaarns gaan een voor een uit
T_ZOOM = 50       # de camera begint te bewegen
T_ZOOMED = 110    # ingezoomd op het Teal-masker
T_EYES = 122      # de ogen gaan branden (lantaarns zijn dan uit)
T_LEAP = 164      # Ogerpon springt
T_FLASH = 204
T_END = 216
STEP = 3          # gameframes per beeld

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
YS, XS = np.mgrid[0:H, 0:W]
BY = BAYER[YS % 4, XS % 4]

SKY = [(6, 6, 22), (12, 12, 40), (22, 20, 62), (36, 30, 84)]
SIL = (8, 6, 16)
WOOD = [(40, 22, 14), (74, 42, 24), (112, 70, 38), (150, 102, 56)]
RED = [(96, 14, 18), (168, 30, 30), (224, 64, 44)]
PAPER = (236, 222, 190)
INK = (24, 18, 18)
LGLOW = [(255, 150, 60), (255, 206, 110), (255, 246, 196)]
EYE = [(255, 210, 60), (255, 250, 200)]


def mix(a, b, k):
    return tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))


# ------------------------------------------------------------------ maskers uit de echte sprites
def mask_of(form, xflood=26):
    """Het masker uit een Ogerpon-front-sprite: alles links van x=37, minus Ogerpons eigen haar/lijf (flood fill vanaf
    rechts over de kleuren van het lijf)."""
    path = os.path.join(film.ROOT, 'graphics/pokemon/ogerpon/%s.png' % form)
    im = Image.open(path)
    a = np.array(im)
    P = np.array(im.getpalette()[:48], np.uint8).reshape(16, 3)
    x1 = 37
    body = set(np.unique(a[:, x1:][a[:, x1:] > 0]))
    eat = np.zeros(a.shape, bool)
    q = deque()
    for y in range(64):
        for x in range(x1, 64):
            if a[y, x]:
                eat[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < 64 and xflood <= xx < 64 and not eat[yy, xx] and a[yy, xx] in body:
                eat[yy, xx] = True
                q.append((yy, xx))
    keep = (a > 0) & ~eat
    keep[45:] = False
    rgba = np.zeros((64, 64, 4), np.uint8)
    rgba[..., :3] = P[a]
    rgba[..., 3] = keep * 255
    return Image.fromarray(rgba[:46, :40], 'RGBA')


MASKS = [mask_of('wellspring/front'), mask_of('hearthflame/front', 36), mask_of('front'), None,
         mask_of('cornerstone/front')]
TAGS = ['500P', '500P', 'NOT FOR SALE', 'STOLEN', '500P']
HOOKS = [40, 80, 120, 160, 200]
TEAL = 2
EYES_AT = [(16, 25), (22, 21)]        # ogen van het Teal-masker (maskercoördinaten)
MASK_Y = 78
OGERPON = scale2x(gr.sprite('graphics/pokemon/ogerpon/front.png'))


# ------------------------------------------------------------------ het festival (wereld = 1x)
LANTERNS = [(14 + i * 30, 0) for i in range(8)]


def rope_y(x):
    return 10 + 10 * math.sin(math.pi * ((x % 120) / 120.0))


def lantern(d, cx, cy, on, sway=0):
    """Papieren lantaarn (chochin): rood met ribben, zwarte kapjes, gloeiend hart als hij aan is."""
    cx += sway
    w, h = 9, 13
    body = RED[2] if on else RED[0]
    d.line([(cx - sway, cy - 8), (cx, cy - h // 2 - 1)], fill=INK)
    d.ellipse([cx - w, cy - h // 2, cx + w, cy + h // 2], fill=body, outline=RED[0])
    if on:
        d.ellipse([cx - w + 3, cy - h // 2 + 2, cx + w - 3, cy + h // 2 - 2], fill=LGLOW[1])
        d.ellipse([cx - 2, cy - 3, cx + 2, cy + 3], fill=LGLOW[2])
    for k in (-4, 0, 4):
        d.line([(cx - w + 2, cy + k), (cx + w - 2, cy + k)], fill=RED[1] if on else (60, 10, 14))
    d.rectangle([cx - 5, cy - h // 2 - 2, cx + 5, cy - h // 2], fill=INK)
    d.rectangle([cx - 5, cy + h // 2, cx + 5, cy + h // 2 + 2], fill=INK)


def background():
    img = np.zeros((H, W, 3), np.uint8)
    for y in range(H):
        k = y / 110.0
        lv = min(3, k * 3.0)
        lo = int(lv)
        img[y] = SKY[lo]
        hi = min(3, lo + 1)
        m = BY[y] < (lv - lo)
        img[y][m] = SKY[hi]
    rng = np.random.RandomState(2)
    for _ in range(40):
        x, y = rng.randint(W), rng.randint(60)
        img[y, x] = (200, 200, 230) if rng.rand() < 0.4 else (120, 120, 170)
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im)
    # torii en kraampjes in de verte (silhouet)
    d.rectangle([168, 40, 174, 100], fill=SIL)
    d.rectangle([214, 40, 220, 100], fill=SIL)
    d.polygon([(156, 34), (232, 34), (236, 30), (152, 30)], fill=SIL)
    d.rectangle([162, 44, 226, 48], fill=SIL)
    for x0, w, h in ((0, 44, 30), (34, 40, 22), (226, 30, 26)):
        d.polygon([(x0, 100 - h), (x0 + w // 2, 100 - h - 10), (x0 + w, 100 - h), (x0 + w, 100), (x0, 100)], fill=SIL)
    # bomen
    for x0 in range(-10, 250, 26):
        d.ellipse([x0, 62 + (x0 * 7) % 10, x0 + 34, 104], fill=(10, 14, 22))
    d.rectangle([0, 100, W, H], fill=(14, 10, 20))
    return im


def stall(im, lanterns_on, eyes=0.0, dim=1.0):
    d = ImageDraw.Draw(im)
    # lantaarnslinger
    pts = [(x, rope_y(x)) for x in range(0, W + 1, 4)]
    d.line(pts, fill=INK, width=1)
    for i, (x, _) in enumerate(LANTERNS):
        on = lanterns_on[i]
        y = rope_y(x) + 12
        if on:
            # gloed (dither)
            a = np.array(im)
            r = 17
            yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
            dd = np.hypot(xx, yy) / r
            for (oy, ox), v in np.ndenumerate(dd):
                X, Y = x + ox - r, int(y) + oy - r
                if 0 <= X < W and 0 <= Y < H and v < 1 and BAYER[Y % 4, X % 4] > v * 1.3 + 0.15:
                    a[Y, X] = mix(tuple(a[Y, X]), LGLOW[0], 0.35)
            im.paste(Image.fromarray(a))
            d = ImageDraw.Draw(im)
        lantern(d, x, int(y), on)
    # kraam: palen, luifel (rood-wit), achterwand, toonbank
    d.rectangle([14, 56, 19, 160], fill=WOOD[1])
    d.rectangle([221, 56, 226, 160], fill=WOOD[1])
    d.rectangle([18, 68, 222, 140], fill=WOOD[0])
    for x in range(18, 222, 6):
        d.line([(x, 70), (x, 140)], fill=(48, 26, 16))
    for i, x in enumerate(range(10, 230, 20)):
        d.rectangle([x, 52, x + 19, 66], fill=RED[1] if i % 2 == 0 else PAPER)
        d.ellipse([x, 60, x + 19, 72], fill=RED[1] if i % 2 == 0 else PAPER)
    d.rectangle([8, 48, 232, 53], fill=WOOD[2])
    # bordje op de luifel
    s = 'FESTIVAL MASKS'
    tw = text35_width(s, 1)
    d.rectangle([120 - tw // 2 - 4, 40, 120 + tw // 2 + 3, 48], fill=PAPER, outline=INK)
    a = np.array(im)
    text35(lambda u, v: a.__setitem__((v, u), INK), 120 - tw // 2, 42, s)
    # haken, maskers, kaartjes
    for i, hx in enumerate(HOOKS):
        a[MASK_Y - 6:MASK_Y - 2, hx] = (180, 180, 170)
        a[MASK_Y - 2, hx - 1:hx + 2] = (180, 180, 170)
        m = MASKS[i]
        if m is not None:
            mi = Image.fromarray(a)
            mm = m
            if i == TEAL and eyes > 0:
                mm = glowing(m, eyes)
            mi.paste(mm, (hx - 19, MASK_Y - 3), mm)
            a = np.array(mi)
        tag = TAGS[i]
        tw = text35_width(tag, 1)
        ty = 128
        a[ty - 2:ty + 7, hx - tw // 2 - 2:hx + tw // 2 + 3] = PAPER if i != TEAL else (250, 236, 120)
        a[ty - 3, hx] = INK
        text35(lambda u, v: a.__setitem__((v, u), INK if i != 3 else RED[1]), hx - tw // 2, ty, tag)
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    d.rectangle([10, 140, 230, 160], fill=WOOD[2])
    d.rectangle([10, 140, 230, 142], fill=WOOD[3])
    for x in range(10, 230, 24):
        d.line([(x, 143), (x, 160)], fill=WOOD[1])
    if dim < 1.0:
        a = (np.array(im).astype(np.float64) * dim).astype(np.uint8)
        if eyes > 0:
            # de ogen dimmen niet mee
            g = np.array(glowing(MASKS[TEAL], eyes))
            o = np.array(MASKS[TEAL])
            hx = HOOKS[TEAL] - 19
            diff = (g[..., :3] != o[..., :3]).any(2) & (g[..., 3] > 0)
            ys, xs = np.nonzero(diff)
            a[ys + MASK_Y - 3, xs + hx] = g[ys, xs, :3]
        im = Image.fromarray(a)
    return im


def glowing(m, k):
    """Het Teal-masker met brandende ogen (k = 0..1)."""
    a = np.array(m).copy()
    for (ex, ey) in EYES_AT:
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                r = math.hypot(dx, dy)
                X, Y = ex + dx, ey + dy
                if 0 <= X < a.shape[1] and 0 <= Y < a.shape[0] and a[Y, X, 3]:
                    if r <= 1.0 * k + 0.2:
                        a[Y, X, :3] = EYE[1]
                    elif r <= 2.3 * k:
                        a[Y, X, :3] = EYE[0]
    return Image.fromarray(a, 'RGBA')


def camera(world, zoom, cx, cy):
    """Uitsnede rond (cx, cy) met zoom (nearest, pixel-art)."""
    w, h = W / zoom, H / zoom
    x0 = min(max(cx - w / 2, 0), W - w)
    y0 = min(max(cy - h / 2, 0), H - h)
    crop = world.crop((int(round(x0)), int(round(y0)), int(round(x0 + w)), int(round(y0 + h))))
    return np.array(crop.resize((W, H), Image.NEAREST))


def ease(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def leaves(img, t, rng_seed, n=40, origin=(120, 110)):
    """Wolk bladeren die naar buiten (op de camera af) vliegt."""
    rng = np.random.RandomState(rng_seed)
    a = img
    for i in range(n):
        ang = rng.uniform(0, 2 * math.pi)
        sp = rng.uniform(2.0, 6.5)
        r = sp * t + rng.uniform(0, 8)
        x = origin[0] + math.cos(ang) * r
        y = origin[1] + math.sin(ang) * r * 0.8 - t * 0.6
        s = 1 + int(r / 40)
        col = [(40, 140, 60), (90, 190, 70), (20, 96, 66)][i % 3]
        for k in range(-2 * s, 2 * s + 1):
            for j in range(-s, s + 1):
                X = int(x + k * math.cos(ang + 1) - j * math.sin(ang + 1))
                Y = int(y + k * math.sin(ang + 1) + j * math.cos(ang + 1))
                if 0 <= X < W and 0 <= Y < H and abs(j) <= s * (1 - abs(k) / (2.0 * s + 1)) + 0.5:
                    a[Y, X] = col


def build(preview=None):
    f = film.Film('ogerpon')
    bg = background()
    frames = {}
    moving = {}
    teal_c = (HOOKS[TEAL], MASK_Y + 20)
    for t in range(T_IN, T_LEAP, STEP):
        # lantaarns: aan, dan na het inzoomen een voor een uit (van buiten naar binnen)
        on = [True] * 8
        order = [0, 7, 1, 6, 2, 5]
        if t >= T_OUT:
            for j in order[:(t - T_OUT) // 4 + 1]:
                on[j] = False
        if t >= T_EYES:
            on[3] = on[4] = False      # de laatste twee gaan tegelijk uit als de ogen opengaan
        eyes = 0.0 if t < T_EYES else min(1.0, (t - T_EYES) / 12.0)
        dim = 1.0 - 0.25 * min(1.0, max(0.0, (t - T_OUT) / 24.0)) - (0.3 if t >= T_EYES else 0.0)
        world = stall(bg.copy(), on, eyes, dim)
        u = ease((t - T_ZOOM) / float(T_ZOOMED - T_ZOOM))
        # van wijd (iets naar links, op het lege haakje en de lantaarns) naar het Teal-masker
        zoom = 1.0 + 1.9 * u
        cx = 104 + (teal_c[0] - 104) * u
        cy = 84 + (teal_c[1] - 84) * u
        if t >= T_EYES + 8:
            # na het oplichten: kleine schok naar voren
            zoom += min(0.25, (t - T_EYES - 8) * 0.03)
        frames[t] = camera(world, zoom, cx, cy)
        moving[t] = T_ZOOM <= t < T_ZOOMED
    # Ogerpon springt op je af: donker, bladeren, de sprite groeit (2x -> 2,6x)
    dark = frames[T_LEAP - STEP] // 3
    for t in range(T_LEAP, T_END, STEP):
        k = (t - T_LEAP) / float(T_END - T_LEAP)
        img = dark.copy()
        leaves(img, t - T_LEAP + 4, 5, 50)
        z = 1.0 + 0.25 * ease(k * 1.3)
        o = OGERPON.resize((int(128 * z), int(128 * z)), Image.NEAREST)
        im = Image.fromarray(img)
        im.paste(o, (int(120 - o.width / 2), int(152 - o.height + (1 - ease(k * 2)) * 70)), o)
        img = np.array(im)
        leaves(img, t - T_LEAP, 6, 26)
        frames[t] = img

    pa = film.auto_palettes([frames[t] for t in sorted(frames) if t < T_LEAP][::4], [(0, 0, 0), INK, PAPER])
    pb = film.auto_palettes([frames[t] for t in sorted(frames) if t >= T_LEAP][::2], [(0, 0, 0), (40, 140, 60)])
    pa = [p[:15] for p in pa]
    pb = [p[:15] for p in pb]

    def tinted(p, fade=1.0, white=0.0, tint=(255, 255, 255)):
        return f.palset(*[[mix(mix((0, 0, 0), c, fade), tint, white) for c in pal] for pal in p])

    qa, qb = tinted(pa), tinted(pb)
    blank = f.palset([(0, 0, 0)], [(0, 0, 0)], [(0, 0, 0)])
    for t in range(T_IN):
        f.add(None, blank)
    for t in range(T_IN, T_END):
        base = T_IN if t < T_LEAP else T_LEAP
        img = frames[t - (t - base) % STEP]
        if t < T_LEAP:
            fade = min(1.0, (t - T_IN + 1) / 14.0)
            wh = 0.3 if T_EYES + 10 <= t < T_EYES + 14 else 0.0
            # tijdens het zoomen grover (minder tiles laden): het beeld beweegt toch
            f.add(img, tinted(pa, fade, wh, EYE[0]), q=qa, budget=300 if moving.get(t - (t - base) % STEP) else None)
        else:
            wh = 0.0
            if t < T_LEAP + 3:
                wh = 0.6
            if t >= T_FLASH:
                wh = min(1.0, (t - T_FLASH + 1) / 8.0)
            f.add(img, tinted(pb, 1.0, wh, (220, 255, 210)), q=qb)
    f.encode(preview)
    print('ogerpon: %d frames (%.1f s)' % (len(f.frames), len(f.frames) / 60.0))
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    f = build(d)
    if d:
        film.sheet(f.preview_frames, [24, 40, 56, 72, 90, 110, 128, 150, 166, 178, 192, 206],
                   os.path.join(d, 'ogerpon_keys.png'))
