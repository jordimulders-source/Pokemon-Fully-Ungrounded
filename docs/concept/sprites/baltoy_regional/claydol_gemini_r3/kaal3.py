# Kale reductie: natief model r3 -> paletindex -> schrappen -> 64x64 (onderkant op rij 63, horizontaal gecentreerd).
import numpy as np
from schrap3 import schrap
from klas import dump
RIJEN=[16,21,39,45,48,60,73,76]
KOLOMMEN=[15,24,33,47,53,63,78,80,83]
def kaal():
    kk,aa,ny,nx=schrap(RIJEN,KOLOMMEN); h,w=kk.shape; oy=64-h; ox=(64-w)//2
    S=np.zeros((64,64),int); A=np.full((64,64,3),255); NY=np.full((64,64),-1); NX=np.full((64,64),-1)
    S[oy:oy+h,ox:ox+w]=kk; A[oy:oy+h,ox:ox+w]=aa; NY[oy:oy+h,ox:ox+w]=ny; NX[oy:oy+h,ox:ox+w]=nx
    return S,A,NY,NX
if __name__=='__main__':
    S,*_=kaal(); np.save('kaal.npy',S); print(np.bincount(S.ravel(),minlength=14)); dump(S)
