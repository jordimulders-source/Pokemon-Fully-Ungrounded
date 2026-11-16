# r4: tintvlakjes in de kop tellen (4-buren, zelfde index, creme 3/4/5 en goud 14) met grootte < 3; lijnen/roze niet.
import numpy as np, sys; from PIL import Image
from scipy import ndimage
a=np.asarray(Image.open(sys.argv[1] if len(sys.argv)>1 else 'sprite.png')).astype(int)
Y,X=np.mgrid[:64,:64]; Z=(X<22)&(Y<27)&(Y>6)&~((X>=18)&(Y>=24))
for k in (3,4,5,14):
    lab,n=ndimage.label((a==k)&Z)
    for c in range(1,n+1):
        ys,xs=np.where(lab==c)
        if len(ys)<3: print('index',k,'vlakje',len(ys),'px',list(zip(xs.tolist(),ys.tolist())))
