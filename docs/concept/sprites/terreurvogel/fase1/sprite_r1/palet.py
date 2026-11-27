# k-means (3 tinten) per groep op de natieve modelpixels -> voorstel paletwaarden
import numpy as np; from lib import *
for g in (2,3,4,5,6,7):
    px=N[GR==g].astype(float); k=3 if g!=7 else 2
    if len(px)<k: print(g,len(px)); continue
    c=np.percentile(px.mean(1),np.linspace(15,85,k))
    cen=np.array([px[np.argmin(abs(px.mean(1)-v))] for v in c])
    for _ in range(30):
        lab=np.argmin(((px[:,None]-cen[None])**2).sum(2),1)
        cen=np.array([px[lab==i].mean(0) if (lab==i).any() else cen[i] for i in range(k)])
    o=np.argsort(cen.mean(1))
    print(GNAAM[g],len(px),[tuple(cen[i].round().astype(int)) for i in o],[int((lab==i).sum()) for i in o])
