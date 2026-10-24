"""Spritegenerator: 3D-poppetje -> Gen 3-sprite (64x64) volgens de Dragonfly Cave-regels (docs/lessen/SPRITING.md).
Elke beslissing valt per vlak of per curve op hoge resolutie (8x) en wordt pas daarna op het pixelraster bemonsterd;
zo ontstaan vloeiende omtrekken en schone schaduwgrenzen in plaats van korrelige pixelkeuzes.
Stappen: 1 render 8x, 2 silhouet (afgevlakt, bemonsterd, 'pixel-perfect' hoeken), 3 delen/materialen,
4 tonen per vlak (licht/basis/schaduw), 5 omlijning (zwart aan de schaduwkant, kleurlijn aan de lichte kant,
schaduwtint als lijn-hooglicht), 6 binnenlijnen alleen waar een deel vóór een ander ligt, 7 sjablonen (ogen),
8 handlaag, 9 controles."""
import math
import numpy as np
from PIL import Image
from model3d import camera, bbox, render

SS = 8          # supersampling
N = 64


def box(a, k):
    """Gemiddelde over een k x k venster (gecentreerd), randen met nul."""
    a = a.astype(np.float32)
    c = np.cumsum(np.cumsum(np.pad(a, ((k, k), (k, k))), 0), 1)
    h = k // 2
    H, W = a.shape
    y0, y1 = np.arange(H) + k - h - 1, np.arange(H) + k + (k - h) - 1
    x0, x1 = np.arange(W) + k - h - 1, np.arange(W) + k + (k - h) - 1
    s = c[y1][:, x1] - c[y0][:, x1] - c[y1][:, x0] + c[y0][:, x0]
    return s / (k * k)


def noise(shape, scale, seed):
    """Laagfrequente ruis (-1..1) voor 'minder geometrisch': grilliger omtrek en gekartelde schaduwgrenzen."""
    rng = np.random.default_rng(seed)
    h, w = shape
    gh, gw = max(2, int(h / scale) + 2), max(2, int(w / scale) + 2)
    g = rng.uniform(-1, 1, (gh, gw))
    ys = np.linspace(0, gh - 1.001, h); xs = np.linspace(0, gw - 1.001, w)
    y0 = ys.astype(int); x0 = xs.astype(int); fy = (ys - y0)[:, None]; fx = (xs - x0)[None, :]
    a = g[y0][:, x0]; b = g[y0][:, x0 + 1]; c = g[y0 + 1][:, x0]; d = g[y0 + 1][:, x0 + 1]
    return a * (1 - fy) * (1 - fx) + b * (1 - fy) * fx + c * fy * (1 - fx) + d * fy * fx


def smooth(a, k=SS):
    return box(box(a, k), k)      # tentfilter: ±1 spritepixel


def centers(a):
    return a[SS // 2::SS, SS // 2::SS]


def generate(model, spec):
    Rc = camera(spec['yaw'], spec['pitch'], spec.get('stretch_x', 1.0))
    x0, x1, y0, y1 = bbox(model, Rc)
    sc = []
    if 'height' in spec: sc.append(spec['height'] / (y1 - y0))
    if 'width' in spec: sc.append(spec['width'] / (x1 - x0))
    scale = min(sc)
    w = (x1 - x0) * scale
    left = (N - w) / 2 + spec.get('dx', 0)
    top = N - spec.get('bottom', 3) - (y1 - y0) * scale
    origin = (x0 - left / scale, y1 + top / scale)
    R = render(model, Rc, N * SS, scale * SS, origin)
    for mname, px in spec.get('thicken', {}).items():     # dunne delen minstens zo dik (in spritepixels)
        if mname not in R['mats']:
            continue
        i = R['mats'].index(mname)
        sel = R['mat'] == i
        k = int(px * SS) | 1
        grow = box(sel, k) > 0
        add = grow & ~sel
        # alleen uitbreiden over achtergrond of over verder weg gelegen delen
        R['mat'][add] = i
        R['part'][add] = R['part'][sel][0] if sel.any() else -1
        R['z'][add] = R['z'][sel].max()
    fig = R['mat'] >= 0

    # 2. silhouet: afgevlakte dekking, bemonsterd op pixelmiddens
    cov = smooth(fig)
    rough = spec.get('rough_edge', 0.0)       # 0 = glad, 0.1-0.25 = losser, handgetekend
    if rough:
        cov = cov + rough * noise(cov.shape, SS * 2.5, spec.get('seed', 1))
    mask = centers(cov) > 0.5
    mask = clean_mask(mask)

    # 3. delen en materialen: grootste afgevlakte dekking per pixel
    def label_map(lab, names):
        best = np.full((N, N), -1); bv = np.zeros((N, N))
        for i in range(len(names)):
            v = centers(smooth(lab == i))
            upd = v > bv
            best[upd] = i; bv[upd] = v[upd]
        best[~mask] = -1
        return best
    part = label_map(R['part'], R['parts'])
    mat = label_map(R['mat'], R['mats'])
    for pin in spec.get('pin', []):   # kleine materialen (neus, klauw) winnen bij een minimale dekking
        if pin in R['mats']:
            i = R['mats'].index(pin)
            v = centers(smooth(R['mat'] == i))
            mat[(v > spec.get('pin_cov', 0.3)) & mask] = i

    # 4. tonen: afgevlakt licht per pixel
    L = np.array(spec.get('light', (-0.6, 0.7, 0.35)), float); L /= np.linalg.norm(L)
    lv = R['n'] @ L
    lit = centers(smooth(np.where(fig, lv, 0))) / np.maximum(centers(smooth(fig)), 1e-6)
    zc = centers(smooth(np.where(fig, R['z'], 0))) / np.maximum(centers(smooth(fig)), 1e-6)
    # toonverdeling als aandelen van de figuur (R/S-stijl: veel hooglicht, een stevige schaduwkant)
    f_hi, f_sh = spec.get('tones', (0.30, 0.35))
    fur = spec.get('rough_shade', 0.0)       # gekartelde schaduwgrens (vacht)
    if fur:
        lit = lit + fur * centers(noise((N * SS, N * SS), SS * 1.5, spec.get('seed', 1) + 7))
    vals = lit[mask]
    t_hi, t_sh = np.quantile(vals, 1 - f_hi), np.quantile(vals, f_sh)
    tone = np.where(lit > t_hi, 0, np.where(lit > t_sh, 1, 2))
    for pname in spec.get('far', []):       # verre delen: één toon donkerder
        if pname in R['parts']:
            sel = part == R['parts'].index(pname)
            tone[sel] = np.minimum(tone[sel] + 1, 2)

    # 5/6. lijnen
    sl = np.array((-0.6, -0.8))     # licht in schermcoördinaten (x rechts, y omlaag): van linksboven
    g = np.zeros((N, N, 2))
    gy, gx = np.gradient(smooth(fig, SS * 2))
    g[..., 0] = -centers(gx); g[..., 1] = -centers(gy)     # naar buiten gerichte normaal
    out = np.full((N, N), '', dtype=object)
    pal = spec['palette']
    mats = R['mats']
    for y in range(N):
        for x in range(N):
            if not mask[y, x]:
                continue
            m = mats[mat[y, x]]
            out[y, x] = f'{m}{"hbs"[tone[y, x]]}'
    def line_color(y, x, nvec):
        m = mats[mat[y, x]]
        nv = nvec / (np.linalg.norm(nvec) + 1e-9)
        f = nv @ (-sl)  # >0: naar het licht
        if f > spec.get('line_hi', 0.75):
            return f'{m}s'          # schaduwtint als lijn-hooglicht
        if f > spec.get('line_mid', -0.15):
            return f'{m}l'          # omlijningsbasis
        return 'K'
    nb4 = ((0, 1), (1, 0), (0, -1), (-1, 0))
    for y in range(N):
        for x in range(N):
            if not mask[y, x]:
                continue
            edge = any(not (0 <= y + dy < N and 0 <= x + dx < N) or not mask[y + dy, x + dx] for dy, dx in nb4)
            if edge:
                out[y, x] = line_color(y, x, g[y, x])
                continue
            # binnenlijn: dit deel ligt duidelijk vóór het buurdeel
            limbs = spec.get('lined_parts', ())
            for dy, dx in nb4:
                yy, xx = y + dy, x + dx
                if part[yy, xx] == part[y, x]:
                    continue
                pa, pb = R['parts'][part[y, x]], R['parts'][part[yy, xx]]
                front = zc[y, x] > zc[yy, xx] + spec.get('dz', 4)
                if not front and (pa in limbs or pb in limbs):
                    front = zc[y, x] > zc[yy, xx]
                # niet naast een silhouetlijn (anders wordt de omlijning 2 px dik)
                side = [(y + ddy, x + ddx) for ddy, ddx in nb4 if (ddy, ddx) != (dy, dx)]
                if front:
                    out[y, x] = line_color(y, x, np.array((-dx, -dy), float))
                    break
            # gemarkeerde materialen krijgen een lijn op hun grens
            else:
                if mats[mat[y, x]] in spec.get('lined', ()):
                    for dy, dx in nb4:
                        if mat[y + dy, x + dx] != mat[y, x] and mats[mat[y + dy, x + dx]] not in spec.get('lined', ()):
                            pass
    # korte losse binnenlijnen (< min_line px) weghalen: die lezen als scheurtjes
    isline = np.zeros((N, N), bool)
    for y in range(N):
        for x in range(N):
            if out[y, x] and (out[y, x] == 'K' or out[y, x].endswith('l')):
                inner = all(0 <= y + dy < N and 0 <= x + dx < N and mask[y + dy, x + dx] for dy, dx in nb4)
                isline[y, x] = inner
    seen = np.zeros((N, N), bool)
    for y in range(N):
        for x in range(N):
            if isline[y, x] and not seen[y, x]:
                comp, st = [], [(y, x)]
                seen[y, x] = True
                touches_edge = False
                while st:
                    cy, cx = st.pop(); comp.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            yy, xx = cy + dy, cx + dx
                            if 0 <= yy < N and 0 <= xx < N:
                                if isline[yy, xx] and not seen[yy, xx]:
                                    seen[yy, xx] = True; st.append((yy, xx))
                                elif out[yy, xx] and not isline[yy, xx] and (out[yy, xx] == 'K' or out[yy, xx].endswith('l')):
                                    touches_edge = True
                if len(comp) < spec.get('min_line', 3) and not touches_edge or len(comp) < 2:
                    for cy, cx in comp:
                        mname = mats[mat[cy, cx]]
                        out[cy, cx] = f'{mname}{"hbs"[tone[cy, cx]]}'
    # 7. sjablonen
    for t in spec.get('templates', []):
        name, tmpl, colors = t[:3]
        anchor = t[3] if len(t) > 3 else None      # (kolom, rij) in het sjabloon die op het punt valt
        if name not in model.points:
            continue
        p = Rc @ np.array(model.points[name], float)
        px = (p[0] - origin[0]) * scale
        py = (origin[1] - p[1]) * scale
        hh, ww = len(tmpl), len(tmpl[0])
        ax, ay = anchor if anchor else (ww / 2, hh / 2)
        X0, Y0 = int(round(px - ax)), int(round(py - ay))
        zi = R['z'][min(N * SS - 1, int(py * SS)), min(N * SS - 1, int(px * SS))]
        if t[4:5] != ('always',) and zi > p[2] + spec.get('occl', 3):
            continue              # verborgen achter iets anders
        for j, row in enumerate(tmpl):
            for i, ch in enumerate(row):
                if ch != '.' and 0 <= Y0 + j < N and 0 <= X0 + i < N:
                    out[Y0 + j, X0 + i] = colors[ch]
    # 8. handlaag
    for y, x, keys in spec.get('hand', []):
        for i, k in enumerate(keys):
            if k:
                out[y, x + i] = k
    return out, dict(mask=mask, mat=mat, part=part, tone=tone, scale=scale, origin=origin, R=R)


def clean_mask(m):
    m = m.copy()
    for _ in range(2):
        n4 = np.zeros(m.shape, int)
        for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            n4 += np.roll(np.roll(m, dy, 0), dx, 1)
        m &= ~(m & (n4 <= 1))        # losse uitsteeksels
        m |= (~m & (n4 >= 3))        # gaatjes van 1 px
    # 'pixel-perfect': een uitwendige hoek op een trap (L-vorm) weghalen
    H, W = m.shape
    res = m.copy()
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if not m[y, x]:
                continue
            u, d, l, r = m[y - 1, x], m[y + 1, x], m[y, x - 1], m[y, x + 1]
            if u + d + l + r != 2 or (u and d) or (l and r):
                continue
            dy = -1 if u else 1
            dx = -1 if l else 1
            if m[y + dy, x + dx] and not m[y - dy, x - dx]:
                res[y, x] = False
    return res


def to_image(grid, palette):
    keys = sorted({k for k in grid.ravel() if k})
    rgb = np.zeros((N, N, 4), np.uint8)
    for k in keys:
        col = palette[k]
        sel = grid == k
        rgb[sel, :3] = col
        rgb[sel, 3] = 255
    return Image.fromarray(rgb, 'RGBA'), keys


def check(grid, palette=None):
    fig = grid != ''
    rep = {}
    rep['pixels'] = int(fig.sum())
    keys = {k for k in grid.ravel() if k}
    rep['kleuren'] = len({tuple(palette[k]) for k in keys}) if palette else len(keys)
    seen = np.zeros(fig.shape, bool); st = [(0, 0)]
    while st:
        y, x = st.pop()
        if 0 <= y < N and 0 <= x < N and not seen[y, x] and not fig[y, x]:
            seen[y, x] = True; st += [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
    rep['gaatjes'] = [(x, y) for y in range(N) for x in range(N) if not fig[y, x] and not seen[y, x]]
    return rep
