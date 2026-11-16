import sys; from PIL import Image; import numpy as np
from collections import deque
def load(f):
    im=Image.open(f)
    if im.mode!='P': im=im.convert('P')
    a=np.array(im)[:64,:64]; pal=np.array(im.getpalette()[:768]).reshape(-1,3)
    return a,pal
def stats(f,face=None):
    a,pal=load(f); L=(pal*[0.299,0.587,0.114]).sum(1)
    H=a!=0; n=H.sum()
    used=[i for i in np.unique(a[H])]
    dark=min(used,key=lambda i:L[i])
    edge=np.zeros_like(H)
    for y in range(64):
        for x in range(64):
            if H[y,x] and any(not(0<=y+dy<64 and 0<=x+dx<64) or not H[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1))): edge[y,x]=1
    # small clusters (4-conn) per index, all non-dark colours
    seen=np.zeros_like(H); small=[]
    for y in range(64):
        for x in range(64):
            if H[y,x] and not seen[y,x] and a[y,x]!=dark:
                c=a[y,x]; q=deque([(y,x)]); seen[y,x]=1; comp=[(y,x)]
                while q:
                    yy,xx=q.popleft()
                    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                        y2,x2=yy+dy,xx+dx
                        if 0<=y2<64 and 0<=x2<64 and H[y2,x2] and not seen[y2,x2] and a[y2,x2]==c: seen[y2,x2]=1; q.append((y2,x2)); comp.append((y2,x2))
                if len(comp)<3: small.append((c,comp))
    # checkerboard 2x2
    cb=0
    for y in range(63):
        for x in range(63):
            w=a[y:y+2,x:x+2]
            if (w!=0).all() and w[0,0]==w[1,1] and w[0,1]==w[1,0] and w[0,0]!=w[0,1]: cb+=1
    # interior dark isolated
    iso=0; intdark=0
    for y in range(1,63):
        for x in range(1,63):
            if a[y,x]==dark and not edge[y,x]:
                intdark+=1
                if all(a[y+dy,x+dx]!=dark for dy,dx in((1,0),(-1,0),(0,1),(0,-1))): iso+=1
    e=edge.sum(); ed=(edge&(a==dark)).sum()
    print(f"{f.split('/')[-2] if 'graphics' in f else f.split('/')[-1]:22s} px {n:5d} kleuren {len(used):2d} zwart {100*(a==dark).sum()/n:4.1f}% rand-zwart {100*ed/e:4.1f}% binnen-zwart {100*intdark/n:4.1f}% los-zwart {iso:3d} vlakjes<3 {len(small):3d} ({1000*len(small)/n:4.1f}/1000) dambord {cb}")
    return a,pal,small,edge,dark
if __name__=='__main__':
    for f in sys.argv[1:]: stats(f)
