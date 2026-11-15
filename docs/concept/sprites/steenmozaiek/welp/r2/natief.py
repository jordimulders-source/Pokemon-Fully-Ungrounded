# Natief raster terughalen: pitch 5,12 px (fourier op randsterkte, x en y gelijk), fase uit dezelfde meting.
# Elke cel = mediaan van het binnenste 3x3 van de cel. Niets getekend.
import sys; from PIL import Image; import numpy as np
SRC='../../referenties/model_welp_gekozen.png'
a=np.asarray(Image.open(SRC).convert('RGB')).astype(float)
P=5.12; res={}
for ax in (1,0):
    g=np.abs(np.diff(a,axis=ax)).sum(axis=2).sum(axis=1-ax); g=g-g.mean()
    ph=np.exp(2j*np.pi*np.arange(len(g))/P); res[ax]=(-np.angle((g*ph).sum())*P/(2*np.pi))%P+1  # grens tussen pixel i en i+1
ox,oy=res[1],res[0]; print('fase x %.2f y %.2f'%(ox,oy))
def cells(o,n): 
    s=o-P
    while s>0: s-=P
    return [s+k*P for k in range(int((n-s)/P)+1)]
cx,cy=cells(ox,1024),cells(oy,1024)
H,W=len(cy)-1,len(cx)-1; out=np.zeros((H,W,3),'uint8')
for j in range(H):
    for i in range(W):
        mx,my=cx[i]+P/2,cy[j]+P/2
        x0,x1=max(0,int(round(mx-1.5))),min(1024,int(round(mx+1.5)))
        y0,y1=max(0,int(round(my-1.5))),min(1024,int(round(my+1.5)))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
# bijsnijden op figuur + 2 rand
m=out.min(axis=2)<215; yy,xx=np.where(m)
out=out[yy.min()-2:yy.max()+3, xx.min()-2:xx.max()+3]
print('figuur', xx.max()-xx.min()+1,'x',yy.max()-yy.min()+1)
Image.fromarray(out).save('natief.png')
Image.fromarray(out).resize((out.shape[1]*6,out.shape[0]*6),Image.NEAREST).save('natief_6x.png')
