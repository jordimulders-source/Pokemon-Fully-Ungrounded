"""Project Grounded: tilesets van de Spacetime Cave en de Kanto-locaties erachter (deel 1).

FRLG-kaarten worden 1-op-1 overgenomen (zelfde metatile-raster, botsing en hoogte), maar met een eigen secondary
die per FRLG-metatile een nieuwe tegel maakt ("reskin"): de vorm blijft, de aankleding wordt Emerald/Ekat.
  pokemon_tower  FRLG-torentiles; vloer = Ekat's "Pokemon Tower Interior (Revamp)"-vloer (schaduwen worden
                 overgenomen), graven op de vloer = Revamp-graven (16x32, kop steekt in de tegel erboven,
                 willekeurig: gewoon/hart/bal/bloemen/kaarsen/krans), paars -> Revamp-grijs.
  cerulean_cave  FRLG-grot; vloer = Emerald-grotvloer (Cave 0x201), groene heuvels -> Emerald-rotskleuren,
                 losse keien = Emerald-keien, water/ladders blijven (bijgekleurd).
  lavender_town  Emerald-huizen (Petalburg, paars dak), de FRLG-toren (gras eromheen = Emerald-gras), PC-/Mart-
                 dakhoekjes en een scheur; grond, bomen, PC en Mart komen uit General.
  spacetime_cave Kopie van de Cave-tileset met de scheuren achteraan (palet 12) + violet getinte paletten;
                 primary spacetime_general = General met getinte paletten (BASE).
Gedrag: FRLG-gedrag op naam vertaald naar Emerald; FRLG-encountervlag (land) -> MB_CAVE / MB_INDOOR_ENCOUNTER.
De FRLG-bestanden worden gedownload naar build/frlg_cache (pret/pokefirered).
Gebruik: python3 tools/grounded/maptools/spacetime_tiles.py   (daarna make voor de tiles.4bpp)"""
import json, os, re, struct, sys, urllib.request, random, colorsys
import numpy as np
from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

src = open('tools/grounded/snow_tileset.py').read()
_ns = {'np': np, 'Image': Image, 'struct': struct, 'os': os, 'LAYER_COVERED': 1}
exec(src[src.index('def to5('):src.rindex('\nif TOWN:')], _ns)
emit = _ns['emit']

FRLG = 'https://raw.githubusercontent.com/pret/pokefirered/master/'
CACHE = 'build/frlg_cache'
EKAT = 'graphics/grounded/tilesets/ekat/pokemon_tower_interior_revamp.png'


def frlg(path):
    dst = os.path.join(CACHE, path)
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(urllib.request.urlopen(FRLG + path).read())
    return dst


# ====================================================================== FRLG lezen
NP = 640
COL = 0x400


def jasc(path):
    L = open(path).read().replace('\r', '').split('\n')[3:19]
    return [tuple(int(v) for v in l.split()) for l in L]


class FTS:
    def __init__(s, name):
        d = 'data/tilesets/' + name
        s.idx = np.array(Image.open(frlg(d + '/tiles.png')))
        s.w = s.idx.shape[1] // 8
        b = open(frlg(d + '/metatiles.bin'), 'rb').read()
        s.mt = struct.unpack('<%dH' % (len(b) // 2), b)
        b = open(frlg(d + '/metatile_attributes.bin'), 'rb').read()
        s.attr = struct.unpack('<%dI' % (len(b) // 4), b)
        s.pals = [jasc(frlg(d + '/palettes/%02d.pal' % i)) for i in range(16)]

    def tile(s, n):
        y, x = divmod(n, s.w)
        return s.idx[y * 8:y * 8 + 8, x * 8:x * 8 + 8]


class FPair:
    def __init__(s, prim, sec):
        s.p, s.s = FTS(prim), FTS(sec)

    def mtdata(s, m):
        if m < NP:
            return s.p.mt[m * 8:m * 8 + 8], s.p.attr[m]
        return s.s.mt[(m - NP) * 8:(m - NP) * 8 + 8], s.s.attr[m - NP]

    def layer_img(s, m, layer, opaque):
        ent, _ = s.mtdata(m)
        img = np.zeros((16, 16, 4), np.int32)
        for q in range(4):
            e = ent[layer * 4 + q]
            t = e & 0x3FF
            til = s.p.tile(t) if t < NP else s.s.tile(t - NP)
            if e & 0x400: til = til[:, ::-1]
            if e & 0x800: til = til[::-1]
            pn = (e >> 12) & 15
            P = s.p.pals[pn] if pn < 7 else s.s.pals[pn]
            oy, ox = (q // 2) * 8, (q % 2) * 8
            for yy in range(8):
                for xx in range(8):
                    c = til[yy, xx]
                    if c or opaque:
                        img[oy + yy, ox + xx, :3] = P[c] if c else s.p.pals[0][0]
                        img[oy + yy, ox + xx, 3] = 255
        return img

    def attr(s, m):
        a = s.mtdata(m)[1]
        return a & 0x1FF, (a >> 24) & 7, (a >> 29) & 3


def frlg_layout(name):
    L = [l for l in json.load(open(frlg('data/layouts/layouts.json')))['layouts'] if l.get('name') == name + '_Layout'][0]
    W, H = L['width'], L['height']
    b = open(frlg('data/layouts/%s/map.bin' % name), 'rb').read()
    return W, H, list(struct.unpack('<%dH' % (W * H), b))


def frlg_map(name):
    return json.load(open(frlg('data/maps/%s/map.json' % name)))


# ====================================================================== gedrag vertalen
def _enum(path):
    out = {}
    for l in open(path):
        m = re.match(r'\s*(MB_\w+)', l)
        if m and m.group(1) not in out:
            out[m.group(1)] = len(out)
    return out


EM = _enum('include/constants/metatile_behaviors.h')
FR = {}
for l in open(frlg('include/constants/metatile_behaviors.h')):
    m = re.match(r'#define (MB_\w+)\s+(0x[0-9A-Fa-f]+|\d+)', l)
    if m:
        FR[int(m.group(2), 0)] = m.group(1)
FR_RENAME = {'MB_CAVE_DOOR': 'MB_NON_ANIMATED_DOOR', 'MB_REGULAR_WARP': 'MB_AQUA_HIDEOUT_WARP',
             'MB_FALL_WARP': 'MB_MT_PYRE_HOLE'}


def em_beh(fbeh, enc, land_beh):
    n = FR.get(fbeh, 'MB_NORMAL')
    n = FR_RENAME.get(n, n)
    v = EM.get(n, 0)
    if v == 0 and enc == 1:
        v = EM[land_beh]
    return v


# ====================================================================== kleurhulpjes
def lum(c):
    return 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]


def hsv(c):
    return colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)


def cells(path):
    a = np.array(Image.open(path).convert('RGBA')).astype(np.int32)
    return lambda c, r: a[r * 16:r * 16 + 16, c * 16:c * 16 + 16].copy()


def over(base, top):
    out = base.copy()
    m = top[..., 3] > 127
    out[m] = top[m]
    out[..., 3] = np.maximum(base[..., 3], np.where(m, 255, 0))
    return out


def img(a):
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


def em_render(prim, sec, m, layer=None):
    """RGBA 16x16 van een Emerald-metatile (layer None = beide lagen samen)."""
    import gridrender
    pt, pm, ppal = gridrender.load2(gridrender.R + 'data/tilesets/primary/' + prim)
    st, sm, spal = gridrender.load2(gridrender.R + 'data/tilesets/secondary/' + sec)
    pal = ppal[:6] + spal[6:13]
    src_, mi = (pm, m) if m < 512 else (sm, m - 512)
    ent = struct.unpack_from('<8H', src_, mi * 16)
    out = np.zeros((16, 16, 4), np.int32)
    for L in ((0, 1) if layer is None else (layer,)):
        for k in range(4):
            e = ent[L * 4 + k]; t = e & 0x3FF; hf = (e >> 10) & 1; vf = (e >> 11) & 1; pn = (e >> 12) & 15
            data, i = (pt, t) if t < 512 else (st, t - 512)
            b = data[i * 32:(i + 1) * 32]
            for y in range(8):
                for x in range(8):
                    sy, sx = (7 - y if vf else y), (7 - x if hf else x)
                    c = (b[sy * 4 + sx // 2] >> (4 * (sx & 1))) & 15 if len(b) == 32 else 0
                    if c == 0 and (L == 1 or layer is not None):
                        continue
                    oy, ox = (k // 2) * 8 + y, (k % 2) * 8 + x
                    out[oy, ox, :3] = pal[pn][c] if pn < len(pal) else (255, 0, 255)
                    out[oy, ox, 3] = 255
    return out


def patch_attrs(OUT, attrs):
    """attrs: lijst (gedrag, laagtype) in metatile-volgorde; overschrijft wat emit() schreef."""
    open(OUT + '/metatile_attributes.bin', 'wb').write(b''.join(struct.pack('<H', b | (l << 12)) for b, l in attrs))


# ====================================================================== de scheur (2x2 metatiles)
def rift_art(unstable=False, seed=7):
    """32x32 RGBA: gerafelde scheur in ruimte-tijd (donkere kern, violette spiraal, cyaan glinsters)."""
    rnd = random.Random(seed)
    a = np.zeros((32, 32, 4), np.int32)
    cx = cy = 15.5
    for y in range(32):
        for x in range(32):
            dx, dy = (x - cx) / 1.0, (y - cy) / 1.25
            r = (dx * dx + dy * dy) ** 0.5
            th = np.arctan2(dy, dx)
            R = 12.5 * (1 + 0.16 * np.sin(5 * th + 0.7) + 0.08 * np.sin(11 * th + 2.1))
            t = r / R
            if t > 1.0:
                continue
            band = (np.sin(th * 2 + r * 0.75) + 1) / 2
            if t > 0.86:
                col = (40, 16, 72) if not unstable else (52, 52, 64)
            elif t < 0.30:
                col = (8, 4, 20)
            else:
                k = (t - 0.3) / 0.56
                if unstable:
                    g = int(30 + 60 * k + 40 * band)
                    col = (g, g, g + 18)
                else:
                    col = (int(40 + 120 * band * k), int(14 + 30 * k), int(70 + 130 * k * (0.6 + 0.4 * band)))
            a[y, x, :3] = col
            a[y, x, 3] = 255
    for _ in range(14 if not unstable else 6):
        ang = rnd.random() * 6.283; rr = rnd.random() * 9
        x, y = int(cx + rr * np.cos(ang)), int(cy + rr * np.sin(ang) * 1.25)
        if a[y, x, 3]:
            a[y, x, :3] = (120, 248, 248) if not unstable else (150, 150, 170)
    return a


def rift_quads(art):
    return [art[qy * 16:qy * 16 + 16, qx * 16:qx * 16 + 16] for qy in (0, 1) for qx in (0, 1)]


MB_RIFT = 'MB_AQUA_HIDEOUT_WARP'   # teleporttegel-effect (DoTeleportTileWarp)


# ====================================================================== 1. Pokemon Tower (FRLG + Revamp)
TOWER_FLOORS = ['PokemonTower_1F', 'PokemonTower_2F', 'PokemonTower_3F', 'PokemonTower_4F', 'PokemonTower_7F']
GRAVES = {0x289, 0x291, 0x293, 0x2d8, 0x2d9, 0x2dc, 0x2dd, 0x2e3, 0x2e4}
GRAVE_TYPES = [(0, 3), (1, 3), (2, 3)] * 4 + [(3, 3), (4, 3)] * 2 + \
              [(0, 7), (4, 7), (1, 9), (3, 9), (2, 11)]      # (kolom, koprij); lijf = rij+1


def grave_type(x, y, floor_i):
    return GRAVE_TYPES[random.Random(x * 131 + y * 17 + floor_i * 1009).randrange(len(GRAVE_TYPES))]


def tower_tileset():
    fp = FPair('primary/building', 'secondary/pokemon_tower')
    ek = cells(EKAT)
    rv_floor = ek(1, 2)
    f282 = fp.layer_img(0x282, 0, True)
    floor_cols = {tuple(c[:3]) for c in f282.reshape(-1, 4)}
    f284 = fp.layer_img(0x284, 0, True)
    shade = {tuple(f284[y, x, :3]) for y in range(16) for x in range(16)} - floor_cols

    def recolor(a, keep_floor=False):
        out = a.copy()
        for y in range(16):
            for x in range(16):
                if out[y, x, 3] == 0:
                    continue
                c = tuple(out[y, x, :3])
                if c in floor_cols and not keep_floor:
                    out[y, x, :3] = rv_floor[y, x, :3]
                elif c in shade and not keep_floor:
                    out[y, x, :3] = rv_floor[y, x, :3] * 0.70
                else:
                    h, s_, v = hsv(c)
                    if s_ > 0.12 and 0.62 < h < 0.86:              # paars -> Revamp-grijs (licht groenig)
                        L = lum(c) * 1.08
                        out[y, x, :3] = (L * 0.96, L * 1.0, L * 0.94)
        return out

    def base_imgs(m):
        b = recolor(fp.layer_img(m, 0, True))
        t = recolor(fp.layer_img(m, 1, False))
        return b, t

    keys = []           # (frlg-id, soort, koptype-van-onder, laagtype-override)
    grids = {}
    for fi, name in enumerate(TOWER_FLOORS):
        W, H, v = frlg_layout(name)
        g = []
        for y in range(H):
            row = []
            for x in range(W):
                m = v[y * W + x] & 0x3FF
                body = grave_type(x, y, fi) if m in GRAVES else None
                below = v[(y + 1) * W + x] & 0x3FF if y + 1 < H else None
                head = grave_type(x, y + 1, fi) if below in GRAVES else None
                k = (m, body, head)
                if k not in keys:
                    keys.append(k)
                row.append(k)
            g.append(row)
        grids[name] = (W, H, v, g)
    mts, attrs = [], []
    for (m, body, head) in keys:
        fbeh, enc, layer = fp.attr(m)
        beh = em_beh(fbeh, enc, 'MB_INDOOR_ENCOUNTER')
        if body is not None:
            bot = over(rv_floor, ek(body[0], body[1] + 1)); top = None
            beh = 0
        else:
            bot, top = base_imgs(m)
        if head is not None:
            h = ek(head[0], head[1])
            top = h if top is None else over(top, h)
            layer = 0       # kop over de speler
        if top is not None and not (top[..., 3] > 0).any():
            top = None
        mts.append(((m, body, head), img(bot), img(top) if top is not None else None, beh))
        attrs.append((beh, layer))
    OUT = 'data/tilesets/secondary/pokemon_tower'
    res = emit(mts, OUT, 512, 6, 7)
    patch_attrs(OUT, attrs)
    out = {}
    for name, (W, H, v, g) in grids.items():
        out[name] = (W, H, [(res['names'][g[i // W][i % W]]) | (v[i] & 0xFC00) for i in range(W * H)])
    return out


# ====================================================================== 2. Cerulean Cave (FRLG + Emerald Cave)
CAVE_FLOORS = ['CeruleanCave_1F', 'CeruleanCave_2F', 'CeruleanCave_B1F']
BOULDERS = {0x282: 0x202, 0x283: 0x203}
RIFT_CAVE = (8, 21)        # wordt door spacetime_cave.py gebruikt: plek van de terugscheur in 1F (linksboven)


def cave_tileset(rift_at):
    fp = FPair('primary/general', 'secondary/cerulean_cave')
    em_floor = em_render('general', 'cave', 0x201)
    f281 = fp.layer_img(0x281, 0, True)
    floor_cols = {tuple(c[:3]) for c in f281.reshape(-1, 4)}
    floor_L = np.mean([lum(c) for c in floor_cols])
    # Emerald-rotskleuren (oplopend in helderheid) uit de massieve rots en de wand
    rock = []
    for m in (0x211, 0x219, 0x212, 0x210, 0x221):
        a = em_render('general', 'cave', m)
        rock += [tuple(c[:3]) for c in a.reshape(-1, 4) if c[3]]
    rock = sorted(set(rock), key=lum)
    rock = rock[:max(2, int(len(rock) * 0.8))]          # alleen het donkere deel: heuvels donkerder dan de vloer
    em_rock = em_render('general', 'cave', 0x211)
    fill = {tuple(c[:3]) for c in fp.layer_img(0x291, 0, True).reshape(-1, 4)}
    greens = set()
    for m in range(NP, NP + len(fp.s.attr)):
        for L in (0, 1):
            a = fp.layer_img(m, L, L == 0)
            for c in a.reshape(-1, 4):
                if c[3]:
                    h, s_, v_ = hsv(tuple(c[:3]))
                    if 0.17 < h < 0.48 and s_ > 0.15:
                        greens.add(tuple(c[:3]))
    gl = sorted(lum(c) for c in greens)
    g0, g1 = gl[0], gl[-1]

    def recolor(a):
        out = a.copy()
        for y in range(16):
            for x in range(16):
                if out[y, x, 3] == 0:
                    continue
                c = tuple(out[y, x, :3])
                if c in floor_cols:
                    out[y, x, :3] = em_floor[y, x, :3]
                elif c in fill:
                    out[y, x, :3] = em_rock[y, x, :3] * 0.78
                elif c in greens:
                    t = (lum(c) - g0) / max(1, g1 - g0)
                    out[y, x, :3] = rock[min(len(rock) - 1, int(t * (len(rock) - 1) + 0.5))]
                else:
                    h, s_, v_ = hsv(c)
                    if s_ < 0.12:              # grijze vloerschaduw -> donkerder Emerald-vloer
                        out[y, x, :3] = em_floor[y, x, :3] * min(1.1, lum(c) / floor_L)
        return out

    rq = rift_quads(rift_art())
    keys, grids = [], {}
    for name in CAVE_FLOORS:
        W, H, v = frlg_layout(name)
        g = []
        for y in range(H):
            row = []
            for x in range(W):
                m = v[y * W + x] & 0x3FF
                rk = None
                if name in rift_at:
                    rx, ry = rift_at[name]
                    if rx <= x <= rx + 1 and ry <= y <= ry + 1:
                        rk = (y - ry) * 2 + (x - rx)
                k = (m, rk)
                if k not in keys:
                    keys.append(k)
                row.append(k)
            g.append(row)
        grids[name] = (W, H, v, g)
    mts, attrs = [], []
    for (m, rk) in keys:
        fbeh, enc, layer = fp.attr(m)
        beh = em_beh(fbeh, enc, 'MB_CAVE')
        if m in BOULDERS:
            bot, top = em_floor.copy(), em_render('general', 'cave', BOULDERS[m], 1)
        else:
            bot, top = recolor(fp.layer_img(m, 0, True)), recolor(fp.layer_img(m, 1, False))
        if rk is not None:
            bot, top, beh, layer = over(bot, top), rq[rk], EM[MB_RIFT], 1
        if not (top[..., 3] > 0).any():
            top = None
        mts.append(((m, rk), img(bot), img(top) if top is not None else None, beh))
        attrs.append((beh, layer))
    OUT = 'data/tilesets/secondary/cerulean_cave'
    res = emit(mts, OUT, 512, 6, 7)
    patch_attrs(OUT, attrs)
    out = {}
    for name, (W, H, v, g) in grids.items():
        cells_ = []
        for i in range(W * H):
            k = g[i // W][i % W]
            val = res['names'][k] | (v[i] & 0xFC00)
            if k[1] is not None:
                val = res['names'][k] | (3 << 12) | (COL if k[1] >= 2 else 0)   # scheur: bovenrij warp, onderrij dicht
            cells_.append(val)
        out[name] = (W, H, cells_)
    return out


# ====================================================================== 3. Lavender Town (secondary)
HOUSE = [[0x26c, 0x26d, 0x26d, 0x26e], [0x274, 0x275, 0x275, 0x276], [0x27c, 0x27f, 0x27d, 0x27e],
         [0x284, 0x287, 0x28f, 0x286]]          # Petalburg (Oldale), deur = 0x287
ROOF_EXTRA = {'pc_tr1': 0x282, 'pc_tr2': 0x283, 'mart_tr': 0x285}   # dakhoekjes van PC/Mart (Petalburg)
TOWER_X0, TOWER_Y0 = 15, 0                       # FRLG-toren: 7x7 vanaf (15,0)


def purple(a):
    """Rode/oranje dakpixels -> paars (Lavender)."""
    out = a.copy()
    for y in range(16):
        for x in range(16):
            if not out[y, x, 3]:
                continue
            c = tuple(out[y, x, :3])
            h, s_, v_ = hsv(c)
            if s_ > 0.35 and (h < 0.10 or h > 0.93):
                r, g, b = colorsys.hsv_to_rgb(0.76, s_ * 0.75, v_ * 0.92)
                out[y, x, :3] = (r * 255, g * 255, b * 255)
    return out


def lavender_tileset():
    fp = FPair('primary/general', 'secondary/lavender_town')
    grass = em_render('general', 'petalburg', 0x001)
    fgrass = set()
    for m in (0x001, 0x008, 0x009, 0x010, 0x011):
        fgrass |= {tuple(c[:3]) for c in fp.layer_img(m, 0, True).reshape(-1, 4)}
    W, H, v = frlg_layout('LavenderTown')
    mts, attrs, names = [], [], []

    def add(key, bot, top, beh=0, layer=1):
        mts.append((key, img(bot), img(top) if top is not None and (top[..., 3] > 0).any() else None, beh))
        attrs.append((beh, layer))
        names.append(key)

    pet_attr = open('data/tilesets/secondary/petalburg/metatile_attributes.bin', 'rb').read()

    def pattr(m):
        a = struct.unpack_from('<H', pet_attr, (m - 512) * 2)[0]
        return a & 0xFF, a >> 12

    for r, row in enumerate(HOUSE):
        for c, m in enumerate(row):
            b, l = pattr(m)
            add(('house', r, c), purple(em_render('general', 'petalburg', m, 0)),
                purple(em_render('general', 'petalburg', m, 1)), b, l)
    for k, m in ROOF_EXTRA.items():
        b, l = pattr(m)
        add(k, em_render('general', 'petalburg', m, 0), em_render('general', 'petalburg', m, 1), b, l)

    def regrass(a):
        out = a.copy()
        for y in range(16):
            for x in range(16):
                if out[y, x, 3] and tuple(out[y, x, :3]) in fgrass:
                    out[y, x, :3] = grass[y, x, :3]
        return out

    for dy in range(7):
        for dx in range(7):
            m = v[(TOWER_Y0 + dy) * W + TOWER_X0 + dx] & 0x3FF
            fbeh, enc, layer = fp.attr(m)
            beh = em_beh(fbeh, enc, 'MB_NORMAL')
            if FR.get(fbeh) == 'MB_WARP_DOOR':
                beh = EM['MB_NON_ANIMATED_DOOR']
            add(('tower', dx, dy), regrass(fp.layer_img(m, 0, True)), regrass(fp.layer_img(m, 1, False)), beh, layer)
    for i, q in enumerate(rift_quads(rift_art())):
        add(('rift', i), grass, q, EM[MB_RIFT], 1)
    # S1 (haunted Lavender): graven (Mt. Pyre, Facility 0x324/0x325) en dode bomen (Ekat, Haunted Woods; 1x2)
    for k, m in (('grave_orange', 0x324), ('grave_gray', 0x325)):
        add(k, regrass(em_render('general', 'facility', m)), None, 0, 1)
    dead = np.array(Image.open(DEADTREES).convert('RGBA')).astype(np.int32)
    for y in range(32):
        for x in range(32):
            if tuple(dead[y, x, :3]) in ((56, 144, 48), (24, 160, 104)):   # lichtgroene voet weg (eigen gras eronder)
                dead[y, x, 3] = 0
    for t in range(2):
        for r in range(2):
            add(('deadtree', t, r), grass, dead[r * 16:r * 16 + 16, t * 16:t * 16 + 16], 0, 1)
    OUT = 'data/tilesets/secondary/lavender_town'
    res = emit(mts, OUT, 512, 6, 7)
    patch_attrs(OUT, attrs)
    lavender_moods()
    return res['names']


DEADTREES = 'graphics/grounded/tilesets/ekat/haunted_woods_deadtrees.png'   # Haunted Woods (Normal Pallet), 2 bomen


def haunt(c):
    """Spookstad: donker, ontkleurd violetgrijs."""
    L = lum(c)
    t = (L * 0.70 + 10, L * 0.62 + 6, L * 0.86 + 24)
    return tuple(int(min(248, max(0, 0.22 * a * 0.8 + 0.78 * b))) for a, b in zip(c, t))


def calm(c):
    """Na de bevrijding: zachte schemer, nog wat paarsig, maar weer kleur."""
    L = lum(c)
    t = (L * 0.9 + 18, L * 0.82 + 8, L * 0.9 + 24)
    return tuple(int(min(248, max(0, 0.8 * a * 0.94 + 0.2 * b))) for a, b in zip(c, t))


LAV_MOODS = [('LavenderHauntGeneral', 'primary/lavender_haunt_general', 'primary/general', haunt),
             ('LavenderHaunt', 'secondary/lavender_haunt', 'secondary/lavender_town', haunt),
             ('LavenderCalmGeneral', 'primary/lavender_calm_general', 'primary/general', calm),
             ('LavenderCalm', 'secondary/lavender_calm', 'secondary/lavender_town', calm)]


def lavender_moods():
    """Alleen paletten (tiles/metatiles gedeeld met General resp. lavender_town; BASE voor de renders)."""
    for sym, d, base, tf in LAV_MOODS:
        D = 'data/tilesets/' + d
        os.makedirs(D + '/palettes', exist_ok=True)
        open(D + '/BASE', 'w').write(os.path.basename(base) + '\n')
        for i in range(16):
            cols = jasc('data/tilesets/%s/palettes/%02d.pal' % (base, i))
            write_pal(D + '/palettes/%02d.pal' % i, [cols[0]] + [tf(c) for c in cols[1:]])


# ====================================================================== 4. Spacetime Cave (Cave-kopie + scheuren)
def tint(c):
    L = lum(c)
    t = (L * 0.78 + 6, L * 0.70 + 2, L * 1.08 + 26)
    return tuple(int(min(248, max(0, 0.45 * a + 0.55 * b))) for a, b in zip(c, t))


def write_pal(path, cols):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % tuple(c) for c in cols))


def spacetime_tilesets():
    # primary: General-tiles met getinte paletten
    P = 'data/tilesets/primary/spacetime_general'
    os.makedirs(P + '/palettes', exist_ok=True)
    open(P + '/BASE', 'w').write('general\n')
    for i in range(16):
        cols = jasc('data/tilesets/primary/general/palettes/%02d.pal' % i)
        write_pal(P + '/palettes/%02d.pal' % i, [cols[0]] + [tint(c) for c in cols[1:]])
    # secondary: kopie van Cave + scheuren (palet 12)
    S, C = 'data/tilesets/secondary/spacetime_cave', 'data/tilesets/secondary/cave'
    os.makedirs(S + '/palettes', exist_ok=True)
    cpals = [jasc(C + '/palettes/%02d.pal' % i) for i in range(16)]
    for i in range(16):
        cols = cpals[i] if i < 6 or i > 11 else [cpals[i][0]] + [tint(c) for c in cpals[i][1:]]
        write_pal(S + '/palettes/%02d.pal' % i, cols)
    src_png = Image.open(C + '/tiles.png')
    idx = np.array(src_png)
    NT = 441
    tiles = [idx[(n // 16) * 8:(n // 16) * 8 + 8, (n % 16) * 8:(n % 16) * 8 + 8] for n in range(NT)]
    # scheurtegels: 2 varianten (actief / instabiel) x 4 kwarten x 4 tiles, eigen palet 12
    arts = [rift_art(), rift_art(True, 3)]
    pts = np.concatenate([a.reshape(-1, 4)[a.reshape(-1, 4)[:, 3] > 0][:, :3] for a in arts]).astype(float)
    cent = np.round(_ns['kmeans'](pts, 15, seed=1) / 8) * 8
    for a in arts:
        m = a[..., 3] > 0
        px = a[..., :3][m].astype(float)
        a[..., :3][m] = cent[((px[:, None, :] - cent[None]) ** 2).sum(2).argmin(1)]
    pal = [(255, 0, 255)] + [tuple(int(v) for v in c) for c in cent]
    pal = list(dict.fromkeys(pal))
    assert len(pal) <= 16, len(pal)
    write_pal(S + '/palettes/12.pal', pal + [(0, 0, 0)] * (16 - len(pal)))
    mt = bytearray(open(C + '/metatiles.bin', 'rb').read())
    at = bytearray(open(C + '/metatile_attributes.bin', 'rb').read())
    floor = struct.unpack_from('<4H', mt, (0x201 - 512) * 16)          # onderlaag = Cave-vloer 0x201
    first = len(mt) // 16 + 512
    ids = {}
    for vi, art in enumerate(arts):
        for qi, q in enumerate(rift_quads(art)):
            ents = []
            for sy in (0, 8):
                for sx in (0, 8):
                    blk = q[sy:sy + 8, sx:sx + 8]
                    t = np.zeros((8, 8), np.uint8)
                    for y in range(8):
                        for x in range(8):
                            if blk[y, x, 3]:
                                t[y, x] = pal.index(tuple(int(v) // 8 * 8 for v in blk[y, x, :3]))
                    if not t.any():
                        ents.append(0)
                        continue
                    tiles.append(t)
                    ents.append((512 + len(tiles) - 1) | (12 << 12))
            mt += struct.pack('<8H', *floor, *ents)
            beh = EM[MB_RIFT] if vi == 0 else 0
            at += struct.pack('<H', beh | (1 << 12))
            ids[(vi, qi)] = first + vi * 4 + qi
    assert len(tiles) <= 512
    n = (len(tiles) + 15) // 16 * 16
    out = np.zeros((n // 16 * 8, 128), np.uint8)
    for i, t in enumerate(tiles):
        out[(i // 16) * 8:(i // 16) * 8 + 8, (i % 16) * 8:(i % 16) * 8 + 8] = t
    im = Image.fromarray(out, 'P')
    im.putpalette(src_png.getpalette())
    im.save(S + '/tiles.png')
    open(S + '/metatiles.bin', 'wb').write(bytes(mt))
    open(S + '/metatile_attributes.bin', 'wb').write(bytes(at))
    print(S, len(tiles), 'tiles,', len(mt) // 16, 'metatiles')
    return ids


# ====================================================================== registratie in headers/graphics/metatiles
TILESETS = [  # (symbool, map, secondary?, tiles-symbool (None = eigen), callback, omschrijving)
    ('SpacetimeGeneral', 'primary/spacetime_general', False, 'General', 'InitTilesetAnim_General', 'Spacetime Cave: General getint'),
    ('SpacetimeCave', 'secondary/spacetime_cave', True, None, 'InitTilesetAnim_Cave', 'Spacetime Cave: Cave + scheuren'),
    ('PokemonTower', 'secondary/pokemon_tower', True, None, 'NULL', 'Pokemon Tower (FRLG + Ekat Revamp)'),
    ('CeruleanCave', 'secondary/cerulean_cave', True, None, 'NULL', 'Cerulean Cave (FRLG + Emerald Cave)'),
    ('LavenderTown', 'secondary/lavender_town', True, None, 'NULL', 'Lavender Town (Emerald-huizen, FRLG-toren)'),
    # S1: Lavender met een eigen sfeer (alleen paletten): spookstad en, na de bevrijding, een zachte schemer
    ('LavenderHauntGeneral', 'primary/lavender_haunt_general', False, 'General', 'InitTilesetAnim_General', 'Lavender Town: General als spookstad'),
    ('LavenderHaunt', 'secondary/lavender_haunt', True, 'LavenderTown', 'NULL', 'Lavender Town als spookstad'),
    ('LavenderCalmGeneral', 'primary/lavender_calm_general', False, 'General', 'InitTilesetAnim_General', 'Lavender Town: General na de bevrijding'),
    ('LavenderCalm', 'secondary/lavender_calm', True, 'LavenderTown', 'NULL', 'Lavender Town na de bevrijding'),
]


def register():
    gh = open('src/data/tilesets/graphics.h').read()
    mh = open('src/data/tilesets/metatiles.h').read()
    hh = open('src/data/tilesets/headers.h').read()
    for sym, d, sec, tiles_sym, cb, why in TILESETS:
        D = 'data/tilesets/' + d
        tsym = tiles_sym or sym
        if tiles_sym is None and 'gTilesetTiles_%s[]' % sym not in gh:
            gh += '\n// Project Grounded: %s (spacetime_tiles.py)\nconst u32 gTilesetTiles_%s[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n' % (why, sym, D)
        if 'gTilesetPalettes_%s[]' % sym not in gh:
            gh += ('\n// Project Grounded: %s (paletten)\nconst u16 gTilesetPalettes_%s[][16] =\n{\n' % (why, sym)
                   + ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (D, i) for i in range(16)) + '};\n')
        msym = 'General' if not sec else (tiles_sym or sym)     # een secondary met tiles_sym deelt ook de metatiles
        if sec and tiles_sym is None and 'gMetatiles_%s[]' % sym not in mh:
            mh += ('\nconst u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin"); // Project Grounded: %s\n'
                   'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % (sym, D, why, sym, D))
        if 'gTileset_%s =' % sym not in hh:
            hh += ('\nconst struct Tileset gTileset_%s = // Project Grounded: %s\n{\n'
                   '    .isCompressed = TRUE,\n    .isSecondary = %s,\n    .tiles = gTilesetTiles_%s,\n'
                   '    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n'
                   '    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = %s,\n};\n'
                   % (sym, why, 'TRUE' if sec else 'FALSE', tsym, sym, msym, msym, cb))
    open('src/data/tilesets/graphics.h', 'w').write(gh)
    open('src/data/tilesets/metatiles.h', 'w').write(mh)
    open('src/data/tilesets/headers.h', 'w').write(hh)


def build_all():
    tower = tower_tileset()
    lav = lavender_tileset()
    hub = spacetime_tilesets()
    register()
    return tower, lav, hub


if __name__ == '__main__':
    build_all()
    print('klaar')
