# Natief raster van gemini_r2 terughalen: pitch 10,24, fase 9,25 (gemeten met randsterkte) -> natief.png
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../model/gemini_r2.png').convert('RGB')).astype(int)
P,PH=10.24,9.25
cs=np.arange(PH+P/2,1024,P); n=len(cs)
out=np.zeros((n,n,3),'uint8')
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,y1=int(y-2),int(y+3); x0,x1=int(x-2),int(x+3)
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png'); print(n)
