import sys, numpy as np
from gio import to_txt, from_txt, CH
from ijs import IJS
G=from_txt(sys.argv[1]); m=np.load('mask_r1.npy')
for y,(x0,s) in IJS.items():
    for k,c in enumerate(s): G[y,x0+k]=CH.index(c)
print('buiten mask:',int(((G>=0)&~m).sum()),'gat:',int(((G<0)&m).sum()))
to_txt(G,sys.argv[2])
