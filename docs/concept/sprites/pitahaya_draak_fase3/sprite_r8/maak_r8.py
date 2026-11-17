# Pitahaya-draak fase 3, r8 (maker): coördinatorpunten op r7 (nek/schouder, verre arm, nabije arm/romp, roze rug).
# Basis = ../sprite_r7/pitahaya3_r7.png (palet ongewijzigd). Gebruik: python3 maak_r8.py
import numpy as np; from PIL import Image
CH = '.#drpPgGhHwWkqQs'
B = Image.open('../sprite_r7/pitahaya3_r7.png'); o = np.asarray(B).astype(int).copy(); r7 = o.copy(); pal = B.getpalette()
LOG = []
def zet(naam, pixels):
    for x, y, oud, nieuw in pixels:
        assert CH[o[y, x]] in oud, (naam, x, y, CH[o[y, x]], oud)
        LOG.append((naam, x, y, CH[o[y, x]], nieuw)); o[y, x] = CH.index(nieuw)
def rij(naam, y, x0, oud, nieuw):
    assert len(oud) == len(nieuw), (naam, y)
    zet(naam, [(x0+i, y, a, b) for i, (a, b) in enumerate(zip(oud, nieuw)) if a != b])

# 1. Nek/schouder. Hooglicht als smalle band onder de rugplaten; slagschaduw van de kop op de nek; schaduw langs de
#    onderkant van de nek (richting buik); spierlijn nek -> schouder (model) en een klein hooglicht op de schouderbolling.
rij('1 band onder platen', 22, 21, 'HHHHH', 'HHhhh')
rij('1 band onder platen', 23, 21, 'HHhhhHH', 'Hhhhhhh')
rij('1 band onder platen', 25, 28, 'HHHHH', 'hhHHH')
rij('1 band onder platen', 26, 32, 'hhh', 'HHh')
rij('1 band onder platen', 27, 33, 'hhh', 'hHH')
rij('1 slagschaduw kop', 24, 20, 'hhh', 'GGh')
rij('1 slagschaduw kop', 25, 21, 'hh', 'GG')
rij('1 slagschaduw kop', 26, 21, 'HHh', 'GGh')
rij('1 slagschaduw kop', 27, 20, 'HHH', 'GGh')
rij('1 slagschaduw kop', 28, 19, 'h', 'G')
rij('1 slagschaduw kop', 29, 20, 'hh', 'GG')
rij('1 onderkant nek', 30, 25, 'hh', 'GG')
rij('1 onderkant nek', 31, 28, 'hh', 'GG')
rij('1 onderkant nek', 32, 29, 'hh', 'GG')
rij('1 onderkant nek', 33, 29, 'hh', 'GG')
rij('1 spierlijn', 27, 24, 'hh', 'GG')
rij('1 spierlijn', 28, 26, 'hh', 'GG')
rij('1 spierlijn', 29, 28, 'hh', 'GG')
rij('1 schouderbolling', 30, 29, 'hhh', 'HHh')
rij('1 schouderbolling', 31, 30, 'hh', 'HH')
rij('1 schaduw achter schouder', 31, 34, 'hh', 'GG')
rij('1 schaduw achter schouder', 30, 33, 'hh', 'hG')

# 2. Verre arm: eigen licht (h aan de lichte kant), vulling G, schaduw g; blijft een stap donkerder dan de nabije arm.
for y, x0, oud, nieuw in [(35, 18, 'GG', 'hG'), (36, 17, 'GGG', 'hGG'), (37, 16, 'GGG', 'hhG'), (38, 14, 'GGGG', 'hhGG'),
                          (39, 13, 'GGGG', 'hhGG'), (40, 12, 'GGG', 'hGG'), (41, 11, 'GGG', 'hGG'), (42, 11, 'GGG', 'hGG'),
                          (43, 11, 'GGG', 'hGG')]:
    rij('2 verre arm', y, x0, oud, nieuw)

# 3. Romp achter/boven de nabije arm in schaduw, zodat de arm loskomt
rij('3 romp achter arm', 35, 35, 'h', 'G')
rij('3 romp achter arm', 36, 29, 'hhh', 'GGG')

# 4. Roze rug: donker onderaan tegen het groen, licht bovenaan
rij('4 plaat', 23, 28, 'rrr', 'ddd')
rij('4 plaat', 27, 41, 'rr', 'pp')
rij('4 plaat', 28, 40, 'rr', 'pp')

im = Image.fromarray(o.astype('uint8'), 'P'); im.putpalette(pal); im.save('pitahaya3_r8.png', transparency=0)
zt = np.asarray(Image.open('../sprite_r6/pitahaya3_r6_zonder_tong.png')).astype(int)
bk = np.asarray(Image.open('../sprite_r6/pitahaya3_r6_buik.png')).astype(int)
import sys; sys.path.insert(0, '../sprite_r6'); from buik import RIJEN
assert ((o > 0) == (r7 > 0)).all(), 'silhouet'
kd = np.argwhere(o[12:30, 0:21] != zt[12:30, 0:21])
assert all(zt[12+y, x] in (6, 7, 8, 9) for y, x in kd), 'kop: alleen groene nekpixels mogen in het kopvak wijzigen'
assert (o[26:39, 0:13] == zt[26:39, 0:13]).all(), 'bek'
print('groene nekpixels in kopvak gewijzigd:', [(x, 12+y) for y, x in kd])
assert all((o[y, a:b+1] == bk[y, a:b+1]).all() for y, (a, b) in RIJEN.items()), 'buik'
n = (o != r7).sum()
with open('pitahaya3_r8_afwijkingen.txt', 'w') as f:
    f.write('# pitahaya3_r8.png t.o.v. ../sprite_r7/pitahaya3_r7.png: stap | x | y | r7 -> r8 (tekens %s)\n# totaal %d px\n' % (CH, n))
    for r in LOG: f.write('%s | %d | %d | %s -> %s\n' % r)
print('r8 t.o.v. r7:', n)
