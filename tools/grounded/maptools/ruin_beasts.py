"""Project Grounded: de vier Beasts of Ruin, elk verzegeld in een schrijn (post-game).
- Vier kleine tilesets (data/tilesets/secondary/ruin_{fire,earth,moss,ice}) uit Ekat99's Volcano Set
  (graphics/grounded/tilesets/ekat99_lava_rotsen.png, 16x16-raster), per thema getint; primary = SnowTownBase
  (zoals de Regigigas-tempel), emit() uit snow_tileset.py. Per schrijn is de grot rond het beest op zijn eigen manier
  geruïneerd (ruin_fire/earth/moss/ice hieronder; per pixel getekend, plus uitsneden uit Ekat's Haunted Woods en Egypt
  in graphics/grounded/tilesets/ekat/). RUIN_PREVIEW=<map> schrijft ook een canvas-png per kaart.
- Kaarten (gMapGroup_Grounded):
  JaggedPass_RuinChamber  Chi-Yu (beads), ingang = grotopening bovenin Jagged Pass (11,6)
  JaggedPass_RuinCaldera  oud lavaveld (tot v0.9.172 met Chi-Yu); onbereikbaar, alleen een uitgang terug (oude saves)
  DesertUnderpass_RuinShrine  Ting-Lu (vessels), opening in de zuidwand van de Desert Underpass (61,13)
  PetalburgWoods_RuinShrine   Wo-Chien (tablets), verborgen boomgat (zoals naar Toadstool Hollow) in de zuidoosthoek van Petalburg Woods (43,36)
  Route135_RuinShrine         Chien-Pao (sword), grot in de klif van Route 135 (51,21)
- Mechaniek: aanspreken zet de zegelvlag (FLAG_RUIN_SEAL_*); na de Hall of Fame breken de zegels pas als alle
  vier de schrijnen bezocht zijn (bezoeken vóór de HoF tellen mee). Dan lv 70, MUS_RG_VS_LEGEND (placeholder).
Idempotent (outdoor-kaarten worden alleen gewijzigd als ze nog de oude tegels hebben).
Gebruik: python3 tools/grounded/maptools/ruin_beasts.py"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, math, os, random, struct, zlib
from collections import deque
import numpy as np
from PIL import Image

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)
src = open('tools/grounded/snow_tileset.py').read()
ns = {'np': np, 'Image': Image, 'struct': struct, 'os': os, 'LAYER_COVERED': 1}
exec(src[src.index('def to5('):src.rindex('\nif TOWN:')], ns)
emit = ns['emit']

SHEET = np.array(Image.open('graphics/grounded/tilesets/ekat99_lava_rotsen.png').convert('RGBA')).astype(float)
SOUTH, NORTH = 0x65, 0x64


def tint(theme):
    a = SHEET.copy(); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    if theme == 'earth':
        a[..., 0], a[..., 1], a[..., 2] = r * 1.05 + 14, g * 1.0 + 8, b * 0.72
    elif theme == 'moss':
        a[..., 0], a[..., 1], a[..., 2] = r * 0.80, g * 0.95 + 14, b * 0.70 + 2
    elif theme == 'ice':
        L = 0.3 * r + 0.59 * g + 0.11 * b
        a[..., 0], a[..., 1], a[..., 2] = L * 0.80 + 26, L * 0.95 + 40, L * 1.05 + 66
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')


FLOORS = [(6, 18), (7, 18), (6, 19), (7, 19), (1, 3)]
LAVA = [(0, 18), (1, 18), (2, 18)]
POOL = {'NW': (3, 14), 'N': (5, 13), 'NE': (7, 14), 'W': (3, 15), 'E': (7, 15), 'S': (5, 17)}


class Map:
    def __init__(s, W, H, seed):
        s.W, s.H = W, H
        s.rnd = random.Random(seed)
        s.floor = set(); s.lava = set(); s.cell = {}; s.block = set(); s.beh = {}
        s.fv = {(x, y): s.rnd.choice((0, 0, 1, 1, 2, 3, 4)) for x in range(W) for y in range(H)}

    def rect(s, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.floor.add((x, y))

    def pool(s, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                k = 'N' if y == y0 else None
                if x == x0: k = 'NW' if y == y0 else 'W'
                elif x == x1: k = 'NE' if y == y0 else 'E'
                s.cell[(x, y)] = ('c', POOL[k] if k else LAVA[(x + y) % 3], 0)
                s.block.add((x, y)); s.lava.add((x, y))
        for x in range(x0, x1 + 1):
            if (x, y1 + 1) in s.floor and (x, y1 + 1) not in s.lava:
                s.cell[(x, y1 + 1)] = ('c', POOL['S'], 0)

    def bridge(s, x, y0, y1):
        for y in range(y0, y1 + 1):
            s.cell[(x, y)] = ('c', (1, 24 + (y % 2)), 0); s.block.discard((x, y)); s.lava.discard((x, y))

    def stake(s, x, y):  # rotspilaar van 1x2 als zegelstaak
        s.cell[(x, y)] = ('o', (4, 6)); s.cell[(x, y + 1)] = ('o', (4, 7)); s.block |= {(x, y), (x, y + 1)}

    def exit(s, x, y, beh):
        s.floor.add((x, y)); s.beh[(x, y)] = beh

    def decor(s, n, cells, avoid, blocking=False, opaque=False):
        free = [p for p in sorted(s.floor) if p not in s.cell and p not in avoid and p not in s.beh
                and 1 <= p[1] < s.H - 1]
        for p in s.rnd.sample(free, min(n, len(free))):
            c = s.rnd.choice(cells)
            s.cell[p] = ('c', c, 0) if opaque else ('o', c)
            if blocking: s.block.add(p)

    def keys(s):
        """grid van metatile-sleutels + botsing"""
        F = s.floor
        out = []
        for y in range(s.H):
            row = []
            for x in range(s.W):
                p = (x, y); fv = s.fv[p]
                if p in s.cell:
                    k = s.cell[p]
                    k = ('o', k[1], fv) if k[0] == 'o' else k
                    row.append((k, p in s.block)); continue
                if p in F:
                    row.append((('x', fv, s.beh[p]) if p in s.beh else ('f', fv), False)); continue
                if (x, y + 1) in F: c = (x % 2, 8)
                elif (x + 1, y) in F: c = (0, 3)
                elif (x - 1, y) in F: c = (2, 3)
                elif (x, y - 1) in F: c = (x % 2, 9)
                else: c = (x % 2, 6 + (y % 2))
                row.append((('c', c, 0), True))
            out.append(row)
        return out

    def reach(s, start):
        seen = {start}; q = deque([start])
        while q:
            x, y = q.popleft()
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + d[0], y + d[1])
                if n in s.floor and n not in s.block and n not in seen:
                    seen.add(n); q.append(n)
        return seen


def shrine(seed, north_exit=False):
    """13x11: zaal x 2-10 / y 2-8, gang naar de uitgang onderin (6,10), beest op (6,3), vier staken."""
    m = Map(13, 11, seed)
    m.rect(2, 2, 10, 8); m.rect(6, 9, 6, 9); m.exit(6, 10, SOUTH)
    if north_exit:
        m.rect(6, 1, 6, 1); m.exit(6, 0, NORTH)
    for (x, y) in ((3, 2), (9, 2), (3, 6), (9, 6)):
        m.stake(x, y)
    return m


def caldera(seed):
    """20x18: lavaband met brug, twee lavapoelen naast het altaar, Chi-Yu bovenin (9,4)."""
    m = Map(20, 18, seed)
    m.rect(2, 2, 17, 15); m.rect(9, 16, 9, 16); m.exit(9, 17, SOUTH)
    m.pool(2, 9, 17, 11); m.bridge(9, 9, 11)
    m.pool(3, 3, 5, 6); m.pool(14, 3, 16, 6)
    for (x, y) in ((7, 3), (11, 3), (7, 6), (11, 6)):
        m.stake(x, y)
    return m


MAPS = {}
# ---------------------------------------------------------------- de kaarten
# Elk schrijn: een uitgeholde kamer (zaal x 2-10 / y 2-8), vier staken, het beest op (6,3). Rond het beest is de grot
# op de eigen manier van het beest geruïneerd. Dat wordt per pixel op een canvas van de hele kaart getekend (geditherde
# overgangen, scheuren, wortels, ijs) en daarna weer in metatiles geknipt; zo lopen effecten over tegelgrenzen heen
# zonder halve tegels.
EKAT = 'graphics/grounded/tilesets/ekat/'   # uitsneden uit Ekat's Public Tiles (zie CREDITS.md)
ROT = np.array(Image.open(EKAT + 'haunted_woods_rot.png').convert('RGBA')).astype(float)     # Haunted Woods, (0,3)-(5,6)
VINES = np.array(Image.open(EKAT + 'haunted_woods_vines.png').convert('RGBA')).astype(float)  # Haunted Woods, (5,44)-(8,47)
VASES = np.array(Image.open(EKAT + 'egypt_vases.png').convert('RGBA')).astype(float)          # Egypt, (7,36)-(7,38)
B4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16

AVOID_SHRINE = {(x, y) for x in range(5, 8) for y in range(2, 11)} | {(4, 8), (8, 8), (3, 8), (9, 8), (4, 7), (8, 7), (2, 7), (10, 7)}


def crop(a, cx, cy, w=1, h=1):
    return a[cy * 16:(cy + h) * 16, cx * 16:(cx + w) * 16].copy()


def over(dst, src, x, y):
    """src (RGBA, float) op dst leggen met linksboven (x, y) in pixels"""
    h, w = src.shape[:2]
    H, W = dst.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x0 >= x1 or y0 >= y1: return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]; d = dst[y0:y1, x0:x1]
    a = (s[..., 3:4] > 127).astype(float)
    d[..., :3] = d[..., :3] * (1 - a) + s[..., :3] * a
    d[..., 3] = np.maximum(d[..., 3], s[..., 3] * a[..., 0])


def recolor(a, ramp):
    """grijswaarde -> kleurverloop (lijst RGB van donker naar licht); alfa blijft"""
    out = a.copy(); L = (0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]) / 255
    r = np.array(ramp, float); n = len(r) - 1
    t = np.clip(L * n, 0, n - 1e-6); i = t.astype(int); f = (t - i)[..., None]
    out[..., :3] = r[i] * (1 - f) + r[i + 1] * f
    return out


class Canvas:
    def __init__(s, m, sheet):
        s.m = m; W, H = m.W, m.H
        s.bot = np.zeros((H * 16, W * 16, 4)); s.top = np.zeros((H * 16, W * 16, 4))
        s.grid = m.keys()
        cell = lambda c: sheet[c[1] * 16:c[1] * 16 + 16, c[0] * 16:c[0] * 16 + 16]
        for y in range(H):
            for x in range(W):
                k, _ = s.grid[y][x]
                fl = cell(FLOORS[k[2] if k[0] in 'co' else k[1]])
                s.bot[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = fl
                if k[0] == 'c': over(s.bot, cell(k[1]), x * 16, y * 16)
                if k[0] == 'o': s.top[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = cell(k[1])
        yy, xx = np.mgrid[0:H * 16, 0:W * 16]
        s.yy, s.xx = yy, xx
        s.dith = B4[yy % 4, xx % 4]
        g = np.random.RandomState(m.W * 100 + m.H + len(m.floor)).uniform(-1, 1, (H + 3, W + 3))
        gy, gx = yy / 16.0, xx / 16.0; iy, ix = gy.astype(int), gx.astype(int); fy, fx = gy - iy, gx - ix
        fy, fx = fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)
        s.noise = (g[iy, ix] * (1 - fx) * (1 - fy) + g[iy, ix + 1] * fx * (1 - fy)
                   + g[iy + 1, ix] * (1 - fx) * fy + g[iy + 1, ix + 1] * fx * fy)
        # kamervloer (pixels), voor effecten die alleen op de grond horen
        s.floor = np.zeros((H * 16, W * 16), bool)
        for (x, y) in m.floor:
            s.floor[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = True
        # randen van de kaart (rij 0, kolom 0/W-1, onderste rijen) blijven schoon: daar sluit de border aan
        s.edge = (np.clip((yy - 14) / 10, 0, 1) * np.clip((xx - 14) / 10, 0, 1)
                  * np.clip((W * 16 - 14 - xx) / 10, 0, 1))

    def radial(s, cx, cy, r, fade, sy=1.0, wobble=0.22):
        """masker 1 binnen straal r, met een grillige rand (laagfrequente ruis) die over 'fade' pixels wegloopt"""
        d = np.hypot(s.xx - cx, (s.yy - cy) * sy) - s.noise * r * wobble
        return np.clip((r - d) / fade, 0, 1) * s.edge

    def apply(s, f, fn, where=None):
        """fn(rgb) -> rgb op de pixels waar het geditherde masker f aan staat"""
        on = f > s.dith
        if where is not None: on &= where
        rgb = s.bot[..., :3]; rgb[on] = fn(rgb[on])
        return on

    def line(s, x0, y0, x1, y1):
        pts = []; n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n):
            t = i / max(n - 1, 1)
            pts.append((int(round(x0 + (x1 - x0) * t)), int(round(y0 + (y1 - y0) * t))))
        return pts

    def crack(s, rnd, x, y, ang, L, seg=(3, 7), wob=0.65, branch=0.22, depth=0, out=None, ymin=22):
        """scheur als zigzag van korte rechte stukjes; geeft {(px, py): sterkte 0..1}"""
        out = {} if out is None else out
        dist = 0.0
        while dist < L:
            n = rnd.randint(*seg); a = ang + rnd.uniform(-wob, wob)
            x1, y1 = x + math.cos(a) * n, y + math.sin(a) * n
            if y1 < ymin: break                  # nooit tot tegen de bovenrand (daar sluit de border aan)
            for p in s.line(x, y, x1, y1):
                out[p] = max(out.get(p, 0), 1 - dist / L)
            x, y = x1, y1; dist += n
            if depth < 2 and rnd.random() < branch:
                s.crack(rnd, x, y, ang + rnd.choice((-1, 1)) * rnd.uniform(0.6, 1.1), (L - dist) * rnd.uniform(0.35, 0.6),
                        seg, wob, branch, depth + 1, out, ymin)
        return out

    def ok(s, x, y):
        return 16 <= y < s.bot.shape[0] - 16 and 16 <= x < s.bot.shape[1] - 16

    def paint_crack(s, pts, core, rim, hot=None, thick=0.6, hi=None, hot_at=0.75):
        """core: kleur van de scheur; rim: rand (4-buren); hi: lichte rand rechtsonder (diepte)"""
        P = dict(pts)
        for (x, y), w in pts.items():
            if w > thick:
                for q in ((x + 1, y), (x, y + 1)):
                    P[q] = max(P.get(q, 0), w)
        for (x, y) in P:
            for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if q not in P and s.ok(*q):
                    c = hi if hi is not None and q in ((x + 1, y), (x, y + 1)) else rim
                    s.bot[q[1], q[0], :3] = c(s.bot[q[1], q[0], :3]) if callable(c) else c
        for (x, y), w in P.items():
            if s.ok(x, y):
                s.bot[y, x, :3] = hot if hot is not None and w > hot_at else core
        return P

    def stamp(s, img, cx, cy, block=True, layer='bot'):
        """img (16x16 RGBA) op cel (cx, cy)"""
        over(s.bot if layer == 'bot' else s.top, img, cx * 16, cy * 16)
        if block: s.m.block.add((cx, cy))

    def cells(s):
        """(onder, boven, gedrag, botsing) per cel"""
        out = []
        for y in range(s.m.H):
            row = []
            for x in range(s.m.W):
                b = np.clip(s.bot[y * 16:y * 16 + 16, x * 16:x * 16 + 16], 0, 255); b[..., 3] = 255
                t = s.top[y * 16:y * 16 + 16, x * 16:x * 16 + 16]
                t = np.clip(t, 0, 255) if (t[..., 3] > 127).any() else None
                p = (x, y)
                blocked = s.grid[y][x][1] or p in s.m.block
                row.append((b, t, s.m.beh.get(p, 0), blocked))
            out.append(row)
        return out


BCX, BCY = 6 * 16 + 8, 3 * 16 + 10   # midden van het beest in pixels


def cap(a, L, top=22):
    """scheuren naar boven stoppen ruim onder de rand van de kaart (anders kapt de border ze af)"""
    up = -math.sin(a)
    return min(L, (BCY - top) / up) if up > 0.05 else L


def free_cells(m, n, avoid, rows=range(2, 9), cols=range(2, 11)):
    c = [(x, y) for y in rows for x in cols if (x, y) in m.floor and (x, y) not in m.cell and (x, y) not in avoid
         and (x, y) not in m.block]
    return m.rnd.sample(c, min(n, len(c)))


# ---- vuur (Chi-Yu): verschroeid, lavascheuren, gloeiende kieren in de wanden
def ruin_fire(cv, rnd):
    f = cv.radial(BCX, BCY, 62, 34, 1.1)
    cv.apply(f, lambda c: c * np.array([0.55, 0.42, 0.38]) + np.array([10, 2, 0]))                   # verschroeid
    cv.apply(cv.radial(BCX, BCY, 30, 18, 1.1) * 0.8, lambda c: c * np.array([0.45, 0.32, 0.28]) + 4)  # zwartgeblakerd hart
    for i in range(7):
        a = -math.pi / 2 + i * (2 * math.pi / 7) + rnd.uniform(-0.25, 0.25)
        L = cap(a, rnd.uniform(46, 70))
        pts = cv.crack(rnd, BCX + math.cos(a) * 6, BCY + math.sin(a) * 4, a, L, branch=0.18)
        cv.paint_crack(pts, core=(248, 136, 24), rim=(120, 36, 20), hot=(248, 232, 120), thick=0.55, hot_at=0.7)
    # gloeiende kieren in de wanden (los van de vloer): korte verticale scheurtjes in de noord- en zijwanden
    for (x, y, a, L) in ((4 * 16 + 9, 30, -1.45, 11), (8 * 16 + 5, 30, -1.7, 12), (1 * 16 + 9, 3 * 16, 1.5, 12),
                         (11 * 16 + 6, 3 * 16 + 4, 1.6, 12), (6 * 16 + 2, 30, -1.6, 9)):
        cv.paint_crack(cv.crack(rnd, x, y, a, L, seg=(2, 4), wob=0.5, branch=0.0), core=(248, 120, 24),
                       rim=(96, 28, 16), hot=(248, 216, 96), thick=0.75, hot_at=0.8)


# ---- aarde (Ting-Lu): gebarsten grond, scherven van de vaten
def ruin_earth(cv, rnd):
    cv.apply(cv.radial(BCX, BCY, 64, 36, 1.1) * 0.7, lambda c: c * 0.82)   # verzakte, stoffige grond
    hi_of = lambda c: tuple(min(255, v * 1.25 + 10) for v in c)
    dark = lambda c: c * 0.62
    allp = {}
    lip = lambda c: np.minimum(255, c * 1.32 + 12)
    for i in range(7):
        a = -math.pi / 2 + i * (2 * math.pi / 7) + rnd.uniform(-0.2, 0.2)
        L = cap(a, rnd.uniform(56, 84), 30)
        pts = cv.crack(rnd, BCX + math.cos(a) * 7, BCY + math.sin(a) * 5, a, L, seg=(5, 10), wob=0.4, branch=0.28)
        allp.update(cv.paint_crack(pts, core=(48, 30, 20), rim=dark, hi=lip, thick=0.8))
    # ringscheur rond het beest (de grond is onder hem weggezakt)
    ring = {}
    for k in range(60):
        t = k / 60 * 2 * math.pi; r = 24 + rnd.uniform(-1.5, 1.5)
        ring[(int(BCX + math.cos(t) * r), int(BCY + math.sin(t) * r * 0.75))] = 0.3
    ring = {p: w for p, w in ring.items() if rnd.random() < 0.8}
    allp.update(cv.paint_crack(ring, core=(48, 30, 20), rim=dark, hi=lip, thick=1.0))
    # losse schotsen: elk stuk grond tussen de scheuren een eigen tint (verschoven/verzakte platen)
    zone = (cv.radial(BCX, BCY, 86, 1, 1.1) > 0) & cv.floor
    free = zone & cv.floor
    for (x, y) in allp:
        for q in ((x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= q[1] < free.shape[0] and 0 <= q[0] < free.shape[1]: free[q[1], q[0]] = False
    seen = np.zeros_like(free)
    for y0, x0 in zip(*np.nonzero(free)):
        if seen[y0, x0]: continue
        reg = [(y0, x0)]; seen[y0, x0] = True; k = 0
        while k < len(reg):
            y, x = reg[k]; k += 1
            for q in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= q[0] < free.shape[0] and 0 <= q[1] < free.shape[1] and free[q] and not seen[q]:
                    seen[q] = True; reg.append(q)
        if len(reg) < 12: continue
        if any(not zone[min(y + 1, zone.shape[0] - 1), x] or not zone[max(y - 1, 0), x] or not zone[y, min(x + 1, zone.shape[1] - 1)]
               or not zone[y, max(x - 1, 0)] for y, x in reg): continue          # alleen platen die helemaal door scheuren omsloten zijn
        f = rnd.choice((0.8, 0.86, 0.92, 1.0, 1.0, 1.08))
        ys, xs = zip(*reg); cv.bot[list(ys), list(xs), :3] *= f
    # gebroken vaten (de bovenkant eraf, binnenkant donker) + scherven
    def pot(seed):
        r = random.Random(seed); img = np.zeros((16, 16, 4))
        ycut = [6 + r.choice((0, 0, 1, 2, -1)) for _ in range(16)]
        for y in range(16):
            for x in range(16):
                nx, ny = (x - 7.5) / 6.6, (y - 9.5) / 5.8
                if nx * nx + ny * ny > 1 or y < ycut[x]: continue
                edge = nx * nx + ny * ny > 0.72 or y == ycut[x] or (x > 0 and y < ycut[x - 1]) or (x < 15 and y < ycut[x + 1])
                inner = ((x - 7.5) / 5.0) ** 2 + ((y - 7.6) / 2.2) ** 2 < 1
                if edge: col = (64, 30, 20)
                elif inner: col = (52, 24, 16) if y < 8 else (84, 40, 26)
                else:
                    sh = -nx * 0.6 - ny * 0.5
                    col = (232, 156, 104) if sh > 0.35 else ((192, 104, 60) if sh > -0.25 else (140, 68, 40))
                    if y in (11, 12) and not edge: col = tuple(int(v * 0.72) for v in col) if y == 12 else (216, 176, 96)
                img[y, x] = (*col, 255)
        return img
    for (cx, cy) in ((4, 4), (8, 5), (10, 5), (2, 5)):
        cv.bot[cy * 16 + 14:cy * 16 + 16, cx * 16 + 2:cx * 16 + 14, :3] *= 0.7
        cv.stamp(pot(cx * 31 + cy), cx, cy)
    sh = [(64, 30, 20), (192, 104, 60), (232, 156, 104)]
    for (cx, cy) in ((4, 4), (8, 5), (10, 5), (2, 5), (6, 5), (5, 3), (7, 2)):
        for _ in range(5):
            x = cx * 16 + 8 + rnd.randint(-16, 16); y = cy * 16 + 12 + rnd.randint(-10, 12)
            w, h = rnd.choice(((3, 2), (2, 2), (4, 2), (3, 3), (2, 1)))
            if not all(cv.ok(x + i, y + j) and cv.floor[y + j, x + i] for i in range(-1, w + 1) for j in range(-1, h + 2)):
                continue
            if (int((x + 1) // 16), int((y + 1) // 16)) in cv.m.block and (cx, cy) != ((x + 1) // 16, (y + 1) // 16):
                continue
            for i in range(w):
                cv.bot[y + h, x + i, :3] *= 0.6                                          # schaduw
                for j in range(h):
                    cv.bot[y + j, x + i, :3] = sh[2] if (i + j == 0) else sh[1]
            cv.bot[y + h - 1, x + w - 1, :3] = sh[0]


# ---- mos (Wo-Chien): rottende wortels, schimmel, mos over de wanden
def ruin_moss(cv, rnd):
    moss = lambda c: (c * np.array([0.35, 0.55, 0.25]) + np.array([24, 58, 18]))
    cv.apply(cv.radial(BCX, BCY - 14, 92, 44, 1.0) * 0.9, moss, where=~cv.floor)         # mos over de wanden
    cv.apply(cv.radial(BCX, BCY, 50, 30, 1.15) * 0.75, moss, where=cv.floor)            # mos op de vloer
    cv.apply(cv.radial(BCX, BCY, 26, 14, 1.15) * 0.6, lambda c: c * np.array([0.5, 0.48, 0.4]))   # rotte, donkere kern
    # rottende wortels: dikke kronkels die uit de wanden komen en naar het beest kruipen
    for (x, y) in ((3 * 16 + 4, 30), (5 * 16 + 2, 30), (8 * 16 + 12, 30), (10 * 16 + 4, 30), (32, 4 * 16 + 6), (11 * 16 - 1, 5 * 16)):
        a = math.atan2(BCY - y, BCX - x)
        pts = cv.crack(rnd, x, y, a, math.hypot(BCX - x, BCY - y) * rnd.uniform(0.75, 1.05), seg=(4, 8), wob=0.45, branch=0.3)
        pts = {p: max(w, 0.3) for p, w in pts.items()}
        cv.paint_crack(pts, core=(96, 64, 40), rim=(40, 26, 18), hi=(150, 112, 70), thick=0.25)
    # schimmel: bleke paddenstoelen (Haunted Woods, ontkleurd) en zwamvlekken
    pale = [(48, 30, 24), (110, 70, 44), (170, 120, 70), (214, 184, 120), (240, 232, 200)]
    for (cx, cy) in ((4, 3), (8, 4), (2, 4), (10, 5)):
        cv.stamp(recolor(crop(ROT, 2, 2), pale), cx, cy, block=False)
    for (cx, cy) in ((2, 2), (10, 2)):
        cv.stamp(recolor(crop(ROT, 1, 1), [(40, 26, 18), (84, 58, 36), (120, 92, 56), (100, 120, 60), (150, 170, 90)]), cx, cy)
    for (cx, cy) in ((4, 5), (8, 2)):
        cv.stamp(recolor(crop(ROT, 3 + (cx > 6), 2), [(36, 24, 16), (72, 48, 32), (112, 80, 52), (140, 108, 72)]), cx, cy)
    for _ in range(26):
        x = BCX + rnd.randint(-52, 52); y = BCY + rnd.randint(-14, 44)
        if not (cv.ok(x, y) and cv.floor[y, x]): continue
        for (i, j) in ((0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)):
            if cv.ok(x + i, y + j) and rnd.random() < 0.8:
                cv.bot[y + j, x + i, :3] = (200, 208, 168) if (i, j) == (0, 0) else (150, 168, 112)
    # lianen over de noordwand
    for x in (2 * 16, 4 * 16 + 8, 9 * 16, 10 * 16 + 8):
        v = recolor(VINES[16:48, 0:16] if x % 32 else VINES[16:48, 32:48], [(20, 40, 16), (48, 88, 32), (88, 136, 48), (136, 176, 72)])
        over(cv.bot, v, x, 0)


# ---- ijs (Chien-Pao): bevroren vloer, ijspegels, rijp
def ruin_ice(cv, rnd):
    ice = lambda c: (0.3 * c[:, :1] + 0.59 * c[:, 1:2] + 0.11 * c[:, 2:]) * 0.55 + np.array([96, 144, 176])
    cv.apply(cv.radial(BCX, BCY, 44, 10, 1.15), ice, where=cv.floor)                    # bevroren vloer
    cv.apply(cv.radial(BCX, BCY - 12, 78, 34, 1.0) * 0.7, lambda c: c * 0.6 + np.array([92, 108, 124]), where=~cv.floor)  # rijp op de wanden
    cv.apply(cv.radial(BCX, BCY, 70, 26, 1.15) * 0.45, lambda c: c * 0.7 + np.array([64, 76, 88]), where=cv.floor)
    on = (cv.radial(BCX, BCY, 72, 30, 1.1) * 0.3 > cv.dith) & ((cv.xx * 7 + cv.yy * 13) % 9 == 0)
    cv.bot[on, :3] = (240, 248, 248)                                                     # witte rijpkorrels
    # glansstrepen over het ijs
    glaze = cv.radial(BCX, BCY, 34, 1, 1.15)
    for _ in range(14):
        x = BCX + rnd.randint(-36, 36); y = BCY + rnd.randint(-10, 34)
        for k in range(rnd.randint(3, 6)):
            if cv.ok(x + k, y - k) and cv.floor[y - k, x + k] and glaze[y - k, x + k] > 0:
                cv.bot[y - k, x + k, :3] = (232, 248, 248)
    # scheuren in het ijs
    for i in range(5):
        a = rnd.uniform(0, 2 * math.pi)
        cv.paint_crack(cv.crack(rnd, BCX, BCY + 4, a, rnd.uniform(18, 34), branch=0.25), core=(72, 120, 160),
                       rim=(168, 208, 224), thick=1.0)
    # ijspegels aan de noordwand (rij 1) en de zijwanden bij het beest
    def icicle(x, y, n, w0):
        for j in range(n):
            w = max(1, int(round(w0 * (1 - j / n) ** 0.8)))
            o = (w0 - w) // 2
            for i in range(-1, w + 1):
                if not cv.ok(x + o + i, y + j): continue
                cv.bot[y + j, x + o + i, :3] = ((40, 72, 104) if i in (-1, w) else
                                                (248, 252, 252) if i == 0 else ((176, 220, 240) if i < w - 1 else (112, 168, 208)))
        cv.bot[y + n, x + (w0 - 1) // 2, :3] = (40, 72, 104)
    x = 2 * 16 + 2
    while x < 11 * 16 - 6:
        near = abs(x - BCX) < 52
        w0 = rnd.choice((3, 4, 5)) if near else rnd.choice((2, 3))
        icicle(x, 17, rnd.randint(9, 14) if near else rnd.randint(5, 8), w0)
        x += w0 + rnd.randint(2, 5)
    # ijskristallen op de grond (blokkeren)
    def crystal(cx, cy):
        img = np.zeros((16, 16, 4))
        for (bx, h, w) in ((3, 9, 3), (8, 13, 4), (12, 7, 3)):
            for j in range(h):
                ww = max(1, int(w * (j + 1) / h + 0.5))
                for i in range(-ww, ww + 1):
                    x, y = bx + i, 15 - h + j
                    if 0 <= x < 16:
                        col = (40, 64, 96) if abs(i) == ww or j == 0 else ((248, 252, 252) if i == -ww + 1 else
                                                                         ((160, 208, 232) if i <= 0 else (104, 160, 200)))
                        img[y, x] = (*col, 255)
        cv.bot[cy * 16 + 14:cy * 16 + 16, cx * 16 + 1:cx * 16 + 15, :3] *= 0.75
        cv.stamp(img, cx, cy)
    for c in ((2, 2), (10, 2), (4, 4), (8, 4), (10, 5)):
        crystal(*c)


m = shrine(531)
MAPS['JaggedPass_RuinChamber'] = ('fire', m, ruin_fire)
m = caldera(532); m.decor(12, [(4, 1), (5, 1), (6, 1), (7, 1)], {(9, y) for y in range(2, 18)} | {(8, 4), (10, 4), (9, 5)}, opaque=True)
MAPS['JaggedPass_RuinCaldera'] = ('fire', m, None)   # sinds v0.9.173 onbereikbaar (alleen een uitgang terug, voor oude saves)
MAPS['DesertUnderpass_RuinShrine'] = ('earth', shrine(533), ruin_earth)
MAPS['PetalburgWoods_RuinShrine'] = ('moss', shrine(534), ruin_moss)
MAPS['Route135_RuinShrine'] = ('ice', shrine(535), ruin_ice)

THEMES = {'fire': 'RuinFire', 'earth': 'RuinEarth', 'moss': 'RuinMoss', 'ice': 'RuinIce'}
layouts = {}
PREVIEW = {}
for theme, sym in THEMES.items():
    sheet = np.array(tint(theme)).astype(float)
    mts = []; seen = {}
    border = sheet[6 * 16:7 * 16, 0:16].copy()
    bfloor = sheet[FLOORS[0][1] * 16:FLOORS[0][1] * 16 + 16, FLOORS[0][0] * 16:FLOORS[0][0] * 16 + 16].copy()
    over(bfloor, border, 0, 0); bfloor[..., 3] = 255
    def mt(b, t, beh):
        k = (b.astype(np.uint8).tobytes(), None if t is None else t.astype(np.uint8).tobytes(), beh)
        if k not in seen:
            seen[k] = len(mts)
            mts.append((k, Image.fromarray(b.astype(np.uint8), 'RGBA'),
                        None if t is None else Image.fromarray(t.astype(np.uint8), 'RGBA'), beh))
        return k
    bkey = mt(bfloor, None, 0)
    grids = {}
    for name, (th, m, fx) in MAPS.items():
        if th != theme: continue
        cv = Canvas(m, sheet)
        if fx: fx(cv, random.Random(zlib.crc32(name.encode())))
        PREVIEW[name] = cv
        grids[name] = [[(mt(b, t, beh), bl) for (b, t, beh, bl) in row] for row in cv.cells()]
    res = emit(mts, 'data/tilesets/secondary/ruin_' + theme, 512, 6, 7)
    ids = res['names']
    for name, g in grids.items():
        m = MAPS[name][1]
        os.makedirs('data/layouts/' + name, exist_ok=True)
        data = b''.join(struct.pack('<H', ids[k] | ((1 if bl else 0) << 10) | (3 << 12)) for row in g for k, bl in row)
        open('data/layouts/%s/map.bin' % name, 'wb').write(data)
        open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *([ids[bkey] | (1 << 10) | (3 << 12)] * 4)))
        layouts[name] = (m.W, m.H, sym)
if os.environ.get('RUIN_PREVIEW'):
    for name, cv in PREVIEW.items():
        im = Image.fromarray(np.clip(cv.bot, 0, 255).astype(np.uint8), 'RGBA'); im.alpha_composite(Image.fromarray(np.clip(cv.top, 0, 255).astype(np.uint8), 'RGBA'))
        im.save(os.path.join(os.environ['RUIN_PREVIEW'], name + '.png'))

# ---------------------------------------------------------------- bereikbaarheid
for name, (th, m, _) in MAPS.items():
    starts = [p for p, b in m.beh.items()]
    r = m.reach(starts[0])
    assert all(p in r for p in starts), name + ': uitgangen niet verbonden'
    if 'Caldera' in name: continue
    assert (6, 4) in r and (4, 7) in r, name + ': beest of inscriptie niet bereikbaar'
    los = [p for p in m.floor if p not in m.block and p not in r]
    assert not los, name + ': losse vakjes %s' % los
print('bereikbaarheid ok')

# ---------------------------------------------------------------- tileset-registratie
gh = open('src/data/tilesets/graphics.h').read()
mh = open('src/data/tilesets/metatiles.h').read()
hh = open('src/data/tilesets/headers.h').read()
for theme, sym in THEMES.items():
    d = 'data/tilesets/secondary/ruin_' + theme
    if 'gTilesetTiles_%s[]' % sym not in gh:
        gh += ('\n// Project Grounded: Beasts of Ruin (%s; Volcano Set van Ekat99, ruin_beasts.py)\n'
               'const u32 gTilesetTiles_%s[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n\n'
               'const u16 gTilesetPalettes_%s[][16] =\n{\n' % (theme, sym, d, sym)
               + ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (d, i) for i in range(16)) + '};\n')
    if 'gMetatiles_%s[]' % sym not in mh:
        mh += ('\nconst u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin"); // Project Grounded: Beasts of Ruin\n'
               'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % (sym, d, sym, d))
    if 'gTileset_%s =' % sym not in hh:
        hh += ('\nconst struct Tileset gTileset_%s = // Project Grounded: Beasts of Ruin (%s)\n{\n'
               '    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_%s,\n'
               '    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n'
               '    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = NULL,\n};\n' % (sym, theme, sym, sym, sym, sym))
open('src/data/tilesets/graphics.h', 'w').write(gh)
open('src/data/tilesets/metatiles.h', 'w').write(mh)
open('src/data/tilesets/headers.h', 'w').write(hh)


def const(name):
    import re
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper()


lj = open('data/layouts/layouts.json').read()
anchor = lj.index('"id": "LAYOUT_REGIGIGAS_TEMPLE_SEALED"'); j = lj.index('},', anchor) + 2
add = ''
for name, (W, H, sym) in layouts.items():
    if '"LAYOUT_%s"' % const(name) in lj: continue
    add += ('\n    {\n      "id": "LAYOUT_%s",\n      "name": "%s_Layout",\n      "width": %d,\n      "height": %d,\n'
            '      "primary_tileset": "gTileset_SnowTownBase",\n      "secondary_tileset": "gTileset_%s",\n'
            '      "border_filepath": "data/layouts/%s/border.bin",\n      "blockdata_filepath": "data/layouts/%s/map.bin"\n    },'
            % (const(name), name, W, H, sym, name, name))
if add:
    open('data/layouts/layouts.json', 'w').write(lj[:j] + add + lj[j:])

# ---------------------------------------------------------------- buitenkaarten: openingen + warps
def lay(name):
    L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('name') == name + '_Layout'][0]
    W = L['width']; p = L['blockdata_filepath']
    v = list(struct.unpack('<%dH' % (W * L['height']), open(p, 'rb').read()))
    return W, p, v

# (buitenkaart, layout, [(x, y, bron-x, bron-y)], warp (x, y), schrijn)
OUTDOOR = [
    ('JaggedPass', [(11, 5, 16, 5), (11, 6, 16, 6)], (11, 6), 'JaggedPass_RuinChamber'),
    ('DesertUnderpass', [(61, 13, 10, 12), (60, 14, 9, 13), (61, 14, 10, 13), (62, 14, 11, 13)], (61, 13), 'DesertUnderpass_RuinShrine'),
    ('PetalburgWoods', [(42, 35, 46, 9), (43, 35, 47, 9), (42, 36, 46, 10), (43, 36, 47, 10)], (43, 36), 'PetalburgWoods_RuinShrine'),
    ('Route135', [(50 + dx, 20 + dy, 5 + dx, 10 + dy) for dy in (0, 1) for dx in range(3)], (51, 21), 'Route135_RuinShrine'),
]
back = {}
for mapname, tiles, (wx, wy), dst in OUTDOOR:
    mj = json.load(open('data/maps/%s/map.json' % mapname))
    W, p, v = lay(mapname)
    for x, y, sx, sy in tiles:
        v[y * W + x] = v[sy * W + sx]
    open(p, 'wb').write(struct.pack('<%dH' % len(v), *v))
    if not any(w['dest_map'] == 'MAP_' + const(dst) for w in mj['warp_events']):
        mj['warp_events'].append({'x': wx, 'y': wy, 'elevation': 0, 'dest_map': 'MAP_' + const(dst), 'dest_warp_id': '0'})
        open('data/maps/%s/map.json' % mapname, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')
    back[dst] = ('MAP_' + const(mapname), [i for i, w in enumerate(mj['warp_events']) if w['dest_map'] == 'MAP_' + const(dst)][0])

# ---------------------------------------------------------------- kaarten
BEASTS = {  # kaart: (soort, gfx, vlag-suffix, beest-x, beest-y, mapsec)
    'JaggedPass_RuinChamber': ('CHI_YU', 'CHI_YU', 6, 3, 'MAPSEC_JAGGED_PASS'),
    'DesertUnderpass_RuinShrine': ('TING_LU', 'TING_LU', 6, 3, 'MAPSEC_DESERT_UNDERPASS'),
    'PetalburgWoods_RuinShrine': ('WO_CHIEN', 'WO_CHIEN', 6, 3, 'MAPSEC_PETALBURG_WOODS'),
    'Route135_RuinShrine': ('CHIEN_PAO', 'CHIEN_PAO', 6, 3, 'MAPSEC_ROUTE_135'),
}
base = json.load(open('data/maps/RegigigasTemple/map.json'))
for name, (th, m, _) in MAPS.items():
    mj = {k: base[k] for k in base}
    mj.update({'id': 'MAP_' + const(name), 'name': name, 'layout': 'LAYOUT_' + const(name), 'music': 'MUS_SEALED_CHAMBER',
               'map_type': 'MAP_TYPE_UNDERGROUND', 'show_map_name': False,
               'region_map_section': BEASTS[name][4] if name in BEASTS else 'MAPSEC_JAGGED_PASS'})
    mj['object_events'] = []; mj['coord_events'] = []; mj['bg_events'] = []
    if name in BEASTS:
        sp, gfx, bx, by, _ = BEASTS[name]
        mj['object_events'].append({'local_id': 'LOCALID_RUIN_' + sp, 'graphics_id': 'OBJ_EVENT_GFX_SPECIES(%s)' % gfx,
                                    'x': bx, 'y': by, 'elevation': 3, 'movement_type': 'MOVEMENT_TYPE_FACE_DOWN',
                                    'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE',
                                    'trainer_sight_or_berry_tree_id': '0', 'script': 'RuinBeasts_EventScript_' + sp,
                                    'flag': 'FLAG_HIDE_RUIN_' + sp})
    # inscriptie op de linkeronderstaak (onderste tegel), te lezen van rechts (4,7)
    sx, sy = (7, 7) if 'Caldera' in name else (3, 7)
    mj['bg_events'].append({'type': 'sign', 'x': sx, 'y': sy, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
                            'script': name + '_EventScript_Stake'})
    if name == 'JaggedPass_RuinChamber':  # tweede inscriptie (de oude tekst van het lavaveld) op de rechteronderstaak
        mj['bg_events'].append({'type': 'sign', 'x': 9, 'y': 7, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
                                'script': 'JaggedPass_RuinCaldera_EventScript_Stake'})
    ex = [p for p, b in m.beh.items() if b == SOUTH][0]
    if name == 'JaggedPass_RuinCaldera':
        # onbereikbaar sinds v0.9.173; alleen een uitgang terug voor een save die hier nog staat
        warps = [{'x': ex[0], 'y': ex[1], 'elevation': 0, 'dest_map': 'MAP_JAGGED_PASS_RUIN_CHAMBER', 'dest_warp_id': '0'}]
    else:
        dm, di = back[name]
        warps = [{'x': ex[0], 'y': ex[1], 'elevation': 0, 'dest_map': dm, 'dest_warp_id': str(di)}]
    mj['warp_events'] = warps
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')

g = open('data/maps/map_groups.json').read()
for name in MAPS:
    if '"%s"' % name not in g:
        i = g.index('"gMapGroup_Grounded": ['); j = g.index('\n  ]', i)
        g = g[:j] + ',\n    "%s"' % name + g[j:]
open('data/maps/map_groups.json', 'w').write(g)
es = open('data/event_scripts.s').read()
for name in MAPS:
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        es = es.replace('\t.include "data/maps/Route126_SilentCrater/scripts.inc"\n',
                        '\t.include "data/maps/Route126_SilentCrater/scripts.inc"\n' + inc, 1)
open('data/event_scripts.s', 'w').write(es)
print('klaar')
