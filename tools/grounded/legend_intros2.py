#!/usr/bin/env python3
"""Project Grounded: lichte gevechtsintro's, tweede reeks (Articuno, Zapdos, Moltres, Zacian/Zamazenta, Xerneas/Yveltal).
Zelfde aanpak als legend_intros.py / gym_intro_lib.py: een paar stilstaande BG0-beelden (paletten 13-15) en de beweging
in C (src/data/legend_intros2.h). De achtergronden zijn de echte kaarten waar de legendary staat (metatiles van de
tilesets, dezelfde uitsnede als in de game), zodat de intro begint op de plek waar je net stond.

Uitvoer in graphics/battle_transitions/legend_<naam>.png/.pal + legend_<naam>_maps.bin, plus
src/data/legend_intros2_gen.h (paletindexen die C nodig heeft).
- articuno: VORST (ijsvarens van de randen naar binnen; index 1-15 van palet 13 = groeifase, C kleurt ze in en blendt
            additief over de echte grotkaart), BARST (zelfde, met barsten vanuit het midden in palet 14)
- zapdos:   INSTITUUT (Route 119: de klif en het Weather Institute; in C 's nachts en in het onweer, de bliksem licht
            het beeld op), ONDERSCHRIFT (zelfde met de balk "FORECAST: 100% ZAPDOS")
- moltres:  KRATER (Mt. Chimney: het lavameer op de top; lava-indexen voor de paletcyclus)
- wolves:   OPEN PLEK (Mega Forest: de bloemenweide achterin, in C in de schaduw)
- xerneas:  BALLONLEA (heksenkring), kleur in palet 13-15 en de 'uitgedoofde' versie (zelfde tiles) in 10-12
- yveltal:  GLIMWOOD (heksenkring in de Tangle), idem
Gebruik: python3 tools/grounded/legend_intros2.py [voorbeeldmap] [naam ...]"""
import json, math, os, random, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw
from gym_intro_lib import Encoder, text, text_width, preview_strip, OUT, KEY, gba, ROOT

PREVIEW = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].isalpha() else None
PFX = 'legend_'
GEN = {}   # naam -> waarde, voor src/data/legend_intros2_gen.h


# ------------------------------------------------------------------ echte kaarten renderen
def _tsdir(sym):
    import re
    name = re.sub(r'(?<!^)([A-Z])', r'_\1', sym.replace('gTileset_', '')).lower()
    for kind in ('primary', 'secondary'):
        d = os.path.join(ROOT, 'data/tilesets', kind, name)
        if os.path.isdir(d):
            return d
    raise SystemExit('geen tilesetmap voor ' + sym)


def _tiles(d):
    b = os.path.join(d, 'BASE')
    td = os.path.join(os.path.dirname(d), open(b).read().strip()) if os.path.exists(b) else d
    im = Image.open(os.path.join(td, 'tiles.png'))
    a = np.array(im) & 15
    w, h = im.size
    return [a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] for ty in range(h // 8) for tx in range(w // 8)], td


def _jasc(fn):
    L = open(fn).read().split('\n')[3:19]
    return [tuple(int(v) for v in l.split()[:3]) for l in L if l.strip()]


def render_map(layout, x0, y0, w=15, h=10):
    """Uitsnede van w x h metatiles (standaard precies 240 x 160) uit een layout, met de echte tiles en paletten."""
    L = [l for l in json.load(open(os.path.join(ROOT, 'data/layouts/layouts.json')))['layouts'] if l.get('id') == layout][0]
    W, H = L['width'], L['height']
    v = struct.unpack('<%dH' % (W * H), open(os.path.join(ROOT, L['blockdata_filepath']), 'rb').read())
    pdir, sdir = _tsdir(L['primary_tileset']), _tsdir(L['secondary_tileset'])
    T, ptd = _tiles(pdir)
    T = T + [np.zeros((8, 8), int)] * (512 - len(T))
    S, std = _tiles(sdir)
    T += S
    pals = []
    for i in range(16):
        f = os.path.join(pdir if i < 6 else sdir, 'palettes', '%02d.pal' % i)
        pals.append(np.array(_jasc(f) if os.path.exists(f) else [(0, 0, 0)] * 16, np.uint8))
    mtp = open(os.path.join(ptd, 'metatiles.bin'), 'rb').read()
    msd = sdir if os.path.exists(os.path.join(sdir, 'metatiles.bin')) else std
    mts = open(os.path.join(msd, 'metatiles.bin'), 'rb').read()
    img = np.zeros((h * 16, w * 16, 3), np.uint8)
    for r in range(h):
        for c in range(w):
            m = v[(y0 + r) * W + x0 + c] & 0x3FF
            b = mtp[m * 16:m * 16 + 16] if m < 512 else mts[(m - 512) * 16:(m - 512) * 16 + 16]
            e = struct.unpack('<8H', b)
            for layer in range(2):
                for q in range(4):
                    val = e[layer * 4 + q]
                    t, hf, vf, p = val & 0x3FF, val >> 10 & 1, val >> 11 & 1, val >> 12
                    tl = T[t] if t < len(T) else np.zeros((8, 8), int)
                    if hf:
                        tl = tl[:, ::-1]
                    if vf:
                        tl = tl[::-1]
                    oy, ox = r * 16 + (q // 2) * 8, c * 16 + (q % 2) * 8
                    sub = img[oy:oy + 8, ox:ox + 8]
                    if layer == 0:
                        sub[:] = pals[p][0]
                    msk = tl != 0
                    sub[msk] = pals[p][tl[msk]]
    img = (img >> 3) << 3
    # zuiver zwart is in BG-beelden doorzichtig: een tikje lichter
    blk = (img == 0).all(2)
    img[blk] = (8, 8, 8)
    return Image.fromarray(img)


# ------------------------------------------------------------------ drie paletten van 15 kleuren voor een beeld
def _median_cut(pix, n):
    pix = np.unique(pix, axis=0)
    if len(pix) <= n:
        return [tuple(int(v) for v in c) for c in pix]
    im = Image.fromarray(pix.reshape(1, -1, 3).astype(np.uint8))
    q = im.quantize(n, method=Image.Quantize.MEDIANCUT)
    p = q.getpalette()[:n * 3]
    return [gba(p[i * 3:i * 3 + 3]) for i in range(len(p) // 3)]


def _err(px, pal):
    if not len(px):
        return 0
    P = np.array(pal, np.int32)
    d = ((px[:, None, :] - P[None, :, :]) ** 2 * np.array([3, 6, 2])).sum(2)
    return d.min(1).sum()


def quantize3(imgs, forced=(), iters=8, n=3, shared=3):
    """Tile-k-means: verdeelt de tiles over n paletten en kiest per palet 15 kleuren (median cut). De 'shared' kleuren
    die de meeste pixels beslaan (de grond) staan in elk palet, anders verschilt de grond per tile."""
    tiles = []
    for im in imgs:
        a = (np.array(im.convert('RGB')).astype(np.int32) >> 3) << 3
        for ty in range(a.shape[0] // 8):
            for tx in range(a.shape[1] // 8):
                t = a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].reshape(64, 3)
                m = ~((t == np.array(KEY)).all(1) | (t == 0).all(1))
                tiles.append(t[m])
    allp = np.concatenate([t for t in tiles if len(t)])
    u, cnt = np.unique(allp, axis=0, return_counts=True)
    common = [tuple(int(v) for v in u[i]) for i in np.argsort(-cnt)[:shared]]
    forced = list(forced) + [c for c in common if c not in forced]
    means = np.array([t.mean(0) if len(t) else (0, 0, 0) for t in tiles])
    lum = means @ np.array([0.3, 0.6, 0.1])
    order = np.argsort(lum)
    assign = np.zeros(len(tiles), int)
    for k in range(n):
        assign[order[k * len(order) // n:(k + 1) * len(order) // n]] = k
    pals = None
    for it in range(iters):
        pals = []
        for k in range(n):
            pix = [t for t, a_ in zip(tiles, assign) if a_ == k and len(t)]
            pix = np.concatenate(pix) if pix else np.zeros((1, 3), np.int32)
            fm = np.zeros(len(pix), bool)
            for c in forced:
                fm |= (pix == np.array(c)).all(1)
            rest = pix[~fm]
            pal = _median_cut(rest, 15 - len(forced)) if len(rest) else []
            pal = list(forced) + [c for c in pal if c not in forced]
            pals.append(pal[:15])
        new = np.array([np.argmin([_err(t, pals[k]) for k in range(n)]) for t in tiles])
        if (new == assign).all():
            break
        assign = new
    return pals


class EncoderN(Encoder):
    """Encoder met n paletten vanaf BG-palet 'base' (de wereld is zwart en ligt helemaal onder het beeld, dus ook de
    paletten van de kaart zijn vrij; C slaat ze over bij het zwart maken van de wereld)."""
    def __init__(self, name, pals, base, prefix=PFX):
        Encoder.__init__(self, name, pals[:3], prefix)
        from gym_intro_lib import pad16
        self.pals = [pad16(p) for p in pals]
        self.base = base

    def add(self, img, force_pal=None, label=''):
        n0 = len(self.tiles)
        a = np.array(img.convert('RGB')).astype(np.int32)
        H, W = a.shape[0] // 8, a.shape[1] // 8
        out = []
        key = np.array(KEY)
        P = [np.array(p[1:], np.int32) for p in self.pals]
        for ty in range(H):
            for tx in range(W):
                t = a[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].reshape(64, 3)
                transp = (t == key).all(1) | (t == 0).all(1)
                g = (t >> 3) << 3
                best = None
                for k, pal in enumerate(P):
                    d = ((g[:, None, :] - pal[None, :, :]) ** 2 * np.array([3, 6, 2])).sum(2)
                    idx = d.argmin(1) + 1
                    err = d.min(1)
                    err[transp] = 0
                    e = err.sum()
                    if best is None or e < best[0]:
                        best = (e, k, idx)
                e, k, idx = best
                idx = idx.astype(np.uint8)
                idx[transp] = 0
                self.worst = max(self.worst, e)
                if not idx.any():
                    out.append(0)
                    continue
                out.append(self._tile(idx.reshape(8, 8)) | ((self.base + k) << 12))
        self.maps.append(out)
        print('  %s %s: +%d tiles (slechtste tile-fout %d)' % (self.name, label, len(self.tiles) - n0, self.worst))
        return out

    def save(self, maps_name='maps'):
        Encoder.save(self, maps_name)
        write_pal(OUT + '%s%s.pal' % (self.prefix, self.name), [c for p in self.pals for c in p])

    def render(self, m, w=30, pals=None):
        pals = pals or self.pals
        h = len(m) // w
        img = Image.new('RGB', (w * 8, h * 8), (0, 0, 0))
        for i, v in enumerate(m):
            t = self.tiles[v & 0x3FF].reshape(8, 8)
            if v & 0x400:
                t = t[:, ::-1]
            if v & 0x800:
                t = t[::-1]
            p = pals[(v >> 12) - self.base] if v else pals[0]
            rgb = np.array(p, np.uint8)[t]
            rgb[t == 0] = (0, 0, 0)
            img.paste(Image.fromarray(rgb), ((i % w) * 8, (i // w) * 8))
        return img


def screen_index(enc, m):
    """Tilemap m (30 x 20) terug naar per pixel (palet, index)."""
    P = np.zeros((160, 240), np.int32)
    I = np.zeros((160, 240), np.int32)
    for i, v in enumerate(m):
        t = enc.tiles[v & 0x3FF].reshape(8, 8)
        if v & 0x400:
            t = t[:, ::-1]
        if v & 0x800:
            t = t[::-1]
        y, x = (i // 30) * 8, (i % 30) * 8
        I[y:y + 8, x:x + 8] = t
        P[y:y + 8, x:x + 8] = (v >> 12) if v else 0
    return P, I


def write_pal(path, cols):
    with open(path, 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n%d\n' % len(cols))
        for c in cols:
            fp.write('%d %d %d\n' % tuple(c))


def save_preview(name, imgs):
    if PREVIEW:
        preview_strip(imgs, os.path.join(PREVIEW, 'legend_%s.png' % name), k=2, cols=3)


# ================================================================== Articuno
ART_ICE = [(104, 152, 216), (72, 112, 184), (136, 184, 232)]   # 'oud' ijs (palet 14), per fase afwisselend
ART_CRACK = [(248, 248, 248), (168, 208, 248)]                  # barst (licht dat erdoor valt), glans erlangs
ART_CX, ART_CY, ART_RX, ART_RY = 120, 80, 46, 40                 # het heldere midden (daar komt Articuno)


def art_code(i):
    """Codekleur van groeifase i (palet 13; C zet de echte kleur)."""
    return (8 + i * 8, 64 + (i % 4) * 32, 248 - i * 8)


def articuno():
    rnd = random.Random(11)
    T = np.full((160, 240), np.inf)

    def put(x, y, t):
        ix, iy = int(x), int(y)
        if 0 <= ix < 240 and 0 <= iy < 160:
            T[iy, ix] = min(T[iy, ix], t)

    def grow(x, y, ang, length, t0, depth):
        for s in range(int(length)):
            x += math.cos(ang)
            y += math.sin(ang)
            ang += rnd.uniform(-0.07, 0.07)
            if not (0 <= x < 240 and 0 <= y < 160):
                return
            t = t0 + s
            put(x, y, t)
            if depth == 0:
                put(x + math.sin(ang), y - math.cos(ang), t + 1)
            if depth < 2 and s % 6 == 3 and s > 2:
                for side in (-1, 1):
                    if rnd.random() < 0.8:
                        grow(x, y, ang + side * math.pi / 3, length * rnd.uniform(0.18, 0.32), t, depth + 1)

    # varens vanaf de vier randen, schuin naar binnen
    for x in range(4, 240, 15):
        grow(x + rnd.uniform(-4, 4), 0, math.pi / 2 + rnd.uniform(-0.5, 0.5), rnd.uniform(36, 70), rnd.uniform(0, 8), 0)
        grow(x + rnd.uniform(-4, 4), 159, -math.pi / 2 + rnd.uniform(-0.5, 0.5), rnd.uniform(36, 70), rnd.uniform(0, 8), 0)
    for y in range(4, 160, 15):
        grow(0, y + rnd.uniform(-4, 4), rnd.uniform(-0.5, 0.5), rnd.uniform(40, 80), rnd.uniform(0, 8), 0)
        grow(239, y + rnd.uniform(-4, 4), math.pi + rnd.uniform(-0.5, 0.5), rnd.uniform(40, 80), rnd.uniform(0, 8), 0)
    # rijp: losse ijskorrels die later komen, dichter bij de rand
    yy, xx = np.mgrid[0:160, 0:240]
    dedge = np.minimum(np.minimum(xx, 239 - xx), np.minimum(yy, 159 - yy)).astype(float)
    noise = np.array([[rnd.random() for _ in range(240)] for _ in range(160)])
    frost = (noise < 0.04 + 0.26 * np.clip(1 - dedge / 40, 0, 1)) & ~np.isfinite(T)
    T[frost] = dedge[frost] * 1.15 + 14 + noise[frost] * 16
    # spiegelen (linksboven is de bron): gespiegelde tiles worden ontdubbeld, ±4x zo weinig tiles
    T[:, 120:] = T[:, :120][:, ::-1]
    T[80:] = T[:80][::-1]
    noise[:, 120:] = noise[:, :120][:, ::-1]
    noise[80:] = noise[:80][::-1]
    # het midden (ellips) blijft vrij tot het eind: fase 14 (rand) en 15 (binnen)
    e = ((xx - ART_CX) / ART_RX) ** 2 + ((yy - ART_CY) / ART_RY) ** 2
    ph = np.zeros((160, 240), int)
    fin = np.isfinite(T)
    out = fin & (e >= 1)
    q = np.quantile(T[out], np.linspace(0, 1, 14)[1:-1])
    ph[out] = 1 + np.searchsorted(q, T[out])
    ph[fin & (e < 1)] = 14
    inner = (e < 0.8) & (noise < 0.55)
    ph[inner & (ph == 0)] = 15
    ph[(e < 1) & (e >= 0.8) & (noise < 0.45) & (ph == 0)] = 14
    GEN['ART_PHASES'] = 15
    # VORST: codekleuren
    a = np.zeros((160, 240, 3), np.uint8)
    a[:] = KEY
    for i in range(1, 16):
        a[ph == i] = art_code(i)
    vorst = Image.fromarray(a)
    # BARST: barsten van het midden naar buiten (in de 'oude' ijskleuren van palet 14)
    crack = np.zeros((160, 240), int)
    for k in range(6):
        ang = k * 2 * math.pi / 6 + rnd.uniform(-0.25, 0.25)
        x, y = ART_CX + rnd.uniform(-6, 6), ART_CY + rnd.uniform(-6, 6)
        L = rnd.uniform(60, 140)
        for s in range(int(L)):
            x += math.cos(ang)
            y += math.sin(ang)
            ang += rnd.uniform(-0.35, 0.35) if s % 5 == 0 else 0
            ix, iy = int(x), int(y)
            if 0 <= ix < 240 and 0 <= iy < 160:
                crack[iy, ix] = 1
                if 0 <= iy - 1 and crack[iy - 1, ix] == 0:
                    crack[iy - 1, ix] = 2
    b = a.copy()
    ctile = np.zeros((20, 30), bool)
    for ty in range(20):
        for tx in range(30):
            ctile[ty, tx] = crack[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].any()
    for ty in range(20):
        for tx in range(30):
            if not ctile[ty, tx]:
                continue
            sl = (slice(ty * 8, ty * 8 + 8), slice(tx * 8, tx * 8 + 8))
            sub, ps, cr = b[sl], ph[sl], crack[sl]
            for i in range(1, 16):
                sub[ps == i] = ART_ICE[i % 3]
            sub[cr == 2] = ART_CRACK[1]
            sub[cr == 1] = ART_CRACK[0]
    barst = Image.fromarray(b)
    enc = Encoder('articuno', [[art_code(i) for i in range(1, 16)], ART_ICE + ART_CRACK, [(248, 248, 248)]], prefix=PFX)
    enc.add(vorst, 0, 'vorst')
    enc.add(barst, None, 'barst')
    enc.save()
    # voorbeeld: alles bevroren
    show = a.copy()
    for i in range(1, 16):
        show[ph == i] = ART_ICE[i % 3]
    save_preview('articuno', [vorst, Image.fromarray(show), barst])


# ================================================================== Zapdos
def zapdos():
    base = render_map('LAYOUT_ROUTE119', 0, 22)
    cap = base.copy()
    d = ImageDraw.Draw(cap)
    d.rectangle((0, 144, 239, 159), fill=(8, 8, 8))
    d.rectangle((0, 144, 239, 144), fill=(248, 216, 64))
    s = 'FORECAST: 100% ZAPDOS'
    text(cap, 120 - text_width(s) // 2, 144, s, (248, 248, 248), (88, 88, 104))
    pals = quantize3([base], n=5) + [[(8, 8, 8), (248, 248, 248), (88, 88, 104), (248, 216, 64)]]
    enc = EncoderN('zapdos', pals, 10)
    enc.add(base, None, 'instituut')
    enc.add(cap, None, 'onderschrift')
    enc.save()
    save_preview('zapdos', [base, cap, enc.render(enc.maps[1])])


# ================================================================== Moltres
def moltres():
    base = render_map('LAYOUT_MT_CHIMNEY_SUMMIT', 10, 0)
    pals = quantize3([base], n=6)
    enc = EncoderN('moltres', pals, 10)
    enc.add(base, None, 'krater')
    enc.save()
    # lava-kleuren (rood/oranje) per palet, voor de paletcyclus in C
    lava = []
    for k, pal in enumerate(enc.pals):
        for i, c in enumerate(pal[1:], 1):
            if c[0] >= 200 and c[1] <= 150 and c[2] <= 80:
                lava.append((enc.base + k) * 16 + i)
    GEN['MOL_LAVA'] = lava
    print('  moltres: lava-indexen', lava)
    save_preview('moltres', [base, enc.render(enc.maps[0])])


# ================================================================== Zacian / Zamazenta
WOLF_CRACK = [(248, 248, 248), (200, 216, 240), (120, 136, 168)]   # barsten in het "glas" (palet 15)


def wolf_cracks(stage, rnd_seed=4):
    """Barsten vanuit het midden (Zamazenta's schild klapt tegen het scherm); stage 1-3 groeit, 3 = heel het beeld."""
    rnd = random.Random(rnd_seed)
    im = Image.new('RGB', (240, 160), KEY)
    d = ImageDraw.Draw(im)
    cx, cy = 120, 80
    n = 9
    frac = {1: 0.2, 2: 0.45, 3: 1.0}[stage]
    for k in range(n):
        ang = k * 2 * math.pi / n + rnd.uniform(-0.2, 0.2)
        x, y = cx + math.cos(ang) * 6, cy + math.sin(ang) * 6
        L = 190 * rnd.uniform(0.75, 1.0)
        pts = [(x, y)]
        s_ = 0
        while s_ < L:                       # hele pad (stage 3), dan afkappen: de barsten groeien per klap door
            st = rnd.uniform(6, 12)
            ang += rnd.uniform(-0.35, 0.35)
            x += math.cos(ang) * st
            y += math.sin(ang) * st
            s_ += st
            pts.append((x, y))
        pts = pts[:max(2, int(len(pts) * frac))]
        d.line(pts, fill=WOLF_CRACK[1], width=2)
        d.line(pts, fill=WOLF_CRACK[0], width=1)
    # ringen (spinnenweb) vanaf stage 2
    for r, st in ((22, 2), (48, 3), (78, 3)):
        if stage < st:
            continue
        pts = []
        for k in range(n + 1):
            a = k * 2 * math.pi / n
            rr = r * rnd.uniform(0.85, 1.15)
            pts.append((cx + math.cos(a) * rr * 1.2, cy + math.sin(a) * rr))
        d.line(pts, fill=WOLF_CRACK[2], width=1)
    # inslagpunt
    d.ellipse((cx - 5, cy - 4, cx + 5, cy + 4), fill=WOLF_CRACK[1])
    d.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=WOLF_CRACK[0])
    return im


def wolves():
    """De open plek (palet 10-14) en drie barst-stadia over een zwart scherm (palet 15, de rest doorzichtig)."""
    base = render_map('LAYOUT_MEGA_FOREST', 16, 0)
    pals = quantize3([base], n=5) + [WOLF_CRACK]
    enc = EncoderN('wolves', pals, 10)
    enc.add(base, None, 'open_plek')
    cracks = [wolf_cracks(k) for k in (1, 2, 3)]
    for k, im in enumerate(cracks):
        enc.add(im, None, 'barst%d' % (k + 1))
    enc.save()
    save_preview('wolves', [base, enc.render(enc.maps[0])] + [enc.render(m) for m in enc.maps[1:]])


# ------------------------------------------------------------------ grote objecten (128 x 128, vier 64x64-sprites)
def scale2x_idx(a):
    h, w = a.shape
    p = np.pad(a, 1, mode='edge')
    B, D, E, F, H = p[:-2, 1:-1], p[1:-1, :-2], p[1:-1, 1:-1], p[1:-1, 2:], p[2:, 1:-1]
    o = np.zeros((h * 2, w * 2), a.dtype)
    c = (B != H) & (D != F)
    o[0::2, 0::2] = np.where(c & (D == B), D, E)
    o[0::2, 1::2] = np.where(c & (B == F), F, E)
    o[1::2, 0::2] = np.where(c & (D == H), D, E)
    o[1::2, 1::2] = np.where(c & (H == F), F, E)
    return o


def save_big(name, idx, pal, extra_pals=()):
    """idx: 128 x 128 indexbeeld -> legend_<name>.png (64 x 256: de kwadranten LB, RB, LO, RO onder elkaar) + .pal;
    extra_pals: (achtervoegsel, palet) voor andere toestanden (C mengt ertussen)."""
    assert idx.shape == (128, 128) and idx.max() < 16
    sheet = np.concatenate([idx[:64, :64], idx[:64, 64:], idx[64:, :64], idx[64:, 64:]], 0).astype(np.uint8)
    im = Image.fromarray(sheet, 'P')
    full = [(0, 0, 0)] + [gba(c) for c in pal] + [(0, 0, 0)] * (15 - len(pal))
    im.putpalette([v for c in full for v in c] + [0] * (768 - 48))
    im.save(OUT + PFX + name + '.png')
    write_pal(OUT + PFX + name + '.pal', full)
    for suf, p in extra_pals:
        write_pal(OUT + PFX + name + '_' + suf + '.pal', [(0, 0, 0)] + [gba(c) for c in p] + [(0, 0, 0)] * (15 - len(p)))


def big_preview(idx, pal):
    full = np.array([(255, 0, 255)] + list(pal) + [(0, 0, 0)] * (15 - len(pal)), np.uint8)
    return Image.fromarray(full[idx])


# Rusted Sword / Rusted Shield (item-icoon x4 met Scale2x); index: 1-4 grijs (kling / binnenkant), 5 rand, 6-9 roest
# (kling / binnenkant), 10-13 grijs (gevest / schildrand), 14-15 roest (gevest / schildrand)
RUST = [(136, 128, 128), (112, 112, 112), (88, 88, 88), (64, 64, 64), (40, 36, 40), (184, 96, 88), (152, 72, 72),
        (120, 56, 56), (80, 40, 40), (136, 128, 128), (112, 112, 112), (88, 88, 88), (64, 64, 64), (152, 72, 72),
        (80, 40, 40)]
SWORD_CLEAN = [(232, 240, 248), (184, 208, 240), (120, 160, 216), (64, 104, 168), (24, 32, 64), (248, 248, 248),
               (200, 224, 248), (136, 184, 232), (72, 120, 184), (248, 240, 176), (240, 216, 136), (208, 152, 80),
               (136, 72, 40), (208, 152, 80), (136, 72, 40)]
SHIELD_CLEAN = [(240, 104, 112), (216, 56, 64), (168, 40, 48), (112, 24, 32), (48, 16, 24), (248, 248, 200),
                (240, 216, 136), (208, 152, 80), (152, 96, 48), (248, 240, 176), (240, 216, 136), (208, 152, 80),
                (136, 72, 40), (208, 152, 80), (136, 72, 40)]


def rusted(name):
    im = Image.open(os.path.join(ROOT, 'graphics/items/icons/%s.png' % name))
    a = np.array(im).astype(int)          # 0 leeg, 1-4 grijs, 5 rand, 6-9 roest (zelfde volgorde als RUST)
    a[a > 9] = 0
    big = scale2x_idx(scale2x_idx(a))     # 96 x 96
    yy, xx = np.mgrid[0:96, 0:96] / 4.0
    if name == 'rusted_sword':
        # kling = linksonder, voorbij het kruisstuk; gevest en kruisstuk rechtsboven
        s_ = ((13.5 - xx) + (yy - 9.5)) / math.sqrt(2)
        hilt = s_ <= 2.3
    else:
        # schildrand: binnen 2 px (op 96) van de buitenkant
        solid = big > 0
        m = solid.copy()
        for _ in range(9):
            m = m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)
        hilt = solid & ~m
    out = big.copy()
    grey = (big >= 1) & (big <= 4)
    rust = big >= 6
    out[grey & hilt] = big[grey & hilt] + 9          # 10-13
    out[rust & hilt] = np.where(big[rust & hilt] <= 7, 14, 15)
    canvas = np.zeros((128, 128), int)
    canvas[16:112, 16:112] = out
    return canvas


def flakes():
    """Vier roestschilfers (16 x 16) voor als de roest eraf valt."""
    rnd = random.Random(3)
    a = np.zeros((64, 16), np.uint8)
    for f in range(4):
        cx, cy = 7 + rnd.randint(-1, 1), f * 16 + 7
        for k in range(5 + f):
            x, y = cx + rnd.randint(-3, 3), cy + rnd.randint(-2, 2)
            a[y, x] = 1 + (k % 3)
            if k % 2:
                a[y, x + 1] = 2
    im = Image.fromarray(a, 'P')
    pal = [(0, 0, 0), (184, 96, 88), (120, 56, 56), (80, 40, 40)] + [(0, 0, 0)] * 12
    im.putpalette([v for c in pal for v in c] + [0] * (768 - 48))
    im.save(OUT + PFX + 'rust_flakes.png')
    write_pal(OUT + PFX + 'rust_flakes.pal', pal)


def weapons():
    sw = rusted('rusted_sword')
    sh = rusted('rusted_shield')
    save_big('sword', sw, RUST, [('clean', SWORD_CLEAN)])
    save_big('shield', sh, RUST, [('clean', SHIELD_CLEAN)])
    flakes()
    if PREVIEW:
        ims = [big_preview(sw, RUST), big_preview(sw, SWORD_CLEAN), big_preview(sh, RUST), big_preview(sh, SHIELD_CLEAN)]
        W = Image.new('RGB', (4 * 132, 128), (40, 40, 40))
        for i, x in enumerate(ims):
            W.paste(x, (i * 132, 0))
        W.resize((W.width * 2, W.height * 2), Image.NEAREST).save(os.path.join(PREVIEW, 'legend_weapons.png'))


# ------------------------------------------------------------------ de Y van Yveltal en de X van Xerneas
# Y: index 1 rand, 2 lijf (zwart), 3 donkergrijs, 4 grijs (veerpunten), 5 rood, 6 donkerrood, 7 rode gloed
Y_PAL = [(16, 16, 24), (40, 40, 48), (72, 72, 80), (136, 136, 144), (216, 40, 56), (136, 24, 40), (248, 104, 112)]
Y_DARK = [(16, 16, 24), (40, 40, 48), (72, 72, 80), (136, 136, 144), (40, 40, 48), (40, 40, 48), (56, 48, 56)]
# X: 1 rand, 2 donkerblauw, 3 blauw, 4 lichtblauw, 5 zwart (de strepen in het gewei), 6 wit (glans),
#    7-10 de lichtjes van de Active Mode (geel, paars, rood, blauw; C laat ze rondgaan)
X_PAL = [(16, 24, 56), (32, 56, 120), (56, 104, 192), (136, 192, 248), (24, 24, 40), (248, 248, 248),
         (248, 216, 64), (176, 96, 224), (232, 64, 72), (72, 160, 248)]
X_DIM = [(16, 16, 24), (48, 52, 64), (72, 76, 88), (104, 108, 120), (24, 24, 32), (120, 124, 136),
         (64, 64, 72), (64, 64, 72), (64, 64, 72), (64, 64, 72)]


def _outline(a):
    """Rand van 1 px (index 1) rond alle gevulde pixels (zonder om de randen heen te lopen)."""
    a[0, :] = a[-1, :] = a[:, 0] = a[:, -1] = 0
    m = a > 0
    g = m.copy()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        g |= np.roll(np.roll(m, dy, 0), dx, 1)
    a[g & ~m] = 1
    return a


def _taper(d, x0, y0, x1, y1, w0, w1, fill):
    """Taps toelopende balk van (x0, y0) (breedte w0) naar (x1, y1) (breedte w1)."""
    L = math.hypot(x1 - x0, y1 - y0) or 1
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    d.polygon([(x0 + nx * w0 / 2, y0 + ny * w0 / 2), (x1 + nx * w1 / 2, y1 + ny * w1 / 2),
               (x1 - nx * w1 / 2, y1 - ny * w1 / 2), (x0 - nx * w0 / 2, y0 - ny * w0 / 2)], fill=fill)


def y_symbol():
    im = Image.new('P', (128, 128), 0)
    d = ImageDraw.Draw(im)
    for side in (-1, 1):
        X = lambda x: 64 + side * (x - 64)
        # arm van de vleugel: van de schouder schuin omhoog naar buiten
        _taper(d, X(60), 56, X(22), 18, 18, 8, 2)
        # slagpennen: lange veren die naar buiten waaieren (Yveltal's "hand"), de buitenste het langst
        for (bx, by, ex, ey, w) in [(30, 26, 4, 4, 7), (26, 22, 14, 0, 6), (34, 30, 2, 18, 6), (42, 38, 8, 34, 6),
                                    (50, 46, 18, 50, 5)]:
            _taper(d, X(bx), by, X(ex), ey, w, 1, 2)
            _taper(d, X(bx), by, X(ex), ey, max(w - 4, 1), 1, 3)
        # rode band langs de onderkant van de arm
        _taper(d, X(58), 62, X(26), 26, 6, 2, 5)
        _taper(d, X(58), 64, X(40), 44, 3, 1, 6)
    # lijf en staart: smal naar beneden, met een rode punt
    d.polygon([(54, 48), (74, 48), (74, 62), (69, 90), (66, 110), (64, 124), (62, 110), (59, 90), (54, 62)], fill=2)
    d.line([(64, 52), (64, 100)], fill=3, width=1)
    d.polygon([(60, 98), (68, 98), (66, 112), (64, 122), (62, 112)], fill=5)
    d.polygon([(63, 104), (65, 104), (64, 116)], fill=7)
    # rode kraag en "kop" tussen de schouders
    d.polygon([(54, 48), (64, 58), (74, 48), (70, 62), (64, 66), (58, 62)], fill=6)
    d.polygon([(60, 40), (68, 40), (66, 50), (62, 50)], fill=2)
    a = np.array(im).astype(int)
    # grijze punten aan de veren (waar de taps toelopende veer eindigt)
    return _outline(a)


def x_symbol():
    im = Image.new('P', (128, 128), 0)
    d = ImageDraw.Draw(im)
    lights = []
    for flip in (False, True):
        X = lambda x: (127 - x) if flip else x
        # de balken: breed in het midden, smal naar de punten
        for (x0, y0, x1, y1) in [(64, 64, 10, 10), (64, 64, 118, 118)]:
            _taper(d, X(x0), y0, X(x1), y1, 16, 6, 2)
            _taper(d, X(x0), y0, X(x1), y1, 8, 2, 3)
        # geweitakken: taps toelopend, naar buiten gebogen, met een lichtje op de punt
        for (bx, by, ex, ey) in [(26, 26, 4, 34), (26, 26, 34, 4), (40, 40, 18, 54), (40, 40, 54, 18),
                                 (102, 102, 124, 94), (102, 102, 94, 124), (88, 88, 110, 74), (88, 88, 74, 110)]:
            _taper(d, X(bx), by, X(ex), ey, 7, 2, 2)
            _taper(d, X(bx), by, X(ex), ey, 3, 1, 3)
            lights.append((X(ex), ey))
        # zwarte strepen in het gewei
        for k in (0.18, 0.32, 0.68, 0.82):
            x, y = 10 + k * 108, 10 + k * 108
            d.line([(X(x - 4), y + 4), (X(x + 4), y - 4)], fill=5, width=2)
    for j, (x, y) in enumerate(lights):
        d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=7 + j % 4)
        d.point((x - 1, y - 1), fill=6)
    # glans in het midden (vierpuntige ster)
    d.polygon([(64, 48), (67, 61), (80, 64), (67, 67), (64, 80), (61, 67), (48, 64), (61, 61)], fill=6)
    d.polygon([(64, 56), (66, 62), (72, 64), (66, 66), (64, 72), (62, 66), (56, 64), (62, 62)], fill=4)
    return _outline(np.array(im).astype(int))


def symbols():
    y = y_symbol()
    x = x_symbol()
    save_big('ysym', y, Y_PAL, [('dark', Y_DARK)])
    save_big('xsym', x, X_PAL, [('dim', X_DIM)])
    if PREVIEW:
        ims = [big_preview(y, Y_DARK), big_preview(y, Y_PAL), big_preview(x, X_DIM), big_preview(x, X_PAL)]
        W = Image.new('RGB', (4 * 132, 128), (40, 40, 40))
        for i, im in enumerate(ims):
            W.paste(im, (i * 132, 0))
        W.resize((W.width * 2, W.height * 2), Image.NEAREST).save(os.path.join(PREVIEW, 'legend_symbols.png'))


# ================================================================== Xerneas / Yveltal (leven en dood)
def glim(name, layout, x0, y0):
    """Kleurbeeld in palet 13-15; de uitgedoofde versie gebruikt dezelfde tiles met palet 10-12 (in C per vak)."""
    col = render_map(layout, x0, y0)
    dim = render_map(layout + '_DYING', x0, y0)
    pals = quantize3([col], n=6)
    enc = EncoderN(name, pals, 10)
    m = enc.add(col, None, 'kleur')
    enc.save()
    P, I = screen_index(enc, m)
    da = np.array(dim).astype(np.int64)
    out = []
    for k in range(6):
        cols = [(0, 0, 0)]
        for i in range(1, 16):
            msk = (P == enc.base + k) & (I == i)
            if msk.any():
                u, cnt = np.unique(da[msk], axis=0, return_counts=True)
                cols.append(gba(u[cnt.argmax()]))   # de meest voorkomende uitgedoofde kleur
            else:
                cols.append(gba(np.array(enc.pals[k][i]) * 0.45))
        out += cols
    write_pal(OUT + '%s%s_dying.pal' % (PFX, name), out)
    dimr = enc.render(m, pals=[out[k * 16:(k + 1) * 16] for k in range(6)])
    save_preview(name, [col, enc.render(m), dimr])


def xerneas():
    glim('xerneas', 'LAYOUT_GLIMWOOD_TANGLE_BALLONLEA', 10, 0)


def yveltal():
    glim('yveltal', 'LAYOUT_GLIMWOOD_TANGLE', 15, 23)


def write_gen():
    p = os.path.join(ROOT, 'src/data/legend_intros2_gen.h')
    old = {}
    if os.path.exists(p):
        for l in open(p):
            if l.startswith('// GEN '):
                k, v = l[7:].split(' = ', 1)
                old[k] = json.loads(v)
    old.update(GEN)
    L = ['// Gegenereerd door tools/grounded/legend_intros2.py: niet met de hand bewerken.']
    for k in sorted(old):
        v = old[k]
        L.append('// GEN %s = %s' % (k, json.dumps(v)))
        if isinstance(v, list):
            L.append('#define %s_COUNT %d' % (k, len(v)))
            L.append('static const u8 s%s[] = {%s}; // BG-paletindex (palet * 16 + kleur)' % (''.join(w.capitalize() for w in k.split('_')), ', '.join(str(x) for x in v)))
        else:
            L.append('#define %s %d' % (k, v))
    open(p, 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    names = [a for a in sys.argv[1:] if a.isalpha()] or ['articuno', 'zapdos', 'moltres', 'wolves', 'xerneas', 'yveltal']
    for n in names:
        globals()[n]()
    write_gen()
