# Fully Ungrounded: variant 3 van de regiokaart. Basis = variant 2 (regiokaart2.py, door Jordi gekozen: gedraaid,
# binnenzee, landmarks), bijgewerkt met de besluiten uit REGIO.md, ROUTEPLAN.md, CONCEPT.md, DUNGEONS.md en
# MYTHOLOGIE.md: gyms, hoofdpad, spoorlijn, lussen en vaste plekken. Stijl: de Emerald-regiokaart.
# Kleuren en stadsiconen komen uit graphics/pokenav/region_map (Hoenn). Eén vak = 8x8 pixels, zoals op de GBA.
# Stijlregels (afgekeken van Hoenn): alleen Hoenn-kleuren; hoogte = geneste vlekken die naar binnen lichter worden
# (lichtste groen zeldzaam), donkergroene rand van 2-7 px langs elke kust en elk meer, geen spikkels (eilandjes >= 24 px,
# licht midden), vlakke oppervlakken (zee, zand, zout) in strepen van 1 px, routes lichter boven hoger terrein.
# Uitvoer: docs/concept/regiokaart3.png (kaal) en docs/concept/regiokaart3_namen.png (met namen en legenda).
# Draaien vanuit de repo-root: python3 tools/concept/regiokaart3.py  (--grid drukt een vakkenraster af)
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 48, 28            # vakken (liggend, zoals het GBA-scherm)
PW, PH = W * 8, H * 8    # pixels

def hexc(s):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))

SEA = [hexc('#9cd5ff'), hexc('#a4b4ff')]
SEAROUTE = [hexc('#4a9ce6'), hexc('#2983e6')]
GREEN = [hexc(c) for c in ('#007300', '#39ac08', '#62d500', '#acee31', '#d5ff7b')]
ROUTE = [hexc(c) for c in ('#e6a400', '#eebd39', '#f6d552', '#eee673', '#eee6ac')]
SAND = [hexc('#eee6ac'), hexc('#cdcd94')]          # Hoenn-zand (strepen)
SAND_HI = [hexc('#f6eec5'), hexc('#eee6ac')]
SNOW = [hexc('#ffffff'), hexc('#cdcdcd')]
SALT = [hexc('#ffffff'), hexc('#cdcdcd')]

# ---------- ruis ----------
def value_noise(seed, scale):
    r = random.Random(seed)
    gw, gh = PW // scale + 3, PH // scale + 3
    g = np.array([[r.random() for _ in range(gw)] for _ in range(gh)])
    yy, xx = np.mgrid[0:PH, 0:PW] / scale
    x0, y0 = xx.astype(int), yy.astype(int)
    fx, fy = xx - x0, yy - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a = g[y0, x0] * (1 - fx) + g[y0, x0 + 1] * fx
    b = g[y0 + 1, x0] * (1 - fx) + g[y0 + 1, x0 + 1] * fx
    return a * (1 - fy) + b * fy

def fbm(seed, scales=(32, 16, 8), weights=(0.5, 0.3, 0.2)):
    return sum(value_noise(seed + i, s) * w for i, (s, w) in enumerate(zip(scales, weights)))

ys, xs = np.mgrid[0:PH, 0:PW].astype(float)
cx, cy = xs / 8, ys / 8   # in vakken
n = fbm(10)
hills = fbm(20, (20, 10, 5), (0.5, 0.33, 0.17))
fine = value_noise(40, 4)

def ellipse(x0, y0, rx, ry):
    return ((cx - x0) / rx) ** 2 + ((cy - y0) / ry) ** 2 < 1

def rellipse(x0, y0, rx, ry, deg):
    t = math.radians(deg)
    dx, dy = cx - x0, cy - y0
    u = (dx * math.cos(t) + dy * math.sin(t)) / rx
    v = (-dx * math.sin(t) + dy * math.cos(t)) / ry
    return u * u + v * v < 1

# ---------- land: het continent gedraaid en liggend (zoals Hoenn = Kyushu, 90 graden gedraaid) ----------
# Echt noorden -> rechts, echt zuiden -> links, Stille Oceaan/Andes -> boven, Atlantische kust -> onder.
def interp(pts, v):
    return np.interp(v, [p[0] for p in pts], [p[1] for p in pts])
TOP = [(0, 13), (3, 11), (6, 7.5), (10, 5), (15, 4), (20, 3.5), (24, 3), (27, 2.6), (30, 3.4), (33, 2.5), (37, 2.5), (40, 3.5), (48, 4)]   # Pacifische kust (y per x)
BOT = [(0, 15), (3, 16.5), (6, 18), (10, 20), (14, 21.5), (19, 23.5), (24, 24.5), (29, 25), (33, 25.5), (37, 24), (40, 21), (43, 17), (48, 15)]  # Atlantische kust
RIGHT = [(0, 39), (4, 42), (8, 44), (12, 44.5), (16, 44), (20, 42), (28, 40)]   # Caribische/noordkust (x per y)
tc, bc, rc = interp(TOP, cx), interp(BOT, cx), interp(RIGHT, cy)
cn = n + (value_noise(91, 6) - 0.5) * 0.35 + (value_noise(92, 3) - 0.5) * 0.12
land = (cy > tc + (cn - 0.5) * 2.4) & (cy < bc + (cn - 0.5) * 2.6) & (cx < rc + (cn - 0.5) * 2.4) & (cx > 2.2 + (cn - 0.5) * 2)
# Patagonië: korte, grillige punt met fjorden aan de bovenkant
fjord = (cx < 11) & (cy < tc + 1.8) & (value_noise(55, 3) > 0.5)
land &= ~fjord
# baaien in de Atlantische kust (meer kust, minder blok)
land &= ~rellipse(13.2, 21.4, 2.0, 0.8, -15)          # Río de la Plata
land &= ~rellipse(22.5, 24.6, 1.1, 0.7, 0)            # baai van Rio (Guanabara)
land &= ~rellipse(30.5, 25.4, 1.3, 0.8, 10)           # Allerheiligenbaai (Salvador)
land &= ~rellipse(41.6, 14.6, 2.2, 1.0, 35)           # monding van de binnenzee
islands = (ellipse(31.5, 0.9, 1.1, 0.6) | ellipse(33.6, 1.0, 0.6, 0.4) | ellipse(30, 1.5, 0.5, 0.35)   # Galápagos
           | ellipse(13.5, 1.2, 0.7, 0.45)                                                          # Paaseiland
           | rellipse(2.0, 15.6, 1.6, 0.7, -20)                                                     # Vuurland
           | ellipse(40.8, 24.6, 0.6, 0.4)                                                          # Fernando de Noronha
           | ellipse(25.5, 26.4, 0.8, 0.45) | ellipse(27.4, 26.8, 0.5, 0.35)                        # eilanden voor Rio
           | ellipse(45.5, 9, 0.9, 0.5) | ellipse(46.2, 5.5, 0.6, 0.4))                         # Caribische eilanden
land |= islands & (n > 0.3)
chiloe = rellipse(3.9, 9.1, 1.0, 0.45, -15)                     # Chiloé (v3)
land |= chiloe
land &= ~(rellipse(4.4, 9.9, 1.8, 0.3, -15) & ~chiloe)            # zeestraat (Canal de Chacao)
pad = land.copy()
for _ in range(10):
    p = np.pad(pad, 1)
    pad = pad | p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
near = pad & ~land
dots = near & (value_noise(66, 5) > 0.8) & ((cx < 10) | (cy > 22) | (cx > 40))
land |= dots
# de binnenzee (het oude Amazonebekken, Pebas): open water met een verdronken woud van eilandjes
inland = ((rellipse(31, 13.2, 6.8, 3.0, -6) | rellipse(26.4, 14.0, 2.4, 1.5, 20) | rellipse(36.2, 12.6, 3.0, 1.8, -15))
          & (fbm(110, (20, 10, 5)) + (value_noise(111, 4) - 0.5) * 0.25 > 0.36))
inland &= ~((value_noise(113, 5) > 0.68) & ~rellipse(31, 12.6, 4.5, 0.9, -6))   # verdronken woud: eilandjes van boomtoppen, met een vaargeul
inland |= rellipse(39.8, 14.0, 3.6, 1.0, 25)          # brede uitstroom naar zee
land &= ~inland

# ---------- pixelhulpjes ----------
from collections import deque
def components(mask):
    """Labels van samenhangende stukken (4-buren); geeft (labels, groottes)."""
    lab = np.full(mask.shape, -1, int)
    sizes = []
    hh, ww = mask.shape
    for y0, x0 in zip(*np.nonzero(mask)):
        if lab[y0, x0] >= 0:
            continue
        k = len(sizes)
        lab[y0, x0] = k
        dq, nn = deque([(y0, x0)]), 0
        while dq:
            y, x = dq.popleft()
            nn += 1
            for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= ny < hh and 0 <= nx < ww and mask[ny, nx] and lab[ny, nx] < 0:
                    lab[ny, nx] = k
                    dq.append((ny, nx))
        sizes.append(nn)
    return lab, np.array(sizes)

def drop_small(mask, minsize):
    lab, sizes = components(mask)
    if not len(sizes):
        return mask
    keep = sizes >= minsize
    return mask & keep[np.maximum(lab, 0)] & (lab >= 0)

def erode(m):
    q = np.pad(m, 1)
    return m & q[:-2, 1:-1] & q[2:, 1:-1] & q[1:-1, :-2] & q[1:-1, 2:]

def dilate(m):
    q = np.pad(m, 1)
    return m | q[:-2, 1:-1] | q[2:, 1:-1] | q[1:-1, :-2] | q[1:-1, 2:]

def dist_in(m, maxd=16):
    """Afstand (in stappen) van elk pixel in m tot de rand van m."""
    d = np.zeros(m.shape, int)
    cur = m.copy()
    for i in range(maxd):
        d[cur] = i + 1
        cur = erode(cur)
    return d

# Hoenn heeft geen losse pixels in zee: de kleinste eilandjes zijn klodders van ±25 px, en de kust heeft
# geen spikkels. Kleine stukjes land en kleine gaatjes zee weg.
land = drop_small(land, 24)
land = ~drop_small(~land, 16) | (~land & inland)
# kustlijn iets gladder (Hoenn: trapjes van 1-2 px, geen losse uitsteeksels van één pixel)
for _ in range(2):
    q = np.pad(land, 1, mode='edge').astype(int)
    nb = sum(np.roll(np.roll(q, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1))[1:-1, 1:-1]
    land = np.where(nb >= 6, True, np.where(nb <= 3, False, land))
land &= ~inland
land = drop_small(land, 24)
land_lab, land_sizes = components(land)
mainland = land & (land_lab == int(np.argmax(land_sizes)))

# ---------- hoogte ----------
ridge = tc + 3.2 + 0.5 * np.sin(cx * 0.5)                     # de Andes: een rug langs de Pacifische kust
andes = np.exp(-((cy - ridge) / 2.4) ** 2) * (cx < 38)
plateau = (np.exp(-((cy - (ridge + 2.8 + (n - 0.5) * 3)) / 2.0) ** 2)
           * np.clip(1 - np.abs(cx - 20) / 6 + (n - 0.5) * 0.6, 0, 1))                     # altiplano
tepui = 0.7 * np.exp(-(((cx - 37.5) / 2.6) ** 2 + ((cy - 8.5) / 1.6) ** 2))                # Guyana-hoogland
brazil = 0.35 * np.exp(-(((cx - 27) / 5) ** 2 + ((cy - 20.5) / 2.5) ** 2))
amazon = np.exp(-(((cx - 30) / 9) ** 2 + ((cy - 13) / 4) ** 2))
pantanal = np.exp(-(((cx - 21.5) / 2.2) ** 2 + ((cy - 16) / 1.6) ** 2))
bumps = np.zeros((PH, PW))
br = random.Random(5)
wx = xs + (value_noise(301, 10) - 0.5) * 18 + (value_noise(302, 5) - 0.5) * 6
wy = ys + (value_noise(303, 10) - 0.5) * 18 + (value_noise(304, 5) - 0.5) * 6
for _ in range(int(520 * W * H / 1600)):
    bx, by = br.uniform(0, PW), br.uniform(0, PH)
    ra, rb = br.uniform(4, 16), br.uniform(3, 8)
    ang = br.uniform(0, math.pi)
    hgt = br.uniform(0.15, 0.45)
    dx, dy = wx - bx, wy - by
    u = (dx * math.cos(ang) + dy * math.sin(ang)) / ra
    v = (-dx * math.sin(ang) + dy * math.cos(ang)) / rb
    bumps = np.maximum(bumps, hgt * np.exp(-(u * u + v * v)))
elev = (np.maximum(andes * 0.6, plateau * 0.5) + brazil * 0.6 + tepui
        + bumps * 1.35 + (hills - 0.5) * 0.2 - amazon * 0.15 - pantanal * 0.25)
# landmark: de reuzentepui, een tafelberg met steile wanden die hoog boven de jungle uitsteekt
tepui_top = rellipse(37.6, 8.4, 1.5, 0.75, -10) & (value_noise(112, 3) > 0.25)
elev = np.where(tepui_top, 1.2, elev)
dsea = dist_in(land, 20)
coastw = 3 + np.round((value_noise(81, 12) - 0.5) * 5 + (value_noise(82, 5) - 0.5) * 2).astype(int)
coast = land & (dsea <= np.clip(coastw, 2, 7))
isl = land & ~mainland
elev = np.where(isl, np.maximum(elev, (dsea - 2) * 0.12 + bumps * 0.6), elev)
lvl = np.digitize(elev, [0.28, 0.42, 0.6, 0.8])
for _ in range(2):
    q = np.pad(lvl, 1, mode='edge')
    stack = np.stack([q[1 + dy:PH + 1 + dy, 1 + dx:PW + 1 + dx] for dy in (-1, 0, 1) for dx in (-1, 0, 1)])
    counts = np.stack([(stack == k).sum(0) for k in range(5)])
    lvl = np.where(counts.max(0) >= 5, counts.argmax(0), lvl)
lvl[coast] = 0
lvl[tepui_top & ~coast] = 4

# ---------- biomen ----------
biome = np.zeros((PH, PW), int)
pn = fbm(97, (24, 12, 6))
pn = 0.5 + (pn - pn.mean()) / pn.std() * 0.22
desert = land & (cx > 11.5) & (cx < 28) & (cy < ridge - 0.9 + (n - 0.5) * 2)              # kustwoestijn (Atacama/Peru)
desert |= land & (cx > 13 + (pn - 0.5) * 3) & (cx < 20.5 + (pn - 0.5) * 3) & (cy < ridge + 2.4 + (pn - 0.5) * 5)   # puna/Lípez
desert |= land & rellipse(35.5 + (value_noise(93, 5) - 0.5) * 1.2, 22.6, 1.5, 0.7, 0)    # Lençóis
biome[desert] = 2
snow = land & (((lvl >= 4) & (cx > 9) & (cx < 30) & (andes > 0.75) & (biome != 2))
               | ((cx < 10) & (lvl >= 3)) | (cx < 3.4)
               | (ellipse(23.2, 10.2, 1.4, 1.0) & (lvl >= 2))          # Cordillera Real
               | ellipse(14.5, 7.3, 0.6, 0.5))                         # Licancabur (tussen San Pedro en Lípez)
snow &= ~tepui_top
biome[snow] = 3
sn = (value_noise(92, 4) - 0.5) * 0.7
salt = ((rellipse(18.2, 8.1, 1.8 + sn, 0.9 + sn, 70) | rellipse(19.0, 9.3, 0.8 + sn, 0.5 + sn, 20)
         | rellipse(17.5, 7.0, 0.6 + sn, 0.4, 40)) & ~ellipse(18.2, 8.0, 0.22, 0.15))
biome[salt] = 4
# Titicaca: langgerekt (in deze draaiing van rechtsboven naar linksonder), met zeestraat en eilanden,
# en een eigen landmark: een vulkaaneiland met krater midden in het meer
tn = (value_noise(91, 4) - 0.5) * 0.5
titicaca = ((rellipse(22.9, 6.6, 2.1 + tn, 0.85 + tn, -38) | rellipse(21.2, 8.0, 0.9 + tn, 0.45 + tn / 2, -20)
             | rellipse(21.9, 7.4, 0.45, 0.12, -40))
            & ~rellipse(22.0, 7.15, 0.5, 0.22, 20))
volcano = ellipse(23.4, 6.2, 0.55, 0.42)
crater = ellipse(23.4, 6.2, 0.2, 0.15)
titicaca &= ~volcano
titicaca |= crater
lakes = (titicaca
         | ellipse(7.5, 10.4, 0.5, 0.3) | ellipse(6.4, 11.5, 0.6, 0.35) | ellipse(5.5, 11.1, 0.4, 0.3)   # meren bij Bariloche
         | ellipse(15.6, 8.6, 0.45, 0.3)                                                              # Laguna Colorada
         | (ellipse(21.5, 16, 1.6, 1.1) & (value_noise(70, 4) > 0.55)))                                # Pantanal
lakes &= land
biome[volcano & land] = 3

# ---------- rivieren ----------
river = np.zeros((PH, PW), bool)
def draw_river(points, width=1, wobble=2.0):
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 16)
        for i in range(steps + 1):
            t = i / steps
            x, y = (x0 + (x1 - x0) * t) * 8, (y0 + (y1 - y0) * t) * 8
            x += math.sin(t * 9 + y0) * wobble * (abs(y1 - y0) > abs(x1 - x0))
            y += math.sin(t * 9 + x0) * wobble * (abs(x1 - x0) >= abs(y1 - y0))
            hi = width + 1 + (width == 0)
            river[max(0, int(y) - width):int(y) + hi, max(0, int(x) - width):int(x) + hi] = True
draw_river([(26, 7.5), (26.2, 10), (26.3, 12.5)], 1)                 # uit de Andes de binnenzee in
draw_river([(31, 6.5), (30.5, 9), (30.4, 11)], 0)
draw_river([(36, 10), (35, 11.2)], 0)                                # van de tepui
draw_river([(22, 17), (19, 18.5), (16, 19.5), (13.5, 20.8)], 1)      # Paraná naar de Río de la Plata
draw_river([(18, 16.2), (17.4, 18.6)], 0)                            # Iguazú
draw_river([(16.5, 13), (16.2, 16), (16.6, 19.2)], 0)
river &= land

# ---------- schilderen ----------
# Alleen kleuren die de Hoenn-kaart zelf gebruikt. Vormtaal van Hoenn: hoger terrein = geneste vlekken die naar
# binnen lichter worden; vlakke oppervlakken (zee, zand) = horizontale strepen van 1 px; al het water heeft een
# donkergroene oever.
img = np.zeros((PH, PW, 3), np.uint8)
stripes = ys.astype(int) % 2
def paint(mask, pal, idx):
    for i, c in enumerate(pal):
        img[mask & (idx == i)] = c
water_in = (lakes | river) & land
# rivieren en meren met een donkergroene oever van 1 px (zoals elke kust in Hoenn)
wbank = dilate(water_in) & land & ~water_in
paint(~land, SEA, stripes)
# de lichtste groentint is in Hoenn zeldzaam (alleen de toppen van de hoogste heuvels)
glvl = np.where((lvl == 4) & (elev < 0.95), 3, lvl)
paint(land & ((biome == 0) | (coast & (biome == 3))), GREEN, glvl)
# woestijn: vlak zand in Hoenn-strepen (zoals Route 111 en de stranden); duinen/hoogland als geneste vlekken
# in dezelfde twee zandkleuren
dz = land & (biome == 2)
dlv = np.where(coast, 0, lvl)
dune = value_noise(95, 7) * 0.55 + value_noise(96, 3) * 0.2 + n * 0.25   # grillige duinvlekken, geen cirkels
dhi = dz & (dlv >= 1) & (dune > 0.56)
paint(dz & ~dhi, SAND, stripes)
dlv = np.where(dune > 0.66, 4, dlv)
img[dhi] = SAND[1]
img[erode(dhi) & (dlv >= 4) | erode(erode(dhi))] = SAND[0]
# sneeuw: witte toppen met een grijze rand, op de groene ondergrond; de kust blijft donkergroen
sm = land & (biome == 3) & ~coast
# twee tinten zoals de heuvels: grijs lager, wit hoger, met een grijze rand van 1 px
img[sm] = SNOW[1]
selev = elev + bumps * 0.8
thr = np.quantile(selev[sm], 0.3) if sm.any() else 0
img[erode(sm) & (selev > thr)] = SNOW[0]
# zoutvlakte: vlak en spiegelend, dus strepen (wit/grijs) zoals de zee
sa = land & (biome == 4)
paint(sa, SALT, stripes)
img[sa & ~erode(sa)] = SNOW[1]
img[wbank] = GREEN[0]
paint(water_in, SEA, stripes)


# landmark: de Nazca-kolibrie, zo groot dat je hem op de regiokaart ziet (lichte lijnen in het zand)
NAZCA = ["....#.......",
         "...###......",
         "....#....##.",
         "..#.#...##..",
         ".####..##...",
         "..#.####....",
         "....###.....",
         "...#.#.#....",
         "..#..#..#...",
         ".....#......"]
nx0, ny0 = 22 * 8 - 2, 1 * 8 + 6
for r, row in enumerate(NAZCA):
    for c, ch in enumerate(row):
        if ch == '#' and land[ny0 + r, nx0 + c]:
            img[ny0 + r, nx0 + c] = hexc('#fff6de')
# ---------- plaatsen (vakcoördinaten) ----------
# (naam, x, y, icoon, kant van het label: R/L/A/B, gym: '1'..'8', 'L' = League of '')
# Hoenn-leesbaarheid: alleen steden, hubs, grote dungeons en landmarks als icoon; de rest staat in de legenda.
PLACES = [
    # Bolivia (het zuiden naar verhouding groot)
    ('La Paz (start)', 20, 9, 'cityh', 'B', ''),
    ('Uyuni', 16, 10, 'cityh', 'A', '1'),
    ('Oruro', 20, 11, 'town', 'R', ''),
    ('Potosí', 18, 13, 'town', 'R', ''),
    ('Cordillera Real', 23, 10, 'town', 'R', '2'),
    ('Titicaca', 22, 7, 'spot', 'L', ''),
    ('Lípez', 14, 9, 'town', 'L', ''),
    # Atacama en Peru
    ('San Pedro', 12, 6, 'cityh', 'L', '3'),
    ('Valle de la Luna', 11, 5, 'spot', 'L', ''),
    ('Arequipa', 19, 4, 'town', 'A', ''),
    ('Nazca', 24, 3, 'spot', 'A', ''),
    ('Cuzco', 25, 6, 'cityv', 'L', '4'),
    ('Rainbow Mountain', 24, 8, 'spot', 'R', ''),
    ('Machu Picchu', 28, 6, 'cityh', 'A', 'L'),
    ('Chavín', 28, 3, 'spot', 'A', ''),
    # Noord-Argentinië, Mendoza, Patagonië
    ('Humahuaca', 14, 11, 'town', 'R', ''),
    ('Salta', 12, 12, 'cityh', 'B', ''),
    ('Cafayate', 10, 13, 'town', 'L', ''),
    ('Aconcagua', 9, 9, 'spot', 'L', ''),
    ('Mendoza', 8, 11, 'cityh', 'L', ''),
    ('Bariloche', 6, 12, 'town', 'L', ''),
    ('Chiloé', 4, 9, 'spot', 'A', ''),
    ('Perito Moreno', 3, 13, 'spot', 'B', ''),
    ('Valdés', 8, 16, 'spot', 'L', ''),
    ('Buenos Aires', 11, 19, 'cityh', 'L', '5'),
    # Brazilië
    ('Iguazú', 17, 17, 'spot', 'R', ''),
    ('Pantanal', 21, 14, 'town', 'R', ''),
    ('Florianópolis', 18, 21, 'town', 'B', ''),
    ('Rio de Janeiro', 22, 22, 'cityv', 'R', '6'),
    ('Salvador', 30, 23, 'town', 'B', ''),
    ('Lençóis', 35, 21, 'spot', 'R', ''),
    ('Belém', 39, 16, 'town', 'R', ''),
    # Andes-noordkant, Caribisch gebied, Guyana
    ('Quito', 31, 4, 'town', 'A', ''),
    ('Galápagos', 31, 1, 'spot', 'R', ''),
    ('Salento', 33, 6, 'town', 'B', ''),
    ('Medellín', 35, 5, 'cityv', 'R', ''),
    ('Cartagena', 38, 4, 'cityh', 'A', ''),
    ('Paramaribo', 41, 8, 'cityh', 'R', '7'),
    ('Tepui (Mew)', 37, 9, 'spot', 'B', ''),
    # Amazone
    ('Verdronken woud', 31, 12, 'spot', 'A', ''),
    ('Diepe jungle', 26, 13, 'town', 'R', '8'),
]

# ---------- routes ----------
route = np.zeros((H, W), bool)
sea_route = np.zeros((H, W), bool)
stub = np.zeros((H, W), bool)
def path(*pts, sea=False):
    tgt = sea_route if sea else route
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            tgt[y0, x] = True
        for y in range(min(y0, y1), max(y0, y1) + 1):
            tgt[y, x1] = True

RAIL = [(17.5, 11.0), (17.5, 11.5), (21.5, 11.5), (21.5, 10.0)]   # spoor Uyuni -> Oruro -> La Paz (in vakken)
# segment 0-1: La Paz -> over de altiplano -> Uyuni (gym 1)
path((19, 9), (18, 9), (18, 10))
# segment 2: met de trein terug via Oruro; Potosí (mijn) als zijtak; Cordillera Real (gym 2)
path((17, 11), (21, 11), (21, 10))
path((18, 12), (18, 12))
path((22, 9), (22, 10))
# zijtak: Titicaca (Isla del Sol, Uros, Wanaku, Tiwanaku)
path((21, 8), (22, 8))
# segment 3: Uyuni -> Lípez (Laguna Colorada, geisers, Licancabur) -> San Pedro (gym 3)
path((15, 10), (15, 9))
path((14, 8), (14, 6))
# segment 4: langs de kustwoestijn naar Peru -> Arequipa -> Nazca -> Cuzco (gym 4)
path((13, 5), (13, 4), (25, 4), (25, 5))
path((24, 7), (24, 7))                                     # Rainbow Mountain (en Moray) bij Cuzco
# Inca Trail = Victory Road: Cuzco -> Intipunku -> Machu Picchu (League)
path((26, 7), (27, 7), (27, 6))
# segment 5: lange tocht zuid: terug door Atacama (Valle de la Luna) -> Humahuaca -> Salta -> Cafayate -> Mendoza
#            -> Patagonië -> Buenos Aires (gym 5)
path((12, 7), (12, 10), (13, 10), (13, 11))
path((15, 11), (15, 11))                                   # Humahuaca -> Uyuni (lus terug naar Bolivia)
path((11, 12), (11, 13))                                   # Salta -> Cafayate
path((10, 12), (10, 11))                                   # Cafayate -> Mendoza
path((9, 10), (9, 10))                                     # Aconcagua
path((7, 11), (7, 12))                                     # Mendoza -> Bariloche
path((5, 12), (4, 12), (4, 13))                            # Bariloche -> Perito Moreno (grotten)
path((6, 13), (6, 16), (7, 16))                            # Bariloche -> langs de kust -> Valdés
path((9, 16), (10, 16), (10, 19))                          # Valdés -> Buenos Aires
# segment 6: Buenos Aires -> Iguazú (oversteken) -> Zuid-Brazilië -> Rio (gym 6)
path((13, 19), (14, 19), (14, 17), (16, 17))
path((17, 18), (17, 21), (21, 21))
path((17, 16), (17, 14), (20, 14))                         # optioneel: Pantanal
path((23, 22), (29, 22), (29, 23))                         # optioneel: Salvador
path((31, 23), (34, 23), (34, 21))                         # Salvador -> Lençóis
# segment 7: terug naar de Andes-noordkant (Fly) -> Chavín -> Quito -> Galápagos -> Salento -> Medellín -> Cartagena
#            -> Paramaribo (gym 7)
path((26, 4), (30, 4))
path((31, 5), (32, 5), (32, 6))
path((34, 6), (34, 6))
path((36, 5), (37, 5), (37, 4))
path((40, 4), (40, 8))                                     # Cartagena -> Venezuela (Catatumbo) -> Paramaribo
path((41, 9), (38, 9))                                     # Paramaribo -> tepui/Kaieteur (Mew, optioneel)
# segment 8: Paramaribo -> door het oerwoud naar de Amazone -> de rivier af tot het einde (gym 8)
path((42, 9), (42, 12))

river_route = np.zeros((H, W), bool)
from collections import deque
cell_water = np.array([[(~land[y * 8:(y + 1) * 8, x * 8:(x + 1) * 8]).mean() for x in range(W)] for y in range(H)])
def sea_path(a, b):
    """Kortste pad over vakken die vooral water zijn (rechte stukken zoals Hoenn)."""
    ok = (cell_water >= 0.3) | river_route
    def snap(c):   # dichtstbijzijnde watervak; het stukje kust ertussen hoort bij de route
        best = min(((abs(x - c[0]) + abs(y - c[1]), (x, y)) for y in range(H) for x in range(W) if cell_water[y, x] >= 0.5))
        return best[1]
    a2, b2 = snap(a), snap(b)
    for c, c2 in ((a, a2), (b, b2)):
        before = sea_route.copy()
        path(c, (c2[0], c[1]), c2, sea=True)
        stub[sea_route & ~before] = True
    a, b = a2, b2
    prev = {a: None}
    dq = deque([a])
    while dq:
        c = dq.popleft()
        if c == b:
            break
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = c[0] + dx, c[1] + dy
            if 0 <= nx < W and 0 <= ny < H and ok[ny, nx] and (nx, ny) not in prev:
                prev[(nx, ny)] = c
                dq.append((nx, ny))
    if b not in prev:
        print('geen zeepad', a, b)
        return
    c = b
    while c:
        sea_route[c[1], c[0]] = True
        c = prev[c]
sea_path((42, 13), (31, 12))                               # de Amazone op: monding -> verdronken woud
sea_path((31, 12), (27, 13))                               # -> het einde van de rivier (gym 8)
sea_path((30, 3), (31, 1))                                 # Ecuadoraanse kust -> Galápagos
sea_path((5, 11), (4, 9))                                  # Bariloche/Puerto Montt -> Chiloé
sea_path((39, 16), (36, 14))                               # Belém -> Amazonemonding
sea_path((23, 23), (39, 17))                               # post-game: boot Rio -> Belém
sea_route |= river_route
sea_route &= ~route
# controle: landroutes niet op open zee, zeeroutes niet dwars over land
for y in range(H):
    for x in range(W):
        if route[y, x] and cell_water[y, x] > 0.5:
            print('landroute op water:', x, y)
        if sea_route[y, x] and cell_water[y, x] < 0.3 and not stub[y, x]:
            print('zeeroute over land:', x, y)

rr = np.kron(river_route, np.ones((8, 8), bool))
q = np.pad(rr, 1)
bank = ~rr & (q[:-2, 1:-1] | q[2:, 1:-1] | q[1:-1, :-2] | q[1:-1, 2:]) & land
img[bank] = GREEN[0]

# routes per pixel: half doorzichtig, lichter boven hoger terrein (zoals Hoenn)
rmask = np.kron(route, np.ones((8, 8), bool))
smask = np.kron(sea_route, np.ones((8, 8), bool))
pl = lvl.copy()
pl[biome == 2] = np.clip(lvl[biome == 2], 1, 2)   # over zand: donkerder oranje, anders valt de route weg in het zand
pl[(biome == 3) | (biome == 4)] = 3   # over sneeuw/zout: licht geel (niet de zandkleur)
pl[coast] = 0
paint(rmask, ROUTE, pl)
# water op een landroute wordt waterroute-blauw (zoals het meertje op Route 120 in Hoenn)
paint(rmask & ((lakes & land) | ~land), SEAROUTE, stripes)
cwater = np.kron((cell_water >= 0.5) | river_route, np.ones((8, 8), bool))
paint(smask & ~cwater & land, ROUTE, pl)
paint(smask & (cwater | ~land), SEAROUTE, stripes)

# spoorlijn (nieuw in v3): donkere rails met dwarsliggers over de route, in de icoonkleuren van de Hoenn-kaart
RAILC, TIEC = hexc('#626262'), hexc('#940000')
for (x0, y0), (x1, y1) in zip(RAIL, RAIL[1:]):
    px0, py0, px1, py1 = int(x0 * 8), int(y0 * 8), int(x1 * 8), int(y1 * 8)
    n_ = max(abs(px1 - px0), abs(py1 - py0))
    for i in range(n_ + 1):
        x = px0 + (px1 - px0) * i // max(n_, 1)
        y = py0 + (py1 - py0) * i // max(n_, 1)
        horiz = py0 == py1
        if horiz:
            img[y - 1, x] = RAILC; img[y + 1, x] = RAILC
            if i % 3 == 0:
                img[y, x] = TIEC
        else:
            img[y, x - 1] = RAILC; img[y, x + 1] = RAILC
            if i % 3 == 0:
                img[y, x] = TIEC

# ---------- stadsiconen uit de Hoenn-kaart ----------
d = 'graphics/pokenav/region_map/'
til = Image.open(d + 'map.png').convert('RGB')
tm = open(d + 'map.bin', 'rb').read()
def cell_img(x, y):
    t = tm[y * 64 + x]
    return np.array(til.crop(((t % 16) * 8, (t // 16) * 8, (t % 16) * 8 + 8, (t // 16) * 8 + 8)))
ICONCOL = {hexc(c) for c in ('#940000', '#ff3910', '#ffffff', '#cdcdcd', '#626262', '#ffac10', '#f60000',
                             '#0073ac', '#00398b', '#7bb4d5')}
ICONS = {'town': [[cell_img(6, 5)]], 'spot': [[cell_img(2, 11)]],
         'cityh': [[cell_img(9, 8), cell_img(10, 8)]], 'cityv': [[cell_img(1, 7)], [cell_img(1, 8)]]}
for name, x, y, kind, side, gym in PLACES:
    for r, row in enumerate(ICONS[kind]):
        for c, tile in enumerate(row):
            blk = img[(y + r) * 8:(y + r + 1) * 8, (x + c) * 8:(x + c + 1) * 8]
            m = np.array([[tuple(tile[py, px]) in ICONCOL for px in range(8)] for py in range(8)])
            blk[m] = tile[m]

out = Image.fromarray(img)
out.resize((PW * 3, PH * 3), Image.NEAREST).save('docs/concept/regiokaart3.png')

# ---------- versie met namen en legenda (onder de kaart) ----------
S = 4
big = out.resize((PW * S, PH * S), Image.NEAREST)
LEG_H = 340
canvas = Image.new('RGB', (PW * S, PH * S + LEG_H), hexc('#203050'))
canvas.paste(big, (0, 0))
dr = ImageDraw.Draw(canvas)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
head = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
BADGE = 16
def badge(x, y, g):
    col = hexc('#ffd84a') if g != 'L' else hexc('#ff8a4a')
    dr.rounded_rectangle((x, y, x + BADGE, y + BADGE), 3, fill=col, outline=(20, 30, 50), width=2)
    dr.text((x + BADGE / 2 + 0.5, y + BADGE / 2 + 0.5), g, font=font, fill=(20, 30, 50), anchor='mm')
boxes = []
for name, x, y, kind, side, gym in PLACES:
    w = 2 if kind == 'cityh' else 1
    h = 2 if kind == 'cityv' else 1
    tw = dr.textlength(name, font=font)
    full = tw + (BADGE + 4 if gym else 0)
    if side == 'L':
        tx, ty = x * 8 * S - full - 4, y * 8 * S + 4
    elif side == 'A':
        tx, ty = (x + w / 2) * 8 * S - full / 2, y * 8 * S - 19
    elif side == 'B':
        tx, ty = (x + w / 2) * 8 * S - full / 2, (y + h) * 8 * S + 2
    else:
        tx, ty = (x + w) * 8 * S + 4, y * 8 * S + 4
    tx = max(2, min(PW * S - full - 2, tx))
    dr.text((tx, ty), name, font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(20, 30, 50))
    if gym:
        badge(tx + tw + 5, ty, gym)
    boxes.append((name, tx, ty, tx + full, ty + 16))
# controle: overlappende labels
for i, a in enumerate(boxes):
    for b in boxes[i + 1:]:
        if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
            print('labels overlappen:', a[0], '/', b[0])

# legenda: drie kolommen onder de kaart
y0 = PH * S + 12
cols = [
    [('Fully Ungrounded – regiokaart v3', head), ('voorstel; variant 2 blijft de basis', small), ('', small),
     ('Rode pil: stad   Blauwe stip: dorp/hub', small), ('Rode stip: bijzondere plek of dungeon', small),
     ('Oranje: route   Blauw: waterroute', small), ('Rails: spoor Uyuni – Oruro – La Paz', small),
     ('Geel vakje: gym (L = League, Machu Picchu)', small), ('', small),
     ('Gyms: 1 Ground Uyuni · 2 Ice Cordillera Real', small), ('3 Fire San Pedro · 4 Dragon Cuzco', small),
     ('5 Poison Buenos Aires · 6 Dark Rio', small), ('7 Grass Paramaribo · 8 Bug diepe jungle', small),
     ('E4: Electric, Flying, Ghost, Steel', small), ('Fly na gym 4', small)],
    [('Hoofdpad', head), ('0  La Paz (start, teleférico)', small), ('1  altiplano → Uyuni', small),
     ('2  trein via Oruro → La Paz → Cordillera Real', small), ('3  Lípez (Laguna Colorada, geisers) → San Pedro', small),
     ('4  kustwoestijn → Arequipa → Nazca → Cuzco', small), ('5  lange tocht zuid: Atacama (Valle de la Luna)', small),
     ('    → Humahuaca → Salta → Cafayate → Mendoza', small), ('    → Patagonië → Valdés → Buenos Aires', small),
     ('6  Iguazú (oversteken) → Florianópolis → Rio', small), ('7  (Fly) Andes-noord: Chavín → Quito → Galápagos', small),
     ('    → Salento → Medellín → Cartagena → Paramaribo', small), ('8  oerwoud → de Amazone af tot het einde', small),
     ('L  Cuzco → Inca Trail → Intipunku → Machu Picchu', small)],
    [('Niet als icoon (op de Town Map in het gebied)', head),
     ('Uyuni: Isla Incahuasi, treinkerkhof', small), ('Potosí: mijn van de Cerro Rico (El Tío)', small),
     ('Titicaca: Isla del Sol, Uros, Wanaku, Tiwanaku', small), ('La Paz: Alasitas · Yungas: Dodenweg', small),
     ('Lípez: geisers, Licancabur · Cuzco: Moray,', small), ('   Sacsayhuamán · Inca Trail: Intipunku', small),
     ('Patagonië: Cueva del Milodón, Cuevas de Mármol,', small), ('   Cueva de las Manos · Córdoba: Uritorco', small),
     ('Iguazú: Garganta del Diablo (M\'boí)', small), ('Venezuela: Catatumbo · Guyana: Kaieteur', small),
     ('Amazone: rest houses, Zarude, Paititi (PG)', small), ('Colombia: El Dorado (PG) · Chiloé: Caleuche', small),
     ('Post-game: boot Rio → Belém, spiegel van Uyuni', small)],
]
for ci, col in enumerate(cols):
    yy = y0
    for text, f in col:
        dr.text((24 + ci * 512, yy), text, font=f, fill=(255, 255, 255))
        yy += 23 if f is head else 22
canvas.save('docs/concept/regiokaart3_namen.png')
import sys
if '--grid' in sys.argv:
    print('   ' + ''.join(str(x % 10) for x in range(W)))
    for y in range(H):
        row = ''
        for x in range(W):
            blk = (slice(y * 8, y * 8 + 8), slice(x * 8, x * 8 + 8))
            if cell_water[y, x] >= 0.5:
                row += '~'
                continue
            b = np.bincount(biome[blk][land[blk]], minlength=5).argmax() if land[blk].any() else 0
            if (lakes & land)[blk].mean() > 0.3:
                row += 'l'
            else:
                row += '.sS*z'[b] if b else ('^' if lvl[blk].mean() >= 2.5 else '.')
        print('%2d ' % y + row)
print('ok')
