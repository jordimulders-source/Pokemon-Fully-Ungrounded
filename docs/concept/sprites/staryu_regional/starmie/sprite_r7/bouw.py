# bouw.py r7: python3 sprite_r7/bouw.py   (vanuit starmie/)
# Eindkeuring Dragonfly Cave op r6_licht: alleen uitvoering. Silhouet bevroren (alpha-diff 0, assert).
# Elke wijziging: (x, y, oude index, nieuwe index, reden); de oude index wordt per pixel ge-assert.
import numpy as np; from PIL import Image
IN='sprite_r6/starmie_r6_licht.png'; OUT='sprite_r7/starmie_r7.png'
im=Image.open(IN); o=np.array(im).copy(); o0=o.copy()
pal=[tuple(im.getpalette()[3*i:3*i+3]) for i in range(16)]

W=[]
# (a) schaduw/volume. D = modelhelderheid van alleen de koekcellen onder de pixel, Dp = idem glazuur (natief r4-raster).
# a1 voorste bovenpunt + rechterrand bovenarm: donker vlak (4) aan de schaduwkant tot in de afgestompte tip,
#    zoals de Gen 3-tip (licht links, donker rechts). D 128-157, behalve (32,8) D177 (doorlopend gehouden, geen gat).
for x,y in [(31,6),(32,7),(32,8),(33,9),(34,10),(34,11),(35,12),(35,13)]: W.append((x,y,5,4,'a1 tip/rand boven donker vlak'))
# a2 rechtsonderarm: sikkel 5-4-3 i.p.v. sprong 5->3 (D 150-153)
for x,y in [(44,47),(44,48),(44,49)]: W.append((x,y,5,4,'a2 sikkel rechtsonder'))
# a3 achterpunt rechtsonder: licht vlak langs de bovenrand tot de tip (D 146-152 tegen 125-140 eronder)
for x,y in [(48,35),(49,35),(50,36)]: W.append((x,y,4,5,'a3 lichtrand achterpunt rechtsonder'))
# a4 glazuurlicht uit het model (Dp 178-199): binnenstrook lichtkant bovenarm, bovenkant linkerarm, linksonderarm
for x,y in [(29,10),(28,11),(28,12),(27,13),(23,21),(21,22),(22,22),(17,46)]: W.append((x,y,9,10,'a4 glazuurlicht model'))
# (b) belijning
# b1 glazuurlijn bovenarm rechts doorlopend 1 px (was: zwart binnen het silhouet, gat, en een koeklijn-pixel)
W+= [(33,11,1,5,'b1 zwart binnen silhouet -> koekrand'),(33,12,1,7,'b1 zwart -> glazuurlijn'),
     (33,13,8,7,'b1 gat in glazuurlijn'),(35,16,2,7,'b1 koeklijn -> glazuurlijn')]
# b2 bovenrand rechterpunt (rij 21): 2,2,1,1,2,2,1,2,1 om en om -> outline base aan de lichtkant, zwart alleen aan het eind
W+= [(49,21,1,2,'b2 om-en-om'),(50,21,1,2,'b2 om-en-om'),(53,21,1,2,'b2 om-en-om')]

for x,y,a,b,r in W:
    assert o0[y,x]==a, (x,y,o0[y,x],a,r)
    o[y,x]=b
# (c) tinten: koek = regionale Staryu (zelfde deeg, zoals Game Freak Staryu/Starmie hetzelfde goud geeft)
pal[2]=(146,74,34); pal[3]=(198,112,50); pal[4]=(228,160,72); pal[5]=(244,198,118)
pal[6]=(252,228,150)      # glans/gele hagelslag, L 210 (stap 23 boven 5)
pal[15]=(102,54,36)       # chocolade = Staryu-chip
# paars: hue shift (licht naar roze, schaduw naar blauw), helderheid gelijk
pal[7]=(66,34,92); pal[8]=(125,70,156); pal[10]=(223,168,232)

assert ((o>0)==(o0>0)).all(), 'silhouet veranderd'
assert (o!=o0).sum()==len(W)
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette([v for c in pal for v in c]+[0]*(768-48)); p.save(OUT,transparency=0)
from collections import Counter
print('gewijzigd',len(W),Counter(w[4].split()[0] for w in W))
