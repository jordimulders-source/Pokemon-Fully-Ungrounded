# r4: ronde bollen naar een gemeten pixelcirkel + delen verschuiven. Geen neveneffecten bij import.
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np; from scipy import ndimage; import gemeen as g, kaal as kl
D=g.D
a,deel,dot=g.natief(); C=kl.C
R3=np.load(os.path.join(D,'r3.npy')); DL3=np.load(os.path.join(D,'r3_deel.npy'))
def cirkelfit_model(k):
    """kleinste-kwadratencirkel op de modelomtrek van deel k (natieve randpixels die aan de achtergrond grenzen)."""
    m=deel==k; e=m&ndimage.binary_dilation(deel<0,np.ones((3,3)))
    yy,xx=np.where(e); xx=xx+0.5; yy=yy+0.5
    A=np.c_[2*xx,2*yy,np.ones(len(xx))]; cx,cy,c=np.linalg.lstsq(A,xx**2+yy**2,rcond=None)[0]; r=np.sqrt(c+cx**2+cy**2)
    return cx,cy,r
def sprite_cirkel(k):
    cx,cy,r=cirkelfit_model(k)
    sx=kl.OX+(cx-kl.X0)*kl.s; sy=kl.OY+(cy-kl.Y0)*kl.s; sr=r*kl.s
    Dm=int(round(2*sr))
    # middelpunt op het raster: even diameter -> op een pixelhoek, oneven -> op een pixelmidden (symmetrische cirkel)
    snap=(lambda v: round(v)) if Dm%2==0 else (lambda v: np.floor(v)+0.5)
    return snap(sx),snap(sy),Dm/2,(sx,sy,sr)
def cirkelmasker(cx,cy,r):
    Y,X=np.mgrid[0:64,0:64]
    return np.hypot(X+0.5-cx,Y+0.5-cy)<=r
WT=kl.WT
def modelkleur(k,x,y):
    sub=(np.arange(8)+0.5)/8
    xs=np.clip((kl.X0+(x-kl.OX+sub)/kl.s).astype(int),0,deel.shape[1]-1); ys=np.clip((kl.Y0+(y-kl.OY+sub)/kl.s).astype(int),0,deel.shape[0]-1)
    dd=deel[ys[:,None],xs[None,:]].ravel(); cc=C[ys[:,None],xs[None,:]].ravel()
    m=(dd==k)&~np.isin(cc,[1,8])
    if not m.any(): return 0
    return int((np.bincount(cc[m],minlength=16)*WT).argmax())
def rondmaken(s,DL,k,cx,cy,r):
    """deel k (in r3-coordinaten) naar de cirkel (cx,cy,r): binnenwerk r3 waar het al binnenwerk was, anders uit de
    modelcel; daarna de buitenlijn op de nieuwe rand (normaal vanuit het middelpunt: schaduwkant zwart, lichtkant selout)."""
    oud=(DL==k)&(s>0)
    q=np.pad(oud,1); oudrand=oud&~(q[:-2,1:-1]&q[2:,1:-1]&q[1:-1,:-2]&q[1:-1,2:])
    nieuw=cirkelmasker(cx,cy,r)
    out=np.zeros_like(s); 
    for y,x in zip(*np.where(nieuw)):
        if oud[y,x] and not oudrand[y,x]: out[y,x]=s[y,x]
        else:
            c=modelkleur(k,x,y)
            out[y,x]=c
    # gaten (geen modelkleur): meest voorkomende buurkleur binnen het deel
    for _ in range(3):
        for y,x in zip(*np.where(nieuw&(out==0))):
            b=[out[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if 0<=yy<64 and 0<=xx<64 and nieuw[yy,xx] and out[yy,xx]>0]
            if b: out[y,x]=max(set(b),key=b.count)
    q=np.pad(nieuw,1); rand=nieuw&~(q[:-2,1:-1]&q[2:,1:-1]&q[1:-1,:-2]&q[1:-1,2:])
    Y,X=np.mgrid[0:64,0:64]; nx=X+0.5-cx; ny=Y+0.5-cy
    sch=(0.6*nx+0.8*ny)>0.05*np.hypot(nx,ny)
    sel=g.SELOUT[g.NAMEN[k]]
    out[rand&sch]=1; out[rand&~sch]=sel
    # zwart dat binnen het deel ligt (oude buitenlijn) -> selout
    out[nieuw&~rand&(out==1)]=sel
    return out,nieuw
def deel_beeld(s,DL,k):
    m=(DL==k)&(s>0); o=np.zeros_like(s); o[m]=s[m]; return o,m
def schuif(img,m,dx,dy):
    o=np.zeros_like(img); mm=np.zeros_like(m)
    ys,xs=np.where(m); ys2=ys+dy; xs2=xs+dx
    assert xs2.min()>=0 and xs2.max()<64 and ys2.min()>=0 and ys2.max()<64,(dx,dy)
    o[ys2,xs2]=img[ys,xs]; mm[ys2,xs2]=True; return o,mm
def samen(delen):
    s=np.zeros((64,64),int); DL=np.full((64,64),-1)
    for k,(img,m) in delen.items():
        assert not (m&(DL>=0)).any(),('overlap',k)
        s[m]=img[m]; DL[m]=k
    return s,DL
def tussenruimtes(DL):
    pts={k:np.argwhere(DL==k) for k in range(7)}; res=[]
    for i in range(7):
        for j in range(i+1,7):
            d=np.abs(pts[i][:,None,:]-pts[j][None,:,:]).max(2).min()-1; res.append((d,g.NAMEN[i],g.NAMEN[j]))
    return sorted(res)
