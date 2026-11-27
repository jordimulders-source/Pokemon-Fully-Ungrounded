# 3x-reductie van het (bewerkte) natieve raster: per 3x3-blok materiaal + gemiddelde helderheid.
import numpy as np; import materiaal as mt
def reduceer(a, fase=(2,2), houtvan=150, lijn_k=3, donker_k=3):
    hr=np.zeros(a.shape[:2],bool); hr[houtvan:,:]=True
    M,L=mt.kaart(a,hr)
    fx,fy=fase; H=(a.shape[0]-fy)//3; W=(a.shape[1]-fx)//3
    mat=np.zeros((H,W),int); lum=np.zeros((H,W)); lijn=np.zeros((H,W),bool)
    for j in range(H):
        for i in range(W):
            bm=M[fy+3*j:fy+3*j+3, fx+3*i:fx+3*i+3].ravel(); bl=L[fy+3*j:fy+3*j+3, fx+3*i:fx+3*i+3].ravel()
            if (bm!=0).sum()<5: continue
            k=(bm==1).sum()
            if k>=lijn_k: mat[j,i]=1; lijn[j,i]=True; lum[j,i]=bl[bm==1].mean(); continue
            rest=bm[(bm>1)]
            if len(rest)==0: mat[j,i]=1; continue
            m=np.bincount(rest).argmax(); mat[j,i]=m
            sel=bl[bm==m]
            # donkere zandlijn (binnenlijn in het model) wint als hij >= donker_k pixels heeft
            if m==2 and ((bl<100)&(bm!=0)).sum()>=donker_k: lum[j,i]=min(sel.min(),95)
            else: lum[j,i]=sel.mean()
    return mat,lum
