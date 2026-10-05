#!/usr/bin/env python3
"""Project Grounded: tiles en tilemaps voor B_TRANSITION_NEO_PLASMA (de Neo Team Plasma-transitie uit Black 2/White 2).

Bron: graphics/grounded/trainers/neo_plasma/bw2_neo_plasma_transitie_bron.gif (512x382, 31 frames, 2,58 s).
- De blauwe P (frame 0) en het Plasma-schild (frame 11) komen uit de GIF zelf: P = blauwe pixels + de zwarte rand
  eromheen; schild = verschil tussen frame 11 en frame 0 (+ de P), gaten gevuld. Verkleind naar GBA-maat
  (160/382: de DS-hoogte past precies), midden op het scherm.
- De lichtstreep (Z), de lichtbol en de bliksems worden hier getekend (scherper dan verkleinde GIF-pixels).
- Achtergrond: donker nachtblauw met een subtiel raster van 16 px (in plaats van het Plasma-schip).

Uitvoer (graphics/battle_transitions/):
- route_neo_plasma.png / .pal: ontdubbelde tiles (ook gespiegeld) en 2 paletten (normaal, bliksems fel).
- route_neo_plasma.bin: NP_KEYS tilemaps van 30x20 (u16 met flip-bits, palet 15 al ingevuld), op volgorde:
  0 = P, 1..NP_BALL = lichtbol trekt de Z, NP_BALL+1 = volledige Z, daarna het schild, daarna NP_BOLTS bliksemvarianten.
Gebruik: python3 tools/grounded/neo_plasma_transition.py [voorbeeldmap]
"""
import math, os, random, struct, sys
import numpy as np
from PIL import Image, ImageSequence
from scipy import ndimage as nd

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
GIF = os.path.join(ROOT, 'graphics/grounded/trainers/neo_plasma/bw2_neo_plasma_transitie_bron.gif')
OUT = os.path.join(ROOT, 'graphics/battle_transitions/')
W, H = 240, 160
K = 160 / 382.0                       # GIF -> GBA
NP_BALL = 9                           # sleutelbeelden van de lichtbol
NP_BOLTS = 6                          # bliksemvarianten

# palet (8-bit); index 0 = leeg
PAL = [(0, 0, 0), (0, 0, 0), (6, 8, 22), (16, 24, 52),
       (10, 40, 120), (20, 90, 200), (24, 140, 232), (20, 192, 250), (165, 235, 255), (255, 255, 255),
       (48, 50, 58), (100, 104, 112), (165, 168, 176), (218, 220, 228),
       (140, 200, 255), (40, 90, 210)]
PAL_FLASH = list(PAL)
PAL_FLASH[14] = (215, 240, 255)       # bliksems flakkeren: glans feller
PAL_FLASH[15] = (80, 150, 250)
ART_IDX = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]   # kleuren voor P en schild
BG, GRID, BLACK, WHITE, LCYAN, CYAN, AZURE, BLUE, BOLT, HALO = 2, 3, 1, 9, 8, 7, 6, 5, 14, 15


def gba(c):
    return tuple((v >> 3) << 3 for v in c)


def nearest(rgb, idxs):
    best, bd = 0, 1e18
    for i in idxs:
        p = PAL[i]
        d = 3 * (rgb[0] - p[0]) ** 2 + 6 * (rgb[1] - p[1]) ** 2 + 2 * (rgb[2] - p[2]) ** 2
        if d < bd:
            best, bd = i, d
    return best


def gif_frames():
    return [np.array(f.convert('RGB')).astype(int) for f in ImageSequence.Iterator(Image.open(GIF))]


def extract(frames):
    f0, f11 = frames[0], frames[11]
    yy, xx = np.mgrid[:f0.shape[0], :f0.shape[1]]
    R, B = f0[..., 0], f0[..., 2]
    blue = (B > 100) & (B - R > 60) & (xx > 170) & (xx < 345) & (yy > 55) & (yy < 303)
    ring = nd.binary_dilation(blue, iterations=5) & (f0.mean(2) < 60) & (xx > 170) & (xx < 345) & (yy > 55) & (yy < 303)
    pmask = nd.binary_opening(blue | ring, iterations=1)
    d = (np.abs(f11 - f0).sum(2) > 40) & (xx > 145) & (xx < 370) & (yy > 55) & (yy < 305)
    d |= pmask
    smask = nd.binary_opening(nd.binary_fill_holes(nd.binary_closing(d, iterations=4)), iterations=2)
    return shrink(f0, pmask), shrink(f11, smask)


def shrink(rgb, mask):
    """Naar GBA-maat (premultiplied), dan per pixel naar het palet. Geeft een 240x160-array van indexen (0 = leeg)."""
    h, w = mask.shape
    nw, nh = int(round(w * K)), int(round(h * K))
    rgba = np.zeros((h, w, 4), np.float64)
    rgba[..., :3] = rgb * mask[..., None]
    rgba[..., 3] = mask * 255.0
    chans = [np.array(Image.fromarray(rgba[..., c].astype(np.float32), 'F').resize((nw, nh), Image.BOX)) for c in range(4)]
    a = chans[3]
    out = np.zeros((H, W), np.uint8)
    ox = (W - nw) // 2
    oy = 2
    for y in range(nh):
        for x in range(nw):
            if a[y, x] >= 110 and 0 <= y + oy < H and 0 <= x + ox < W:
                c = tuple(chans[k][y, x] * 255.0 / a[y, x] for k in range(3))
                out[y + oy, x + ox] = nearest(c, ART_IDX)
    # buitenrand: 1 px zwart rondom, zodat de vorm los komt van de donkere achtergrond
    m = out > 0
    edge = nd.binary_dilation(m) & ~m
    out[edge] = BLACK
    return out


def gx(x):
    return W / 2 + (x - 256) * K


def gy(y):
    return y * K + 2


# de Z (uit GIF-frame 6): van rechts, naar links, schuin naar rechtsonder, dan naar links het beeld uit
Z_PTS = [(W + 16, gy(139)), (gx(142), gy(139)), (gx(330), gy(232)), (-16, gy(232))]


def seg_dist(px, py, a, b):
    ax, ay = a; bx, by = b
    vx, vy = bx - ax, by - ay
    L = vx * vx + vy * vy
    t = max(0.0, min(1.0, ((px - ax) * vx + (py - ay) * vy) / L)) if L else 0.0
    return math.hypot(px - ax - t * vx, py - ay - t * vy)


# waar de lichtbol is (booglengte langs de Z) op GBA-frame t, gemeten in de GIF: frame 1 (t 14) aan de rechterrand,
# frame 2 (t 18) rechts van de P, frame 3 (t 21,6) in de linkerhoek, frame 4 (t 25) halverwege de schuine streep,
# frame 5 (t 29) links op de onderste streep, frame 6 (t 32) het beeld uit
NP_ZSTART = 14
BALL_TS = [(14, 16), (18, 85), (21.6, 185), (25, 229), (29, 358), (32, 440)]
BALL_TOTAL = 440


def ball_s(t):
    for (t0, s0), (t1, s1) in zip(BALL_TS, BALL_TS[1:]):
        if t <= t1:
            return s0 + (s1 - s0) * (max(t, t0) - t0) / (t1 - t0)
    return BALL_TS[-1][1]


def path_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def partial(pts, s):
    """De polylijn tot booglengte s, plus het eindpunt."""
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        l = math.hypot(b[0] - a[0], b[1] - a[1])
        if s <= l:
            p = (a[0] + (b[0] - a[0]) * s / l, a[1] + (b[1] - a[1]) * s / l)
            out.append(p)
            return out, p
        s -= l
        out.append(b)
    return out, pts[-1]


def draw_beam(img, pts):
    ys, xs = np.mgrid[:H, :W]
    d = np.full((H, W), 99.0)
    for a, b in zip(pts, pts[1:]):
        x0, x1 = sorted((a[0], b[0])); y0, y1 = sorted((a[1], b[1]))
        sel = (xs >= x0 - 6) & (xs <= x1 + 6) & (ys >= y0 - 6) & (ys <= y1 + 6)
        for y, x in zip(*np.nonzero(sel)):
            d[y, x] = min(d[y, x], seg_dist(x + 0.5, y + 0.5, a, b))
    img[d < 4.2] = BLUE
    img[d < 3.2] = CYAN
    img[d < 2.2] = LCYAN
    img[d < 1.2] = WHITE


def draw_ball(img, c):
    cx, cy = c
    for y in range(max(0, int(cy) - 16), min(H, int(cy) + 17)):
        for x in range(max(0, int(cx) - 16), min(W, int(cx) + 17)):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            r = math.hypot(dx, dy)
            spike = (abs(dy) < 1 and abs(dx) < 16) or (abs(dx) < 1 and abs(dy) < 14) or (abs(abs(dx) - abs(dy)) < 0.8 and r < 10)
            if r < 5.5:
                img[y, x] = WHITE
            elif r < 7.5 or (spike and r < 10):
                img[y, x] = LCYAN if img[y, x] not in (WHITE,) else img[y, x]
            elif r < 9.5 or spike:
                if img[y, x] not in (WHITE, LCYAN):
                    img[y, x] = CYAN


def background():
    img = np.full((H, W), BG, np.uint8)
    img[::16, :] = GRID
    img[:, ::16] = GRID
    return img


def overlay(base, art):
    out = base.copy()
    out[art > 0] = art[art > 0]
    return out


def bolt_path(rng, a, b, rough):
    pts = [a, b]
    for _ in range(4):
        npts = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
            l = math.hypot(q[0] - p[0], q[1] - p[1])
            nx, ny = -(q[1] - p[1]) / (l or 1), (q[0] - p[0]) / (l or 1)
            off = rng.uniform(-1, 1) * l * rough
            npts += [(mx + nx * off, my + ny * off), q]
        pts = npts
    return pts


def draw_bolt(img, pts, rng):
    """Dunne bliksem: witte kern van 1 px, glans eromheen, hier en daar een ruitvormige lus (zoals in de GIF)."""
    ys, xs = np.mgrid[:H, :W]
    core = np.zeros((H, W), bool)
    for a, b in zip(pts, pts[1:]):
        n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1]))) + 1
        for i in range(n + 1):
            x = int(a[0] + (b[0] - a[0]) * i / n); y = int(a[1] + (b[1] - a[1]) * i / n)
            if 0 <= x < W and 0 <= y < H:
                core[y, x] = True
    # ruitjes: een tweede, licht verschoven kern over een stukje van de lijn
    for k in range(2, len(pts) - 3, 5):
        if rng.random() < 0.6:
            a, b = pts[k], pts[k + 2]
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            l = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
            nx, ny = -(b[1] - a[1]) / l * 3, (b[0] - a[0]) / l * 3
            for p, q in ((a, (mx + nx, my + ny)), ((mx + nx, my + ny), b)):
                n = int(max(abs(q[0] - p[0]), abs(q[1] - p[1]))) + 1
                for i in range(n + 1):
                    x = int(p[0] + (q[0] - p[0]) * i / n); y = int(p[1] + (q[1] - p[1]) * i / n)
                    if 0 <= x < W and 0 <= y < H:
                        core[y, x] = True
    glow = nd.binary_dilation(core) & ~core
    halo = nd.binary_dilation(core, iterations=2) & ~core & ~glow
    img[halo & (img != WHITE) & (img != LCYAN)] = HALO
    img[glow] = BOLT
    img[core] = WHITE


# bliksems: (start bij het schild, eindpunt buiten beeld), in GBA-pixels; naar de GIF (frames 15-30)
BOLTS = [((100, 52), (-6, -4)),      # linksboven
         ((124, 40), (110, -6)),     # omhoog
         ((96, 74), (-6, 66)),       # links
         ((146, 74), (246, 70)),     # rechts
         ((104, 106), (8, 166)),     # linksonder
         ((140, 104), (232, 166))]   # rechtsonder


BOLT_VERSIONS = 3
# per sleutelbeeld welke versie elke bliksem heeft: zo ontstaan NP_BOLTS verschillende beelden uit 3 versies per
# bliksem (de tiles van één bliksem worden hergebruikt; alleen waar bliksems elkaar kruisen ontstaan nieuwe tiles)
BOLT_MIX = [(0, 1, 2, 0, 1, 2), (1, 2, 0, 2, 0, 1), (2, 0, 1, 1, 2, 0), (1, 0, 2, 2, 1, 0), (0, 2, 1, 0, 0, 2),
            (2, 1, 0, 1, 2, 1)]


def bolt_points(d, v):
    rng = random.Random(1000 + d * 31 + v * 7)
    a, b = BOLTS[d]
    ax, ay = a[0] + rng.uniform(-3, 3), a[1] + rng.uniform(-3, 3)
    bx, by = b[0] + rng.uniform(-14, 14), b[1] + rng.uniform(-10, 10)
    return bolt_path(rng, (ax, ay), (bx, by), 0.24), rng


def bolts_layer(base, mix):
    img = base.copy()
    for d, v in enumerate(mix):
        pts, rng = bolt_points(d, v)
        draw_bolt(img, pts, rng)
    return img


def tiles_of(img):
    return [tuple(img[r * 8:(r + 1) * 8, c * 8:(c + 1) * 8].flatten()) for r in range(20) for c in range(30)]


def build():
    frames = gif_frames()
    P, S = extract(frames)
    bg = background()
    keys = [overlay(bg, P)]
    total = path_len(Z_PTS)
    for i in range(NP_BALL):
        s = ball_s(NP_ZSTART + 2 * i) * total / BALL_TOTAL
        pts, head = partial(Z_PTS, s)
        img = keys[0].copy()
        draw_beam(img, pts)
        draw_ball(img, head)
        keys.append(img)
    full = keys[0].copy()
    draw_beam(full, Z_PTS)
    keys.append(full)
    shield = overlay(bg, S)
    keys.append(shield)
    for v in range(NP_BOLTS):
        keys.append(bolts_layer(shield, BOLT_MIX[v]))

    # tiles ontdubbelen (ook gespiegeld)
    tiles, lookup, maps = [], {}, []
    for img in keys:
        tm = []
        for t in tiles_of(img):
            if t not in lookup:
                a = np.array(t).reshape(8, 8)
                n = len(tiles) + 1
                tiles.append(t)
                lookup[t] = n
                for flip, arr in ((1 << 10, a[:, ::-1]), (2 << 10, a[::-1, :]), (3 << 10, a[::-1, ::-1])):
                    lookup.setdefault(tuple(arr.flatten()), n | flip)
            tm.append(lookup[t] | (15 << 12))
        maps.append(tm)
    return keys, tiles, maps


def save(tiles, maps):
    allt = [(0,) * 64] + tiles
    cols = 16
    rows = (len(allt) + cols - 1) // cols
    img = Image.new('P', (cols * 8, rows * 8))
    for i, t in enumerate(allt):
        ox, oy = (i % cols) * 8, (i // cols) * 8
        for p, v in enumerate(t):
            img.putpixel((ox + p % 8, oy + p // 8), int(v))
    img.putpalette([v for c in PAL for v in gba(c)] + [0] * (768 - 48))
    img.save(OUT + 'route_neo_plasma.png')
    with open(OUT + 'route_neo_plasma.pal', 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n32\n')
        for pal in (PAL, PAL_FLASH):
            for c in pal:
                fp.write('%d %d %d\n' % gba(c))
    with open(OUT + 'route_neo_plasma.bin', 'wb') as fp:
        for tm in maps:
            fp.write(struct.pack('<600H', *tm))
    print('neo_plasma:', len(allt), 'tiles,', len(maps), 'tilemaps')


def preview(keys, d):
    pal = [gba(c) for c in PAL]
    for i, k in enumerate(keys):
        im = Image.fromarray(np.array([[pal[v] for v in row] for row in k], np.uint8))
        im.resize((W * 2, H * 2), Image.NEAREST).save(os.path.join(d, 'np_key%02d.png' % i))


if __name__ == '__main__':
    keys, tiles, maps = build()
    save(tiles, maps)
    seen = set()
    for i, m in enumerate(maps):
        new = set(x & 0x3FF for x in m) - seen
        seen |= new
        print('  tilemap %d: %d nieuwe tiles' % (i, len(new)))
    if len(sys.argv) > 1:
        preview(keys, sys.argv[1])
