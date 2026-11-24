# Haalt het eigen pixelraster van het Gemini-model terug (pitch 10,24, fase 9,25 gemeten met randsterkte) -> natief.png
import sys; from PIL import Image; import numpy as np
IN='../../r8/gemini_v8.png'; OUT='natief.png'
a=np.asarray(Image.open(IN).convert('RGB')).astype(int)
p=10.24; ph=9.25
cs=np.arange(ph-p+p/2,1024,p); cs=cs[cs>=0]
W=len(cs); out=np.zeros((W,W,3),'uint8')
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT); print(W)
g=out.min(axis=2)<215; yy,xx=np.where(g); print('bbox',xx.min(),xx.max(),yy.min(),yy.max())
Image.fromarray(out).resize((W*8,W*8),Image.NEAREST).save('natief_8x.png')
