# check.py: kleine tintclusters (<3 px) per index, open randen (lichte kleur tegen transparant), losse zwarte pixels
import numpy as np
from collections import deque
class ndimage:
    @staticmethod
    def label(m):
        lab=np.zeros(m.shape,int); n=0
        for y,x in zip(*np.where(m)):
            if lab[y,x]: continue
            n+=1; q=deque([(y,x)]); lab[y,x]=n
            while q:
                a,b=q.popleft()
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    c,d=a+dy,b+dx
                    if 0<=c<m.shape[0] and 0<=d<m.shape[1] and m[c,d] and not lab[c,d]: lab[c,d]=n; q.append((c,d))
        return lab,n
o=np.load('sprite.npy'); CH='.#DPpWwlmTt'
for i in range(2,11):
    lab,n=ndimage.label(o==i)
    for k in range(1,n+1):
        ys,xs=np.where(lab==k)
        if len(ys)<3: print('cluster',CH[i],len(ys),list(zip(ys.tolist(),xs.tolist())))
pad=np.pad(o,1)
for y in range(64):
    for x in range(64):
        v=o[y,x]
        if v in (4,5,6,7,9,10):
            nb=[pad[y,x+1],pad[y+2,x+1],pad[y+1,x],pad[y+1,x+2]]
            if 0 in nb: print('open rand',CH[v],(y,x))
