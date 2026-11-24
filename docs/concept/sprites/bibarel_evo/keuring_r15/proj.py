# model r10_k8 geprojecteerd op het 64-raster (vlakgemiddelde), zelfde mapping als sprite_r13/reductie.py
import numpy as np
from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/bibarel_evo/'
MK=np.asarray(Image.open(B+'model/r10_k8.png').convert('RGB')).astype(float)
s_=64/90; mx0,my0,oy=0,9,6
def proj():
    out=np.zeros((64,64,3))
    for y in range(64):
        for x in range(64):
            x0=mx0+x/s_; x1=mx0+(x+1)/s_; y0=my0+(y-oy)/s_; y1=my0+(y+1-oy)/s_
            acc=np.zeros(3); W=0
            for yy in range(int(np.floor(y0)),int(np.ceil(y1))):
                for xx in range(int(np.floor(x0)),int(np.ceil(x1))):
                    if 0<=xx<99 and 0<=yy<99:
                        wx=min(xx+1,x1)-max(xx,x0); wy=min(yy+1,y1)-max(yy,y0)
                        if wx>0 and wy>0: acc+=MK[yy,xx]*wx*wy; W+=wx*wy
            out[y,x]=acc/W if W else 255
    return out
if __name__=='__main__':
    P=proj(); np.save('model_proj.npy',P)
    Image.fromarray(P.astype('uint8')).resize((512,512),Image.NEAREST).save('model_proj_8x.png')
