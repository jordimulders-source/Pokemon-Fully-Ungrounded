# Fully Ungrounded: eerste schets van de regiokaart in de stijl van de Emerald-regiokaart.
# Kleuren en stadsiconen komen uit graphics/pokenav/region_map (Hoenn). Eén vak = 8x8 pixels, zoals op de GBA.
# Uitvoer: docs/concept/regiokaart.png (kaal) en docs/concept/regiokaart_namen.png (met namen en legenda).
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 40, 40            # vakken
PW, PH = W * 8, H * 8    # pixels
rng = random.Random(1)

def hexc(s):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))

SEA = [hexc('#9cd5ff'), hexc('#a4b4ff')]
SEAROUTE = [hexc('#4a9ce6'), hexc('#2983e6')]
GREEN = [hexc(c) for c in ('#007300', '#39ac08', '#62d500', '#acee31', '#d5ff7b')]
JUNGLE = [hexc('#005a00'), hexc('#007300'), hexc('#1f8f04')]
SAND = [hexc(c) for c in ('#cdcd94', '#eee6ac', '#f6eec5', '#fff6de')]
SNOW = [hexc(c) for c in ('#9cb4cd', '#c5d5ee', '#e6eef6', '#ffffff')]
SALT = [hexc('#ffffff'), hexc('#dee6ee')]
ROUTE = [hexc(c) for c in ('#e6a400', '#e6a400', '#eebd39', '#f6d552', '#eee673')]
ROUTE_LIGHT = hexc('#eee6ac')

# ---------- ruis ----------
def value_noise(seed, scale):
    r = random.Random(seed)
    gw, gh = PW // scale + 3, PH // scale + 3
    g = np.array([[r.random() for _ in range(gw)] for _ in range(gh)])
    ys, xs = np.mgrid[0:PH, 0:PW] / scale
    x0, y0 = xs.astype(int), ys.astype(int)
    fx, fy = xs - x0, ys - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a = g[y0, x0] * (1 - fx) + g[y0, x0 + 1] * fx
    b = g[y0 + 1, x0] * (1 - fx) + g[y0 + 1, x0 + 1] * fx
    return a * (1 - fy) + b * fy

def fbm(seed):
    return (value_noise(seed, 32) * 0.5 + value_noise(seed + 1, 16) * 0.3 + value_noise(seed + 2, 8) * 0.2)

ys, xs = np.mgrid[0:PH, 0:PW].astype(float)
cx, cy = xs / 8, ys / 8   # in vakken

# ---------- land: een gestileerd continent (geïnspireerd, niet nagemeten) ----------
def west_coast(y):   # x van de westkust per rij (vakken)
    pts = [(1, 11), (5, 7.5), (9, 6.5), (14, 6), (18, 8), (22, 9.5), (27, 10.5), (31, 11), (35, 12), (39, 14)]
    return np.interp(y, [p[0] for p in pts], [p[1] for p in pts])

def east_coast(y):
    pts = [(1, 19), (3, 30), (6, 36.5), (10, 38), (15, 37.5), (20, 35), (25, 31), (29, 26), (32, 22), (35, 19.5), (39, 18)]
    return np.interp(y, [p[0] for p in pts], [p[1] for p in pts])

n = fbm(10)
wc, ec = west_coast(cy), east_coast(cy)
land = (cx > wc + (n - 0.5) * 2.2) & (cx < ec + (n - 0.5) * 2.6) & (cy > 1.2 + (n - 0.5) * 2) & (cy < 38.5)
# noordkust grilliger (Caribisch)
land &= ~((cy < 3.5) & (cx > 20) & (cx < 27) & (n < 0.55))

def ellipse(x0, y0, rx, ry):
    return ((cx - x0) / rx) ** 2 + ((cy - y0) / ry) ** 2 < 1

# eilanden (Galápagos, Paaseiland, Vuurland, Chiloé, Caribisch)
islands = (ellipse(3, 13, 1.2, 0.8) | ellipse(4.6, 14.2, 0.7, 0.5) | ellipse(2.4, 14.6, 0.5, 0.4)
           | ellipse(2.5, 30, 0.7, 0.5)
           | ellipse(17.5, 39, 2.6, 0.9) | ellipse(13.2, 34.5, 0.6, 1.4)
           | ellipse(25, 1.3, 1.6, 0.5) | ellipse(29.5, 1.6, 0.8, 0.4))
land |= islands & (n > 0.32)

# ---------- hoogte ----------
ridge = west_coast(cy) + 3.0 + 0.6 * np.sin(cy * 0.45)
andes = np.exp(-((cx - ridge) / 2.6) ** 2)
plateau = np.exp(-(((cx - 15.5) / 4.0) ** 2 + ((cy - 20.5) / 4.5) ** 2) ** 1.5)   # altiplano
brazil = 0.45 * np.exp(-(((cx - 30) / 4.5) ** 2 + ((cy - 19) / 4) ** 2))
guiana = 0.35 * np.exp(-(((cx - 25) / 4) ** 2 + ((cy - 6) / 2) ** 2))
elev = np.maximum(andes * (0.85 + 0.15 * n), plateau * 0.8) + brazil + guiana + (n - 0.5) * 0.25
amazon = np.exp(-(((cx - 25) / 9) ** 2 + ((cy - 11) / 5) ** 2))
elev -= amazon * 0.35
elev = np.clip(elev, 0, 1.2)

lvl = np.digitize(elev, [0.18, 0.36, 0.55, 0.78])   # 0..4

# ---------- biomen ----------
biome = np.zeros((PH, PW), int)   # 0 groen, 1 jungle, 2 woestijn, 3 sneeuw, 4 zout, 5 meer
jungle = land & (amazon * (0.8 + 0.4 * n) > 0.45) & (lvl <= 1)
biome[jungle] = 1
desert = land & (cy > 16) & (cy < 31) & (cx < ridge - 0.6 + (n - 0.5) * 2)
biome[desert] = 2
puna = land & ellipse(14.5, 26.5, 4, 3) & (lvl >= 1)          # Atacama-hoogland
biome[puna] = 2
snow = land & (((lvl >= 4) & (cy < 31) & (n > 0.5) & (cy > 14)) | ((cy > 31) & (lvl >= 2)) | (cy > 37.3)
               | (ellipse(18, 18.5, 1.8, 2.3) & (lvl >= 2)))   # Cordillera Real naast de startstad
biome[snow] = 3
salt = ellipse(14.2, 24.2, 2.2, 1.2) & (n > 0.3)
biome[salt] = 4
lakes = (ellipse(13.4, 18.7, 1.5, 0.75) & (n > 0.3)          # Titicaca
         | ellipse(13.3, 34.6, 0.5, 0.3) | ellipse(14.4, 35.6, 0.6, 0.35) | ellipse(15.1, 33.4, 0.4, 0.3))
biome[lakes] = 5

# ---------- rivieren ----------
river = np.zeros((PH, PW), bool)
def draw_river(points, width=1.0):
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 16)
        for i in range(steps + 1):
            t = i / steps
            x, y = (x0 + (x1 - x0) * t) * 8, (y0 + (y1 - y0) * t) * 8
            wob = math.sin(t * 9 + x0) * 2
            y += wob
            r = int(width)
            river[max(0, int(y) - r):int(y) + r + 1, max(0, int(x) - r):int(x) + r + 1] = True
draw_river([(13, 12), (17, 11.5), (21, 12.5), (25, 11.5), (29, 10.5), (33, 10), (37.5, 9)], 1)      # Amazone
draw_river([(14.5, 8), (17, 10), (19, 12.2)], 0.6)
draw_river([(22, 16.5), (23, 14), (24.5, 11.8)], 0.6)
draw_river([(28, 6), (28.5, 9), (29, 10.5)], 0.6)
draw_river([(25.5, 22.5), (25, 25), (24, 28), (23.2, 30.2)], 0.8)                                       # Paraná / Iguazú
draw_river([(19.5, 26.5), (21, 28), (23.2, 30.2)], 0.6)
river &= land & ~lakes

# ---------- schilderen ----------
img = np.zeros((PH, PW, 3), np.uint8)
stripes = (ys.astype(int) % 2)
for i in range(2):
    img[(~land) & (stripes == i)] = SEA[i]

def paint(mask, pal, idx):
    for i, c in enumerate(pal):
        img[mask & (idx == i)] = c

paint(land & (biome == 0), GREEN, lvl)
jn = value_noise(77, 3)
paint(land & (biome == 1), JUNGLE, np.digitize(jn, [0.35, 0.7]))
paint(land & (biome == 2), SAND, np.clip(lvl, 0, 3))
paint(land & (biome == 3), SNOW, np.clip(lvl - 1, 0, 3))
crack = ((xs.astype(int) + ys.astype(int) * 2) % 7 == 0) | ((xs.astype(int) - ys.astype(int) * 2) % 9 == 0)
paint(land & (biome == 4), SALT, crack.astype(int))
for i in range(2):
    img[(lakes | river) & (stripes == i) & land] = SEA[i]

# kustlijn: één pixel donker langs de zee (zoals Hoenn), zand langs de woestijn
pad = np.pad(land, 1)
edge = land & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
img[edge & (biome != 2)] = GREEN[0]
img[edge & (biome == 2)] = SAND[0]

# ---------- plaatsen (vakcoördinaten) ----------
# soort: 'city' = rode pil (stad), 'town' = blauwe stip, 'spot' = rode stip (bijzondere plek)
PLACES = {
    'La Paz (start)':      (16, 20, 'cityh'),
    'Cordillera Real':     (18, 18, 'town'),     # ijsgebied, gym 2
    'Cuzco':               (12, 15, 'cityv'),
    'Machu Picchu':        (10, 13, 'spot'),
    'Rainbow Mountain':    (14, 16, 'spot'),
    'Lima':                (8, 15, 'cityv'),
    'Nazca':               (9, 19, 'spot'),
    'Uyuni':               (17, 24, 'town'),
    'San Pedro':           (11, 28, 'cityh'),
    'Salta':               (17, 28, 'town'),
    'Mendoza':             (13, 31, 'cityh'),
    'Aconcagua (League?)': (11, 30, 'spot'),
    'Bariloche':           (15, 35, 'cityh'),
    'Buenos Aires':        (22, 31, 'cityh'),
    'Iguazú':              (26, 24, 'town'),
    'Rio de Janeiro':      (34, 22, 'cityv'),
    'Amazone-stad':        (22, 11, 'cityh'),
    'Paramaribo':          (30, 4, 'cityh'),
    'Medellín':            (10, 7, 'cityv'),
    'Salento':             (12, 9, 'town'),
    'Cartagena':           (11, 3, 'cityh'),
    'Galápagos':           (3, 13, 'spot'),
    'Paaseiland':          (2, 30, 'spot'),
    'Vuurland':            (18, 39, 'spot'),
}

# ---------- routes (vakken; horizontale/verticale stukken zoals in Hoenn) ----------
route = np.zeros((H, W), bool)
sea_route = np.zeros((H, W), bool)
def seg(a, b, sea=False):
    (x0, y0), (x1, y1) = a, b
    tgt = sea_route if sea else route
    for x in range(min(x0, x1), max(x0, x1) + 1):
        tgt[y0, x] = True
    for y in range(min(y0, y1), max(y0, y1) + 1):
        tgt[y, x1] = True
def path(*pts, sea=False):
    for a, b in zip(pts, pts[1:]):
        seg(a, b, sea)

path((16, 20), (18, 20), (18, 18))                 # La Paz -> Cordillera Real
path((18, 18), (16, 17), (16, 20))                 # lus terug langs de gletsjers
path((16, 20), (14, 20), (14, 16), (12, 16), (12, 15))   # langs het Titicacameer naar Cuzco
path((12, 15), (10, 15), (10, 13))                 # Machu Picchu
path((12, 15), (8, 15))                            # Cuzco -> Lima (afdaling)
path((8, 15), (8, 19), (9, 19))                    # kust naar Nazca
path((9, 19), (11, 19), (11, 21), (14, 21))        # Nazca terug omhoog: lus
path((16, 20), (16, 24), (17, 24))                 # La Paz -> Uyuni
path((17, 24), (12, 24), (12, 27), (11, 27), (11, 28))                 # over de zoutvlakte naar San Pedro
path((11, 28), (17, 28))                           # de busrit: San Pedro -> Salta
path((17, 28), (17, 31), (13, 31))                 # Salta -> Mendoza
path((13, 31), (11, 31), (11, 30))                 # Aconcagua
path((13, 31), (13, 35), (15, 35))                 # Mendoza -> Bariloche
path((17, 31), (22, 31))                           # Salta/Mendoza -> Buenos Aires
path((22, 31), (22, 26), (26, 26), (26, 24))       # Buenos Aires -> Iguazú
path((26, 24), (30, 24), (30, 22), (34, 22))       # Iguazú -> Rio
path((12, 15), (12, 12), (22, 12), (22, 11))       # Cuzco -> Amazone (afdaling oostwaarts)
path((22, 11), (22, 8), (12, 8), (12, 9))          # Amazone -> Salento
path((12, 9), (10, 9), (10, 7))                    # Salento -> Medellín
path((10, 7), (10, 4), (11, 4), (11, 3))           # Medellín -> Cartagena
path((22, 8), (28, 8), (28, 4), (30, 4))           # Amazone -> Paramaribo
# zeeroutes
path((13, 3), (25, 2), (29, 3), sea=True)
path((32, 4), (37, 6), (38, 13), (36, 20), (35, 22), sea=True)   # Paramaribo -> Rio langs de kust
path((7, 15), (5, 15), (5, 13), sea=True)          # Lima -> Galápagos
path((11, 30), (4, 30), sea=True)                  # Paaseiland
path((15, 36), (15, 38), (17, 38), sea=True)       # Bariloche -> Vuurland
sea_route &= ~route

def cell_lvl(x, y):
    sub = lvl[y * 8:(y + 1) * 8, x * 8:(x + 1) * 8]
    return int(np.median(sub))

for y in range(H):
    for x in range(W):
        if route[y, x]:
            b = int(np.median(biome[y * 8:(y + 1) * 8, x * 8:(x + 1) * 8]))
            col = ROUTE_LIGHT if b in (3, 4) else ROUTE[min(cell_lvl(x, y), 4)]
            blk = img[y * 8:(y + 1) * 8, x * 8:(x + 1) * 8]
            blk[:] = col
            if b == 2:
                blk[::2] = hexc('#eebd39')
        elif sea_route[y, x]:
            for r in range(8):
                img[y * 8 + r, x * 8:(x + 1) * 8] = SEAROUTE[(y * 8 + r) % 2]

# ---------- stadsiconen uit de Hoenn-kaart ----------
d = 'graphics/pokenav/region_map/'
til = Image.open(d + 'map.png').convert('RGB')
tm = open(d + 'map.bin', 'rb').read()
def cell_img(cx_, cy_):
    t = tm[cy_ * 64 + cx_]
    return np.array(til.crop(((t % 16) * 8, (t // 16) * 8, (t % 16) * 8 + 8, (t // 16) * 8 + 8)))
ICONCOL = {hexc(c) for c in ('#940000', '#ff3910', '#ffffff', '#cdcdcd', '#626262', '#ffac10', '#f60000',
                             '#0073ac', '#00398b', '#7bb4d5')}
ICONS = {
    'town': [[cell_img(6, 5)]],
    'spot': [[cell_img(2, 11)]],
    'cityh': [[cell_img(9, 8), cell_img(10, 8)]],
    'cityv': [[cell_img(1, 7)], [cell_img(1, 8)]],
}
def stamp(kind, x, y):
    for r, row in enumerate(ICONS[kind]):
        for c, tile in enumerate(row):
            blk = img[(y + r) * 8:(y + r + 1) * 8, (x + c) * 8:(x + c + 1) * 8]
            for py in range(8):
                for px in range(8):
                    if tuple(tile[py, px]) in ICONCOL:
                        blk[py, px] = tile[py, px]
for name, (x, y, kind) in PLACES.items():
    stamp(kind, x, y)

out = Image.fromarray(img)
out.resize((PW * 3, PH * 3), Image.NEAREST).save('docs/concept/regiokaart.png')

# ---------- versie met namen ----------
S = 3
big = out.resize((PW * S, PH * S), Image.NEAREST)
canvas = Image.new('RGB', (PW * S + 300, PH * S), hexc('#203050'))
canvas.paste(big, (0, 0))
dr = ImageDraw.Draw(canvas)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
for name, (x, y, kind) in PLACES.items():
    w = 2 if kind == 'cityh' else 1
    tx, ty = (x + w) * 8 * S + 4, y * 8 * S + 2
    if name == 'San Pedro':
        ty -= 22
    if x > 30:
        tx = x * 8 * S - dr.textlength(name, font=font) - 4
    dr.text((tx, ty), name, font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(20, 30, 50))
lx = PW * S + 16
lines = [('Pokémon Fully Ungrounded', font), ('Regiokaart – schets 1', small), ('', small),
         ('Rode pil: stad', small), ('Blauwe stip: dorp', small), ('Rode stip: bijzondere plek', small),
         ('Oranje: route', small), ('Donkerblauw: zeeroute', small), ('', small),
         ('Groen: hoger = lichter', small), ('Donkergroen: jungle', small), ('Zand: woestijn', small),
         ('Wit/blauw: sneeuw en ijs', small), ('Wit: zoutvlakte', small), ('', small),
         ('Lussen: La Paz–Cordillera,', small), ('Cuzco–Lima–Nazca–La Paz,', small),
         ('Andes–Amazone–noorden,', small), ('zuiden–Iguazú–Rio–kust.', small)]
yy = 16
for text, f in lines:
    dr.text((lx, yy), text, font=f, fill=(255, 255, 255))
    yy += 22
canvas.save('docs/concept/regiokaart_namen.png')
print('ok')
