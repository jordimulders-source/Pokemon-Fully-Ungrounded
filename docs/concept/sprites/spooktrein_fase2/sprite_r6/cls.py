# Per spritepixel: samenstelling modelklassen (natieve klassering r2/cls.npy, vertaald naar huidige paletindex), supersampling 8x8.
import numpy as np, sys; from PIL import Image
s,X0,Y0,oy,XC,k=[float(v) for v in open('../sprite_r2/sprite.meta').read().split()]
cls=np.load('../sprite_r2/cls.npy')
R={0:0,1:1,2:2,3:3,4:4,5:5,6:5,7:6,8:7,9:8,10:9,11:10,12:11,13:12,14:13}
cur=np.vectorize(R.get)(cls)
def inv(u): return np.where(u<XC-X0, X0+u, XC+(u-(XC-X0))/k)
SS=8; C=np.zeros((14,64,64))
for j in range(64):
    for i in range(64):
        us=(i+(np.arange(SS)+0.5)/SS)/s; vs=Y0+(j-oy+(np.arange(SS)+0.5)/SS)/s
        xx=np.clip(inv(us).astype(int),0,198); yy=np.clip(vs.astype(int),0,198)
        c=cur[np.ix_(yy,xx)].ravel(); C[:,j,i]=np.bincount(c,minlength=14)/c.size
np.save('clsfrac.npy',C)
