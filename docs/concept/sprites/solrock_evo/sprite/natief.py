# Haalt het eigen pixelraster van het Gemini-model terug. Niets getekend: cel = mediaan van het binnenste.
# gebruik: python3 natief.py pitch fase uit.png
import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open('../referenties/model.png').convert('RGB')).astype(int)
p=float(sys.argv[1]); ph=float(sys.argv[2]); OUT=sys.argv[3]
cs=np.arange(ph+p/2,1024,p)
n=len(cs); out=np.zeros((n,n,3),'uint8'); r=max(1,int(p/4))
for j,y in enumerate(cs):
    for i,x in enumerate(cs):
        y0,y1=int(y-r),int(y+r+1); x0,x1=int(x-r),int(x+r+1)
        out[j,i]=np.median(a[max(0,y0):y1,max(0,x0):x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT); print(n)
