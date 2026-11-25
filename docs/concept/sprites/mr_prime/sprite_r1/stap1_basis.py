# Stap 1: kale reductie (gezicht_fase.red(0,2) op natief_stok.png) in 64x64 zetten, r9-bolhoed + golvende lokken weghalen. Tonen: 0=zwart 1=48 2=64 3=80 4=112 5=144 6=208 7=248, -1=transparant.
import numpy as np
k=np.load('kaal_idx.npy')[:61]
C=np.full((64,64),-1); OY=3; C[OY:OY+61,:]=k
log={}
def zet(y,x,v,zone):
    if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
# --- hoed + lokken weg (reductiecoords +OY) ---
for y in range(0,13):
    for x in range(24,64):
        if C[y+OY,x]!=-1: zet(y+OY,x,-1,'hoed/haar r9 weg')
for y in range(13,17):
    for x in range(45,64):
        v=C[y+OY,x]
        if x>=49: 
            if v!=-1: zet(y+OY,x,-1,'hoed/haar r9 weg')
        elif v not in (6,7): zet(y+OY,x,-1,'hoed/haar r9 weg')
# (stok wordt dikker gemaakt op het natieve raster: stok.py)
np.save('basis.npy',C); print(log)
