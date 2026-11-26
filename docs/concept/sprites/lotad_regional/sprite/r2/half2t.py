# Kale reductie v2: exact 2x2 op de toonkaart (tonen.py). Lijnregels als half2.py; tint = meest voorkomende toon van het
# hoofdmateriaal in het blok (gelijkspel: de toon het dichtst bij de gemiddelde helderheid). Niets getekend.
import sys, numpy as np
from tonen import toonkaart; from gemeen import opslaan
c,t,L,oog=toonkaart(); H,W=c.shape
MINL=6
def clusters(m):
    lab=np.zeros(m.shape,int); n=0
    for y in range(m.shape[0]):
        for x in range(m.shape[1]):
            if m[y,x] and not lab[y,x]:
                n+=1; st=[(y,x)]
                while st:
                    y_,x_=st.pop()
                    if 0<=y_<m.shape[0] and 0<=x_<m.shape[1] and m[y_,x_] and not lab[y_,x_]:
                        lab[y_,x_]=n; st+=[(y_+dy,x_+dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
    return lab,n
LIJN={2:2,3:2,4:6,5:6,6:6}   # lijntoon per materiaal
lt=np.zeros_like(t); 
for m,k in LIJN.items(): lt[(c==m)&(t==k)]=1
blk=(c==1)|(lt==1); lab,n=clusters(blk); grootte=np.bincount(lab.ravel()); lang=blk&(grootte[lab]>=MINL)
def reduceer(OY,OX):
    h=(H-OY)//2; w=(W-OX)//2; o=np.zeros((h,w),int); mat=np.zeros((h,w),int); nb=np.zeros((h,w),int); nl=np.zeros((h,w),int)
    oogb=np.zeros((h,w),bool); nz=np.zeros((h,w),int)
    def lijnkleur(j,i):
        if nz[j,i]>=1 or mat[j,i]<2: return 1
        return LIJN[mat[j,i]]
    for j in range(h):
        for i in range(w):
            sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2)); cc=c[sl]; tt=t[sl]
            if (cc>0).sum()<2: continue
            nb[j,i]=blk[sl].sum(); nz[j,i]=(cc==1).sum(); nl[j,i]=lang[sl].sum(); oogb[j,i]=oog[sl].any()
            f=[(cc==k).sum() for k in range(2,7)]
            if max(f)==0: o[j,i]=1; mat[j,i]=1; continue
            m=2+int(np.argmax(f)); mat[j,i]=m
            v,k=np.unique(tt[cc==m],return_counts=True)
            beste=v[k==k.max()]
            o[j,i]=beste[0] if len(beste)==1 else beste[len(beste)//2]
    fig=o>0
    for j in range(h):
        for i in range(w):
            if not fig[j,i]: continue
            if nb[j,i]>=2: o[j,i]=lijnkleur(j,i); continue
            if nl[j,i]==1:
                rand=any(not(0<=y<h and 0<=x<w) or not fig[y,x] for y,x in ((j-1,i),(j+1,i),(j,i-1),(j,i+1)))
                buren=sum(1 for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=j+dy<h and 0<=i+dx<w and nl[j+dy,i+dx]>=1)
                if rand or buren>=2: o[j,i]=lijnkleur(j,i)
    return o,mat,oogb
def plaats(o,*rest):
    ys,xs=np.where(o>0); y0,y1,x0_,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1; hh,ww=y1-y0,x1-x0_
    X0=(64-ww)//2; Y0=63-hh; uit=[]
    for arr in (o,)+rest:
        f=np.zeros((64,64),arr.dtype); f[Y0:63,X0:X0+ww]=arr[y0:y1,x0_:x1]; uit.append(f)
    return uit,(y0,x0_,Y0,X0)
if __name__=='__main__':
    for OY in (0,1):
        for OX in (0,1):
            o,mat,oogb=reduceer(OY,OX); (full,*_),_=plaats(o,mat,oogb)
            opslaan(full,'kaal3_%d%d.png'%(OY,OX))
            ys,xs=np.where(full>0); print(OY,OX,'maat',xs.max()-xs.min()+1,ys.max()-ys.min()+1,'px',(full>0).sum(),'zwart',(full==1).sum())
