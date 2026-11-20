# kuif15.py (r15): verre vleugel, kuifplukken en kruin opnieuw op het r14-raster (zone x4-30, y0-19 + kruinrand y20).
# Tekens: . = transparant, 1 lijn, 2-5 mauve (donker->licht), 6 bruin kern, 7 bruin licht.
# Leest ../r14/hoatzin.png, schrijft k15.npy.
import numpy as np; from PIL import Image
a = np.array(Image.open('../r14/hoatzin.png')).astype(int)
for y in range(0, 19):
    for x in range(4, 30): a[y, x] = 0
# ---------- verre vleugel: 4 ronde toppen (model), toppen 4/3, scheidingen 2, lijn 2 boven/links, 1 rechts ----------
W = {2: (8, '22..22'),
     3: (7, '24422442.22'),
     4: (7, '244324432442'),
     5: (7, '243324332443222'),
     6: (7, '2433333324332441'),
     7: (7, '2333333333332431'),
     8: (7, '23333333333333331'),
     9: (7, '23333333333333331'),
     10: (7, '233333333333333331'),
     11: (7, '233333333333333331'),
     12: (7, '2333333333333333331'),
     13: (7, '23333333333333333331'),
     14: (7, '23333333333333333331'),
     15: (7, '233333333333333333331'),
     16: (7, '233333333333333333331'),
     17: (7, '2333333333333333333331'),
     18: (7, '2333333333333333333331')}
def paint(rows):
    for y, (x0, s) in rows.items():
        for i, c in enumerate(s):
            if c != '.': a[y, x0+i] = int(c)
paint(W)
# ---------- kruin (x7-20, y15-19): 7 linksboven, 6 kern, 2 als gebogen sikkel rechtsonder ----------
K = {14: (9, '77'),
     15: (8, '777766666'),
     16: (7, '2777666666'),
     17: (7, '276666666662'),
     18: (7, '27666666666622'),
     19: (6, '276666666666222')}
# twee korte haarstrepen 7 in de kruin, ongelijk van lengte en richting (geen arcering)
K2 = {17: (12, '7....7'), 18: (12, '7....7')}
paint(K)
# ---------- plukken uit het model (lengte en afstand gevarieerd) ----------
# per rij: 7 = lichtkant (boven/links), 6 = kern, 2 = schaduw onder/rechts op de vleugel, 1 = lijn tegen de lucht
P = {
 # P1 steil linksboven, tip (5,8) steekt uit; schaduw 2 alleen bij de voet
 'P1': {8: (5, '1'), 9: (5, '61'), 10: (5, '261'), 11: (5, '276'), 12: (6, '276'), 13: (6, '276'), 14: (7, '2762')},
 # P2 kort, recht omhoog, eindigt in de vleugel (tip 11,9); schaduw 2 alleen bij de voet
 'P2': {9: (11, '6'), 10: (11, '76'), 11: (11, '76'), 12: (11, '76'), 13: (11, '762'), 14: (11, '762')},
 # P6 kort, steil rechtsboven (ca. 60 graden), eindigt in de vleugel (tip 17,7), voet samen met P3
 'P6': {7: (17, '2'), 8: (16, '62'), 9: (15, '762'), 10: (15, '77'), 11: (14, '77')},
 # P3 lang, 45 graden, tip (21-23,7) steekt uit, einde (24,7)
 'P3': {7: (21, '6661'), 8: (19, '7662'), 9: (18, '7662'), 10: (17, '762'), 11: (16, '762'),
        12: (15, '762'), 13: (14, '762'), 14: (13, '762')},
 # P4 vlak naar rechts, tip (27,12) steekt uit
 'P4': {12: (22, '777661'), 13: (18, '777766621'), 14: (16, '776666222'), 15: (17, '6222')},
 # P5 naar rechts en omlaag, loopt over in de punt (28,19) van r14
 'P5': {16: (17, '777766'), 17: (17, '66662277766'), 18: (23, '66666')},
}
for nm in ['P1', 'P2', 'P6', 'P3', 'P4', 'P5']: paint(P[nm])
paint(K2)
# kruin onderrand: geen rechte 2-rij meer boven het gezicht links; (9,20),(10,20) bruin
a[20, 9] = 6; a[20, 10] = 6
a[18, 21] = 2; a[18, 22] = 2   # geen vleugelgaatje tussen sikkel en P5
np.save('k15.npy', a)
Image.fromarray(a.astype('uint8'), 'P').save('/tmp/k15_tmp.png')
