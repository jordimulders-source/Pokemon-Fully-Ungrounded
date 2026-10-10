#!/usr/bin/env python3
"""Project Grounded: gevechtsintro's van Dialga, Palkia, Arceus en Mew (C: src/data/legend_intros_dp.h).
Zelfde aanpak als legend_intros2.py: een paar stilstaande BG0-beelden, de beweging in C (sprites, paletcycli,
tilemapmenging, HBlank-DMA). Alle vier lopen op de maat van hun muziek (gMain.vblankCounter1).

Uitvoer in graphics/battle_transitions/legend_dp_*.png/.pal(/_maps.bin) en src/data/legend_intros_dp_gen.h.
- dp_spiral:  tijd/ruimte-tunnel (twee armen, 180 graden symmetrisch: de onderste helft is de bovenste, gespiegeld).
              Index 1-14 = fase langs de spiraal (C draait het palet rond), 15 = de kern. Dialga (blauw) en Palkia
              (roze) delen hem. De klok van Dialga is de echte wandklok uit de slaapkamer (gWallClock_*, staat al in
              de ROM), dus die kost niets.
- dp_cities:  Palkia: echte kaartuitsneden van Littleroot, Petalburg, Fortree, Mossdeep, Sootopolis en Spear Pillar,
              samen in 12 BG-paletten (4-15; de wereld staat dan uit).
- dp_arceus:  Arceus: heilig licht (vignet, index = afstand tot de rand) en stralenkrans (index = hoek; C draait het
              palet rond). dp_arceus_sym: het Arceus-teken (vector uit Jordi's plaatje), 128x128 als vier sprites.
- dp_mew:     Mew: Guyana bij zonsopgang (tepui met een waterval à la Kaieteur, regenwoud, rivier, nevel), 256 px
              breed en naadloos, zodat C de lagen per beeldlijn met eigen snelheid kan laten schuiven (parallax).
              dp_mew_tail: Mews echte staart, uitgeknipt uit zijn frontsprite.
Gebruik: python3 tools/grounded/legend_intros_dp.py [voorbeeldmap] [naam ...]"""
import math, os, struct, sys, zlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image, ImageDraw

_ARGS = sys.argv[1:]
sys.argv = sys.argv[:1]          # legend_intros2 leest sys.argv bij het importeren
import legend_intros2 as L2
from gym_intro_lib import OUT, KEY, gba, ROOT, preview_strip

PREVIEW = _ARGS[0] if _ARGS and not _ARGS[0].isalpha() else None
PFX = 'legend_dp_'
GEN = {}


def write_pal(path, cols):
    L2.write_pal(path, [gba(c) for c in cols])


class IndexEncoder:
    """Indexbeelden (0 = doorzichtig) naar tiles + tilemaps, ontdubbeld met spiegelen. Palet per beeld vast."""
    def __init__(self, name):
        self.name = name
        self.tiles = [np.zeros(64, np.uint8)]
        self.index = {self.tiles[0].tobytes(): 0}
        self.maps = []

    def _tile(self, t):
        for flip in range(4):
            u = t
            if flip & 1:
                u = u[:, ::-1]
            if flip & 2:
                u = u[::-1]
            k = np.ascontiguousarray(u).reshape(64).astype(np.uint8).tobytes()
            if k in self.index:
                return self.index[k] | (flip << 10)
        n = len(self.tiles)
        self.tiles.append(t.reshape(64).astype(np.uint8))
        self.index[self.tiles[-1].tobytes()] = n
        return n

    def add(self, idx, pal, label=''):
        n0 = len(self.tiles)
        H, W = idx.shape[0] // 8, idx.shape[1] // 8
        out = []
        for ty in range(H):
            for tx in range(W):
                t = idx[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
                out.append(0 if not t.any() else self._tile(t) | (pal << 12))
        self.maps.append(out)
        print('  %s %s: +%d tiles' % (self.name, label, len(self.tiles) - n0))
        return out

    def save(self, pal_cols):
        cols = 16
        rows = (len(self.tiles) + cols - 1) // cols
        img = Image.new('P', (cols * 8, rows * 8))
        for i, t in enumerate(self.tiles):
            img.paste(Image.fromarray(t.reshape(8, 8)), ((i % cols) * 8, (i // cols) * 8))
        full = [(0, 0, 0)] + [gba(c) for c in pal_cols][:15]
        full += [(0, 0, 0)] * (16 - len(full))
        img.putpalette([v for c in full for v in c] + [0] * (768 - 48))
        img.save(OUT + PFX + self.name + '.png')
        write_pal(OUT + PFX + self.name + '.pal', full)
        allm = sum(self.maps, [])
        open(OUT + PFX + self.name + '_maps.bin', 'wb').write(struct.pack('<%dH' % len(allm), *allm))
        print('%s: %d tiles' % (self.name, len(self.tiles)))
        GEN['DP_%s_TILES' % self.name.upper()] = len(self.tiles)


def bayer(n=4):
    b = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0
    return b


def save_preview(name, imgs, cols=3):
    if PREVIEW:
        preview_strip(imgs, os.path.join(PREVIEW, 'legend_dp_%s.png' % name), k=2, cols=cols)


def idx_preview(idx, pal):
    full = np.array([(0, 0, 0)] + list(pal) + [(0, 0, 0)] * (15 - len(pal)), np.uint8)
    return Image.fromarray(full[idx])


# ================================================================== tunnel (Dialga en Palkia)
SPIRAL_PREVIEW = [(8, 16, 40), (16, 32, 72), (32, 64, 120), (64, 104, 168), (120, 168, 216), (200, 232, 248),
                  (248, 248, 248), (160, 208, 240), (96, 144, 200), (48, 88, 144), (24, 48, 96), (16, 24, 64),
                  (8, 16, 48), (8, 16, 40), (255, 255, 255)]


def spiral():
    H, W = 160, 240
    y, x = np.mgrid[0:H, 0:W]
    dx, dy = x + 0.5 - 120, y + 0.5 - 80
    r = np.hypot(dx, dy)
    th = np.arctan2(dy, dx)
    # twee armen; log(r) maakt de ringen naar buiten toe breder (perspectief)
    ph = (np.log(r + 2.0) * 2.4 + 2 * th / (2 * math.pi)) % 1.0
    idx = (1 + np.floor(ph * 14)).astype(np.uint8)
    idx[r < 5] = 15
    enc = IndexEncoder('spiral')
    enc.add(idx, 0, 'tunnel')
    enc.save(SPIRAL_PREVIEW)
    save_preview('spiral', [idx_preview(idx, SPIRAL_PREVIEW)])


# ================================================================== Palkia: vijf steden en Spear Pillar
CITIES = [('LAYOUT_LITTLEROOT_TOWN', 0, 4), ('LAYOUT_PETALBURG_CITY', 6, 2), ('LAYOUT_FORTREE_CITY', 14, 0),
          ('LAYOUT_MOSSDEEP_CITY', 56, 1), ('LAYOUT_SOOTOPOLIS_CITY', 23, 25), ('LAYOUT_SPEAR_PILLAR', 10, 11)]


def cities():
    imgs = [L2.render_map(l, x, y) for l, x, y in CITIES]
    pals = L2.quantize3(imgs, n=12, shared=2)
    enc = L2.EncoderN('cities', pals, 4, prefix=PFX)
    maps = [enc.add(im, None, l) for im, (l, _, _) in zip(imgs, CITIES)]
    enc.save()
    GEN['DP_CITIES_TILES'] = len(enc.tiles)
    save_preview('cities', [enc.render(m) for m in maps])


# ================================================================== Arceus
VIGNETTE_PREVIEW = [(248, 240, 200)] * 15
RAYS_PREVIEW = [(248, 248, 248), (248, 240, 200), (240, 216, 136), (248, 240, 200), (248, 248, 248)] * 3


def arceus():
    H, W = 160, 240
    y, x = np.mgrid[0:H, 0:W]
    dx, dy = x + 0.5 - 120, y + 0.5 - 80
    # heilig licht: superellips (p = 3) van het midden naar de hoeken; 1 = binnenste band, 15 = hoek
    s = ((np.abs(dx) / 132) ** 3 + (np.abs(dy) / 92) ** 3) ** (1 / 3)
    qx, qy = np.where(x < 120, x, 239 - x), np.where(y < 80, y, 159 - y)
    b = bayer()[qy % 4, qx % 4]                      # gespiegeld: vier kwarten met dezelfde tiles
    v = (s - 0.30) / 0.72 * 15 + (b - 0.5) * 1.2
    vig = np.clip(np.floor(v) + 1, 0, 15).astype(np.uint8)
    vig[v < 0] = 0
    # stralenkrans: 30 stralen (15 indexen, tegenover elkaar dezelfde); dither op de grens
    th = (np.arctan2(dy, dx) / (2 * math.pi)) % 1.0
    bot = y >= 80                                    # 180 graden gedraaid: zelfde tiles, beide kanten gespiegeld
    rx, ry = np.where(bot, 239 - x, x), np.where(bot, 159 - y, y)
    b2 = bayer()[ry % 4, rx % 4]
    ray = th * 30 + (b2 - 0.5) * 0.35 * np.clip(np.hypot(dx, dy) / 40, 0, 1)
    rays = (1 + (np.floor(ray).astype(int) % 15)).astype(np.uint8)
    enc = IndexEncoder('arceus')
    enc.add(vig, 13, 'licht')
    enc.add(rays, 14, 'stralen')
    enc.save(VIGNETTE_PREVIEW)
    save_preview('arceus', [idx_preview(vig, [(int(255 * min(1, i / 15)),) * 3 for i in range(1, 16)]),
                            idx_preview(rays, RAYS_PREVIEW)])
    symbol()


# het teken: 1 omlijning, 2-6 goud (licht -> donker), 7 glans, 8 binnenrand
SYM_PAL = [(80, 48, 8), (248, 232, 144), (240, 208, 96), (216, 176, 64), (184, 136, 40), (144, 100, 24),
           (255, 255, 224), (112, 72, 16)]


def symbol():
    src = os.path.join(ROOT, 'tools/grounded/art/arceus_symbol.png')
    im = np.array(Image.open(src).convert('RGB')).astype(float)
    # goud op wit: alles wat duidelijk niet wit is
    m = (im.max(2) - im.min(2) > 40) | (im.mean(2) < 200)
    ys, xs = np.nonzero(m)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    m = m[y0:y1, x0:x1]
    h, w = m.shape
    S = 118
    k = S / max(h, w)
    nh, nw = int(round(h * k)), int(round(w * k))
    small = np.array(Image.fromarray((m * 255).astype(np.uint8)).resize((nw * 4, nh * 4), Image.LANCZOS)
                     .resize((nw, nh), Image.BOX)) / 255.0
    mask = np.zeros((128, 128), bool)
    oy, ox = (128 - nh) // 2, (128 - nw) // 2
    mask[oy:oy + nh, ox:ox + nw] = small > 0.5
    # links-rechts symmetrisch maken (het teken is symmetrisch; de bron niet helemaal)
    mask = mask | mask[:, ::-1]
    idx = np.zeros((128, 128), np.uint8)
    yy, xx = np.mgrid[0:128, 0:128]
    # goud: licht linksboven, donker rechtsonder
    g = ((xx - ox) / nw * 0.45 + (yy - oy) / nh * 0.55)
    ramp = np.clip((g * 5).astype(int), 0, 4) + 2
    idx[mask] = ramp[mask]
    # binnenrand (rechtsonder van elke vorm) en glans (linksboven)
    def sh(a, dy, dx):
        return np.roll(np.roll(a, dy, 0), dx, 1)
    lo = mask & ~(sh(mask, -1, -1) & sh(mask, -1, 0) & sh(mask, 0, -1))
    hi = mask & ~(sh(mask, 1, 1) & sh(mask, 1, 0) & sh(mask, 0, 1))
    idx[lo] = 8
    idx[hi & ~lo] = 7
    out = np.zeros_like(mask)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        out |= sh(mask, dy, dx)
    idx[out & ~mask] = 1
    idx[0, :] = idx[-1, :] = idx[:, 0] = idx[:, -1] = 0
    L2.PFX, old = PFX, L2.PFX
    L2.save_big('arceus_sym', idx, SYM_PAL)
    L2.PFX = old
    if PREVIEW:
        im = L2.big_preview(idx, SYM_PAL)
        im.resize((512, 512), Image.NEAREST).save(os.path.join(PREVIEW, 'legend_dp_arceus_sym.png'))


# ================================================================== Mew: Guyana
# vaste lagen (per beeldlijn een eigen snelheid in C): lucht + tepui's, ver woud (onder de nevel), rivier, dichtbij.
# Binnen een laag is alles wat over de grens kijkt horizontaal egaal (lucht, nevel), zodat het schuiven niet opvalt.
MEW_BANDS = [0, 88, 108, 126, 160]


def _wrapd(x, cx, W):
    return (x - cx + W / 2) % W - W / 2


def _per(x, W, seed, terms=4, amp=1.0):
    """Naadloze ruis met periode W."""
    r = np.random.RandomState(seed)
    v = np.zeros_like(x, dtype=float)
    for k in range(1, terms + 1):
        v += np.sin(2 * math.pi * x * (k * 3 + r.randint(0, 3)) / W + r.uniform(0, 6.3)) / k
    return v * amp


def _dith(v, levels, B):
    """v in [0, 1] -> 0..levels-1 met Bayer-dither."""
    return np.clip(np.floor(v * (levels - 1) + B), 0, levels - 1).astype(int)


def _mix(a, b, t):
    return np.array(a, float) * (1 - t) + np.array(b, float) * t


def mew_scene():
    W, H = 256, 160
    yy, xx = np.mgrid[0:H, 0:W]
    B = bayer()[yy % 4, xx % 4]
    img = np.zeros((H, W, 3), float)
    # lucht bij zonsopgang: 6 tinten met dither (per rij gelijk: dedupliceert goed)
    sky = [(88, 136, 200), (120, 160, 208), (160, 184, 208), (200, 200, 200), (232, 208, 184), (248, 224, 176)]
    lv = _dith(np.clip(yy / 82.0, 0, 1), len(sky), B)
    img[:] = np.array(sky, float)[lv]
    # zon: een gloed achter de kleine tepui
    sx, sy = 170, 44
    d = np.hypot(_wrapd(xx, sx, W), (yy - sy) * 1.1)
    glow = np.clip(1 - d / 34.0, 0, 1) ** 1.5
    gl = _dith(glow, 4, B)
    for k, c in ((1, (248, 232, 192)), (2, (248, 240, 208)), (3, (248, 248, 232))):
        img[gl == k] = c
    # tepui's (tafelbergen): steile wanden met richels, begroeide top, rotsstrepen; ver = blauwiger
    teps = [(64, 64, 30, 0.10, 1, 0.30), (182, 34, 46, 0.16, 7, 0.45)]
    rock_l, rock_m, rock_d = (176, 144, 144), (120, 100, 112), (72, 64, 88)
    hazec = (168, 184, 200)
    for cx, half, top, slope, seed, haze in teps:
        dxw = _wrapd(xx, cx, W)
        ledge = np.floor(_per(yy.astype(float), 64, seed, 3, 1.6) + 0.5)
        hw = half + (yy - top) * slope + ledge
        topj = top + np.round(_per(xx.astype(float), W, seed + 1, 3, 0.9))
        m = (np.abs(dxw) <= hw) & (yy >= topj) & (yy < 96)
        side = dxw / np.maximum(hw, 1)
        streak = _per(xx.astype(float), W, seed + 2, 6, 0.18)
        v = np.clip((side + streak) * 0.5 + 0.5 + (B - 0.5) * 0.25, 0, 0.999)
        k = (v * 3).astype(int)
        cols = np.array([rock_l, rock_m, rock_d], float)
        c = cols[k]
        c = c * (1 - haze) + np.array(hazec) * haze
        img[m] = c[m]
        # groene rand bovenop
        g = m & (yy < topj + 2 + (np.abs(np.sin(xx * 1.3)) > 0.6))
        img[g] = _mix((80, 120, 80), hazec, haze * 0.7)
        # bovenkant licht
        e = m & (yy == topj)
        img[e] = _mix((120, 160, 104), hazec, haze * 0.6)
    # Kaieteur: een waterval van de grote tepui, valt in de nevel (C laat de 3 tinten rondgaan)
    fall = np.zeros((H, W), np.int8)
    fx = 38
    for y in range(31, 90):
        w = 2 + (y - 31) // 12
        for x in range(fx - w // 2, fx + (w + 1) // 2):
            fall[y, x % W] = 1 + ((y // 2) + (x - fx) * 2) % 3
    # nevel aan de voet: horizontaal egaal, met dither (valt binnen de schuivende lagen weg)
    mist = np.clip((yy - 62) / 24.0, 0, 1)
    lvm = _dith(mist * 0.9, 4, B)
    mc = [None, (192, 200, 200), (208, 216, 208), (224, 228, 216)]
    for k in (1, 2, 3):
        mm = (lvm == k) & (yy < MEW_BANDS[1] + 6)
        img[mm] = _mix(img[mm], mc[k], 0.55 + 0.15 * k)
    # ver regenwoud: dichte kruinen tegen een donkere ondergroei
    def crowns(lay, y0, y1, n, rmin, rmax, seed, flat=1.0):
        r_ = np.random.RandomState(seed)
        for i in range(n):
            cx = r_.uniform(0, W)
            cy = r_.uniform(y0, y1)
            rad = r_.uniform(rmin, rmax)
            dxw = _wrapd(xx, cx, W)
            dd = dxw ** 2 + ((yy - cy) * flat) ** 2
            m = dd <= rad * rad
            lit = (-dxw * 0.55 - (yy - cy) * 0.85) / rad + (B - 0.5) * 0.55
            lay[m] = np.where(lit[m] > 0.40, 4, np.where(lit[m] > -0.05, 3, 2))
        return lay
    far = np.zeros((H, W), np.int8)
    far[(yy >= 96) & (yy < MEW_BANDS[2])] = 1
    crowns(far, 94, 104, 90, 4, 7, 11, 1.2)
    far[yy < MEW_BANDS[1]] = 0
    far[yy >= MEW_BANDS[2]] = 0
    fcol = {1: (32, 64, 56), 2: (48, 88, 64), 3: (72, 120, 72), 4: (112, 152, 88)}
    for k, c in fcol.items():
        img[far == k] = _mix(c, hazec, 0.15)
    # rivierband: oevers + water dat de lucht weerspiegelt
    rb0, rb1 = MEW_BANDS[2], MEW_BANDS[3]
    cyr = 117 + 2.5 * np.sin(2 * math.pi * xx / W * 2 + 0.8) + 1.2 * np.sin(2 * math.pi * xx / W * 3 + 2)
    hw = 4.5 + 1.2 * np.sin(2 * math.pi * xx / W + 2)
    band = (yy >= rb0) & (yy < rb1)
    img[band] = (40, 72, 56)
    bank = band & (((xx * 7 + yy * 3) % 11) < 2)
    img[bank] = (56, 96, 64)
    wat = band & (np.abs(yy - cyr) <= hw)
    t = np.clip((np.abs(yy - cyr) / np.maximum(hw, 1)), 0, 1)
    wl = _dith(1 - t, 4, B)
    wc = np.array([(88, 120, 136), (128, 160, 176), (176, 192, 192), (216, 216, 200)], float)
    img[wat] = wc[wl][wat]
    edge = wat & ~np.roll(wat, 1, 0)
    img[edge] = (24, 48, 40)
    gl = wat & (((xx * 13 + yy * 7) % 37) < 3) & (t < 0.5)
    img[gl] = (248, 248, 232)
    # dichtbij: grote donkere kruinen
    near = np.zeros((H, W), np.int8)
    near[yy >= rb1] = 1
    crowns(near, 132, 150, 24, 7, 11, 29, 1.1)
    crowns(near, 142, 158, 26, 10, 16, 23, 1.0)
    near[yy < rb1] = 0
    ncol = {1: (20, 40, 28), 2: (24, 56, 32), 3: (40, 88, 40), 4: (72, 128, 56)}
    for k, c in ncol.items():
        img[near == k] = c
    img = np.clip(img, 0, 255).astype(np.uint8)
    return img, fall


MEW_FALL = [(248, 248, 248), (200, 224, 248), (144, 184, 232)]
MEW_PALS = 10     # BG-palet 6-15; index 1-3 van elk palet = de waterval (C laat ze rondgaan)


def mew():
    img, fall = mew_scene()
    a = img.copy()
    for k in (1, 2, 3):
        a[fall == k] = MEW_FALL[k - 1]
    im = Image.fromarray(a)
    pals = L2.quantize3([im], forced=MEW_FALL, n=MEW_PALS, shared=2)
    enc = L2.EncoderN('mew', pals, 16 - MEW_PALS, prefix=PFX)
    m = enc.add(im, None, 'guyana')
    enc.save()
    GEN['DP_MEW_TILES'] = len(enc.tiles)
    GEN['DP_MEW_PAL0'] = 16 - MEW_PALS
    GEN['DP_MEW_BAND1'] = MEW_BANDS[1]
    GEN['DP_MEW_BAND2'] = MEW_BANDS[2]
    GEN['DP_MEW_BAND3'] = MEW_BANDS[3]
    pv = enc.render(m, w=32)
    save_preview('mew', [Image.fromarray(img).crop((0, 0, 240, 160)), pv.crop((0, 0, 240, 160)), pv.crop((16, 0, 256, 160))], cols=3)
    mew_tail()


def mew_tail():
    src = Image.open(os.path.join(ROOT, 'graphics/pokemon/mew/anim_front.png'))
    a = np.array(src)[:64]
    pal = src.getpalette()[:48]
    pal = [tuple(pal[i * 3:i * 3 + 3]) for i in range(16)]
    yy, xx = np.mgrid[0:64, 0:64]
    tail = a * ((xx <= 27) & (yy <= 43))
    ys, xs = np.nonzero(tail)
    # de staartbasis: onderste pixel van de staart
    by = ys.max()
    bx = int(round(xs[ys >= by - 2].mean()))
    out = np.zeros((64, 64), np.uint8)
    ox, oy = 18, 14
    out[ys + oy, xs + ox] = tail[ys, xs]
    # basis t.o.v. het midden van de sprite (32, 32)
    GEN['DP_MEW_TAIL_BX'] = bx + ox - 32
    GEN['DP_MEW_TAIL_BY'] = by + oy - 32
    im = Image.fromarray(out, 'P')
    full = [gba(c) for c in pal]
    im.putpalette([v for c in full for v in c] + [0] * (768 - 48))
    im.save(OUT + PFX + 'mew_tail.png')
    write_pal(OUT + PFX + 'mew_tail.pal', full)
    if PREVIEW:
        prev = np.array(full, np.uint8)[out]
        prev[out == 0] = (40, 120, 40)
        Image.fromarray(prev).resize((256, 256), Image.NEAREST).save(os.path.join(PREVIEW, 'legend_dp_mew_tail.png'))


def write_gen():
    p = os.path.join(ROOT, 'src/data/legend_intros_dp_gen.h')
    old = {}
    if os.path.exists(p):
        for l in open(p):
            if l.startswith('#define '):
                k, v = l[8:].split(None, 1)
                old[k] = int(v)
    old.update(GEN)
    L = ['// Gegenereerd door tools/grounded/legend_intros_dp.py: niet met de hand bewerken.']
    for k in sorted(old):
        L.append('#define %s %d' % (k, old[k]))
    open(p, 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    names = [a for a in _ARGS if a.isalpha()] or ['spiral', 'cities', 'arceus', 'mew']
    for n in names:
        globals()[n]()
    write_gen()
