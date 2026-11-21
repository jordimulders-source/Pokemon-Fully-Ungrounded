# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie (Swablu-zones)
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
def zone(X,Y):
    if Y<=23 and X>=23: return 'voelsprieten+vonken'
    if 21<=X<=33 and 24<=Y<=37: return 'kop+oog+snavel'
    if Y>=39 or (X>=40 and Y>=37): return 'onderwolk+staartje'
    if X<=20: return 'wolk links'
    return 'vleugel+wolk rechts'
t={}
for Y,X in zip(*np.where(k!=o)):
    t.setdefault(zone(X,Y),[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print(z,len(l))
print('totaal',sum(len(l) for l in t.values()))
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
