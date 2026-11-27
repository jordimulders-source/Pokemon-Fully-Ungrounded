# Binnenlijnen in het natieve raster weghalen (niet tekenen): lijnpixels (helderheid < drempel) in een zone,
# 8-samenhangende stukken kleiner dan minpx worden vervangen door de mediaan van de omliggende niet-lijn-zandpixels.
import numpy as np; import materiaal as mt; import schoon
def lijnmasker(a,drempel=100):
    M,L=mt.kaart(a); return (L<drempel)&(M!=0)&(M!=3), M, L
def weg(a, zone, minpx, drempel=100, randvrij=True):
    a=a.copy(); lm,M,L=lijnmasker(a,drempel)
    H,W=lm.shape; bg=(M==0)
    for c in schoon.comps(lm&zone):
        if len(c)>=minpx: continue
        if randvrij and any(bg[max(0,y-1):y+2,max(0,x-1):x+2].any() for y,x in c): continue
        for y,x in c:
            win=a[max(0,y-2):y+3,max(0,x-2):x+3].reshape(-1,3); wl=L[max(0,y-2):y+3,max(0,x-2):x+3].ravel(); wm=M[max(0,y-2):y+3,max(0,x-2):x+3].ravel()
            ok=(wl>=drempel)&(wm==2)
            if ok.any(): a[y,x]=np.median(win[ok],axis=0)
    return a
def toon_comps(a,zone,drempel=100):
    lm,M,L=lijnmasker(a,drempel); return [(len(c),c[0]) for c in schoon.comps(lm&zone)]
