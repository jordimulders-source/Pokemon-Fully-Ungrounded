# Losse tintvlekjes < 3 px (4-verbonden) per kleurindex; print met buren.
import sys
from PIL import Image
f=sys.argv[1] if len(sys.argv)>1 else '../sprite_r2/rood_c.png'
a=Image.open(f).load()
def g(x,y): return a[x,y] if 0<=x<64 and 0<=y<64 else 0
seen=set(); out=[]
for y in range(64):
    for x in range(64):
        v=a[x,y]
        if v in (0,1) or (x,y) in seen: continue
        comp=[(x,y)]; seen.add((x,y)); i=0
        while i<len(comp):
            cx,cy=comp[i]; i+=1
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                n=(cx+dx,cy+dy)
                if n not in seen and g(*n)==v: seen.add(n); comp.append(n)
        if len(comp)<3: out.append((v,comp))
from collections import Counter
print(Counter(v for v,_ in out))
for v,c in out:
    if v in (8,9,10,4,5,11,12):
        x,y=c[0]
        nb=[g(x+dx,y+dy) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))]
        print(v,c,'buren',nb)
