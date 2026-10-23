"""kop17.py <map>: schrijft de delen 'staart' en 'kop' van ronde 17 (kop = ronde 16 + snuitpatch, staart nieuw) in bron/delen_abs.txt uit segmenten
(y, x, pixels) met absolute x, zodat er niet in lange rijen geteld hoeft te worden. Overige delen blijven."""
import sys, os
B = os.path.join(sys.argv[1], 'bron')

# --- kop: lijst van (y, x, pixels); latere segmenten overschrijven eerdere ---
_d = os.path.abspath(sys.argv[1])
while not os.path.isdir(os.path.join(_d, 'ronde15')):
    _d = os.path.dirname(_d)
OUD = [r.rstrip('\n') for r in open(os.path.join(_d, 'ronde15', 'bron', 'raster_f1.txt'))]

# schedel: per rij (y, links, rechts); links omlijning 1 (lichte kant), rechts 0 (schaduwkant).
# boven: runs 8,3,2,1 ; achter: x36,37,38,38,39,39,39,39,38,38,37 ; kin/keel apart.
RIJEN = [(22,24,26),(23,21,28),(24,18,34),(25,16,36),(26,15,37),(27,14,38),(28,14,38),(29,13,39),(30,11,39),
         (31,10,39),(32,9,39),(33,9,38),(34,9,38),(35,10,37),(36,11,37),(37,15,37),(38,16,36)]
KOP = []
for y, l, r in RIJEN:
    rij = ''
    for x in range(l, r + 1):
        if x == l or y == 22 or (y == 23 and x in (21, 22, 23, 27, 28)) or (y == 24 and x < 21): c = '1'
        elif x == r: c = '0'
        elif x - l + (y - 24) < 7 and y < 30: c = '4'
        elif x >= r - 2 or y >= 38: c = '2'
        else: c = '3'
        rij += c
    KOP.append((y, l, rij))
KOP += [
 # verre oor (achter de schedel; eerst, zodat de schedel eroverheen ligt -> daarom vooraan ingevoegd)
]
OREN = [(20,17,'11'), (21,16,'1351'), (22,15,'135521'), (23,15,'125221'), (24,15,'122')]
KOP = OREN + KOP + [
 # nabije oor (voor de schedel)
 (19,31,'111'), (20,30,'14330'), (21,29,'1476320'), (22,29,'1366520'), (23,29,'1365220'), (24,29,'3322220'),
 (25,30,'2222'),
]
# snuit, neus, grijns en onderkaak = ronde 15 (letterlijk overgenomen)
for y, x0, x1 in [(30,11,14),(31,10,14),(32,9,14),(33,9,15),(34,9,15),(35,10,27),(36,11,26),(37,15,24),(38,16,21)]:
    KOP.append((y, x0, OUD[y][x0:x1 + 1]))
KOP += [
 # masker: verre lob, neusbrug (kopkleur), nabije lob met vleugel naar het oor, onderrand als golf
 (28,15,'11111'), (29,14,'111111'), (30,15,'11111'), (31,15,'11111'), (32,15,'1111111111'),
 (28,20,'443'), (29,20,'433'),
 (26,34,'1'), (27,31,'111'), (28,24,'111111111'), (29,23,'1'), (29,29,'1111'),
 (30,19,'11111'), (30,29,'1111'), (31,19,'11111'), (31,29,'1111'), (32,24,'1'), (32,28,'11111'),
 (33,16,'111111111111111111'), (34,16,'111111'), (34,22,'66666655'), (34,30,'1111'), (35,31,'11'),
 # wenkbrauwboogjes
 (26,24,'676'), (27,23,'6'), (27,27,'5'), (26,17,'66'), (27,16,'6'), (27,19,'5'),
 # nabij oog: bovenlid zwart met flick, iris donker boven/licht onder, pupil tegen het lid, glans linksboven
 (28,29,'0'), (29,24,'00000'), (30,24,'ddb0d'), (31,24,'cc00c'), (32,25,'ccc'),
 # ver oog: 3 breed, 1 rij lager
 (30,16,'000'), (31,16,'b0d'), (32,17,'cc'),
 # kin en keel
 (36,27,'3333333'), (37,25,'333333322'), (38,22,'2222222222222'), (39,19,'000000222222220'), (40,25,'000000'), (39,31,'00'),
]
# --- ronde 17, punt 3 (Jordi): neus tussen de ogen. In ronde 16 stak de snuit links voorbij het verre oog uit
# (neuspunt x9, verre oog x16-18, nabije oog x24-28): de kop las als profiel. Hier: neus (zelfde 3x3 '0a0/000/050')
# onder de neusbrug op x20-22, y34-36 (onder de maskerband, met room eromheen); grijns met hoektand mee naar rechts; wang aan de verre kant rond gesloten;
# onderkaak onder de nieuwe mond. Patch per rij: WIS = (y, x0, x1) leeg maken, ZET = (y, x, pixels).
import os as _os
VARIANT = _os.environ.get('OLI_VARIANT', '')
WIS = [(30, 9, 11), (31, 9, 10), (32, 9, 10), (33, 9, 10), (34, 9, 10), (35, 9, 11), (36, 9, 12), (37, 9, 13)]
ZET = [
 (30, 12, '144'),
 (31, 11, '1443'),
 (32, 11, '1433'),
 (33, 11, '13333'), (33, 20, '666'),
 (34, 11, '13333'), (34, 19, '60a066666'),
 (35, 12, '1333'), (35, 16, '666600066666551'),
 (36, 13, '033'), (36, 16, '666605066666666'), (36, 31, '1'),
 (37, 14, '00555555511666661'),
 (38, 19, '55555511111'),
 (39, 25, '555b5'),
]
if VARIANT == 'ogen':
    # variant_ogen: verre oog 2 px naar links (x14-16), verre maskerlob loopt mee tot de wangrand; neus en grijns
    # als de hoofdversie. De neus valt zo precies midden tussen de ogen en de verre wang wordt smaller (meer 3/4).
    ZET += [
     (30, 12, '11000111'),
     (31, 11, '141b0d111'),
     (32, 11, '14111cc111'),
     (33, 11, '133111111'),
    ]
_px = {}
for y, x, p in KOP:
    for i, c in enumerate(p):
        if c != '.':
            _px[(x + i, y)] = c
for y, a, b in WIS:
    for x in range(a, b + 1):
        _px.pop((x, y), None)
for y, x, p in ZET:
    for i, c in enumerate(p):
        _px[(x + i, y)] = c
KOP = []
for y in sorted({k[1] for k in _px}):
    run = []
    for x in sorted(x for x, yy in _px if yy == y) + [None]:
        if run and (x is None or x != run[-1] + 1):
            KOP.append((y, run[0], ''.join(_px[(u, y)] for u in run))); run = []
        if x is not None:
            run.append(x)

# --- staart ronde 17 (punt 1): hangende J. Vanaf de romp laag naar achteren (top y34, niet boven de rug uit),
# buigt omlaag langs x57-62 en krult onderaan terug omhoog met een ronde punt in vachtkleur (x50-54, y46-49).
# Lucht: zak tussen romp en staart (x54-56, y40-45) en het gat van de haak (x55-56, y47-48). Ringen subtiel
# (schaduwtint, loodrecht op de staart: y36-37 x55 en y42 x59-61). Met de hand per rij, x48..63; '.' = niets.
STAART_RIJEN = {
 #    x: 4455555555556666
 #       8901234567890123
 34:    '.....1111.......',
 35:    '..111444411.....',
 36:    '..1433323441....',
 37:    '.143333233341...',
 38:    '.1333322223320..',
 39:    '.2222200023320..',
 40:    '.........143320.',
 41:    '.........143320.',
 42:    '.........142220.',
 43:    '..........13320.',
 44:    '..........1420..',
 45:    '..........1320..',
 46:    '....11....1320..',
 47:    '...1441..13220..',
 48:    '..14430..1320...',
 49:    '..1333211220....',
 50:    '...00222200.....',
 51:    '.....0000.......',
}
STAART = []
for y, rij in STAART_RIJEN.items():
    assert len(rij) == 16, (y, len(rij))
    x = 0
    while x < 16:
        if rij[x] == '.':
            x += 1; continue
        x0 = x
        while x < 16 and rij[x] != '.':
            x += 1
        STAART.append((y, 48 + x0, rij[x0:x]))

def schrijf(naam, kop, segs, regels):
    uit = ['## ' + kop]
    uit += ['# ' + r for r in regels]
    for y, x, p in segs:
        uit.append('%d %d %s' % (y, x, p))
    return uit

src = open(os.path.join(B, 'delen_abs.txt'), encoding='utf-8').read().split('\n')
blok, naam = {}, None
volg = []
for r in src:
    if r.startswith('## '):
        naam = r[3:].split()[0]; volg.append(naam); blok[naam] = [r]
    elif naam:
        blok[naam].append(r)
    else:
        blok.setdefault('_kop', []).append(r)
blok['kop'] = schrijf('kop', 'kop -1', KOP, ['ronde 17: gegenereerd door kop17.py (niet hier bewerken)'])
if STAART:
    blok['staart'] = schrijf('staart', 'staart 1', STAART, ['ronde 17: gegenereerd door kop17.py (niet hier bewerken)'])
uit = blok.get('_kop', [])
for n in volg:
    uit += blok[n]
open(os.path.join(B, 'delen_abs.txt'), 'w', encoding='utf-8').write('\n'.join(l for l in uit) .rstrip('\n') + '\n')
