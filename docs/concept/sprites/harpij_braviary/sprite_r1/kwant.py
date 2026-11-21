# Stap 1: kleuren van het natieve model meten (k-means op de vogelpixels) -> modelpalet + model_kwant.png
import numpy as np; from PIL import Image; from collections import deque
a=np.asarray(Image.open('../model/model_natief.png').convert('RGB')).astype(float); H,W=a.shape[:2]
light=a.min(2)>=244
bg=np.zeros((H,W),bool); q=deque([(y,x) for y in range(H) for x in (0,W-1)]+[(y,x) for x in range(W) for y in (0,H-1)])
while q:
    y,x=q.popleft()
    if 0<=y<H and 0<=x<W and light[y,x] and not bg[y,x]:
        bg[y,x]=True; q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
P=a[~bg]; K=int(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else 12
rng=np.random.default_rng(1)
# init: helderheid-kwantielen
lum=P.mean(1); idx=np.argsort(lum); c=P[idx[np.linspace(0,len(P)-1,K).astype(int)]].copy()
for _ in range(60):
    d=((P[:,None]-c[None])**2).sum(-1); l=d.argmin(1)
    for k in range(K):
        if (l==k).any(): c[k]=P[l==k].mean(0)
order=np.argsort(c.mean(1)); c=c[order]
d=((P[:,None]-c[None])**2).sum(-1); l=d.argmin(1)
for k in range(K): print(k+1,c[k].astype(int).tolist(),(l==k).sum())
o=np.zeros((H,W),int); o[~bg]=l+1
np.save('model_idx.npy',o); np.save('model_pal.npy',c)
pal=[(255,255,255)]+[tuple(int(v) for v in x) for x in c]
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for t in pal for v in t]+[0]*(768-3*len(pal)))
im.convert('RGB').resize((W*8,H*8),Image.NEAREST).save('model_kwant_8x.png')
print('vogel bbox', np.argwhere(~bg).min(0), np.argwhere(~bg).max(0))
