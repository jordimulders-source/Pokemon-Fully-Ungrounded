# Pitahaya-draak fase 3, r11 (maker). Basis = ../sprite_r10/pitahaya3_r10_A.png (knots/been en verre been uit r10 blijven).
# Jordi op r10: "de binnenkant van de mond is niet verbeterd, 2 stipjes onder elkaar geeft niet het juiste effect.
#                Doe de stipjes op de buik ook onregelmatiger".
# Palet: index 13 'q' (was ongebruikt dubbel zwart) = teju-grijs i (155,154,159) in alle drie de varianten.
# Gebruik: python3 maak_r11.py  (schrijft pitahaya3_r11_C/D/E.png + pitahaya3_r11_afwijkingen.txt)
import sys, numpy as np; from PIL import Image
CH = '.#drpPgGhHwWkqQs'
B0 = Image.open('../sprite_r10/pitahaya3_r10_A.png'); r10 = np.asarray(B0).astype(int); pal = list(B0.getpalette())
pal[13*3:13*3+3] = [155, 154, 159]

def zetter(o, LOG):
    def zet(naam, pixels):
        for x, y, oud, nw in pixels:
            assert CH[o[y, x]] in oud, (naam, x, y, CH[o[y, x]], oud)
            if CH[o[y, x]] != nw: LOG.append((naam, x, y, CH[o[y, x]], nw)); o[y, x] = CH.index(nw)
    return zet

# 2. BUIK: oude pitjes (zigzag-raster) weg, 7 nieuwe op wisselende afstanden. Elk pitje heeft rondom (ook diagonaal)
#    geen ander pitje; 6 staan met vier buren in wit (niet tegen rand of schaduw), 1 bovenaan raakt alleen de
#    slagschaduw van de kaak. Stappen tussen opeenvolgende pitjes: (-2,1) (3,1) (1,2) (2,3) (2,1) (1,2), geen rij/kolom.
OUD = [(20,31),(22,32),(20,33),(24,34),(24,36),(26,37),(28,38),(26,39),(28,40),(27,42)]
NIEUW = [(21,31),(19,32),(22,33),(23,35),(25,38),(27,39),(28,41)]
def buik(o, LOG):
    zet = zetter(o, LOG)
    for x, y in OUD: zet('2 buik weg', [(x, y, 's', 'w' if (x, y) == (27, 42) else 'W')])   # (27,42) ligt in de sikkel
    for x, y in NIEUW: zet('2 buik pit', [(x, y, 'Ww', 's')])

# 1. BEK. Model (gemeten): wit vlees x 7,5-12,5, y 26-30; op (11,29) toont het model vlees, de sprite had daar zwart
#    -> bekopening 1 px groter, (11,29) # -> W, in alle varianten. Oude pitjes (9,27) (9,29) (11,28) eerst weg.
def bek_basis(o, LOG):
    zet = zetter(o, LOG)
    zet('1 bek basis', [(9,27,'s','W'), (9,29,'s','W'), (11,28,'s','W'), (11,29,'#','W')])
def bek_C(o, LOG):   # wit vlees, 2 pitjes schuin t.o.v. elkaar (dx 1, dy 2)
    zetter(o, LOG)('1C bek', [(9,27,'W','s'), (10,29,'W','s')])
def bek_D(o, LOG):   # teju-opbouw: bovenrij grijs (slagschaduw bovenkaak, achterin donkerder), achterkant grijs, voor wit;
                     # 3 pitjes als driehoek (keurdertip) (9,27) (11,28) (8,29)
    zetter(o, LOG)('1D bek', [(8,26,'W','w'), (9,26,'W','w'), (10,26,'W','w'), (11,26,'W','q'), (11,27,'W','w'),
                              (9,27,'W','s'), (11,28,'W','s'), (8,29,'W','s')])
def bek_E(o, LOG):   # wit vlees; één zwart pitje middenin, de twee pitjes die tegen de rand vallen in grijs q
    zetter(o, LOG)('1E bek', [(10,28,'W','s'), (11,26,'W','q'), (8,29,'W','q')])

uit = {}
for n, f in (('C', bek_C), ('D', bek_D), ('E', bek_E)):
    o, LOG = r10.copy(), []
    buik(o, LOG); bek_basis(o, LOG); f(o, LOG)
    im = Image.fromarray(o.astype('uint8'), 'P'); im.putpalette(pal); im.save('pitahaya3_r11_%s.png' % n, transparency=0)
    uit[n] = (o, LOG)

# Controles
bek = np.zeros((64,64), bool); bek[26:30, 7:12] = True
buikz = np.zeros((64,64), bool); buikz[30:44, 17:31] = True
for n, (o, _) in uit.items():
    sil = (o > 0) == (r10 > 0); assert sil.all(), n
    assert ((o != r10) & ~bek & ~buikz).sum() == 0, 'buiten bek/buik ' + n
    assert len(set(o.flatten())) <= 16
for a in 'DE':
    d = np.argwhere(uit['C'][0] != uit[a][0]); assert all(bek[y, x] for y, x in d), 'C/' + a
for x, y in NIEUW:   # geen pitje grenst aan een ander pitje (8-buren)
    assert not any((x+dx, y+dy) in NIEUW for dx in (-1,0,1) for dy in (-1,0,1) if (dx, dy) != (0, 0))
with open('pitahaya3_r11_afwijkingen.txt', 'w') as f:
    for n in 'CDE':
        o, LOG = uit[n]
        f.write('# pitahaya3_r11_%s.png t.o.v. ../sprite_r10/pitahaya3_r10_A.png: stap | x | y | r10A -> r11 (tekens %s; q = grijs 155,154,159)\n# totaal %d px\n' % (n, CH, (o != r10).sum()))
        for r in LOG: f.write('%s | %d | %d | %s -> %s\n' % r)
        f.write('\n')
print({n: int((o != r10).sum()) for n, (o, _) in uit.items()})
