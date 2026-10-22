"""Gedeelde hulpjes voor de concept-tilesets (tools/concept/tiles/*_tiles.py).

- Teken-primitieven op RGBA-canvassen (numpy, kleuren als RGB-tuples uit vaste paletten).
- Tileset-bouwer: metatiles (onderlaag + bovenlaag, gedrag, laagtype) -> 8x8-tegels per palet,
  ontdubbeld (ook gespiegeld), en de bestanden zoals een GBA secondary ze heeft
  (tiles.png, palettes/NN.pal, metatiles.bin, metatile_attributes.bin, metatile_names.json).
- Renderen van bestaande tilesets/kaarten uit de repo (schoon, zonder markeringen) voor vergelijkingen.
"""
import json, os, re, struct
import numpy as np
from PIL import Image

T = (0, 0, 0, 0)

BEH = {}
for _l in open('include/constants/metatile_behaviors.h'):
    _m = re.match(r'\s*(MB_\w+)', _l)
    if _m and _m.group(1) not in BEH:
        BEH[_m.group(1)] = len(BEH)
LAYER = {'normal': 0, 'covered': 1, 'split': 2}


def snap(c):
    return tuple(int(v) & 0xF8 for v in c)


# ---------------------------------------------------------------- tekenen
class Canvas:
    def __init__(self, w, h, fill=None):
        self.a = np.zeros((h, w, 4), np.uint8)
        if fill is not None:
            self.a[:, :, :3] = fill
            self.a[:, :, 3] = 255
        self.w, self.h = w, h

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            if c is None or len(c) == 4 and c[3] == 0:
                self.a[y, x] = 0
            else:
                self.a[y, x, :3] = c[:3]
                self.a[y, x, 3] = 255

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h and self.a[y, x, 3]:
            return tuple(int(v) for v in self.a[y, x, :3])
        return None

    def rect(self, x0, y0, x1, y1, c):  # inclusief
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.px(x, y, c)

    def hline(self, x0, x1, y, c):
        self.rect(x0, y, x1, y, c)

    def vline(self, x, y0, y1, c):
        self.rect(x, y0, x, y1, c)

    def box(self, x0, y0, x1, y1, c):
        self.hline(x0, x1, y0, c); self.hline(x0, x1, y1, c)
        self.vline(x0, y0, y1, c); self.vline(x1, y0, y1, c)

    def paste(self, other, ox, oy):
        for y in range(other.h):
            for x in range(other.w):
                if other.a[y, x, 3]:
                    self.px(ox + x, oy + y, tuple(other.a[y, x, :3]))

    def sub(self, x, y, w, h):
        c = Canvas(w, h)
        c.a = self.a[y:y + h, x:x + w].copy()
        return c

    def mask_fill(self, mask, c):
        """mask: functie (x, y) -> bool"""
        for y in range(self.h):
            for x in range(self.w):
                if mask(x, y):
                    self.px(x, y, c)

    def outline(self, c, diag=False):
        """Omlijning rond alle niet-transparante pixels (binnen het canvas)."""
        a = self.a[:, :, 3] > 0
        out = []
        for y in range(self.h):
            for x in range(self.w):
                if a[y, x]:
                    continue
                nb = [(1, 0), (-1, 0), (0, 1), (0, -1)] + ([(1, 1), (-1, 1), (1, -1), (-1, -1)] if diag else [])
                if any(0 <= x + dx < self.w and 0 <= y + dy < self.h and a[y + dy, x + dx] for dx, dy in nb):
                    out.append((x, y))
        for x, y in out:
            self.px(x, y, c)

    def recolor(self, mp):
        for y in range(self.h):
            for x in range(self.w):
                c = self.get(x, y)
                if c is not None and c in mp:
                    self.px(x, y, mp[c])

    def img(self):
        return Image.fromarray(self.a, 'RGBA')


def ellipse_mask(cx, cy, rx, ry):
    return lambda x, y: ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1


# ---------------------------------------------------------------- tileset
class Tileset:
    """Verzamelt metatiles en bouwt er een GBA-secondary van (paletten 6..12)."""

    def __init__(self, palettes, first=6):
        self.pals = {}          # nummer -> lijst van 16 RGB (0 = transparant)
        for i, cols in enumerate(palettes):
            cols = [snap(c) for c in cols]
            assert len(cols) <= 15, (first + i, len(cols))
            assert len(set(cols)) == len(cols), ('dubbele kleur', first + i)
            self.pals[first + i] = [(255, 0, 255)] + cols + [(0, 0, 0)] * (15 - len(cols))
        self.first = first
        self.tiles = []         # lijst van 8x8 index-arrays
        self.tile_key = {}      # bytes -> (idx, hflip, vflip)
        self.mts = []           # (naam, [8 entries], attr)
        self.names = {}
        self.hint = {}          # kleur -> palet (voorkeur)
        self.errors = []
        self.cost = {}          # metatile-naam -> nieuwe tegels

    def colors_of(self, p):
        return set(self.pals[p][1:])

    def _pal_for(self, block):
        cols = {tuple(int(v) for v in block[y, x, :3]) for y in range(8) for x in range(8) if block[y, x, 3]}
        cands = [p for p in self.pals if cols <= self.colors_of(p)]
        return cands, cols

    def _tile(self, block, pal_pref=None):
        if not block[:, :, 3].any():
            return 0  # tegel 0 van de primary (leeg)
        cands, cols = self._pal_for(block)
        if not cands:
            best = max(self.pals, key=lambda p: len(cols & self.colors_of(p)))
            self.errors.append((sorted(cols - self.colors_of(best)), best))
            cands = [best]
        p = pal_pref if pal_pref in cands else cands[0]
        lut = {c: i for i, c in enumerate(self.pals[p]) if i}
        for c in cols - set(lut):  # vreemde kleur (bijv. kabel over een boom): dichtstbijzijnde kleur
            lut[c] = min(range(1, 16), key=lambda i: sum((a - b) ** 2 for a, b in zip(c, self.pals[p][i])))
        idx = np.zeros((8, 8), np.uint8)
        for y in range(8):
            for x in range(8):
                if block[y, x, 3]:
                    c = tuple(int(v) for v in block[y, x, :3])
                    idx[y, x] = lut[c]
        for hf in (0, 1):
            for vf in (0, 1):
                t = idx[:, ::-1] if hf else idx
                t = t[::-1, :] if vf else t
                k = t.tobytes()
                if k in self.tile_key:
                    n = self.tile_key[k]
                    return (512 + n) | (hf << 10) | (vf << 11) | (p << 12)
        self.tiles.append(idx)
        self.tile_key[idx.tobytes()] = len(self.tiles) - 1
        return (512 + len(self.tiles) - 1) | (p << 12)

    def add(self, name, bottom, top=None, beh='MB_NORMAL', layer='covered', pal_pref=None):
        """bottom/top: Canvas 16x16 (of None). Onderlaag moet dekkend zijn."""
        if name in self.names:
            raise ValueError('dubbele naam ' + name)
        n0 = len(self.tiles)
        ents = []
        for lay in (bottom, top):
            for k in range(4):
                ox, oy = (k % 2) * 8, (k // 2) * 8
                if lay is None:
                    ents.append(0)
                    continue
                blk = lay.a[oy:oy + 8, ox:ox + 8]
                ents.append(self._tile(blk, pal_pref))
        attr = BEH[beh] | (LAYER[layer] << 12)
        self.cost[name] = len(self.tiles) - n0
        self.names[name] = 512 + len(self.mts)
        self.mts.append((name, ents, attr))
        return self.names[name]

    def add_palvariant(self, name, src, frm, to):
        """Kopie van metatile `src` waarin palet frm overal palet to wordt (zelfde tegels, 0 extra)."""
        n, ents, attr = self.mts[self.names[src] - 512]
        ne = [((e & 0x0FFF) | (to << 12)) if (e >> 12) == frm and e else e for e in ents]
        self.names[name] = 512 + len(self.mts)
        self.mts.append((name, ne, attr))

    # ------------------------------------------------------------ uitvoer
    def write(self, out):
        os.makedirs(out + '/palettes', exist_ok=True)
        n = len(self.tiles)
        rows = (n + 15) // 16
        arr = np.zeros((rows * 8, 128), np.uint8)
        for i, t in enumerate(self.tiles):
            arr[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = t
        im = Image.fromarray(arr, 'P')
        flat = []
        for c in self.pals[self.first]:
            flat += list(c)
        im.putpalette(flat + [0] * (768 - len(flat)))
        im.save(out + '/tiles.png')
        for p, cols in self.pals.items():
            with open(f'{out}/palettes/{p:02}.pal', 'w') as f:
                f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join(f'{r} {g} {b}\r\n' for r, g, b in cols))
        with open(out + '/metatiles.bin', 'wb') as f:
            for _, ents, _ in self.mts:
                f.write(struct.pack('<8H', *ents))
        with open(out + '/metatile_attributes.bin', 'wb') as f:
            for _, _, a in self.mts:
                f.write(struct.pack('<H', a))
        json.dump({k: hex(v) for k, v in self.names.items()}, open(out + '/metatile_names.json', 'w'), indent=1)

    # ------------------------------------------------------------ renderen
    def render_mt(self, m, prim=None):
        """RGB 16x16 van metatile-id m (>=512 eigen; <512 uit prim (Prim))."""
        if m < 512:
            return prim.render_mt(m)
        _, ents, _ = self.mts[m - 512]
        img = np.zeros((16, 16, 3), np.uint8)
        for layer in range(2):
            for k in range(4):
                e = ents[layer * 4 + k]
                t, hf, vf, p = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
                if t < 512:
                    if layer == 0 and prim is not None:
                        pass
                    continue
                tp = self.tiles[t - 512]
                tp = tp[:, ::-1] if hf else tp
                tp = tp[::-1, :] if vf else tp
                ox, oy = (k % 2) * 8, (k // 2) * 8
                pal = np.array(self.pals[p], np.uint8)
                blk = img[oy:oy + 8, ox:ox + 8]
                mask = tp != 0
                blk[mask] = pal[tp][mask]
        return img

    def sheet(self, path, per_row=8, scale=2):
        n = len(self.mts)
        rows = (n + per_row - 1) // per_row
        img = np.full((rows * 16, per_row * 16, 3), 40, np.uint8)
        for i in range(n):
            img[(i // per_row) * 16:(i // per_row) * 16 + 16, (i % per_row) * 16:(i % per_row) * 16 + 16] = self.render_mt(512 + i)
        Image.fromarray(img).resize((per_row * 16 * scale, rows * 16 * scale), Image.NEAREST).save(path)

    def tiles_sheet(self, path, scale=2):
        """Tegels in hun eigen palet (zoals ze in de tileset staan, gekleurd)."""
        usedpal = {}
        for _, ents, _ in self.mts:
            for e in ents:
                if (e & 0x3FF) >= 512:
                    usedpal.setdefault((e & 0x3FF) - 512, e >> 12)
        n = len(self.tiles)
        rows = (n + 15) // 16
        img = np.full((rows * 8, 128, 3), 255, np.uint8)
        for i, t in enumerate(self.tiles):
            pal = np.array(self.pals[usedpal.get(i, self.first)], np.uint8)
            blk = pal[t].copy()
            blk[t == 0] = (255, 255, 255)
            img[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = blk
        Image.fromarray(img).resize((128 * scale, rows * 8 * scale), Image.NEAREST).save(path)

    def render_map(self, grid, prim=None):
        """grid: lijst van rijen met metatile-id's."""
        h, w = len(grid), len(grid[0])
        img = np.zeros((h * 16, w * 16, 3), np.uint8)
        for y in range(h):
            for x in range(w):
                img[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = self.render_mt(grid[y][x], prim)
        return img


def palette_strip(ts, path, scale=12):
    ps = sorted(ts.pals)
    img = np.zeros((len(ps), 16, 3), np.uint8)
    for r, p in enumerate(ps):
        img[r] = ts.pals[p]
    Image.fromarray(img).resize((16 * scale, len(ps) * scale), Image.NEAREST).save(path)


# ---------------------------------------------------------------- bestaande kaarten (schoon renderen)
def _load_dir(dirn):
    base = dirn
    if os.path.exists(dirn + '/BASE'):
        base = os.path.join(os.path.dirname(dirn), open(dirn + '/BASE').read().strip())
    tdir = base
    if os.path.exists(dirn + '/TILES'):
        tdir = os.path.join(os.path.dirname(dirn), open(dirn + '/TILES').read().strip())
    b = np.frombuffer(open(tdir + '/tiles.4bpp', 'rb').read(), np.uint8)
    nt = len(b) // 32
    tiles = np.stack([b & 15, b >> 4], -1).reshape(nt, 8, 8)
    mts = np.frombuffer(open(base + '/metatiles.bin', 'rb').read(), '<u2').reshape(-1, 8)
    pals = np.zeros((16, 16, 3), np.uint8)
    for i in range(16):
        f = f'{dirn}/palettes/{i:02}.pal'
        if os.path.exists(f):
            lines = open(f).read().split('\n')[3:19]
            pals[i] = [tuple(map(int, l.split())) for l in lines]
    return tiles, mts, pals


def _tsname(sym):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', sym.replace('gTileset_', '')).lower()


def render_repo_map(mapname, y0=0, y1=None, x0=0, x1=None):
    d = json.load(open(f'data/maps/{mapname}/map.json'))
    L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == d['layout']][0]
    w, h = L['width'], L['height']
    v = struct.unpack(f'<{w * h}H', open(L['blockdata_filepath'], 'rb').read())
    pt, pm, pp = _load_dir('data/tilesets/primary/' + _tsname(L['primary_tileset']))
    st, sm, sp = _load_dir('data/tilesets/secondary/' + _tsname(L['secondary_tileset']))
    pal = np.concatenate([pp[:6], sp[6:13], pp[13:]])
    y1 = h if y1 is None else y1
    x1 = w if x1 is None else x1
    img = np.zeros(((y1 - y0) * 16, (x1 - x0) * 16, 3), np.uint8)
    for my in range(y0, y1):
        for mx in range(x0, x1):
            m = v[my * w + mx] & 0x3FF
            ent = pm[m] if m < 512 else sm[m - 512]
            for layer in range(2):
                for k in range(4):
                    e = int(ent[layer * 4 + k])
                    t, hf, vf, pn = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, (e >> 12) & 15
                    tp = pt[t] if t < 512 else (st[t - 512] if t - 512 < len(st) else np.zeros((8, 8), np.uint8))
                    tp = tp[:, ::-1] if hf else tp
                    tp = tp[::-1, :] if vf else tp
                    oy, ox = (my - y0) * 16 + (k // 2) * 8, (mx - x0) * 16 + (k % 2) * 8
                    blk = img[oy:oy + 8, ox:ox + 8]
                    col = pal[pn][tp]
                    mask = tp != 0 if layer else np.ones_like(tp, bool)
                    blk[mask] = col[mask]
    return img


class Prim:
    """Metatiles van een bestaande (primary) tileset renderen, bijv. General voor gras/bomen."""

    def __init__(self, name='general'):
        self.t, self.m, self.p = _load_dir('data/tilesets/primary/' + name)

    def render_mt(self, m):
        img = np.zeros((16, 16, 3), np.uint8)
        for layer in range(2):
            for k in range(4):
                e = int(self.m[m][layer * 4 + k])
                t, hf, vf, pn = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, (e >> 12) & 15
                if t >= len(self.t):
                    continue
                tp = self.t[t]
                tp = tp[:, ::-1] if hf else tp
                tp = tp[::-1, :] if vf else tp
                blk = img[(k // 2) * 8:(k // 2) * 8 + 8, (k % 2) * 8:(k % 2) * 8 + 8]
                mask = tp != 0 if layer else np.ones_like(tp, bool)
                blk[mask] = self.p[pn][tp][mask]
        return img


def side_by_side(a, b, path, gap=8, label_h=0):
    h = max(a.shape[0], b.shape[0])
    img = np.full((h, a.shape[1] + gap + b.shape[1], 3), 24, np.uint8)
    img[:a.shape[0], :a.shape[1]] = a
    img[:b.shape[0], a.shape[1] + gap:] = b
    Image.fromarray(img).save(path)
    return img


def repo_top_layer(mapname, x0, y0, x1, y1):
    """Bovenlaag (objecten) van een stuk bestaande kaart als RGBA-Canvas (voor hergebruik/omkleuren)."""
    d = json.load(open(f'data/maps/{mapname}/map.json'))
    L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == d['layout']][0]
    w, h = L['width'], L['height']
    v = struct.unpack(f'<{w * h}H', open(L['blockdata_filepath'], 'rb').read())
    pt, pm, pp = _load_dir('data/tilesets/primary/' + _tsname(L['primary_tileset']))
    st, sm, sp = _load_dir('data/tilesets/secondary/' + _tsname(L['secondary_tileset']))
    pal = np.concatenate([pp[:6], sp[6:13], pp[13:]])
    c = Canvas((x1 - x0) * 16, (y1 - y0) * 16)
    for my in range(y0, y1):
        for mx in range(x0, x1):
            m = v[my * w + mx] & 0x3FF
            ent = pm[m] if m < 512 else sm[m - 512]
            for k in range(4):
                e = int(ent[4 + k])
                t, hf, vf, pn = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, (e >> 12) & 15
                tp = pt[t] if t < 512 else st[t - 512]
                tp = tp[:, ::-1] if hf else tp
                tp = tp[::-1, :] if vf else tp
                oy, ox = (my - y0) * 16 + (k // 2) * 8, (mx - x0) * 16 + (k % 2) * 8
                for yy in range(8):
                    for xx in range(8):
                        if tp[yy, xx]:
                            c.px(ox + xx, oy + yy, tuple(int(q) for q in pal[pn][tp[yy, xx]]))
    return c


def budget(ts, groups):
    """Tegels per groep (prefixen) voor NOTITIES.md."""
    out = {}
    for name, c in ts.cost.items():
        g = next((k for k in groups if name.startswith(k)), 'overig')
        out[g] = out.get(g, 0) + c
    return out
