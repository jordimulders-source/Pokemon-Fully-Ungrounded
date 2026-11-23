# Telt per zone de pixels die afwijken van de kale reductie (basis.npy) en het silhouetverschil.
import numpy as np, json
b0=np.load('basis.npy'); b1=np.load('r1.npy'); Z=json.load(open('zones.json'))
d=(b0!=b1); tot=int(d.sum()); print('totaal afwijkend van kale reductie:',tot,'van',int((b1>0).sum()),'pixels')
gezien=set()
for k,v in Z.items():
    pts=[tuple(p) for p in v if d[p[0],p[1]] and tuple(p) not in gezien]
    gezien|=set(pts); print('%-12s %4d'%(k,len(pts)))
rest=[(y,x) for y,x in zip(*np.where(d)) if (y,x) not in gezien]; print('zonder zone:',len(rest))
print('silhouet: erbij',int(((b0==0)&(b1>0)).sum()),' eraf',int(((b0>0)&(b1==0)).sum()))
