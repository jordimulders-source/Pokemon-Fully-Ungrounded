# lijnen.py: donkere tentakellijnen (R0/K) van VL en VR uit het natieve model, geprojecteerd op het spriteraster.
# Per spritepixel: lijngewicht (natieve oppervlakte) en hoek t.o.v. het mondje. Alleen meten.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from anemonen import *; from gemeen import *
a,c,L=klassen(); H,W=c.shape
def lijnkaart(i, dmax=0.92):
    w=np.zeros((64,64))
    for v in range(H):
        for u in range(W):
            if c[v,u] not in (1,2): continue
            if eigenaar(u+.5,v+.5)!=i or afstand(i,u+.5,v+.5)>dmax or in_mond(i,u+.5,v+.5,1.2): continue
            X=X0+(u+.5-U0)*S; Y=Y0+(v+.5-V0)*S
            w[int(Y),int(X)]+=S*S
    return w
if __name__=='__main__':
    for i in (0,1):
        w=lijnkaart(i); print(AN[i][0])
        ys,xs=np.where(w>0)
        for y in range(ys.min(),ys.max()+1): print('%2d '%y+''.join(' ' if w[y,x]==0 else str(min(9,int(w[y,x]*10))) for x in range(xs.min()-1,xs.max()+2)), xs.min()-1)
