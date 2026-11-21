# Natief raster terughalen: pitch 10.24 (=1024/100), fase 9.25 (randen) -> celmidden; mediaan 5x5 per cel
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../model/model.png').convert('RGB')).astype(int)
P=10.24; PH=9.25
# randen liggen op idx ph+k*p ; celmidden op ph+p/2 + k*p (en de cel ervoor)
cs=np.arange(PH+1-P+P/2,1024,P); cs=cs[cs>2]
W=len(cs); out=np.zeros((W,W,3),'uint8')
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png')
g=out.min(axis=2); yy,xx=np.where(g<215); print(W,'bbox',xx.min(),xx.max(),yy.min(),yy.max())
Image.fromarray(out).resize((W*8,W*8),Image.NEAREST).save('natief_8x.png')
