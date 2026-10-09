"""Project Grounded: Chargestone Cave (Spacetime Cave-sidequest; Unova in een andere tijd).

Drie kaarten (gMapGroup_Spacetime, achteraan), Meteor Falls-vormen met een donkerblauwe tint en zwevende
magneetstenen (chargestone_tiles.py):
  ChargestoneCave_1F   Ingang (warp 0 = terug naar de Spacetime Cave; hier komt de hub-scheur uit), grote hal,
                       oostkamer met de ladder naar B1F, zijgrot achter een duwsteen (Strength).
  ChargestoneCave_B1F  Grote grot; de ladder naar B2F staat achter een hek van zwevende stenen: twee duwstenen
                       (licht puzzelpad, door dit script met een Sokoban-BFS gecontroleerd).
  ChargestoneCave_B2F  Colress' lab: zijn machine tapt de stroom van ZERAORA af. Verslaat je hem, dan gaat de
                       machine uit en verschijnt ZERAORA achterin (lv 70, legendary-gevecht).
Quest: vier Neo Plasma-assistenten (lv 66-70) + COLRESS (andere dimensie: kent je niet, is hier wél evil, lv 72-75).
Klaar-flag: FLAG_SPACETIME_CHARGESTONE_DONE (Zeraora gevangen of verslagen).
Extra: mapsec MAPSEC_CHARGESTONE_CAVE is een magnetisch veld: Magneton -> Magnezone, Charjabug -> Vikavolt.
Flags FLAG_GROUNDED 760-799, trainers 1124-1128.
Teksten zijn placeholders (Jordi herschrijft ze).
Gebruik: python3 tools/grounded/maptools/chargestone.py [render-uitmap]"""
import json, math, os, random, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import meteor_falls_ext as mf          # werkmap = repo-root
import victory_road_ext as vre
import beacon_dragon as bd
import chargestone_tiles as ct

os.chdir(ct.REPO)
Scr, text = bd.Scr, bd.text
cell = mf.cell
E = mf.E_FLOOR
ID = ct.ids()
PRIM, SEC = 'gTileset_ChargestoneGeneral', 'gTileset_Chargestone'
GROUP = 'gMapGroup_Spacetime'
F1, B1, B2 = 'ChargestoneCave_1F', 'ChargestoneCave_B1F', 'ChargestoneCave_B2F'
MUSIC = 'MUS_RG_SEVII_CAVE'

# ====================================================================== flags (FLAG_GROUNDED 760-799)
FLAGS = [
    (760, 'FLAG_SPACETIME_CHARGESTONE_DONE', 'Chargestone Cave: ZERAORA gevangen of verslagen (klaar-flag sidequest)'),
    (761, 'FLAG_HIDE_CHARGESTONE_ZERAORA', 'Chargestone Cave B2F: ZERAORA verborgen (voor Colress verslagen is of na het gevecht)'),
    (762, 'FLAG_HIDE_CHARGESTONE_COLRESS', 'Chargestone Cave B2F: Colress weg (na ZERAORA)'),
    (763, 'FLAG_ITEM_CHARGESTONE_1F_THUNDER_STONE', 'Chargestone Cave 1F: Thunder Stone'),
    (764, 'FLAG_ITEM_CHARGESTONE_1F_MAX_REVIVE', 'Chargestone Cave 1F: Max Revive (zijgrot achter de duwsteen)'),
    (765, 'FLAG_ITEM_CHARGESTONE_B1F_MAGNET', 'Chargestone Cave B1F: Magnet'),
    (766, 'FLAG_ITEM_CHARGESTONE_B1F_METAL_COAT', 'Chargestone Cave B1F: Metal Coat'),
    (767, 'FLAG_ITEM_CHARGESTONE_B2F_ELECTIRIZER', 'Chargestone Cave B2F: Electirizer'),
    (768, 'FLAG_ITEM_CHARGESTONE_B2F_PP_MAX', 'Chargestone Cave B2F: PP Max'),
    (769, 'FLAG_HIDDEN_ITEM_CHARGESTONE_1F_CELL_BATTERY', 'Chargestone Cave 1F: verborgen Cell Battery'),
    (770, 'FLAG_HIDDEN_ITEM_CHARGESTONE_B1F_BIG_NUGGET', 'Chargestone Cave B1F: verborgen Big Nugget'),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// chargestone { (tools/grounded/maptools/chargestone.py; FLAG_GROUNDED 760-799, 771-799 nog vrij)\n'
    for n, name, why in FLAGS:
        assert 760 <= n <= 799
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// chargestone {' in s:
        i = s.index('// chargestone {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// mega_forest {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    s = s.replace('620-659 Mega Forest (mega_forest.py), 660+ vrij.',
                  '620-659 Mega Forest (mega_forest.py), 760-799 Chargestone Cave (chargestone.py), 660+ vrij '
                  '(behalve 760-799).')
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== kaarten
def const(name):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper().replace('CAVE_1_F', 'CAVE_1F')


CONST = {F1: 'CHARGESTONE_CAVE_1F', B1: 'CHARGESTONE_CAVE_B1F', B2: 'CHARGESTONE_CAVE_B2F'}


class Cave(mf.Map):
    """Meteor Falls-autotiler met organische vormen (9 okt, Jordi: te steriel/rechthoekig):
    kamers = overlappende ruisellipsen + kronkelgangen, op een 2x2-raster (geen trapjes van 1 tegel), dunne
    rotsribbels weg; terrassen (lage klif met trap) over de volle breedte van een kamer; decor (zwevende stenen in
    drie maten, kristallen, gloeiende scheuren, schroot, Colress' machines en kabels) buiten de looproutes."""

    def __init__(self, w, h, seed):
        super().__init__(w, h)
        self.rnd = random.Random(seed)
        self.stones = []
        self.frozen = {}          # (x,y) -> 'F'/'R' na het vormen
        self.terraces = []        # (xa, xb, ys, stairs)
        self.blocked_decor = set()

    # ---------------------------------------------------------------- vormen
    def blob(self, cx, cy, rx, ry, seed, noise=0.12):
        rnd = random.Random('%s-%s' % (seed, self.W))
        nz = [rnd.uniform(-noise, noise) for _ in range(10)]
        for y in range(max(0, int(cy - ry) - 2), min(self.H, int(cy + ry) + 3)):
            for x in range(max(0, int(cx - rx) - 2), min(self.W, int(cx + rx) + 3)):
                a = math.atan2((y - cy) / ry, (x - cx) / rx)
                k = (a + math.pi) / (2 * math.pi) * 10
                i, f = int(k) % 10, k - int(k)
                n = nz[i] * (1 - f) + nz[(i + 1) % 10] * f
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= (1 + n) ** 2:
                    self.k[y][x] = 'F'

    def lobes(self, x0, y0, x1, y1, seed, n=6):
        """Organische kamer binnen het vak (x0,y0)-(x1,y1): een ellips met n bulten langs de rand, nooit buiten het vak."""
        rnd = random.Random('%s-%d-%d' % (seed, x0, y0))
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 0.5, (y1 - y0) / 2 + 0.5
        parts = [(cx, cy, rx * 0.66, ry * 0.62)]
        for i in range(n):
            a = 2 * math.pi * (i + rnd.uniform(0.15, 0.85)) / n
            k = rnd.uniform(0.22, 0.42)
            d = rnd.uniform(0.55, 0.8)
            parts.append((cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d, max(1.8, rx * k), max(1.6, ry * k * 1.2)))
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if any(((x - px) / prx) ** 2 + ((y - py) / pry) ** 2 <= 1 for px, py, prx, pry in parts):
                    self.k[y][x] = 'F'

    def path(self, pts, r=1.9):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 1
            for i in range(n + 1):
                px, py = x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n
                for y in range(int(py - r) - 1, int(py + r) + 2):
                    for x in range(int(px - r) - 1, int(px + r) + 2):
                        if (x - px) ** 2 + (y - py) ** 2 <= r * r and 0 <= x < self.W and 0 <= y < self.H:
                            self.k[y][x] = 'F'

    def freeze(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.frozen[(x, y)] = c

    def terrace(self, x0, x1, ys, stairs):
        """Terras over de volle breedte (x0-x1) op rij ys (lip) / ys+1 (klifwand met een trap van 2 op stairs)."""
        self.freeze(x0, ys - 1, x1, ys + 2, 'F')
        self.freeze(x0 - 3, ys - 1, x0 - 1, ys + 2, 'R')
        self.freeze(x1 + 1, ys - 1, x1 + 3, ys + 2, 'R')
        self.terraces.append((x0, x1, ys, (stairs, stairs + 1)))

    def shape(self):
        """Op een raster van 2x2-blokken: meerderheid per blok, rotsbanden van 1 blok (2 tegels) open, diagonale
        aanrakingen open, rand van 2 blokken rots; daarna de bevroren cellen (terrassen, gangen)."""
        Wc, Hc = self.W // 2, self.H // 2
        B = [[sum(self.k[2 * by + b][2 * bx + a] == 'F' for a in (0, 1) for b in (0, 1)) >= 2 for bx in range(Wc)]
             for by in range(Hc)]
        fb = {}
        for (x, y), c in self.frozen.items():
            if x // 2 < Wc and y // 2 < Hc:
                fb.setdefault((x // 2, y // 2), set()).add(c)
        for _ in range(20):
            ch = 0
            for by in range(Hc):
                for bx in range(Wc):
                    if bx < 2 or by < 2 or bx >= Wc - 2 or by >= Hc - 2:
                        B[by][bx] = False
            for (bx, by), cs in fb.items():
                if cs == {'F'}:
                    B[by][bx] = True
                elif cs == {'R'}:
                    B[by][bx] = False
            for by in range(1, Hc - 1):
                for bx in range(1, Wc - 1):
                    if B[by][bx] or fb.get((bx, by)) == {'R'}:
                        continue
                    if (B[by][bx - 1] and B[by][bx + 1]) or (B[by - 1][bx] and B[by + 1][bx]):
                        B[by][bx] = True; ch += 1
            for by in range(Hc - 1):
                for bx in range(Wc - 1):
                    q = (B[by][bx], B[by][bx + 1], B[by + 1][bx], B[by + 1][bx + 1])
                    if q == (True, False, False, True):
                        B[by][bx + 1] = True; ch += 1
                    elif q == (False, True, True, False):
                        B[by][bx] = True; ch += 1
            if not ch:
                break
        for y in range(self.H):
            for x in range(self.W):
                bx, by = x // 2, y // 2
                self.k[y][x] = 'F' if bx < Wc and by < Hc and B[by][bx] else 'R'
        for (x, y), c in self.frozen.items():
            self.k[y][x] = c
        for y in range(self.H):
            for x in range(self.W):
                if x < 3 or y < 2 or x >= self.W - 3 or y >= self.H - 3:
                    assert self.k[y][x] == 'R', ('vloer te dicht bij de rand', x, y)

    # ---------------------------------------------------------------- decor
    def stone(self, x, y, kind=None):
        kind = kind or self.rnd.choice(('stoneA', 'stoneA_f', 'stoneB', 'stoneB_f'))
        n = int(round(len(ID[kind]) ** 0.5))
        for i, m in enumerate(ID[kind]):
            self.set(x + i % n, y + i // n, m, 1)
            self.blocked_decor.add((x + i % n, y + i // n))
        self.stones.append((x, y, n))

    def shard(self, x, y):
        self.set(x, y, ID['shard'][0], 1)
        self.blocked_decor.add((x, y))

    def one(self, x, y, kind, blocked=True):
        self.set(x, y, ID[kind][0], 1 if blocked else 0)
        if blocked:
            self.blocked_decor.add((x, y))

    def cable(self, cells):
        """Kabel over de vloer langs een rij aaneengesloten cellen (eerste/laatste cel sluit aan op een machine)."""
        cells = list(cells)
        for i, (x, y) in enumerate(cells):
            dirs = set()
            for j in (i - 1, i + 1):
                if 0 <= j < len(cells):
                    nx, ny = cells[j]
                    dirs.add('N' if ny < y else 'S' if ny > y else 'W' if nx < x else 'E')
            if len(dirs) == 1:                     # uiteinde: recht doortrekken naar de machine ernaast
                d = dirs.pop()
                dirs = {d, {'N': 'S', 'S': 'N', 'W': 'E', 'E': 'W'}[d]}
            key = ''.join(c for c in 'NSWE' if c in dirs)
            name = {'NS': 'cableNS', 'WE': 'cableWE', 'NE': 'cableNE', 'NW': 'cableNW', 'SE': 'cableSE',
                    'SW': 'cableSW'}[key]
            self.set(x, y, ID[name][0], 0)

    def terrace_rows(self):
        return {(x, y) for x0, x1, ys, _ in self.terraces for x in range(x0 - 1, x1 + 2) for y in range(ys - 1, ys + 3)}

    def free(self, x, y, w, h, keep, margin=1):
        tr = self.terrace_rows()
        for b in range(-margin, h + margin):
            for a in range(-margin, w + margin):
                p = (x + a, y + b)
                inside = 0 <= a < w and 0 <= b < h
                if inside and (not self.isF(*p) or self.k[p[1]][p[0]] != 'F' or p in keep or p in self.over or p in tr):
                    return False
                if not inside and (p in self.blocked_decor):
                    return False
        return True

    def decorate(self, keep, counts, area=None):
        x0, y0, x1, y1 = area or (0, 0, self.W - 1, self.H - 1)
        size = {'stoneL': (3, 3), 'stone': (2, 2), 'crysL': (2, 2), 'pebble': (1, 1), 'shard': (1, 1), 'crys': (1, 1),
                'scrap': (1, 1), 'crack': (1, 1), 'spark': (1, 1)}
        for kind, n in counts:
            w, h = size[kind]
            tries = 0
            while n and tries < 3000:
                tries += 1
                x, y = self.rnd.randint(x0, x1 - w + 1), self.rnd.randint(y0, y1 - h + 1)
                walk = kind in ('crack', 'spark')
                if walk:
                    if not self.isF(x, y) or (x, y) in self.over or (x, y) in self.terrace_rows() or (x, y) in keep:
                        continue
                elif not self.free(x, y, w, h, keep, 1 if kind != 'stoneL' else 2):
                    continue
                if kind in ('crys', 'crysL') and not any(not self.isF(x + a, y - b) for a in range(w) for b in (1, 2)):
                    continue                        # kristallen groeien tegen een wand
                if kind == 'stoneL':
                    self.stone(x, y, self.rnd.choice(('stoneL', 'stoneL_f')))
                elif kind == 'stone':
                    self.stone(x, y)
                elif kind == 'crysL':
                    for i, m in enumerate(ID['crysL']):
                        self.set(x + i % 2, y + i // 2, m, 1); self.blocked_decor.add((x + i % 2, y + i // 2))
                elif kind == 'pebble':
                    self.one(x, y, self.rnd.choice(('pebble1', 'pebble2')))
                elif kind == 'crys':
                    self.one(x, y, self.rnd.choice(('crys1', 'crys2')))
                elif kind == 'shard':
                    self.shard(x, y)
                elif kind == 'scrap':
                    self.one(x, y, 'scrap')
                elif kind == 'crack':
                    self.one(x, y, self.rnd.choice(('crack1', 'crack2', 'crack3')), False)
                else:
                    self.one(x, y, self.rnd.choice(('spark1', 'spark2')), False)
                n -= 1

    # ---------------------------------------------------------------- opbouw
    def build(self):
        g = super().build()
        dark = {mf.LIP_N: 'lipD', mf.EDGE_E: 'edgeED', mf.EDGE_W: 'edgeWD'}
        for y in range(self.H):
            for x in range(self.W):
                if self.k[y][x] != 'R' or (x, y) in self.over:
                    continue
                v = g[y][x] & 0x3FF
                if v in dark:
                    g[y][x] = cell(ID[dark[v]][0], 1, 0)
                elif v == mf.ROCK:
                    g[y][x] = cell(ID['rockD'][0], 1, 0)
                elif v == mf.LIP_S1:
                    up = y > 0 and self.k[y - 1][x] in 'FW'
                    g[y][x] = cell(ID['rimSD' if up else 'rockD'][0], 1, 0)
        for y in range(self.H):
            for x in range(self.W):
                if self.k[y][x] == 'R' and (x, y) not in self.over and not any(
                        self.isF(x + a, y + b) for a in range(-3, 4) for b in range(-3, 4)):
                    g[y][x] = cell(ID['rockD'][0], 1, 0)
        return g

    def steps(self):
        for x0, x1, ys, stairs in self.terraces:
            assert all(x0 <= s <= x1 for s in stairs)
            self.step(x0, x1, ys, stairs=stairs)

    def ladder(self, x, y):
        self.set(x, y, mf.LADDER, 0)


def keep_paths(g, pts, extra=()):
    """Looproutes tussen alle sleutelplekken (op de echte botsing, dus via de trappen), 1 tegel verbreed."""
    keep = set(extra)
    start = pts[0]
    for p in pts[1:]:
        prev = {start: None}
        q = [start]
        while q:
            nq = []
            for c in q:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = (c[0] + dx, c[1] + dy)
                    if n in prev or not (0 <= n[0] < len(g[0]) and 0 <= n[1] < len(g)):
                        continue
                    if g[n[1]][n[0]] & 0xC00 and n != p:
                        continue
                    prev[n] = c; nq.append(n)
            q = nq
            if p in prev:
                break
        assert p in prev, ('geen route', start, p)
        c = p
        while c is not None:
            keep |= {(c[0] + a, c[1] + b) for a in (-1, 0, 1) for b in (-1, 0, 1)}
            c = prev[c]
    return keep


def sight(xy, face, n):
    dx, dy = {'DOWN': (0, 1), 'UP': (0, -1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}[face]
    return {(xy[0] + dx * k, xy[1] + dy * k) for k in range(0, n + 1)}


def stones_ok(m, keep, first=0):
    for (x, y, n) in m.stones[first:]:
        for dx in range(n):
            for dy in range(n):
                assert m.k[y + dy][x + dx] == 'F', ('steen op rots', x, y)
                assert (x + dx, y + dy) not in keep, ('steen op een event', x, y)


def item_spot(m, g, target, taken):
    """Dichtstbijzijnde vrije vloertegel (niet op decor/terras/trap) bij target."""
    best = None
    tr = m.terrace_rows()
    for y in range(m.H):
        for x in range(m.W):
            p = (x, y)
            if g[y][x] & 0xC00 or p in m.over or p in taken or p in tr or m.k[y][x] != 'F':
                continue
            d = (x - target[0]) ** 2 + (y - target[1]) ** 2
            if best is None or d < best[0]:
                best = (d, p)
    return best[1]


def wall_spot(m, target):
    """Wandtegel (rots) direct boven een vloertegel, dichtst bij target (voor een bord)."""
    best = None
    for y in range(1, m.H - 1):
        for x in range(m.W):
            if m.k[y][x] == 'R' and m.k[y + 1][x] == 'F' and (x, y + 1) not in m.over and (x, y) not in m.over:
                d = (x - target[0]) ** 2 + (y - target[1]) ** 2
                if best is None or d < best[0]:
                    best = (d, (x, y))
    return best[1]


EV = {F1: {}, B1: {}, B2: {}}     # opgeloste plekken (items, borden) per kaart


def place_items(name, m, g, wanted, taken):
    """wanted: [(doel, item, flag, aantal, verborgen)] -> EV[name]['items']"""
    out = []
    for tgt, it, fl, q, hid in wanted:
        p = item_spot(m, g, tgt, taken)
        taken |= {p}
        out.append((p, it, fl, q, hid))
    EV[name]['items'] = out
    return {p for p, *_ in out}


def new_items(name, targets):
    import nieuwe_items as ni
    return [(targets[it], it, fl, q, hid) for fl, it, q, hid in ni.items(name)]


# --------------------------------------------------------------------- 1F
F1_EXIT = (11, 34)           # zuiduitgang = terug naar de Spacetime Cave (warp 0)
F1_LADDER = (42, 30)         # ladder naar B1F (warp 1)
F1_BOULDER = (21, 30)
F1_TRAINER = (16, 12)
F1_ITEMS = [((7, 7), 'ITEM_THUNDER_STONE', 'FLAG_ITEM_CHARGESTONE_1F_THUNDER_STONE', 1, False),
            ((28, 32), 'ITEM_MAX_REVIVE', 'FLAG_ITEM_CHARGESTONE_1F_MAX_REVIVE', 1, False),
            ((44, 6), 'ITEM_CELL_BATTERY', 'FLAG_HIDDEN_ITEM_CHARGESTONE_1F_CELL_BATTERY', 1, True)]
F1_NEW = {'ITEM_FAST_BALL': (45, 26), 'ITEM_POWER_LENS': (24, 6)}
F1_SIGN = (12, 26)


def build_1f():
    m = Cave(50, 40, 7101)
    # ingangshal (zuid) + gang omhoog
    m.lobes(5, 26, 18, 33, 'h')
    m.path([(9.5, 15), (8.5, 20), (10, 26)])
    # grote hal met een terras (bovenste deel: Thunder Stone, Power Lens)
    m.lobes(4, 4, 26, 17, 'g', 9)
    # gang oost, oostkamer boven (terras), gang omlaag, oostkamer onder (ladder)
    m.path([(25, 6), (30, 6.5), (36, 6)], 1.5)
    m.lobes(35, 4, 46, 17, 'o')
    m.path([(41, 17), (40.5, 20.5), (41.5, 24)])
    m.lobes(35, 24, 46, 32, 'u')
    # zijgrot achter de duwsteen: rechte gang van 3 met rots erboven en eronder
    m.lobes(25, 27, 30, 33, 'z', 4)
    m.freeze(19, 29, 24, 31, 'F'); m.freeze(19, 26, 24, 28, 'R'); m.freeze(19, 32, 24, 35, 'R')
    m.freeze(10, 32, 12, 34, 'F'); m.freeze(8, 35, 14, 39, 'R')
    m.shape()
    m.terrace(4, 25, 10, 19)
    m.terrace(35, 45, 10, 41)
    m.shape()
    m.build()
    m.steps()
    m.exit_south(*F1_EXIT)
    m.ladder(*F1_LADDER)
    m.shard(21, 29); m.shard(21, 31)                 # de duwsteen houdt de zijgrot dicht
    g = m.build()
    taken = {F1_EXIT, F1_LADDER, F1_BOULDER, F1_TRAINER}
    sign_xy = wall_spot(m, F1_SIGN)
    EV[F1]['sign'] = sign_xy
    ip = place_items(F1, m, g, F1_ITEMS + new_items(F1, F1_NEW), taken)
    pts = [(F1_EXIT[0], F1_EXIT[1] - 1), (F1_LADDER[0], F1_LADDER[1] - 1), (20, 30), F1_TRAINER,
           (sign_xy[0], sign_xy[1] + 1)] + sorted(ip - {EV[F1]['items'][1][0]})
    keep = keep_paths(g, pts, sight(F1_TRAINER, 'DOWN', 3) | {(x, 30) for x in range(17, 30)} | ip |
                      {(x, y) for x in range(24, 31) for y in range(28, 33)})
    m.decorate(keep, [('stoneL', 3), ('crysL', 3), ('stone', 11), ('crys', 10), ('pebble', 9), ('shard', 6),
                      ('scrap', 2), ('crack', 18), ('spark', 14)])
    stones_ok(m, keep)
    return m, m.build()


# --------------------------------------------------------------------- B1F
B1_ARRIVE = (12, 36)         # ladder omhoog (warp 0) = waar je vanuit 1F aankomt
B1_LADDER = (12, 8)          # ladder naar B2F (warp 1), achter het stenenhek
B1_FENCE_Y = 13              # hek: stenen op rij 12-13, gaten met duwstenen
B1_BOULDERS = [(9, 13), (17, 13)]
B1_TRAINERS = [(19, 18), (44, 30)]   # westhal (kijkt naar links), grote grot
B1_ITEMS = [((46, 6), 'ITEM_MAGNET', 'FLAG_ITEM_CHARGESTONE_B1F_MAGNET', 1, False),
            ((7, 7), 'ITEM_METAL_COAT', 'FLAG_ITEM_CHARGESTONE_B1F_METAL_COAT', 1, False),
            ((38, 40), 'ITEM_BIG_NUGGET', 'FLAG_HIDDEN_ITEM_CHARGESTONE_B1F_BIG_NUGGET', 1, True)]
B1_NEW = {'ITEM_EJECT_PACK': (32, 7), 'ITEM_TERRAIN_EXTENDER': (47, 38)}


def build_b1f():
    m = Cave(54, 46, 7202)
    m.lobes(5, 31, 20, 41, 'a', 7)
    m.path([(14.5, 32.5), (15.5, 27), (14, 21)])
    m.lobes(5, 16, 22, 22, 'w1')
    m.lobes(5, 3, 22, 10, 'w3')
    m.freeze(5, 10, 22, 15, 'F'); m.freeze(2, 3, 4, 16, 'R'); m.freeze(23, 3, 26, 23, 'R')
    m.path([(19.5, 35), (25, 34), (31, 32)])
    m.lobes(30, 25, 49, 41, 'c', 9)
    m.path([(43, 26), (43.5, 20), (42, 15)])
    m.lobes(28, 4, 49, 14, 'n', 8)
    m.shape()
    m.terrace(31, 48, 35, 36)
    m.terrace(29, 48, 10, 40)
    m.shape()
    m.build()
    m.steps()
    m.ladder(*B1_ARRIVE)
    m.ladder(*B1_LADDER)
    # hek van zwevende stenen (rij 12-13) over de hele westhal, met twee gaten (duwstenen)
    gaps = {x for x, _ in B1_BOULDERS}
    x = 5
    while x <= 22:
        if x in gaps:
            x += 1
            continue
        if x + 1 <= 22 and x + 1 not in gaps:
            m.stone(x, B1_FENCE_Y - 1); x += 2
        else:
            m.shard(x, B1_FENCE_Y); m.shard(x, B1_FENCE_Y - 1); x += 1
    fence = len(m.stones)
    g = m.build()
    taken = {B1_ARRIVE, B1_LADDER} | set(B1_TRAINERS) | set(B1_BOULDERS)
    ip = place_items(B1, m, g, B1_ITEMS + new_items(B1, B1_NEW), taken)
    extra = sight(B1_TRAINERS[0], 'LEFT', 4) | sight(B1_TRAINERS[1], 'DOWN', 4) | ip
    for (bx, by) in B1_BOULDERS:
        extra |= {(bx, by + 1), (bx, by - 1), (bx, by - 2), (bx, by - 3), (bx, by + 2), (bx, by + 3)}
    extra |= {(x, y) for x in range(5, 23) for y in range(10, 16)}
    pts = [(B1_ARRIVE[0], B1_ARRIVE[1] - 1), (9, 15), (17, 15), (B1_TRAINERS[0][0] - 1, B1_TRAINERS[0][1]),
           (B1_TRAINERS[1][0], B1_TRAINERS[1][1] + 1)] + sorted(p for p in ip if p[1] > 15)
    keep = keep_paths(g, pts, extra)
    # boven het hek (alleen na het duwen bereikbaar): eigen routes
    keep |= keep_paths(g, [(9, 10)] + [p for p in ip if p[1] < 12] + [(B1_LADDER[0], B1_LADDER[1] + 1)], set())
    m.decorate(keep, [('stoneL', 4), ('crysL', 4), ('stone', 14), ('crys', 12), ('pebble', 10), ('shard', 6),
                      ('scrap', 3), ('crack', 22), ('spark', 16)])
    stones_ok(m, keep, fence)
    return m, m.build()


# --------------------------------------------------------------------- B2F
B2_ARRIVE = (10, 33)         # ladder omhoog (warp 0)
B2_COLRESS = (25, 10)
B2_MACHINE = (24, 7)         # Colress' machine (2x2) met een bord op de onderste rij
B2_ZERAORA = (25, 5)         # verschijnt achter de machine, achterin de hal
B2_TRAINERS = [(30, 27)]
B2_ITEMS = [((38, 33), 'ITEM_ELECTIRIZER', 'FLAG_ITEM_CHARGESTONE_B2F_ELECTIRIZER', 1, False),
            ((11, 6), 'ITEM_PP_MAX', 'FLAG_ITEM_CHARGESTONE_B2F_PP_MAX', 1, False)]
B2_NEW = {'ITEM_ABILITY_SHIELD': (38, 6), 'ITEM_EXP_CANDY_XL': (36, 21)}


def build_b2f():
    m = Cave(46, 40, 7303)
    m.lobes(5, 27, 19, 36, 'a')
    m.path([(17, 31.5), (22, 33), (27.5, 31.5)])
    m.lobes(26, 20, 42, 36, 'm', 8)
    m.path([(33.5, 22), (34, 17.5), (32.5, 13.5)])
    m.lobes(8, 3, 41, 13, 'l', 10)
    m.freeze(21, 4, 29, 12, 'F')
    m.shape()
    m.terrace(27, 41, 25, 35)
    m.shape()
    m.build()
    m.steps()
    m.ladder(*B2_ARRIVE)
    # het lab: Colress' machine tapt de stroom af van twee spoelen en twee grote stenen (kabels over de vloer)
    for i, mt in enumerate(ID['machine']):
        m.set(B2_MACHINE[0] + i % 2, B2_MACHINE[1] + i // 2, mt, 1)
        m.blocked_decor.add((B2_MACHINE[0] + i % 2, B2_MACHINE[1] + i // 2))
    m.one(20, 8, 'coil'); m.one(29, 8, 'coil')
    m.cable([(23, 8), (22, 8), (21, 8)])
    m.cable([(26, 8), (27, 8), (28, 8)])
    m.stone(14, 7, 'stoneL'); m.stone(33, 7, 'stoneL_f')
    m.cable([(19, 8), (18, 8), (17, 8)])
    m.cable([(30, 8), (31, 8), (32, 8)])
    m.one(22, 5, 'console'); m.one(28, 5, 'console')
    m.one(19, 11, 'scrap'); m.one(31, 11, 'scrap')
    fixed = len(m.stones)
    g = m.build()
    taken = {B2_ARRIVE, B2_COLRESS, B2_ZERAORA} | set(B2_TRAINERS)
    ip = place_items(B2, m, g, B2_ITEMS + new_items(B2, B2_NEW), taken)
    extra = sight(B2_TRAINERS[0], 'DOWN', 4) | ip | {(x, y) for x in range(21, 30) for y in range(4, 13)}
    pts = [(B2_ARRIVE[0], B2_ARRIVE[1] - 1), (B2_COLRESS[0], B2_COLRESS[1] + 1), (B2_ZERAORA[0] - 1, B2_ZERAORA[1]),
           (B2_TRAINERS[0][0], B2_TRAINERS[0][1] + 1)] + sorted(ip)
    keep = keep_paths(g, pts, extra)
    m.decorate(keep, [('stoneL', 2), ('crysL', 3), ('stone', 9), ('crys', 10), ('pebble', 8), ('shard', 5),
                      ('scrap', 4), ('crack', 18), ('spark', 12)])
    stones_ok(m, keep, fixed)
    return m, m.build()


# ====================================================================== registratie
def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"%s": [' % GROUP); j = g.index('\n  ]', i)
        body = g[i:j]
        sep = ',' if body.rstrip().endswith('"') else ''
        g = g[:j] + sep + '\n    "%s"' % name + g[j:]
    d = json.loads(g)
    assert len(d[GROUP]) <= 128
    open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/SpacetimeCave/scripts.inc"\n'
        if anchor not in es:
            anchor = '\t.include "data/maps/MangroveMire/scripts.inc"\n'
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def save(name, g):
    W, H = len(g[0]), len(g)
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', t) for r in g for t in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack("<4H", *([cell(ID["rockD"][0], 1, 0)] * 4)))
    bd.register_layout(name, CONST[name], W, H, PRIM, SEC)


def write_map(name, objs, warps, bgs, coords=(), head=None):
    m = {'id': 'MAP_' + CONST[name], 'name': name, 'layout': 'LAYOUT_' + CONST[name], 'music': MUSIC,
         'region_map_section': 'MAPSEC_CHARGESTONE_CAVE', 'requires_flash': False, 'weather': 'WEATHER_NONE',
         'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': True, 'allow_running': True,
         'show_map_name': name == F1, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
         'object_events': objs, 'warp_events': warps, 'coord_events': list(coords), 'bg_events': bgs}
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    register_map(name)


warp, obj, tr, ball, sign = bd.warp, bd.obj, bd.tr, bd.ball, bd.sign


def hidden(xy, it, flag, q=1):
    h = {'type': 'hidden_item', 'x': xy[0], 'y': xy[1], 'elevation': 3, 'item': it, 'flag': flag}
    if q > 1:
        h['quantity'] = q
    return h


def items_ev(name):
    objs, bgs = [], []
    for p, it, fl, q, hid in EV[name]['items']:
        if hid:
            bgs.append(hidden(p, it, fl, q))
        else:
            o = ball(p[0], p[1], it, fl)
            if q > 1:
                o['movement_range_x'] = q
            objs.append(o)
    return objs, bgs


def boulder(x, y):
    return obj('OBJ_EVENT_GFX_PUSHABLE_BOULDER', x, y, 'EventScript_StrengthBoulder', '0', 'MOVEMENT_TYPE_LOOK_AROUND')


def render(name, out):
    H = len(MAPS[name][1])
    subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', name, out, '0', str(H)], check=True)


MAPS = {}


def build_maps():
    for name, fn in ((F1, build_1f), (B1, build_b1f), (B2, build_b2f)):
        m, g = fn()
        MAPS[name] = (m, g)
        save(name, g)


# ====================================================================== trainers (1124-1128)
mon, AI, AI_BOSS = bd.mon, bd.AI, bd.AI_BOSS
TRAINERS = [  # (sleutel, id, naam, klasse, pic, gender, music, ai, mugshot, team, waarom)
    ('CHARGESTONE_GRUNT_1F', 1124, 'GRUNT', 'Neo Plasma', 'Neo Plasma Grunt M', 'Male', 'Suspicious', AI, None, [
        mon('Klinklang', 66, ['Gear Grind', 'Wild Charge', 'Shift Gear', 'Screech']),
        mon('Eelektross', 66, ['Wild Charge', 'Crunch', 'Drain Punch', 'Flamethrower']),
        mon('Galvantula', 66, ['Thunder', 'Bug Buzz', 'Sticky Web', 'Energy Ball'])],
     'Chargestone Cave 1F, Colress-assistent'),
    ('CHARGESTONE_GRUNT_B1F_1', 1125, 'GRUNT', 'Neo Plasma', 'Neo Plasma Grunt F', 'Female', 'Suspicious', AI, None, [
        mon('Rotom_Wash', 67, ['Hydro Pump', 'Thunderbolt', 'Will-O-Wisp', 'Volt Switch']),
        mon('Heliolisk', 67, ['Parabolic Charge', 'Grass Knot', 'Surf', 'Volt Switch']),
        mon('Ferrothorn', 67, ['Power Whip', 'Gyro Ball', 'Leech Seed', 'Spikes'])],
     'Chargestone Cave B1F, Colress-assistent bij het stenenhek'),
    ('CHARGESTONE_GRUNT_B1F_2', 1126, 'GRUNT', 'Neo Plasma', 'Neo Plasma Grunt M', 'Male', 'Suspicious', AI, None, [
        mon('Kingambit', 68, ['Kowtow Cleave', 'Iron Head', 'Sucker Punch', 'Swords Dance']),
        mon('Magnezone', 68, ['Thunderbolt', 'Flash Cannon', 'Volt Switch', 'Mirror Coat']),
        mon('Golurk', 68, ['Earthquake', 'Shadow Punch', 'Dynamic Punch', 'Ice Punch'])],
     'Chargestone Cave B1F, Colress-assistent in de grote grot'),
    ('CHARGESTONE_GRUNT_B2F', 1127, 'GRUNT', 'Neo Plasma', 'Neo Plasma Grunt F', 'Female', 'Suspicious', AI, None, [
        mon('Electivire', 69, ['Wild Charge', 'Ice Punch', 'Cross Chop', 'Earthquake']),
        mon('Probopass', 69, ['Power Gem', 'Flash Cannon', 'Earth Power', 'Thunder Wave']),
        mon('Bronzong', 69, ['Gyro Ball', 'Earthquake', 'Trick Room', 'Psychic']),
        mon('Vikavolt', 70, ['Bug Buzz', 'Thunderbolt', 'Energy Ball', 'Sticky Web'])],
     'Chargestone Cave B2F, Colress-assistent voor het lab'),
    ('CHARGESTONE_COLRESS', 1128, 'COLRESS', 'Scientist', 'Colress', 'Male', 'Intense', AI_BOSS, 'Blue', [
        mon('Rotom_Heat', 72, ['Overheat', 'Thunderbolt', 'Will-O-Wisp', 'Volt Switch']),
        mon('Porygon_Z', 73, ['Tri Attack', 'Thunderbolt', 'Ice Beam', 'Nasty Plot']),
        mon('Metagross', 73, ['Meteor Mash', 'Zen Headbutt', 'Earthquake', 'Bullet Punch']),
        mon('Copperajah', 73, ['Iron Head', 'Heavy Slam', 'Earthquake', 'Play Rough']),
        mon('Archaludon', 74, ['Electro Shot', 'Flash Cannon', 'Draco Meteor', 'Body Press']),
        mon('Genesect @ Douse Drive', 75, ['Techno Blast', 'U-turn', 'Iron Head', 'Shift Gear'])],
     'Chargestone Cave B2F, COLRESS uit een andere dimensie (hier wel evil)'),
]


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = '// chargestone { (tools/grounded/maptools/chargestone.py; id 1124-1128)\n'
    for key, n, *_, why in TRAINERS:
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (key, n, why)
    blk += '// }'
    if '// chargestone {' in s:
        i = s.index('// chargestone {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for key, n, *_ in TRAINERS:
        hits = re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)
        assert len(hits) == 1, ('trainer-id dubbel', n, hits)
    open(p, 'w').write(s)
    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- chargestone (tools/grounded/maptools/chargestone.py) --- */\n\n'
    for key, n, nm, cls, pic, gender, music, ai, mug, team, why in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music,
               'Double Battle: No', ai] + (['Mugshot: ' + mug] if mug else [])
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (key, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde chargestone --- */'
    s = bd.replace_block(s, '/* --- chargestone', '/* --- einde chargestone --- */', blk)
    open(p, 'w').write(s)


# ====================================================================== wilde Pokemon
WILD = {
    'CHARGESTONE_CAVE_1F': dict(land=(8, [
        ('GALVANTULA', 60, 62), ('BOLDORE', 60, 62), ('KLINKLANG', 60, 62), ('EELEKTRIK', 60, 62),
        ('FERROTHORN', 60, 62), ('MAGNETON', 60, 62), ('DURANT', 61, 63), ('ZEBSTRIKA', 61, 63),
        ('EMOLGA', 61, 63), ('BRONZONG', 61, 63), ('PROBOPASS', 62, 63), ('ROTOM', 62, 63)])),
    'CHARGESTONE_CAVE_B1F': dict(land=(8, [
        ('GALVANTULA', 62, 64), ('GIGALITH', 62, 64), ('EELEKTRIK', 62, 64), ('KLINKLANG', 62, 64),
        ('MAGNETON', 62, 64), ('HELIOLISK', 62, 64), ('CARBINK', 63, 65), ('EXCADRILL', 63, 65),
        ('ESCAVALIER', 63, 65), ('FERROTHORN', 63, 65), ('EELEKTROSS', 64, 65), ('TOGEDEMARU', 64, 65)])),
    'CHARGESTONE_CAVE_B2F': dict(land=(8, [
        ('GALVANTULA', 64, 66), ('GIGALITH', 64, 66), ('EELEKTRIK', 64, 66), ('MAGNETON', 64, 66),
        ('BRONZONG', 64, 66), ('EXCADRILL', 64, 66), ('BISHARP', 65, 67), ('PROBOPASS', 65, 67),
        ('VIKAVOLT', 65, 67), ('GOLURK', 65, 67), ('EELEKTROSS', 66, 67), ('ROTOM', 66, 67)])),
}


def wild():
    for mp, tabs in WILD.items():
        assert len({x[0] for x in tabs['land'][1]}) == 12, mp
    bd.WILD = WILD
    bd.wild()


# ====================================================================== mapsec, evolutie, gevechtsstart
def mapsecs():
    bd.MAPSECS[:] = [('MAPSEC_CHARGESTONE_CAVE', 'CHARGESTONE CAVE', 26, 4, 1, 1, 'MAPPOPUP_THEME_STONE',
                      'Chargestone Cave (Spacetime)')]
    bd.mapsecs()


EVOS = [('src/data/pokemon/species_info/gen_1_families.h', 'SPECIES_MAGNEZONE'),
        ('src/data/pokemon/species_info/gen_7_families.h', 'SPECIES_VIKAVOLT')]


def evolutions():
    """Magnetisch veld: Magneton en Charjabug evolueren ook door een level-up in Chargestone Cave.
    (Nosepass evolueert in dit project al gewoon op lv 30.)"""
    for p, sp in EVOS:
        s = open(p).read()
        old = '{EVO_LEVEL, 0, %s, CONDITIONS({IF_IN_MAPSEC, MAPSEC_NEW_MAUVILLE})},' % sp
        add = ('\n                                {EVO_LEVEL, 0, %s, CONDITIONS({IF_IN_MAPSEC, MAPSEC_CHARGESTONE_CAVE})}, '
               '// Project Grounded: magnetisch veld (chargestone.py)' % sp)
        assert old in s
        if old + add not in s:
            s = s.replace(old, old + add, 1)
        open(p, 'w').write(s)


def battle_setup():
    p = 'src/battle_setup.c'
    s = open(p).read()
    if 'case SPECIES_ZERAORA' not in s:
        a = '    case SPECIES_VOLCANION:'
        assert a in s
        s = s.replace(a, '    case SPECIES_ZERAORA: // Project Grounded: Chargestone Cave (placeholder: Kanto-legendary-thema, '
                         'bestaande transitie)\n        CreateBattleStartTask(B_TRANSITION_ANGLED_WIPES, MUS_RG_VS_LEGEND);\n'
                         '        break;\n' + a, 1)
        open(p, 'w').write(s)


# ====================================================================== events en scripts
def tr_obj(gfx, xy, face, sight, script):
    return bd.tr(gfx, xy[0], xy[1], script, face, sight)


def head(name, scripts=()):
    h = '@ Project Grounded: %s (tools/grounded/maptools/chargestone.py)\n%s_MapScripts::\n' % (name, name)
    for kind, lbl in scripts:
        h += '\tmap_script %s, %s\n' % (kind, lbl)
    return h + '\t.byte 0\n'


HUB_DEST = ('SPACETIME_CAVE', 7)   # warp-index van de Chargestone-scheur in de hub (spacetime_cave.py)


def events():
    # ---------------------------------------------------------------- 1F
    S = Scr(F1, head(F1))
    g1 = S.trainer('Grunt', 'CHARGESTONE_GRUNT_1F',
                   "Halt! This cave is property of TEAM PLASMA's research division.\n\n"
                   "Which is one man. And us. We're the division's legs.",
                   "My legs have been defeated.",
                   "COLRESS? Nice? Who told you that?\n\nThe man once fired an intern for saying 'good morning' "
                   "without a hypothesis.")
    S.npc('Plaque', "CHARGESTONE CAVE\n\nThe stones float because of magnetism. Do not lick the stones.\n\n"
          "Someone has added in marker: 'the stones float because of ZERAORA. Lick at own risk.'", 'MSGBOX_SIGN')
    S.write()
    objs = [tr_obj('OBJ_EVENT_GFX_NEO_PLASMA_GRUNT_M', F1_TRAINER, 'DOWN', 3, g1)]
    io, ib = items_ev(F1)
    objs += io + [boulder(*F1_BOULDER)]
    warps = [warp(F1_EXIT[0], F1_EXIT[1], HUB_DEST[0], HUB_DEST[1], elev=3),
             warp(F1_LADDER[0], F1_LADDER[1], CONST[B1], 0, elev=3)]
    bgs = [sign(EV[F1]['sign'][0], EV[F1]['sign'][1], S.P + 'Plaque', 'BG_EVENT_PLAYER_FACING_NORTH')] + ib
    write_map(F1, objs, warps, bgs)
    # ---------------------------------------------------------------- B1F
    S = Scr(B1, head(B1))
    a = S.trainer('GruntFence', 'CHARGESTONE_GRUNT_B1F_1',
                  "You found the fence! We built it out of floating rocks. Very modern.\n\n"
                  "It's also the only fence in the world you can push over. We're working on that.",
                  "The fence was a metaphor anyway.",
                  "Push the stones in the gaps. Or don't. I'm not your supervisor. My supervisor is evil.")
    b = S.trainer('GruntCavern', 'CHARGESTONE_GRUNT_B1F_2',
                  "Every rock in here hums at fifty hertz. So do I, after three weeks of overtime.",
                  "Bzzt. That's me, short-circuiting emotionally.",
                  "COLRESS says the cave runs on a ZERAORA now. I asked what it ran on before.\n\n"
                  "He said 'ignorance' and docked my pay.")
    S.write()
    objs = [tr_obj('OBJ_EVENT_GFX_NEO_PLASMA_GRUNT_F', B1_TRAINERS[0], 'LEFT', 4, a),
            tr_obj('OBJ_EVENT_GFX_NEO_PLASMA_GRUNT_M', B1_TRAINERS[1], 'DOWN', 4, b)]
    io, ib = items_ev(B1)
    objs += io + [boulder(*xy) for xy in B1_BOULDERS]
    warps = [warp(B1_ARRIVE[0], B1_ARRIVE[1], CONST[F1], 1, elev=3),
             warp(B1_LADDER[0], B1_LADDER[1], CONST[B2], 0, elev=3)]
    write_map(B1, objs, warps, ib)
    # ---------------------------------------------------------------- B2F
    S = Scr(B2, head(B2, [('MAP_SCRIPT_ON_TRANSITION', B2 + '_OnTransition')]))
    P, T = S.P, S.T
    c = S.trainer('Grunt', 'CHARGESTONE_GRUNT_B2F',
                  "The lab is through here. Please wipe your feet. The floor is load-bearing AND current-bearing.",
                  "My shoes are smoking. That's new.",
                  "When the machine is on, ZERAORA screams at a frequency only POKéMON can hear.\n\n"
                  "We wear earplugs anyway. Solidarity.")
    S.npc('Machine', "A floating stone wired to a laptop. The screen reads:\n\n"
          "ZERAORA OUTPUT: 98%.\nZERAORA MOOD: no.\nETHICS MODULE: not found.", 'MSGBOX_SIGN')
    S.raw(f"""{B2}_OnTransition:
	setflag FLAG_HIDE_CHARGESTONE_ZERAORA
	goto_if_set FLAG_SPACETIME_CHARGESTONE_DONE, {P}OnTransitionEnd
	goto_if_not_defeated TRAINER_CHARGESTONE_COLRESS, {P}OnTransitionEnd
	clearflag FLAG_HIDE_CHARGESTONE_ZERAORA
{P}OnTransitionEnd:
	end

{P}Colress::
	lock
	faceplayer
	goto_if_defeated TRAINER_CHARGESTONE_COLRESS, {P}ColressAfter
	msgbox {T}ColressIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_CHARGESTONE_COLRESS, {T}ColressDefeat
	msgbox {T}ColressShutdown, MSGBOX_DEFAULT
	closemessage
	playse SE_THUNDER
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 10
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	special SpawnCameraObject
	applymovement OBJ_EVENT_ID_CAMERA, {P}Movement_CameraUp
	waitmovement 0
	clearflag FLAG_HIDE_CHARGESTONE_ZERAORA
	addobject LOCALID_CHARGESTONE_ZERAORA
	playse SE_M_THUNDERBOLT
	playmoncry SPECIES_ZERAORA, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox {T}ZeraoraFree, MSGBOX_DEFAULT
	closemessage
	applymovement OBJ_EVENT_ID_CAMERA, {P}Movement_CameraDown
	waitmovement 0
	special RemoveCameraObject
	release
	end

{P}Movement_CameraUp:
	walk_slow_up
	walk_slow_up
	walk_slow_up
	step_end

{P}Movement_CameraDown:
	walk_down
	walk_down
	walk_down
	step_end

{P}ColressAfter::
	goto_if_set FLAG_SPACETIME_CHARGESTONE_DONE, {P}ColressDone
	msgbox {T}ColressAfter, MSGBOX_DEFAULT
	release
	end

{P}ColressDone::
	msgbox {T}ColressDone, MSGBOX_DEFAULT
	release
	end

{P}Zeraora::
	lock
	faceplayer
	playmoncry SPECIES_ZERAORA, CRY_MODE_ENCOUNTER
	msgbox {T}Zeraora, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_ZERAORA, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}ZeraoraStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}ZeraoraStays
	removeobject LOCALID_CHARGESTONE_ZERAORA
	setflag FLAG_HIDE_CHARGESTONE_ZERAORA
	setflag FLAG_SPACETIME_CHARGESTONE_DONE
	msgbox {T}CaveCalm, MSGBOX_DEFAULT
{P}ZeraoraStays::
	release
	end
""", [('ColressIntro', "COLRESS: ...Why are you looking at me like that? Do I know you?\n\n"
                           "...I'm not evil? Where on earth did you hear that?\n\n"
                           "Parallel dimensions. While I do not dispute the possibility, it doesn't change my "
                           "current standing.\n\n"
                           "Here, I am evil, and I am very good at it. My machine drains ZERAORA's current into "
                           "the cave. The rocks float. The lights stay on. ZERAORA has some notes.\n\n"
                           "You came all this way to switch it off? Wonderful. A control group!"),
          ('ColressDefeat', "Fascinating. You reduced my output by exactly one hundred percent."),
          ('ColressShutdown', "COLRESS: The machine is overloading. It appears it relied on my POKéMON "
                              "not losing.\n\nA design flaw. I'll fix it in the next dimension.\n\n"
                              "Ah. And there goes the battery."),
          ('ZeraoraFree', "The floating stones drop a few inches all at once.\n\n"
                          "Something at the back of the lab stretches, crackles, and turns to look at you."),
          ('ColressAfter', "COLRESS: Go on, then. It's free, it's furious, and it is standing right behind my "
                           "machine.\n\nI'd love the data. Try not to become part of it."),
          ('ColressDone', "COLRESS: The cave runs on plain old magnetism again. Dreadfully natural.\n\n"
                          "In your dimension I'm the nice one? Tell him he's wasting his potential."),
          ('Zeraora', "ZERAORA: Grrrah!\n\nIts fur is standing on end. So is yours."),
          ('CaveCalm', "The hum in the walls fades to a gentle buzz.\n\nCHARGESTONE CAVE runs on its own "
                       "again.")])
    S.write()
    objs = [tr_obj('OBJ_EVENT_GFX_NEO_PLASMA_GRUNT_F', B2_TRAINERS[0], 'DOWN', 4, c),
            obj('OBJ_EVENT_GFX_COLRESS', B2_COLRESS[0], B2_COLRESS[1], P + 'Colress', 'FLAG_HIDE_CHARGESTONE_COLRESS',
                move='MOVEMENT_TYPE_FACE_UP', local_id='LOCALID_CHARGESTONE_COLRESS'),
            obj('OBJ_EVENT_GFX_SPECIES(ZERAORA)', B2_ZERAORA[0], B2_ZERAORA[1], P + 'Zeraora',
                'FLAG_HIDE_CHARGESTONE_ZERAORA', move='MOVEMENT_TYPE_FACE_DOWN', local_id='LOCALID_CHARGESTONE_ZERAORA')]
    io, ib = items_ev(B2)
    objs += io
    warps = [warp(B2_ARRIVE[0], B2_ARRIVE[1], CONST[B1], 1, elev=3)]
    bgs = [sign(B2_MACHINE[0] + dx, B2_MACHINE[1] + 1, P + 'Machine', 'BG_EVENT_PLAYER_FACING_NORTH') for dx in (0, 1)] + ib
    write_map(B2, objs, warps, bgs)


# ====================================================================== controles
FACE = {'DOWN': (0, 1), 'UP': (0, -1), 'LEFT': (-1, 0), 'RIGHT': (1, 0)}


def checks():
    for name in MAPS:
        g = MAPS[name][1]
        d = json.load(open('data/maps/%s/map.json' % name))
        objs = d['object_events']
        start = (d['warp_events'][0]['x'], d['warp_events'][0]['y'])
        solid = {(o['x'], o['y']) for o in objs} - {start}
        boulders = {(o['x'], o['y']) for o in objs if 'BOULDER' in o['graphics_id']}
        r_all = mf.reachable(g, start, solid - boulders)          # duwstenen weg = na het duwen
        for o in objs:
            p = (o['x'], o['y'])
            assert mf.next_to(r_all, *p) or p in r_all, (name, 'object onbereikbaar', o['script'], p)
            if o['trainer_type'] == 'TRAINER_TYPE_NORMAL':
                dx, dy = FACE[o['movement_type'].split('_')[-1]]
                for k in range(1, int(o['trainer_sight_or_berry_tree_id']) + 1):
                    assert (o['x'] + dx * k, o['y'] + dy * k) in r_all, (name, 'zichtlijn', o['script'], k)
        for w in d['warp_events']:
            assert (w['x'], w['y']) in r_all or (w['x'], w['y']) == start, (name, 'warp onbereikbaar', w)
        for b in d['bg_events']:
            p = (b['x'], b['y'])
            assert p in r_all if b['type'] == 'hidden_item' else mf.next_to(r_all, *p), (name, 'bg onbereikbaar', p)
        print(name, 'bereikbaar:', len(r_all), 'tegels')
    # B1F: het hek houdt de ladder dicht; één duw omhoog in een gat opent hem (licht puzzelpad)
    g = MAPS[B1][1]
    d = json.load(open('data/maps/%s/map.json' % B1))
    solid = {(o['x'], o['y']) for o in d['object_events']} - {B1_ARRIVE}
    assert B1_LADDER not in mf.reachable(g, B1_ARRIVE, solid), 'B1F: hek lekt'
    for bx, by in B1_BOULDERS:
        assert (bx, by + 1) in mf.reachable(g, B1_ARRIVE, solid - {(bx, by)}), ('B1F: duwplek', bx)
        moved = (solid - {(bx, by)}) | {(bx, by - 3)}           # drie keer omhoog geduwd
        assert B1_LADDER in mf.reachable(g, B1_ARRIVE, moved), ('B1F: ladder na het duwen', bx)
    g = MAPS[F1][1]
    d = json.load(open('data/maps/%s/map.json' % F1))
    solid = {(o['x'], o['y']) for o in d['object_events']} - {F1_EXIT}
    assert not mf.next_to(mf.reachable(g, F1_EXIT, solid), *EV[F1]['items'][1][0]), '1F: zijgrot lekt'


def overview(dirn):
    from PIL import Image
    ims = [Image.open(os.path.join(dirn, n + '.png')) for n in (F1, B1, B2)]
    o = Image.new('RGB', (sum(i.width for i in ims) + 32, max(i.height for i in ims)), (10, 14, 32))
    x = 0
    for i in ims:
        o.paste(i, (x, 0)); x += i.width + 16
    o.save(os.path.join(dirn, 'overzicht.png'))


def main():
    flags()
    import nieuwe_items as ni
    ni.flags()
    build_maps()
    mapsecs()
    events()
    trainers()
    wild()
    evolutions()
    battle_setup()
    checks()
    if len(sys.argv) > 1:
        for name in MAPS:
            render(name, os.path.join(sys.argv[1], name + '.png'))
        overview(sys.argv[1])


if __name__ == '__main__':
    main()
