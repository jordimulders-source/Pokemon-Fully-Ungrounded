# grootste egale vlakken (4-samenhang) per tint in de romp x26-42 r31-45
import sys
from PIL import Image
for f in sys.argv[1:]:
    a=Image.open(f).load(); seen=set(); out=[]
    for y in range(31,46):
        for x in range(26,43):
            if (x,y) in seen or a[x,y]==0: continue
            v=a[x,y]; st=[(x,y)]; seen.add((x,y)); n=0
            while st:
                p=st.pop(); n+=1
                for d in ((1,0),(-1,0),(0,1),(0,-1)):
                    q=(p[0]+d[0],p[1]+d[1])
                    if 26<=q[0]<43 and 31<=q[1]<46 and q not in seen and a[q]==v: seen.add(q); st.append(q)
            out.append((n,v,(x,y)))
    print(f, sorted(out,reverse=True)[:4])
