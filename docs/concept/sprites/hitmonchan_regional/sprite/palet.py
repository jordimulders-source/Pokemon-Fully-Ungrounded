# Palet meten op het natieve model: k-means in Lab op alle figuurpixels (k=7 vanaf r5; 15 en 9 gaven hetzelfde beeld met bijna-gelijke tinten en meer spikkels in de facetten), gesorteerd op helderheid.
# Schrijft pal.txt (index 0 = achtergrond) en natief_q.png (natief per pixel naar dichtstbijzijnde paletkleur).
from PIL import Image; import numpy as np, sys
D='docs/concept/sprites/hitmonchan_regional/sprite/'
sys.path.insert(0,D); from toon import lab, save_idx
K=int(sys.argv[1]) if len(sys.argv)>1 else 7
nat=np.asarray(Image.open(D+'natief.png').convert('RGB')).astype(float)
# achtergrond = neutraal wit (min>=248, grijs); ijswit is blauwig (bv. 239,248,250) en hoort bij de figuur.
# Ook ingesloten gaten in neutraal wit (onder de wachtvuist) zijn achtergrond.
fg=~((nat.min(2)>=248)&((nat.max(2)-nat.min(2))<8))
np.save(D+'silhouet.npy',fg)
X=nat[fg]; L=lab(X)
rng=np.random.default_rng(1)
best=None
for t in range(8):
    C=L[rng.choice(len(L),K,replace=False)]
    for it in range(60):
        d=((L[:,None]-C[None])**2).sum(2); a=d.argmin(1)
        C2=np.array([L[a==k].mean(0) if (a==k).any() else C[k] for k in range(K)])
        if np.allclose(C,C2): break
        C=C2
    e=d.min(1).sum()
    if best is None or e<best[0]: best=(e,C,a)
e,C,a=best
rgb=np.array([np.median(X[a==k],0) for k in range(K)])
o=np.argsort(lab(rgb)[:,0]); rgb=rgb[o].round().astype(int)
cnt=[int((a==o[k]).sum()) for k in range(K)]
pal=[(255,255,255)]+[tuple(map(int,c)) for c in rgb]
open(D+'pal.txt','w').write(repr(pal)+'\n')
for k,(c,n) in enumerate(zip(pal[1:],cnt),1): print(k,c,'L=%.0f'%lab(np.array(c,float))[0],n)
PL=lab(np.array(pal[1:],float))
idx=np.zeros(fg.shape,int)
idx[fg]=((lab(X)[:,None]-PL[None])**2).sum(2).argmin(1)+1
np.save(D+'natief_q.npy',idx)
save_idx(idx,pal,D+'natief_q_10x.png',10)
