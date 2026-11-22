# Pitahaya-draak fase 3, r7 (maker). Basis = r6 buik + bekzone (x 0-12, y 26-38) uit r6 zonder tong.
# Jordi 18 nov: "de tong lijkt zo niet echt op een tong, dus haal die maar weg. Daarnaast vind ik rechts de beste, maar ik
# heb nog wel wat kritiek. Er is geen belijning tussen de achterpoot en de staart, lijkt net een blur. Plus het schaduw en
# kleur gebruik is in de hele sprite nog niet optimaal. Kan je daar nog aan werken? Hoofd en de vruchtvlees buik zijn nog
# het beste, maar verder mist die al het contrast dat sprites normaal wel hebben"
# Gebruik: python3 maak_r7.py   (schrijft pitahaya3_r7.png + pitahaya3_r7_afwijkingen.txt)
import sys, numpy as np; from PIL import Image
R6 = '../sprite_r6/'
CH = '.#drpPgGhHwWkqQs'          # 12 = k (nieuw: diepste groen); 13/14 ongebruikt (waren tonggeel)
def lees(p): return np.asarray(Image.open(p)).astype(int)
buik = lees(R6+'pitahaya3_r6_buik.png'); zt = lees(R6+'pitahaya3_r6_zonder_tong.png')
o = buik.copy(); o[26:39, 0:13] = zt[26:39, 0:13]
basis = o.copy()
assert not np.isin(o, [12, 13, 14]).any(), 'nog tongpixels (geel)'
LOG = []
def zet(naam, pixels):
    """pixels: lijst (x, y, oud, nieuw) met assert op het oude teken"""
    for x, y, oud, nieuw in pixels:
        assert CH[o[y, x]] in oud, (naam, x, y, CH[o[y, x]], oud)
        LOG.append((naam, x, y, CH[o[y, x]], nieuw)); o[y, x] = CH.index(nieuw)
def rij(naam, y, x0, oud, nieuw):
    assert len(oud) == len(nieuw), (naam, y)
    zet(naam, [(x0+i, y, a, b) for i, (a, b) in enumerate(zip(oud, nieuw)) if a != b])

# 1. Lijn voet/staart (model: donkere lijn van (42,57) schuin omhoog naar de onderkant van het gat bij (52,53))
zet('1 lijn voet-staart', [(42,57,'H','#'),(43,57,'H','#'),(44,57,'h','#'),(45,56,'g','#'),(46,56,'g','#'),(47,56,'g','#'),
    (48,56,'g','#'),(49,55,'G','#'),(50,55,'h','#'),(51,54,'g','#'),(50,53,'g','#'),(52,53,'g','#')])
# staart direct onder de lijn licht, zodat voet (donker) en staart (licht) uit elkaar liggen
zet('1 staart onder de lijn licht', [(49,56,'h','H'),(50,56,'h','H'),(51,55,'h','H'),(52,55,'h','H'),(45,57,'h','H'),
    (46,57,'h','H'),(47,57,'h','H'),(48,57,'h','H')])
# 1b. Bovenrand en rechtercontour van de dij (model: boog op y~40, contour x 47-48 naar de bestaande ## op rij 44)
zet('1b dijboog + contour', [(41,40,'h','g'),(42,40,'h','g'),(43,40,'h','g'),(44,40,'h','g'),(46,41,'h','k'),
    (47,42,'h','k'),(48,43,'h','k')])

# 2. Dij: hooglicht linksboven onder de boog, schaduwkant rechts van de rib, onderkant in schaduw
rij('2 dij', 41, 41, 'hhh', 'HHH')
rij('2 dij', 42, 40, 'hhhhhgh', 'HHhhhgG')
rij('2 dij', 43, 40, 'hhhhhgh', 'HhhhhgG')
rij('2 dij', 44, 39, 'hhhhhhggh', 'hhhhhhggG')
rij('2 dij', 46, 45, 'h', 'G')
rij('2 dij', 47, 45, 'hgg', 'GgG')
rij('2 dij', 48, 40, 'hhhghhhg', 'hhGgGGGg')
rij('2 dij', 49, 40, 'hhhgghhg', 'GGGggGGg')
rij('2 scheen', 50, 41, 'hhhghhg', 'hGGgGGg')
# slagschaduw van de dij op heup/staartwortel rechts van de contour
zet('2 slagschaduw heup', [(47,41,'h','G'),(48,41,'h','G'),(48,42,'h','G'),(49,42,'h','G'),(49,43,'h','G'),(50,44,'h','G'),
    (50,45,'h','G'),(50,46,'h','G'),(50,47,'h','G')])

# 2c. Romp: schaduwband onderaan de romp (onder de rug, boven arm en dij), flank boven de dij in schaduw
rij('2c romp', 32, 37, 'hhhhh', 'GGGGG')
rij('2c romp', 33, 35, 'hhhhhhh', 'GGGGGGG')
rij('2c romp', 34, 36, 'hh', 'GG')
rij('2c flank boven dij', 38, 41, 'hhhhhhh', 'hhGGGGG')
rij('2c flank boven dij', 39, 41, 'hhhhhhhhh', 'GGGGGGGGG')

# 3. Staart (rechtop deel): rib = terminator; rechts ervan schaduw, onderaan een sikkel tegen de buitenlijn
for y, x0, oud, nieuw in [
    (42, 55, 'h', 'G'), (43, 55, 'h', 'G'),
    (44, 55, 'hghg', 'GgGG'), (45, 55, 'hggh', 'GggG'), (46, 55, 'hhgh', 'GGgG'), (47, 55, 'hhgh', 'GGgG'),
    (48, 56, 'hghh', 'GgGG'), (49, 56, 'hghh', 'GgGG'), (50, 56, 'hghh', 'GgGG'), (51, 58, 'hh', 'GG'),
    (52, 57, 'hhh', 'hGG'), (53, 57, 'hhh', 'hGG'), (54, 57, 'hGG', 'GGg'), (55, 58, 'GG', 'gg'),
    (56, 57, 'GGG', 'Ggg'), (57, 55, 'GGGG', 'GGgg'), (58, 52, 'hhGGGG', 'hGGGgg'),
    (59, 33, 'hhhhhhhhhhhhhhhhhhhhhGG', 'hhhhhhhhhhhhGGGGGGGGGgg'),
    (60, 38, 'hghhhhhhggggggGG', 'GGGGGGGGggggggkk')]:
    rij('3 staart', y, x0, oud, nieuw)

# 4. Verre poot / vorm onder de buik (achter de nabije arm): iets meer schaduw rechts
zet('4 vorm achter arm', [(24,47,'h','G'),(24,48,'h','G'),(23,49,'h','G'),(27,50,'G','g'),(28,50,'G','g')])

# 5. Knots: selout op de bovenrand, hooglicht linksboven, schaduw rechtsonder
zet('5 knots', [(20,51,'p','r'),(21,51,'p','r'),(23,51,'p','r'),(24,51,'p','r'),(25,51,'p','r'),
    (20,52,'p','P'),(21,52,'p','P'),(22,52,'p','P'),(19,53,'p','P'),(20,53,'p','P'),
    (27,53,'p','r'),(28,53,'p','r'),(25,54,'p','r'),(26,54,'p','r')])

# 6. Rugstekels: klein hooglicht linksboven per plaat
zet('6 stekels', [(26,18,'p','P'),(27,18,'p','P'),(28,18,'p','P'),(25,19,'p','P'),(26,19,'p','P'),
    (32,19,'p','P'),(33,19,'p','P'),(32,20,'p','P'),
    (38,22,'p','P'),(39,22,'p','P'),(38,23,'p','P'),
    (45,31,'p','P'),(46,31,'p','P'),(45,32,'p','P')])

# Palet: groen meer spreiding (L oud 75/112/150/196 -> nieuw ~62/115/160/214) + diepste groen k
pal = Image.open(R6+'pitahaya3_r6_buik.png').getpalette()[:48]
NIEUW = {6: (36, 76, 44), 7: (64, 120, 56), 8: (108, 164, 72), 9: (184, 224, 112), 12: (22, 46, 32),
         13: (19, 19, 15), 14: (19, 19, 15)}
for i, c in NIEUW.items(): pal[3*i:3*i+3] = list(c)
OUT = 'pitahaya3_r7.png'
im = Image.fromarray(o.astype('uint8'), 'P'); im.putpalette(pal); im.save(OUT, transparency=0)
# controles
assert ((o > 0) == (basis > 0)).all(), 'silhouet gewijzigd'
assert not np.isin(o, [13, 14]).any()
assert len(np.unique(o)) <= 16
with open('pitahaya3_r7_afwijkingen.txt', 'w') as f:
    f.write('# %s: elke pixel die afwijkt van de basis (r6 buik + bek zonder tong): stap | x | y | oud -> nieuw (tekens %s)\n' % (OUT, CH))
    f.write('# totaal %d px; daarnaast paletwijziging (zie NOTITIES.md)\n' % (o != basis).sum())
    for r in LOG: f.write('%s | %d | %d | %s -> %s\n' % r)
print(OUT, 'px t.o.v. basis:', (o != basis).sum())
