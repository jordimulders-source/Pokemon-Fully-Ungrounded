# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie (Altaria-zones)
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
def zone(X,Y):
    if (Y<=16 and 24<=X<=45) or (Y<=21 and 32<=X<=45): return 'kuif'
    if 21<=X<=31 and 16<=Y<=24: return 'kop+oog+snavel'
    if 21<=X<=31 and 25<=Y<=41: return 'hals'
    if Y>=51: return 'shelf cloud onder'
    if X<=21 and Y<=40: return 'vleugel links'
    if X>=40 and Y<=33: return 'vleugel rechts'
    return 'wolk midden'
t={}
for Y,X in zip(*np.where(k!=o)):
    t.setdefault(zone(X,Y),[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in sorted(t.items()): print(z,len(l))
print('totaal',sum(len(l) for l in t.values()))
if len(sys.argv)>3:
    for z,l in sorted(t.items()): print(z,l)
