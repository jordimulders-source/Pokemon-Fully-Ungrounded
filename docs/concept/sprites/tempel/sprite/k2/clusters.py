import sys
from PIL import Image
import numpy as np
a=np.array(Image.open(sys.argv[1])); b=np.array(Image.open(sys.argv[2])) if len(sys.argv)>2 else None
H,W=a.shape; seen=np.zeros_like(a,bool); res=[]
for y in range(H):
    for x in range(W):
        if seen[y,x] or a[y,x]==0: continue
        c=a[y,x]; st=[(x,y)]; comp=[]; seen[y,x]=True
        while st:
            X,Y=st.pop(); comp.append((X,Y))
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                u,v=X+dx,Y+dy
                if 0<=u<W and 0<=v<H and not seen[v,u] and a[v,u]==c: seen[v,u]=True; st.append((u,v))
        if len(comp)<3 and c not in (1,2,7,10,11,12,14):
            nieuw = b is None or any(a[v,u]!=b[v,u] for u,v in comp)
            res.append((c,len(comp),comp[0],'NIEUW' if nieuw else 'oud'))
for r in res: print(r)
print(len(res),'clusters <3; nieuw:',sum(r[3]=='NIEUW' for r in res))
