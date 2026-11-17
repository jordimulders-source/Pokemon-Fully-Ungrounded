# Technische controle: kleurtal, kleine tintclusters, dambord (2x2 om en om), losse zwarte pixels binnenin, licht op de buitenrand
import sys,numpy as np; from PIL import Image
a=np.asarray(Image.open(sys.argv[1])).astype(int); H,W=a.shape
print('kleuren',len(set(a.ravel()))-1, 'bbox', [int(v) for v in (np.where(a>0)[1].min(),np.where(a>0)[1].max(),np.where(a>0)[0].min(),np.where(a>0)[0].max())])
seen=np.zeros(a.shape,bool); klein=[]
for y in range(H):
    for x in range(W):
        v=a[y,x]
        if v<2 or seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; c=[]
        while st:
            q=st.pop(); c.append(q)
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=q[0]+dy,q[1]+dx
                if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and a[yy,xx]==v: seen[yy,xx]=True; st.append((yy,xx))
        if len(c)<3: klein.append((v,[(x_,y_) for y_,x_ in c]))
print('tintclusters <3 px:',len(klein)); print(' ',klein)
db=[]
for y in range(H-1):
    for x in range(W-1):
        q=a[y:y+2,x:x+2]
        if q.min()>0 and q[0,0]==q[1,1] and q[0,1]==q[1,0] and q[0,0]!=q[0,1]: db.append((x,y))
print('dambord 2x2:',db)
los=[]
for y in range(1,H-1):
    for x in range(1,W-1):
        if a[y,x]!=1: continue
        nb=[a[y-1,x],a[y+1,x],a[y,x-1],a[y,x+1],a[y-1,x-1],a[y-1,x+1],a[y+1,x-1],a[y+1,x+1]]
        if 0 not in nb and sum(1 for v in nb if v in (1,2))==0: los.append((x,y))
print('losse zwarte pixels binnenin:',los)
licht=[(x,y) for y in range(1,H-1) for x in range(1,W-1) if a[y,x]>=3 and a[y,x] not in (1,2,9) and 0 in (a[y-1,x],a[y+1,x],a[y,x-1],a[y,x+1])]
print('vulkleur op de buitenrand:',licht)
