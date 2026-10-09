"""Project Grounded: zes Ultra Beast-werelden in Ultra Space, elk met een eigen, per pixel getekende tileset.

Vervangt de oude kaarten van ultra_space.py (die waren uitsneden van vanilla kaarten met een ander palet; Jordi: "lege
caves in rare vormen en mappen die je schaamteloos opnieuw gebruikt"). Kaartnamen, flags (FLAG_ULTRA_*), de UB-scripts
en de terugweg (wormgat-object -> UltraSpace_EventScript_ReturnToHub) blijven gelijk; ultra_space.py slaat deze zes over
(REBUILT) en leest de aankomstplek uit het hub-script, dat dit script bijwerkt.

  Nihilego    waterplaneet met illusies: glazen vlonders naar Nihilego die boven het water zweeft, twee zonnen die in het
              water spiegelen, een stad die alleen in de weerspiegeling bestaat, een gespiegeld eiland, en nep-eilanden
              die oplossen als je er naartoe surft (coord-triggers + setmetatile)
  Buzzwole    jungle met verkeerde verhoudingen: reuzenbladeren, reuzenpaddenstoelen, druppels zo groot als een huis,
              grassprieten als bomen, piepkleine boompjes, halters van bessen en Buzzwole op een boomstronk
  Pheromosa   elementen zonder effect op elkaar: vuur dat op water brandt, bliksem die in lava staat, ijs in vlammen,
              zwevende brokken van een aardbeving; alles is beloopbaar (er gebeurt toch niks), Pheromosa op marmer
  Xurkitree   kabelwereld: geweven kabelbundels als grond, kabelbomen met stekkers en lampjes, stopcontacten,
              knipperende leds en vonken (tegelanimatie)
  Celesteela  eindeloze steppe: gras tot aan de mist, Celesteela-monolieten (objecten), beelden en silhouetten in de
              verte (tegels), schroeikringen van lanceringen
  Kartana     omgekeerde bibliotheek: boekenkasten en trappen op hun kop, kroonluchters die omhoog staan, een kaars
              die naar beneden brandt, papier overal en vallende bladzijden (tegelanimatie)

Werkwijze per wereld: een canvas van de hele kaart (16 px per cel) met periodieke texturen (zodat tegels ontdubbelen),
randen uit een vervaagd celmasker (hangen alleen af van de 3x3-buren) en stempels; daarna in metatiles geknipt.
Eigen primary (grond, meest gebruikte metatiles) + secondary (de rest + animatietegels) per wereld: 2x512 tiles,
6+7 paletten. Tegelanimaties: 8 frames, gereserveerde tegels vooraan de secondary (src/tileset_anims.c, blok
ultra_worlds_a). Controleert de bereikbaarheid van de UB, het wormgat en items.
Gebruik: python3 tools/grounded/maptools/ultra_worlds_a.py [--preview <map>]  (preview: canvas-png's, niets schrijven)"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
_sys.path.append(_os.path.dirname(_os.path.abspath(__file__)))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, math, os, random, re, struct, sys, zlib  # noqa: E401,E402
from collections import deque  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
import nieuwe_items as ni  # noqa: E402

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)
PREVIEW = sys.argv[sys.argv.index('--preview') + 1] if '--preview' in sys.argv else None
SCRATCH = os.environ.get('UW_OUT', '/tmp')


def _mb():
    src = open('include/constants/metatile_behaviors.h').read()
    body = src[src.index('{', src.index('enum')) + 1:]
    out, n = {}, 0
    for tok in re.findall(r'^\s*(MB_\w+)\s*(?:=\s*(\w+))?\s*,', body, re.M):
        if tok[1]:
            n = int(tok[1], 0)
        out[tok[0]] = n
        n += 1
    return out


MB = _mb()
B4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16
LAYER_COVERED, LAYER_SPLIT = 1, 2


def hexs(*h):
    return [tuple(int(x[i:i + 2], 16) for i in (0, 2, 4)) for x in h]


def lerp(a, b, t):
    return tuple(a[k] + (b[k] - a[k]) * t for k in range(3))


def ramp_at(ramp, t):
    t = min(max(t, 0.0), 1.0) * (len(ramp) - 1)
    i = min(int(t), len(ramp) - 2)
    return lerp(ramp[i], ramp[i + 1], t - i)


def pnoise(P, n, seed):
    """periodieke waardenruis (P x P pixels, n x n roosterpunten), -1..1, naadloos"""
    r = np.random.RandomState(seed).uniform(-1, 1, (n, n))
    yy, xx = np.mgrid[0:P, 0:P] * (n / P)
    iy, ix = yy.astype(int), xx.astype(int)
    fy, fx = yy - iy, xx - ix
    fy, fx = fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)
    a, b = r[iy % n, ix % n], r[iy % n, (ix + 1) % n]
    c, d = r[(iy + 1) % n, ix % n], r[(iy + 1) % n, (ix + 1) % n]
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy


def boxblur(a, r):
    """box-blur (2r+1) over beide assen, randen herhaald"""
    if r <= 0:
        return a.astype(float)
    p = np.pad(a.astype(float), r, mode='edge')
    c = np.cumsum(np.pad(p, ((1, 0), (0, 0))), 0)
    p = (c[2 * r + 1:] - c[:-2 * r - 1]) / (2 * r + 1)
    c = np.cumsum(np.pad(p, ((0, 0), (1, 0))), 1)
    return (c[:, 2 * r + 1:] - c[:, :-2 * r - 1]) / (2 * r + 1)


def load_mon(sp, kind='front', frame=0):
    """Pokemon-sprite als RGBA (float); front.png van 64x128 (twee frames): frame 0"""
    d = 'graphics/pokemon/' + sp
    p = d + '/%s.png' % kind
    if not os.path.exists(p):
        p = d + '/anim_front.png'
    im = Image.open(p)
    pal = [tuple(map(int, l.split())) for l in open(d + '/normal.pal').read().replace('\r', '').split('\n')[3:19]]
    idx = np.array(im)
    if kind == 'front':
        idx = idx[frame * 64:(frame + 1) * 64]
    out = np.zeros(idx.shape + (4,))
    for i, c in enumerate(pal):
        out[idx == i] = (*c, 0 if i == 0 else 255)
    return out


def load_ow(sp, frame=0):
    """overworld-sprite (32x32-frames) als RGBA"""
    d = 'graphics/pokemon/' + sp
    im = Image.open(d + '/overworld.png')
    pal = [tuple(map(int, l.split())) for l in open(d + '/overworld_normal.pal').read().replace('\r', '').split('\n')[3:19]]
    idx = np.array(im)
    h = idx.shape[0]
    idx = idx[:, frame * h:(frame + 1) * h]
    out = np.zeros(idx.shape + (4,))
    for i, c in enumerate(pal):
        out[idx == i] = (*c, 0 if i == 0 else 255)
    return out


# ====================================================================== canvas
class World:
    """Canvas van een kaart: bot = onderlaag (RGB, onder de speler), ovr = bovenlaag (RGBA, over de speler)."""

    def __init__(s, key, W, H, seed):
        s.key, s.W, s.H = key, W, H
        s.rnd = random.Random(seed)
        s.bot = np.zeros((H * 16, W * 16, 3))
        s.ovr = np.zeros((H * 16, W * 16, 4))
        s.solid = np.zeros((H, W), bool)
        s.water = np.zeros((H, W), bool)       # elevation 1 (surfen)
        s.beh = np.zeros((H, W), int)
        s.elev1 = set()                          # extra cellen op elevation 1 (nep-eilanden)
        s.anim = {}                              # (x, y) -> lijst van 8 frames (16x16x3)
        s.yy, s.xx = np.mgrid[0:H * 16, 0:W * 16]
        s.dith = B4[s.yy % 4, s.xx % 4]
        s.objects, s.coords, s.bgs, s.scripts, s.texts = [], [], [], [], []
        s.mapscripts, s.decor, s.item_spots, s.drop_kinds = '', [], [], []
        s.land = s.surf = None
        s.cycles, s.cspeed = [], 8
        s.land_rate = s.surf_rate = 0
        s.reserved = set()                       # cellen die vrij moeten blijven (aankomst, wormgat, UB)

    # ---------------------------------------------------------------- maskers
    def cells(s, m):
        """celmasker (H x W bool) -> pixelmasker"""
        return np.kron(m.astype(np.uint8), np.ones((16, 16), np.uint8)).astype(bool)

    def soft(s, m, r=6):
        """vervaagd celmasker (0..1 per pixel); hangt alleen af van de 3x3-buren als r < 16"""
        return boxblur(s.cells(m).astype(float), r)

    def wob(s, P=16, n=4, seed=1, amp=0.12):
        """periodieke wiebel (periode P px) voor drempels: grillige maar herhalende randen"""
        t = pnoise(P, n, seed) * amp
        return t[s.yy % P, s.xx % P]

    # ---------------------------------------------------------------- tekenen
    def tex(s, where, t):
        """periodieke textuur t (P x Q x 3) op de pixels van masker where"""
        P, Q = t.shape[:2]
        s.bot[where] = t[s.yy[where] % P, s.xx[where] % Q]

    def over(s, img, px, py, layer='bot', alpha=1.0):
        """img (RGBA) met linksboven (px, py) op bot of ovr"""
        h, w = img.shape[:2]
        H, W = s.bot.shape[:2]
        x0, y0, x1, y1 = max(px, 0), max(py, 0), min(px + w, W), min(py + h, H)
        if x0 >= x1 or y0 >= y1:
            return
        src = img[y0 - py:y1 - py, x0 - px:x1 - px]
        a = (src[..., 3:4] > 127).astype(float) * alpha
        if layer == 'bot':
            d = s.bot[y0:y1, x0:x1]
            d[...] = d * (1 - a) + src[..., :3] * a
        else:
            d = s.ovr[y0:y1, x0:x1]
            m = a[..., 0] > 0
            d[m, :3] = src[m, :3]
            d[m, 3] = 255

    def stamp(s, img, cx, cy, solid_rows=None, over_rows=0, layer_split=True):
        """img op cel (cx, cy). Bovenste over_rows celrijen gaan naar ovr (over de speler, beloopbaar),
        de rest naar bot; solid_rows: aantal onderste rijen die blokkeren (None = alles behalve over_rows)."""
        h, w = img.shape[0] // 16, img.shape[1] // 16
        top = img[:over_rows * 16]
        rest = img[over_rows * 16:]
        if over_rows:
            s.over(top, cx * 16, cy * 16, 'ovr')
        s.over(rest, cx * 16, (cy + over_rows) * 16, 'bot')
        n = h - over_rows if solid_rows is None else solid_rows
        for j in range(h - n, h):
            for i in range(w):
                if 0 <= cx + i < s.W and 0 <= cy + j < s.H:
                    if (img[j * 16:(j + 1) * 16, i * 16:(i + 1) * 16, 3] > 127).sum() > 40:
                        s.solid[cy + j, cx + i] = True

    def shade(s, where, f):
        s.bot[where] = s.bot[where] * f

    # ---------------------------------------------------------------- cellen -> metatiles
    def cell_list(s):
        out = []
        for y in range(s.H):
            for x in range(s.W):
                b = np.clip(s.bot[y * 16:y * 16 + 16, x * 16:x * 16 + 16], 0, 255).astype(np.uint8)
                o = s.ovr[y * 16:y * 16 + 16, x * 16:x * 16 + 16]
                o = np.clip(o, 0, 255).astype(np.uint8) if (o[..., 3] > 127).any() else None
                a = s.anim.get((x, y))
                out.append((x, y, b, o, int(s.beh[y, x]), a))
        return out


# ====================================================================== emitter
def to5(a):
    a = np.array(a, dtype=np.int32)
    a[..., :3] = (a[..., :3] // 8) * 8
    return a


def kmeans(pts, k, iters=12, seed=0):
    rng = np.random.default_rng(seed)
    uniq = np.unique(pts, axis=0)
    if len(uniq) <= k:
        return uniq.astype(float)
    cent = uniq[rng.choice(len(uniq), k, replace=False)].astype(float)
    for _ in range(iters):
        d = ((pts[:, None, :] - cent[None]) ** 2).sum(2)
        lab = d.argmin(1)
        for j in range(k):
            sel = pts[lab == j]
            if len(sel):
                cent[j] = sel.mean(0)
    return cent


def colors_of(b):
    m = b[..., 3] > 127
    return b[..., :3][m].reshape(-1, 3)


def rgba(b):
    if b.shape[-1] == 4:
        return b
    return np.concatenate([b, np.full(b.shape[:-1] + (1,), 255, b.dtype)], -1)


def quads(img):
    return [img[qy:qy + 8, qx:qx + 8] for qy in (0, 8) for qx in (0, 8)]


def canon(b):
    """sleutel van een 8x8-blok die gelijk is voor alle spiegelingen"""
    b = to5(rgba(b))
    b = np.where(b[..., 3:4] > 127, b, 0).astype(np.uint8)
    ks = [b, b[:, ::-1], b[::-1], b[::-1, ::-1]]
    return min(k.tobytes() for k in ks)


def emit2(mts, OUT, base, pal_first, num_pals, shared=None, blank=False, anims=(), cycles=()):
    """mts: lijst (bot RGB 16x16, ovr RGBA of None, gedrag, laagtype, anim (4 animtegel-ids) of None).
    anims: lijst animtegels, elk 8 frames van 8x8 RGB; die krijgen de eerste tegelplekken (vast, niet ontdubbeld).
    shared: resultaat van de primary; identieke tegels daaruit worden hergebruikt."""
    def shared_ref(b):
        if shared is None:
            return None
        c = b[..., :3].reshape(-1, 3)
        m = (b[..., 3] > 127).reshape(-1)
        if not m.any():
            return None
        for j, p in enumerate(shared['pals']):
            d = ((c[:, None, :].astype(float) - p[None]) ** 2).sum(2)
            if d.min(1)[m].max() > 0:
                continue
            idx = np.where(m, d.argmin(1) + 1, 0).reshape(8, 8)
            for hf in (0, 1):
                for vf in (0, 1):
                    v = idx[:, ::-1] if hf else idx
                    v = v[::-1, :] if vf else v
                    key = v.astype(np.uint8).tobytes()
                    if key in shared['lookup']:
                        return shared['lookup'][key], hf, vf, shared['pal_first'] + j
        return None

    blocks = []
    for bot, ovr, beh, lay, an in mts:
        if an is None:
            blocks += [to5(rgba(q)) for q in quads(bot)]
        if ovr is not None:
            blocks += [to5(q) for q in quads(ovr)]
    seen, opaque = set(), []
    for b in blocks:
        if not (b[..., 3] > 127).any():
            continue
        k = b.astype(np.uint8).tobytes()
        if k in seen:
            continue
        seen.add(k)
        if shared_ref(b) is None:
            opaque.append(b)
    # paletcycli (lava, water, leds): blokken met een cycluskleur krijgen een eigen palet; de cycluskleuren staan
    # achteraan dat palet (vaste indexen), de callback in tileset_anims.c laat ze rondlopen
    cyc = [np.array(c, float) for c in cycles]
    nn = num_pals - len(cyc)

    def cyc_group(b):
        c = colors_of(b).astype(float)
        gs = [gi for gi, cc in enumerate(cyc) if (np.abs(c[:, None, :] - cc[None]).sum(2) == 0).any()]
        assert len(gs) <= 1, '%s: blok met twee cyclusgroepen' % OUT
        return gs[0] if gs else None
    groups = opaque + [to5(rgba(np.concatenate(fr, 0))) for fr in anims]   # animtegel: alle frames samen
    normal = [b for b in groups if cyc_group(b) is None]
    feat = np.array([np.concatenate([colors_of(b).mean(0), colors_of(b).std(0)]) for b in normal])
    assign = ((feat[:, None, :] - kmeans(feat, nn)[None]) ** 2).sum(2).argmin(1)
    for it in range(6):
        pals = []
        for j in range(nn):
            pts = np.concatenate([colors_of(b) for b, a in zip(normal, assign) if a == j] or [np.zeros((1, 3))])
            pals.append(np.round(kmeans(pts.astype(float), 15, seed=it) / 8) * 8)
        errs = []
        for b in normal:
            c = colors_of(b).astype(float)
            errs.append([((c[:, None, :] - p[None]) ** 2).sum(2).min(1).sum() for p in pals])
        assign = np.array(errs).argmin(1)
    for gi, cc in enumerate(cyc):
        pts = [colors_of(b) for b in groups if cyc_group(b) == gi]
        pts = np.concatenate(pts) if pts else np.zeros((1, 3))
        pts = pts[(np.abs(pts[:, None, :].astype(float) - cc[None]).sum(2) != 0).all(1)]
        free = np.round(kmeans(pts.astype(float), 15 - len(cc)) / 8) * 8 if len(pts) else np.zeros((1, 3))
        free = np.concatenate([free] + [free[:1]] * (15 - len(cc) - len(free)))
        pals.append(np.concatenate([free, cc]))
    pals = [np.clip(p, 0, 248) for p in pals]

    def pal_for(b):
        g_ = cyc_group(b)
        if g_ is not None:
            return [nn + g_]
        return list(range(nn))

    def qidx(b, p):
        c = b[..., :3].reshape(-1, 3).astype(float)
        m = (b[..., 3] > 127).reshape(-1)
        d = ((c[:, None, :] - p[None]) ** 2).sum(2)
        return np.where(m, d.argmin(1) + 1, 0).reshape(b.shape[:2]), d.min(1)[m].sum()

    tiles = [np.zeros((8, 8), dtype=np.int64)] if blank else []
    anim_frames = []                      # per animtegel: (palet, [8 x 8x8 indices])
    for fr in anims:
        allb = to5(rgba(np.concatenate(fr, 0)))
        j = min(pal_for(allb), key=lambda j: qidx(allb, pals[j])[1])
        idx = [qidx(to5(rgba(f)), pals[j])[0] for f in fr]
        anim_frames.append((j, idx))
        tiles.append(idx[0])
    lookup = {}

    def tile_ref(b):
        r = shared_ref(b) if cyc_group(b) is None else None
        if r is not None:
            return r
        if not (b[..., 3] > 127).any():
            return None
        best = min(pal_for(b), key=lambda j: qidx(b, pals[j])[1])
        idx, _ = qidx(b, pals[best])
        for hf in (0, 1):
            for vf in (0, 1):
                v = idx[:, ::-1] if hf else idx
                v = v[::-1, :] if vf else v
                key = v.astype(np.uint8).tobytes()
                if key in lookup:
                    return base + lookup[key], hf, vf, pal_first + best
        tiles.append(idx)
        lookup[idx.astype(np.uint8).tobytes()] = len(tiles) - 1
        return base + len(tiles) - 1, 0, 0, pal_first + best

    mdata, adata = bytearray(), bytearray()
    for bot, ovr, beh, lay, an in mts:
        ent = []
        if an is not None:
            for a in an:
                j, _ = anim_frames[a]
                ent.append((base + (1 if blank else 0) + a) | ((pal_first + j) << 12))
        else:
            for q in quads(bot):
                t, hf, vf, pn = tile_ref(to5(rgba(q)))
                ent.append(t | (hf << 10) | (vf << 11) | (pn << 12))
        for q in (quads(ovr) if ovr is not None else [None] * 4):
            r = tile_ref(to5(q)) if q is not None else None
            if r is None:
                ent.append(0)
            else:
                t, hf, vf, pn = r
                ent.append(t | (hf << 10) | (vf << 11) | (pn << 12))
        mdata += struct.pack('<8H', *ent)
        adata += struct.pack('<H', beh | (lay << 12))
    assert len(tiles) <= 512, '%s: te veel tiles: %d' % (OUT, len(tiles))
    assert len(mts) <= 512, '%s: te veel metatiles: %d' % (OUT, len(mts))
    os.makedirs(OUT + '/palettes', exist_ok=True)
    grey = sum(([i * 16] * 3 for i in range(16)), []) + [0] * 720

    def save_idx(tl, path, cols=16):
        rows = (len(tl) + cols - 1) // cols
        img = Image.new('P', (cols * 8, max(rows, 1) * 8), 0)
        for i, t in enumerate(tl):
            img.paste(Image.fromarray(t.astype(np.uint8), 'P'), ((i % cols) * 8, (i // cols) * 8))
        img.putpalette(grey)
        img.save(path)
    save_idx(tiles, OUT + '/tiles.png')
    if anims:
        os.makedirs(OUT + '/anim', exist_ok=True)
        for f in range(8):
            save_idx([fr[1][f] for fr in anim_frames], OUT + '/anim/%d.png' % f, cols=len(anim_frames))
    for i in range(16):
        j = i - pal_first
        cols = [(0, 0, 0)] * 16
        if 0 <= j < num_pals:
            cols = [(255, 0, 255)] + [tuple(int(v) for v in c) for c in pals[j]]
            cols += [(0, 0, 0)] * (16 - len(cols))
        with open('%s/palettes/%02d.pal' % (OUT, i), 'w', newline='\r\n') as f:
            f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in cols))
    open(OUT + '/metatiles.bin', 'wb').write(mdata)
    open(OUT + '/metatile_attributes.bin', 'wb').write(adata)
    print('  %s: %d metatiles, %d tiles (%d anim)' % (OUT, len(mts), len(tiles), len(anims)))
    return {'pals': pals[:nn], 'lookup': lookup, 'pal_first': pal_first, 'ntiles': len(tiles),
            'cycles': [(pal_first + nn + gi, 16 - len(cc), [tuple(int(v) for v in c) for c in cc]) for gi, cc in enumerate(cyc)]}


def build_tilesets(w):
    """canvas -> primary + secondary; geeft het metatile-raster (H x W) terug"""
    cl = w.cell_list()
    # animtegels: elke animcel = 4 tegels; identieke reeksen delen hun tegels
    anims, akeys, cell_anim = [], {}, {}
    for (x, y), frames in w.anim.items():
        ids = []
        for qi, (qy, qx) in enumerate(((0, 0), (0, 8), (8, 0), (8, 8))):
            fr = [np.clip(f[qy:qy + 8, qx:qx + 8], 0, 255).astype(np.uint8) for f in frames]
            k = b''.join(to5(f).astype(np.uint8).tobytes() for f in fr)
            if k not in akeys:
                akeys[k] = len(anims)
                anims.append(fr)
            ids.append(akeys[k])
        cell_anim[(x, y)] = tuple(ids)
    keys, arr, freq = [], {}, {}
    grid_keys = {}
    for x, y, b, o, beh, a in cl:
        an = cell_anim.get((x, y))
        lay = LAYER_SPLIT if o is not None else LAYER_COVERED
        k = (b.tobytes() if an is None else b'', None if o is None else o.tobytes(), beh, lay, an)
        if k not in arr:
            arr[k] = (b, o, beh, lay, an)
            keys.append(k)
        freq[k] = freq.get(k, 0) + 1
        grid_keys[(x, y)] = k
    cyccols = {tuple(int(v) for v in c) for cc in w.cycles for c in cc}

    def has_cyc(k):
        b, o, beh, lay, an = arr[k]
        px = {tuple(int(v) for v in c) for c in to5(b).reshape(-1, 3)}
        if o is not None:
            q = to5(o)
            px |= {tuple(int(v) for v in c[:3]) for c in q.reshape(-1, 4) if c[3] > 127}
        return bool(px & cyccols)
    order = sorted([k for k in keys if k[4] is None and not has_cyc(k)], key=lambda k: -freq[k])
    prim, pblocks = [], {canon(np.zeros((8, 8, 4), np.uint8))}
    for k in order:
        b, o, beh, lay, an = arr[k]
        bl = {canon(q) for q in quads(b)} | ({canon(q) for q in quads(o)} if o is not None else set())
        if len(pblocks | bl) <= 510 and len(prim) < 511:
            pblocks |= bl
            prim.append(k)
    pset = set(prim)
    sec = [k for k in keys if k not in pset]
    P = 'data/tilesets/primary/ultra_world_%s_ground' % w.key.lower()
    S = 'data/tilesets/secondary/ultra_world_%s' % w.key.lower()
    print('%s: %d cellen, %d unieke metatiles (%d primary, %d secondary), %d animtegels'
          % (w.key, w.W * w.H, len(keys), len(prim), len(sec), len(anims)))
    res = emit2([arr[k] for k in prim], P, 0, 0, 6, blank=True)
    res2 = emit2([arr[k] for k in sec], S, 512, 6, 7, shared=res, anims=anims, cycles=w.cycles)
    w.cycle_info = res2['cycles']
    ids = {k: i for i, k in enumerate(prim)}
    ids.update({k: 512 + i for i, k in enumerate(sec)})
    g = np.zeros((w.H, w.W), int)
    for (x, y), k in grid_keys.items():
        g[y, x] = ids[k]
    w.ntiles = (res['ntiles'], res2['ntiles'])
    w.nanim = len(anims)
    w.tileset_dirs = (P, S)
    return g


# ====================================================================== registratie
def const(name):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper()


def block_replace(path, start, end, body, anchor=None):
    """vervang (of voeg toe) een gegenereerd blok start ... end in een bestand"""
    s = open(path).read()
    blk = start + '\n' + body.rstrip('\n') + '\n' + end
    if start in s:
        i = s.index(start)
        j = s.index(end, i) + len(end)
        s = s[:i] + blk + s[j:]
    elif anchor:
        i = s.rindex(anchor)
        s = s[:i] + blk + '\n\n' + s[i:]
    else:
        s = s.rstrip('\n') + '\n\n' + blk + '\n'
    open(path, 'w').write(s)


def register_tilesets(worlds):
    gfx, mts, hdr, anim_c, anim_h = [], [], [], [], []
    for w in worlds:
        P, S = w.tileset_dirs
        k = w.key
        for sym, d, sec in (('UltraWorld%sGround' % k, P, False), ('UltraWorld%s' % k, S, True)):
            gfx.append('const u32 gTilesetTiles_%s[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");' % (sym, d))
            gfx.append('const u16 gTilesetPalettes_%s[][16] =\n{\n%s};\n' % (
                sym, ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (d, i) for i in range(16))))
            mts.append('const u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin");' % (sym, d))
            mts.append('const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");' % (sym, d))
            cb = 'InitTilesetAnim_UltraWorld%s' % k if sec and (w.nanim or w.cycle_info) else 'NULL'
            hdr.append('const struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n    .isSecondary = %s,\n'
                       '    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n'
                       '    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n'
                       '    .callback = %s,\n};\n' % (sym, 'TRUE' if sec else 'FALSE', sym, sym, sym, sym, cb))
        if w.nanim or w.cycle_info:
            n = w.nanim
            anim_c += [] if not n else ['const u16 gTilesetAnims_UltraWorld%s_Frame%d[] = INCBIN_U16("%s/anim/%d.4bpp");' % (k, f, S, f)
                       for f in range(8)]
            if n:
                anim_c.append('const u16 *const gTilesetAnims_UltraWorld%s[] = {\n%s};\n' % (
                    k, ''.join('    gTilesetAnims_UltraWorld%s_Frame%d,\n' % (k, f) for f in range(8))))
            body = []
            if n:
                body.append('    if (timer %% %d == 0)\n        AppendTilesetAnimToBuffer(gTilesetAnims_UltraWorld%s[(timer / %d) %% 8], '
                            '(u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY)), %d * TILE_SIZE_4BPP);' % (w.speed, k, w.speed, n))
            for ci, (slot, first, cols) in enumerate(w.cycle_info):
                anim_c.append('static const u16 sUltraWorld%s_Cycle%d[] = {%s};' % (
                    k, ci, ', '.join('RGB(%d, %d, %d)' % (c[0] >> 3, c[1] >> 3, c[2] >> 3) for c in cols)))
                body.append('    if (timer %% %d == 0)\n        UltraWorld_CyclePal(%d, %d, %d, sUltraWorld%s_Cycle%d, timer / %d);'
                            % (w.cspeed, slot, first, len(cols), k, ci, w.cspeed))
            anim_c.append('''static void TilesetAnim_UltraWorld%s(u16 timer)
{
%s
}

void InitTilesetAnim_UltraWorld%s(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = 256;
    sSecondaryTilesetAnimCallback = TilesetAnim_UltraWorld%s;
}
''' % (k, '\n'.join(body), k, k))
            anim_h.append('void InitTilesetAnim_UltraWorld%s(void);' % k)
    tag = '(tools/grounded/maptools/ultra_worlds_a.py: eigen tilesets van zes Ultra Beast-werelden)'
    block_replace('src/data/tilesets/graphics.h', '// ultra_worlds_a { ' + tag, '// } ultra_worlds_a', '\n'.join(gfx))
    block_replace('src/data/tilesets/metatiles.h', '// ultra_worlds_a { ' + tag, '// } ultra_worlds_a', '\n'.join(mts))
    block_replace('src/data/tilesets/headers.h', '// ultra_worlds_a { ' + tag, '// } ultra_worlds_a', '\n'.join(hdr))
    cyc_fn = '''#include "constants/rgb.h"

// paletcyclus: kleuren first..first+n-1 van BG-palet pal schuiven elke stap een plek op (lava, water, leds)
static void UltraWorld_CyclePal(u8 pal, u8 first, u8 n, const u16 *cols, u16 step)
{
    u32 i;
    for (i = 0; i < n; i++)
        gPlttBufferUnfaded[BG_PLTT_ID(pal) + first + i] = cols[(i + step) % n];
    if ((u8)FindTaskIdByFunc(Task_BattleTransition_Intro) == TASK_NONE)
        BlendPalette(BG_PLTT_ID(pal) + first, n, gPaletteFade.y, gPaletteFade.blendColor & 0x7FFF);
}
'''
    block_replace('src/tileset_anims.c', '// ultra_worlds_a { ' + tag, '// } ultra_worlds_a', cyc_fn + '\n'.join(anim_c))
    block_replace('include/tileset_anims.h', '// ultra_worlds_a {', '// } ultra_worlds_a', '\n'.join(anim_h),
                  anchor='#endif')


def save_layout(w, g):
    name = 'UltraSpace_' + w.key
    d = 'data/layouts/' + name
    os.makedirs(d, exist_ok=True)
    data = bytearray()
    for y in range(w.H):
        for x in range(w.W):
            elev = 1 if (w.water[y, x] or (x, y) in w.elev1) else 3
            data += struct.pack('<H', int(g[y, x]) | (int(w.solid[y, x]) << 10) | (elev << 12))
    open(d + '/map.bin', 'wb').write(bytes(data))
    b = [int(g[w.border[1] + j, w.border[0] + i]) | (1 << 10) | (3 << 12) for j in (0, 1) for i in (0, 1)]
    open(d + '/border.bin', 'wb').write(struct.pack('<4H', *b))
    lj = open('data/layouts/layouts.json').read()
    c = 'LAYOUT_' + const(name)
    entry = '''    {
      "id": "%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_UltraWorld%sGround",
      "secondary_tileset": "gTileset_UltraWorld%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (c, name, w.W, w.H, w.key, w.key, name, name)
    m = re.search(r'    \{\n      "id": "%s",.*?\n    \}' % c, lj, re.S)
    if m:
        lj = lj[:m.start()] + entry + lj[m.end():]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    json.loads(lj)
    open('data/layouts/layouts.json', 'w').write(lj)
    return c


def obj(lid, gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', elev=3, rx=0, ry=0, sight='0'):
    o = {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
         'movement_range_x': rx, 'movement_range_y': ry, 'trainer_type': 'TRAINER_TYPE_NONE',
         'trainer_sight_or_berry_tree_id': sight, 'script': script, 'flag': flag}
    return dict(local_id=lid, **o) if lid else o


def write_map(w, layout_const):
    name = 'UltraSpace_' + w.key
    p = 'data/maps/%s/map.json' % name
    d = json.load(open(p))
    d.update({'layout': layout_const, 'music': w.music, 'map_type': 'MAP_TYPE_UNDERGROUND', 'weather': w.weather,
              'object_events': w.objects, 'warp_events': [], 'coord_events': w.coords, 'bg_events': w.bgs})
    assert len(w.objects) <= 15, (name, len(w.objects))
    open(p, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')


def write_wild(w):
    name = 'UltraSpace_' + w.key
    mapc = 'MAP_' + const(name)
    js = open('src/data/wild_encounters.json').read()
    m = re.search(r'\n        \{\n          "map": "%s",.*?\n        \}(?=,?\n)' % mapc, js, re.S)
    if not w.land and not w.surf:
        if m:   # tabel weg
            s, e = m.start(), m.end()
            if js[e] == ',':
                e += 1
            elif js[s - 1] == ',':
                s -= 1
            js = js[:s] + js[e:]
            open('src/data/wild_encounters.json', 'w').write(js)
        return
    entry = {'map': mapc, 'base_label': 'g' + name.replace('_', '')}
    if w.land:
        assert len(w.land) == 12 and len({x[0] for x in w.land}) == 12, (name, 'land: 12 unieke soorten')
        entry['land_mons'] = {'encounter_rate': w.land_rate,
                              'mons': [{'min_level': a, 'max_level': b, 'species': 'SPECIES_' + sp} for sp, a, b in w.land]}
    if w.surf:
        assert len(w.surf) == 5 and len({x[0] for x in w.surf}) == 5
        entry['water_mons'] = {'encounter_rate': w.surf_rate,
                               'mons': [{'min_level': a, 'max_level': b, 'species': 'SPECIES_' + sp} for sp, a, b in w.surf]}
    txt = '\n' + '\n'.join('        ' + l for l in json.dumps(entry, indent=2).split('\n'))
    if m:
        js = js[:m.start()] + txt + js[m.end():]
    else:
        anchor = '\n      ]\n    },\n    {\n      "label": "gBattlePyramidWildMonHeaders"'
        i = js.index(anchor)
        js = js[:i] + ',' + txt + js[i:]
    json.loads(js)
    open('src/data/wild_encounters.json', 'w').write(js)


def text_lines(txt):
    """tekst met \\p (nieuw vak) -> .string-regels; afbreken met dezelfde regels als de Dialoogstudio-importer"""
    import importlib.util
    spec = importlib.util.spec_from_file_location('dialogen_import', 'tools/dialogen/import.py')
    dimp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dimp)
    plain = txt.replace('\\p', '\n\n').replace('\\l', ' ')
    plain = '\n\n'.join(re.sub(r'\s*\n\s*', ' ', b).strip() for b in plain.split('\n\n'))
    return ['\t.string "%s"' % l for l in dimp.to_strings(plain)]


def write_scripts(w):
    """logica (gegenereerd blok, elke keer opnieuw) + teksten (alleen als het label nog niet bestaat: Dialoogstudio)"""
    name = 'UltraSpace_' + w.key
    p = 'data/maps/%s/scripts.inc' % name
    s = open(p).read()
    for kind in w.drop_kinds:     # oude decor-scripts die niet meer gebruikt worden (script + tekst)
        s = re.sub(r'%s_EventScript_%s::\n(?:\t[^\n]*\n)*\n?' % (name, kind), '', s)
        s = re.sub(r'%s_Text_%s:\n(?:\t\.string [^\n]*\n)*\n?' % (name, kind), '', s)
    s = re.sub(r'%s_MapScripts::\n(?:\tmap_script [^\n]*\n)*\t\.byte 0\n' % name,
               '%s_MapScripts::\n%s\t.byte 0\n' % (name, w.mapscripts), s)
    open(p, 'w').write(s)
    block_replace(p, '@ ultra_worlds_a { gegenereerd door tools/grounded/maptools/ultra_worlds_a.py; niet met de hand bewerken',
                  '@ } ultra_worlds_a', '\n'.join(w.scripts))
    s = open(p).read()
    add = []
    for label, txt in w.texts:
        if '\n%s:' % label not in s:
            add += ['%s:' % label] + text_lines(txt) + ['']
    if add:
        s = s.rstrip('\n') + '\n\n' + '\n'.join(add)
        open(p, 'w').write(s)


def update_hub(w, arrive):
    p = 'data/maps/UltraSpace_Hub/scripts.inc'
    s = open(p).read()
    mc = 'MAP_' + const('UltraSpace_' + w.key)
    assert 'warp %s,' % mc in s
    open(p, 'w').write(re.sub(r'warp %s, \d+, \d+' % mc, 'warp %s, %d, %d' % (mc, arrive[0], arrive[1]), s))


# ====================================================================== bereikbaarheid
def reach(w, start, extra_block=()):
    """BFS; land <-> water mag (surfen); objecten blokkeren"""
    blocked = set(extra_block)
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if not (0 <= n[0] < w.W and 0 <= n[1] < w.H) or n in seen or n in blocked or w.solid[n[1], n[0]]:
                continue
            seen.add(n)
            q.append(n)
    return seen


def next_to(r, c):
    return any((c[0] + dx, c[1] + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


# ====================================================================== tekenhulp
def quant(t, ramp, dith):
    """waarde 0..1 -> kleur uit een korte ramp, met ordered dithering tussen twee stappen (Gen 3-stijl)"""
    r = np.array(ramp, float)
    n = len(r)
    v = np.clip(t, 0, 0.9999) * (n - 1)
    i = v.astype(int)
    i = np.minimum(i + ((v - i) > dith), n - 1)
    return r[i]


def grid(P, Q=None):
    Q = Q or P
    yy, xx = np.mgrid[0:P, 0:Q]
    return yy, xx, B4[yy % 4, xx % 4]


def ellipse(W, H, cx, cy, rx, ry):
    yy, xx = np.mgrid[0:H, 0:W]
    return ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0


def path_cells(pts):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            c = (x0 + (x1 - x0) * i // max(n, 1), y0 + (y1 - y0) * i // max(n, 1))
            if c not in out:
                out.append(c)
    return out


def img_new(w, h):
    return np.zeros((h, w, 4))


def put(img, x, y, c):
    if 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
        img[y, x] = (*c, 255)


def outline(img, col):
    """1 px omlijning rond de dekkende pixels (Gen 3-sprites)"""
    a = img[..., 3] > 127
    o = np.zeros_like(a)
    o[1:] |= a[:-1]; o[:-1] |= a[1:]; o[:, 1:] |= a[:, :-1]; o[:, :-1] |= a[:, 1:]
    o &= ~a
    img[o] = (*col, 255)
    return img


def silhouette(img, col, alpha_keep=True):
    out = img.copy()
    m = out[..., 3] > 127
    out[m, :3] = col
    return out


def shaded_sprite(img, ramp):
    """grijswaarde van een sprite -> kleurverloop"""
    out = img.copy()
    L = (0.3 * img[..., 0] + 0.59 * img[..., 1] + 0.11 * img[..., 2]) / 255
    r = np.array(ramp, float)
    n = len(r) - 1
    t = np.clip(L * n, 0, n - 1e-6)
    i = t.astype(int)
    f = (t - i)[..., None]
    out[..., :3] = r[i] * (1 - f) + r[i + 1] * f
    return out


# ====================================================================== Nihilego: waterplaneet met illusies
def w_nihilego():
    W, H = 40, 32
    w = World('Nihilego', W, H, 1440)
    w.music, w.weather, w.speed = 'MUS_UNDERWATER', 'WEATHER_NONE', 8
    WATER = hexs('3a6ea0', '5a94c4', '7cb4d8', 'a4d4e8', 'd4f0f4', 'fcfcfc')
    SAND = hexs('7c6cb0', 'a494d0', 'c8b8e4', 'e4d8f0', 'fcf4f8')
    GLASS = hexs('7894c8', 'a8c8e4', 'cce4f0', 'e8f8f8', 'ffffff')
    PINK, CYAN, LILAC = hexs('f0a8d0', '88e0e8', 'c0a0e8')
    yy, xx, dith = w.yy, w.xx, w.dith

    # ---- water: periodieke textuur (32 px), golfstreepjes in baksteenverband
    P = 64
    ty, tx, td = grid(P)
    ph = 2 * np.pi * ty / 16 + 2.4 * pnoise(P, 4, 11) + 0.5 * np.sin(2 * np.pi * tx / 64)
    n2 = pnoise(P, 8, 12)
    base = np.zeros((P, P, 3))
    base[...] = WATER[2]
    base[np.sin(ph) > 0.82] = WATER[1]
    base[(np.sin(ph) > 0.7) & (np.sin(ph) <= 0.82) & (td < 0.5)] = WATER[1]
    base[(np.sin(ph) < -0.86) & (n2 > -0.1)] = WATER[3]
    base[(np.sin(ph) < -0.97) & (n2 > 0.35)] = WATER[4]
    water = np.ones((H, W), bool)

    # ---- eilanden (cellen)
    arrive_isle = ellipse(W, H, 20, 27.6, 5.6, 2.9)
    real_isle = ellipse(W, H, 4.6, 26.6, 2.7, 1.9)
    fakes = [ellipse(W, H, 7.2, 18.6, 2.3, 1.6), ellipse(W, H, 33, 20.5, 2.4, 1.7), ellipse(W, H, 31.5, 15.6, 1.7, 1.25)]
    walk = path_cells([(20, 24), (20, 21), (16, 21), (16, 17), (24, 17), (24, 13), (22, 13), (22, 11), (21, 11)])
    wm = np.zeros((H, W), bool)
    for x, y in walk:
        wm[y, x] = True
    land = arrive_isle | real_isle
    for f in fakes:
        land |= f
    water &= ~land & ~wm
    w.water = water.copy()
    w.water[wm] = False
    w.tex(np.ones((H * 16, W * 16), bool), base)

    # ---- weerspiegelde stad (bestaat niet): omgekeerde torens vanaf de bovenrand, periode 128 px, golvend
    city = np.zeros((4 * 16, 128), bool)
    win = np.zeros_like(city)
    r = random.Random(7)
    x = 0
    while x < 128:
        bw = r.choice((10, 12, 14, 18))
        h = r.randint(20, 50)
        for i in range(bw - 1):
            if x + i < 128:
                city[:h, x + i] = True
                for j in range(4, h - 4, 6):
                    if 2 <= i < bw - 3 and i % 4 in (1, 2) and r.random() < 0.6:
                        win[j:j + 2, x + i] = True
        if r.random() < 0.4:   # spits (omgekeerd: punt naar beneden)
            for j in range(10):
                c0 = x + bw // 2 - max(0, 3 - j // 3)
                city[h + j, c0:c0 + max(1, 7 - j * 2 // 3)] = True if h + j < city.shape[0] else False
        x += bw + r.choice((0, 2, 3))
    cy = yy[:64, :]
    shift = np.round(1.4 * np.sin(cy / 2.2) + 0.8 * np.sin(cy / 5.3 + 1)).astype(int)
    cxs = (xx[:64, :] + shift) % 128
    ref = city[cy, cxs]
    rwin = win[cy, cxs]
    fade = np.clip((64 - cy) / 28.0, 0, 1)
    on = ref & (fade > dith[:64]) & ~((cy % 5 == 4) & (cy > 24))
    seg = w.bot[:64]
    lit = (cxs % 8 < 2)                                               # lichte kant van elke toren
    seg[on] = np.array([150, 136, 208])
    seg[on & lit] = np.array([184, 168, 232])
    seg[on & (cy < 3)] = np.array([120, 104, 184])
    seg[on & rwin] = np.array([248, 216, 168])

    # ---- twee zonnen (alleen in het water te zien) + glitterpad naar beneden
    suns = [(8 * 16 + 8, 9 * 16 + 8), (32 * 16 + 8, 9 * 16 + 8)]
    for sx, sy in suns:
        d = np.hypot(xx - sx, (yy - sy) * 1.25)
        for r0, r1, c, a in ((17, 26, (232, 196, 216), 0.85), (26, 36, (184, 176, 224), 0.6), (36, 44, (160, 176, 224), 0.35)):
            m = (d >= r0) & (d < r1) & (a > dith)
            w.bot[m] = c
        col = (np.abs(xx - sx) < 11 - (yy - sy) / 30) & (yy > sy + 22) & (yy < 21 * 16)
        glint = col & ((yy % 8) < 1) & (((xx + (yy // 8) * 5) % 9) < 6)
        t = np.clip(1 - (yy - sy - 22) / 170.0, 0, 1)
        g = glint & (t > dith * 0.8)
        w.bot[g] = np.array([252, 236, 200])
        g2 = np.roll(g, 1, 0) & ~g
        w.bot[g2] = np.array([232, 196, 200])
    # zonkern: geanimeerd (3x3 cellen), golfjes schuiven door de schijf
    sun_frames = []
    for f in range(8):
        cv = w.bot[8 * 16:11 * 16, 7 * 16:10 * 16].copy()
        ly, lx = np.mgrid[0:48, 0:48]
        d = np.hypot(lx - 24, (ly - 24) * 1.25)
        band = ((ly + f) % 6 == 0) | (((ly * 3 + f * 2) % 11 == 0) & (d > 8))
        core = (d < 12) & ~band
        ring = (d >= 12) & (d < 17) & ~band & (B4[ly % 4, lx % 4] < 0.6)
        cv[ring] = np.array([248, 216, 152])
        cv[core] = np.array([255, 248, 224])
        cv[(d < 7) & ~band] = np.array([255, 255, 255])
        wav = band & (d < 17)
        cv[wav] = cv[wav] * 0.7 + np.array([248, 200, 160]) * 0.3
        sun_frames.append(cv)
    for sx, sy in suns:
        cx0, cy0 = sx // 16 - 1, sy // 16 - 1
        for j in range(3):
            for i in range(3):
                w.anim[(cx0 + i, cy0 + j)] = [fr[j * 16:j * 16 + 16, i * 16:i * 16 + 16] for fr in sun_frames]
        w.bot[cy0 * 16:cy0 * 16 + 48, cx0 * 16:cx0 * 16 + 48] = sun_frames[0]

    # ---- rimpelringen rond Nihilego
    UB = (20, 11)
    ux, uy = UB[0] * 16 + 8, UB[1] * 16 + 10
    d = np.hypot(xx - ux, (yy - uy) * 1.3)
    for rad, a in ((18, 0.95), (31, 0.75), (45, 0.5), (60, 0.3)):
        ring = (np.abs(d - rad) < 1.0) & (a > dith)
        w.bot[ring] = np.array([224, 240, 248])
        ring2 = (np.abs(d - rad - 1.5) < 0.6) & (a * 0.8 > dith)
        w.bot[ring2] = w.bot[ring2] * 0.8
    glow = (d < 14) & (0.5 > dith)
    w.bot[glow] = w.bot[glow] * 0.6 + np.array([240, 208, 232]) * 0.4

    # ---- iets heel groots onder het oppervlak: een reuzen-Nihilego (silhouet, 2x), vaag
    ns = load_mon('nihilego')
    big = ns[..., 3] > 127
    oy, ox = 24 * 16, 30 * 16
    hh, ww_ = big.shape
    reg = (slice(oy, min(oy + hh, H * 16)), slice(ox, min(ox + ww_, W * 16)))
    bm = big[:reg[0].stop - oy, :reg[1].stop - ox] & (dith[reg] < 0.5)
    w.bot[reg][bm] = w.bot[reg][bm] * 0.72 + np.array([40, 48, 120]) * 0.28

    # ---- eilanden: parelzand, natte rand, schuim
    sy_, sx_, sd_ = grid(16)
    sn = pnoise(16, 4, 3)
    sand = np.zeros((16, 16, 3))
    sand[...] = SAND[3]
    sand[(sn < -0.2) | ((sn < -0.05) & (sd_ < 0.5))] = SAND[2]
    sand[(sx_ * 7 + sy_ * 3) % 23 == 0] = SAND[4]
    sand[(sx_ * 5 + sy_ * 11) % 29 == 0] = (240, 196, 224)

    def isle(mask, seed):
        s = w.soft(mask, 7) + w.wob(16, 4, seed, 0.1)
        inside = s > 0.5
        wet = (s > 0.38) & ~inside
        foam = (s > 0.3) & (s <= 0.38) & (((xx % 16) + (yy % 16) * 3) % 7 < 4)
        w.bot[foam] = WATER[4]
        w.bot[wet] = WATER[3]
        w.tex(inside, sand)
        face = inside & ~np.roll(inside, -5, 0)            # zuidkant: een klifje van parelmoer
        w.bot[face] = SAND[1]
        w.bot[face & ((xx % 5 == 0) | ((xx + yy) % 7 == 0))] = SAND[0]
        w.bot[face & ~np.roll(inside, -1, 0)] = SAND[0]
        topf = face & np.roll(inside, -1, 0) & ~np.roll(face, 1, 0)
        w.bot[topf] = SAND[4]
        top = inside & ~np.roll(inside, 2, 0)
        w.bot[top] = SAND[4]
        side = inside & ~face & (~np.roll(inside, 2, 1) | ~np.roll(inside, -2, 1))
        w.bot[side] = SAND[2]
        return inside
    isle(arrive_isle, 1)
    isle(real_isle, 2)
    fake_px = [isle(f, 3 + i) for i, f in enumerate(fakes)]

    # ---- glazen vlonders
    # zwevende glazen schijven (een per cel), met een brug naar de buurschijf
    gy, gx = yy % 16, xx % 16
    dd = np.hypot(gx - 7.5, gy - 7.5)
    cellm = w.cells(wm)
    slab = cellm & (dd < 7.6)
    for dx, dy, half in ((1, 0, gx >= 7), (-1, 0, gx <= 8), (0, 1, gy >= 7), (0, -1, gy <= 8)):
        nb = np.roll(np.roll(cellm | w.cells(arrive_isle), -dx * 16, 1), -dy * 16, 0) & cellm
        strip = (np.abs(gy - 7.5) < 3.5) if dx else (np.abs(gx - 7.5) < 3.5)
        slab |= nb & strip & half
    sh = np.zeros_like(slab)
    sh[3:, 1:] = slab[:-3, :-1]
    sh &= ~slab
    w.bot[sh] = w.bot[sh] * 0.7 + np.array([40, 40, 90]) * 0.3
    w.bot[slab] = GLASS[2]
    w.bot[slab & (dd < 5.5)] = GLASS[3]
    w.bot[slab & (np.abs(gx - gy - 4) < 1.2) & (dd < 6)] = GLASS[4]
    w.bot[slab & (np.abs(gx - gy + 1) < 0.7) & (dd < 5)] = GLASS[4]
    edge_b = slab & ~np.roll(slab, -1, 0)
    edge_r = slab & ~np.roll(slab, -1, 1)
    edge_t = slab & ~np.roll(slab, 1, 0)
    edge_l = slab & ~np.roll(slab, 1, 1)
    w.bot[(edge_b | edge_r)] = GLASS[0]
    w.bot[(edge_t | edge_l) & ~(edge_b | edge_r)] = GLASS[4]
    w.bot[slab & ~edge_b & np.roll(edge_b, -1, 0)] = GLASS[1]

    # ---- glazen palmen en kristallen
    FROND = hexs('3c8cb0', '58b8d0', '88e0e8', 'c8f8f8')

    def palm(flip=False):
        img = img_new(48, 48)
        trunk = [(22 + int(round(4 * math.sin((j - 12) / 14.0))), j) for j in range(12, 46)]
        for x, y in trunk:
            for i in range(-2, 3):
                c = GLASS[3] if i < 0 else (GLASS[2] if i < 2 else GLASS[0])
                if (y % 5) == 0:
                    c = LILAC if i < 1 else (136, 112, 192)
                put(img, x + i, y, c)
        hx, hy = trunk[0]
        for ang in (-2.9, -2.35, -1.75, -1.2, -0.6, -0.1, 2.75, 0.4):
            pts = []
            for t in range(23):
                px = hx + math.cos(ang) * t
                py = hy + math.sin(ang) * t * 0.6 + (t / 7.5) ** 2
                pts.append((px, py))
            for t, (px, py) in enumerate(pts):
                wdt = 3.2 * math.sin(math.pi * min(t + 2, 22) / 24)
                for o in np.arange(-wdt, wdt + 0.1, 0.5):
                    k = 3 if o < -wdt + 1 else (2 if o < 0 else (1 if o < wdt - 1 else 0))
                    c = FROND[k]
                    if abs(o) < 0.5 and t > 2:
                        c = PINK
                    put(img, int(round(px)), int(round(py + o)), c)
        for i, (dx, dy) in enumerate(((-2, 1), (2, 1), (0, 2))):
            for ox, oy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                put(img, hx + dx + ox, hy + dy + oy, PINK if (ox + oy) else (255, 240, 248))
        outline(img, (56, 72, 136))
        return img[:, ::-1] if flip else img
    PALM = palm()
    PALM2 = palm(True)

    def crystal(seed, h=16):
        rr = random.Random(seed)
        img = img_new(16, h)
        for bx, hh, ww, c in ((4, h - 6, 2, PINK), (9, h - 2, 3, CYAN), (12, h - 8, 2, LILAC)):
            for j in range(hh):
                k = max(1, int(ww * (j + 1) / hh + 0.5))
                for i in range(-k, k + 1):
                    col = (255, 255, 255) if i == -k + 1 else (c if i <= 0 else tuple(int(v * 0.75) for v in c))
                    put(img, bx + i, h - hh + j, col)
        return outline(img, (72, 64, 128))
    CRY = crystal(1)
    # weerspiegelingen van palmen die er niet staan (omgekeerd, golvend, lila)
    for (cx, cy, im) in ((12, 6, PALM), (36, 27, PALM)):
        ref = im[::-1].copy()
        for j in range(48):
            ref[j] = np.roll(ref[j], int(round(1.2 * math.sin(j / 2.0))), 0)
            if j % 4 == 3:
                ref[j, :, 3] = 0
        m = ref[..., 3] > 127
        ref[m, :3] = ref[m, :3] * 0.5 + np.array([128, 128, 208]) * 0.5
        w.over(ref, cx * 16, cy * 16)
    w.stamp(PALM, 15, 24, solid_rows=1, over_rows=2)
    w.stamp(PALM2, 23, 24, solid_rows=1, over_rows=2)
    for c in ((17, 29), (23, 29), (25, 27), (3, 26), (6, 27)):
        w.stamp(CRY, *c)
    w.stamp(PALM, 3, 24, solid_rows=1, over_rows=2)
    # nep-eilanden: elk een palm; alles wat erbij hoort verdwijnt
    fake_cells = []
    for i, (f, (px, py)) in enumerate(zip(fakes, ((6, 16), (32, 18), (30, 13)))):
        w.stamp(PALM if i % 2 == 0 else PALM2, px, py, solid_rows=1, over_rows=2)
        cells = {(x, y) for y in range(H) for x in range(W) if f[y, x]}
        cells |= {(px + i2, py + j2) for i2 in range(3) for j2 in range(3)}
        fake_cells.append(sorted(cells))
        for (x, y) in cells:
            w.solid[y, x] = True
            w.elev1.add((x, y))
            w.water[y, x] = False
    # ---- tegelanimatie: glinsteringen op open water (periode 64 px)
    plain = np.zeros((H, W), bool)
    cellsum = np.zeros((H, W))
    ref = np.zeros((H * 16, W * 16, 3))
    ref[...] = base[yy % 64, xx % 64]
    same = (np.abs(w.bot - ref).sum(2) == 0) & ~(w.ovr[..., 3] > 0)
    for y in range(H):
        for x in range(W):
            plain[y, x] = same[y * 16:y * 16 + 16, x * 16:x * 16 + 16].all() and water[y, x]
    rr = random.Random(9)
    sparks = [(rr.randint(1, 62), rr.randint(1, 62), rr.randint(0, 7)) for _ in range(9)]
    tile64 = np.zeros((64, 64, 3))
    tile64[...] = base
    frames64 = []
    for f in range(8):
        t = tile64.copy()
        for sx, sy, ph in sparks:
            k = (f - ph) % 8
            if k in (0, 2):
                t[sy, sx] = WATER[5]
            elif k == 1:
                t[sy, sx] = WATER[5]
                for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    t[(sy + ddy) % 64, (sx + ddx) % 64] = WATER[4]
        frames64.append(t)
    for y in range(H):
        for x in range(W):
            if plain[y, x] and (x, y) not in w.anim and (x % 4, y % 4) in ((0, 0), (2, 1), (1, 2), (3, 3)):
                oy, ox = (y % 4) * 16, (x % 4) * 16
                w.anim[(x, y)] = [fr[oy:oy + 16, ox:ox + 16] for fr in frames64]
    w.plain_water = {(x % 4, y % 4): (x, y) for y in range(H) for x in range(W) if plain[y, x]}

    # ---- gedrag, botsing
    w.beh[water] = MB['MB_POND_WATER']
    for (x, y) in [c for f in fake_cells for c in f]:
        w.beh[y, x] = MB['MB_POND_WATER']
    w.solid[UB[1], UB[0]] = True
    w.arrive, w.ret, w.ub = (20, 27), (20, 29), UB
    w.ub_elev = 3
    w.border = (0, 28)
    w.fake_cells = fake_cells
    w.decor = [('FRILLISH', 12, 25, 'MOVEMENT_TYPE_WANDER_AROUND', 'Jelly', 1, 2),
               ('JELLICENT', 29, 25, 'MOVEMENT_TYPE_WANDER_AROUND', 'Jelly', 1, 2),
               ('NIHILEGO', 6, 13, 'MOVEMENT_TYPE_FACE_DOWN', 'Echo', 1, 0),
               ('NIHILEGO', 36, 11, 'MOVEMENT_TYPE_FACE_DOWN', 'Echo', 1, 0)]
    w.land, w.land_rate = None, 0
    w.surf, w.surf_rate = [('JELLICENT', 84, 86), ('PALAFIN', 84, 86), ('VELUZA', 83, 85), ('TENTACRUEL', 85, 87),
                           ('VAPOREON', 86, 88)], 4
    w.drop_kinds = []
    return w


# ====================================================================== Buzzwole: jungle met verkeerde verhoudingen
G = hexs('143818', '205a24', '2e7a2c', '48a038', '78c450', 'b4e470')     # mos/blad, donker -> licht


def leaf_img(w_, h_, ramp, seed, angle=0.0, vein=None):
    """plat liggend reuzenblad (spits ovaal) met nerven; RGBA"""
    img = img_new(w_, h_)
    cx, cy = w_ / 2 - 0.5, h_ / 2 - 0.5
    ca, sa = math.cos(angle), math.sin(angle)
    L, Wd = w_ / 2 - 2, h_ / 2 - 2
    for y in range(h_):
        for x in range(w_):
            u = ((x - cx) * ca + (y - cy) * sa) / L
            v = (-(x - cx) * sa + (y - cy) * ca) / Wd
            if abs(u) > 1:
                continue
            lim = (1 - u * u) ** 0.8 * (1 - 0.25 * u)
            if abs(v) > lim:
                continue
            t = 0.55 - 0.35 * v + 0.1 * u
            if abs(v) < 0.07:
                t = 0.92
            elif (abs(abs(v) - (abs(u * 1.3 + 0.2) % 0.33) * 2.4) < 0.09) and abs(v) < lim * 0.85:
                t = 0.8 if v < 0 else 0.35
            if abs(v) > lim - 0.12:
                t = 0.15
            img[y, x] = (*ramp_at(vein or ramp, t), 255)
    return img


def w_buzzwole():
    W, H = 40, 32
    w = World('Buzzwole', W, H, 1441)
    w.music, w.weather, w.speed = 'MUS_ROUTE119', 'WEATHER_NONE', 8
    yy, xx, dith = w.yy, w.xx, w.dith
    rnd = random.Random(41)
    # ---- mostapijt met klavertjes (periode 32)
    ty, tx, td = grid(32)
    n = pnoise(32, 4, 21)
    moss = np.zeros((32, 32, 3))
    moss[...] = G[2]
    moss[(n < -0.3) | ((n < -0.15) & (td < 0.5))] = G[1]
    moss[(n > 0.4) & (td < 0.4)] = G[3]
    for (cx, cy) in ((5, 6), (21, 3), (13, 18), (28, 22), (7, 27), (24, 12)):
        for (dx, dy) in ((0, -2), (-2, 1), (2, 1)):
            for (ox, oy) in ((0, 0), (1, 0), (0, 1), (1, 1)):
                moss[(cy + dy + oy) % 32, (cx + dx + ox) % 32] = G[4] if (ox, oy) != (1, 1) else G[3]
        moss[(cy + 2) % 32, cx % 32] = G[1]
    for (cx, cy) in ((16, 9), (2, 15), (30, 30), (19, 26)):
        moss[cy, cx] = G[5]
    w.tex(np.ones((H * 16, W * 16), bool), moss)
    # ---- pad van bladstrooisel
    DIRT = hexs('4c3018', '6c4824', '8c6434', 'a8844c', 'c8a868')
    dn = pnoise(32, 4, 22)
    dirt = np.zeros((32, 32, 3))
    dirt[...] = DIRT[2]
    dirt[(dn < -0.25) | ((dn < -0.1) & (td < 0.5))] = DIRT[1]
    dirt[(dn > 0.35) & (td < 0.5)] = DIRT[3]
    for (cx, cy, c) in ((4, 4, (184, 120, 48)), (20, 9, (200, 152, 64)), (12, 22, (160, 88, 40)), (27, 27, (200, 152, 64))):
        for i in range(4):
            dirt[(cy + i // 2) % 32, (cx + i) % 32] = c
    path = path_cells([(20, 28), (20, 25), (17, 23), (17, 19), (20, 17), (20, 13)])
    pm = np.zeros((H, W), bool)
    for x, y in path:
        pm[y, x] = True
        pm[y, x + 1 if x < 20 else x - 1] = True
    s = w.soft(pm, 6) + w.wob(16, 4, 23, 0.12)
    on = s > 0.5
    w.tex(on, dirt)
    rim = (s > 0.42) & ~on
    w.bot[rim & (dith < 0.5)] = DIRT[1]
    # ---- wanden van reuzengrassprieten (randen + plukken)
    wall = np.zeros((H, W), bool)
    wall[:3] = True; wall[-1:] = True; wall[:, :2] = True; wall[:, -2:] = True
    for (x0, y0, x1, y1) in ((2, 3, 4, 6), (35, 3, 37, 5), (2, 27, 5, 30), (34, 27, 37, 30), (12, 3, 13, 4), (27, 3, 29, 3)):
        wall[y0:y1 + 1, x0:x1 + 1] = True
    BL = hexs('103014', '1c4c20', '2c6e28', '4a9634', '74bc48', 'a8dc6c')
    wsoft = w.soft(wall, 5) + w.wob(16, 4, 24, 0.1)
    wpx = wsoft > 0.5
    wtex = np.zeros((48, 32, 3))
    wtex[...] = BL[0]
    rr = random.Random(25)
    for k in range(9):
        bx = rr.randint(0, 31)
        top = rr.randint(-20, 30)
        wd = rr.choice((7, 9, 11))
        curve = rr.uniform(-0.12, 0.12)
        for y in range(48):
            t = (y - top) / 48.0
            if t < 0:
                continue
            half = wd / 2 * min(1, 0.25 + t * 1.6)
            c = bx + curve * (y - top) ** 1.2 if y > top else bx
            for x in range(int(c - half) - 1, int(c + half) + 2):
                u = (x - c) / max(half, 0.5)
                if abs(u) > 1:
                    continue
                col = BL[4] if u < -0.55 else (BL[3] if u < 0.1 else (BL[2] if u < 0.7 else BL[1]))
                if abs(u) < 0.12 and t > 0.1:
                    col = BL[5]
                wtex[y % 48, x % 32] = col
    w.bot[wpx] = wtex[yy[wpx] % 48, xx[wpx] % 32]
    foot = wpx & ~np.roll(wpx, -2, 0)
    w.bot[foot] = BL[0]
    shadow = ~wpx & np.roll(wpx, 3, 0)
    w.bot[shadow] = w.bot[shadow] * 0.65
    w.solid |= wall
    # ---- boomstronk (arena) met Buzzwole erop
    scx, scy = 20 * 16 + 8, 7 * 16 + 4
    RX, RY = 74, 44
    e = ((xx - scx) / RX) ** 2 + ((yy - scy) / RY) ** 2
    topm = e <= 1
    side = (((xx - scx) / RX) ** 2 + ((yy - scy - 30) / RY) ** 2 <= 1) & (yy > scy) & ~topm & (np.abs(xx - scx) < RX)
    BARK = hexs('2c1c10', '4c3018', '6c4424', '8c5c30', 'a87c48')
    bark = BARK[2] * np.ones((H * 16, W * 16, 3))
    stripe = ((xx + (yy // 6) % 2) % 7)
    bark[stripe < 2] = BARK[1]
    bark[stripe == 4] = BARK[3]
    bark[(yy % 9 == 0) & (stripe < 5)] = BARK[0]
    w.bot[side] = bark[side]
    w.bot[side & (np.abs(xx - scx) > RX - 6)] = BARK[0]
    rings = np.sqrt(e)
    RING = hexs('b88850', 'd0a468', 'e4c084', 'f0d8a0')
    rv = (rings * 9) % 1
    top_col = np.where((rv < 0.18)[..., None], np.array(RING[0]), np.where((rv < 0.55)[..., None], np.array(RING[2]), np.array(RING[1])))
    w.bot[topm] = top_col[topm]
    w.bot[topm & (rings > 0.93)] = BARK[3]
    w.bot[topm & (rings > 0.97)] = BARK[1]
    crack = topm & (np.abs((xx - scx) * 0.5 - (yy - scy) * 1.2 - 8) < 0.8) & (rings < 0.7) & (rings > 0.15)
    w.bot[crack] = RING[0]
    # wortels als oprit (midden onder)
    ramp_px = (np.abs(xx - scx) < 20) & (yy > scy + 20) & (yy < scy + 82) & ~topm
    rr2 = ((xx - scx + 40) // 8) % 3
    w.bot[ramp_px] = np.where((rr2 == 1)[ramp_px][..., None], np.array(BARK[3]), np.array(BARK[2]))
    w.bot[ramp_px & ((xx - scx + 40) % 8 == 0)] = BARK[0]
    w.bot[ramp_px & ((yy - scy) % 10 == 0)] = BARK[1]
    for y in range(H):
        for x in range(W):
            blk = side[y * 16:y * 16 + 16, x * 16:x * 16 + 16].mean()
            rmp = ramp_px[y * 16:y * 16 + 16, x * 16:x * 16 + 16].mean()
            if blk > 0.35 and rmp < 0.3:
                w.solid[y, x] = True
            tp = topm[y * 16:y * 16 + 16, x * 16:x * 16 + 16].mean()
            if 0 < tp < 0.55 and rmp < 0.3 and not side[y * 16:y * 16 + 16, x * 16:x * 16 + 16].any():
                w.solid[y, x] = True          # rand van het stronkblad
    for x in range(W):
        for y in range(H):
            if topm[y * 16 + 8, x * 16 + 8] and not topm[min(y * 16 + 24, H * 16 - 1), x * 16 + 8] and \
                    not ramp_px[min(y * 16 + 24, H * 16 - 1), x * 16 + 8]:
                w.solid[y, x] = w.solid[y, x] or False
    # ---- halters van bessen (Buzzwole traint met planten)
    def barbell(c1, c2):
        img = img_new(80, 32)
        for x in range(10, 70):
            for y in range(14, 19):
                put(img, x, y, (216, 196, 120) if y < 16 else (168, 140, 72))
            if x % 12 == 0:
                for y in range(14, 19):
                    put(img, x, y, (120, 100, 48))
        for (bx, col) in ((12, c1), (66, c2)):
            for y in range(32):
                for x in range(80):
                    d = math.hypot((x - bx) / 11.5, (y - 16) / 14.5)
                    if d <= 1:
                        sh = (x - bx) * 0.05 + (y - 16) * 0.06
                        k = 2 if sh < -0.35 else (1 if sh < 0.35 else 0)
                        c = col[k]
                        if d > 0.88:
                            c = col[0]
                        put(img, x, y, c)
            put(img, bx - 4, 7, (255, 255, 255)); put(img, bx - 3, 7, (255, 255, 255)); put(img, bx - 4, 8, (255, 255, 255))
            for y in range(2, 6):
                put(img, bx, y, (72, 112, 40))
        return outline(img, (32, 24, 16))
    ORAN = [(32, 64, 136), (56, 112, 200), (120, 176, 240)]
    PECHA = [(152, 56, 96), (224, 112, 152), (248, 184, 208)]
    w.stamp(barbell(ORAN, PECHA), 15, 4, solid_rows=2)
    w.stamp(barbell(PECHA, ORAN), 21, 9, solid_rows=2)
    # ---- reuzenpaddenstoelen (zelfde ontwerp, even posities -> gedeelde tiles)
    def mushroom(cap, spot):
        img = img_new(64, 80)
        for y in range(80):
            for x in range(64):
                if y < 44:
                    d = ((x - 31.5) / 31) ** 2 + ((y - 40) / 36) ** 2
                    if d <= 1 and y < 40:
                        sh = (x - 31.5) / 31 * 0.6 + (y - 20) / 30 * 0.6
                        k = 3 if sh < -0.3 else (2 if sh < 0.25 else (1 if sh < 0.6 else 0))
                        img[y, x] = (*cap[k], 255)
                    elif 36 <= y < 44 and abs(x - 31.5) < 30 - (y - 36) * 2:
                        img[y, x] = (*((200, 184, 160) if (x // 3) % 2 else (168, 148, 128)), 255)
                elif abs(x - 31.5) < 11 - (79 - y) / 30.0 and y >= 40:
                    u = (x - 31.5) / 11
                    img[y, x] = (*((248, 240, 220) if u < -0.4 else ((224, 212, 188) if u < 0.4 else (176, 160, 136))), 255)
        rr = random.Random(77)
        for _ in range(9):
            sx, sy, rad = rr.randint(10, 52), rr.randint(6, 30), rr.choice((2.5, 3.5, 4.5))
            for y in range(int(sy - rad), int(sy + rad) + 1):
                for x in range(int(sx - rad), int(sx + rad) + 1):
                    if math.hypot(x - sx, y - sy) <= rad and 0 <= y < 40 and img[y, x, 3] > 0:
                        img[y, x, :3] = spot if math.hypot(x - sx + 1, y - sy + 1) > 1.2 else (255, 255, 255)
        return outline(img, (24, 16, 32))
    CAP = hexs('2a1850', '4a2c88', '7048b8', '9c70dc')
    MUSH = mushroom(CAP, (248, 216, 72))
    for (cx, cy) in ((4, 8), (30, 10), (8, 20), (32, 20)):
        w.stamp(MUSH, cx, cy, solid_rows=2, over_rows=3)
    # ---- druppels zo groot als een huis
    def place_drop(cx, cy, S=48):
        px, py = cx * 16, cy * 16
        ly, lx = np.mgrid[0:S, 0:S]
        c = S / 2 - 0.5
        d = np.hypot((lx - c) / (c - 1), (ly - c - S * 0.06) / (c - 1.5))
        m = (d <= 1) | ((ly < S * 0.3) & (np.abs(lx - c) < (ly - 1) * 0.8))
        reg = w.bot[py:py + S, px:px + S]
        flipped = reg[::-1, ::-1].copy()                                   # breking: de wereld op zijn kop
        sh = np.zeros_like(m)
        sh[4:, 4:] = m[:-4, :-4]
        reg[sh & ~m] = reg[sh & ~m] * 0.6
        inner = flipped * 0.5 + np.array([128, 208, 224]) * 0.5
        reg[m] = inner[m]
        edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
        reg[m & (d > 0.84)] = (88, 160, 192)
        reg[edge] = (40, 88, 120)
        reg[m & (np.hypot(lx - S * 0.32, ly - S * 0.38) < S * 0.08)] = (255, 255, 255)
        reg[m & (np.hypot(lx - S * 0.26, ly - S * 0.5) < S * 0.035)] = (255, 255, 255)
        reg[m & (np.abs(np.hypot(lx - c, ly - c) - S * 0.33) < 1.0) & (lx > c + 2) & (ly > c + 2)] = (232, 252, 252)
        n = S // 16
        for j in range(n):
            for i in range(n):
                if m[j * 16:j * 16 + 16, i * 16:i * 16 + 16].mean() > 0.2:
                    w.solid[cy + j, cx + i] = True
    for (cx, cy) in ((26, 14), (12, 13), (24, 26)):
        place_drop(cx, cy)
    place_drop(36, 17, 32)
    # ---- liggende reuzenbladeren (beloopbaar)
    LEAFR = hexs('2c6c20', '4c9430', '74bc40', '9cd858', 'd0f088')
    for (cx, cy, wl, hl, ang) in ((5, 14, 96, 48, -0.25), (27, 23, 112, 48, 0.15), (9, 25, 80, 40, 0.4)):
        w.over(leaf_img(wl, hl, LEAFR, cx, ang), cx * 16, cy * 16)
    # ---- piepkleine boompjes (beloopbaar: ze zijn te klein om in de weg te staan)
    def tiny_tree(seed):
        img = img_new(16, 16)
        for y in range(9, 15):
            put(img, 7, y, (112, 72, 40)); put(img, 8, y, (80, 48, 24))
        for y in range(1, 11):
            for x in range(2, 14):
                if math.hypot(x - 7.5, (y - 6) * 1.2) < 5.6:
                    img[y, x] = (*((96, 176, 72) if x + y < 13 else (56, 128, 48)), 255)
        put(img, 5, 4, (168, 224, 112)); put(img, 6, 3, (168, 224, 112))
        return outline(img, (24, 48, 24))
    TT = tiny_tree(1)
    for (cx, cy) in ((14, 18), (24, 18), (6, 18), (30, 26), (14, 28), (36, 22), (18, 26), (28, 16)):
        if not w.solid[cy, cx]:
            w.over(TT, cx * 16, cy * 16)
    # ---- een reuzenlieveheersbeestje (echte sprite, 2x vergroot: bij deze verhoudingen hoort het zo)
    im = load_mon('ledyba')
    a = im[..., 3] > 127
    ys, xs = np.nonzero(a)
    im = im[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    im = np.kron(im, np.ones((2, 2, 1)))
    im = outline(im, (16, 16, 16))
    hh, ww_ = im.shape[:2]
    pad = img_new(((ww_ + 15) // 16) * 16, ((hh + 15) // 16) * 16)
    pad[pad.shape[0] - hh:, :ww_] = im
    w.stamp(pad, 32, 1, solid_rows=2, over_rows=pad.shape[0] // 16 - 2)
    # ---- reuzenbloem (rafflesia) met een poel nectar
    def flower():
        img = img_new(64, 64)
        PET = hexs('701830', 'a83048', 'd85868', 'f09098')
        for y in range(64):
            for x in range(64):
                a_ = math.atan2(y - 31.5, x - 31.5)
                r_ = math.hypot(x - 31.5, y - 31.5)
                rad = 30 * (0.72 + 0.28 * abs(math.cos(2.5 * a_)))
                if r_ <= rad:
                    t = r_ / rad
                    k = 3 if t > 0.85 else (2 if t > 0.55 else 1)
                    c = PET[k]
                    if (int(x / 5) + int(y / 5)) % 3 == 0 and 0.3 < t < 0.85:
                        c = (248, 232, 216)
                    if r_ < 12:
                        c = (248, 200, 72) if r_ < 9 else PET[0]
                        if r_ < 5:
                            c = (255, 240, 160)
                    img[y, x] = (*c, 255)
        return outline(img, (48, 8, 24))
    w.stamp(flower(), 34, 12, solid_rows=4)
    # ---- reuzenspruiten (hoog gras: wilde Pokemon)
    SPR = hexs('1c4820', '2c6c2c', '5aa040', '8cd060')
    grassm = np.zeros((H, W), bool)
    for (x0, y0, x1, y1) in ((3, 20, 6, 23), (29, 26, 33, 29), (31, 6, 35, 8), (5, 9, 8, 11), (13, 21, 15, 24)):
        grassm[y0:y1 + 1, x0:x1 + 1] = True
    grassm &= ~w.solid
    sprout = np.zeros((16, 16, 4))
    for (bx, h0) in ((3, 12), (8, 15), (12, 11)):
        for y in range(16 - h0, 16):
            for dx in (-1, 0, 1):
                c = SPR[3] if dx < 0 else (SPR[2] if dx == 0 else SPR[1])
                sprout[y, (bx + dx) % 16] = (*c, 255)
        for (ox, oy) in ((-2, 0), (-1, -1), (0, -1), (1, -1), (2, 0), (-1, 0), (0, 0), (1, 0)):
            sprout[16 - h0 + oy + 1, (bx + ox) % 16] = (*SPR[3], 255)
        sprout[16 - h0, bx] = (248, 232, 120, 255)
    for y in range(H):
        for x in range(W):
            if grassm[y, x]:
                w.over(sprout, x * 16, y * 16)
                w.beh[y, x] = MB['MB_TALL_GRASS']
    w.arrive, w.ret, w.ub = (20, 28), (20, 30), (20, 6)
    w.ub_elev = 3
    w.border = (0, 0)
    w.item_spots = [(36, 9)]
    w.decor = [('HERACROSS', 17, 6, 'MOVEMENT_TYPE_WALK_IN_PLACE_DOWN', 'Lifter', 3, 0),
               ('COMBEE', 10, 17, 'MOVEMENT_TYPE_WANDER_AROUND', 'Bug', 3, 2),
               ('PINSIR', 28, 19, 'MOVEMENT_TYPE_FACE_LEFT', 'Bug', 3, 0)]
    w.land, w.land_rate = [('HERACROSS', 84, 86), ('PINSIR', 84, 86), ('LURANTIS', 84, 86), ('GOLISOPOD', 85, 87),
                           ('VIKAVOLT', 85, 87), ('RIBOMBEE', 84, 86), ('SCOLIPEDE', 85, 87), ('ESCAVALIER', 85, 87),
                           ('BRELOOM', 85, 87), ('TROPIUS', 85, 87), ('HAWLUCHA', 86, 88), ('KLEAVOR', 87, 89)], 15
    w.texts = [('UltraSpace_Buzzwole_Text_Bug', 'It is the size of a normal bug.\nHere, that makes it a speck.\\p'
                'It looks at the giant mushrooms and\nfeels nothing. Respect.')]
    w.bgs = [{'type': 'sign', 'x': 22, 'y': 9, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
              'script': 'UltraSpace_Buzzwole_EventScript_Barbell'}]
    w.texts.append(('UltraSpace_Buzzwole_Text_Barbell', 'Two giant BERRIES on a stick.\\pThe sticker says: “ORGANIC. 900 KG.\nDO NOT EAT BETWEEN SETS.”'))
    return w


# ====================================================================== Pheromosa: elementen zonder effect op elkaar
def load_anim_png(path, fw, fh):
    """battle-animatieplaatje (geïndexeerd, index 0 = transparant) -> lijst frames RGBA"""
    im = Image.open(path)
    idx = np.array(im)
    pal = im.getpalette()
    out = np.zeros(idx.shape + (4,))
    for i in range(16):
        out[idx == i] = (pal[i * 3], pal[i * 3 + 1], pal[i * 3 + 2], 0 if i == 0 else 255)
    fr = []
    for y in range(0, idx.shape[0], fh):
        for x in range(0, idx.shape[1], fw):
            fr.append(out[y:y + fh, x:x + fw])
    return fr


FIRE5 = hexs('a01800', 'e04800', 'f89800', 'f8e040', 'f8f8e0')


def fire_frames():
    """de vlammen uit de vuuraanval (8 frames, 32x32), teruggebracht naar 5 kleuren"""
    out = []
    for f in load_anim_png('graphics/battle_anims/sprites/fire.png', 32, 32):
        g = f.copy()
        L = (0.3 * f[..., 0] + 0.59 * f[..., 1] + 0.11 * f[..., 2]) / 255
        k = np.clip((L * 5.2 - 0.6).astype(int), 0, 4)
        g[..., :3] = np.array(FIRE5, float)[k]
        out.append(g)
    return out


def anim_block(w, cx, cy, frames, base=None, nx=2, ny=2):
    """frames (8 x RGBA, nx*16 x ny*16) over de huidige onderlaag (of base: 8 achtergronden) -> animcellen"""
    px, py = cx * 16, cy * 16
    bg = w.bot[py:py + ny * 16, px:px + nx * 16].copy()
    comp = []
    for f in range(8):
        b = (base[f] if base is not None else bg).copy()
        fr = frames[f % len(frames)]
        m = fr[..., 3] > 127
        b[m] = fr[m, :3]
        comp.append(b)
    w.bot[py:py + ny * 16, px:px + nx * 16] = comp[0]
    for j in range(ny):
        for i in range(nx):
            w.anim[(cx + i, cy + j)] = [c[j * 16:j * 16 + 16, i * 16:i * 16 + 16] for c in comp]


def speckle_tex(base, details, seed, P=32):
    """effen ondergrond met losse details (Gen 3-stijl), naadloos P x P. details: [(patroon, kleuren, aantal)];
    patroon = lijst regels, cijfer k = kleuren[k-1], '.' = niets"""
    t = np.zeros((P, P, 3))
    t[...] = base
    rr = random.Random(seed)
    for pat, cols, n in details:
        for _ in range(n):
            x0, y0 = rr.randint(0, P - 1), rr.randint(0, P - 1)
            for j, row in enumerate(pat):
                for i, ch in enumerate(row):
                    if ch != '.':
                        t[(y0 + j) % P, (x0 + i) % P] = cols[int(ch) - 1]
    return t


def w_pheromosa():
    W, H = 40, 32
    w = World('Pheromosa', W, H, 1442)
    w.music, w.weather, w.speed, w.cspeed = 'MUS_LILYCOVE_MUSEUM', 'WEATHER_NONE', 6, 8
    yy, xx, dith = w.yy, w.xx, w.dith
    LAVA = hexs('c02800', 'f06008', 'f8a018', 'f8e060')
    WAT = hexs('2058a8', '3080d0', '58a8e8', '98d0f8')
    w.cycles = [LAVA, WAT]
    ICE = hexs('6890b8', '98c0e0', 'c0e0f0', 'e8f8f8')
    ASH = hexs('282020', '403430', '5c4c44', '806858')
    EARTH = hexs('583818', '805428', 'a47840', 'c89c5c')
    GRASS = hexs('285c2c', '387c34', '58a040', '88c858')
    ROCK = hexs('3c2c28', '5c443c', '806050', 'a88470', 'c8a890')
    MARB = hexs('a8a0b8', 'd0c8d8', 'f0ecf4', 'ffffff')
    # ---- de leegte (sterren) rond het zwevende land
    VOID = hexs('100820', '1c1034', '2c2048')
    vn = pnoise(32, 4, 31)
    vt = np.zeros((32, 32, 3))
    vt[...] = VOID[0]
    vt[(vn > 0.3) & (grid(32)[2] < 0.5)] = VOID[1]
    for (sx, sy, c) in ((5, 7, (232, 224, 248)), (22, 3, (168, 160, 216)), (14, 20, (232, 224, 248)), (28, 26, (168, 160, 216))):
        vt[sy, sx] = c
    vt[20, 13] = vt[21, 14] = vt[19, 14] = vt[20, 15] = (120, 112, 184)
    w.tex(np.ones((H * 16, W * 16), bool), vt)
    # ---- celindeling: land, waterrivier (west -> oost), lavarivier (noord -> zuid), kruising onder het podium
    land = np.zeros((H, W), bool)
    land[2:30, 2:38] = True
    for (x, y) in ((2, 2), (37, 2), (2, 29), (37, 29), (3, 2), (2, 3), (36, 2), (37, 3), (2, 28), (37, 28), (3, 29), (36, 29),
                   (2, 9), (2, 10), (37, 21), (37, 22), (12, 2), (13, 2), (28, 29), (29, 29), (10, 29)):
        land[y, x] = False
    watc = np.zeros((H, W), bool)
    lavc = np.zeros((H, W), bool)
    def wrow(x):
        return 13 if x < 9 else (15 if x < 31 else 16)

    def lcol(y):
        return 22 if y < 8 else (20 if y < 23 else 18)
    for x in range(0, W):
        c = wrow(x)
        watc[c - 1:c + 2, x] = True
    for y in range(0, H):
        c = lcol(y)
        lavc[y, c - 1:c + 2] = True
    lavc &= ~watc
    watc &= land | np.roll(land, 1, 1) | np.roll(land, -1, 1)
    lavc &= land | np.roll(land, 1, 0) | np.roll(land, -1, 0)
    ls = w.soft(land, 7) + w.wob(16, 4, 32, 0.12)
    landpx = ls > 0.5
    # kwadranten (per cel, met de rivieren ertussen)
    quad = np.zeros((H, W), int)
    for y in range(H):
        for x in range(W):
            wc = wrow(x)
            lc = lcol(y)
            quad[y, x] = (0 if y < wc else 2) + (0 if x < lc else 1)    # 0 NW ijs, 1 NO aarde, 2 ZW as, 3 ZO gras
    qpx = np.kron(quad, np.ones((16, 16), int))
    ice_t = speckle_tex(ICE[2], [(['44', '.4'], [None, None, None, ICE[3]], 0),
                                 (['4.', '.4', '..', '..'], [None, None, None, ICE[3]], 6),
                                 (['1'], [ICE[1]], 10), (['33'], [None, None, ICE[3]], 8)], 51)
    ice_t[(grid(32)[1] + grid(32)[0]) % 32 == 0] = ICE[3]
    ash_t = speckle_tex(ASH[1], [(['3'], [None, None, ASH[2]], 30), (['1'], [ASH[0]], 22), (['o'.replace('o', '1')], [(232, 96, 24)], 4),
                                 (['11', '1.'], [ASH[2]], 6)], 52)
    earth_t = speckle_tex(EARTH[2], [(['22', '21'], [EARTH[1], EARTH[3]], 7), (['1'], [EARTH[1]], 18),
                                     (['2'], [None, EARTH[3]], 14)], 53)
    grass_t = speckle_tex(GRASS[2], [(['1.1', '.1.'], [GRASS[3]], 9), (['1'], [GRASS[1]], 26), (['1'], [(240, 240, 248)], 5),
                                     (['2.2', '.2.'], [None, GRASS[1]], 6)], 54)
    for qi, t in enumerate((ice_t, earth_t, ash_t, grass_t)):
        w.tex(landpx & (qpx == qi), t)
    # klifrand onder het zwevende land
    face = ~landpx & np.roll(landpx, 9, 0)
    cl = np.zeros((H * 16, W * 16, 3))
    cl[...] = ROCK[2]
    cl[(xx + (yy // 3)) % 6 < 2] = ROCK[1]
    cl[(xx % 6 == 3) & (yy % 4 == 0)] = ROCK[3]
    w.bot[face] = cl[face]
    w.bot[face & ~np.roll(landpx, 7, 0)] = ROCK[0]
    w.bot[landpx & ~np.roll(landpx, -1, 0)] = ROCK[3]
    # ---- rivieren (vervaagd celmasker: randen hangen alleen van de buren af; banden lopen via de paletcyclus)
    ws = w.soft(watc, 9) + w.wob(16, 4, 33, 0.06)
    lsft = w.soft(lavc, 9) + w.wob(16, 4, 34, 0.06)
    wat = (ws > 0.5) & (landpx | (yy % 1 == 0))
    lav = (lsft > 0.5) & ~wat
    tn = pnoise(32, 4, 38)[yy % 32, xx % 32]
    wb = ((xx / 8.0 + 1.6 * tn).astype(int)) % 4
    lb = ((yy / 8.0 + 1.6 * pnoise(32, 4, 39)[yy % 32, xx % 32]).astype(int)) % 4
    w.bot[wat] = np.array(WAT, float)[wb[wat]]
    w.bot[lav] = np.array(LAVA, float)[lb[lav]]
    cr = pnoise(32, 4, 40)[yy % 32, xx % 32]
    w.bot[lav & (cr > 0.42)] = (88, 24, 16)
    w.bot[lav & (cr > 0.58)] = (48, 16, 16)
    w.bot[wat & (((xx % 32) * 3 + (yy % 32) * 7) % 29 == 0)] = (240, 248, 248)
    w.bot[lav & (~np.roll(lav, 1, 1) | ~np.roll(lav, -1, 1))] = (48, 16, 16)
    w.bot[(wat | lav) & ~np.roll(wat | lav, -1, 0) & landpx] = (24, 16, 32)
    # buiten het land vallen ze de leegte in (bandjes naar beneden)
    off = ~landpx & ~face
    w.bot[wat & off] = np.array(WAT, float)[((yy[wat & off] // 4) % 4)]
    w.bot[lav & off] = np.array(LAVA, float)[((yy[lav & off] // 4) % 4)]
    # ---- podium van marmer op de kruising
    cx0, cy0 = 20 * 16 + 8, 15 * 16 + 8
    d = np.hypot(xx - cx0, yy - cy0)
    plat = d < 42
    w.bot[plat] = MARB[2]
    w.bot[plat & (pnoise(32, 4, 41)[yy % 32, xx % 32] > 0.35) & (dith < 0.5)] = MARB[1]
    vein = plat & (np.abs(np.sin((xx - yy) / 9.0 + pnoise(32, 2, 42)[yy % 32, xx % 32] * 3)) < 0.07)
    w.bot[vein] = MARB[0]
    w.bot[plat & (np.abs(d - 35) < 1.1)] = (200, 152, 64)
    w.bot[plat & (np.abs(d - 37) < 0.7)] = (248, 216, 120)
    w.bot[(d >= 42) & (d < 45)] = MARB[0]
    w.bot[(d >= 45) & (d < 49) & (yy > cy0 + 10)] = (80, 72, 96)
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        sx, sy = cx0 + math.cos(a) * 28, cy0 + math.sin(a) * 28
        dd = np.hypot(xx - sx, yy - sy)
        sym = dd < 3.6
        w.bot[sym] = [(248, 104, 24), (56, 136, 232), (248, 224, 72), (152, 216, 248)][k % 4]
        w.bot[sym & (dd < 1.6)] = (255, 255, 255)
    # marmeren pad van de aankomst naar het podium
    path = path_cells([(28, 27), (28, 22), (24, 22), (24, 18), (22, 18)])
    pm = np.zeros((H, W), bool)
    for c in path:
        pm[c[1], c[0]] = True
    pt = w.cells(pm) & (np.abs((xx % 16) - 7.5) < 7) & (np.abs((yy % 16) - 7.5) < 7) & ~plat & ~wat & ~lav
    w.bot[pt] = MARB[2]
    w.bot[pt & (((xx % 16) == 1) | ((yy % 16) == 1))] = MARB[3]
    w.bot[pt & (((xx % 16) == 14) | ((yy % 16) == 14))] = MARB[0]
    # ---- vuur dat op het water brandt, bliksem in de lava, ijs in het vuur, vuur op het ijs
    FIRE = fire_frames()

    def interior(m, cx, cy, nx=2, ny=2):
        return all(m[cy + j, cx + i] and m[cy + j - 1:cy + j + 2, cx + i - 1:cx + i + 2].all() for j in range(ny) for i in range(nx))
    for (cx, cy) in ((6, 14), (32, 14)):
        anim_block(w, cx, cy, FIRE)
    def bolt_frames(bg):
        out = []
        rr = random.Random(43)
        pts = [(16, 0)]
        while pts[-1][1] < 38:
            x, y = pts[-1]
            pts.append((max(6, min(25, x + rr.randint(-6, 6))), y + rr.randint(4, 8)))
        for f in range(8):
            b = bg.copy()
            bright = f % 4 in (0, 1)
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                n = max(abs(x1 - x0), abs(y1 - y0))
                for i in range(n + 1):
                    x = int(round(x0 + (x1 - x0) * i / n)); y = int(round(y0 + (y1 - y0) * i / n))
                    if 0 <= y < 48:
                        for dx in (-1, 0, 1):
                            if 0 <= x + dx < 32:
                                b[y, x + dx] = (248, 248, 224) if dx == 0 else ((248, 224, 96) if bright else (184, 152, 64))
            yc, xc = min(pts[-1][1], 44), pts[-1][0]
            for y in range(30, 48):
                for x in range(32):
                    r_ = math.hypot((x - xc) / 1.6, y - yc)
                    if abs(r_ - (2 + (f % 4) * 1.6)) < 0.8:
                        b[y, x] = (248, 248, 224)
            out.append(b)
        return out
    for (cx, cy) in ((21, 3), (17, 24)):
        bg = w.bot[cy * 16:cy * 16 + 48, cx * 16:cx * 16 + 32].copy()
        fr = bolt_frames(bg)
        for j in range(3):
            for i in range(2):
                w.anim[(cx + i, cy + j)] = [f[j * 16:j * 16 + 16, i * 16:i * 16 + 16] for f in fr]
        w.bot[cy * 16:cy * 16 + 48, cx * 16:cx * 16 + 32] = fr[0]
        w.solid[cy + 2, cx] = w.solid[cy + 2, cx + 1] = True
    def ice_crystal():
        img = img_new(32, 32)
        for (bx, h, wd) in ((10, 22, 4), (18, 28, 5), (25, 16, 3)):
            for j in range(h):
                k = max(1, int(wd * min(1, (j + 2) / 6)))
                for i in range(-k, k + 1):
                    col = ICE[3] if i < 0 else (ICE[2] if i < k - 1 else ICE[1])
                    if j > h - 3:
                        col = (255, 255, 255)
                    put(img, bx + i, 31 - j, col)
        return outline(img, (40, 64, 104))
    CR = ice_crystal()
    for (cx, cy) in ((6, 21), (12, 25), (10, 19), (4, 25), (14, 21), (8, 27)):
        base_bg = w.bot[cy * 16:cy * 16 + 32, cx * 16:cx * 16 + 32].copy()
        frames = []
        for f in range(8):
            b = base_bg.copy()
            fr = FIRE[f]
            m = fr[..., 3] > 127
            b[m] = fr[m, :3]
            m2 = CR[..., 3] > 127
            b[m2] = CR[m2, :3]
            frames.append(np.concatenate([b, np.full((32, 32, 1), 255.0)], 2))
        anim_block(w, cx, cy, frames)
        w.solid[cy + 1, cx] = w.solid[cy + 1, cx + 1] = True
    for (cx, cy) in ((8, 5), (14, 9), (10, 3), (16, 11)):
        anim_block(w, cx, cy, FIRE)
        w.solid[cy + 1, cx] = w.solid[cy + 1, cx + 1] = True
    for (cx, cy, f) in ((4, 7, 2), (12, 4, 5), (16, 6, 1)):
        fr = FIRE[f]
        reg = w.bot[cy * 16:cy * 16 + 32, cx * 16:cx * 16 + 32]
        m = fr[..., 3] > 127
        reg[m] = fr[m, :3] * 0.5 + np.array(ICE[2]) * 0.5
        ly, lx = np.mgrid[0:32, 0:32]
        reg[m & ((lx + ly) % 7 == 0)] = ICE[3]
        reg[(lx == 0) | (ly == 0)] = reg[(lx == 0) | (ly == 0)]
        w.solid[cy + 1, cx] = w.solid[cy + 1, cx + 1] = True
    # vlammetjes die in het gras bloeien zonder iets te verbranden (zuidoost)
    small = []
    for f in FIRE:
        im = Image.fromarray(np.clip(f, 0, 255).astype(np.uint8), 'RGBA').resize((16, 16), Image.NEAREST)
        small.append(np.array(im).astype(float))
    for (cx, cy) in ((32, 20), (34, 24), (26, 24), (32, 26), (24, 20), (36, 22), (30, 24), (34, 28), (36, 18), (22, 26)):
        anim_block(w, cx, cy, small, nx=1, ny=1)
    # aardschokken (noordoost): scheuren en zwevende brokken grond
    def chunk(seed):
        img = img_new(32, 32)
        top = [int(5 + 3 * math.sin(i / 4.0 + seed)) for i in range(32)]
        for x in range(3, 29):
            for y in range(top[x], 22 - abs(x - 16) // 2):
                col = EARTH[2] if y < top[x] + 4 else (ROCK[2] if (x + y) % 5 else ROCK[1])
                if y == top[x]:
                    col = EARTH[3]
                put(img, x, y, col)
        return outline(img, (24, 16, 16))
    CH = [chunk(1), chunk(2)]
    for (cx, cy, k) in ((26, 6, 0), (32, 8, 1), (30, 4, 1), (34, 11, 0), (36, 8, 0), (28, 12, 1), (0, 12, 0), (38, 6, 1), (8, 0, 1), (16, 30, 0), (36, 30, 1)):
        reg = w.bot[(cy + 1) * 16:(cy + 3) * 16, cx * 16:(cx + 2) * 16]
        msk = CH[k][..., 3] > 127
        if reg.shape[:2] == (32, 32):
            reg[msk & (B4[np.mgrid[0:32, 0:32][0] % 4, np.mgrid[0:32, 0:32][1] % 4] < 0.5)] *= 0.5
        w.over(CH[k], cx * 16, cy * 16)
        if 0 < cy < H - 1 and land[cy, cx]:
            w.solid[cy, cx] = w.solid[cy, cx + 1] = True
    crk = speckle_tex(EARTH[2], [], 0)
    for (x0, y0, pts) in ((27 * 16, 9 * 16, [(0, 0), (6, 3), (9, 10), (16, 12), (22, 20), (30, 22)]),
                          (31 * 16 + 4, 4 * 16, [(0, 0), (-4, 8), (-2, 15), (-8, 24)])):
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            n = max(abs(bx - ax), abs(by - ay))
            for i in range(n + 1):
                x = x0 + ax + (bx - ax) * i // n; y = y0 + ay + (by - ay) * i // n
                w.bot[y, x] = (40, 24, 16); w.bot[y, x + 1] = (40, 24, 16); w.bot[y + 1, x] = EARTH[3]
    # een breuklijn van de aardbeving: de grond erboven ligt hoger
    fl = (yy >= 10 * 16) & (yy < 10 * 16 + 5) & (xx > 24 * 16 + 4) & (xx < 36 * 16) & landpx & (qpx == 1)
    w.bot[fl] = np.where(((xx[fl] // 3) % 3 == 0)[..., None], np.array(EARTH[0]), np.array(EARTH[1]))
    w.bot[fl & (yy == 10 * 16)] = EARTH[3]
    sh = (yy >= 10 * 16 + 5) & (yy < 10 * 16 + 8) & (xx > 24 * 16 + 4) & (xx < 36 * 16) & landpx & (qpx == 1)
    w.bot[sh] = w.bot[sh] * 0.75
    # onweerswolk die in de lava regent (geen stoom: het maakt niks uit)
    cloud = img_new(64, 32)
    for (bx, by, r_) in ((14, 18, 11), (30, 13, 13), (46, 17, 11), (24, 21, 9), (40, 22, 8)):
        for y in range(32):
            for x in range(64):
                if math.hypot(x - bx, (y - by) * 1.2) < r_:
                    c = (120, 112, 144) if y > by + r_ * 0.3 else ((184, 176, 208) if y < by - r_ * 0.4 else (152, 144, 176))
                    cloud[y, x] = (*c, 255)
    outline(cloud, (40, 32, 56))
    w.stamp(cloud, 17, 8, solid_rows=0, over_rows=2)
    for k in range(9):
        x0 = 17 * 16 + 6 + k * 6
        for j in range(10 * 16, 13 * 16, 7):
            for i in range(4):
                if (j + i + k * 3) % 13 < 9 and lav[j + i, x0 - i // 2]:
                    w.bot[j + i, x0 - i // 2] = (200, 224, 248)
    # bevroren bliksem in het ijs (noordwest)
    rr = random.Random(45)
    x, y = 6 * 16 + 8, 2 * 16 + 10
    while y < 6 * 16:
        nx_, ny_ = x + rr.randint(-6, 6), y + rr.randint(4, 7)
        for t in np.linspace(0, 1, 12):
            px_, py_ = int(x + (nx_ - x) * t), int(y + (ny_ - y) * t)
            w.bot[py_, px_ - 1:px_ + 2] = (168, 216, 248)
            w.bot[py_, px_] = (248, 248, 255)
        x, y = nx_, ny_
    # ---- botsing en gedrag
    for y in range(H):
        for x in range(W):
            if landpx[y * 16:y * 16 + 16, x * 16:x * 16 + 16].mean() < 0.5:
                w.solid[y, x] = True
            elif wat[y * 16:y * 16 + 16, x * 16:x * 16 + 16].mean() > 0.5:
                w.beh[y, x] = MB['MB_SHALLOW_WATER']
    w.arrive, w.ret, w.ub = (28, 26), (28, 28), (20, 15)
    w.solid[15, 20] = False
    w.beh[~w.solid & (w.beh == 0)] = MB['MB_CAVE']          # wilde Pokemon op het land (niet op het water)
    w.ub_elev = 3
    w.border = (0, 0)
    w.decor = [('CASTFORM', 10, 11, 'MOVEMENT_TYPE_WANDER_AROUND', 'Weather', 3, 2),
               ('ROTOM', 30, 20, 'MOVEMENT_TYPE_WANDER_AROUND', 'Weather', 3, 2)]
    w.drop_kinds = ['Judge', 'Crowd']
    w.land, w.land_rate = [('CASTFORM', 84, 86), ('ROTOM', 84, 86), ('MAGMORTAR', 85, 87), ('ELECTIVIRE', 85, 87),
                           ('ABOMASNOW', 85, 87), ('FLAREON', 85, 87), ('JOLTEON', 85, 87), ('GLACEON', 85, 87),
                           ('LEAFEON', 85, 87), ('SALAZZLE', 85, 87), ('VOLCARONA', 87, 89), ('ARCANINE', 87, 89)], 6
    w.bgs = [{'type': 'sign', 'x': 30, 'y': 25, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
              'script': 'UltraSpace_Pheromosa_EventScript_Treaty'}]
    w.solid[25, 30] = True
    w.texts = [('UltraSpace_Pheromosa_Text_Treaty', 'THE ELEMENTAL TREATY\\pArticle 1: Nothing affects anything.\nArticle 2: See article 1.\\p'
                'Article 3: Fire may sit in water if it\nwants to. Water is fine with it.'),
               ('UltraSpace_Pheromosa_Text_Weather', 'It tried to change the weather.\nThe weather did not care.\\p'
                'Nothing here cares. It is very\nrelaxing, in a horrifying way.')]
    return w


def cable_strip(cols, period=32, seed=0, power=None):
    """32 px brede baan van drie dikke kabels (horizontaal), naadloos in x (periode 32); cols: 3 ramps (donker->licht)"""
    t = np.zeros((32, period, 4))
    prof = [0, 1, 1, 2, 3, 3, 2, 2, 1, 1, 0]                 # schaduw over de doorsnede van een ronde kabel
    rr = random.Random(seed)
    for k in range(3):
        y0 = 1 + k * 10
        ramp = cols[k]
        for j, p in enumerate(prof[:10]):
            t[y0 + j, :, :3] = ramp[min(p, len(ramp) - 1)]
            t[y0 + j, :, 3] = 255
        if power is not None and k == 1:                     # stroompuls: banden in de paletcyclus
            for x in range(period):
                for j in range(2, 8):
                    t[y0 + j, x, :3] = power[((x // 4) + (j > 4)) % 4]
        else:
            xs = rr.randint(0, period - 1)
            for j in range(10):                              # tie-wrap
                t[y0 + j, xs, :3] = (176, 176, 184) if j < 5 else (120, 120, 128)
                t[y0 + j, (xs + 1) % period, :3] = (96, 96, 104)
            if k != 1 and rr.random() < 0.7:                 # gekleurde streep
                for x in range(period):
                    if (x // 3) % 2 == 0:
                        t[y0 + 4, x, :3] = (176, 152, 48)
    t[0, :, 3] = 0
    t[31, :, 3] = 0
    return t


def w_xurkitree():
    W, H = 40, 32
    w = World('Xurkitree', W, H, 1443)
    w.music, w.weather, w.speed, w.cspeed = 'MUS_RG_SILPH', 'WEATHER_NONE', 4, 8
    yy, xx, dith = w.yy, w.xx, w.dith
    LED = [(248, 240, 120), (104, 96, 48), (96, 88, 56), (88, 96, 48)]         # loopt rond: knipperende leds
    PWR = [(24, 72, 112), (48, 144, 208), (136, 224, 248), (40, 104, 168)]     # stroompuls door de hoofdkabel
    w.cycles = [LED, PWR]
    BLK = hexs('101018', '202430', '384050', '5c6878')
    RED = hexs('401010', '702020', 'a03830', 'd06850')
    BLU = hexs('101830', '203868', '3060a0', '5890d0')
    YEL = hexs('403010', '806020', 'b89030', 'e0c860')
    GRN = hexs('103018', '205830', '388848', '68b870')
    # ---- de leegte: diep onder je lopen nog meer kabels (donker, dunner), met verre lampjes
    vt = np.zeros((64, 64, 3))
    vt[...] = (6, 6, 14)
    for (y0, c) in ((6, (20, 22, 40)), (30, (24, 18, 30)), (50, (18, 26, 34))):
        vt[y0:y0 + 3] = c
        vt[y0] = (c[0] + 10, c[1] + 10, c[2] + 14)
    for (x0, c) in ((14, (22, 22, 36)), (44, (28, 20, 28))):
        vt[:, x0:x0 + 3] = c
        vt[:, x0] = (c[0] + 10, c[1] + 10, c[2] + 14)
    for (x, y, c) in ((5, 20, (64, 72, 120)), (40, 12, (96, 56, 72)), (27, 42, (56, 88, 96)), (58, 60, (88, 80, 48))):
        vt[y, x] = c
    w.tex(np.ones((H * 16, W * 16), bool), vt)
    # ---- banen van kabelbundels (beloopbaar), 2 cellen breed; horizontale banen liggen over de verticale
    walk = np.zeros((H, W), bool)
    lanes_v = [(6, 3, 27, [BLK, RED, BLK], None), (32, 3, 27, [BLU, BLK, YEL], None), (19, 8, 25, [BLK, None, BLK], PWR)]
    lanes_h = [(25, 2, 37, [RED, BLK, BLU], None), (12, 4, 35, [GRN, BLK, RED], None), (19, 6, 19, [YEL, BLK, GRN], None),
               (19, 33, 37, [BLK, GRN, BLK], None), (5, 8, 31, [BLU, RED, BLK], None)]
    shadow = np.zeros((H * 16, W * 16), bool)

    def draw_lane(x0, y0, x1, y1, cols, power, horiz):
        cols = [c if c is not None else BLK for c in cols]
        t = cable_strip(cols, 32, x0 * 7 + y0, power)
        if not horiz:
            t = t.transpose(1, 0, 2)
        px0, py0, px1, py1 = x0 * 16, y0 * 16, (x1 + 1) * 16, (y1 + 1) * 16
        reg = (slice(py0, py1), slice(px0, px1))
        ly, lx = yy[reg] - py0, xx[reg] - px0
        tt = t[ly % 32, xx[reg] % 32] if horiz else t[yy[reg] % 32, lx % 32]
        a = tt[..., 3] > 127
        # schaduw op de diepte eronder
        sh = np.zeros_like(a)
        sh[4:, 3:] = a[:-4, :-3]
        sub = w.bot[reg]
        sub[sh & ~a] = sub[sh & ~a] * 0.35
        sub[a] = tt[a][:, :3]
        # afgesneden einden: koperkernen
        for (ex, ey) in (((px0, py0), (px1 - 3, py0)) if horiz else ((px0, py0), (px0, py1 - 3))):
            pass
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                walk[y, x] = True
    for (x, y0, y1, cols, pw) in lanes_v:
        draw_lane(x, y0, x + 1, y1 + 1, cols, pw, False)
    for (y, x0, x1, cols, pw) in lanes_h:
        draw_lane(x0, y, x1 + 1, y + 1, cols, pw, True)
    # kabeleinden: doorgesneden, koperen kernen
    def cap(px, py, horiz):
        for k in range(3):
            cy_, cx_ = (py + 1 + k * 10 + 5, px) if horiz else (py, px + 1 + k * 10 + 5)
            for dy in range(-4, 5):
                for dx in range(-4, 5):
                    r_ = math.hypot(dx, dy)
                    if r_ <= 4.5:
                        c = (40, 40, 48) if r_ > 3.2 else ((232, 168, 88) if r_ < 1.6 else (184, 112, 48))
                        w.bot[cy_ + dy, cx_ + dx] = c
    for (y, x0, x1, cols, pw) in lanes_h:
        cap(x0 * 16 + 3, y * 16, True)
        cap((x1 + 2) * 16 - 4, y * 16, True)
    for (x, y0, y1, cols, pw) in lanes_v:
        cap(x * 16, y0 * 16 + 3, False)
        cap(x * 16, (y1 + 2) * 16 - 4, False)
    # ---- pleinen van geweven kabelmatten: aankomst en voor de transformator
    INS = [BLK, RED, BLU, GRN]
    mat = np.zeros((32, 32, 3))
    for row in range(8):
        c = INS[(row * 3) % 4]
        mat[row * 4] = c[3]; mat[row * 4 + 1] = c[2]; mat[row * 4 + 2] = c[1]; mat[row * 4 + 3] = c[0]
    for col in (4, 20):
        for y in range(32):
            over_ = (y // 4 + col // 4) % 2 == 0
            if over_:
                c = INS[(col // 4) % 4]
                mat[y, col:col + 4] = [c[0], c[2], c[3], c[1]]
    plazas = [(15, 26, 24, 29), (14, 7, 25, 10)]
    for (x0, y0, x1, y1) in plazas:
        pm = np.zeros((H, W), bool)
        pm[y0:y1 + 1, x0:x1 + 1] = True
        ps = w.soft(pm, 5) > 0.5
        sh = np.zeros_like(ps)
        sh[4:, 3:] = ps[:-4, :-3]
        w.bot[sh & ~ps] = w.bot[sh & ~ps] * 0.35
        w.tex(ps, mat)
        w.bot[ps & ~np.roll(ps, 1, 0)] = (120, 128, 144)
        w.bot[ps & ~np.roll(ps, -1, 0)] = (8, 8, 16)
        walk |= pm
    # ---- transformator met spoelen (Xurkitree staat ervoor)
    def transformer():
        img = img_new(96, 64)
        for y in range(10, 64):
            for x in range(4, 92):
                c = (72, 80, 96) if (x // 6) % 2 else (96, 104, 120)
                if y > 56:
                    c = (40, 44, 56)
                if y < 14:
                    c = (136, 144, 160)
                img[y, x] = (*c, 255)
        for bx in (18, 48, 78):
            for y in range(0, 34):
                for x in range(bx - 7, bx + 8):
                    if abs(x - bx) <= 7:
                        c = (176, 104, 48) if (y // 3) % 2 else (224, 160, 96)
                        if abs(x - bx) > 5:
                            c = (120, 64, 32)
                        if y < 3:
                            c = (200, 200, 208)
                        img[y, x] = (*c, 255)
        for y in range(34, 52):
            for x in range(36, 60):
                img[y, x] = (*((248, 208, 32) if (x + y) // 4 % 2 else (24, 24, 24)), 255)
        for (x, y) in ((48, 37), (47, 39), (49, 39), (46, 41), (48, 41), (50, 41), (47, 43), (48, 45), (48, 47)):
            img[y, x] = (248, 64, 32, 255)
        for i, x in enumerate((10, 26, 70, 86)):                # leds op de kast
            for y in (20, 21):
                img[y, x] = img[y, x + 1] = (*LED[i % 4], 255)
        return outline(img, (4, 4, 12))
    w.stamp(transformer(), 17, 3, solid_rows=3, over_rows=1)
    # ---- kabelbomen: stam van gedraaide kabels, kruin van uitwaaierende kabels met stekkers en lampjes
    def cable_tree(seed):
        rr = random.Random(seed)
        img = img_new(80, 96)
        for k in range(4):
            c = INS[k]
            for y in range(44, 96):
                x = 40 + 7 * math.sin(y / 6.0 + k * math.pi / 2)
                for dx in range(-3, 4):
                    put(img, int(x + dx), y, c[3] if dx < -1 else (c[2] if dx < 1 else (c[1] if dx < 3 else c[0])))
        ends = []
        for k in range(11):
            a = -math.pi / 2 + (k - 5) * 0.3 + rr.uniform(-0.08, 0.08)
            L = rr.randint(28, 42)
            c = INS[k % 4]
            x, y = 40.0, 46.0
            for t in range(L):
                x += math.cos(a)
                y += math.sin(a) + t * 0.04
                for dy in (-2, -1, 0, 1, 2):
                    put(img, int(x), int(y + dy), c[3] if dy < -1 else (c[2] if dy < 1 else (c[1] if dy < 2 else c[0])))
            ends.append((int(x), int(y)))
        for i, (x, y) in enumerate(ends):
            if i % 3 == 0:                                       # stekker
                for yy_ in range(y - 4, y + 4):
                    for xx_ in range(x - 4, x + 5):
                        put(img, xx_, yy_, (216, 216, 224) if xx_ < x else (152, 152, 168))
                for k2 in range(4, 7):
                    put(img, x - 2, y + k2, (232, 200, 96)); put(img, x + 2, y + k2, (232, 200, 96))
            else:                                                # lampje (ledcyclus)
                led = LED[(i * 3 + seed) % 4]
                for yy_ in range(y - 3, y + 4):
                    for xx_ in range(x - 3, x + 4):
                        if math.hypot(xx_ - x, yy_ - y) <= 3.2:
                            put(img, xx_, yy_, led)
                put(img, x - 1, y - 1, (255, 255, 255))
        return outline(img, (4, 4, 12))
    TREES = [cable_tree(1), cable_tree(2)]
    for i, (cx, cy) in enumerate(((1, 14), (34, 13), (9, 19), (25, 13), (35, 25), (1, 25), (24, 0), (10, 0))):
        if cy + 5 < H:
            w.stamp(TREES[i % 2], cx, cy, solid_rows=1, over_rows=5)
    # ---- stopcontacten en reuzenstekkers
    def socket():
        img = img_new(32, 48)
        for y in range(4, 46):
            for x in range(2, 30):
                img[y, x] = (*((232, 228, 216) if x < 22 else (184, 180, 168)), 255)
                if y > 38:
                    img[y, x] = (*((152, 148, 140) if x < 22 else (120, 116, 108)), 255)
        for (x0, y0) in ((10, 12), (19, 12)):
            for y in range(y0, y0 + 10):
                img[y, x0] = img[y, x0 + 1] = (24, 24, 32, 255)
        for y in range(27, 32):
            for x in range(14, 18):
                img[y, x] = (24, 24, 32, 255)
        return outline(img, (4, 4, 12))
    def plug():
        img = img_new(48, 32)
        for y in range(4, 28):
            for x in range(14, 46):
                img[y, x] = (*((224, 224, 232) if y < 12 else ((184, 184, 192) if y < 22 else (136, 136, 152))), 255)
        for y in (9, 10, 21, 22):
            for x in range(2, 14):
                img[y, x] = (*((232, 200, 96) if y in (9, 21) else (176, 136, 48)), 255)
        return outline(img, (4, 4, 12))
    for (cx, cy) in ((10, 25), (27, 24)):
        w.stamp(plug(), cx, cy, solid_rows=2)
    for (cx, cy) in ((29, 9), (3, 9)):
        w.stamp(socket(), cx, cy, solid_rows=1, over_rows=2)
    # ---- vonken (tegelanimatie uit de elektriciteitsaanval)
    el = load_anim_png('graphics/battle_anims/sprites/electricity.png', 32, 32)
    sparks = [el[f % 4] for f in range(8)]
    for f in (1, 3, 6):
        sparks[f] = img_new(32, 32)
    for (cx, cy) in ((6, 21), (32, 21), (12, 5)):
        anim_block(w, cx, cy, sparks)
    # ---- botsing
    w.solid[:] = ~walk
    for (x, y) in zip(*np.nonzero(walk.T)):
        pass
    for y in range(H):
        for x in range(W):
            if walk[y, x] and w.solid[y, x]:
                w.solid[y, x] = False
    # stempels die blokkeren (al gezet door stamp(): opnieuw toepassen na het walk-masker)
    for (cx, cy) in ((10, 25), (27, 24)):
        w.solid[cy + 1, cx:cx + 3] = True
    for (cx, cy) in ((29, 9), (3, 9)):
        w.solid[cy + 2, cx:cx + 2] = True
    for i, (cx, cy) in enumerate(((1, 14), (34, 13), (9, 19), (25, 13), (35, 25), (1, 25), (24, 0), (10, 0))):
        if cy + 5 < H:
            w.solid[cy + 5, cx + 2] = True
    w.solid[4:7, 17:23] = True
    for (cx, cy) in ((6, 21), (32, 21), (12, 5)):
        w.solid[cy + 1, cx] = w.solid[cy + 1, cx + 1] = True
    w.arrive, w.ret, w.ub = (20, 27), (20, 29), (20, 7)
    w.solid[7, 20] = False
    w.beh[~w.solid] = MB['MB_CAVE']          # wilde Pokemon overal op de kabels
    w.ub_elev = 3
    w.border = (0, 0)
    w.item_spots = [(37, 26)]
    w.decor = [('JOLTIK', 10, 12, 'MOVEMENT_TYPE_WANDER_AROUND', 'Spark', 3, 2),
               ('TYNAMO', 24, 26, 'MOVEMENT_TYPE_WANDER_AROUND', 'Spark', 3, 2),
               ('XURKITREE', 33, 6, 'MOVEMENT_TYPE_FACE_DOWN', 'Cable', 3, 0)]
    w.land, w.land_rate = [('GALVANTULA', 84, 86), ('MAGNEZONE', 84, 86), ('EELEKTROSS', 85, 87), ('BELLIBOLT', 84, 86),
                           ('KLINKLANG', 85, 87), ('HELIOLISK', 85, 87), ('TOGEDEMARU', 84, 86), ('EMOLGA', 84, 86),
                           ('PORYGON_Z', 86, 88), ('TOXTRICITY', 86, 88), ('ZEBSTRIKA', 87, 89), ('AMPHAROS', 87, 89)], 6
    w.bgs = [{'type': 'sign', 'x': 4, 'y': 11, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
              'script': 'UltraSpace_Xurkitree_EventScript_Socket'}]
    w.texts = [('UltraSpace_Xurkitree_Text_Socket', 'A wall socket the size of a door.\\pYou could plug in a whole town.\nSomeone already did. It was MAUVILLE.')]
    return w


def w_celesteela():
    W, H = 48, 36
    w = World('Celesteela', W, H, 1444)
    w.music, w.weather, w.speed = 'MUS_RG_SEVII_67', 'WEATHER_NONE', 8
    yy, xx, dith = w.yy, w.xx, w.dith
    GR = hexs('4c6428', '6c8434', '8ca444', 'b0c060', 'd4d88c')          # steppegras, droog groengoud
    MIST = hexs('8c9cb0', 'a8b8c8', 'c8d4e0', 'e4ecf0')
    DRY = hexs('6c5c28', '8c7834', 'b09c48', 'd0bc68', 'ecdc98')
    # ---- gras (periode 32): effen met losse halmen (geen vlekken: dat werd behang)
    def grass_tex(R, seed):
        # graspollen: lichte toppen, donkere voet (geen losse ruispixels)
        t = speckle_tex(R[2], [(['3..3.', '3.32.', '23212', '1211.'], [R[1], R[3], R[4]], 6),
                               (['.3', '32', '21'], [R[1], R[3], R[4]], 9),
                               (['3', '2'], [None, R[3], R[4]], 8),
                               (['11', '.1'], [R[1]], 7)], seed)
        return t
    g = grass_tex(GR, 72)
    w.tex(np.ones((H * 16, W * 16), bool), g)
    # droge, goudgele plekken (vervaagd celmasker: randen hangen alleen van de buren af)
    rr = random.Random(73)
    dry = np.zeros((H, W), bool)
    for _ in range(9):
        cx, cy = rr.randint(4, W - 5), rr.randint(9, H - 4)
        dry |= ellipse(W, H, cx, cy, rr.uniform(2, 4.5), rr.uniform(1.4, 2.6))
    ds = w.soft(dry, 12) + w.wob(16, 4, 74, 0.1)
    DRYM = [lerp(a, b, 0.45) for a, b in zip(DRY, GR)]
    w.tex(ds > 0.55, grass_tex(DRY, 72))
    rim = (ds > 0.42) & (ds <= 0.55)
    w.tex(rim, grass_tex(DRYM, 72))
    # ---- rand: het gras loopt uit in mist; bovenaan de horizon met de lucht
    ex = np.minimum(np.minimum(xx, W * 16 - 1 - xx), H * 16 - 1 - yy).astype(float)
    fog = np.clip((56 - ex) / 48.0, 0, 1)
    lv = np.floor(fog * 4 + dith * 0.999) / 4                 # 4 niveaus, geditherd ertussen
    on = lv > 0
    w.bot[on] = w.bot[on] * (1 - lv[on][:, None]) + np.array(MIST[2]) * lv[on][:, None]
    hz = 6 * 16
    t = np.clip((hz + 64 - yy) / 64.0, 0, 1)
    lv = np.floor(t * 4 + dith * 0.999) / 4 * 0.8
    far = lv > 0
    w.bot[far] = w.bot[far] * (1 - lv[far][:, None]) + np.array(MIST[1]) * lv[far][:, None]
    sky = yy < hz
    st = yy[sky] / hz
    w.bot[sky] = np.array(MIST, float)[np.clip(np.floor((1 - st) * 3 + dith[sky] * 0.999).astype(int) + 1, 0, 3)]
    w.bot[(yy >= hz - 1) & (yy < hz + 1)] = (160, 172, 176)
    # ---- Celesteela in de verte (silhouetten op de horizon, tegels)
    cs = load_mon('celesteela')
    a = cs[..., 3] > 127
    ys, xs = np.nonzero(a)
    cs = cs[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    small = np.array(Image.fromarray(np.clip(cs, 0, 255).astype(np.uint8), 'RGBA').resize(
        (max(8, cs.shape[1] // 2), max(8, cs.shape[0] // 2)), Image.NEAREST)).astype(float)
    tiny = np.array(Image.fromarray(np.clip(cs, 0, 255).astype(np.uint8), 'RGBA').resize(
        (max(6, cs.shape[1] // 3), max(6, cs.shape[0] // 3)), Image.NEAREST)).astype(float)
    for (img, col, xs_, base) in ((tiny, (176, 184, 200), (3, 11, 19, 33, 41), hz + 2), (small, (136, 144, 164), (7, 15, 37, 43), hz + 12)):
        sil = img.copy()
        m = sil[..., 3] > 127
        sil[m, :3] = col
        for cx in xs_:
            w.over(sil, cx * 16, base - sil.shape[0])
    # ---- echte stenen Celesteela-beelden in het gras (tegels, 64x64), schaduw naar rechts
    statue = shaded_sprite(load_mon('celesteela'), hexs('383c48', '5c6070', '8c90a0', 'c0c4cc', 'e8eaee'))
    statue = outline(statue, (24, 24, 32))
    for (cx, cy) in ((6, 12), (38, 18), (10, 25)):
        sx, sy = cx * 16 + 52, cy * 16 + 60
        shadow = (((xx - sx) / 30.0) ** 2 + ((yy - sy) / 6.0) ** 2 <= 1) & (dith < 0.75)
        w.bot[shadow] *= 0.62
        w.stamp(statue, cx, cy, solid_rows=1, over_rows=3)
    # ---- schroeikringen van lanceringen, met een verbrande streep naar het noorden
    def scorch(cx, cy, r):
        d = np.hypot(xx - cx, (yy - cy) * 1.3)
        ring = (d < r) & (np.abs(d - r * 0.7) < r * 0.3) & ((xx * 3 + yy * 5) % 4 != 0)
        w.bot[ring] = w.bot[ring] * 0.45 + np.array([40, 32, 24]) * 0.55
        core = d < r * 0.4
        w.bot[core & (dith < 0.6)] = (56, 48, 40)
        w.bot[core & (dith >= 0.6)] = (88, 76, 60)
        streak = (np.abs(xx - cx) < 9 - (cy - yy) / 30.0) & (yy < cy - r * 0.6) & (yy > hz + 8)
        fade = np.clip((yy - (hz + 8)) / float(max(1, cy - hz)), 0, 1)
        st = streak & (fade * 0.8 > dith) & ((xx + yy // 2) % 3 != 0)
        w.bot[st] = w.bot[st] * 0.55 + np.array([200, 196, 150]) * 0.45   # platgedrukt, verbleekt gras
    scorch(16 * 16 + 8, 20 * 16 + 8, 28)
    scorch(33 * 16 + 8, 27 * 16 + 8, 22)
    # lanceerplaats van Celesteela: betonnen ring
    lx, ly = 24 * 16 + 8, 9 * 16 + 8
    d = np.hypot(xx - lx, (yy - ly) * 1.25)
    pad = d < 36
    w.bot[pad] = (176, 172, 160)
    w.bot[pad & (((xx - lx) % 12 == 0) | ((yy - ly) % 12 == 0))] = (136, 132, 124)
    w.bot[pad & (((xx - lx) % 12 == 1) | ((yy - ly) % 12 == 1))] = (200, 196, 184)
    w.bot[pad & (np.abs(d - 30) < 1.2)] = (232, 192, 64)
    w.bot[pad & (d < 14)] = (64, 56, 48)
    w.bot[(d >= 36) & (d < 38.5)] = (96, 92, 84)
    # ---- losse keien en droge plukken
    def boulder():
        img = img_new(32, 32)
        for y in range(32):
            for x in range(32):
                dd = math.hypot((x - 15.5) / 13, (y - 18) / 11)
                if dd <= 1 and y > 8:
                    sh_ = (x - 15.5) / 13 * 0.6 + (y - 18) / 11 * 0.6
                    c = (184, 176, 160) if sh_ < -0.3 else ((144, 136, 124) if sh_ < 0.3 else (104, 96, 88))
                    img[y, x] = (*c, 255)
        return outline(img, (48, 44, 40))
    BO = boulder()
    for (cx, cy) in ((28, 14), (42, 26), (4, 20), (20, 28)):
        w.stamp(BO, cx, cy, solid_rows=1)
    # ---- botsing: mist aan de randen en de verte
    for y in range(H):
        for x in range(W):
            if y < 8 or x < 2 or x >= W - 2 or y >= H - 2:
                w.solid[y, x] = True
    w.arrive, w.ret, w.ub = (24, 30), (24, 32), (24, 9)
    w.solid[32, 24] = False
    w.solid[9, 24] = False
    w.solid[8, 24] = True
    w.ub_elev = 3
    w.border = (0, H - 2)
    rocket = [(12, 15), (14, 11), (31, 12), (36, 10), (41, 14), (12, 21), (28, 22), (37, 28), (6, 29), (19, 16), (30, 17)]
    w.decor = [('CELESTEELA', x, y, 'MOVEMENT_TYPE_RUN_IN_PLACE_UP' if i % 3 == 0 else 'MOVEMENT_TYPE_FACE_DOWN', 'Rocket', 3, 0)
               for i, (x, y) in enumerate(rocket)]
    w.drop_kinds = ['Smoke']
    w.texts = [('UltraSpace_Celesteela_Text_Statue', 'A stone CELESTEELA.\\pThe plaque says: “FIRST TO LAUNCH.”\nIt has not launched.')]
    w.bgs = [{'type': 'sign', 'x': 8, 'y': 15, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
              'script': 'UltraSpace_Celesteela_EventScript_Statue'}]
    return w


def w_kartana():
    W, H = 36, 30
    w = World('Kartana', W, H, 1445)
    w.music, w.weather, w.speed = 'MUS_RG_POKE_MANSION', 'WEATHER_NONE', 6
    yy, xx, dith = w.yy, w.xx, w.dith
    WOOD = hexs('3c2014', '5c3420', '804c2c', 'a8703c', 'c89858')
    PAPER = hexs('a08c70', 'c8b494', 'e4d4b4', 'fcf4e0')
    BOOKS = [hexs('581820', '902830', 'c04848'), hexs('182850', '284890', '4870c0'), hexs('183c20', '286838', '48945c'),
             hexs('402050', '683488', '9058b8'), hexs('5c4010', '987020', 'c8a040'), hexs('302c28', '58504c', '807870')]
    # ---- 'vloer' = het plafond: stucwerk met cassettes en rozetten (periode 32)
    P = 32
    ty, tx, td = grid(P)
    c = np.zeros((P, P, 3))
    c[...] = PAPER[2]
    inner = (tx >= 3) & (tx <= 28) & (ty >= 3) & (ty <= 28)
    c[inner] = PAPER[1]
    c[(tx >= 6) & (tx <= 25) & (ty >= 6) & (ty <= 25)] = PAPER[2]
    c[((tx == 3) | (ty == 3)) & inner] = PAPER[0]
    c[((tx == 28) | (ty == 28)) & inner] = PAPER[3]
    c[((tx == 6) | (ty == 6)) & (tx >= 6) & (tx <= 25) & (ty >= 6) & (ty <= 25)] = PAPER[3]
    c[((tx == 25) | (ty == 25)) & (tx >= 6) & (tx <= 25) & (ty >= 6) & (ty <= 25)] = PAPER[0]
    d = np.hypot(tx - 15.5, ty - 15.5)
    c[(d < 4.5)] = PAPER[1]
    c[(np.abs(d - 3) < 0.8)] = PAPER[3]
    c[d < 1.5] = (200, 168, 96)
    w.tex(np.ones((H * 16, W * 16), bool), c)
    # ---- wanden: boven ingebouwde kasten (op hun kop), onder ramen (op hun kop), zijkanten lambrisering
    def bookcase(seed, h=32, flip=True):
        rr = random.Random(seed)
        img = np.zeros((h, 16, 4))
        img[..., :3] = WOOD[1]
        img[..., 3] = 255
        img[:, 0] = (*WOOD[0], 255); img[:, 15] = (*WOOD[0], 255)
        img[0:3] = (*WOOD[3], 255); img[1] = (*WOOD[4], 255)
        shelf_rows = [(3, 13), (15, 28)] if h == 32 else [(3, 13)]
        for (a, b) in shelf_rows:
            x = 1
            while x < 15:
                bw = rr.choice((2, 2, 3))
                col = rr.choice(BOOKS)
                top = a + rr.choice((0, 1, 2, 3))
                for i in range(bw):
                    if x + i < 15:
                        img[top:b, x + i, :3] = col[1] if i < bw - 1 else col[0]
                        img[top, x + i, :3] = col[2]
                        if (b - top) > 6:
                            img[top + (b - top) // 2, x + i, :3] = (232, 200, 96)
                x += bw
            img[b:b + 2, 1:15, :3] = WOOD[3]
            img[b + 1, 1:15, :3] = WOOD[2]
        return img[::-1] if flip else img
    CASES = [bookcase(s) for s in range(5)]
    top_wall = np.zeros((H, W), bool)
    top_wall[0:3] = True
    for x in range(W):
        cs = CASES[(x * 7) % 5]
        w.bot[0:32, x * 16:x * 16 + 16] = cs[..., :3]
        w.bot[32:48, x * 16:x * 16 + 16] = WOOD[2]
        w.bot[32:36, x * 16:x * 16 + 16] = WOOD[4]                    # sierlijst (onder: dit is de bovenkant)
        w.bot[34, x * 16:x * 16 + 16] = WOOD[3]
        w.bot[44:48, x * 16:x * 16 + 16] = WOOD[0]
        w.bot[38:42, x * 16 + 2:x * 16 + 14] = WOOD[1]
    # onder: muur met ramen op hun kop (het gras zit boven, de lucht onder)
    by0 = (H - 3) * 16
    w.bot[by0:, :] = (152, 120, 96)
    w.bot[by0:by0 + 4] = WOOD[0]
    w.bot[by0 + 4:by0 + 8] = WOOD[3]
    w.bot[by0 + 6] = WOOD[4]
    for x in range(W):
        if (x % 2) == 0:
            w.bot[by0 + 8:, x * 16 + 7] = (136, 104, 84)
    for wx in (4, 11, 23, 30):
        x0, y0 = wx * 16, by0 + 10
        for y in range(y0, y0 + 30):
            for x in range(x0, x0 + 32):
                f = (y - y0) / 30.0
                if f < 0.3:
                    col = (88, 152, 72) if (x + y) % 5 else (64, 120, 56)          # gras (boven!)
                elif f < 0.38:
                    col = (120, 168, 96)
                else:
                    col = lerp((168, 208, 240), (104, 160, 224), (f - 0.38) / 0.62)
                    if 0.55 < f < 0.65 and (x - x0) % 13 < 6:
                        col = (240, 248, 248)                                       # wolkje
                w.bot[y, x] = col
        w.bot[y0:y0 + 30, x0] = WOOD[0]; w.bot[y0:y0 + 30, x0 + 31] = WOOD[0]
        w.bot[y0:y0 + 30, x0 + 15:x0 + 17] = WOOD[2]
        w.bot[y0, x0:x0 + 32] = WOOD[0]; w.bot[y0 + 29, x0:x0 + 32] = WOOD[3]
        w.bot[y0 + 14:y0 + 16, x0:x0 + 32] = WOOD[2]
    # zijwanden
    for x0 in (0, (W - 2) * 16):
        reg = (slice(48, by0), slice(x0, x0 + 32))
        w.bot[reg] = WOOD[1]
        w.bot[48:by0, x0 + (0 if x0 else 31)] = WOOD[0]
        w.bot[48:by0, x0 + (31 if x0 == 0 else 0)] = WOOD[3]
        for y in range(48, by0, 16):
            w.bot[y:y + 2, x0:x0 + 32] = WOOD[2]
    w.solid[0:3] = True
    w.solid[H - 3:] = True
    w.solid[:, :2] = True
    w.solid[:, -2:] = True
    # ---- vrijstaande boekenkasten op hun kop (2 hoog), in gangen
    rows = [(10, 3, 12), (10, 23, 32), (15, 3, 10), (15, 25, 32), (20, 3, 12), (20, 23, 32)]
    for (y, x0, x1) in rows:
        for x in range(x0, x1 + 1):
            cs = CASES[(x * 3 + y) % 5]
            reg = w.bot[y * 16:(y + 2) * 16, x * 16:x * 16 + 16]
            reg[...] = cs[..., :3]
            w.solid[y, x] = w.solid[y + 1, x] = True
        # schaduw (valt naar boven: alles is omgekeerd)
        w.bot[y * 16 - 3:y * 16, x0 * 16:(x1 + 1) * 16] *= 0.75
    # ---- trappen op hun kop (leiden nergens heen)
    def stairs():
        img = img_new(48, 64)
        for k in range(8):
            y = k * 8
            for x in range(4, 44):
                for j in range(8):
                    col = WOOD[3] if j < 2 else (WOOD[2] if j < 6 else WOOD[1])
                    img[y + j, x] = (*col, 255)
        for y in range(64):
            for x in (2, 3, 44, 45):
                img[y, x] = (*WOOD[0 if x in (2, 45) else 4], 255)
            if y % 8 == 0:
                for x in (1, 46):
                    img[y, x] = (*WOOD[4], 255)
        img = outline(img, (24, 12, 8))
        return img[::-1]
    w.stamp(stairs(), 3, 3, solid_rows=4)
    w.stamp(stairs()[:, ::-1], 30, 3, solid_rows=4)
    # ---- kroonluchters die omhoog staan, met kaarsen die naar beneden branden (vlammetje flakkert)
    def chandelier(fr):
        img = img_new(48, 32)
        for x in range(8, 40):
            for y in (21, 22):
                img[y, x] = (*((216, 176, 72) if y == 21 else (152, 112, 40)), 255)
        for y in range(0, 22):
            img[y, 23] = img[y, 24] = (*((216, 176, 72) if y % 4 else (248, 224, 120)), 255)
        for cx_ in (10, 18, 30, 38):
            for y in range(14, 21):
                img[y, cx_] = img[y, cx_ + 1] = (240, 236, 220, 255)
            # vlam onder de kaars (hij brandt naar beneden)
            h = 4 if fr == 0 else 5
            for j in range(h):
                ww = 1 if j < h - 2 else 0
                for i in range(-ww, ww + 2):
                    img[23 + j, cx_ + i] = (*((248, 224, 96) if j < 2 else (248, 136, 24)), 255)
        return outline(img, (40, 24, 16))
    CH = [chandelier(f % 2) for f in range(8)]
    for (cx, cy) in ((16, 13), (8, 24), (26, 24)):
        base = w.bot[cy * 16:cy * 16 + 32, cx * 16:cx * 16 + 48].copy()
        frames = []
        for f in range(8):
            b = base.copy()
            m = CH[(f // 2) % 2][..., 3] > 127
            b[m] = CH[(f // 2) % 2][m, :3]
            frames.append(np.concatenate([b, np.full(b.shape[:2] + (1,), 255.0)], 2))
        anim_block(w, cx, cy, frames, nx=3, ny=2)
        w.solid[cy + 1, cx:cx + 3] = True
    # ---- bureaus op hun kop (poten omhoog), met inkt die omhoog druppelt
    def desk():
        img = img_new(48, 32)
        for y in range(14, 24):
            for x in range(2, 46):
                img[y, x] = (*(WOOD[3] if y < 16 else (WOOD[2] if y < 22 else WOOD[1])), 255)
        for lx in (5, 41):
            for y in range(0, 14):
                img[y, lx] = img[y, lx + 1] = (*WOOD[2], 255)
                img[y, lx + 2] = (*WOOD[1], 255)
        for y in range(24, 30):                                 # het inktpotje hangt onder het blad
            for x in range(20, 26):
                img[y, x] = (40, 40, 64, 255)
        for (x, y) in ((22, 11), (23, 9), (22, 6), (23, 3)):     # inkt druppelt omhoog
            img[y, x] = img[y + 1, x] = (24, 24, 48, 255)
        return outline(img, (24, 12, 8))
    w.stamp(desk(), 13, 20, solid_rows=1)
    w.stamp(desk(), 20, 15, solid_rows=1)
    # ---- het grote open boek waarop Kartana staat
    def open_book():
        img = img_new(96, 64)
        for y in range(4, 60):
            for x in range(4, 92):
                page = (PAPER[3] if x < 46 else PAPER[2])
                if abs(x - 47.5) < 2:
                    page = PAPER[0]
                if (y - 4) % 6 == 3 and 10 <= x <= 40 or (y - 4) % 6 == 3 and 54 <= x <= 86:
                    if (x * 7 + y) % 11 > 2:
                        page = (88, 80, 72)
                img[y, x] = (*page, 255)
        for y in range(58, 63):
            for x in range(2, 94):
                img[y, x] = (*((128, 32, 40) if y < 61 else (88, 16, 24)), 255)
        return outline(img, (56, 40, 32))
    w.stamp(open_book(), 15, 5, solid_rows=0)
    # ---- sneden van Kartana: lange rechte sneden door het plafond; erdoor zie je de lucht (onder je!)
    def slash(x0, y0, x1, y1, wd=2.2):
        L = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        t = (xx - x0) * ux + (yy - y0) * uy
        dist = np.abs(-(xx - x0) * uy + (yy - y0) * ux)
        taper = np.clip(np.minimum(t, L - t) / 40.0, 0, 1)
        core = (t > 0) & (t < L) & (dist < wd * taper)
        lip = (t > 0) & (t < L) & (dist < wd * taper + 1.6) & ~core
        sky = lerp((168, 208, 240), (232, 240, 248), 0.3)
        w.bot[core] = sky
        w.bot[core & ((xx + yy) % 9 < 3)] = (240, 248, 255)
        side = (-(xx - x0) * uy + (yy - y0) * ux) > 0
        w.bot[lip & side] = (96, 72, 56)
        w.bot[lip & ~side] = PAPER[3]
    slash(5 * 16, 22 * 16, 15 * 16, 13 * 16 + 8)
    slash(24 * 16, 26 * 16 + 4, 33 * 16, 19 * 16)
    slash(22 * 16 + 8, 4 * 16, 29 * 16, 9 * 16 + 8, 2.6)
    # ---- potplanten op hun kop: de pot staat, de plant groeit naar beneden
    def plant():
        img = img_new(16, 32)
        for y in range(0, 10):
            for x in range(3, 13):
                if abs(x - 7.5) < 5 - y * 0.15:
                    img[y, x] = (*((200, 104, 64) if x < 8 else (160, 72, 48)), 255)
        for y in range(0, 2):
            for x in range(2, 14):
                img[y, x] = (216, 136, 88, 255)
        rr2 = random.Random(5)
        for k in range(6):
            x, y = 4 + k * 1.6, 10
            a = math.pi / 2 + (k - 2.5) * 0.25
            for t in range(16 + rr2.randint(-3, 3)):
                x += math.cos(a) * 0.8
                y += math.sin(a)
                put(img, int(x), int(y), (64, 136, 64) if t % 5 else (112, 184, 96))
                if t % 5 == 2:
                    put(img, int(x) + 1, int(y), (112, 184, 96))
        return outline(img, (32, 32, 24))
    PL = plant()
    for (cx, cy) in ((2, 8), (33, 8), (2, 22), (33, 22), (13, 25), (23, 25)):
        w.stamp(PL, cx, cy, solid_rows=2)
    # ---- stapels papier (blokkeren) en schilderijen op hun kop aan de onderste muur
    def stack(seed):
        img = img_new(16, 16)
        rr2 = random.Random(seed)
        y = 14
        while y > 3:
            off = rr2.randint(-1, 1)
            for x in range(2 + off, 14 + off):
                img[y, x] = (*PAPER[3 if y % 2 else 1], 255)
            y -= 1
        return outline(img, (88, 72, 56))
    for (cx, cy) in ((13, 9), (24, 9), (12, 17), (24, 22), (4, 13), (31, 13)):
        if not w.solid[cy, cx]:
            w.stamp(stack(cx), cx, cy, solid_rows=1)
    port = shaded_sprite(load_mon('kartana'), hexs('282018', '584830', '988458', 'd8c890', 'fcf4d8'))[::-1]
    by0 = (H - 3) * 16
    for x0 in (17 * 16 + 4,):
        w.bot[by0 + 8:by0 + 46, x0 - 4:x0 + 36] = WOOD[0]
        w.bot[by0 + 10:by0 + 44, x0 - 2:x0 + 34] = (216, 176, 72)
        w.bot[by0 + 12:by0 + 42, x0:x0 + 32] = (64, 48, 40)
        pim = np.array(Image.fromarray(np.clip(port, 0, 255).astype(np.uint8), 'RGBA').resize((30, 30), Image.NEAREST)).astype(float)
        w.over(pim, x0 + 1, by0 + 12)
    # ---- losse bladzijden op de vloer en vallende bladzijden (tegelanimatie)
    def page_img(rot):
        img = img_new(10, 10)
        for y in range(10):
            for x in range(10):
                u, v = (x - 4.5), (y - 4.5)
                a, b = (u * math.cos(rot) + v * math.sin(rot)), (-u * math.sin(rot) + v * math.cos(rot))
                if abs(a) < 4 and abs(b) < 3:
                    img[y, x] = (*(PAPER[3] if a < 2 else PAPER[1]), 255)
                    if abs(b) < 0.6 and abs(a) < 3:
                        img[y, x] = (120, 112, 104, 255)
        return outline(img, (88, 72, 56))
    rr = random.Random(81)
    litter = [(rr.randint(3, 32), rr.randint(4, 25), rr.uniform(0, 3)) for _ in range(22)]
    for (cx, cy, rot) in litter:
        if not w.solid[cy, cx]:
            w.over(page_img(rot), cx * 16 + (cy * 5) % 6, cy * 16 + (cx * 3) % 6)
    falling = []
    for f in range(8):
        col = np.zeros((32, 16, 4))
        for k, (ox, ph, rot) in enumerate(((2, 0, 0.3), (5, 16, 1.6))):
            y = (ph + f * 4) % 32
            pg = page_img(rot + f * 0.4 * (1 if k else -1))
            for j in range(10):
                for i in range(10):
                    if pg[j, i, 3] > 127:
                        col[(y + j) % 32, min(15, ox + i)] = pg[j, i]
        falling.append(col)
    for x in (14, 22, 6, 29):
        for y in range(5 if x in (6, 29) else 12, 19 if x in (6, 29) else 20):
            if w.solid[y, x] or (x, y) in w.anim:
                continue
            base = w.bot[y * 16:y * 16 + 16, x * 16:x * 16 + 16].copy()
            frs = []
            for f in range(8):
                b = base.copy()
                pc = falling[f][(y % 2) * 16:(y % 2) * 16 + 16]
                m = pc[..., 3] > 127
                b[m] = pc[m, :3]
                frs.append(b)
            w.anim[(x, y)] = frs
            w.bot[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = frs[0]
    w.beh[~w.solid] = MB['MB_CAVE']
    w.arrive, w.ret, w.ub = (18, 24), (18, 26), (18, 7)
    w.ub_elev = 3
    w.border = (0, H - 2)
    w.decor = [('KARTANA', 7, 7, 'MOVEMENT_TYPE_FACE_RIGHT', 'Fold', 3, 0), ('KARTANA', 28, 18, 'MOVEMENT_TYPE_FACE_LEFT', 'Fold', 3, 0),
               ('UNOWN', 11, 13, 'MOVEMENT_TYPE_WANDER_AROUND', 'Reader', 3, 2)]
    w.land, w.land_rate = [('CHANDELURE', 84, 86), ('AEGISLASH', 85, 87), ('KLEFKI', 84, 86), ('REUNICLUS', 84, 86),
                           ('SMEARGLE', 84, 86), ('UNOWN', 84, 86), ('GOTHITELLE', 85, 87), ('HATTERENE', 85, 87),
                           ('KINGAMBIT', 86, 88), ('MIMIKYU', 85, 87), ('SINISTCHA', 87, 89), ('ALAKAZAM', 87, 89)], 5
    w.bgs = [{'type': 'sign', 'x': 8, 'y': 11, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
              'script': 'UltraSpace_Kartana_EventScript_Books'}]
    w.texts = [('UltraSpace_Kartana_Text_Books', 'The books are upside down.\\pYou tilt your head. The words are\nstill upside down. So is your head.\\p'
                'One title reads: “HOW TO FOLD A\nBLADE IN 900 EASY STEPS.”'),
               ('UltraSpace_Kartana_Text_Reader', 'It is reading the shelf backwards.\nIt says the ending is better first.')]
    return w


def post_nihilego(w, g):
    """nep-eilanden: in de buurt (manhattan <= 2) lossen ze op (setmetatile naar open water)"""
    name = 'UltraSpace_Nihilego'
    for i, cells in enumerate(w.fake_cells):
        var = 'VAR_TEMP_%d' % (i + 1)
        lab = '%s_EventScript_Mirage%d' % (name, i)
        cs = set(cells)
        trig = set()
        for (x, y) in cs:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    c = (x + dx, y + dy)
                    if abs(dx) + abs(dy) <= 2 and c not in cs and 0 <= c[0] < w.W and 0 <= c[1] < w.H \
                            and w.water[c[1], c[0]] and not w.solid[c[1], c[0]]:
                        trig.add(c)
        for (x, y) in sorted(trig):
            w.coords.append({'type': 'trigger', 'x': x, 'y': y, 'elevation': 0, 'var': var, 'var_value': '0',
                             'script': lab})
        body = [lab + '::', '\tlockall', '\tplayse SE_M_HAZE']
        ring = {(x + dx, y + dy) for (x, y) in cs for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
        ring = {c for c in ring - cs if 0 <= c[0] < w.W and 0 <= c[1] < w.H and w.water[c[1], c[0]]
                and c not in w.anim and not w.solid[c[1], c[0]]}
        for (x, y) in sorted(cs | ring):
            rx, ry = w.plain_water[(x % 4, y % 4)]
            body.append('\tsetmetatile %d, %d, %d, FALSE' % (x, y, g[ry, rx]))
        body += ['\tspecial DrawWholeMapView', '\twaitse', '\tsetvar %s, 1' % var, '\treleaseall', '\tend', '']
        w.scripts += body


WORLDS = {'Nihilego': w_nihilego, 'Buzzwole': w_buzzwole, 'Pheromosa': w_pheromosa, 'Xurkitree': w_xurkitree, 'Celesteela': w_celesteela, 'Kartana': w_kartana}
POST = {'Nihilego': post_nihilego}
WORM = 'OBJ_EVENT_GFX_ULTRA_WORMHOLE'
FLAGGED_KINDS = ('Echo', 'Cable', 'Fold', 'Wall')
UB_SPECIES = {'Nihilego': 'NIHILEGO', 'Buzzwole': 'BUZZWOLE', 'Pheromosa': 'PHEROMOSA', 'Xurkitree': 'XURKITREE',
              'Celesteela': 'CELESTEELA', 'Kartana': 'KARTANA'}


def finalize(w, g):
    name = 'UltraSpace_' + w.key
    sp = UB_SPECIES[w.key]
    flag = 'FLAG_ULTRA_' + sp
    w.objects = [obj('LOCALID_ULTRA_%s_RETURN' % w.key.upper(), WORM, w.ret[0], w.ret[1], 'UltraSpace_EventScript_ReturnToHub'),
                 obj('LOCALID_ULTRA_%s_UB' % w.key.upper(), 'OBJ_EVENT_GFX_SPECIES(%s)' % sp, w.ub[0], w.ub[1],
                     name + '_EventScript_UB', flag, elev=w.ub_elev)]
    blocked = {w.ret, w.ub}
    kinds = []
    for d in w.decor:
        spc, x, y, move, kind, elev, rng = d
        gfx = spc if spc.startswith('OBJ_EVENT_GFX') else 'OBJ_EVENT_GFX_SPECIES(%s)' % spc
        w.objects.append(obj(None, gfx, x, y, '%s_EventScript_%s' % (name, kind), flag if kind in FLAGGED_KINDS else '0',
                             move, elev=elev, rx=rng, ry=rng))
        assert not w.solid[y, x], (name, 'decor op een muur', d)
        if not rng:
            blocked.add((x, y))
        if kind not in kinds:
            kinds.append(kind)
    items = ni.items(name)
    spots = list(getattr(w, 'item_spots', []))
    assert len(spots) >= len(items), (name, 'te weinig itemplekken')
    for (fl, it, q, hid), (x, y) in zip(items, spots):
        assert not w.solid[y, x]
        if hid:
            w.bgs.append({'type': 'hidden_item', 'x': x, 'y': y, 'elevation': 3, 'item': it, 'flag': fl})
        else:
            w.objects.append(obj(None, 'OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', fl,
                                 'MOVEMENT_TYPE_LOOK_AROUND', rx=q, sight=it))
            blocked.add((x, y))
    r = reach(w, w.arrive, blocked)
    assert next_to(r, w.ub), (name, 'UB onbereikbaar')
    assert next_to(r, w.ret), (name, 'wormgat onbereikbaar')
    for (x, y) in spots[:len(items)]:
        assert (x, y) in r or next_to(r, (x, y)), (name, 'item onbereikbaar', (x, y))
    for b in w.bgs:
        if b['type'] == 'sign':
            assert next_to(r, (b['x'], b['y'])) or (b['x'], b['y']) in r, (name, 'bord onbereikbaar', b)
    for d in w.decor:
        if not d[6]:
            assert next_to(r, (d[1], d[2])), (name, 'decor onbereikbaar', d)
    w.reach = r
    # scripts voor decor-soorten en borden die nog niet (buiten het gegenereerde blok) bestaan
    p = 'data/maps/%s/scripts.inc' % name
    blk = open(p).read().split('@ ultra_worlds_a {')[0]
    for kind in kinds:
        if '%s_EventScript_%s::' % (name, kind) not in blk:
            w.scripts += ['%s_EventScript_%s::' % (name, kind), '\tmsgbox %s_Text_%s, MSGBOX_NPC' % (name, kind), '\tend', '']
    for b in w.bgs:
        if b['type'] == 'sign' and '%s::' % b['script'] not in blk:
            lab = b['script'].replace('_EventScript_', '_Text_')
            w.scripts += ['%s::' % b['script'], '\tmsgbox %s, MSGBOX_SIGN' % lab, '\tend', '']
    if w.key in POST:
        POST[w.key](w, g)


def main():
    only = [a for a in sys.argv[1:] if not a.startswith('-')]
    built = []
    for k in WORLDS:
        if only and k not in only:
            continue
        w = WORLDS[k]()
        g = build_tilesets(w)
        finalize(w, g)
        lc = save_layout(w, g)
        write_map(w, lc)
        write_wild(w)
        write_scripts(w)
        update_hub(w, w.arrive)
        preview(w, os.path.join(SCRATCH, 'canvas_%s.png' % k))
        built.append(w)
        print('%s: aankomst %s, UB %s, wormgat %s, %d objecten, tiles %s' % (k, w.arrive, w.ub, w.ret, len(w.objects), w.ntiles))
    if not only:
        register_tilesets(built)
    else:
        print('alleen %s gebouwd: tileset-registratie overgeslagen' % only)


def preview(w, path):
    im = Image.fromarray(np.clip(w.bot, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    im.alpha_composite(Image.fromarray(np.clip(w.ovr, 0, 255).astype(np.uint8), 'RGBA'))
    im.save(path)


if __name__ == '__main__' and not PREVIEW:
    main()

if __name__ == '__main__' and PREVIEW:
    for k in (WORLDS if PREVIEW == 'all' else [PREVIEW]):
        w = WORLDS[k]()
        preview(w, os.path.join(SCRATCH, 'canvas_%s.png' % k))
        if '--count' in sys.argv:
            cl = w.cell_list()
            print(k, 'unieke 8x8-blokken (ruw):', len({canon(q) for c in cl if c[5] is None for q in quads(c[2])}
                                                     | {canon(q) for c in cl if c[3] is not None for q in quads(c[3])}))
