#!/usr/bin/env python3
"""Project Grounded: zet de sneeuw-tileset van CinnaYva (Pokémon Essentials-formaat, 2x vergroot)
om naar een GBA secondary tileset (data/tilesets/secondary/snow).

- Bron: graphics/grounded/snow_src/ (CustomTilesetSnow.png + Autotiles), credits: CinnaYva.
- Kiest per 8x8-blokje het best passende van 7 paletten (6..12), ontdubbelt tiles (ook gespiegeld)
  en schrijft tiles.png, palettes/*.pal, metatiles.bin, metatile_attributes.bin.
- Schrijft ook data/tilesets/secondary/snow/metatile_names.json (naam -> metatile-id) voor de kaartbouwers.

Gebruik: python3 tools/grounded/snow_tileset.py
"""
import json, os, struct
import numpy as np
from PIL import Image

SRC = 'graphics/grounded/snow_src'
OUT = 'data/tilesets/secondary/snow'
PAL_FIRST, NUM_PALS = 6, 7
MB = {'normal': 0x00, 'tall_grass': 0x02, 'ice': 0x20, 'door': 0x60, 'pond': 0x10}
LAYER_COVERED = 1

sheet = Image.open(f'{SRC}/CustomTilesetSnow.png').convert('RGBA')
sheet = sheet.resize((sheet.width // 2, sheet.height // 2), Image.NEAREST)


def load_auto(name):
    im = Image.open(f'{SRC}/Autotiles/{name}.png').convert('RGBA')
    return im.resize((im.width // 2, im.height // 2), Image.NEAREST)


def cell(c, r):
    return sheet.crop((c * 16, r * 16, c * 16 + 16, r * 16 + 16))


def over(*imgs):
    out = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for im in imgs:
        if im is not None:
            out.alpha_composite(im)
    return out


def auto_pieces(im):
    """RMXP-autotile (48x64 na verkleinen) -> 9 randstukken + 4 binnenhoeken + los stuk."""
    t = lambda c, r: im.crop((c * 16, r * 16, c * 16 + 16, r * 16 + 16))
    p = {}
    names = [['tl', 't', 'tr'], ['l', 'c', 'r'], ['bl', 'b', 'br']]
    for r in range(3):
        for c in range(3):
            p[names[r][c]] = t(c, r + 1)
    inner = t(2, 0)
    for key, (qx, qy) in {'in_tl': (0, 0), 'in_tr': (8, 0), 'in_bl': (0, 8), 'in_br': (8, 8)}.items():
        m = p['c'].copy()
        m.paste(inner.crop((qx, qy, qx + 8, qy + 8)), (qx, qy))
        p[key] = m
    p['single'] = t(0, 0)
    return p


G = cell(0, 23)                       # basis: besneeuwde grond (naadloos)
metatiles = []                        # (naam, onderlaag, bovenlaag, gedrag)


def add(name, bottom, top=None, beh='normal'):
    metatiles.append((name, bottom, top, MB[beh]))


# --- grond ---
add('snow', G)
add('snow_dots', cell(2, 23))
add('snow_light', cell(0, 28))
add('snow_deep', cell(7, 29))
add('snow_deep2', cell(6, 30))
add('ice_floor', cell(6, 56), beh='ice')
# --- gras en plukjes (loopbaar) ---
add('grass_snow', G, cell(7, 23), 'tall_grass')
add('grass_green', G, cell(7, 25), 'tall_grass')
for i, (c, r) in enumerate([(1, 23), (0, 24), (1, 24), (2, 24), (3, 24), (4, 24), (3, 25), (4, 25), (5, 25), (3, 23)]):
    add(f'tuft{i}', G, cell(c, r))
flowers = load_auto('FlowersSnow')
add('flowers_blue', G, flowers.crop((0, 0, 16, 16)))
flowers1 = load_auto('FlowersSnow1')
add('flowers_pink', G, flowers1.crop((0, 0, 16, 16)))
# --- paden (autotiles) ---
for key, fname in [('path_stone', 'SnowPath'), ('path_pink', 'SnowPath2'), ('deep', 'SnowPath23')]:
    pieces = auto_pieces(load_auto(fname))
    for pn in ['tl', 't', 'tr', 'l', 'c', 'r', 'bl', 'b', 'br', 'in_tl', 'in_tr', 'in_bl', 'in_br']:
        add(f'{key}_{pn}', over(G, pieces[pn]))
# --- hoogvlakte / kliffen (sneeuw bovenop, bruine rand, voorkant) ---
for (c, r), n in {(0, 0): 'cliff_tl', (1, 0): 'cliff_t', (2, 0): 'cliff_tr',
                  (0, 1): 'cliff_l', (1, 1): 'cliff_c', (2, 1): 'cliff_r',
                  (0, 2): 'cliff_bl', (1, 2): 'cliff_b', (2, 2): 'cliff_br',
                  (3, 0): 'cliff_in_a', (4, 0): 'cliff_in_b', (5, 0): 'cliff_in_c',
                  (3, 1): 'cliff_in_d', (4, 1): 'cliff_in_e', (5, 1): 'cliff_in_f',
                  (3, 2): 'cliff_front_a', (4, 2): 'cliff_front_b', (5, 2): 'cliff_front_c',
                  (3, 3): 'cave_l', (5, 3): 'cave_r',
                  (0, 12): 'cliff2_tl', (1, 12): 'cliff2_t', (2, 12): 'cliff2_tr',
                  (0, 13): 'cliff2_l', (1, 13): 'cliff2_c', (2, 13): 'cliff2_r',
                  (6, 0): 'rockcap_l', (7, 0): 'rockcap_r', (6, 1): 'rockcap_bl', (7, 1): 'rockcap_br',
                  (6, 2): 'cliff_front_d', (7, 2): 'cliff_front_fall'}.items():
    add(n, over(G, cell(c, r)))
add('cave_door', over(G, cell(4, 3)), beh='door')
# --- bergtop (2x2) en grote kei (2x2) ---
for dy in range(2):
    for dx in range(2):
        add(f'peak_{dx}{dy}', over(G, cell(dx, 14 + dy)))
        add(f'boulder_{dx}{dy}', over(G, cell(dx, 10 + dy)))
# --- bomen ---
for dy in range(3):
    for dx in range(2):
        add(f'pine_{dx}{dy}', G, cell(4 + dx, 31 + dy))       # besneeuwde den 2x3
        add(f'pinegreen_{dx}{dy}', G, cell(0 + dx, 31 + dy))  # groene den 2x3
for dy in range(3):
    add(f'thinpine_{dy}', G, cell(6, 37 + dy))                # smalle den 1x3
# --- rotsen en decor (1x1, blokkerend) ---
for n, (c, r) in {'rock_snow': (5, 6), 'rock_snow2': (7, 6), 'rock_cluster': (5, 7), 'rock_snow3': (6, 7),
                  'rock_snow4': (7, 7), 'ice_rock': (5, 18), 'ice_rock2': (7, 18), 'ice_chunks': (5, 19),
                  'ice_crystal': (6, 19), 'ice_crystal2': (7, 19), 'snowball': (6, 20), 'snowball2': (7, 20),
                  'snowman': (3, 22), 'bunny_statue': (4, 22), 'log': (3, 37), 'bush_snow': (3, 38),
                  'stump': (3, 39)}.items():
    add(n, G, cell(c, r))

# --- oevers: bewegend vijverwater (primary tile 0x11e, palet 1) met een sneeuwrand erover ---
WATER = ('prim', [0x111e] * 4)
_edge = np.array(G, dtype=np.int32)
_rim = np.array([96, 80, 104, 255])               # oeverrand (donker steen)
_rim_hi = np.array([168, 184, 208, 255])          # lichte rand op de sneeuw
_shadow = np.array([80, 136, 208, 255])           # schaduw op het water


def shore(n, s_, w, e, nw=False, ne=False, sw=False, se=False, depth=5):
    out = np.zeros((16, 16, 4), dtype=np.int32)
    for y in range(16):
        for x in range(16):
            snow = (n and y < depth) or (s_ and y >= 16 - depth) or (w and x < depth) or (e and x >= 16 - depth)
            r = depth + 1
            if nw and (x - 0) ** 2 + (y - 0) ** 2 < r * r: snow = True
            if ne and (x - 15) ** 2 + (y - 0) ** 2 < r * r: snow = True
            if sw and (x - 0) ** 2 + (y - 15) ** 2 < r * r: snow = True
            if se and (x - 15) ** 2 + (y - 15) ** 2 < r * r: snow = True
            # buitenhoeken rond maken
            R = 9
            for cn, cw, sx, sy in ((n, w, -1, -1), (n, e, 1, -1), (s_, w, -1, 1), (s_, e, 1, 1)):
                if cn and cw:
                    cx = depth + R if sx < 0 else 15 - depth - R
                    cy = depth + R if sy < 0 else 15 - depth - R
                    if (x - cx) * sx > 0 and (y - cy) * sy > 0 and (x - cx) ** 2 + (y - cy) ** 2 > R * R:
                        snow = True
            if snow:
                out[y, x] = _edge[y, x]
    # oever: donkere steenrand direct langs de sneeuw, daaronder een schaduwband op het water
    m = out[..., 3] > 0
    dist = np.full((16, 16), 99)
    for y in range(16):
        for x in range(16):
            if m[y, x]:
                continue
            for yy in range(16):
                for xx in range(16):
                    if m[yy, xx]:
                        dist[y, x] = min(dist[y, x], max(abs(yy - y), abs(xx - x)))
    for y in range(16):
        for x in range(16):
            if m[y, x] and any(0 <= y + dy < 16 and 0 <= x + dx < 16 and not m[y + dy, x + dx]
                               for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y, x] = _rim_hi
            elif dist[y, x] <= 2:
                out[y, x] = _rim
            elif dist[y, x] <= 4:
                out[y, x] = _shadow
    return Image.fromarray(out.astype(np.uint8), 'RGBA')


add('water', WATER, None, 'pond')
for n_ in (0, 1):
    for s_ in (0, 1):
        for w_ in (0, 1):
            for e_ in (0, 1):
                if n_ + s_ + w_ + e_ == 0 or (n_ and s_) or (w_ and e_):
                    continue
                add(f'shore_{"n" if n_ else ""}{"s" if s_ else ""}{"w" if w_ else ""}{"e" if e_ else ""}',
                    WATER, shore(n_, s_, w_, e_), 'pond')
for corner in ('nw', 'ne', 'sw', 'se'):
    add(f'shore_in_{corner}', WATER, shore(0, 0, 0, 0, **{corner: True}), 'pond')
# --- houten trap (tegen een klif op) ---
add('stairs', over(G, cell(3, 4)))

# --- besneeuwde Hoenn-randbomen: de bosbomen uit de General-tileset (0x1CE-0x1EF), groen -> sneeuw ---
def _general_tree_layers():
    gp = 'data/tilesets/primary/general/'
    gtiles = open(gp + 'tiles.4bpp', 'rb').read()
    gmt = open(gp + 'metatiles.bin', 'rb').read()
    gpal = [tuple(map(int, l.split())) for l in open(gp + 'palettes/02.pal').read().split('\n')[3:19]]
    recolor = {1: (240, 248, 255), 2: (192, 212, 236), 3: (56, 120, 104), 4: (32, 72, 72),
               15: (126, 148, 196)}          # 12/13/14 = gras -> doorzichtig
    def tile_img(e):
        t, hf, vf, pn = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
        img = Image.new('RGBA', (8, 8), (0, 0, 0, 0))
        if pn != 2:
            return img
        b = gtiles[t * 32:(t + 1) * 32]
        for y in range(8):
            for x in range(8):
                c = (b[y * 4 + x // 2] >> (4 * (x & 1))) & 15
                if c in recolor:
                    img.putpixel((x, y), recolor[c] + (255,))
                elif c not in (0, 12, 13, 14):
                    img.putpixel((x, y), gpal[c] + (255,))
        if hf: img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if vf: img = img.transpose(Image.FLIP_TOP_BOTTOM)
        return img
    def layer(ents):
        out = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        for k, e in enumerate(ents):
            out.alpha_composite(tile_img(e), ((k % 2) * 8, (k // 2) * 8))
        return out
    res = {}
    for mid in list(range(0x1CE, 0x1D0)) + list(range(0x1D4, 0x1D8)) + list(range(0x1DC, 0x1E0)) + \
            list(range(0x1E4, 0x1E8)) + list(range(0x1EC, 0x1F0)):
        e = struct.unpack_from('<8H', gmt, mid * 16)
        res[mid] = (layer(e[:4]), layer(e[4:]))
    return res
for _mid, (_bot, _top) in _general_tree_layers().items():
    add(f'htree_{_mid:03x}', over(G, _bot), _top if _top.getbbox() else None)
# --- klein blauw huisje (4x4, dak begint halverwege rij 107), deur op (1,3) ---
for dy in range(4):
    for dx in range(4):
        add(f'house_blue_{dx}{dy}', over(G, cell(dx, 107 + dy)), beh='door' if (dx, dy) == (1, 3) else 'normal')
# --- U-vormige oevers (smalle inham van 1 tile breed/hoog) ---
for _n, _s, _w, _e in ((0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 1, 0), (1, 1, 0, 1)):
    add(f'shore_{"n" if _n else ""}{"s" if _s else ""}{"w" if _w else ""}{"e" if _e else ""}', WATER, shore(_n, _s, _w, _e), 'pond')

# ---------------------------------------------------------------- kleuren en paletten
def to5(a):
    a = a.copy()
    a[..., :3] = (a[..., :3] // 8) * 8
    return a


blocks = []   # alle 8x8-blokjes (RGBA)
for _, bottom, top, _ in metatiles:
    for layer in (bottom, top):
        if layer is None or isinstance(layer, tuple):
            continue
        a = to5(np.array(layer, dtype=np.int32))
        for qy in (0, 8):
            for qx in (0, 8):
                blocks.append(a[qy:qy + 8, qx:qx + 8])


def colors_of(b):
    m = b[..., 3] > 127
    return b[..., :3][m].reshape(-1, 3)


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


# tiles clusteren naar 7 paletten (k-means op gemiddelde kleur), daarna iteratief verfijnen
feat = []
opaque_blocks = [b for b in blocks if (b[..., 3] > 127).any()]
for b in opaque_blocks:
    c = colors_of(b)
    feat.append(np.concatenate([c.mean(0), c.std(0)]))
feat = np.array(feat)
assign = ((feat[:, None, :] - kmeans(feat, NUM_PALS)[None]) ** 2).sum(2).argmin(1)
for it in range(6):
    pals = []
    for j in range(NUM_PALS):
        pts = np.concatenate([colors_of(b) for b, a in zip(opaque_blocks, assign) if a == j] or [np.zeros((1, 3))])
        pals.append(np.round(kmeans(pts.astype(float), 15, seed=it) / 8) * 8)
    errs = []
    for b in opaque_blocks:
        c = colors_of(b).astype(float)
        errs.append([((c[:, None, :] - p[None]) ** 2).sum(2).min(1).sum() for p in pals])
    assign = np.array(errs).argmin(1)
pals = [np.clip(p, 0, 248) for p in pals]


def quantize(b):
    """8x8 RGBA -> (paletindex, 8x8 indices)"""
    c = b[..., :3].reshape(-1, 3).astype(float)
    m = (b[..., 3] > 127).reshape(-1)
    if not m.any():
        return None
    best = None
    for j, p in enumerate(pals):
        d = ((c[:, None, :] - p[None]) ** 2).sum(2)
        idx = d.argmin(1)
        err = d.min(1)[m].sum()
        if best is None or err < best[0]:
            best = (err, j, idx)
    _, j, idx = best
    idx = np.where(m, idx + 1, 0).reshape(8, 8)
    return j, idx


tiles = []            # lijst van 8x8 index-arrays
tile_lookup = {}      # bytes -> (tile, hflip, vflip)


def tile_ref(b):
    q = quantize(b)
    if q is None:
        return None
    j, idx = q
    for hf in (0, 1):
        for vf in (0, 1):
            v = idx[:, ::-1] if hf else idx
            v = v[::-1, :] if vf else v
            key = v.astype(np.uint8).tobytes()
            if key in tile_lookup:
                return tile_lookup[key][0], hf, vf, j
    tiles.append(idx)
    tile_lookup[idx.astype(np.uint8).tobytes()] = (len(tiles) - 1,)
    return len(tiles) - 1, 0, 0, j


metatile_data = bytearray()
attr_data = bytearray()
names = {}
for n, (name, bottom, top, beh) in enumerate(metatiles):
    entries = []
    for layer in (bottom, top):
        if isinstance(layer, tuple):
            entries += layer[1]
            continue
        a = to5(np.array(layer, dtype=np.int32)) if layer is not None else None
        for qy in (0, 8):
            for qx in (0, 8):
                ref = tile_ref(a[qy:qy + 8, qx:qx + 8]) if a is not None else None
                if ref is None:
                    entries.append(0)
                else:
                    t, hf, vf, j = ref
                    entries.append((512 + t) | (hf << 10) | (vf << 11) | ((PAL_FIRST + j) << 12))
    metatile_data += struct.pack('<8H', *entries)
    attr_data += struct.pack('<H', beh | (LAYER_COVERED << 12))
    names[name] = 512 + n

assert len(tiles) <= 512, f'te veel tiles: {len(tiles)}'
assert len(metatiles) <= 512

os.makedirs(f'{OUT}/palettes', exist_ok=True)
cols = 16
rows = (len(tiles) + cols - 1) // cols
img = Image.new('P', (cols * 8, rows * 8), 0)
for i, t in enumerate(tiles):
    img.paste(Image.fromarray(t.astype(np.uint8), 'P'), ((i % cols) * 8, (i // cols) * 8))
grey = []
for i in range(16):
    grey += [i * 16, i * 16, i * 16]
img.putpalette(grey + [0] * (768 - 48))
img.save(f'{OUT}/tiles.png')
for i in range(16):
    j = i - PAL_FIRST
    colors = [(0, 0, 0)] * 16
    if 0 <= j < NUM_PALS:
        colors = [(255, 0, 255)] + [tuple(int(v) for v in c) for c in pals[j]]
        colors += [(0, 0, 0)] * (16 - len(colors))
    with open(f'{OUT}/palettes/{i:02}.pal', 'w') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in colors))
open(f'{OUT}/metatiles.bin', 'wb').write(metatile_data)
open(f'{OUT}/metatile_attributes.bin', 'wb').write(attr_data)
json.dump(names, open(f'{OUT}/metatile_names.json', 'w'), indent=1)
print(f'{len(metatiles)} metatiles, {len(tiles)} tiles, {NUM_PALS} paletten')
