# Pitahaya-draak fase 3, r9 (maker): keurderpunten op r8. Basis = ../sprite_r8/pitahaya3_r8.png, palet ongewijzigd.
# Gebruik: python3 maak_r9.py   (schrijft pitahaya3_r9.png + pitahaya3_r9_afwijkingen.txt)
import sys, numpy as np; from PIL import Image
CH = '.#drpPgGhHwWkqQs'
B = Image.open('../sprite_r8/pitahaya3_r8.png'); o = np.asarray(B).astype(int).copy(); r8 = o.copy(); pal = B.getpalette()
LOG = []
def zet(naam, pixels):
    for x, y, oud, nieuw in pixels:
        assert CH[o[y, x]] in oud, (naam, x, y, CH[o[y, x]], oud)
        if CH[o[y, x]] != nieuw: LOG.append((naam, x, y, CH[o[y, x]], nieuw)); o[y, x] = CH.index(nieuw)
def rij(naam, y, x0, oud, nieuw):
    assert len(oud) == len(nieuw), (naam, y)
    zet(naam, [(x0+i, y, a, b) for i, (a, b) in enumerate(zip(oud, nieuw)) if a != b])

# 1. Schutblad beenzijde: taps, brede voet bovenaan, h linksboven, G rechts, donkere scheiding links tegen het roze
zet('1 schutblad', [(26,51,'G','h'), (26,52,'r','g'), (26,53,'r','d'), (27,53,'h','G'), (28,53,'G','r'), (27,54,'G','g')])

# 2. Banding liggende staart: H kort (x 34-40), h/G/g versprongen laten eindigen, sikkel rechts dikker
rij('2 staart liggend', 57, 33, 'ggggg', 'GGGGG')
rij('2 staart liggend', 58, 33, 'H', 'h')
rij('2 staart liggend', 58, 41, 'HHH', 'hhh')
rij('2 staart liggend', 59, 45, 'GG', 'hh')
rij('2 staart liggend', 59, 52, 'GG', 'gg')
rij('2 staart liggend', 60, 42, 'GGGG', 'gggg')

# 3. Diepte onderbenen (model: de gestreepte dij + scheen in het midden is het nabije been; de vorm x 19-28, y 41-50
#    onder de arm is het verre achterbeen, in het model donkerder). Scheen: doorlopende lichte voorkant langs de
#    linkercontour, één rib (x 46), schaduw rechts. Verre been een stap donkerder (h->G, G->g).
for y, x0, oud, nieuw in [
    (47, 43, 'g', 'h'),
    (48, 42, 'GgGGGgG', 'hGGGGgG'),
    (49, 40, 'GGGggGGgG', 'GhhGGGgGG'),
    (50, 41, 'hGGgGGgG', 'hhGGGgGG'),
    (51, 42, 'GhgGGgG', 'hhGGgGG'),
    (52, 43, 'GGgGgG', 'hhGgGG'),
    (53, 44, 'GgGggG', 'hhgGGG'),
    (54, 44, 'hgGGgGG', 'hhgGGGG'),
    (55, 43, 'hhgGGg', 'hhGgGG')]:
    rij('3 scheen', y, x0, oud, nieuw)
#    Eigen licht blijft: de meest linkse h per rij (lichte kant, net als de verre arm) blijft h.
for y in range(43, 51):
    eerste_h = min([x for x in range(19, 29) if CH[o[y, x]] == 'h'], default=None)
    for x in range(19, 29):
        c = CH[o[y, x]]
        if c == 'h' and x != eerste_h: zet('3 verre achterbeen', [(x, y, 'h', 'G')])
        elif c == 'G' and not (y in (44, 45) and x >= 26): zet('3 verre achterbeen', [(x, y, 'G', 'g')])

# 4. Streepruis rechterflank staart: één rib (x 56) in g, links G, rechts G en een dichte sikkel van 2 px g tegen de lijn
for y, x0, oud, nieuw in [
    (44, 55, 'GgGG', 'GgGg'), (45, 55, 'GggGg', 'GgGgg'), (46, 55, 'GGgGg', 'GgGgg'), (47, 55, 'GGgGg', 'GgGgg'),
    (48, 55, 'hGgGGG', 'hgGGgg'), (49, 55, 'hGgGGG', 'hgGGgg'), (50, 55, 'hGgGGG', 'hgGGgg'),
    (51, 55, 'hggGGG', 'hgGGgg'), (52, 55, 'hghGGG', 'hgGGgg'), (53, 55, 'hghGGG', 'hgGGgg')]:
    rij('4 staartflank', y, x0, oud, nieuw)

# 5. Nabije hand: losse h tussen de vingerlijnen -> G (vingerlijnen alleen in g)
zet('5 hand', [(30,47,'h','G'), (32,47,'h','G'), (34,46,'h','G')])

im = Image.fromarray(o.astype('uint8'), 'P'); im.putpalette(pal); im.save('pitahaya3_r9.png', transparency=0)
zt = np.asarray(Image.open('../sprite_r6/pitahaya3_r6_zonder_tong.png')).astype(int)
bk = np.asarray(Image.open('../sprite_r6/pitahaya3_r6_buik.png')).astype(int)
sys.path.insert(0, '../sprite_r6'); from buik import RIJEN
assert ((o > 0) == (r8 > 0)).all(), 'silhouet'
assert (o[12:30, 0:21] == r8[12:30, 0:21]).all() and (o[26:39, 0:13] == zt[26:39, 0:13]).all(), 'kop/bek'
assert all((o[y, a:b+1] == bk[y, a:b+1]).all() for y, (a, b) in RIJEN.items()), 'buik'
n = (o != r8).sum()
with open('pitahaya3_r9_afwijkingen.txt', 'w') as f:
    f.write('# pitahaya3_r9.png t.o.v. ../sprite_r8/pitahaya3_r8.png: stap | x | y | r8 -> r9 (tekens %s)\n# totaal %d px\n' % (CH, n))
    for r in LOG: f.write('%s | %d | %d | %s -> %s\n' % r)
print('r9 t.o.v. r8:', n)
