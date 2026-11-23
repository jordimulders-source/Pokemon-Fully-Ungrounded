# Stap 1a: natief raster terughalen (pitch 10,24 fase 9,25 gemeten met gereedschap/pitch.py-methode op model_v2_r4.webp).
# Per cel: mediaan van het midden (6x6), dan vergelijk met de modus om webp-ruis te tonen.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('referenties/model_v2_r4.webp').convert('RGB')).astype(int)
p=10.24; ph=9.25
xs=np.arange(ph+0.5+p/2-p,1024,p); xs=xs[xs>0]
out=np.zeros((len(xs),len(xs),3),'uint8')
for j,y in enumerate(xs):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-3)),int(min(1024,y+3)); x0,x1=int(max(0,x-3)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('sprite_v2/natief_ruw.png')
m=out.min(2)<215; yy,xx=np.where(m); print(out.shape,'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max())
