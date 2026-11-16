import sys, numpy as np
from gio import to_txt, CH
from rijen import R
m=np.load('mask_r1.npy')
G=np.full((64,64),-1)
for y,segs in R.items():
    for x0,s in segs:
        for k,c in enumerate(s):
            G[y,x0+k]=CH.index(c)
diff=(G>=0)!=m
for y in range(64):
    xs=np.where(diff[y])[0]
    if len(xs): print('rij',y,'mask',np.where(m[y])[0].min(),np.where(m[y])[0].max(),'grid',np.where(G[y]>=0)[0].min() if (G[y]>=0).any() else None,np.where(G[y]>=0)[0].max() if (G[y]>=0).any() else None)
to_txt(G,sys.argv[1])
