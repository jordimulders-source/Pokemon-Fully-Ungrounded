# vlekjes.py raster.txt : alle 8-samenhangende clusters < 3 px per paletindex (behalve 0 en 1), met coordinaten (x,y)
import sys,numpy as np
from txt import CH
a=np.loadtxt(sys.argv[1],dtype=int); H,W=a.shape
N8=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
seen=np.zeros_like(a,bool); n=0
for y in range(H):
    for x in range(W):
        v=a[y,x]
        if v<=1 or seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; c=[]
        while st:
            p=st.pop(); c.append(p)
            for dy,dx in N8:
                q=(p[0]+dy,p[1]+dx)
                if 0<=q[0]<H and 0<=q[1]<W and not seen[q] and a[q]==v: seen[q]=True; st.append(q)
        if len(c)<3: n+=1; print(CH[v],[(x,y) for y,x in c])
print('totaal',n)
