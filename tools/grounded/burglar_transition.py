#!/usr/bin/env python3
"""Project Grounded: B_TRANSITION_BURGLAR (Simon de inbreker, het inbreker-event in de steden; ook in het Stadium).

Bewakingscamerabeeld (groenig zwart-wit, scanlines, een rollende storingsstreep, ruis): "CAM 03", tijdstempel en een
knipperende REC. Een woonkamer bij nacht; de Burglar uit Red/Blue (de echte Game Boy-sprite, als comic relief) sluipt
op zijn tenen door het beeld, blijft staan, en draait zich naar de camera. Digitale zoom (2X, 4X): hij kijkt recht in
de lens. REC knippert. Dan het alarm: rood flitsen, ALARM, gevecht.

Film (zie film.py): tiles/tilemaps/paletten naar graphics/battle_transitions/film_burglar*.
Gebruik: python3 tools/grounded/burglar_transition.py [voorbeeldmap]
"""
import math, os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import film
import film_art as fa
from film import W, H, text35, text35_width

# ------------------------------------------------------------------ tijdlijn (zie BURGLAR_* in battle_transition.c)
T_ON = 8          # het beeld springt aan (lijn die opengaat)
T_WALK = 20       # hij sluipt binnen
T_STOP = 92
T_TURN = 106      # draait zich naar de camera
T_ZOOM2 = 124
T_ZOOM4 = 142
T_ALARM = 182
T_END = 218

# ------------------------------------------------------------------ kleuren: groenig zwart-wit
TONE = [(8, 16, 10), (30, 44, 32), (58, 78, 60), (92, 116, 94), (136, 160, 138), (188, 210, 190)]
TXT = (232, 248, 232)
RED = (248, 32, 32)
SCAN = 0.78


def dark(c):
    return fa.shade(c, SCAN)


COLS = TONE + [dark(c) for c in TONE[1:]] + [TXT, RED]      # 13 kleuren


# ------------------------------------------------------------------ de Gen 1-sprite (4 grijstinten, 56x56)
def burglar_grid():
    src = Image.open(os.path.join(film.ROOT, 'graphics/grounded/trainers/burglar/burglar_redblue_bron.png')).convert('L')
    N, LV = 56, [0, 96, 168, 255]
    s = 320 / N
    g = np.array([[min(range(4), key=lambda i: abs(LV[i] - src.getpixel((int((x + 0.5) * s), int((y + 0.5) * s)))))
                   for x in range(N)] for y in range(N)])
    bg = np.zeros((N, N), bool)
    stack = [(x, y) for x in range(N) for y in (0, N - 1)] + [(x, y) for y in range(N) for x in (0, N - 1)]
    while stack:
        x, y = stack.pop()
        if 0 <= x < N and 0 <= y < N and not bg[y, x] and g[y, x] == 3:
            bg[y, x] = True
            stack += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    rgba = np.zeros((N, N, 4), np.uint8)
    lut = [TONE[0], TONE[2], TONE[4], TONE[5]]
    for y in range(N):
        for x in range(N):
            if not bg[y, x]:
                rgba[y, x, :3] = lut[g[y, x]]
                rgba[y, x, 3] = 255
    return Image.fromarray(rgba, 'RGBA')


BURGLAR = burglar_grid()
BURGLAR_R = BURGLAR.transpose(Image.FLIP_LEFT_RIGHT)       # sluipt naar rechts
FACE = (26, 23)                                              # midden van het gezicht in de sprite


# ------------------------------------------------------------------ de kamer
def room():
    a = fa.canvas(TONE[2])
    # achterwand (boven), vloer (onder) met perspectief vanuit een hoge hoek
    fa.rect(a, 0, 0, W, 64, TONE[3])
    fa.rect(a, 0, 62, W, 64, TONE[1])                        # plint
    ys, xs = np.mgrid[0:H, 0:W]
    floor = ys >= 64
    a[floor] = TONE[2]
    # vloerplanken die naar de camera toe uitwaaieren
    for k in range(-8, 9):
        x0 = 120 + k * 18
        for y in range(64, H):
            x = int(round(x0 + (x0 - 120) * (y - 64) / 70.0))
            if 0 <= x < W:
                a[y, x] = TONE[1]
    # deuropening links (donker), schilderij, bank, staande lamp, tv rechts
    fa.rect(a, 14, 8, 50, 64, TONE[0])
    fa.rect(a, 12, 6, 52, 8, TONE[4])
    fa.rect(a, 12, 6, 14, 64, TONE[4])
    fa.rect(a, 50, 6, 52, 64, TONE[4])
    fa.rect(a, 80, 14, 112, 38, TONE[4])
    fa.rect(a, 83, 17, 109, 35, TONE[1])
    fa.rect(a, 88, 26, 104, 35, TONE[2])                     # bergje op het schilderij
    fa.rect(a, 120, 40, 196, 54, TONE[1])                    # bank: rugleuning
    fa.rect(a, 116, 50, 200, 70, TONE[0])
    fa.rect(a, 118, 52, 198, 60, TONE[2])
    fa.rect(a, 116, 46, 124, 70, TONE[1])
    fa.rect(a, 192, 46, 200, 70, TONE[1])
    fa.rect(a, 212, 30, 238, 50, TONE[0])                    # tv op een kastje
    fa.rect(a, 214, 32, 236, 48, TONE[1])
    fa.rect(a, 210, 50, 240, 66, TONE[2])
    fa.rect(a, 210, 50, 240, 52, TONE[4])
    fa.rect(a, 64, 8, 66, 62, TONE[1])                       # staande lamp
    fa.rect(a, 58, 6, 72, 14, TONE[4])
    # vloerkleed
    rug = (((xs - 150) / 70.0) ** 2 + ((ys - 112) / 22.0) ** 2) < 1
    fa.dither(a, rug, TONE[3], 0.5)
    # vignet in de hoeken (lens)
    v = ((xs - 120) / 150.0) ** 2 + ((ys - 80) / 100.0) ** 2
    fa.dither(a, v > 0.75, TONE[0], 0.5)
    a[v > 1.0] = TONE[0]
    return a


def osd(a, rec_on, secs, zoom=None):
    def put(x, y, s, col=TXT, sc=1):
        text35(lambda u, v: a.__setitem__((v + 1, u + 1), TONE[0]) if 0 <= u + 1 < W and 0 <= v + 1 < H else None,
               x, y, s, sc)
        text35(lambda u, v: a.__setitem__((v, u), col) if 0 <= u < W and 0 <= v < H else None, x, y, s, sc)
    put(8, 8, 'CAM 03', TXT, 2)
    put(8, 144, 'NOV 05  03:14:%02d AM' % secs, TXT, 1)
    put(8, 20, 'LIVING ROOM', TXT, 1)
    ys, xs = np.mgrid[0:H, 0:W]
    dot = (xs - 196) ** 2 + (ys - 12) ** 2 <= 12
    a[dot] = RED if rec_on else TONE[1]
    put(204, 8, 'REC', TXT, 2)
    if zoom:
        put(196, 144, 'ZOOM %dX' % zoom, TXT, 1)
    return a


def scanlines(a):
    out = a.copy()
    lut = {tuple(c): dark(c) for c in TONE}
    rows = out[1::2]
    for c, d in lut.items():
        m = (rows == c).all(-1)
        rows[m] = d
    return out


def noise(a, rng, band_y, n=14):
    """Storingsstreep (twee lichte lijnen) en wat losse ruispixels."""
    for y in (band_y, band_y + 1):
        if 0 <= y < H:
            row = a[y]
            m = (row != np.array(TXT)).any(-1) & (row != np.array(RED)).any(-1)
            row[m] = TONE[4]
    for _ in range(n):
        x, y = rng.randint(0, W - 2), rng.randint(0, H)
        a[y, x:x + rng.randint(1, 4)] = TONE[5] if rng.rand() < 0.5 else TONE[0]
    return a


def wide(bx, by, mirrored=True):
    a = room()
    fa.blit(a, BURGLAR_R if mirrored else BURGLAR, bx, by)
    return a


def zoomed(base, cx, cy, k):
    """Digitale zoom: uitsnede rond (cx, cy), k keer vergroot (naaste buur, blokkerig zoals een goedkope camera)."""
    w, h = W / k, H / k
    x0 = int(round(min(max(cx - w / 2, 0), W - w)))
    y0 = int(round(min(max(cy - h / 2, 0), H - h)))
    crop = Image.fromarray(base).crop((x0, y0, x0 + int(w), y0 + int(h)))
    return np.array(crop.resize((W, H), Image.NEAREST))


# ------------------------------------------------------------------ film
def build(preview=None):
    f = film.Film('burglar')
    rng = np.random.RandomState(4)
    pal = list(COLS)

    def ps(alarm=0.0, rec=True, k=1.0):
        out = []
        for c in pal:
            if c == RED and not rec:
                c = TONE[1]
            elif alarm and c != TXT:
                c = fa.mix(c, (255, 40, 40), alarm * (0.35 + 0.65 * (sum(c) / 600.0)))
            out.append(fa.shade(c, k))
        return f.palset(out, out, out)

    f.ref = ps()
    for t in range(T_ON):
        f.add(None, ps(k=0.0))
    # aan: een lichte lijn die opengaat tot het beeld
    bx0, bx1, by = -56, 104, 86
    first = scanlines(osd(wide(bx0, by), True, 7))
    for t in range(T_ON, T_WALK):
        k = t - T_ON
        img = fa.canvas(TONE[0])
        hh = int(80 * min(1.0, (k + 1) / 6.0))
        if k < 6:
            img[80 - max(1, hh):80 + max(1, hh)] = first[80 - max(1, hh):80 + max(1, hh)]
            img[80 - max(1, hh):80 - max(1, hh) + 1] = TXT
        else:
            img = first
        f.add(img, f.ref)

    def frame_at(t, img_fn):
        secs = 7 + (t - T_ON) // 60
        rec = ((t // 16) % 2) == 0
        img = scanlines(osd(img_fn(), True, secs, img_fn.zoom if hasattr(img_fn, 'zoom') else None))
        return noise(img, rng, (t * 3) % 200 - 20, 4), rec

    # sluipen: op zijn tenen, elke 2 frames een stapje, met een wipje per pas
    for t in range(T_WALK, T_STOP, 4):
        u = (t - T_WALK) / (T_STOP - T_WALK)
        x = bx0 + (bx1 - bx0) * u
        bob = [0, -2][(t // 4) % 2]
        fn = lambda: wide(x, by + bob)
        img, rec = frame_at(t, fn)
        f.add(img, ps(rec=rec), 4)
    for t in range(T_STOP, T_TURN, 4):
        img, rec = frame_at(t, lambda: wide(bx1, by))
        f.add(img, ps(rec=rec), min(4, T_TURN - t))
    for t in range(T_TURN, T_ZOOM2, 4):
        img, rec = frame_at(t, lambda: wide(bx1, by, False))
        f.add(img, ps(rec=rec), min(4, T_ZOOM2 - t))
    base = wide(bx1, by, False)
    cx, cy = bx1 + FACE[0], by + FACE[1]
    for z, t0, t1 in ((2, T_ZOOM2, T_ZOOM4), (4, T_ZOOM4, T_END)):
        zb = zoomed(base, cx, cy, z)
        def fn(zb=zb):
            return zb.copy()
        fn.zoom = z
        for t in range(t0, t1, 2):
            if (t - t0) % 4 == 0:
                img0, rec = frame_at(t, fn)
            img = img0.copy()
            rec = ((t // 16) % 2) == 0
            if t >= T_ALARM:
                k = (t - T_ALARM) // 4
                on = k % 2 == 0
                if on:
                    w = text35_width('ALARM', 4)
                    text35(lambda u, v: img.__setitem__((v, u), TXT), (W - w) // 2, 64, 'ALARM', 4)
                f.add(img, ps(alarm=1.0 if on else 0.35, rec=rec), min(2, t1 - t))
            else:
                f.add(img, ps(rec=rec), min(2, t1 - t))
    f.encode(preview)
    return f


if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else None
    f = build(d)
    if d:
        film.sheet(f.preview_frames, [12, 18, 40, 70, 96, 112, 130, 150, 170, 184, 190, 214],
                   os.path.join(d, 'burglar_keys.png'))
