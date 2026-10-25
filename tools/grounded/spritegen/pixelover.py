"""Pixel-over-motor: 2D-tekening -> sprite, volgens de stappen van de Dragonfly Cave-gids
(docs/lessen/bronnen/dragonflycave_spriting_guide.txt, 'Pixel-Overs'):
 1. verkleinen tot spritemaat (de tekening blijft op hoge resolutie de bron voor elke beslissing);
 2. de omlijning overtrekken: silhouet + de lijnen van de tekening, 1 px, gladde trapjes, geen dubbele pixels;
    dunne delen (1-2 px) krijgen een pseudo-omlijning (alleen kleur);
 3. vullen met de schaduwkleur, dan de basislaag, dan hooglicht in ronde vlakken, dan glans;
 4. de omlijning inkleuren: zwart aan de schaduwkant, omlijningsbasis, schaduwtint rond hooglicht.
Invoer: RGB(A)-tekening + figuurmasker + lijnmasker + materiaallabels (uit een eigen tekening: exact;
uit een gescande tekening: geschat). Uitvoer: raster van kleursleutels + palet."""
import numpy as np
from PIL import Image

NB4 = ((0, 1), (1, 0), (0, -1), (-1, 0))
NB8 = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))


def boxmean(a, k):
    a = a.astype(np.float32)
    k = max(1, int(round(k)))
    c = np.cumsum(np.cumsum(np.pad(a, ((k, k), (k, k))), 0), 1)
    h = k // 2
    H, W = a.shape
    y0 = np.arange(H) + k - h - 1; y1 = y0 + k
    x0 = np.arange(W) + k - h - 1; x1 = x0 + k
    return (c[y1][:, x1] - c[y0][:, x1] - c[y1][:, x0] + c[y0][:, x0]) / (k * k)


def sample(a, f, w, h, ox=0.0, oy=0.0):
    """Waarde op de pixelmiddens van een w x h-raster dat met factor f over de tekening ligt."""
    ys = np.clip((oy + (np.arange(h) + 0.5) * f).astype(int), 0, a.shape[0] - 1)
    xs = np.clip((ox + (np.arange(w) + 0.5) * f).astype(int), 0, a.shape[1] - 1)
    return a[ys][:, xs]


def thin(m):
    """Zhang-Suen-verdunning tot 1-px-lijnen."""
    m = m.copy().astype(np.uint8)
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            P = np.pad(m, 1)
            p2, p3, p4, p5 = P[:-2, 1:-1], P[:-2, 2:], P[1:-1, 2:], P[2:, 2:]
            p6, p7, p8, p9 = P[2:, 1:-1], P[2:, :-2], P[1:-1, :-2], P[:-2, :-2]
            nbs = [p2, p3, p4, p5, p6, p7, p8, p9]
            B = sum(n.astype(int) for n in nbs)
            A = sum(((nbs[i] == 0) & (nbs[(i + 1) % 8] == 1)).astype(int) for i in range(8))
            if step == 0:
                c = (p2 * p4 * p6 == 0) & (p4 * p6 * p8 == 0)
            else:
                c = (p2 * p4 * p8 == 0) & (p2 * p6 * p8 == 0)
            rm = (m == 1) & (B >= 2) & (B <= 6) & (A == 1) & c
            if rm.any():
                m[rm] = 0; changed = True
    return m.astype(bool)


def prune(m, n):
    """Korte uitlopers (< n px) van een lijnennetwerk weghalen."""
    m = m.copy()
    for _ in range(n):
        P = np.pad(m, 1)
        cnt = sum(np.roll(np.roll(P, dy, 0), dx, 1)[1:-1, 1:-1].astype(int) for dy, dx in NB8)
        ends = m & (cnt <= 1)
        if not ends.any():
            break
        m &= ~ends
    return m


def l_corners(m, protect=None):
    """'Pixel-perfect': een lijnpixel die alleen een L vormt (buren recht boven/onder én links/rechts) weg."""
    m = m.copy()
    H, W = m.shape
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if not m[y, x] or (protect is not None and protect[y, x]):
                continue
            u, d, l, r = m[y - 1, x], m[y + 1, x], m[y, x - 1], m[y, x + 1]
            if (u or d) and (l or r) and (u + d + l + r) == 2:
                dy = -1 if u else 1; dx = -1 if l else 1
                diag_free = not m[y - dy, x - dx]
                if diag_free:
                    m[y, x] = False
    return m


def mask_corners(fig):
    """Uitwendige trap-hoeken van het silhouet weghalen (1 px per trede)."""
    res = fig.copy()
    H, W = fig.shape
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            if not fig[y, x]:
                continue
            u, d, l, r = fig[y - 1, x], fig[y + 1, x], fig[y, x - 1], fig[y, x + 1]
            if u + d + l + r != 2 or (u and d) or (l and r):
                continue
            dy = -1 if u else 1; dx = -1 if l else 1
            if fig[y + dy, x + dx] and not fig[y - dy, x - dx]:
                res[y, x] = False
    return res


def majority(lab, mask, it=1):
    """Ronde vlakken: losse pixels en rafels opnemen in de meerderheid van hun 8 buren (binnen het masker)."""
    lab = lab.copy()
    H, W = lab.shape
    for _ in range(it):
        new = lab.copy()
        for y in range(H):
            for x in range(W):
                if not mask[y, x]:
                    continue
                vals = [lab[y + dy, x + dx] for dy, dx in NB8 if 0 <= y + dy < H and 0 <= x + dx < W and mask[y + dy, x + dx]]
                if not vals:
                    continue
                v, c = np.unique(vals, return_counts=True)
                if c.max() >= 6 and v[c.argmax()] != lab[y, x]:
                    new[y, x] = v[c.argmax()]
        lab = new
    return lab


def pixelover(art, fig_hi, line_hi, mat_hi, tone_hi, w, h, spec):
    """art: HxWx3; fig_hi/line_hi: bool; mat_hi: int materiaal per pixel (-1 = geen); tone_hi: float helderheid 0..1.
    w, h: spritemaat van de figuur. spec: palet ('<mat><h|b|s|l>', 'K'), stijl."""
    st = dict(line_cov=0.42, hi_q=0.72, sh_q=0.38, line_hi=0.75, line_mid=-0.1, round_it=1)
    st.update(spec.get('style', {}))
    H, W = fig_hi.shape
    f = max(W / w, H / h)
    w, h = int(round(W / f)), int(round(H / f))
    # 1. silhouet: dekking per spritepixel
    cov = sample(boxmean(fig_hi, f), f, w, h)
    fig = mask_corners(cov > 0.5)
    # 2. lijnen van de tekening: lijn binnen een halve spritepixel van het midden
    near = boxmean(line_hi & fig_hi, f * 0.9) > 0
    lc = sample(boxmean(line_hi & fig_hi, f), f, w, h)
    linep = sample(near, f, w, h) & fig & (lc > st['line_cov'] * (1.0 / f) * 1.5)
    linep = thin(linep)
    linep = prune(linep, st.get('prune', 2))
    linep = l_corners(linep)
    # 3. materiaal en toon per pixel (lijnen in de tekening tellen niet mee)
    mats = sorted(set(np.unique(mat_hi)) - {-1})
    best = np.full((h, w), -1); bv = np.zeros((h, w))
    for mi in mats:
        v = sample(boxmean((mat_hi == mi) & ~line_hi, f), f, w, h)
        up = v > bv; best[up] = mi; bv[up] = v[up]
    tsum = sample(boxmean(np.where(~line_hi & fig_hi, tone_hi, 0), f), f, w, h)
    tcnt = sample(boxmean(~line_hi & fig_hi, f), f, w, h)
    tone = tsum / np.maximum(tcnt, 1e-6)
    # vullen met schaduwkleur -> basis -> hooglicht (aandelen per materiaal), dan ronde vlakken
    T = np.full((h, w), 2)
    for mi in mats:
        sel = fig & (best == mi)
        if sel.sum() < 3:
            continue
        q_hi, q_sh = np.quantile(tone[sel], st['hi_q']), np.quantile(tone[sel], st['sh_q'])
        T[sel & (tone > q_sh)] = 1
        T[sel & (tone > q_hi)] = 0
    T = majority(T, fig, st['round_it'])
    # 4. omlijning
    names = spec['materials']
    out = np.full((h, w), '', dtype=object)
    gy, gx = np.gradient(boxmean(fig_hi, f * 2))
    L2 = np.array((-0.6, -0.8))
    for y in range(h):
        for x in range(w):
            if not fig[y, x]:
                continue
            m = names[best[y, x]] if best[y, x] >= 0 else names[mats[0]]
            out[y, x] = m + 'hbs'[T[y, x]]
            edge = any(not (0 <= y + dy < h and 0 <= x + dx < w) or not fig[y + dy, x + dx] for dy, dx in NB4)
            if edge or linep[y, x]:
                if edge:
                    cy, cx = int((y + 0.5) * f), int((x + 0.5) * f)
                    n = -np.array((gx[min(H - 1, cy), min(W - 1, cx)], gy[min(H - 1, cy), min(W - 1, cx)]))
                else:
                    n = np.zeros(2)
                    for dy, dx in NB8:   # binnenlijn: kant naar het licht = kant met de lichtste buren
                        yy, xx = y + dy, x + dx
                        if 0 <= yy < h and 0 <= xx < w and fig[yy, xx] and not linep[yy, xx]:
                            n += np.array((dx, dy)) * (1 - T[yy, xx]) * 0.5
                nn = n / (np.linalg.norm(n) + 1e-9)
                fdot = nn @ L2
                out[y, x] = (m + 's') if fdot > st['line_hi'] else (m + 'l') if fdot > st['line_mid'] or not edge else 'K'
    return out, dict(fig=fig, line=linep, mat=best, tone=T, f=f)
