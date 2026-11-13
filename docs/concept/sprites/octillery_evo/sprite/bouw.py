# bouw.py: onderlaag-bouwer. silhouet + klasse uit model, tonen uit modelhelderheid, lijnen als polylijnen.
import cfg,numpy as np
CH=cfg.CH
def idx(ch): return CH.index(ch)
def bres(p,q):
    (x0,y0),(x1,y1)=p,q; pts=[]; dx=abs(x1-x0); dy=-abs(y1-y0); sx=1 if x0<x1 else -1; sy=1 if y0<y1 else -1; e=dx+dy
    while True:
        pts.append((x0,y0))
        if (x0,y0)==(x1,y1): break
        e2=2*e
        if e2>=dy: e+=dy; x0+=sx
        if e2<=dx: e+=dx; y0+=sy
    return pts
def poly(G,pts,ch,only=None):
    for p,q in zip(pts,pts[1:]):
        for x,y in bres(p,q):
            if only is None or G[y,x]!=0: G[y,x]=idx(ch)
def toon_rood(l):
    return 6 if l>=150 else 5 if l>=118 else 4 if l>=96 else 3 if l>=79 else 2
def toon_roze(l):
    return 9 if l>=165 else 8 if l>=125 else 7
def basis():
    g=cfg.read('r1/glad.txt'); L=np.load('lum.npy')
    m=g>0; G=np.zeros((64,64),int); K=np.zeros((64,64),int)  # K: 0 rood 1 roze 2 geel 3 grijs
    for y in range(64):
        for x in range(64):
            if not m[y,x]: continue
            v=g[y,x]
            k=1 if v in (7,8,9) else 2 if v in (10,11,12) else 3 if v in (13,14) else 0
            K[y,x]=k; l=L[y,x] if L[y,x] else 60
            G[y,x]={0:toon_rood,1:toon_roze}.get(k,lambda l:v)(l) if k in (0,1) else v
    return G,K,m
def glad(G,K,n=2):
    for _ in range(n):
        H=G.copy()
        for y in range(1,63):
            for x in range(1,63):
                if G[y,x]==0: continue
                w=[G[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if G[yy,xx]!=0 and K[yy,xx]==K[y,x]]
                c=np.bincount(w,minlength=16)
                if c[G[y,x]]<=2 and c.max()>=4: H[y,x]=c.argmax()
        G[:]=H
def omlijn(G,m,lit='f'):
    pad=np.pad(m,1)
    for y in range(64):
        for x in range(64):
            if not m[y,x]: continue
            up=not pad[y,x+1]; dn=not pad[y+2,x+1]; lf=not pad[y+1,x]; rt=not pad[y+1,x+2]
            if up or dn or lf or rt:
                G[y,x]=idx(lit) if ((up or lf) and not (dn or rt)) else 1
