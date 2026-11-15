# Bewaakt r5: silhouet = r4 (gladde rug), patronen/kenmerken (lila, creme, oog, tand, tong) op dezelfde plek als r4, buitenrand zoals r4.
import numpy as np, sys
r4=np.load('welp_r4.npy'); a=np.load('welp_r5.npy'); H,W=a.shape
sil=int(((a>0)!=(r4>0)).sum())
pat=lambda z: np.isin(z,[6,7,8,9,10,11,12,13])
pm=int((pat(a)!=pat(r4)).sum())
edge=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if r4[y,x] and any(not(0<=y+dy<H and 0<=x+dx<W) or r4[y+dy,x+dx]==0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): edge[y,x]=True
ed=int((a!=r4)[edge].sum())
fig=(a>0).sum()
print('silhouet-diff:',sil,'| patroon/kenmerk-diff:',pm,'| buitenrand-diff:',ed,'| zwart %.1f%% lijnbruin %.1f%%'%(100*(a==1).sum()/fig,100*(a==2).sum()/fig),'| bruintinten',sorted({int(v) for v in a.ravel() if v in (3,4,5)}),'| kleuren',len(set(a.ravel()))-1)
ok=sil==0 and pm==0 and ed==0; print('OK' if ok else 'FAIL'); sys.exit(0 if ok else 1)
