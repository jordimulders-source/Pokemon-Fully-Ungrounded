# r9: bovenkant opnieuw uit het model (gewricht, kraag, antennes, klein gewricht, staaf naar paneel),
# linkerjunctie lijf/klein paneel met een heldere zwarte lijn + paneelrandlijn, lijf witter (palet + groter wit vlak),
# ring linksboven 1 px en ronder. Basis: ../r8/sprite_p2.png (pupil p2 blijft). Draaien vanuit deze map: python3 bouw_r9.py
import numpy as np
from PIL import Image
im0 = Image.open('../r8/sprite_p2.png'); a = np.array(im0).astype(int); pal = im0.getpalette()[:48]
r8 = a.copy()
H = '0123456789ABCDEF'
def put(x, y, s):
    for i, c in enumerate(s):
        if c == '-': continue
        a[y, x + i] = 0 if c == '.' else H.index(c)

# ---- palet: lijf minder lavendel; C (paneellijn) los van lijftint 4 ----
pal[2*3:2*3+3] = [242, 240, 238]
pal[3*3:3*3+3] = [222, 217, 230]
pal[4*3:4*3+3] = [188, 177, 208]
pal[5*3:5*3+3] = [146, 126, 170]
pal[12*3:12*3+3] = [160, 148, 214]

# ---- bovenkant leegmaken (alles boven het lijf tussen klein paneel en groot paneel) ----
for y in range(5, 20):
    for x in range(21, 45): a[y, x] = 0
for x in range(21, 45): a[20, x] = 0 if x > 36 else a[20, x]

# linker (achterste) antenne: bol x34-37 r7-10, staaf schuin naar de kraag (model: (34,10) -> (24,17))
put(35, 7, '88')
put(34, 8, '8671')
put(34, 9, '8781')
put(33, 10, '7811')
put(31, 11, '778')
put(30, 12, '78')
put(29, 13, '78')
put(28, 14, '78')
# rij 15: staaf L | groot gewricht top | rechter antenne begin
put(26, 15, '7788816688')
put(25, 16, '788866718')
# rechter (voorste) antenne: boog omhoog naar rechts, runs 2-2-2-3-6; bol x47-50 r9-12
put(34, 14, '6688')
put(36, 13, '66888')
put(38, 12, '666888888')
put(41, 11, '6666668671')
put(48, 9, '88')
put(47, 10, '8361')
put(48, 12, '11')
# rij 17-19: klein paneel-hoek | kraag links (schuin oplopend) | groot gewricht | kraag rechts | klein gewricht
put(19, 17, '991888666863718888')
put(15, 18, '9999BB17661118667166678')
put(14, 19, '9BBB99B1111222877811111888')
put(43, 18, '669')
put(41, 19, '6688')
# klein gewricht x37-40 r19-23 + staaf naar paneel
put(12, 20, '99BB999B11' + '3222222' + '111' + '22334' + '8661' + '88')
put(11, 21, '9B99999' + '11' + '3' + '2' * 12 + '3344' + '8671')
put(10, 22, '9B99999' + '1' + '3' + '2' * 13 + '33445' + '8771')
put(10, 23, '9B99B9' + '1' + '3' + '2' * 13 + '33444' + '55' + '11')
a[23, 40] = 0
put(9, 24, '9B99BB' + '1' + '3' + '2' * 13 + '33' + '444' + '555' + '1')
put(9, 25, '9BBBB' + '1' + '3' + '2' * 12 + '333' + '4444' + '555' + '1')
# rij 26-30: ring linksboven 1 px en ronder (loopt bij x15-16 een rij lager de lijn in), rechts schuin vlak
put(13, 26, 'B1' + '22' + '666666' + '7' + '2222' + '3333' + '44' + '555' + '1')
put(13, 27, '91' + '66' + '222' + '33' + '66' + '77' + '2222' + '333' + '44' + '55' + '1')
put(33, 28, '3345')
put(32, 29, '33445')
put(32, 30, '334455')

# paneelrandlijn (lichte paneellijn B) langs de zwarte scheidingslijn, zoals in het model
for x, y in [(17, 21), (16, 22), (15, 23), (13, 27), (13, 28)]: a[y, x] = 11
# linkerjunctie volgens de modelmeting per rij (zwarte lijn: r18-20 x21, r21 x19, r22 x18, r23 x17, r24 x16, r25 x15, r26-28 x14)
# kraag links: bovenlijn r16 x23-24 / r17 x22, kleur r17-18, onderrand r19 in 8 (model: kraag 3-4 px hoog, licht naar het gewricht)
put(23, 16, '88')
put(21, 17, '1866666')
put(21, 18, '1766667')
put(20, 19, 'B18888')
a[19, 26] = 2; a[19, 27] = 2
put(19, 20, 'BB1')
put(17, 21, '9B1333')
put(16, 22, '9B1332')
put(15, 23, '9B1332')
put(14, 24, 'BB1332')
put(13, 25, 'BB1332')
put(14, 26, '133')
# schuin vlak rechts: 4-vlak dat in het midden breder wordt (geen strook evenwijdig aan de rand), 5 als sikkel rechtsonder
put(32, 20, '22334')
put(32, 21, '33444')
put(31, 22, '334445')
put(30, 23, '3344455')
put(29, 24, '33444455')
put(28, 25, '2334444455')
put(28, 26, '334444455')
put(29, 27, '33444455')
a[28, 27] = 2
put(31, 28, '334451')
put(32, 29, '334451')
put(32, 30, '334451')
put(32, 31, '334451')
put(36, 32, '51')
# staaf klein gewricht -> paneel eindigt op de paneelrand (r8-rest weg)
a[17, 44] = 0; a[17, 45] = 6; a[17, 46] = 9
# keurder r8 (1): witte buitenring links-onder de lens laten doorlopen
a[38, 14] = 3; a[38, 15] = 1

def sla(arr, naam):
    im = Image.fromarray(arr.astype('uint8'), 'P'); im.putpalette(pal + [0] * (768 - len(pal)))
    im.save(naam, transparency=0)
    b = Image.new('RGBA', (64, 64), (255, 255, 255, 255)); rgba = im.convert('RGBA'); m = np.array(rgba); m[arr == 0, 3] = 0; b.alpha_composite(Image.fromarray(m))
    b.convert('RGB').resize((512, 512), Image.NEAREST).save(naam.replace('.png', '_8x.png'))
sla(a, 'sprite.png')
np.save('r9.npy', a)
d = (a != r8)
print('afwijkend t.o.v. r8:', d.sum())
for nm, (x0, x1, y0, y1) in {'boven': (21, 51, 5, 21), 'links': (8, 21, 16, 29), 'lijf': (21, 40, 20, 31)}.items():
    print(nm, d[y0:y1, x0:x1].sum())
