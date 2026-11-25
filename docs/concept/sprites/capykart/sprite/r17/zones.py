# zones.py: pixels die afwijken van de kale reductie, per zone en per stap (laatste stap die de pixel veranderde)
import sys, numpy as np
sys.path.insert(0,'sprite/r17'); from gemeen import CH
o=np.load('sprite/r17/_o.npy'); k=np.load('sprite/r17/_kaal.npy'); st=np.load('sprite/r17/_stap.npy',allow_pickle=True)
def zone(X,Y):
    if 43<=X<=60 and Y<=30: return 'toren (blokken+dak)'
    if X<=40 and Y<=31 and not (X>=33 and Y>=27): return 'kop'
    if 15<=X<=26 and 31<=Y<=36: return 'kin/tanden'
    return 'auto+hoepels+wielen+nek'
t={}
for Y,X in zip(*np.where(k!=o)):
    z=zone(X,Y); t.setdefault(z,{}).setdefault(st[Y,X],[]).append((int(X),int(Y),CH[k[Y,X]]+'>'+CH[o[Y,X]]))
for z,d in t.items():
    print(z,sum(len(l) for l in d.values()),{s:len(l) for s,l in d.items()})
    if len(sys.argv)>1:
        for s,l in d.items(): print('   ',s,l)
print('totaal',int((k!=o).sum()))
