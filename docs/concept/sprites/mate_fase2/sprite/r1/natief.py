# Natief raster van referenties/model.png (pitch 10,24, fase 0; zelfde methode als ogen/natief.py)
import numpy as np; from PIL import Image
D='docs/concept/sprites/mate_fase2/'
a=np.asarray(Image.open(D+'referenties/model.png').convert('RGB')).astype(int)
p=10.24; cs=np.arange(p/2,1024,p)
out=np.zeros((len(cs),len(cs),3),'uint8')
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,y1=int(max(0,y-2)),int(min(1024,y+3)); x0,x1=int(max(0,x-2)),int(min(1024,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(D+'sprite/r1/natief.png')
