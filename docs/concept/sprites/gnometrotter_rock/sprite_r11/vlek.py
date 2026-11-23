# vlek.py: vlekjes < 3 px (4-buren, zelfde index, zonder 0/1) per sprite; met --lijst de nieuwe vlekjes t.o.v. r10
import sys, numpy as np; from PIL import Image; from scipy import ndimage as nd
def vlek(a):
    m=np.zeros(a.shape,bool)
    for i in range(2,16):
        lab,n=nd.label(a==i)
        if n:
            s=nd.sum(np.ones_like(a),lab,range(1,n+1))
            for k,sz in enumerate(s,1):
                if sz<3: m|=lab==k
    return m
A=[np.array(Image.open(f)) for f in sys.argv[1:3]]
M=[vlek(a) for a in A]
for f,a,m in zip(sys.argv[1:3],A,M): print(f, m.sum(), '/', ((a>1)).sum())
nieuw=M[1]&~M[0]
print('nieuw in tweede:',[(x,y,'%X'%A[1][y,x]) for y,x in zip(*np.where(nieuw))])
