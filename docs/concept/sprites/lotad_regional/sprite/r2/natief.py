# Haalt het natieve pixelraster van het model r8/gemini_r8_1.png terug -> natief.png (+ r1 -> natief_r1.png)
# Pitch gemeten met een kamscore op de randsterkte: 8,525 scoort met fase 8,0 en 3,75 even hoog -> echte cel ±4,26 px.
import numpy as np, sys; from PIL import Image
def natief(IN,OUT):
    a=np.asarray(Image.open(IN).convert('RGB')).astype(int); g=a.mean(2)
    dx=np.abs(np.diff(g,axis=1)).sum(0); dy=np.abs(np.diff(g,axis=0)).sum(1)
    def fit(e):
        best=(0,0,0)
        for p in np.arange(4.20,4.32,0.002):
            for ph in np.arange(0,p,0.05):
                idx=np.round(np.arange(ph,len(e)-1,p)).astype(int); s=e[idx].mean()
                if s>best[0]: best=(s,p,ph)
        return best
    _,px,phx=fit(dx); _,py,phy=fit(dy)
    print(IN,'pitch x %.3f fase %.2f | y %.3f fase %.2f'%(px,phx,py,phy))
    H,W=g.shape
    xs=np.arange(phx+0.5+px/2,W-1,px); ys=np.arange(phy+0.5+py/2,H-1,py)
    out=np.zeros((len(ys),len(xs),3),'uint8')
    for j,y in enumerate(ys):
        for i,x in enumerate(xs):
            y0,y1=int(max(0,y-1)),int(min(H,y+2)); x0,x1=int(max(0,x-1)),int(min(W,x+2))
            out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
    Image.fromarray(out).save(OUT)
    m=out.min(2)<225; yy,xx=np.where(m); print(' natief',out.shape[1],out.shape[0],'figuur x',xx.min(),xx.max(),'y',yy.min(),yy.max())
    return px,phx,py,phy
D='../../'
natief(D+'r8/gemini_r8_1.png','natief.png')
natief(D+'r1/gemini_r1.png','natief_r1.png')
