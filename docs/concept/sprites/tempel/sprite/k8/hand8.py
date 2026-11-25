# k8: handwerk bovenop dik.npy (k7 + 2 px afschuining)
import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
a6,pal=laad('../k6/tempel.png'); a=np.load('dik.npy')
STEEN=(3,4,5,6)
# 1. grote steen onderblok rechts (x37-49, y45-52): banden 3/4/5/6 -> één steen, basis 4
R=[]
for y in range(45,53):
    for x in range(37,50):
        if a6[y,x] in STEEN and not (y==45 and x>=47): R.append((x,y))
for x,y in R: a[y,x]=4
for x,y in R:
    licht = (y in (45,46) and x<=45) or (x in (37,38) and y<=50)
    donker= (y in (51,52) and x>=41) or (x>=48 and y>=47) or (x>=46 and y>=49)
    if licht and not donker: a[y,x]=3
    elif donker and not licht: a[y,x]=5
# putje uit het model midden-rechts, met lichte pixel aan de lichtkant (sluit aan op de lichte rand)
for x,y in [(42,48),(43,48),(43,49),(42,49)]: a[y,x]=5
a[47,41]=3
# 2. gezichtsvelden
for x,y in [(17,41)]: a[y,x]=3                       # licht linksboven tussen de ogen 2 px
for x,y in [(20,42),(21,41)]: a[y,x]=5               # sikkel rechtsonder 2 px
for x,y in [(27,41),(28,41),(27,42)]: a[y,x]=5       # vlek rechts van het rechteroog (model)
# 3. zijvlaksteen x40-47 y36-40: vlek
for x,y in [(42,39),(43,39),(43,40)]: a[y,x]=15
# 4. vlekken op terrasvoorkanten
for x,y in [(27,30),(28,30),(28,31)]: a[y,x]=5
for x,y in [(36,37),(37,37),(37,38)]: a[y,x]=5
for (x,y) in [(17,41),(20,42),(21,41),(27,41),(28,41),(27,42),(42,39),(43,39),(43,40),(27,30),(28,30),(28,31),(36,37),(37,37),(37,38)]:
    assert a6[y,x] in STEEN,(x,y)
a7,_=laad('../k7/tempel.png')
# kleine restjes van de 2 px-afschuining opruimen
a[29,35]=3; a[30,35]=3; a[30,31]=a7[30,31]; a[30,32]=a7[30,32]; a[51,29]=5; a[54,31]=3; a[45,49]=6
np.save('k8.npy',a); bewaar(a,pal,'tempel.png')
