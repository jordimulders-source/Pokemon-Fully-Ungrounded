# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=laden(sys.argv[1]); o=laden(sys.argv[2])
def zone(X,Y):
    if Y<=13 and X<=16: return 'vinger'
    if X<=20 and Y<=24: return 'hand (vinger)'
    if 12<=Y<=18 and 24<=X<=36: return 'ogen'
    if Y<=21 and X>=40: return 'antennes rechts'
    if Y<=21: return 'kop, snor'
    if Y>=50 and 24<=X<=46: return 'benen'
    if X>=48 and Y<=36: return 'andere hand'
    if Y<=30 and 26<=X<=36: return 'hemd'
    return 'jasje, rokpanden, lijf'
t={}
for Y,X in zip(*np.where(k!=o)): t.setdefault(zone(X,Y),[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print('%-26s %d'%(z,len(l)))
print('totaal',sum(len(l) for l in t.values()),'van',int((o>0).sum()),'px')
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
