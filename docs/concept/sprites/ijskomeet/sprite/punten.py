# Punten: spitse tips (1 px) en een lichtvlak van 2 px (j) waar de punt >= 4 px breed is.
import sys, numpy as np
from gio import from_txt, to_txt, CH
G=from_txt(sys.argv[1]); I={c:k for k,c in enumerate(CH)}
# tips: j links van de tip-K weg (lavendel of gas)
for (y,x,c) in [(10,53,'w'),(14,41,'w'),(16,31,'w'),(19,50,'w'),(32,45,'w'),(36,45,'w'),(43,42,'W')]:
    G[y,x]=I[c]
ice=np.load('ice_r1.npy')
H=G.copy()  # op kopie toetsen: geen doorrollen
for y in range(64):
    for x in range(62):
        if ice[y,x]: continue
        if H[y,x]==I['j'] and all(H[y,x+k]==I['i'] for k in (1,2,3)):
            G[y,x+1]=I['j']
to_txt(G,sys.argv[2])
