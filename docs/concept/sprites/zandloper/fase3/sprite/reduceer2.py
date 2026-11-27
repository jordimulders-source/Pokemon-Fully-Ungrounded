# 3x-reductie, versie 2: eerst elke natieve pixel naar zijn tintband (label), dan per 3x3-blok:
# >= lijn_k lijnpixels -> lijn (1); anders de meest voorkomende tintband (gelijk -> donkerste). Geen middeling, dus harde tintgrenzen.
# zones: dict naam->(masker natief, lijn_k, bruinlijn) om per zone de lijnregel te kiezen.
import numpy as np; import materiaal as mt; import kleur
def pixlabels(a,houtvan=150,bruin=None):
    hr=np.zeros(a.shape[:2],bool); hr[houtvan:,:]=True
    M,L=mt.kaart(a,hr); P=np.zeros(M.shape,int)
    P[M==1]=1
    s=M==2; P[s]=10+np.searchsorted(kleur.ZAND,L[s])
    br=np.ones(M.shape,bool) if bruin is None else bruin
    P[s&(L<100)&br]=1                       # donkerbruine modellijn telt als lijn (waar bruin=True)
    g=M==3; P[g]=20+np.searchsorted(kleur.GLAS,L[g])
    h=M==4; P[h]=30+np.searchsorted(kleur.HOUT,L[h])
    return P
def reduceer(a,fase=(2,2),lijn_k=2,kzone=None,kz=3,bruin=None):
    P=pixlabels(a,bruin=bruin); fx,fy=fase; H=(a.shape[0]-fy)//3; W=(a.shape[1]-fx)//3
    lab=np.zeros((H,W),int)
    for j in range(H):
        for i in range(W):
            sl=(slice(fy+3*j,fy+3*j+3),slice(fx+3*i,fx+3*i+3))
            b=P[sl].ravel()
            if (b!=0).sum()<5: continue
            k=lijn_k
            if kzone is not None and kzone[sl].sum()>=5: k=kz
            if (b==1).sum()>=k: lab[j,i]=1; continue
            r=b[b>=10]
            if len(r)==0: lab[j,i]=1; continue
            mats=r//10; m=np.bincount(mats).argmax(); r=r[mats==m]
            v,c=np.unique(r,return_counts=True); best=v[c==c.max()].min()
            lab[j,i]=best
    return lab
