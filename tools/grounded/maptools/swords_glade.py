"""Project Grounded: Virizion-kamer in Mangrove Mire (aangeroepen door swords_keldeo.py; deterministisch, idempotent).

- Mangrove Mire: aan het einde van het oostelijke zijpad (49-50,13) wordt de boomrand een groene tunnel: een donkere
  opening onder twee bomen, omlijst door een boog van mangrovewortels met lianen; schaduw op het gras ervoor.
  Tegelgedrag MB_NON_ANIMATED_DOOR (je loopt naar het noorden de tunnel in). Virizion en de boom met de snede staan
  niet meer op het zijpad; de plek is weer gewoon bosrand.
- MangroveMire_VirizionGlade (20x16, gMapGroup_Grounded): een open plek omsloten door jungle-bomen, met een grote
  mangrove met een schone diagonale zwaardsnede in de stam (bord), mangroves en wortelbogen, varens, orchideeen en
  een zonnevlek waar Virizion staat. Uitgang: de donkere tunnel onderaan (zuidpijl-warp).
De tiles en metatiles komen achteraan de secondary mangrove_mire (die van mangrove_swamp.py); bestaande tiles en
metatiles worden hergebruikt (ontdubbeld), dus opnieuw draaien voegt niets dubbel toe. Draai na mangrove_swamp.py
altijd swords_keldeo.py opnieuw (dat script schrijft tileset en moeraskaart opnieuw)."""
import json, math, os, random, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ogerpon_quest as oq          # zet ook de werkmap op de repo-root
import jungle_tileset as J

MIRE_TS = 'data/tilesets/secondary/mangrove_mire'
BASE_MT = 216                       # zoveel metatiles maakt mangrove_swamp.py; alles daarna is van dit script
P_SWAMP = 8
GRASS_MAP = {12: 1, 13: 2, 14: 3}   # General-gras (palet 2) -> moeraspalet 8
MB_NON_ANIMATED_DOOR, MB_SOUTH_ARROW_WARP = 0x60, 0x65
SOLID = 0xc00


class MireTiles(J.JungleTileset):
    """De bestaande secondary mangrove_mire, met ontdubbelen tegen alles wat er al in staat."""

    def __init__(self):
        J.SRC = J.TS = MIRE_TS
        super().__init__()
        # terug naar de tileset van mangrove_swamp.py (BASE_MT metatiles); tiles die alleen eerdere runs van dit
        # script gebruikten, komen weer vrij
        assert len(self.mts) // 16 >= BASE_MT
        del self.mts[BASE_MT * 16:]
        del self.attrs[BASE_MT * 2:]
        ref = {(e & 0x3FF) - 512 for e in struct.unpack('<%dH' % (len(self.mts) // 2), self.mts) if e & 0x3FF >= 512}
        for slot in range(1, 512):
            if slot not in ref:
                self.tiles[slot] = [[0] * 8 for _ in range(8)]
        self.free = [t for t in range(1, 512) if t not in ref]
        for slot in range(1, 512):
            t = self.tiles[slot]
            if any(any(r) for r in t):
                self.tidx.setdefault(tuple(tuple(r) for r in t), 512 + slot)
        n = len(self.mts) // 16
        for i in range(n):
            e = struct.unpack_from('<8H', self.mts, i * 16)
            at = struct.unpack_from('<H', self.attrs, i * 2)[0]
            self.midx.setdefault((tuple(e[:4]), tuple(e[4:]), at), 512 + i)
        self.n0 = n

    def metatile(self, bottom, top, attr):
        key = (tuple(bottom), tuple(top), attr)
        if key not in self.midx:
            idx = 512 + len(self.mts) // 16
            assert idx < 1024, 'te veel metatiles'
            self.mts += struct.pack('<8H', *(list(bottom) + list(top)))
            self.attrs += struct.pack('<H', attr)
            self.midx[key] = idx
        return self.midx[key]

    def save(self):
        from PIL import Image
        out = Image.new('P', (128, 256), 0)
        out.putpalette(self.pngpal)
        for n, t in enumerate(self.tiles):
            for y in range(8):
                for x in range(8):
                    out.putpixel(((n % 16) * 8 + x, (n // 16) * 8 + y), t[y][x])
        out.save(MIRE_TS + '/tiles.png')
        open(MIRE_TS + '/metatiles.bin', 'wb').write(self.mts)
        open(MIRE_TS + '/metatile_attributes.bin', 'wb').write(self.attrs)
        return len(self.mts) // 16 - self.n0, len(self.free)

    # -- pixels van een bestaande laag (palet, index)
    def tilepix(self, e):
        ti, hf, vf = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1
        src = self.gtiles[ti] if ti < 512 else self.tiles[ti - 512]
        return [[src[7 - y if vf else y][7 - x if hf else x] for x in range(8)] for y in range(8)], e >> 12

    def layer(self, ents):
        cv, pals = J.Canvas(16, 16), set()
        for k, e in enumerate(ents):
            pix, pal = self.tilepix(e)
            if any(any(r) for r in pix):
                pals.add(pal)
            for y in range(8):
                for x in range(8):
                    cv.p[(k // 2) * 8 + y][(k % 2) * 8 + x] = pix[y][x]
        return cv, pals


def attr_of(ts, m):
    return ts.base(m)[2]


def grass_canvas(ts):
    """16x16 gras (General 0x001) in moeraspalet 8."""
    cv, pals = ts.layer(ts.base(0x001)[0])
    for y in range(16):
        for x in range(16):
            cv.p[y][x] = GRASS_MAP.get(cv.p[y][x], 2)
    return cv


BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def dith(x, y, a):
    """True met kans a (0..1) volgens een 4x4-Bayer-raster."""
    return BAYER[y & 3][x & 3] < a * 16


# ====================================================================== tunnelingang in het moeras
DOOR = [(49, 13), (50, 13)]


def tunnel(ts):
    """Twee metatiles (links, rechts) voor de tunnel in de boomrand + twee schaduwvakken voor het gras eronder."""
    trunk = 0x201
    left, pals = ts.layer(ts.base(trunk)[0])
    assert pals == {J.P_TREE}, pals
    cv = J.Canvas(32, 16)
    cv.paste(left, 0, 0)
    cv.paste(left, 16, 0)
    for y in range(16):                         # paste slaat 0 over: de stam heeft geen doorzichtige pixels nodig
        for x in range(16):
            cv.p[y][x] = left.p[y][x]
            cv.p[y][16 + x] = left.p[y][x]
    cx, hw, top = 15.5, 12.5, 2.0

    def ell(x, y, grow=0.0):
        return ((x - cx) / (hw + grow)) ** 2 + ((y - 16.5) / (16.5 - top + grow)) ** 2
    for y in range(16):
        for x in range(32):
            e = ell(x, y)
            if e < 1:                           # binnenkant: diep donkergroen, onderaan licht dat naar binnen valt
                c = 4
                if y >= 13 and dith(x, y, (y - 12) / 5):
                    c = 3
                cv.p[y][x] = c
            elif ell(x, y, 2.6) < 1:            # wortelboog (2-3 px): bruin, lichtkant boven-links
                c = 5
                if ell(x, y, 1.2) < 1 and (x < cx or y < 6):
                    c = 7
                cv.p[y][x] = c
    for x0 in (2, 4, 27, 29):                   # uitgespreide wortelvoetjes
        for y in range(12, 16):
            xx = x0 + (y - 12) // 2 * (-1 if x0 < 16 else 1)
            cv.set(xx, y, 5)
    for vx, y1, ph in ((9, 7, 0.0), (15, 5, 2.0), (21, 8, 1.0)):   # lianen die in de opening hangen
        ytop = int(top + 16.5 - 16.5 * math.sqrt(max(0.0, 1 - ((vx - cx) / hw) ** 2))) - 1
        J.vine(cv, vx, max(0, ytop), max(ytop + 2, y1), ph, tip=True)
    door = []
    for i in range(2):
        at = (attr_of(ts, trunk) & 0xF000) | MB_NON_ANIMATED_DOOR
        door.append(ts.metatile(ts.cut(cv, i * 16, 0, J.P_TREE), [0, 0, 0, 0], at))
    # schaduw op het gras ervoor: bovenaan donker, naar onderen toe weg (alleen onder de opening)
    g = J.Canvas(32, 16)
    gc = grass_canvas(ts)
    for y in range(16):
        for x in range(32):
            c = gc.p[y][x % 16]
            # een zachte halve ellips onder de opening: kern donker (4), rand halftoon (5), schaakbord-overgang
            e = ((x - cx) / (hw - 0.5)) ** 2 + (y / 4.5) ** 2
            if e < 0.45:
                c = 4 if (x + y) & 1 or y == 0 else 5
            elif e < 0.8:
                c = 5
            elif e < 1.0 and (x + y) & 1:
                c = 5
            g.p[y][x] = c
    shade = [ts.metatile(ts.cut(g, i * 16, 0, P_SWAMP), [0, 0, 0, 0], attr_of(ts, 0x001)) for i in range(2)]
    return door, shade


def mire(ts, glade_warps):
    """Tunnel in het moeras + warps; Virizion en het oude bord eruit."""
    W, H = 56, 44
    path = 'data/layouts/MangroveMire/map.bin'
    g = oq.read_layout(path, W, H)
    door, shade = tunnel(ts)
    for i, (x, y) in enumerate(DOOR):
        cur = g[y][x] & 0x3FF
        assert cur == 0x201 or cur >= 512 + BASE_MT, ('geen boomstam op de tunnelplek', x, y, hex(cur))
        g[y][x] = door[i] | (3 << 12)
        below = g[y + 1][x] & 0x3FF
        assert below == 0x001 or below >= 512 + BASE_MT, ('geen gras voor de tunnel', x, y + 1, hex(below))
        g[y + 1][x] = shade[i] | (3 << 12)
    oq.cx.save_grid(g, path)

    def fn(m):
        m['object_events'] = [o for o in m['object_events'] if o.get('local_id') != 'LOCALID_MANGROVE_MIRE_VIRIZION']
        m['bg_events'] = [b for b in m['bg_events'] if b.get('script') != 'MangroveMire_EventScript_CutTree']
        m['warp_events'] = [w for w in m['warp_events'] if w['dest_map'] != 'MAP_MANGROVE_MIRE_VIRIZION_GLADE']
        idx = []
        for (x, y), wid in zip(DOOR, glade_warps):
            idx.append(len(m['warp_events']))
            m['warp_events'].append({'x': x, 'y': y, 'elevation': 3, 'dest_map': 'MAP_MANGROVE_MIRE_VIRIZION_GLADE',
                                     'dest_warp_id': str(wid)})
        return idx
    idx = oq.edit_map('MangroveMire', fn)
    r = oq.reach(g, [(54, 29)])
    for x, y in DOOR:
        assert (x, y + 1) in r, ('tunnel onbereikbaar', x, y)
    return idx


# ====================================================================== de open plek
GW, GH = 20, 16
PLAN = ['TTTTTTTTTTTTTTTTTTTT',
        'TTTTTTTTTTTTTTTTTTTT',
        'TTTTggggggggggggTTTT',
        'TTTgggggggggggggggTT',
        'TTggggggggggggggggTT',
        'TTggggggggggggggggTT',
        'TTggggggggggggggggTT',
        'TTggggggggggggggggTT',
        'TTggggggggggggggggTT',
        'TTTgggggggggggggggTT',
        'TTTggggggggggggggTTT',
        'TTTTgggggggggggggTTT',
        'TTTTTTggggggggTTTTTT',
        'TTTTTTTTTggTTTTTTTTT',
        'TTTTTTTTTggTTTTTTTTT',
        'TTTTTTTTTggTTTTTTTTT']
EXIT = [(9, GH - 1), (10, GH - 1)]
VIRIZION = (10, 7)
BIG = (5, 2)                        # grote mangrove met de zwaardsnede (3x3), bord op het middelste wortelvak
CUT_SIGN = (6, 4)
SMALL = [(15, 3), (2, 5), (15, 8)]  # kleine mangroves (2x3)
ARCHES = [(4, 10), (12, 11)]        # wortelbogen (2x1)
LOG = (11, 3)                        # omgevallen stam (3x1)


def slash(cv):
    """Schone diagonale snede door de stam van de grote mangrove: licht hout in de snede, donkere kier erboven."""
    x0, y0, x1, y1 = 15, 27, 32, 37
    n = 60
    for i in range(n + 1):
        t = i / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        xi, yi = int(round(x)), int(round(y))
        for dy, c in ((-1, 6), (0, 13), (1, 13), (2, 9)):
            if 0 <= yi + dy < cv.h and cv.p[yi + dy][xi] in (6, 7, 8, 9, 13):
                cv.p[yi + dy][xi] = c
    return cv


def glade(ts, mire_warps):
    rng = random.Random(640)                    # Virizion
    T = [list(r) for r in PLAN]
    assert len(T) == GH and all(len(r) == GW for r in T)
    for _ in range(3):
        for y in range(1, GH - 1):              # geen losse 1-hoge of 1-brede bosstukjes
            for x in range(1, GW - 1):
                if T[y][x] == 'T' and ((T[y - 1][x] == 'g' and T[y + 1][x] == 'g') or
                                       (T[y][x - 1] == 'g' and T[y][x + 1] == 'g')):
                    T[y][x] = 'g'
    if os.environ.get('GLADE_DEBUG'):
        for y in range(GH):
            print('%2d ' % y + ''.join(T[y]))

    def kind(x, y):
        return T[y][x] if 0 <= x < GW and 0 <= y < GH else 'T'

    def val(mt, coll, elev):
        return mt | (coll << 10) | (elev << 12)
    FOREST = [ts.jungle(m) for m in (0x0C6, 0x0C7)]
    TRUNK = [ts.jungle(m) for m in (0x016, 0x017)]
    CANOPY = [ts.jungle(m) for m in (0x00E, 0x00F)]
    for m in FOREST + TRUNK + CANOPY:
        assert m < 512 + ts.n0, 'bosmetatiles horen al in het moeras te staan'
    M = [[0] * GW for _ in range(GH)]
    for y in range(GH):
        for x in range(GW):
            below = kind(x, y + 1)
            if T[y][x] == 'T':
                if below != 'T':
                    base = rng.choice((0x016, 0x017))
                    mt = ts.jungle(base)
                    if rng.random() < 0.35:
                        vx, ph = rng.choice((3, 11)), rng.choice((0.0, 2.0))
                        mt = ts.recolor(base, draw=lambda cv, vx=vx, ph=ph: J.vine(cv, vx, 0, 11, ph, tip=True))
                    M[y][x] = val(mt, 1, 0)
                else:
                    M[y][x] = val(rng.choice(FOREST), 1, 0)
            elif below == 'T' and (x, y) not in EXIT:
                M[y][x] = val(rng.choice(CANOPY), 0, 3)
            else:
                M[y][x] = val(0x001, 0, 3)
    # zonnevlek rond Virizion (lichter gras, zachte geditherde rand)
    gc = grass_canvas(ts)
    LIGHT = {3: 2, 2: 1, 1: 15, 4: 5, 5: 2}
    cxp, cyp = VIRIZION[0] * 16 + 8, VIRIZION[1] * 16 + 6
    for y in range(VIRIZION[1] - 2, VIRIZION[1] + 3):
        for x in range(VIRIZION[0] - 2, VIRIZION[0] + 3):
            if M[y][x] & 0x3FF != 0x001:
                continue
            cv, hit = J.Canvas(16, 16), False
            for py in range(16):
                for px in range(16):
                    X, Y = x * 16 + px, y * 16 + py
                    d = ((X - cxp) / 30.0) ** 2 + ((Y - cyp) / 22.0) ** 2
                    c = gc.p[py][px]
                    if d < 1 and dith(X, Y, min(1.0, (1 - d) * 1.6)):
                        c = LIGHT.get(c, c); hit = True
                    cv.p[py][px] = c
            if hit:
                M[y][x] = val(ts.metatile(ts.cut(cv, 0, 0, P_SWAMP), [0, 0, 0, 0], attr_of(ts, 0x001)), 0, 3)
    # uitgang: donkere tunnelvloer onderaan, wordt naar de kaartrand toe donker
    for row, (y, a0, a1) in enumerate(((GH - 2, 0.0, 0.35), (GH - 1, 0.35, 1.0))):
        for i, x in enumerate((9, 10)):
            cv = J.Canvas(16, 16)
            for py in range(16):
                for px in range(16):
                    X = i * 16 + px
                    a = a0 + (a1 - a0) * py / 15
                    side = min(X, 31 - X)
                    if side < 4:
                        a = min(1.0, a + (4 - side) * 0.12)
                    c = gc.p[py][px]
                    if dith(X, y * 16 + py, a):
                        c = 14 if dith(X + 2, py + 1, max(0.0, a - 0.45) * 2) else 4
                    cv.p[py][px] = c
            at = attr_of(ts, 0x001) | (MB_SOUTH_ARROW_WARP if y == GH - 1 else 0)
            M[y][x] = val(ts.metatile(ts.cut(cv, 0, 0, P_SWAMP), [0, 0, 0, 0], at), 0, 3)

    # decor
    BLOCK = set()
    EV = {VIRIZION, CUT_SIGN} | set(EXIT)
    KEEP = set()
    for x, y in EV | {(VIRIZION[0], VIRIZION[1] + 1), (CUT_SIGN[0], CUT_SIGN[1] + 1)}:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                KEEP.add((x + dx, y + dy))
    for y in range(9, GH):
        for x in (8, 9, 10, 11):
            KEEP.add((x, y))

    def mid(x, y):
        return M[y][x] & 0x3FF

    def free_ground(x, y):
        if not (0 <= x < GW and 0 <= y < GH) or T[y][x] != 'g' or (x, y) in BLOCK:
            return False
        b, t, _ = ts.base(mid(x, y))
        return not any(t) and kind(x, y + 1) != 'T' and M[y][x] & SOLID == 0

    def stamp(x0, y0, cv, pal, block=True):
        w, h = cv.w // 16, cv.h // 16
        cells = [(x0 + i, y0 + j) for j in range(h) for i in range(w)]
        if not all(free_ground(x, y) for x, y in cells) or (block and any(c in KEEP for c in cells)):
            return False
        for j in range(h):
            for i in range(w):
                x, y = x0 + i, y0 + j
                v = M[y][x]
                M[y][x] = ts.overlay(mid(x, y), cv, i * 16, j * 16, pal, layer=1) | ((1 if block else 0) << 10) | (v & 0xF000)
        if block:
            BLOCK.update(cells)
        return True

    big = slash(J.mangrove(True, False))
    for c in [(BIG[0] + i, BIG[1] + j) for j in range(3) for i in range(3)]:
        KEEP.discard(c)
    assert stamp(BIG[0], BIG[1], big, J.P_JUNGLE), 'grote mangrove past niet'
    BLOCK.add(CUT_SIGN)
    for (x, y), big_ in ((p, False) for p in SMALL):
        assert stamp(x, y, J.mangrove(big_, False), J.P_JUNGLE), ('mangrove past niet', x, y)
    assert stamp(LOG[0], LOG[1], J.log(3), J.P_JUNGLE), 'stam past niet'
    for x, y in ARCHES:
        assert stamp(x, y, J.root_arch(False), J.P_JUNGLE), ('wortelboog past niet', x, y)
    cells = [(x, y) for y in range(GH) for x in range(GW)]
    rng.shuffle(cells)
    n = {'fern': 0, 'flower': 0, 'litter': 0}
    for x, y in cells:
        if (x, y) in KEEP or (x, y) in EV:
            continue
        t = sum(kind(x + dx, y + dy) == 'T' for dx in (-1, 0, 1) for dy in (-1, 0, 1))
        r = rng.random()
        if t >= 2 and r < 0.5:
            n['fern'] += stamp(x, y, J.fern(rng.randrange(2)), J.P_JUNGLE, block=False)
        elif t == 0 and r < 0.18 and n['flower'] < 6:
            n['flower'] += stamp(x, y, J.groundflowers(rng.randrange(2)), J.P_FLOWER, block=False)
        elif r < 0.3:
            n['litter'] += stamp(x, y, J.litter(rng.randrange(3)), J.P_JUNGLE, block=False)
    # bereikbaarheid
    blocked = {VIRIZION}
    r = oq.reach(M, [EXIT[0]], blocked=blocked)
    for p in EXIT + [(VIRIZION[0], VIRIZION[1] + 1), (CUT_SIGN[0], CUT_SIGN[1] + 1)]:
        assert p in r, ('onbereikbaar', p)
    assert M[CUT_SIGN[1]][CUT_SIGN[0]] & SOLID
    if os.environ.get('GLADE_DEBUG'):
        for y in range(GH):
            print('%2d ' % y + ''.join('#' if M[y][x] & SOLID else ('V' if (x, y) == VIRIZION else '.') for x in range(GW)))
    # schrijven
    os.makedirs('data/layouts/MangroveMire_VirizionGlade', exist_ok=True)
    oq.cx.save_grid(M, 'data/layouts/MangroveMire_VirizionGlade/map.bin')
    f = FOREST[0] | 0x400
    open('data/layouts/MangroveMire_VirizionGlade/border.bin', 'wb').write(struct.pack('<4H', f, FOREST[1] | 0x400, FOREST[1] | 0x400, f))
    oq.register_layout('MangroveMire_VirizionGlade', 'MANGROVE_MIRE_VIRIZION_GLADE', GW, GH, 'gTileset_MangroveMire')
    o = oq.obj('OBJ_EVENT_GFX_SPECIES(VIRIZION)', VIRIZION[0], VIRIZION[1], 'MangroveMire_VirizionGlade_EventScript_Virizion',
               'FLAG_TEMP_1', 'LOCALID_VIRIZION_GLADE_VIRIZION', move='MOVEMENT_TYPE_FACE_DOWN')
    warps = [{'x': x, 'y': y, 'elevation': 3, 'dest_map': 'MAP_MANGROVE_MIRE', 'dest_warp_id': str(w)}
             for (x, y), w in zip(EXIT, mire_warps)]
    oq.write_map('MangroveMire_VirizionGlade', 'MANGROVE_MIRE_VIRIZION_GLADE', 'MangroveMire', 'MANGROVE_MIRE_VIRIZION_GLADE',
                 [o], warps, show_map_name=False, allow_cycling=False, allow_escaping=False)
    oq.edit_map('MangroveMire_VirizionGlade', lambda m: m.__setitem__('bg_events', [
        {'type': 'sign', 'x': CUT_SIGN[0], 'y': CUT_SIGN[1], 'elevation': 0,
         'player_facing_dir': 'BG_EVENT_PLAYER_FACING_NORTH', 'script': 'MangroveMire_VirizionGlade_EventScript_CutTree'}]))
    oq.register_map('MangroveMire_VirizionGlade')
    return n


def main():
    ts = MireTiles()
    # warpvolgorde ligt vast: kaart 'MangroveMire' krijgt zijn tunnelwarps achteraan, de open plek heeft er twee (0, 1)
    m = json.load(open('data/maps/MangroveMire/map.json'))
    keep = [w for w in m['warp_events'] if w['dest_map'] != 'MAP_MANGROVE_MIRE_VIRIZION_GLADE']
    mire_idx = mire(ts, [0, 1])
    assert mire_idx == [len(keep), len(keep) + 1]
    n = glade(ts, mire_idx)
    new, free = ts.save()
    print('open plek:', n, '| %d nieuwe metatiles in mangrove_mire, %d tiles vrij' % (new, free))


if __name__ == '__main__':
    main()
