# Haalt het eigen pixelraster van het Gemini-model terug (pitch 10,24 px = 100x100) -> natief.png
# Kopie/aanpassing van octillery_evo/sprite3/natief.py (pitch gemeten met randsterkte: 10,24, fase 9,25).
import sys; from PIL import Image; import numpy as np
IN='../referenties/gemini_gekozen_oddish.png'; OUT='gereedschap/natief.png'
a=np.asarray(Image.open(IN).convert('RGB')).astype(int)
p,ph=10.24,9.25
xs=np.arange(ph+1+p/2-0.5,1024,p); ys=xs
W,H=len(xs),len(ys); out=np.zeros((H,W,3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
im=Image.fromarray(out); im.save(OUT); print(W,H)
g=np.asarray(im.convert('L')); m=np.asarray(im).min(2)<215; yy,xx=np.where(m); print('bbox',xx.min(),xx.max(),yy.min(),yy.max())
