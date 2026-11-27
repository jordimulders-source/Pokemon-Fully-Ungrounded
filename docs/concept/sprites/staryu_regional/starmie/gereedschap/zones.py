# zones.py KAAL.png SPRITE.png [lijst]: pixels per zone die afwijken van de kale samenstelling
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *; from kaal import voorste
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int); _,fm=voorste()
def zone(X,Y):
    if not fm[Y,X]: return 'achterste punten'
    if (X-31)**2+(Y-29.5)**2<=8.5**2: return 'juweel'
    return 'voorste ster'
t={}
for Y,X in zip(*np.where(k!=o)): t.setdefault(zone(X,Y),[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print(z,len(l))
print('totaal',sum(len(l) for l in t.values()),'silhouet-diff',int(((k>0)!=(o>0)).sum()))
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
