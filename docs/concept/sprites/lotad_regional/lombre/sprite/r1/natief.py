# Natief raster van het model terughalen: pitch 10,24 (= 1024/100, gemeten met pitch.py), fase 9,25 -> 100x100.
# Per cel de mediaan van het middelste 5x5-blok. Uitvoer natief.png.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('../../r1/gemini_r1.png').convert('RGB')).astype(int)
P=10.24; PH=9.25-P   # celgrenzen op PH+k*P
H,W=a.shape[:2]; n=int((W-PH)//P)
out=np.zeros((n,n,3),'uint8')
for j in range(n):
    for i in range(n):
        y=PH+j*P+P/2; x=PH+i*P+P/2
        y0,y1=int(max(0,y-2)),int(min(H,y+3)); x0,x1=int(max(0,x-2)),int(min(W,x+3))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('natief.png')
m=out.min(2)<230; yy,xx=np.where(m); print('natief',n,'figuur x',xx.min(),xx.max(),'y',yy.min(),yy.max())
# controle: spreiding binnen cellen (laag = raster klopt)
sp=[]
for j in range(n):
    for i in range(n):
        y=PH+j*P+P/2; x=PH+i*P+P/2
        b=a[int(max(0,y-3)):int(y+4),int(max(0,x-3)):int(x+4)]; sp.append(b.std(axis=(0,1)).mean())
print('gem. spreiding binnen cel (7x7)',np.mean(sp))
