from proj import *
from collections import deque
GR={2,3,4,5,6,13}; FILL={7,8,9,10,11,12}; IJ={1}|FILL
def ok(y,x): return 0<=y<64 and 0<=x<64
def rand(a,y,x): return x==0 or any(ok(y+dy,x+dx) and a[y+dy,x+dx]==0 for dy,dx in((0,1),(1,0),(0,-1),(-1,0)))
def masks(r):
    groen=np.isin(r,list(GR))
    gz=np.array([[groen[max(0,y-2):y+3,max(0,x-2):x+3].any() for x in range(64)] for y in range(64)])
    kop=np.zeros((64,64),bool); q=deque([(30,15)]); kop[30,15]=True
    while q:
        y,x=q.popleft()
        for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
            Y,X=y+dy,x+dx
            if 20<=Y<=44 and ok(Y,X) and not kop[Y,X] and r[Y,X] in IJ: kop[Y,X]=True; q.append((Y,X))
    gezicht=(r==1)&gz&kop&(np.arange(64)[:,None]>=26)
    rnd=np.array([[r[y,x] in IJ and rand(r,y,x) for x in range(64)] for y in range(64)])
    return kop,gezicht,rnd
