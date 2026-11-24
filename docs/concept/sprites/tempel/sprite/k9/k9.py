# k9 = k8 + bergwand (facetten, barsten, putje, lichte rand) + poortlijnen volgens de regels
import sys, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
a8,pal=laad('../k8/tempel.png'); a=a8.copy()
E,F,Z=14,15,6
def zet(c,pts):
    for x,y in pts:
        assert a8[y,x] in (6,14,15),(x,y,a8[y,x]); a[y,x]=c
# --- bergwand boven (x48-56, y22-25): verticale e-streep x50 weg, schuine barst, lichte facetrand linksboven
zet(F,[(50,22),(50,23),(50,24),(50,25)])
zet(Z,[(48,22),(49,22),(48,23)])
zet(E,[(51,23),(52,23),(52,24),(53,24),(54,24)])
# --- bergwand midden (x49-55, y31-39): streep x53 wordt een barst die naar linksonder knikt
zet(F,[(53,36),(53,37),(53,38),(53,39)])
zet(E,[(52,35),(52,36),(52,37),(51,37),(51,38),(51,39)])
zet(Z,[(49,34),(50,34),(49,35)])
zet(F,[(56,34),(57,34),(57,35),(58,35)])   # facet in het donkere vlak (model: schuine facetrand)
# --- bergwand onder (x49-58, y49-56): streep x53 wordt barst naar rechtsonder, putje, lichte rand onder de voeg
zet(F,[(53,52),(53,53),(53,54),(53,55)])
zet(E,[(54,51),(54,52),(55,52),(55,53)])
zet(Z,[(50,51),(51,51),(50,52)])
zet(E,[(51,54),(51,55),(50,55)])
np.save('wand.npy',a)
# --- poort: lichtkant (boven/links) in de voegtint 7, schaduwkant (onder/rechts) zwart
w=a.copy()
L7=[(x,44) for x in range(13,23)]+[(23,45),(24,45),(25,45),(12,45),(12,46)]+[(13,y) for y in range(48,52)]+[(12,y) for y in range(52,57)]+[(11,57)]
L1=[(x,47) for x in range(13,22)]+[(25,y) for y in range(46,58)]+[(26,y) for y in range(58,61)]+[(22,48),(23,48),(24,48)]
for x,y in L7:
    assert a8[y,x]==2,(x,y,a8[y,x]); w[y,x]=7
for x,y in L1:
    assert a8[y,x]==2,(x,y,a8[y,x]); w[y,x]=1
bewaar(w,pal,'tempel.png')
print('rest 2 in poortgebied:',[(x,y) for y in range(43,62) for x in range(10,27) if w[y,x]==2])
