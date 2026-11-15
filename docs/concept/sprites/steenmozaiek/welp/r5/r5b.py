# Variant r5b: r3 met al zijn lijnen (structuur van het model), maar binnenlijnen in lijnbruin i.p.v. zwart
# (zwart alleen buitenrand schaduwkant + oog/neus/mond/oren); rug en buitenrand van r4.
import numpy as np
r4=np.load('welp_r4.npy'); r3=np.load('welp_r3_A_oog1.npy'); r5=np.load('welp_r5.npy'); H,W=r4.shape
_,K,d,S,M,L=range(6)
edge=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if r4[y,x] and any(not(0<=y+dy<H and 0<=x+dx<W) or r4[y+dy,x+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): edge[y,x]=True
feat=np.zeros((H,W),bool)
feat[8:12,8:15]=True; feat[13:17,1:7]=True; feat[16:24,2:14]=True; feat[0:9,4:10]=True; feat[0:9,16:25]=True; feat[9:11,3:5]=True
a=r5.copy(); n=0
binnen_r3=(r3>0)
for y in range(H):
    for x in range(W):
        if edge[y,x] or r4[y,x]==0 or not binnen_r3[y,x]: continue
        if r3[y,x] in (K,d):
            # r3-binnenlijn terug, behalve waar r3's eigen oude rugrand lag (rug is in r4 verlegd)
            if any(not(0<=y+dy<H and 0<=x+dx<W) or r3[y+dy,x+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): continue
            v=K if (feat[y,x] and r3[y,x]==K) else d
            if a[y,x]!=v and a[y,x] in (S,M,L,K,d): a[y,x]=v; n+=1
# r4-lijnen die r3 niet had (gegenereerde vormgrenzen) -> facettint van r3 (buren)
m=0
for y in range(H):
    for x in range(W):
        if edge[y,x] or a[y,x]!=d or r3[y,x] in (K,d): continue
        cnt={}
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                yy,xx=y+dy,x+dx
                if 0<=yy<H and 0<=xx<W and r3[yy,xx] in (S,M,L): cnt[r3[yy,xx]]=cnt.get(r3[yy,xx],0)+1
        if cnt: a[y,x]=max(cnt,key=cnt.get); m+=1
np.save('welp_r5b.npy',a); fig=(a>0).sum()
print('r3-lijnen terug',n,'r4-extralijnen weg',m,'zwart %.1f%% lijnbruin %.1f%%'%(100*(a==1).sum()/fig,100*(a==2).sum()/fig))
