# Controle C2: diff t.o.v. C en v6, tintvlakjes < 3 px rond ogen en mond
import numpy as np, json
from PIL import Image
from scipy import ndimage
from gezicht import a6, D
a=np.array(Image.open(D+'/kandidaat_C2.png')).astype(int); c=np.array(Image.open(D+'/kandidaat_C.png')).astype(int)
d=np.argwhere(a!=c); print('diff t.o.v. C:',len(d),'px, bbox x',d[:,1].min(),'-',d[:,1].max(),'y',d[:,0].min(),'-',d[:,0].max())
dv=np.argwhere(a!=a6); print('diff t.o.v. v6 bbox x',dv[:,1].min(),'-',dv[:,1].max(),'y',dv[:,0].min(),'-',dv[:,0].max(),'| silhouet',int(((a==0)!=(a6==0)).sum()),'| kleuren',len(np.unique(a)))
for k in (6,7,8,9):
    lab,n=ndimage.label(a==k,structure=np.ones((3,3)))
    for L in range(1,n+1):
        ys,xs=np.nonzero(lab==L)
        if len(ys)<3 and all(14<=x<=38 and 19<=y<=39 for x,y in zip(xs,ys)): print('vlakje',k,list(zip(xs.tolist(),ys.tolist())))
