"""Capykart r7 -> r8: schaduwronde (Dragonfly Cave). Alleen tinttoewijzing per pixel + palet.
Silhouet, oog, tanden, morrillo, neusgaten/mond, kinlijn: niet aangeraakt (zie controle in log)."""
import os, sys
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, '../../eindkeuring/capykart_r7.png')
im = Image.open(SRC); W, H = im.size
g = [[im.getpixel((x, y)) for x in range(W)] for y in range(H)]
orig = [r[:] for r in g]
WIJZ = {}  # (x,y) -> (zone, reden); laatste zone wint
ZONE = ['']; REDEN = ['']
def zone(z, r): ZONE[0] = z; REDEN[0] = r
def s(x, y, v):
    v = int(v, 16) if isinstance(v, str) else v
    if g[y][x] == 0: raise SystemExit(f'transparant aangeraakt {x},{y}')
    if g[y][x] != v:
        g[y][x] = v
        WIJZ[(x, y)] = (ZONE[0], REDEN[0])
def row(y, x0, txt):
    for i, c in enumerate(txt):
        if c != ' ': s(x0 + i, y, c)
def rep(xs, ys, frm, to):
    for y in ys:
        for x in xs:
            if g[y][x] in frm: s(x, y, to)

# ---------------- PALET ----------------
pal = im.getpalette()[:48]
def setc(i, rgb): pal[i*3:i*3+3] = list(rgb)
setc(5, (244, 178, 116))   # hout licht = vacht-hooglicht = gele zijkant = rode bevel (iets minder verzadigd dan r7)

# ---------------- DRIEHOEK (groen) ----------------
zone('groene driehoek', "twee harde vlakken (licht links, schaduw rechts); rechterschuinte = schaduwkant -> zwart, zodat het schaduwvlak een rand heeft")
row(2, 52, '1')
row(3, 53, '1')
row(4, 54, '1')
row(5, 55, '1')
row(6, 56, '1')
row(7, 57, '1')

# ---------------- GEEL BLOK ----------------
zone('geel blok', "kubus: voorvlak geel met witte bovenbevel (rand vangt licht, zoals Porygon), zijvlak in de schaduw (6, warm hout-oker) met lichte bovenbevel (5)")
row(9, 45, '99')
row(10, 47, '999')
for y in range(12, 16):
    for x in range(51, 55): s(x, y, 6)
row(16, 51, '66')

# ---------------- ROOD BLOK ----------------
zone('rood blok', "kubus: voorvlak rood met lichte bovenbevel (5, warme hue shift), zijvlak donkerrood met rode bovenbevel, onderbevel donker")
row(17, 46, '55'); row(17, 53, 'CC')
row(18, 45, '5  55CCC')
row(24, 46, 'DDDD')

# ---------------- BLAUW BLOK ----------------
zone('blauw blok', "kubus: voorvlak blauw met witte bovenbevel, zijvlak blauwgrijs met blauwe bovenbevel; bovenrand zijvlak in de schaduw onder het rode blok -> zwart")
row(25, 44, '99'); row(25, 52, '11111')
row(26, 46, '9999AAAAAAA')

# ---------------- HOEPELS ----------------
zone('rechterhoepel', "metaal: witte glans bovenaan de boog en op het bovenste stuk van de band, onderaan donker")
row(30, 44, '99')
row(35, 49, '9'); row(36, 49, '9')
rep([49], range(44, 48), [7], 8)
zone('linkerhoepel', "metaal: witte glans op de kruin van de boog (lichtkant), dalend deel rechts donker")
row(36, 15, '99999')

# ---------------- KOP ----------------
zone('kop hooglicht', "bolling voorhoofd/snuitbovenkant in het lichtste (5), zoals Capybarrel af; licht linksboven")
row(14, 24, '55555')
row(15, 25, '5555')
row(16, 24, '555')
row(17, 21, '5555')
row(18, 19, '555')
zone('kop sikkel', "sikkelschaduw achter/onder: rechterrand van de kop een tint donkerder, dikker naar onder; wang rond afgesloten met 3")
for y in range(19, 23): 
    xs = [x for x in range(30, 41) if g[y][x] == 3 and g[y][x+1] == 1]
    for x in xs: s(x, y, 4)
for y in range(23, 29):
    xs = [x for x in range(30, 41) if g[y][x] == 3 and g[y][x+1] == 1]
    for x in xs: s(x, y, 4); s(x-1, y, 4) if g[y][x-1] == 3 else None
row(27, 31, '33')
row(28, 28, '3333')
zone('kaak/nek', "onderkant kaak en slagschaduw op de nek in 4; nek links (lichtkant) een tint lichter")
rep(range(30, 38), [29], [3], 4)
rep(range(31, 38), [30], [3], 4)
row(32, 30, '22'); row(33, 31, '22'); row(34, 31, '22')
rep(range(20, 23), [29], [3], 4)
zone('schouder in kart', "groot effen 4-vlak: bovenlinks (dicht bij de lichte nek) een tint lichter")
row(36, 34, '3333'); row(37, 34, '33')

# ---------------- KART: NEUS ----------------
zone('kart neus bovenvlak', "nerf op het lichte vlak een stap van het vlak (2 i.p.v. 4/6)")
row(41, 21, '22')
row(40, 9, '22222'); row(42, 13, '2222')
row(39, 21, '6666'); row(40, 20, '666')
zone('kart neus voorvlak', "verticale nerf in 3 (een stap van 6) en korter; hooglicht op de ronde linkerhoek")
row(45, 2, '55'); row(46, 2, '55')
for (x, y0, y1) in [(4,45,46),(3,47,49),(7,46,47),(8,46,46),(6,48,51),(11,47,47),(12,47,51),(16,45,46),(15,47,50),(16,48,48)]:
    for y in range(y0, y1+1):
        if g[y][x] == 4: s(x, y, 3)
# lange lijnen onderaan in de sikkel laten opgaan
zone('kart neus sikkel', "sikkelschaduw onderlangs, dunner links en dikker rechts (naar het wiel)")
for x in range(3, 22):
    yb = max(y for y in range(40, 60) if g[y][x] not in (0, 1) and (y+1 < H and g[y+1][x] == 1))
    n = 2 if x < 9 else (3 if x < 15 else 4)
    for y in range(yb-n+1, yb+1):
        if g[y][x] in (3, 5, 6): s(x, y, 4)
zone('kart neus zijvlak', "horizontale nerf in 3; lichte hoekstrook in de sikkel een tint terug")
rep(range(19, 23), [49], [4], 3)
rep([18], range(53, 56), [5, 4], 6)
# ---------------- KART: VOORWIEL ----------------
zone('voorwiel', "bolling: rand linksboven licht (5 bestaat al), sikkel rechtsonder in 4, naaf als een knop (ring 4, kern 5/6)")
row(54, 30, '55'); row(55, 30, '55'); row(51, 26, '6'); row(52, 26, '6')
for y in range(52, 57):
    for x in (33, 34, 35):
        if g[y][x] == 6: s(x, y, 4)
rep(range(28, 35), range(57, 61), [6], 4); row(56, 32, '4')
row(57, 26, '66')
# ---------------- KART: MIDDEN ----------------
zone('kart midden', "nerf in 3 en korter; slagschaduw van het voorwiel rechts ervan; onderrand sikkel")
rep(range(37, 41), [49], [4], 3)
rep(range(40, 43), [48], [4], 3)
rep(range(41, 45), [42], [4], 3); row(42, 36, '66'); rep(range(43, 45), [41], [4], 3)
row(50, 36, '4'); row(51, 36, '44'); 
rep(range(37, 47), [50, 51, 52], [6, 3], 4); rep([37], [53], [6], 4)
# ---------------- KART: ACHTER ----------------
zone('kart achterbak', "lange lijnen in 3 en korter; rechterkant en boven het wiel sikkel in 4")
rep(range(55, 61), [36], [4], 3)
row(35, 56, '3')
row(41, 53, '6'); rep(range(54, 59), [41], [4], 3); row(41, 59, '66')
row(42, 58, '33')
rep([61], range(36, 48), [6], 4)
rep([60], range(39, 44), [6], 4); row(41, 59, '4'); row(48, 61, '4')
zone('achterwiel', "naaf als een vorm met glans linksboven; spaak in 3; sikkel rechtsonder in 4")
row(49, 55, '55')
rep([54], [54, 55], [4], 3)
rep([58], range(50, 56), [6], 4); rep([59], range(49, 55), [6], 4)
rep(range(55, 58), [55, 56], [6], 4)

out = Image.new('P', (W, H)); out.putpalette(pal + [0]*(768-48))
out.putdata([v for r in g for v in r])
out.info['transparency'] = 0
out.save(os.path.join(D, 'capykart.png'), transparency=0)
out.convert('RGBA').resize((W*8, H*8), Image.NEAREST).save(os.path.join(D, 'capykart_8x.png'))
# alpha-diff
ad = sum(1 for y in range(H) for x in range(W) if (orig[y][x] == 0) != (g[y][x] == 0))
ch = sum(1 for y in range(H) for x in range(W) if orig[y][x] != g[y][x])
print('alpha-diff', ad, 'gewijzigd', ch)
import json
json.dump({f'{x},{y}': [orig[y][x], g[y][x], z, r] for (x, y), (z, r) in WIJZ.items() if orig[y][x] != g[y][x]},
          open(os.path.join(D, 'wijzigingen.json'), 'w'), ensure_ascii=False, indent=0)
