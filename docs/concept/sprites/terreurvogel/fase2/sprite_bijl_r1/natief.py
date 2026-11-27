# Natief raster van gemini/r1_eenvoud.png terughalen: pitch 10.24 (x en y), fase 9.25 (gemeten, piek over 4.5-16).
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../gemini/r1_eenvoud.png').convert('RGB')).astype(int)
p=10.24; ph=9.25
xs=np.arange(ph+p/2,1024,p); ys=np.arange(ph+p/2,1024,p)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(y-2),int(y+3); x0,x1=int(x-2),int(x+3)
        out[j,i]=np.median(a[max(0,y0):y1,max(0,x0):x1].reshape(-1,3),axis=0)
# eerste cel links/boven (fase 9.25 -> kolom 0..9 is ook een cel)
Image.fromarray(out).save('natief.png')
m=out.astype(int).min(2)<225; yy,xx=np.where(m); print(out.shape,'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max())
