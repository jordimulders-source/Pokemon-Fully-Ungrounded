"""Project Grounded: Yoshi's Island (Spacetime Cave, post-game; de ?????-kamer "gaat fout").

Een andere dimensie: top-down in Pokemon-stijl, maar grafisch compleet anders (dat is de grap). Alles komt uit de
Super Mario Advance 3-sheets in graphics/grounded/yoshis_island/ (Mode 7-eilandobjecten van Trasher, achtergronden
van Tech Static/Bowserman en p.k, objecten van A.J. Nitro) en is verder per pixel getekend in die stijl (krijtarcering,
dikke omlijning, pasteltinten).

Kaarten (achteraan gMapGroup_Spacetime):
  YoshisIsland_Beach      aankomst (je valt uit de lucht, Yoshi vindt je), strand + weide, terugscheur naar de hub,
                          twee Shy Guys bewaken de pijp naar de heuvels (multi battle 1 met Yoshi).
  YoshisIsland_Hills      pastelheuvels, torentjes, het Shy Guy-kamp (multi battles 2 en 3), Pecharunts
                          mochikraampje, Boo's spookhuis (west) en Wario's fort (noord, dicht tot Boo verslagen is).
  YoshisIsland_BooMansion binnen: Commander Boo (multi battle met Yoshi, 2 tegen 1).
  YoshisIsland_WarioFort  binnen: twee Shy Guy-wachters (multi battle 4) en Wario (eindbaas, 2 tegen 1).
  YoshisIsland_YoshiHouse binnen: het Yoshi-huis (oosthoek van het strand), tien Yoshi's in alle kleuren
                          (paletwissels uit yoshi_sprites.py, twee kleuren per palet); de roze geeft een Sweet Heart.
  Jungle: Nep-Enut (SMA3-watermonster op ware grootte, 128x128) loert in het meertje; aanspreken vanaf de oever.
Tilesets: primary yoshi_island_base (de grond: gras, pad, zand, water, hoog gras, plateaus; per 8x8 uit een
afstandsveld, dus organische randen die toch ontdubbelen) + per kaart een eigen secondary (yoshi_beach, yoshi_hills,
yoshi_boo, yoshi_fort). emit() uit snow_tileset.py zet een getekend canvas om naar tiles/paletten.
Verhaal (TODO 4, SPACETIME_PLAN 3): Shy Guys = parodie op een evil team en praten niet (sarcasme tussen haakjes);
Yoshi is partner (PARTNER_YOSHI, multi battles); Shy Guys -> Commander Boo -> Wario zit erachter. Pecharunt verkocht
Wario de mochi waarmee hij de Shy Guys gehoorzaam houdt; na Wario kun je hem vangen.
Klaar: FLAG_SPACETIME_YOSHI_DONE (FLAG_GROUNDED(580)). Flags FLAG_GROUNDED 1024-1119 (blok 'yoshis_island'),
trainers 1017-1019, 1026-1029, 1049, 1055, 1056 (blok 'yoshis_island'), partner PARTNER_YOSHI.
Idempotent; controleert de bereikbaarheid. Gebruik: python3 tools/grounded/maptools/yoshis_island.py [renderdir]"""
# Levels: de levelcurve is leidend; check_levels zet bestaande levels terug (zie glimwood.py).
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
import check_levels  # noqa: E402
check_levels.protect()
import json, math, os, re, struct, sys, zlib
from collections import deque
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.normpath(os.path.join(HERE, '..', '..', '..')))
bd = None                           # beacon_dragon (Scr, warp, obj, ...): pas in main() geladen (heeft gebouwde tiles nodig)


def load_bd():
    global bd
    if bd is None:
        import beacon_dragon
        bd = beacon_dragon
    return bd

SRC = 'graphics/grounded/yoshis_island'
GROUP = 'gMapGroup_Spacetime'
HUB_DEST = ('SPACETIME_CAVE', 13)   # terugscheur -> de ?????-kamer in de hub (landingswarp 13, spacetime_cave.py)
                                    # van het ?????-portaal (spacetime_cave.py) en draait dit script opnieuw.
SEED = 1025                         # nationaal dexnummer van Pecharunt

_src = open('tools/grounded/snow_tileset.py').read()
_ns = {'np': np, 'Image': Image, 'struct': struct, 'os': os, 'LAYER_COVERED': 1}
exec(_src[_src.index('def to5('):_src.rindex('\nif TOWN:')], _ns)
emit = _ns['emit']

MB = dict(normal=0x00, tall_grass=0x02, pond=0x10, sand=0x21, b1f_warp=0x29, aqua_warp=0x67, door=0x60,
          south_arrow=0x65, north_arrow=0x64, indoor=0x0B, cave=0x08)


# ====================================================================== pixel-hulpjes
def rgba(c, a=255):
    return np.array(list(c) + [a], float)


def hexs(*cs):
    return [tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in cs]


def rng(*key):
    return np.random.default_rng(zlib.crc32(repr(key).encode()))


def vnoise(seed, period, cells, size=None):
    """Periodieke value noise (periode `period` px, `cells` roosterpunten per periode), waarden 0..1."""
    size = size or period
    r = rng('vn', seed, period, cells)
    g = r.random((cells, cells))
    ys, xs = np.mgrid[0:size, 0:size].astype(float)
    u, v = xs / period * cells, ys / period * cells
    x0, y0 = np.floor(u).astype(int), np.floor(v).astype(int)
    fx, fy = u - x0, v - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a = g[y0 % cells, x0 % cells]; b = g[y0 % cells, (x0 + 1) % cells]
    c = g[(y0 + 1) % cells, x0 % cells]; d = g[(y0 + 1) % cells, (x0 + 1) % cells]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def outline_of(mask):
    """Pixels van mask die aan een niet-mask-pixel grenzen (4-buren)."""
    m = mask
    nb = np.zeros_like(m)
    nb[1:] |= ~m[:-1]; nb[:-1] |= ~m[1:]; nb[:, 1:] |= ~m[:, :-1]; nb[:, :-1] |= ~m[:, 1:]
    return m & nb


def dilate(mask, n=1):
    m = mask.copy()
    for _ in range(n):
        o = m.copy()
        o[1:] |= m[:-1]; o[:-1] |= m[1:]; o[:, 1:] |= m[:, :-1]; o[:, :-1] |= m[:, 1:]
        m = o
    return m


def paint(cv, mask, col):
    cv[mask] = rgba(col)


def stamp(cv, spr, x, y):
    """Alpha-stempel (RGBA float of uint8) op canvas cv op pixelpositie (x, y) linksboven; knipt af."""
    s = np.asarray(spr, float)
    H, W = cv.shape[:2]
    h, w = s.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x0 >= x1 or y0 >= y1:
        return
    sub = s[y0 - y:y1 - y, x0 - x:x1 - x]
    a = sub[..., 3:4] / 255.0
    cv[y0:y1, x0:x1, :3] = cv[y0:y1, x0:x1, :3] * (1 - a) + sub[..., :3] * a
    cv[y0:y1, x0:x1, 3] = np.maximum(cv[y0:y1, x0:x1, 3], sub[..., 3])


def sheet(name):
    return np.array(Image.open(os.path.join(SRC, name)).convert('RGBA')).astype(float)


def key_out(a, bg, tol=0):
    a = a.copy()
    d = np.abs(a[..., :3] - np.array(bg, float)).sum(2)
    a[d <= tol, 3] = 0
    return a


def crop_obj(a, box, bg, tol=0):
    x0, y0, x1, y1 = box
    return key_out(a[y0:y1, x0:x1], bg, tol)


def trim(a):
    m = a[..., 3] > 0
    ys, xs = np.where(m)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def keep_largest(a):
    """Alleen het grootste samenhangende stuk (8-buren) houden: losse snippers van buurobjecten in de sheet weg."""
    m = a[..., 3] > 0
    H, W = m.shape
    lab = -np.ones((H, W), int)
    best, bestn = -1, 0
    k = 0
    for y in range(H):
        for x in range(W):
            if m[y, x] and lab[y, x] < 0:
                st = [(y, x)]; lab[y, x] = k; n = 0
                while st:
                    cy, cx = st.pop(); n += 1
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and lab[ny, nx] < 0:
                                lab[ny, nx] = k; st.append((ny, nx))
                if n > bestn:
                    best, bestn = k, n
                k += 1
    a = a.copy()
    a[lab != best, 3] = 0
    return a


def pad_cells(a, w, h, ax='c', ay='b', dx=0, dy=0):
    """Zet sprite a in een vak van w x h cellen (16 px), standaard onderaan gecentreerd."""
    out = np.zeros((h * 16, w * 16, 4))
    sh, sw = a.shape[:2]
    x = {'c': (w * 16 - sw) // 2, 'l': 0, 'r': w * 16 - sw}[ax] + dx
    y = {'b': h * 16 - sh, 't': 0, 'c': (h * 16 - sh) // 2}[ay] + dy
    stamp(out, a, x, y)
    return out


def shadow_under(a, col=(0, 0, 0), alpha=70, rx=None, ry=3, cy=None):
    """Zachte ovale slagschaduw onder een sprite (geditherd, zodat er geen halftinten in de tiles komen)."""
    h, w = a.shape[:2]
    out = np.zeros_like(a)
    rx = rx or w * 0.42
    cy = cy if cy is not None else h - 2
    ys, xs = np.mgrid[0:h, 0:w]
    e = ((xs - (w - 1) / 2) / rx) ** 2 + ((ys - cy) / ry) ** 2
    m = (e <= 1) & (((xs + ys) % 2) == 0)
    out[m] = rgba(col, alpha)
    stamp(out, a, 0, 0)
    return out


# ====================================================================== grondtexturen (periode 32 px, naadloos)
P = 32
GR = hexs('a8d870', 'c8ec90', 'e0f8b0', '80b858', '4c8838', '2c5828')        # gras: basis, licht, lichter, donker, rand
PA = hexs('f0c868', 'f8e090', 'fcf0c8', 'd09848', '8c5c20', '603810')        # pad (level 1-geel)
SA = hexs('f8e8b0', 'fcf4d8', 'ffffff', 'e0c890', 'b89858', '806030')        # zand
WA = hexs('68c0e8', '98d8f0', 'f0f8fc', '4898d0', '2870b0', '184880')        # water
TG = hexs('78c048', 'a8dc60', 'd8f498', '4c9030', '1c4018', '305c20')        # hoog gras (bossige plukken)
PL = hexs('c8d898', 'e0ecb8', 'f4f8e0', 'a0b878', '506838', '202c18')        # plateauwand (SMA3: lichtgroen met noppen)
FR = hexs('f8c820', 'fce070', 'fff8c0', 'd09000', '885000', '302000')        # gele franje (SMA3-randstruik)


def crayon(base, cols, seed, n=26, lmin=3, lmax=6, slope=1, dots=0, dotcol=None, tufts=0, tuftcol=None):
    """Krijtarcering: korte diagonale streepjes in lichtere/donkerdere tinten, naadloos met periode P."""
    t = np.zeros((P, P, 4)); t[...] = rgba(base)
    r = rng('crayon', seed)
    for _ in range(n):
        x, y = r.integers(0, P, 2)
        L = r.integers(lmin, lmax + 1)
        c = cols[r.integers(0, len(cols))]
        for k in range(L):
            t[(y - k * slope // max(1, abs(slope))) % P if False else (y - k) % P, (x + k) % P] = rgba(c)
    for _ in range(dots):
        x, y = r.integers(0, P, 2)
        t[y % P, x % P] = rgba(dotcol)
    for _ in range(tufts):                     # kleine 'v'-plukjes
        x, y = r.integers(0, P, 2)
        for dx, dy in ((0, 0), (-1, -1), (1, -1), (-2, -2), (2, -2)):
            t[(y + dy) % P, (x + dx) % P] = rgba(tuftcol)
    return t


def tex_grass():
    t = crayon(GR[0], [GR[1], GR[1], GR[1], GR[2]], 'gras', n=13, lmin=2, lmax=4, tufts=3, tuftcol=GR[3])
    return t


def tex_path():
    t = crayon(PA[0], [PA[1], PA[1], PA[2]], 'pad', n=34, lmin=3, lmax=7)
    r = rng('pad-heuveltjes')
    for _ in range(2):                         # kleine omlijnde heuveltjes (level 1)
        cx, cy = r.integers(0, P, 2)
        for dx in range(-3, 4):
            for dy in range(-2, 1):
                if dx * dx / 12.0 + dy * dy / 4.0 <= 1.0:
                    t[(cy + dy) % P, (cx + dx) % P] = rgba(PA[2] if dy < -1 else PA[1])
        for dx in range(-3, 4):
            dy = -int(round(math.sqrt(max(0.0, 4.0 * (1 - dx * dx / 12.0)))))
            t[(cy + dy - 1) % P, (cx + dx) % P] = rgba(PA[4])
        t[(cy) % P, (cx - 4) % P] = rgba(PA[4]); t[(cy) % P, (cx + 4) % P] = rgba(PA[4])
    return t


def tex_sand():
    t = crayon(SA[0], [SA[1], SA[1], SA[2]], 'zand', n=22, lmin=2, lmax=4, dots=10, dotcol=SA[3])
    return t


def tex_water(phase=0):
    t = np.zeros((P, P, 4)); t[...] = rgba(WA[0])
    n = vnoise('water', P, 4)
    t[n > 0.62] = rgba(WA[1])
    t[n < 0.25] = rgba(WA[3])
    r = rng('golfjes')
    for _ in range(5):                         # witte golfjes: korte boogjes
        x, y = r.integers(0, P, 2)
        for dx in range(-2, 3):
            t[(y - (1 if abs(dx) < 2 else 0)) % P, (x + dx) % P] = rgba(WA[2])
    for _ in range(4):
        x, y = r.integers(0, P, 2)
        t[y % P, x % P] = rgba(WA[2])
    return t


def tex_plateau_top():
    """Bovenkant van een plateau: dichte, ronde struikjes met omlijning (de SMA3-heuvelbegroeiing van bovenaf)."""
    C = hexs('5c9c40', '7cbc50', 'a8dc70', '3c7030', '1c3818')
    t = np.zeros((P, P, 4)); t[...] = rgba(C[3])
    r = rng('struikjes')
    ys, xs = np.mgrid[0:P, 0:P]
    pts = [(r.uniform(0, P), r.uniform(0, P), r.uniform(4.2, 6.2)) for _ in range(14)]
    for cx, cy, rad in sorted(pts, key=lambda p: p[1]):
        for ox in (-P, 0, P):
            for oy in (-P, 0, P):
                d2 = (xs - cx - ox) ** 2 + ((ys - cy - oy) * 1.1) ** 2
                m = d2 <= rad * rad
                if not m.any():
                    continue
                t[m] = rgba(C[0])
                t[m & (d2 <= (rad * 0.62) ** 2) & (ys - cy - oy < 0)] = rgba(C[1])
                t[m & (d2 <= (rad * 0.32) ** 2) & (ys - cy - oy < -1)] = rgba(C[2])
                t[m & (d2 > (rad - 1.1) ** 2) & (ys - cy - oy > 0)] = rgba(C[4])
    return t


def tex_face():
    """Zijwand van een plateau: lichtgroene grond met lichte streepjes en ronde noppen (SMA3, 'unused'-sheet)."""
    t = crayon(PL[0], [PL[1], PL[1], PL[2]], 'wand', n=26, lmin=2, lmax=3)
    r = rng('noppen')
    for (cx, cy) in ((6, 9), (22, 25)):
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                d = dx * dx + dy * dy
                if d <= 5:
                    t[cy + dy, cx + dx] = rgba(PL[4] if d >= 4 else (PL[2] if dx + dy < -1 else PL[3]))
    return t


def tiled(tex, H, W):
    reps = (H // P + 1, W // P + 1, 1)
    return np.tile(tex, reps)[:H, :W].copy()


# ====================================================================== afstandsveld per 3x3-omgeving
_U = np.arange(16) + 0.5
_DT = {}
for _dy in (-1, 0, 1):
    for _dx in (-1, 0, 1):
        ax = np.maximum(np.maximum(_dx * 16 - _U, 0), _U - (_dx * 16 + 16))
        ay = np.maximum(np.maximum(_dy * 16 - _U, 0), _U - (_dy * 16 + 16))
        _DT[(_dx, _dy)] = np.hypot(ax[None, :], ay[:, None])


def sdist(region):
    """Per pixel: afstand tot buiten de regio min afstand tot binnen (positief = binnen); alleen de 3x3-buren tellen
    (dus elke cel hangt alleen van zijn eigen buurt af en ontdubbelt). Buiten de kaart = de dichtstbijzijnde rand."""
    H, W = region.shape
    pad = np.pad(region, 1, mode='edge')
    din = np.full((H * 16, W * 16), 99.0)
    dout = np.full((H * 16, W * 16), 99.0)
    for (dx, dy), D in _DT.items():
        nb = pad[1 + dy:1 + dy + H, 1 + dx:1 + dx + W]
        Dt = np.tile(D, (H, W))
        big = np.kron(nb, np.ones((16, 16), bool))
        din = np.where(big, np.minimum(din, Dt), din)
        dout = np.where(~big, np.minimum(dout, Dt), dout)
    return dout - din


def edge_noise(seed, H, W, amp=2.5):
    n = vnoise(seed, P, 4)
    return (tiled(np.dstack([n] * 4), H, W)[..., 0] - 0.5) * 2 * amp


# ====================================================================== objecten (stempels)
M7_BG = (160, 240, 192)          # mintgroene achtergrond van de Mode 7-sheet
_M7 = None


def m7(box, largest=True):
    global _M7
    if _M7 is None:
        _M7 = sheet('island_mode7.png')
    a = crop_obj(_M7, box, M7_BG)
    if largest:
        a = keep_largest(a)
    return trim(a)


def pipe_art():
    """Groene warppijp van bovenaf: rand + zwart gat (bovenste rij, beloopbaar = warp), lijf (onderste rij)."""
    G = hexs('184818', '308830', '58b838', '90d858', 'c8f090', '082008')
    a = np.zeros((32, 32, 4))
    ys, xs = np.mgrid[0:32, 0:32]
    cx = 15.5
    body = (np.abs(xs - cx) <= 12.5) & (ys >= 12) & (ys <= 30)
    a[body] = rgba(G[1])
    t = (xs - cx + 12.5) / 25.0
    a[body & (t > 0.18) & (t < 0.34)] = rgba(G[3])
    a[body & (t > 0.22) & (t < 0.28)] = rgba(G[4])
    a[body & (t > 0.72)] = rgba(G[0])
    rim = ((xs - cx) / 15.0) ** 2 + ((ys - 10) / 8.0) ** 2 <= 1
    a[rim] = rgba(G[2])
    hl = rim & (((xs - cx + 6) / 6.0) ** 2 + ((ys - 5) / 2.2) ** 2 <= 1)
    a[hl] = rgba(G[4])
    hole = ((xs - cx) / 10.5) ** 2 + ((ys - 10.5) / 5.0) ** 2 <= 1
    a[hole] = rgba(G[5])
    a[hole & (ys <= 7)] = rgba(G[0])
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba(G[5])
    a[(np.abs(xs - cx) <= 12.5) & (ys == 18) & m] = rgba(G[0])
    return a


def rift_art():
    """Terugscheur naar de Spacetime Cave: paarse draaikolk met sterretjes (2x2)."""
    C = hexs('180828', '3c1868', '6c34b0', 'a070e8', 'd8b8ff', 'ffffff')
    a = np.zeros((32, 32, 4))
    ys, xs = np.mgrid[0:32, 0:32]
    dx, dy = xs - 15.5, (ys - 17.5) * 1.25
    r = np.hypot(dx, dy)
    ang = np.arctan2(dy, dx)
    m = r <= 14.5
    sw = (np.sin(ang * 3 + r * 0.55) + 1) / 2
    a[m] = rgba(C[1])
    a[m & (sw > 0.45)] = rgba(C[2])
    a[m & (sw > 0.75)] = rgba(C[3])
    a[m & (r < 4.5)] = rgba(C[0])
    a[m & (r < 2.0)] = rgba(C[4])
    for (x, y) in ((8, 9), (24, 12), (20, 26), (6, 22), (14, 6)):
        a[y, x] = rgba(C[5])
    a[outline_of(m)] = rgba(C[0])
    return a


def tent_art(main, dark, light):
    """Shy Guy-tent (3x2): driehoekig doek in de kleur van de bende, wit masker-embleem, donkere ingang."""
    W_, H_ = 48, 32
    a = np.zeros((H_, W_, 4))
    ys, xs = np.mgrid[0:H_, 0:W_]
    cx = 23.5
    body = (ys >= 3) & (ys <= 30) & (np.abs(xs - cx) <= (ys - 3) * 0.85 + 2)
    a[body] = rgba(main)
    a[body & (xs < cx - (ys - 3) * 0.3)] = rgba(light)
    a[body & (xs > cx + (ys - 3) * 0.45)] = rgba(dark)
    door = (ys >= 17) & (np.abs(xs - cx) <= (ys - 17) * 0.5 + 1)
    a[door & body] = rgba((24, 16, 24))
    mask = ((xs - cx) / 4.2) ** 2 + ((ys - 11) / 5.0) ** 2 <= 1
    a[mask] = rgba((248, 248, 248))
    for ex in (cx - 1.8, cx + 1.8):
        a[(np.abs(xs - ex) < 0.9) & (ys >= 9) & (ys <= 10)] = rgba((16, 16, 16))
    a[(np.abs(xs - cx) < 0.6) & (ys == 13)] = rgba((16, 16, 16))
    m = a[..., 3] > 0
    a[outline_of(m) & ~door] = rgba((16, 8, 16))
    a[1:4, 22:26] = rgba((120, 72, 32))
    return a


def campfire_art():
    a = np.zeros((16, 16, 4))
    L = hexs('603018', '985028', 'c87838')
    a[12:14, 2:14] = rgba(L[1]); a[10:12, 3:13] = rgba(L[2])
    F = hexs('f84010', 'f8a020', 'f8e070', 'fff8d0')
    ys, xs = np.mgrid[0:16, 0:16]
    for r, c in ((6.0, F[0]), (4.2, F[1]), (2.6, F[2]), (1.2, F[3])):
        m = (((xs - 7.5) / (r * 0.8)) ** 2 + ((ys - 9 + (6 - r) * 0.3) / r) ** 2 <= 1) & (ys <= 11)
        a[m] = rgba(c)
    mm = a[..., 3] > 0
    a[outline_of(mm)] = rgba((40, 16, 8))
    return a


def mochi_stand_art():
    """Pecharunts kraampje (2x2): paarse luifel, tafel met mochi in pastelkleuren."""
    a = np.zeros((32, 32, 4))
    pur = hexs('3c1850', '6c2c8c', 'a050c0', 'd090e8')
    wood = hexs('603818', '906030', 'c08848')
    ys, xs = np.mgrid[0:32, 0:32]
    aw = (ys >= 2) & (ys <= 11) & (xs >= 1) & (xs <= 30)
    a[aw] = rgba(pur[1])
    a[aw & ((xs // 4) % 2 == 0)] = rgba(pur[3])
    a[aw & (ys >= 10) & ((xs % 4) < 2)] = rgba(pur[2])
    a[12:28, 3:5] = rgba(wood[1]); a[12:28, 27:29] = rgba(wood[1])
    a[20:28, 2:30] = rgba(wood[2]); a[26:28, 2:30] = rgba(wood[0])
    for i, x in enumerate(range(6, 27, 5)):
        c = [(248, 200, 224), (248, 248, 240), (200, 240, 168), (232, 184, 248), (248, 216, 200)][i % 5]
        m = ((xs - x) / 2.4) ** 2 + ((ys - 18.5) / 1.8) ** 2 <= 1
        a[m] = rgba(c)
        a[m & (ys < 18)] = rgba((255, 255, 255))
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba((24, 8, 24))
    return a


def sign_art():
    a = np.zeros((16, 16, 4))
    W_ = hexs('583010', '906028', 'c89850', 'e8c078')
    a[3:10, 2:14] = rgba(W_[2]); a[4:6, 3:13] = rgba(W_[3]); a[9:10, 2:14] = rgba(W_[1])
    a[10:15, 7:9] = rgba(W_[1])
    for (x, y) in ((7, 5), (8, 5), (9, 6), (8, 7), (8, 8)):
        a[y, x] = rgba(W_[0])
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba(W_[0])
    return a


def qblock_art():
    """Geel ?-blok met klinknageltjes."""
    a = np.zeros((16, 16, 4))
    Y = hexs('f8d020', 'fce878', 'c89000', '603000', 'ffffff')
    a[1:15, 1:15] = rgba(Y[0]); a[1:3, 1:15] = rgba(Y[1]); a[1:15, 1:3] = rgba(Y[1])
    a[13:15, 1:15] = rgba(Y[2]); a[1:15, 13:15] = rgba(Y[2])
    for (x, y) in ((3, 3), (12, 3), (3, 12), (12, 12)):
        a[y, x] = rgba(Y[3])
    q = ['.###.', '#...#', '...#.', '..#..', '.....', '..#..']
    for j, row in enumerate(q):
        for i, ch in enumerate(row):
            if ch == '#':
                a[4 + j, 6 + i] = rgba(Y[4])
                a[4 + j, 5 + i] = rgba(Y[3])
    a[0, 1:15] = rgba(Y[3]); a[15, 1:15] = rgba(Y[3]); a[1:15, 0] = rgba(Y[3]); a[1:15, 15] = rgba(Y[3])
    return a


def egg_art(spot=(56, 176, 48)):
    """Yoshi-ei (wit met gekleurde vlekken), 16x16."""
    a = np.zeros((16, 16, 4))
    ys, xs = np.mgrid[0:16, 0:16]
    m = ((xs - 7.5) / 5.6) ** 2 + ((ys - 8.5) / 6.6) ** 2 <= 1
    a[m] = rgba((248, 248, 240))
    a[m & (xs > 9) & (ys > 9)] = rgba((208, 208, 200))
    for (x, y, r) in ((5, 6, 1.8), (10, 9, 1.6), (6, 12, 1.4)):
        a[m & (((xs - x) ** 2 + (ys - y) ** 2) <= r * r)] = rgba(spot)
    a[outline_of(m)] = rgba((24, 24, 24))
    a[4:6, 5:6] = rgba((255, 255, 255))
    return a


def flower_smiley():
    """SMA3-lachbloem (wit met geel hart en een gezichtje), 16x16."""
    a = np.zeros((16, 16, 4))
    ys, xs = np.mgrid[0:16, 0:16]
    pet = np.zeros((16, 16), bool)
    for k in range(6):
        ang = k * math.pi / 3
        px, py = 7.5 + 4.6 * math.cos(ang), 7.5 + 4.6 * math.sin(ang)
        pet |= ((xs - px) ** 2 + (ys - py) ** 2) <= 3.2 ** 2
    a[pet] = rgba((248, 248, 248))
    c = ((xs - 7.5) ** 2 + (ys - 7.5) ** 2) <= 3.4 ** 2
    a[c] = rgba((248, 208, 48))
    a[6:8, 6] = rgba((24, 24, 24)); a[6:8, 9] = rgba((24, 24, 24))
    a[9, 6:10] = rgba((200, 40, 40))
    m = a[..., 3] > 0
    a[outline_of(m) & ~c] = rgba((24, 24, 24))
    return a


def tulip_art(col=(232, 120, 96)):
    a = np.zeros((16, 16, 4))
    dk = tuple(int(v * 0.65) for v in col)
    lt = tuple(min(255, int(v * 1.15 + 20)) for v in col)
    a[8:15, 7:9] = rgba((56, 120, 40))
    a[11:13, 4:7] = rgba((88, 168, 56)); a[12:14, 9:12] = rgba((88, 168, 56))
    cup = np.zeros((16, 16), bool)
    cup[3:9, 4:12] = True
    cup[3, 4] = cup[3, 11] = False
    cup[3:5, 6:7] = False; cup[3:5, 9:10] = False
    a[cup] = rgba(col)
    sub = cup.copy(); sub[:, :] = False; sub[4:8, 5:7] = True
    a[cup & sub] = rgba(lt)
    sub[:, :] = False; sub[7:9, 9:11] = True
    a[cup & sub] = rgba(dk)
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba((40, 16, 16))
    return a


def objects():
    """Bibliotheek: naam -> dict(art = RGBA in een vak van w x h cellen, solid = vaste cellen, beh = gedrag per cel)."""
    O = {}

    def add(name, spr, w, h, solid=None, beh=None, ax='c', ay='b', dx=0, dy=0, shadow=True):
        a = pad_cells(spr, w, h, ax, ay, dx, dy)
        if solid is None:
            solid = [(i, j) for i in range(w) for j in range(h)]
        O[name] = dict(art=a, w=w, h=h, solid=set(solid), beh=beh or {}, shadow=shadow)
    # uit de Mode 7-sheet (Trasher)
    add('hill', m7((0, 0, 32, 30)), 2, 2)
    add('dome', m7((32, 64, 48, 84)), 1, 2, solid=[(0, 1)])
    add('tower_red', m7((48, 64, 64, 96)), 1, 2)
    add('tower_beige', m7((64, 64, 80, 96)), 1, 2)
    add('tower_spot', m7((80, 64, 96, 96)), 1, 2)
    add('tower_grey', m7((48, 96, 64, 128)), 1, 2)
    add('fir', m7((0, 85, 16, 112)), 1, 2)
    add('palm', m7((176, 64, 192, 89)), 1, 2)
    add('bush_tree', m7((176, 110, 192, 128)), 1, 1)
    add('mush_house', m7((240, 46, 256, 64)), 1, 1)
    add('castle_small', m7((240, 28, 256, 46)), 1, 1)
    add('volcano', m7((192, 64, 232, 98)), 3, 2)
    add('rock', m7((224, 160, 256, 189)), 2, 2)
    add('red_keep', m7((32, 128, 61, 160)), 2, 2)
    add('flag', m7((97, 0, 128, 31)), 2, 2, solid=[(0, 1)])
    add('dead_tree', m7((0, 128, 16, 161)), 1, 2)
    add('peak', m7((12, 192, 52, 256)), 3, 4)
    add('cloud', m7((4, 64, 28, 80)), 2, 1)
    # getekend
    # pijp: de rand (boven) is vast, het lijf (onder) is de warp: je loopt er van het zuiden in en wordt gelanceerd
    add('pipe', pipe_art(), 2, 2, solid=[(0, 0), (1, 0)], beh={(0, 1): MB['b1f_warp'], (1, 1): MB['b1f_warp']})
    add('rift', rift_art(), 2, 2, solid=[(0, 1), (1, 1)], beh={(0, 0): MB['aqua_warp'], (1, 0): MB['aqua_warp']})
    add('tent_red', tent_art((216, 40, 40), (136, 16, 24), (248, 112, 96)), 3, 2)
    add('tent_green', tent_art((48, 160, 64), (24, 96, 40), (120, 216, 112)), 3, 2)
    add('tent_pink', tent_art((240, 112, 176), (176, 48, 120), (252, 184, 216)), 3, 2)
    add('campfire', campfire_art(), 1, 1)
    add('mochi_stand', mochi_stand_art(), 2, 2)
    add('sign', sign_art(), 1, 1)
    add('qblock', qblock_art(), 1, 1)
    add('egg_green', egg_art((56, 176, 48)), 1, 1)
    add('egg_red', egg_art((224, 56, 48)), 1, 1)
    add('egg_yellow', egg_art((232, 184, 24)), 1, 1)
    add('smiley', flower_smiley(), 1, 1, solid=[], shadow=False)
    add('tulip', tulip_art(), 1, 1, solid=[], shadow=False)
    add('tulip_pink', tulip_art((232, 128, 168)), 1, 1, solid=[], shadow=False)
    add_facades(O)
    inside_objects(O)
    sma3_objects(O)
    return O


# ====================================================================== kaart + canvas
def tall_cell():
    """Hoog gras (16x16): vier bossige plukken met omlijning, zoals de SMA3-struikjes, maar groen."""
    a = np.zeros((16, 16, 4))
    ys, xs = np.mgrid[0:16, 0:16]
    for (cx, cy, r) in ((4, 6, 4.2), (11.5, 5, 4.0), (8, 11, 4.4), (1, 13, 3.4), (15, 12.5, 3.4)):
        m = ((xs - cx) ** 2 + ((ys - cy) * 1.15) ** 2) <= r * r
        ring = m & ~(((xs - cx) ** 2 + ((ys - cy) * 1.15) ** 2) <= (r - 1.1) ** 2)
        a[m] = rgba(TG[0])
        a[m & (ys < cy - r * 0.25) & (xs < cx + r * 0.3)] = rgba(TG[1])
        a[m & (ys < cy - r * 0.55) & (xs < cx)] = rgba(TG[2])
        a[m & (ys > cy + r * 0.45)] = rgba(TG[3])
        a[ring & (ys >= cy - r * 0.2)] = rgba(TG[4])
    return a


class YMap:
    """Kaart op celniveau: terrein (letters), objecten, warps; render() tekent het hele canvas."""
    def __init__(self, name, W, H, fill='g'):
        self.name, self.W, self.H = name, W, H
        self.T = np.full((H, W), fill, '<U1')
        self.objs = []                        # (naam, x, y)
        self.solid = np.zeros((H, W), bool)
        self.beh = np.zeros((H, W), int)
        self.extra = {}                       # (x, y) -> functie(canvas, x, y) voor losse tekeningen
        self.objmask = np.zeros((H, W), bool) # cellen met een object (gaan naar de secondary)

    def rect(self, x0, y0, x1, y1, c):
        self.T[y0:y1 + 1, x0:x1 + 1] = c

    def put(self, name, x, y):
        self.objs.append((name, x, y))

    def render(self, O, seed):
        H, W = self.H * 16, self.W * 16
        T = self.T
        cv = tiled(tex_grass(), H, W)
        # zand (ook onder het water, zodat de kust over zand loopt)
        sand = np.isin(T, list('sw'))
        if sand.any():
            m = sdist(sand) + edge_noise(('zand', seed), H, W, 2.5) > 0
            cv[m] = tiled(tex_sand(), H, W)[m]
            rim = dilate(m) & ~m
            cv[rim] = rgba(GR[4])
        path = T == 'p'
        if path.any():
            m = sdist(path) + edge_noise(('pad', seed), H, W, 2.0) > 0.5
            cv[m] = tiled(tex_path(), H, W)[m]
            cv[outline_of(m)] = rgba(PA[4])
        water = T == 'w'
        if water.any():
            sd = sdist(water) + edge_noise(('water', seed), H, W, 3.5)
            m = sd > 1.0
            cv[m] = tiled(tex_water(), H, W)[m]
            foam = m & (sd < 3.2)
            cv[foam] = rgba(WA[2])
            cv[outline_of(m)] = rgba(WA[4])
        tall = T == 't'
        if tall.any():
            tc = tall_cell()
            for y, x in zip(*np.where(tall)):
                stamp(cv, tc, x * 16, y * 16)
        self._sky(cv, seed)
        self._plateaus(cv, seed)
        if (T == 'J').any():
            self._plateaus(cv, seed, ch='J', top=tex_canopy(), face=tex_trunks(), fr=FRJ, foot=TRK[2])
        thorn = T == 'n'
        if thorn.any():
            for y, x in zip(*np.where(thorn)):
                stamp(cv, thorn_cell((x + y) % 2), x * 16, y * 16)
        # objecten: eerst schaduwen, dan van boven naar onder (onderste staat ervoor)
        for name, x, y in sorted(self.objs, key=lambda o: o[2] + O[o[0]]['h']):
            o = O[name]
            if o['shadow']:
                self._shadow(cv, o, x, y)
            stamp(cv, o['art'], x * 16, y * 16)
            self.objmask[y:y + o['h'] + (1 if o['shadow'] else 0), x:x + o['w']] = True
            for (dx, dy) in o['solid']:
                self.solid[y + dy, x + dx] = True
            for (dx, dy), b in o['beh'].items():
                self.beh[y + dy, x + dx] = b
        for (x, y), fn in self.extra.items():
            fn(cv, x, y)
            self.objmask[y, x] = True
        # gedrag en botsing van het terrein
        self.beh[(T == 't') & (self.beh == 0)] = MB['tall_grass']
        self.beh[(T == 'w') & (self.beh == 0)] = MB['pond']
        self.solid |= np.isin(T, list('HFvJkn'))
        return cv

    def _shadow(self, cv, o, x, y):
        a = o['art']
        h, w = a.shape[:2]
        m = a[..., 3] > 0
        if not m.any():
            return
        ys, xs = np.where(m)
        bot = ys.max()
        cx = (xs.min() + xs.max()) / 2
        rx = (xs.max() - xs.min()) / 2 + 2
        Y, X = np.mgrid[0:h + 4, 0:w]
        e = ((X - cx) / rx) ** 2 + ((Y - bot - 0.5) / 3.0) ** 2 <= 1
        e &= ((X + Y) % 2 == 0)
        px, py = x * 16, y * 16
        sub = cv[py:py + h + 4, px:px + w]
        e = e[:sub.shape[0], :sub.shape[1]]
        sub[e, :3] = sub[e, :3] * 0.72

    def _plateaus(self, cv, seed, face_rows=2, ch='H', top=None, face=None, fr=FR, foot=PL[3]):
        """Plateaus ('H'): bovenkant met gele SMA3-franje langs de rand, onderaan een wand van `face_rows` cellen
        (lichtgroen met noppen) en een slagschaduw op de grond eronder."""
        T = self.T
        top_tex, face_tex = top, face
        Hr = T == ch
        if not Hr.any():
            return
        H, W = cv.shape[:2]
        face = np.zeros_like(Hr)
        for x in range(self.W):
            for y in range(self.H):
                if Hr[y, x] and (y + 1 >= self.H or not Hr[y + 1, x]) and y + 1 < self.H:
                    for k in range(face_rows):
                        if y - k >= 0 and Hr[y - k, x]:
                            face[y - k, x] = True
        self.face = face
        top = Hr & ~face
        mH = sdist(Hr) + edge_noise(('plat', seed) if ch == 'H' else ('plat', seed, ch), H, W, 1.5) > 0.5
        sdt = sdist(top)
        bump = (tiled(np.dstack([vnoise(('franje', seed), P, 8)] * 4), H, W)[..., 0]) * 2.5
        topm = mH & (sdt > -0.5 + edge_noise(('pt', seed), H, W, 1.0) * 0)
        facem = mH & ~topm
        cv[topm] = tiled(top_tex if top_tex is not None else tex_plateau_top(), H, W)[topm]
        cv[facem] = tiled(face_tex if face_tex is not None else tex_face(), H, W)[facem]
        # franje: band langs de rand van de bovenkant
        band = topm & (sdt < 6.0 + bump)
        hi = tiled(np.dstack([vnoise(('fhi', seed), P, 8)] * 4), H, W)[..., 0]
        cv[band] = rgba(fr[0])
        cv[band & (hi > 0.6)] = rgba(fr[1])
        cv[band & (hi > 0.8)] = rgba(fr[2])
        cv[band & (hi < 0.3)] = rgba(fr[3])
        cv[outline_of(band) & topm & ~outline_of(topm)] = rgba(fr[4])
        lower = np.zeros_like(mH)
        lower[:-3] = mH[3:]
        cv[facem & ~lower] = rgba(foot)                       # donkere voet van de wand
        cv[outline_of(mH)] = rgba(fr[5])
        # schaduw op de grond onder de wand
        Y, X = np.mgrid[0:H, 0:W]
        shade = (dilate(mH, 3) & ~mH) & ((X + Y) % 2 == 0)
        # alleen onder (zuid van) een wand
        south = np.zeros_like(mH)
        for k in range(1, 4):
            south[k:] |= facem[:-k]
        shade &= south
        cv[shade, :3] *= 0.72

    def cells(self, cv):
        """Canvas -> lijst (cel-sleutel, 16x16 RGBA) per cel."""
        out = {}
        for y in range(self.H):
            for x in range(self.W):
                out[(x, y)] = cv[y * 16:y * 16 + 16, x * 16:x * 16 + 16]
        return out

    def reach(self, start, blocked=()):
        seen = {start}
        q = deque([start])
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.W and 0 <= ny < self.H and (nx, ny) not in seen and not self.solid[ny, nx] \
                        and self.T[ny, nx] != 'w' and (nx, ny) not in blocked:
                    seen.add((nx, ny)); q.append((nx, ny))
        return seen


# ====================================================================== kaart 1: het strand (aankomst)
BW, BH = 37, 24                      # (was 30 breed; de oosthoek x 27-33 is voor het Yoshi-huis)
B_LAND = (15, 15)                    # warp 0: hier val je uit de lucht (bestemming van het ?????-portaal)
B_RIFT = (5, 14)                     # terugscheur (2x2, bovenste rij = warp)
B_PIPE = (14, 5)                     # pijp naar de heuvels (2x2, onderste rij = warp)
B_GUARDS = [(14, 7), (15, 7)]        # twee Shy Guys versperren de pijp
B_YOSHI = (13, 12)                   # Yoshi (na de aankomstscene staat hij hier tot hij vooruit rent)
B_SIGN = (18, 12)
B_JPIPE = (25, 10)                   # pijp naar de jungle (onderste rij = warp)
B_MSG = (20, 14)                     # Message Block op het strand
B_CLOUD = (12, 14)                   # ?-wolk (Shalour Sable)
B_HOUSE = (28, 6)                    # Yoshi-huis 6x4, deur op (30, 9) en (31, 9)
B_HOUSE_DOOR = (B_HOUSE[0] + 2, B_HOUSE[1] + 3)
B_MAIL = (33, 10)                    # brievenbus (Message Block) naast het huis


def beach_map():
    m = YMap('YoshisIsland_Beach', BW, BH)
    T = m.T
    m.rect(0, 0, BW - 1, 4, 'H')                       # noordrand (wand op rij 3-4)
    m.rect(0, 0, 2, 13, 'H'); m.rect(BW - 3, 0, BW - 1, 13, 'H')
    m.rect(3, 5, 4, 8, 'H'); m.rect(25, 5, 26, 7, 'H')
    # strand en zee
    m.rect(0, 13, BW - 1, BH - 1, 's')
    m.rect(0, 14, 1, 15, 's')
    r = rng('kust')
    for x in range(BW):
        top = 19 + int(round(math.sin(x * 0.45) * 0.8 + math.sin(x * 0.17 + 1) * 0.9))
        m.rect(x, top, x, BH - 1, 'w')
    # pad van het strand naar de pijp
    m.rect(14, 7, 15, 12, 'p')
    m.rect(16, 11, 21, 12, 'p'); m.rect(20, 9, 21, 10, 'p')
    # hoog gras
    m.rect(5, 6, 9, 9, 't'); m.rect(6, 10, 10, 11, 't'); m.rect(18, 6, 23, 8, 't'); m.rect(22, 9, 24, 11, 't')
    # objecten
    m.put('pipe', *B_PIPE)
    m.put('hill', 12, 5); m.put('hill', 16, 5)
    m.put('tower_spot', 10, 4); m.put('tower_beige', 19, 4)
    m.put('rift', *B_RIFT)
    for x, y in ((3, 16), (8, 13), (21, 14), (26, 16), (24, 13)):
        m.put('palm', x, y)
    m.put('rock', 27, 14)
    m.put('egg_green', 9, 17); m.put('egg_red', 11, 17); m.put('egg_yellow', 22, 17)
    m.put('qblock', 17, 9)
    m.put('sign', *B_SIGN)
    m.put('bush_tree', 11, 9); m.put('bush_tree', 24, 5); m.put('bush_tree', 5, 11)
    m.put('mush_house', 23, 12)
    m.put('pipe', *B_JPIPE)
    m.put('msgblock', *B_MSG)
    m.put('chomp_grey', 8, 15)
    m.put('yoshi_house', *B_HOUSE)
    m.put('msgblock', *B_MAIL)
    m.rect(B_HOUSE_DOOR[0], B_HOUSE_DOOR[1] + 1, B_HOUSE_DOOR[0] + 1, 12, 'p')       # paadje naar de deur
    for x, y in ((27, 10), (33, 12), (29, 12)):
        m.put('tulip' if (x + y) % 2 else 'tulip_pink', x, y)
    m.put('egg_red', 27, 8); m.put('egg_yellow', 34, 14)
    for x, y in ((12, 11), (17, 7), (19, 10), (7, 12), (25, 12), (11, 7)):
        m.put('smiley', x, y)
    for x, y in ((13, 10), (16, 9), (22, 12), (4, 10), (10, 12)):
        m.put('tulip' if (x + y) % 2 else 'tulip_pink', x, y)
    return m


# ====================================================================== canvas -> tilesets + map.bin
PRIM_DIR = 'data/tilesets/primary/yoshi_island_base'
PRIM_SYM = 'YoshiIslandBase'


def cell_list(m, cv):
    """[(x, y, sleutel, 16x16 RGBA, gedrag)] voor alle cellen van kaart m."""
    out = []
    for y in range(m.H):
        for x in range(m.W):
            a = np.clip(cv[y * 16:y * 16 + 16, x * 16:x * 16 + 16], 0, 255).astype(np.uint8).copy()
            a[..., 3] = 255
            b = int(m.beh[y, x])
            out.append((x, y, (a.tobytes(), b), a, b))
    return out


def build_tilesets(outdoor, indoor):
    """outdoor/indoor: [(YMap, canvas, secondary-map, symbool)]. Primary = de vaakst voorkomende cellen zonder object
    uit de buitenkaarten; per kaart een secondary met de rest. Geeft per kaart een HxW-raster met metatile-nummers."""
    freq, arr = {}, {}
    for m, cv, _, _ in outdoor:
        for x, y, k, a, b in cell_list(m, cv):
            # de oosthoek van het strand (x >= 27, sinds het Yoshi-huis) telt niet mee: zo blijft de primary
            # gelijk aan die van het oude, smallere strand (de volle secondaries van jungle en bloemenveld rekenen erop)
            if not m.objmask[y, x] and not (m.name == 'YoshisIsland_Beach' and x >= 27):
                freq[k] = freq.get(k, 0) + 1
                arr[k] = (a, b)
    keys = sorted(freq, key=lambda k: -freq[k])
    # de heuvel-secondary zit tegen de 512 tiles aan: wat in de primary nog past, gaat daarheen (objectcellen van
    # de heuvels, in kaartvolgorde)
    spill = []
    for m, cv, _, _ in outdoor:
        if m.name == 'YoshisIsland_Hills':
            for x, y, k, a, b in cell_list(m, cv):
                if m.objmask[y, x] and k not in freq and k not in arr:
                    arr[k] = (a, b); spill.append(k)
    keys += spill
    n = min(len(keys), 480)
    while True:
        prim = [('p%d' % i, arr[k][0], None, arr[k][1]) for i, k in enumerate(keys[:n])]
        try:
            res = emit(prim, PRIM_DIR, 0, 0, 6, blank_tile=True)
            break
        except AssertionError as e:
            print('primary te vol (%s), minder cellen' % e)
            n -= 8
    pid = {k: i for i, k in enumerate(keys[:n])}
    grids = {}
    for m, cv, sec_dir, sym in outdoor + indoor:
        cl = cell_list(m, cv)
        own, oid = [], {}
        for x, y, k, a, b in cl:
            if k not in pid and k not in oid:
                oid[k] = len(own)
                own.append(('s%d' % len(own), a, None, b))
        m.extra_ids = {}
        for (x, y), c in sorted(getattr(m, 'extra', {}).items()):     # losse varianten (de brug van de ?-wolk)
            a = np.clip(c, 0, 255).astype(np.uint8).copy(); a[..., 3] = 255
            k = (a.tobytes(), 0)
            if k not in pid and k not in oid:
                oid[k] = len(own)
                own.append(('s%d' % len(own), a, None, 0))
            m.extra_ids[(x, y)] = pid[k] if k in pid else 512 + oid[k]
        assert len(own) <= 512, (m.name, len(own))
        emit(own, sec_dir, 512, 6, 7, shared=res)
        g = np.zeros((m.H, m.W), int)
        for x, y, k, a, b in cl:
            g[y, x] = pid[k] if k in pid else 512 + oid[k]
        grids[m.name] = g
        print('%s: %d eigen metatiles' % (m.name, len(own)))
    return grids


def write_tilesets(syms):
    """Registreer primary + secondaries (graphics.h, metatiles.h, headers.h); idempotent."""
    gh = open('src/data/tilesets/graphics.h').read()
    mh = open('src/data/tilesets/metatiles.h').read()
    hh = open('src/data/tilesets/headers.h').read()
    for sym, d, sec, why in [(PRIM_SYM, PRIM_DIR, False, "Yoshi's Island: grond (primary)")] + syms:
        if 'gTilesetTiles_%s[]' % sym not in gh:
            gh += ('\n// Project Grounded: %s (tools/grounded/maptools/yoshis_island.py)\n'
                   'const u32 gTilesetTiles_%s[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n' % (why, sym, d))
            gh += ('const u16 gTilesetPalettes_%s[][16] =\n{\n' % sym
                   + ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (d, i) for i in range(16)) + '};\n')
        if 'gMetatiles_%s[]' % sym not in mh:
            mh += ('\nconst u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin"); // Project Grounded: %s\n'
                   'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");\n'
                   % (sym, d, why, sym, d))
        if 'gTileset_%s =' % sym not in hh:
            hh += ('\nconst struct Tileset gTileset_%s = // Project Grounded: %s\n{\n'
                   '    .isCompressed = TRUE,\n    .isSecondary = %s,\n    .tiles = gTilesetTiles_%s,\n'
                   '    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n'
                   '    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = NULL,\n};\n'
                   % (sym, why, 'TRUE' if sec else 'FALSE', sym, sym, sym, sym))
    open('src/data/tilesets/graphics.h', 'w').write(gh)
    open('src/data/tilesets/metatiles.h', 'w').write(mh)
    open('src/data/tilesets/headers.h', 'w').write(hh)


def const(name):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper()


def save_layout(m, grid, sec_sym, border_mt):
    d = 'data/layouts/' + m.name
    os.makedirs(d, exist_ok=True)
    data = bytearray()
    for y in range(m.H):
        for x in range(m.W):
            coll = 1 if m.solid[y, x] else 0
            elev = 1 if m.T[y, x] == 'w' else 3
            if (x, y) in getattr(m, 'elev0', ()):       # Nep-Enut: elevation 0, aan te spreken vanaf het land
                elev = 0
            data += struct.pack('<H', int(grid[y, x]) | (coll << 10) | (elev << 12))
    open(d + '/map.bin', 'wb').write(bytes(data))
    open(d + '/border.bin', 'wb').write(struct.pack('<4H', *([border_mt | (1 << 10) | (3 << 12)] * 4)))
    lj = open('data/layouts/layouts.json').read()
    c = const(m.name)
    entry = '''    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_%s",
      "secondary_tileset": "gTileset_%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (c, m.name, m.W, m.H, PRIM_SYM, sec_sym, m.name, m.name)
    if '"LAYOUT_%s"' % c in lj:
        i = lj.index('"id": "LAYOUT_%s"' % c); s = lj.rindex('    {', 0, i); e = lj.index('    }', i) + 5
        lj = lj[:s] + entry + lj[e:]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    json.loads(lj)
    open('data/layouts/layouts.json', 'w').write(lj)
    return 'LAYOUT_' + c


# ====================================================================== gevels: Boo's spookhuis en Wario's fort
COB = hexs('5c4830', '806040', 'a07c54', 'c09868', '30241c', 'd8a060')    # SMA3-kasteelkeien (bg-2)


def tex_cobble(base=None, w=64, h=32, seed='keien', cols=COB):
    """Ronde keien in versprongen rijen (zoals de kasteelvloer in de SMA3-achtergrond); naadloos w x h."""
    t = np.zeros((h, w, 4)); t[...] = rgba(cols[4])
    r = rng(seed)
    ys, xs = np.mgrid[0:h, 0:w]
    for row in range(h // 8):
        off = (row % 2) * 8
        for k in range(w // 16):
            cx, cy = (off + k * 16 + 7.5) % w, row * 8 + 3.5
            jx, jy = r.uniform(-0.6, 0.6), r.uniform(-0.3, 0.3)
            for ox in (-w, 0, w):
                d = ((xs - cx - jx - ox) / 7.2) ** 2 + ((ys - cy - jy) / 3.6) ** 2
                m = d <= 1
                t[m] = rgba(cols[1])
                t[m & (ys < cy - 0.8)] = rgba(cols[2])
                t[m & (ys < cy - 2.2) & (xs - ox < cx - 1)] = rgba(cols[3])
                t[m & (ys > cy + 1.6)] = rgba(cols[0])
    return t


def boo_house_art():
    """Spookhuis (6x5 cellen): leistenen dak, houten wand uit de SMA3-spookhuisachtergrond, boogdeur."""
    W_, H_ = 96, 80
    a = np.zeros((H_, W_, 4))
    bg = sheet('sma3_backgrounds_a.png')
    wall = bg[1092:1092 + 56, 46:46 + 96].copy()            # wand met de boogvensters (bg.png, spookhuis)
    wall[..., 3] = 255
    stamp(a, wall, 0, 22)
    DX = 88 - 47.5                                           # deur rechts van de vensters (cel 5)
    # dak: donker violet, schubben, puntgevel
    R = hexs('1c1028', '3a2450', '5a3a78', '7c58a0')
    ys, xs = np.mgrid[0:H_, 0:W_]
    roof = (ys >= 2) & (ys <= 24) & (np.abs(xs - 47.5) <= 46 - (24 - ys) * 0.55)
    a[roof] = rgba(R[1])
    sc = roof & (((xs + (ys // 4) * 3) % 6) == 0) | roof & ((ys % 4) == 0)
    a[sc] = rgba(R[0])
    a[roof & (ys < 8)] = rgba(R[2])
    a[roof & (ys < 5) & (np.abs(xs - 47.5) < 10)] = rgba(R[3])
    # deur (boog), net boven de onderrand
    dc = 47.5 + DX
    door = (ys >= 54) & (ys <= 79) & (np.abs(xs - dc) <= 6.5) & ~((ys < 61) & (((xs - dc) / 6.5) ** 2 + ((ys - 61) / 7) ** 2 > 1))
    a[door] = rgba((16, 8, 24))
    a[door & (ys > 72)] = rgba((48, 24, 72))
    # spookachtige ogen in de deur
    a[64:66, int(dc) - 3:int(dc) - 1] = rgba((248, 248, 248)); a[64:66, int(dc) + 2:int(dc) + 4] = rgba((248, 248, 248))
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba((8, 4, 12))
    a[78:80, 0:96][~door[78:80, 0:96]] = rgba((24, 24, 32))
    return a


def fort_art():
    """Wario's fort (8x6 cellen): keienmuur met kantelen, twee torens, paarse W-vlag, grote poort."""
    W_, H_ = 128, 96
    a = np.zeros((H_, W_, 4))
    cob = tiled(tex_cobble(seed='fort'), H_, W_)
    ys, xs = np.mgrid[0:H_, 0:W_]
    body = (ys >= 30) & (xs >= 10) & (xs < 118)
    towers = ((xs < 34) | (xs >= 94)) & (ys >= 10)
    m = body | towers
    a[m] = cob[m]
    # kantelen
    for x0 in list(range(0, 34, 8)) + list(range(94, 128, 8)):
        a[4:10, x0:x0 + 5] = cob[4:10, x0:x0 + 5]
    for x0 in range(34, 94, 10):
        a[24:30, x0:x0 + 6] = cob[24:30, x0:x0 + 6]
    # oranje rand links op de torens (lichtval, zoals in de bron)
    for x0 in (0, 94):
        a[10:96, x0:x0 + 3][a[10:96, x0:x0 + 3, 3] > 0] = rgba(COB[5])
    # poort
    gate = (ys >= 58) & (np.abs(xs - 64) <= 13) & ~((ys < 70) & (((xs - 64) / 13.0) ** 2 + ((ys - 70) / 12.0) ** 2 > 1))
    a[gate] = rgba((32, 20, 16))
    for gx in range(53, 77, 5):
        a[60:96, gx:gx + 1][gate[60:96, gx:gx + 1]] = rgba((96, 72, 40))
    # vlag met W
    a[0:30, 62:64] = rgba((120, 96, 72))
    flag = (ys >= 2) & (ys <= 15) & (xs >= 64) & (xs <= 84)
    a[flag] = rgba((136, 56, 168))
    for (x, y) in ((67, 5), (68, 8), (69, 11), (70, 9), (71, 7), (72, 9), (73, 11), (74, 8), (75, 5),
                   (67, 6), (68, 9), (69, 12), (73, 12), (74, 9), (75, 6), (71, 8)):
        a[y, x + 2] = rgba((248, 216, 40))
    # ramen
    for (x, y) in ((18, 34), (106, 34), (44, 42), (80, 42)):
        a[y:y + 8, x:x + 6] = rgba((24, 16, 16))
        a[y:y + 2, x + 1:x + 5] = rgba((248, 200, 64))
    mm = a[..., 3] > 0
    a[outline_of(mm)] = rgba((24, 16, 12))
    return a


YH_SPOTS = hexs('38b030', 'e83830', 'f8c818', '58b8f0', 'f088c0', '9850d0', 'a06830', '303038', '2858d8')


def yoshi_house_art():
    """Het Yoshi-huis (6x4 cellen): een reuzen-Yoshi-ei als dak (wit, met vlekken in alle Yoshi-kleuren), muur van
    lichte keien, ronde raampjes en de rode houten deur uit de SMA3-objectensheet (32x32, onderste rij = deur)."""
    W_, H_ = 96, 64
    a = np.zeros((H_, W_, 4))
    ys, xs = np.mgrid[0:H_, 0:W_]
    wallc = hexs('a89070', 'c8b090', 'e0d0b0', 'f0e8d0', '584430', 'f8f0e0')
    wall = (ys >= 28) & (xs >= 6) & (xs < 90)
    cob = tiled(tex_cobble(seed='yoshihuis', cols=wallc), H_, W_)
    a[wall] = cob[wall]
    # dak: de bovenkant van een groot ei, iets breder dan de muur
    egg = (((xs - 47.5) / 47.5) ** 2 + ((ys - 34) / 33.0) ** 2 <= 1) & (ys <= 33)
    a[egg] = rgba((248, 248, 240))
    a[egg & (xs > 60) & (ys > 14)] = rgba((216, 216, 208))
    a[egg & (((xs - 30) / 9.0) ** 2 + ((ys - 9) / 4.0) ** 2 <= 1)] = rgba((255, 255, 255))
    for k, (cx, cy, r) in enumerate(((22, 22, 4.5), (40, 12, 4.0), (58, 20, 4.5), (75, 26, 4.0), (12, 30, 3.2),
                                     (31, 28, 3.4), (50, 29, 3.0), (68, 9, 3.4), (84, 30, 3.0))):
        sp = egg & (((xs - cx) ** 2 + ((ys - cy) * 1.15) ** 2) <= r * r)
        a[sp] = rgba(YH_SPOTS[k])
    a[outline_of(egg)] = rgba((24, 24, 24))
    a[(ys == 33) & (xs >= 2) & (xs < 94)] = rgba((96, 96, 96))           # dakrand
    # ronde raampjes met warm licht
    for wx in (18, 77):
        win = ((xs - wx) ** 2 + (ys - 43) ** 2) <= 36
        a[win] = rgba((248, 208, 96))
        a[win & (ys < 42) & (xs < wx)] = rgba((255, 240, 176))
        a[win & ((xs == wx) | (ys == 43))] = rgba((120, 80, 40))
        a[outline_of(win)] = rgba((88, 56, 32))
    m = a[..., 3] > 0
    a[outline_of(m) & ~egg] = rgba((40, 28, 16))
    door = sma((176, 13, 208, 45))
    stamp(a, door, 32, 64 - door.shape[0])
    return a


def add_facades(O):
    def add(name, spr, w, h, solid, beh):
        O[name] = dict(art=pad_cells(spr, w, h), w=w, h=h, solid=set(solid), beh=beh, shadow=False)
    # spookhuis: deur op (3, 4) (cel in het vak), rest vast
    add('boo_house', boo_house_art(), 6, 5, [(i, j) for i in range(6) for j in range(5) if (i, j) != (5, 4)],
        {(5, 4): MB['door']})
    add('fort', fort_art(), 8, 6, [(i, j) for i in range(8) for j in range(6) if (i, j) != (4, 5)],
        {(4, 5): MB['door']})
    add('yoshi_house', yoshi_house_art(), 6, 4, [(i, j) for i in range(6) for j in range(4) if (i, j) not in ((2, 3), (3, 3))],
        {(2, 3): MB['door'], (3, 3): MB['door']})


# ====================================================================== kaart 2: de heuvels (Shy Guy-kamp)
HW, HH = 40, 32
H_PIPE = (19, 27)                    # pijp terug naar het strand (onderste rij = warp)
H_FORT = (16, 1)                     # fortgevel 8x6, deur op (20, 6)
H_BOO = (3, 7)                       # spookhuis 6x5, deur op (6, 11)
H_FORT_DOOR = (H_FORT[0] + 4, H_FORT[1] + 5)
H_BOO_DOOR = (H_BOO[0] + 5, H_BOO[1] + 4)
H_GATE_GUARD = (H_FORT_DOOR[0], H_FORT_DOOR[1] + 1)
H_CAMP_A = [(30, 17), (31, 17)]      # bende A in het kamp
H_CAMP_B = [(12, 14), (12, 15)]      # bende B versperren het pad naar het spookhuis
H_YOSHI = (21, 18)
H_PECHA = (34, 20)                   # Pecharunt achter zijn kraampje (kraam op 32-33, 19-20)
H_SIGN = (22, 24)
H_CLOUD = (16, 25)                   # ?-wolk: een sterrenregen (doet niets, zoals de meeste verzamelobjecten)


def hills_map():
    m = YMap('YoshisIsland_Hills', HW, HH)
    T = m.T
    m.rect(0, 0, HW - 1, 4, 'H')                         # noordwand (rij 3-4)
    m.rect(0, 0, 1, HH - 1, 'H'); m.rect(HW - 2, 0, HW - 1, HH - 1, 'H')
    m.rect(0, HH - 2, HW - 1, HH - 1, 'H')
    # spookhuistuin: omsloten door plateaus, alleen het pad van oost
    m.rect(2, 5, 13, 6, 'H')
    m.rect(2, 16, 13, 19, 'H')
    m.rect(13, 5, 14, 13, 'H')
    # rest van het reliëf
    m.rect(25, 5, 37, 8, 'H')
    m.rect(2, 20, 6, 29, 'H')
    m.rect(33, 25, 37, 29, 'H')
    # paden
    m.rect(19, 7, 20, 29, 'p')
    m.rect(8, 12, 8, 15, 'p'); m.rect(6, 14, 18, 15, 'p')
    m.rect(21, 16, 28, 17, 'p')
    m.rect(26, 12, 34, 22, 'p')                          # kampplein
    # hoog gras
    m.rect(8, 21, 15, 26, 't'); m.rect(22, 21, 30, 23, 't'); m.rect(23, 9, 30, 11, 't'); m.rect(4, 8, 4, 11, 't')
    m.rect(26, 24, 31, 28, 't'); m.rect(8, 27, 13, 28, 't')
    # gebouwen
    m.put('fort', *H_FORT)
    m.put('boo_house', *H_BOO)
    m.put('pipe', *H_PIPE)
    # kamp
    m.put('tent_red', 26, 10); m.put('tent_green', 30, 10); m.put('tent_pink', 34, 13)
    m.put('campfire', 29, 15)
    m.put('flag', 26, 19)
    m.put('mochi_stand', 32, 19)
    # decor
    m.put('dead_tree', 3, 12); m.put('dead_tree', 11, 11); m.put('dead_tree', 10, 8)
    m.put('volcano', 6, 1)
    m.put('hill', 15, 19); m.put('hill', 23, 13); m.put('dome', 17, 11); m.put('dome', 22, 10)
    m.put('tower_red', 25, 3); m.put('tower_grey', 36, 4); m.put('red_keep', 30, 3)
    m.put('fir', 7, 19); m.put('fir', 16, 23); m.put('fir', 35, 22); m.put('fir', 31, 23)
    m.put('bush_tree', 17, 27); m.put('bush_tree', 22, 27); m.put('bush_tree', 24, 18); m.put('bush_tree', 36, 17)
    m.put('rock', 14, 28)
    m.put('qblock', 21, 7); m.put('qblock', 25, 15)
    m.put('egg_green', 16, 17); m.put('egg_yellow', 24, 25)
    m.put('sign', *H_SIGN)
    for x, y in ((18, 21), (21, 25), (17, 15), (22, 8), (34, 23), (15, 9), (11, 20)):
        m.put('smiley', x, y)
    for x, y in ((18, 25), (21, 21), (16, 12), (25, 20), (36, 20)):
        m.put('tulip' if (x + y) % 2 else 'tulip_pink', x, y)
    return m


# ====================================================================== binnenkaarten
def tex_planks(cols, seed, w=32, h=32):
    """Houten vloer: horizontale planken (8 px) met naden en nerf, naadloos."""
    t = np.zeros((h, w, 4)); t[...] = rgba(cols[1])
    r = rng('plank', seed)
    for row in range(h // 8):
        y0 = row * 8
        t[y0, :] = rgba(cols[3])
        t[y0 + 1, :] = rgba(cols[2])
        cut = (r.integers(0, w) + row * 13) % w
        t[y0:y0 + 8, cut] = rgba(cols[3])
        for _ in range(3):
            x, y = r.integers(0, w), y0 + r.integers(3, 7)
            for k in range(r.integers(3, 7)):
                t[y, (x + k) % w] = rgba(cols[0])
    return t


BOO_FLOOR = hexs('2c2440', '3c3458', '504870', '18142c')
BOO_CARPET = hexs('8c1c3c', 'b83050', 'e05c70', '4c0c20')
FORT_FLOOR = hexs('6c6050', '8c7c68', 'a89880', 'c8b8a0', '3c3428', 'd8c8a8')
FORT_CARPET = hexs('901820', 'c02830', 'e85848', '500c10')


def carpet_art(cols, w, h):
    a = np.zeros((h * 16, w * 16, 4)); a[...] = rgba(cols[1])
    a[:, :2] = rgba(cols[3]); a[:, -2:] = rgba(cols[3])
    a[:, 2:3] = rgba(cols[2]); a[:, -3:-2] = rgba(cols[2])
    for y in range(0, h * 16, 8):
        a[y + 3:y + 5, 6:w * 16 - 6] = rgba(cols[0])
    return a


def candle_art():
    a = np.zeros((32, 16, 4))
    G = hexs('604010', 'a07018', 'e0b030', 'f8e070')
    a[26:30, 3:13] = rgba(G[1]); a[29:31, 2:14] = rgba(G[0])
    a[12:26, 7:9] = rgba(G[1]); a[18:20, 3:13] = rgba(G[2])
    for x in (3, 7, 12):
        a[10:18, x:x + 2] = rgba((240, 240, 232))
        a[6:10, x:x + 2] = rgba((120, 200, 248)); a[7:9, x:x + 2] = rgba((220, 248, 255))   # blauwe spookvlam
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba((24, 16, 8))
    return a


def yoshi_portrait_art():
    """Ingelijst ei met groene vlekken (het familieportret van de Yoshi's: allemaal eieren)."""
    a = np.zeros((16, 16, 4))
    a[1:15, 2:14] = rgba((184, 144, 40)); a[2:14, 3:13] = rgba((168, 216, 248))
    stamp(a, egg_art()[2:15, 2:14], 3, 2)
    a[0, 2:14] = rgba((24, 16, 8)); a[15, 2:14] = rgba((24, 16, 8)); a[1:15, 1] = rgba((24, 16, 8)); a[1:15, 14] = rgba((24, 16, 8))
    return a


def portrait_art():
    """Schilderij van een Boo (de Boo uit de trainerfoto-bron, verkleind tot 12x12) in een gouden lijst."""
    a = np.zeros((16, 16, 4))
    a[1:15, 2:14] = rgba((184, 144, 40)); a[2:14, 3:13] = rgba((56, 40, 72))
    b = np.array(Image.open('graphics/grounded/trainers/guests/boo_bron.png').convert('RGBA').resize((10, 10), Image.NEAREST)).astype(float)
    b[b[..., 3] < 128, 3] = 0; b[b[..., 3] >= 128, 3] = 255
    stamp(a, b, 3, 3)
    a[0, 2:14] = rgba((24, 16, 8)); a[15, 2:14] = rgba((24, 16, 8)); a[1:15, 1] = rgba((24, 16, 8)); a[1:15, 14] = rgba((24, 16, 8))
    return a


def web_art(flip=False):
    a = np.zeros((16, 16, 4))
    c = rgba((176, 192, 208))
    for k in range(16):
        a[0, k] = c if k < 14 else a[0, k]
    for i in range(14):
        a[i, i] = c
        if i < 10:
            a[i, 0] = c
    for r_ in (4, 8, 12):
        for k in range(r_):
            a[r_ - k, k] = c if (k % 2 == 0) else a[r_ - k, k]
    if flip:
        a = a[:, ::-1].copy()
    return a


def pillar_art():
    a = np.zeros((32, 16, 4))
    st = tiled(tex_cobble(seed='pilaar', w=16, h=32), 32, 16)
    a[4:30, 2:14] = st[4:30, 2:14]
    a[0:5, 1:15] = rgba(FORT_FLOOR[3]); a[29:32, 1:15] = rgba(FORT_FLOOR[1])
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba(FORT_FLOOR[4])
    return a


def throne_art():
    a = np.zeros((32, 32, 4))
    G = hexs('7c5410', 'b88818', 'f0c838', 'fff090')
    R_ = hexs('681050', 'a02878', 'd058a8')
    ys, xs = np.mgrid[0:32, 0:32]
    back = (ys >= 1) & (ys <= 22) & (np.abs(xs - 15.5) <= 11) & ~((ys < 8) & (((xs - 15.5) / 11) ** 2 + ((ys - 8) / 7) ** 2 > 1))
    a[back] = rgba(G[1])
    a[back & (np.abs(xs - 15.5) <= 7) & (ys >= 6)] = rgba(R_[1])
    a[back & (np.abs(xs - 15.5) <= 7) & (ys >= 6) & (xs < 13)] = rgba(R_[2])
    seat = (ys >= 20) & (ys <= 30) & (np.abs(xs - 15.5) <= 13)
    a[seat] = rgba(G[2]); a[seat & (ys >= 27)] = rgba(G[0])
    a[(ys >= 21) & (ys <= 24) & (np.abs(xs - 15.5) <= 10)] = rgba(R_[1])
    # W in goud bovenin
    for (x, y) in ((11, 3), (12, 5), (13, 4), (14, 3), (15, 5), (16, 3), (17, 4), (18, 5), (19, 3)):
        a[y, x] = rgba(G[3])
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba((32, 16, 8))
    return a


def coins_art(seed):
    a = np.zeros((16, 16, 4))
    r = rng('munten', seed)
    G = hexs('a87010', 'e8b020', 'f8e070', 'fffcd0')
    ys, xs = np.mgrid[0:16, 0:16]
    pts = [(r.uniform(3, 13), r.uniform(7, 13)) for _ in range(9)]
    for cx, cy in sorted(pts, key=lambda p: p[1]):
        m = ((xs - cx) / 3.2) ** 2 + ((ys - cy) / 2.0) ** 2 <= 1
        a[m] = rgba(G[1]); a[m & (ys < cy - 0.5)] = rgba(G[2]); a[m & (ys < cy - 1.2) & (xs < cx)] = rgba(G[3])
        a[outline_of(m)] = rgba(G[0])
    mm = a[..., 3] > 0
    a[outline_of(mm)] = rgba((48, 32, 8))
    return a


def torch_art():
    a = np.zeros((16, 16, 4))
    a[8:14, 7:9] = rgba((96, 64, 32)); a[7:9, 5:11] = rgba((120, 80, 40))
    F = hexs('f84010', 'f8a020', 'f8e070')
    ys, xs = np.mgrid[0:16, 0:16]
    for r_, c in ((3.5, F[0]), (2.4, F[1]), (1.2, F[2])):
        a[(((xs - 7.5) / (r_ * 0.8)) ** 2 + ((ys - 4.5) / r_) ** 2) <= 1] = rgba(c)
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba((40, 16, 8))
    return a


def inside_objects(O):
    def add(name, spr, w, h, solid=None, shadow=False, ay='b'):
        O[name] = dict(art=pad_cells(spr, w, h, ay=ay), w=w, h=h,
                       solid=set(solid if solid is not None else [(i, j) for i in range(w) for j in range(h)]),
                       beh={}, shadow=shadow)
    add('candle', candle_art(), 1, 2)
    add('portrait', portrait_art(), 1, 1)
    add('web', web_art(), 1, 1, solid=[], ay='t')
    add('web_r', web_art(True), 1, 1, solid=[], ay='t')
    add('pillar', pillar_art(), 1, 2)
    add('throne', throne_art(), 2, 2)
    add('coins', coins_art(1), 1, 1)
    add('coins2', coins_art(2), 1, 1)
    add('torch', torch_art(), 1, 1, solid=[])
    add('boo_carpet', carpet_art(BOO_CARPET, 2, 1), 2, 1, solid=[])
    add('fort_carpet', carpet_art(FORT_CARPET, 2, 1), 2, 1, solid=[])
    add('egg_box', egg_art((136, 56, 168)), 1, 1)
    add('hearth', hearth_art(), 2, 2)
    add('portrait_yoshi', yoshi_portrait_art(), 1, 1)


class Inside(YMap):
    """Binnenkaart: 'v' leegte (zwart), 'W' muur (noord), 'f' vloer, 'x' uitgangsmat (zuidpijl-warp)."""
    def __init__(self, name, W, H, floor_tex, wall_fn, floor_cols):
        super().__init__(name, W, H, fill='v')
        self.floor_tex, self.wall_fn, self.fc = floor_tex, wall_fn, floor_cols

    def render(self, O, seed):
        H, W = self.H * 16, self.W * 16
        T = self.T
        cv = np.zeros((H, W, 4)); cv[...] = rgba((0, 0, 0))
        fl = np.kron(np.isin(T, list('fx')), np.ones((16, 16), bool))
        cv[fl] = tiled(self.floor_tex, H, W)[fl]
        wl = np.kron(T == 'W', np.ones((16, 16), bool))
        self.wall_fn(cv, wl)
        # schaduw van de muur op de vloer (2 px, geditherd) en een donkere rand rond de vloer
        Y, X = np.mgrid[0:H, 0:W]
        under = np.zeros_like(wl); under[2:] = wl[:-2]; under[1:] |= wl[:-1]
        sh = fl & under & ((X + Y) % 2 == 0)
        cv[sh, :3] *= 0.6
        edge = outline_of(fl | wl)
        cv[edge & fl] = rgba(self.fc[0])
        for y, x in zip(*np.where(T == 'x')):                       # deurmat
            cv[y * 16 + 3:y * 16 + 13, x * 16 + 2:x * 16 + 14] = rgba(self.fc[0])
            cv[y * 16 + 4:y * 16 + 12, x * 16 + 3:x * 16 + 13] = rgba(self.fc[2])
        for name, x, y in sorted(self.objs, key=lambda o: o[2] + O[o[0]]['h']):
            o = O[name]
            stamp(cv, o['art'], x * 16, y * 16)
            self.objmask[y:y + o['h'], x:x + o['w']] = True
            for (dx, dy) in o['solid']:
                self.solid[y + dy, x + dx] = True
        self.solid |= np.isin(T, list('vW'))
        self.beh[T == 'x'] = MB['south_arrow']
        return cv


def boo_wall(cv, wl):
    bg = sheet('sma3_backgrounds_a.png')
    tex = bg[1040:1040 + 48, 6:262].copy(); tex[..., 3] = 255      # spookhuiswand, periode 256 px
    H, W = cv.shape[:2]
    ys, xs = np.where(wl)
    y0 = ys.min()
    cv[wl] = tex[(ys - y0) % 48, xs % 256]


def fort_wall(cv, wl):
    H, W = cv.shape[:2]
    t = tiled(tex_cobble(seed='fortmuur', cols=hexs('4c3824', '705034', '906c48', 'b08c60', '24180c', 'd8a060')), H, W)
    cv[wl] = t[wl]
    ys, xs = np.where(wl)
    top = ys.min()
    band = wl & (np.arange(H)[:, None] < top + 4)
    cv[band] = rgba((60, 44, 28))


BM_W, BM_H = 18, 14
BM_EXIT = (8, 13)
BM_BOO = (8, 5)


def boo_mansion_map():
    m = Inside('YoshisIsland_BooMansion', BM_W, BM_H, tex_planks(BOO_FLOOR, 'boo'), boo_wall, BOO_FLOOR)
    m.rect(1, 1, 16, 3, 'W')
    m.rect(1, 4, 16, 12, 'f')
    m.T[BM_EXIT[1], BM_EXIT[0]] = 'x'
    for y in range(6, 13, 1):
        m.put('boo_carpet', 8, y)
    for x in (3, 13):
        m.put('candle', x, 4)
    m.put('candle', 6, 4); m.put('candle', 10, 4)
    for x in (4, 8, 12):
        m.put('portrait', x, 2)
    m.put('web', 1, 1); m.put('web_r', 16, 1)
    m.put('candle', 1, 11); m.put('candle', 16, 11)
    m.put('egg_box', 2, 7); m.put('egg_box', 15, 6)
    return m


WF_W, WF_H = 18, 16
WF_EXIT = (8, 15)
WF_WARIO = (8, 5)
WF_GUARDS = [(8, 9), (9, 9)]


def wario_fort_map():
    m = Inside('YoshisIsland_WarioFort', WF_W, WF_H, tex_cobble(seed='vloer', cols=FORT_FLOOR), fort_wall, FORT_FLOOR)
    m.rect(1, 1, 16, 3, 'W')
    m.rect(1, 4, 16, 14, 'f')
    m.T[WF_EXIT[1], WF_EXIT[0]] = 'x'
    for y in range(5, 15):
        m.put('fort_carpet', 8, y)
    m.put('throne', 8, 3)
    for x in list(range(1, 8)) + list(range(10, 17)):
        if x in (1, 16):
            continue
        m.put('pillar', x, 8)
    m.put('pillar', 1, 8); m.put('pillar', 16, 8)
    for x, y in ((3, 4), (4, 5), (13, 4), (14, 5), (12, 6), (2, 6), (5, 4)):
        m.put('coins' if (x + y) % 2 else 'coins2', x, y)
    for x in (4, 13):
        m.put('torch', x, 2)
    return m


YH_FLOOR = hexs('8c5c30', 'b07840', 'c89058', '5c3818')
YH_W, YH_H = 14, 12
YH_EXIT = (6, 11)
YH_YOSHIS = [  # (kleur, x, y, bewegingstype)
    ('GREEN', 2, 5, 'MOVEMENT_TYPE_FACE_DOWN'), ('RED', 4, 5, 'MOVEMENT_TYPE_LOOK_AROUND'),
    ('YELLOW', 9, 5, 'MOVEMENT_TYPE_FACE_LEFT'), ('LIGHT_BLUE', 11, 5, 'MOVEMENT_TYPE_LOOK_AROUND'),
    ('PINK', 2, 8, 'MOVEMENT_TYPE_FACE_RIGHT'), ('PURPLE', 4, 8, 'MOVEMENT_TYPE_FACE_LEFT'),
    ('BROWN', 9, 8, 'MOVEMENT_TYPE_LOOK_AROUND'), ('BLACK', 11, 8, 'MOVEMENT_TYPE_FACE_LEFT'),
    ('WHITE', 3, 10, 'MOVEMENT_TYPE_FACE_UP'), ('BLUE', 10, 10, 'MOVEMENT_TYPE_FACE_UP'),
]


def hearth_art():
    """Open haard (2x2) in de muur, zoals in het huis van Yoshi in SMW: keien, zwarte opening, kampvuur erin."""
    a = np.zeros((32, 32, 4))
    st = tiled(tex_cobble(seed='haard', w=32, h=32, cols=hexs('707070', '909090', 'b0b0b0', 'd0d0d0', '303030', 'e0e0e0')), 32, 32)
    a[2:32, 1:31] = st[2:32, 1:31]
    ys, xs = np.mgrid[0:32, 0:32]
    hole = (ys >= 12) & (np.abs(xs - 15.5) <= 9) & ~((ys < 18) & (((xs - 15.5) / 9) ** 2 + ((ys - 18) / 6) ** 2 > 1))
    a[hole] = rgba((24, 16, 16))
    stamp(a, campfire_art(), 8, 16)
    a[0:3, 0:32] = rgba((96, 64, 40))
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba((32, 24, 16))
    return a


def yh_wall(cv, wl):
    H, W = cv.shape[:2]
    t = tiled(tex_planks(hexs('a87848', 'c89060', 'e0b080', '704820'), 'yoshiwand'), H, W)
    cv[wl] = t[wl]
    ys, xs = np.where(wl)
    top = ys.min()
    cv[wl & (np.arange(H)[:, None] >= ys.max() - 3)] = rgba((96, 64, 40))      # plint
    cv[wl & (np.arange(H)[:, None] < top + 3)] = rgba((72, 48, 28))


def yoshi_house_map():
    m = Inside('YoshisIsland_YoshiHouse', YH_W, YH_H, tex_planks(YH_FLOOR, 'yoshihuis'), yh_wall, YH_FLOOR)
    m.rect(1, 1, YH_W - 2, 3, 'W')
    m.rect(1, 4, YH_W - 2, YH_H - 2, 'f')
    m.T[YH_EXIT[1], YH_EXIT[0]] = 'x'
    m.put('hearth', 6, 2)
    for x, (name) in zip((1, 4, 9, 12), ('egg_green', 'egg_red', 'egg_yellow', 'egg_box')):
        m.put(name, x, 4)
    m.put('portrait_yoshi', 3, 2); m.put('portrait_yoshi', 10, 2)
    return m


# ====================================================================== uitbreiding: meer SMA3 (jungle, grot, bloemenveld)
# Bronnen: sma3_objects.png (A.J. Nitro: Message Block, ?-wolken, Chomp Rocks, eierblokken, POW, kisten, GOAL!),
# sma3_level1.png (p.k: krijttulpen, witte bloemetjes), sma3_backgrounds_a/b.png (jungle, kristalgrot).
OBJ_BG = (165, 235, 255)          # lichtblauwe achtergrond van de objectensheet
_SHEETS = {}


def sma(box, name='sma3_objects.png', bg=OBJ_BG, largest=False):
    if name not in _SHEETS:
        _SHEETS[name] = sheet(name)
    a = crop_obj(_SHEETS[name], box, bg)
    if largest:
        a = keep_largest(a)
    return trim(a)


# jungle: bladerdak (bovenkant van 'J'), lianenfranje en stammenwand
JT = hexs('2c5428', '3c7030', '64a040', '9cd060', '142810', 'f088a8', 'fff0f8')
FRJ = hexs('78b840', 'a8d860', 'd8f498', '4c8c30', '284c18', '0c1c08')
TRK = hexs('a86c34', 'd8a050', '603818', '2c1c10', 'f0c878', '1c3020')


def tex_canopy():
    """Bovenkant van een junglewand: dichte bladerclusters (zoals de SMA3-junglebomen) met roze bloemetjes."""
    t = np.zeros((P, P, 4)); t[...] = rgba(JT[0])
    r = rng('bladerdak')
    ys, xs = np.mgrid[0:P, 0:P]
    pts = [(r.uniform(0, P), r.uniform(0, P), r.uniform(3.6, 5.6)) for _ in range(16)]
    for cx, cy, rad in sorted(pts, key=lambda p: p[1]):
        for ox in (-P, 0, P):
            for oy in (-P, 0, P):
                d2 = ((xs - cx - ox) * 0.8) ** 2 + ((ys - cy - oy) * 1.2) ** 2
                m = d2 <= rad * rad
                if not m.any():
                    continue
                t[m] = rgba(JT[1])
                t[m & (d2 <= (rad * 0.6) ** 2) & (ys - cy - oy < 0)] = rgba(JT[2])
                t[m & (d2 <= (rad * 0.3) ** 2) & (ys - cy - oy < -1)] = rgba(JT[3])
                t[m & (d2 > (rad - 1.0) ** 2) & (ys - cy - oy > 0)] = rgba(JT[4])
    for (x, y) in ((7, 9), (23, 26)):
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            t[(y + dy) % P, (x + dx) % P] = rgba(JT[5])
        t[y, x] = rgba(JT[6])
    return t


def tex_trunks():
    """Zijwand van een junglewand: dicht opeen staande stammen met schors (uit de SMA3-junglebomen, bg-b)."""
    t = np.zeros((P, P, 4)); t[...] = rgba(TRK[5])
    for x0, w in ((1, 11), (17, 12)):
        t[:, x0:x0 + w] = rgba(TRK[0])
        t[:, x0 + 1:x0 + 4] = rgba(TRK[1])
        t[:, x0 + 2:x0 + 3] = rgba(TRK[4])
        t[:, x0 + w - 3:x0 + w] = rgba(TRK[2])
        t[:, x0] = rgba(TRK[3]); t[:, x0 + w - 1] = rgba(TRK[3])
        r = rng('schors', x0)
        for _ in range(5):
            y = r.integers(0, P); xx = x0 + r.integers(3, w - 3)
            t[y % P, xx] = rgba(TRK[2]); t[(y + 1) % P, xx] = rgba(TRK[2]); t[(y + 2) % P, xx + 1] = rgba(TRK[2])
        for y in (5, 21):                       # knoesten zoals op de bron
            t[y:y + 3, x0 + w // 2 - 1:x0 + w // 2 + 2] = rgba(TRK[2])
            t[y + 1, x0 + w // 2] = rgba(TRK[4])
    return t


# lucht onder het bloemenveld (de 'k'-kloof): blauw met wolkenrand
SKY = hexs('b0dcf8', 'c4e6fc', 'e0f2fe', '88bce8', 'ffffff', 'e8f4fc', '4878b8')


def tex_sky():
    t = crayon(SKY[0], [SKY[1], SKY[1], SKY[2]], 'lucht', n=14, lmin=3, lmax=6)
    r = rng('wolkjes')
    ys, xs = np.mgrid[0:P, 0:P]
    for _ in range(3):                          # kleine wolkjes diep beneden
        cx, cy = r.uniform(4, 28), r.uniform(4, 28)
        for k, (dx, rr) in enumerate(((-3, 2.6), (0, 3.4), (3.5, 2.6))):
            m = ((xs - cx - dx) ** 2 + ((ys - cy) * 1.3) ** 2) <= rr * rr
            t[m] = rgba(SKY[5])
            t[m & (ys < cy - 1)] = rgba(SKY[4])
    return t


def thorn_cell(var=0):
    """Doornstruik (SMA3-doorns): donkergroene ranken met witte stekels; vast, alleen Poochy loopt erdoor."""
    a = np.zeros((16, 16, 4))
    G = hexs('183818', '2c5c28', '4c8c3c', '0c180c', 'f8f8f0', 'c03048')
    ys, xs = np.mgrid[0:16, 0:16]
    for k, (cx, cy, rr) in enumerate(((4, 9, 4.6), (11, 6, 4.4), (9, 12, 4.0), (1, 3, 3.0), (15, 14, 3.0))):
        if var and k == 3:
            cx, cy = 13, 1
        m = ((xs - cx) ** 2 + (ys - cy) ** 2) <= rr * rr
        a[m] = rgba(G[1])
        a[m & (ys < cy - 1) & (xs < cx + 1)] = rgba(G[2])
        a[m & (ys > cy + rr * 0.4)] = rgba(G[0])
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba(G[3])
    r = rng('stekels', var)
    for _ in range(9):                           # stekels: wit puntje met donkere voet
        y, x = r.integers(1, 15, 2)
        if m[y, x]:
            a[y, x] = rgba(G[4])
            a[min(15, y + 1), x] = rgba(G[3])
    for (x, y) in ((6, 4), (12, 11)):            # rode besjes
        if m[y, x]:
            a[y, x] = rgba(G[5])
    return a


def bridge_art(h_cells):
    """Verticale brug van gestippelde SMA3-vlotjes (de groene 'flatbed ferry', gedraaid), 2 cellen breed."""
    f = sma((173, 524, 225, 536))                # 52x12 groen vlot
    f = np.rot90(f, 1).copy()                    # 12x52, verticaal
    a = np.zeros((h_cells * 16, 32, 4))
    y = 0
    while y < h_cells * 16:
        seg = f[:min(48, h_cells * 16 - y)]
        for dx in (3, 17):
            stamp(a, seg, dx, y)
        y += 48 - 4
    a[:, 15:17] = rgba((120, 72, 32))           # touw tussen de twee rijen vlotjes
    return a


def cave_mouth_art():
    """Grotingang (2x2) in SMA3-stijl: ronde keienboog uit de kasteelstenen, zwart gat, deur in de onderste rij."""
    a = np.zeros((32, 32, 4))
    ys, xs = np.mgrid[0:32, 0:32]
    cob = tiled(tex_cobble(seed='grotboog', w=64, h=32, cols=hexs('3c3c48', '5c5c6c', '7c7c90', '9c9cb0', '18181c', 'b0b0c8')), 32, 32)
    arch = (((xs - 15.5) / 15.5) ** 2 + ((ys - 20) / 19.0) ** 2 <= 1) | ((ys >= 20) & (np.abs(xs - 15.5) <= 15.5))
    a[arch] = cob[arch]
    hole = (((xs - 15.5) / 9.5) ** 2 + ((ys - 20) / 13.0) ** 2 <= 1) | ((ys >= 20) & (np.abs(xs - 15.5) <= 9.5))
    a[hole] = rgba((8, 8, 16))
    a[hole & (ys < 14)] = rgba((24, 24, 40))
    m = a[..., 3] > 0
    a[outline_of(m) & ~hole] = rgba((8, 8, 12))
    return a


def mushroom_art():
    """SMA3-paddenstoelplatform (2x2): rode hoed met witte stippen op een beige steel."""
    a = np.zeros((32, 32, 4))
    ys, xs = np.mgrid[0:32, 0:32]
    stem = (ys >= 14) & (np.abs(xs - 15.5) <= 5.5)
    a[stem] = rgba((240, 216, 168)); a[stem & (xs > 17)] = rgba((208, 176, 120))
    cap = (((xs - 15.5) / 15.0) ** 2 + ((ys - 12) / 10.0) ** 2 <= 1) & (ys <= 16)
    a[cap] = rgba((216, 48, 40)); a[cap & (ys < 6)] = rgba((240, 104, 88))
    for (cx, cy, rr) in ((9, 8, 2.6), (20, 6, 2.2), (16, 12, 2.4), (25, 12, 1.8), (6, 13, 1.6)):
        a[cap & (((xs - cx) ** 2 + (ys - cy) ** 2) <= rr * rr)] = rgba((248, 248, 240))
    a[(ys >= 15) & (ys <= 16) & cap] = rgba((150, 24, 24))
    m = a[..., 3] > 0
    a[outline_of(m)] = rgba((40, 12, 8))
    return a


def goal_art():
    """GOAL! uit de objectensheet (de letters van het eind van elk SMA3-level), 12x3 cellen."""
    boxes = ((5, 1585, 41, 1633), (46, 1585, 84, 1633), (89, 1585, 126, 1633), (131, 1585, 166, 1633), (171, 1586, 184, 1633))
    parts = [sma(b) for b in boxes]
    W_ = sum(p.shape[1] for p in parts) + 3 * (len(parts) - 1)
    a = np.zeros((48, W_, 4))
    x = 0
    for p_ in parts:
        stamp(a, p_, x, 48 - p_.shape[0]); x += p_.shape[1] + 3
    return a


def message_block_art():
    return sma((47, 454, 63, 470))


def sma3_objects(O):
    def add(name, spr, w, h, solid=None, beh=None, ay='b', shadow=True, dy=0):
        a = pad_cells(spr, w, h, 'c', ay, 0, dy)
        if solid is None:
            solid = [(i, j) for i in range(w) for j in range(h)]
        O[name] = dict(art=a, w=w, h=h, solid=set(solid), beh=beh or {}, shadow=shadow)
    L1 = 'sma3_level1.png'
    add('msgblock', message_block_art(), 1, 1)                       # het blije blok = bordje
    add('eggblock', sma((5, 389, 21, 405)), 1, 1)                    # eierblok (groen)
    add('eggblock_red', sma((5, 410, 21, 426)), 1, 1)
    add('switch_red', sma((173, 498, 193, 519)), 2, 2, solid=[(0, 1), (1, 1)])
    add('crate', sma((93, 438, 124, 466)), 2, 2)
    add('stake', sma((94, 385, 124, 433)), 2, 3, solid=[(0, 2), (1, 2), (0, 1), (1, 1)])
    add('chomp_grey', sma((5, 1066, 37, 1098)), 2, 2)                 # Chomp Rocks (rotsen met gezichtjes)
    add('chomp_brown', sma((42, 1066, 74, 1098)), 2, 2)
    add('pow', sma((126, 975, 158, 1003)), 2, 2)
    add('qpot', sma((192, 1067, 220, 1098)), 2, 2)
    add('bluerock', sma((5, 1190, 37, 1222)), 2, 2)
    add('pinkrock', sma((5, 1227, 37, 1259)), 2, 2)
    add('flowerpot', sma((5, 725, 36, 775)), 2, 4, solid=[(0, 3), (1, 3), (0, 2), (1, 2)])
    bs = sma((194, 653, 226, 685))
    add('bigsmiley', trim(key_out(bs, tuple(bs[0, 0, :3]), 40)), 2, 2)          # zonnebloem zonder haar vierkantje
    add('smiley_big2', sma((5, 780, 37, 812)), 2, 2)
    add('piranha_tulip', sma((47, 698, 63, 721)), 1, 2, solid=[(0, 1)])
    add('tulip_big', sma((19, 523, 51, 555), L1, (255, 255, 255)), 2, 2)
    add('tulip_big2', sma((64, 522, 96, 552), L1, (255, 255, 255)), 2, 2)
    add('whiteflowers', sma((108, 532, 123, 546), L1, (255, 255, 255)), 1, 1, solid=[], shadow=False)
    add('whiteflowers2', sma((136, 530, 152, 546), L1, (255, 255, 255)), 1, 1, solid=[], shadow=False)
    add('lizard', sma((239, 529, 255, 543), L1, (255, 255, 255)), 1, 1, solid=[], shadow=False)
    add('goal', goal_art(), 12, 3)
    add('cave_mouth', cave_mouth_art(), 2, 2, solid=[(0, 0), (1, 0)], beh={(0, 1): MB['door'], (1, 1): MB['door']},
        shadow=False)
    add('mushroom', mushroom_art(), 2, 2)
    # het oude houten bordje wordt overal een Message Block
    O['sign'] = O['msgblock']


def _sky(self, cv, seed):
    """'k': de lucht onder het bloemenveld (je staat op de wolken). Rand = witte wolkenfranje, daarbinnen diep blauw."""
    T = self.T
    sky = T == 'k'
    if not sky.any():
        return
    H, W = cv.shape[:2]
    sd = sdist(sky) + edge_noise(('lucht', seed), H, W, 2.5)
    m = sd > 0.5
    cv[m] = tiled(tex_sky(), H, W)[m]
    hi = tiled(np.dstack([vnoise(('wolkrand', seed), P, 8)] * 4), H, W)[..., 0]
    band = m & (sd < 5.0 + hi * 3)
    cv[band] = rgba(SKY[4])
    cv[band & (hi < 0.35)] = rgba(SKY[5])
    cv[outline_of(band) & m & ~outline_of(m)] = rgba(SKY[2])
    cv[outline_of(m)] = rgba(SKY[6])


YMap._sky = _sky


# ====================================================================== kaart 5: de jungle (via de pijp oost op het strand)
JW, JH = 40, 30
J_PIPE = (19, 25)                    # pijp terug naar het strand (onderste rij = warp)
J_PIPE2 = (35, 15)                   # pijp naar het bloemenveld
J_CAVE = (19, 2)                     # grotingang 2x2, deuren in de onderste rij (19-20, 3)
J_POOCHY = (10, 8)                   # Poochy staat op de oostelijkste doorn (T1); de rit gaat over rij 8
J_THORN = (8, 10, 8)                 # doorns x 8-10 op rij 8 (T0, T1, rij)
J_NEP = (32, 10)                     # Nep-Enut (128x128) IN het meertje; voetafdruk x 30-34 op deze rij, aanspreken vanaf de oever
J_SHY = (21, 15)                     # Shy Guy-trainer naast het pad
J_CLOUD = (4, 10)                    # ?-wolk in het verborgen bosje
J_MSG = [(17, 23), (13, 9), (26, 13)]


def jungle_map():
    m = YMap('YoshisIsland_Jungle', JW, JH)
    m.rect(0, 0, JW - 1, 4, 'J'); m.rect(0, 0, 1, JH - 1, 'J'); m.rect(JW - 2, 0, JW - 1, JH - 1, 'J')
    m.rect(0, JH - 2, JW - 1, JH - 1, 'J')
    # verborgen bosje (west), alleen via de doorns met Poochy
    m.rect(7, 5, 12, 7, 'J'); m.rect(7, 9, 12, 14, 'J'); m.rect(2, 13, 12, 14, 'J')
    t0, t1, ty = J_THORN
    m.rect(t0, ty, t1, ty, 'n')
    # meertje (noordoost) met zandoever; de jungle sluit het af
    m.rect(22, 5, 26, 9, 'J')
    m.rect(27, 11, 37, 13, 's')
    m.rect(27, 5, 37, 10, 'w')
    # middenblokken voor wat reliëf
    m.rect(8, 15, 11, 16, 'J'); m.rect(26, 15, 29, 16, 'J')
    # grotingang in de noordwand
    m.rect(J_CAVE[0], J_CAVE[1] + 1, J_CAVE[0] + 1, 4, 'p')
    # paden
    m.rect(19, 5, 20, 24, 'p'); m.rect(12, 8, 18, 8, 'p'); m.rect(21, 18, 34, 18, 'p'); m.rect(33, 14, 34, 17, 'p')
    # hoog gras
    m.rect(3, 17, 15, 24, 't'); m.rect(22, 20, 31, 25, 't'); m.rect(13, 10, 17, 13, 't'); m.rect(30, 21, 36, 24, 't')
    m.rect(3, 6, 5, 7, 't')
    # objecten
    m.put('pipe', *J_PIPE); m.put('pipe', *J_PIPE2)
    m.put('cave_mouth', *J_CAVE)
    for x, y in ((3, 15), (17, 15), (23, 15), (35, 19), (17, 25), (33, 25)):    # zelfde pariteit: ontdubbelt
        m.put('palm', x, y)
    m.put('chomp_brown', 12, 18)
    m.put('tulip_big', 6, 25); m.put('tulip_big', 27, 26)
    m.put('piranha_tulip', 18, 10); m.put('piranha_tulip', 21, 6); m.put('piranha_tulip', 2, 9)
    m.put('crate', 22, 10); m.put('stake', 15, 5)
    m.put('eggblock', 18, 6)
    for x, y in J_MSG:
        m.put('msgblock', x, y)
    for x, y in ((18, 13), (21, 23), (16, 17), (34, 13), (5, 11), (28, 13), (21, 4)):
        m.put('smiley', x, y)
    for x, y in ((18, 21), (21, 20), (3, 12), (30, 12), (17, 19)):
        m.put('whiteflowers' if (x + y) % 2 else 'whiteflowers2', x, y)
    m.put('lizard', 25, 17)
    m.elev0 = {J_NEP}
    return m


# ====================================================================== kaart 6: Shy Guy-kristalgrot (achter de grotingang in de jungle)
CW, CH = 24, 17
C_EXIT = (11, 16)
C_SHY = (16, 12)
C_MSG = (10, 5)


def crystal_wall(cv, wl):
    bg = sheet('sma3_backgrounds_a.png')
    tex = bg[462:462 + 48, 6:262].copy(); tex[..., 3] = 255       # kristalgrot (bg-a, rij 2), periode 256 px
    ys, xs = np.where(wl)
    y0 = ys.min()
    cv[wl] = tex[(ys - y0) % 48, xs % 256]


CAVE_FLOOR = hexs('34303c', '4c4658', '686078', '201c28', '8c84a0', 'a8a0c0')


def cave_map():
    m = Inside('YoshisIsland_Cave', CW, CH, tex_cobble(seed='grotvloer', cols=CAVE_FLOOR), crystal_wall, CAVE_FLOOR)
    m.rect(1, 1, CW - 2, 3, 'W')
    m.rect(1, 4, CW - 2, 15, 'f')
    m.T[C_EXIT[1], C_EXIT[0]] = 'x'
    # kristalblokken en Chomp Rocks als pilaren
    m.put('bluerock', 5, 8); m.put('pinkrock', 15, 7); m.put('bluerock', 8, 12); m.put('chomp_grey', 17, 7)
    m.put('chomp_grey', 2, 5); m.put('chomp_brown', 19, 9)
    m.put('bluerock', 20, 4); m.put('pinkrock', 2, 13); m.put('bluerock', 12, 9)
    m.put('eggblock', 13, 4); m.put('eggblock_red', 14, 4)
    m.put('qpot', 4, 4)
    m.put('msgblock', *C_MSG)
    m.put('pow', 20, 13)
    m.put('torch', 6, 3); m.put('torch', 17, 3)
    return m


# ====================================================================== kaart 7: het bloemenveld boven de wolken (via de jungle)
FW, FH = 36, 30
F_PIPE = (17, 25)
F_BRIDGE = (17, 11, 4)               # x (2 breed), bovenste rij, hoogte in rijen
F_BRIDGE_CLOUD = (20, 15)
F_CLOUD = (27, 18)
F_SHY = (9, 20)
F_MSG = [(15, 24), (15, 8), (21, 16)]
F_SWITCH = (28, 23)


def flowers_map():
    m = YMap('YoshisIsland_Flowers', FW, FH)
    m.rect(0, 0, FW - 1, 1, 'k'); m.rect(0, 0, 1, FH - 1, 'k'); m.rect(FW - 2, 0, FW - 1, FH - 1, 'k')
    m.rect(0, FH - 2, FW - 1, FH - 1, 'k')
    bx, by, bh = F_BRIDGE
    m.rect(0, by, FW - 1, by + bh - 1, 'k')                   # de kloof (de brug verschijnt via de ?-wolk)
    # golvende wolkenranden
    for x, y in ((2, 2), (3, 2), (33, 3), (2, 27), (32, 27), (10, 10), (11, 10), (26, 15), (27, 15)):
        m.T[y, x] = 'k'
    # paden
    m.rect(17, 15, 18, 24, 'p'); m.rect(17, 6, 18, 10, 'p'); m.rect(10, 8, 25, 9, 'p')
    m.rect(8, 22, 16, 22, 'p'); m.rect(19, 19, 28, 19, 'p')
    # hoog gras (bloemenweide)
    m.rect(3, 16, 12, 20, 't'); m.rect(22, 21, 31, 25, 't'); m.rect(4, 23, 13, 26, 't'); m.rect(26, 3, 31, 6, 't')
    m.put('pipe', *F_PIPE)
    m.put('goal', 12, 2)
    m.put('flowerpot', 5, 3)
    m.put('bigsmiley', 3, 7); m.put('smiley_big2', 29, 8)
    m.put('tulip_big', 8, 6); m.put('tulip_big2', 24, 5)
    m.put('mushroom', 23, 15)
    m.put('tulip_big', 13, 16)
    m.put('eggblock', 13, 19); m.put('eggblock_red', 24, 17)
    m.put('switch_red', *F_SWITCH)
    for x, y in F_MSG:
        m.put('msgblock', x, y)
    for x, y in ((16, 17), (19, 21), (11, 23), (25, 20), (20, 7), (9, 9), (27, 9), (14, 6), (6, 18), (31, 20)):
        m.put('smiley', x, y)
    for x, y in ((16, 20), (19, 24), (12, 7), (23, 8)):
        m.put('whiteflowers' if (x + y) % 2 else 'whiteflowers2', x, y)
    for x, y in ((16, 21), (20, 22), (19, 7)):
        m.put('tulip' if (x + y) % 2 else 'tulip_pink', x, y)
    return m


def bridge_cells(m, cv):
    """De brugcellen (los getekend over de kloof) -> {(x, y): 16x16 RGBA}; die gaan als extra metatiles in de
    secondary van het bloemenveld, setmetatile zet ze neer als de ?-wolk knapt."""
    bx, by, bh = F_BRIDGE
    cv2 = cv.copy()
    stamp(cv2, bridge_art(bh + 2), bx * 16, (by - 1) * 16)    # loopt een halve cel door op de oevers
    out = {}
    for y in range(by, by + bh):
        for x in (bx, bx + 1):
            out[(x, y)] = cv2[y * 16:y * 16 + 16, x * 16:x * 16 + 16]
    return out


# ====================================================================== flags (FLAG_GROUNDED 1024-1119)
FLAGS = [
    (1024, 'FLAG_YI_ARRIVED', "Yoshi's Island: aankomstscene gezien (uit de lucht gevallen, Yoshi gevonden)"),
    (1025, 'FLAG_YI_BEACH_GUARDS', "Yoshi's Island: de twee Shy Guys bij de pijp verslagen (multi battle 1)"),
    (1026, 'FLAG_YI_CAMP_A', "Yoshi's Island: bende A in het Shy Guy-kamp verslagen (multi battle 2)"),
    (1027, 'FLAG_YI_CAMP_B', "Yoshi's Island: bende B voor het spookhuis verslagen (multi battle 3)"),
    (1028, 'FLAG_YI_BOO_DONE', "Yoshi's Island: Commander Boo verslagen (de fortwachter vlucht)"),
    (1029, 'FLAG_YI_FORT_GUARDS', "Yoshi's Island: de twee fortwachters verslagen (multi battle 4)"),
    (1030, 'FLAG_YI_WARIO_DONE', "Yoshi's Island: Wario verslagen (zet ook FLAG_SPACETIME_YOSHI_DONE)"),
    (1031, 'FLAG_YI_PECHARUNT_DONE', "Yoshi's Island: Pecharunt gevangen (of verslagen; komt dan terug)"),
    (1032, 'FLAG_YI_YOSHI_AHEAD', "Yoshi's Island: Yoshi is vooruit de pijp in (verbergt Yoshi op het strand)"),
    (1033, 'FLAG_YI_YOSHI_HOME', "Yoshi's Island: quest klaar, Yoshi wacht op het strand (verbergt hem elders)"),
    (1040, 'FLAG_ITEM_YOSHIS_ISLAND_BEACH_HONEY', "Yoshi's Island strand: Honey"),
    (1041, 'FLAG_ITEM_YOSHIS_ISLAND_BEACH_HEAL_BALL', "Yoshi's Island strand: Heal Ball"),
    (1042, 'FLAG_HIDDEN_ITEM_YOSHIS_ISLAND_BEACH_EXP_CANDY_XS', "Yoshi's Island strand: verborgen Exp. Candy XS"),
    (1043, 'FLAG_ITEM_YOSHIS_ISLAND_HILLS_LAGGING_TAIL', "Yoshi's Island heuvels: Lagging Tail"),
    (1044, 'FLAG_ITEM_YOSHIS_ISLAND_HILLS_TOXIC_PLATE', "Yoshi's Island heuvels: Toxic Plate (bij Pecharunts kraampje)"),
    (1045, 'FLAG_HIDDEN_ITEM_YOSHIS_ISLAND_HILLS_STICKY_BARB', "Yoshi's Island heuvels: verborgen Sticky Barb"),
    (1046, 'FLAG_ITEM_YOSHIS_ISLAND_BOO_MANSION_FLOAT_STONE', "Yoshi's Island spookhuis: Float Stone"),
    (1047, 'FLAG_ITEM_YOSHIS_ISLAND_BOO_MANSION_POKE_DOLL', "Yoshi's Island spookhuis: Poke Doll"),
    (1048, 'FLAG_ITEM_YOSHIS_ISLAND_WARIO_FORT_GRIP_CLAW', "Yoshi's Island fort: Grip Claw"),
    (1049, 'FLAG_ITEM_YOSHIS_ISLAND_WARIO_FORT_MALICIOUS_ARMOR', "Yoshi's Island fort: Malicious Armor"),
    (1050, 'FLAG_YI_NEP_ENUT_DONE', "Yoshi's Island jungle: Nep-Enut (het watermonster in het meertje, een Dondozo) verslagen of gevangen"),
    (1051, 'FLAG_YI_POOCHY_DUG', "Yoshi's Island jungle: Poochy heeft in het bosje iets opgegraven"),
    (1052, 'FLAG_YI_BRIDGE_CLOUD', "Yoshi's Island bloemenveld: ?-wolk geknapt, de brug over de kloof ligt er"),
    (1053, 'FLAG_YI_STAR_CLOUD', "Yoshi's Island heuvels: ?-wolk met de sterrenregen geknapt"),
    (1054, 'FLAG_YI_POOCHY_MET', "Yoshi's Island jungle: Poochy leren kennen (korte uitleg alleen de eerste keer)"),
]
NI_RANGE = (1060, 1069)   # items die nergens anders liggen: via nieuwe_items.py (eigen blok in flags.h)
F_FIRST, F_LAST = 1024, 1119


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = ("// yoshis_island { (tools/grounded/maptools/yoshis_island.py; FLAG_GROUNDED %d-%d; %d-%d = nieuwe items "
           "(blok nieuwe_items), %d-%d en %d-%d nog vrij)\n" % (F_FIRST, F_LAST, NI_RANGE[0], NI_RANGE[1],
                                                               max(n for n, *_ in FLAGS) + 1, NI_RANGE[0] - 1,
                                                               NI_RANGE[1] + 1, F_LAST))
    for n, name, why in FLAGS:
        assert F_FIRST <= n <= F_LAST
        blk += '#define %-52s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// yoshis_island {' in s:
        i = s.index('// yoshis_island {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// national_park {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== mapsec
def mapsecs():
    p = 'src/data/region_map/region_map_sections.json'
    s = open(p).read()
    mid = 'MAPSEC_YOSHIS_ISLAND'
    if '"%s"' % mid not in s:
        i = s.rindex('    }\n  ]')
        s = s[:i + 5] + ',\n    {\n      "id": "%s",\n      "name": "YOSHI\'S ISLAND"\n    }' % mid + s[i + 5:]
    json.loads(s)
    open(p, 'w').write(s)
    p = 'src/map_name_popup.c'
    s = open(p).read()
    a = '    [MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_STONE, // Project Grounded: Spacetime Cave\n'
    b = '    [MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: Spacetime Cave\n'
    assert a in s and b in s
    if '[%s - KANTO' % mid not in s:
        s = s.replace(a, a + "    [%s - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_WOOD, // Project Grounded: Yoshi's Island\n" % mid, 1)
        s = s.replace(b, b + "    [%s - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: Yoshi's Island\n" % mid, 1)
    open(p, 'w').write(s)


# ====================================================================== wilde Pokemon (post-game, lv 91-93)
WILD = {  # levels per evolutiefase (v0.9.202): eindvormen 80-90, sterke soorten (BST >= 580) 90-94
    'YOSHIS_ISLAND_BEACH': dict(
        land=(18, [('TROPIUS', 86, 88), ('EXEGGUTOR_ALOLA', 88, 90), ('BELLOSSOM', 87, 89), ('JUMPLUFF', 84, 86),
                   ('TOUCANNON', 86, 88), ('CRAMORANT', 85, 87), ('ORICORIO_POM_POM', 85, 87), ('PALOSSAND', 86, 88),
                   ('LUDICOLO', 87, 88), ('COMFEY', 86, 87), ('BRELOOM', 85, 86), ('SLAKING', 93, 93)]),
        water=(4, [('SEAKING', 87, 89), ('PELIPPER', 83, 85), ('OCTILLERY', 87, 89), ('MANTINE', 86, 87),
                   ('LAPRAS', 89, 89)])),
    'YOSHIS_ISLAND_HILLS': dict(
        land=(18, [('CARNIVINE', 84, 86), ('DUGTRIO', 82, 84), ('ELECTRODE', 88, 90), ('AMOONGUSS', 85, 87),
                   ('DRIFBLIM', 87, 89), ('VILEPLUME', 87, 89), ('MR_MIME', 84, 86), ('LICKILICKY', 88, 90),
                   ('MIMIKYU', 85, 86), ('MISMAGIUS', 86, 87), ('TOGEKISS', 89, 90), ('SNORLAX', 89, 89)])),
    # jungle: Ukiki-apen, Piranha-planten en junglekevers; het meertje heeft de vissen die Nep-Enut niet opat
    'YOSHIS_ISLAND_JUNGLE': dict(
        land=(18, [('AMBIPOM', 84, 86), ('PASSIMIAN', 84, 86), ('VICTREEBEL', 86, 88), ('LEAVANNY', 85, 87),
                   ('LURANTIS', 84, 86), ('TANGROWTH', 87, 89), ('HERACROSS', 85, 87), ('ORANGURU', 84, 86),
                   ('TSAREENA', 86, 88), ('SCOLIPEDE', 87, 89), ('RILLABOOM', 89, 90), ('DECIDUEYE', 89, 90)]),
        water=(4, [('POLITOED', 85, 87), ('QUAGSIRE', 84, 86), ('ARAQUANID', 85, 87), ('BARRASKEWDA', 86, 88),
                   ('SWAMPERT', 89, 90)])),
    # kristalgrot: Fang-vleermuizen, Chomp Rocks en de mijnwerkers van de Shy Guys
    'YOSHIS_ISLAND_CAVE': dict(
        land=(10, [('CROBAT', 86, 88), ('SWOOBAT', 84, 86), ('GOLEM', 87, 89), ('GIGALITH', 86, 88),
                   ('CRUSTLE', 84, 86), ('PROBOPASS', 86, 88), ('SABLEYE', 84, 86), ('MAWILE', 84, 86),
                   ('EXCADRILL', 87, 89), ('BRONZONG', 86, 88), ('NOIVERN', 89, 90), ('GARGANACL', 89, 90)])),
    # bloemenveld boven de wolken
    'YOSHIS_ISLAND_FLOWERS': dict(
        land=(18, [('FLORGES', 86, 88), ('LILLIGANT', 85, 87), ('WHIMSICOTT', 84, 86), ('BEAUTIFLY', 82, 84),
                   ('VESPIQUEN', 84, 86), ('RIBOMBEE', 84, 86), ('SAWSBUCK', 85, 87), ('GOGOAT', 85, 87),
                   ('ALTARIA', 86, 88), ('CASTFORM', 82, 84), ('MEGANIUM', 89, 90), ('ARBOLIVA', 89, 90)])),
}


# ====================================================================== trainers + partner
TRAINERS = []          # gevuld in trainer_data() (bd.mon nodig)
SHY_PICS = {'red': 'Guest Shy Guy Red', 'green': 'Guest Shy Guy Green', 'pink': 'Guest Shy Guy Pink',
            'black': 'Guest Shy Guy Black'}
SHY_GFX = {c: 'OBJ_EVENT_GFX_SHY_GUY_' + c.upper() for c in SHY_PICS}


def trainer_data():
    mon = bd.mon
    IV = 'IVs: 28 HP / 28 Atk / 28 Def / 28 SpA / 28 SpD / 28 Spe'
    AI, AIB = bd.AI, bd.AI_BOSS

    def m(head, lvl, moves, ab=None):
        return mon(head, lvl, moves, ab, IV)
    T = [  # (sleutel, id, naam, klasse, foto, muziek, ai, items, team, kleur, omschrijving)
        ('YI_SHY_GUY_BEACH_A', 1017, 'SHY GUY', 'Shy Squad', SHY_PICS['red'], 'Suspicious', AI, None, [
            m('Mr. Mime', 92, ['Psychic', 'Dazzling Gleam', 'Reflect', 'Light Screen'], 'Filter'),
            m('Mimikyu', 92, ['Play Rough', 'Shadow Claw', 'Shadow Sneak', 'Swords Dance'])], 'red', 'strand, pijpwachter 1'),
        ('YI_SHY_GUY_BEACH_B', 1018, 'SHYER GUY', 'Shy Squad', SHY_PICS['green'], 'Suspicious', AI, None, [
            m('Breloom', 92, ['Spore', 'Seed Bomb', 'Mach Punch', 'Rock Tomb']),
            m('Amoonguss', 92, ['Spore', 'Giga Drain', 'Sludge Bomb', 'Clear Smog'])], 'green', 'strand, pijpwachter 2'),
        ('YI_SHY_GUY_CAMP_A1', 1019, 'FLY GUY', 'Shy Squad', SHY_PICS['pink'], 'Suspicious', AI, None, [
            m('Jumpluff', 93, ['Sleep Powder', 'Acrobatics', 'Leech Seed', 'U-turn']),
            m('Altaria', 93, ['Dragon Pulse', 'Moonblast', 'Cotton Guard', 'Roost']),
            m('Togekiss', 93, ['Air Slash', 'Dazzling Gleam', 'Aura Sphere', 'Roost'])], 'pink', 'kamp, bende A'),
        ('YI_SHY_GUY_CAMP_A2', 1026, 'SHADY GUY', 'Shy Squad', SHY_PICS['black'], 'Suspicious', AI, None, [
            m('Zoroark', 93, ['Night Daze', 'Flamethrower', 'Focus Blast', 'Nasty Plot']),
            m('Liepard', 93, ['Knock Off', 'U-turn', 'Play Rough', 'Fake Out']),
            m('Honchkrow', 93, ['Brave Bird', 'Sucker Punch', 'Heat Wave', 'Roost'])], 'black', 'kamp, bende A'),
        ('YI_SHY_GUY_CAMP_B1', 1027, 'SPEAR GUY', 'Shy Squad', SHY_PICS['red'], 'Suspicious', AI, None, [
            m("Sirfetch'd", 93, ['Leaf Blade', 'Close Combat', 'Brave Bird', 'Knock Off']),
            m('Escavalier', 93, ['Megahorn', 'Iron Head', 'Drill Run', 'Swords Dance']),
            m('Gallade', 93, ['Sacred Sword', 'Psycho Cut', 'Leaf Blade', 'Swords Dance'])], 'red', 'heuvels, bende B (spookhuis)'),
        ('YI_SHY_GUY_CAMP_B2', 1028, 'SNIFIT', 'Shy Squad', SHY_PICS['green'], 'Suspicious', AI, None, [
            m('Octillery', 93, ['Octazooka', 'Fire Blast', 'Ice Beam', 'Gunk Shot']),
            m('Inteleon', 93, ['Snipe Shot', 'Ice Beam', 'U-turn', 'Dark Pulse']),
            m('Clawitzer', 93, ['Water Pulse', 'Dark Pulse', 'Aura Sphere', 'Dragon Pulse'])], 'green', 'heuvels, bende B (spookhuis)'),
        ('YI_COMMANDER_BOO', 1029, 'BOO', 'Commander', 'Guest Boo', 'Suspicious', AIB, 'Full Restore / Full Restore', [
            m('Drifblim', 94, ['Shadow Ball', 'Air Slash', 'Will-O-Wisp', 'Destiny Bond']),
            m('Froslass', 94, ['Shadow Ball', 'Ice Beam', 'Spikes', 'Destiny Bond']),
            m('Spiritomb', 94, ['Foul Play', 'Shadow Sneak', 'Will-O-Wisp', 'Pain Split']),
            m('Polteageist', 94, ['Shell Smash', 'Shadow Ball', 'Giga Drain', 'Stored Power']),
            m('Dusknoir', 95, ['Poltergeist', 'Shadow Sneak', 'Ice Punch', 'Earthquake']),
            m('Dragapult @ Choice Band', 96, ['Dragon Darts', 'Phantom Force', 'U-turn', 'Sucker Punch'])],
         None, 'spookhuis, baas'),
        ('YI_SHY_GUY_FORT_A', 1049, 'NINJA GUY', 'Shy Squad', SHY_PICS['black'], 'Suspicious', AI, None, [
            m('Greninja', 94, ['Hydro Pump', 'Dark Pulse', 'Ice Beam', 'Gunk Shot']),
            m('Kingambit', 94, ['Kowtow Cleave', 'Iron Head', 'Sucker Punch', 'Swords Dance']),
            m('Scizor', 94, ['Bullet Punch', 'U-turn', 'Knock Off', 'Swords Dance'])], 'black', 'fort, wachter'),
        ('YI_SHY_GUY_FORT_B', 1055, 'BOUNCER', 'Shy Squad', SHY_PICS['pink'], 'Suspicious', AI, None, [
            m('Bewear', 94, ['Hammer Arm', 'Double-Edge', 'Payback', 'Bulk Up']),
            m('Gholdengo', 94, ['Make It Rain', 'Shadow Ball', 'Nasty Plot', 'Recover']),
            m('Hatterene', 94, ['Dazzling Gleam', 'Psychic', 'Mystical Fire', 'Trick Room'])], 'pink', 'fort, wachter'),
        ('YI_WARIO', 1056, 'WARIO', 'Boss', 'Guest Wario', 'Rich', AIB, 'Full Restore / Full Restore', [
            m('Grafaiai @ Focus Sash', 95, ['Encore', 'Knock Off', 'Super Fang', 'U-turn'], 'Prankster'),
            m('Sableye @ Leftovers', 95, ['Will-O-Wisp', 'Knock Off', 'Recover', 'Foul Play'], 'Prankster'),
            m('Perrserker @ Life Orb', 95, ['Iron Head', 'Close Combat', 'Fake Out', 'Pay Day'], 'Tough Claws'),
            m('Garbodor @ Rocky Helmet', 95, ['Gunk Shot', 'Toxic Spikes', 'Drain Punch', 'Spikes']),
            m('Muk_Alola @ Assault Vest', 96, ['Knock Off', 'Poison Jab', 'Drain Punch', 'Ice Punch'], 'Poison Touch'),
            m('Hariyama @ Choice Band', 97, ['Close Combat', 'Headlong Rush', 'Knock Off', 'Bullet Punch'])],
         None, 'fort, eindbaas'),
        # gewone Shy Guy-trainers (Jordi: Shy Guys worden trainers); ze praten nog steeds niet
        ('YI_SHY_GUY_JUNGLE', 1109, 'JUNGLE GUY', 'Shy Squad', SHY_PICS['green'], 'Suspicious', AI, None, [
            m('Ambipom', 93, ['Fake Out', 'Double Hit', 'U-turn', 'Knock Off']),
            m('Lurantis', 93, ['Leaf Blade', 'X-Scissor', 'Superpower', 'Swords Dance']),
            m('Toucannon', 93, ['Beak Blast', 'Bullet Seed', 'Rock Blast', 'Roost'])], 'green', 'jungle, naast het pad'),
        ('YI_SHY_GUY_CAVE', 1129, 'MINER GUY', 'Shy Squad', SHY_PICS['black'], 'Suspicious', AI, None, [
            m('Excadrill', 93, ['Earthquake', 'Iron Head', 'Rock Slide', 'Swords Dance']),
            m('Gigalith', 93, ['Stone Edge', 'Heavy Slam', 'Earthquake', 'Stealth Rock']),
            m('Crobat', 93, ['Brave Bird', 'Cross Poison', 'U-turn', 'Roost'])], 'black', 'kristalgrot, mijnwerker'),
        ('YI_SHY_GUY_FLOWERS', 1183, 'GROOVY GUY', 'Shy Squad', SHY_PICS['pink'], 'Suspicious', AI, None, [
            m('Florges', 93, ['Moonblast', 'Petal Blizzard', 'Calm Mind', 'Synthesis']),
            m('Altaria', 93, ['Dragon Pulse', 'Moonblast', 'Hurricane', 'Roost']),
            m('Whimsicott', 93, ['Moonblast', 'Energy Ball', 'Tailwind', 'Encore']),
            m('Lilligant', 94, ['Petal Dance', 'Quiver Dance', 'Sleep Powder', 'Hurricane'])], 'pink',
         'bloemenveld, flowerpower'),
    ]
    TRAINERS[:] = T
    return T


def trainers():
    trainer_data()
    p = 'include/constants/opponents.h'
    s = open(p).read()
    ids = ', '.join(str(t[1]) for t in TRAINERS)
    blk = '// yoshis_island { (tools/grounded/maptools/yoshis_island.py; id %s)\n' % ids
    for key, n, *_, why in TRAINERS:
        blk += "#define TRAINER_%-28s%d // Project Grounded: Yoshi's Island, %s\n" % (key, n, why)
    blk += '// }'
    if '// yoshis_island {' in s:
        i = s.index('// yoshis_island {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for key, n, *_ in TRAINERS:
        hits = re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)
        assert len(hits) == 1, ('trainer-id dubbel', n, hits)
        assert n < 1200
    open(p, 'w').write(s)
    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- yoshis_island (tools/grounded/maptools/yoshis_island.py) --- */\n\n'
    for key, n, nm, cls, pic, music, ai, items, team, col, why in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: Male', 'Music: ' + music]
        if items:
            hdr.append('Items: ' + items)
        hdr += ['Double Battle: No', ai]
        if key in ('YI_COMMANDER_BOO', 'YI_WARIO'):
            hdr.append('Mugshot: ' + ('Purple' if key == 'YI_COMMANDER_BOO' else 'Yellow'))
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (key, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde yoshis_island --- */'
    s = bd.replace_block(s, '/* --- yoshis_island', '/* --- einde yoshis_island --- */', blk)
    open(p, 'w').write(s)


PARTNER = '''=== PARTNER_YOSHI ===
Name: YOSHI
Class: Guest Star
Pic: Guest Yoshi
Gender: Male
Music: Twins
Back Pic: Yoshi
AI: Check Bad Move / Try To Faint / Check Viability

Dracovish @ Choice Band
Level: 93
Ability: Strong Jaw
Nature: Adamant
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 Atk / 4 SpD
- Fishious Rend
- Psychic Fangs
- Crunch
- Dragon Rush

Tyrantrum @ Life Orb
Level: 93
Ability: Strong Jaw
Nature: Adamant
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 Atk / 4 SpD
- Rock Slide
- Dragon Claw
- Crunch
- Dragon Dance

Gouging Fire @ Booster Energy
Level: 94
Ability: Protosynthesis
Nature: Adamant
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 Atk / 4 SpD
- Flare Blitz
- Breaking Swipe
- Stomping Tantrum
- Morning Sun

'''


def partner():
    p = 'src/data/battle_partners.party'
    s = open(p).read()
    anchor = '/* --- Battle Stadium (gegenereerd door tools/grounded/stadium/pool.py) --- */'
    if '=== PARTNER_YOSHI ===' in s:                  # vervangen (team van Jordi, 9 okt)
        i = s.index('=== PARTNER_YOSHI ===')
        j = min(k for k in (s.find('\n=== ', i + 5), s.find(anchor, i)) if k > 0)
        s = s[:i] + PARTNER.rstrip('\n') + '\n\n' + s[j:].lstrip('\n')
    else:
        assert anchor in s
        s = s.replace(anchor, PARTNER + anchor, 1)
    open(p, 'w').write(s)
    p = 'include/constants/battle_partner.h'
    s = open(p).read()
    if 'PARTNER_YOSHI ' not in s:
        a = '#define PARTNER_CALYREX 4 // Project Grounded: Calyrex in het brandende National Park\n'
        assert a in s
        top, rest = s.split(a)
        rest = re.sub(r'(#define PARTNER_\w+ )(\d+)', lambda mm: mm.group(1) + str(int(mm.group(2)) + 1), rest)
        s = top + a + "#define PARTNER_YOSHI 5 // Project Grounded: Yoshi op Yoshi's Island (multi battles)\n" + rest
        open(p, 'w').write(s)


def trainer_class():
    p = 'include/constants/trainers.h'
    s = open(p).read()
    if 'TRAINER_CLASS_SHY_SQUAD' not in s:
        s = s.replace('    TRAINER_CLASS_COUNT,\n',
                      "    TRAINER_CLASS_SHY_SQUAD, // Project Grounded: Yoshi's Island (Shy Guys, parodie op een evil team)\n"
                      '    TRAINER_CLASS_COUNT,\n', 1)
        open(p, 'w').write(s)
    p = 'src/battle_main.c'
    s = open(p).read()
    if '[TRAINER_CLASS_SHY_SQUAD]' not in s:
        a = '    [TRAINER_CLASS_ROCKET_EXEC] = { _("ROCKET EXEC"), 25, BALL_ULTRA }, // Project Grounded: Rocket-sidequest\n'
        assert a in s
        s = s.replace(a, a + '    [TRAINER_CLASS_SHY_SQUAD] = { _("SHY SQUAD"), 30, BALL_POKE }, '
                             "// Project Grounded: Yoshi's Island\n", 1)
        open(p, 'w').write(s)
    p = 'src/pokemon.c'
    s = open(p).read()
    a = '     || trainerId == TRAINER_SHY_GUY_DESERT)\n        return MUS_GROUNDED_VS_SUNSET_WILDS;'
    if 'TRAINER_CLASS_SHY_SQUAD' not in s:
        assert a in s
        s = s.replace(a, "     || trainerId == TRAINER_SHY_GUY_DESERT\n     || trainerClass == TRAINER_CLASS_SHY_SQUAD) "
                         "// Project Grounded: ook de Shy Squad op Yoshi's Island\n        return MUS_GROUNDED_VS_SUNSET_WILDS;", 1)
        open(p, 'w').write(s)


def battle_setup():
    p = 'src/battle_setup.c'
    s = open(p).read()
    a = '    case SPECIES_ZERAORA: // Project Grounded: Chargestone Cave'
    if 'SPECIES_PECHARUNT' not in s:
        assert a in s
        s = s.replace(a, "    case SPECIES_PECHARUNT: // Project Grounded: Yoshi's Island (placeholder: Kanto-legendary-thema, bestaande transitie)\n"
                         '        CreateBattleStartTask(B_TRANSITION_SWIRL, MUS_RG_VS_LEGEND);\n        break;\n' + a, 1)
        open(p, 'w').write(s)


def stadium():
    """Yoshi, Commander Boo en Wario staan al in de Battle Stadium-pool (gasten); Boo heet daar nu ook Commander."""
    p = 'src/data/trainers.party'
    s = open(p).read()
    i = s.index('=== TRAINER_STADIUM_BOO ===')
    j = s.index('\n===', i + 5)
    blk = s[i:j]
    nb = blk.replace('Class: Guest Star', 'Class: Commander')
    if nb != blk:
        s = s[:i] + nb + s[j:]
        open(p, 'w').write(s)
    p = 'tools/grounded/stadium/announcer.py'
    s = open(p).read()
    old = "    'STADIUM_BOO': \"BOO! Don't look at him. Seriously, look away. It's in the rules.\","
    new = ("    'STADIUM_BOO': \"COMMANDER BOO! Don't look at him. Seriously. He hates that."
           "\",")
    if old in s:
        s = s.replace(old, new)
        open(p, 'w').write(s)


# ====================================================================== scripts en teksten
def multi(S, tag, a, b, partner, won_label, intro_key, intro, defeat_a, defeat_b=None):
    """Multi battle met Yoshi (2 tegen 2, of 2 tegen 1 als b None is), zoals de schimmen in national_park.py."""
    P, X = S.P, S.T
    battle = (f'\tmulti_2_vs_2 TRAINER_{a}, {X}{tag}DefeatA, TRAINER_{b}, {X}{tag}DefeatB, {partner}\n' if b else
              f'\tmulti_2_vs_1 TRAINER_{a}, {X}{tag}DefeatA, {partner}\n')
    S.raw(f'''{P}{tag}Battle::
	msgbox {X}{intro_key}, MSGBOX_DEFAULT
	closemessage
{P}{tag}Choose::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, {P}{tag}Fight
	special LoadPlayerParty
	goto {P}{tag}Choose

{P}{tag}Fight::
{battle}	switch VAR_RESULT
	case 1, {won_label}
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate
''', [(intro_key, intro), (tag + 'DefeatA', defeat_a)] + ([(tag + 'DefeatB', defeat_b)] if b else []))


def beach_scripts():
    S = bd.Scr('YoshisIsland_Beach', "@ Project Grounded: Yoshi's Island, het strand (tools/grounded/maptools/yoshis_island.py)\n"
               'YoshisIsland_Beach_MapScripts::\n'
               '\tmap_script MAP_SCRIPT_ON_TRANSITION, YoshisIsland_Beach_OnTransition\n'
               '\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, YoshisIsland_Beach_OnFrame\n\t.byte 0\n')
    P, X = S.P, S.T
    S.raw(f'''YoshisIsland_Beach_OnTransition:
	call_if_set FLAG_YI_ARRIVED, {P}SetArrived
	end

{P}SetArrived::
	setvar VAR_TEMP_1, 1
	return

YoshisIsland_Beach_OnFrame:
	map_script_2 VAR_TEMP_1, 0, {P}Arrival
	.2byte 0

{P}Arrival::
	lockall
	setvar VAR_TEMP_1, 1
	setflag FLAG_YI_ARRIVED
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 10
	setvar VAR_0x8007, 4
	special ShakeCamera
	waitstate
	playse SE_FALL
	msgbox {X}Arrival1, MSGBOX_DEFAULT
	closemessage
	playse SE_PIN
	applymovement LOCALID_YI_BEACH_YOSHI, {P}Movement_YoshiIn
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_FaceLeft
	waitmovement 0
	msgbox {X}Arrival2, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_YI_BEACH_YOSHI, {P}Movement_YoshiBack
	waitmovement 0
	msgbox {X}Arrival3, MSGBOX_DEFAULT
	releaseall
	end

{P}Movement_YoshiIn:
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_right
	face_right
	jump_in_place_right
	step_end

{P}Movement_YoshiBack:
	walk_left
	walk_up
	walk_up
	walk_up
	face_down
	step_end

{P}Yoshi::
	lock
	faceplayer
	goto_if_set FLAG_YI_WARIO_DONE, {P}YoshiDone
	msgbox {X}YoshiPipe, MSGBOX_DEFAULT
	release
	end

{P}YoshiDone::
	msgbox {X}YoshiDone, MSGBOX_DEFAULT
	release
	end

{P}Guards::
	lock
	faceplayer
	goto {P}GuardsBattle

{P}GuardsWon::
	msgbox {X}GuardsWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_BEACH_GUARD_A
	removeobject LOCALID_YI_BEACH_GUARD_B
	removeobject LOCALID_YI_BEACH_YOSHI
	setflag FLAG_YI_BEACH_GUARDS
	setflag FLAG_YI_YOSHI_AHEAD
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox {X}YoshiAhead, MSGBOX_DEFAULT
	release
	end
''', [('Arrival1', "Something went wrong.\n\nThe ????? rift spits you out of a hole in the sky, high above an island "
                   "that looks like it was drawn with crayons. You fall for a very long time. You land face-first in "
                   "warm sand.\n\nNothing is broken. The art style would never allow it."),
      ('Arrival2', "YOSHI: Yoshi?\n\n(A green dinosaur in red shoes pokes you with his nose, decides you are not "
                   "a melon, and looks relieved for both of you.)\n\nYOSHI: Yoshi! Yoshi yoshi!\n\n(Roughly: the "
                   "SHY GUYS took over the island. They stole the eggs, the flags and the fun. He could use a "
                   "trainer. You will do.)"),
      ('Arrival3', "(YOSHI points at the green pipe up the path. Two SHY GUYS are standing in front of it, "
                   "trying very hard to look like a wall.)"),
      ('YoshiPipe', "YOSHI: Yoshi!\n\n(He points at the SHY GUYS by the pipe, then at you, then at himself. "
                    "Two against two. He has done the maths. It is the only maths he knows.)"),
      ('YoshiDone', "YOSHI: Yoshi... yoshi!\n\n(He waves at the rift with his whole body. The island is safe, the "
                    "eggs are home, and he will keep your spot on the beach warm. Literally. He is lying on it.)"),
      ('GuardsWon', "(The SHY GUYS shuffle aside. One of them writes something in a tiny notebook. "
                    "It is probably your name. It is probably misspelled.)"),
      ('YoshiAhead', "YOSHI: Yoshi!\n\n(YOSHI dives headfirst into the pipe. There is a loud BWOING. Then, "
                     "faintly, from very far away: 'yoshi'.)")])
    multi(S, 'Guards', 'YI_SHY_GUY_BEACH_A', 'YI_SHY_GUY_BEACH_B', 'PARTNER_YOSHI', P + 'GuardsWon', 'GuardsIntro',
          "(Two SHY GUYS block the pipe. They do not speak. The red one adjusts his mask. The green one adjusts "
          "his mask in solidarity.)\n\nYOSHI: Yoshi!\n\n(YOSHI hops next to you. Pick three POKéMON; he brings "
          "his own.)",
          "(The SHY GUY stares at you. It's unclear whether it's judging you. It is.)",
          "(The SHYER GUY hides behind the SHY GUY. Nobody was ready for this level of shyness.)")
    S.npc('Sign', "WELCOME TO YOSHI'S ISLAND\nPopulation: Yoshis. Also SHY GUYS, temporarily.\n"
                  "Please do not eat the scenery. (Yoshis excepted.)", 'MSGBOX_SIGN')
    beach_extra(S)
    S.write()


def hills_scripts():
    S = bd.Scr('YoshisIsland_Hills', "@ Project Grounded: Yoshi's Island, de heuvels (tools/grounded/maptools/yoshis_island.py)\n"
               'YoshisIsland_Hills_MapScripts::\n\t.byte 0\n')
    P, X = S.P, S.T
    S.raw(f'''{P}Yoshi::
	lock
	faceplayer
	goto_if_unset FLAG_YI_CAMP_A, {P}YoshiCamp
	goto_if_unset FLAG_YI_CAMP_B, {P}YoshiPass
	goto_if_unset FLAG_YI_BOO_DONE, {P}YoshiBoo
	msgbox {X}YoshiFort, MSGBOX_DEFAULT
	release
	end

{P}YoshiCamp::
	msgbox {X}YoshiCamp, MSGBOX_DEFAULT
	release
	end

{P}YoshiPass::
	msgbox {X}YoshiPass, MSGBOX_DEFAULT
	release
	end

{P}YoshiBoo::
	msgbox {X}YoshiBoo, MSGBOX_DEFAULT
	release
	end

{P}CampA::
	lock
	faceplayer
	goto {P}CampABattle

{P}CampAWon::
	msgbox {X}CampAWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_CAMP_A1
	removeobject LOCALID_YI_CAMP_A2
	setflag FLAG_YI_CAMP_A
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

{P}CampB::
	lock
	faceplayer
	goto_if_unset FLAG_YI_CAMP_A, {P}CampBWait
	goto {P}CampBBattle

{P}CampBWait::
	msgbox {X}CampBWait, MSGBOX_DEFAULT
	release
	end

{P}CampBWon::
	msgbox {X}CampBWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_CAMP_B1
	removeobject LOCALID_YI_CAMP_B2
	setflag FLAG_YI_CAMP_B
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

{P}GateGuard::
	msgbox {X}GateGuard, MSGBOX_NPC
	end

{P}Pecharunt::
	lock
	faceplayer
	goto_if_set FLAG_YI_WARIO_DONE, {P}PecharuntBattle
	msgbox {X}PecharuntShop, MSGBOX_DEFAULT
	release
	end

{P}PecharuntBattle::
	playmoncry SPECIES_PECHARUNT, CRY_MODE_ENCOUNTER
	msgbox {X}PecharuntBattle, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_PECHARUNT, 92
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}PecharuntCaught
	msgbox {X}PecharuntEscaped, MSGBOX_DEFAULT
	release
	end

{P}PecharuntCaught::
	removeobject LOCALID_YI_PECHARUNT
	setflag FLAG_YI_PECHARUNT_DONE
	msgbox {X}PecharuntCaught, MSGBOX_DEFAULT
	release
	end
''', [('YoshiCamp', "YOSHI: Yoshi yoshi!\n\n(The SHY GUY camp is east. The two by the campfire are in charge of "
                    "the snacks, which makes them the most dangerous ones.)"),
      ('YoshiPass', "YOSHI: Yoshi!\n\n(Two more are guarding the path west, to the haunted house. Something in "
                    "there giggles at night. YOSHI does not like giggling he did not start.)"),
      ('YoshiBoo', "YOSHI: Yoshi... yoshi.\n\n(The haunted house. COMMANDER BOO lives there. YOSHI is being very "
                   "brave about it, from back here.)"),
      ('YoshiFort', "YOSHI: YOSHI!\n\n(The fort's door is open. Whoever is behind all this smells strongly of "
                    "garlic. YOSHI has a theory. The theory is wearing yellow.)"),
      ('CampAWon', "(The SHY GUYS drop a sack of stolen eggs, a stolen flag and, for some reason, a stolen sense "
                   "of direction. They run off to file a complaint with management.)"),
      ('CampBWait', "(The SHY GUYS cross their arms and point east, at the camp. Apparently you need to be "
                    "beaten up by the camp first. It's policy.)"),
      ('CampBWon', "(The SHY GUYS step aside and bow. Then they keep bowing, to be safe, until you are out of "
                   "sight.)"),
      ('GateGuard', "(A SHY GUY in a black cloak holds up a sign: MEMBERS ONLY. On the back, in smaller letters: "
                    "MEMBERSHIP = BEING COMMANDER BOO. You are, sadly, not COMMANDER BOO.)"),
      ('PecharuntShop', "PECHARUNT: Mochi? Mochi! One for you, one for the nice SHY GUYS, a whole crate for the big "
                        "man in the fort. He pays in gold. Gold is chewy too.\n\n(The mochi glisten. They smell "
                        "like obedience and strawberries. You politely decline.)"),
      ('PecharuntBattle', "PECHARUNT: The big man stopped buying. The SHY GUYS stopped obeying. Business is "
                          "terrible.\n\nPECHARUNT: ...unless YOU would like to be my new best customer!"),
      ('PecharuntEscaped', "(PECHARUNT has rolled back behind the counter, rearranging mochi. He will be here "
                           "all week.)"),
      ('PecharuntCaught', "(The mochi stall is empty. A little sign reads: CLOSED FOR GOOD. UNDER NEW "
                          "MANAGEMENT. The new management is you.)")])
    multi(S, 'CampA', 'YI_SHY_GUY_CAMP_A1', 'YI_SHY_GUY_CAMP_A2', 'PARTNER_YOSHI', P + 'CampAWon', 'CampAIntro',
          "(A FLY GUY and a SHADY GUY are roasting a stolen Yoshi egg over the fire. Well. Warming it. Very "
          "gently. They look at you like you interrupted a ritual.)\n\nYOSHI: YOSHI!!",
          "(The FLY GUY's propeller slows to a sad little spin.)",
          "(The SHADY GUY tries to pickpocket you on his way down. He gets a receipt.)")
    multi(S, 'CampB', 'YI_SHY_GUY_CAMP_B1', 'YI_SHY_GUY_CAMP_B2', 'PARTNER_YOSHI', P + 'CampBWon', 'CampBIntro',
          "(A SPEAR GUY and a SNIFIT block the path to the haunted house. The SNIFIT inhales. It is a very "
          "threatening inhale.)\n\nYOSHI: Yoshi!",
          "(The SPEAR GUY's spear droops. He was compensating.)",
          "(The SNIFIT exhales. That was the whole plan.)")
    S.npc('Sign', "SHY GUY CAMP\nTrespassers will be stared at.\nUnmasking is strictly forbidden. "
                  "(Mostly because we lost the instructions.)", 'MSGBOX_SIGN')
    hills_extra(S)
    S.write()


def boo_scripts():
    S = bd.Scr('YoshisIsland_BooMansion', "@ Project Grounded: Yoshi's Island, Boo's spookhuis (tools/grounded/maptools/yoshis_island.py)\n"
               'YoshisIsland_BooMansion_MapScripts::\n\t.byte 0\n')
    P, X = S.P, S.T
    S.raw(f'''{P}Boo::
	lock
	faceplayer
	goto {P}BooBattle

{P}BooWon::
	msgbox {X}BooWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_BOO
	setflag FLAG_YI_BOO_DONE
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox {X}BooGone, MSGBOX_DEFAULT
	release
	end

{P}Yoshi::
	msgbox {X}Yoshi, MSGBOX_NPC
	end
''', [('BooWon', "COMMANDER BOO: Fine! FINE! Take the stupid fort! It was never mine anyway. I just do the "
                 "spooking. The big guy does the paperwork.\n\nCOMMANDER BOO: ...don't look at me while I'm "
                 "crying."),
      ('BooGone', "(COMMANDER BOO turns invisible out of embarrassment. Somewhere outside, a SHY GUY in a black "
                  "cloak hears the news and quietly cancels his membership.)"),
      ('Yoshi', "YOSHI: Y-yoshi...\n\n(YOSHI is hiding behind a candle. It is a thin candle. It is not "
                "working.)")])
    multi(S, 'Boo', 'YI_COMMANDER_BOO', None, 'PARTNER_YOSHI', P + 'BooWon', 'BooIntro',
          "COMMANDER BOO: Hee hee hee! A visitor! Nobody visits! Do you know how hard it is to make friends when "
          "everyone you meet screams?\n\nCOMMANDER BOO: The boss pays me in mochi to keep the SHY GUYS in line. "
          "And to keep YOU out. Mostly the mochi part.\n\nYOSHI: ...yoshi! (Very small, but brave.)",
          "COMMANDER BOO: Stop LOOKING at me!")
    S.npc('Portrait', "(A portrait of a BOO. Its eyes follow you around the room. Then it gets embarrassed and "
                      "looks away.)", 'MSGBOX_SIGN')
    S.write()


def fort_scripts():
    S = bd.Scr('YoshisIsland_WarioFort', "@ Project Grounded: Yoshi's Island, Wario's fort (tools/grounded/maptools/yoshis_island.py)\n"
               'YoshisIsland_WarioFort_MapScripts::\n\t.byte 0\n')
    P, X = S.P, S.T
    S.raw(f'''{P}Guards::
	lock
	faceplayer
	goto {P}GuardsBattle

{P}GuardsWon::
	msgbox {X}GuardsWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_FORT_GUARD_A
	removeobject LOCALID_YI_FORT_GUARD_B
	setflag FLAG_YI_FORT_GUARDS
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

{P}Wario::
	lock
	faceplayer
	goto {P}WarioBattle

{P}WarioWon::
	msgbox {X}WarioWon, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_WARIO
	setflag FLAG_YI_WARIO_DONE
	setflag FLAG_SPACETIME_YOSHI_DONE
	fadescreenswapbuffers FADE_FROM_BLACK
	applymovement LOCALID_YI_FORT_YOSHI, Common_Movement_FaceUp
	waitmovement 0
	msgbox {X}YoshiThanks, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_YI_FORT_YOSHI
	setflag FLAG_YI_YOSHI_HOME
	clearflag FLAG_YI_YOSHI_AHEAD
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox {X}Done, MSGBOX_DEFAULT
	release
	end

{P}Yoshi::
	msgbox {X}Yoshi, MSGBOX_NPC
	end
''', [('GuardsWon', "(The NINJA GUY vanishes in a puff of smoke. The BOUNCER GUY has to walk. It takes a while.)"),
      ('WarioWon', "WARIO: WAAAH! My gold! My fort! My mochi subscription!\n\nWARIO: Fine. FINE. I'll go back "
                   "to my own dimension. The one with the microgames. You'd have lost those, by the way. "
                   "Five seconds each. No POKéMON. Think about it."),
      ('YoshiThanks', "YOSHI: Yoshi! Yoshi yoshi YOSHI!\n\n(YOSHI hugs you, hard, the way only a dinosaur raised "
                      "on fruit can. The eggs are safe. The SHY GUYS are unemployed. He will see you on the "
                      "beach.)"),
      ('Done', "(Spacetime hums. Somewhere far away, in a cave full of rifts, a folded wall unfolds a little. "
               "The ????? rift sounds less confused.)"),
      ('Yoshi', "YOSHI: Yoshi!\n\n(He is cracking his knuckles. He does not have knuckles. It is the thought "
                "that counts.)")])
    multi(S, 'Guards', 'YI_SHY_GUY_FORT_A', 'YI_SHY_GUY_FORT_B', 'PARTNER_YOSHI', P + 'GuardsWon', 'GuardsIntro',
          "(A NINJA GUY and a BOUNCER GUY guard the carpet. The BOUNCER GUY checks a list. You are not on it. "
          "Nobody is on it. It is a blank list. That's the joke. He doesn't get it either.)\n\nYOSHI: Yoshi!",
          "(The NINJA GUY throws a smoke bomb. It is a dud. He leaves anyway, on foot, with dignity.)",
          "(The BOUNCER GUY crosses you off the blank list.)")
    multi(S, 'Wario', 'YI_WARIO', None, 'PARTNER_YOSHI', P + 'WarioWon', 'WarioIntro',
          "WARIO: WAH HA HA! So YOU'RE the one beating up my employees! Do you know what SHY GUYS cost? "
          "Nothing! I pay them in mochi! It's GENIUS!\n\nWARIO: The fort, the gold, the eggs, the island: all "
          "WARIO's! And the purple mochi guy says the mochi make them do whatever I want. No refunds!\n\n"
          "YOSHI: YOSHI!!\n\nWARIO: Two against one? Fine! WARIO doesn't play fair anyway!",
          "WARIO: That was NOT in the contract!")
    S.npc('Throne', "(A golden throne with a big W on it. The cushion is shaped like a very specific behind.)",
          'MSGBOX_SIGN')
    S.write()


# ---------------------------------------------------------------- uitbreiding: ?-wolken, Message Blocks, Poochy, Nep-Enut
def ni_items(mp):
    """Items uit de centrale lijst (nieuwe_items.py) voor kaart mp: {item: (flag, aantal, verborgen)}."""
    import nieuwe_items as ni
    return {it: (fl, q, h) for fl, it, q, h in ni.items(mp)}


CLOUD_MOVE = '''{P}Movement_CloudPop:
	jump_in_place_down
	jump_in_place_down
	step_end
'''


def cloud(S, key, lid, flag, item=None, qty=1, text=''):
    """?-wolk: aanspreken laat hem knappen (geluid, hupje, weg) en geeft een item of alleen een gebeurtenis."""
    P, X = S.P, S.T
    give = '\tgiveitem %s, %d\n' % (item, qty) if item else ''
    S.raw(f'''{P}{key}::
	lock
	playse SE_BALLOON_RED
	applymovement {lid}, {P}Movement_CloudPop
	waitmovement 0
	removeobject {lid}
	setflag {flag}
	playse SE_BALLOON_BLUE
	msgbox {X}{key}, MSGBOX_DEFAULT
{give}	release
	end
''', [(key, text)])


def beach_extra(S):
    P = S.P
    sable = ni_items('YoshisIsland_Beach')['ITEM_SHALOUR_SABLE']
    S.raw(CLOUD_MOVE.format(P=P))
    cloud(S, 'Cloud', 'LOCALID_YI_BEACH_CLOUD', sable[0], 'ITEM_SHALOUR_SABLE', sable[1],
          "POP! The ? CLOUD bursts. It was full of biscuits.\n\nNobody knows how biscuits get into clouds. "
          "Nobody on this island has ever asked.")
    S.npc('MsgBlock', "MESSAGE BLOCK: Hi! I'm a MESSAGE BLOCK! Hit me from below for a helpful hint!\n\n"
                      "MESSAGE BLOCK: ...you can't. This game is top-down. Fine. The hint is free: the pipe on the "
                      "right goes to the jungle. The jungle has a lake. The lake has eyebrows. Lakes should not have "
                      "eyebrows.", 'MSGBOX_SIGN')
    S.npc('Mailbox', "(YOSHI's mailbox. There's a note inside: \"Gone to rescue my friends. Back soon. -YOSHI\")\n\n"
                     "(The friends are all inside. They have been back for decades. Nobody told the mailbox.)",
          'MSGBOX_SIGN')


def hills_extra(S):
    P = S.P
    S.raw(CLOUD_MOVE.format(P=P))
    cloud(S, 'StarCloud', 'LOCALID_YI_STAR_CLOUD', 'FLAG_YI_STAR_CLOUD', None, 0,
          "POP! The ? CLOUD bursts into a shower of little stars.\n\nYou now have 1 STAR. Stars do nothing in this "
          "game. You will carry it with you anyway. Like most collectibles.")


def jungle_scripts():
    S = bd.Scr('YoshisIsland_Jungle', "@ Project Grounded: Yoshi's Island, de jungle (tools/grounded/maptools/yoshis_island.py)\n"
               'YoshisIsland_Jungle_MapScripts::\n\t.byte 0\n')
    P, X = S.P, S.T
    t0, t1, ty = J_THORN
    k = t1 - t0 + 2
    it = ni_items('YoshisIsland_Jungle')
    dig, milk = it['ITEM_STRANGE_SOUVENIR'], it['ITEM_MOOMOO_MILK']
    S.raw(f'''{P}Poochy::
	lock
	faceplayer
	goto_if_set FLAG_YI_POOCHY_MET, {P}PoochyRide
	setflag FLAG_YI_POOCHY_MET
	msgbox {X}PoochyMeet, MSGBOX_DEFAULT
{P}PoochyRide::
	msgbox {X}PoochyRide, MSGBOX_DEFAULT
	closemessage
	getplayerxy VAR_TEMP_0, VAR_TEMP_1
	goto_if_gt VAR_TEMP_0, {t1}, {P}PoochyWest
	applymovement LOCALID_YI_POOCHY, {P}Movement_PoochyEast
	applymovement OBJ_EVENT_ID_PLAYER, {P}Movement_PlayerEast
	waitmovement 0
	fadescreenswapbuffers FADE_TO_BLACK
	setobjectxyperm LOCALID_YI_POOCHY, {t1}, {ty}
	setobjectxy LOCALID_YI_POOCHY, {t1}, {ty}
	turnobject LOCALID_YI_POOCHY, DIR_EAST
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

{P}PoochyWest::
	applymovement LOCALID_YI_POOCHY, {P}Movement_PoochyWest
	applymovement OBJ_EVENT_ID_PLAYER, {P}Movement_PlayerWest
	waitmovement 0
	call_if_unset FLAG_YI_POOCHY_DUG, {P}PoochyDig
	fadescreenswapbuffers FADE_TO_BLACK
	setobjectxyperm LOCALID_YI_POOCHY, {t0}, {ty}
	setobjectxy LOCALID_YI_POOCHY, {t0}, {ty}
	turnobject LOCALID_YI_POOCHY, DIR_WEST
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

{P}PoochyDig::
	applymovement LOCALID_YI_POOCHY, {P}Movement_PoochySniff
	waitmovement 0
	playse SE_M_DIG
	msgbox {X}PoochyDig, MSGBOX_DEFAULT
	giveitem {'ITEM_STRANGE_SOUVENIR'}, {dig[1]}
	setflag FLAG_YI_POOCHY_DUG
	setflag {dig[0]}
	closemessage
	return

{P}Movement_PoochyEast:
''' + '\twalk_fast_right\n' * k + f'''	step_end

{P}Movement_PlayerEast:
''' + '\twalk_fast_right\n' * k + f'''	step_end

{P}Movement_PoochyWest:
''' + '\twalk_fast_left\n' * k + f'''	step_end

{P}Movement_PlayerWest:
''' + '\twalk_fast_left\n' * k + f'''	step_end

{P}Movement_PoochySniff:
	face_down
	jump_in_place_down
	face_left
	jump_in_place_left
	step_end

{P}NepEnut::
	lock
	goto_if_set FLAG_YI_NEP_ENUT_DONE, {P}NepChill
	msgbox {X}Nep1, MSGBOX_DEFAULT
	closemessage
	@ hij is 8 tegels hoog: de camera kijkt even omhoog, anders valt zijn kop buiten beeld
	special SpawnCameraObject
	applymovement OBJ_EVENT_ID_CAMERA, {P}Movement_CamUp
	waitmovement 0
	playse SE_M_DIVE
	applymovement LOCALID_YI_NEP_ENUT, {P}Movement_NepRise
	delay 24
	playmoncry SPECIES_DONDOZO, CRY_MODE_ENCOUNTER
	msgbox {X}Nep2, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	applymovement OBJ_EVENT_ID_CAMERA, {P}Movement_CamDown
	waitmovement 0
	special RemoveCameraObject
	setwildbattle SPECIES_DONDOZO, 90
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}NepGone
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}NepGone
	msgbox {X}NepStill, MSGBOX_DEFAULT
	release
	end

{P}NepGone::
	setflag FLAG_YI_NEP_ENUT_DONE
	msgbox {X}NepGone, MSGBOX_DEFAULT
	release
	end

{P}NepChill::
	msgbox {X}NepChill, MSGBOX_DEFAULT
	release
	end

{P}Movement_NepRise:
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	walk_in_place_slow_down
	step_end

{P}Movement_CamUp:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

{P}Movement_CamDown:
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	step_end
''', [('PoochyMeet', "POOCHY: Ruff!\n\n(This dog's name is POOCHY. He's pretty cute, huh? He does not care about "
                     "thorns. He has never cared about anything except running in the direction you are facing.)"),
      ('PoochyRide', "POOCHY: RUFF RUFF! (Hitch a ride!)"),
      ('PoochyDig', "(POOCHY sniffs the ground, digs like his life depends on it, and proudly drops something at "
                    "your feet. It is a souvenir. Of what, nobody knows. POOCHY knows. POOCHY isn't telling.)"),
      ('Nep1', "(Two very angry eyebrows are floating on the lake. Under the eyebrows: eyes. Under the eyes: a lot "
               "more lake than you would like.)"),
      ('Nep2', "NEP-ENUT: GLOOOORP!!\n\n(NEP-ENUT rises out of the lake. All of him. He used to chase YOSHI through "
               "entire levels. Then he found out you can just wait in a lake for people to come and look.)\n\n"
               "(Up close he's a DONDOZO. Most lake monsters are a fish if you get close enough. Nobody gets close "
               "enough.)"),
      ('NepStill', "(NEP-ENUT sinks back down until only the eyebrows are left. The eyebrows keep watching. "
                   "Judging, mostly.)"),
      ('NepGone', "(NEP-ENUT sinks back down until only the eyebrows are left. He seems... relieved? Being a final "
                  "boss for one lake is a lot of pressure.)"),
      ('NepChill', "(NEP-ENUT is floating. Just floating. The eyebrows are relaxed for the first time in 30 years.)\n\n"
                   "NEP-ENUT: ...blorp.\n\n(He is off the clock.)")])
    S.raw(CLOUD_MOVE.format(P=P))
    cloud(S, 'Cloud', 'LOCALID_YI_JUNGLE_CLOUD', milk[0], 'ITEM_MOOMOO_MILK', milk[1],
          "POP! The ? CLOUD bursts and it rains milk. Only on you.\n\nYou caught some of it in bottles. You had "
          "bottles. You have always had bottles.")
    S.trainer('ShyGuy', 'YI_SHY_GUY_JUNGLE',
              "(The JUNGLE GUY has painted his mask green for camouflage. He is standing on a yellow path.)",
              "(The JUNGLE GUY quietly unpaints his mask.)",
              "(The JUNGLE GUY is pretending to be a bush. You are being polite about it.)")
    S.npc('MsgEntrance', "MESSAGE BLOCK: Welcome to the jungle! We've got fun and games! Mostly games. Mostly "
                         "SHY GUYS.\n\nMESSAGE BLOCK: Tip: the tall grass is level 91. It does not care about your "
                         "feelings.", 'MSGBOX_SIGN')
    S.npc('MsgThorns', "MESSAGE BLOCK: THORNS! YOSHIS can't walk on thorns. Trainers can't walk on thorns.\n\n"
                       "MESSAGE BLOCK: POOCHY can walk on thorns. POOCHY can walk on anything. Science stopped "
                       "asking.", 'MSGBOX_SIGN')
    S.npc('MsgLake', "MESSAGE BLOCK: Please do not feed the eyebrows.\n\nMESSAGE BLOCK: The eyebrows are attached to "
                     "something. The something is attached to the lake. Swimming is at your own risk. The risk is "
                     "large. Very large. Larger than it looks.", 'MSGBOX_SIGN')
    S.npc('EggBlock', "(An EGG BLOCK. You bonk it. An egg pops out, rolls into the jungle and is never seen again. "
                      "EGG BLOCKS are like that.)", 'MSGBOX_SIGN')
    S.write()


YH_TEXT = {
    'GREEN': "(A green YOSHI. Not THE YOSHI. This one is called GREG. People keep asking GREG to save the island. GREG "
             "is in his pajamas.)",
    'RED': "(The red YOSHI breathes fire after he eats a red shell. There are no red shells on this island. He has "
           "been waiting since 1990. He has a lot of fire saved up.)",
    'YELLOW': "(The yellow YOSHI makes the ground shake when he lands. He is sitting very, very still. For everyone's "
              "sake, including the furniture's.)",
    'LIGHT_BLUE': "(The light-blue YOSHI can fly with a blue shell. He asks if any of your POKEMON is a shell. He looks "
                  "at your party for a very long time.)",
    'PURPLE': "(The purple YOSHI says purple is just a darker, better pink and that the pink one copied him. The pink "
              "one is not listening. The pink one is baking.)",
    'BROWN': "(The brown YOSHI would like you to know he is not dirty. It's his natural color. He says it like he's "
             "had to say it a lot.)",
    'BLACK': "(The black YOSHI is wearing sunglasses indoors. He is the edgy one. He is eating a cupcake with "
             "sprinkles. Edgily.)",
    'WHITE': "(The white YOSHI is very rare. He tells you this immediately. Then once more. He has a small framed "
             "certificate and nowhere to hang it.)",
    'BLUE': "(A real blue YOSHI. Not a fish in a costume, not a lake with eyebrows. He wants that on record. Please "
            "put it on record.)",
}


def house_scripts():
    S = bd.Scr('YoshisIsland_YoshiHouse', "@ Project Grounded: Yoshi's Island, het Yoshi-huis (tools/grounded/maptools/yoshis_island.py)\n"
               'YoshisIsland_YoshiHouse_MapScripts::\n\t.byte 0\n')
    P, X = S.P, S.T
    heart = ni_items('YoshisIsland_YoshiHouse')['ITEM_SWEET_HEART']
    for col, x, y, mv in YH_YOSHIS:
        key = 'Yoshi' + ''.join(w.capitalize() for w in col.split('_'))
        if col == 'PINK':
            S.raw(f'''{P}{key}::
	lock
	faceplayer
	goto_if_set {heart[0]}, {P}{key}After
	msgbox {X}{key}, MSGBOX_DEFAULT
	giveitem ITEM_SWEET_HEART, {heart[1]}
	goto_if_eq VAR_RESULT, FALSE, {P}{key}End
	setflag {heart[0]}
{P}{key}After::
	msgbox {X}{key}After, MSGBOX_DEFAULT
{P}{key}End::
	release
	end
''', [(key, "(The pink YOSHI baked you something. It's shaped like a heart. It has been in her mouth. It is still a "
                  "gift. Gifts are about the thought.)"),
                 (key + 'After', "(The pink YOSHI is baking another one. For herself, this time. She has earned it.)")])
        else:
            S.npc(key, YH_TEXT[col])
    S.npc('Hearth', "(A crackling fireplace. Every YOSHI's house has one. Nobody knows who lights it. The fire doesn't "
                    "know either.)", 'MSGBOX_SIGN')
    S.npc('Portrait', "(A family portrait. It's an egg. All the YOSHI family portraits are eggs. It's a very "
                      "efficient family.)", 'MSGBOX_SIGN')
    S.write()


def cave_scripts():
    S = bd.Scr('YoshisIsland_Cave', "@ Project Grounded: Yoshi's Island, kristalgrot (tools/grounded/maptools/yoshis_island.py)\n"
               'YoshisIsland_Cave_MapScripts::\n\t.byte 0\n')
    S.trainer('ShyGuy', 'YI_SHY_GUY_CAVE',
              "(The MINER GUY has a tiny lamp on his mask. He shines it in your eyes. On purpose.)",
              "(The MINER GUY's lamp flickers out. He keeps it on his mask out of principle.)",
              "(The MINER GUY is mining the same crystal he mined yesterday. It's a union thing.)")
    S.npc('MsgBlock', "MESSAGE BLOCK: This crystal cave belongs to the SHY GUY MINING UNION.\n\nMESSAGE BLOCK: Hard "
                      "hats required. Masks required. Faces strictly optional, and frankly discouraged.", 'MSGBOX_SIGN')
    S.npc('EggBlock', "(Two EGG BLOCKS, a green one and a red one. They are not on speaking terms.)", 'MSGBOX_SIGN')
    S.npc('Bucket', "(A ? BUCKET. You look inside. It's empty. The ? was a lie.)", 'MSGBOX_SIGN')
    S.npc('Pow', "(A POW BLOCK. You think about it. You decide not to. The cave thanks you.)", 'MSGBOX_SIGN')
    S.write()


def flowers_scripts(m):
    S = bd.Scr('YoshisIsland_Flowers', "@ Project Grounded: Yoshi's Island, het bloemenveld (tools/grounded/maptools/yoshis_island.py)\n"
               'YoshisIsland_Flowers_MapScripts::\n'
               '\tmap_script MAP_SCRIPT_ON_LOAD, YoshisIsland_Flowers_OnLoad\n\t.byte 0\n')
    P, X = S.P, S.T
    gal = ni_items('YoshisIsland_Flowers')['ITEM_LUMIOSE_GALETTE']
    tiles = ''.join('\tsetmetatile %d, %d, 0x%03X, FALSE\n' % (x, y, mt) for (x, y), mt in sorted(m.extra_ids.items()))
    S.raw(f'''YoshisIsland_Flowers_OnLoad:
	call_if_set FLAG_YI_BRIDGE_CLOUD, {P}SetBridge
	end

{P}SetBridge::
{tiles}	return

{P}BridgeCloud::
	lock
	playse SE_BALLOON_RED
	applymovement LOCALID_YI_BRIDGE_CLOUD, {P}Movement_CloudPop
	waitmovement 0
	removeobject LOCALID_YI_BRIDGE_CLOUD
	setflag FLAG_YI_BRIDGE_CLOUD
	playse SE_DING_DONG
	call {P}SetBridge
	special DrawWholeMapView
	msgbox {X}BridgeCloud, MSGBOX_DEFAULT
	release
	end
''', [('BridgeCloud', "POP! The ? CLOUD bursts and a row of little rafts unrolls across the gap, like a carpet "
                      "that has been waiting its whole life for this.\n\nIt's a bridge now. Don't look down. "
                      "Down is also clouds.")])
    S.raw(CLOUD_MOVE.format(P=P))
    cloud(S, 'Cloud', 'LOCALID_YI_FLOWERS_CLOUD', gal[0], 'ITEM_LUMIOSE_GALETTE', gal[1],
          "POP! The ? CLOUD bursts and two galettes float down, still warm.\n\nThe sky bakes. Nobody told you the "
          "sky bakes.")
    S.trainer('ShyGuy', 'YI_SHY_GUY_FLOWERS',
              "(The GROOVY GUY has a flower stuck in his mask. It's the 70s up here. It's always the 70s up here.)",
              "(The GROOVY GUY gives you the flower. It wilts immediately. Bad vibes.)",
              "(The GROOVY GUY is lying in the grass, watching the clouds. The clouds are below him. He has not "
              "noticed.)")
    S.npc('MsgEntrance', "MESSAGE BLOCK: FLOWER FIELD, ABOVE THE CLOUDS.\n\nMESSAGE BLOCK: Safety notice: the edges "
                         "are clouds. Clouds are not floors. We have had complaints. Well. We had complaints.",
          'MSGBOX_SIGN')
    S.npc('MsgGoal', "MESSAGE BLOCK: Congratulations, you reached the GOAL!\n\nMESSAGE BLOCK: There is no bonus "
                     "roulette. There is no score screen. There is a CHERISH BALL and a deep sense of closure.",
          'MSGBOX_SIGN')
    S.npc('MsgBridge', "MESSAGE BLOCK: No bridge? Pop the ? CLOUD!\n\nMESSAGE BLOCK: ? CLOUDS contain items, "
                       "bridges or disappointment. The odds are not published.", 'MSGBOX_SIGN')
    S.npc('Switch', "(A red ! SWITCH. In another game it would make things solid. You press it anyway.\n\nSomewhere, "
                    "something becomes slightly more solid. You will never find out what.)", 'MSGBOX_SIGN')
    S.npc('EggBlock', "(An EGG BLOCK. It's out of eggs. There's a little sign: BACK IN 5 MINUTES. The sign is "
                      "dated three games ago.)", 'MSGBOX_SIGN')
    S.write()


# ====================================================================== map.json
ITEMS = {  # kaart -> [(x, y, item, flag, verborgen)]
    'YoshisIsland_Beach': [(23, 15, 'ITEM_HONEY', 'FLAG_ITEM_YOSHIS_ISLAND_BEACH_HONEY', False),
                           (4, 13, 'ITEM_HEAL_BALL', 'FLAG_ITEM_YOSHIS_ISLAND_BEACH_HEAL_BALL', False),
                           (28, 17, 'ITEM_EXP_CANDY_XS', 'FLAG_HIDDEN_ITEM_YOSHIS_ISLAND_BEACH_EXP_CANDY_XS', True)],
    'YoshisIsland_Hills': [(13, 20, 'ITEM_LAGGING_TAIL', 'FLAG_ITEM_YOSHIS_ISLAND_HILLS_LAGGING_TAIL', False),
                           (35, 22, 'ITEM_TOXIC_PLATE', 'FLAG_ITEM_YOSHIS_ISLAND_HILLS_TOXIC_PLATE', False),
                           (36, 9, 'ITEM_STICKY_BARB', 'FLAG_HIDDEN_ITEM_YOSHIS_ISLAND_HILLS_STICKY_BARB', True)],
    'YoshisIsland_BooMansion': [(2, 9, 'ITEM_FLOAT_STONE', 'FLAG_ITEM_YOSHIS_ISLAND_BOO_MANSION_FLOAT_STONE', False),
                                (15, 9, 'ITEM_POKE_DOLL', 'FLAG_ITEM_YOSHIS_ISLAND_BOO_MANSION_POKE_DOLL', False)],
    'YoshisIsland_WarioFort': [(2, 12, 'ITEM_GRIP_CLAW', 'FLAG_ITEM_YOSHIS_ISLAND_WARIO_FORT_GRIP_CLAW', False),
                               (15, 4, 'ITEM_MALICIOUS_ARMOR', 'FLAG_ITEM_YOSHIS_ISLAND_WARIO_FORT_MALICIOUS_ARMOR', False)],
}


def lid(o, name):
    o['local_id'] = name
    return o


def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"%s": [' % GROUP); j = g.index('\n  ]', i)
        g = g[:j] + ',\n    "%s"' % name + g[j:]
    d = json.loads(g)
    assert len(d[GROUP]) <= 128
    open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/SpacetimeCave/scripts.inc"\n'
        assert anchor in es
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def write_map(name, layout, objs, warps, bgs, coords=(), **kw):
    m = {'id': 'MAP_' + const(name), 'name': name, 'layout': layout, 'music': 'MUS_RG_BERRY_PICK',
         'region_map_section': 'MAPSEC_YOSHIS_ISLAND', 'requires_flash': False, 'weather': 'WEATHER_NONE',
         'map_type': 'MAP_TYPE_ROUTE', 'allow_cycling': False, 'allow_escaping': False, 'allow_running': True,
         'show_map_name': True, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
         'object_events': objs, 'warp_events': warps, 'coord_events': list(coords), 'bg_events': bgs}
    m.update(kw)
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    register_map(name)


NI_SPOTS = {  # kaart -> {item: (x, y)} voor item balls/verborgen items uit nieuwe_items.py
    'YoshisIsland_Jungle': {'ITEM_GALARICA_TWIG': (2, 11)},
    'YoshisIsland_Cave': {'ITEM_RELIC_BAND': (21, 14), 'ITEM_PEWTER_CRUNCHIES': (2, 10)},
    'YoshisIsland_Flowers': {'ITEM_CHERISH_BALL': (25, 7)},
}


def items_of(name):
    objs, bgs = [], []
    spots = list(ITEMS.get(name, []))
    for it, (fl, q, hid) in ni_items(name).items():
        if it in NI_SPOTS.get(name, {}):
            spots.append(NI_SPOTS[name][it] + (it, fl, hid))
    for x, y, it, fl, hid in spots:
        if hid:
            bgs.append(bd.hidden(x, y, it, fl))
        else:
            objs.append(bd.ball(x, y, it, fl))
    return objs, bgs


def map_jsons(lay):
    Y = 'OBJ_EVENT_GFX_YOSHI'
    # strand
    P = 'YoshisIsland_Beach_EventScript_'
    objs = [lid(bd.obj(Y, B_YOSHI[0], B_YOSHI[1], P + 'Yoshi', 'FLAG_YI_YOSHI_AHEAD'), 'LOCALID_YI_BEACH_YOSHI'),
            lid(bd.obj(SHY_GFX['red'], B_GUARDS[0][0], B_GUARDS[0][1], P + 'Guards', 'FLAG_YI_BEACH_GUARDS'),
                'LOCALID_YI_BEACH_GUARD_A'),
            lid(bd.obj(SHY_GFX['green'], B_GUARDS[1][0], B_GUARDS[1][1], P + 'Guards', 'FLAG_YI_BEACH_GUARDS'),
                'LOCALID_YI_BEACH_GUARD_B')]
    Q = 'OBJ_EVENT_GFX_QCLOUD'
    WIP = 'MOVEMENT_TYPE_WALK_IN_PLACE_DOWN'
    late = [lid(bd.obj(Q, B_CLOUD[0], B_CLOUD[1], P + 'Cloud', ni_items('YoshisIsland_Beach')['ITEM_SHALOUR_SABLE'][0],
                       WIP), 'LOCALID_YI_BEACH_CLOUD')]          # nieuwe objecten achteraan (na de item balls)
    io, ib = items_of('YoshisIsland_Beach')
    warps = [bd.warp(B_LAND[0], B_LAND[1], HUB_DEST[0], HUB_DEST[1], elev=3),
             bd.warp(B_RIFT[0], B_RIFT[1], HUB_DEST[0], HUB_DEST[1], elev=3),
             bd.warp(B_RIFT[0] + 1, B_RIFT[1], HUB_DEST[0], HUB_DEST[1], elev=3),
             bd.warp(B_PIPE[0], B_PIPE[1] + 1, 'YOSHIS_ISLAND_HILLS', 0, elev=3),
             bd.warp(B_PIPE[0] + 1, B_PIPE[1] + 1, 'YOSHIS_ISLAND_HILLS', 1, elev=3),
             bd.warp(B_JPIPE[0], B_JPIPE[1] + 1, 'YOSHIS_ISLAND_JUNGLE', 0, elev=3),
             bd.warp(B_JPIPE[0] + 1, B_JPIPE[1] + 1, 'YOSHIS_ISLAND_JUNGLE', 1, elev=3),
             bd.warp(B_HOUSE_DOOR[0], B_HOUSE_DOOR[1], 'YOSHIS_ISLAND_YOSHI_HOUSE', 0, elev=3),
             bd.warp(B_HOUSE_DOOR[0] + 1, B_HOUSE_DOOR[1], 'YOSHIS_ISLAND_YOSHI_HOUSE', 0, elev=3)]
    write_map('YoshisIsland_Beach', lay['YoshisIsland_Beach'], objs + io + late, warps,
              [bd.sign(B_SIGN[0], B_SIGN[1], P + 'Sign'), bd.sign(B_MSG[0], B_MSG[1], P + 'MsgBlock'),
               bd.sign(B_MAIL[0], B_MAIL[1], P + 'Mailbox')] + ib,
              music='MUS_RG_BERRY_PICK')
    # heuvels
    P = 'YoshisIsland_Hills_EventScript_'
    objs = [lid(bd.obj(Y, H_YOSHI[0], H_YOSHI[1], P + 'Yoshi', 'FLAG_YI_YOSHI_HOME'), 'LOCALID_YI_HILLS_YOSHI'),
            lid(bd.obj(SHY_GFX['pink'], H_CAMP_A[0][0], H_CAMP_A[0][1], P + 'CampA', 'FLAG_YI_CAMP_A'), 'LOCALID_YI_CAMP_A1'),
            lid(bd.obj(SHY_GFX['black'], H_CAMP_A[1][0], H_CAMP_A[1][1], P + 'CampA', 'FLAG_YI_CAMP_A'), 'LOCALID_YI_CAMP_A2'),
            lid(bd.obj(SHY_GFX['red'], H_CAMP_B[0][0], H_CAMP_B[0][1], P + 'CampB', 'FLAG_YI_CAMP_B',
                       'MOVEMENT_TYPE_FACE_RIGHT'), 'LOCALID_YI_CAMP_B1'),
            lid(bd.obj(SHY_GFX['green'], H_CAMP_B[1][0], H_CAMP_B[1][1], P + 'CampB', 'FLAG_YI_CAMP_B',
                       'MOVEMENT_TYPE_FACE_RIGHT'), 'LOCALID_YI_CAMP_B2'),
            lid(bd.obj(SHY_GFX['black'], H_GATE_GUARD[0], H_GATE_GUARD[1], P + 'GateGuard', 'FLAG_YI_BOO_DONE'),
                'LOCALID_YI_GATE_GUARD'),
            lid(bd.obj('OBJ_EVENT_GFX_SPECIES(PECHARUNT)', H_PECHA[0], H_PECHA[1], P + 'Pecharunt',
                       'FLAG_YI_PECHARUNT_DONE', 'MOVEMENT_TYPE_FACE_LEFT'), 'LOCALID_YI_PECHARUNT')]
    late = [lid(bd.obj(Q, H_CLOUD[0], H_CLOUD[1], P + 'StarCloud', 'FLAG_YI_STAR_CLOUD', WIP), 'LOCALID_YI_STAR_CLOUD')]
    io, ib = items_of('YoshisIsland_Hills')
    warps = [bd.warp(H_PIPE[0], H_PIPE[1] + 1, 'YOSHIS_ISLAND_BEACH', 3, elev=3),
             bd.warp(H_PIPE[0] + 1, H_PIPE[1] + 1, 'YOSHIS_ISLAND_BEACH', 4, elev=3),
             bd.warp(H_BOO_DOOR[0], H_BOO_DOOR[1], 'YOSHIS_ISLAND_BOO_MANSION', 0, elev=3),
             bd.warp(H_FORT_DOOR[0], H_FORT_DOOR[1], 'YOSHIS_ISLAND_WARIO_FORT', 0, elev=3)]
    write_map('YoshisIsland_Hills', lay['YoshisIsland_Hills'], objs + io + late, warps,
              [bd.sign(H_SIGN[0], H_SIGN[1], P + 'Sign')] + ib, music='MUS_RG_FOLLOW_ME')
    # spookhuis
    P = 'YoshisIsland_BooMansion_EventScript_'
    objs = [lid(bd.obj('OBJ_EVENT_GFX_COMMANDER_BOO', BM_BOO[0], BM_BOO[1], P + 'Boo', 'FLAG_YI_BOO_DONE'), 'LOCALID_YI_BOO'),
            lid(bd.obj(Y, 11, 11, P + 'Yoshi', 'FLAG_YI_YOSHI_HOME', 'MOVEMENT_TYPE_FACE_UP'), 'LOCALID_YI_BOO_YOSHI')]
    io, ib = items_of('YoshisIsland_BooMansion')
    bgs = [bd.sign(x, 2, P + 'Portrait', 'BG_EVENT_PLAYER_FACING_NORTH') for x in (4, 8, 12)]
    write_map('YoshisIsland_BooMansion', lay['YoshisIsland_BooMansion'], objs + io,
              [bd.warp(BM_EXIT[0], BM_EXIT[1], 'YOSHIS_ISLAND_HILLS', 2, elev=3)], bgs + ib,
              music='MUS_RG_POKE_MANSION', map_type='MAP_TYPE_INDOOR', show_map_name=False)
    # fort
    P = 'YoshisIsland_WarioFort_EventScript_'
    objs = [lid(bd.obj('OBJ_EVENT_GFX_WARIO', WF_WARIO[0], WF_WARIO[1], P + 'Wario', 'FLAG_YI_WARIO_DONE'), 'LOCALID_YI_WARIO'),
            lid(bd.obj(SHY_GFX['black'], WF_GUARDS[0][0], WF_GUARDS[0][1], P + 'Guards', 'FLAG_YI_FORT_GUARDS'),
                'LOCALID_YI_FORT_GUARD_A'),
            lid(bd.obj(SHY_GFX['pink'], WF_GUARDS[1][0], WF_GUARDS[1][1], P + 'Guards', 'FLAG_YI_FORT_GUARDS'),
                'LOCALID_YI_FORT_GUARD_B'),
            lid(bd.obj(Y, 10, 6, P + 'Yoshi', 'FLAG_YI_YOSHI_HOME', 'MOVEMENT_TYPE_FACE_LEFT'), 'LOCALID_YI_FORT_YOSHI')]
    io, ib = items_of('YoshisIsland_WarioFort')
    bgs = [bd.sign(8, 3, P + 'Throne', 'BG_EVENT_PLAYER_FACING_NORTH'), bd.sign(9, 3, P + 'Throne', 'BG_EVENT_PLAYER_FACING_NORTH')]
    write_map('YoshisIsland_WarioFort', lay['YoshisIsland_WarioFort'], objs + io,
              [bd.warp(WF_EXIT[0], WF_EXIT[1], 'YOSHIS_ISLAND_HILLS', 3, elev=3)], bgs + ib,
              music='MUS_RG_ROCKET_HIDEOUT', map_type='MAP_TYPE_INDOOR', show_map_name=False)
    # jungle
    P = 'YoshisIsland_Jungle_EventScript_'
    ji = ni_items('YoshisIsland_Jungle')
    objs = [lid(bd.obj('OBJ_EVENT_GFX_POOCHY', J_POOCHY[0], J_POOCHY[1], P + 'Poochy', '0', 'MOVEMENT_TYPE_FACE_RIGHT'),
                'LOCALID_YI_POOCHY'),
            lid(bd.obj('OBJ_EVENT_GFX_NEP_ENUT', J_NEP[0], J_NEP[1], P + 'NepEnut', '0', elev=0),
                'LOCALID_YI_NEP_ENUT'),
            lid(bd.obj(Q, J_CLOUD[0], J_CLOUD[1], P + 'Cloud', ji['ITEM_MOOMOO_MILK'][0], WIP), 'LOCALID_YI_JUNGLE_CLOUD'),
            bd.tr(SHY_GFX['green'], J_SHY[0], J_SHY[1], P + 'ShyGuy', 'LEFT', 3)]
    io, ib = items_of('YoshisIsland_Jungle')
    warps = [bd.warp(J_PIPE[0], J_PIPE[1] + 1, 'YOSHIS_ISLAND_BEACH', 5, elev=3),
             bd.warp(J_PIPE[0] + 1, J_PIPE[1] + 1, 'YOSHIS_ISLAND_BEACH', 6, elev=3),
             bd.warp(J_CAVE[0], J_CAVE[1] + 1, 'YOSHIS_ISLAND_CAVE', 0, elev=3),
             bd.warp(J_CAVE[0] + 1, J_CAVE[1] + 1, 'YOSHIS_ISLAND_CAVE', 0, elev=3),
             bd.warp(J_PIPE2[0], J_PIPE2[1] + 1, 'YOSHIS_ISLAND_FLOWERS', 0, elev=3),
             bd.warp(J_PIPE2[0] + 1, J_PIPE2[1] + 1, 'YOSHIS_ISLAND_FLOWERS', 1, elev=3)]
    bgs = [bd.sign(x, y, P + k) for (x, y), k in zip(J_MSG, ('MsgEntrance', 'MsgThorns', 'MsgLake'))]
    bgs += [bd.sign(18, 6, P + 'EggBlock')]
    write_map('YoshisIsland_Jungle', lay['YoshisIsland_Jungle'], objs + io, warps, bgs + ib,
              music='MUS_RG_VIRIDIAN_FOREST')
    # Yoshi-huis
    P = 'YoshisIsland_YoshiHouse_EventScript_'
    objs = [bd.obj('OBJ_EVENT_GFX_YOSHI_' + col, x, y, P + 'Yoshi' + ''.join(w.capitalize() for w in col.split('_')),
                   '0', mv) for col, x, y, mv in YH_YOSHIS]
    bgs = [bd.sign(6, 3, P + 'Hearth', 'BG_EVENT_PLAYER_FACING_NORTH'), bd.sign(7, 3, P + 'Hearth', 'BG_EVENT_PLAYER_FACING_NORTH'),
           bd.sign(3, 3, P + 'Portrait', 'BG_EVENT_PLAYER_FACING_NORTH'), bd.sign(10, 3, P + 'Portrait', 'BG_EVENT_PLAYER_FACING_NORTH')]
    write_map('YoshisIsland_YoshiHouse', lay['YoshisIsland_YoshiHouse'], objs,
              [bd.warp(YH_EXIT[0], YH_EXIT[1], 'YOSHIS_ISLAND_BEACH', 7, elev=3)], bgs,
              music='MUS_RG_PALLET', map_type='MAP_TYPE_INDOOR', show_map_name=False)
    # kristalgrot
    P = 'YoshisIsland_Cave_EventScript_'
    objs = [bd.tr(SHY_GFX['black'], C_SHY[0], C_SHY[1], P + 'ShyGuy', 'LEFT', 3)]
    io, ib = items_of('YoshisIsland_Cave')
    bgs = [bd.sign(C_MSG[0], C_MSG[1], P + 'MsgBlock'), bd.sign(13, 4, P + 'EggBlock'), bd.sign(14, 4, P + 'EggBlock'),
           bd.sign(4, 5, P + 'Bucket'), bd.sign(5, 5, P + 'Bucket'), bd.sign(20, 14, P + 'Pow'), bd.sign(21, 14, P + 'Pow')]
    write_map('YoshisIsland_Cave', lay['YoshisIsland_Cave'], objs + io,
              [bd.warp(C_EXIT[0], C_EXIT[1], 'YOSHIS_ISLAND_JUNGLE', 2, elev=3)], bgs + ib,
              music='MUS_RG_MT_MOON', map_type='MAP_TYPE_UNDERGROUND')
    # bloemenveld
    P = 'YoshisIsland_Flowers_EventScript_'
    fi = ni_items('YoshisIsland_Flowers')
    objs = [lid(bd.obj(Q, F_BRIDGE_CLOUD[0], F_BRIDGE_CLOUD[1], P + 'BridgeCloud', 'FLAG_YI_BRIDGE_CLOUD', WIP),
                'LOCALID_YI_BRIDGE_CLOUD'),
            lid(bd.obj(Q, F_CLOUD[0], F_CLOUD[1], P + 'Cloud', fi['ITEM_LUMIOSE_GALETTE'][0], WIP),
                'LOCALID_YI_FLOWERS_CLOUD'),
            bd.tr(SHY_GFX['pink'], F_SHY[0], F_SHY[1], P + 'ShyGuy', 'RIGHT', 4)]
    io, ib = items_of('YoshisIsland_Flowers')
    warps = [bd.warp(F_PIPE[0], F_PIPE[1] + 1, 'YOSHIS_ISLAND_JUNGLE', 4, elev=3),
             bd.warp(F_PIPE[0] + 1, F_PIPE[1] + 1, 'YOSHIS_ISLAND_JUNGLE', 5, elev=3)]
    bgs = [bd.sign(x, y, P + k) for (x, y), k in zip(F_MSG, ('MsgEntrance', 'MsgGoal', 'MsgBridge'))]
    bgs += [bd.sign(F_SWITCH[0] + dx, F_SWITCH[1] + 1, P + 'Switch') for dx in (0, 1)]
    bgs += [bd.sign(13, 19, P + 'EggBlock'), bd.sign(24, 17, P + 'EggBlock')]
    write_map('YoshisIsland_Flowers', lay['YoshisIsland_Flowers'], objs + io, warps, bgs + ib,
              music='MUS_RG_BERRY_PICK')


# ====================================================================== controle
def check(maps):
    probs = []
    B, Hm, BM, WF = (maps[k] for k in ('beach', 'hills', 'boo', 'fort'))

    def adj(r, p):
        return any((p[0] + dx, p[1] + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    # strand
    guards = set(B_GUARDS)
    start = B_LAND
    r = B.reach(start, guards | {B_YOSHI})
    for p in guards | {B_YOSHI, B_SIGN}:
        if not adj(r, p):
            probs.append(('strand: onbereikbaar', p))
    for x in (B_RIFT[0], B_RIFT[0] + 1):
        if (x, B_RIFT[1]) not in r:
            probs.append(('strand: scheur onbereikbaar', x))
    pipe = {(B_PIPE[0], B_PIPE[1] + 1), (B_PIPE[0] + 1, B_PIPE[1] + 1)}
    if pipe & r:
        probs.append(('strand: pijp bereikbaar zonder de wachters', None))
    r2 = B.reach(start, {B_YOSHI})
    if not (pipe & r2):
        probs.append(('strand: pijp onbereikbaar', None))
    for x, y, *_ in ITEMS['YoshisIsland_Beach']:
        if not (adj(r, (x, y)) or (x, y) in r):
            probs.append(('strand: item onbereikbaar', (x, y)))
    for (x, y) in [(B_YOSHI[0], B_YOSHI[1] + k) for k in range(4)] + [(B_YOSHI[0] + 1, B_YOSHI[1] + 3)]:
        if B.solid[y, x] or B.T[y, x] == 'w':
            probs.append(('strand: Yoshi-loopje geblokkeerd', (x, y)))
    # heuvels
    camp_b, gate = set(H_CAMP_B), {H_GATE_GUARD}
    npcs = set(H_CAMP_A) | camp_b | gate | {H_YOSHI, H_PECHA}
    start = (H_PIPE[0], H_PIPE[1] + 1)
    r = Hm.reach(start, npcs)
    for p in npcs | {H_SIGN}:
        if not adj(r, p):
            probs.append(('heuvels: onbereikbaar', p))
    if H_BOO_DOOR in r:
        probs.append(('heuvels: spookhuis bereikbaar zonder bende B', None))
    if H_FORT_DOOR in r:
        probs.append(('heuvels: fort bereikbaar zonder Boo', None))
    if H_BOO_DOOR not in Hm.reach(start, npcs - camp_b):
        probs.append(('heuvels: spookhuisdeur onbereikbaar', None))
    if H_FORT_DOOR not in Hm.reach(start, npcs - gate):
        probs.append(('heuvels: fortdeur onbereikbaar', None))
    rall = Hm.reach(start, npcs - camp_b - gate)
    for x, y, *_ in ITEMS['YoshisIsland_Hills']:
        if not (adj(rall, (x, y)) or (x, y) in rall):
            probs.append(('heuvels: item onbereikbaar', (x, y)))
    # binnen
    r = BM.reach(BM_EXIT, {BM_BOO, (11, 11)})
    for p in (BM_BOO, (11, 11)):
        if not adj(r, p):
            probs.append(('spookhuis: onbereikbaar', p))
    for x, y, *_ in ITEMS['YoshisIsland_BooMansion']:
        if not adj(r, (x, y)):
            probs.append(('spookhuis: item onbereikbaar', (x, y)))
    g = set(WF_GUARDS)
    r = WF.reach(WF_EXIT, g | {WF_WARIO, (10, 6)})
    if adj(r, WF_WARIO):
        probs.append(('fort: Wario bereikbaar zonder de wachters', None))
    for p in g:
        if not adj(r, p):
            probs.append(('fort: wachter onbereikbaar', p))
    r2 = WF.reach(WF_EXIT, {WF_WARIO, (10, 6)})
    if not adj(r2, WF_WARIO):
        probs.append(('fort: Wario onbereikbaar', None))
    for x, y, *_ in ITEMS['YoshisIsland_WarioFort']:
        if not adj(r2, (x, y)):
            probs.append(('fort: item onbereikbaar', (x, y)))
    # strand: nieuwe pijp, Message Block, ?-wolk
    r = B.reach(B_LAND, {B_YOSHI, B_CLOUD} | set(B_GUARDS))
    for p in (B_MSG, B_CLOUD):
        if not adj(r, p):
            probs.append(('strand: onbereikbaar', p))
    if not {(B_JPIPE[0], B_JPIPE[1] + 1), (B_JPIPE[0] + 1, B_JPIPE[1] + 1)} <= r:
        probs.append(('strand: junglepijp onbereikbaar', None))
    if not {B_HOUSE_DOOR, (B_HOUSE_DOOR[0] + 1, B_HOUSE_DOOR[1])} <= r:
        probs.append(('strand: deur Yoshi-huis onbereikbaar', None))
    if not adj(r, B_MAIL):
        probs.append(('strand: brievenbus onbereikbaar', None))
    YHm = maps['house']
    yp = {(x, y) for _, x, y, _ in YH_YOSHIS}
    r_h = YHm.reach(YH_EXIT, yp)
    for p_ in yp | {(6, 3), (3, 3), (10, 3)}:
        if not adj(r_h, p_) and p_ not in r_h:
            probs.append(('Yoshi-huis: onbereikbaar', p_))
    if not adj(Hm.reach((H_PIPE[0], H_PIPE[1] + 1), npcs | {H_CLOUD}), H_CLOUD):
        probs.append(('heuvels: ?-wolk onbereikbaar', None))
    # jungle
    Jm = maps['jungle']
    t0, t1, ty = J_THORN
    npc = {J_POOCHY, J_NEP, J_SHY, J_CLOUD}
    if Jm.T[J_NEP[1], J_NEP[0]] != 'w' or Jm.T[J_NEP[1] + 1, J_NEP[0]] == 'w':
        probs.append(('jungle: Nep-Enut niet in het water aan de oever', J_NEP))
    r = Jm.reach((J_PIPE[0], J_PIPE[1] + 1), npc)
    for p in (J_NEP, J_SHY, *J_MSG):
        if not adj(r, p):
            probs.append(('jungle: onbereikbaar', p))
    if (t1 + 1, ty) not in r:
        probs.append(('jungle: oostoever bij Poochy onbereikbaar', None))
    if (t0 - 1, ty) in r or J_CLOUD in r:
        probs.append(('jungle: bosje bereikbaar zonder Poochy', None))
    for c in ((J_CAVE[0], J_CAVE[1] + 1), (J_CAVE[0] + 1, J_CAVE[1] + 1), (J_PIPE2[0], J_PIPE2[1] + 1),
              (J_PIPE2[0] + 1, J_PIPE2[1] + 1)):
        if c not in r:
            probs.append(('jungle: warp onbereikbaar', c))
    for x in range(t0, t1 + 1):
        if not Jm.solid[ty, x]:
            probs.append(('jungle: doorn niet vast', x))
    for x in range(t0 - 1, t1 + 3):             # de rit: Poochy loopt tot t1+2 (oost) en t0-2 (west)
        if x < t0 or x > t1:
            if Jm.solid[ty, x]:
                probs.append(('jungle: Poochy-rit geblokkeerd', x))
    if Jm.solid[ty, t0 - 2]:
        probs.append(('jungle: Poochy-rit geblokkeerd', t0 - 2))
    grove = Jm.reach((t0 - 1, ty), npc)
    for p in [J_CLOUD] + [NI_SPOTS['YoshisIsland_Jungle'][k] for k in NI_SPOTS['YoshisIsland_Jungle']]:
        if not (adj(grove, p) or p in grove):
            probs.append(('jungle: bosje-item onbereikbaar', p))
    # grot
    Cm = maps['cave']
    r = Cm.reach(C_EXIT, {C_SHY})
    for p in [C_SHY, C_MSG] + list(NI_SPOTS['YoshisIsland_Cave'].values()):
        if not (adj(r, p) or p in r):
            probs.append(('grot: onbereikbaar', p))
    # bloemenveld: noordkant alleen over de brug
    Fm = maps['flowers']
    npc = {F_BRIDGE_CLOUD, F_CLOUD, F_SHY}
    start = (F_PIPE[0], F_PIPE[1] + 1)
    r = Fm.reach(start, npc)
    for p in (F_BRIDGE_CLOUD, F_CLOUD, F_SHY, F_MSG[0], F_MSG[2], (F_SWITCH[0], F_SWITCH[1] + 1)):
        if not adj(r, p):
            probs.append(('bloemenveld: onbereikbaar', p))
    goal = NI_SPOTS['YoshisIsland_Flowers']['ITEM_CHERISH_BALL']
    if adj(r, goal) or adj(r, F_MSG[1]):
        probs.append(('bloemenveld: noordkant bereikbaar zonder brug', None))
    bx, by, bh = F_BRIDGE
    sol = Fm.solid.copy()
    for (x, y) in Fm.extra:
        Fm.solid[y, x] = False
    Fm.T[by:by + bh, bx:bx + 2] = 'g'
    r = Fm.reach(start, npc)
    Fm.solid[...] = sol; Fm.T[by:by + bh, bx:bx + 2] = 'k'
    for p in (goal, F_MSG[1]):
        if not adj(r, p):
            probs.append(('bloemenveld: noordkant onbereikbaar met brug', p))
    for p in probs:
        print('PROBLEEM', p)
    assert not probs
    print('bereikbaarheid in orde')


# ====================================================================== render (uit de echte tilesets)
def render(grids, maps, outdir):
    import gridrender as gr
    os.makedirs(outdir, exist_ok=True)
    out = {}
    for key, m in maps.items():
        sec = SECS[m.name][1].split('/')[-1]
        im = gr.render(grids[m.name].tolist(), 'yoshi_island_base', sec)
        im.save(os.path.join(outdir, m.name + '.png'))
        out[key] = im
    # overzicht: heuvels boven het strand (pijp op pijp), binnenkaarten rechts
    b, h, bm, wf = out['beach'], out['hills'], out['boo'], out['fort']
    W = max(b.width, h.width) + 32 + max(bm.width, wf.width)
    Hh = h.height + 16 + b.height
    ov = Image.new('RGB', (W, Hh), (24, 24, 32))
    ov.paste(h, (0, 0))
    ov.paste(b, ((H_PIPE[0] - B_PIPE[0]) * 16, h.height + 16))
    ov.paste(wf, (h.width + 32, 0))
    ov.paste(bm, (h.width + 32, wf.height + 16))
    ov.save(os.path.join(outdir, 'overzicht.png'))
    # tweede overzicht: jungle (met de grot erboven) en het bloemenveld
    j, f, c = out['jungle'], out['flowers'], out['cave']
    ov = Image.new('RGB', (j.width + 32 + f.width, c.height + 16 + max(j.height, f.height)), (24, 24, 32))
    ov.paste(c, ((J_CAVE[0] - C_EXIT[0]) * 16, 0))
    ov.paste(j, (0, c.height + 16))
    ov.paste(f, (j.width + 32, c.height + 16))
    ov.save(os.path.join(outdir, 'overzicht_2.png'))
    # derde: strand met het Yoshi-huis en het interieur ernaast
    yh = out['house']
    ov = Image.new('RGB', (b.width + 32 + yh.width, max(b.height, yh.height)), (24, 24, 32))
    ov.paste(b, (0, 0)); ov.paste(yh, (b.width + 32, 0))
    ov.save(os.path.join(outdir, 'overzicht_yoshihuis.png'))


SECS = {  # kaart -> (symbool, map)
    'YoshisIsland_Beach': ('YoshiBeach', 'data/tilesets/secondary/yoshi_beach'),
    'YoshisIsland_Hills': ('YoshiHills', 'data/tilesets/secondary/yoshi_hills'),
    'YoshisIsland_BooMansion': ('YoshiBoo', 'data/tilesets/secondary/yoshi_boo'),
    'YoshisIsland_WarioFort': ('YoshiFort', 'data/tilesets/secondary/yoshi_fort'),
    'YoshisIsland_Jungle': ('YoshiJungle', 'data/tilesets/secondary/yoshi_jungle'),
    'YoshisIsland_Cave': ('YoshiCave', 'data/tilesets/secondary/yoshi_cave'),
    'YoshisIsland_Flowers': ('YoshiFlowers', 'data/tilesets/secondary/yoshi_flowers'),
    'YoshisIsland_YoshiHouse': ('YoshiHouse', 'data/tilesets/secondary/yoshi_house'),
}


def main():
    load_bd()
    O = objects()
    maps = {'beach': beach_map(), 'hills': hills_map(), 'boo': boo_mansion_map(), 'fort': wario_fort_map(),
            'jungle': jungle_map(), 'cave': cave_map(), 'flowers': flowers_map(), 'house': yoshi_house_map()}
    cvs = {k: m.render(O, SEED + i) for i, (k, m) in enumerate(maps.items())}
    for m in maps.values():
        if m.name in ('YoshisIsland_Beach', 'YoshisIsland_Jungle'):
            m.beh[(m.T == 's') & (m.beh == 0)] = MB['sand']
    maps['cave'].beh[(maps['cave'].T == 'f') & (maps['cave'].beh == 0)] = MB['cave']   # wilde Pokemon op de grotvloer
    maps['flowers'].extra = bridge_cells(maps['flowers'], cvs['flowers'])
    # de primary komt alleen uit strand + heuvels (zo blijft de volle heuvel-secondary gelijk); de nieuwe kaarten
    # hergebruiken wat ze daaruit kunnen en krijgen verder elk een eigen secondary
    out = [(maps[k], cvs[k], SECS[maps[k].name][1], SECS[maps[k].name][0]) for k in ('beach', 'hills')]
    ins = [(maps[k], cvs[k], SECS[maps[k].name][1], SECS[maps[k].name][0]) for k in ('boo', 'fort', 'jungle', 'cave', 'flowers', 'house')]
    grids = build_tilesets(out, ins)
    write_tilesets([(SECS[n][0], SECS[n][1], True, "Yoshi's Island: " + n.split('_')[1]) for n in SECS])
    lay = {}
    for k, m in maps.items():
        g = grids[m.name]
        # rand: een cel helemaal binnen een plateau (buiten) of de leegte (binnen)
        if isinstance(m, Inside):
            bmt = int(g[0, 0])
        else:
            ch = 'J' if (m.T == 'J').any() else ('H' if (m.T == 'H').any() else 'k')
            ys, xs = np.where((m.T == ch) & ~m.objmask)
            cand = [(y, x) for y, x in zip(ys, xs) if 0 < y < m.H - 1 and 0 < x < m.W - 1 and (m.T[y - 1:y + 2, x - 1:x + 2] == ch).all()]
            y, x = cand[0]
            bmt = int(g[y, x])
        lay[m.name] = save_layout(m, g, SECS[m.name][0], bmt)
    flags()
    import nieuwe_items
    nieuwe_items.flags()
    mapsecs()
    bd.WILD = WILD
    bd.wild()
    trainer_class()
    trainers()
    partner()
    battle_setup()
    stadium()
    map_jsons(lay)
    beach_scripts()
    hills_scripts()
    boo_scripts()
    fort_scripts()
    jungle_scripts()
    cave_scripts()
    flowers_scripts(maps['flowers'])
    house_scripts()
    check(maps)
    if len(sys.argv) > 1:
        return grids, maps
    return grids, maps


if __name__ == '__main__':
    g, m = main()
    if len(sys.argv) > 1:
        try:
            render(g, m, sys.argv[1])
        except FileNotFoundError as e:
            print('render overgeslagen (eerst make voor de tiles.4bpp):', e)
