# Vlakgemiddelde (mediaan van het celmidden) uit model.webp op het spriteraster, naar het r9-ijzerpalet (1,7-12).
from PIL import Image; import numpy as np
m=np.array(Image.open('model/model.webp').convert('RGB')).astype(int)
im=Image.open('sprite_r9/sprite.png'); P=np.array(im.getpalette()[:14*3]).reshape(14,3)
K=13.77
def cel(x,y,r=4):
    cx=102+(x+0.5)*K; cy=71+(y-2+0.5)*K
    return np.median(m[int(cy-r):int(cy+r+1),int(cx-r):int(cx+r+1)].reshape(-1,3),axis=0)
def raster(idx=(1,7,8,9,10,11,12,2,3,4,5,6)):
    o=np.zeros((64,64),'uint8')
    for y in range(64):
        for x in range(64):
            c=cel(x,y)
            if c.min()>225: continue
            o[y,x]=idx[int(np.argmin([((c-P[i])**2).sum() for i in idx]))]
    return o
if __name__=='__main__':
    o=raster(); r=Image.fromarray(o,'P'); r.putpalette(im.getpalette()); r.save('sprite_r10/model_vlak.png',transparency=0)
    print('   '+''.join(str(x%10) for x in range(40)))
    for y in range(12,64): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in o[y,:40]))
