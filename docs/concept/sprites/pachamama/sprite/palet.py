# Palet uit het model: k-means op de natieve modelpixels (niet-zwart), gezaaid met de modelgroepen.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('natief.png')).astype(float)
fg=a.min(2)<235; lum=a@[.299,.587,.114]
px=a[fg&(lum>55)]
seed=np.array([(84,60,48),(108,100,84),(150,140,122),(122,72,60),(160,84,70),(180,108,100),(200,136,132),
 (160,126,64),(200,166,88),(62,100,90),(80,130,116),(114,170,150),(192,190,170),(244,242,222),(205,214,222)],float)
C=seed.copy()
for it in range(30):
  d=((px[:,None]-C[None])**2).sum(2); l=d.argmin(1)
  C=np.array([px[l==k].mean(0) if (l==k).any() else C[k] for k in range(len(C))])
cnt=np.bincount(l,minlength=len(C))
for k in range(len(C)): print(k+2,C[k].astype(int).tolist(),cnt[k])
np.save('palet_kmeans.npy',C)
