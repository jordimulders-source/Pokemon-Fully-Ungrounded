from PIL import Image; import numpy as np
a=np.asarray(Image.open('natief.png')).astype(float)
m=a.min(axis=2)<236
X=a[m]; rng=np.random.default_rng(1)
K=int(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else 18
C=X[rng.choice(len(X),K,replace=False)]
# kmeans++ init
C=[X[rng.integers(len(X))]]
for _ in range(K-1):
    d=np.min(((X[:,None]-np.array(C)[None])**2).sum(2),1); C.append(X[rng.choice(len(X),p=d/d.sum())])
C=np.array(C)
for it in range(60):
    l=((X[:,None]-C[None])**2).sum(2).argmin(1)
    C=np.array([X[l==k].mean(0) if (l==k).any() else C[k] for k in range(K)])
o=np.argsort(C.sum(1))
for k in o: print(k,C[k].round().astype(int),(l==k).sum())
np.save('km.npy',C[o])
