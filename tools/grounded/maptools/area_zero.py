"""Project Grounded: Area Zero (Spacetime Cave-sidequest, post-game; Paldea in een andere tijd).

Een krater waar je steeds verder afdaalt (9 okt: elke laag is een kom met ringvormige terrassen, trappen om en om in de
noordwanden, binnenkomst bovenaan op de rand en de uitgang naar de volgende diepte op de bodem in het midden; zie bowl()).
Hoe dieper, hoe vreemder de kleuren (zelfde tiles, andere paletten:
area_zero_tiles.py). Kaarten (gMapGroup_Spacetime, achteraan):
  AreaZero_Rim       laag 1, de kraterwand: groene plateaus, grijze rotswanden, bomen, hoog gras, onderzoeksstation 1.
                     Warp 0 = ladder omhoog = terug naar de Spacetime Cave (hier komt de hub-scheur uit).
  AreaZero_Depths    laag 2: het groen verkleurt, kristallen breken door de rots. SCREAM TAIL en IRON HANDS.
  AreaZero_Crystal   laag 3, de kristalgrot: de Zero Gate met twee kanalen (verleden links, toekomst rechts) en een
                     grotgat dat met kristallen is dichtgegroeid (de Tera-grot).
  AreaZero_Future    toekomst-Area Zero (zelfde vorm als het verleden): Violet-paradoxen, IRON LEAVES, IRON BOULDER,
                     IRON CROWN, MIRAIDON en het beveiligingssysteem (terminal).
  AreaZero_Past      verleden-Area Zero: Scarlet-paradoxen, WALKING WAKE, GOUGING FIRE, RAGING BOLT, KORAIDON en
                     het beveiligingssysteem. De draaikolk in beide tijden wisselt naar dezelfde plek in de andere tijd.
  AreaZero_TeraCave  opent als beide beveiligingssystemen offline zijn: het alarmsysteem (het enige gevecht buiten
                     The Spire waarin de tegenstander terastaliseert, elk teamlid; src/battle_gimmick.c), daarna
                     TERAPAGOS (lv 100). Klaar-flag FLAG_SPACETIME_AREAZERO_DONE.
Paradoxen tellen niet als legendaries: de gewone in de wilde tabellen, de rest als vaste gevechten die terugkomen
zolang ze niet gevangen zijn. Flags FLAG_GROUNDED 920-999 (blok 'area_zero'), trainers 1180-1182.
Teksten zijn placeholders (Jordi herschrijft ze). Idempotent, vaste seeds; controleert de bereikbaarheid.
Gebruik: python3 tools/grounded/maptools/area_zero.py [rendermap]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, math, os, random, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chargestone as cs           # Cave (organische Meteor Falls-autotiler); zet de werkmap op de repo-root
import meteor_falls_ext as mf
import beacon_dragon as bd
import area_zero_tiles as azt

HUB_DEST = ('SPACETIME_CAVE', 11)  # terugweg: de Area Zero-scheur in de hub (warps 11-12, spacetime_cave.py)
GROUP = 'gMapGroup_Spacetime'
RIM, DEP, CRY, FUT, PAS, TERA = ('AreaZero_Rim', 'AreaZero_Depths', 'AreaZero_Crystal', 'AreaZero_Future',
                                 'AreaZero_Past', 'AreaZero_TeraCave')
CONST = {RIM: 'AREA_ZERO_RIM', DEP: 'AREA_ZERO_DEPTHS', CRY: 'AREA_ZERO_CRYSTAL', FUT: 'AREA_ZERO_FUTURE',
         PAS: 'AREA_ZERO_PAST', TERA: 'AREA_ZERO_TERA_CAVE'}
VARIANT = {RIM: 'rim', DEP: 'deep', CRY: 'crystal', FUT: 'future', PAS: 'past', TERA: 'tera'}
MUSIC = {RIM: 'MUS_RG_VICTORY_ROAD', DEP: 'MUS_RG_VICTORY_ROAD', CRY: 'MUS_RG_SEVII_CAVE', FUT: 'MUS_RG_SEVII_DUNGEON',
         PAS: 'MUS_RG_SEVII_DUNGEON', TERA: 'MUS_SEALED_CHAMBER'}
ID = {}
E = mf.E_FLOOR
cell = mf.cell


def tileset_syms(name):
    v = VARIANT[name]
    return 'gTileset_' + azt.sym(v, True), 'gTileset_' + azt.sym(v)


# ====================================================================== kaart-bouwer
class AZ(cs.Cave):
    """chargestone.Cave met Area Zero-decor."""
    VARS = {'crysS': ['crysS1', 'crysS2', 'crysS3'], 'crysM': ['crysM1', 'crysM2'], 'treeS': ['treeS1', 'treeS2'],
            'fern': ['fern1', 'fern2'], 'spark': ['spark1', 'spark2'], 'vein': ['vein1', 'vein2', 'vein3'],
            'circ': ['circ1', 'circ2', 'circ3']}
    SIZE = {'crysS': (1, 1), 'crysM': (2, 2), 'crysL': (3, 3), 'crysP': (1, 2), 'treeL': (3, 3), 'treeS': (1, 2),
            'fern': (1, 1), 'cube': (1, 1), 'cubeL': (2, 2), 'bones': (2, 1), 'spark': (1, 1), 'vein': (1, 1),
            'circ': (1, 1), 'flower': (1, 1), 'tera': (3, 3), 'station': (3, 2), 'terminal': (2, 2)}
    WALK = {'spark', 'vein', 'circ', 'flower'}
    WALLGROW = {'crysS'}                                  # kleine kristallen groeien tegen een wand

    def __init__(self, w, h, seed):
        super().__init__(w, h, seed)
        self.grass = set()
        LAST.append(self)

    def build(self):
        """Kraterwanden van 2 blokken (rand, rots, wand, wand): de donkere rotsrij wordt een klifrand (lipD), zodat
        de wand als één klif naar het lagere terras leest en niet als een kuil."""
        g = super().build()
        rimSD, rockD, lipD = ID['rimSD'][0], ID['rockD'][0], ID['lipD'][0]
        for y in range(1, self.H - 1):
            for x in range(self.W):
                if (x, y) not in self.over and g[y][x] & 0x3FF == rockD and g[y - 1][x] & 0x3FF == rimSD and \
                        g[y + 1][x] & 0x3FF in (0x231, 0x230, 0x232):
                    g[y][x] = cell(lipD, 1, 0)
        self.g = g
        return g

    def put(self, kind, x, y):
        name = self.rnd.choice(self.VARS[kind]) if kind in self.VARS else kind
        if kind == 'flower':
            self.set(x, y, 0x004, 0)
            return
        w, h = self.SIZE[kind]
        for i, m in enumerate(ID[name]):
            dx, dy = i % w, i // w
            self.set(x + dx, y + dy, m, 0 if kind in self.WALK else 1)
            if kind not in self.WALK:
                self.blocked_decor.add((x + dx, y + dy))

    def decorate(self, keep, counts, area=None):
        x0, y0, x1, y1 = area or (0, 0, self.W - 1, self.H - 1)
        tr = self.terrace_rows()
        for kind, n in counts:
            w, h = self.SIZE[kind]
            tries = 0
            while n and tries < 4000:
                tries += 1
                x, y = self.rnd.randint(x0, x1 - w + 1), self.rnd.randint(y0, y1 - h + 1)
                if kind in self.WALK:
                    if not self.isF(x, y) or self.k[y][x] != 'F' or (x, y) in self.over or (x, y) in tr or \
                            (x, y) in keep or (x, y) in self.grass:
                        continue
                elif not self.free(x, y, w, h, keep, 2 if w * h >= 6 else 1) or \
                        any((x + a, y + b) in self.grass for a in range(w) for b in range(h)):
                    continue
                if kind in self.WALLGROW and not any(not self.isF(x + a, y - b) for a in range(w) for b in (1, 2)):
                    continue
                self.put(kind, x, y)
                n -= 1

    def tall_grass(self, cx, cy, rx, ry, keep=()):
        nz = random.Random('%s-%s' % (cx, cy))
        ph = nz.uniform(0, 6.28)
        tr = self.terrace_rows()
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if not (0 <= x < self.W and 0 <= y < self.H):
                    continue
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                wob = 0.22 * math.sin(3 * math.atan2(y - cy, x - cx) + ph)
                if d <= 1 + wob and self.k[y][x] == 'F' and (x, y) not in self.over and (x, y) not in tr and \
                        (x, y) not in keep and not any((x + a, y + b) in self.blocked_decor for a in (-1, 0, 1) for b in (-1, 0, 1)):
                    self.set(x, y, 0x00D, 0)
                    self.grass.add((x, y))

    def pool(self, cx, cy, rx, ry):
        """Organische vijver (water, alleen te bezwemmen met Surf); na de laatste shape(), vóór build()."""
        ph = random.Random('%s-%s' % (cx, cy)).uniform(0, 6.28)
        tr = self.terrace_rows()
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if any((x + a, y + b) in tr for a in (-1, 0, 1) for b in (-1, 0, 1)):
                    continue
                d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
                if d <= 1 + 0.2 * math.sin(3 * math.atan2(y - cy, x - cx) + ph) and self.k[y][x] == 'F' and \
                        all(self.k[y + b][x + a] in 'FW' for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2)):
                    self.k[y][x] = 'W'

    def panels(self, cx, cy, rx, ry, keep=()):
        """Vlak van toekomstpanelen (beloopbaar), grillige rand."""
        ph = random.Random('%s-%s' % (cx, cy)).uniform(0, 6.28)
        tr = self.terrace_rows()
        for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
            for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
                if not (0 <= x < self.W and 0 <= y < self.H):
                    continue
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d <= 1 + 0.25 * math.sin(2 * math.atan2(y - cy, x - cx) + ph) and self.k[y][x] == 'F' and \
                        (x, y) not in self.over and (x, y) not in tr:
                    r = self.rnd.random()
                    self.set(x, y, ID['circ1' if r < 0.6 else 'circ2' if r < 0.8 else 'circ3'][0], 0)
                    self.grass.add((x, y))

    def gate(self, x, y):
        """Poortframe (3x2) met de draaikolk op (x, y); je stapt er van onderen op."""
        for i, m in enumerate(ID['gate']):
            dx, dy = i % 3 - 1, i // 3 - 1
            if (dx, dy) == (0, 0):
                self.set(x, y, ID['pad'][0], 0)
            else:
                self.set(x + dx, y + dy, m, 1)
                self.blocked_decor.add((x + dx, y + dy))


def sight(xy, face, n):
    return cs.sight(xy, face, n)


EV = {}       # per kaart: opgeloste plekken
LAST = []     # laatst gebouwde kaart (debug-render bij een fout)


def place_items(name, m, g, wanted, taken):
    out = []
    for tgt, it, fl, q, hid in wanted:
        p = cs.item_spot(m, g, tgt, taken)
        taken |= {p}
        out.append((p, it, fl, q, hid))
    EV.setdefault(name, {})['items'] = out
    return {p for p, *_ in out}


def new_items(name, targets):
    import nieuwe_items as ni
    lst = ni.items(name)
    assert len(lst) == len(targets), (name, lst)
    return [(targets[it], it, fl, q, hid) for fl, it, q, hid in lst]


# --------------------------------------------------------------------- de kom (9 okt, Jordi: "het lijkt niet op een krater")
# Elke laag is een trechter: ringvormige terrassen (vloer) gescheiden door ringvormige rotswanden die naar het midden
# afdalen. De noordwanden zijn hoog (zichtbare klifwand), de zuidwanden laag (perspectief van een kom); per wand één
# trap in een recht stuk van de noordwand, om en om links en rechts van het midden (spiraal naar beneden). Binnenkomst
# bovenaan op de buitenste ring, de uitgang naar de volgende diepte op de bodem in het midden.
# Profiel: lijst (soort, noord, zuid, zijkant) van binnen naar buiten, in tegels; soort 'F' = vloer, 'R' = wand.
BOWL3 = [('F', 6, 5, 8), ('R', 4, 3, 3), ('F', 4.5, 4, 5), ('R', 4, 3, 3), ('F', 4.5, 4, 5)]
BOWL2 = [('F', 7, 5, 8), ('R', 4, 3, 3), ('F', 4.5, 4, 5)]


BOWL_P = 2.5          # superellips: vlakke noord- en zuidwanden (rechte stukken voor de trappen), ronde hoeken


def pnorm(x, y):
    return (abs(x) ** BOWL_P + abs(y) ** BOWL_P) ** (1 / BOWL_P)


def bowl_bounds(prof, seed):
    """Straal van elke grens (van binnen naar buiten) als functie van de hoek, met ruis (ronde, grillige vorm)."""
    rnd = random.Random(seed)
    nb = len(prof)
    shared = [(rnd.uniform(0.6, 1.0), k, rnd.uniform(0, 6.28)) for k in (2, 3)]
    own = [[(rnd.uniform(0.2, 0.5), k, rnd.uniform(0, 6.28)) for k in (2, 3)] for _ in range(nb)]

    def bounds(t):
        s2, c2 = math.sin(t) ** 2, math.cos(t) ** 2
        out, r = [], 0.0
        for i, (kind, n, s, side) in enumerate(prof):
            w = side * c2 + (n if math.sin(t) < 0 else s) * s2
            amp = (0.25 if kind == 'R' else 0.6) * (0.4 + 0.6 * i / max(1, nb - 1))
            w += amp * sum(a * math.sin(k * t + p) for a, k, p in shared) / 1.5
            w += sum(a * math.sin(k * t + p) for a, k, p in own[i]) / (8 if kind == 'R' else 3)
            r += max(w, 3.5 if kind == 'F' else 2.5)
            out.append(r)
        return out
    return bounds


def bowl(m, prof, stairs, seed):
    """Vult m.k met een kom rond (m.cx, m.cy). stairs[i] = x-afstand tot het midden van de trap in wand i (van buiten
    naar binnen). Zet m.lvl (niveau per 2x2-blok; 0 = buitenste ring) en m.terraces."""
    bounds = bowl_bounds(prof, seed)
    cx, cy = m.cx, m.cy
    nfl = sum(1 for p in prof if p[0] == 'F')
    Wc, Hc = m.W // 2, m.H // 2
    L = [[-1] * Wc for _ in range(Hc)]                    # -1 rots, anders niveau (0 = buiten)
    for by in range(Hc):
        for bx in range(Wc):
            px, py = 2 * bx + 1 - cx, 2 * by + 1 - cy
            d, t = pnorm(px, py), math.atan2(py, px)
            fl = nfl
            for (kind, *_), b in zip(prof, bounds(t)):
                if kind == 'F':
                    fl -= 1
                if d < b:
                    L[by][bx] = fl if kind == 'F' else -1
                    break
    nb8 = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a, b) != (0, 0)]
    for _ in range(30):                                    # verschillende niveaus raken elkaar nergens (ook diagonaal)
        ch = 0
        for by in range(1, Hc - 1):
            for bx in range(1, Wc - 1):
                if L[by][bx] >= 0 and any(L[by + b][bx + a] >= 0 and L[by + b][bx + a] < L[by][bx] for a, b in nb8):
                    L[by][bx] = -1; ch += 1
        for by in range(Hc - 1):                            # diagonale aanraking binnen één niveau: open
            for bx in range(Wc - 1):
                q = (L[by][bx], L[by][bx + 1], L[by + 1][bx], L[by + 1][bx + 1])
                if q[0] >= 0 and q[0] == q[3] and q[1] < 0 and q[2] < 0:
                    L[by][bx + 1] = q[0]; ch += 1
                elif q[1] >= 0 and q[1] == q[2] and q[0] < 0 and q[3] < 0:
                    L[by][bx] = q[1]; ch += 1
        for by in range(1, Hc - 1):                        # losse rotsplekjes binnen één niveau: dicht
            for bx in range(1, Wc - 1):
                if L[by][bx] >= 0:
                    continue
                near = {L[by + b][bx + a] for a, b in nb8} - {-1}
                if len(near) == 1 and ((L[by][bx - 1] >= 0 and L[by][bx + 1] >= 0) or
                                       (L[by - 1][bx] >= 0 and L[by + 1][bx] >= 0)):
                    L[by][bx] = near.pop(); ch += 1
        if not ch:
            break
    def below(bx, by):
        while by < Hc and L[by][bx] < 0:
            by += 1
        return L[by][bx] if by < Hc else -1

    for _ in range(4):           # noordwanden max. 2 blokken (dikker geeft een rotsvlakte die als kuil/plateau leest)
        for bx in range(Wc):
            for by in range(1, Hc - 3):
                up = L[by - 1][bx]
                if up >= 0 and L[by][bx] < 0 and L[by + 1][bx] < 0 and L[by + 2][bx] < 0 and below(bx, by) > up and \
                        {L[by + b][bx + a] for a, b in nb8 if 0 <= bx + a < Wc} <= {up, -1}:
                    L[by][bx] = up
    for by in range(Hc):
        for bx in range(Wc):
            if bx < 2 or by < 1 or bx >= Wc - 2 or by >= Hc - 2:
                assert L[by][bx] < 0, ('kom te groot voor de kaart', bx, by)
    # trappen: per wand een uitsnede van 3 blokken breed door de noordwand, met een terras (rand + trap) onderaan
    m.stair_cells = set()

    def runs_at(i, bxs):
        """Per kolom (bovenkant wand, eerste blok van het volgende niveau) langs de noordwand; None als het niet past."""
        runs = {}
        if bxs < 3 or bxs > Wc - 4:
            return None
        for bx in (bxs - 1, bxs, bxs + 1):
            by = 0
            while by < Hc and L[by][bx] != i:
                by += 1
            while by < Hc and L[by][bx] == i:
                by += 1
            top = by
            while by < Hc and L[by][bx] < 0:
                by += 1
            if by >= Hc or L[by][bx] != i + 1 or by > cy // 2:
                return None
            runs[bx] = (top, by)
        bmin = min(b for _, b in runs.values())
        if bmin - max(t for t, _ in runs.values()) < 1 or max(b for _, b in runs.values()) - bmin > 2:
            return None
        if any(L[by][bx] >= 0 for bx in (bxs - 2, bxs + 2) for by in (bmin - 1,)):
            return None
        return runs, bmin

    for i, dx in enumerate(stairs):
        sgn = 1 if dx >= 0 else -1
        for k in range(0, 40):                              # dichtst bij de gewenste plek, eerst naar het midden toe
            bxs = int(cx + dx - sgn * 2 * ((k + 1) // 2) * (1 if k % 2 else -1)) // 2
            got = runs_at(i, bxs)
            if got:
                break
        if not got:
            print('\n'.join(''.join('#' if v < 0 else str(v) for v in row) for row in L))
        assert got, ('trap: geen recht stuk noordwand', i)
        runs, bmin = got
        for bx, (top, bin_) in runs.items():
            for by in range(top, bin_):
                L[by][bx] = i if by < bmin else i + 1
        x0, x1, ys = 2 * (bxs - 1), 2 * (bxs + 1) + 1, 2 * bmin - 2
        m.terraces.append((x0, x1, ys, (2 * bxs, 2 * bxs + 1)))
        m.stair_cells |= {(2 * bxs, ys + 1), (2 * bxs + 1, ys + 1)}
    for y in range(m.H):
        for x in range(m.W):
            bx, by = x // 2, y // 2
            m.k[y][x] = 'F' if bx < Wc and by < Hc and L[by][bx] >= 0 else 'R'
    m.lvl = L
    m.nlev = nfl


def lvl(m, x, y):
    if not (0 <= x < m.W and 0 <= y < m.H) or x // 2 >= len(m.lvl[0]) or y // 2 >= len(m.lvl):
        return -1
    return m.lvl[y // 2][x // 2]


def spot(m, level, deg, frac=0.5):
    """Vloertegel van een niveau op de straal vanuit het midden onder hoek deg (0 = oost, -90 = noord), op frac van
    de breedte van de ring."""
    t = math.radians(deg)
    run, r = [], 0.0
    while r < max(m.W, m.H):
        x, y = int(m.cx + r * math.cos(t)), int(m.cy + r * math.sin(t))
        if lvl(m, x, y) == level and m.k[y][x] == 'F' and (x, y) not in run:
            run.append((x, y))
        r += 0.25
    assert run, ('geen vloer', level, deg)
    return run[min(len(run) - 1, int(frac * len(run)))]


def fit(m, target, w, h, level=None, front=1):
    """Linksboven van een w x h object (plus front rijen vloer ervoor en 1 kolom vrij opzij), dichtst bij target."""
    tr = m.terrace_rows()
    best = None
    for y in range(2, m.H - 3):
        for x in range(3, m.W - 3):
            cells = [(x + a, y + b) for a in range(-1, w + 1) for b in range(0, h + front)]
            if all(m.k[cy_][cx_] == 'F' and (cx_, cy_) not in m.over and (cx_, cy_) not in tr and
                   (level is None or lvl(m, cx_, cy_) == level) for cx_, cy_ in cells):
                d = (x + w / 2 - target[0]) ** 2 + (y + h / 2 - target[1]) ** 2
                if best is None or d < best[0]:
                    best = (d, (x, y))
    assert best, ('geen plek', target, w, h)
    return best[1]


def top_of(m, level, dx):
    """Bovenste vloertegel van een niveau in kolom cx+dx (tegen de noordwand: plek voor de ladder)."""
    x = int(m.cx + dx)
    for y in range(m.H):
        if lvl(m, x, y) == level and m.k[y][x] == 'F':
            return (x, y)
    raise AssertionError(('geen vloer in kolom', level, dx))


def bottom_of(m, level, dx):
    x = int(m.cx + dx)
    for y in range(m.H - 1, -1, -1):
        if lvl(m, x, y) == level and m.k[y][x] == 'F':
            return (x, y)
    raise AssertionError(('geen vloer in kolom', level, dx))


def new_bowl(seed, prof, stairs):
    """Kaart precies groot genoeg voor de kom: rondom 4-5 tegels rots (de bovenwand van de krater)."""
    bounds = bowl_bounds(prof, seed)
    ts = [2 * math.pi * i / 720 for i in range(720)]
    ext = [(bounds(t)[-1] * math.cos(t) / pnorm(math.cos(t), math.sin(t)),
            bounds(t)[-1] * math.sin(t) / pnorm(math.cos(t), math.sin(t))) for t in ts]
    north = -min(y for _, y in ext)
    south = max(y for _, y in ext)
    side = max(abs(x) for x, _ in ext)
    cy = 2 * math.ceil((north + 5) / 2)
    cx = 2 * math.ceil((side + 4) / 2)
    w, h = 2 * cx, 2 * math.ceil((cy + south + 4) / 2)
    m = AZ(w, h, seed)
    m.cx, m.cy = cx, cy
    bowl(m, prof, stairs, seed)
    return m


def center(m):
    """Midden van de bodem (even coördinaten: midden van een blok)."""
    return (m.cx, m.cy)


def polar_items(m, targets):
    return {it: spot(m, *t) for it, t in targets.items()}


def spiral_check(name, m, g, start, goal):
    """Zonder de trappen is de bodem niet te bereiken: de route loopt echt via de terrassen omlaag."""
    r = mf.reachable(g, start, set(m.stair_cells))
    assert goal not in r and not mf.next_to(r, *goal), (name, 'bodem bereikbaar zonder trap')


def crystal_ring(m, c, keep, n=8, rad=3.2):
    """Kristallen in een kring rond de uitgang op de bodem."""
    for i in range(n):
        t = 2 * math.pi * (i + 0.5) / n
        x, y = int(round(c[0] + rad * 1.25 * math.cos(t))), int(round(c[1] + rad * math.sin(t)))
        if m.k[y][x] == 'F' and (x, y) not in keep and (x, y) not in m.over and (x, y) not in m.terrace_rows():
            m.put('crysS', x, y)


# --------------------------------------------------------------------- laag 1: de kraterwand
RIM_LADDER = RIM_EXIT = RIM_STATION = None    # door build_rim gezet (warp 0 = ladder omhoog = hub, warp 1 = midden)
RIM_ITEMS = {'ITEM_QUICK_BALL': (1, 10, 0.5), 'ITEM_MUSCLE_BAND': (1, 170, 0.5)}   # (niveau, hoek, plek in de ring)
RIM_OLD_T = [((0, 30, 0.5), 'ITEM_FULL_RESTORE', 'FLAG_ITEM_AREA_ZERO_RIM_FULL_RESTORE', 1, False),
             ((0, 135, 0.5), 'ITEM_MAX_ELIXIR', 'FLAG_HIDDEN_ITEM_AREA_ZERO_RIM_MAX_ELIXIR', 1, True)]


def build_rim():
    global RIM_LADDER, RIM_EXIT, RIM_STATION
    m = new_bowl(9101, BOWL3, [8, -5])
    m.build()
    m.steps()
    RIM_LADDER = top_of(m, 0, -12)
    RIM_EXIT = center(m)
    m.ladder(*RIM_LADDER)
    m.ladder(*RIM_EXIT)
    RIM_STATION = fit(m, spot(m, 0, -10, 0.5), 3, 2, level=0)
    for i, mt in enumerate(ID['station']):
        m.set(RIM_STATION[0] + i % 3, RIM_STATION[1] + i // 3, mt, 1)
        m.blocked_decor.add((RIM_STATION[0] + i % 3, RIM_STATION[1] + i // 3))
    g = m.build()
    taken = {RIM_LADDER, RIM_EXIT, (RIM_STATION[0] + 1, RIM_STATION[1] + 2)}
    old = [(spot(m, *t), it, fl, q, hid) for t, it, fl, q, hid in RIM_OLD_T]
    ip = place_items(RIM, m, g, old + new_items(RIM, polar_items(m, RIM_ITEMS)), taken)
    logw = cs.wall_spot(m, spot(m, 1, -120, 0.3))
    EV[RIM]['log'] = logw
    pts = [(RIM_LADDER[0], RIM_LADDER[1] + 1), (RIM_EXIT[0], RIM_EXIT[1] + 1), (RIM_STATION[0] + 1, RIM_STATION[1] + 2),
           (logw[0], logw[1] + 1)] + sorted(ip)
    keep = cs.keep_paths(g, pts, ip | {(RIM_EXIT[0] + a, RIM_EXIT[1] + b) for a in (-1, 0, 1) for b in (-1, 0, 1, 2)})
    for lv, deg, rx, ry in ((0, -150, 4, 2), (0, 160, 3, 3), (0, 60, 5, 2), (1, -20, 3, 2.5), (1, 120, 4, 2),
                            (2, 200, 2.5, 1.5)):
        x, y = spot(m, lv, deg)
        m.tall_grass(x, y, rx, ry, keep)
    m.decorate(keep, [('treeL', 7), ('treeS', 30), ('crysM', 2), ('crysS', 10), ('fern', 14), ('flower', 22),
                      ('spark', 6)])
    crystal_ring(m, RIM_EXIT, keep, 6)
    rubble(m, keep, 12)
    g = m.build()
    spiral_check(RIM, m, g, (RIM_LADDER[0], RIM_LADDER[1] + 1), RIM_EXIT)
    return m, g


def hole_spot(m, target, level=None):
    """Plek voor een grotgat in een noordwand: 3 rotscellen breed, 2 hoog, met vloer eronder; dichtst bij target."""
    best = None
    tr = m.terrace_rows()
    for y in range(2, m.H - 2):
        for x in range(2, m.W - 2):
            if all(m.k[y + b][x + a] == 'R' for a in (-1, 0, 1) for b in (-1, 0)) and \
                    all(m.k[y + 1][x + a] == 'F' and (level is None or lvl(m, x + a, y + 1) == level)
                        for a in (-2, -1, 0, 1, 2)) and \
                    not any((x + a, y + b) in m.over or (x + a, y + b) in tr for a in (-2, -1, 0, 1, 2) for b in (-1, 0, 1)):
                d = (x - target[0]) ** 2 + (y - target[1]) ** 2
                if best is None or d < best[0]:
                    best = (d, (x, y))
    return best[1]


def rubble(m, keep, n):
    tr = m.terrace_rows()
    tries = 0
    while n and tries < 3000:
        tries += 1
        x, y = m.rnd.randint(2, m.W - 3), m.rnd.randint(2, m.H - 3)
        if m.k[y][x] != 'F' or (x, y) in m.over or (x, y) in keep or (x, y) in tr or (x, y) in m.grass or \
                any((x + a, y + b) in m.blocked_decor for a in (-1, 0, 1) for b in (-1, 0, 1)):
            continue
        m.set(x, y, m.rnd.choice(mf.RUBBLE), 1)
        m.blocked_decor.add((x, y))
        n -= 1


# --------------------------------------------------------------------- laag 2: de diepte
DEP_LADDER = DEP_EXIT = DEP_SCREAM = DEP_HANDS = None
DEP_ITEMS = {'ITEM_ADRENALINE_ORB': (0, 45, 0.5), 'ITEM_SHED_SHELL': (1, 150, 0.5)}
DEP_OLD_T = [((2, 0, 0.6), 'ITEM_PP_UP', 'FLAG_ITEM_AREA_ZERO_DEPTHS_PP_UP', 1, False)]


def build_depths():
    global DEP_LADDER, DEP_EXIT, DEP_SCREAM, DEP_HANDS
    m = new_bowl(9202, BOWL3, [-8, 5])
    m.build()
    m.steps()
    DEP_LADDER = top_of(m, 0, 12)
    DEP_EXIT = center(m)
    m.ladder(*DEP_LADDER)
    m.ladder(*DEP_EXIT)
    DEP_SCREAM = spot(m, 0, 180, 0.5)                 # SCREAM TAIL: westkant van de buitenste ring
    DEP_HANDS = spot(m, 1, 30, 0.5)                   # IRON HANDS: tweede ring, oostkant
    g = m.build()
    for p in (DEP_SCREAM, DEP_HANDS):
        assert m.k[p[1]][p[0]] == 'F' and p not in m.over, ('boss niet op vloer', p)
    taken = {DEP_LADDER, DEP_EXIT, DEP_SCREAM, DEP_HANDS}
    old = [(spot(m, *t), it, fl, q, hid) for t, it, fl, q, hid in DEP_OLD_T]
    ip = place_items(DEP, m, g, old + new_items(DEP, polar_items(m, DEP_ITEMS)), taken)
    logw = cs.wall_spot(m, spot(m, 0, -60, 0.2))
    EV.setdefault(DEP, {})['log'] = logw
    pts = [(DEP_LADDER[0], DEP_LADDER[1] + 1), (DEP_EXIT[0], DEP_EXIT[1] + 1), (DEP_SCREAM[0], DEP_SCREAM[1] + 1),
           (DEP_HANDS[0], DEP_HANDS[1] + 1), (logw[0], logw[1] + 1)] + sorted(ip)
    extra = ip | {(x, y) for x in range(DEP_SCREAM[0] - 1, DEP_SCREAM[0] + 2) for y in range(DEP_SCREAM[1] - 1, DEP_SCREAM[1] + 3)} | \
        {(x, y) for x in range(DEP_HANDS[0] - 1, DEP_HANDS[0] + 2) for y in range(DEP_HANDS[1] - 1, DEP_HANDS[1] + 3)} | \
        {(DEP_EXIT[0] + a, DEP_EXIT[1] + b) for a in (-1, 0, 1) for b in (-1, 0, 1, 2)}
    keep = cs.keep_paths(g, pts, extra)
    for lv, deg, rx, ry in ((0, -130, 4, 2), (0, 100, 4, 2), (1, -60, 3, 2), (1, 170, 2.5, 2.5), (2, 150, 2.5, 1.5)):
        x, y = spot(m, lv, deg)
        m.tall_grass(x, y, rx, ry, keep)
    m.decorate(keep, [('crysL', 4), ('crysP', 10), ('crysM', 10), ('crysS', 22), ('treeL', 4), ('treeS', 14),
                      ('fern', 12), ('vein', 26), ('spark', 14)])
    crystal_ring(m, DEP_EXIT, keep, 8)
    rubble(m, keep, 12)
    g = m.build()
    spiral_check(DEP, m, g, (DEP_LADDER[0], DEP_LADDER[1] + 1), DEP_EXIT)
    return m, g


# --------------------------------------------------------------------- laag 3: de kristalgrot
CRY_LADDER = CRY_GATE_PAST = CRY_GATE_FUT = None   # warp 0 ladder omhoog, 1/2 draaikolken (verleden/toekomst), 3 gat
CRY_ITEMS = {'ITEM_BEAST_BALL': (0, 20, 0.5), 'ITEM_RING_TARGET': (1, 200, 0.5)}
CRY_OLD_T = [((0, 150, 0.5), 'ITEM_MAX_REVIVE', 'FLAG_ITEM_AREA_ZERO_CRYSTAL_MAX_REVIVE', 1, False)]


def build_crystal():
    global CRY_LADDER, CRY_GATE_PAST, CRY_GATE_FUT
    m = new_bowl(9303, [('F', 6, 5, 9)] + BOWL3[1:], [8, -5])
    m.build()
    m.steps()
    CRY_LADDER = top_of(m, 0, -2)
    m.ladder(*CRY_LADDER)
    cx, cy = center(m)
    CRY_GATE_PAST = (cx - 4, cy + 1)                   # de Zero Gate op de bodem: verleden links, toekomst rechts
    CRY_GATE_FUT = (cx + 4, cy + 1)
    for gx, gy in (CRY_GATE_PAST, CRY_GATE_FUT):
        assert all(m.k[gy + b][gx + a] == 'F' and lvl(m, gx + a, gy + b) == m.nlev - 1
                   for a in (-2, -1, 0, 1, 2) for b in (-1, 0, 1)), ('poort niet op de bodem', gx, gy)
    m.gate(*CRY_GATE_PAST)
    m.gate(*CRY_GATE_FUT)
    g = m.build()
    hx, hy = hole_spot(m, (cx, cy - 6), level=m.nlev - 1)   # het verzegelde grotgat in de noordwand van de bodem
    m.cave_hole(hx, hy)
    m.set(hx, hy, ID['plug'][0], 1)          # dicht; opent via setmetatile (ON_LOAD) als beide systemen offline zijn
    EV.setdefault(CRY, {})['hole'] = (hx, hy)
    g = m.build()
    taken = {CRY_LADDER, CRY_GATE_PAST, CRY_GATE_FUT, (hx, hy + 1)}
    old = [(spot(m, *t), it, fl, q, hid) for t, it, fl, q, hid in CRY_OLD_T]
    ip = place_items(CRY, m, g, old + new_items(CRY, polar_items(m, CRY_ITEMS)), taken)
    logw = cs.wall_spot(m, spot(m, 1, -110, 0.2))
    EV[CRY]['log'] = logw
    signs = [(CRY_GATE_PAST[0] - 1, CRY_GATE_PAST[1] + 1), (CRY_GATE_FUT[0] + 1, CRY_GATE_FUT[1] + 1)]   # bord = pijler
    EV[CRY]['signs'] = signs
    pts = [(CRY_LADDER[0], CRY_LADDER[1] + 1), (CRY_GATE_PAST[0], CRY_GATE_PAST[1] + 1),
           (CRY_GATE_FUT[0], CRY_GATE_FUT[1] + 1), (hx, hy + 1), (logw[0], logw[1] + 1)] + signs + sorted(ip)
    extra = ip | set(signs) | {(x, y) for gx, gy in (CRY_GATE_PAST, CRY_GATE_FUT) for x in range(gx - 2, gx + 3)
                               for y in range(gy - 2, gy + 3)} | {(x, y) for x in range(hx - 2, hx + 3) for y in range(hy, hy + 3)}
    keep = cs.keep_paths(g, pts, extra)
    m.decorate(keep, [('crysL', 10), ('crysP', 20), ('crysM', 20), ('crysS', 40), ('vein', 40), ('spark', 34)])
    rubble(m, keep, 6)
    g = m.build()
    spiral_check(CRY, m, g, (CRY_LADDER[0], CRY_LADDER[1] + 1), (CRY_GATE_PAST[0], CRY_GATE_PAST[1] + 1))
    return m, g


# --------------------------------------------------------------------- laag 4: toekomst en verleden (zelfde vorm)
ERA_GATE = ERA_LADDER = ERA_LEGEND = ERA_TERMINAL = ERA_BOSSES = None
# warp 0 = aankomst/draaikolk naar de andere tijd, warp 1 = ladder omhoog (beide bovenaan op de rand);
# MIRAIDON/KORAIDON en de beveiligingsterminal op de bodem in het midden; drie paradoxen op de ringen
ERA_ITEMS = {FUT: {'ITEM_BOOSTER_ENERGY': (0, 40, 0.5), 'ITEM_METAL_ALLOY': (1, 190, 0.5), 'ITEM_AIR_BALLOON': (1, -20, 0.5)},
             PAS: {'ITEM_POWER_HERB': (0, 40, 0.5), 'ITEM_GRIP_CLAW': (1, 190, 0.5), 'ITEM_STICKY_BARB': (1, -20, 0.5)}}
ERA_OLD_T = {FUT: [((2, 150, 0.6), 'ITEM_PP_MAX', 'FLAG_ITEM_AREA_ZERO_FUTURE_PP_MAX', 1, False)],
             PAS: [((2, 150, 0.6), 'ITEM_RARE_CANDY', 'FLAG_ITEM_AREA_ZERO_PAST_RARE_CANDY', 1, False)]}


def build_era(name):
    global ERA_GATE, ERA_LADDER, ERA_LEGEND, ERA_TERMINAL, ERA_BOSSES
    m = new_bowl(9404, [('F', 6, 5, 9)] + BOWL3[1:], [-8, 5])   # zelfde seed: zelfde vorm in beide tijden
    m.build()
    m.steps()
    gx, gy = top_of(m, 0, 4)
    ERA_GATE = (gx, gy + 1)
    m.gate(*ERA_GATE)
    ERA_LADDER = top_of(m, 0, -2)
    m.ladder(*ERA_LADDER)
    cx, cy = center(m)
    ERA_LEGEND = (cx - 2, cy)
    ERA_TERMINAL = (cx + 2, cy - 2)                  # 2x2 (linksboven); aanspreken op de onderste rij
    ERA_BOSSES = [spot(m, 0, 175), spot(m, 1, 20), spot(m, 0, 75)]
    for i, mt in enumerate(ID['terminal']):
        m.set(ERA_TERMINAL[0] + i % 2, ERA_TERMINAL[1] + i // 2, mt, 1)
        m.blocked_decor.add((ERA_TERMINAL[0] + i % 2, ERA_TERMINAL[1] + i // 2))
    g = m.build()
    for p in ERA_BOSSES + [ERA_LEGEND]:
        assert m.k[p[1]][p[0]] == 'F' and p not in m.over, (name, 'boss niet op vloer', p)
    m.rnd = random.Random(9404 + (1 if name == PAS else 2))
    taken = {ERA_GATE, ERA_LADDER, ERA_LEGEND} | set(ERA_BOSSES)
    old = [(spot(m, *t), it, fl, q, hid) for t, it, fl, q, hid in ERA_OLD_T[name]]
    ip = place_items(name, m, g, old + new_items(name, polar_items(m, ERA_ITEMS[name])), taken)
    logw = cs.wall_spot(m, spot(m, 1, -120, 0.2))
    EV[name]['log'] = logw
    term = (ERA_TERMINAL[0], ERA_TERMINAL[1] + 2)
    pts = [(ERA_GATE[0], ERA_GATE[1] + 1), (ERA_LADDER[0], ERA_LADDER[1] + 1), (ERA_LEGEND[0], ERA_LEGEND[1] + 1),
           term, (logw[0], logw[1] + 1)] + [(x, y + 1) for x, y in ERA_BOSSES] + sorted(ip)
    extra = ip | {term, (term[0] + 1, term[1])}
    for (x0, y0) in ERA_BOSSES + [ERA_LEGEND, ERA_GATE]:
        extra |= {(x, y) for x in range(x0 - 2, x0 + 3) for y in range(y0 - 2, y0 + 3)}
    keep = cs.keep_paths(g, pts, extra)
    if name == FUT:
        for lv, deg, rx, ry in ((2, 90, 5, 2.2), (0, -150, 4, 2), (0, 120, 4, 2.2), (1, 100, 5, 2), (1, -150, 3, 2),
                                (0, -20, 3, 2.5)):
            x, y = spot(m, lv, deg)
            m.panels(x, y, rx, ry, keep)
        m.decorate(keep, [('cubeL', 10), ('crysP', 10), ('crysM', 8), ('cube', 26), ('crysS', 16), ('spark', 20)])
        rubble(m, keep, 6)
    else:
        for lv, deg, rx, ry in ((0, -150, 3.5, 2), (0, 120, 4, 2), (1, 100, 4, 2), (1, -150, 3, 2), (2, 200, 2.5, 1.5)):
            x, y = spot(m, lv, deg)
            m.tall_grass(x, y, rx, ry, keep)
        m.decorate(keep, [('treeL', 7), ('bones', 7), ('crysM', 8), ('crysP', 6), ('treeS', 24), ('fern', 36),
                          ('crysS', 16), ('vein', 24)])
        rubble(m, keep, 12)
    g = m.build()
    spiral_check(name, m, g, (ERA_GATE[0], ERA_GATE[1] + 1), (ERA_LEGEND[0], ERA_LEGEND[1] + 1))
    return m, g


# --------------------------------------------------------------------- de Tera-grot
TERA_EXIT = TERA_CORE = TERA_PAGOS = TERA_ALARM = None
# warp 0 = zuiduitgang terug naar de kristalgrot (op de rand); de Tera-kern, TERAPAGOS en het alarm op de bodem


def build_tera():
    global TERA_EXIT, TERA_CORE, TERA_PAGOS, TERA_ALARM
    m = new_bowl(9505, BOWL2, [-5])
    TERA_EXIT = bottom_of(m, 0, 0)
    m.build()
    m.steps()
    m.exit_south(*TERA_EXIT)
    cx, cy = center(m)
    TERA_CORE = (cx - 1, cy - 5)
    TERA_PAGOS = (cx, cy)
    TERA_ALARM = (cx + 4, cy - 2)
    for i, mt in enumerate(ID['tera']):
        m.set(TERA_CORE[0] + i % 3, TERA_CORE[1] + i // 3, mt, 1)
        m.blocked_decor.add((TERA_CORE[0] + i % 3, TERA_CORE[1] + i // 3))
    for i, mt in enumerate(ID['terminal']):
        m.set(TERA_ALARM[0] + i % 2, TERA_ALARM[1] + i // 2, mt, 1)
        m.blocked_decor.add((TERA_ALARM[0] + i % 2, TERA_ALARM[1] + i // 2))
    for p in [(TERA_CORE[0] + a, TERA_CORE[1] + b) for a in range(3) for b in range(3)] + \
            [(TERA_ALARM[0] + a, TERA_ALARM[1] + b) for a in range(2) for b in range(3)] + [TERA_PAGOS]:
        assert m.k[p[1]][p[0]] == 'F' and lvl(m, *p) == m.nlev - 1, ('Tera-grot: niet op de bodem', p)
    g = m.build()
    term = (TERA_ALARM[0], TERA_ALARM[1] + 2)
    pts = [(TERA_EXIT[0], TERA_EXIT[1] - 1), (TERA_PAGOS[0], TERA_PAGOS[1] + 1), term]
    extra = {(x, y) for x in range(TERA_PAGOS[0] - 2, TERA_PAGOS[0] + 3) for y in range(TERA_PAGOS[1] - 1, TERA_PAGOS[1] + 3)}
    extra |= {term, (term[0] + 1, term[1])}
    keep = cs.keep_paths(g, pts, extra)
    m.decorate(keep, [('crysL', 5), ('crysP', 12), ('crysM', 10), ('crysS', 22), ('vein', 22), ('spark', 22)])
    g = m.build()
    spiral_check(TERA, m, g, (TERA_EXIT[0], TERA_EXIT[1] - 1), (TERA_PAGOS[0], TERA_PAGOS[1] + 1))
    return m, g


# --------------------------------------------------------------------- render (zonder events, voor de vormcontrole)
def preview(name, g, out):
    import gridrender as gr
    prim, sec = tileset_syms(name)
    im = gr.render(g, azt_dir(prim), azt_dir(sec))
    im.save(out)
    return im


def azt_dir(sym):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', sym.replace('gTileset_', '')).lower()


BUILDERS = {RIM: build_rim, DEP: build_depths, CRY: build_crystal, FUT: lambda: build_era(FUT),
            PAS: lambda: build_era(PAS), TERA: build_tera}



# ====================================================================== flags (FLAG_GROUNDED 920-999)
FLAGS = [
    (920, 'FLAG_SPACETIME_AREAZERO_DONE', 'Spacetime-sidequest klaar: TERAPAGOS gevangen'),
    (921, 'FLAG_AREAZERO_SCREAM_TAIL', 'Area Zero, diepte: SCREAM TAIL gevangen'),
    (922, 'FLAG_AREAZERO_IRON_HANDS', 'Area Zero, diepte: IRON HANDS gevangen'),
    (923, 'FLAG_AREAZERO_IRON_LEAVES', 'Area Zero, toekomst: IRON LEAVES gevangen'),
    (924, 'FLAG_AREAZERO_IRON_BOULDER', 'Area Zero, toekomst: IRON BOULDER gevangen'),
    (925, 'FLAG_AREAZERO_IRON_CROWN', 'Area Zero, toekomst: IRON CROWN gevangen'),
    (926, 'FLAG_AREAZERO_MIRAIDON', 'Area Zero, toekomst: MIRAIDON gevangen (beveiligingssysteem gaat aan)'),
    (927, 'FLAG_AREAZERO_WALKING_WAKE', 'Area Zero, verleden: WALKING WAKE gevangen'),
    (928, 'FLAG_AREAZERO_GOUGING_FIRE', 'Area Zero, verleden: GOUGING FIRE gevangen'),
    (929, 'FLAG_AREAZERO_RAGING_BOLT', 'Area Zero, verleden: RAGING BOLT gevangen'),
    (930, 'FLAG_AREAZERO_KORAIDON', 'Area Zero, verleden: KORAIDON gevangen (beveiligingssysteem gaat aan)'),
    (931, 'FLAG_AREAZERO_INTRO', 'Area Zero: introtekst bij de eerste afdaling gezien'),
    (932, 'FLAG_ITEM_AREA_ZERO_RIM_FULL_RESTORE', 'Area Zero, kraterwand: Full Restore'),
    (933, 'FLAG_HIDDEN_ITEM_AREA_ZERO_RIM_MAX_ELIXIR', 'Area Zero, kraterwand: verborgen Max Elixir'),
    (934, 'FLAG_ITEM_AREA_ZERO_DEPTHS_PP_UP', 'Area Zero, diepte: PP Up'),
    (935, 'FLAG_ITEM_AREA_ZERO_CRYSTAL_MAX_REVIVE', 'Area Zero, kristalgrot: Max Revive'),
    (936, 'FLAG_ITEM_AREA_ZERO_FUTURE_PP_MAX', 'Area Zero, toekomst: PP Max'),
    (937, 'FLAG_ITEM_AREA_ZERO_PAST_RARE_CANDY', 'Area Zero, verleden: Rare Candy'),
]
FLAG_NOTE = '950-961 nieuwe items (nieuwe_items.py)'


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// area_zero { (tools/grounded/maptools/area_zero.py; FLAG_GROUNDED 920-999: %d-949 en 962-999 nog vrij, %s)\n' % (
        max(n for n, *_ in FLAGS) + 1, FLAG_NOTE)
    for n, name, why in FLAGS:
        assert 920 <= n <= 999
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// area_zero {' in s:
        i = s.index('// area_zero {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// glimwood {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== mapsec
MAPSEC = ('MAPSEC_AREA_ZERO', 'AREA ZERO', 'MAPPOPUP_THEME_STONE', 'Area Zero (Spacetime Cave)')


def mapsecs():
    mid, nm, theme, why = MAPSEC
    p = 'src/data/region_map/region_map_sections.json'
    s = open(p).read()
    if '"%s"' % mid not in s:
        i = s.rindex('    }\n  ]')
        s = s[:i + 5] + ',\n    {\n      "id": "%s",\n      "name": "%s"\n    }' % (mid, nm) + s[i + 5:]
    json.loads(s)
    open(p, 'w').write(s)
    p = 'src/map_name_popup.c'
    s = open(p).read()
    a = '    [MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_STONE, // Project Grounded: Spacetime Cave\n'
    b = '    [MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: Spacetime Cave\n'
    assert a in s and b in s
    if '[%s - KANTO' % mid not in s:
        s = s.replace(a, a + '    [%s - KANTO_MAPSEC_COUNT] = %s, // Project Grounded: %s\n' % (mid, theme, why), 1)
        s = s.replace(b, b + '    [%s - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: %s\n' % (mid, why), 1)
    open(p, 'w').write(s)


# ====================================================================== wilde Pokemon (achteraan de kaarttabellen)
WILD = {
    'AREA_ZERO_RIM': (7, [('FARIGIRAF', 88, 90), ('RAICHU', 88, 90), ('ESPEON', 88, 90), ('ALTARIA', 88, 90),
                          ('GOLDUCK', 88, 90), ('MEDICHAM', 88, 90), ('GARGANACL', 89, 91), ('GARCHOMP', 89, 91),
                          ('DRAGONITE', 89, 91), ('GLIMMORA', 89, 91), ('SALAMENCE', 90, 91), ('BAXCALIBUR', 90, 91)]),
    'AREA_ZERO_DEPTHS': (8, [('GLIMMORA', 89, 91), ('CARBINK', 89, 91), ('BRONZONG', 89, 91), ('UMBREON', 89, 91),
                             ('GARCHOMP', 89, 91), ('DRAGONITE', 89, 91), ('BAXCALIBUR', 90, 92), ('SALAMENCE', 90, 92),
                             ('HYDREIGON', 90, 92), ('METAGROSS', 90, 92), ('SCREAM_TAIL', 91, 92), ('IRON_HANDS', 91, 92)]),
    'AREA_ZERO_CRYSTAL': (8, [('CARBINK', 90, 92), ('GLIMMORA', 90, 92), ('SABLEYE', 90, 92), ('REUNICLUS', 90, 92),
                              ('PROBOPASS', 90, 92), ('GOTHITELLE', 90, 92), ('TINKATON', 91, 93), ('ARMAROUGE', 91, 93),
                              ('CERULEDGE', 91, 93), ('KINGAMBIT', 91, 93), ('GREAT_TUSK', 92, 93), ('IRON_TREADS', 92, 93)]),
    'AREA_ZERO_FUTURE': (9, [('IRON_TREADS', 91, 93), ('IRON_BUNDLE', 91, 93), ('IRON_JUGULIS', 91, 93),
                             ('IRON_MOTH', 91, 93), ('IRON_THORNS', 91, 93), ('PORYGON_Z', 91, 93), ('MAGNEZONE', 92, 94),
                             ('KLINKLANG', 92, 94), ('METAGROSS', 92, 94), ('ROTOM', 92, 94), ('IRON_VALIANT', 93, 94),
                             ('ARCHALUDON', 93, 94)]),
    'AREA_ZERO_PAST': (9, [('GREAT_TUSK', 91, 93), ('BRUTE_BONNET', 91, 93), ('FLUTTER_MANE', 91, 93),
                           ('SLITHER_WING', 91, 93), ('SANDY_SHOCKS', 91, 93), ('TYRANTRUM', 91, 93), ('AERODACTYL', 92, 94),
                           ('ARCHEOPS', 92, 94), ('AURORUS', 92, 94), ('ARMALDO', 92, 94), ('ROARING_MOON', 93, 94),
                           ('KABUTOPS', 93, 94)]),
}


def wild():
    p = 'src/data/wild_encounters.json'
    s = open(p).read()
    for mp, (rate, spec) in WILD.items():
        assert len(spec) == 12 and len({x[0] for x in spec}) == 12, mp
        lbl = 'g' + ''.join(w.title() for w in mp.split('_'))
        e = {'map': 'MAP_' + mp, 'base_label': lbl,
             'land_mons': {'encounter_rate': rate, 'mons': bd.mons(spec)}}
        blob = json.dumps(e, indent=2)
        blob = '\n'.join('        ' + ln for ln in blob.split('\n'))
        key = '"map": "MAP_%s"' % mp
        if key in s:
            i = s.index(key); a = s.rindex('{', 0, i)
            depth, j = 0, a
            while True:
                if s[j] == '{': depth += 1
                elif s[j] == '}':
                    depth -= 1
                    if depth == 0: break
                j += 1
            s = s[:a] + blob.lstrip() + s[j + 1:]
        else:
            anchor = '\n      ]\n    },\n    {\n      "label": "gBattlePyramidWildMonHeaders"'
            assert s.count(anchor) == 1
            s = s.replace(anchor, ',\n' + blob + anchor, 1)
    json.loads(s)
    open(p, 'w').write(s)


# ====================================================================== trainers: beveiliging en alarm (1180-1182)
IV = 'IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe'
AI_BOSS = bd.AI_BOSS


def mon(head, moves, tera=None, lvl=100):
    out = [head, 'Level: %d' % lvl, IV] + (['Tera Type: ' + tera] if tera else []) + ['- ' + m for m in moves]
    return '\n'.join(out)


TRAINERS = [
    ('AREA_ZERO_SECURITY_FUTURE', 1180, 'SECURITY', 'Zero Security', 'Area Zero, toekomst: beveiligingssysteem na MIRAIDON', [
        mon('Iron Valiant @ Booster Energy', ['Spirit Break', 'Close Combat', 'Knock Off', 'Swords Dance']),
        mon('Iron Moth @ Booster Energy', ['Fiery Dance', 'Sludge Wave', 'Energy Ball', 'Psychic']),
        mon('Iron Hands @ Leftovers', ['Drain Punch', 'Wild Charge', 'Ice Punch', 'Swords Dance']),
        mon('Iron Jugulis @ Choice Specs', ['Hurricane', 'Dark Pulse', 'Earth Power', 'Flamethrower']),
        mon('Iron Treads @ Booster Energy', ['Earthquake', 'Iron Head', 'Rapid Spin', 'Knock Off']),
        mon('Iron Bundle @ Booster Energy', ['Freeze-Dry', 'Hydro Pump', 'Encore', 'Flip Turn'])]),
    ('AREA_ZERO_SECURITY_PAST', 1181, 'SECURITY', 'Zero Security', 'Area Zero, verleden: beveiligingssysteem na KORAIDON', [
        mon('Roaring Moon @ Booster Energy', ['Dragon Dance', 'Acrobatics', 'Knock Off', 'Earthquake']),
        mon('Flutter Mane @ Booster Energy', ['Moonblast', 'Shadow Ball', 'Mystical Fire', 'Calm Mind']),
        mon('Great Tusk @ Booster Energy', ['Headlong Rush', 'Close Combat', 'Ice Spinner', 'Rapid Spin']),
        mon('Slither Wing @ Booster Energy', ['First Impression', 'Close Combat', 'Wild Charge', 'U-turn']),
        mon('Sandy Shocks @ Booster Energy', ['Thunderbolt', 'Earth Power', 'Spikes', 'Volt Switch']),
        mon('Scream Tail @ Leftovers', ['Play Rough', 'Encore', 'Thunder Wave', 'Wish'])]),
    ('AREA_ZERO_ALARM', 1182, 'ALARM', 'Zero Alarm', 'Area Zero, Tera-grot: alarmsysteem (terastaliseert, elk teamlid)', [
        mon('Iron Boulder @ Booster Energy', ['Mighty Cleave', 'Close Combat', 'Zen Headbutt', 'Swords Dance'], 'Rock'),
        mon('Walking Wake @ Choice Specs', ['Hydro Steam', 'Draco Meteor', 'Flamethrower', 'Dragon Pulse'], 'Water'),
        mon('Iron Leaves @ Booster Energy', ['Psyblade', 'Leaf Blade', 'Close Combat', 'Swords Dance'], 'Grass'),
        mon('Gouging Fire @ Booster Energy', ['Flare Blitz', 'Dragon Dance', 'Earthquake', 'Dragon Claw'], 'Ground'),
        mon('Raging Bolt @ Booster Energy', ['Thunderclap', 'Draco Meteor', 'Calm Mind', 'Dragon Pulse'], 'Fairy'),
        mon('Iron Crown @ Booster Energy', ['Tachyon Cutter', 'Psyshock', 'Focus Blast', 'Calm Mind'], 'Fighting')]),
]


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = '// area_zero { (tools/grounded/maptools/area_zero.py; id 1180-1182)\n'
    for key, n, nm, pic, why, team in TRAINERS:
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (key, n, why)
    blk += '// }'
    if '// area_zero {' in s:
        i = s.index('// area_zero {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for key, n, *_ in TRAINERS:
        hits = re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)
        assert len(hits) == 1, ('trainer-id dubbel', n, hits)
    open(p, 'w').write(s)
    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- area_zero (tools/grounded/maptools/area_zero.py) --- */\n\n'
    for key, n, nm, pic, why, team in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: Zero Lab', 'Pic: ' + pic, 'Gender: Male', 'Music: Suspicious',
               'Double Battle: No', AI_BOSS]
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (key, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde area_zero --- */'
    s = bd.replace_block(s, '/* --- area_zero', '/* --- einde area_zero --- */', blk)
    open(p, 'w').write(s)


def trainer_class_and_pics():
    """Nieuwe klasse ZERO LAB (geen geld), twee trainerfoto's (drone), muziek en transitie."""
    p = 'include/constants/trainers.h'
    s = open(p).read()
    if 'TRAINER_PIC_ZERO_SECURITY' not in s:
        m = re.search(r'#define TRAINER_PIC_COUNT\s+(\d+)', s)
        n = int(m.group(1))
        s = s.replace(m.group(0), '#define TRAINER_PIC_ZERO_SECURITY         %d // Project Grounded: Area Zero, beveiligingsdrone (area_zero_tiles.py)\n'
                      '#define TRAINER_PIC_ZERO_ALARM            %d // Project Grounded: Area Zero, alarmdrone\n'
                      '#define TRAINER_PIC_COUNT                 %d' % (n, n + 1, n + 2), 1)
    if 'TRAINER_CLASS_ZERO_LAB' not in s:
        assert '    TRAINER_CLASS_COUNT,' in s
        s = s.replace('    TRAINER_CLASS_COUNT,', '    TRAINER_CLASS_ZERO_LAB, // Project Grounded: Area Zero (beveiligings- en alarmsysteem)\n'
                      '    TRAINER_CLASS_COUNT,', 1)
    open(p, 'w').write(s)
    p = 'src/data/graphics/trainers.h'
    s = open(p).read()
    if 'gTrainerFrontPic_ZeroSecurity' not in s:
        a = 'const u16 gTrainerPalette_Petrel[] = INCBIN_U16("graphics/trainers/front_pics/petrel.gbapal");\n'
        assert a in s
        s = s.replace(a, a + 'const u32 gTrainerFrontPic_ZeroSecurity[] = INCBIN_U32("graphics/trainers/front_pics/zero_security.4bpp.smol"); // Project Grounded: Area Zero\n'
                      'const u16 gTrainerPalette_ZeroSecurity[] = INCBIN_U16("graphics/trainers/front_pics/zero_security.gbapal");\n'
                      'const u32 gTrainerFrontPic_ZeroAlarm[] = INCBIN_U32("graphics/trainers/front_pics/zero_alarm.4bpp.smol"); // Project Grounded: Area Zero\n'
                      'const u16 gTrainerPalette_ZeroAlarm[] = INCBIN_U16("graphics/trainers/front_pics/zero_alarm.gbapal");\n', 1)
        b = '    TRAINER_SPRITE(TRAINER_PIC_PETREL, gTrainerFrontPic_Petrel, gTrainerPalette_Petrel),\n'
        assert b in s
        s = s.replace(b, b + '    TRAINER_SPRITE(TRAINER_PIC_ZERO_SECURITY, gTrainerFrontPic_ZeroSecurity, gTrainerPalette_ZeroSecurity),\n'
                      '    TRAINER_SPRITE(TRAINER_PIC_ZERO_ALARM, gTrainerFrontPic_ZeroAlarm, gTrainerPalette_ZeroAlarm),\n', 1)
    open(p, 'w').write(s)
    p = 'src/battle_main.c'
    s = open(p).read()
    a = '    [TRAINER_CLASS_ROCKET_EXEC] = { _("ROCKET EXEC"), 25, BALL_ULTRA }, // Project Grounded: Rocket-sidequest\n'
    if 'TRAINER_CLASS_ZERO_LAB]' not in s:
        assert a in s
        s = s.replace(a, a + '    [TRAINER_CLASS_ZERO_LAB] = { _("ZERO LAB"), 0, BALL_MASTER }, // Project Grounded: Area Zero\n', 1)
    open(p, 'w').write(s)
    p = 'src/pokemon.c'
    s = open(p).read()
    a = '    case TRAINER_CLASS_ROCKET_EXEC: // Project Grounded: Petrel\n        return MUS_RG_VS_GYM_LEADER;\n'
    if 'TRAINER_CLASS_ZERO_LAB' not in s:
        assert a in s
        s = s.replace(a, a + '    case TRAINER_CLASS_ZERO_LAB: // Project Grounded: Area Zero (placeholder; Jordi maakt een eigen thema)\n'
                      '        return trainerId == TRAINER_AREA_ZERO_ALARM ? MUS_RG_VS_LEGEND : MUS_VS_FRONTIER_BRAIN;\n', 1)
    open(p, 'w').write(s)
    p = 'src/battle_setup.c'
    s = open(p).read()
    a = '    if (trainerClass == TRAINER_CLASS_TEAM_ROCKET || trainerClass == TRAINER_CLASS_ROCKET_EXEC)\n        return B_TRANSITION_ROCKET;\n'
    if 'TRAINER_CLASS_ZERO_LAB' not in s:
        assert a in s
        s = s.replace(a, a + '    // Project Grounded: Area Zero, de beveiligings-/alarmdrones (placeholder-transitie)\n'
                      '    if (trainerClass == TRAINER_CLASS_ZERO_LAB)\n        return B_TRANSITION_FRONTIER_SQUARES_SCROLL;\n', 1)
    open(p, 'w').write(s)


# ====================================================================== legendary-gevechten en Tera
LEGEND_CASES = [
    (('SCREAM_TAIL', 'IRON_HANDS'), 'B_TRANSITION_BLACKHOLE_PULSATE', 'Area Zero, de eerste paradoxen'),
    (('IRON_LEAVES', 'IRON_BOULDER', 'IRON_CROWN'), 'B_TRANSITION_FRONTIER_SQUARES', 'Area Zero, toekomst'),
    (('WALKING_WAKE', 'GOUGING_FIRE', 'RAGING_BOLT'), 'B_TRANSITION_ANGLED_WIPES', 'Area Zero, verleden'),
    (('MIRAIDON',), 'B_TRANSITION_SHRED_SPLIT', 'Area Zero, toekomst'),
    (('KORAIDON',), 'B_TRANSITION_SLICE', 'Area Zero, verleden'),
    (('TERAPAGOS_NORMAL', 'TERAPAGOS_TERASTAL', 'TERAPAGOS_STELLAR'), 'B_TRANSITION_FRONTIER_CIRCLES_SYMMETRIC_SPIRAL',
     'Area Zero, Tera-grot'),
]


def battle_setup():
    p = 'src/battle_setup.c'
    s = open(p).read()
    a = '    case SPECIES_XERNEAS: // Project Grounded: Glimwood Tangle'
    assert a in s
    if 'case SPECIES_MIRAIDON' not in s:
        blk = ''
        for sps, tr, why in LEGEND_CASES:
            for i, sp in enumerate(sps):
                blk += '    case SPECIES_%s:%s\n' % (sp, (' // Project Grounded: %s (placeholder: Kanto-legendary-thema)' % why) if i == 0 else '')
            blk += '        CreateBattleStartTask(%s, MUS_RG_VS_LEGEND);\n        break;\n' % tr
        s = s.replace(a, blk + a, 1)
    open(p, 'w').write(s)
    # Tera alleen voor de tegenstander in het alarmgevecht (naast The Spire); elk teamlid mag terastaliseren
    p = 'src/battle_gimmick.c'
    s = open(p).read()
    old = ('    // Project Grounded: Mega, Z-moves, Dynamax, Tera e.d. alleen in The Spire (Jordi), voor iedereen\n'
           '    if (!TESTING && !gSpireBattle)\n        return FALSE;\n')
    new = ('    // Project Grounded: Mega, Z-moves, Dynamax, Tera e.d. alleen in The Spire (Jordi), voor iedereen.\n'
           '    // Uitzondering: het alarmsysteem van Area Zero (area_zero.py) terastaliseert; de speler niet.\n'
           '    if (!TESTING && !gSpireBattle && !(gimmick == GIMMICK_TERA && IsAreaZeroTeraBattle() && !IsOnPlayerSide(battler)))\n'
           '        return FALSE;\n')
    if 'IsAreaZeroTeraBattle' not in s:
        assert old in s
        s = s.replace(old, new, 1)
        a = '// Returns whether a battler is able to use a gimmick. Checks consumption and gimmick specific functions.\n'
        assert a in s
        s = s.replace(a, '// Project Grounded: het Tera-gevecht van Area Zero (alarmsysteem, TRAINER_AREA_ZERO_ALARM)\n'
                      'bool32 IsAreaZeroTeraBattle(void)\n{\n'
                      '    return (gBattleTypeFlags & BATTLE_TYPE_TRAINER) && !(gBattleTypeFlags & BATTLE_TYPE_FRONTIER)\n'
                      '        && TRAINER_BATTLE_PARAM.opponentA == TRAINER_AREA_ZERO_ALARM;\n}\n\n' + a, 1)
        inc = '#include "battle_setup.h"\n#include "constants/opponents.h" // Project Grounded: Area Zero\n'
        first = s.index('\n', s.index('#include')) + 1      # na global.h
        s = s[:first] + inc + s[first:]
    open(p, 'w').write(s)
    p = 'include/battle_gimmick.h'
    s = open(p).read()
    if 'IsAreaZeroTeraBattle' not in s:
        a = 'bool32 CanActivateGimmick(u32 battler, enum Gimmick gimmick);\n'
        assert a in s
        s = s.replace(a, a + 'bool32 IsAreaZeroTeraBattle(void); // Project Grounded: Area Zero\n', 1)
    open(p, 'w').write(s)
    # elk teamlid van het alarmsysteem mag terastaliseren (één keer per Pokemon): HasTrainerUsedGimmick per Pokemon
    p = 'src/battle_gimmick.c'
    s = open(p).read()
    a = 'bool32 HasTrainerUsedGimmick(u32 battler, enum Gimmick gimmick)\n{\n'
    if 'Area Zero: elk teamlid' not in s:
        assert a in s
        s = s.replace(a, a + '    // Project Grounded: Area Zero: elk teamlid van het alarmsysteem terastaliseert, één keer per Pokemon\n'
                      '    if (gimmick == GIMMICK_TERA && IsAreaZeroTeraBattle() && !IsOnPlayerSide(battler))\n'
                      '        return GetActiveGimmick(battler) == GIMMICK_TERA;\n\n', 1)
    open(p, 'w').write(s)


# ====================================================================== kaarten registreren
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


def save(name, g):
    W, H = len(g[0]), len(g)
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', t) for r in g for t in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *([cell(ID['rockD'][0], 1, 0)] * 4)))
    prim, sec = tileset_syms(name)
    bd.register_layout(name, CONST[name], W, H, prim, sec)


def write_map(name, objs, warps, bgs, coords=()):
    m = {'id': 'MAP_' + CONST[name], 'name': name, 'layout': 'LAYOUT_' + CONST[name], 'music': MUSIC[name],
         'region_map_section': MAPSEC[0], 'requires_flash': False, 'weather': 'WEATHER_NONE',
         'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': True, 'allow_running': True,
         'show_map_name': name == RIM, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
         'object_events': objs, 'warp_events': warps, 'coord_events': list(coords), 'bg_events': bgs}
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    register_map(name)


def lid(o, name):
    o['local_id'] = name
    return o


def items_ev(name):
    objs, bgs = [], []
    for p, it, fl, q, hid in EV[name]['items']:
        if hid:
            h = {'type': 'hidden_item', 'x': p[0], 'y': p[1], 'elevation': 3, 'item': it, 'flag': fl}
            if q > 1:
                h['quantity'] = q
            bgs.append(h)
        else:
            o = bd.ball(p[0], p[1], it, fl)
            if q > 1:
                o['movement_range_x'] = q
            objs.append(o)
    return objs, bgs


def head(name, scripts=()):
    h = '@ Project Grounded: %s (tools/grounded/maptools/area_zero.py)\n%s_MapScripts::\n' % (name, name)
    for kind, lbl in scripts:
        h += '\tmap_script %s, %s\n' % (kind, lbl)
    return h + '\t.byte 0\n'


def boss_script(S, key, species, lvl, flag, local, meet, ko, after=''):
    """Vast gevecht dat terugkomt zolang het niet gevangen is. `after` = extra code na het vangen."""
    P, T = S.P, S.T
    S.raw(f'''{P}{key}::
	lock
	faceplayer
	playmoncry SPECIES_{species}, CRY_MODE_ENCOUNTER
	msgbox {T}{key}, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_{species}, {lvl}
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}{key}Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}{key}Back
	release
	end

{P}{key}Back::
	msgbox {T}{key}Back, MSGBOX_DEFAULT
	release
	end

{P}{key}Caught::
	removeobject {local}
	setflag {flag}
{after}	release
	end
''', [(key, meet), (key + 'Back', ko)])


def mon_obj(species, xy, script, flag, local):
    return lid(bd.obj('OBJ_EVENT_GFX_SPECIES(%s)' % species, xy[0], xy[1], script, flag, 'MOVEMENT_TYPE_FACE_DOWN'), local)


SEC = {FUT: 'TRAINER_AREA_ZERO_SECURITY_FUTURE', PAS: 'TRAINER_AREA_ZERO_SECURITY_PAST'}


def events():
    for n in MAPS:
        os.makedirs('data/maps/' + n, exist_ok=True)
    # ---------------------------------------------------------------- laag 1
    S = bd.Scr(RIM, head(RIM, [('MAP_SCRIPT_ON_TRANSITION', RIM + '_OnTransition'),
                               ('MAP_SCRIPT_ON_FRAME_TABLE', RIM + '_OnFrame')]))
    P, T = S.P, S.T
    S.raw(f'''{RIM}_OnTransition:
	call_if_unset FLAG_AREAZERO_INTRO, {P}SetIntro
	end

{P}SetIntro::
	setvar VAR_TEMP_1, 1
	return

{RIM}_OnFrame:
	map_script_2 VAR_TEMP_1, 1, {P}Intro
	.2byte 0

{P}Intro::
	lockall
	setvar VAR_TEMP_1, 0
	delay 16
	msgbox {T}Intro, MSGBOX_DEFAULT
	setflag FLAG_AREAZERO_INTRO
	releaseall
	end
''', [('Intro', "The rift spits you out on a ledge above an enormous crater.\n\nSomewhere far below, something is humming "
                "in a key that doesn't exist yet. Or anymore. Hard to say down here.")])
    S.npc('Station', "RESEARCH STATION No. 1\nStatus: unmanned since (DATE CORRUPTED).\n\nA sticky note on the door: "
          "'Elevator broken. Also time. Take the ladders.'", 'MSGBOX_SIGN')
    S.npc('Log', "RESEARCH LOG 01\nDay 3: the POKéMON up here are normal. Suspiciously normal.\n\nA FARIGIRAF looked "
          "at me like it knew my PIN.\nDay 4: it did know my PIN.", 'MSGBOX_SIGN')
    S.write()
    io, ib = items_ev(RIM)
    lg = EV[RIM]['log']
    warps = [bd.warp(RIM_LADDER[0], RIM_LADDER[1], HUB_DEST[0], HUB_DEST[1], elev=3),
             bd.warp(RIM_EXIT[0], RIM_EXIT[1], CONST[DEP], 0, elev=3)]
    bgs = [bd.sign(RIM_STATION[0] + 1, RIM_STATION[1] + 1, P + 'Station', 'BG_EVENT_PLAYER_FACING_NORTH'),
           bd.sign(lg[0], lg[1], P + 'Log', 'BG_EVENT_PLAYER_FACING_NORTH')] + ib
    write_map(RIM, io, warps, bgs)

    # ---------------------------------------------------------------- laag 2
    S = bd.Scr(DEP, head(DEP))
    P, T = S.P, S.T
    S.npc('Log', "RESEARCH LOG 02\nThe deeper we go, the more the colours drift. The grass is now 'teal-adjacent'.\n\n"
          "The crystals hum. Our intern hums back. We have asked him to stop. He says he can't.", 'MSGBOX_SIGN')
    boss_script(S, 'ScreamTail', 'SCREAM_TAIL', 94, 'FLAG_AREAZERO_SCREAM_TAIL', 'LOCALID_AREA_ZERO_SCREAM_TAIL',
                "A pink, fluffy thing with an enormous mouth stares at you.\n\nIt screams. It isn't angry. That's just "
                "its resting face.",
                "SCREAM TAIL dissolves into crystal dust... and screams itself back together.\n\nParadoxes don't really "
                "do 'gone'. Try catching it.")
    boss_script(S, 'IronHands', 'IRON_HANDS', 94, 'FLAG_AREAZERO_IRON_HANDS', 'LOCALID_AREA_ZERO_IRON_HANDS',
                "A hulking machine flexes two gigantic hands.\n\nA label on its back reads: DO NOT HIGH-FIVE.",
                "IRON HANDS powers down... and reboots with a cheerful chime.\n\nIt wants a rematch. It always wants "
                "a rematch.")
    S.write()
    io, ib = items_ev(DEP)
    lg = EV[DEP]['log']
    objs = [mon_obj('SCREAM_TAIL', DEP_SCREAM, P + 'ScreamTail', 'FLAG_AREAZERO_SCREAM_TAIL', 'LOCALID_AREA_ZERO_SCREAM_TAIL'),
            mon_obj('IRON_HANDS', DEP_HANDS, P + 'IronHands', 'FLAG_AREAZERO_IRON_HANDS', 'LOCALID_AREA_ZERO_IRON_HANDS')] + io
    warps = [bd.warp(DEP_LADDER[0], DEP_LADDER[1], CONST[RIM], 1, elev=3),
             bd.warp(DEP_EXIT[0], DEP_EXIT[1], CONST[CRY], 0, elev=3)]
    bgs = [bd.sign(lg[0], lg[1], P + 'Log', 'BG_EVENT_PLAYER_FACING_NORTH')] + ib
    write_map(DEP, objs, warps, bgs)

    # ---------------------------------------------------------------- laag 3
    hx, hy = EV[CRY]['hole']
    S = bd.Scr(CRY, head(CRY, [('MAP_SCRIPT_ON_LOAD', CRY + '_OnLoad')]))
    P, T = S.P, S.T
    S.raw(f'''{CRY}_OnLoad:
	checktrainerflag {SEC[FUT]}
	goto_if FALSE, {P}Sealed
	checktrainerflag {SEC[PAS]}
	goto_if FALSE, {P}Sealed
	setmetatile {hx}, {hy}, 0x24E, FALSE
{P}Sealed:
	end

{P}Hole::
	checktrainerflag {SEC[FUT]}
	goto_if FALSE, {P}HoleShut
	checktrainerflag {SEC[PAS]}
	goto_if FALSE, {P}HoleShut
	end

{P}HoleShut::
	msgbox {T}HoleShut, MSGBOX_SIGN
	end
''', [('HoleShut', "Crystals have grown over a cave mouth.\n\nBehind them something enormous is asleep, and two "
                   "security systems are very much awake. One in the past, one in the future. Naturally.")])
    S.npc('Log', "RESEARCH LOG 03\nWe built a gate. It goes to the past AND the future. The paperwork goes to "
          "neither.\n\nIf you see the PROFESSOR: the coffee machine in the future is fine. The one in the past is "
          "a rock.", 'MSGBOX_SIGN')
    S.npc('SignPast', "ZERO GATE - CHANNEL A\nPAST\n\nWarranty void if you meet yourself.", 'MSGBOX_SIGN')
    S.npc('SignFuture', "ZERO GATE - CHANNEL B\nFUTURE\n\nPlease do not bring back souvenirs. They bring themselves "
          "back.", 'MSGBOX_SIGN')
    S.write()
    io, ib = items_ev(CRY)
    lg = EV[CRY]['log']
    sp, sf = EV[CRY]['signs']
    warps = [bd.warp(CRY_LADDER[0], CRY_LADDER[1], CONST[DEP], 1, elev=3),
             bd.warp(CRY_GATE_PAST[0], CRY_GATE_PAST[1], CONST[PAS], 0, elev=3),
             bd.warp(CRY_GATE_FUT[0], CRY_GATE_FUT[1], CONST[FUT], 0, elev=3),
             bd.warp(hx, hy, CONST[TERA], 0, elev=3)]
    bgs = [bd.sign(lg[0], lg[1], P + 'Log', 'BG_EVENT_PLAYER_FACING_NORTH'),
           bd.sign(sp[0], sp[1] - 1, P + 'SignPast', 'BG_EVENT_PLAYER_FACING_NORTH'),
           bd.sign(sf[0], sf[1] - 1, P + 'SignFuture', 'BG_EVENT_PLAYER_FACING_NORTH'),
           bd.sign(hx, hy, P + 'Hole', 'BG_EVENT_PLAYER_FACING_NORTH')] + ib
    write_map(CRY, io, warps, bgs)

    # ---------------------------------------------------------------- toekomst en verleden
    ERA = {
        FUT: dict(legend='MIRAIDON', lflag='FLAG_AREAZERO_MIRAIDON', other=PAS, gate=2, word='FUTURE',
                  bosses=[('IronLeaves', 'IRON_LEAVES', 'FLAG_AREAZERO_IRON_LEAVES',
                           "A green, gleaming knight raises a psychic blade.\n\nIt looks like a legend you once heard "
                           "about. The legend never had a firmware update.",
                           "IRON LEAVES kneels, sparks, and stands up again. Chivalry is a renewable resource."),
                          ('IronBoulder', 'IRON_BOULDER', 'FLAG_AREAZERO_IRON_BOULDER',
                           "A polished, horned machine stands perfectly still.\n\nIts horn is so sharp the air "
                           "apologises when it moves.",
                           "IRON BOULDER reassembles itself, polishing out the dents. Vanity is futureproof."),
                          ('IronCrown', 'IRON_CROWN', 'FLAG_AREAZERO_IRON_CROWN',
                           "A crowned metal warrior regards you.\n\nIt has no idea what a crown is for, but it knows it "
                           "looks great in one.",
                           "IRON CROWN straightens its crown and reboots. Royalty doesn't stay down. It delegates.")],
                  meet="MIRAIDON lies curled up at the bottom of the crater, idling like an engine somebody forgot to switch off.\n\n"
                       "It opens one eye. Then the other. Then a third one, on a screen, somewhere.",
                  ko="MIRAIDON reboots in a shower of sparks.\n\nTurning it off and on again: still the oldest trick "
                     "in the future.",
                  log="RESEARCH LOG 7F\nThe robots here are polite. They call me 'organic legacy unit'. I've decided "
                      "to take it as a compliment.\n\nMIRAIDON sleeps at the bottom of the crater. The security system "
                      "sleeps next to it. Lightly.",
                  standby="ZERO LAB SECURITY TERMINAL\nSTATUS: STANDBY.\n\nCONTAINED: 1x MIRAIDON.\nDo not pet. Do not "
                          "feed after midnight. Do not explain midnight to it."),
        PAS: dict(legend='KORAIDON', lflag='FLAG_AREAZERO_KORAIDON', other=FUT, gate=1, word='PAST',
                  bosses=[('WalkingWake', 'WALKING_WAKE', 'FLAG_AREAZERO_WALKING_WAKE',
                           "A roaring blue beast with a blazing mane snorts steam at you.\n\nSomebody's ancient "
                           "legend. Extra spicy.",
                           "WALKING WAKE shakes the water off and comes right back. Extinction is a suggestion."),
                          ('GougingFire', 'GOUGING_FIRE', 'FLAG_AREAZERO_GOUGING_FIRE',
                           "A colossal molten beast paws the ground.\n\nThe floor underneath it has given up on being "
                           "solid.",
                           "GOUGING FIRE flares up again from its own embers. The floor sighs."),
                          ('RagingBolt', 'RAGING_BOLT', 'FLAG_AREAZERO_RAGING_BOLT',
                           "A long-necked thundercloud of a dinosaur grumbles at you.\n\nEvery grumble is a minor "
                           "weather event.",
                           "RAGING BOLT crackles back to life. Lightning never strikes the same place twice. This one "
                           "does, out of spite.")],
                  meet="KORAIDON lies at the bottom of the crater, sunning itself under a sun that went out millions of years "
                       "ago.\n\nIt wags. That's either friendly or a warning. Possibly both.",
                  ko="KORAIDON rolls over, yawns, and gets up again. Apex predators don't do naps on command.",
                  log="RESEARCH LOG 7P\nEverything here wants to eat me, including two of the plants.\n\nKORAIDON "
                      "naps at the bottom of the crater like a very large, very smug dog. The security system watches it. "
                      "It watches me back.",
                  standby="ZERO LAB SECURITY TERMINAL\nSTATUS: STANDBY.\n\nCONTAINED: 1x KORAIDON.\nDo not throw "
                          "sticks. It will bring back the tree."),
    }
    for name in (FUT, PAS):
        e = ERA[name]
        sec = SEC[name]
        other_sec = SEC[e['other']]
        S = bd.Scr(name, head(name))
        P, T = S.P, S.T
        objs = []
        for i, (key, sp, fl, meet, ko) in enumerate(e['bosses']):
            local = 'LOCALID_AREA_ZERO_' + sp
            boss_script(S, key, sp, 96, fl, local, meet, ko)
            objs.append(mon_obj(sp, ERA_BOSSES[i], P + key, fl, local))
        legend_local = 'LOCALID_AREA_ZERO_' + e['legend']
        boss_script(S, 'Legend', e['legend'], 98, e['lflag'], legend_local, e['meet'], e['ko'],
                    after='\tmsgbox %sAlarm, MSGBOX_DEFAULT\n\tgoto %sFight\n' % (T, P))
        objs.append(mon_obj(e['legend'], ERA_LEGEND, P + 'Legend', e['lflag'], legend_local))
        S.raw(f'''{P}Terminal::
	lock
	goto_if_defeated {sec}, {P}Offline
	goto_if_set {e['lflag']}, {P}Rearm
	msgbox {T}Standby, MSGBOX_DEFAULT
	release
	end

{P}Rearm::
	msgbox {T}Alarm, MSGBOX_DEFAULT
{P}Fight::
	trainerbattle_no_intro {sec}, {T}Defeat
	msgbox {T}Down, MSGBOX_DEFAULT
	checktrainerflag {other_sec}
	goto_if FALSE, {P}OneLeft
	msgbox {T}BothDown, MSGBOX_DEFAULT
	release
	end

{P}OneLeft::
	msgbox {T}OneLeft, MSGBOX_DEFAULT
	release
	end

{P}Offline::
	msgbox {T}Offline, MSGBOX_DEFAULT
	release
	end
''', [('Standby', e['standby']),
      ('Alarm', "BWEEEP. BWEEEP.\nSPECIMEN REMOVED FROM CONTAINMENT.\n\nINITIATING SECURITY PROTOCOL: ABSOLUTELY NOT."),
      ('Defeat', "PROTOCOL... FAILED.\nFILING A COMPLAINT WITH MYSELF."),
      ('Down', "The terminal goes dark with a sad little descending beep."),
      ('OneLeft', "A status line flickers before it dies: SECURITY NETWORK HALF OFFLINE. The other half is in the "
                  "%s. Of course it is." % ('PAST' if name == FUT else 'FUTURE')),
      ('BothDown', "A status line flickers before it dies: SECURITY NETWORK FULLY OFFLINE.\n\nFar above, in the crystal "
                   "cave, something cracks like ice on a lake."),
      ('Offline', "SECURITY OFFLINE.\nHAVE A NICE DAY. OR ERA.")])
        S.npc('Log', e['log'], 'MSGBOX_SIGN')
        S.write()
        io, ib = items_ev(name)
        objs += io
        lg = EV[name]['log']
        warps = [bd.warp(ERA_GATE[0], ERA_GATE[1], CONST[e['other']], 0, elev=3),
                 bd.warp(ERA_LADDER[0], ERA_LADDER[1], CONST[CRY], e['gate'], elev=3)]
        bgs = [bd.sign(ERA_TERMINAL[0], ERA_TERMINAL[1] + 1, P + 'Terminal', 'BG_EVENT_PLAYER_FACING_NORTH'),
               bd.sign(ERA_TERMINAL[0] + 1, ERA_TERMINAL[1] + 1, P + 'Terminal', 'BG_EVENT_PLAYER_FACING_NORTH'),
               bd.sign(lg[0], lg[1], P + 'Log', 'BG_EVENT_PLAYER_FACING_NORTH')] + ib
        write_map(name, objs, warps, bgs)

    # ---------------------------------------------------------------- de Tera-grot
    S = bd.Scr(TERA, head(TERA, [('MAP_SCRIPT_ON_TRANSITION', TERA + '_OnTransition')]))
    P, T = S.P, S.T
    S.raw(f'''{TERA}_OnTransition:
	setflag FLAG_TEMP_1
	goto_if_set FLAG_SPACETIME_AREAZERO_DONE, {P}TransEnd
	checktrainerflag TRAINER_AREA_ZERO_ALARM
	goto_if FALSE, {P}TransEnd
	clearflag FLAG_TEMP_1
{P}TransEnd:
	end

{P}Alarm::
	lock
	goto_if_defeated TRAINER_AREA_ZERO_ALARM, {P}AlarmOff
	msgbox {T}AlarmIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_AREA_ZERO_ALARM, {T}AlarmDefeat
	playse SE_THUNDERSTORM_STOP
	msgbox {T}Freed, MSGBOX_DEFAULT
	clearflag FLAG_TEMP_1
	addobject LOCALID_AREA_ZERO_TERAPAGOS
	playmoncry SPECIES_TERAPAGOS, CRY_MODE_NORMAL
	waitmoncry
	release
	end

{P}AlarmOff::
	msgbox {T}AlarmOff, MSGBOX_DEFAULT
	release
	end
''', [('AlarmIntro', "ALARM SYSTEM. THE LAST ONE. THE LOUD ONE.\n\nYOU HAVE DISABLED TWO SECURITY SYSTEMS. THAT WAS "
                     "VERY RUDE.\n\nENGAGING TERASTAL PROTOCOL. EVERY. SINGLE. ONE."),
      ('AlarmDefeat', "ALARM... SNOOZED."),
      ('Freed', "The alarm whines down to silence.\n\nThe great crystal at the back of the cave cracks, and something "
                "small and shell-shaped blinks at the light for the first time in a very long time."),
      ('AlarmOff', "ALARM SYSTEM: OFFLINE.\nSomebody has drawn a frowny face on the screen. From the inside.")])
    boss_script(S, 'Terapagos', 'TERAPAGOS', 100, 'FLAG_SPACETIME_AREAZERO_DONE', 'LOCALID_AREA_ZERO_TERAPAGOS',
                "TERAPAGOS looks at you, then at the dead alarm, then back at you.\n\nIt seems grateful. It also seems "
                "like a nuclear reactor shaped like a turtle.",
                "TERAPAGOS retreats into its shell and quietly re-crystallises. It's fine. It has done this for a few "
                "thousand years.",
                after='\tmsgbox %sDone, MSGBOX_DEFAULT\n' % T)
    S.raw('', [('Done', "TERAPAGOS is yours.\n\nAREA ZERO falls quiet: past, future and present, all minding their own "
                        "business for once.")])
    S.write()
    objs = [lid(bd.obj('OBJ_EVENT_GFX_SPECIES(TERAPAGOS)', TERA_PAGOS[0], TERA_PAGOS[1], P + 'Terapagos', 'FLAG_TEMP_1',
                       'MOVEMENT_TYPE_FACE_DOWN'), 'LOCALID_AREA_ZERO_TERAPAGOS')]
    warps = [bd.warp(TERA_EXIT[0], TERA_EXIT[1], CONST[CRY], 3, elev=3)]
    bgs = [bd.sign(TERA_ALARM[0], TERA_ALARM[1] + 1, P + 'Alarm', 'BG_EVENT_PLAYER_FACING_NORTH'),
           bd.sign(TERA_ALARM[0] + 1, TERA_ALARM[1] + 1, P + 'Alarm', 'BG_EVENT_PLAYER_FACING_NORTH')]
    write_map(TERA, objs, warps, bgs)


# ====================================================================== controle
def checks():
    for name, (m, g) in MAPS.items():
        d = json.load(open('data/maps/%s/map.json' % name))
        start = (d['warp_events'][0]['x'], d['warp_events'][0]['y'])
        if name == CRY:
            g = [list(r) for r in g]
            hx, hy = EV[CRY]['hole']
            g[hy][hx] = cell(0x24E, 0, E)                  # open (na beide beveiligingssystemen)
        solid = {(o['x'], o['y']) for o in d['object_events']} - {start}
        r = mf.reachable(g, start, solid)
        for o in d['object_events']:
            p = (o['x'], o['y'])
            assert mf.next_to(r, *p) or p in r, (name, 'object onbereikbaar', o['script'], p)
        for w in d['warp_events']:
            assert (w['x'], w['y']) in r, (name, 'warp onbereikbaar', w)
        for b in d['bg_events']:
            p = (b['x'], b['y'])
            assert p in r if b['type'] == 'hidden_item' else mf.next_to(r, *p), (name, 'bg onbereikbaar', p)
        print(name, 'bereikbaar:', len(r), 'tegels')
    g = MAPS[CRY][1]
    hx, hy = EV[CRY]['hole']
    assert (hx, hy) not in mf.reachable(g, (CRY_LADDER[0], CRY_LADDER[1]), set()), 'kristalgrot: gat niet dicht'


# ====================================================================== render
def render(outdir):
    os.makedirs(outdir, exist_ok=True)
    from PIL import Image
    ims = {}
    for name in MAPS:
        out = os.path.join(outdir, name + '.png')
        subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', name, out, '0', str(len(MAPS[name][1]))],
                       check=True)
        ims[name] = Image.open(out)
    # overzicht: van boven naar beneden afdalen; toekomst en verleden naast elkaar, de Tera-grot ernaast
    row1 = [ims[RIM], ims[DEP], ims[CRY]]
    row2 = [ims[PAS], ims[FUT], ims[TERA]]
    W = max(sum(i.width for i in row1), sum(i.width for i in row2)) + 64
    H = max(i.height for i in row1) + max(i.height for i in row2) + 48
    ov = Image.new('RGB', (W, H), (12, 10, 24))
    x = 16
    for i in row1:
        ov.paste(i, (x, 16)); x += i.width + 16
    x, y = 16, max(i.height for i in row1) + 32
    for i in row2:
        ov.paste(i, (x, y)); x += i.width + 16
    ov.save(os.path.join(outdir, 'overzicht.png'))


MAPS = {}


def main():
    import nieuwe_items as ni
    ID.update(azt.build())
    cs.ID = ID
    azt.register()
    azt.security_pic('graphics/trainers/front_pics/zero_security.png')
    azt.security_pic('graphics/trainers/front_pics/zero_alarm.png', alarm=True)
    flags()
    ni.flags()
    for name, fn in BUILDERS.items():
        m, g = fn()
        MAPS[name] = (m, g)
        save(name, g)
    mapsecs()
    events()
    trainers()
    trainer_class_and_pics()
    wild()
    battle_setup()
    checks()
    if len(sys.argv) > 1:
        render(sys.argv[1])


if __name__ == '__main__':
    main()
