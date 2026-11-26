# Modelkleuren clusteren (k-means in RGB op de figuurpixels van natief.png). Print centra + aantallen.
import numpy as np, sys; from PIL import Image
a=np.asarray(Image.open('natief.png')).astype(float); H,W,_=a.shape
fig=a.min(2)<232
X=a[fig]; K=int(sys.argv[1]) if len(sys.argv)>1 else 16
rng=np.random.default_rng(1); best=None
for t in range(8):
    C=X[rng.choice(len(X),K,replace=False)]
    for _ in range(60):
        d=((X[:,None]-C[None])**2).sum(2); l=d.argmin(1)
        C=np.array([X[l==k].mean(0) if (l==k).any() else C[k] for k in range(K)])
    e=d.min(1).sum()
    if best is None or e<best[0]: best=(e,C,l)
e,C,l=best; o=np.argsort([0.3*c[0]+0.59*c[1]+0.11*c[2] for c in C])
for k in o: print(k,tuple(int(v) for v in C[k]),(l==k).sum())
lab=np.full((H,W),-1); lab[fig]=l; np.save('kmeans_lab.npy',lab); np.save('kmeans_C.npy',C)
