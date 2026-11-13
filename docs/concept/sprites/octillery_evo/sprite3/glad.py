# Ontkorrelen zonder te hertekenen: alleen vulkleuren (rood 3-7, mondroze 8-9); lijnen (1,2), geel (10-12) en silhouet blijven.
# Stap 1: losse pixels en clusters < MIN px nemen de meest voorkomende vulkleur van hun buren aan. Stap 2: uitsteeksels van 1 px op tintgrenzen glad.
# Gebruik: python3 glad.py IN UIT [MIN]
import sys; from PIL import Image; import numpy as np
from collections import deque, Counter
IN,UIT=sys.argv[1],sys.argv[2]; MIN=int(sys.argv[3]) if len(sys.argv)>3 else 4
im=Image.open(IN); a=np.array(im); pal=im.getpalette(); o=a.copy(); H,W=a.shape
FILL=set(range(3,10)); GRP=lambda c: 0 if c<=7 else 1
def clusters(o):
    seen=np.zeros((H,W),bool); out=[]
    for y in range(H):
        for x in range(W):
            if seen[y,x] or o[y,x] not in FILL: continue
            c=o[y,x]; q=deque([(y,x)]); seen[y,x]=True; cl=[]
            while q:
                cy,cx=q.popleft(); cl.append((cy,cx))
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<H and 0<=nx<W and not seen[ny,nx] and o[ny,nx]==c: seen[ny,nx]=True; q.append((ny,nx))
            out.append((c,cl))
    return out
n1=0
for _ in range(4):
    ch=False
    for c,cl in sorted(clusters(o),key=lambda t:len(t[1])):
        if len(cl)>=MIN: continue
        nb=Counter()
        for y,x in cl:
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=y+dy,x+dx
                if 0<=ny<H and 0<=nx<W and o[ny,nx] in FILL and o[ny,nx]!=c and GRP(o[ny,nx])==GRP(c): nb[o[ny,nx]]+=1
        if not nb: continue
        # dichtstbijzijnde tint bij gelijke stand
        t=max(nb,key=lambda k:(nb[k],-abs(int(k)-int(c))))
        for y,x in cl: o[y,x]=t
        n1+=len(cl); ch=True
    if not ch: break
n2=0
for _ in range(2):
    p=o.copy()
    for y in range(1,H-1):
        for x in range(1,W-1):
            c=p[y,x]
            if c not in FILL: continue
            nb=[p[y-1,x],p[y+1,x],p[y,x-1],p[y,x+1]]; same=sum(v==c for v in nb)
            fill=[v for v in nb if v in FILL and v!=c and GRP(v)==GRP(c)]
            if same<=1 and len(fill)>=3:
                t=Counter(fill).most_common(1)[0]
                if t[1]>=3: o[y,x]=t[0]; n2+=1
out=Image.fromarray(o,'P'); out.putpalette(pal); out.save(UIT,transparency=0)
print('losse clusters:',n1,'px; uitsteeksels:',n2,'px; totaal gewijzigd',int((o!=a).sum()),'van',int((a>0).sum()))
