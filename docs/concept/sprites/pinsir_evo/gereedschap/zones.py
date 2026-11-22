# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
def zone(X,Y):
    if 26<=Y<=35 and 15<=X<=23: return 'gezicht (ogen, mond)'
    if k[Y,X] in KAAK or o[Y,X] in KAAK: return 'kaken'
    if k[Y,X] in SCHILD or o[Y,X] in SCHILD: return 'dekschild'
    if Y<=27 and X<=40: return 'kopschild + stekels'
    if Y>=45: return 'poten en staart'
    return 'lijf (romp, arm, rugstekels)'
t={}
for Y,X in zip(*np.where(k!=o)):
    t.setdefault(zone(X,Y),[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print('%-30s %d'%(z,len(l)))
print('totaal',sum(len(l) for l in t.values()),'van',int((o>0).sum()),'px')
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
