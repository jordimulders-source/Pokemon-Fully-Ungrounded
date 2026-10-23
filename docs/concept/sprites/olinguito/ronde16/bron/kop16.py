"""kop16.py <map>: schrijft de delen 'staart' en 'kop' van ronde 16 in bron/delen_abs.txt uit segmenten
(y, x, pixels) met absolute x, zodat er niet in lange rijen geteld hoeft te worden. Overige delen blijven."""
import sys, os
B = os.path.join(sys.argv[1], 'bron')

# --- kop: lijst van (y, x, pixels); latere segmenten overschrijven eerdere ---
OUD = [r.rstrip('\n') for r in open(os.path.join(sys.argv[1], '..', 'ronde15', 'bron', 'raster_f1.txt'))]

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
# --- staart: taps (romp-voet 9 breed incl. omlijning -> 5 bij y21), leunt naar rechts, haak naar links ---
# links (lichte kant) omlijning 1, rechts 0; links verspringt elke 2 rijen (taps), rechts elke 4 (lean).
STAART = []
# (y, links, rechts) met de hand: rechts runs 4,4,4,4,3 (helt naar rechts), links runs 1,2,2,1,2,2,2,2,3 (taps)
SCHACHT = {22:(57,61),23:(56,61),24:(56,60),25:(55,60),26:(55,60),27:(54,60),28:(53,59),29:(53,59),30:(52,59),
           31:(52,59),32:(51,58),33:(51,58),34:(50,58),35:(50,58),36:(49,57),37:(49,57),38:(49,57),39:(50,56)}
for y in range(22, 40):
    L, R = SCHACHT[y]
    rij = ''
    for x in range(L, R + 1):
        if y == 39: ch = '0'
        elif x == L: ch = '1'
        elif x == R: ch = '0'
        elif x == L + 1: ch = '4'
        elif x >= R - 1 - (1 if R - L > 6 else 0): ch = '2'
        else: ch = '3'
        rij += ch
    STAART.append((y, L, rij))
STAART += [
 # haak: buitenbocht (x61 -> 56), kap op y15, punt omlaag naar links met donkere weerhaak,
 # lucht in de bocht (x53-55, y19-21)
 # ringen (subtiel, schuin: loodrecht op de helling van de staart)
 (25,56,'22'), (26,57,'22'), (30,53,'222'), (31,55,'22'),
 (15,53,'1111'),
 (16,51,'1144430'),
 (17,50,'144333320'),
 (18,49,'14320003320'),
 (19,49,'1220'), (19,55,'144320'),
 (20,50,'110'), (20,56,'143320'),
 (21,51,'0'), (21,56,'143320'),
]

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
blok['kop'] = schrijf('kop', 'kop -1', KOP, ['ronde 16: gegenereerd door kop16.py (niet hier bewerken)'])
if STAART:
    blok['staart'] = schrijf('staart', 'staart -1', STAART, ['ronde 16: gegenereerd door kop16.py (niet hier bewerken)'])
uit = blok.get('_kop', [])
for n in volg:
    uit += blok[n]
open(os.path.join(B, 'delen_abs.txt'), 'w', encoding='utf-8').write('\n'.join(l for l in uit) .rstrip('\n') + '\n')
