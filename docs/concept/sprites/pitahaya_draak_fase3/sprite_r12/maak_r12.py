# Pitahaya-draak fase 3, r12 (maker). Basis = ../sprite_r11/pitahaya3_r11_D.png (Jordi koos D).
# Jordi: "d is het beste, maar deze rechte lijn die ik geel getekend heb aan sprites ziet er een beetje gek uit, in de mond
#         kan dat onderdeel van het wit worden en buiten de mond kan die misschien iets minder rechtlijning worden" (rij y30, x7-16).
# Gebruik: python3 maak_r12.py  (schrijft pitahaya3_r12.png, pitahaya3_r12_alt.png, pitahaya3_r12_afwijkingen.txt)
import numpy as np; from PIL import Image
CH = '.#drpPgGhHwWkqQs'
B0 = Image.open('../sprite_r11/pitahaya3_r11_D.png'); D = np.asarray(B0).astype(int); pal = B0.getpalette()
def zetter(o, LOG):
    def zet(naam, pixels):
        for x, y, oud, nw in pixels:
            assert CH[o[y, x]] in oud, (naam, x, y, CH[o[y, x]], oud)
            if CH[o[y, x]] != nw: LOG.append((naam, x, y, CH[o[y, x]], nw)); o[y, x] = CH.index(nw)
    return zet
def mond(o, LOG):
    # 1. In de mond: de donkere bodemlijn (8-10,30) wordt vlees in de schaduwtint w (grijs onder, wit midden, grijs boven:
    #    holte). (7,30) blijft d als tandvlees naast de hoektand (6,30), anders loopt de tand in het vlees over.
    #    Ondertanden: (9,31) w -> W zodat de tanden (8-9,31) lichter zijn dan het vlees erboven en los lezen.
    zetter(o, LOG)('1 mond', [(8,30,'d','w'), (9,30,'d','w'), (10,30,'#','w'), (9,31,'w','W')])
def kaak(o, LOG, extra):
    # 2. Onderkaak: in het model loopt de onderrand schuin omhoog van (11,31,5) naar (14,30,3) en dan pas vlak naar de nek.
    #    Silhouet +1 px (12,31) (alt: +2 px, ook (13,31)); de pixel(s) erboven worden kaakvulling d.
    zet = zetter(o, LOG)
    for x in [12] + ([13] if extra else []):
        zet('2 kaak', [(x, 31, '.', '#'), (x, 30, '#', 'd')])
uit = {}
for naam, extra in (('', False), ('_alt', True)):
    o, LOG = D.copy(), []; mond(o, LOG); kaak(o, LOG, extra)
    im = Image.fromarray(o.astype('uint8'), 'P'); im.putpalette(pal); im.save('pitahaya3_r12%s.png' % naam, transparency=0)
    uit[naam] = (o, LOG)
for naam, (o, _) in uit.items():
    d = np.argwhere(o != D); assert all(26 <= y <= 31 and 6 <= x <= 16 for y, x in d), naam   # alleen bek/kaak
    sil = np.argwhere((o > 0) != (D > 0)); print(naam or 'r12', 'px:', len(d), 'silhouet erbij:', [(x, y) for y, x in sil])
with open('pitahaya3_r12_afwijkingen.txt', 'w') as f:
    for naam, (o, LOG) in uit.items():
        f.write('# pitahaya3_r12%s.png t.o.v. ../sprite_r11/pitahaya3_r11_D.png: stap | x | y | D -> r12 (tekens %s)\n# totaal %d px\n' % (naam, CH, (o != D).sum()))
        for r in LOG: f.write('%s | %d | %d | %s -> %s\n' % r)
        f.write('\n')
