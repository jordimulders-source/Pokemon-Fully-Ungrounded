# Haalt het natieve raster (pitch ~4,6) van Jordi's vuurwerkvel terug voor de roze barst midden onder (b2) en de grote roze
# linksonder (b1), en deelt elke pixel in: 0 leeg, 1 donker (gedimd magenta), 2 midden (roze), 3 fel (lichtroze/wit).
import numpy as np, json; from PIL import Image
a=np.asarray(Image.open('../../referenties/vuurwerk_pixelart_jordi.png').convert('RGB')).astype(float)
bgc=np.array([0,12,37.])
def raster(x0,y0,x1,y1,p=4.6):
    best=None
    for phx in np.arange(0,p,0.2):
        for phy in np.arange(0,p,0.2):
            xs=np.arange(x0+phx,x1,p); ys=np.arange(y0+phy,y1,p)
            # scherpte: variantie binnen cellen klein
            v=0
            for y in ys[:-1]:
                for x in xs[:-1]:
                    blk=a[int(y)+1:int(y+p)-1,int(x)+1:int(x+p)-1]; v+=blk.std(axis=(0,1)).sum()
            if best is None or v<best[0]: best=(v,phx,phy)
    _,phx,phy=best; xs=np.arange(x0+phx,x1-p,p); ys=np.arange(y0+phy,y1-p,p)
    g=np.zeros((len(ys),len(xs)),int); col=np.zeros((len(ys),len(xs),3))
    for j,y in enumerate(ys):
        for i,x in enumerate(xs):
            c=np.median(a[int(y+p/2)-1:int(y+p/2)+2,int(x+p/2)-1:int(x+p/2)+2].reshape(-1,3),0); col[j,i]=c
            d=np.abs(c-bgc).sum(); L=c@[0.299,0.587,0.114]
            g[j,i]=0 if d<45 else (1 if L<70 else (2 if L<150 else 3))
    return g,col
out={}
for naam,box in {'b2':(268,505,402,642),'b1':(40,450,222,625),'b3':(42,42,142,138)}.items():   # b3 = kleine barst linksboven (oranje)
    g,col=raster(*box); out[naam]=g.tolist()
    print(naam,g.shape)
    for r in g: print(''.join(' .o#'[v] for v in r))
json.dump(out,open('ref_burst.json','w'))
