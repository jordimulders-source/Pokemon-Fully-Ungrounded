# r13: afwerkingsronde kleur, schaduw, lijnen. Basis ../r12/sprite.png. Vorm/silhouet/lijnposities bevroren:
# alleen tinten van bestaande vlakken en het palet veranderen. Draaien vanuit deze map: python3 bouw_r13.py
import numpy as np
from PIL import Image
im0 = Image.open('../r12/sprite.png'); a = np.array(im0).astype(int); r12 = a.copy()
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c == '-': continue
        a[y, x + i] = 0 if c == '.' else H.index(c)

# ================= PALET =================
# lijf/koepel (wit metaal, naar Glalie 255/231/206/166/125 en Magneton): F hooglicht, 2 basis, 3 schaduw, 4 sikkel, 5 diepste/lichte lijn
PAL = {
    1: (24, 18, 34),      # zwart (schaduwkant)
    2: (232, 231, 238),   # lijf basis (was 242,240,238)
    3: (208, 205, 220),   # lijf schaduw (was 222,217,230)
    4: (172, 166, 190),   # lijf sikkel (was 188,177,208: te lavender)
    5: (130, 122, 152),   # lijf diepst + lichte lijn (was 146,126,170)
    6: (196, 146, 204), 7: (138, 90, 156), 8: (92, 58, 116),      # gewrichten/antennes/ringen
    9: (48, 32, 80), 10: (76, 66, 130), 11: (100, 92, 160), 12: (160, 148, 214),  # panelen
    13: (134, 194, 192), 14: (86, 170, 166),                         # iris
    15: (255, 255, 255),  # NIEUW: hooglicht lijf/koepel (vrij slot)
}
pal = []
for i in range(16): pal += list(PAL.get(i, (255, 0, 255)))

# ================= LIJF + KOEPEL (alleen tinten; licht linksboven) =================
# hooglicht F als ovaal op de bolling linksboven (1-2 px basis tussen hooglicht en contour), basis 2,
# schaduw 3 als band die de ronding volgt, sikkel 4 rechts, diepste 5 tegen de zwarte rand rechts.
put(20, 19, '22FFF222')
put(19, 20, '22FFFFF222')
put(18, 21, '22FFFFFF22223333444')
put(17, 22, '22FFFFFFF2222333444' + '5')
put(17, 23, '22FFFFFF22223333' + '444' + '55')
put(16, 24, '2222FFFF22223333' + '4444' + '55')
put(16, 25, '22222FF22223333' + '44444' + '55')
put(24, 26, '222333344445' + '5')
put(26, 27, '2333344445' + '5')
put(27, 28, '233344445')
# lijfzijde rechts van de koepelrand: volgt de bol (was een losse witte streep)
put(28, 29, '3334444' + '5')
put(29, 30, '3334444' + '5')
put(29, 31, '3334444' + '5')
# koepel: binnenste witte ring krijgt het hooglicht linksboven
put(17, 27, 'FFFF2')
put(15, 28, '2FFFF222')
# lens: glanspunt puur wit
put(18, 34, 'F')
# onderkant koepel/lijf: lichte rand linksonder (teruggekaatst licht, zoals Glalie), sikkel rechtsonder
put(16, 43, '33')
put(17, 44, '333')
put(19, 45, '33')
put(21, 46, '444')

# ================= PANELEN =================
# Licht linksboven: fill-tint volgt een diagonaal veld s (lichter linksboven, donkerder rechtsonder) i.p.v. twee vlakke helften;
# rasterlijnen lopen mee (C in het licht, B in het donker, A in de donkerste hoek); glansband (r12, uit het model) blijft.
PAN = (9, 10, 11, 12)
NB = ((-1, 0), (0, -1), (1, 0), (0, 1))
def buren(y, x): return [(y + dy, x + dx, dy, dx) for dy, dx in NB if 0 <= y + dy < 64 and 0 <= x + dx < 64]
def rand9(y, x):  # navy buitenlijn links/boven (grenst links of boven aan iets dat geen paneel is)
    return any(r12[q, p] not in PAN and (dy < 0 or dx < 0) for q, p, dy, dx in buren(y, x))
def frame(y, x):  # lichte framelijn: ligt tegen de buitenlijn (1, randnavy of transparant)
    return any(r12[q, p] in (0, 1) or (r12[q, p] == 9 and rand9(q, p)) for q, p, dy, dx in buren(y, x))
def paneel(gebied, fill, lijntint):
    for y in range(64):
        for x in range(64):
            v = r12[y, x]
            if not gebied(y, x) or v not in PAN: continue
            if v == 9 and rand9(y, x): continue
            lijn = v == 12 or (v == 11 and y >= 38)
            if lijn:
                if frame(y, x): continue
                t = lijntint(y, x, v)
            else:
                t = fill(y, x, v)
            if t: a[y, x] = t
s_groot = lambda y, x: (y - 14) + 0.55 * (x - 44)
def fill_groot(y, x, v):
    if y <= 33: return 11 if s_groot(y, x) < 11 else (10 if s_groot(y, x) < 21 else 9)   # bovenste twee rijen cellen
    return None                                                                              # glansrij en onderste rijen: r12
def lijn_groot(y, x, v):
    if v == 11 and s_groot(y, x) > 28: return 10      # donkerste hoek rechtsonder: lijn een tint dieper
    return None
paneel(lambda y, x: x >= 28 and y >= 13, fill_groot, lijn_groot)
# klein paneel (achter): een sleutel donkerder dan het grote paneel; framelijn B blijft (leesbaar op donker),
# binnenlijnen in de onderste cellen B -> A (lopen mee met het licht: boven B, onder A)
def lijn_klein(y, x, v): return 10 if v == 11 and y >= 26 else None
def fill_klein(y, x, v): return None
def paneel_klein():
    for y in range(64):
        for x in range(21):
            v = r12[y, x]
            if v == 11 and y >= 26 and not frame(y, x): a[y, x] = 10
paneel_klein()
a[38, 3] = 11   # linker framelijn (dubbele navy buitenlijn ernaast, valt buiten frame())

# ================= LIJNEN =================
# lijfcontour linksboven (lichtkant, tegen het kleine paneel): eigen donkerste tint 5 i.p.v. zwart, zoals Magneton
# (bol-omlijning E/D ook waar de bol over de zwarte magneet ligt). Zwart blijft rechts/onder (schaduwkant) en de boog linksonder.
for x, y in ((20, 18), (19, 19), (18, 20), (17, 21), (16, 22), (16, 23), (15, 24), (15, 25), (14, 26)):
    a[y, x] = 5
# ================= BOLLETJES =================
# overal dezelfde opbouw: hooglicht 3 linksboven, 6, 7, schaduw 8 rechtsonder, rand 8 boven/links, zwart rechts/onder
put(35, 8, '36'); put(35, 9, '67')            # antennebol links (was 6 7 / 7 8)
put(48, 10, '36'); put(48, 11, '67')          # antennebol rechts (was 3 6 / 6 7: zelfde, ongewijzigd)
put(32, 33, '6366'); put(32, 34, '666'); put(32, 35, '677'); put(32, 36, '777'); put(32, 37, '88')   # gewricht bij de koepel: hooglicht linksboven i.p.v. midden

# ================= KLEINE REPARATIES NA DE CONTROLE =================
a[28, 27] = 3                    # los 2-pixel onder de koepelrand
a[25, 44] = a[25, 45] = 11       # celhoek linksonder bovenste rij: B zoals de cel erboven (geen los A-reepje)
a[26, 12] = 11                   # klein paneel: lijnpixel aan de framehoek blijft B (geen B/A om en om op de hoek)
a[17, 21] = 8                    # hoek lijf/rand linksboven: 5-lijn gaat over in de 8-rand, geen los zwart ertussen

# ======== OPSLAAN
def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette(pal + [0] * (768 - len(pal)))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); rgba = im.convert('RGBA'); m = np.array(rgba); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
sla(a, 'sprite.png'); np.save('r13.npy', a)
d = a != r12
print('afwijkend t.o.v. r12:', d.sum(), ' kleuren', len(np.unique(a)), ' silhouet-diff', ((a == 0) != (r12 == 0)).sum())
for nm, (x0, x1, y0, y1) in {'lijf boven': (14, 40, 16, 32), 'koepel': (8, 30, 26, 48), 'groot paneel': (36, 64, 8, 56), 'klein paneel': (0, 21, 12, 43)}.items():
    print('  %-13s %d' % (nm, d[y0:y1, x0:x1].sum()))
