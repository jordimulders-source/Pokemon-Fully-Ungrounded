# zones.py KAAL.png SPRITE.png: aantal pixels per zone dat afwijkt van de kale reductie
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
def zone(X,Y):
    if Y<=19 and X>=21 and (o[Y,X] in HOUT|GRIJS or k[Y,X] in HOUT|GRIJS): return 'emmer'
    if 19<=Y<=24 and 20<=X<=35: return 'ogen'
    if 24<=Y<=27 and 19<=X<=35: return 'mond'
    if 27<=Y<=34 and 13<=X<=41 and not (o[Y,X] in STEEN or k[Y,X] in STEEN): return 'baardfranje'
    if o[Y,X] in STEEN or k[Y,X] in STEEN or (X,Y)==(23,40): return 'stenen'
    return 'omlijning/vacht'
t={}
for Y,X in zip(*np.where(k!=o)): t.setdefault(zone(X,Y),[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z in ('emmer','ogen','mond','baardfranje','stenen','omlijning/vacht'): print(z,len(t.get(z,[])))
print('totaal',sum(len(l) for l in t.values()))
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
