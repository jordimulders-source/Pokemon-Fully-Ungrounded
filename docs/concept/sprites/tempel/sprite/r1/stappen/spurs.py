# spurs.py raster.txt: binnenlijn-uitlopers (vrije einden) met hun lengte tot een kruising
import sys
R=[l.rstrip('\n') for l in open(sys.argv[1])][:64]
L=lambda x,y: 0<=x<64 and 0<=y<64 and R[y][x] in 'X+z'
def nb(x,y): return [(x+dx,y+dy) for dx in (-1,0,1) for dy in (-1,0,1) if (dx or dy) and L(x+dx,y+dy)]
out=[]
for y in range(64):
  for x in range(64):
    if R[y][x]=='+' and len(nb(x,y))==1:
      path=[(x,y)]; cur=(x,y); prev=None
      while True:
        n=[p for p in nb(*cur) if p!=prev and p not in path]
        if len(n)!=1 or len(path)>6: break
        prev=cur; cur=n[0]
        if len(nb(*cur))>2: break
        path.append(cur)
      out.append((len(path),path))
for l,p in sorted(out): print(l,p)
