"""Algemene icoon-onderlaag (ICOON_WERKWIJZE stap 2-3), uit de front + een klein JSON per soort.

python3 docs/concept/sprites/graphics_proef/icoon/icoon_bouw.py <soort.json> [uitmap]
  -> <uitmap>/onderlaag.png   (32x32, modus P, gekozen icoonpalet, index 0 transparant)
     <uitmap>/onderlaag_8x.png (front 4x | onderlaag 8x | echte Gen 3-iconen 8x als buren)
     <uitmap>/rapport.txt     (schalen, minimummaten, paletafstanden, maten)

JSON (alle coordinaten in de front, 64x64):
{
 "front": "docs/concept/sprites/.../af/x.png",       # front, modus P (frame 1 = bovenste 64 rijen)
 "anker": [x, y],              # halsgewricht: de kopgroep schaalt hieromheen
 "factoren": {"kop":1.25, "lijf":0.95, "overig":1.0},   # t.o.v. gewone verkleining S (meetstudie); optioneel
 "doelhoogte": 18,             # optioneel; anders uit de fronthoogte-tabel (25->15 ... 61->24)
 "buren": ["wailmer", "goldeen", "relicanth"],          # echte iconen op het vel
 "palet": 2,                   # optioneel: palet forceren (anders het dichtstbijzijnde)
 "delen": [                    # TEKENVOLGORDE: achter -> voor. Bij overlap van polygonen wint het voorste deel.
   {"naam":"staart", "groep":"overig",           # kop | lijf | overig (overig hangt aan "ouder", standaard lijf)
    "poly":[[x,y],...] | "box":[x0,y0,x1,y1],    # gebied in de front (box inclusief)
    "kleuren":[3,4,5],          # optioneel: alleen deze front-indices horen bij dit deel
    "min":"staart",             # optioneel: oor | voorpoot | staart | oog -> minimummaat uit de meetstudie
    "aanhecht":[x,y],           # draaipunt voor eigen schaal (min-maat of "schaal"), standaard het anker/oorsprong
    "schaal":1.1,               # optioneel: extra factor t.o.v. de groep
    "dun":true,                 # dunne delen: masker 1 px verdikt, zodat ze als stompje blijven
    "binnenlijn":true,          # lijn (index 14) waar dit deel over een eerder getekend deel ligt;
                                #   "achter" = de lijn komt op het achterste deel (dun deel zoals een staf)
    "lijn_op":["lijf"],         # optioneel: alleen tegen deze delen een binnenlijn
    "verschuif":[dx,dy],        # in icoonpixels (posewissel/compact maken, zoals Linoone)
    "ramp":[i_donker,...,i_licht]  # optioneel: vaste icoontinten voor dit deel, op helderheid verdeeld
   }, ...],
 "oog": {"deel":"kop", "front":[x0,y0,x1,y1], "patroon":["DD","DW"], "kleur":{"D":15,"W":3}}  # optioneel
}
Regels uit de meetstudie: kop x1,25, lijf x0,95 t.o.v. S; oog verschuift niet in de kop (zelfde transformatie);
minimummaten oog 1+0,26f, oor 2+0,29f, voorpoot max(2,1,2+0,28f), staart 3+0,32f (f = langste maat in de front).
"""
import sys, os, json, re, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../..'))
ARGV = [os.path.abspath(a) for a in sys.argv[1:]]
os.chdir(ROOT)
TABEL = [(25, 15), (35, 18), (45, 21), (54, 22), (61, 24), (64, 25)]
MIN = {'oog': lambda f: 1.0 + .26 * f, 'oor': lambda f: 2.0 + .29 * f,
       'voorpoot': lambda f: max(2.0, 1.2 + .28 * f), 'staart': lambda f: 3.0 + .32 * f}


def lees_pal(p):
    L = open(p).read().split('\n'); return np.array([[int(v) for v in L[3 + k].split()[:3]] for k in range(16)], float)


IPAL = [lees_pal(f'graphics/pokemon/icon_palettes/pal{k}.pal') for k in range(6)]


def lab(c):  # sRGB (0-255) -> CIELAB
    c = np.asarray(c, float) / 255; c = np.where(c > .04045, ((c + .055) / 1.055) ** 2.4, c / 12.92)
    M = np.array([[.4124, .3576, .1805], [.2126, .7152, .0722], [.0193, .1192, .9505]])
    xyz = c @ M.T / np.array([.9505, 1.0, 1.089])
    f = np.where(xyz > .008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def afstand(a, b):  # kleurafstand in CIELAB (Delta E 1976): tint telt mee, paars wordt geen blauw
    return np.sqrt(((lab(a) - lab(b)) ** 2).sum(-1))


def icon_pal_index():
    gba, mod = {}, {}
    for fn in os.listdir('src/data/pokemon/species_info'):
        for mm in re.finditer(r'\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},', open('src/data/pokemon/species_info/' + fn).read(), re.S):
            v = re.search(r'iconPalIndex = (?:P_GBA_STYLE_SPECIES_ICONS \? (\d) : )?(\d)', mm.group(2))
            if v: gba[mm.group(1).lower()] = int(v.group(1) or v.group(2)); mod[mm.group(1).lower()] = int(v.group(2))
    return gba, mod


def bouw(cfg, S_extra=1.0, log=None):
    fr_im = Image.open(cfg['front']); fr = np.array(fr_im)[:64]
    FP = np.array(fr_im.getpalette()[:48], float).reshape(16, 3)
    rgb = FP[fr]; lum = FP.mean(1)[fr]; vol = fr > 0
    # lijnkleuren: front-indices die als lijn tellen (standaard: helderheid < 45, meestal alleen zwart)
    donker = np.isin(fr, cfg['lijnkleuren']) if 'lijnkleuren' in cfg else (lum < 45) & vol
    # buitenste donkere rand van de front hoort niet bij de vlakken (anders wordt alles 1 px te dik)
    rand = vol & ~nd.binary_erosion(vol); buitenlijn = rand & donker
    fy, fx = np.nonzero(vol); fh = fy.max() - fy.min() + 1
    th = cfg.get('doelhoogte') or float(np.interp(fh, *zip(*TABEL)))
    S = (th - 2) / fh * S_extra          # -2: de omlijning komt er buiten omheen
    fac = {'kop': 1.25, 'lijf': .95, 'overig': 1.0}; fac.update(cfg.get('factoren', {}))
    A = np.array(cfg['anker'], float)
    # labels: voorste deel wint
    delen = cfg['delen']; lab = np.full((64, 64), -1)
    for i in reversed(range(len(delen))):
        d = delen[i]; m = Image.new('L', (64, 64), 0)
        if 'poly' in d: ImageDraw.Draw(m).polygon([tuple(p) for p in d['poly']], fill=1, outline=1)
        else: ImageDraw.Draw(m).rectangle(d['box'], fill=1)
        m = np.array(m) > 0
        if 'kleuren' in d: m &= np.isin(fr, d['kleuren'])
        lab[m & vol & (lab < 0)] = i
    # rest: naar het dichtstbijzijnde deel
    rest = vol & (lab < 0)
    if rest.any():
        _, (iy, ix) = nd.distance_transform_edt(lab < 0, return_indices=True); lab[rest] = lab[iy[rest], ix[rest]]
    OFF = np.array([16.0, 8.0])
    def T_groep(g, p):  # front -> icoon voor een groep (zonder eigen schaal)
        p = np.asarray(p, float)
        if g == 'kop': return OFF + A * S * fac['lijf'] + (p - A) * S * fac['kop']
        return OFF + p * S * fac['lijf']
    info = []
    trans = []
    for i, d in enumerate(delen):
        g = d.get('groep', 'lijf'); ouder = d.get('ouder', 'lijf') if g == 'overig' else g
        s = S * fac[g] * d.get('schaal', 1.0)
        m = lab == i
        if not m.any(): trans.append(None); continue
        yy, xx = np.nonzero(m)
        if d.get('aanhecht') is not None: h = d['aanhecht']
        elif g == 'kop': h = A
        elif g == 'lijf': h = [0, 0]
        else:  # draaipunt = punt van het deel dichtst bij het anker
            k = np.argmin((xx - A[0]) ** 2 + (yy - A[1]) ** 2); h = [xx[k], yy[k]]
        h = np.array(h, float)
        if 'min' in d:
            f = max(xx.max() - xx.min() + 1, yy.max() - yy.min() + 1); mn = MIN[d['min']](f)
            if f * s < mn:
                info.append(f"  {d['naam']}: {d['min']} f={f} -> {f*s:.1f} px < minimum {mn:.1f}: schaal x{mn/(f*s):.2f}"); s = mn / f
            else: info.append(f"  {d['naam']}: {d['min']} f={f} -> {f*s:.1f} px >= minimum {mn:.1f}")
        base = T_groep(ouder, h) + np.array(d.get('verschuif', [0, 0]), float)
        trans.append((h, s, base))
    # renderen: 4x4 monsters per icoonpixel
    N = 64; kleur = np.zeros((N, N, 3)); deel = np.full((N, N), -1); isdonker = np.zeros((N, N), bool); isglans = isdonker.copy()
    ddrem = cfg.get('donker_drempel', .6)   # aandeel donkere frontpixels waarboven een icoonpixel lijn wordt
    sub = (np.arange(4) + .5) / 4
    for i, d in enumerate(delen):
        if trans[i] is None: continue
        h, s, base = trans[i]; m = (lab == i) & ~buitenlijn
        if d.get('dun'): m = nd.binary_dilation(m) & ((lab == i) | ~vol) | m
        drem = .35 if d.get('dun') else .45
        k = 1 / s
        for Y in range(N):
            for X in range(N):
                c = h + (np.array([X + .5, Y + .5]) - base) / s
                px = np.clip(np.floor(c[0] - k / 2 + sub[None, :] * k).astype(int), -1, 64)
                py = np.clip(np.floor(c[1] - k / 2 + sub[:, None] * k).astype(int), -1, 64)
                PX, PY = np.broadcast_arrays(px, py); ok = (PX >= 0) & (PX < 64) & (PY >= 0) & (PY < 64)
                if not ok.any(): continue
                sel = np.zeros(PX.shape, bool); sel[ok] = m[PY[ok], PX[ok]]
                if sel.mean() < drem: continue
                q = sel & ok; dk = donker[PY[q], PX[q]]; lic = ~dk & vol[PY[q], PX[q]]   # transparante pixels (verdikte dunne delen) tellen niet voor de kleur
                if lic.sum() == 0 or dk.mean() > ddrem: isdonker[Y, X] = True; kleur[Y, X] = 40
                else:
                    # kleur = de meest voorkomende frontkleur (geen gemiddelde: dat geeft modder en blur)
                    isdonker[Y, X] = False; fi = fr[PY[q][lic], PX[q][lic]]
                    if cfg.get('kleurkeuze', 'modus') == 'gemiddeld': kleur[Y, X] = FP[fi].mean(0)
                    else: kleur[Y, X] = FP[np.bincount(fi, minlength=16).argmax()]
                    wit = FP.mean(1)[fi] > 215
                    isglans[Y, X] = wit.mean() >= .3
                    if isglans[Y, X]: kleur[Y, X] = FP[fi[wit]].mean(0)
                deel[Y, X] = i
    mask = deel >= 0
    if os.environ.get("IB_DEBUG"): np.save(os.environ["IB_DEBUG"], deel)
    if not cfg.get('gaten'):
        gat = nd.binary_fill_holes(mask) & ~mask
        if gat.any():
            _, (iy, ix) = nd.distance_transform_edt(~mask, return_indices=True)
            deel[gat] = deel[iy[gat], ix[gat]]; kleur[gat] = kleur[iy[gat], ix[gat]]; mask |= gat
    # uitsteeksels van 1 pixel weg (behalve dunne delen)
    for _ in range(2):
        nb = nd.convolve(mask.astype(int), np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]), mode='constant')
        weg = mask & (nb <= 1) & ~np.isin(deel, [i for i, d in enumerate(delen) if d.get('dun')])
        mask &= ~weg; deel[weg] = -1
    # afronden: convexe hoekpixels (2 lege orthogonale buren in een L + lege diagonaal) weg, behalve dunne delen
    dunid = [i for i, d in enumerate(delen) if d.get('dun')]
    for _ in range(cfg.get('afronden', 0)):
        Pm = np.pad(mask, 1); hoek = np.zeros_like(mask)
        for a, b in (((0, 1), (1, 0)), ((0, 1), (-1, 0)), ((0, -1), (1, 0)), ((0, -1), (-1, 0))):
            sh = lambda o: Pm[1 + o[0]:N + 1 + o[0], 1 + o[1]:N + 1 + o[1]]
            hoek |= mask & ~sh(a) & ~sh(b) & ~sh((a[0] + b[0], a[1] + b[1])) & sh((-a[0], -a[1])) & sh((-b[0], -b[1]))
        rond = [i for i, d in enumerate(delen) if d.get('afronden', not d.get('dun') and d.get('groep') != 'overig')]
        hoek &= np.isin(deel, rond); mask &= ~hoek; deel[hoek] = -1
    # palet kiezen: gemiddelde afstand van de vlakpixels tot het dichtstbijzijnde icoonkleur 1-13
    vlak = mask & ~isdonker; C = kleur[vlak]
    afst, tint = [], []
    for k, P in enumerate(IPAL):
        D = afstand(C[:, None, :], P[None, 1:14, :]); afst.append(D.min(1).mean())
        u, n = np.unique(D.argmin(1), return_counts=True); tint.append(int((n >= max(2, .03 * len(C))).sum()))
    # binnen 3% van de beste afstand: het palet dat de meeste tinten oplevert (schaduw blijft), daarna de kleinste afstand
    best = min(afst); kand = [k for k in range(6) if afst[k] <= best * 1.03]
    pk = cfg.get('palet', max(kand, key=lambda k: (tint[k], -afst[k]))); P = IPAL[pk]
    idx = np.zeros((N, N), np.uint8)
    for i, d in enumerate(delen):
        mi = vlak & (deel == i)
        if not mi.any(): continue
        ramp = d.get('ramp')
        if ramp == 'auto':  # tinten van het palet met dezelfde kleurtoon als het deel, op helderheid gesorteerd
            import colorsys
            hs = lambda c: colorsys.rgb_to_hsv(*(np.asarray(c) / 255))
            hm, sm, _ = hs(kleur[mi].mean(0)); kand = []
            for j in range(1, 14):
                hj, sj, vj = hs(P[j])
                if sm < .2: ok = sj < .2
                else: ok = sj > .2 and min(abs(hj - hm), 1 - abs(hj - hm)) < d.get('toonvenster', .07)
                if ok: kand.append(j)
            kand = sorted(kand or [int(afstand(kleur[mi].mean(0)[None], P[1:14]).argmin() + 1)], key=lambda j: P[j].mean())
            # Gen 3-verdeling: het grootste deel in de basistint, alleen de lichtste 20%/5% een of twee tinten lichter,
            # de donkerste 15%/5% een of twee tinten donkerder (volgorde = helderheid in de front)
            L = kleur[mi].mean(1); r = np.argsort(np.argsort(L)) / max(1, len(L) - 1)
            basis = int(afstand(kleur[mi].mean(0)[None], P[kand]).argmin())
            stap = np.zeros(len(L), int)
            for drem, st in ((.80, 1), (.95, 2)): stap[(r >= drem) & (L > np.median(L) + 8)] = st
            for drem, st in ((.15, -1), (.05, -2)): stap[(r <= drem) & (L < np.median(L) - 8)] = st
            idx[mi] = np.array(kand)[np.clip(basis + stap, 0, len(kand) - 1)]
            info.append(f"  {d['naam']}: auto-ramp {kand} (basis {kand[basis]})")
        elif ramp:  # helderheid binnen het deel lineair over de opgegeven tinten
            L = kleur[mi].mean(1); lo, hi = np.percentile(L, 5), np.percentile(L, 95)
            t = np.clip((L - lo) / max(1, hi - lo), 0, .999); idx[mi] = np.array(d['ramp'])[(t * len(d['ramp'])).astype(int)]
        else:
            hoog = 16 if cfg.get('donkere_vulling', True) else 14   # Gen 3 vult zwarte/donkere delen met 14/15 (Umbreon, Murkrow)
            idx[mi] = (afstand(kleur[mi][:, None, :], P[None, 1:hoog, :]).argmin(1) + 1)
    gl = vlak & isglans          # glans/wit uit de front: dichtstbijzijnde van alle tinten (wit mag)
    if gl.any(): idx[gl] = afstand(kleur[gl][:, None, :], P[None, 1:14, :]).argmin(1) + 1
    # (wit telt niet mee voor de paletkeuze: die gebeurt op de vlakken hierboven)
    idx[mask & isdonker] = 14
    # losse pixels in een vlak -> meest voorkomende buur van hetzelfde deel
    for _ in range(2):
        for Y, X in zip(*np.nonzero(vlak)):
            nbs = [(Y + a, X + b) for a, b in ((0, 1), (1, 0), (0, -1), (-1, 0)) if 0 <= Y + a < N and 0 <= X + b < N]
            same = [idx[p] for p in nbs if deel[p] == deel[Y, X] and idx[p] == idx[Y, X]]
            if not same:
                kand = [idx[p] for p in nbs if deel[p] == deel[Y, X] and vlak[p]]
                if kand: idx[Y, X] = max(set(kand), key=kand.count)
    # binnenlijnen: voorste deel krijgt lijn waar het tegen een eerder getekend deel ligt
    for i, d in enumerate(delen):
        if not d.get('binnenlijn', False): continue
        mi = mask & (deel == i); achter = mask & (deel >= 0) & (deel < i)
        if d.get('lijn_op'): achter &= np.isin(deel, [j for j, e in enumerate(delen) if e['naam'] in d['lijn_op']])
        if d['binnenlijn'] == 'achter':   # dun deel voor een groter deel (staf voor het lijf): lijn op het achterste deel
            grens = achter & nd.binary_dilation(mi, np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
            idx[grens & ~isdonker] = 14; continue
        grens = mi & nd.binary_dilation(achter, np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]))
        # niet als het deel daardoor bijna verdwijnt
        if grens.sum() < .5 * mi.sum(): idx[grens] = 14
    # omlijning BUITEN het silhouet: boven 15, onder 14
    buiten = nd.binary_dilation(mask, np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])) & ~mask
    allm = mask | buiten; ys, xs = np.nonzero(allm); mid = (ys.min() + ys.max()) / 2
    for Y, X in zip(*np.nonzero(buiten)): idx[Y, X] = 15 if Y < mid else 14
    # oog op de omgerekende plek
    for o in ([cfg['oog']] if isinstance(cfg.get('oog'), dict) else cfg.get('oog', [])):
        i = [d['naam'] for d in delen].index(o.get('deel', 'kop')); h, s, base = trans[i]
        x0, y0, x1, y1 = o['front']; c = base + (np.array([(x0 + x1 + 1) / 2, (y0 + y1 + 1) / 2]) - h) * s
        pat = o['patroon']; ph, pw = len(pat), len(pat[0])
        oy, ox = int(round(c[1] - ph / 2)), int(round(c[0] - pw / 2))
        for a, row in enumerate(pat):
            for b, ch in enumerate(row):
                if ch in o['kleur']: idx[oy + a, ox + b] = o['kleur'][ch]
        f = max(x1 - x0 + 1, y1 - y0 + 1)
        info.append(f"  oog: front {f} px, centrum icoon ({c[0]:.1f},{c[1]:.1f}), patroon {pw}x{ph}, minimum {MIN['oog'](f):.1f}")
    # lijnen uit de front (mond, strepen, staf): polylijn in frontcoordinaten, 1 px, met de transformatie van het deel
    namen = [d['naam'] for d in delen]
    for l in cfg.get('lijnen', []):
        h, s, base = trans[namen.index(l['deel'])]
        pts = [base + (np.array(p, float) + .5 - h) * s for p in l['punten']]
        kl = l['kleur']
        if isinstance(kl, list): kl = int(afstand(np.array(kl, float)[None, :], P[1:14]).argmin() + 1)
        for a, b in (zip(pts[:-1], pts[1:]) if len(pts) > 1 else [(pts[0], pts[0])]):
            n = int(max(abs(b - a)) * 2) + 1
            for t in np.linspace(0, 1, n):
                q = a + (b - a) * t; X, Y = int(np.floor(q[0])), int(np.floor(q[1]))
                if l.get('alleen_binnen', True) and not mask[Y, X]: continue
                idx[Y, X] = kl
    if os.environ.get('IB_DEBUG'): np.save(os.environ['IB_DEBUG'] + '_idx.npy', idx); np.save(os.environ['IB_DEBUG'] + '_kleur.npy', kleur)
    # bijsnijden en plaatsen: onderkant y 29, midden x 15.5
    ys, xs = np.nonzero(idx > 0); crop = idx[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    hgt, wdt = crop.shape; res = np.zeros((32, 32), np.uint8)
    oy = 30 - hgt; ox = int(round(15.5 - (wdt - 1) / 2))
    for a in range(hgt):
        for b in range(wdt):
            if crop[a, b] and 0 <= oy + a < 32 and 0 <= ox + b < 32: res[oy + a, ox + b] = crop[a, b]
    meta = dict(S=S, fh=fh, th=th, hoogte=hgt, breedte=wdt, palet=pk, afst=afst, tint=tint, info=info, fac=fac)
    return res, meta


def vel(cfg, ims, labels, uit):
    gba, _ = icon_pal_index()
    fr_im = Image.open(cfg['front']); fr = np.array(fr_im)[:64]; FP = np.array(fr_im.getpalette()[:48]).reshape(16, 3)
    def rgba(a, P):
        o = np.zeros(a.shape + (4,), np.uint8)
        for k in range(1, 16): o[a == k] = tuple(P[k]) + (255,)
        return Image.fromarray(o)
    tiles = [('front', rgba(fr, FP).resize((256, 256), Image.NEAREST))]
    for a, P, l in zip(ims, [IPAL[p] for p in [m for m in labels[1]]], labels[0]):
        tiles.append((l, rgba(a, P.astype(int)).resize((256, 256), Image.NEAREST)))
    for sp in cfg.get('buren', []):
        a = np.array(Image.open(f'graphics/pokemon/{sp}/icon_gba.png'))[:32]
        tiles.append((f'{sp} (pal{gba.get(sp,0)})', rgba(a, IPAL[gba.get(sp, 0)].astype(int)).resize((256, 256), Image.NEAREST)))
    # 1x-strook: icoon tussen de buren, zoals in het partymenu
    W = Image.new('RGB', (len(tiles) * 266 + 10, 330), (115, 197, 164)); d = ImageDraw.Draw(W)
    for n, (l, t) in enumerate(tiles):
        W.paste(t, (10 + n * 266, 22), t); d.text((10 + n * 266, 4), l, fill=0)
    x = 10
    for l, t in tiles[1:]:
        s = t.resize((64, 64), Image.NEAREST) if l != 'front' else t
        W.paste(s.resize((32, 32), Image.NEAREST), (x, 290), s.resize((32, 32), Image.NEAREST)); x += 40
    d.text((x + 10, 300), '1x', fill=0)
    W.save(uit)


if __name__ == '__main__':
    cfg = json.load(open(ARGV[0])); uit = ARGV[1] if len(ARGV) > 1 else os.path.dirname(ARGV[0])
    os.makedirs(uit, exist_ok=True)
    # hoogte en breedte naar het doel bijsturen (hooguit 6 keer)
    S_extra = 1.0
    for it in range(6):
        res, meta = bouw(cfg, S_extra)
        ys, xs = np.nonzero(res); h = ys.max() - ys.min() + 1; w = xs.max() - xs.min() + 1
        f = meta['th'] / h
        if w > 27: f = min(f, 27 / w)
        if abs(h - meta['th']) <= 1 and w <= 27: break
        S_extra *= f
    im = Image.fromarray(res, 'P'); im.putpalette(IPAL[meta['palet']].astype(int).flatten().tolist() + [0] * 720)
    im.save(os.path.join(uit, 'onderlaag.png'), transparency=0)
    vel(cfg, [res], (['onderlaag'], [meta['palet']]), os.path.join(uit, 'onderlaag_8x.png'))
    r = [f"front {cfg['front']}", f"fronthoogte {meta['fh']} -> doelhoogte {meta['th']:.1f}; S {meta['S']:.3f} (bijgestuurd x{S_extra:.2f})",
         f"factoren {meta['fac']}", f"icoon {meta['breedte']}x{meta['hoogte']} (onderkant y29, midden x15.5)",
         'minimummaten:'] + meta['info'] + ['paletafstand (gemiddelde Delta E in Lab; lager = beter):'] + \
        [f"  pal{k}: {a:.1f}  ({meta['tint'][k]} tinten){'   <- gekozen' if k == meta['palet'] else ''}" for k, a in enumerate(meta['afst'])]
    open(os.path.join(uit, 'rapport.txt'), 'w').write('\n'.join(r) + '\n'); print('\n'.join(r))
