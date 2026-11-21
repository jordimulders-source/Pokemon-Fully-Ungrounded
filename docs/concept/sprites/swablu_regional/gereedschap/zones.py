# zones.py KAAL.png SPRITE.png: aantal pixels per zone dat afwijkt van de kale reductie
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
def zone(X,Y,v):
    if (18<=X<=34 and 32<=Y<=41) or (24<=X<=31 and 41<=Y<=46): return 'mond+kwijl'
    if Y<=25 and (v in STEEN|GLOED or v==1) and 17<=X<=40: return 'lavabrok'
    if X<=18 and 23<=Y<=34: return 'kelp links'
    if X>=33 and 23<=Y<=39 and v in KELP|STEEN|GLOED|{1} and not (X<=40 and Y>=36): return 'kelp rechts'
    return 'lijf+ogen+vinnen'
t={}
for Y,X in zip(*np.where(k!=o)):
    z=zone(X,Y,k[Y,X] if k[Y,X] else o[Y,X]); t.setdefault(z,[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print(z,len(l))
print('totaal',sum(len(l) for l in t.values()))
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
