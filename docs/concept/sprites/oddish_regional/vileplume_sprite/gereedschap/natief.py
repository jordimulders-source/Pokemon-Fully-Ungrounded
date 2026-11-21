# Haalt het eigen pixelraster van het Vileplume-model terug -> gereedschap/natief.png
# Randsterkte-zoeker gaf pitch 10,24 / fase 9,25 (zelfde als de Oddish), maar op een uitvergrote uitsnede
# (krater, tentakels) zijn de echte cellen 5,12 px: half raster (les pitahaya). 200x200 natieve px.
from PIL import Image; import numpy as np
IN='../referenties/gemini_gekozen_vileplume.png'; OUT='gereedschap/natief.png'
a=np.asarray(Image.open(IN).convert('RGB')).astype(int)
p=5.12; c0=9.75+p/2-0.5          # celmidden (grens 9,75 + halve cel)
xs=np.arange(c0%p,1024,p); ys=xs
W,H=len(xs),len(ys); out=np.zeros((H,W,3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,round(y)-1)),int(min(1024,round(y)+2)); x0,x1=int(max(0,round(x)-1)),int(min(1024,round(x)+2))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
im=Image.fromarray(out); im.save(OUT); print(W,H,'eerste celmidden',xs[0])
m=np.asarray(im).min(2)<215; yy,xx=np.where(m); print('bbox natief',xx.min(),xx.max(),yy.min(),yy.max())
