"""layerlib: sprites opbouwen uit lagen van eenvoudige vormen (Pokémon-stijl:
grote egale vlakken, 1 px omlijning, selout linksboven, licht van linksboven).

Gebruik (zie docs/concept/sprites/nachtaap/ronde2/bron/build.py):
    C = Canvas()
    C.layer(ellipse(30, 24, 15, 12), 'vacht', light=(30, 24, 15, 12))
    ...
    idx = C.render(RAMPS)          # 64x64 indexarray
    C.px(x, y, i) / C.stamp(x, y, rows, key)   # handwerk erna

Een laag die later komt, ligt ervoor. De rand van een laag krijgt een lijn:
tegen transparant zwart (index 15) aan de onder-/rechterkant en de donkerste tint
van het eigen onderdeel aan de boven-/linkerkant (selout); tegen een laag erachter
de donkerste tint van het eigen onderdeel.
RAMPS = {'onderdeel': [hooglicht, basis, schaduw, selout]} (indexen).
"""
import numpy as np
from PIL import Image, ImageDraw

W = H = 64
YY, XX = np.mgrid[0:H, 0:W] + 0.5


def ellipse(cx, cy, rx, ry):
    return ((XX - cx) / rx) ** 2 + ((YY - cy) / ry) ** 2 <= 1.0


def rect(x0, y0, x1, y1):
    return (XX >= x0) & (XX < x1) & (YY >= y0) & (YY < y1)


def polygon(pts):
    im = Image.new('L', (W, H), 0)
    ImageDraw.Draw(im).polygon([(x, y) for x, y in pts], fill=1)
    return np.array(im).astype(bool)


def _seg_dist(px, py, a, b):
    ax, ay = a; bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy or 1e-9
    t = np.clip(((px - ax) * dx + (py - ay) * dy) / L2, 0, 1)
    return np.hypot(px - (ax + t * dx), py - (ay + t * dy))


def stroke(pts, r):
    """Pixels binnen afstand r van de polylijn pts."""
    d = np.full((H, W), 1e9)
    for a, b in zip(pts, pts[1:]):
        d = np.minimum(d, _seg_dist(XX, YY, a, b))
    return d <= r


def stroke_var(pts, radii):
    """Polylijn met een straal per punt (lineair tussen de punten)."""
    m = np.zeros((H, W), bool)
    for (a, b), ra, rb in zip(zip(pts, pts[1:]), radii, radii[1:]):
        ax, ay = a; bx, by = b
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy or 1e-9
        t = np.clip(((XX - ax) * dx + (YY - ay) * dy) / L2, 0, 1)
        d = np.hypot(XX - (ax + t * dx), YY - (ay + t * dy))
        m |= d <= ra + (rb - ra) * t
    return m


def bezier(p0, p1, p2, n=24):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2 = map(np.array, (p0, p1, p2))
    return [tuple(v) for v in (1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t * t * p2]


def spiral(cx, cy, r0, r1, a0, a1, n=200):
    """Archimedische spiraal van straal r0 (hoek a0, graden) naar r1 (hoek a1)."""
    a = np.radians(np.linspace(a0, a1, n)); r = np.linspace(r0, r1, n)
    return [(cx + rr * np.cos(aa), cy + rr * np.sin(aa)) for rr, aa in zip(r, a)]


class Canvas:
    def __init__(self):
        self.layers = []          # (mask, part, light, edgeparts)
        self.idx = None

    def layer(self, mask, part, light=None, shade=None, flat=False, inner=None):
        """light = (cx, cy, rx, ry) van de bolling die belicht wordt.
        shade = (hl, sh): drempels voor hooglicht/schaduw (standaard 0.55/-0.15).
        flat = alleen basistint (kleine vormen).
        inner = optioneel masker van de vulling; de rest van mask wordt lijn
        (voor dunne vormen die over zichzelf lopen, zoals een spiraalstaart)."""
        self.layers.append(dict(mask=mask.copy(), part=part, light=light,
                                shade=shade or (0.55, -0.15), flat=flat,
                                inner=None if inner is None else inner & mask))

    def render(self, ramps, lx=-0.55, ly=-0.85):
        zbuf = np.full((H, W), -1)
        part = np.full((H, W), '', object)
        shadev = np.zeros((H, W))
        for z, L in enumerate(self.layers):
            m = L['mask']
            zbuf[m] = z; part[m] = L['part']
            if L['light'] is not None:
                cx, cy, rx, ry = L['light']
                u = (XX - cx) / rx; v = (YY - cy) / ry
                s = u * lx + v * ly
                r2 = u * u + v * v
                shadev[m] = (s - 0.25 * np.clip(r2 - 0.6, 0, 1))[m]
        self.z = zbuf; self.part = part
        idx = np.zeros((H, W), np.uint8)
        for z, L in enumerate(self.layers):
            m = zbuf == z
            hl, base, sh, so = ramps[L['part']]
            if L['flat'] or L['light'] is None:
                idx[m] = base
            else:
                thl, tsh = L['shade']
                v = shadev
                idx[m & (v >= thl)] = hl
                idx[m & (v < thl) & (v >= tsh)] = base
                idx[m & (v < tsh)] = sh
        # lijnen
        p = np.pad(zbuf, 1, constant_values=-1)
        nb = {(dx, dy): p[1 + dy:H + 1 + dy, 1 + dx:W + 1 + dx] for dx, dy in
              [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]}
        for y in range(H):
            for x in range(W):
                z = zbuf[y, x]
                if z < 0: continue
                so = ramps[part[y, x]][3]
                out = [(dx, dy) for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                       if nb[(dx, dy)][y, x] < 0]
                behind = [(dx, dy) for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                          if 0 <= nb[(dx, dy)][y, x] < z]
                if out:
                    # richting naar buiten: boven/links = selout, anders zwart
                    ox = sum(d[0] for d in out); oy = sum(d[1] for d in out)
                    lit = oy < 0 or (ox < 0 and oy <= 0)
                    idx[y, x] = so if lit else 15
                elif behind:
                    idx[y, x] = so
        # lagen met een expliciete vulling: alles buiten de vulling is lijn
        for z, L in enumerate(self.layers):
            if L['inner'] is None: continue
            m = (zbuf == z) & ~L['inner']
            so = ramps[L['part']][3]
            fill = L['inner']; pf = np.pad(fill, 1)
            for y, x in zip(*np.nonzero(m)):
                # lijn aan de boven-/linkerkant van de vulling = selout
                below = pf[y + 2, x + 1]; right = pf[y + 1, x + 2]
                above = pf[y, x + 1]; left = pf[y + 1, x]
                idx[y, x] = so if (below or right) and not (above or left) else 15
        self.idx = idx
        return idx

    def px(self, x, y, i):
        self.idx[y, x] = i

    def stamp(self, x0, y0, rows, key):
        """rows: lijst strings; key: teken -> index ('.' of ' ' = laten)."""
        for dy, row in enumerate(rows):
            for dx, ch in enumerate(row):
                if ch in key:
                    self.idx[y0 + dy, x0 + dx] = key[ch]


def save_indexed(path, frames, pal):
    a = np.vstack(frames).astype(np.uint8)
    im = Image.fromarray(a, 'P')
    flat = [v for c in pal for v in c] + [0] * (768 - 3 * len(pal))
    im.putpalette(flat)
    im.info['transparency'] = 0
    im.save(path, transparency=0)


def write_pal(path, pal):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n')
        for c in pal:
            f.write('%d %d %d\n' % c)


def gba(c):
    return tuple(round(v / 255 * 31) * 255 // 31 for v in c)


def hexc(h):
    h = h.lstrip('#'); return gba(tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)))


def preview(idx_frames, pal, z=6, bg=(250, 249, 244)):
    ims = []
    for a in idx_frames:
        rgb = np.zeros(a.shape + (3,), np.uint8); rgb[:] = bg
        for k in range(1, 16):
            rgb[a == k] = pal[k]
        ims.append(Image.fromarray(rgb).resize((a.shape[1] * z, a.shape[0] * z), Image.NEAREST))
    out = Image.new('RGB', (sum(i.width for i in ims) + 8 * (len(ims) - 1), ims[0].height), (200, 200, 200))
    x = 0
    for i in ims:
        out.paste(i, (x, 0)); x += i.width + 8
    return out
