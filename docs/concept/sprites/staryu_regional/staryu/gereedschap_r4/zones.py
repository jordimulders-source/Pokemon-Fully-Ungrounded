# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap_r4'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
def zone(X,Y,v):
    if 24<=X<=34 and 28<=Y<=37: return 'juweel'
    if Y<=26 and 20<=X<=38: return 'bovenarm'
    if Y<=38 and X<26: return 'linkerarm'
    if Y<=38 and X>33: return 'rechterarm'
    return 'benen'
t={}
for Y,X in zip(*np.where(k!=o)):
    z=zone(X,Y,k[Y,X] if k[Y,X] else o[Y,X]); t.setdefault(z,[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print(z,len(l))
print('totaal',sum(len(l) for l in t.values()))
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
