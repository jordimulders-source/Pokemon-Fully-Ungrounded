# Volgorde: natief.py -> km.py -> reduce.py 2.9 0 0.97 -> plaats.py -> build.py -> render/vel
# reductie.npy (+lijnfam) -> basis.npy / basis_fam.npy: uitsnede in 64x64, onderkant op rij 61, horizontaal gecentreerd. Bewaart de verschuiving (plaats.json) voor de modelvergelijking.
import numpy as np, json
o=np.load('reductie.npy'); fam=np.load('lijnfam.npy'); ys,xs=np.where(o>0)
y0s,x0s=ys.min(),xs.min(); c=o[y0s:ys.max()+1,x0s:xs.max()+1]; cf=fam[y0s:ys.max()+1,x0s:xs.max()+1]; h,w=c.shape
f=np.zeros((64,64),int); ff=-np.ones((64,64),int); y0=61-h+1; x0=(64-w)//2
f[y0:y0+h,x0:x0+w]=c; ff[y0:y0+h,x0:x0+w]=cf; np.save('basis.npy',f); np.save('basis_fam.npy',ff)
json.dump({'dy':int(y0-y0s),'dx':int(x0-x0s)},open('plaats.json','w')); print(h,w,y0,x0)
