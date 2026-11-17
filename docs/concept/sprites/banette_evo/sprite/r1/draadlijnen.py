# Middellijnen van de draden in spritecoördinaten
import numpy as np; from scipy import ndimage as nd
dr=np.load('draden_mask.npy'); lab,n=nd.label(dr,structure=np.ones((3,3)))
S=968/62; sx=lambda x:(x-24)/S+1; sy=lambda y:(y-1)/S+4
L={}
for k in range(1,n+1):
    ys,xs=np.where(lab==k)
    if len(ys)<60: continue
    pts=[]
    for y in range(ys.min(),ys.max()+1):
        xr=xs[ys==y]
        if len(xr): pts.append((sx(xr.mean()+0.5),sy(y+0.5)))
    L[k]=pts
    print(k,'van (%.1f,%.1f) tot (%.1f,%.1f)'%(pts[0]+pts[-1]))
np.save('draadlijnen.npy',np.array([L],dtype=object))
