# Natief raster van het Gemini-model terughalen (pitch 10,24, fase 9,25; gemeten op randsterkte)
import sys; from PIL import Image; import numpy as np
IN=sys.argv[1]; OUT=sys.argv[2]; P=float(sys.argv[3]) if len(sys.argv)>3 else 10.24; PH=float(sys.argv[4]) if len(sys.argv)>4 else 9.25
a=np.asarray(Image.open(IN).convert('RGB')).astype(int)
cs=np.arange(PH+1-P,1024,P)+P/2; cs=cs[(cs>=0)&(cs<1024)]
H=W=len(cs); out=np.zeros((H,W,3),'uint8')
for j,y in enumerate(cs):
  for i,x in enumerate(cs):
    r=max(1,int(P/4)); y0,y1=int(max(0,y-r)),int(min(1024,y+r+1)); x0,x1=int(max(0,x-r)),int(min(1024,x+r+1))
    out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT); print(W,H)
