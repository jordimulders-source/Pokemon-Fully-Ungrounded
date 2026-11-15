# lijnen.py: binnenlijnen opnieuw uit het model, 1 px dik en doorlopend.
#  stap 1: spritepixel is lijnkandidaat als zijn 2x2-modelblok >= 1 zwarte modelpixel heeft ("any": niets valt weg)
#  stap 2: Zhang-Suen-verdunning naar 1 px (topologie blijft: lijnen breken niet); de silhouetrand doet niet mee
#          (die wordt los omlijnd); bij keuze verdwijnt eerst de pixel met de minste zwarte modelpixels
import numpy as np
from auto import nbg, ndrk
def ndk_map():
    m=np.zeros((64,64),int)
    for y in range(7,64):
        for x in range(1,64):
            ny,nx=2*y-14,2*x-1
            if ny+2<=ndrk.shape[0] and nx+2<=ndrk.shape[1]: m[y,x]=ndrk[ny:ny+2,nx:nx+2].sum()
    return m
def verdun(L,vast,ndk):
    L=L.copy()
    def nb(y,x):
        return [L[y-1,x],L[y-1,x+1],L[y,x+1],L[y+1,x+1],L[y+1,x],L[y+1,x-1],L[y,x-1],L[y-1,x-1]]
    while True:
        changed=False
        for stap in (0,1):
            weg=[]
            for y,x in zip(*np.where(L)):
                if vast[y,x] or y in(0,63) or x in(0,63): continue
                P=[int(v) for v in nb(y,x)]; Bn=sum(P)
                if not 2<=Bn<=6: continue
                A=sum(P[i]==0 and P[(i+1)%8]==1 for i in range(8))
                if A!=1: continue
                if stap==0 and (P[0]*P[2]*P[4] or P[2]*P[4]*P[6]): continue
                if stap==1 and (P[0]*P[2]*P[6] or P[0]*P[4]*P[6]): continue
                weg.append((ndk[y,x],y,x))
            # minst zwarte modelpixels eerst; per stap opnieuw toetsen zodat er geen gat valt
            for _,y,x in sorted(weg):
                P=[int(v) for v in nb(y,x)]
                A=sum(P[i]==0 and P[(i+1)%8]==1 for i in range(8))
                if 2<=sum(P)<=6 and A==1: L[y,x]=False; changed=True
        if not changed: return L
