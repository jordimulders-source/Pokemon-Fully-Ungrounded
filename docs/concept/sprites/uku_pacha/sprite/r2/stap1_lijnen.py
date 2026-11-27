# Uku Pacha r2 stap 1: model -> 64 px met DOORLOPENDE lijnen.
# Elke lijncel van het model (klassen 0-4) wordt naar spriteruimte geprojecteerd en met haar
# 8-buren verbonden (Bresenham), zodat lijnen niet in streepjes breken. Vlakken = oppervlak-
# gewogen meerderheid van de niet-lijnklassen in de voetafdruk. Silhouet = identiek aan r1.
import numpy as np, geom
from PIL import Image
N=geom.N; BG=geom.BG
idx=np.load('nat_idx.npy').copy()
r,g,b=N[...,0],N[...,1],N[...,2]
idx[(r>170)&(g>150)&(r>b+60)]=16          # geel oog
idx[(r>g+12)&(b>g+25)]=17                 # paarse tong
idx[geom.WITDETAIL]=18                    # tanden / glans
idx[BG]=-1
LIJN=set([0,1,2,3,4])
np.save('cls.npy',idx)
# silhouet (zelfde regel als r1: >50% achtergrond = transparant)
S=np.full((64,64),-1)
votes=np.zeros((64,64,19))
for j in range(64):
  for i in range(64):
    x0,x1,y0,y1=geom.s2n(i,j)
    if x1<=0 or y1<=0 or x0>=100 or y0>=100: continue
    acc=np.zeros(20)
    for cy in range(max(0,int(y0)),min(100,int(np.ceil(y1)))):
      for cx in range(max(0,int(x0)),min(100,int(np.ceil(x1)))):
        a=(min(x1,cx+1)-max(x0,cx))*(min(y1,cy+1)-max(y0,cy))
        if a>0: acc[idx[cy,cx]+1 if idx[cy,cx]>=0 else 0]+=a
    if acc.sum()==0 or acc[0]/acc.sum()>0.5: continue
    S[j,i]=99; votes[j,i]=acc[1:20]
# lijnen
L=np.full((64,64),-1)
def put(i,j,c):
    if 0<=i<64 and 0<=j<64 and S[j,i]>=0:
        if L[j,i]<0 or c<L[j,i]: L[j,i]=c
def proj(x,y):
    sx,sy=geom.n2s(x+0.5,y+0.5); return int(np.floor(sx)),int(np.floor(sy))
for y in range(100):
  for x in range(100):
    c=idx[y,x]
    if c not in LIJN: continue
    i0,j0=proj(x,y); put(i0,j0,c)
    for dy,dx in ((0,1),(1,0),(1,1),(1,-1)):
      yy,xx=y+dy,x+dx
      if 0<=yy<100 and 0<=xx<100 and idx[yy,xx] in LIJN:
        if dy and dx and (idx[y,xx] in LIJN or idx[yy,x] in LIJN): continue  # diagonaal al gedekt
        i1,j1=proj(xx,yy)
        n=max(abs(i1-i0),abs(j1-j0))
        for t in range(1,n+1):
          put(round(i0+(i1-i0)*t/n),round(j0+(j1-j0)*t/n),max(c,idx[yy,xx]) if False else min(c,idx[yy,xx]))
# vlakken
V=np.full((64,64),-1)
for j in range(64):
  for i in range(64):
    if S[j,i]<0: continue
    v=votes[j,i].copy(); v[list(LIJN)]=0
    if v.sum()>0: V[j,i]=int(np.argmax(v))
# lege vlakpixels (voetafdruk alleen lijn): dichtstbijzijnde vlakklasse in het model
for j,i in zip(*np.where((S>=0)&(V<0))):
    x0,x1,y0,y1=geom.s2n(i,j); cx,cy=(x0+x1)/2,(y0+y1)/2
    best=None
    for rr in range(1,6):
      for yy in range(int(cy)-rr,int(cy)+rr+1):
        for xx in range(int(cx)-rr,int(cx)+rr+1):
          if 0<=yy<100 and 0<=xx<100 and idx[yy,xx]>=5:
            d=(yy-cy)**2+(xx-cx)**2
            if best is None or d<best[0]: best=(d,idx[yy,xx])
      if best: break
    V[j,i]=best[1]
np.save('S.npy',S); np.save('L.npy',L); np.save('V.npy',V)
print('lijnpx',(L>=0).sum(),'silhouet',(S>=0).sum())
