import numpy as np
from PIL import Image
MK=np.asarray(Image.open('model/r10_k8.png').convert('RGB')).astype(float)
P=np.array(Image.open('sprite_r12/sprite.png').getpalette()[:48]).reshape(16,3).astype(float)
s_=64/90; mx0,my0,oy=0,9,6
def red(x,y,allowed):
    x0=mx0+x/s_; x1=mx0+(x+1)/s_; y0=my0+(y-oy)/s_; y1=my0+(y+1-oy)/s_
    xs=range(int(np.floor(x0)),int(np.ceil(x1))); ys=range(int(np.floor(y0)),int(np.ceil(y1)))
    px=[];w=[]
    for yy in ys:
        for xx in xs:
            if 0<=xx<99 and 0<=yy<99:
                wx=min(xx+1,x1)-max(xx,x0); wy=min(yy+1,y1)-max(yy,y0)
                if wx>0 and wy>0: px.append(MK[yy,xx]); w.append(wx*wy)
    px=np.array(px); w=np.array(w); lum=px@[0.299,0.587,0.114]
    if lum.min()<75 and (w[lum<75].sum()/w.sum())>=0.25: c=px[np.argmin(lum)]   # lijnweging: donkerste wint als de lijn >=25% beslaat
    else: c=(px*w[:,None]).sum(0)/w.sum()
    A=np.array(allowed); return int(A[np.argmin(((P[A]-c)**2).sum(1))]), c
