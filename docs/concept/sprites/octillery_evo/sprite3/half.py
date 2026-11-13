# natief.png (127x115) -> palet (K kleuren) -> 2x2-reductie met regels -> onderlaag 64x64
import sys; from PIL import Image; import numpy as np
K=int(sys.argv[1]) if len(sys.argv)>1 else 14; DARKMIN=int(sys.argv[2]) if len(sys.argv)>2 else 2
IN=sys.argv[3] if len(sys.argv)>3 else 'sprite3/natief.png'; TAG=sys.argv[4] if len(sys.argv)>4 else 'half'
im=Image.open(IN).convert('RGB'); a=np.asarray(im).astype(int)
bgm=(a.min(axis=2)>=215)
g=a[~bgm]
rng=np.random.default_rng(1); C=g[rng.choice(len(g),K,replace=False)].astype(float)
for _ in range(40):
    d=((g[:,None,:]-C[None])**2).sum(2); l=d.argmin(1)
    for k in range(K):
        if (l==k).any(): C[k]=g[l==k].mean(0)
C=C.round().astype(int); lum=C@np.array([.299,.587,.114]); order=np.argsort(lum); C=C[order]; lum=lum[order]
d=((a[:,:,None,:]-C[None,None])**2).sum(3); L=d.argmin(2)+1; L[bgm]=0
H,W=L.shape; best=None
isdark=np.concatenate([[False],lum<60]); isyel=np.concatenate([[False],(C[:,0]>180)&(C[:,1]>140)&(C[:,2]<140)])
def red(oy,ox):
    h=(H-oy)//2; w=(W-ox)//2; o=np.zeros((h,w),int)
    for j in range(h):
        for i in range(w):
            b=L[oy+2*j:oy+2*j+2,ox+2*i:ox+2*i+2].ravel()
            nb=(b==0).sum()
            if nb>=3: o[j,i]=0; continue
            b=b[b>0]
            if isdark[b].sum()>=DARKMIN: o[j,i]=b[isdark[b]][0] if True else 0; o[j,i]=np.bincount(b[isdark[b]]).argmax(); continue
            if isyel[b].sum()>=2: o[j,i]=np.bincount(b[isyel[b]]).argmax(); continue
            o[j,i]=np.bincount(b).argmax()
    return o
for oy in (0,1):
    for ox in (0,1):
        o=red(oy,ox)
        ys,xs=np.where(o>0); o2=o[ys.min():ys.max()+1,xs.min():xs.max()+1]
        full=np.zeros((64,64),int); h,w=o2.shape; x0=(64-w)//2; full[63-h:63,x0:x0+w]=o2
        pal=[255,0,255]+[int(v) for c in C for v in c]; pal+= [0]*(768-len(pal))
        p=Image.fromarray(full.astype('uint8'),'P'); p.putpalette(pal); p.save(f'sprite3/{TAG}_{oy}{ox}.png',transparency=0)
        print(oy,ox,w,h,(o2>0).sum())
print(C.tolist())
