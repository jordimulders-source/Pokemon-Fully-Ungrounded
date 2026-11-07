"""Controle silhouet: losse pixels, gaatjes, langste horizontale/verticale randstukken."""
import sys
from PIL import Image
def check(f):
    p=Image.open(f); P=p.load()
    S={(x,y) for x in range(64) for y in range(64) if P[x,y]!=0}
    iso=[q for q in S if sum((q[0]+dx,q[1]+dy) in S for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))<=1]
    holes=[(x,y) for x in range(1,63) for y in range(1,63) if (x,y) not in S and all((x+dx,y+dy) in S for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
    def runs(edge):
        best=[]
        for y in range(64):
            r=[]
            for x in range(65):
                if x<64 and (x,y) in S and edge(x,y): r.append(x)
                else:
                    if len(r)>4: best.append((len(r),y,r[0],r[-1]))
                    r=[]
        return sorted(best,reverse=True)
    top=runs(lambda x,y:(x,y-1) not in S); bot=runs(lambda x,y:(x,y+1) not in S)
    xs=[q[0] for q in S]; ys=[q[1] for q in S]
    print(f.split('/')[-1],len(S),'px, %dx%d'%(max(xs)-min(xs)+1,max(ys)-min(ys)+1),'los',iso,'gaten',holes)
    print('  bovenranden >4:',top[:8]); print('  onderranden >4:',bot[:8])
for f in sys.argv[1:]: check(f)
