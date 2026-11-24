import sys, numpy as np
from PIL import Image
def tel(p, x0=40, conn=4):
    a=np.array(Image.open(p)); H,W=a.shape; seen=np.zeros_like(a,bool); n=0; lijst=[]
    nb=[(1,0),(-1,0),(0,1),(0,-1)]+([(1,1),(1,-1),(-1,1),(-1,-1)] if conn==8 else [])
    for y in range(H):
        for x in range(W):
            if seen[y,x] or a[y,x]==0: continue
            c=a[y,x]; st=[(x,y)]; seen[y,x]=True; comp=[]
            while st:
                q=st.pop(); comp.append(q)
                for d in nb:
                    u,v=q[0]+d[0],q[1]+d[1]
                    if 0<=u<W and 0<=v<H and not seen[v,u] and a[v,u]==c: seen[v,u]=True; st.append((u,v))
            if len(comp)<3 and min(p[0] for p in comp)>=x0: n+=1; lijst.append((c,comp))
    return n,lijst
for p in sys.argv[1:]:
    n4,l=tel(p); n8,_=tel(p,conn=8); print(p,'clusters <3 px op x>=40: 4-samenhang',n4,'| 8-samenhang',n8)
    if '-v' in p: pass
