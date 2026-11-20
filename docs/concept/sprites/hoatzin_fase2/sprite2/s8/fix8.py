# fix8.py: s8 = s7 + keurderpunten op s7. Alleen bestaande paletindexen, alleen binnen het silhouet.
# Elke regel verandert een pixel alleen als hij de verwachte s7-waarde heeft (anders gemeld).
import numpy as np
from PIL import Image
im7 = Image.open('../s7/hoatzin.png'); A = np.array(im7).astype(int); B = A.copy()
mis = []
def zet(pts, van, naar):
    for x, y in pts:
        if B[y, x] == van: B[y, x] = naar
        else: mis.append((x, y, int(B[y, x]), van, naar))
def blok(x0, x1, y0, y1): return [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]
def waar(pts, v): return [(x, y) for x, y in pts if A[y, x] == v]
# 1. licht/schaduw over het vlak van de nabije vleugel en het lijf
zet(waar(blok(32, 34, 10, 21), 3), 3, 2)          # lichte sikkel langs de voorrand
zet(waar(blok(38, 44, 20, 22), 3), 3, 4)          # schaduw onder de dekveren
zet(waar(blok(40, 41, 34, 40), 3), 3, 4)          # schaduwsikkel rechts op het lijf
# 2. streeppatroon: alleen de bovenste 2 pennen (y <= 12) houden een lichte bovenrand
zet(waar(blok(43, 58, 13, 24), 2), 2, 3)
# 3. dubbele lijnen kuif (e = 14 -> d = 13)
zet([(7, 26), (8, 26), (9, 26), (10, 26), (14, 23), (13, 24), (12, 25), (13, 25)], 14, 13)
# 4. snavel lichter, onderkaak eindigt op x8 (model: rij 34 x6-7 kaakgrijs, x8-11 warm grijs/creme-schaduw)
zet([(4, 32), (5, 32)], 7, 6); zet([(8, 34)], 7, 4); zet([(x, 34) for x in range(9, 14)], 7, 6)
# 5. zwarte klont bij de verre voet
zet([(42, 57), (43, 57)], 1, 7)
# 6. verre vleugel: lichte pentoppen langs de bovenrand (rij 18 niet: gaf barcode 4/3 om en om met rij 16)
zet(waar([(17, 16), (18, 16), (19, 16), (17, 20), (18, 20), (19, 20)], 4), 4, 3)
# klein: een enkele 6 op de lichtkant van elke poot ((17,53) en (19,51) uit de keuring zijn lucht; dichtstbijzijnde pootpixel)
zet([(27, 53), (41, 54)], 7, 6)
Image.fromarray(B.astype(np.uint8), 'P').save('hoatzin.png') if False else None
out = Image.fromarray(B.astype(np.uint8), 'P'); out.putpalette(im7.getpalette()); out.save('hoatzin.png', transparency=0)
out.convert('RGB').resize((512, 512), Image.NEAREST).save('hoatzin_8x.png')
print('niet toegepast (x, y, is, verwacht, naar):', mis)
print('anders dan s7:', int((A != B).sum()), '· silhouet anders dan s7:', int(((A > 0) != (B > 0)).sum()))
