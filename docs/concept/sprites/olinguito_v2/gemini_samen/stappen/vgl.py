import sys,numpy as np
m=np.load('stappen/sil.npy')
g=[l.rstrip('\n') for l in open(sys.argv[1])]
def segs(v):
    xs=np.where(v)[0]; out=[]
    if len(xs)==0: return out
    s=p=xs[0]
    for x in xs[1:]:
        if x!=p+1: out.append((int(s),int(p))); s=x
        p=x
    out.append((int(s),int(p))); return out
for y in range(64):
    a=np.array([c!='.' for c in g[y]])
    if (a!=m[y]).any(): print(y,'sil',segs(m[y]),'verf',segs(a))
