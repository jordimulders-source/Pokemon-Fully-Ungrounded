# tintvlakjes < 3 px (4-buren, zelfde index) binnen de figuur, exclusief buitenrand/lijnen (1) en oog
import numpy as np, sys; from PIL import Image
sys.path.insert(0,'.')
from r4 import RAND,OOG
S=np.array(Image.open(sys.argv[1])).astype(int)
seen=set(); klein=[]
for y0 in range(64):
    for x0 in range(64):
        v=S[y0,x0]
        if v in (0,1) or (y0,x0) in seen or (y0,x0) in OOG: continue
        comp=[(y0,x0)]; st=[(y0,x0)]; seen.add((y0,x0))
        while st:
            y,x=st.pop()
            for a,b in((-1,0),(1,0),(0,-1),(0,1)):
                q=(y+a,x+b)
                if 0<=q[0]<64 and 0<=q[1]<64 and S[q]==v and q not in seen: seen.add(q); comp.append(q); st.append(q)
        if len(comp)<3 and not all(p in RAND for p in comp): klein.append((v,comp))
for v,c in klein: print(v,c)
print(len(klein),'kleine vlakjes')
