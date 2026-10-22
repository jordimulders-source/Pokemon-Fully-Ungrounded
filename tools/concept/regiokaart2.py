# Fully Ungrounded: variant 2 van de regiokaart (gedraaid, binnenzee, landmarks) in de stijl van de Emerald-regiokaart.
# Kleuren en stadsiconen komen uit graphics/pokenav/region_map (Hoenn). Eén vak = 8x8 pixels, zoals op de GBA.
# Stijlregels (afgekeken van Hoenn): alleen Hoenn-kleuren; hoogte = geneste vlekken die naar binnen lichter worden
# (lichtste groen zeldzaam), donkergroene rand van 2-7 px langs elke kust en elk meer, geen spikkels (eilandjes >= 24 px,
# licht midden), vlakke oppervlakken (zee, zand, zout) in strepen van 1 px, routes lichter boven hoger terrein.
# Uitvoer: docs/concept/regiokaart.png (kaal) en docs/concept/regiokaart_namen.png (met namen en legenda).
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
desert = land & (cx > 14) & (cx < 28) & (cy < ridge - 0.9 + (n - 0.5) * 2)              # kustwoestijn (Atacama/Peru)
desert |= land & (cx > 15 + (pn - 0.5) * 3) & (cx < 20.5 + (pn - 0.5) * 3) & (cy < ridge + 2.4 + (pn - 0.5) * 5)   # puna/Lípez
desert |= land & rellipse(35.5 + (value_noise(93, 5) - 0.5) * 1.2, 22.6, 1.5, 0.7, 0)    # Lençóis
biome[desert] = 2
snow = land & (((lvl >= 4) & (cx > 9) & (cx < 30) & (andes > 0.75) & (biome != 2))
               | ((cx < 10) & (lvl >= 3)) | (cx < 3.4)
               | (ellipse(23.2, 10.2, 1.4, 1.0) & (lvl >= 2))          # Cordillera Real
               | ellipse(16.4, 6.9, 0.6, 0.5))                         # vulkaan van Lípez (Licancabur)
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
         | ellipse(7.5, 10.4, 0.5, 0.3) | ellipse(6.4, 11.5, 0.6, 0.35) | ellipse(8.6, 11.0, 0.4, 0.3)   # meren bij Bariloche
         | ellipse(16.0, 8.4, 0.4, 0.28)                                                              # Laguna Colorada
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
PLACES = [
    ('La Paz (start)', 20, 9, 'cityh'),
    ('Cordillera Real', 23, 10, 'town'),
    ('Uyuni', 18, 10, 'town'),
    ('Lípez', 15, 8, 'town'),
    ('Potosí', 19, 12, 'town'),
    ('Cuzco', 25, 6, 'cityv'),
    ('Machu Picchu', 26, 5, 'spot'),
    ('Rainbow Mountain', 24, 8, 'spot'),
    ('Lima', 26, 3, 'cityv'),
    ('Huacachina', 24, 3, 'spot'),
    ('Nazca', 23, 4, 'spot'),
    ('Arequipa', 21, 5, 'town'),
    ('Quito', 30, 5, 'town'),
    ('San Pedro', 13, 6, 'cityh'),
    ('Salta', 14, 10, 'town'),
    ('Aconcagua', 9, 6, 'spot'),
    ('Mendoza', 10, 7, 'cityh'),
    ('Bariloche', 6, 9, 'cityh'),
    ('Torres del Paine', 5, 10, 'spot'),
    ('Vuurland', 2, 15, 'spot'),
    ('Valdés', 9, 16, 'spot'),
    ('Buenos Aires', 11, 20, 'cityh'),
    ('Iguazú', 17, 17, 'town'),
    ('Pantanal', 21, 14, 'town'),
    ('Rio de Janeiro', 22, 22, 'cityv'),
    ('Salvador', 30, 23, 'town'),
    ('Lençóis', 35, 21, 'spot'),
    ('Noronha', 40, 24, 'spot'),
    ('Belém', 39, 16, 'town'),
    ('Amazone-stad', 24, 12, 'cityh'),
    ('Verdronken woud', 31, 12, 'town'),
    ('Reuzentepui', 37, 9, 'spot'),
    ('Paramaribo', 41, 8, 'cityh'),
    ('Medellín', 35, 5, 'cityv'),
    ('Salento', 33, 6, 'town'),
    ('Cartagena', 39, 4, 'cityh'),
    ('Galápagos', 31, 1, 'spot'),
    ('Paaseiland', 13, 1, 'spot'),
]

# ---------- routes ----------
route = np.zeros((H, W), bool)
sea_route = np.zeros((H, W), bool)
def path(*pts, sea=False):
    tgt = sea_route if sea else route
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            tgt[y0, x] = True
        for y in range(min(y0, y1), max(y0, y1) + 1):
            tgt[y, x1] = True

path((19, 9), (19, 10))                                    # La Paz -> Uyuni (gym 1)
path((18, 9), (16, 9), (16, 8))                            # Uyuni -> zoutvlakte -> Lípez
path((15, 7), (15, 6))                                     # Lípez -> San Pedro
path((19, 11), (19, 12))                                   # Uyuni -> Potosí
path((20, 12), (22, 12), (22, 10))                         # Potosí -> Cordillera Real
path((22, 9), (23, 9), (23, 10))                           # La Paz -> Cordillera Real
path((22, 9), (24, 9), (24, 7), (25, 7))                   # langs Titicaca, Rainbow Mountain -> Cuzco
path((25, 5), (26, 5))                                     # Machu Picchu
path((25, 5), (25, 4))                                     # Cuzco -> Lima
path((25, 3), (24, 3), (23, 3), (23, 4))                   # Lima -> Huacachina -> Nazca
path((23, 5), (21, 5))                                     # Nazca -> Arequipa
path((21, 6), (20, 6), (20, 8))                            # Arequipa -> La Paz (lus)
path((14, 7), (14, 10))                                    # busrit San Pedro -> Salta
path((13, 10), (12, 10), (12, 7))                          # Salta -> Mendoza
path((10, 6), (9, 6))                                      # Aconcagua
path((10, 8), (10, 9), (8, 9))                             # Mendoza -> Bariloche
path((6, 10), (5, 10))                                     # Torres del Paine
path((14, 11), (14, 20), (13, 20))                         # Salta -> Buenos Aires
path((11, 19), (11, 17), (9, 17), (9, 16))                 # Valdés
path((14, 17), (17, 17))                                   # Buenos Aires-route -> Iguazú
path((17, 16), (17, 14), (21, 14))                         # Iguazú -> Pantanal
path((19, 13), (19, 14))                                   # Potosí -> Pantanal
path((17, 18), (17, 21), (22, 21))                         # Iguazú -> Rio
path((23, 22), (29, 22), (29, 23))                         # Rio -> Salvador
path((25, 8), (25, 11))                                    # Cuzco -> Amazone-stad
path((24, 11), (24, 10), (28, 10), (28, 5), (30, 5))       # Amazone-stad -> Quito
path((31, 5), (33, 5), (33, 6))                            # Quito -> Salento
path((34, 6), (34, 6))                                     # Salento -> Medellín
path((36, 5), (38, 5), (38, 4))                            # Medellín -> Cartagena
path((35, 7), (35, 9), (36, 9))                            # Medellín -> reuzentepui
path((38, 9), (40, 9), (40, 8))                            # tepui -> Paramaribo
path((22, 15), (22, 18), (32, 18), (32, 17))               # dwars door de jungle naar de zuidoever van de binnenzee (late game)

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
        path(c, (c2[0], c[1]), c2, sea=True)
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
sea_path((26, 12), (31, 12))                               # Amazone-stad -> verdronken woud (binnenzee)
sea_path((31, 12), (39, 16))                               # -> Belém (uitstroom naar zee)
sea_path((39, 16), (40, 24))                               # Belém -> Noronha
sea_path((36, 21), (40, 24))                               # Lençóis -> Noronha
sea_path((26, 3), (31, 1))                                 # Lima -> Galápagos
sea_path((13, 5), (13, 1))                                 # San Pedro -> Paaseiland
sea_path((5, 10), (2, 15))                                  # Torres del Paine -> Vuurland
sea_path((41, 4), (41, 7))                                 # Cartagena -> Paramaribo
sea_route |= river_route
sea_route &= ~route
# controle: landroutes op land, zeeroutes op water
for y in range(H):
    for x in range(W):
        if route[y, x] and cell_water[y, x] > 0.5:
            print('landroute op water:', x, y)

# rivierbedding van de Amazone: oevers in donkergroen
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
# zeeroutes: vakken die vooral land zijn (het stukje van de stad naar de kust) worden landroute
cwater = np.kron((cell_water >= 0.5) | river_route, np.ones((8, 8), bool))
paint(smask & ~cwater & land, ROUTE, pl)
paint(smask & (cwater | ~land), SEAROUTE, stripes)

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
for name, x, y, kind in PLACES:
    for r, row in enumerate(ICONS[kind]):
        for c, tile in enumerate(row):
            blk = img[(y + r) * 8:(y + r + 1) * 8, (x + c) * 8:(x + c + 1) * 8]
            m = np.array([[tuple(tile[py, px]) in ICONCOL for px in range(8)] for py in range(8)])
            blk[m] = tile[m]

out = Image.fromarray(img)
out.resize((PW * 3, PH * 3), Image.NEAREST).save('docs/concept/regiokaart2.png')

# ---------- versie met namen ----------
S = 3
big = out.resize((PW * S, PH * S), Image.NEAREST)
canvas = Image.new('RGB', (PW * S + 320, PH * S), hexc('#203050'))
canvas.paste(big, (0, 0))
dr = ImageDraw.Draw(canvas)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
LEFT = {'Huacachina', 'Arequipa', 'Torres del Paine', 'Aconcagua', 'Valdés', 'Lípez', 'Salta', 'Nazca'}
ABOVE = {'Machu Picchu', 'Lima'}
for name, x, y, kind in PLACES:
    w = 2 if kind == 'cityh' else 1
    tw = dr.textlength(name, font=font)
    tx = x * 8 * S - tw - 4 if name in LEFT else (x + w) * 8 * S + 4
    ty = y * 8 * S + 4
    if name in ABOVE:
        tx, ty = x * 8 * S + 12 - tw / 2, y * 8 * S - 18
    dr.text((max(2, tx), ty), name, font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(20, 30, 50))
lx = PW * S + 16
lines = [('Pokémon Fully Ungrounded', font), ('Regiokaart – variant 2', small), ('', small),
         ('Rode pil: stad', small), ('Blauwe stip: dorp of hub', small), ('   in de natuur', small),
         ('Rode stip: bijzondere plek', small), ('Oranje: route', small), ('Donkerblauw: waterroute', small),
         ('', small), ('Lichter groen: hoger', small), ('Zand: woestijn en duinen', small),
         ('Wit: sneeuw, ijs, zout', small), ('', small),
         ('Gym 1: Uyuni (Ground)', small), ('Gym 2: Ice (plek open)', small), ('League: Machu Picchu', small),
         ('   (Cuzco al eerder bezocht)', small), ('', small),
         ('Gedraaid zoals Hoenn (Kyushu).', small), ('Het Amazonebekken is een', small), ('binnenzee met een verdronken', small), ('woud (het oude Pebas-meer).', small),
         ('', small), ('Landmarks: reuzentepui,', small), ('vulkaaneiland in de Titicaca,', small), ('Nazca-kolibrie in de woestijn.', small)]
yy = 16
for text, f in lines:
    dr.text((lx, yy), text, font=f, fill=(255, 255, 255))
    yy += 22
canvas.save('docs/concept/regiokaart2_namen.png')
print('ok')
