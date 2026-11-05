"""Tintclusters (4-samenhangend, zelfde index) kleiner dan 3 px, voor de vlaktinten 3-8, A, B, E. Gebruik: python3 clusters.py raster.txt"""
import sys
r=[l.rstrip('\n') for l in open(sys.argv[1] if len(sys.argv)>1 else 'raster.txt')][:64]
VLAK=set('345678ABE')
seen=set(); out=[]
for y in range(64):
    for x in range(64):
        c=r[y][x]
        if c not in VLAK or (x,y) in seen: continue
        st=[(x,y)]; comp=[]; seen.add((x,y))
        while st:
            a,b=st.pop(); comp.append((a,b))
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                p=(a+dx,b+dy)
                if 0<=p[0]<64 and 0<=p[1]<64 and p not in seen and r[p[1]][p[0]]==c: seen.add(p); st.append(p)
        if len(comp)<3: out.append((c,sorted(comp)))
for c,comp in out: print(c,comp)
print('aantal clusters < 3 px:',len(out))
