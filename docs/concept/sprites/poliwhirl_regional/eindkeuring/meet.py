# Modelhelderheid van het geel per spritepixel (raster uit ../sprite_r4/reductie.npz, sprite = cel + (7,12)) -> ylum.npy
import numpy as np; from PIL import Image
m=np.asarray(Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB')).astype(float)
L=(m[...,0]*299+m[...,1]*587+m[...,2]*114)/1000; R,G,B=m[...,0],m[...,1],m[...,2]
yel=(R>140)&(G>110)&(B<120)&(R-B>50)
d=np.load('../sprite_r4/reductie.npz'); xs,ys=d['xs'],d['ys']; out=np.full((64,64),np.nan)
for y in range(64):
    for x in range(64):
        cy,cx=y-12,x-7
        if 0<=cy<len(ys)-1 and 0<=cx<len(xs)-1:
            sl=(slice(int(ys[cy]),int(ys[cy+1])),slice(int(xs[cx]),int(xs[cx+1]))); mm=yel[sl]
            if mm.sum()>20: out[y,x]=L[sl][mm].mean()
np.save('ylum.npy',out)
