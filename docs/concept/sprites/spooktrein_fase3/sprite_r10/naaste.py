# Model op het spriteraster: elke spritepixel = de dichtstbijzijnde natieve modelpixel (schrappen), gekwantiseerd naar het r9-palet.
from PIL import Image; import numpy as np
n=np.array(Image.open('model/natief.png').convert('RGB')).astype(int)
im=Image.open('sprite_r9/sprite.png'); P=np.array(im.getpalette()[:14*3]).reshape(14,3)
def nat(x,y): return int(round(9+(x+0.5)/0.744-0.5)), int(round(6+(y-2+0.5)/0.744-0.5))
def raster(idx=range(1,14)):
    out=np.zeros((64,64),'uint8')
    for y in range(64):
        for x in range(64):
            nx,ny=nat(x,y)
            if not(0<=nx<99 and 0<=ny<99): continue
            c=n[ny,nx]
            if c.min()>225: continue
            d=[((c-P[i])**2).sum() for i in idx]; out[y,x]=list(idx)[int(np.argmin(d))]
    return out
if __name__=='__main__':
    o=raster(); r=Image.fromarray(o,'P'); r.putpalette(im.getpalette()); r.save('sprite_r10/model_naaste.png',transparency=0)
    for y in range(12,64): print('%2d '%y+''.join('.' if v==0 else '%X'%v for v in o[y,:40]))
