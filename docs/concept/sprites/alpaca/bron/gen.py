"""Alpaca (Fighting-starter fase 1): procedurele basis + handmatige details.

Onderdelen worden als maskers getekend (achter -> voor), per onderdeel belicht
(licht linksboven, bolle normaal + wolbultjes), daarna omlijning met selout.
"""
import sys, os, math
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../../tools/concept/sprites'))
import ramp as R

OUT = os.path.dirname(os.path.abspath(__file__))
G = R.gba
PAL = [R.TRANSPARENT,
       G((255, 250, 222)), G((246, 226, 174)), G((206, 176, 126)), G((132, 100, 98)),   # 1-4 wol
       G((250, 196, 136)), G((206, 134, 80)), G((128, 70, 56)),                         # 5-7 vacht (gezicht/poten)
       G((255, 120, 160)), G((222, 52, 110)), G((140, 36, 82)),                         # 8-10 kwastjes
       G((170, 92, 52)), G((84, 40, 30)),                                               # 11-12 oog (iris)
       G((214, 90, 110)),                                                               # 13 mond binnenkant
       (255, 255, 255),                                                                 # 14 wit (glans)
       (16, 16, 16)]                                                                    # 15 omlijning
RAMPS = {'wol': [1, 2, 3, 4], 'vacht': [5, 6, 7], 'kwast': [8, 9, 10]}
LX, LY, LZ = -0.62, -0.72, 0.85
_n = math.sqrt(LX * LX + LY * LY + LZ * LZ); LX, LY, LZ = LX / _n, LY / _n, LZ / _n
W = H = 64


class Canvas:
    def __init__(s):
        s.part = np.zeros((H, W), int)      # part-id (0 = leeg)
        s.shade = np.zeros((H, W))          # belichting -1..1
        s.ramp = {}                         # part-id -> rampnaam
        s.dark = {}                         # part-id -> extra donkerte (verre ledematen)
        s.n = 0

    def new(s, rampname, dark=0.0):
        s.n += 1; s.ramp[s.n] = rampname; s.dark[s.n] = dark
        return s.n


def ell(cx, cy, rx, ry):
    yy, xx = np.mgrid[0:H, 0:W]
    u = (xx + 0.5 - cx) / rx; v = (yy + 0.5 - cy) / ry
    d = u * u + v * v
    return d <= 1.0, u, v, d


def normal_light(u, v):
    d = np.clip(u * u + v * v, 0, 1)
    z = np.sqrt(1 - d)
    return u * LX + v * LY + z * LZ


def put(c, pid, mask, light):
    c.part[mask] = pid
    c.shade[mask] = light[mask] - c.dark[pid]


def blob(c, pid, cx, cy, rx, ry):
    m, u, v, _ = ell(cx, cy, rx, ry)
    put(c, pid, m, normal_light(u, v))


def wool(c, pid, cx, cy, rx, ry, bump=2.6, step=3.6, seed=0, skip=(), lw=0.55):
    """Wolwolk: ellips + rand van bultjes; elke bult eigen glans, gemengd met de grote vorm."""
    m0, u0, v0, _ = ell(cx, cy, rx - bump * 0.6, ry - bump * 0.6)
    glob = normal_light(np.clip(u0 * (rx - bump * .6) / rx, -1, 1), np.clip(v0 * (ry - bump * .6) / ry, -1, 1))
    mask = m0.copy(); light = glob.copy()
    per = math.pi * (rx + ry)
    k = max(6, int(per / step))
    bumps = []
    for i in range(k):
        a = 2 * math.pi * (i + 0.5 * (seed % 2)) / k + seed * 0.37
        if any(lo <= (math.degrees(a) % 360) <= hi for lo, hi in skip):
            continue
        bx = cx + (rx - bump * 0.45) * math.cos(a); by = cy + (ry - bump * 0.45) * math.sin(a)
        bumps.append((bx, by))
    # glob op de hele uitgebreide vorm
    yy, xx = np.mgrid[0:H, 0:W]
    U = (xx + 0.5 - cx) / rx; V = (yy + 0.5 - cy) / ry
    globl = normal_light(np.clip(U, -1, 1), np.clip(V, -1, 1))
    loc = np.full((H, W), -9.0)
    for bx, by in bumps:
        mb, ub, vb, db = ell(bx, by, bump, bump)
        nl = normal_light(ub, vb)
        mask |= mb
        loc = np.where(mb & (nl > loc), nl, loc)
    loc = np.where(loc < -5, globl, loc)
    light = globl * (1 - lw) + loc * lw
    put(c, pid, mask, light)
    return mask


def wool2(c, pid, core, bumps, lw=0.6, gscale=1.0):
    """Wolwolk uit een kern-ellips + schijfjes op gehele pixelposities (nette bogen).
    Elke pixel hoort bij het dichtstbijzijnde schijfje (genormaliseerd): eigen glans per krul."""
    cx, cy, rx, ry = core
    yy, xx = np.mgrid[0:H, 0:W]
    m, _, _, _ = ell(cx, cy, rx, ry)
    allx = [b[0] for b in bumps] + [cx - rx, cx + rx]; ally = [b[1] for b in bumps] + [cy - ry, cy + ry]
    gx0, gx1, gy0, gy1 = min(b[0] - b[2] for b in bumps), max(b[0] + b[2] for b in bumps), min(b[1] - b[2] for b in bumps), max(b[1] + b[2] for b in bumps)
    gcx, gcy = (gx0 + gx1) / 2 + 0.5, (gy0 + gy1) / 2 + 0.5
    grx, gry = (gx1 - gx0) / 2 * gscale + 0.5, (gy1 - gy0) / 2 * gscale + 0.5
    globl = normal_light(np.clip((xx + .5 - gcx) / grx, -1, 1), np.clip((yy + .5 - gcy) / gry, -1, 1))
    best = np.full((H, W), 9.0); loc = globl.copy()
    for bx, by, r in bumps:
        dx = xx - bx; dy = yy - by
        d = np.sqrt(dx * dx + dy * dy) / r
        inb = (dx * dx + dy * dy) <= r * r
        m |= inb
        sel = inb & (d < best)
        best = np.where(sel, d, best)
        nl = normal_light(np.clip(dx / (r + .5), -1, 1), np.clip(dy / (r + .5), -1, 1))
        loc = np.where(sel, nl, loc)
    light = globl * (1 - lw) + loc * lw
    put(c, pid, m, light)
    return m


def poly(c, pid, pts, width):
    """Dikke lijn (ledemaat/oor) langs punten, rond belicht dwars op de lijn."""
    yy, xx = np.mgrid[0:H, 0:W]
    best = np.full((H, W), 1e9); bu = np.zeros((H, W)); bv = np.zeros((H, W))
    for (x0, y0), (x1, y1), w0, w1 in zip(pts[:-1], pts[1:], width[:-1], width[1:]):
        dx, dy = x1 - x0, y1 - y0; L2 = dx * dx + dy * dy
        t = np.clip(((xx + .5 - x0) * dx + (yy + .5 - y0) * dy) / L2, 0, 1)
        px = x0 + t * dx; py = y0 + t * dy
        w = w0 + (w1 - w0) * t
        ex = (xx + .5 - px) / w; ey = (yy + .5 - py) / w
        d = np.sqrt(ex * ex + ey * ey)
        sel = d < best
        best = np.where(sel, d, best); bu = np.where(sel, ex, bu); bv = np.where(sel, ey, bv)
    m = best <= 1.0
    put(c, pid, m, normal_light(bu * 0.9, bv * 0.9 - 0.15))


def quantize(c, cuts):
    """Belichting -> rampindex per onderdeel (percentielen per rampnaam over het hele frame)."""
    out = np.zeros((H, W), int)
    for name, idx in RAMPS.items():
        pids = [p for p, r in c.ramp.items() if r == name]
        m = np.isin(c.part, pids)
        if not m.any():
            continue
        vals = c.shade[m]
        qs = cuts[name]                      # aandeel per tint, licht -> donker
        th = np.percentile(vals, [100 * (1 - sum(qs[:i + 1])) for i in range(len(qs) - 1)])
        t = np.zeros(vals.shape, int)
        for i, tv in enumerate(th):
            t += vals < tv
        out[m] = np.array(idx)[t]
    return out


CUTS = {'wol': [0.08, 0.50, 0.27, 0.15], 'vacht': [0.18, 0.52, 0.30], 'kwast': [0.25, 0.45, 0.30]}


def outline(c, img, lineparts=None):
    """1px buitenlijn: boven/links donkerste rampkleur van het buurvlak, rechts/onder zwart.
    Binnenlijnen: waar een onderdeel tegen een *ander rampsoort* onderdeel erachter ligt."""
    opq = c.part > 0
    out = img.copy()
    for y in range(H):
        for x in range(W):
            if opq[y, x]:
                continue
            ox = oy = 0; nb = []
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if (dx or dy) and 0 <= yy < H and 0 <= xx < W and opq[yy, xx]:
                        ox -= dx; oy -= dy
                        if abs(dx) + abs(dy) == 1:
                            nb.append(c.part[yy, xx])
            if not nb:
                continue
            pid = max(set(nb), key=nb.count)
            rp = RAMPS.get(c.ramp[pid])
            if ox + oy < 0 and rp:
                out[y, x] = rp[-1]
            else:
                out[y, x] = 15
    return out


def inner_lines(c, img, pairs):
    """pairs: (voor-pid, achter-pid, kleur of None=donkerste van achter). Lijn op de achterpixels."""
    out = img.copy()
    for front, back, col in pairs:
        for y in range(1, H - 1):
            for x in range(1, W - 1):
                if c.part[y, x] != back:
                    continue
                if any(c.part[y + dy, x + dx] == front for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0))):
                    out[y, x] = col if col else RAMPS[c.ramp[back]][-1]
    return out


def build(f2=False, head=False):
    """Lijf, poten, nek en staart (de kop komt als stempel uit headgen)."""
    c = Canvas()
    P = {}
    by = 0 if not f2 else -1
    # verre poten (achter het lijf)
    P['hf'] = c.new('vacht', 0.3); poly(c, P['hf'], [(44.5, 46), (44.5, 52.2)], [2.1, 2.0])
    P['ff'] = c.new('vacht', 0.3); poly(c, P['ff'], [(31.5, 46), (31.5, 52.2)], [2.1, 2.0])
    # staartpluim
    P['tail'] = c.new('wol', 0.15)
    if not f2:
        wool2(c, P['tail'], (48.5, 36.5, 1.5, 1.5), [(48, 35, 2.3), (50, 37, 2.3), (48, 38, 2.3)], lw=0.35)
    else:
        wool2(c, P['tail'], (49, 33.5, 1.5, 1.5), [(49, 32, 2.3), (51, 34, 2.3), (49, 35, 2.3)], lw=0.35)
    # lijf
    P['body'] = c.new('wol')
    B = [(27, 36), (30, 33), (35, 32), (40, 32), (45, 34), (48, 38), (48, 43), (46, 47), (41, 48), (35, 48), (29, 47), (25, 44), (25, 40)]
    wool2(c, P['body'], (36, 41.5 + by, 9, 6.5), [(round(36 + (x - 36.5) * 0.84), round(41.5 + (y - 41) * 0.9) + by, 3.2) for x, y in B], lw=0.35)
    # nabije poten
    P['hn'] = c.new('vacht'); poly(c, P['hn'], [(40.5, 47), (40.5, 53.2)], [2.3, 2.2])
    P['fn'] = c.new('vacht')
    if not f2:
        poly(c, P['fn'], [(27, 47), (27, 53.2)], [2.3, 2.2])
    else:   # voorpoot opgetild, knie naar voren (stampen/trappen)
        poly(c, P['fn'], [(27, 45.5), (23.5, 48.5), (23, 51.2)], [2.3, 2.2, 2.1])
    # nek (wol)
    P['neck'] = c.new('wol')
    ny = 0 if not f2 else -2
    NB = [(22, 29), (21, 33), (23, 37), (28, 39), (31, 34), (30, 30), (26, 27)]
    wool2(c, P['neck'], (26.5, 33.5 + ny, 5.5, 6.0), [(x, y + ny, 2.3) for x, y in NB], lw=0.5)
    c.P = P
    return finish(c, P)


def hoof(c, P, img):
    """Onderste 2 rijen van elke poot: hoefje (donkerste vachttint), met een lichtpixel links."""
    for k in ('hf', 'ff', 'hn', 'fn'):
        m = c.part == P[k]
        ys, xs = np.nonzero(m)
        if len(ys) == 0:
            continue
        yb = ys.max()
        for y in (yb - 1, yb):
            row = np.nonzero(m[y])[0]
            img[y, row] = 7
            if y == yb - 1 and len(row) > 2:
                img[y, row[0]] = 6


def finish(c, P):
    img = quantize(c, CUTS)
    img[c.part == 0] = 0
    hoof(c, P, img)
    g = lambda k: P.get(k, -1)
    img = inner_lines(c, img, [
        (g('face'), g('neck'), None), (g('snout'), g('neck'), None),
        (g('knot'), g('face'), None), (g('ear_n'), g('knot'), None), (g('ear_n'), g('face'), None),
        (g('tas_n'), g('ear_n'), None), (g('tas_f'), g('ear_f'), None), (g('tas_n'), g('face'), None),
        (g('neck'), g('body'), None), (g('body'), g('tail'), None),
        (g('body'), g('hf'), 15), (g('body'), g('ff'), 15), (g('body'), g('fn'), None), (g('body'), g('hn'), None),
        (g('knot'), g('ear_f'), None), (g('face'), g('ear_f'), None), (g('neck'), g('ff'), 15),
        (g('fn'), g('ff'), 15), (g('neck'), g('fn'), None),
    ])
    img = outline(c, img)
    return c, P, img


def save(frames, name='anim_front.png'):
    a = np.vstack(frames).astype(np.uint8)
    im = Image.fromarray(a, 'P')
    flat = []
    for col in PAL:
        flat += list(col)
    im.putpalette(flat)
    im.save(os.path.join(OUT, name), transparency=0)
    R.write_pal(os.path.join(OUT, 'normal.pal'), PAL)


def dump(img, path):
    ch = '.123456789ABCDEF'
    b = np.nonzero(img)
    y0, y1, x0, x1 = 0, 63, 0, 63
    with open(path, 'w') as f:
        f.write('    ' + ''.join(str(x % 10) for x in range(64)) + '\n')
        for y in range(64):
            f.write('%2d  ' % y + ''.join(ch[v] for v in img[y]) + '\n')


if __name__ == '__main__':
    import stamp
    _, _, f1 = build(False)
    _, _, f2 = build(True)
    f1 = stamp.apply(f1, os.path.join(OUT, 'head1.txt'), 8, 8)
    if os.path.exists(os.path.join(OUT, 'head2.txt')):
        f2 = stamp.apply(f2, os.path.join(OUT, 'head2.txt'), 7, 6)
    else:
        f2 = stamp.apply(f2, os.path.join(OUT, 'head1.txt'), 7, 6)
    np.save(os.path.join(OUT, 'base1.npy'), f1); np.save(os.path.join(OUT, 'base2.npy'), f2)
    dump(f1, os.path.join(OUT, 'base1.txt')); dump(f2, os.path.join(OUT, 'base2.txt'))
    save([f1, f2], 'base_front.png')
