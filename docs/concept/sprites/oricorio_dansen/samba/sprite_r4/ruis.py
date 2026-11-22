# telling losse tintvlakjes (< 3 px, 8-samenhang) per vultint; lijn-/rand-tinten (G4, Y3) en de Pom-Pom/Baile-overnames (kop rij 26-33 kol 23-36,
# voeten rij 50-63) tellen niet mee. gebruik: ruis.py raster.npy [toon]
import numpy as np, sys
from scipy import ndimage as nd
o=np.load(sys.argv[1]); N=['_','O','G1','G2','G3','G4','Y1','Y2','Y3','B1','B2','K1','K2','K3','W']
vrij=np.zeros(o.shape,bool); vrij[26:34,23:37]=True; vrij[50:,:]=True
res={}
for k in (2,3,4,6,7,9,10):
    lab,n=nd.label(o==k,structure=np.ones((3,3)))
    pts=[]
    for i in range(1,n+1):
        p=np.argwhere(lab==i)
        if len(p)<3 and not vrij[tuple(p[0])]: pts.append([tuple(int(v) for v in q) for q in p])
    res[N[k]]=pts
print({k:len(v) for k,v in res.items()})
if len(sys.argv)>2:
    for k,v in res.items(): print(k,v)
