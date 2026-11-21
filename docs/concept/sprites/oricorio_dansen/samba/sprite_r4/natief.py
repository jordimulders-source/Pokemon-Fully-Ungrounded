# Natief raster van gemini_r10 terughalen: pitch 5,12 (=1024/200) in x en y (Fourier op randsterkte: 0,59 tegen 0,07 bij 10,24),
# randen op 4,64 mod 5,12 -> celcentra 2,08 + k*5,12. Mediaan van de 3x3 middelste modelpixels per cel -> natief.png (200x200)
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../model/gemini_r10.png').convert('RGB')).astype(int)
P=5.12; C0=2.08
cs=np.arange(C0,1024,P); n=len(cs)
out=np.zeros((n,n,3),'uint8')
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,y1=int(round(y-1)),int(round(y+2)); x0,x1=int(round(x-1)),int(round(x+2))
        out[j,i]=np.median(a[max(y0,0):y1,max(x0,0):x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png'); print(out.shape)
