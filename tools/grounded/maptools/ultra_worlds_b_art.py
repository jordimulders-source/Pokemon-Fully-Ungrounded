"""Project Grounded: teken- en knipgereedschap voor tools/grounded/maptools/ultra_worlds_b.py (Ultra Space, vijf werelden).

Werkwijze (zoals ruin_beasts.py, maar groter): elke wereld wordt als één canvas van de hele kaart getekend
(onderlaag RGB + bovenlaag RGBA, per vak botsing/gedrag/laagtype), daarna in metatiles geknipt. emit_pair() maakt
er een eigen primary + secondary van (2 x 512 tiles, 13 paletten): paletten met k-means, tiles ontdubbeld (ook
gespiegeld) en, als het te veel wordt, verliesgevend samengevoegd (de minst opvallende tiles eerst).
Geanimeerde vakken (Anim) krijgen vaste tileplekken vooraan in de secondary; de frames schrijft emit_pair als
anim/<naam>/<n>.png (128 breed, 8 hoog per 16 tiles) voor src/tileset_anims.c.
"""
import math, os, random, struct, zlib  # noqa: E401
import numpy as np
from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
COVERED, SPLIT, NORMAL = 1, 2, 0
B4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16


# ====================================================================== bestaande tilesets lezen
def read_pal(path):
    if not os.path.exists(path):
        return [(0, 0, 0)] * 16
    return [tuple(map(int, l.split())) for l in open(path).read().split('\n')[3:19]]


class VTileset:
    """vanilla tileset-paar (primary + secondary) als pixels: metatile(id) -> (onder RGBA, boven RGBA, attr)"""
    def __init__(self, prim, sec):
        self.ts = []
        for kind, d in (('primary', prim), ('secondary', sec)):
            p = os.path.join(REPO, 'data/tilesets', kind, d)
            im = np.array(Image.open(p + '/tiles.png'))
            n = (im.shape[0] // 8) * (im.shape[1] // 8)
            tiles = [im[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] for i in range(n)]
            mts = open(p + '/metatiles.bin', 'rb').read()
            attrs = open(p + '/metatile_attributes.bin', 'rb').read()
            pals = [read_pal('%s/palettes/%02d.pal' % (p, i)) for i in range(16)]
            self.ts.append((tiles, mts, attrs, pals))
        self.pal = self.ts[0][3][:6] + self.ts[1][3][6:13] + [[(0, 0, 0)] * 16] * 3

    def tile(self, t):
        idx, hf, vf, pn = t & 0x3ff, (t >> 10) & 1, (t >> 11) & 1, t >> 12
        tiles = self.ts[0][0] if idx < 512 else self.ts[1][0]
        i = idx if idx < 512 else idx - 512
        a = tiles[i] if i < len(tiles) else np.zeros((8, 8), np.uint8)
        if hf:
            a = a[:, ::-1]
        if vf:
            a = a[::-1, :]
        pal = np.array(self.pal[pn], float)
        out = np.zeros((8, 8, 4))
        out[..., :3] = pal[a]
        out[..., 3] = np.where(a > 0, 255, 0)
        return out

    def metatile(self, m):
        k = 0 if m < 512 else 1
        _, mts, attrs, _ = self.ts[k]
        i = m if m < 512 else m - 512
        e = struct.unpack_from('<8H', mts, i * 16)
        attr = struct.unpack_from('<H', attrs, i * 2)[0]
        layers = []
        for L in (0, 1):
            a = np.zeros((16, 16, 4))
            for q in range(4):
                a[(q // 2) * 8:(q // 2) * 8 + 8, (q % 2) * 8:(q % 2) * 8 + 8] = self.tile(e[L * 4 + q])
            layers.append(a)
        return layers[0], layers[1], attr


def load_layout(name):
    import json
    L = [l for l in json.load(open(os.path.join(REPO, 'data/layouts/layouts.json')))['layouts'] if l.get('name') == name + '_Layout'][0]
    W, H = L['width'], L['height']
    v = struct.unpack('<%dH' % (W * H), open(os.path.join(REPO, L['blockdata_filepath']), 'rb').read())
    return [list(v[y * W:(y + 1) * W]) for y in range(H)], L


def tsdir(sym):
    import re
    return re.sub(r'(?<!^)(?=[A-Z])', '_', sym.replace('gTileset_', '')).lower()


def render_vanilla(name, x0=0, y0=0, w=None, h=None):
    """vanilla kaart -> (onder RGB, boven RGBA, botsing[h][w], gedrag[h][w], laagtype[h][w])"""
    g, L = load_layout(name)
    ts = VTileset(tsdir(L['primary_tileset']), tsdir(L['secondary_tileset']))
    w = w or len(g[0]) - x0
    h = h or len(g) - y0
    bot = np.zeros((h * 16, w * 16, 3))
    top = np.zeros((h * 16, w * 16, 4))
    coll = np.zeros((h, w), bool)
    beh = np.zeros((h, w), int)
    lay = np.zeros((h, w), int)
    for y in range(h):
        for x in range(w):
            v = g[y0 + y][x0 + x]
            b, t, attr = ts.metatile(v & 0x3ff)
            layer = attr >> 12
            base = b.copy()
            # onderlaag dekkend maken (index 0 = achtergrondkleur van palet 0)
            bg = np.array(ts.pal[0][0], float)
            m = base[..., 3] < 128
            base[m, :3] = bg
            if layer == NORMAL:          # NORMAL: onder = BG2, boven = BG1; beide als onder/boven gebruiken
                pass
            bot[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = base[..., :3]
            if layer == COVERED:         # boven ligt ook onder de speler: in de onderlaag mengen
                over_rgb(bot[y * 16:y * 16 + 16, x * 16:x * 16 + 16], t)
            else:
                top[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = t
            coll[y, x] = bool((v >> 10) & 3)
            beh[y, x] = attr & 0xff
            lay[y, x] = SPLIT if layer != COVERED and (t[..., 3] > 0).any() else COVERED
    return bot, top, coll, beh, lay


def over_rgb(dst, src):
    a = (src[..., 3:4] > 127).astype(float)
    dst[...] = dst * (1 - a) + src[..., :3] * a


# ====================================================================== kleur/teken-hulpjes
def to5(c):
    return (np.clip(np.asarray(c, float), 0, 255).astype(int) // 8) * 8


def lum(rgb):
    return (0.30 * rgb[..., 0] + 0.59 * rgb[..., 1] + 0.11 * rgb[..., 2]) / 255.0


def ramp(L, stops):
    """L (0..1) -> kleur op een verloop van stops (lijst RGB)"""
    r = np.array(stops, float)
    n = len(r) - 1
    t = np.clip(L * n, 0, n - 1e-6)
    i = t.astype(int)
    f = (t - i)[..., None]
    return r[i] * (1 - f) + r[i + 1] * f


def load_png(path):
    return np.array(Image.open(path).convert('RGBA')).astype(float)


def cut(sheet, cx, cy, w=1, h=1, px=16):
    return sheet[cy * px:(cy + h) * px, cx * px:(cx + w) * px].copy()


def value_noise(H, W, cell, seed):
    """gladde ruis (-1..1) met kenlengte 'cell' pixels"""
    rs = np.random.RandomState(seed)
    gh, gw = H // cell + 3, W // cell + 3
    g = rs.uniform(-1, 1, (gh, gw))
    yy, xx = np.mgrid[0:H, 0:W]
    gy, gx = yy / cell, xx / cell
    iy, ix = gy.astype(int), gx.astype(int)
    fy, fx = gy - iy, gx - ix
    fy, fx = fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)
    return (g[iy, ix] * (1 - fx) * (1 - fy) + g[iy, ix + 1] * fx * (1 - fy)
            + g[iy + 1, ix] * (1 - fx) * fy + g[iy + 1, ix + 1] * fx * fy)


def periodic_noise(size, cell, seed, octaves=1):
    """ruis die naadloos herhaalt over size x size pixels (tegelbaar)"""
    rs = np.random.RandomState(seed)
    out = np.zeros((size, size))
    amp = 1.0
    for o in range(octaves):
        n = max(1, size // cell)
        g = rs.uniform(-1, 1, (n, n))
        yy, xx = np.mgrid[0:size, 0:size]
        gy, gx = yy * n / size, xx * n / size
        iy, ix = gy.astype(int), gx.astype(int)
        fy, fx = gy - iy, gx - ix
        fy, fx = fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)
        a = g[iy % n, ix % n]; b = g[iy % n, (ix + 1) % n]
        c = g[(iy + 1) % n, ix % n]; d = g[(iy + 1) % n, (ix + 1) % n]
        out += amp * (a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy)
        amp *= 0.5
        cell = max(1, cell // 2)
    return out


def paste(dst, src, x, y, alpha=True):
    """src (RGBA) op dst (RGB of RGBA) leggen met linksboven (x, y) in pixels"""
    h, w = src.shape[:2]
    H, W = dst.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x0 >= x1 or y0 >= y1:
        return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    d = dst[y0:y1, x0:x1]
    m = s[..., 3] > 127 if alpha else np.ones(s.shape[:2], bool)
    if dst.shape[2] == 4:
        d[m] = s[m]
    else:
        d[m] = s[m][:, :3]


def flip_h(a):
    return a[:, ::-1].copy()


# ====================================================================== wereld-canvas
class World:
    def __init__(self, key, W, H, seed=0):
        self.key, self.W, self.H = key, W, H
        self.bot = np.zeros((H * 16, W * 16, 3))
        self.top = np.zeros((H * 16, W * 16, 4))
        self.coll = np.zeros((H, W), bool)
        self.beh = np.zeros((H, W), int)
        self.layer = np.full((H, W), COVERED, int)
        self.elev = np.full((H, W), 3, int)
        self.rnd = random.Random(seed)
        self.anims = []          # Anim-objecten
        self.anim_cell = {}      # (x, y) -> (anim, index van het vak in de animatie)
        yy, xx = np.mgrid[0:H * 16, 0:W * 16]
        self.yy, self.xx = yy, xx
        self.dith = B4[yy % 4, xx % 4]

    # ---- vakken
    def block(self, x, y, on=True):
        if 0 <= x < self.W and 0 <= y < self.H:
            self.coll[y, x] = on

    def cellpix(self, x, y, layer='bot'):
        a = self.bot if layer == 'bot' else self.top
        return a[y * 16:y * 16 + 16, x * 16:x * 16 + 16]

    def put(self, img, x, y, layer='bot'):
        """img (RGBA, veelvoud van 16) op vak (x, y); layer 'top' = boven de speler (SPLIT)"""
        if layer == 'bot':
            paste(self.bot, img, x * 16, y * 16)
        else:
            paste(self.top, img, x * 16, y * 16)
            for cy in range(img.shape[0] // 16):
                for cx in range(img.shape[1] // 16):
                    if 0 <= x + cx < self.W and 0 <= y + cy < self.H and (img[cy * 16:cy * 16 + 16, cx * 16:cx * 16 + 16, 3] > 127).any():
                        self.layer[y + cy, x + cx] = SPLIT

    def apply(self, f, fn, where=None, layer='bot'):
        """fn(rgb) -> rgb op de pixels waar het geditherde masker f (0..1) aan staat"""
        on = f > self.dith
        if where is not None:
            on &= where
        a = self.bot if layer == 'bot' else self.top
        rgb = a[..., :3]
        if layer == 'top':
            on &= a[..., 3] > 127
        rgb[on] = fn(rgb[on])
        return on

    def radial(self, cx, cy, r, fade, sy=1.0, wobble=0.2, noise=None):
        d = np.hypot(self.xx - cx, (self.yy - cy) * sy)
        if noise is not None:
            d = d - noise * r * wobble
        return np.clip((r - d) / fade, 0, 1)

    def line(self, x0, y0, x1, y1):
        pts = []
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n):
            t = i / max(n - 1, 1)
            pts.append((int(round(x0 + (x1 - x0) * t)), int(round(y0 + (y1 - y0) * t))))
        return pts

    def crack(self, rnd, x, y, ang, L, seg=(3, 7), wob=0.65, branch=0.22, depth=0, out=None):
        out = {} if out is None else out
        dist = 0.0
        while dist < L:
            n = rnd.randint(*seg)
            a = ang + rnd.uniform(-wob, wob)
            x1, y1 = x + math.cos(a) * n, y + math.sin(a) * n
            for p in self.line(x, y, x1, y1):
                out[p] = max(out.get(p, 0), 1 - dist / L)
            x, y = x1, y1
            dist += n
            if depth < 2 and rnd.random() < branch:
                self.crack(rnd, x, y, ang + rnd.choice((-1, 1)) * rnd.uniform(0.6, 1.1), (L - dist) * rnd.uniform(0.35, 0.6),
                           seg, wob, branch, depth + 1, out)
        return out

    def paint_crack(self, pts, core, rim, hot=None, thick=0.6, hot_at=0.75, hi=None, mask=None):
        P = dict(pts)
        Hh, Ww = self.bot.shape[:2]
        for (x, y), w in pts.items():
            if w > thick:
                for q in ((x + 1, y), (x, y + 1)):
                    P[q] = max(P.get(q, 0), w)
        ok = lambda x, y: 0 <= x < Ww and 0 <= y < Hh and (mask is None or mask[y, x])  # noqa: E731
        for (x, y) in P:
            for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if q not in P and ok(*q):
                    c = hi if hi is not None and q in ((x + 1, y), (x, y + 1)) else rim
                    self.bot[q[1], q[0]] = c(self.bot[q[1], q[0]]) if callable(c) else c
        for (x, y), w in P.items():
            if ok(x, y):
                self.bot[y, x] = hot if hot is not None and w > hot_at else core
        return P

    # ---- animaties
    def anim(self, name, frames_fn, cells, seq, period, layer='bot'):
        """frames_fn(f, x, y) -> RGBA 16x16 van vak (x, y) in frame f; cells: lijst (x, y); seq: framevolgorde."""
        a = Anim(name, frames_fn, list(cells), list(seq), period, layer)
        self.anims.append(a)
        for i, c in enumerate(a.cells):
            self.anim_cell[c] = (a, i)
        return a

    # ---- uitvoer
    def preview(self, path, scale=1):
        im = Image.fromarray(np.clip(self.bot, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
        im.alpha_composite(Image.fromarray(np.clip(self.top, 0, 255).astype(np.uint8), 'RGBA'))
        if scale != 1:
            im = im.resize((im.size[0] * scale, im.size[1] * scale), Image.NEAREST)
        im.save(path)
        return im


class Anim:
    def __init__(self, name, fn, cells, seq, period, layer):
        self.name, self.fn, self.cells, self.seq, self.period, self.layer = name, fn, cells, seq, period, layer
        self.nframes = max(seq) + 1


# ====================================================================== knippen + tileset maken
def _kmeans(X, k, seed=0, iters=25):
    X = np.asarray(X, float)
    rs = np.random.RandomState(seed)
    if len(X) <= k:
        C = np.zeros((k, X.shape[1]))
        C[:len(X)] = X
        if len(X):
            C[len(X):] = X[0]
        return C
    # k-means++
    C = [X[rs.randint(len(X))]]
    for _ in range(1, k):
        d = np.min(((X[:, None, :] - np.array(C)[None]) ** 2).sum(2), 1)
        if d.sum() == 0:
            C.append(X[rs.randint(len(X))])
            continue
        C.append(X[rs.choice(len(X), p=d / d.sum())])
    C = np.array(C)
    for _ in range(iters):
        a = ((X[:, None, :] - C[None]) ** 2).sum(2).argmin(1)
        for j in range(k):
            if (a == j).any():
                C[j] = X[a == j].mean(0)
    return C


def _wkmeans(X, w, k, seed=0, iters=20):
    """gewogen k-means op kleuren (X: unieke kleuren, w: aantallen)"""
    X = np.asarray(X, float)
    w = np.asarray(w, float)
    if len(X) <= k:
        C = np.zeros((k, 3))
        C[:len(X)] = X
        if len(X):
            C[len(X):] = X[0]
        return C
    rs = np.random.RandomState(seed)
    idx = [int(np.argmax(w))]
    for _ in range(1, k):
        d = np.min(((X[:, None, :] - X[idx][None]) ** 2).sum(2), 1) * w
        if d.sum() == 0:
            break
        idx.append(int(rs.choice(len(X), p=d / d.sum())))
    C = X[idx].copy()
    if len(C) < k:
        C = np.concatenate([C, np.repeat(C[:1], k - len(C), 0)])
    for _ in range(iters):
        a = ((X[:, None, :] - C[None]) ** 2).sum(2).argmin(1)
        for j in range(k):
            m = a == j
            if m.any():
                C[j] = (X[m] * w[m, None]).sum(0) / w[m].sum()
    return C


def _uniq_colors(blocks):
    c = np.concatenate([b[..., :3][b[..., 3] > 127] for b in blocks]) if blocks else np.zeros((0, 3))
    if not len(c):
        return np.zeros((1, 3)), np.ones(1)
    u, n = np.unique(c.astype(int), axis=0, return_counts=True)
    return u.astype(float), n.astype(float)


def emit_pair(world, out_prim, out_sec, num_pals=13, tile_limit=1023, mt_limit=1024, log=print):
    """Knipt world in metatiles en schrijft een eigen primary (out_prim) + secondary (out_sec).
    Geeft (grid met metatile-id's, info) terug."""
    W, H = world.W, world.H
    bot = to5(world.bot)
    top = world.top.copy()
    top[..., :3] = to5(top[..., :3])
    top[..., 3] = np.where(top[..., 3] > 127, 255, 0)
    # ---- animaties: vaste tileplekken (frame 0 bepaalt de metatile, de frames gaan naar anim/)
    anim_tiles = []    # lijst van (anim, celindex, kwadrant) in volgorde van de plekken
    for a in world.anims:
        for i, (cx, cy) in enumerate(a.cells):
            for q in range(4):
                anim_tiles.append((a, i, q))
    n_anim = len(anim_tiles)
    # ---- metatiles verzamelen
    cells = {}
    grid = [[None] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            b = bot[y * 16:y * 16 + 16, x * 16:x * 16 + 16]
            t = top[y * 16:y * 16 + 16, x * 16:x * 16 + 16]
            lay = world.layer[y, x]
            if not (t[..., 3] > 0).any():
                t = None
                lay = COVERED
            attr = (int(world.beh[y, x]) & 0xff) | (lay << 12)
            ac = world.anim_cell.get((x, y))
            akey = (ac[0].name, ac[1]) if ac else None
            k = (b.astype(np.uint8).tobytes(), None if t is None else t.astype(np.uint8).tobytes(), attr, akey)
            if k not in cells:
                cells[k] = dict(b=b.copy(), t=None if t is None else t.copy(), attr=attr, anim=ac, n=0)
            cells[k]['n'] += 1
            grid[y][x] = k
    keys = list(cells)
    log('%s: %d unieke vakken' % (world.key, len(keys)))
    # ---- te veel metatiles: gelijkende samenvoegen (zelfde attr, zelfde wel/geen bovenlaag, geen animaties)
    remap = {}
    if len(keys) > mt_limit:
        keys, remap = _merge_cells(cells, keys, mt_limit, log)
    # ---- 8x8-blokken
    blocks = []      # (sleutel, laag, kwadrant, pixels RGBA)
    for k in keys:
        c = cells[k]
        if c['anim']:
            continue
        for L, arr in ((0, c['b']), (1, c['t'])):
            if arr is None:
                continue
            for q in range(4):
                qy, qx = (q // 2) * 8, (q % 2) * 8
                if L == 0:
                    blk = np.concatenate([arr[qy:qy + 8, qx:qx + 8], np.full((8, 8, 1), 255.0)], 2)
                else:
                    blk = arr[qy:qy + 8, qx:qx + 8]
                if (blk[..., 3] > 127).any():
                    blocks.append(blk)
    # animatieblokken (alle frames) tellen mee voor de paletten
    anim_blocks = []
    for a in world.anims:
        frames = []
        for f in range(a.nframes):
            fr = []
            for (cx, cy) in a.cells:
                img = np.array(a.fn(f, cx, cy), float)
                img[..., :3] = to5(img[..., :3])
                img[..., 3] = np.where(img[..., 3] > 127, 255, 0)
                if a.layer == 'bot':
                    img[..., 3] = 255
                fr.append(img)
            frames.append(fr)
        a.frames = frames
        for fr in frames:
            for img in fr:
                for q in range(4):
                    qy, qx = (q // 2) * 8, (q % 2) * 8
                    anim_blocks.append(img[qy:qy + 8, qx:qx + 8])
    # ---- paletten: blokken clusteren op kleurgebruik
    MERGE_FLIP.clear()
    seenb = set()
    ub = []
    for b in blocks:
        kb = b.astype(np.uint8).tobytes()
        if kb not in seenb:
            seenb.add(kb)
            ub.append(b)
    allb = ub + anim_blocks
    feats = []
    for b in allb:
        c = b[..., :3][b[..., 3] > 127]
        feats.append(np.concatenate([c.mean(0), c.std(0) * 0.7]))
    feats = np.array(feats)
    # unieke blokken wegen (anders bepalen herhaalde vloeren alles)
    _, ui = np.unique(np.round(feats), axis=0, return_index=True)
    assign = ((feats[:, None, :] - _kmeans(feats[ui], num_pals, seed=1)[None]) ** 2).sum(2).argmin(1)
    for it in range(5):
        pals = []
        for j in range(num_pals):
            sel = [b for b, a_ in zip(allb, assign) if a_ == j]
            u, n = _uniq_colors(sel)
            pals.append(np.clip(np.round(_wkmeans(u, np.sqrt(n), 15, seed=it) / 8) * 8, 0, 248))
        errs = np.zeros((len(allb), num_pals))
        for i, b in enumerate(allb):
            c = b[..., :3][b[..., 3] > 127]
            for j, p in enumerate(pals):
                errs[i, j] = ((c[:, None, :] - p[None]) ** 2).sum(2).min(1).sum()
        new = errs.argmin(1)
        if (new == assign).all():
            break
        assign = new
    pals = [np.array(p) for p in pals]

    qcache = {}

    def quant(blk, pset=None):
        ck = (blk.astype(np.uint8).tobytes(), None if pset is None else tuple(pset))
        if ck not in qcache:
            qcache[ck] = _quant(blk, pset)
        return qcache[ck]

    def _quant(blk, pset=None):
        c = blk[..., :3].reshape(-1, 3)
        m = (blk[..., 3] > 127).reshape(-1)
        best = None
        for j in (range(num_pals) if pset is None else pset):
            d = ((c[:, None, :] - pals[j][None]) ** 2).sum(2)
            err = d.min(1)[m].sum()
            if best is None or err < best[0]:
                best = (err, j, d.argmin(1))
        _, j, idx = best
        return j, np.where(m, idx + 1, 0).reshape(blk.shape[:2]).astype(np.uint8)

    # ---- animatietiles: één palet voor alle frames van een kwadrant
    anim_slots = []      # per plek: (palet, [indices per frame])
    for a in world.anims:
        for i in range(len(a.cells)):
            for q in range(4):
                qy, qx = (q // 2) * 8, (q % 2) * 8
                fb = [a.frames[f][i][qy:qy + 8, qx:qx + 8] for f in range(a.nframes)]
                stack = np.concatenate(fb, 0)
                j, _ = quant(stack)
                anim_slots.append((j, [quant(b, [j])[1] for b in fb]))
    # ---- gewone tiles ontdubbelen
    uniq = []          # indexarrays
    upal = []          # palet per unieke tile
    ucount = []
    lookup = {}

    def tile_id(blk):
        if not (blk[..., 3] > 127).any():
            return None
        j, idx = quant(blk)
        for hf in (0, 1):
            for vf in (0, 1):
                v = idx[:, ::-1] if hf else idx
                v = v[::-1, :] if vf else v
                kk = (v.tobytes(), j)
                if kk in lookup:
                    t = lookup[kk]
                    ucount[t] += 1
                    return t, hf, vf
        uniq.append(idx)
        upal.append(j)
        ucount.append(1)
        lookup[(idx.tobytes(), j)] = len(uniq) - 1
        return len(uniq) - 1, 0, 0

    ment = {}
    for k in keys:
        c = cells[k]
        ent = []
        for L, arr in ((0, c['b']), (1, c['t'])):
            for q in range(4):
                if arr is None:
                    ent.append(None)
                    continue
                qy, qx = (q // 2) * 8, (q % 2) * 8
                if c['anim'] and L == (0 if c['anim'][0].layer == 'bot' else 1):
                    a, i = c['anim']
                    ent.append(('A', anim_tiles.index((a, i, q))))
                    continue
                if L == 0:
                    blk = np.concatenate([arr[qy:qy + 8, qx:qx + 8], np.full((8, 8, 1), 255.0)], 2)
                else:
                    blk = arr[qy:qy + 8, qx:qx + 8]
                ent.append(tile_id(blk))
        ment[k] = ent
    log('%s: %d unieke tiles + %d animatietiles (limiet %d)' % (world.key, len(uniq), n_anim, tile_limit))
    # ---- te veel tiles: verliesgevend samenvoegen
    budget = tile_limit - n_anim
    tmap = list(range(len(uniq)))
    if len(uniq) > budget:
        tmap = _merge_tiles(uniq, upal, ucount, pals, budget, log)
    keep = sorted(set(tmap))
    # plekken: primary 1..511, secondary: eerst animaties, dan de rest
    slots = {}
    order = keep
    prim_n = min(511, len(order))
    for n, t in enumerate(order[:prim_n]):
        slots[t] = 1 + n
    for n, t in enumerate(order[prim_n:]):
        slots[t] = 512 + n_anim + n
    assert 512 + n_anim + len(order) - prim_n <= 1024, 'te veel tiles'

    def entry(e):
        if e is None:
            return 0
        if e[0] == 'A':
            j = anim_slots[e[1]][0]
            return (512 + e[1]) | ((j) << 12)
        t, hf, vf = e
        r = tmap[t]
        # samengevoegde tile: spiegeling van de vervanger t.o.v. het origineel zit in _merge_tiles (MERGE_FLIP)
        fh, fv = MERGE_FLIP.get(t, (0, 0))
        return slots[r] | ((hf ^ fh) << 10) | ((vf ^ fv) << 11) | (upal[r] << 12)

    # ---- metatiles: eerst de veelgebruikte (primary), dan de rest
    keys_sorted = sorted(keys, key=lambda k: -cells[k]['n'])
    mid = {}
    pm, sm = bytearray(), bytearray()
    pa, sa = bytearray(), bytearray()
    for n, k in enumerate(keys_sorted):
        ents = [entry(e) for e in ment[k]]
        data = struct.pack('<8H', *ents)
        at = struct.pack('<H', cells[k]['attr'])
        if n < 512:
            mid[k] = n
            pm += data
            pa += at
        else:
            mid[k] = 512 + n - 512
            sm += data
            sa += at
    assert len(keys_sorted) <= 1024
    # primary aanvullen tot 512 metatiles (anders verschuift NUM_METATILES_IN_PRIMARY niets, maar zo blijft het netjes)
    while len(pm) < 512 * 16:
        pm += struct.pack('<8H', *([0] * 8))
        pa += struct.pack('<H', COVERED << 12)
    # ---- schrijven
    for out, base in ((out_prim, 0), (out_sec, 512)):
        os.makedirs(out + '/palettes', exist_ok=True)
    def write_tiles(out, arrs):
        rows = max(1, (len(arrs) + 15) // 16)
        img = np.zeros((rows * 8, 128), np.uint8)
        for i, t in enumerate(arrs):
            img[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = t
        im = Image.fromarray(img, 'P')
        grey = []
        for i in range(16):
            grey += [i * 16, i * 16, i * 16]
        im.putpalette(grey + [0] * (768 - 48))
        im.save(out + '/tiles.png')
    ptiles = [np.zeros((8, 8), np.uint8)] + [uniq[t] for t in order[:prim_n]]
    stiles = [s[1][0] for s in anim_slots] + [uniq[t] for t in order[prim_n:]]
    write_tiles(out_prim, ptiles)
    write_tiles(out_sec, stiles)
    for out, rng in ((out_prim, range(0, 6)), (out_sec, range(6, 13))):
        for i in range(16):
            cols = [(0, 0, 0)] * 16
            if i in rng and i < num_pals:
                cols = [(255, 0, 255)] + [tuple(int(v) for v in c) for c in pals[i]]
            with open('%s/palettes/%02d.pal' % (out, i), 'w', newline='\r\n') as f:
                f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in cols))
    open(out_prim + '/metatiles.bin', 'wb').write(pm)
    open(out_prim + '/metatile_attributes.bin', 'wb').write(pa)
    open(out_sec + '/metatiles.bin', 'wb').write(sm or struct.pack('<8H', *([0] * 8)))
    open(out_sec + '/metatile_attributes.bin', 'wb').write(sa or struct.pack('<H', COVERED << 12))
    # animatieframes: per animatie een reeks png's (alle plekken van die animatie achter elkaar)
    pos = 0
    anim_info = []
    for a in world.anims:
        n = len(a.cells) * 4
        d = '%s/anim/%s' % (out_sec, a.name)
        os.makedirs(d, exist_ok=True)
        for f in range(a.nframes):
            arrs = [anim_slots[pos + i][1][f] for i in range(n)]
            rows = (n + 15) // 16
            img = np.zeros((rows * 8, 128), np.uint8)
            for i, t in enumerate(arrs):
                img[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = t
            im = Image.fromarray(img, 'P')
            grey = []
            for i in range(16):
                grey += [i * 16, i * 16, i * 16]
            im.putpalette(grey + [0] * (768 - 48))
            im.save('%s/%d.png' % (d, f))
        anim_info.append(dict(name=a.name, slot=pos, ntiles=n, nframes=a.nframes, seq=a.seq, period=a.period,
                              rows=(n + 15) // 16))
        pos += n
    out_grid = [[mid[remap.get(grid[y][x], grid[y][x])] for x in range(W)] for y in range(H)]
    info = dict(tiles=len(order) + n_anim, prim_tiles=prim_n + 1, sec_tiles=len(stiles), metatiles=len(keys_sorted),
                anims=anim_info, pals=pals)
    log('%s: %d tiles (%d primary, %d secondary), %d metatiles' % (world.key, info['tiles'], prim_n + 1, len(stiles), len(keys_sorted)))
    return out_grid, info


MERGE_FLIP = {}


def _merge_tiles(uniq, upal, ucount, pals, budget, log):
    """voegt de meest gelijkende tiles samen tot er 'budget' over zijn; geeft tmap (tile -> vervanger)"""
    n = len(uniq)
    rgb = np.zeros((n, 4, 64 * 3))        # 4 spiegelingen
    alpha = np.zeros((n, 64))
    for i, (idx, j) in enumerate(zip(uniq, upal)):
        p = np.concatenate([[[0, 0, 0]], pals[j]])
        for f, (hf, vf) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
            v = idx[:, ::-1] if hf else idx
            v = v[::-1, :] if vf else v
            c = p[v].reshape(-1, 3).copy()
            c[v.reshape(-1) == 0] = -400          # doorzichtig telt zwaar mee
            rgb[i, f] = c.reshape(-1)
        alpha[i] = (idx.reshape(-1) > 0)
    alive = np.ones(n, bool)
    tmap = list(range(n))
    count = np.array(ucount, float)
    flip = [(0, 0)] * n
    flips = ((0, 0), (1, 0), (0, 1), (1, 1))
    while alive.sum() > budget:
        A = np.where(alive)[0]
        X = rgb[A, 0]
        sq = (X ** 2).sum(1)
        best_d = np.full(len(A), np.inf)
        best_j = np.zeros(len(A), int)
        best_f = np.zeros(len(A), int)
        for f in range(4):
            Y = rgb[A, f]
            D = sq[:, None] + (Y ** 2).sum(1)[None] - 2 * X @ Y.T
            np.fill_diagonal(D, np.inf)
            j = D.argmin(1)
            d = D[np.arange(len(A)), j]
            m = d < best_d
            best_d[m], best_j[m], best_f[m] = d[m], j[m], f
        # kosten: verschil x hoe vaak de weg te halen tile voorkomt
        cost = best_d * np.sqrt(count[A])
        excess = int(alive.sum() - budget)
        order = np.argsort(cost)
        touched = set()
        done = 0
        for o in order:
            if done >= max(1, excess // 3) or done >= excess:
                break
            a, b = A[o], A[best_j[o]]
            if a in touched or b in touched:
                continue
            # a verdwijnt, b blijft; a = spiegeling f van b  ->  b gespiegeld f benadert a
            alive[a] = False
            fh, fv = flips[best_f[o]]
            # rgb[b, f] ~ rgb[a, 0]: a ~ b gespiegeld met f
            for t in range(n):
                if tmap[t] == a:
                    tmap[t] = b
                    ph, pv = flip[t]
                    flip[t] = (ph ^ fh, pv ^ fv)
            count[b] += count[a]
            touched |= {a, b}
            done += 1
    for t in range(n):
        MERGE_FLIP[t] = flip[t]
    log('  samengevoegd: %d -> %d tiles' % (n, alive.sum()))
    return tmap


def _merge_cells(cells, keys, limit, log):
    """te veel metatiles: gelijkende vakken (zelfde attr/bovenlaag, geen animatie) samenvoegen"""
    remap = {}
    alive = list(keys)
    def vec(c):
        v = c['b'].reshape(-1)
        if c['t'] is not None:
            v = np.concatenate([v, c['t'].reshape(-1)])
        return v
    while len(alive) > limit:
        groups = {}
        for k in alive:
            c = cells[k]
            if c['anim']:
                continue
            groups.setdefault((c['attr'], c['t'] is None), []).append(k)
        cands = []
        for g, ks in groups.items():
            if len(ks) < 2:
                continue
            X = np.array([vec(cells[k]) for k in ks])
            sq = (X ** 2).sum(1)
            D = sq[:, None] + sq[None] - 2 * X @ X.T
            np.fill_diagonal(D, np.inf)
            j = D.argmin(1)
            for i in range(len(ks)):
                cands.append((D[i, j[i]] * math.sqrt(cells[ks[i]]['n']), ks[i], ks[j[i]]))
        cands.sort(key=lambda c: c[0])
        excess = len(alive) - limit
        touched = set()
        done = 0
        for _, a, b in cands:
            if done >= max(1, excess // 3) or done >= excess:
                break
            if a in touched or b in touched:
                continue
            remap[a] = b
            cells[b]['n'] += cells[a]['n']
            touched |= {a, b}
            alive.remove(a)
            done += 1
    # ketens oplossen
    for k in list(remap):
        r = remap[k]
        while r in remap:
            r = remap[r]
        remap[k] = r
    log('  vakken samengevoegd tot %d' % len(alive))
    return alive, remap
