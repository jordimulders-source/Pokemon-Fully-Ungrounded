# check.py sprite.npy : tintvlakjes < 3 px per index (behalve 0,1,2) en losse zwarte pixels zonder zwarte/lijnbuur
import sys, numpy as np
a=np.load(sys.argv[1]); H,W=a.shape; ch='.#abcdGHIstu'
seen=np.zeros(a.shape,bool); kl=[]
for y in range(H):
    for x in range(W):
        v=a[y,x]
        if v in (0,1,2) or seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; c=[]
        while st:
            q=st.pop(); c.append(q)
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=q[0]+dy,q[1]+dx
                if 0<=yy<H and 0<=xx<W and not seen[yy,xx] and a[yy,xx]==v: seen[yy,xx]=True; st.append((yy,xx))
        if len(c)<3: kl.append((ch[v],[(x,y) for y,x in c]))
print('kleine vlakjes:',kl)
los=[(x,y) for y in range(1,H-1) for x in range(1,W-1) if a[y,x]==1 and not any(a[y+dy,x+dx] in (0,1) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx)]
print('losse zwarte pixels:',los)
