# Saturnus (bol + ringband) als functie, zelfde opbouw als r3 (sprite/r3/bouw.py stap 1), met bolmaat en ruimte als
# parameters. Ook de ijsplaneet op een gekozen maat (uit het model geschaald). Geen neveneffecten bij import.
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from scipy import ndimage; import gemeen as g, kaal as kl, saturnus as sa
a,deel,dot=g.natief(); C=kl.C
(CX,CY,RN),(CE,ANG,AMAJ,BMIN),_=sa.meet()
A2=(AMAJ-1.75)*kl.s; B2=BMIN*kl.s
def maak(scx,scy,sr,xmin,xmax,ymin=0,ymax=63,Avast=None):
    ang=ANG
    def xbereik(A,B): return np.sqrt((A*np.cos(ang))**2+(B*np.sin(ang))**2)
    A=A2
    ruimte=min(scx-xmin+0.5,xmax+0.5-scx)
    while xbereik(A+0.01,(A+0.01)*B2/A2)+0.95<ruimte-1.0: A+=0.01      # -1: plaats voor de ringrand buiten de band
    if Avast is not None: A=Avast
    B=A*B2/A2; rcx,rcy=scx,scy
    n=np.zeros((64,64),int)
    Y,X=np.mgrid[0:64,0:64]
    bol=np.hypot(X+0.5-scx,Y+0.5-scy)<=sr
    T=np.linspace(0,2*np.pi,4000,endpoint=False)
    PX=rcx+A*np.cos(T)*np.cos(ang)-B*np.sin(T)*np.sin(ang); PY=rcy+A*np.cos(T)*np.sin(ang)+B*np.sin(T)*np.cos(ang)
    dmin=np.full((64,64),9.0); voorz=np.zeros((64,64),bool)
    for y in range(max(0,int(scy)-14),min(64,int(scy)+14)):
        for x in range(max(0,xmin-2),min(64,xmax+3)):
            d=np.hypot(PX-(x+0.5),PY-(y+0.5)); i=d.argmin(); dmin[y,x]=d[i]; voorz[y,x]=np.sin(T[i])>0
    band=dmin<=0.95
    U=(X+0.5-rcx)*np.cos(ang)+(Y+0.5-rcy)*np.sin(ang); W=-(X+0.5-rcx)*np.sin(ang)+(Y+0.5-rcy)*np.cos(ang)
    f=RN/sr
    for y,x in zip(*np.where(bol)):
        sub=(np.arange(8)+0.5)/8
        xs=np.clip((CX+(x+sub-scx)*f).astype(int),0,deel.shape[1]-1); ys=np.clip((CY+(y+sub-scy)*f).astype(int),0,deel.shape[0]-1)
        yy,xx=np.meshgrid(ys,xs,indexing='ij'); yy=yy.ravel(); xx=xx.ravel()
        cc=C[yy,xx]; m=(deel[yy,xx]==2)&np.isin(cc,[2,3,4,5])
        n[y,x]=np.bincount(cc[m],minlength=16).argmax() if m.any() else -5
    for y,x in zip(*np.where(n==-5)):
        b=[n[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if n[yy,xx] in (2,3,4,5)]
        n[y,x]=max(set(b),key=b.count) if b else 4
    q=np.pad(bol,1); bb=bol&~(q[:-2,1:-1]&q[2:,1:-1]&q[1:-1,:-2]&q[1:-1,2:])
    nx=X+0.5-scx; ny=Y+0.5-scy; sch=(0.6*nx+0.8*ny)>0.05*np.hypot(nx,ny)
    n[bb&sch]=1; n[bb&~sch]=2
    zicht=band&(voorz|~bol)
    grijs=zicht&(dmin<0.5)
    lab,k=ndimage.label(grijs,np.ones((3,3)))
    while k>1:
        best=None
        for y,x in zip(*np.where(zicht&~grijs)):
            nbl=set(lab[max(0,y-1):y+2,max(0,x-1):x+2].ravel())-{0}
            if len(nbl)>=2 and (best is None or dmin[y,x]<best[0]): best=(dmin[y,x],y,x)
        if best is None: break
        grijs[best[1],best[2]]=True; lab,k=ndimage.label(grijs,np.ones((3,3)))
    for y,x in zip(*np.where(grijs)):
        for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)):
            if not (0<=xx<64 and 0<=yy<64): grijs[y,x]=False; continue
            if zicht[yy,xx] or bol[yy,xx]: continue
            if (U[yy,xx]/A)**2+(W[yy,xx]/B)**2<1: continue
            if xmin<=xx<=xmax and ymin<=yy<=ymax: zicht[yy,xx]=True
            else: grijs[y,x]=False
    rand=zicht&~grijs
    n[grijs]=13
    gnx=U*np.cos(ang)/A**2-W*np.sin(ang)/B**2; gny=U*np.sin(ang)/A**2+W*np.cos(ang)/B**2
    buiten=(U/A)**2+(W/B)**2>1
    for y,x in zip(*np.where(rand)):
        tegen_bg=any((not(0<=xx<64)) or not(bol[yy,xx] or zicht[yy,xx]) for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)))
        sgn=1 if buiten[y,x] else -1
        n[y,x]=1 if (tegen_bg and sgn*(0.6*gnx[y,x]+0.8*gny[y,x])>0) else 6
    M=n>0
    for y,x in zip(*np.where(n==1)):
        e=lambda yy,xx: not(0<=xx<64) or n[yy,xx]==0
        if (e(y,x-1) or e(y-1,x)) and not (e(y,x+1) or e(y+1,x)): n[y,x]=6
    return n,M,(A,B)
def ijs(cx,cy,r,rond):
    """ijsplaneet op straal r: modelijs geschaald (cirkelfit natief), per pixel modelhelderheid: L<208 cyaan (8), anders
    bijna-wit (9) (regel van r2), dan buitenlijn: lichtkant grijsleisteen 13, schaduwkant zwart."""
    ncx,ncy,nr=rond.cirkelfit_model(1)
    L=(a*[0.3,0.59,0.11]).sum(2)
    m=rond.cirkelmasker(cx,cy,r); n=np.zeros((64,64),int); f=nr/r
    for y,x in zip(*np.where(m)):
        sub=(np.arange(8)+0.5)/8
        xs=np.clip((ncx+(x+sub-cx)*f).astype(int),0,deel.shape[1]-1); ys=np.clip((ncy+(y+sub-cy)*f).astype(int),0,deel.shape[0]-1)
        yy,xx=np.meshgrid(ys,xs,indexing='ij'); mm=deel[yy,xx]==1
        n[y,x]=8 if (mm.any() and L[yy,xx][mm].mean()<208) else 9
    q=np.pad(m,1); rand=m&~(q[:-2,1:-1]&q[2:,1:-1]&q[1:-1,:-2]&q[1:-1,2:])
    Y,X=np.mgrid[0:64,0:64]; nx=X+0.5-cx; ny=Y+0.5-cy; sch=(0.6*nx+0.8*ny)>0.05*np.hypot(nx,ny)
    n[rand&sch]=1; n[rand&~sch]=13
    return n,m
