"""Project Grounded: drie nieuwe Safari Zone-gebieden, elk met een eigen tileset (zie safari_tilesets.py).

- SafariZone_FairyForest (44x40): betoverd feeënbos, pastel; ingang in de westrand van SafariZone_Southwest (0,30).
- SafariZone_ThunderPlains (48x40): dorre savanne onder onweer, acacia's (Route 113-bomen); grot in de bergwand van
  SafariZone_Northeast (24,7).
- SafariZone_HauntedCamp (44x40): vervallen kampeerterrein in de mist, oud rusthuis, kapotte lantaarns; ingang in de
  westrand van SafariZone_Northwest (0,28).

Bouwt (idempotent, vaste seed): tilesets, map.bin/border.bin, map.json's van de nieuwe kaarten, de openingen + warps +
afzettingen (Safari-medewerker, verdwijnt met FLAG_SAFARI_ZONES_OPEN) in de bestaande Safari-kaarten, en registreert
layouts.json, map_groups.json (gMapGroup_Grounded) en event_scripts.s. Controleert de bereikbaarheid van alle events.
De scripts.inc's staan met de hand in data/maps/SafariZone_*.

Gebruik: python3 tools/grounded/maptools/safari_zones.py [uitmap-voor-renders]"""
import json, math, os, random, struct, subprocess, sys
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import safari_tilesets

NEW = safari_tilesets.build()
LILY_WEST = NEW['lilycove_west_arrow']


def val(mt, coll, elev):
    return mt | (coll << 10) | (elev << 12)


class Zone:
    def __init__(self, w, h, seed):
        self.W, self.H = w, h
        self.rng = random.Random(seed)
        self.T = [['T'] * w for _ in range(h)]

    def inb(self, x, y):
        return 0 <= x < self.W and 0 <= y < self.H

    def k(self, x, y):
        return self.T[y][x] if self.inb(x, y) else 'T'

    def disc(self, cx, cy, r, kind='g', only=None):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if 1 <= x < self.W - 1 and 1 <= y < self.H - 1 and (x - cx) ** 2 + ((y - cy) * 1.15) ** 2 <= r * r:
                    if only is None or self.T[y][x] in only:
                        self.T[y][x] = kind

    def blob(self, cx, cy, r, kind, only=None, n=5):
        self.disc(cx, cy, r, kind, only)
        for _ in range(n):
            a = self.rng.random() * 2 * math.pi
            d = r * (0.4 + 0.5 * self.rng.random())
            self.disc(cx + math.cos(a) * d, cy + math.sin(a) * d, r * (0.45 + 0.3 * self.rng.random()), kind, only)

    def path(self, pts, w=2, kind='g'):
        """Pad door de waypoints; vakken x..x+w-1 en y..y+w-1 vanaf het punt (vierkante kwast)."""
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(abs(x1 - x0), abs(y1 - y0)) * 3 + 1
            for i in range(n + 1):
                t = i / n
                x = int(math.floor(x0 + (x1 - x0) * t + 0.5))
                y = int(math.floor(y0 + (y1 - y0) * t + 0.5))
                for dy in range(w):
                    for dx in range(w):
                        if 1 <= x + dx < self.W - 1 and 1 <= y + dy < self.H - 1:
                            self.T[y + dy][x + dx] = kind

    def rect(self, x0, y0, x1, y1, kind):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.T[y][x] = kind

    def tidy(self):
        """Losse bosvakjes van 1 hoog tussen twee open vakken openen (rommelig)."""
        for _ in range(2):
            for y in range(1, self.H - 1):
                for x in range(1, self.W - 1):
                    if self.T[y][x] == 'T' and self.T[y - 1][x] != 'T' and self.T[y + 1][x] != 'T':
                        self.T[y][x] = 'g'

    def bfs(self, starts, ok):
        seen, q = set(starts), deque(starts)
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if self.inb(*n) and n not in seen and ok(*n):
                    seen.add(n)
                    q.append(n)
        return seen


def show(z, walk=()):
    for y in range(z.H):
        print('%2d ' % y + ''.join('.' if (x, y) in walk and z.T[y][x] == 'g' else z.T[y][x] for x in range(z.W)))


def near(x, y, s):
    return any((x + dx, y + dy) in s for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


# ---------------------------------------------------------------- autotiling met de bomen van General (bos)
GRASS, TALL, BANK, FLOWER, ROCK, SIGN = 0x001, 0x00D, 0x002, 0x004, 0x0E0, 0x01B
FOREST, TRUNK, CANOPY = (0x0C6, 0x0C7), (0x016, 0x017), (0x00E, 0x00F)
HOUSE = [[0x008, 0x009, 0x009, 0x00A], [0x010, 0x011, 0x011, 0x012], [0x018, 0x019, 0x00B, 0x01A],
         [0x020, 0x021, 0x013, 0x022]]


def forest_tiles(z, extra):
    """T bos, w vijver, g gras, L hoog gras, f bloemen, r rots, s bord; extra: soort -> (metatile(s), botsing)."""
    rng, H, W = z.rng, z.H, z.W
    M = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            k = z.T[y][x]
            below = z.k(x, y + 1) if y + 1 < H else 'T'
            if k == 'T':
                M[y][x] = val(rng.choice(TRUNK) if below != 'T' else rng.choice(FOREST), 1, 0)
            elif k == 'w':
                up, lf, rt = z.k(x, y - 1) != 'w', z.k(x - 1, y) != 'w', z.k(x + 1, y) != 'w'
                ul, ur = z.k(x - 1, y - 1) != 'w', z.k(x + 1, y - 1) != 'w'
                if up:
                    mt = 0xB0 if lf else 0xB2 if rt else 0xB1
                elif lf:
                    mt = 0xB8
                elif rt:
                    mt = 0xBA
                elif ul:
                    mt = 0xC0
                elif ur:
                    mt = 0xC2
                else:
                    mt = 0xA1
                M[y][x] = val(mt, 0, 1)
            elif below == 'T' and k in 'gLfGk':
                M[y][x] = val(rng.choice(CANOPY), 0, 3)          # boomkruin van de boom eronder
            elif k == 'L':
                M[y][x] = val(TALL, 0, 3)
            elif k == 'f':
                M[y][x] = val(FLOWER, 0, 3)
            elif k == 'r':
                M[y][x] = val(ROCK, 1, 3)
            elif k == 's':
                M[y][x] = val(SIGN, 1, 3)
            elif k in extra:
                mts, coll = extra[k]
                M[y][x] = val(rng.choice(mts) if isinstance(mts, (list, tuple)) else mts, coll, 3)
            else:
                M[y][x] = val(BANK if z.k(x, y - 1) == 'w' else GRASS, 0, 3)
    return M


def pond(z, x0, y0, x1, y1):
    z.rect(x0, y0, x1, y1, 'w')
    z.rect(x0, y1 + 1, x1, y1 + 1, 'g')          # oevertegel onder het water


# ================================================================ FAIRY FOREST
def build_fairy():
    z = Zone(44, 40, 670)                        # Floette
    EX = (43, 21)
    z.path([(42, 21), (36, 20)], 2)
    z.T[21][43] = 'g'
    z.T[22][43] = 'g'
    z.disc(22, 21, 9.0)                          # open plek met de vijver
    z.path([(36, 21), (29, 21)], 2)
    z.path([(20, 14), (18, 10)], 2)              # naar de bloemenweide (noord)
    z.blob(15, 7, 5.4, 'g')
    z.path([(35, 21), (34, 15), (34, 11)], 2)    # open plek noordoost
    z.disc(34, 8, 4.6)
    z.path([(16, 26), (11, 30)], 2)              # bosje zuidwest
    z.disc(9, 32, 4.6)
    z.path([(27, 27), (32, 30)], 2)              # weide zuidoost
    z.disc(33, 32, 4.6)
    z.path([(12, 8), (6, 12), (4, 16)], 2)       # doodlopend west
    z.disc(5, 18, 3.0)
    # hoog gras
    for cx, cy, r in ((16, 17, 2.4), (28, 16, 2.4), (17, 27, 2.0), (29, 25, 2.0), (34, 8, 2.6), (9, 32, 2.6),
                      (33, 32, 2.6), (12, 6, 2.2), (35, 17, 1.8)):
        z.blob(cx, cy, r, 'L', only='g')
    pond(z, 20, 21, 25, 23)
    # sprookjesring van glinsterbloemen rond de vijver, bloemen in de weide
    for y in range(17, 28):
        for x in range(16, 30):
            if z.T[y][x] == 'g' and 1.5 <= math.hypot((x - 22.5) / 1.4, y - 22) <= 3.2:
                z.T[y][x] = 'G'
    for y in range(2, 13):
        for x in range(9, 22):
            if z.T[y][x] == 'g':
                r = z.rng.random()
                z.T[y][x] = 'G' if r < 0.22 else 'f' if r < 0.42 else 'k' if r < 0.5 else 'g'
    for y in range(1, z.H - 1):
        for x in range(1, z.W - 1):
            if z.T[y][x] == 'g' and z.rng.random() < 0.05:
                z.T[y][x] = 'k'                  # glinsters op de open plekken
    SIGNPOS = (38, 20)
    z.T[20][38] = 's'
    z.tidy()
    ITEMS = [(36, 6, 'ITEM_PIXIE_PLATE', 'FLAG_ITEM_SAFARI_FAIRY_PIXIE_PLATE'),
             (7, 33, 'ITEM_FAIRY_FEATHER', 'FLAG_ITEM_SAFARI_FAIRY_FAIRY_FEATHER')]
    HIDDEN = [(3, 19, 'ITEM_SHINY_STONE', 'FLAG_HIDDEN_ITEM_SAFARI_FAIRY_SHINY_STONE')]
    for x, y, *_ in ITEMS + HIDDEN:
        if z.T[y][x] not in 'gL':
            z.T[y][x] = 'g'
    z.T[EX[1]][EX[0]] = 'x'
    extra = {'G': ([NEW['fairy']['glow%d' % i] for i in range(3)], 0),
             'k': ([NEW['fairy']['sparkle%d' % i] for i in range(2)], 0),
             'x': (NEW['fairy']['east_arrow'], 0)}
    M = forest_tiles(z, extra)
    walk = z.bfs([EX], lambda x, y: z.T[y][x] in 'gLfGkx' and (x, y) not in {(i[0], i[1]) for i in ITEMS})
    if os.environ.get('SHOW'):
        show(z, walk)
    for x, y, *_ in ITEMS:
        assert near(x, y, walk), ('item onbereikbaar', x, y)
    for x, y, *_ in HIDDEN:
        assert (x, y) in walk, ('verborgen item onbereikbaar', x, y)
    assert near(*SIGNPOS, walk)
    assert z.T[20][43] == 'T' and z.T[23][43] == 'T'
    print('Fairy Forest: %d vakken bereikbaar' % len(walk))
    return dict(name='SafariZone_FairyForest', id='MAP_SAFARI_ZONE_FAIRY_FOREST', layout='LAYOUT_SAFARI_ZONE_FAIRY_FOREST',
                M=M, W=z.W, H=z.H, ts=('gTileset_SafariFairyGeneral', 'gTileset_SafariFairy'),
                border=[val(0x0C6, 1, 0), val(0x0C7, 1, 0), val(0x0C7, 1, 0), val(0x0C6, 1, 0)],
                music='MUS_SAFARI_ZONE', weather='WEATHER_NONE', mapsec='MAPSEC_SAFARI_FAIRY_FOREST',
                warps=[(EX[0], EX[1], 3, 'MAP_SAFARI_ZONE_SOUTHWEST', 1)], items=ITEMS, hidden=HIDDEN,
                signs=[(SIGNPOS[0], SIGNPOS[1], 'SafariZone_FairyForest_EventScript_Sign')], npcs=[])


# ================================================================ THUNDER PLAINS
def build_thunder():
    z = Zone(48, 40, 403)                        # Shinx
    W, H = z.W, z.H
    z.rect(0, 0, W - 1, H - 1, 'g')
    z.rect(0, 0, W - 1, 2, 'M')                  # bergwand met de grot (noord)
    z.rect(0, 3, W - 1, 3, 'C')
    CAVE = (24, 3)
    trees = set()                                # linkerbovenhoek van elke boom (2x2)
    belt = set()
    for y in range(4, H, 2):
        for x in (0, 2, W - 4, W - 2):
            belt.add((x, y))
    for x in range(4, W - 4, 2):
        for y in (H - 4, H - 2):
            belt.add((x, y))
    # dor hoog gras
    for cx, cy, r in ((12, 12, 4.6), (34, 10, 4.2), (10, 27, 4.6), (31, 29, 4.6), (21, 20, 3.2), (40, 21, 3.0),
                      (20, 31, 2.6), (39, 32, 2.4)):
        z.blob(cx, cy, r, 'L', only='g')
    pond(z, 26, 16, 31, 18)                      # drinkplaats
    z.rect(25, 15, 32, 15, 'g')
    z.rect(25, 16, 25, 19, 'g')
    z.rect(32, 16, 32, 19, 'g')
    ITEMS = [(41, 6, 'ITEM_ZAP_PLATE', 'FLAG_ITEM_SAFARI_THUNDER_ZAP_PLATE'),
             (6, 33, 'ITEM_MAGNET', 'FLAG_ITEM_SAFARI_THUNDER_MAGNET')]
    HIDDEN = [(15, 21, 'ITEM_THUNDER_STONE', 'FLAG_HIDDEN_ITEM_SAFARI_THUNDER_THUNDER_STONE')]
    SIGNPOS = (22, 5)
    KEEP = {(CAVE[0], 4), (CAVE[0], 5), SIGNPOS} | {(x, y) for x, y, *_ in ITEMS + HIDDEN}
    for x in range(21, 28):
        for y in range(4, 8):
            KEEP.add((x, y))
    # losse acacia's en een paar groepjes (niet in het gras, niet op de vijver, niet tegen elkaar)
    def free(x, y):
        return all(z.inb(x + dx, y + dy) and z.T[y + dy][x + dx] == 'g' and (x + dx, y + dy) not in KEEP
                   for dx in range(-1, 3) for dy in range(-1, 3))
    cands = [(x, y) for y in range(5, H - 6) for x in range(5, W - 6)]
    z.rng.shuffle(cands)
    for x, y in cands:
        if len(trees) >= 15:
            break
        if free(x, y) and all(abs(x - a) > 4 or abs(y - b) > 4 for a, b in trees):
            trees.add((x, y))
    for x, y in [(36, 24), (38, 24), (8, 18), (8, 20)]:     # twee groepjes
        if all(z.T[y + dy][x + dx] == 'g' for dx in range(2) for dy in range(2)):
            trees.add((x, y))
    for x, y in list(trees) + list(belt):
        for dx in range(2):
            for dy in range(2):
                z.T[y + dy][x + dx] = 't'
    rocks = 0
    for x, y in cands[::-1]:
        if rocks >= 9:
            break
        if z.T[y][x] == 'g' and (x, y) not in KEEP and all(z.T[y + dy][x + dx] in 'gL' for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
            z.T[y][x] = 'r'
            rocks += 1
    z.T[SIGNPOS[1]][SIGNPOS[0]] = 's'
    # tegels
    GROUND, DRY = 0x218, NEW['thunder']['dry_grass']
    M = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            k = z.T[y][x]
            if k == 'M':
                M[y][x] = val(0x071, 1, 3)
            elif k == 'C':
                M[y][x] = val(0x079, 1, 3)
            elif k == 'L':
                M[y][x] = val(DRY, 0, 3)
            elif k == 'r':
                M[y][x] = val(ROCK, 1, 3)
            elif k == 's':
                M[y][x] = val(SIGN, 1, 3)
            elif k == 'w':
                up, lf, rt = z.k(x, y - 1) != 'w', z.k(x - 1, y) != 'w', z.k(x + 1, y) != 'w'
                mt = (0xB0 if lf else 0xB2 if rt else 0xB1) if up else 0xB8 if lf else 0xBA if rt else 0xA1
                M[y][x] = val(mt, 0, 1)
            elif k == 't':
                M[y][x] = 0                       # hieronder
            else:
                M[y][x] = val(BANK if z.k(x, y - 1) == 'w' else 0x001 if (z.k(x - 1, y) == 'w' or z.k(x + 1, y) == 'w') else GROUND, 0, 3)
    for (x, y) in trees | belt:
        top_coll = 1 if (x, y) in belt else 0
        M[y][x], M[y][x + 1] = val(0x204, top_coll, 3), val(0x205, top_coll, 3)
        M[y + 1][x], M[y + 1][x + 1] = val(0x20C, 1, 3), val(0x20D, 1, 3)
    # grot: 07b 064 07d boven, 079 0a7 091 onder
    cx, cy = CAVE
    M[cy - 1][cx - 1], M[cy - 1][cx], M[cy - 1][cx + 1] = val(0x07B, 1, 3), val(0x064, 1, 3), val(0x07D, 1, 3)
    M[cy][cx], M[cy][cx + 1] = val(0x0A7, 0, 3), val(0x091, 1, 3)
    walkable = lambda x, y: (z.T[y][x] in 'gL' or (z.T[y][x] == 't' and not (M[y][x] >> 10) & 3)) and (x, y) not in {(i[0], i[1]) for i in ITEMS}
    walk = z.bfs([(cx, cy + 1)], walkable)
    for x, y, *_ in ITEMS:
        assert near(x, y, walk), ('item onbereikbaar', x, y)
    for x, y, *_ in HIDDEN:
        assert (x, y) in walk, ('verborgen item onbereikbaar', x, y)
    assert near(*SIGNPOS, walk)
    print('Thunder Plains: %d vakken bereikbaar, %d bomen, %d rotsen' % (len(walk), len(trees), rocks))
    return dict(name='SafariZone_ThunderPlains', id='MAP_SAFARI_ZONE_THUNDER_PLAINS', layout='LAYOUT_SAFARI_ZONE_THUNDER_PLAINS',
                M=M, W=W, H=H, ts=('gTileset_SafariThunderGeneral', 'gTileset_SafariThunder'),
                border=[val(0x204, 1, 3), val(0x205, 1, 3), val(0x20C, 1, 3), val(0x20D, 1, 3)],
                music='MUS_SAFARI_ZONE', weather='WEATHER_RAIN_THUNDERSTORM', mapsec='MAPSEC_SAFARI_THUNDER_PLAINS',
                warps=[(cx, cy, 3, 'MAP_SAFARI_ZONE_NORTHEAST', 0)], items=ITEMS, hidden=HIDDEN,
                signs=[(SIGNPOS[0], SIGNPOS[1], 'SafariZone_ThunderPlains_EventScript_Sign')], npcs=[])


# ================================================================ HAUNTED CAMP
def build_spook():
    z = Zone(44, 40, 854)                        # Sinistea
    EX = (43, 27)
    z.path([(42, 27), (24, 27)], 2)
    z.T[27][43] = 'g'
    z.T[28][43] = 'g'
    z.disc(21, 22, 10.0)                         # het kampeerterrein
    z.rect(13, 13, 21, 19, 'g')                  # erf van het rusthuis
    HX, HY = 15, 13                              # rusthuis 4x4 (deur op HX+1, HY+3)
    z.path([(12, 19), (8, 13), (7, 10)], 2)      # mistig bosje noordwest
    z.disc(7, 8, 4.4)
    z.path([(21, 14), (26, 12), (31, 10)], 2)    # open plek noordoost
    z.disc(33, 9, 5.0)
    z.path([(18, 29), (15, 32)], 2)              # vijver zuid
    z.disc(14, 34, 5.0)
    for cx, cy, r in ((12, 27, 2.6), (29, 24, 2.2), (33, 9, 3.2), (7, 8, 2.6), (35, 33, 2.6), (25, 31, 2.0), (5, 25, 2.2)):
        z.blob(cx, cy, r, 'L', only='g')
    z.path([(30, 27), (34, 30)], 2)
    z.disc(35, 33, 3.8)                          # overwoekerde tentplekken zuidoost
    z.path([(12, 22), (6, 24)], 2)               # doodlopend west
    z.disc(5, 25, 3.2)
    pond(z, 10, 33, 15, 35)
    z.rect(HX, HY, HX + 3, HY + 3, 'h')
    z.rect(HX - 1, HY + 4, HX + 4, HY + 5, 'g')  # voor de deur vrij
    FIRE = (23, 23)                              # kampvuurkring: rotsen rondom, onderkant open
    for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)):
        z.T[FIRE[1] + dy][FIRE[0] + dx] = 'r'
    z.T[FIRE[1]][FIRE[0]] = 'g'
    z.T[FIRE[1] + 1][FIRE[0]] = 'g'
    LAMPS = [(13, 21), (21, 17), (28, 20), (14, 28), (26, 28), (31, 26)]
    for x, y in LAMPS:
        z.T[y][x] = 'l'
    for x in range(23, 27):                      # scheef hek
        z.T[16][x] = 'F'
    SIGNPOS = (38, 26)
    z.T[26][38] = 's'
    z.tidy()
    ITEMS = [(35, 7, 'ITEM_SPOOKY_PLATE', 'FLAG_ITEM_SAFARI_SPOOK_SPOOKY_PLATE'),
             (5, 7, 'ITEM_REAPER_CLOTH', 'FLAG_ITEM_SAFARI_SPOOK_REAPER_CLOTH')]
    HIDDEN = [(17, 35, 'ITEM_DUSK_STONE', 'FLAG_HIDDEN_ITEM_SAFARI_SPOOK_DUSK_STONE'),
              (13, 17, 'ITEM_SPELL_TAG', 'FLAG_HIDDEN_ITEM_SAFARI_SPOOK_SPELL_TAG')]
    for x, y, *_ in ITEMS + HIDDEN:
        if z.T[y][x] not in 'gL':
            z.T[y][x] = 'g'
    z.T[EX[1]][EX[0]] = 'x'
    extra = {'x': (NEW['spook']['east_arrow'], 0), 'l': (0x240, 1), 'F': ((0x250, 0x251, 0x252), 1), 'h': (GRASS, 1)}
    M = forest_tiles(z, extra)
    for i, x in enumerate(range(23, 27)):
        M[16][x] = val((0x250, 0x251, 0x251, 0x252)[i], 1, 3)
    for dy in range(4):
        for dx in range(4):
            M[HY + dy][HX + dx] = val(HOUSE[dy][dx], 1, 3)
    DOOR = (HX + 1, HY + 3)
    blocked = {(i[0], i[1]) for i in ITEMS}
    walk = z.bfs([EX], lambda x, y: z.T[y][x] in 'gLx' and (x, y) not in blocked)
    if os.environ.get('SHOW'):
        show(z, walk)
    for x, y, *_ in ITEMS:
        assert near(x, y, walk), ('item onbereikbaar', x, y)
    for x, y, *_ in HIDDEN:
        assert (x, y) in walk, ('verborgen item onbereikbaar', x, y)
    for p in [SIGNPOS, DOOR, FIRE] + LAMPS[:1]:
        assert near(*p, walk) or p in walk, ('niet bereikbaar', p)
    assert (DOOR[0], DOOR[1] + 1) in walk
    print('Haunted Camp: %d vakken bereikbaar' % len(walk))
    return dict(name='SafariZone_HauntedCamp', id='MAP_SAFARI_ZONE_HAUNTED_CAMP', layout='LAYOUT_SAFARI_ZONE_HAUNTED_CAMP',
                M=M, W=z.W, H=z.H, ts=('gTileset_SafariSpookGeneral', 'gTileset_SafariSpook'),
                border=[val(0x0C6, 1, 0), val(0x0C7, 1, 0), val(0x0C7, 1, 0), val(0x0C6, 1, 0)],
                music='MUS_MT_PYRE_EXTERIOR', weather='WEATHER_FOG_HORIZONTAL', mapsec='MAPSEC_SAFARI_HAUNTED_CAMP',
                warps=[(EX[0], EX[1], 3, 'MAP_SAFARI_ZONE_NORTHWEST', 0)], items=ITEMS, hidden=HIDDEN,
                signs=[(SIGNPOS[0], SIGNPOS[1], 'SafariZone_HauntedCamp_EventScript_Sign'),
                       (DOOR[0], DOOR[1], 'SafariZone_HauntedCamp_EventScript_Door'),
                       (FIRE[0], FIRE[1], 'SafariZone_HauntedCamp_EventScript_Campfire'),
                       (LAMPS[0][0], LAMPS[0][1], 'SafariZone_HauntedCamp_EventScript_Lantern'),
                       (LAMPS[1][0], LAMPS[1][1], 'SafariZone_HauntedCamp_EventScript_Lantern')],
                npcs=[])


# ================================================================ schrijven
def obj(gfx, x, y, elev, move, sight, script, flag):
    return {"graphics_id": gfx, "x": x, "y": y, "elevation": elev, "movement_type": move,
            "movement_range_x": 0, "movement_range_y": 0, "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": str(sight), "script": script, "flag": flag}


def write_zone(d):
    name, W, H = d['name'], d['W'], d['H']
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', v) for r in d['M'] for v in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *d['border']))
    objs = [obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 3, 'MOVEMENT_TYPE_LOOK_AROUND', item, 'Common_EventScript_FindItem', flag)
            for x, y, item, flag in d['items']]
    mj = {
        "id": d['id'], "name": name, "layout": d['layout'], "music": d['music'],
        "region_map_section": d['mapsec'], "requires_flash": False, "weather": d['weather'],
        "map_type": "MAP_TYPE_ROUTE", "allow_cycling": True, "allow_escaping": False, "allow_running": True,
        "show_map_name": True, "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": [],
        "object_events": objs,
        "warp_events": [{"x": x, "y": y, "elevation": e, "dest_map": m, "dest_warp_id": str(w)} for x, y, e, m, w in d['warps']],
        "coord_events": [],
        "bg_events": [{"type": "sign", "x": x, "y": y, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                       "script": s} for x, y, s in d['signs']] +
                     [{"type": "hidden_item", "x": x, "y": y, "elevation": 3, "item": item, "flag": flag}
                      for x, y, item, flag in d['hidden']],
    }
    os.makedirs('data/maps/' + name, exist_ok=True)
    with open('data/maps/%s/map.json' % name, 'w') as fp:
        json.dump(mj, fp, indent=2, ensure_ascii=False)
        fp.write('\n')
    lj = open('data/layouts/layouts.json').read()
    if '"%s"' % d['layout'] not in lj:
        i = lj.rindex('    }\n  ]')
        j = i + len('    }')
        lj = lj[:j] + ''',
    {
      "id": "%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "%s",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (d['layout'], name, W, H, d['ts'][0], d['ts'][1], name, name) + lj[j:]
        open('data/layouts/layouts.json', 'w').write(lj)
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"gMapGroup_Grounded": [')
        j = g.index('\n  ]', i)
        g = g[:j] + ',\n    "%s"' % name + g[j:]
        open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/FortreeJungle/scripts.inc"\n'
        assert anchor in es
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


# ---------------------------------------------------------------- openingen in de bestaande Safari-kaarten
def edit_safari(name, edits, warp, guard):
    path = 'data/layouts/%s/map.bin' % name
    v = list(struct.unpack('<1600H', open(path, 'rb').read()))
    for (x, y), m in edits.items():
        v[y * 40 + x] = m
    open(path, 'wb').write(struct.pack('<1600H', *v))
    mj = json.load(open('data/maps/%s/map.json' % name))
    x, y, e, dest = warp
    if not any(w['dest_map'] == dest for w in mj['warp_events']):
        mj['warp_events'].append({"x": x, "y": y, "elevation": e, "dest_map": dest, "dest_warp_id": "0"})
    gx, gy, ge, face, script = guard
    if not any(o['script'] == script for o in mj['object_events']):
        mj['object_events'].append(obj('OBJ_EVENT_GFX_CAMPER', gx, gy, ge, 'MOVEMENT_TYPE_FACE_' + face, 0, script,
                                       'FLAG_SAFARI_ZONES_OPEN'))
    with open('data/maps/%s/map.json' % name, 'w') as fp:
        json.dump(mj, fp, indent=2, ensure_ascii=False)
        fp.write('\n')
    return [w['dest_map'] for w in mj['warp_events']].index(dest)


wid = {}
# Southwest (0,30): het gat in de bomenrand aan de westkant, boven de vijver -> Fairy Forest
wid['fairy'] = edit_safari('SafariZone_Southwest', {(0, 30): val(LILY_WEST, 0, 3)},
                           (0, 30, 3, 'MAP_SAFARI_ZONE_FAIRY_FOREST'),
                           (0, 30, 3, 'RIGHT', 'SafariZone_Southwest_EventScript_FairyGuard'))
# Northwest (0,28): het hoge gras loopt hier tot de rand; (0,29) wordt een rots zodat het gat 1 breed is -> Haunted Camp
wid['spook'] = edit_safari('SafariZone_Northwest', {(0, 28): val(LILY_WEST, 0, 7), (0, 29): val(ROCK, 1, 7)},
                           (0, 28, 7, 'MAP_SAFARI_ZONE_HAUNTED_CAMP'),
                           (0, 28, 7, 'RIGHT', 'SafariZone_Northwest_EventScript_SpookGuard'))
# Northeast (24,7): grot in de bergwand boven het plateau -> Thunder Plains
wid['thunder'] = edit_safari('SafariZone_Northeast', {(23, 6): val(0x07B, 1, 3), (24, 6): val(0x064, 1, 3),
                                                      (25, 6): val(0x07D, 1, 3), (24, 7): val(0x0A7, 0, 3),
                                                      (25, 7): val(0x091, 1, 3), (24, 8): val(GRASS, 0, 3)},
                             (24, 7, 3, 'MAP_SAFARI_ZONE_THUNDER_PLAINS'),
                             (24, 8, 3, 'DOWN', 'SafariZone_Northeast_EventScript_ThunderGuard'))

zones = {'fairy': build_fairy(), 'thunder': build_thunder(), 'spook': build_spook()}
for key, d in zones.items():
    x, y, e, m, _ = d['warps'][0]
    d['warps'][0] = (x, y, e, m, wid[key])
    write_zone(d)

if len(sys.argv) > 1:
    for d in zones.values():
        subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', d['name'],
                        os.path.join(sys.argv[1], d['name'] + '.png'), '0', str(d['H'])], check=True)
print('klaar', wid)
