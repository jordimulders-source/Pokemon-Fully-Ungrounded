# natief (201x201, figuur 175x101) -> exacte 3x3-reductie met regels (afgeleid van pitahaya_draak/sprite_r1/half3.py).
# Niets getekend: elke spritepixel komt uit zijn eigen 3x3 modelpixels; kleuren zijn echte modelkleuren.
# Gebruik: python3 half3.py UIT.png oy ox ZT PT
import sys; from PIL import Image; import numpy as np
from groepen import laad, tonen
UIT=sys.argv[1]; OY=int(sys.argv[2]); OX=int(sys.argv[3]); ZT=int(sys.argv[4]); PT=int(sys.argv[5])
ONDER=62; N=3
a,lum,g=laad(); H,W=g.shape
T2=tonen(a,lum,g,2,5); T2=np.array([c for c in T2 if not (c[1]>90 and c[0]<200)])   # gemengde roze/groen-randtint eruit
T={2:T2,4:tonen(a,lum,g,4,4),6:tonen(a,lum,g,6,2)}
ZW=np.median(a[g==1],0).astype(int)
# index: 1 zwart | 2-5 roze (donker->licht) | 6-9 groen | 10-11 wit (vruchtvlees grijs, licht) | 12 pit
BASE={2:2,4:6,6:10}
PIT=np.median(a[g==7],0).astype(int)
PAL=[(255,0,255),tuple(ZW)]+[tuple(c) for k in (2,4,6) for c in T[k]]+[tuple(PIT)]
tn=np.zeros_like(g)
for k,c in T.items():
    m=g==k; tn[m]=((a[m][:,None,:]-c[None])**2).sum(2).argmin(1)
h=(H-OY)//N; w=(W-OX)//N; o=np.zeros((h,w),int)
nbk=np.zeros((h,w),int); nzw=np.zeros((h,w),int); npit=np.zeros((h,w),int)
for j in range(h):
    for i in range(w):
        sl=(slice(OY+N*j,OY+N*j+N),slice(OX+N*i,OX+N*i+N)); gb=g[sl]
        nbk[j,i]=(gb==0).sum(); nzw[j,i]=(gb==1).sum(); npit[j,i]=(gb==7).sum()
        if nbk[j,i]>=5: continue
        if nzw[j,i]>=ZT: o[j,i]=1; continue                       # lijn: donkerste wint
        if npit[j,i]>=PT: o[j,i]=12; continue                     # pitje
        cnt={k:(gb==k).sum() for k in (2,4,6)}
        if cnt[6]>=4 or (cnt[6]>=2 and npit[j,i]>=1):               # vruchtvlees/tand/oogwit (pit telt als vlees)
            c=a[sl][(gb==6)].mean(0); o[j,i]=10+((T[6]-c)**2).sum(1).argmin(); continue
        k=max(cnt,key=cnt.get)
        if cnt[k]==0: o[j,i]=1; continue
        c=a[sl][gb==k].mean(0); o[j,i]=BASE[k]+((T[k]-c)**2).sum(1).argmin()
ys,xs=np.where(o>0); o2=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; hh,ww=o2.shape
full=np.zeros((64,64),int); x0=(64-ww)//2; y0=ONDER+1-hh; full[y0:y0+hh,x0:x0+ww]=o2
def plaats(x): f=np.zeros((64,64),int); f[y0:y0+hh,x0:x0+ww]=x[ys.min():ys.max()+1,xs.min():xs.max()+1]; return f
np.savez(UIT[:-4]+'_info.npz',nzw=plaats(nzw),nbk=plaats(nbk),npit=plaats(npit),geo=np.array([OY,OX,ys.min(),xs.min(),y0,x0]))
p=Image.fromarray(full.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL))); p.save(UIT,transparency=0)
tot=(full>0).sum(); print(UIT,'maat',ww,hh,'px',tot,'zwart %.1f%%'%(100*(full==1).sum()/tot),'pit',(full==12).sum(),'kleuren',len(set(full.ravel()))-1,'pos x',x0,'y',y0)
