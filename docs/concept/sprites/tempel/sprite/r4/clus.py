# clus.py raster.txt [x0 y0 x1 y1] : clusters (4-verbonden) per tint kleiner dan 3 px, behalve X/./o/p/z
import sys
R=[l.rstrip('\n') for l in open(sys.argv[1])][:64]
x0,y0,x1,y1=map(int,sys.argv[2:6]) if len(sys.argv)>5 else (0,0,63,63)
seen=set(); out=[]
for y in range(64):
  for x in range(64):
    c=R[y][x]
    if (x,y) in seen or c in '.Xopz': continue
    st=[(x,y)]; comp={(x,y)}; seen.add((x,y))
    while st:
      a,b=st.pop()
      for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        q=(a+dx,b+dy)
        if 0<=q[0]<64 and 0<=q[1]<64 and q not in seen and R[q[1]][q[0]]==c: seen.add(q); comp.add(q); st.append(q)
    if len(comp)<3 and any(x0<=p[0]<=x1 and y0<=p[1]<=y1 for p in comp): out.append((c,sorted(comp)))
for c,cp in out: print(c,cp)
print(len(out))
