# Haalt het eigen pixelraster van het Gemini-model terug (pitch 10,24, fase 9,25 gemeten met pitch.py) -> natief.png (100x100)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../r1/gemini_r1.png').convert('RGB')).astype(int)
p=10.24; ph=9.25
xs=np.arange(ph+0.5+p/2-p,1024,p); xs=xs[xs>0]
out=np.zeros((len(xs),len(xs),3),'uint8')
for j,y in enumerate(xs):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png')
m=out.min(2)<225; yy,xx=np.where(m); print('natief',out.shape,'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max())
Image.fromarray(out).resize((out.shape[1]*8,out.shape[0]*8),Image.NEAREST).save('natief_8x.png')
