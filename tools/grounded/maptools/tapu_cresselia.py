"""Project Grounded: het Tapu-eiland en Fullmoon Island (Cresselia). Deterministisch en idempotent.

  TapuIsle        Tropisch eiland in de Midden-zee (Town Map x 15-16, y 8-9), ten noorden van Route 132
                  (verbinding, x 14-65 van Route 132). General + fortree_jungle (jungle-groene bomen, reuzenpalmen,
                  tropische bloemen en de stenen ruinestukken van Zarude). Zandstrand rondom, in het midden een
                  verhoogd heiligdom (terras met klifwanden, stenen trap in de zuidwand) met de kahuna op een altaar
                  en vier stenen Tapu-beelden (objecten, statue_sprites.py), en vier ruines in de vier hoeken:
                    noordoost  Tapu Koko  (bliksemruine: gebroken/omgevallen zuilen, losse blokken)
                    zuidoost   Tapu Lele  (bloemenruine: bloemenveld, hibiscus, heliconia)
                    noordwest  Tapu Bulu  (woudruine: dichte jungle, stammen, monstera, bananen)
                    zuidwest   Tapu Fini  (waterruine: een lagune met waterlelies, het altaar op een eilandje)
                  Elke Tapu staat op het voorste vak van zijn altaar (3x2). Voor de Hall of Fame houdt de mist je
                  tegen (coord-triggers op rij FOG_Y). De onderste rijen bevatten alleen primary-tiles (water,
                  zand, zeerotsen): Route 132 heeft een andere secondary tileset; het script controleert dat.
  FullmoonIsland  Klein halvemaanvormig eiland in de West-zee (Town Map x 1-2, y 11-12), ten oosten van Route 105
                  (verbinding, y 30-63 van Route 105; dezelfde tileset General + Dewford). Een rond maanmeertje in
                  de bocht van de maan; 's nachts (post-game) staat Cresselia aan de oever. Een slapeloze zeeman.

De jungle-varianten van de General-bomen worden in fortree_jungle op inhoud teruggezocht (zelfde pixels, zelfde
attributen); de decor-metatiles (0x345-0x369) staan vast en het script controleert het aantal metatiles van
fortree_jungle (draait iemand fortree_jungle.py met een andere uitkomst, dan faalt dit script en moeten de nummers
opnieuw bekeken worden).

Gebruik: python3 tools/grounded/maptools/tapu_cresselia.py [rendermap]"""
import json, math, os, random, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chimney_ext as cx            # zet ook de werkmap op de repo-root
import ogerpon_quest as oq
import sea_market_steam as sms

t, mt, WATER, reach = sms.t, sms.mt, sms.WATER, cx.reach


def val(m, coll, elev):
    return m | (coll << 10) | (elev << 12)


# ====================================================================== tilesets
def _load(kind, name):
    d = 'data/tilesets/%s/%s' % (kind, name)
    return open(d + '/metatiles.bin', 'rb').read(), open(d + '/metatile_attributes.bin', 'rb').read(), \
        open(d + '/tiles.4bpp', 'rb').read()


GM, GA, GT = _load('primary', 'general')
JM, JA, JT = _load('secondary', 'fortree_jungle')
assert len(JM) // 16 == 362, 'fortree_jungle is veranderd: controleer de decor-nummers in tapu_cresselia.py'


def _pix(tiles, i):
    b = tiles[i * 32:(i + 1) * 32]
    if len(b) < 32:
        return ((0,) * 8,) * 8
    return tuple(tuple((b[y * 4 + x // 2] >> (4 * (x & 1))) & 15 for x in range(8)) for y in range(8))


def _shape(m):
    """Pixel-indexbeeld (zonder palet) en attribuut van metatile m in General + fortree_jungle."""
    src, attrs, i = (GM, GA, m) if m < 512 else (JM, JA, m - 512)
    ent = struct.unpack_from('<8H', src, i * 16)
    img = []
    for e in ent:
        ti, hf, vf = e & 0x3ff, (e >> 10) & 1, (e >> 11) & 1
        p = _pix(GT, ti) if ti < 512 else _pix(JT, ti - 512)
        if vf:
            p = p[::-1]
        if hf:
            p = tuple(r[::-1] for r in p)
        img.append(p)
    return tuple(img), struct.unpack_from('<H', attrs, i * 2)[0]


def jungle_variant(m):
    """De jungle-groene kopie van General-boommetatile m in fortree_jungle (zelfde pixels/attribuut)."""
    want = _shape(m)
    for j in range(0x318, 0x200 + len(JM) // 16):
        if _shape(j) == want:
            return j
    raise SystemExit('geen jungle-variant van %#x' % m)


GRASS, LONG, LONG_S, BANK, FLOWER = 0x001, 0x015, 0x208, 0x002, 0x004
FOREST, TRUNK, CANOPY = (0x0C6, 0x0C7), (0x016, 0x017), (0x00E, 0x00F)
PALM = [[0x248, 0x249, 0x24A], [0x250, 0x251, 0x252], [0x0C7, 0x241, 0x0C7], [0x0C7, 0x273, 0x0C6]]
# fortree_jungle-decor (zie jungle_tileset.py / zarude_ruins.py); botsing zoals in FortreeJungle
LILY, LOTUS = 0x345, 0x346
LOG = (0x347, 0x348)
ARCH = (0x349, 0x34A)
HELICONIA = (0x34B, 0x34C)          # boven (over de speler), onder (blokkeert)
BANANA = (0x34D, 0x34E)
HIBISCUS, HIBISCUS_RED, MONSTERA = 0x34F, 0x351, 0x350
LITTER = (0x352, 0x353, 0x356)
FERN = (0x354, 0x357)
JFLOWER = (0x355, 0x358)            # paarse en rode bodembloempjes
DAIS = [(0x35A, 0x35B, 0x35C), (0x35D, 0x35E, 0x35F)]
PILLAR, PILLAR_BROKEN = (0x360, 0x361), (0x362, 0x363)
FALLEN = (0x364, 0x365)
BLOCK = (0x366, 0x367)
PAVING = (0x368, 0x369)
POND = dict(TL=0xB0, T=0xB1, TR=0xB2, L=0xB8, R=0xBA, IUL=0xC0, IUR=0xC2, C=0xA1)
OPEN_MT = {GRASS, FLOWER, LONG, LONG_S, 0x355, 0x358, 0x368, 0x369}
ROCKS = ((0x150, 0x151, 0x158, 0x159), (0x175, 0x176, 0x17d, 0x17e))


# ====================================================================== zand-autotiler (General, zoals Route 105)
def sand_tile(land, x, y):
    H, W = len(land), len(land[0])
    def w(dx, dy):
        xx, yy = x + dx, y + dy
        return not (0 <= xx < W and 0 <= yy < H and land[yy][xx])
    n, s, e, wst = w(0, -1), w(0, 1), w(1, 0), w(-1, 0)
    assert not (n and s) and not (e and wst), ('zandstrook van 1 breed', x, y)
    if n:
        m = 0x11b if wst else 0x11d if e else 0x11c
    elif s:
        m = 0x12b if wst else 0x12d if e else 0x12c
    elif wst:
        m = 0x123
    elif e:
        m = 0x125
    elif w(-1, -1):
        m = 0x13d
    elif w(1, -1):
        m = 0x13e
    elif w(-1, 1):
        m = 0x145
    elif w(1, 1):
        m = 0x146
    else:
        m = 0x124
    return t(m)


def smooth(land, passes=3):
    """Haalt uitsteeksels/gaten van 1 breed weg (de zand-autotiler kent geen stroken van 1 vak)."""
    H, W = len(land), len(land[0])
    for _ in range(passes):
        changed = False
        for y in range(H):
            for x in range(W):
                if not land[y][x]:
                    continue
                def L(dx, dy):
                    xx, yy = x + dx, y + dy
                    return 0 <= xx < W and 0 <= yy < H and land[yy][xx]
                if (not L(0, -1) and not L(0, 1)) or (not L(-1, 0) and not L(1, 0)):
                    land[y][x] = False
                    changed = True
        if not changed:
            break


def dist_to_water(land):
    H, W = len(land), len(land[0])
    INF = 99
    d = [[0 if not land[y][x] else INF for x in range(W)] for y in range(H)]
    q = [(x, y) for y in range(H) for x in range(W) if not land[y][x]]
    while q:
        nq = []
        for x, y in q:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < W and 0 <= yy < H and d[yy][xx] > d[y][x] + 1:
                        d[yy][xx] = d[y][x] + 1
                        nq.append((xx, yy))
        q = nq
    return d


# ====================================================================== karakterkaart-hulpjes
class Chars:
    def __init__(self, W, H, fill):
        self.W, self.H = W, H
        self.c = [[fill] * W for _ in range(H)]

    def inb(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H

    def get(self, x, y, default='T'):
        return self.c[y][x] if self.inb(x, y) else default

    def disc(self, cx, cy, r, k, only=None):
        for y in range(int(cy - r - 2), int(cy + r + 3)):
            for x in range(int(cx - r - 2), int(cx + r + 3)):
                if self.inb(x, y) and (x - cx) ** 2 + ((y - cy) * 1.15) ** 2 <= r * r:
                    if only is None or self.c[y][x] in only:
                        self.c[y][x] = k

    def rect(self, x0, y0, x1, y1, k, only=None):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if only is None or self.c[y][x] in only:
                    self.c[y][x] = k

    def path(self, pts, w, k, only=None):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0)) * 3 + 1
            for i in range(n + 1):
                f = i / n
                x, y = x0 + (x1 - x0) * f, y0 + (y1 - y0) * f
                for dy in range(w):
                    for dx in range(w):
                        xx, yy = int(round(x - (w - 1) / 2 + dx)), int(round(y - (w - 1) / 2 + dy))
                        if self.inb(xx, yy) and (only is None or self.c[yy][xx] in only):
                            self.c[yy][xx] = k


def pond_tile(C, x, y):
    def notw(dx, dy):
        return C.get(x + dx, y + dy) != 'w'
    up, lf, rt = notw(0, -1), notw(-1, 0), notw(1, 0)
    if up:
        m = POND['TL'] if lf else POND['TR'] if rt else POND['T']
    elif lf:
        m = POND['L']
    elif rt:
        m = POND['R']
    elif notw(-1, -1):
        m = POND['IUL']
    elif notw(1, -1):
        m = POND['IUR']
    else:
        m = POND['C']
    return val(m, 0, 1)


def place_rocks(g, n, seed, ok):
    rnd = random.Random(seed)
    H, W = len(g), len(g[0])
    placed = tries = 0
    while placed < n and tries < 5000:
        tries += 1
        x, y = rnd.randint(0, W - 2), rnd.randint(0, H - 2)
        if not ok(x, y):
            continue
        if any(mt(g[yy][xx]) != WATER for yy in range(y - 1, y + 3) for xx in range(x - 1, x + 3)
               if 0 <= yy < H and 0 <= xx < W):
            continue
        r = rnd.choice(ROCKS)
        for k, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
            g[y + dy][x + dx] = t(r[k], True, 1)
        placed += 1


def trainer(gfx, x, y, script, face, sight):
    o = cx.obj(gfx, x, y, script, ttype='TRAINER_TYPE_NORMAL', sight=str(sight), move='MOVEMENT_TYPE_FACE_' + face)
    return o


def obj(gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', local_id=None, elev=3, rx=0, ry=0):
    return sms.obj(gfx, x, y, script, flag, move=move, local_id=local_id, elev=elev, rx=rx, ry=ry)


def sign(x, y, script):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
            'script': script}


def hidden(x, y, it, flag):
    return cx.hidden(x, y, it, flag)


# ====================================================================== Tapu-eiland
TW, TH = 56, 50
TAPU_OFFSET = 0                     # x van het eiland op Route 132 (x 0-55)
REEF_GAP = (27, 2)                  # zeerots (2x2) in het rif bovenaan Route 132 die weg moet: vaargeul x 27-28
FOG_Y = 45                          # mist voor de Hall of Fame (hele rij coord-triggers)
SAFE_ROWS = 10                      # onderste rijen alleen primary (grens met Route 132)
CX, CY = 28, 22                     # midden van het eiland (plein)
SHRINE = (22, 14, 35, 25)           # verhoogd heiligdom (x0, y0, x1, y1 incl. wanden; zuidwand = 2 rijen)
STAIRS_X = 28                       # stenen trap (2 breed) midden in de zuidwand
# stenen Tapu-beelden (objecten, tools/grounded/statue_sprites.py), elk in de hoek van zijn eigen ruine
STATUES = {'BULU': (25, 17), 'KOKO': (32, 17), 'FINI': (25, 21), 'LELE': (32, 21)}
ALTAR = (27, 16)                    # stenen altaar (3x2) achter op het terras; de kahuna staat ervoor op de vloer
# altaren (linksboven van 3x2); de Tapu staat op het middelste voorvak, de speler eronder
DAIS_AT = {'KOKO': (40, 8), 'LELE': (40, 28), 'BULU': (14, 8), 'FINI': (14, 28)}
CLEARING = {'KOKO': (41, 12, 4.8), 'LELE': (41, 32, 5.0), 'BULU': (15, 12, 4.4)}
LAGOON = (15, 31, 5.8, 4.5)         # midden, halve breedte, halve hoogte


STAIRS = (0x0AF, 0x0CF)              # stenen Hoenn-trap (General 175 links / 207 rechts)
WALL = dict(W=0x070, E=0x072, FACE=0x07C, FACE_W=0x070, FACE_E=0x072, FOOT=0x079, FOOT_W=0x078, FOOT_E=0x07A)


def shrine_wall(x, y):
    """Klifwand van het terras (General, zoals Route 119/121): zijwanden links/rechts, zuidwand van 2 rijen
    (bovenrij FACE, onderrij FOOT met schaduw), hoeken waar ze samenkomen. Rechte rechthoek, geen schuine hoeken."""
    sx0, sy0, sx1, sy1 = SHRINE
    side = 'W' if x == sx0 else 'E' if x == sx1 else ''
    if y == sy1:
        return WALL['FOOT_' + side] if side else WALL['FOOT']
    if y == sy1 - 1:
        return WALL['FACE_' + side] if side else WALL['FACE']
    assert side, ('wand midden op het terras', x, y)
    return WALL[side]


def tapu_pos(k):
    x, y = DAIS_AT[k]
    return x + 1, y + 1


def open_reef():
    """Route 132 (vloed en eb) is aan de noordkant afgesloten door een rif van zeerotsen (rij 0-3). Eén rots van 2x2
    gaat weg, zodat er een vaargeul van 2 breed naar het Tapu-eiland loopt (recht onder het strand)."""
    x0, y0 = REEF_GAP
    for lay in ('Route132', 'Route132_LowTide'):
        g = sms.read(lay, 80, 40)
        water = g[y0 - 1][x0]
        assert mt(water) == WATER and cx.walkable(water)
        rock = [mt(g[y0 + dy][x0 + dx]) for dy in (0, 1) for dx in (0, 1)]
        if rock == [WATER] * 4:
            continue                                        # al open
        assert rock == [0x150, 0x151, 0x158, 0x159], (lay, [hex(m) for m in rock])
        for dy in (0, 1):
            for dx in (0, 1):
                g[y0 + dy][x0 + dx] = water
        sms.save(g, lay)
        for y in range(0, 6):                               # geul open van rij 0 tot het open water
            for x in (x0, x0 + 1):
                assert cx.walkable(g[y][x]) and mt(g[y][x]) == WATER, (lay, x, y)


def tapu_isle():
    name, const = 'TapuIsle', 'TAPU_ISLE'
    rng = random.Random(785)                        # nationaal dexnummer van Tapu Koko
    jv = {m: jungle_variant(m) for m in FOREST + TRUNK + CANOPY}
    jpalm = [[jungle_variant(m) if m in FOREST else m for m in row] for row in PALM]

    # ---- eilandvorm: golvende superellips (volle hoeken voor de vier ruines)
    land = [[False] * TW for _ in range(TH)]
    ph = [rng.random() * 6.28 for _ in range(3)]
    for y in range(TH):
        for x in range(TW):
            a = math.atan2(y - CY, x - CX)
            r = 1 + 0.035 * math.sin(3 * a + ph[0]) + 0.03 * math.sin(5 * a + ph[1]) + 0.02 * math.sin(7 * a + ph[2])
            if abs((x - CX) / 25.0) ** 3.2 + abs((y - CY) / 19.5) ** 3.2 <= r ** 3.2:
                land[y][x] = True
    smooth(land)
    d = dist_to_water(land)

    # ---- karakters: ~ zee, S zand, g gras, T bos, L lang gras, w lagune, p plaveisel, f bloemen
    C = Chars(TW, TH, '~')
    for y in range(TH):
        for x in range(TW):
            if land[y][x]:
                C.c[y][x] = 'S' if d[y][x] <= 3 else 'g' if d[y][x] == 4 else 'T'
    J = set('TgLpf')
    sx0, sy0, sx1, sy1 = SHRINE
    C.rect(sx0 - 2, sy0 + 1, sx1 + 2, sy1 + 3, 'g', only=J)             # hof rond het heiligdom
    C.path([(CX, sy1 + 2), (CX, 38)], 3, 'g', only=J)                   # zuid: strand -> hof
    for k, (x, y, r) in CLEARING.items():
        C.disc(x, y, r, 'g', only=J)
    C.path([(sx1 + 2, sy0 + 2), (sx1 + 4, sy0), (CX + 12, CY - 9)], 2, 'g', only=J)            # Koko
    C.path([(sx1 + 2, sy1 + 2), (sx1 + 3, sy1 + 5), (CX + 10, CY + 9)], 2, 'g', only=J)        # Lele
    C.path([(sx0 - 2, sy0 + 2), (sx0 - 4, sy0), (CX - 11, CY - 10)], 2, 'g', only=J)           # Bulu
    lx, ly, lw, lh = LAGOON
    C.disc(lx, ly, lw + 1.2, 'g', only=J)                               # oever van de lagune
    C.path([(sx0 - 2, sy1 + 2), (sx0 - 3, sy1 + 4)], 2, 'g', only=J)                           # Fini
    for y in range(TH):
        for x in range(TW):
            if ((x - lx) / lw) ** 2 + ((y - ly) / lh) ** 2 <= 1 and C.c[y][x] == 'g':
                C.c[y][x] = 'w'
    fx, fy = DAIS_AT['FINI']
    C.rect(fx, fy, fx + 2, fy + 2, 'g')                                 # eilandje met het altaar
    for k, (x, y) in DAIS_AT.items():                                   # ruimte rond de altaren
        if k != 'FINI':
            C.rect(x - 1, y, x + 3, y + 2, 'g', only=J)
    # het heiligdom: verhoogd terras (W = klifwand, H = trap) met een stenen vloer, ervoor een geplaveid voorplein
    C.rect(sx0, sy0, sx1, sy1, 'W')
    C.rect(sx0 + 1, sy0, sx1 - 1, sy1 - 2, 'p')
    for x in range(sx0 + 1, sx1):                                      # mos/gras langs de randen van het terras
        C.c[sy0][x] = 'g'
    for y in range(sy0, sy1 - 1):
        C.c[y][sx0 + 1] = C.c[y][sx1 - 1] = 'g'
    for y in (sy1 - 1, sy1):
        C.c[y][STAIRS_X] = C.c[y][STAIRS_X + 1] = 'H'
    C.rect(STAIRS_X - 1, sy1 + 1, STAIRS_X + 2, sy1 + 3, 'p')
    for k, (x, y) in DAIS_AT.items():
        if k != 'FINI':
            C.rect(x, y + 2, x + 2, y + 2, 'p')
    # lang gras (plukken langs de paden en aan de randen van de open plekken)
    for cx_, cy_, r in ((CX + 10, CY - 9, 1.6), (CX + 8, CY + 8, 1.6), (CX - 9, CY - 9, 1.6), (CX - 6, CY + 8, 1.6),
                        (CX + 4, CY + 11, 2.2), (CX - 4, CY + 12, 1.8), (44, 15, 1.8), (37, 36, 1.8),
                        (18, 9, 1.4), (11, 14, 1.4)):
        C.disc(cx_, cy_, r, 'L', only='g')
    # bloemenveld van Lele
    lx2, ly2, lr2 = CLEARING['LELE']
    for y in range(TH):
        for x in range(TW):
            if C.c[y][x] == 'g' and math.hypot(x - lx2, (y - ly2) * 1.15) <= lr2 - 0.3 and rng.random() < 0.45:
                C.c[y][x] = 'f'
    # losse bosvakjes van 1 breed tussen twee open vakken: openen
    for _ in range(2):
        for y in range(1, TH - 1):
            for x in range(1, TW - 1):
                if C.c[y][x] == 'T' and C.c[y - 1][x] in 'gLpf' and C.c[y + 1][x] in 'gLpf':
                    C.c[y][x] = 'g'
                if C.c[y][x] == 'T' and C.c[y][x - 1] in 'gLpf' and C.c[y][x + 1] in 'gLpf':
                    C.c[y][x] = 'g'

    # open vakjes die alleen schuin aan de rest raken (of helemaal los liggen): bos
    seen, st = {(CX, 40)}, [(CX, 40)]
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if C.inb(*n) and n not in seen and C.c[n[1]][n[0]] not in 'TW':
                seen.add(n); st.append(n)
    for y in range(TH):
        for x in range(TW):
            if C.c[y][x] in 'gLpf' and (x, y) not in seen:
                C.c[y][x] = 'T'
    if os.environ.get('TAPU_DEBUG'):
        print('\n'.join('%2d ' % y + ''.join(r) for y, r in enumerate(C.c)))
    # ---- events
    P = name + '_EventScript_'
    KAHUNA = (ALTAR[0] + 1, ALTAR[1] + 2)  # vóór het altaar op de vloer (op het altaar leek hij te zweven)
    HIDDEN_PEARL = (52, 22)
    TABLET = (STAIRS_X - 1, SHRINE[3] - 3)            # de stenen tafel met de volgorde, links boven aan de trap
    objs = [
        obj('OBJ_EVENT_GFX_OLD_MAN', KAHUNA[0], KAHUNA[1], P + 'Kahuna', local_id='LOCALID_TAPU_ISLE_KAHUNA'),
        obj('OBJ_EVENT_GFX_FAT_MAN', CX + 5, 39, P + 'Tourist', move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_SPECIES(TAPU_KOKO)', *tapu_pos('KOKO'), P + 'TapuKoko', 'FLAG_TEMP_12',
            local_id='LOCALID_TAPU_ISLE_KOKO'),
        obj('OBJ_EVENT_GFX_SPECIES(TAPU_LELE)', *tapu_pos('LELE'), P + 'TapuLele', 'FLAG_TEMP_13',
            local_id='LOCALID_TAPU_ISLE_LELE'),
        obj('OBJ_EVENT_GFX_SPECIES(TAPU_BULU)', *tapu_pos('BULU'), P + 'TapuBulu', 'FLAG_TEMP_14',
            local_id='LOCALID_TAPU_ISLE_BULU'),
        obj('OBJ_EVENT_GFX_SPECIES(TAPU_FINI)', *tapu_pos('FINI'), P + 'TapuFini', 'FLAG_TEMP_15',
            local_id='LOCALID_TAPU_ISLE_FINI'),
        trainer('OBJ_EVENT_GFX_BLACK_BELT', SHRINE[2] + 2, SHRINE[1] + 2, P + 'Kaimana', 'DOWN', 3),
        trainer('OBJ_EVENT_GFX_WOMAN_2', SHRINE[2] - 1, SHRINE[3] + 3, P + 'Leilani', 'LEFT', 3),
        trainer('OBJ_EVENT_GFX_MAN_4', SHRINE[0] - 1, SHRINE[1] + 6, P + 'Makoa', 'UP', 3),
        trainer('OBJ_EVENT_GFX_EXPERT_F', SHRINE[0] + 1, SHRINE[3] + 1, P + 'Nalu', 'RIGHT', 3),
        cx.item(11, 11, 'ITEM_STAR_PIECE', 'FLAG_ITEM_TAPU_ISLE_STAR_PIECE'),
    ]
    for k, (x, y) in STATUES.items():
        objs.append(obj('OBJ_EVENT_GFX_STATUE_TAPU_' + k, x, y, P + 'Statue' + k.capitalize()))
    bgs = [sign(TABLET[0], TABLET[1], P + 'Tablet')]
    for k in DAIS_AT:
        bgs.append(sign(*tapu_pos(k), P + 'Dais' + k.capitalize()))
    bgs.append(hidden(HIDDEN_PEARL[0], HIDDEN_PEARL[1], 'ITEM_BIG_PEARL', 'FLAG_HIDDEN_ITEM_TAPU_ISLE_BIG_PEARL'))
    coords = [sms.coord(x, FOG_Y, P + 'Fog', elev=1) for x in range(TW)]
    for o in objs:
        x, y = o['x'], o['y']
        if 'SPECIES' in o['graphics_id']:
            continue
        assert C.c[y][x] in 'gpLfS', ('event niet op open grond', o['script'], C.c[y][x])
    assert C.c[TABLET[1]][TABLET[0]] in 'gp'

    # ---- karakters -> metatiles
    g = [[0] * TW for _ in range(TH)]
    for y in range(TH):
        for x in range(TW):
            k = C.c[y][x]
            below = C.get(x, y + 1, '~')
            if k == '~':
                g[y][x] = t(WATER, False, 1)
            elif k == 'S':
                g[y][x] = sand_tile(land, x, y)
            elif k == 'T':
                g[y][x] = val(jv[rng.choice(TRUNK if below != 'T' else FOREST)], 1, 0)
            elif k == 'w':
                g[y][x] = pond_tile(C, x, y)
            elif k == 'W':
                g[y][x] = val(shrine_wall(x, y), 1, 3)
            elif k == 'H':
                g[y][x] = val(STAIRS[x - STAIRS_X], 0, 3)
            elif below == 'T':
                g[y][x] = val(jv[rng.choice(CANOPY)], 0, 3)
            elif k == 'L':
                g[y][x] = val(LONG if below == 'L' else LONG_S, 0, 3)
            elif k == 'f':
                g[y][x] = val(rng.choice((FLOWER, FLOWER, JFLOWER[0], JFLOWER[1])), 0, 3)
            elif k == 'p':
                g[y][x] = val(rng.choice(PAVING), 0, 3)
            else:
                g[y][x] = val(BANK if C.get(x, y - 1) == 'w' else GRASS, 0, 3)

    # ---- altaren
    for k, (x0, y0) in DAIS_AT.items():
        for j in range(2):
            for i in range(3):
                assert C.c[y0 + j][x0 + i] in 'gpfL', ('altaar niet op open grond', k)
                g[y0 + j][x0 + i] = val(DAIS[j][i], 1, 3)
        px, py = tapu_pos(k)
        assert C.c[py + 1][px] in 'gpfL', ('voor het altaar moet je kunnen staan', k)

    ax, ay = ALTAR
    for j in range(2):
        for i in range(3):
            assert C.c[ay + j][ax + i] in 'gp', 'altaar van de kahuna niet op het terras'
            g[ay + j][ax + i] = val(DAIS[j][i], 1, 3)
    assert C.c[ay + 2][ax + 1] in 'gp' and C.c[ay + 3][ax + 1] in 'gp', 'voor de kahuna moet je kunnen staan'

    # ---- vaste decor per ruine (overgeslagen als het niet op open grond past; de controle hieronder vangt de rest)
    EVENT = {(o['x'], o['y']) for o in objs} | {(b_['x'], b_['y']) for b_ in bgs}
    EVENT |= {(tapu_pos(k)[0], tapu_pos(k)[1] + 1) for k in DAIS_AT}
    EVENT |= {(KAHUNA[0], KAHUNA[1] + 1)} | {(x + dx, y - dy) for x, y in STATUES.values() for dx in (-1, 0, 1)
                                              for dy in (1, 2)}
    EVENT_OBJ = {(o['x'], o['y']) for o in objs}
    DECOR = []
    def can(cells):
        return all(C.inb(x, y) and C.c[y][x] in 'gpfL' and (x, y) not in EVENT and (x, y) not in DECOR
                   and mt(g[y][x]) in OPEN_MT for x, y in cells)
    def put(cells_mts, why):
        cells = [c for c, _ in cells_mts]
        if not can(cells):
            print('  decor overgeslagen:', why, cells)
            return
        old = [g[y][x] for (x, y), _ in cells_mts]
        before = len(reach(g, [(CX, 40)], blocked=EVENT_OBJ))
        for (x, y), v in cells_mts:
            g[y][x] = v
        lost = sum(1 for (x, y), v in cells_mts if not cx.walkable(v))
        if len(reach(g, [(CX, 40)], blocked=EVENT_OBJ)) != before - lost:
            for ((x, y), _), v in zip(cells_mts, old):
                g[y][x] = v
            print('  decor overgeslagen (sluit iets af):', why, cells)
            return
        DECOR.extend(cells)
    def col(x, y, pair, why):                       # 1x2: boven over de speler, onder blokkeert
        put([((x, y), val(pair[0], 0, 3)), ((x, y + 1), val(pair[1], 1, 3))], why)
    def row2(x, y, pair, why):
        put([((x, y), val(pair[0], 1, 3)), ((x + 1, y), val(pair[1], 1, 3))], why)
    def one(x, y, m, why):
        put([((x, y), val(m, 1, 3))], why)
    def rel(k, dx, dy):
        return DAIS_AT[k][0] + dx, DAIS_AT[k][1] + dy
    # Koko: gespleten en omgevallen zuilen, losse blokken (de bliksem slaat hier vaker in)
    col(*rel('KOKO', -2, 0), PILLAR, 'koko'); col(*rel('KOKO', 4, 0), PILLAR_BROKEN, 'koko')
    col(*rel('KOKO', -3, 3), PILLAR_BROKEN, 'koko'); col(*rel('KOKO', 5, 3), PILLAR_BROKEN, 'koko')
    row2(*rel('KOKO', 3, 6), FALLEN, 'koko')
    one(*rel('KOKO', -2, 6), BLOCK[0], 'koko'); one(*rel('KOKO', 4, 3), BLOCK[1], 'koko')
    # Lele: zuilen naast het altaar, hibiscus en heliconia tussen de bloemen
    col(*rel('LELE', -2, 0), PILLAR, 'lele'); col(*rel('LELE', 4, 0), PILLAR, 'lele')
    one(*rel('LELE', -3, 4), HIBISCUS, 'lele'); one(*rel('LELE', 5, 5), HIBISCUS_RED, 'lele')
    one(*rel('LELE', 3, 7), HIBISCUS, 'lele'); one(*rel('LELE', -1, 7), HIBISCUS_RED, 'lele')
    col(*rel('LELE', 5, 2), HELICONIA, 'lele'); col(*rel('LELE', -2, 5), HELICONIA, 'lele')
    # Bulu: overwoekerde zuilen, stammen, wortelboog, monstera en bananen
    col(*rel('BULU', -2, 0), PILLAR_BROKEN, 'bulu'); col(*rel('BULU', 4, 0), PILLAR_BROKEN, 'bulu')
    row2(*rel('BULU', -3, 4), LOG, 'bulu'); row2(*rel('BULU', 3, 5), ARCH, 'bulu')
    one(*rel('BULU', 5, 3), MONSTERA, 'bulu'); one(*rel('BULU', -3, 6), MONSTERA, 'bulu')
    col(*rel('BULU', -1, 5), BANANA, 'bulu'); col(*rel('BULU', 4, 2), BANANA, 'bulu')
    # Fini: waterlelies en lotus in de lagune
    for x, y, m in ((-4, 2, LILY), (3, 5, LOTUS), (-3, 6, LILY), (4, 1, LOTUS), (0, 6, LOTUS), (-5, 4, LILY)):
        x, y = rel('FINI', x, y)
        if C.c[y][x] == 'w' and mt(g[y][x]) == POND['C']:
            g[y][x] = val(m, 0, 1)
    # heiligdom: zuilen op de hoeken van het terras, het altaar met de kahuna, de stenen tafel naast de trap
    sx0, sy0, sx1, sy1 = SHRINE
    for x in (sx0 + 1, sx1 - 1):
        col(x, sy0, PILLAR, 'heiligdom')
        col(x, sy1 - 3, PILLAR_BROKEN, 'heiligdom')
    g[TABLET[1]][TABLET[0]] = val(BLOCK[0], 1, 3)

    # ---- strooidecor (alleen begaanbaar: varens, bladeren, bloempjes) op gras in het bos
    for y in range(TH):
        for x in range(TW):
            if mt(g[y][x]) == GRASS and C.c[y][x] == 'g':
                r = rng.random()
                if r < 0.06:
                    g[y][x] = val(rng.choice(LITTER), 0, 3)
                elif r < 0.09:
                    g[y][x] = val(rng.choice(FERN), 0, 3)
                elif r < 0.11:
                    g[y][x] = val(rng.choice(JFLOWER), 0, 3)
    # reuzenpalmen in massief bos
    used = set()
    cands = [(x, y) for y in range(2, TH - SAFE_ROWS - 4) for x in range(1, TW - 3)]
    rng.shuffle(cands)
    palms = 0
    for x, y in cands:
        if palms >= 8:
            break
        if all(C.get(x + dx, y + dy) == 'T' for dy in range(-1, 5) for dx in range(3)) and \
                not any((x + dx, y + dy) in used for dy in range(-3, 7) for dx in range(-2, 5)):
            for dy in range(4):
                for dx in range(3):
                    g[y + dy][x + dx] = val(jpalm[dy][dx], 1, 0)
                    used.add((x + dx, y + dy))
            palms += 1

    # zeerotsen rondom (niet in de aanloop vanaf Route 132)
    place_rocks(g, 14, 786, lambda x, y: (not (CX - 8 <= x <= CX + 8 and y >= 36) and y < FOG_Y - 1) or
                (y >= FOG_Y + 1 and not (CX - 14 <= x <= CX + 14)))

    # ---- controles
    start = [(CX, 40)]
    assert C.c[40][CX] == 'S'
    blocked = {(o['x'], o['y']) for o in objs}
    r = reach(g, start, blocked=blocked)
    for o in objs:
        if o['graphics_id'].startswith('OBJ_EVENT_GFX_SPECIES'):
            continue
        assert cx.next_to((o['x'], o['y']), r), ('object onbereikbaar', o['script'])
    for k in DAIS_AT:
        px, py = tapu_pos(k)
        assert (px, py + 1) in r, ('Tapu-altaar onbereikbaar', k)
    assert cx.next_to(TABLET, r)
    assert HIDDEN_PEARL in r and C.c[HIDDEN_PEARL[1]][HIDDEN_PEARL[0]] == 'S', 'verborgen item'
    # alle open land (behalve decor) hoort bereikbaar te zijn
    open_land = {(x, y) for y in range(TH) for x in range(TW) if C.c[y][x] in 'gLpfS' and cx.walkable(g[y][x])}
    lost = open_land - r - blocked
    assert not lost, ('afgesloten stukjes', sorted(lost)[:10])
    assert sms.primary_only(g, range(TH - SAFE_ROWS, TH)), 'onderste rijen moeten primary zijn (grens met Route 132)'
    r132 = sms.read('Route132', 80, 40)
    r132lo = sms.read('Route132_LowTide', 80, 40)
    for lay in (r132, r132lo):
        assert sms.primary_only([row[TAPU_OFFSET:TAPU_OFFSET + TW] for row in lay], range(0, 6)), 'Route 132 boven niet primary'
    for y in (FOG_Y,):
        assert all(mt(g[y][x]) == WATER for x in range(TW)), 'mistrij moet open water zijn'
    assert all(mt(g[TH - 1][x]) == WATER for x in range(CX - 12, CX + 12)), 'aanloop vanaf Route 132 dicht'

    sms.save(g, name)
    sms.border(name, t(WATER, False, 1))
    oq.register_layout(name, const, TW, TH, 'gTileset_FortreeJungle')
    sms.write_map(name, const, objs, [], coords, bgs, music='MUS_RG_SEVII_45', weather='WEATHER_FOG_HORIZONTAL',
                  region_map_section='MAPSEC_TAPU_ISLE',
                  connections=[{'map': 'MAP_ROUTE132', 'offset': -TAPU_OFFSET, 'direction': 'down'}])
    oq.register_map(name)
    sms.set_connection('Route132', 'MAP_TAPU_ISLE', 'up', TAPU_OFFSET)
    return name


# ====================================================================== Fullmoon Island (Cresselia)
FW, FH = 38, 36
FULLMOON_OFFSET = 30                # y van het eiland op Route 105
MOON_POOL = (11, 22)                # midden van het maanmeertje
CRESSELIA = (11, 19)
MOON_SIGN = (14, 22)                # onzichtbaar bord op de oostrand van het meertje


def fullmoon_island():
    name, const = 'FullmoonIsland', 'FULLMOON_ISLAND'
    rng = random.Random(488)                        # nationaal dexnummer van Cresselia
    land = [[False] * FW for _ in range(FH)]
    for y in range(FH):
        for x in range(FW):
            big = (x - 17) ** 2 + (y - 18) ** 2 <= 14 ** 2
            bite = (x - 25) ** 2 + (y - 12.5) ** 2 <= 10 ** 2
            land[y][x] = big and not bite
    smooth(land, 6)
    d = dist_to_water(land)
    C = Chars(FW, FH, '~')
    for y in range(FH):
        for x in range(FW):
            if land[y][x]:
                C.c[y][x] = 'S' if d[y][x] <= 2 else 'g'
    # maanmeertje (rond) in de buik van de maan, met grasoever
    for y in range(FH):
        for x in range(FW):
            dd = math.hypot(x - MOON_POOL[0], (y - MOON_POOL[1]) * 1.1)
            if dd <= 3.2 and C.c[y][x] == 'g':
                C.c[y][x] = 'w'
    # een paar boompjes (2 breed) op het gras, uit de buurt van de oever
    trees = [(6, 15), (18, 26), (9, 11)]
    for x, y in trees:
        for dx in range(2):
            for dy in range(2):
                if C.c[y + dy][x + dx] == 'g':
                    C.c[y + dy][x + dx] = 'T'
    # bloemen (wit/geel op het General-gras) rond het meertje
    for y in range(FH):
        for x in range(FW):
            if C.c[y][x] == 'g' and 3.4 <= math.hypot(x - MOON_POOL[0], (y - MOON_POOL[1]) * 1.1) <= 5.0 \
                    and rng.random() < 0.3:
                C.c[y][x] = 'f'

    if os.environ.get('TAPU_DEBUG'):
        print('\n'.join('%2d ' % y + ''.join(r) for y, r in enumerate(C.c)))
    P = name + '_EventScript_'
    SAILOR = (22, 25)
    objs = [
        obj('OBJ_EVENT_GFX_SPECIES(CRESSELIA)', *CRESSELIA, P + 'Cresselia', 'FLAG_TEMP_12',
            local_id='LOCALID_FULLMOON_CRESSELIA'),
        obj('OBJ_EVENT_GFX_SAILOR', *SAILOR, P + 'Sailor', move='MOVEMENT_TYPE_FACE_LEFT'),
    ]
    bgs = [sign(MOON_SIGN[0], MOON_SIGN[1], P + 'MoonPool'),
           hidden(16, 29, 'ITEM_MOON_STONE', 'FLAG_HIDDEN_ITEM_FULLMOON_ISLAND_MOON_STONE')]
    assert C.c[CRESSELIA[1]][CRESSELIA[0]] in 'gfS', 'Cresselia moet op land staan'
    assert C.c[MOON_SIGN[1]][MOON_SIGN[0]] == 'w' and C.c[MOON_SIGN[1]][MOON_SIGN[0] + 1] in 'gfS'

    g = [[0] * FW for _ in range(FH)]
    for y in range(FH):
        for x in range(FW):
            k = C.c[y][x]
            below = C.get(x, y + 1, '~')
            if k == '~':
                g[y][x] = t(WATER, False, 1)
            elif k == 'S':
                g[y][x] = sand_tile(land, x, y)
            elif k == 'T':
                g[y][x] = val(rng.choice(TRUNK if below != 'T' else FOREST), 1, 0)
            elif k == 'w':
                g[y][x] = pond_tile(C, x, y)
            elif below == 'T':
                g[y][x] = val(rng.choice(CANOPY), 0, 3)
            elif k == 'f':
                g[y][x] = val(FLOWER, 0, 3)
            else:
                g[y][x] = val(BANK if C.get(x, y - 1) == 'w' else GRASS, 0, 3)
    place_rocks(g, 7, 489, lambda x, y: x < FW - 4)

    # controles: aankomst vanaf Route 105 (west) over het water; alles op het eiland bereikbaar
    start = [(0, y) for y in range(FH) if mt(g[y][0]) == WATER]
    r = reach(g, start)
    for o in objs:
        assert cx.next_to((o['x'], o['y']), r), ('object onbereikbaar', o['script'])
    assert (16, 29) in r and (MOON_SIGN[0] + 1, MOON_SIGN[1]) in r
    open_land = {(x, y) for y in range(FH) for x in range(FW) if C.c[y][x] in 'gfS' and cx.walkable(g[y][x])}
    assert not open_land - r, 'afgesloten stukjes'
    r105 = sms.read('Route105', 40, 80)
    assert all(mt(r105[FULLMOON_OFFSET + y][39]) == WATER or not cx.walkable(r105[FULLMOON_OFFSET + y][39])
               for y in range(FH))

    sms.save(g, name)
    sms.border(name, t(WATER, False, 1))
    oq.register_layout(name, const, FW, FH, 'gTileset_Dewford')
    sms.write_map(name, const, objs, [], [], bgs, music='MUS_RG_SEVII_67', weather='WEATHER_NONE',
                  region_map_section='MAPSEC_FULLMOON_ISLAND',
                  connections=[{'map': 'MAP_ROUTE105', 'offset': -FULLMOON_OFFSET, 'direction': 'left'}])
    oq.register_map(name)
    sms.set_connection('Route105', 'MAP_FULLMOON_ISLAND', 'right', FULLMOON_OFFSET)
    return name


if __name__ == '__main__':
    open_reef()
    names = [tapu_isle(), fullmoon_island()]
    if len(sys.argv) > 1:
        import subprocess
        for n in names:
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', '60'], check=True)
    print('klaar:', ', '.join(names))
