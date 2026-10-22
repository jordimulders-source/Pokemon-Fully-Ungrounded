"""Ronde 2 van de concept-tilesets: bouwen op Hoenn-tegels (op indexniveau) in plaats van alles zelf te tekenen.

- load_set(): tiles (n,8,8 indexen), metatiles, attributen en paletten van een bestaande tileset uit de repo.
- Pair: een primary (paletten 0-5) + secondary (6-12) in aanbouw. De Andes-primary is een kopie van General
  met dezelfde tegelnummers, dus Hoenn-secondaries die naar General-tegels wijzen werken er ongewijzigd op.
- import_mt / import_region: Hoenn-metatiles overnemen (secondary-tegels kopiëren, palet omzetten naar een eigen slot).
- add_drawn: zelf getekende metatiles (RGBA-canvassen) kwantiseren naar de kleuren van een gekozen palet.
- Renderen en de opleverbestanden (tiles.png, palettes, metatiles.bin, attributes, names, sheets).
"""
import json, os, re, struct
import numpy as np
from PIL import Image

from tilelib import Canvas, BEH, LAYER  # noqa: F401


def load_set(kind, name):
    d = f'data/tilesets/{kind}/{name}'
    b = np.frombuffer(open(d + '/tiles.4bpp', 'rb').read(), np.uint8)
    tiles = np.stack([b & 15, b >> 4], -1).reshape(-1, 8, 8).copy()
    mts = np.frombuffer(open(d + '/metatiles.bin', 'rb').read(), '<u2').reshape(-1, 8).copy()
    attrs = np.frombuffer(open(d + '/metatile_attributes.bin', 'rb').read(), '<u2').copy()
    pals = np.zeros((16, 16, 3), int)
    for i in range(16):
        f = f'{d}/palettes/{i:02}.pal'
        if os.path.exists(f):
            pals[i] = [tuple(map(int, l.split())) for l in open(f).read().split('\n')[3:19]]
    return {'tiles': tiles, 'mts': mts, 'attrs': attrs, 'pals': pals, 'name': name}


def snap(c):
    return tuple(int(v) & 0xF8 for v in c)


def recolor(pal16, mapping):
    """pal16: 16 kleuren; mapping: {index: kleur} of {oude kleur: nieuwe kleur}."""
    out = [tuple(int(v) for v in c) for c in pal16]
    for k, v in mapping.items():
        if isinstance(k, int):
            out[k] = tuple(v)
        else:
            out = [tuple(v) if c == tuple(k) else c for c in out]
    return out


def _key(t):
    return t.tobytes()


class Pair:
    def __init__(self, prim_tiles, prim_mts, prim_attrs, prim_pals):
        self.pt = [t.copy() for t in prim_tiles]          # primary-tegels (512)
        self.pm = [list(map(int, m)) for m in prim_mts]    # primary-metatiles
        self.pa = [int(a) for a in prim_attrs]
        self.pals = [list(map(tuple, p)) for p in prim_pals[:6]] + [[(255, 0, 255)] + [(0, 0, 0)] * 15 for _ in range(7)]
        self.st, self.sm, self.sa = [], [], []
        self.names = {}
        self.pnames = {}
        self.cost = {}
        self._index()

    def _index(self):
        self.pkey = {}
        for i, t in enumerate(self.pt):
            for hf in (0, 1):
                for vf in (0, 1):
                    tt = t[:, ::-1] if hf else t
                    tt = tt[::-1, :] if vf else tt
                    self.pkey.setdefault(_key(tt), (i, hf, vf))
        self.skey = {}

    # ---------------------------------------------------------------- tegels
    def tile_ref(self, idx, pal, target='S'):
        """Zoek of maak een tegel; geeft een metatile-entry terug (tegel | flips | palet)."""
        if not idx.any():
            return 0
        k = _key(idx)
        if k in self.pkey:
            i, hf, vf = self.pkey[k]
            return i | (hf << 10) | (vf << 11) | (pal << 12)
        if target == 'P':
            free = self.free_prim.pop(0)
            self.pt[free] = idx.copy()
            for hf in (0, 1):
                for vf in (0, 1):
                    tt = idx[:, ::-1] if hf else idx
                    tt = tt[::-1, :] if vf else tt
                    self.pkey.setdefault(_key(tt), (free, hf, vf))
            return free | (pal << 12)
        if k in self.skey:
            i, hf, vf = self.skey[k]
            return (512 + i) | (hf << 10) | (vf << 11) | (pal << 12)
        self.st.append(idx.copy())
        n = len(self.st) - 1
        for hf in (0, 1):
            for vf in (0, 1):
                tt = idx[:, ::-1] if hf else idx
                tt = tt[::-1, :] if vf else tt
                self.skey.setdefault(_key(tt), (n, hf, vf))
        return (512 + n) | (pal << 12)

    def add_mt(self, name, ents, attr, target='S', slot=None):
        if target == 'P':
            m = slot
            self.pm[m] = list(ents)
            self.pa[m] = attr
            self.pnames[name] = m
            self.names[name] = m
            return m
        if name in self.names:
            raise ValueError('dubbel: ' + name)
        self.sm.append(list(ents))
        self.sa.append(attr)
        self.names[name] = 512 + len(self.sm) - 1
        return self.names[name]

    # ---------------------------------------------------------------- Hoenn-metatiles overnemen
    def import_mt(self, src, mid, palmap, name, target='S', slot=None, tilemap=None):
        """src: load_set() van een Hoenn-secondary (mid >= 512) of primary (mid < 512 → General-tegels zijn al
        dezelfde). palmap: {bronpalet: eigen palet}. tilemap: optionele functie (idx-array, bronpalet) -> idx-array."""
        n0 = len(self.st)
        ents_src = src['mts'][mid - 512] if mid >= 512 else src['mts'][mid]
        attr = int(src['attrs'][mid - 512] if mid >= 512 else src['attrs'][mid])
        ents = []
        for e in ents_src:
            e = int(e)
            t, hf, vf, p = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
            np_ = palmap.get(p, p)
            if t < 512 and (tilemap is None):
                ents.append((e & 0x0FFF) | (np_ << 12) if t else 0)
                continue
            idx = (self.pt[t] if t < 512 else src['tiles'][t - 512]).copy()
            if tilemap is not None:
                idx = tilemap(idx, p)
            idx = idx[:, ::-1] if hf else idx
            idx = idx[::-1, :] if vf else idx
            ents.append(self.tile_ref(idx, np_, target) if t else 0)
        m = self.add_mt(name, ents, attr, target, slot)
        self.cost[name] = len(self.st) - n0
        return m

    def import_region(self, src, mapname, x0, y0, x1, y1, palmap, prefix, keep_primary=True):
        """Neem een stuk van een echte Hoenn-kaart over: secondary-metatiles worden gekopieerd, primary-metatiles
        blijven verwijzingen (de Andes-primary heeft dezelfde nummers). Geeft het raster met eigen id's."""
        d = json.load(open(f'data/maps/{mapname}/map.json'))
        L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == d['layout']][0]
        w = L['width']
        v = struct.unpack(f'<{w * L["height"]}H', open(L['blockdata_filepath'], 'rb').read())
        grid = []
        for y in range(y0, y1):
            row = []
            for x in range(x0, x1):
                m = v[y * w + x] & 0x3FF
                if m < 512 and keep_primary:
                    row.append(m)
                    continue
                nm = f'{prefix}_{m:03x}'
                if nm not in self.names:
                    self.import_mt(src, m, palmap, nm)
                row.append(self.names[nm])
            grid.append(row)
        return grid

    # ---------------------------------------------------------------- zelf tekenen
    def quant(self, cv, pal, x0, y0):
        lut = {c: i for i, c in enumerate(self.pals[pal]) if i}
        idx = np.zeros((8, 8), np.uint8)
        miss = 0
        for y in range(8):
            for x in range(8):
                a = cv.a[y0 + y, x0 + x]
                if a[3]:
                    c = (int(a[0]), int(a[1]), int(a[2]))
                    if c not in lut:
                        miss += 1
                        lut[c] = min(range(1, 16), key=lambda i: sum((p - q) ** 2 for p, q in zip(c, self.pals[pal][i])))
                    idx[y, x] = lut[c]
        return idx, miss

    def best_pal(self, cv, x0, y0, pals):
        cols = {tuple(int(v) for v in cv.a[y0 + y, x0 + x, :3]) for y in range(8) for x in range(8) if cv.a[y0 + y, x0 + x, 3]}
        return max(pals, key=lambda p: (len(cols & set(self.pals[p][1:])), -p))

    def add_drawn(self, name, bottom, top=None, pals=(6,), beh='MB_NORMAL', layer='covered', target='S', slot=None,
                  bottom_ents=None):
        """bottom/top: Canvas 16x16. pals: toegestane paletten (per 8x8 het best passende).
        bottom_ents: bestaande onderlaag-entries (bijv. van een grondmetatile) in plaats van bottom."""
        n0 = len(self.st)
        ents = []
        for li, lay in enumerate((bottom, top)):
            if li == 0 and bottom_ents is not None:
                ents += list(bottom_ents)
                continue
            for k in range(4):
                ox, oy = (k % 2) * 8, (k // 2) * 8
                if lay is None or not lay.a[oy:oy + 8, ox:ox + 8, 3].any():
                    ents.append(0)
                    continue
                p = self.best_pal(lay, ox, oy, pals)
                idx, _ = self.quant(lay, p, ox, oy)
                ents.append(self.tile_ref(idx, p, target))
        m = self.add_mt(name, ents, BEH[beh] | (LAYER[layer] << 12), target, slot)
        self.cost[name] = len(self.st) - n0
        return m

    def ents(self, m):
        return self.pm[m] if m < 512 else self.sm[m - 512]

    # ---------------------------------------------------------------- renderen
    def tile(self, t):
        return self.pt[t] if t < 512 else (self.st[t - 512] if t - 512 < len(self.st) else np.zeros((8, 8), np.uint8))

    def render_mt(self, m):
        img = np.zeros((16, 16, 3), np.uint8)
        ents = self.ents(m)
        for layer in range(2):
            for k in range(4):
                e = ents[layer * 4 + k]
                t, hf, vf, p = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
                tp = self.tile(t)
                tp = tp[:, ::-1] if hf else tp
                tp = tp[::-1, :] if vf else tp
                pal = np.array(self.pals[p], np.uint8)
                blk = img[(k // 2) * 8:(k // 2) * 8 + 8, (k % 2) * 8:(k % 2) * 8 + 8]
                mask = tp != 0 if layer else np.ones_like(tp, bool)
                blk[mask] = pal[tp][mask]
        return img

    def render(self, grid):
        h, w = len(grid), len(grid[0])
        img = np.zeros((h * 16, w * 16, 3), np.uint8)
        for y in range(h):
            for x in range(w):
                img[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = self.render_mt(grid[y][x])
        return img

    # ---------------------------------------------------------------- uitvoer
    def _write_pals(self, out, rng):
        os.makedirs(out + '/palettes', exist_ok=True)
        for p in rng:
            with open(f'{out}/palettes/{p:02}.pal', 'w') as f:
                f.write('JASC-PAL\r\n0100\r\n16\r\n' + ''.join(f'{r} {g} {b}\r\n' for r, g, b in map(snap, self.pals[p])))

    @staticmethod
    def _tiles_png(tiles, pal, path):
        n = len(tiles)
        rows = (n + 15) // 16
        arr = np.zeros((rows * 8, 128), np.uint8)
        for i, t in enumerate(tiles):
            arr[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = t
        im = Image.fromarray(arr, 'P')
        flat = [v for c in pal for v in snap(c)]
        im.putpalette(flat + [0] * (768 - len(flat)))
        im.save(path)

    def write(self, out, which):
        os.makedirs(out, exist_ok=True)
        if which == 'P':
            self._tiles_png(self.pt, self.pals[0], out + '/tiles.png')
            self._write_pals(out, range(0, 6))
            mts, attrs = self.pm, self.pa
            names = self.pnames
        else:
            self._tiles_png(self.st, self.pals[6], out + '/tiles.png')
            self._write_pals(out, range(6, 13))
            mts, attrs = self.sm, self.sa
            names = {k: v for k, v in self.names.items() if v >= 512}
        with open(out + '/metatiles.bin', 'wb') as f:
            for e in mts:
                f.write(struct.pack('<8H', *e))
        with open(out + '/metatile_attributes.bin', 'wb') as f:
            for a in attrs:
                f.write(struct.pack('<H', a))
        json.dump({k: hex(v) for k, v in names.items()}, open(out + '/metatile_names.json', 'w'), indent=1)

    def sheet(self, ids, path, per_row=8, scale=2):
        rows = (len(ids) + per_row - 1) // per_row
        img = np.full((rows * 16, per_row * 16, 3), 40, np.uint8)
        for i, m in enumerate(ids):
            img[(i // per_row) * 16:(i // per_row) * 16 + 16, (i % per_row) * 16:(i % per_row) * 16 + 16] = self.render_mt(m)
        Image.fromarray(img).resize((per_row * 16 * scale, rows * 16 * scale), Image.NEAREST).save(path)

    def palette_strip(self, rng, path, scale=12):
        img = np.zeros((len(rng), 16, 3), np.uint8)
        for r, p in enumerate(rng):
            img[r] = [snap(c) for c in self.pals[p]]
        Image.fromarray(img).resize((16 * scale, len(rng) * scale), Image.NEAREST).save(path)


def comparison(images, labels, path, scale=1, gap=8):
    """Plaatjes naast elkaar (zelfde schaal) met een korte titelbalk."""
    from PIL import ImageDraw
    ims = [Image.fromarray(i).resize((i.shape[1] * scale, i.shape[0] * scale), Image.NEAREST) for i in images]
    h = max(i.height for i in ims) + 14
    w = sum(i.width for i in ims) + gap * (len(ims) - 1)
    out = Image.new('RGB', (w, h), (24, 24, 32))
    d = ImageDraw.Draw(out)
    x = 0
    for im, lb in zip(ims, labels):
        out.paste(im, (x, 14))
        d.text((x + 2, 1), lb, fill=(240, 240, 240))
        x += im.width + gap
    out.save(path)
