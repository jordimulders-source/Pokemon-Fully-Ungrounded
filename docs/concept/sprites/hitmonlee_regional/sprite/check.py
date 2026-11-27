# check.py rN: kleurtelling, losse pixels (clusters <3 van een vultint, glans 10/12 uitgezonderd), lijnstatistiek
import numpy as np, sys
from scipy import ndimage
L=np.load(sys.argv[1]+'/idx.npy'); F=L>0; H,W=L.shape
print('figuur',F.sum(),'px; bbox', np.where(F.any(0))[0][[0,-1]], np.where(F.any(1))[0][[0,-1]])
u,c=np.unique(L[F],return_counts=True); print('kleuren in gebruik',len(u),dict(zip(u.tolist(),c.tolist())))
er=ndimage.binary_erosion(F); rim=F&~er
print('buitenrand',rim.sum(),'zwart(1)',(L[rim]==1).sum(),'donkerrood(2)',(L[rim]==2).sum(),'anders',((L[rim]!=1)&(L[rim]!=2)).sum())
print('zwart binnen figuur (niet rand):',((L==1)&~rim).sum(), ' = %.1f%% van binnen'%(100*((L==1)&~rim).sum()/(~rim&F).sum()))
klein=[]
for k in u:
    if k in (1,10): continue
    lab,n=ndimage.label(L==k)
    for i in range(1,n+1):
        m=lab==i
        if m.sum()<3:
            ys,xs=np.where(m); klein.append((int(k),list(zip(xs.tolist(),ys.tolist()))))
print('clusters <3 px:',len(klein))
for k,p in klein: print('  ',k,p)
