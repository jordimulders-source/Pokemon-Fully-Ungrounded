# Natief raster van het Gemini-model terughalen (pitch 10,24, fase 9,25) -> natief.png (100x100)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../referenties/model.png').convert('RGB')).astype(int)
p=10.24; c0=9.25+p/2-p
cs=np.arange(c0,1024,p); cs=cs[cs>=0]
out=np.zeros((len(cs),len(cs),3),'uint8')
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png')
g=np.asarray(Image.fromarray(out).convert('L')); yy,xx=np.where(g<225); print(out.shape,'bbox',xx.min(),xx.max(),yy.min(),yy.max())
Image.fromarray(out).resize((800,800),Image.NEAREST).save('natief_8x.png')
