import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
a0,pal=laad('../k6/tempel.png')
a=np.load('stap2.npy')
F=15
HAND=[
 # gezichtsblok: licht linksboven per veld, donkere sikkel rechtsonder tegen latei/onderrand
 (3,[(17,39),(18,39),(17,40)]),
 (3,[(26,39),(26,40),(27,40)]),
 (5,[(19,43),(20,43),(21,43),(21,42)]),
 (5,[(28,45),(29,45),(30,45),(29,44),(30,44)]),
 # steen rechts van de deur (licht vlak): sikkel rechtsonder
 (4,[(30,47),(30,48),(29,48)]),
 # steen links onder het gezicht
 (5,[(12,49),(12,50),(12,51)]),
 (5,[(11,53),(11,54),(11,55)]),
 # terrasvoorkant tussen de gevels
 (3,[(28,18),(29,18),(28,19)]),
 (5,[(30,21),(31,21),(31,22)]),
 # terrasvoorkant midden
 (5,[(29,32),(30,32),(30,31)]),
 # bovenste terras, steen onder de lichte rand
 (5,[(43,26),(44,26),(44,25)]),
 # zijvlak boventerras
 (F,[(48,19),(48,20),(47,20)]),
 # onderblok rechts: hooglicht linksboven, sikkel rechtsonder
 (3,[(38,47),(39,47),(38,48)]),
 (F,[(46,50),(46,51)]),
 (F,[(53,47),(54,47),(54,46)]),
 # onderste steen rechts: hooglichtvlakje linksboven
 (3,[(37,55),(38,55),(37,56)]),
]
TERUG=[(32,15),(33,15),(34,15),(35,18),(36,18),(37,18)]
for x,y in TERUG: a[y,x]=a0[y,x]
HAND+=[(F,[(47,8)]),(F,[(53,19)]),(F,[(47,34)]),(5,[(6,44),(7,44),(4,45)]),(5,[(28,52)]),
       (5,[(39,38),(40,38),(40,39),(40,40)]),   # terrasvoorkant rechts: sikkel rechtsonder
       (F,[(45,59),(46,59),(44,60),(45,60)])]   # onderste steen rechts: sikkel in de hoek
for c,pts in HAND:
    for x,y in pts:
        assert a0[y,x] in (3,4,5,6), (x,y,a0[y,x])
        a[y,x]=c
np.save('stap3.npy',a); bewaar(a,pal,'tempel.png'); print((a!=a0).sum())
