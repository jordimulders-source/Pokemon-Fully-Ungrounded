# Stekel-/klauwpunten uit het model: uitsteeksels = silhouet min opening (schijf r); per component de punt (verst van de kern,
# BFS binnen de figuur) en de voet (dichtstbijzijnde kernpixel). Levert lijst (punt, voet, grootte) in natieve coordinaten.
import numpy as np
from collections import deque
def schijf(r): return [(dy,dx) for dy in range(-r,r+1) for dx in range(-r,r+1) if dy*dy+dx*dx<=r*r]
def erodeer(m,r):
    p=np.pad(m,r); out=np.ones_like(m)
    for dy,dx in schijf(r): out&=p[r+dy:r+dy+m.shape[0],r+dx:r+dx+m.shape[1]]
    return out
def dilateer(m,r):
    p=np.pad(m,r); out=np.zeros_like(m)
    for dy,dx in schijf(r): out|=p[r+dy:r+dy+m.shape[0],r+dx:r+dx+m.shape[1]]
    return out
def punten(g,r=6,minsize=12):
    from lijnen import componenten
    FIG=g>0; KERN=dilateer(erodeer(FIG,r),r); U=FIG&~KERN
    H,W=g.shape; dist=np.full((H,W),-1); q=deque()
    for y,x in zip(*np.where(KERN)): dist[y,x]=0; q.append((y,x))
    voet=np.zeros((H,W,2),int)
    for y,x in zip(*np.where(KERN)): voet[y,x]=(y,x)
    while q:
        y,x=q.popleft()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and FIG[yy,xx] and dist[yy,xx]<0:
                dist[yy,xx]=dist[y,x]+1; voet[yy,xx]=voet[y,x]; q.append((yy,xx))
    lab,size=componenten(U); out=[]
    for n,s in size.items():
        if s<minsize: continue
        ys,xs=np.where(lab==n); k=np.argmax(dist[ys,xs]); ty,tx=ys[k],xs[k]
        out.append(((tx,ty),tuple(voet[ty,tx][::-1]),s,dist[ty,tx]))
    return out
if __name__=='__main__':
    from groepen import laad
    a,lum,g=laad()
    for p in sorted(punten(g)): print(p)
