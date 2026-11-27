# Ronde 2: zelfde lijn- en materiaalregels als reduceer2, maar de zandtint per spritepixel = band van de GEMETEN
# modelhelderheid van het blok (gemiddelde van de niet-lijn-zandpixels na ontspikkelen: 3x3-mediaan op de natieve helderheid).
import numpy as np; import materiaal as mt; import kleur, reduceer2
def ontspikkel(L):
    H,W=L.shape; P=np.pad(L,1,mode='edge'); st=np.stack([P[dy:dy+H,dx:dx+W] for dy in range(3) for dx in range(3)])
    return np.median(st,axis=0)
def reduceer(a,fase=(2,2),lijn_k=2,kzone=None,kz=3,bruin=None,maat='gem',grenzen=None,bruin_k=None):
    P=reduceer2.pixlabels(a,bruin=bruin); Pb=reduceer2.pixlabels(a)   # Pb: ook bruine modellijnen als lijn
    L=ontspikkel(a.astype(float)@[0.299,0.587,0.114])
    gr=grenzen or kleur.ZAND
    fx,fy=fase; H=(a.shape[0]-fy)//3; W=(a.shape[1]-fx)//3; lab=np.zeros((H,W),int)
    for j in range(H):
        for i in range(W):
            sl=(slice(fy+3*j,fy+3*j+3),slice(fx+3*i,fx+3*i+3)); b=P[sl].ravel(); l=L[sl].ravel()
            if (b!=0).sum()<5: continue
            k=kz if (kzone is not None and kzone[sl].sum()>=5) else lijn_k
            if (b==1).sum()>=k: lab[j,i]=1; continue
            if bruin_k and (Pb[sl].ravel()==1).sum()>=bruin_k: lab[j,i]=1; continue
            r=b[b>=10]
            if len(r)==0: lab[j,i]=1; continue
            mats=r//10; m=np.bincount(mats).argmax()
            if m!=1:   # glas en hout: meest voorkomende band (zoals r1)
                rr=r[mats==m]; vv,cc=np.unique(rr,return_counts=True); lab[j,i]=vv[cc==cc.max()].min(); continue
            sel=(b//10==m)&(b>=10)
            v=l[sel].mean() if maat=='gem' else np.percentile(l[sel],50 if maat=='med' else 15)
            if m==1: lab[j,i]=10+max(1,int(np.searchsorted(gr,v)))
            elif m==2: lab[j,i]=20+int(np.searchsorted(kleur.GLAS,v))
            else: lab[j,i]=30+int(np.searchsorted(kleur.HOUT,v))
    return lab
