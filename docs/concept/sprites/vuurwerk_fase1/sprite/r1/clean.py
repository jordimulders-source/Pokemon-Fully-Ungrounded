# Technische opschoning van de kale reductie (geen tekenwerk):
# 1) losse 1-px-ruis buiten de figuur weg (alleen pixels zonder 4-buur; sterretjes blijven tot de bovenlaag);
# 2) ontkorrelen: vulpixel zonder gelijke 4-buur -> meest voorkomende tint van dezelfde kleurgroep in de 8-buurt;
# 3) buitenlijn 1 px: silhouetrandpixel -> selout (licht, boven/links: d roze, b creme) of zwart-paars (#) aan de schaduwkant.
import numpy as np, sys
from txt import CH, dump
a=np.load('kaal.npy').copy(); H,W=a.shape
I={c:i for i,c in enumerate(CH)}
G={}
for c in 'smlL': G[I[c]]='roze'
for c in 'Mp': G[I[c]]='paars'
for c in 'Yt': G[I[c]]='geel'
for c in 'ckbw': G[I[c]]='creme'
LIJN={I['#'],I['E'],I['d']}
def nb(y,x,r=1):
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W: yield y+dy,x+dx
log=[]
# 2) ontkorrelen (2 passes)
for _ in range(2):
    b=a.copy()
    for y in range(H):
        for x in range(W):
            v=a[y,x]
            if v not in G or v==I['w']: continue
            four=[a[yy,xx] for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1)) if 0<=yy<H and 0<=xx<W]
            if v in four: continue
            cnt={}
            for yy,xx in nb(y,x):
                u=a[yy,xx]
                if G.get(u)==G[v] and u!=v: cnt[u]=cnt.get(u,0)+1
            if cnt:
                u=max(cnt,key=cnt.get); b[y,x]=u; log.append(('korrel',y,x,CH[v],CH[u]))
    a=b
np.save('schoon0.npy',a)
print(len(log),'ontkorreld'); dump(a)
