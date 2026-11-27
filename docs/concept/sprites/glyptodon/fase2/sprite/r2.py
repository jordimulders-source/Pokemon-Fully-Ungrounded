# Ronde 2: vanaf r1 (r1_I.npy), benoemde reparaties van Claude. Elke stap gemeten op comp_nat (= r4/r6/r3_3-cellen).
import numpy as np
from basis import png,PAL
from staart import staart
I=np.load('r1_I.npy').copy(); I0=I.copy()
def near(c,idx): return idx[int(np.argmin([((np.array(PAL[i])-c)**2).sum() for i in idx]))]
# 1. STAART uit r3_3 per pixel
R=staart(); TH=0.30
tm=np.zeros((64,64),bool)
for (y,x),r in R.items():
    if r['a3']>=0.2 and r['a3']>=r['ao'] and r['a3']+r['ao']>=TH: tm[y,x]=True
# niet over de schildrand/poot heen: pixels die in r1 een ander materiaal hadden en waar r3_3 minder dan de helft dekt blijven
dk={}
for (y,x),r in R.items(): dk[(y,x)]=r['d']+r['k']
D=np.zeros((64,64)); 
for (y,x),v in dk.items(): D[y,x]=v
for y,x in zip(*np.where(tm)):
    r=R[(y,x)]
    if r['k']>=0.45: I[y,x]=1; continue
    if r['g']>=0.45 and r['c'] is not None: I[y,x]=near(r['c'],[10,11,12,13]); continue
    rug=D[y,x]>=D[y-1,x] and D[y,x]>=D[y+1,x]
    if D[y,x]>=0.4 and rug: I[y,x]=5; continue
    if r['c'] is None: I[y,x]=5; continue
    I[y,x]=near(r['c'],[5,6,8,9])
# buitenrand staart -> lijn
op=I>0; P=np.pad(op,1)
rand=op&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
I[tm&rand]=1
np.save('r2_I.npy',I); png(I,'r2.png'); png(I,'r2_8x.png',8)
print('staart: pixels anders dan r1:',(I!=I0).sum())
