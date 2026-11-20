# bouw16.py (r16) vanaf ../r15/hoatzin.png:
#  A kuif (plukken + kruin) terug van r14 (Jordi: "14 is de kuif beter dan 15"); verre-vleugeltoppen y2-7 van r15 (W uit kuif15.py)
#    waar ze niet botsen met de r14-kuif; plukdikte ongewijzigd (2 px).
#  B kuif linksonder sluit aan op de kop: harde 2-rand tussen kruin en blauw vlak/snavel -> bruin 6 (plukbasis groeit uit de kruin).
#  C nekscheiding: doorlopende binnenlijn 1 waar de vleugel over de nek valt (grens uit het model), slagschaduw 2 links ervan
#    (2 px breed boven, 1 px onder: taps), lichte voorrand 5 rechts ervan (boven), onderaan uitlopend.
#  D verre (linker) poot: scheen D/D/2/2 + lijn, voet met twee tenen naar links (D boven, 2 onder) en twee klauwen, uit het model;
#    een stap donkerder dan de nabije voet (E/D/2).
import numpy as np; from PIL import Image
a = np.array(Image.open('../r15/hoatzin.png')).astype(int)
r14 = np.array(Image.open('../r14/hoatzin.png')).astype(int)
# ---------- A ----------
a[0:21, 4:31] = r14[0:21, 4:31]
W = {2: (8, '22..22'), 3: (7, '24422442.22'), 4: (7, '244324432442'), 5: (7, '243324332443222'),
     6: (7, '2433333324332441'), 7: (7, '2333333333332431')}
for y in range(0, 8):
    for x in range(4, 31):
        if a[y, x] not in (6, 7): a[y, x] = 0
for y, (x0, s) in W.items():
    for i, c in enumerate(s):
        if c != '.' and a[y, x0+i] not in (6, 7): a[y, x0+i] = int(c)
# aansluiting y7/y8: F4-tip van r14 (22,8) houdt zijn lijn (23,8); rechts van de vleugelrand niets
# ---------- B ----------
for x, y in [(9, 20), (10, 20), (8, 21), (9, 21)]: a[y, x] = 6
# kruinonderrand: het rechte 2-stuk (13-16,19) -> 6, zodat de sikkel (16-17,18)-(17-20,19)-(15-18,20) gebogen blijft
for x in range(13, 17): a[19, x] = 6
# gaatje vleugelpaars linksonder in de kuif (8,15-16) en de donkere stip (8,17) -> bruin: kuif groeit uit de kruin naar de kop
a[15, 8] = 7; a[16, 8] = 7; a[17, 8] = 7
# ---------- C ----------
L = {23: 28, 24: 28, 25: 27, 26: 27, 27: 26, 28: 26, 29: 25, 30: 25, 31: 25, 32: 24, 33: 24, 34: 24, 35: 24}
for y, x in L.items():
    a[y, x] = 1
    a[y, x-1] = 2 if a[y, x-1] in (3, 4, 5) else a[y, x-1]
    if y <= 30 and a[y, x-2] in (3, 4, 5): a[y, x-2] = 2
    if 24 <= y <= 31 and a[y, x+1] in (2, 3, 4): a[y, x+1] = 5
# ---------- D ----------
V = {'.': 0, 'D': 14, 'E': 15}
far = {50: (24, '2DD221'), 51: (23, '2DD221'), 52: (23, '2DD221'), 53: (22, '2DD221'),
       54: (14, '...11111DD221.'),
       55: (14, '..1DDDDDDD21'),
       56: (14, '.1222222DD2'),
       57: (14, '.1.1DDDDD2'),
       58: (14, '1..122222'),
       59: (14, '..1.......'),
       60: (14, '.........')}
for y, (x0, s) in far.items():
    for i, c in enumerate(s): a[y, x0+i] = V[c] if c in V else int(c)
np.save('r16.npy', a)
im = Image.fromarray(a.astype('uint8'), 'P'); im.putpalette(Image.open('../r15/hoatzin.png').getpalette()); im.save('hoatzin.png', transparency=0)
