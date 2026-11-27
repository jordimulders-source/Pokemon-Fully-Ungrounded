# Materiaalkaart per natieve pixel: 0 achtergrond, 1 zwart, 2 zand, 3 glas/boei, 4 hout, 5 oogwit
import numpy as np; from PIL import Image
def hsv(a):
    a=a/255.0; mx=a.max(-1); mn=a.min(-1); d=mx-mn+1e-9
    r,g,b=a[...,0],a[...,1],a[...,2]
    h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))*60
    s=np.where(mx>0,d/(mx+1e-9),0); return h,s,mx
def achtergrond(a):
    wit=(a.min(-1)>228)&((a.max(-1)-a.min(-1))<20)
    H,W=wit.shape; m=np.zeros_like(wit); st=[(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)]
    while st:
        y,x=st.pop()
        if 0<=y<H and 0<=x<W and wit[y,x] and not m[y,x]:
            m[y,x]=1; st+= [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]
    return m
def kaart(a, houtregio=None, ogen=None):
    a=a.astype(float); h,s,v=hsv(a); lum=a@[0.299,0.587,0.114]
    M=np.full(a.shape[:2],2,int)
    glas=(s<0.28)|((h>150)&(h<260))
    M[glas]=3
    if houtregio is not None:
        hout=houtregio&(h<32)&(s>0.35)&(lum<150)
        M[hout]=4
    M[lum<55]=1
    if ogen is not None: M[ogen&(lum>170)&(s<0.25)]=5
    M[achtergrond(a.astype(int))==1]=0
    return M,lum
