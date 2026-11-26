# Labels -> indexbeeld. Tinten = mediaan van modelpixels in die helderheidsband (kleur mag later naar Gen 3 schuiven).
import numpy as np; from PIL import Image; import materiaal as mt
ZAND=[100,140,175,200]      # grenzen S0|S1|S2|S3|S4
GLAS=[105,155,200]          # G0|G1|G2|G3
HOUT=[88,105]               # W0|W1|W2
def band(v,gr): return int(np.searchsorted(gr,v))
def labels(mat,lum):
    H,W=mat.shape; lab=np.zeros((H,W),int)   # 0 transp, 1 zwart, 10+ zand, 20+ glas, 30+ hout
    for j in range(H):
        for i in range(W):
            m=mat[j,i]
            if m==0: continue
            if m==1: lab[j,i]=1
            elif m==2: lab[j,i]=10+band(lum[j,i],ZAND)
            elif m==3: lab[j,i]=20+band(lum[j,i],GLAS)
            elif m==4: lab[j,i]=30+band(lum[j,i],HOUT)
            elif m==5: lab[j,i]=23
    return lab
def modelkleuren(a):
    hr=np.zeros(a.shape[:2],bool); hr[150:,:]=True
    M,L=mt.kaart(a,hr); c={0:(0,0,0),1:(16,16,16)}
    for m,base,gr in ((2,10,ZAND),(3,20,GLAS),(4,30,HOUT)):
        b=np.searchsorted(gr,L)
        for t in range(len(gr)+1):
            sel=(M==m)&(b==t)
            c[base+t]=tuple(np.median(a[sel],axis=0).astype(int)) if sel.sum() else (255,0,255)
    return c
