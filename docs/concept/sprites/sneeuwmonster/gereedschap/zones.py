# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie (sneeuwmonster)
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
def zone(X,Y):
    if Y<=17: return 'sneeuwpluk'
    if 21<=X<=26 and 21<=Y<=27 or 29<=X<=34 and 21<=Y<=28: return 'ogen'
    if Y<=31: return 'kop'
    if 23<=X<=29 and 33<=Y<=46: return 'knopen'
    if Y>=47: return 'voetjes'
    return 'lijf+armpjes'
t={}
for Y,X in zip(*np.where(k!=o)): t.setdefault(zone(X,Y),[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z in ('sneeuwpluk','kop','ogen','lijf+armpjes','knopen','voetjes'): print(z,len(t.get(z,[])))
print('totaal',sum(len(l) for l in t.values()))
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
