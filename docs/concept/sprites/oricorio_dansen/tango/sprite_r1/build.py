# basis.npy (schrap-onderlaag 5->3, elke pixel = modelpixel, 3 px marge) -> tango_kls.npy + log per stap.
import numpy as np, json, sys
from collections import Counter
from lib import *
o=np.load('basis.npy').copy(); H,W=o.shape; log={}; nieuw={}   # nieuw: pixels die niet uit het model komen, per zone
D=[I[n] for n in ('D1','D2','D3','D4','D5','D6')]; K=[I['K1'],I['K2'],I['K3']]
def zet(y,x,v,zone):
    if o[y,x]!=v: o[y,x]=v; nieuw.setdefault(zone,set()).add((y,x))
# 0. randruis: lichte pixels (W/D6/D5) tegen de achtergrond zijn anti-aliasing van het witte model -> transparant
n=0
for it in range(2):
    for y in range(H):
        for x in range(W):
            if o[y,x]==I['W'] and any(yy is None or o[yy,xx]==0 for yy,xx in nb4(o,y,x)) and not (8<=y<=13 and 20<=x<=25):
                o[y,x]=0; n+=1
log['0_randruis']=n
# 1. benen weg (Jordi: mensenbenen -> Oricorio-staakpootjes). Roze/wit/omlijning van de benen vanaf rij 30.
#    In de split (rij <= 43, links en rechts jurk op dezelfde rij) -> D1 (binnenkant jurk), eronder -> transparant.
been=np.zeros_like(o,bool)
for y in range(30,H):
    for x in range(W):
        if o[y,x] in K or (o[y,x]==I['W'] and any(yy is not None and o[yy,xx] in K for yy,xx in nb4(o,y,x))): been[y,x]=True
for it in range(1):   # omlijning direct om de benen die geen jurk raakt
    add=[]
    for y in range(30,H):
        for x in range(W):
            if o[y,x]==I['O'] and not been[y,x] and any(yy is not None and been[yy,xx] for yy,xx in nb4(o,y,x)):
                if y>=48 or not any(yy is not None and o[yy,xx] in D for yy,xx in nb4(o,y,x)): add.append((y,x))
    for p in add: been[p]=True
nd=nt=0
for y,x in zip(*np.where(been)):
    row=o[y]; L=[v for v in row[max(0,x-8):x] if v and v not in K]; R=[v for v in row[x+1:x+9] if v and v not in K]
    if y<=43 and L and R and any(v in D for v in L) and any(v in D for v in R): o[y,x]=I['D1']; nieuw.setdefault('split_binnenkant',set()).add((y,x)); nd+=1
    else: o[y,x]=0; nt+=1
log['1_benen_weg_naar_D1']=nd; log['1_benen_weg_naar_transparant']=nt
np.save('na_benen.npy',o)
