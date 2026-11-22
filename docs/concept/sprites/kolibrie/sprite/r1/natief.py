# Natief raster terughalen: mediaan van het celmidden per Gemini-cel
# gebruik: natief.py IN OUT pitch_x fase_x pitch_y fase_y
import sys; from PIL import Image; import numpy as np
IN,OUT=sys.argv[1],sys.argv[2]; px,phx,py,phy=map(float,sys.argv[3:7])
a=np.asarray(Image.open(IN).convert('RGB')).astype(int); H0,W0=a.shape[:2]
xs=np.arange(phx%px+px/2,W0,px); ys=np.arange(phy%py+py/2,H0,py)
out=np.zeros((len(ys),len(xs),3),'uint8'); r=max(1,int(px*0.22))
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-r)),int(min(H0,y+r+1)); x0,x1=int(max(0,x-r)),int(min(W0,x+r+1))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT)
g=np.asarray(Image.fromarray(out).convert('L')); yy,xx=np.where(g<225)
print(OUT,len(xs),len(ys),'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max(),'=> %dx%d'%(xx.max()-xx.min()+1,yy.max()-yy.min()+1))
