# Natief raster terughalen uit een Gemini-beeld: python3 natief.py in.png uit.png [pmin pmax]
import sys,numpy as np; from PIL import Image
IN,OUT=sys.argv[1],sys.argv[2]; pmin,pmax=(float(sys.argv[3]),float(sys.argv[4])) if len(sys.argv)>4 else (6,20)
a=np.asarray(Image.open(IN).convert('RGB')).astype(int); g=a.mean(2); H,W=g.shape
dx=np.abs(np.diff(g,axis=1)).sum(0); dy=np.abs(np.diff(g,axis=0)).sum(1)
def fit(e):
    best=(0,0,0)
    for p in np.arange(pmin,pmax,0.01):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(e),p)).astype(int); idx=idx[idx<len(e)]
            s=e[idx].mean()-e.mean()*0  
            # straf voor halve pitch: ook midden tussen randen meten
            mid=np.round(np.arange(ph+p/2,len(e),p)).astype(int); mid=mid[mid<len(e)]
            s=e[idx].mean()-e[mid].mean()
            if s>best[0]: best=(s,p,ph)
    return best
_,px,phx=fit(dx); _,py,phy=fit(dy)
print('pitch x %.3f fase %.2f | pitch y %.3f fase %.2f'%(px,phx,py,phy))
xs=np.arange(phx+0.5+px/2,W,px); ys=np.arange(phy+0.5+py/2,H,py)
out=np.zeros((len(ys),len(xs),3),'uint8'); r=max(1,int(px/4))
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-r)),int(min(H,y+r+1)); x0,x1=int(max(0,x-r)),int(min(W,x+r+1))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT)
m=out.min(2)<215; yy,xx=np.where(m); print('natief',out.shape[1],out.shape[0],'bbox x',xx.min(),xx.max(),'y',yy.min(),yy.max(),'=',xx.max()-xx.min()+1,'x',yy.max()-yy.min()+1)
