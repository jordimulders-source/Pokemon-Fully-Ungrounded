# Kale reductie: geschrapt model -> k-means-palet uit het model zelf (14 vulkleuren + lijn), dichtstbijzijnde kleur.
from PIL import Image; import numpy as np
D='docs/concept/sprites/hitmonlee_regional/sprite/'
B=np.asarray(Image.open(D+'r1/geschrapt.png').convert('RGB')).astype(float)
F=np.load(D+'r1/fig.npy')
X=B[F]
rng=np.random.default_rng(1)
K=15
C=X[rng.choice(len(X),K,replace=False)]
for it in range(60):
    d=((X[:,None]-C[None])**2).sum(2); l=d.argmin(1)
    for k in range(K):
        if (l==k).any(): C[k]=X[l==k].mean(0)
C=C[np.argsort(C.mean(1))]
d=((B[...,None,:]-C[None,None])**2).sum(3); L=d.argmin(2)+1; L[~F]=0
for k,c in enumerate(C): print(k+1,c.astype(int),int(c.mean()),(L==k+1).sum())
np.save(D+'r1/kale_idx.npy',L); np.save(D+'r1/kale_pal.npy',C)
