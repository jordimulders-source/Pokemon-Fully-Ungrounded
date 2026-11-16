import numpy as np
from gio import from_txt, to_txt, CH
from r2_rijen import R2
I={c:k for k,c in enumerate(CH)}
G=from_txt('r1.txt'); m=np.load('mask_r1.npy'); ice=np.load('ice_r1.npy')
for y,(x0,s) in R2.items():
    assert x0+len(s)-1==np.where(m[y])[0].max(), (y,x0+len(s)-1,np.where(m[y])[0].max())
    for k,c in enumerate(s): G[y,x0+k]=I[c]
# zachte selout gas: L aan de lichtkant, M alleen aan de schaduwkant (uitgang alleen rechts/onder)
for y in range(64):
    for x in range(64):
        if not m[y,x] or ice[y,x] or CH[G[y,x]] in 'Kij': continue
        out=[(yy,xx) for yy,xx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)] if not m[yy,xx]]
        if out: G[y,x]=I['M'] if all(yy>y or xx>x for yy,xx in out) else I['L']
to_txt(G,'r2_stapA.txt')
