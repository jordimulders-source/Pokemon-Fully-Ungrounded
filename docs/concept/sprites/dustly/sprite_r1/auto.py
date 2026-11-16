# Automatische klassenreductie (natief -> 2/3) op het kale silhouet: elke spritepixel komt uit zijn modelblok.
# Uit: sprite_r1/auto_idx.npy (64x64 indices). Niets getekend; reparaties per pixel gebeuren in trouw.py.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('basis/natief.png').convert('RGB')).astype(float)
X0,Y0=17,18; Wn,Hn=69,63; a=a[Y0:Y0+Hn,X0:X0+Wn]
R,G,B=a[...,0],a[...,1],a[...,2]; lum=.299*R+.587*G+.114*B
import sys; sys.path.insert(0,'basis'); from bgmask import bgmask; bg=bgmask()[Y0:Y0+Hn,X0:X0+Wn]
rim=(R-G>=25)&~bg; rimI=rim&(lum>=175); rimO=rim&~rimI
wit=(lum>=175)&~rim&~bg
K=(lum<35)&~bg; L=(lum>=35)&(lum<56)&~bg&~rim
body=~bg&~rim&~wit&~K&~L
W,H=46,42
w1=np.array([[1,.5,0],[0,.5,1]])   # gewicht natieve kolom 0..2 voor uitvoer 0/1
kaal=np.load('basis/kaal_idx.npy')
o=np.zeros((H,W),int)
for y in range(H):
    for x in range(W):
        if kaal[y,x]<0: continue
        by,bx=3*(y//2),3*(x//2); wy=w1[y%2]; wx=w1[x%2]; wt=np.outer(wy,wx)
        sl=(slice(by,by+3),slice(bx,bx+3)); tot=(wt*~bg[sl]).sum()
        f=lambda m:(wt*m[sl]).sum()/tot
        if f(wit)>=.4: o[y,x]=9
        elif f(K)>=.4: o[y,x]=1
        elif f(rimI)>=.3: o[y,x]=8
        elif f(rimO)>=.3: o[y,x]=7
        elif f(K)+f(L)>=.35: o[y,x]=2
        else:
            bm=wt*body[sl]
            l=(bm*lum[sl]).sum()/bm.sum() if bm.sum()>0 else (wt*lum[sl]*~bg[sl]).sum()/tot
            o[y,x]=3 if l<86 else (4 if l<116 else (5 if l<158 else 6))
full=np.zeros((64,64),int); full[8:8+H,9:9+W]=o
np.save('sprite_r1/auto_idx.npy',full)
print('px',(full>0).sum(),{i:int((full==i).sum()) for i in range(1,12)})
