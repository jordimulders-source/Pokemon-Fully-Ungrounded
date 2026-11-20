# lijnen uit het model op het spriteraster: lichte schachten (streepkaart r4) en donkere pengrenzen (groef: modelpixel >= 15
# donkerder dan venstergemiddelde r=3); per 8-verbonden stuk één cel per rij (grootste aandeel) -> 1 px lijn
import numpy as np
from frac import *
ST=np.load('../r4/streep_nat.npy')
mw=np.isin(Zn,['M','W','K'])
def box(a,m,r):
    P=np.pad(a*m,r); Q=np.pad(m.astype(float),r); sm=np.zeros_like(a); c=np.zeros_like(a)
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            sm+=P[r+dy:r+dy+H,r+dx:r+dx+W]; c+=Q[r+dy:r+dy+H,r+dx:r+dx+W]
    return sm/np.maximum(c,1e-6)
FS=frac(ST&fgn)
FG=frac(mw&(Ln<box(Ln,mw,3)-15))
N8=[(i,j) for i in (-1,0,1) for j in (-1,0,1) if i or j]
def lijnen(F,thr,zone,minl):
    m=(F>=thr)&zone; seen=np.zeros_like(m); out=[]
    for y,x in zip(*np.where(m)):
        if seen[y,x]: continue
        st=[(y,x)]; c=[]; seen[y,x]=1
        while st:
            a,b=st.pop(); c.append((a,b))
            for d,e in N8:
                q,r=a+d,b+e
                if 0<=q<64 and 0<=r<64 and m[q,r] and not seen[q,r]: seen[q,r]=1; st.append((q,r))
        rows={}
        for a,b in c: rows.setdefault(a,[]).append(b)
        cel=[(a,max(bs,key=lambda b:F[a,b])) for a,bs in rows.items()]
        if len(cel)>=minl: out.append(sorted(cel))
    return out
