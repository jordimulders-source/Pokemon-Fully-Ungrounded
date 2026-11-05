import numpy as np, sys
from PIL import Image
from palet import COLS
D='../../silhouet_af/'
sil=np.array(Image.open(D+'silhouet.png'))>0
o=np.array(Image.open(D+'onderlaag.png').convert('RGBA')).astype(float)
CH='.123456789abcdef'
cand=[1,2,3,5,6,7,8,9,10,11,13,14,15]
out=np.zeros((64,64),int)
for y in range(64):
  for x in range(64):
    if not sil[y,x]: continue
    r,g,b,a=o[y,x]
    if a<30: out[y,x]=1; continue
    best=min(cand,key=lambda k: sum((np.array(COLS[k])-np.array((r,g,b)))**2))
    out[y,x]=best
with open('start.txt','w') as f:
  f.write('== frame 1\n')
  for row in out: f.write(''.join(CH[v] for v in row)+'\n')
