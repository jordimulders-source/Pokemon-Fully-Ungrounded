# Bewijs: silhouet (alfa) diff 0, gezicht (neus, snor, wang + lijn eromheen) RGB-diff 0.
from PIL import Image
import os
D = os.path.dirname(os.path.abspath(__file__))
a = Image.open(os.path.join(D,'../../../gnomad/af/gnomad.png')); b = Image.open(os.path.join(D,'na.png'))
assert a.size == b.size == (64,64) and b.mode == 'P'
ap, bp = a.load(), b.load()
ar, br = a.convert('RGB').load(), b.convert('RGB').load()
LILA = {2,3,4,5}
face = set()
for y in range(64):
    for x in range(64):
        i = ap[x,y]
        if i in (12,13,14): face.add((x,y))                       # snor
        elif 25 <= y <= 33 and i not in LILA and i != 0: face.add((x,y))  # neus, wang, lijnen
        elif 34 <= y <= 38 and x <= 28 and i in (1,6,7,8): face.add((x,y)) # roze/zwart tussen de snor
for (x,y) in list(face):                                       # zwart/2-lijn eromheen
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            q = (x+dx, y+dy)
            if 0<=q[0]<64 and 0<=q[1]<64 and ap[q] in (1,2): face.add(q)
alfa = sum(1 for y in range(64) for x in range(64) if (ap[x,y]==0) != (bp[x,y]==0))
fd = sum(1 for p in face if ar[p] != br[p] or ap[p] != bp[p])
idx = sum(1 for y in range(64) for x in range(64) if ap[x,y] != bp[x,y])
used = {bp[x,y] for y in range(64) for x in range(64)} - {0}
print('silhouet-diff (alfa):', alfa)
print('gezichtszone: %d px, diff (index+RGB): %d' % (len(face), fd))
print('gewijzigde pixels (index):', idx, '| kleuren gebruikt:', len(used), '+ transparant')
# masker als plaatje
m = Image.new('RGB',(64,64),(255,255,255)); mp = m.load()
for y in range(64):
    for x in range(64):
        if ap[x,y]: mp[x,y] = (200,200,200)
        if (x,y) in face: mp[x,y] = (60,160,60)
        if ap[x,y] != bp[x,y]: mp[x,y] = (220,30,30)
m.resize((384,384),0).save(os.path.join(D,'diffmasker.png'))
