# natief (199x199, figuur 94x148) -> exacte 3x3-reductie met regels (afgeleid van blobfish/sprite_r1/half4.py
# en de ijskomeet-r15-regel: bij zwarte omlijning en > 2x verkleinen wint in een blok de donkerste pixel).
# Niets wordt getekend: elke spritepixel komt uit zijn eigen 3x3 modelpixels; kleuren zijn echte modelkleuren.
# Gebruik: python3 half3.py UIT.png [oy ox]  -> ook UIT_info.npz (tellingen per blok + geometrie)
import sys; from PIL import Image; import numpy as np
from groepen import laad, tonen
UIT=sys.argv[1]; OY=int(sys.argv[2]) if len(sys.argv)>2 else 0; OX=int(sys.argv[3]) if len(sys.argv)>3 else 0
ONDER=55; N=3; DL=3; ZT=int(sys.argv[5]) if len(sys.argv)>5 else 2; GT=int(sys.argv[6]) if len(sys.argv)>6 else 0; KOPY=110; DLUM=int(sys.argv[4]) if len(sys.argv)>4 else 78
a,lum,g=laad(); H,W=g.shape
T={2:tonen(a,lum,g,2,4),3:tonen(a,lum,g,3,2),4:tonen(a,lum,g,4,4),5:tonen(a,lum,g,5,2)}
ZW=np.median(a[g==1],0).astype(int); WI=np.median(a[g==6],0).astype(int)
# index: 1 zwart | 2-5 roze (donker->licht) | 6-7 kin-mauve | 8-11 groen | 12-13 amber | 14 wit
BASE={2:2,3:6,4:8,5:12}
PAL=[(255,0,255),tuple(ZW)]+[tuple(c) for k in (2,3,4,5) for c in T[k]]+[tuple(WI)]
# toon per modelpixel (dichtstbijzijnde toon binnen zijn groep)
tn=np.zeros_like(g)
for k,c in T.items():
    m=g==k; tn[m]=((a[m][:,None,:]-c[None])**2).sum(2).argmin(1)
h=(H-OY)//N; w=(W-OX)//N; o=np.zeros((h,w),int)
nbk=np.zeros((h,w),int); nzw=np.zeros((h,w),int); regel=np.zeros((h,w),int)
for j in range(h):
    for i in range(w):
        sl=(slice(OY+N*j,OY+N*j+N),slice(OX+N*i,OX+N*i+N)); gb=g[sl]
        nbk[j,i]=(gb==0).sum(); nzw[j,i]=(gb==1).sum()
        if nbk[j,i]>=5: continue                                   # achtergrond (dekking < 1/2)
        kop=(OY+N*j)<KOPY                                          # hoofdzone (modelrijen boven de hals)
        if GT and kop and (gb==4).sum()>=GT and nzw[j,i]<4:       # groene schubpunt in het hoofd: groen boven halve lijn
            c=a[sl][gb==4].mean(0); o[j,i]=8+((T[4]-c)**2).sum(1).argmin(); regel[j,i]=6; continue
        if nzw[j,i]>=ZT: o[j,i]=1; regel[j,i]=1; continue          # lijn: donkerste wint
        if (gb==6).sum()>=2: o[j,i]=14; regel[j,i]=2; continue    # wit (tandje, glans, stekeltjes)
        if (gb==5).sum()>=3:                                      # amber oog
            c=a[sl][gb==5].mean(0); o[j,i]=12+((T[5]-c)**2).sum(1).argmin(); regel[j,i]=3; continue
        cnt={k:(gb==k).sum() for k in (2,3,4,5)}; k=max(cnt,key=cnt.get)
        if cnt[k]==0: o[j,i]=1; regel[j,i]=1; continue
        tb=tn[sl][gb==k]
        lb=lum[sl][gb==k]
        if k==2 and (lb<DLUM).sum()>=2:                          # dunne roze binnenlijn (mond, schubnaden): donkerste pixel wint
            c=a[sl][gb==k][lb.argmin()]; o[j,i]=BASE[k]+((T[k]-c)**2).sum(1).argmin(); regel[j,i]=4; continue
        if k==4 and (tb==0).sum()>=DL: o[j,i]=BASE[k]; regel[j,i]=4; continue   # groene ribbel/donkerste toon (1 modelrij)
        c=a[sl][gb==k].mean(0); o[j,i]=BASE[k]+((T[k]-c)**2).sum(1).argmin(); regel[j,i]=5
ys,xs=np.where(o>0); o2=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; hh,ww=o2.shape
full=np.zeros((64,64),int); x0=(64-ww)//2; y0=ONDER+1-hh; full[y0:y0+hh,x0:x0+ww]=o2
def plaats(x): f=np.zeros((64,64),int); f[y0:y0+hh,x0:x0+ww]=x[ys.min():ys.max()+1,xs.min():xs.max()+1]; return f
np.savez(UIT[:-4]+'_info.npz',nzw=plaats(nzw),nbk=plaats(nbk),regel=plaats(regel),geo=np.array([OY,OX,ys.min(),xs.min(),y0,x0]))
p=Image.fromarray(full.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL))); p.save(UIT,transparency=0)
tot=(full>0).sum(); print(UIT,'maat',ww,hh,'px',tot,'zwart %.1f%%'%(100*(full==1).sum()/tot),'kleuren',len(set(full.ravel()))-1,'pos x',x0,'y',y0)
