# reduceer.py: model gemini_r10 -> 64x64 (zelfde plaatsing als r4/r5: x0=19.33, y0=29.22, 14.85 modelpx per spritepx),
# per cel wint de paletklasse met de meeste modelpixels (geen gemiddelde, geen blur); donkere modelpixels (<70 helderheid) = lijn 1.
import numpy as np; from PIL import Image
from palet import PAL
m=np.array(Image.open('../model/gemini_r10.png').convert('RGB')).astype(int)
x0,y0,s=19.3344,29.216,950.272; k=s/64
P=np.array(PAL[1:14],int)
d=((m[:,:,None,:]-P[None,None])**2).sum(-1); cls=d.argmin(-1)+1
L=m@np.array([0.299,0.587,0.114]); cls[L<70]=1
cls[m.min(-1)>225]=0
o=np.zeros((64,64),np.uint8)
for y in range(64):
    for x in range(64):
        c=cls[int(y0+y*k):int(y0+(y+1)*k),int(x0+x*k):int(x0+(x+1)*k)].ravel()
        o[y,x]=np.bincount(c,minlength=16).argmax()
np.save('model_red.npy',o)
