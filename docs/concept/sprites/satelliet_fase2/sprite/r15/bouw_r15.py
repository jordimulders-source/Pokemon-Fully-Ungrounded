# r15: voorvlak + lens op modelmaat (Jordi na r13/r14: "de bovenste kap is bij ons wat hoger en wat bolliger" · "de vorm klopt nog steeds niet").
# Basis ../r14/sprite.png (tinten r13/r14). Model panelen_80b.png, raster sprite-x = (mx-103)/12,703, sprite-y = (my-143)/12,703 + 7.
# Gemeten (lees_model.py, profiel.py, fit_r15.py): in het model is het voorvlak een ronde schijf met een donkere rand die bovenop op
# rij 26 (x15-21) ligt, rechtsboven trapsgewijs naar x29 (rij 33-37) loopt en onderaan via rij 43 in de buitenlijn overgaat; daarbuiten
# bovenop een paarse rand (rij 25). De lens is een cirkel om (18,5; 34,5) met r = 6 (x12-24, y28-40), 1 px groter boven en links dan r14.
# Opbouw van binnen naar buiten zoals het model: iris (r14, oog b + pupil p2 ongewijzigd) > irisrand (r14) > lila > zwarte lensring >
# witte ring > lila ring (r14, rechts) > witte band > voorvlakrand > paarse rand (alleen bovenop). Draaien vanuit deze map: python3 bouw_r15.py
import numpy as np
from PIL import Image
im0 = Image.open('../r14/sprite.png'); a = np.array(im0).astype(int); pal = im0.getpalette()[:48]; r14 = a.copy()
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c == '-': continue
        a[y, x + i] = 0 if c == '.' else H.index(c)
WIT = (2, 3, 4, 5, 15); IRIS = (13, 14)
# ---------- 1. lens: zwarte ring = cirkel om (18,5; 34,5) r 6 (pixelmiddens met |d-6| < 0,5)
cx, cy, R = 18.5, 34.5, 6.0
ring = np.zeros_like(a, bool); binnen = np.zeros_like(a, bool)
for y in range(26, 44):
    for x in range(10, 28):
        d = np.hypot(x + .5 - cx, y + .5 - cy)
        if abs(d - R) < .5: ring[y, x] = True
        elif d < R - .5: binnen[y, x] = True
# r14-lensbinnenkant (lila/irisrand) en iris blijven; nieuwe binnenpixels krijgen de tint van de dichtstbijzijnde r14-binnenpixel
r14_binnen = np.zeros_like(a, bool)
for y in range(29, 41):
    for x in range(13, 25):
        if r14[y, x] in (6, 7, 8) and np.hypot(x + .5 - 19, y + .5 - 35) < 5: r14_binnen[y, x] = True
bys, bxs = np.where(r14_binnen)
for y, x in zip(*np.where(binnen)):
    if r14[y, x] in IRIS + (9,) or (r14[y, x] == 15 and 16 <= x <= 21 and 32 <= y <= 37) or r14_binnen[y, x]: continue
    i = np.argmin((bys - y) ** 2 + (bxs - x) ** 2); a[y, x] = r14[bys[i], bxs[i]]
a[ring] = 1
# ---------- 2. voorvlakrand (pad uit het model), lichtkant 8, schaduwkant 1 (rechts en onder: r14 had die al zwart)
put(15, 26, '8888888')          # bovenop, x15-21
put(15, 27, '888')              # linksboven: lijn loopt naar de paneelrand (x14 = r14-lijn), witte ring is daar in het model weg
put(15, 28, '1')                # lens en voorvlakrand vallen samen (model: x14-15 donker)
put(22, 27, '88')
put(24, 28, '88')
put(26, 29, '8')
put(27, 30, '8')
put(28, 31, '8')
put(28, 32, '1')                # rij 33-37 x29, 38-39 x28, 40 x27, 41 x25-26, 42 x23-24: r14 had die al (zwart)
# ---------- 3. paarse rand buiten de voorvlakrand, alleen bovenop (model rij 25 x16-21, dan trapsgewijs naar rechtsboven)
put(16, 25, '777777')
put(22, 26, '77')
put(24, 27, '77')               # r14 had hier al 77
put(26, 28, '7')
# ---------- 4. lila ring rechts (r14) sluit bovenaan op de voorvlakrand aan: rij 28 x23
put(23, 28, '6')
# ---------- 5. witte ring/band: oude r14-lijnpixels die nu wit zijn krijgen de tint van de dichtstbijzijnde r14-witpixel
nieuw_wit = [(29, 27), (30, 28)]   # r14-dubbele '5' van de oude bovenrand rechtsboven
wys, wxs = np.where(np.isin(r14, WIT) & (np.arange(64)[None, :] >= 22) & (np.arange(64)[:, None] >= 27) & (np.arange(64)[:, None] <= 40))
for y, x in nieuw_wit:
    dd = (wys - y) ** 2 + (wxs - x) ** 2; dd[(wys == y) & (wxs == x)] = 999; i = np.argmin(dd); a[y, x] = r14[wys[i], wxs[i]]
# ======== OPSLAAN
def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette(pal + [0] * (768 - len(pal)))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); rgba = im.convert('RGBA'); m = np.array(rgba); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
if __name__ == '__main__':
    sla(a, 'sprite.png'); np.save('r15.npy', a)
    d = a != r14
    print('afwijkend t.o.v. r14:', d.sum(), 'buiten x12-30/y24-44:', d.sum() - d[24:45, 12:31].sum(), ' kleuren', len(np.unique(a)) - 1,
          ' silhouet: +', ((a > 0) & (r14 == 0)).sum(), ' -', ((a == 0) & (r14 > 0)).sum())
    H2 = '.123456789ABCDEF'
    for y in range(23, 45): print('%2d ' % y + ''.join(H2[v] for v in r14[y, 8:36]) + '   ' + ''.join(H2[v] for v in a[y, 8:36]))
