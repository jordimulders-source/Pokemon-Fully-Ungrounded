# Volgorde: natief.py -> km.py -> schrap.py 1 0 -> plaats.py -> modeltoon.py -> build.py -> kleur.py -> render.py tango_r5.npy (cp A_donker -> tango.png) -> vel.py
# schrap.npy -> basis.npy: uitsnede in 64x64, onderkant op rij 61, horizontaal gecentreerd
import numpy as np
o=np.load('schrap.npy'); ys,xs=np.where(o>0); c=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; h,w=c.shape
f=np.zeros((64,64),int); y0=61-h+1; x0=(64-w)//2; f[y0:y0+h,x0:x0+w]=c; np.save('basis.npy',f); print(h,w,y0,x0)
