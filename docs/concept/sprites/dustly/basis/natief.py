# Haalt het eigen pixelraster van het Gemini-model terug (pitch 10,24, fase 9,25) -> basis/natief.png (100x100)
from PIL import Image; import numpy as np
a=np.asarray(Image.open('gemini/r6_a.png').convert('RGB')).astype(int)
p,ph=10.24,9.25
c=np.arange(ph+1+p/2-p,1024,p); c=c[c>=0]
H=W=len(c); out=np.zeros((H,W,3),'uint8')
for j,y in enumerate(c):
    for i,x in enumerate(c):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('basis/natief.png'); print(W,H)
