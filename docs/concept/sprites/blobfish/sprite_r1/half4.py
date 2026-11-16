# natief (255x163, vis 203x118) -> exacte 4x4-reductie met regels (afgeleid van octillery_evo/sprite3/half2.py).
# Niets wordt getekend: elke spritepixel komt uit zijn 4x4-blok modelpixels; kleuren zijn echte modelkleuren.
# Gebruik: python3 half4.py UIT.png [oy ox]   -> ook UIT_info.npz (per blok: tellingen) voor metingen
import sys; from PIL import Image; import numpy as np
UIT=sys.argv[1]; OY=int(sys.argv[2]) if len(sys.argv)>2 else 0; OX=int(sys.argv[3]) if len(sys.argv)>3 else 0
ONDER=54                                   # bodemlijn: onderste spriterij (zie NOTITIES.md)
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int); H,W=a.shape[:2]
R,G,B=a[...,0],a[...,1],a[...,2]; lum=0.299*R+0.587*G+0.114*B
bg0=a.min(2)>=215
# achtergrond = bijna-wit dat met de beeldrand verbonden is; wit binnen de vis (glanspunten) is modelkleur
from collections import deque
bg=np.zeros_like(bg0); q=deque((y,x) for y in range(H) for x in (0,W-1) if bg0[y,x]); 
for y,x in q: bg[y,x]=1
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<H and 0<=xx<W and bg0[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
sat=(a.max(2)-a.min(2))/np.maximum(a.max(2),1)
oogwit=(~bg)&(lum>=170)&(sat<0.25)         # wit van de ogen (en het allerlichtste glanspunt)
drk=(~bg)&(lum<62)                          # lijnen, oogpupil
blk=(~bg)&(lum<38)
vul=(~bg)&~drk&~oogwit
# palet: 9 vultonen = k-means op de natieve vulpixels, elk centrum op de dichtstbijzijnde echte modelkleur
px=a[vul].astype(float); l2=px@[0.299,0.587,0.114]; K=9
cen=np.array([px[np.argsort(l2)[int(q*(len(px)-1))]] for q in np.linspace(0.02,0.98,K)])
for _ in range(60):
    lab=((px[:,None]-cen[None])**2).sum(2).argmin(1)
    cen=np.array([px[lab==k].mean(0) if (lab==k).any() else cen[k] for k in range(K)])
uq=np.unique(a[vul],axis=0); cen=np.array([uq[((uq-c)**2).sum(1).argmin()] for c in cen]); cen=cen[np.argsort(cen@[0.299,0.587,0.114])]
def med(m): return np.median(a[m],axis=0).astype(int)
ZW=med(blk); LR=med(drk&~blk); WI=med(oogwit)
# index: 1 zwart, 2 lijnrood, 3..11 vultonen (donker->licht), 12 oogwit
PAL=[(255,0,255),tuple(ZW),tuple(LR)]+[tuple(c) for c in cen]+[tuple(WI)]
h=(H-OY)//4; w=(W-OX)//4; o=np.zeros((h,w),int)
nd=np.zeros((h,w),int); nw=np.zeros((h,w),int); nb=np.zeros((h,w),int)
for j in range(h):
    for i in range(w):
        sl=(slice(OY+4*j,OY+4*j+4),slice(OX+4*i,OX+4*i+4))
        nb[j,i]=bg[sl].sum(); nd[j,i]=drk[sl].sum(); nw[j,i]=oogwit[sl].sum()
        if nb[j,i]>=8: continue                                   # achtergrond (dekking < 1/2)
        if nw[j,i]>=3: o[j,i]=12; continue                         # oogwit / glanspunt
        if nd[j,i]>=4: o[j,i]=1 if blk[sl].sum()*2>=nd[j,i] else 2; continue   # lijn (>= 1 volle modelrij donker)
        rest=vul[sl]
        if not rest.any(): o[j,i]=2; continue
        c=a[sl][rest].mean(0); o[j,i]=3+((cen-c)**2).sum(1).argmin()
ys,xs=np.where(o>0); o2=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; hh,ww=o2.shape
full=np.zeros((64,64),int); x0=(64-ww)//2; y0=ONDER+1-hh; full[y0:y0+hh,x0:x0+ww]=o2
def plaats(x): f=np.zeros((64,64),int); f[y0:y0+hh,x0:x0+ww]=x[ys.min():ys.max()+1,xs.min():xs.max()+1]; return f
np.savez(UIT[:-4]+'_info.npz',nd=plaats(nd),nw=plaats(nw),nb=plaats(nb),geo=np.array([OY,OX,ys.min(),xs.min(),y0,x0]))
p=Image.fromarray(full.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL))); p.save(UIT,transparency=0)
tot=(full>0).sum(); print(UIT,'maat',ww,hh,'px',tot,'zwart %.1f%% lijnrood %.1f%%'%(100*(full==1).sum()/tot,100*(full==2).sum()/tot),'oogwit',(full==12).sum(),'kleuren',len(set(full.ravel()))-1)
