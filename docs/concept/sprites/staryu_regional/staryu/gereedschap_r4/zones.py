# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap_r4'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
import math
ARMEN=[(10.9,'rechterarm'),(70.6,'bovenarm'),(159.2,'linkerarm'),(233.3,'linkerbeen'),(304.9,'rechterbeen')]   # hoeken uit armen.py (model)
def zone(X,Y,v):
    if 23<=X<=32 and 27<=Y<=36: return 'juweel'
    h=math.degrees(math.atan2(-(Y+.5-32.0),X+.5-27.5))%360
    return min(ARMEN,key=lambda t:min(abs(t[0]-h),360-abs(t[0]-h)))[1]
t={}
for Y,X in zip(*np.where(k!=o)):
    z=zone(X,Y,k[Y,X] if k[Y,X] else o[Y,X]); t.setdefault(z,[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print(z,len(l))
print('totaal',sum(len(l) for l in t.values()))
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
