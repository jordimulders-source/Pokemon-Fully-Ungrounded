"""Meet sprite-kenmerken (formaat, palet, ramps, omlijning, licht, dithering,
frames, back) per soort en schrijf een CSV + samenvatting.

  python3 tools/concept/sprites/measure.py uit.csv [--set gba|new] [soort ...|--hoenn|--all]

Ook bruikbaar als bibliotheek: measure_sprite(frames, back, pal) -> dict.
"""
import sys, os, re, csv
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import spritelib as L

NB4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def shift(a, dy, dx, fill=0):
    h, w = a.shape
    out = np.full_like(a, fill)
    ys = slice(max(dy, 0), h + min(dy, 0)); yd = slice(max(-dy, 0), h + min(-dy, 0))
    xs = slice(max(dx, 0), w + min(dx, 0)); xd = slice(max(-dx, 0), w + min(-dx, 0))
    out[ys, xs] = a[yd, xd]
    return out


def adjacency(idx):
    """Telt 4-buurparen tussen paletindexen (beide opaak, verschillend)."""
    A = np.zeros((16, 16), int)
    for dy, dx in [(0, 1), (1, 0)]:
        a = idx[:idx.shape[0] - dy, :idx.shape[1] - dx]
        b = idx[dy:, dx:]
        m = (a != b) & (a > 0) & (b > 0)
        np.add.at(A, (a[m], b[m]), 1)
    return A + A.T


def ramps(idxs, pal, outline):
    """Groepeer gebruikte indexen tot ramps: veel aangrenzend + lijkende tint."""
    used = sorted(set(int(v) for a in idxs for v in np.unique(a)) - {0})
    A = sum(adjacency(a) for a in idxs)
    cnt = {k: int(sum((a == k).sum() for a in idxs)) for k in used}
    parent = {k: k for k in used}
    def f(k):
        while parent[k] != k:
            k = parent[k]
        return k
    hs = {k: L.hsl(pal[k]) for k in used}
    pairs = []
    for i in used:
        for j in used:
            if i < j and i not in outline and j not in outline and A[i, j] > 0:
                pairs.append((A[i, j] / min(cnt[i], cnt[j]), i, j))
    for strength, i, j in sorted(pairs, reverse=True):
        (h1, s1, l1), (h2, s2, l2) = hs[i], hs[j]
        dh = min(abs(h1 - h2), 360 - abs(h1 - h2))
        grey = s1 < 0.12 and s2 < 0.12
        if strength > 0.08 and (dh < 40 or grey or min(s1, s2) < 0.12 and abs(l1 - l2) < 0.35):
            parent[f(i)] = f(j)
    groups = {}
    for k in used:
        if k in outline:
            continue
        groups.setdefault(f(k), []).append(k)
    out = []
    for g in groups.values():
        g.sort(key=lambda k: L.lum(pal[k]))
        out.append(g)
    return out, cnt


def measure_sprite(frames, back, pal):
    r = {}
    f0 = frames[0]
    m = f0 > 0
    x0, y0, x1, y1 = L.bbox(m)
    r.update(w=x1 - x0 + 1, h=y1 - y0 + 1, top=y0, bottom=y1, left=x0, right=x1,
             area=int(m.sum()), cx=(x0 + x1) / 2, mass_cx=float(np.nonzero(m)[1].mean()))
    allidx = frames + ([back] if back is not None else [])
    used = sorted(set(int(v) for a in allidx for v in np.unique(a)) - {0})
    r['colors'] = len(used)
    r['colors_f0'] = len(set(np.unique(f0)) - {0})
    lums = {k: L.lum(pal[k]) for k in used}
    darkest = min(used, key=lambda k: lums[k])
    r['darkest_lum'] = round(lums[darkest], 3)
    r['darkest_rgb'] = '%02x%02x%02x' % pal[darkest]
    # omlijning
    e = L.edge_mask(m)
    ev = f0[e]
    r['edge_px'] = int(e.sum())
    r['edge_darkest'] = round(float((ev == darkest).mean()), 3)
    el = np.array([lums[int(v)] for v in ev])
    r['edge_dark'] = round(float((el < 0.30).mean()), 3)      # donker (zwart of donkere tint)
    r['edge_light'] = round(float((el >= 0.45).mean()), 3)    # 'gebroken' omlijning
    # licht/donker-verdeling van de randpixels per kant (selout: lichte kant = lichtere rand)
    ys, xs = np.nonzero(e)
    cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
    tl = (xs < cxm) & (ys < cym); br = (xs > cxm) & (ys > cym)
    r['edge_lum_tl'] = round(float(el[tl].mean()), 3) if tl.any() else None
    r['edge_lum_br'] = round(float(el[br].mean()), 3) if br.any() else None
    # binnenlijnen: donkerste index niet aan de rand
    inner = m & ~e
    r['inner_darkest_frac'] = round(float((f0[inner] == darkest).mean()), 3)
    # lijndikte: rand-pixel met donkerste index waarvan de binnenbuur ook donkerste is
    pd = np.pad(f0 == darkest, 1)
    thick = 0; tot = 0
    for y, x in zip(ys, xs):
        if f0[y, x] != darkest:
            continue
        tot += 1
        # binnenbuur: de buur tegenover een transparante buur
        for dy, dx in NB4:
            yy, xx = y + dy, x + dx
            outside = not (0 <= yy < 64 and 0 <= xx < 64) or f0[yy, xx] == 0
            if outside:
                iy, ix = y - dy, x - dx
                if 0 <= iy < 64 and 0 <= ix < 64 and f0[iy, ix] == darkest and not e[iy, ix]:
                    thick += 1
                break
    r['double_outline'] = round(thick / tot, 3) if tot else None
    # ramps
    outline = {darkest} if lums[darkest] < 0.2 else set()
    rp, cnt = ramps(allidx, pal, outline)
    rp = [g for g in rp if sum(cnt[k] for k in g) >= 12]
    r['n_ramps'] = len(rp)
    r['ramp_lens'] = '/'.join(str(len(g)) for g in sorted(rp, key=len, reverse=True))
    steps_h, steps_l, steps_s = [], [], []
    for g in rp:
        for a, b in zip(g, g[1:]):          # donker -> licht
            h1, s1, l1 = L.hsl(pal[a]); h2, s2, l2 = L.hsl(pal[b])
            if s1 > 0.15 and s2 > 0.15:
                dh = (h2 - h1 + 540) % 360 - 180
                steps_h.append(dh)
            steps_l.append(l2 - l1); steps_s.append(s2 - s1)
    r['ramp_dl'] = round(float(np.mean(steps_l)), 3) if steps_l else None
    r['ramp_dh'] = round(float(np.mean(np.abs(steps_h))), 1) if steps_h else None
    r['ramp_dh_signed'] = round(float(np.mean(steps_h)), 1) if steps_h else None
    r['ramp_ds'] = round(float(np.mean(steps_s)), 3) if steps_s else None
    # licht: rang binnen de ramp vs. positie
    rank = np.full(f0.shape, np.nan)
    for g in rp:
        for i, k in enumerate(g):
            rank[f0 == k] = i / max(1, len(g) - 1)
    sel = inner & ~np.isnan(rank)
    if sel.sum() > 30:
        yy, xx = np.nonzero(sel)
        X = np.c_[(xx - cxm) / max(1, x1 - x0), (yy - cym) / max(1, y1 - y0), np.ones(len(xx))]
        coef, *_ = np.linalg.lstsq(X, rank[sel], rcond=None)
        r['light_dx'], r['light_dy'] = round(float(coef[0]), 3), round(float(coef[1]), 3)
        # grootte schaduwvlak: aandeel pixels in de donkerste helft van hun ramp
        r['shadow_frac'] = round(float((rank[sel] < 0.5).mean()), 3)
        r['highlight_frac'] = round(float((rank[sel] == 1.0).mean()), 3)
    # dithering: pixel met 4 gelijke buren van een andere (opake) kleur, en diagonaal gelijk aan zichzelf
    c = f0
    p = np.pad(c, 1)
    up, dn, lf, rt = p[:-2, 1:-1], p[2:, 1:-1], p[1:-1, :-2], p[1:-1, 2:]
    ul, dr = p[:-2, :-2], p[2:, 2:]
    chk = (c > 0) & (up == dn) & (dn == lf) & (lf == rt) & (up != c) & (up > 0) & (ul == c) & (dr == c)
    r['dither_px'] = int(chk.sum())
    iso = (c > 0) & (up == dn) & (dn == lf) & (lf == rt) & (up != c) & (up > 0)
    r['isolated_px'] = int(iso.sum())
    # frames
    if len(frames) > 1:
        f1 = frames[1]
        r['frame_diff'] = round(float((f0 != f1).sum() / max(1, ((f0 > 0) | (f1 > 0)).sum())), 3)
        best = (1e9, 0, 0)
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                d = int((shift(f0, dy, dx) != f1).sum())
                best = min(best, (d, dy, dx))
        r['frame_shift'] = '%d,%d' % (best[1], best[2])
        r['frame_diff_after_shift'] = round(best[0] / max(1, ((f0 > 0) | (f1 > 0)).sum()), 3)
        b1 = L.bbox(f1 > 0)
        r['f1_h'] = b1[3] - b1[1] + 1; r['f1_w'] = b1[2] - b1[0] + 1
    if back is not None:
        bm = back > 0
        bx0, by0, bx1, by1 = L.bbox(bm)
        r.update(back_w=bx1 - bx0 + 1, back_h=by1 - by0 + 1, back_bottom=by1,
                 back_area=int(bm.sum()), back_cut=int(bm[63].sum()))
    return r


def evo_stage():
    """soort -> fase (1/2/3) volgens species_info."""
    child = {}
    for fn in sorted(os.listdir(os.path.join(L.ROOT, 'src/data/pokemon/species_info'))):
        if not fn.startswith('gen_'):
            continue
        txt = open(os.path.join(L.ROOT, 'src/data/pokemon/species_info', fn)).read()
        for blk in re.split(r'\n    \[SPECIES_', txt)[1:]:
            name = blk.split(']')[0].lower()
            m = re.search(r'\.evolutions = EVOLUTION\((.*?)\),\n', blk, re.S)
            if m:
                for t in re.findall(r'SPECIES_([A-Z0-9_]+)\}', m.group(1)):
                    child.setdefault(t.lower(), name)
    def stage(s, d=0):
        return 1 + d if s not in child or d > 3 else stage(child[s], d + 1)
    final = set(child.values())
    return stage, child, final


def main():
    args = sys.argv[1:]
    out = args.pop(0)
    which = 'gba'
    if '--set' in args:
        i = args.index('--set'); which = args[i + 1]; del args[i:i + 2]
    if args == ['--hoenn'] or not args:
        sp = L.hoenn_species()
    elif args == ['--all']:
        sp = sorted(d for d in os.listdir(L.GFX) if L.front_path(d, which))
    else:
        sp = args
    stage, child, parents = evo_stage()
    rows = []
    for s in sp:
        try:
            fr, pal = L.load_front(s, which)
            try:
                bk, _ = L.load_back(s, which)
            except Exception:
                bk = None
            r = measure_sprite(fr, bk, pal)
        except Exception as ex:
            print('skip', s, ex); continue
        st = stage(s)
        r = dict(species=s, stage=st, has_evo=int(s in parents), **r)
        rows.append(r)
    keys = list(rows[0].keys())
    for r in rows:
        for k in r:
            if k not in keys: keys.append(k)
    with open(out, 'w', newline='') as fh:
        w = csv.DictWriter(fh, keys); w.writeheader(); w.writerows(rows)
    print(out, len(rows))


if __name__ == '__main__':
    main()
