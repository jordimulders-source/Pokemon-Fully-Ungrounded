# Natief raster van de Claydol-modellen (Gemini 1024). Kopie van gereedschap/natief.py; pitch per plaatje gezocht (9,6-10,8).
import numpy as np, sys; from PIL import Image
def fit(e,lo=9.6,hi=10.8):
    best=(0,0,0)
    for p in np.arange(lo,hi,0.004):
        for ph in np.arange(0,p,0.1):
            idx=np.round(np.arange(ph,len(e),p)).astype(int); idx=idx[idx<len(e)]
            s=e[idx].mean()
            if s>best[0]: best=(s,p,ph)
    return best
def natief(IN,grid=None):
    a=np.asarray(Image.open(IN).convert('RGB')).astype(int); g=a.mean(2)
    if grid is None:
        dx=np.abs(np.diff(g,axis=1)).sum(0); dy=np.abs(np.diff(g,axis=0)).sum(1)
        _,px,phx=fit(dx); _,py,phy=fit(dy); grid=(px,phx,py,phy)
    px,phx,py,phy=grid
    xs=np.arange(phx+0.5+px/2,1024,px); ys=np.arange(phy+0.5+py/2,1024,py)
    out=np.zeros((len(ys),len(xs),3),'uint8')
    for j,y in enumerate(ys):
        for i,x in enumerate(xs):
            y0,y1=int(max(0,y-1.5)),int(min(1024,y+2.5)); x0,x1=int(max(0,x-1.5)),int(min(1024,x+2.5))
            out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
    return out,grid
if __name__=='__main__':
    for n in ['r5','r3','r6']:
        out,gr=natief('gemini/claydol_%s.png'%n)
        print(n,'pitch x %.3f fase %.2f | y %.3f fase %.2f'%gr, out.shape)
        Image.fromarray(out).save('claydol_model/natief_%s.png'%n)
