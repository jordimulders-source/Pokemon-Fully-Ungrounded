# Haalt het natieve raster van Gemini r4 terug (pitch 16.02, grens na pixel 14) -> r1/natief.png (+ spreiding per cel)
from PIL import Image; import numpy as np
a=np.asarray(Image.open('referenties/gemini_gekozen_r3.png').convert('RGB')).astype(int)
P=16.0; PH=14.0
xs=np.arange(PH+1+P/2,1024,P); ys=np.arange(PH+1+P/2,1024,P)
H,W=len(ys),len(xs); out=np.zeros((H,W,3),'uint8'); sd=np.zeros((H,W))
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        b=a[int(y-4):int(y+4),int(x-4):int(x+4)].reshape(-1,3)
        out[j,i]=np.median(b,axis=0); sd[j,i]=b.std(axis=0).mean()
Image.fromarray(out).save('r1/natief.png'); np.save('r1/natief_sd.npy',sd)
g=out.astype(int).sum(axis=2); yy,xx=np.where(g<3*225); print(W,H,'bbox',xx.min(),xx.max(),yy.min(),yy.max(),'max sd fig',sd[yy,xx].max(), 'cells sd>15',(sd[yy,xx]>15).sum())
