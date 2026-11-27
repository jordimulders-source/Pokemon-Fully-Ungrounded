# Natief raster terughalen: pitch P, fase uit pitch.py; mediaan van het celmidden.
import sys; from PIL import Image; import numpy as np
P=float(sys.argv[1]) if len(sys.argv)>1 else 10.24
PHX=float(sys.argv[2]) if len(sys.argv)>2 else 9.25; PHY=float(sys.argv[3]) if len(sys.argv)>3 else 9.25
OUT=sys.argv[4] if len(sys.argv)>4 else 'natief.png'
a=np.asarray(Image.open('../model.png').convert('RGB')).astype(int)
xs=np.arange(PHX%P+P/2,1024,P); ys=np.arange(PHY%P+P/2,1024,P)
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-1.5)),int(min(1024,y+2.5)); x0,x1=int(max(0,x-1.5)),int(min(1024,x+2.5))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
im=Image.fromarray(out); im.save(OUT)
g=out.min(axis=2); m=g<232; yy,xx=np.where(m)
print(len(xs),len(ys),'bbox',xx.min(),xx.max(),yy.min(),yy.max(),'gevuld',m.sum())
