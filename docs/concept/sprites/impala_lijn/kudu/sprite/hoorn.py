# Hoornskelet voor de kudu (zoals impala/sprite/hoornskelet.py): hoornmasker = staalpixels + aangrenzende modellijn boven y340,
# 4x verkleind, Zhang-Suen, langste pad per hoorn; halve breedte (incl. lijn) per punt uit de afstandstransformatie. Spritecoordinaten.
import numpy as np, json
from collections import deque
from scipy import ndimage as nd
def thin(B):
    B=B.copy().astype(np.uint8)
    while True:
        ch=False
        for st in (0,1):
            P=np.pad(B,1); n=[P[:-2,1:-1],P[:-2,2:],P[1:-1,2:],P[2:,2:],P[2:,1:-1],P[2:,:-2],P[1:-1,:-2],P[:-2,:-2]]
            Bn=sum(x.astype(int) for x in n); A=sum(((n[k]==0)&(n[(k+1)%8]==1)).astype(int) for k in range(8))
            c=((n[0]*n[2]*n[4]==0)&(n[2]*n[4]*n[6]==0)) if st==0 else ((n[0]*n[2]*n[6]==0)&(n[0]*n[4]*n[6]==0))
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
    e1,_=bfs(next(iter(pts))); e2,prev=bfs(e1); path=[]; c=e2
    while c is not None: path.append(c); c=prev[c]
    return path
def skelet(Zp,x0,y0,p):
    st=(Zp==2); yy=np.mgrid[:1024,:1024][0]
    hm=(st|(nd.binary_dilation(st,iterations=8)&(Zp==-1)))&(yy<340)
    hm=nd.binary_closing(hm,iterations=3)
    lab,n=nd.label(st&(yy<340)); sz=nd.sum(st,lab,range(1,n+1)); big=np.argsort(sz)[-2:]+1
    big=sorted(big,key=lambda k:np.nonzero(lab==k)[1].mean())
    out={}
    for k in big:
        comp=nd.binary_dilation(lab==k,iterations=8)&hm
        dt=nd.distance_transform_edt(comp)
        D=comp.reshape(256,4,256,4).mean((1,3))>0.5
        path=langste(thin(D))
        P=np.array([((x*4+2-x0)/p,(y*4+2-y0)/p) for y,x in path])
        if P[0][1]<P[-1][1]: P=P[::-1]          # voet eerst
        Q=P.copy()
        for i in range(len(P)): a,b=max(0,i-6),min(len(P),i+7); Q[i]=P[a:b].mean(0)
        Q[0],Q[-1]=P[0],P[-1]
        hw=[float(dt[min(1023,int(y0+v*p)),min(1023,int(x0+u*p))])/p for u,v in Q]
        naam='links' if k==big[0] else 'rechts'
        out[naam]={'pts':Q[::2].tolist(),'hw':hw[::2]}
    return out
