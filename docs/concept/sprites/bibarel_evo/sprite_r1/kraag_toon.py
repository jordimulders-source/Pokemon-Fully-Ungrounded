# kraag_toon.py: toonkaart van het model (oppervlak-middeling, helderheid) per spritepixel -> toon.npy (geen tekenwerk)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('model/r10_k8.png').convert('RGB')).astype(float); fig=np.load('sprite_r1/masker.npy')
yy,xx=np.where(fig); x0,y0=xx.min(),yy.min(); x1,y1=xx.max()+1,yy.max()+1
crop=a[y0:y1,x0:x1]; m=fig[y0:y1,x0:x1].astype(float); L=(crop@[0.299,0.587,0.114])*m
H0,W0=m.shape; s=64/W0; H=round(H0*s); oy=64-H
def wmat(N0,N):
    M=np.zeros((N,N0)); e=N0/N
    for i in range(N):
        lo,hi=i*e,(i+1)*e
        for j in range(int(lo),min(N0,int(np.ceil(hi)))): M[i,j]=max(0,min(hi,j+1)-max(lo,j))
    return M
Wy,Wx=wmat(H0,H),wmat(W0,64)
T=Wy@L@Wx.T/np.maximum(Wy@m@Wx.T,1e-9); out=np.zeros((64,64)); out[oy:]=T; np.save('sprite_r1/toon.npy',out)
