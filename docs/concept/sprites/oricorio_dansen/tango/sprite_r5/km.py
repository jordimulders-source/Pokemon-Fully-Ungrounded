# Clustert de natieve modelkleuren (k-means, K=20) -> km_lab.npy, km_c.npy (gesorteerd op helderheid)
from PIL import Image; import numpy as np
a=np.asarray(Image.open('natief.png')).astype(float); bg=a.min(2)>=215
X=a[~bg]; rng=np.random.default_rng(0); K=20
best=None
for t in range(6):
    C=X[rng.choice(len(X),K,replace=False)]
    for it in range(50):
        d=((X[:,None]-C[None])**2).sum(2); L=d.argmin(1)
        C=np.array([X[L==k].mean(0) if (L==k).any() else C[k] for k in range(K)])
    e=d.min(1).sum()
    if best is None or e<best[0]: best=(e,C,L)
_,C,L=best
o=np.argsort(C@[.299,.587,.114]); rk=np.empty(K,int); rk[o]=np.arange(K); C=C[o]; L=rk[L]
lab=-np.ones(bg.shape,int); lab[~bg]=L; np.save('km_lab.npy',lab); np.save('km_c.npy',C)
for k in range(K): print(k,C[k].astype(int),(L==k).sum())
