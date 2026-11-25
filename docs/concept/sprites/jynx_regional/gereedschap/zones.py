# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie (regionale Jynx)
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
def zone(X,Y,v):
    if 18<=X<=33 and 9<=Y<=28 and v in (1,9,10,11,12,13,14): return 'gezicht'
    if 17<=X<=34 and 9<=Y<=28 and v==6 and o[Y,X]==6 and k[Y,X]==1: return 'gezicht'   # gezichtscontour
    if Y>=55: return 'poten+klauwen'
    if v in HAAR: return 'haar'
    if (X<=14 and Y<=31) or (X>=38 and Y<=31): return 'vleugels'
    return 'lijf+rok'
t={}
for Y,X in zip(*np.where(k!=o)):
    v=k[Y,X] if k[Y,X]>1 else o[Y,X]
    z=zone(X,Y,v); t.setdefault(z,[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print(z,len(l))
print('totaal',sum(len(l) for l in t.values()))
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
