# Modeltinten: k-means op de objectpixels van het natieve model (achtergrond = floodfill wit vanaf de rand)
import numpy as np; from PIL import Image; from collections import deque
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
wit=(a.min(2)>=245)&((a.max(2)-a.min(2))<=8); bg=np.zeros(wit.shape,bool)
q=deque([(y,x) for y in range(100) for x in (0,99)]+[(y,x) for x in range(100) for y in (0,99)])
while q:
    y,x=q.popleft()
    if 0<=y<100 and 0<=x<100 and wit[y,x] and not bg[y,x]: bg[y,x]=True; q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
np.save('bg.npy',bg)
X=a[~bg]; rng=np.random.default_rng(1)
K=int(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else 18
C=X[rng.choice(len(X),K,replace=False)]
for it in range(60):
    l=((X[:,None]-C[None])**2).sum(-1).argmin(1)
    C=np.array([X[l==k].mean(0) if (l==k).any() else C[k] for k in range(K)])
l=((X[:,None]-C[None])**2).sum(-1).argmin(1)
o=np.argsort(C.sum(1))
for k in o: print(tuple(int(v) for v in C[k]),(l==k).sum())
