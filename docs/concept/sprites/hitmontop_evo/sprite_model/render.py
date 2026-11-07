# Sprite ronde 1, stap a: de render van model v3 met precies dezelfde vervormingen als silhouet D
# (kop/handen/voeten groter, benen korter, romp gedrongener), als RGB-laag; daarna 64x64.
import sys, os, numpy as np
sys.path.insert(0,'../silhouet_v3'); os.chdir('../silhouet_v3')
import silhouet as S1, stap2 as S2
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from scipy import ndimage as nd
xx,yy=S2.xx,S2.yy; H,W=S1.M.shape
RGB=np.asarray(S1.SRC0).astype(float)

def warp(L,fx,fy):  # L = (mask, rgb)
    m=nd.map_coordinates(L[0].astype(float),[fy,fx],order=1)>0.5
    c=np.stack([nd.map_coordinates(L[1][...,i],[fy,fx],order=0) for i in range(3)],-1)
    return m,c
def over(dst,src):  # src bovenop dst
    m=dst[0]|src[0]; c=np.where(src[0][...,None],src[1],dst[1]); return m,c
def mask(L,sel): return L[0]&sel, L[1]
def schaal(L,c,s): return warp(L,c[0]+(xx-c[0])/s,c[1]+(yy-c[1])/s)
def schuif(L,v): return warp(L,xx-v[0],yy-v[1])

def been(L,heup,enkel,voet,k):
    heup=np.array(heup,float); enkel=np.array(enkel,float)
    Ln=np.linalg.norm(enkel-heup); u=(enkel-heup)/Ln
    t=(xx-heup[0])*u[0]+(yy-heup[1])*u[1]; p=np.abs(-(xx-heup[0])*u[1]+(yy-heup[1])*u[0])
    t0=0.35*Ln
    zone=L[0]&(t>t0)&(p<95)&~voet[0]
    ts=np.where(t<t0,t,np.where(t<Ln-k,t0+(t-t0)*(Ln-t0)/(Ln-k-t0),t+k)); d=ts-t
    nw=warp((zone,L[1]),xx+d*u[0],yy+d*u[1]); nw=(nw[0]&(t>t0-2),nw[1])
    rest=(L[0]&~zone&~voet[0],L[1])
    return over(rest,nw), schuif(voet,-k*u), -k*u

def bewerk(L):
    M=L[0]; blue=S2.blue
    Lv=mask(L,nd.binary_dilation(blue&(xx<200)&(yy<200),iterations=30)&(xx<175)&(yy<200))
    Rv=mask(L,nd.binary_dilation(blue&(xx>580)&(yy<230),iterations=30)&(yy<215)&(xx>595))
    L,Lv,dl=been(L,(490,335),(145,130),Lv,S2.BEEN*480)
    L,Rv,dr=been(L,(585,355),(668,182),Rv,S2.BEEN*330)
    L=over(L,schaal(Lv,np.array([90,110])+dl,S2.VOET)); L=over(L,schaal(Rv,np.array([662,128])+dr,S2.VOET))
    L=over(L,schaal(mask(L,S2.schijf((440,961),44)),(440,997),S2.HAND))
    L=over(L,schaal(mask(L,S2.schijf((652,332),44)),(652,332),S2.HAND))
    kop=L[0]&(((xx<395)&(yy>540))|S2.schijf((265,635),125))&(yy<760)
    L=over(L,schaal((kop,L[1]),(385,610),S2.KOP))
    return L

def inkorten(L,k):
    sh=np.array([440.,640.]); hp=np.array([540.,370.]); u=(hp-sh)/np.linalg.norm(hp-sh)
    t=(xx-sh[0])*u[0]+(yy-sh[1])*u[1]; tc=100
    up=schuif(mask(L,t>=tc),-k*u); lo=mask(L,t<tc+k)
    r=over(lo,up); return over(r,mask(lo,t<tc))

L=inkorten(bewerk((S1.M,RGB)),45)
M,C=L
ys,xs=np.nonzero(M); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
s=63/(y1-y0+1); ox=(64-(x1-x0+1)*s)/2; oy=63-(y1-y0+1)*s
gx=((xs-x0)*s+ox).astype(int); gy=((ys-y0)*s+oy).astype(int)
cnt=np.zeros((64,64)); acc=np.zeros((64,64,3))
np.add.at(cnt,(gy,gx),1); np.add.at(acc,(gy,gx),C[ys,xs])
fig=S1.los(cnt*s*s>=0.5)
col=acc/np.maximum(cnt,1)[...,None]
np.save('render64.npy',np.dstack([col,fig[...,None]]))
np.save('render64.npy',np.dstack([col,fig[...,None]]))  # tussenbestand (niet in git)
out=np.where(fig[...,None],col,255).astype('uint8')
Image.fromarray(out).save('render64.png'); Image.fromarray(out).resize((512,512),Image.NEAREST).save('render64_8x.png')
# vergelijk met silhouet D
D=np.array([[c=='#' for c in r] for r in open('../silhouet_v3/silhouet_D.txt').read().split()])
print('verschil met D:',int((D!=fig).sum()),'px')
