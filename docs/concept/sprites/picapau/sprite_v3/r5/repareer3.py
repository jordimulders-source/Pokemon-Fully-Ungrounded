# r3 op r2.npy: Picapau-palet terug (2 grijzen + wit), vleugel licht/donker naar de modelmeting, opschonen onder de snavel.
import numpy as np
o=np.load('r2.npy').copy(); R={}
def zet(zone,lst):
    for x,y,v in lst:
        if o[y,x]!=v: R.setdefault(zone,[]).append((x,y,o[y,x],v)); o[y,x]=v
# 1 snavel/poten: middengrijs (18) weg -> randpixels donkergrijs 11, binnen lichtgrijs 10 (150 140 116 = code 10)
zet('snavel',[(20,18,11),(20,19,11),(23,19,11),(24,20,11),(22,21,10),(23,21,10),(24,21,10),(25,21,10),(24,22,10),(25,22,10),(25,23,11)])
zet('nabije poot',[(34,46,10),(34,47,10),(34,48,10),(35,46,11),(35,47,11),(35,48,11),(34,49,11),(35,49,11)])
zet('oogglans',[(30,19,16)])
# 2 vleugel: licht 156 82 0 (12) op het lichtere modeldeel (gemeten helderheid ~90 tegen ~56), grens schuin langs de vleugel
LIM={26:41,27:41,28:41,29:41,30:40,31:39,32:38,33:37}
W={12,13}
for y in range(24,44):
    for x in range(33,50):
        if o[y,x] not in W: continue
        nb=[o[y-1,x],o[y+1,x],o[y,x-1],o[y,x+1]]
        rand=0 in nb or o[y,x-1] in (2,3,4,1)          # buitenrand of linker grens met het lijf blijft donker
        v=12 if (y in LIM and x<=LIM[y] and not rand) else 13
        zet('vleugel',[(x,y,v)])
# 3 onder de snavel: model is daar geel met rood aan de rand (x21 r24-25); rand gladgetrokken
zet('onder snavel',[(20,23,0),(21,23,17),(21,24,6),(21,25,6),(22,25,3)])
np.save('r3.npy',o)
t=0
for z,l in R.items(): print('%-14s %2d px'%(z,len(l)),l if len(l)<8 else ''); t+=len(l)
print('totaal t.o.v. r2',t)
