# lijnkaart.py : aandeel modellijn-pixels (zwart/bruinlijn/donkerlijn) per spritepixel (exacte voetafdruk), opgeslagen als lijnfrac.npy
import numpy as np,sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
from PIL import Image
a=np.asarray(Image.open('model/r10_k8.png').convert('RGB')).astype(float); fig=np.load('sprite_r1/masker.npy'); c=np.load('sprite_r1/km.npy')
yy,xx=np.where(fig); x0,y0=xx.min(),yy.min(); x1,y1=xx.max()+1,yy.max()+1
crop=a[y0:y1,x0:x1]; m=fig[y0:y1,x0:x1].astype(float)
lab=np.argmin(((crop[...,None,:]-c[None,None])**2).sum(-1),-1)
pk=np.vectorize(lambda k:KM2P[k])(lab)
H0,W0=m.shape; s=64/W0; W,H=64,round(H0*s); oy=64-H
def wmat(N0,N):
    M=np.zeros((N,N0)); e=N0/N
    for i in range(N):
        lo,hi=i*e,(i+1)*e
        for j in range(int(lo),min(N0,int(np.ceil(hi)))): M[i,j]=max(0,min(hi,j+1)-max(lo,j))
    return M
Wy,Wx=wmat(H0,H),wmat(W0,W)
lijn=np.isin(pk,(1,2))*m
F=Wy@lijn@Wx.T/(Wy@np.ones_like(m)@Wx.T)
out=np.zeros((64,64)); out[oy:]=F; np.save('sprite_r1/lijnfrac.npy',out)
zw=(pk==1)*m; Z=Wy@zw@Wx.T/(Wy@np.ones_like(m)@Wx.T); o2=np.zeros((64,64)); o2[oy:]=Z; np.save('sprite_r1/zwartfrac.npy',o2)
