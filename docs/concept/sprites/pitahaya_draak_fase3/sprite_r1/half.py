# natief (255x255, figuur 227x184) -> reductie met factor S (niet-geheel, ±3,66) naar ±62 px breed.
# Niets getekend: elke spritepixel komt uit zijn eigen venster natieve modelpixels (oppervlak-gewogen via 4x supersampling);
# kleuren zijn echte modeltonen. Regels (fase 2 half3.py, aangepast aan fracties):
#   achtergrond bij >= BG van het venster; lijn bij >= ZT zwart (donkerste wint); tong bij >= TT geel; pit bij >= PT;
#   vlees bij >= VT wit; anders meerderheid roze/groen -> gemiddelde -> dichtstbijzijnde modeltoon.
# Gebruik: python3 half.py UIT.png [--nat natief.png] [--w 62] [--ox 0] [--oy 0] [--zt .2] [--tt .3] [--pt .12] [--vt .35] [--bg .5]
import sys; from PIL import Image; import numpy as np
from groepen import laad
def arg(k,d,t=float): return t(sys.argv[sys.argv.index(k)+1]) if k in sys.argv else d
UIT=sys.argv[1]; NAT=arg('--nat','natief.png',str); WB=arg('--w',62,int)
OX=arg('--ox',0.); OY=arg('--oy',0.); ZT=arg('--zt',.2); TT=arg('--tt',.3); PT=arg('--pt',.12); VT=arg('--vt',.35); BG=arg('--bg',.5); GT=arg('--gt',.3)
ONDER=62; U=4
a,lum,g=laad(NAT); H,W=g.shape
# tonen: vast gekozen modeltonen (k-means op het model, zie NOTITIES)
T={2:np.array([(112,41,58),(185,44,96),(229,76,130),(238,105,150)]),
   4:np.array([(48,80,35),(74,109,62),(104,142,83),(133,169,106)]),
   6:np.array([(188,189,193),(242,241,246)]),
   8:np.array([(122,100,25),(203,175,83),(250,222,143)])}
ZW=(8,11,3); PIT=(79,69,76)
# index: 1 zwart | 2-5 roze | 6-9 groen | 10-11 wit | 12-14 geel | 15 pit/donkergrijs
BASE={2:2,4:6,6:10,8:12}
PAL=[(255,0,255),ZW]+[tuple(c) for k in (2,4,6,8) for c in T[k]]+[PIT]
REF=arg('--ref',None,str)
if REF: _,_,gr=laad(REF); ys,xs=np.where(gr>0)
else: ys,xs=np.where(g>0)
bx0,bx1,by0,by1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
S=(bx1-bx0)/WB
gu=np.repeat(np.repeat(g,U,0),U,1); au=np.repeat(np.repeat(a,U,0),U,1)
w=int(np.ceil((bx1-bx0)/S))+2; h=int(np.ceil((by1-by0)/S))+2
o=np.zeros((h,w),int); F={k:np.zeros((h,w)) for k in (0,1,2,4,6,7,8)}
for j in range(h):
    for i in range(w):
        y0=int(round(U*(by0-S+OY+S*j))); y1=int(round(U*(by0-S+OY+S*(j+1))))
        x0=int(round(U*(bx0-S+OX+S*i))); x1=int(round(U*(bx0-S+OX+S*(i+1))))
        y0,x0=max(y0,0),max(x0,0); y1,x1=min(y1,H*U),min(x1,W*U)
        gb=gu[y0:y1,x0:x1]; n=gb.size
        for k in F: F[k][j,i]=(gb==k).sum()/n
        if F[0][j,i]>=BG and not (F[4][j,i]>=GT and F[0][j,i]<0.75): continue   # dunne groene stekelpunten winnen bij >= GT groen
        if F[1][j,i]>=ZT: o[j,i]=1; continue
        if F[8][j,i]>=TT:
            c=au[y0:y1,x0:x1][gb==8].mean(0); o[j,i]=12+((T[8]-c)**2).sum(1).argmin(); continue
        if F[7][j,i]>=PT: o[j,i]=15; continue
        if F[6][j,i]>=VT:
            c=au[y0:y1,x0:x1][gb==6].mean(0); o[j,i]=10+((T[6]-c)**2).sum(1).argmin(); continue
        cnt={k:F[k][j,i] for k in (2,4,6,8)}; k=max(cnt,key=cnt.get)
        if F[0][j,i]>=BG: k=4
        if cnt[k]==0: o[j,i]=1; continue
        c=au[y0:y1,x0:x1][gb==k].mean(0); o[j,i]=BASE[k]+((T[k]-c)**2).sum(1).argmin()
yy,xx=np.where(o>0)
PL=arg('--plaats',None,str)
if PL:   # vaste plaatsing (ymin,xmin,Y0,X0) van de hoofdversie
    ym,xm,Y0,X0=[int(v) for v in PL.split(',')]
    yy=np.array([ym,yy.max()]); xx=np.array([xm,xx.max()])
o2=o[yy.min():yy.max()+1,xx.min():xx.max()+1]; hh,ww=o2.shape
if not PL: X0=(64-ww)//2; Y0=ONDER+1-hh
full=np.zeros((64,64),int); full[Y0:Y0+hh,X0:X0+ww]=o2[:64-Y0,:64-X0]
def plaats(v): f=np.zeros((64,64)); f[Y0:Y0+hh,X0:X0+ww]=v[yy.min():yy.max()+1,xx.min():xx.max()+1]; return f
np.savez(UIT[:-4]+'_info.npz',**{'f%d'%k:plaats(F[k]) for k in F},geo=np.array([S,OX,OY,bx0,by0,yy.min(),xx.min(),Y0,X0,U]))
p=Image.fromarray(full.astype('uint8'),'P'); p.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL))); p.save(UIT,transparency=0)
tot=(full>0).sum(); print(UIT,'S %.3f'%S,'maat',ww,hh,'px',tot,'zwart %.1f%%'%(100*(full==1).sum()/tot),'tong',((full>=12)&(full<=14)).sum(),'pit',(full==15).sum(),'pos x',X0,'y',Y0)
