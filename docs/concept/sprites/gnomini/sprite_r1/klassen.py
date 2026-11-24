# Natief model -> indexraster met modelpalet (k-means op de figuur). Schrijft natief_idx.npy + modelpalet.txt, print tekstraster.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('natief.png')).astype(float)
fg=a.min(2)<235
X=a[fg]; rng=np.random.default_rng(1)
K=16; C=X[rng.choice(len(X),K,replace=False)]
for _ in range(60):
    d=((X[:,None]-C[None])**2).sum(2); l=d.argmin(1)
    C=np.array([X[l==k].mean(0) if (l==k).any() else C[k] for k in range(K)])
# samenvoegen van bijna gelijke clusters
keep=[]
for c in C[np.argsort(C.mean(1))]:
    if all(((c-k)**2).sum()>18**2 for k in keep): keep.append(c)
C=np.array(keep)
d=((a[:,:,None]-C[None,None])**2).sum(3); idx=d.argmin(2)+1; idx[~fg]=0
np.save('natief_idx.npy',idx)
CH='.0123456789ABCDEFGH'
with open('modelpalet.txt','w') as f:
    for i,c in enumerate(C): f.write('%s %s n=%d\n'%(CH[i+1],tuple(int(v) for v in c),(idx==i+1).sum()))
print(open('modelpalet.txt').read())
for y in range(20,77): print('%2d '%y+''.join(CH[v] for v in idx[y,26:74]))
