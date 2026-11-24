# Stap 1 (r2): kale reductie (gezicht_fase.red(0,2) op natief_kop.png) in 64x64 (rij+3), r9-bolhoed + lokken weghalen.
# Tonen: 0=zwart 1=48 2=64 3=80 4=112 5=144 6=208 7=248, -1=transparant.
import numpy as np
k=np.load('kaal_idx.npy')[:61]
C=np.full((64,64),-1); OY=3; C[OY:OY+61,:]=k
log={}
def zet(y,x,v,zone):
    if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
for y in range(0,14):                       # r9-hoed (2 rijen hoger door het voorhoofd) -> weg
    for x in range(24,64):
        if C[y,x]!=-1: zet(y,x,-1,'hoed/haar r9 weg')
for y in range(14,20):                      # lokken achter de kop
    for x in range(44,64):
        v=C[y,x]
        if x>=49 or v not in (6,7):
            if v!=-1: zet(y,x,-1,'hoed/haar r9 weg')
np.save('basis.npy',C); print(log)
