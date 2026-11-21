# Natief raster van r6 terughalen (pitch 10.25, fase 8.5) -> plak/natief.png
from PIL import Image; import numpy as np
a=np.asarray(Image.open('gemini/r6.png').convert('RGB')).astype(int)
p,ph=10.25,8.5
cs=np.arange(ph+p/2,1024,p)
out=np.zeros((len(cs),len(cs),3),'uint8')
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,x0=int(y)-1,int(x)-1
        out[j,i]=np.median(a[y0:y0+3,x0:x0+3].reshape(-1,3),axis=0)
Image.fromarray(out).save('plak/natief.png'); print(out.shape)
