"""Project Grounded: de drie Gen 4-meren als bestemming van de portalen in de meren-kamer van de Spacetime Cave.

- LakeAcuity (48x42, General + snow, sneeuw): bergwand bovenin met de grotmond waar het portaal je uitspuugt
  (warp 0 = aankomst + terugweg naar de hub), een bevroren meer met een eilandje; op het eiland een rotsje met een
  grot (warp 1 -> LakeAcuity_Cavern). Besneeuwde Hoenn-randbomen, dennen, hoog sneeuwgras.
- LakeValor / LakeVerity (48x42, General + Fortree): bos (Hoenn-bomen op een 2x2-raster), een meer met rotsoevers
  en een graswal aan de zuidkant (autotile volgens vanilla, zie pond_tile), riet (lang gras) langs de oevers, hoog
  gras, en in het midden de rotsheuvel met een zwemgrot van Route 120 (Scorched Slab, MB_WATER_DOOR; warp 2).
  Aankomst: de lichte open plek van Faraway Island onderaan (warps 0/1, zuidpijlen = terugweg naar de hub).
- *_Cavern (15x20, General + Cave): kopie van Scorched Slab (Cave-paletten i.p.v. de verschroeide), de opening
  bovenin dichtgemaakt; je zwemt binnen (warp 0, zuidpijl op water = terug naar het meer) en bovenin zit het
  meerwezen (Uxie/Azelf/Mesprit lv 94, setwildbattle + BattleSetup_StartLegendaryBattle, eigen case in
  battle_setup.c). Geen kristallen: 0x3A5-0x3A7 hebben op deze vloer (0x201) een donkere ondergrond.
- Registratie: layouts.json, map_groups.json (achteraan gMapGroup_Spacetime), event_scripts.s, mapsecs + popups,
  wilde Pokemon (achteraan de eerste groep in wild_encounters.json), flags (FLAG_GROUNDED 1120-1159, blok 'lakes'),
  items via nieuwe_items.py (1140-1148).
Idempotent, vaste seeds. Controleert de bereikbaarheid (lopen + surfen) van warps, items en de meerwezens.
Gebruik: python3 tools/grounded/maptools/lakes.py [renderdir]   (render: na make, de tiles.4bpp zijn nodig)"""
import importlib.util, json, math, os, random, re, struct, sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
os.chdir(REPO)
sys.path.insert(0, HERE)
import snowlib as sl                    # M, terrace, hforest, blob, smooth, rect, N (sneeuwnamen)
import nieuwe_items as ni

GROUP = 'gMapGroup_Spacetime'
HUB_DEST = ('SPACETIME_CAVE', 0)        # (oud; zie HUB_WARP)
# terugweg naar het eigen portaal in de meren-kamer: warp-index in de hub (spacetime_cave.py print ze)
HUB_WARP = {'LakeValor': 14, 'LakeAcuity': 16, 'LakeVerity': 18}
LEVEL = 94                              # meerwezens (post-game legendaries ±93-95)
W, H = 48, 42

_spec = importlib.util.spec_from_file_location('dialogen_import', 'tools/dialogen/import.py')
dimp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dimp)


def val(mt, coll, elev):
    return mt | (coll << 10) | (elev << 12)


def read_layout(name):
    L = {l['name']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}[name + '_Layout']
    w, h = L['width'], L['height']
    v = struct.unpack('<%dH' % (w * h), open(L['blockdata_filepath'], 'rb').read())
    return [list(v[y * w:(y + 1) * w]) for y in range(h)]


# ====================================================================== flags (FLAG_GROUNDED 1120-1159)
FLAGS = [
    (1120, 'FLAG_HIDE_LAKE_ACUITY_UXIE', 'Lake Acuity: Uxie gevangen of verslagen (verbergt het object)'),
    (1121, 'FLAG_HIDE_LAKE_VALOR_AZELF', 'Lake Valor: Azelf gevangen of verslagen (verbergt het object)'),
    (1122, 'FLAG_HIDE_LAKE_VERITY_MESPRIT', 'Lake Verity: Mesprit gevangen of verslagen (verbergt het object)'),
    (1123, 'FLAG_LAKE_ACUITY_DONE', 'Lake Acuity: meerwezen afgehandeld (voor de meren-quest in de hub)'),
    (1124, 'FLAG_LAKE_VALOR_DONE', 'Lake Valor: meerwezen afgehandeld (voor de meren-quest in de hub)'),
    (1125, 'FLAG_LAKE_VERITY_DONE', 'Lake Verity: meerwezen afgehandeld (voor de meren-quest in de hub)'),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// lakes { (tools/grounded/maptools/lakes.py; FLAG_GROUNDED 1120-1159: 1120-1125 meren, ' \
          '1140-1148 nieuwe items (nieuwe_items.py), 1126-1139 en 1149-1159 nog vrij)\n'
    for n, name, why in FLAGS:
        assert 1120 <= n <= 1159
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// lakes {' in s:
        i = s.index('// lakes {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// yoshis_island {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)
    ni.flags()


# ====================================================================== General-vijver (Fortree): autotile
# Regels afgeleid van alle vanilla General-kaarten (per 3x3-patroon water/land de meest gekozen tegel):
# boven/links/rechts een rotsrand in de watertegel, onder een graswal (0x002) in de landtegel eronder.
BANK = 0x002


def pond_tile(wet, x, y):
    n, s, w, e = wet(x, y - 1), wet(x, y + 1), wet(x - 1, y), wet(x + 1, y)
    nw, ne, sw, se = wet(x - 1, y - 1), wet(x + 1, y - 1), wet(x - 1, y + 1), wet(x + 1, y + 1)
    if not n:
        if not w:
            return 0xC3 if sw else 0xB0
        if not e:
            return 0xC4 if se else 0xB2
        return 0xB1
    if not w:
        return 0xCC if nw else 0xB8
    if not e:
        return 0xBA
    if not nw:
        return 0xC0
    if not ne:
        return 0xC2
    return 0xA1


def clean_water(cells):
    """Geen landtegels van 1 hoog/breed tussen water, geen water van 1 breed: vult/verwijdert tot het past."""
    cells = set(cells)
    for _ in range(50):
        changed = False
        for y in range(-1, H + 1):
            for x in range(-1, W + 1):
                c = (x, y) in cells
                n, s, w, e = ((x, y - 1) in cells, (x, y + 1) in cells, (x - 1, y) in cells, (x + 1, y) in cells)
                if not c and ((n and s) or (w and e)):
                    cells.add((x, y)); changed = True
                elif c and ((not n and not s) or (not w and not e)):
                    cells.discard((x, y)); changed = True
                elif not c and n and not s:
                    # landtegel onder water (graswal): de tegel eronder mag geen water zijn
                    pass
                # diagonaal: water dat alleen schuin raakt
                for dx, dy in ((1, 1), (-1, 1)):
                    if c and (x + dx, y + dy) in cells and (x + dx, y) not in cells and (x, y + dy) not in cells:
                        cells.add((x + dx, y)); changed = True
        if not changed:
            return cells
    raise SystemExit('water niet glad te krijgen')


def noise_blob(cx, cy, rx, ry, seed, rough=0.16):
    return sl.blob(cx, cy, rx, ry, seed=seed, rough=rough)


# ====================================================================== Valor / Verity (General + Fortree)
MOUND = read_layout('Route120')
MOUND = [MOUND[y][17:22] for y in range(20, 24)]          # 5x4 rotsheuvel met zwemgrot (2af, MB_WATER_DOOR)
MOUND[0][0] = MOUND[0][4] = None                           # hoeken = water (autotile)
_fw = read_layout('FarawayIsland_Interior')
PATCH = [_fw[18][12:14], _fw[19][12:14]]                   # lichte open plek; onderste rij = zuidpijl-warps
_r120 = read_layout('Route120')
ROCKS = [_r120[50][3:5], _r120[51][3:5]]                   # klein rotshoopje (Fortree 230/232/240/242)
GRASS, TALL, LONG, FLOWER, SIGN = 0x001, 0x00D, 0x015, 0x004, 0x01B
TREE = (0x1D4, 0x1D5, 0x1DC, 0x1DD)


class Forest:
    def __init__(self, name, seed, lake, mound_xy, meadows, flowers, rocks):
        self.name, self.rng = name, random.Random(seed)
        self.g = [[val(GRASS, 0, 3) for _ in range(W)] for _ in range(H)]
        self.seed, self.lake_spec, self.mxy, self.meadow_spec = seed, lake, mound_xy, meadows
        self.flower_rate, self.n_rocks, self.lone = flowers, rocks, 0.3
        self.events = set()

    def build(self, events):
        rng, g = self.rng, self.g
        mx, my = self.mxy
        self.mound = {(mx + i, my + j) for j in range(4) for i in range(5) if MOUND[j][i] is not None}
        self.door = (mx + 2, my + 3)
        water = set()
        for spec in self.lake_spec:
            water |= set(noise_blob(*spec))
        water = {p for p in water if 3 <= p[0] < W - 3 and 4 <= p[1] < H - 6}
        water |= {(mx + i, my + j) for j in range(-2, 7) for i in range(-2, 7)}   # ring water rond de heuvel
        K = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
        er = {p for p in water if all((p[0] + dx, p[1] + dy) in water for dx, dy in K)}
        water = {(x + dx, y + dy) for (x, y) in er for dx, dy in K}      # opening: geen uitsteeksels van 1-2 tegels
        water = clean_water(sl.smooth(water))
        self.water = water
        wet = lambda x, y: (x, y) in water
        self.bank = {(x, y + 1) for (x, y) in water if (x, y + 1) not in water}
        # ---- open gebied (geen bomen): meer + marge, weides, corridor naar de aankomst
        AX = W // 2 - 1
        self.arrival = (AX, H - 1)
        open_ = set()
        for (x, y) in water:
            for dx in range(-3, 4):
                for dy in range(-3, 5):
                    open_.add((x + dx, y + dy))
        for spec in self.meadow_spec:
            open_ |= set(noise_blob(*spec))
        open_ |= set(sl.rect(AX - 2, H - 10, AX + 3, H - 1))
        for (x, y) in events:
            open_ |= {(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
        # boomcellen (2x2): een cel is bos als geen van zijn tegels open moet zijn
        CW, CH = W // 2, H // 2
        T = [[all((cx * 2 + i, cy * 2 + j) not in open_ for i in (0, 1) for j in (0, 1)) for cx in range(CW)]
             for cy in range(CH)]
        cell = lambda cx, cy: True if not (0 <= cx < CW and 0 <= cy < CH) else T[cy][cx]
        # losse bomen in de weides: alleen cellen met rondom open cellen (sluit niets af), ver van het water
        evc = {(x // 2, y // 2) for (x, y) in events} | {(AX // 2, cy) for cy in range(CH - 5, CH)}
        for cy in range(1, CH - 1):
            for cx in range(1, CW - 1):
                if T[cy][cx] or (cx, cy) in evc or rng.random() > self.lone:
                    continue
                if any(T[cy + j][cx + i] for i in (-1, 0, 1) for j in (-1, 0, 1)):
                    continue
                if any((cx * 2 + i, cy * 2 + j) in water for i in range(-4, 6) for j in range(-4, 6)):
                    continue
                T[cy][cx] = True
        # kruin (onderste rij van de open cel boven een boom) mag niet op water/wal/events
        for _ in range(10):
            bad = False
            for cy in range(1, CH):
                for cx in range(CW):
                    if T[cy][cx] and not T[cy - 1][cx]:
                        crown = {(cx * 2, cy * 2 - 1), (cx * 2 + 1, cy * 2 - 1)}
                        if crown & (water | self.bank | set(events)):
                            T[cy][cx] = False; bad = True
            if not bad:
                break
        # tegels
        for (x, y) in water:
            if (x, y) in self.mound:
                continue
            if 0 <= x < W and 0 <= y < H:
                g[y][x] = val(pond_tile(wet, x, y), 0, 1)
        for j in range(4):
            for i in range(5):
                if MOUND[j][i] is not None:
                    g[my + j][mx + i] = MOUND[j][i]
        for (x, y) in self.bank:
            if 0 <= x < W and 0 <= y < H:
                g[y][x] = val(BANK, 0, 3)
        self.crowns = set()
        for cy in range(CH):
            for cx in range(CW):
                if not T[cy][cx]:
                    continue
                x, y = cx * 2, cy * 2
                Lf, R, B = cell(cx - 1, cy), cell(cx + 1, cy), cell(cx, cy + 1)
                g[y][x] = val(0x1D4 if Lf else 0x1D6, 1, 0); g[y][x + 1] = val(0x1D5 if R else 0x1D7, 1, 0)
                if B:
                    g[y + 1][x] = val(0x1DC, 1, 0); g[y + 1][x + 1] = val(0x1DD, 1, 0)
                else:
                    g[y + 1][x] = val(0x1E4 if Lf else 0x1E6, 1, 0); g[y + 1][x + 1] = val(0x1E5 if R else 0x1E7, 1, 0)
                if cy > 0 and not T[cy - 1][cx]:
                    g[y - 1][x] = val(0x1CE, 0, 3); g[y - 1][x + 1] = val(0x1CF, 0, 3)
                    self.crowns |= {(x, y - 1), (x + 1, y - 1)}
        self.trees = {(x, y) for y in range(H) for x in range(W) if g[y][x] & 0x3FF in range(0x1D4, 0x1E8)}
        for j in range(2):
            for i in range(2):
                g[H - 2 + j][AX + i] = PATCH[j][i]
        self.patch = {(AX + i, H - 2 + j) for i in (0, 1) for j in (0, 1)}
        self.events = set(events)

    def plain(self, x, y):
        return 0 <= x < W and 0 <= y < H and self.g[y][x] == val(GRASS, 0, 3) and (x, y) not in self.events \
            and (x, y) not in self.crowns and (x, y) not in self.patch

    def decorate(self, tall_blobs, keep):
        g, rng = self.g, self.rng
        keep = set(keep) | self.events
        near_tree = lambda x, y: any((x + dx, y + dy) in self.trees for dx in (-1, 0, 1) for dy in (-1, 0, 1))
        # riet: lang gras op land naast het water (niet op de graswal), in stroken langs de oever
        ph = rng.random() * 6.28
        cx = sum(x for x, _ in self.water) / len(self.water); cy = sum(y for _, y in self.water) / len(self.water)
        for y in range(H):
            for x in range(W):
                if not self.plain(x, y) or (x, y) in keep:
                    continue
                d = min([abs(dx) + abs(dy) for dx in range(-2, 3) for dy in range(0, 3)
                         if (x + dx, y + dy) in self.water] or [9])
                ang = math.atan2(y - cy, x - cx)
                if d <= 2 and math.sin(2 * ang + ph) + 0.5 * math.sin(5 * ang) > -0.1 and (x, y - 1) not in self.water:
                    if d == 1 or rng.random() < 0.55:
                        g[y][x] = val(LONG, 0, 3)
        # hoog gras in de weides (niet direct tegen de bomen)
        for spec in tall_blobs:
            for (x, y) in noise_blob(*spec):
                if self.plain(x, y) and (x, y) not in keep and not near_tree(x, y):
                    g[y][x] = val(TALL, 0, 3)
        # rotshoopjes (2x2) en bloemen
        cands = [(x, y) for y in range(2, H - 3) for x in range(2, W - 3)]
        rng.shuffle(cands)
        placed = 0
        for (x, y) in cands:
            if placed >= self.n_rocks:
                break
            cells = [(x + i, y + j) for i in (0, 1) for j in (0, 1)]
            ring = [(x + i, y + j) for i in range(-1, 3) for j in range(-1, 3)]
            if all(self.plain(*c) and c not in keep for c in ring) and not any(near_tree(*c) for c in cells):
                for j in range(2):
                    for i in range(2):
                        g[y + j][x + i] = ROCKS[j][i]
                placed += 1
                if not self.reach_ok():
                    for j in range(2):
                        for i in range(2):
                            g[y + j][x + i] = val(GRASS, 0, 3)
                    placed -= 1
        spots = [(rng.randrange(3, W - 3), rng.randrange(3, H - 3)) for _ in range(int(self.flower_rate * 400))]
        for (fx, fy) in spots:
            for (x, y) in noise_blob(fx, fy, 1.6, 1.2, rng.randrange(1 << 20), 0.4):
                if self.plain(x, y) and (x, y) not in keep and rng.random() < 0.6:
                    g[y][x] = val(FLOWER, 0, 3)

    def walk(self, surf):
        g = self.g
        start = self.arrival
        seen, q = {start}, deque([start])
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if not (0 <= n[0] < W and 0 <= n[1] < H) or n in seen or n in self.events_solid:
                    continue
                v = g[n[1]][n[0]]
                if (v >> 10) & 3:
                    continue
                if (v >> 12) == 1 and not surf:
                    continue
                seen.add(n); q.append(n)
        return seen

    events_solid = set()

    def reach_ok(self):
        r = self.walk(True)
        return self.door in r and all(any((e[0] + dx, e[1] + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                                      for e in self.events_solid)


# ====================================================================== cavern (kopie Scorched Slab, Cave-paletten)
CRYSTAL = {'blue': (0x3A5,), 'red': (0x3A6, 0x3A7), 'mixed': (0x3A5, 0x3A6, 0x3A7)}
LEGEND_XY, CAVE_BALL, CAVE_ENTRY = (7, 3), (9, 5), (7, 16)


def cavern(kind, seed):
    g = read_layout('ScorchedSlab')
    assert max(t & 0x3FF for r in g for t in r) < 0x3A5      # tot daar zijn scorched_slab en cave gelijk
    for x in (6, 7, 8):                                       # opening naar de Sun Hall dicht
        g[1][x] = 0x0619; g[2][x] = 0x0619
    rng = random.Random(seed)
    w, h = len(g[0]), len(g)

    def reach():
        seen, st = {CAVE_ENTRY}, [CAVE_ENTRY]
        while st:
            x, y = st.pop()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= n[0] < w and 0 <= n[1] < h and n not in seen and not g[n[1]][n[0]] & 0xC00:
                    seen.add(n); st.append(n)
        return seen
    keep = {(LEGEND_XY[0] + dx, LEGEND_XY[1] + dy) for dx in (-1, 0, 1) for dy in (0, 1)} | {CAVE_BALL}
    floor = [(x, y) for y in range(h) for x in range(w) if g[y][x] & 0x3FF == 0x201 and (x, y) not in keep
             and sum(g[y + dy][x + dx] & 0x3FF != 0x201 for dx, dy in ((1, 0), (-1, 0), (0, -1))) >= 1]
    rng.shuffle(floor)
    R = reach(); placed = []
    for (x, y) in floor:
        if len(placed) >= 0:   # kristallen (0x3A5-7) hebben een donkere ondergrond op deze vloer (0x201): uit
            break
        if any(abs(x - a) + abs(y - b) < 3 for a, b in placed):
            continue
        old = g[y][x]
        g[y][x] = rng.choice(CRYSTAL[kind]) | 0x400 | (3 << 12)
        R2 = reach()
        if len(R2) < len(R) - 1 or LEGEND_XY not in R2 and not any((LEGEND_XY[0], LEGEND_XY[1] + 1) == p for p in R2):
            g[y][x] = old; continue
        R = R2; placed.append((x, y))
    R = reach()
    assert (LEGEND_XY[0], LEGEND_XY[1] + 1) in R and CAVE_BALL in R, 'cavern onbereikbaar'
    return g


# ====================================================================== Lake Acuity (sneeuw)
def acuity():
    m = sl.M(W, H)
    rnd = random.Random(480)                       # dexnummer Uxie
    AX = 24
    for y in range(H):
        for x in range(W):
            if rnd.random() < 0.05:
                m.put(x, y, rnd.choice(['snow_dots', 'snow_light', 'tuft0', 'tuft1', 'tuft3']))
    # bergwand bovenin met de grotmond (aankomst)
    TOP = set(sl.rect(-1, -1, W, 4)) | set(sl.rect(15, -1, 33, 7))   # bergwand: zijkanten lager, midden met de grot
    sl.terrace(m, TOP)
    for x, n in zip((AX - 1, AX, AX + 1), ('cliff_front_a', 'cliff_front_b', 'cliff_front_c')):
        m.put(x, 6, n, 1)
    for x, n in zip((AX - 1, AX, AX + 1), ('cave_l', 'cave_door', 'cave_r')):
        m.put(x, 7, n, 1)
    m.put(AX, 7, 'cave_door', 0, 0)
    # meer met eiland; op het eiland een rotsje met een grot
    lake = set(sl.blob(24, 27, 16, 9.5, seed=4801, rough=0.18)) | set(sl.blob(13, 31, 6, 4.5, seed=4802)) | set(sl.blob(24, 26, 13.5, 9.5, seed=4804, rough=0.08))
    lake = {p for p in lake if 3 <= p[0] < W - 3 and 13 <= p[1] < H - 5}
    lake = sl.smooth(lake)
    PL = set(sl.rect(21, 23, 27, 27))              # plateau op het eiland (gezicht 2 rijen: 26-27)
    island = set(sl.blob(24, 26, 7.2, 5, seed=4803, rough=0.28)) | {(x + dx, y + dy) for (x, y) in PL for dx in (-1, 0, 1) for dy in (-1, 0, 1)} | set(sl.rect(22, 28, 26, 29))
    island = sl.smooth(island)
    assert all((x + dx, y + dy) in lake for (x, y) in island for dx in range(-3, 4) for dy in range(-3, 4)), \
        'eiland raakt de oever'
    water = sl.smooth(lake - island)
    m.water(water)
    sl.terrace(m, PL)
    IDOOR = (24, 27)
    for x, n in zip((23, 24, 25), ('cliff_front_a', 'cliff_front_b', 'cliff_front_c')):
        m.put(x, 26, n, 1)
    for x, n in zip((23, 24, 25), ('cave_l', 'cave_door', 'cave_r')):
        m.put(x, 27, n, 1)
    m.put(24, 27, 'cave_door', 0, 0)
    # top van het rotsje: ijs en een kei; op de berg toppen en dennen
    m.put(22, 24, 'ice_crystal', 1); m.put(25, 24, 'rock_snow', 1); m.put(26, 25, 'ice_crystal2', 1)
    topc = lambda x, y: 0 <= x < W and 0 <= y < H and m.g[y][x] == sl.N['cliff_c']
    for (px, py) in [(2, 0), (8, 1), (12, 0), (17, 2), (21, 0), (29, 1), (35, 0), (40, 1), (45, 0), (26, 3)]:
        if all(topc(px + i, py + j) for i in (0, 1) for j in (0, 1)):
            for i in (0, 1):
                for j in (0, 1):
                    m.put(px + i, py + j, 'peak_%d%d' % (i, j), 1)
    for (px, py) in [(5, 0), (15, 0), (31, 2), (38, 0), (19, 3)]:
        if all(topc(px + i, py + j) for i in (0, 1) for j in (0, 1, 2)):
            m.pine(px, py, green=px % 2 == 1)
    SIGN_XY = (AX - 4, 9)                          # de sneeuwpop draagt het bord
    BALL = (8, 38); HIDDEN = (40, 14); BALL2 = None
    EVENTS = {SIGN_XY, BALL, HIDDEN}
    path_keep = set(sl.rect(AX - 1, 8, AX + 1, 13)) | set(sl.rect(23, 28, 25, 28))
    STAIRS = set()

    def free(x, y):
        return 0 <= x < W and 0 <= y < H and m.col[y][x] == 0 and m.elev[y][x] == 3 and m.g[y][x] != sl.N['cave_door']

    def near_water(x, y, r):
        return any((x + dx, y + dy) in water for dx in range(-r, r + 1) for dy in range(-r, r + 1))
    okf = lambda x, y: free(x, y) and (x, y) not in EVENTS and (x, y) not in path_keep and not near_water(x, y, 2) \
        and (x, y) not in island
    BAND = set(sl.rect(0, 5, 3, H - 1)) | set(sl.rect(W - 4, 5, W - 1, H - 1)) | set(sl.rect(0, H - 4, W - 1, H - 1))
    BAND |= set(sl.rect(4, 5, 9, 9)) | set(sl.rect(W - 10, 5, W - 5, 9)) | set(sl.rect(4, H - 8, 9, H - 5)) | \
        set(sl.rect(36, H - 8, W - 5, H - 5))
    sl.hforest(m, BAND, okf)
    HT = {sl.N[k] for k in sl.N if k.startswith('htree')}
    near_tree = lambda x, y: any(0 <= x + dx < W and 0 <= y + dy < H and m.g[y + dy][x + dx] in HT
                                 for dx in (-1, 0, 1) for dy in (-1, 0, 1))
    # hoog sneeuwgras
    for c, seed in [((10, 19, 3.5, 3), 1), ((38, 20, 3.5, 3.5), 2), ((33, 37, 4, 2), 3), ((14, 37, 3, 2), 4),
                    ((41, 31, 2.5, 3), 5)]:
        for (x, y) in sl.blob(*c, seed=seed):
            if free(x, y) and (x, y) not in EVENTS and (x, y) not in path_keep and not near_tree(x, y) \
                    and not near_water(x, y, 0):
                m.put(x, y, 'grass_snow', 0)
    # dennen en decor (nooit iets afsluiten)
    def pine(x, y):
        cells = [(x + dx, y + dy) for dx in range(2) for dy in range(3)]
        if all(free(*c) and c not in EVENTS and c not in path_keep and not near_water(*c, 1) and
               m.g[c[1]][c[0]] != sl.N['grass_snow'] for c in cells):
            m.pine(x, y, green=rnd.random() < 0.35)
    for (x, y) in [(9, 9), (14, 10), (33, 9), (39, 10), (42, 15), (5, 15), (5, 24), (42, 25), (11, 33), (30, 37),
                   (20, 37), (39, 35), (17, 11)]:
        pine(x, y)
        if not acuity_reach(m, water, AX, IDOOR, EVENTS):
            for dx in range(2):
                for dy in range(3):
                    m.put(x + dx, y + dy, 'snow', 0, 3)
    BLOCK = ['rock_snow', 'rock_snow2', 'rock_cluster', 'ice_rock', 'ice_crystal', 'ice_crystal2', 'snowball', 'stump', 'log']
    SOFT = ['flowers_blue', 'tuft2', 'tuft4', 'tuft6', 'tuft7', 'snow_deep', 'snow_deep2']
    cands = [(x, y) for y in range(9, H) for x in range(W) if free(x, y)]
    rnd.shuffle(cands)
    for (x, y) in cands:
        if not free(x, y) or (x, y) in EVENTS or (x, y) in path_keep or m.g[y][x] == sl.N['grass_snow']:
            continue
        r = rnd.random()
        clear = all((x + dx, y + dy) not in EVENTS and (x + dx, y + dy) not in path_keep for dx in (-1, 0, 1) for dy in (-1, 0, 1))
        if r < 0.05 and clear and not near_water(x, y, 0) and (x, y) not in island:
            old = m.g[y][x]
            m.put(x, y, rnd.choice(BLOCK), 1)
            if not acuity_reach(m, water, AX, IDOOR, EVENTS):
                m.put(x, y, old, 0)
        elif r < 0.12:
            m.put(x, y, rnd.choice(SOFT), 0)
    # een sneeuwpop die naar het meer kijkt (tegen de bergwand, uit de weg)
    m.put(SIGN_XY[0], SIGN_XY[1], 'snowman', 1)
    assert acuity_reach(m, water, AX, IDOOR, EVENTS), 'Lake Acuity: iets onbereikbaar'
    return m, dict(arrival=(AX, 7), idoor=IDOOR, sign=SIGN_XY, ball=BALL, hidden=HIDDEN, water=water)


def acuity_reach(m, water, AX, IDOOR, EVENTS):
    start = (AX, 8)
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if not (0 <= n[0] < W and 0 <= n[1] < H) or n in seen:
                continue
            if m.col[n[1]][n[0]] or n in EVENTS - {start}:
                continue
            seen.add(n); q.append(n)
    adj = lambda p: any((p[0] + dx, p[1] + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    return IDOOR in seen and all(adj(e) for e in EVENTS) and (AX, 7) in seen | {(AX, 7)}


# ====================================================================== registratie
MAPS = [  # (naam, const, mapsec, muziek, weer, type)
    ('LakeAcuity', 'LAKE_ACUITY', 'MAPSEC_LAKE_ACUITY', 'MUS_RG_SEVII_ROUTE', 'WEATHER_SNOW', 'MAP_TYPE_ROUTE'),
    ('LakeAcuity_Cavern', 'LAKE_ACUITY_CAVERN', 'MAPSEC_LAKE_ACUITY', 'MUS_RG_SEVII_CAVE', 'WEATHER_NONE', 'MAP_TYPE_UNDERGROUND'),
    ('LakeValor', 'LAKE_VALOR', 'MAPSEC_LAKE_VALOR', 'MUS_RG_ROUTE24', 'WEATHER_NONE', 'MAP_TYPE_ROUTE'),
    ('LakeValor_Cavern', 'LAKE_VALOR_CAVERN', 'MAPSEC_LAKE_VALOR', 'MUS_RG_SEVII_CAVE', 'WEATHER_NONE', 'MAP_TYPE_UNDERGROUND'),
    ('LakeVerity', 'LAKE_VERITY', 'MAPSEC_LAKE_VERITY', 'MUS_RG_ROUTE1', 'WEATHER_SUNNY', 'MAP_TYPE_ROUTE'),
    ('LakeVerity_Cavern', 'LAKE_VERITY_CAVERN', 'MAPSEC_LAKE_VERITY', 'MUS_RG_SEVII_CAVE', 'WEATHER_NONE', 'MAP_TYPE_UNDERGROUND'),
]
MAPSECS = [('MAPSEC_LAKE_ACUITY', 'LAKE ACUITY', 'MAPPOPUP_THEME_MARBLE'),
           ('MAPSEC_LAKE_VALOR', 'LAKE VALOR', 'MAPPOPUP_THEME_WOOD'),
           ('MAPSEC_LAKE_VERITY', 'LAKE VERITY', 'MAPPOPUP_THEME_WOOD')]


def register_layout(name, const, w, h, secondary):
    lj = open('data/layouts/layouts.json').read()
    entry = '''    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, w, h, secondary, name, name)
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"id": "LAYOUT_%s"' % const); s = lj.rindex('    {', 0, i); e = lj.index('    }', i) + 5
        lj = lj[:s] + entry + lj[e:]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    json.loads(lj)
    open('data/layouts/layouts.json', 'w').write(lj)


def save_layout(name, const, g, border, secondary):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', v) for r in g for v in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *border))
    register_layout(name, const, len(g[0]), len(g), secondary)


def register_maps():
    g = open('data/maps/map_groups.json').read()
    i = g.index('"%s": [' % GROUP); j = g.index(']', i)
    for name, *_ in MAPS:
        if '"%s"' % name not in g[i:j]:
            k = g.rindex('"', i, j) + 1
            g = g[:k] + ',\n    "%s"' % name + g[k:]
            j = g.index(']', i)
    grp = re.findall(r'"([^"]+)"', g[g.index('[', i):j])
    assert len(grp) <= 128, len(grp)
    json.loads(g)
    open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    for name, *_ in MAPS:
        inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
        if inc not in es:
            a = '\t.include "data/maps/SpacetimeCave/scripts.inc"\n'
            es = es.replace(a, a + inc, 1)
    open('data/event_scripts.s', 'w').write(es)


def mapsecs():
    p = 'src/data/region_map/region_map_sections.json'
    s = open(p).read()
    for mid, nm, _ in MAPSECS:
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
    for mid, nm, theme in MAPSECS:
        if '[%s - KANTO' % mid not in s:
            s = s.replace(a, a + '    [%s - KANTO_MAPSEC_COUNT] = %s, // Project Grounded: %s\n' % (mid, theme, nm.title()), 1)
            s = s.replace(b, b + '    [%s - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: %s\n'
                          % (mid, nm.title()), 1)
    open(p, 'w').write(s)


def battle_setup():
    p = 'src/battle_setup.c'
    s = open(p).read()
    if 'case SPECIES_UXIE:' in s:
        return
    a = '    case SPECIES_CELEBI: // Project Grounded: Ilex Forest'
    i = s.index(a); j = s.index('break;\n', i) + len('break;\n')
    s = s[:j] + ('    case SPECIES_UXIE: // Project Grounded: de Gen 4-meren in de Spacetime Cave (placeholder: Kanto-legendary-thema, rimpelingen)\n'
                 '    case SPECIES_MESPRIT:\n    case SPECIES_AZELF:\n'
                 '        CreateBattleStartTask(B_TRANSITION_RIPPLE, MUS_RG_VS_LEGEND);\n        break;\n') + s[j:]
    open(p, 'w').write(s)


# ---------------------------------------------------------------- wilde Pokemon
WILD = {
    'LAKE_ACUITY': dict(
        land=(20, [('ABOMASNOW', 91, 93), ('BEARTIC', 91, 93), ('WEAVILE', 91, 93), ('MAMOSWINE', 91, 93),
                   ('MEDICHAM', 91, 93), ('FROSLASS', 91, 93), ('GLALIE', 91, 93), ('ALAKAZAM', 91, 93),
                   ('BRONZONG', 92, 93), ('AVALUGG', 92, 93), ('GALLADE', 93, 93), ('URSALUNA', 93, 93)]),
        water=(4, [('GOLDUCK', 91, 93), ('DEWGONG', 91, 93), ('QUAGSIRE', 91, 93), ('WALREIN', 92, 93),
                   ('GYARADOS', 93, 93)]),
        fishing=(25, [('SEAKING', 88, 90), ('WHISCASH', 88, 90), ('BASCULIN', 90, 92), ('POLIWRATH', 90, 92),
                      ('CLOYSTER', 90, 92), ('GOLDUCK', 91, 93), ('DEWGONG', 91, 93), ('QUAGSIRE', 91, 93),
                      ('GYARADOS', 92, 94), ('MILOTIC', 93, 94)])),
    'LAKE_VALOR': dict(
        land=(20, [('STARAPTOR', 91, 93), ('LUXRAY', 91, 93), ('FARIGIRAF', 91, 93), ('HOUNDOOM', 91, 93),
                   ('RHYPERIOR', 91, 93), ('ZANGOOSE', 91, 93), ('SEVIPER', 91, 93), ('HONCHKROW', 91, 93),
                   ('LUCARIO', 92, 93), ('SKUNTANK', 92, 93), ('GARCHOMP', 93, 93), ('TYRANITAR', 93, 93)]),
        water=(4, [('BIBAREL', 91, 93), ('FLOATZEL', 91, 93), ('GASTRODON', 91, 93), ('POLIWRATH', 92, 93),
                   ('GYARADOS', 93, 93)]),
        fishing=(25, [('SEAKING', 88, 90), ('WHISCASH', 88, 90), ('BASCULIN', 90, 92), ('CRAWDAUNT', 90, 92),
                      ('GASTRODON', 90, 92), ('FLOATZEL', 91, 93), ('LUMINEON', 91, 93), ('BIBAREL', 91, 93),
                      ('GYARADOS', 92, 94), ('MILOTIC', 93, 94)])),
    'LAKE_VERITY': dict(
        land=(20, [('BIBAREL', 91, 93), ('ROSERADE', 91, 93), ('LOPUNNY', 91, 93), ('AMBIPOM', 91, 93),
                   ('KRICKETUNE', 91, 93), ('PACHIRISU', 91, 93), ('MR_MIME', 91, 93), ('VESPIQUEN', 91, 93),
                   ('MOTHIM', 92, 93), ('CHERRIM', 92, 93), ('TOGEKISS', 93, 93), ('ESPEON', 93, 93)]),
        water=(4, [('GOLDUCK', 91, 93), ('AZUMARILL', 91, 93), ('POLITOED', 91, 93), ('QUAGSIRE', 92, 93),
                   ('GYARADOS', 93, 93)]),
        fishing=(25, [('SEAKING', 88, 90), ('WHISCASH', 88, 90), ('BASCULIN', 90, 92), ('POLITOED', 90, 92),
                      ('AZUMARILL', 90, 92), ('LUMINEON', 91, 93), ('GOLDUCK', 91, 93), ('QUAGSIRE', 91, 93),
                      ('GYARADOS', 92, 94), ('MILOTIC', 93, 94)])),
}


def wild():
    p = 'src/data/wild_encounters.json'
    s = open(p).read()
    for mp, tabs in WILD.items():
        lbl = 'g' + ''.join(w.title() for w in mp.split('_'))
        e = {'map': 'MAP_' + mp, 'base_label': lbl}
        for kind in ('land', 'water', 'fishing'):
            rate, spec = tabs[kind]
            assert len(spec) == {'land': 12, 'water': 5, 'fishing': 10}[kind]
            assert len({x[0] for x in spec}) == len(spec), ('dubbele soort', mp, kind)
            e[kind + '_mons'] = {'encounter_rate': rate,
                                 'mons': [{'min_level': a, 'max_level': b, 'species': 'SPECIES_' + sp} for sp, a, b in spec]}
        blob = '\n'.join('        ' + ln for ln in json.dumps(e, indent=2).split('\n'))
        key = '"map": "MAP_%s"' % mp
        if key in s:
            i = s.index(key); a = s.rindex('{', 0, i)
        else:
            i = s.rindex('"map": "MAP_'); a = s.rindex('{', 0, i)
        depth, j = 0, a
        while True:
            if s[j] == '{': depth += 1
            elif s[j] == '}':
                depth -= 1
                if depth == 0: break
            j += 1
        if key in s:
            s = s[:a] + blob.lstrip() + s[j + 1:]
        else:
            s = s[:j + 1] + ',\n' + blob + s[j + 1:]
    json.loads(s)
    open(p, 'w').write(s)


# ---------------------------------------------------------------- map.json + scripts
def warp(x, y, dest, wid, elev=0):
    return {'x': x, 'y': y, 'elevation': elev, 'dest_map': 'MAP_' + dest, 'dest_warp_id': str(wid)}


def obj(gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', lid=None, item=None, elev=3):
    o = {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move, 'movement_range_x': 0,
         'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': item or '0',
         'script': script, 'flag': flag}
    return dict(local_id=lid, **o) if lid else o


def ball(x, y, it, flag):
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', flag, 'MOVEMENT_TYPE_LOOK_AROUND', item=it)


def write_map(name, const, mapsec, music, weather, mtype, objs, warps, bgs, show=True):
    mj = {'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + const, 'music': music,
          'region_map_section': mapsec, 'requires_flash': False, 'weather': weather, 'map_type': mtype,
          'allow_cycling': mtype == 'MAP_TYPE_ROUTE', 'allow_escaping': False, 'allow_running': True,
          'show_map_name': show, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
          'object_events': objs, 'warp_events': warps, 'coord_events': [], 'bg_events': bgs}
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')


def text(label, s):
    out = '%s:\n' % label
    for part in dimp.to_strings(s):
        out += '\t.string "%s"\n' % part
    return out + '\n'


def write_scripts(name, header, code, texts):
    s = header.rstrip('\n') + '\n\n' + code.strip('\n') + '\n\n@ ' + '-' * 64 + \
        ' teksten (placeholders, Jordi herschrijft ze)\n' + ''.join(text(name + '_Text_' + k, v) for k, v in texts)
    open('data/maps/%s/scripts.inc' % name, 'w').write(s.rstrip('\n') + '\n')


LEGENDS = {  # meer -> (soort, flag, done-flag, kristal, teksten)
    'LakeAcuity': ('UXIE', 'FLAG_HIDE_LAKE_ACUITY_UXIE', 'FLAG_LAKE_ACUITY_DONE', 'blue',
                   "A small yellow being floats above the water with its eyes shut.\n\nIt is said that meeting its gaze "
                   "wipes your memory. It already knows this about you. It knows a lot about you. It is being polite "
                   "about the browser history."),
    'LakeValor': ('AZELF', 'FLAG_HIDE_LAKE_VALOR_AZELF', 'FLAG_LAKE_VALOR_DONE', 'red',
                  "A small blue being hovers in the dark, perfectly still.\n\nIt is the embodiment of willpower. It has "
                  "been waiting here for a challenger for about four thousand years, out of sheer stubbornness."),
    'LakeVerity': ('MESPRIT', 'FLAG_HIDE_LAKE_VERITY_MESPRIT', 'FLAG_LAKE_VERITY_DONE', 'mixed',
                   "A small pink being drifts over the water, humming.\n\nIt is the embodiment of emotion. It looks at "
                   "you and starts crying, then laughing, then crying again. It is having your feelings for you. "
                   "You're welcome."),
}
SIGNS = {
    'LakeAcuity': "LAKE ACUITY\n\n“Knowledge sleeps beneath the ice. Do not wake it before it has had its coffee.”\n\n"
                  "Below, scratched in later: “The ice is fake. It was installed on Tuesday.”",
    'LakeValor': "LAKE VALOR\n\n“Here sleeps the spirit of willpower. Those who wish to meet it must swim.”\n\n"
                 "Below, smaller: “The spirit of willpower lives on an island. It has never once swum.”",
    'LakeVerity': "LAKE VERITY\n\n“Here sleeps the spirit of emotion. Please lower your voice. It will lower its voice "
                  "too, and then cry about it.”",
}
ARRIVE_TEXT = {
    'LakeAcuity': "The cave behind you hums. That's the rift back to the SPACETIME CAVE.\n\nIt is extremely cold here. "
                  "Somewhere a dimension is saving on heating.",
    'LakeValor': "The shimmering patch behind you is the rift back to the SPACETIME CAVE.\n\nStep on it and walk south "
                 "if you lose your nerve. Nobody here will judge you. Except AZELF.",
    'LakeVerity': "The shimmering patch behind you is the rift back to the SPACETIME CAVE.\n\nThe air smells like a "
                  "picnic you were never invited to.",
}
CAVE_TEXT = {
    'LakeAcuity': "The cave is flooded. Of course it is.",
    'LakeValor': "The cave is flooded. AZELF could have picked dry land. It picked drama.",
    'LakeVerity': "The cave is flooded. With water. And, faintly, with feelings.",
}


def legend_scripts(name, species, lid, flag, done, look):
    P = name + '_EventScript_'
    T = name + '_Text_'
    return f'''{P}{species.title()}::
	lock
	faceplayer
	msgbox {T}Legend, MSGBOX_DEFAULT
	playmoncry SPECIES_{species}, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_{species}, {LEVEL}
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}LegendStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}LegendStays
	removeobject {lid}
	setflag {flag}
	setflag {done}
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}LegendCaught
	msgbox {T}LegendFled, MSGBOX_DEFAULT
	release
	end

{P}LegendCaught::
	msgbox {T}LegendCaught, MSGBOX_DEFAULT
	release
	end

{P}LegendStays::
	release
	end
'''


AFTER = {
    'LakeAcuity': ("You caught UXIE. You will remember this forever. Probably. Ask UXIE.",
                   "UXIE fades away. You feel like you forgot something. You did. You forgot to catch it."),
    'LakeValor': ("You caught AZELF. It looks very brave inside the ball. From a safe distance.",
                  "AZELF vanishes. It wasn't scared. It just had a thing. A brave thing. Elsewhere."),
    'LakeVerity': ("You caught MESPRIT. It is already crying about how happy it is.",
                   "MESPRIT vanishes in a puff of mixed feelings. Mostly yours."),
}


def main():
    flags()
    mapsecs()
    battle_setup()
    wild()
    info = {}
    # ---------------- Acuity
    m, A = acuity()
    save_layout('LakeAcuity', 'LAKE_ACUITY', [[m.bin()[y * W + x] for x in range(W)] for y in range(H)],
                struct.unpack('<4H', open('data/layouts/Route136/border.bin', 'rb').read()), 'gTileset_Snow')
    info['LakeAcuity'] = (m.g, A)
    lakes = {}
    lakes['LakeAcuity'] = dict(arrival_warps=[warp(A['arrival'][0], A['arrival'][1], 'SPACETIME_CAVE', HUB_WARP['LakeAcuity'])],
                               door=A['idoor'], door_elev=0, sign=A['sign'], ball=A['ball'], hidden=A['hidden'],
                               arrive_tile=(A['arrival'][0], A['arrival'][1] + 1))
    # ---------------- Valor / Verity
    SPECS = {
        'LakeValor': dict(seed=482, lake=[(24, 19, 13, 8.5, 4821, 0.2), (14, 23, 5, 4, 4822, 0.2)], mound=(22, 16),
                          meadows=[(10, 33, 7, 4, 4823), (37, 32, 7, 5, 4824), (8, 10, 4, 4, 4825), (40, 9, 4, 4, 4826)],
                          tall=[(9, 33, 4, 2.5, 4827), (38, 33, 4, 3, 4828), (40, 9, 2.5, 2.5, 4829)],
                          flowers=0.015, rocks=5, ball=(6, 9), hidden=(41, 35)),
        'LakeVerity': dict(seed=481, lake=[(25, 17, 12, 7, 4811, 0.22), (16, 22, 7, 5, 4812, 0.25), (32, 23, 5, 4, 4810, 0.2)], mound=(21, 15),
                           meadows=[(12, 33, 8, 4, 4813), (37, 34, 6, 4, 4814), (7, 16, 4, 6, 4815), (42, 12, 3, 4, 4816)],
                           tall=[(12, 34, 5, 2.5, 4817), (7, 17, 2.5, 3.5, 4818), (37, 35, 3, 2, 4819)],
                           flowers=0.07, rocks=2, ball=(42, 11), hidden=(6, 20)),
    }
    for name, sp in SPECS.items():
        f = Forest(name, sp['seed'], sp['lake'], sp['mound'], sp['meadows'], sp['flowers'], sp['rocks'])
        AX = W // 2 - 1
        sign = (AX + 3, H - 3)
        ev = [sp['ball'], sign]
        f.build(ev + [sp['hidden']])
        f.events_solid = {sp['ball'], sign}
        f.g[sign[1]][sign[0]] = val(SIGN, 1, 3)
        assert f.reach_ok(), (name, 'onbereikbaar na build')
        f.decorate(sp['tall'], keep={sp['hidden']} | set(sl.rect(AX - 1, H - 6, AX + 2, H - 1)))
        r = f.walk(True)
        assert f.door in r and sp['hidden'] in r and f.reach_ok(), (name, 'onbereikbaar')
        land = f.walk(False)
        assert all(any((e[0] + dx, e[1] + dy) in land for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                   for e in f.events_solid) and sp['hidden'] in land, (name, 'items alleen via water')
        # uitzicht: geen tegel van de heuvel tegen land
        assert all((x + dx, y + dy) in f.water for (x, y) in f.mound for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if (x + dx, y + dy) not in f.mound), (name, 'heuvel raakt land')
        save_layout(name, name.upper().replace('LAKE', 'LAKE_'), f.g, tuple(val(t, 1, 0) for t in TREE), 'gTileset_Fortree')
        info[name] = (f.g, f)
        lakes[name] = dict(arrival_warps=[warp(AX, H - 1, 'SPACETIME_CAVE', HUB_WARP[name]), warp(AX + 1, H - 1, 'SPACETIME_CAVE', HUB_WARP[name] + 1)],
                           door=f.door, door_elev=1, sign=sign, ball=sp['ball'], hidden=sp['hidden'],
                           arrive_tile=(AX, H - 2))
        print('%s: %d water, %d bomen, deur %s' % (name, len(f.water), len(f.trees), f.door))
    # ---------------- caverns + map.json + scripts
    for (name, const, mapsec, music, weather, mtype) in MAPS:
        if name.endswith('_Cavern'):
            continue
        lake = lakes[name]
        species, flag, done, crystal, legend_text = LEGENDS[name]
        cname, cconst = name + '_Cavern', const + '_CAVERN'
        lake_items = ni.items(name); cave_items = ni.items(cname)
        balls = [(fl, it) for fl, it, q, h in lake_items if not h]
        hids = [(fl, it) for fl, it, q, h in lake_items if h]
        assert len(balls) == 1 and len(hids) == 1 and len(cave_items) == 1, (name, lake_items, cave_items)
        # meer
        warps = lake['arrival_warps'] + [warp(lake['door'][0], lake['door'][1], cconst, 0, lake['door_elev'])]
        door_idx = len(warps) - 1
        objs = [ball(lake['ball'][0], lake['ball'][1], balls[0][1], balls[0][0])]
        bgs = [{'type': 'sign', 'x': lake['sign'][0], 'y': lake['sign'][1], 'elevation': 0,
                'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY', 'script': name + '_EventScript_Sign'},
               {'type': 'hidden_item', 'x': lake['hidden'][0], 'y': lake['hidden'][1], 'elevation': 3,
                'item': hids[0][1], 'flag': hids[0][0]}]
        write_map(name, const, mapsec, music, weather, mtype, objs, warps, bgs)
        P = name + '_EventScript_'
        write_scripts(name, '@ Project Grounded: %s (gegenereerd door tools/grounded/maptools/lakes.py; niet met de hand '
                            'bewerken, teksten via de Dialoogstudio)\n%s_MapScripts::\n\t.byte 0\n' % (name, name),
                      f'{P}Sign::\n\tmsgbox {name}_Text_Sign, MSGBOX_SIGN\n\tend\n',
                      [('Sign', SIGNS[name] + '\n\n' + ARRIVE_TEXT[name])])
        # grot
        g = cavern(crystal, {'LakeAcuity': 480, 'LakeValor': 482, 'LakeVerity': 481}[name])
        save_layout(cname, cconst, g, struct.unpack('<4H', open('data/layouts/ScorchedSlab/border.bin', 'rb').read()),
                    'gTileset_Cave')
        lid = 'LOCALID_%s_%s' % (cconst, species)
        cobjs = [obj('OBJ_EVENT_GFX_SPECIES(%s)' % species, LEGEND_XY[0], LEGEND_XY[1], name + '_Cavern_EventScript_' + species.title(),
                     flag, lid=lid),
                 ball(CAVE_BALL[0], CAVE_BALL[1], cave_items[0][1], cave_items[0][0])]
        cwarps = [warp(CAVE_ENTRY[0], CAVE_ENTRY[1], const, door_idx, 1)]
        cbgs = [{'type': 'sign', 'x': 5, 'y': 2, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_NORTH',
                 'script': cname + '_EventScript_Wall'}]
        write_map(cname, cconst, mapsec, music_for(cname), 'WEATHER_NONE', 'MAP_TYPE_UNDERGROUND', cobjs, cwarps, cbgs, show=False)
        caught, fled = AFTER[name]
        code = legend_scripts(cname, species, lid, flag, done, legend_text) + \
            f'\n{cname}_EventScript_Wall::\n\tmsgbox {cname}_Text_Wall, MSGBOX_SIGN\n\tend\n'
        write_scripts(cname, '@ Project Grounded: %s (gegenereerd door tools/grounded/maptools/lakes.py)\n'
                             '%s_MapScripts::\n\t.byte 0\n' % (cname, cname), code,
                      [('Legend', legend_text), ('LegendCaught', caught), ('LegendFled', fled),
                       ('Wall', CAVE_TEXT[name] + "\n\nSomeone carved a message into the rock: “BACK IN 5 MINUTES.” "
                                                  "The rock is several thousand years old.")])
        lakes[name]['door_idx'] = door_idx
    register_maps()
    for name in ('LakeAcuity', 'LakeValor', 'LakeVerity'):
        a = lakes[name]['arrival_warps'][0]
        print('%s: aankomst/terugweg = warp 0 (%d,%d), grot = warp %d' % (name, a['x'], a['y'], lakes[name]['door_idx']))
    return info, lakes


def music_for(cname):
    return [m[3] for m in MAPS if m[0] == cname][0]


def render(info, outdir):
    from gridrender import render as grender
    from PIL import Image
    os.makedirs(outdir, exist_ok=True)
    ims = []
    for name, sec in (('LakeAcuity', 'snow'), ('LakeValor', 'fortree'), ('LakeVerity', 'fortree')):
        g = read_layout(name)
        im = grender(g, 'general', sec, 1)
        im.save(os.path.join(outdir, name + '.png')); ims.append(im)
        c = read_layout(name + '_Cavern')
        ci = grender(c, 'general', 'cave', 1)
        ci.save(os.path.join(outdir, name + '_Cavern.png')); ims.append(ci)
    tw = sum(i.width for i in ims[::2]) + 16 * 2
    th = max(i.height for i in ims[::2]) + max(i.height for i in ims[1::2]) + 16
    ov = Image.new('RGB', (tw, th), (20, 20, 28))
    x = 0
    for k in range(3):
        a, b = ims[2 * k], ims[2 * k + 1]
        ov.paste(a, (x, 0)); ov.paste(b, (x + (a.width - b.width) // 2, a.height + 16)); x += a.width + 16
    ov.save(os.path.join(outdir, 'overzicht.png'))
    print('render:', outdir)


if __name__ == '__main__':
    info, lakes = main()
    if len(sys.argv) > 1:
        render(info, sys.argv[1])
