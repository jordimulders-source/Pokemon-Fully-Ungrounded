# Haalt het eigen pixelraster van het Gemini-model terug (pitch ~5.6 px) -> natief.png
from PIL import Image; import numpy as np
a=np.asarray(Image.open('referenties/model_v4.png').convert('RGB')).astype(int)
gx=np.abs(np.diff(a,axis=1)).sum(axis=2).sum(axis=0).astype(float)   # randsterkte per kolomgrens
gy=np.abs(np.diff(a,axis=0)).sum(axis=2).sum(axis=1).astype(float)
def fit(g):
    best=None
    for p in np.arange(5.3,5.95,0.005):
        for ph in np.arange(0,p,0.25):
            idx=np.round(np.arange(ph,len(g)-1,p)).astype(int); idx=idx[idx<len(g)]
            s=g[idx].mean()
            if best is None or s>best[0]: best=(s,p,ph)
    return best
bx=fit(gx); by=fit(gy); print('x',bx,'y',by)
px,phx=bx[1],bx[2]; py,phy=by[1],by[2]
xs=np.arange(phx+1+px/2,1024,px); ys=np.arange(phy+1+py/2,1024,py)
W,H=len(xs),len(ys); out=np.zeros((H,W,3),'uint8')
for j,y in enumerate(ys):
    for i,x in enumerate(xs):
        y0,y1=int(max(0,y-1)),int(min(1024,y+2)); x0,x1=int(max(0,x-1)),int(min(1024,x+2))
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
im=Image.fromarray(out); im.save('sprite3/natief.png'); print(W,H)
g=np.asarray(im.convert('L')); yy,xx=np.where(g<215); print('bbox',xx.min(),xx.max(),yy.min(),yy.max())
im.crop((xx.min()-2,yy.min()-2,xx.max()+3,yy.max()+3)).resize(((xx.max()-xx.min()+5)*6,(yy.max()-yy.min()+5)*6),Image.NEAREST).save('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/edb145cf-71a4-55a5-8012-167050278397/scratchpad/nat.png')
