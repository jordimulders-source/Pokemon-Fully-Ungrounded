# stap 1: afschuining 2 px dik bij stenen >= 6 px (alleen tweede pixelrij toevoegen aan k7)
import sys, numpy as np
sys.path.insert(0,'../k1'); sys.path.insert(0,'../k7')
from gereedschap import *
import k7b
a6,pal=laad('../k6/tempel.png'); a7,_=laad('../k7/tempel.png'); H,W=a6.shape; k7b.a0=a7
BLOK={0,1,2,7,12,10,11,8,9,13}
STAP=[3,4,5,6,15]
vast=np.zeros_like(a6,bool)
for (x0,y0,x1,y1) in OGEN: vast[y0:y1+1,x0:x1+1]=True
vast|=deurmasker(a6); vast[45:61,13:16]=True; vast[45:61,22:26]=True
vast[37:44,13:30]=True   # gezichtsveld apart met de hand
isl=np.isin(a6,[7,1])
def blk(x,y): return not(0<=x<W and 0<=y<H) or a6[y,x] in BLOK
def run(x,y,dx,dy):
    n=0
    while not blk(x+dx*n,y+dy*n): n+=1
    return n
def strepen(m):
    out=[];x=0
    while x<len(m):
        if m[x]:
            s=x
            while x<len(m) and m[x]: x+=1
            out.append((s,x))
        else: x+=1
    return out
L=np.zeros_like(a6,bool); D=L.copy()
for y in range(H):
    for s,e in strepen(isl[y]):
        n=e-s
        if n<3: continue
        for u in range(s,s+int(np.ceil(2*n/3)) if n>=5 else e):
            if y+2<H and run(u,y+1,0,1)>=6: L[y+2,u]=True
        for u in range(s+n//3 if n>=5 else s,e):
            if y-2>=0 and run(u,y-1,0,-1)>=6: D[y-2,u]=True
for x in range(W):
    for s,e in strepen(isl[:,x]):
        n=e-s
        if n<3: continue
        for v in range(s,s+int(np.ceil(2*n/3)) if n>=5 else e):
            if x+2<W and run(x+1,v,1,0)>=6: L[v,x+2]=True
        for v in range(s+n//3 if n>=5 else s,e):
            if x-2>=0 and run(x-1,v,-1,0)>=6: D[v,x-2]=True
a=a7.copy()
for y in range(H):
    for x in range(W):
        T=a6[y,x]
        if vast[y,x] or T not in STAP or T==15 or a7[y,x]!=a6[y,x]: continue
        # alleen als de eerste rij (richting voeg) al afgeschuind is in k7, zodat het 2 px wordt
        i=STAP.index(T)
        if L[y,x] and not D[y,x] and i>0:
            nb=[a7[y-1,x],a7[y,x-1]]
            if any(c==STAP[i-1] for c in nb): a[y,x]=STAP[i-1]
        elif D[y,x] and not L[y,x] and i<4:
            nb=[a7[y+1,x],a7[y,x+1]]
            if any(c==STAP[i+1] for c in nb): a[y,x]=STAP[i+1]
# vlakcontrole zoals k7
for y in range(H):
    for x in range(W):
        if a[y,x]==a7[y,x]: continue
        blok=[c for c in a6[max(0,y-3):y+4,max(0,x-3):x+4].ravel() if c in STAP]
        base=np.bincount(blok,minlength=16).argmax()
        if abs(STAP.index(a[y,x])-STAP.index(base))>1: a[y,x]=a7[y,x]
a=k7b.filt(a)
np.save('dik.npy',a); bewaar(a,pal,'dik.png'); print('stap1 px t.o.v. k7:',(a!=a7).sum())
