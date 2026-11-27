# Ronde 1: kale reductie (basis.py) + technische opschoning
#  a) lijnen: rug-detectie op de lijnfractie (1 px dik, zoals de 1-natieve-px-lijn van het model)
#  b) buitenlijn gesloten
import numpy as np
from basis import basis,png,PAL,RAMP
I,MAT,INFO=basis(TH=2.0)   # eerst zonder lijnen: materiaalkleur overal
kf=np.zeros((64,64)); al=np.zeros((64,64))
for (y,x),(a,w) in INFO.items(): kf[y,x]=w.get('K',0); al[y,x]=a
op=I>0
P=np.pad(kf,1)
rugx=(kf>=P[1:-1,:-2])&(kf>=P[1:-1,2:])
rugy=(kf>=P[:-2,1:-1])&(kf>=P[2:,1:-1])
lijn=op&((kf>=0.55)|((kf>=0.25)&(rugx|rugy)))
I[lijn]=1
np.save('r1a_I.npy',I); np.save('r1a_kf.npy',kf)
png(I,'r1a.png'); png(I,'r1a_8x.png',8)
# b) buitenlijn: elke ondoorzichtige pixel die (4-buren) aan transparant grenst wordt lijn,
#    behalve de linkerrand van de stekel (olijf-selout uit r6, index 2 blijft)
op=I>0; P=np.pad(op,1)
rand=op&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
stekel_links=np.zeros_like(op); stekel_links[5:20,10:16]=True
for y,x in zip(*np.where(rand)):
    if stekel_links[y,x] and MAT[y,x]=='S': I[y,x]=2; continue
    I[y,x]=1
np.save('r1b_I.npy',I); png(I,'r1b.png'); png(I,'r1b_8x.png',8)
