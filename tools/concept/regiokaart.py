# Fully Ungrounded: schets van de regiokaart in de stijl van de Emerald-regiokaart.
# Kleuren en stadsiconen komen uit graphics/pokenav/region_map (Hoenn). Eén vak = 8x8 pixels, zoals op de GBA.
# Stijlregels (afgekeken van Hoenn): overal kleine hoogtevlekken in vijf groentinten, een donkergroene rand langs
# de kust, verspreide eilandjes, routes half doorzichtig (lichter boven hoger terrein), zee in strepen.
# Uitvoer: docs/concept/regiokaart.png (kaal) en docs/concept/regiokaart_namen.png (met namen en legenda).
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 40, 40            # vakken
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
SALT = [hexc('#ffffff'), hexc('#e6e6e6')]

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

# ---------- land: een gestileerd continent (geïnspireerd, niet nagemeten) ----------
def interp(pts, y):
    return np.interp(y, [p[0] for p in pts], [p[1] for p in pts])
WEST = [(1, 11), (5, 7.5), (9, 6.5), (14, 6), (18, 8), (22, 9.5), (27, 10.5), (31, 11), (35, 12), (39, 14)]
EAST = [(1, 19), (3, 30), (6, 36.5), (10, 38), (15, 37.5), (20, 35), (25, 31), (29, 26), (32, 22), (35, 19.5), (39, 18)]
wc, ec = interp(WEST, cy), interp(EAST, cy)
land = (cx > wc + (n - 0.5) * 2.4) & (cx < ec + (n - 0.5) * 2.8) & (cy > 1.2 + (n - 0.5) * 2) & (cy < 38.3)
land &= ~((cy < 3.5) & (cx > 20) & (cx < 27) & (n < 0.55))                      # Caribische baai
land &= ~(ellipse(37.5, 9.6, 2.2, 1.1) & ~ellipse(36.3, 10.6, 0.9, 0.5))          # Amazonemonding, Marajó blijft
land &= ~(ellipse(24.2, 31.4, 1.6, 0.7))                                         # Río de la Plata
fjord = (cy > 31) & (cx < wc + 1.6) & (value_noise(55, 3) > 0.5)                # Chileense fjorden
land &= ~fjord

islands = (ellipse(3, 13, 1.2, 0.8) | ellipse(4.6, 14.2, 0.7, 0.5) | ellipse(2.4, 14.6, 0.5, 0.4)   # Galápagos
           | ellipse(2.5, 30, 0.7, 0.5)                                                             # Paaseiland
           | ellipse(17.5, 39, 2.6, 0.8)                                                            # Vuurland
           | ellipse(25, 1.3, 1.6, 0.5) | ellipse(29.5, 1.6, 0.8, 0.4)                              # Caribisch
           | ellipse(38.6, 13, 0.5, 0.35))                                                          # Fernando de Noronha
land |= islands & (n > 0.3)
# losse eilandjes langs de kust, zoals in Hoenn
sea_d = np.zeros_like(land)
pad = land.copy()
for _ in range(10):
    p = np.pad(pad, 1)
    pad = pad | p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
near = pad & ~land
dots = near & (value_noise(66, 3) > 0.84) & ((cy < 5) | (cy > 30) | (cx > 33))
land |= dots

# ---------- hoogte ----------
ridge = wc + 3.0 + 0.6 * np.sin(cy * 0.45)
andes = np.exp(-((cx - ridge) / 2.6) ** 2)
plateau = np.exp(-(((cx - 15.5) / 4.0) ** 2 + ((cy - 20.5) / 4.5) ** 2) ** 1.5)    # altiplano
brazil = 0.35 * np.exp(-(((cx - 31) / 4.5) ** 2 + ((cy - 17) / 5) ** 2))
tepui = 0.35 * np.exp(-(((cx - 25) / 4) ** 2 + ((cy - 5.5) / 2) ** 2))
amazon = np.exp(-(((cx - 25) / 9) ** 2 + ((cy - 11) / 5) ** 2))
pantanal = np.exp(-(((cx - 25) / 2.5) ** 2 + ((cy - 19.5) / 2) ** 2))
elev = (np.maximum(andes * 0.95, plateau * 0.8) + brazil + tepui
        + (hills - 0.5) * 0.75 + 0.22 - amazon * 0.18 - pantanal * 0.25)
# donkergroene rand langs de kust
coast = np.zeros_like(land)
p = land.copy()
for _ in range(3):
    q = np.pad(p, 1)
    p = p & q[:-2, 1:-1] & q[2:, 1:-1] & q[1:-1, :-2] & q[1:-1, 2:]
coast = land & ~p
lvl = np.digitize(elev, [0.28, 0.42, 0.6, 0.8])   # 0..4
lvl[coast] = 0

# ---------- biomen (in Hoenn-kleuren) ----------
biome = np.zeros((PH, PW), int)   # 0 groen, 2 woestijn, 3 sneeuw, 4 zout
desert = land & (cy > 15.5) & (cy < 31) & (cx < ridge - 0.8 + (n - 0.5) * 2)
desert |= land & ellipse(14.5, 27, 3.6, 2.6)                                       # Atacama-hoogland/Lípez
desert |= land & ellipse(32.5, 12.2, 1.4, 0.7) & (fine > 0.3)                     # Lençóis Maranhenses
biome[desert] = 2
snow = land & (((lvl >= 4) & (cy > 14) & (cy < 31) & (hills > 0.6) & (n > 0.5))
               | ((cy > 31) & (lvl >= 3)) | (cy > 37.8)
               | (ellipse(18.3, 18.3, 1.2, 1.6) & (lvl >= 2))                      # Cordillera Real
               | (ellipse(13.4, 28.3, 0.7, 0.5)))                                 # vulkanen/sneeuw van Lípez
biome[snow] = 3
salt = ellipse(14.2, 24.2, 2.2, 1.1) & (n > 0.3)
biome[salt] = 4
lakes = ((ellipse(13.4, 18.7, 1.5, 0.75) & (n > 0.3))                            # Titicaca
         | ellipse(13.3, 34.6, 0.5, 0.3) | ellipse(14.4, 35.6, 0.6, 0.35) | ellipse(15.1, 33.4, 0.4, 0.3)
         | ellipse(13.6, 26.4, 0.45, 0.3)                                         # Laguna Colorada
         | (ellipse(25, 19.6, 1.8, 1.2) & (value_noise(70, 4) > 0.55)))          # Pantanal
lakes &= land

# ---------- rivieren ----------
river = np.zeros((PH, PW), bool)
def draw_river(points, width=1, wobble=2.0):
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 16)
        for i in range(steps + 1):
            t = i / steps
            x, y = (x0 + (x1 - x0) * t) * 8, (y0 + (y1 - y0) * t) * 8
            y += math.sin(t * 9 + x0) * wobble
            river[max(0, int(y) - width):int(y) + width + 1, max(0, int(x) - width):int(x) + width + 1] = True
draw_river([(12.5, 12.5), (16, 11.8), (20, 12.4), (22.5, 12.0)], 1)
draw_river([(22.5, 12.0), (26, 11.6), (30, 10.8), (34, 10.4), (37.5, 10)], 2, 1.0)   # Amazone (bevaarbaar)
draw_river([(14.5, 8), (17, 10), (19, 12.1)], 0)
draw_river([(22, 17), (23, 14), (24.5, 11.8)], 0)
draw_river([(28, 6), (28.5, 9), (29, 10.8)], 0)
draw_river([(25, 20.5), (25.5, 22.5), (25, 25), (24, 28), (23.6, 30.6)], 1)          # Paraná / Iguazú
draw_river([(19.5, 26.5), (21, 28), (23.6, 30.6)], 0)
river &= land

# ---------- schilderen ----------
img = np.zeros((PH, PW, 3), np.uint8)
stripes = ys.astype(int) % 2
def paint(mask, pal, idx):
    for i, c in enumerate(pal):
        img[mask & (idx == i)] = c
paint(~land, SEA, stripes)
paint(land & (biome == 0), GREEN, lvl)
paint(land & (biome == 2) & (lvl <= 1), SAND, stripes)
paint(land & (biome == 2) & (lvl >= 2) & (lvl <= 3), SAND_HI, stripes)
paint(land & (biome == 2) & (lvl >= 4), [hexc('#eee6ac'), hexc('#cdcd94'), hexc('#e6cd8b')], np.digitize(fine, [0.45, 0.7]))
snowedge = np.zeros_like(land)
sm = land & (biome == 3)
q = np.pad(sm, 1)
snowedge = sm & ~(q[:-2, 1:-1] & q[2:, 1:-1] & q[1:-1, :-2] & q[1:-1, 2:])
img[sm] = SNOW[0]
img[snowedge] = SNOW[1]
crack = ((xs.astype(int) + ys.astype(int) * 2) % 7 == 0) | ((xs.astype(int) - ys.astype(int) * 2) % 9 == 0)
paint(land & (biome == 4), SALT, crack.astype(int))
paint(lakes | river, SEA, stripes)
img[coast & (biome == 2)] = SAND[1]

# ---------- plaatsen (vakcoördinaten) ----------
# soort: 'cityh'/'cityv' = rode pil (stad), 'town' = blauwe stip (dorp of hub in de natuur), 'spot' = rode stip
PLACES = [
    ('La Paz (start)', 16, 20, 'cityh'),
    ('Cordillera Real', 18, 18, 'town'),
    ('Uyuni', 17, 24, 'town'),
    ('Lípez', 13, 26, 'town'),
    ('Potosí', 19, 23, 'town'),
    ('Cuzco', 12, 15, 'cityv'),
    ('Machu Picchu (League)', 10, 13, 'spot'),
    ('Rainbow Mountain', 14, 16, 'spot'),
    ('Lima', 8, 15, 'cityv'),
    ('Huacachina', 8, 18, 'spot'),
    ('Nazca', 9, 20, 'spot'),
    ('Arequipa', 11, 21, 'town'),
    ('Quito', 9, 10, 'town'),
    ('San Pedro', 11, 28, 'cityh'),
    ('Salta', 17, 28, 'town'),
    ('Aconcagua', 11, 30, 'spot'),
    ('Mendoza', 13, 31, 'cityh'),
    ('Bariloche', 15, 35, 'cityh'),
    ('Torres del Paine', 12, 37, 'spot'),
    ('Valdés', 20, 34, 'spot'),
    ('Buenos Aires', 22, 31, 'cityh'),
    ('Iguazú', 26, 24, 'town'),
    ('Pantanal', 24, 21, 'town'),
    ('Rio de Janeiro', 34, 22, 'cityv'),
    ('Salvador', 36, 17, 'town'),
    ('Lençóis', 32, 13, 'spot'),
    ('Noronha', 38, 14, 'spot'),
    ('Belém', 34, 9, 'town'),
    ('Amazone-lodge', 28, 12, 'town'),
    ('Amazone-stad', 22, 11, 'cityh'),
    ('Paramaribo', 30, 4, 'cityh'),
    ('Tepuis / Angel Falls', 24, 6, 'spot'),
    ('Medellín', 10, 7, 'cityv'),
    ('Salento', 12, 9, 'town'),
    ('Cartagena', 11, 3, 'cityh'),
    ('Galápagos', 3, 13, 'spot'),
    ('Paaseiland', 2, 30, 'spot'),
    ('Vuurland', 18, 39, 'spot'),
]

# ---------- routes (vakken; horizontale/verticale stukken zoals in Hoenn) ----------
route = np.zeros((H, W), bool)
sea_route = np.zeros((H, W), bool)
def path(*pts, sea=False):
    tgt = sea_route if sea else route
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            tgt[y0, x] = True
        for y in range(min(y0, y1), max(y0, y1) + 1):
            tgt[y, x1] = True

path((16, 20), (16, 24), (17, 24))                         # La Paz -> Uyuni (gym 1)
path((17, 24), (12, 24), (12, 26), (13, 26))               # zoutvlakte -> Lípez (bronnen, geisers, vulkaan)
path((13, 26), (13, 27), (12, 27), (12, 28))               # Lípez -> San Pedro
path((17, 24), (19, 24), (19, 23))                         # Uyuni -> Potosí
path((19, 23), (19, 21), (18, 21), (18, 18))               # Potosí -> Cordillera Real (lus)
path((16, 20), (18, 20))
path((16, 20), (14, 20), (14, 16), (12, 16), (12, 15))     # Titicaca -> Cuzco
path((12, 15), (10, 15), (10, 13))                         # Machu Picchu
path((12, 15), (8, 15))                                    # Cuzco -> Lima
path((8, 15), (8, 18), (9, 18), (9, 20))                   # Huacachina -> Nazca
path((9, 20), (9, 21), (11, 21), (14, 21), (14, 20))       # Arequipa -> terug naar Titicaca (lus)
path((12, 28), (17, 28))                                   # busrit San Pedro -> Salta
path((17, 28), (17, 31), (13, 31))                         # Salta -> Mendoza
path((13, 31), (11, 31), (11, 30))                         # Aconcagua
path((13, 31), (13, 35), (15, 35))                         # Mendoza -> Bariloche
path((13, 35), (13, 37), (12, 37))                         # Torres del Paine
path((17, 31), (22, 31))                                   # -> Buenos Aires
path((22, 31), (22, 34), (20, 34))                         # Valdés
path((22, 31), (22, 26), (26, 26), (26, 24))               # Buenos Aires -> Iguazú
path((26, 24), (26, 22), (24, 22), (24, 21))               # Iguazú -> Pantanal
path((19, 23), (22, 23), (22, 21), (24, 21))               # Potosí -> Pantanal (oostelijke afdaling)
path((26, 24), (30, 24), (30, 22), (34, 22))               # Iguazú -> Rio
path((34, 22), (34, 17), (36, 17))                         # Rio -> Salvador
path((12, 15), (12, 12), (22, 12), (22, 11))               # Cuzco -> Amazone-stad
path((22, 11), (22, 8), (12, 8), (12, 9))                  # Amazone-stad -> Salento
path((12, 9), (10, 9), (10, 7))                            # Salento -> Medellín
path((10, 9), (9, 9), (9, 10))                             # Quito
path((10, 7), (10, 4), (11, 4), (11, 3))                   # Medellín -> Cartagena
path((22, 8), (24, 8), (24, 6))                            # tepuis
path((24, 8), (28, 8), (28, 4), (30, 4))                   # -> Paramaribo
path((22, 12), (22, 16), (20, 16), (20, 19), (22, 19), (22, 21))   # dwars door de jungle naar de Pantanal
path((22, 16), (25, 16), (25, 14))                        # jungle-lus naar het oosten
path((28, 12), (28, 16), (31, 16), (31, 19), (34, 19))    # Amazone-lodge -> zuid door de jungle -> Rio/Salvador
# waterroutes: zijrivieren
path((24, 13), (24, 15), sea=True)
path((28, 9), (28, 7), sea=True)
# waterroutes: de Amazone af naar zee, kust en eilanden
path((23, 11), (27, 11), (27, 12), (28, 12), (29, 12), (29, 10), (34, 10), (34, 9), sea=True)
path((35, 9), (36, 9), (36, 12), (34, 12), (34, 13), (33, 13), sea=True)          # Belém -> Lençóis
path((37, 12), (38, 12), (38, 14), sea=True)
path((13, 3), (25, 2), (29, 3), sea=True)
path((32, 4), (36, 4), (36, 8), sea=True)                  # Paramaribo -> Belém
path((7, 15), (5, 15), (5, 13), sea=True)                  # Lima -> Galápagos
path((10, 30), (4, 30), sea=True)                          # Paaseiland
path((15, 36), (15, 38), (17, 38), sea=True)               # Vuurland
sea_route &= ~route

# routes per pixel: half doorzichtig, lichter boven hoger terrein (zoals Hoenn)
rmask = np.kron(route, np.ones((8, 8), bool))
smask = np.kron(sea_route, np.ones((8, 8), bool))
pl = lvl.copy()
pl[(biome == 2) | (biome == 3) | (biome == 4)] = 4
pl[lakes | river | ~land] = 1
paint(rmask, ROUTE, pl)
paint(smask, SEAROUTE, stripes)

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
out.resize((PW * 3, PH * 3), Image.NEAREST).save('docs/concept/regiokaart.png')

# ---------- versie met namen ----------
S = 3
big = out.resize((PW * S, PH * S), Image.NEAREST)
canvas = Image.new('RGB', (PW * S + 320, PH * S), hexc('#203050'))
canvas.paste(big, (0, 0))
dr = ImageDraw.Draw(canvas)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 13)
small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
LEFT = {'Lima', 'Quito', 'Huacachina', 'Rio de Janeiro', 'Salvador', 'Noronha', 'Belém', 'Arequipa', 'San Pedro',
        'Torres del Paine', 'Medellín', 'Paramaribo'}
for name, x, y, kind in PLACES:
    w = 2 if kind == 'cityh' else 1
    tw = dr.textlength(name, font=font)
    tx = x * 8 * S - tw - 4 if name in LEFT else (x + w) * 8 * S + 4
    if name == 'Paramaribo':
        tx = (x + w) * 8 * S + 4
    dr.text((max(2, tx), y * 8 * S + 4), name, font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(20, 30, 50))
lx = PW * S + 16
lines = [('Pokémon Fully Ungrounded', font), ('Regiokaart – schets 2', small), ('', small),
         ('Rode pil: stad', small), ('Blauwe stip: dorp of hub', small), ('   in de natuur', small),
         ('Rode stip: bijzondere plek', small), ('Oranje: route', small), ('Donkerblauw: waterroute', small),
         ('', small), ('Lichter groen: hoger', small), ('Zand: woestijn en duinen', small),
         ('Wit: sneeuw, ijs, zout', small), ('', small),
         ('Gym 1: Uyuni (Ground)', small), ('Gym 2: Ice (plek open)', small), ('League: Machu Picchu', small),
         ('   (Cuzco al eerder bezocht)', small), ('', small),
         ('De Amazone is bevaarbaar', small), ('tot aan zee (Belém) en je', small), ('kunt er dwars doorheen.', small)]
yy = 16
for text, f in lines:
    dr.text((lx, yy), text, font=f, fill=(255, 255, 255))
    yy += 22
canvas.save('docs/concept/regiokaart_namen.png')
print('ok')
