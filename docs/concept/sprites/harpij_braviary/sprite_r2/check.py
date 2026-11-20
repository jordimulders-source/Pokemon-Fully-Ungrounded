# check.py raster.txt : tintclusters < 3 px (4-buren), losse K-pixels binnenin, open randen (rand-pixel naast transparant die geen lijn is)
import sys
R=[r.rstrip('\n') for r in open(sys.argv[1]) if r.strip('\n')]; H=len(R); W=len(R[0])
g=lambda y,x: R[y][x] if 0<=y<H and 0<=x<W else '.'
seen=set(); small=[]
for y in range(H):
    for x in range(W):
        v=R[y][x]
        if v in '.K' or (y,x) in seen: continue
        st=[(y,x)]; seen.add((y,x)); cl=[]
        while st:
            p=st.pop(); cl.append(p)
            for d in ((1,0),(-1,0),(0,1),(0,-1)):
                q=(p[0]+d[0],p[1]+d[1])
                if q not in seen and g(*q)==v: seen.add(q); st.append(q)
        if len(cl)<3: small.append((v,cl))
print('kleine clusters:',len(small))
for v,cl in small: print(' ',v,[(y,x) for y,x in cl])
# randpixels (grenzend aan transparant) die licht zijn
light='hiWucte'
edge=[(y,x,R[y][x]) for y in range(H) for x in range(W) if R[y][x] in light and any(g(y+dy,x+dx)=='.' for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))]
print('lichte randpixels:',edge)
