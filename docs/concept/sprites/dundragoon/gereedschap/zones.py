# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
L0={41:53,42:53,43:53,44:52,45:51,46:47}
def zone(X,Y,v):
    if Y>=41 and X>L0.get(Y,0) and X>=44: return 'boor'
    if v in VLEUGEL and not (X<=16): return 'vleugels+hoorn rechts'
    if X<=26 and Y<=27: return 'kop+oog+hoorns'
    if (Y>=31 and X<=22) or (Y>=41 and X<=44): return 'pootjes'
    return 'lijf'
t={}
for Y,X in zip(*np.where(k!=o)):
    z=zone(X,Y,k[Y,X] if k[Y,X] else o[Y,X]); t.setdefault(z,[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print(z,len(l))
print('totaal',sum(len(l) for l in t.values()))
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
