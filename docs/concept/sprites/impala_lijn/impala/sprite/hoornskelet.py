# Middellijn (skelet) van elke modelhoorn: hoornvlak (seg 14 = rechterhoorn, 49 = linkerhoorn) 4x verkleind,
# Zhang-Suen-verdunning, langste pad. Uit: hoornskelet.json met per hoorn de punten in spritecelcoordinaten
# (u = (X - x0)/p, v = (Y - y0)/p; pixel i heeft zijn midden op i+0.5), van voet (bij de kop) naar punt.
import numpy as np, json
from collections import deque
seg=np.load('seg.npz')['a']; km=json.load(open('kaal_meta.json')); x0,y0,p=km['x0'],km['y0'],km['p']
def thin(B):
    B=B.copy().astype(np.uint8)
    while True:
        ch=False
        for st in (0,1):
            P=np.pad(B,1); n=[P[:-2,1:-1],P[:-2,2:],P[1:-1,2:],P[2:,2:],P[2:,1:-1],P[2:,:-2],P[1:-1,:-2],P[:-2,:-2]]  # p2..p9
            Bn=sum(n.astype(int) if False else x.astype(int) for x in n)
            A=sum(((n[k]==0)&(n[(k+1)%8]==1)).astype(int) for k in range(8))
            if st==0: c=(n[0]*n[2]*n[4]==0)&(n[2]*n[4]*n[6]==0)
            else:     c=(n[0]*n[2]*n[6]==0)&(n[0]*n[4]*n[6]==0)
            d=(B==1)&(Bn>=2)&(Bn<=6)&(A==1)&c
            if d.any(): B[d]=0; ch=True
        if not ch: return B
def langste(S):
    pts=set(zip(*np.nonzero(S)))
    def bfs(s):
        dist={s:0}; prev={s:None}; q=deque([s])
        while q:
            a=q.popleft()
            for dy in(-1,0,1):
                for dx in(-1,0,1):
                    b=(a[0]+dy,a[1]+dx)
                    if b in pts and b not in dist: dist[b]=dist[a]+1; prev[b]=a; q.append(b)
        e=max(dist,key=dist.get); return e,prev
    e1,_=bfs(next(iter(pts))); e2,prev=bfs(e1)
    path=[]; c=e2
    while c is not None: path.append(c); c=prev[c]
    return path
out={}
for naam,sid in (('rechts',14),('links',49)):
    M=(seg==sid); D=M.reshape(256,4,256,4).mean((1,3))>0.5
    path=langste(thin(D))
    P=[((x*4+2-x0)/p,(y*4+2-y0)/p) for y,x in path]
    if P[0][1]<P[-1][1]: P=P[::-1]        # voet (laagste punt, bij de kop) eerst, punt (bovenaan) laatst
    out[naam]=P[::2]
    print(naam,len(P),'voet',np.round(P[0],1),'punt',np.round(P[-1],1))
json.dump(out,open('hoornskelet.json','w'))
