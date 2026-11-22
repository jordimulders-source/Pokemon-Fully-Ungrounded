# Pitahaya-draak fase 3, r10 (maker): Jordi op r9 (knots los van het been, bek slordig) + controle schaduw/lijn/kleur.
# Basis = ../sprite_r9/pitahaya3_r9.png (= ../af/pitahaya_draak_fase3.png), palet ongewijzigd (index 13 'q' wordt in B grijs i).
# Gebruik: python3 maak_r10.py   (schrijft pitahaya3_r10_A.png, pitahaya3_r10_B.png en pitahaya3_r10_afwijkingen.txt)
import sys, numpy as np; from PIL import Image
CH = '.#drpPgGhHwWkqQs'
B0 = Image.open('../sprite_r9/pitahaya3_r9.png'); r9 = np.asarray(B0).astype(int); pal = B0.getpalette()
def nieuw():
    return r9.copy(), []
def zetter(o, LOG):
    def zet(naam, pixels):
        for x, y, oud, nw in pixels:
            assert CH[o[y, x]] in oud, (naam, x, y, CH[o[y, x]], oud)
            if CH[o[y, x]] != nw: LOG.append((naam, x, y, CH[o[y, x]], nw)); o[y, x] = CH.index(nw)
    def rij(naam, y, x0, oud, nw):
        assert len(oud) == len(nw), (naam, y)
        zet(naam, [(x0+i, y, a, b) for i, (a, b) in enumerate(zip(oud, nw)) if a != b])
    return zet, rij

def gemeen(o, LOG):
    zet, rij = zetter(o, LOG)
    # 1. Knots los van het been (gemeten in het model: rechtsboven de knots staat één spits licht schutblad,
    #    punt omhoog op x 27, y 51-53; links ervan een donkere lijn tegen het roze, rechts het donkere verre been
    #    tot de buitenlijn op x 29; onder het blad de roze lob x 27-28, y 53-55).
    #    r9 had het blad omgekeerd (brede voet bovenaan tegen het been, punt naar beneden) -> blad en been liepen in elkaar over.
    rij('1 schutblad', 51, 26, 'hhG', 'gHg')   # punt H; links donkere lijn, rechts been in schaduw
    rij('1 schutblad', 52, 26, 'ghG', 'gHg')
    rij('1 schutblad', 53, 26, 'dGr', 'dhr')   # blad wordt breder/donkerder naar de knots toe
    zet('1 schutblad', [(27, 54, 'g', 'r')])     # roze lob onder het blad (model)
    #    Onderkant been sluit met een doorlopende donkere lijn tegen de knots (geen groene brug op x 22).
    zet('1 beenonderkant', [(22, 50, 'h', 'g'), (22, 51, 'G', 'r')])
    # 3. Verre achterbeen: één tintstap onder de verre arm (h-G-g zoals de arm, maar met minder h en meer g);
    #    midden x 21-25 naar G, g alleen als sikkel rechts (x 26-28) en als onderlijn tegen de knots.
    rij('3 verre been', 46, 21, 'GGGgg', 'GGGGG')
    rij('3 verre been', 47, 21, 'GGGgg', 'GGGGG')
    rij('3 verre been', 48, 22, 'GGgg', 'GGGG')
    rij('3 verre been', 49, 22, 'Ggg', 'GGG')

def bek_A(o, LOG):
    zet, rij = zetter(o, LOG)
    # 2A. Eén pitje erbij op (9,29): model heeft daar een pit (±9,5;29), 2 px van (9,27) en niet diagonaal tegen (11,28).
    zet('2A bek', [(9, 29, 'W', 's')])
    # en één op (11,26) -> NIET gedaan: vormt met (11,28) een stippellijn langs de rechterrand.

def bek_B(o, LOG):
    zet, rij = zetter(o, LOG)
    # 2B. Zelfde pitjes; vlees naar achteren/boven in schaduw (zoals de teju: bovenrij en achterkant grijs, voor wit).
    rij('2B bek', 26, 8, 'WWWW', 'wwwq')     # schaduw van de bovenkaak; q = donkerder grijs (teju-i) achterin
    zet('2B bek', [(11, 27, 'W', 'w')])      # achterkant mond

uit = {}
for naam, bek in (('A', bek_A), ('B', bek_B)):
    o, LOG = nieuw(); gemeen(o, LOG); bek(o, LOG)
    p = list(pal)
    if naam == 'B': p[13*3:13*3+3] = [155, 154, 159]   # teju-grijs i (index 13 was een ongebruikt dubbel zwart)
    im = Image.fromarray(o.astype('uint8'), 'P'); im.putpalette(p); im.save('pitahaya3_r10_%s.png' % naam, transparency=0)
    uit[naam] = (o, LOG)

A, B = uit['A'][0], uit['B'][0]
# Controles
for n, o in (('A', A), ('B', B)):
    assert ((o > 0) == (r9 > 0)).all(), 'silhouet ' + n
    assert len(set(o.flatten())) <= 16
    zt = np.asarray(Image.open('../sprite_r6/pitahaya3_r6_zonder_tong.png')).astype(int)
    bk = np.asarray(Image.open('../sprite_r6/pitahaya3_r6_buik.png')).astype(int)
    sys.path.insert(0, '../sprite_r6'); from buik import RIJEN
    bek = np.zeros((64, 64), bool); bek[26:30, 7:12] = True
    kop = np.zeros((64, 64), bool); kop[12:30, 0:21] = True; kop &= ~bek
    assert (o[kop] == r9[kop]).all(), 'kop ' + n
    assert all((o[y, a:b+1] == bk[y, a:b+1]).all() for y, (a, b) in RIJEN.items()), 'buik ' + n
verschil = np.argwhere(A != B)
assert all(26 <= y <= 29 and 7 <= x <= 11 for y, x in verschil), 'A en B verschillen buiten de bek'
with open('pitahaya3_r10_afwijkingen.txt', 'w') as f:
    for n in 'AB':
        o, LOG = uit[n]
        f.write('# pitahaya3_r10_%s.png t.o.v. ../sprite_r9/pitahaya3_r9.png: stap | x | y | r9 -> r10 (tekens %s; q in B = grijs 155,154,159)\n# totaal %d px\n' % (n, CH, (o != r9).sum()))
        for r in LOG: f.write('%s | %d | %d | %s -> %s\n' % r)
        f.write('\n')
print('A:', (A != r9).sum(), 'B:', (B != r9).sum(), 'A!=B:', len(verschil))
