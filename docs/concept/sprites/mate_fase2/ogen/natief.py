# Natief raster van r6_water_r2 (pitch 10,24, fase 0) -> ogen/natief.png (100x100)
import numpy as np; from PIL import Image
a=np.asarray(Image.open('r6_samengesteld/r6_water_r2.png').convert('RGB')).astype(int)
p=10.24; cs=np.arange(p/2,1024,p)
out=np.zeros((len(cs),len(cs),3),'uint8')
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('ogen/natief.png')
Image.fromarray(out).resize((800,800),Image.NEAREST).save('ogen/natief_8x.png')
