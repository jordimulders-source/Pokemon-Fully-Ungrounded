# Kale reductie in spritepalet: per 2x2-vak familie (K-lijn, n donkergrijs, geel, grijs, wit) + toon uit de modelhelderheid. Niets getekend.
import numpy as np, sys; from PIL import Image; from pal import *
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); fam=np.load('fam.npy'); lum=a@[0.299,0.587,0.114]
OY,OX=int(sys.argv[1]),int(sys.argv[2]); H,W=a.shape[:2]; h,w=(H-OY)//2,(W-OX)//2
def toon(f,l):
    if f=='H': return 'W' if l>=228 else 'w' if l>=196 else 'v' if l>=165 else 'u'
    if f=='G': return 'W' if l>=215 else 'c' if l>=172 else 'b' if l>=136 else 'a'
    if f=='Y': return 'y' if l>=185 else 'e' if l>=140 else 'd'
g=np.full((h,w),'.'); ml=np.zeros((h,w))
for j in range(h):
    for i in range(w):
        sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2)); f=fam[sl].ravel(); L_=lum[sl].ravel()
        if (f!='.').sum()<2: continue
        if (f=='K').sum()>=2: g[j,i]='K'; continue
        if (f=='D').sum()>=2: g[j,i]='n'; continue
        cnt={k:(f==k).sum() for k in 'YGH'}; k=max(cnt,key=lambda k:(cnt[k],'HGY'.index(k)))
        if cnt[k]==0: g[j,i]='K' if (f=='K').any() else 'n'; continue
        g[j,i]=toon(k,L_[f==k].mean()); ml[j,i]=L_[f==k].mean()
ys,xs=np.where(g!='.'); g=g[ys.min():ys.max()+1,xs.min():xs.max()+1]
schrijf(sys.argv[3],g); print(g.shape)
