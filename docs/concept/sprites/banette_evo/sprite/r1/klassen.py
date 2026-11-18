# Klasse per modelpixel: 0 bg,1 lijn,2 grijs,3 rood,4 mond,5 oog-geel,6 blauw,7 licht(belglans)
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../../model/model.png').convert('RGB')).astype(int)
r,g,b=a[...,0],a[...,1],a[...,2]; L=a.sum(2)/3; mx=a.max(2); mn=a.min(2)
K=np.full(a.shape[:2],2)
K[mn>=232]=0
K[(r-np.maximum(g,b)>45)]=3
K[(b-r>14)&(b>=g)&(mn<232)]=6
K[(r>170)&(g>150)&(b<150)&(r-b>60)]=5
K[(L<62)&(np.abs(r-b)<25)]=4
K[(L<62)&(r-np.maximum(g,b)>12)]=4
K[L<38]=1
K[(mn>180)&(mn<232)&(mx-mn<20)]=7
np.save('klassen.npy',K)
col=np.array([[255,255,255],[0,0,0],[140,140,135],[210,80,80],[90,60,40],[240,220,100],[110,120,200],[220,220,220]])
Image.fromarray(col[K].astype('uint8')).save('klassen.png')
print(np.bincount(K.ravel()))
