"""Dekking per icoonpixel: aandeel frontpixels (alle onderdelen, eigen transformatie) in het bronvak; max over de onderdelen.
Gebruikt door poets.py voor de regel 'rond' (randpixels met twijfeldekking 0,30-0,60 kiezen zodat de omtrek in trapjes loopt)."""
import numpy as np
def dekking(names,lab,bron,TR,shape=(32,32)):
    cov=np.zeros(shape)
    for n in set(names):
        ids=[i for i,m in enumerate(names) if m==n]; pm=np.isin(lab,ids)
        for Y in range(shape[0]):
            for X in range(shape[1]):
                (sx,sy),k=bron(X-TR[0],Y-TR[1],n); k=np.broadcast_to(k,(2,))
                x0,y0=int(np.floor(sx)),int(np.floor(sy)); x1,y1=int(np.ceil(sx+k[0])),int(np.ceil(sy+k[1]))
                if x1<=0 or y1<=0 or x0>=64 or y0>=64: continue
                x0,y0=max(0,x0),max(0,y0); x1,y1=min(64,x1),min(64,y1)
                sel=pm[y0:y1,x0:x1]
                if sel.size: cov[Y,X]=max(cov[Y,X],sel.mean())
    return cov
