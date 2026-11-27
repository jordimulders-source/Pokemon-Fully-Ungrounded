# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
def zone(X,Y,v):
    if X<=33 and Y<=38 and (v in ROOD or v in WIT or (v==1 and Y<=36)): return 'vruchttros+ogen'
    if Y>=42 and (X<=24 or X>=42 or Y>=47): return 'ranken (krullen)'
    if X>=44 and Y<=31: return 'blad'
    return 'rank'
t={}
for Y,X in zip(*np.where(k!=o)):
    z=zone(X,Y,k[Y,X] if k[Y,X] else o[Y,X]); t.setdefault(z,[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print(z,len(l))
print('totaal',sum(len(l) for l in t.values()))
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
