# zones.py KAAL.png SPRITE.png [lijst]: aantal pixels per zone dat afwijkt van de kale reductie
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap'); from gemeen import *
k=np.asarray(Image.open(sys.argv[1])).astype(int); o=np.asarray(Image.open(sys.argv[2])).astype(int)
def zone(X,Y):
    if 19<=Y<=28 and X<=13: return 'bek/snuit'
    if 13<=Y<=18 and X<=15: return 'ogen'
    if X<=22 and Y<=30: return 'kop (oren, voorhoofd)'
    if X<=14 and Y>=29: return 'opgeheven poot'
    if Y>=45: return 'poten'
    if k[Y,X] in VACHT or o[Y,X] in VACHT or k[Y,X]==1: return 'manen/staart/vacht'
    return 'grijs lijf (vlekken)'
t={}
for Y,X in zip(*np.where(k!=o)):
    t.setdefault(zone(X,Y),[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,l in t.items(): print('%-24s %d'%(z,len(l)))
print('totaal',sum(len(l) for l in t.values()),'van',int((o>0).sum()),'px')
if len(sys.argv)>3:
    for z,l in t.items(): print(z,l)
