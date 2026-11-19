# Kale reductie v3: op het gekwantiseerde natieve raster (natief_q), exact 3x3 -> 1.
# dekking >= ALPHA; oogzwart (2) aanwezig -> 2; >= NL lijnpixels (1 of 3) -> meest voorkomende lijnkleur; anders modus van de vlakkleuren
# (gelijkspel -> dichtstbijzijnde bij het blokgemiddelde in natief.png).
import sys, numpy as np
from reduce2 import PAL, n, save
q=np.load('natief_q.npy')
def reduce(px=1,py=1,ALPHA=4,NL=2):
    x0=77-px; y0=15-py; W=(146-x0)//3+1; Hh=(163-y0)//3+1
    out=np.zeros((Hh,W),'uint8')
    for j in range(Hh):
        for i in range(W):
            sl=(slice(y0+3*j,y0+3*j+3),slice(x0+3*i,x0+3*i+3)); b=q[sl].flatten()
            o=b[b>0]
            if len(o)<ALPHA: continue
            c=np.bincount(o,minlength=16)
            if c[2]>=2: out[j,i]=2; continue
            if c[1]+c[3]+c[2]>=NL: out[j,i]=1 if c[1]+c[2]>=c[3] else 3; continue
            f=c.copy(); f[[1,2,3]]=0; mx=f.max(); cand=np.where(f==mx)[0]
            if len(cand)>1:
                m=n[sl][q[sl]>0].mean(0); cand=cand[np.argmin(((PAL[cand]-m)**2).sum(1))]
            else: cand=cand[0]
            out[j,i]=cand
    return out, (x0,y0)
if __name__=='__main__':
    px,py,A,NL=map(int,sys.argv[1:5]); a,org=reduce(px,py,A,NL); np.save('kaal.npy',a); save(a,'kaal.png'); print(a.shape,org)
