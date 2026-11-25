# r16: hoofd opnieuw vanaf het model op het 64-raster (Jordi na r15: "de vorm klopt gewoon nog niet" · "de vorm wijkt echt flink af" ·
# "op meerdere vlakken, het oog stuk, het bovenste bolletje waar de antenne opt komt, de gladde vormen etc" ·
# "de antennes die waren goed (iets dikker dan in het model) en dat is prima, alleen de bol onder de grootste antenne mag meer zoals het model").
# Bron: ../../paneel_varianten/panelen_80b.png, raster sprite-x = (mx-103)/12,703, sprite-y = (my-143)/12,703 + 7 (zie modelraster.py).
# Elke lijnpositie hieronder is gemeten in het model (lijnen_r16.py, profielen en blokmedianen in het verslag); de maker tekent niets zelf:
# - lens: zwarte ring = modelcirkel x13-24 / rij 29-40 (rand 13,2-24,7 / 28,7-40,6), binnenkant = oog B + pupil P2 (r8 p2 / r15-iris);
# - bol onder de grote antenne: modelcirkel x27-32 / rij 15-20 (was in r15 x27-32 / rij 15-21, 1 rij te lang en te hoekig);
# - kapcontour linksboven, voorvlakrand, lila ring, witte sikkel onder de lens, onderrand: modelposities.
# Antennes (staven + eindbolletjes), panelen en het rechtergewricht/knopje blijven r15. Tinten: palet r13/r15.
# Draaien vanuit deze map: python3 bouw_r16.py
import numpy as np
from PIL import Image
im0 = Image.open('../r15/sprite.png'); a = np.array(im0).astype(int); pal = im0.getpalette()[:48]; r15 = a.copy()
r8 = np.array(Image.open('../r8/sprite_p2.png')).astype(int)
M = np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(float); k = 12.703
LM = .299 * M[..., 0] + .587 * M[..., 1] + .114 * M[..., 2]
def Lmed(x, y):   # mediaan helderheid van het binnenste van het modelblok van spritepixel (x, y)
    ya, yb = int(143 + (y - 7) * k) + 2, int(143 + (y - 6) * k) - 2; xa, xb = int(103 + x * k) + 2, int(103 + (x + 1) * k) - 2
    return float(np.median(LM[ya:yb, xa:xb]))
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c == '-': continue
        a[y, x + i] = 0 if c == '.' else H.index(c)

# ---------- 1. kap/lijf (wit metaal): tint uit de modelhelderheid, palet r13 (2 basis, 3 schaduw, 4 sikkel, 5 diepst)
def kaptint(L):
    return 2 if L >= 216 else 3 if L >= 183 else 4 if L >= 150 else 5
KAP = {19: [(23, 26), (32, 36)], 20: [(22, 27), (31, 36)], 21: [(20, 36)], 22: [(18, 36)], 23: [(17, 37)], 24: [(16, 37)],
       25: [(21, 36)], 26: [(24, 36)], 27: [(16, 21), (26, 36)], 28: [(15, 22), (27, 36)], 29: [(15, 16), (21, 23), (27, 36)],
       30: [(14, 14), (23, 24), (26, 26), (28, 36)], 31: [(24, 24), (27, 27), (29, 36)]}
for y, rs in KAP.items():
    for x0, x1 in rs:
        for x in range(x0, x1 + 1): a[y, x] = kaptint(Lmed(x, y))

# volume zoals r13: hooglicht F = de helderste band van het model op de koepel (L >= 240, rij 20-26, x <= 34);
# sikkel 4 langs de rechterrand (x36 rij 25-31, x37 rij 23-24), 3 ernaast op de lijfzijde (x35, rij 28-31)
for y in range(20, 27):
    for x in range(14, 35):
        if a[y, x] in (2, 3) and Lmed(x, y) >= 240: a[y, x] = 15
for y in range(25, 32): a[y, 36] = 4
a[23, 37] = a[24, 37] = 4      # rij 23-24 ligt de rechterrand een pixel verder (x38-39)
for y in range(28, 32): a[y, 35] = 3

# ---------- 2. bol onder de grote antenne (model x27-32, rij 15-20; rand 8 boven/links, zwart rechts/onder, hooglicht 3 linksboven)
put(29, 15, '88')
put(28, 16, '8667')
put(27, 17, '873671')
put(27, 18, '876781')
put(27, 19, '87781')
put(28, 20, '111')

# ---------- 3. kapcontour linksboven (model: rij 19 x22, rij 20 x20-21, rij 21 x18-19, rij 22 x17, rij 23 x16, rij 24 x15, rij 25 x14),
# lichtkant = 5 (eigen donkerste tint, zoals r13); erboven de lichtpaarse rand (r15 rij 18) die bij x20-21 een rij doorloopt (model rij 19-20)
put(20, 18, '7')
put(19, 19, 'B775')
put(18, 20, 'B755')
put(16, 21, 'AB55')
put(15, 22, 'AB5')
put(16, 23, '5')
put(15, 24, '5')
put(14, 25, '5377777')          # contour, witte rand, paarse rand bovenop het voorvlak (model x16-20; r15 x16-21)

# ---------- 4. voorvlakrand (model: rij 26 x15-21, rij 27 x22-23, rij 28 x24-25, (26,29), (27,30), (28,31-32), x29 rij 33-37) en paarse rand erbuiten
put(14, 26, '88888888'); put(22, 26, '77')
put(14, 27, '88'); put(22, 27, '88'); put(24, 27, '77')
put(14, 28, '1'); put(23, 28, '6'); put(24, 28, '887')
put(13, 29, '91'); put(24, 29, '678')
put(13, 30, '1'); put(25, 30, '6'); put(27, 30, '8')
put(13, 31, '7'); put(25, 31, '67'); put(28, 31, '8')
put(13, 32, '7'); put(26, 32, '6'); put(27, 32, '2'); put(28, 32, '1')

a[27, 16] = 3                   # binnenkant voorvlakrand linksboven: lavendel band (model 192), geen losse donkere pixel

# ---------- 4b. onderkant (model): lijfcontour links x13 rij 36-39, x14 rij 40-42, (15,43) (16,44) (17-18,45) (19-20,46), x21-28 rij 47;
# voorvlakrand (29,37) (28,38-39) (27,40) (26,41) x22-25 rij 42, x18-21 rij 43, x16-17 rij 42, (15,41); lila ring (26,37) (25,38-39)
# (24-25,40) (23-24,41); witte sikkel onder de lens (model 192-200): rij 40-42 binnen de rand, rij 43-44 buiten de rand; onderlip 5.
put(13, 36, '1'); put(13, 37, '1'); put(24, 37, '23723'); put(29, 37, '1')
put(13, 38, '1'); put(24, 38, '2733'); put(28, 38, '1')
put(13, 39, '13'); put(23, 39, '22733'); put(28, 39, '1')
put(13, 40, '.133'); put(21, 40, '333773'); put(27, 40, '15')
put(13, 41, '.114333333773135')
put(14, 42, '15113333111135')
put(15, 43, '145111143345')
put(16, 44, '1533333555555')
put(17, 45, '115555555555')
put(19, 46, '1155555555')

# ---------- 5. lens: ring + band = r8 p2 (oog B, modelcirkel), iris/pupil P2/glans = r15
yy, xx = np.mgrid[0:64, 0:64]
lens = (np.hypot(xx + .5 - 19, yy + .5 - 35) <= 6.0)   # 12x12-schijf x13-24 / rij 29-40 (r7-cirkel)
for y, x in zip(*np.nonzero(lens)):
    a[y, x] = r15[y, x] if (16 <= x <= 21 and 32 <= y <= 37 and r15[y, x] in (9, 13, 14, 15)) else r8[y, x]

# ---------- 6. linkerkant lens/paneel: de lensring (x13) is daar de lijfcontour (model: contour 12,5 en ring 13,2 liggen 0,7 px uit elkaar);
# de oude r15-lensring op x12 wordt paneelrand B (model: paarse paneelrand 11,6-12,2); oude r15-contour x12 rij 36-37 weg (model: achtergrond)
for y in range(32, 36): a[y, 12] = 11
a[32, 13] = 7                   # paarse lijfrand onder (13,31), model 116/69
a[36, 12] = 0; a[37, 12] = 0; a[37, 13] = 1

# ---------- 7. technisch opschonen (ruis < 3 px, geen tintbanden langs de contour), alleen tinten, geen lijnen verplaatst
for x, y, v in ((31, 20, 15), (22, 25, 2), (27, 20, 2), (22, 20, 2), (35, 19, 2), (35, 22, 3), (33, 23, 3), (30, 24, 3), (28, 25, 3), (24, 26, 15),
                (15, 25, 2), (21, 25, 2), (21, 27, 3), (15, 28, 3), (16, 29, 3), (21, 29, 2), (28, 30, 2), (24, 32, 2),
                (26, 30, 3), (27, 31, 3), (27, 32, 3), (27, 37, 3),
                (16, 41, 3), (15, 42, 5), (16, 43, 5), (22, 43, 3), (25, 43, 3), (27, 43, 5), (28, 43, 5)):
    a[y, x] = v
for y, x in ((21, 20), (21, 21), (22, 18), (22, 19), (22, 20), (23, 17), (23, 18), (24, 16), (24, 17), (24, 18)):
    if a[y, x] == 3: a[y, x] = 2      # lichte rand langs de kapcontour: basis 2 (r13), geen 3-band evenwijdig aan de contour
put(28, 21, '333')              # slagschaduw onder de bol (model 204-214 onder de bol)
a[25, 37] = 1; a[25, 38] = 0    # rechtercontour rij 25 op x37 (model), niet x38

# ======== OPSLAAN
def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette(pal + [0] * (768 - len(pal)))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); rgba = im.convert('RGBA'); m = np.array(rgba); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
if __name__ == '__main__':
    sla(a, 'sprite.png'); np.save('r16.npy', a)
    H2 = '.123456789ABCDEF'
    print('   ' + ''.join(str(x % 10) for x in range(6, 42)))
    for y in range(12, 50): print('%2d ' % y + ''.join(H2[v] for v in a[y, 6:42]))
