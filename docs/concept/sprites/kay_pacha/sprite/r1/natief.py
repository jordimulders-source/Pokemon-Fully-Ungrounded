# Natief raster terughalen. Pitch 10,24 wint de kam (fase x 9,25 / y 9,0); kleinste details (oogglans) zijn een halve cel
# -> sample op 5,12 (halve cel; vangt het 10,24-raster exact mee). Mediaan in het celmidden (3x3) tegen blur.
import numpy as np; from PIL import Image
a=np.asarray(Image.open('referenties/gemini_gekozen_r10a.png').convert('RGB')).astype(int)
p=5.12; phx=9.25; phy=9.0
xs=np.arange(phx+0.5+p/2-p*int(phx//p+1),1024,p); xs=xs[xs>=1]
ys=np.arange(phy+0.5+p/2-p*int(phy//p+1),1024,p); ys=ys[ys>=1]
out=np.zeros((len(ys),len(xs),3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-1)),int(min(1024,y+2)); x0,x1=int(max(0,x-1)),int(min(1024,x+2))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save('sprite/r1/natief.png')
np.save('sprite/r1/natief_xy.npy',np.array([xs[0],ys[0],p]))
m=out.min(2)<225; yy,xx=np.where(m); print('natief',out.shape,'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max(), 'w',xx.max()-xx.min()+1,'h',yy.max()-yy.min()+1)
