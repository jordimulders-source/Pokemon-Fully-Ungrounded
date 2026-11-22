import numpy as np, sys
from PIL import Image
b=np.load(sys.argv[1]) if sys.argv[1].endswith('.npy') else np.array(Image.open(sys.argv[1]))
seen=np.zeros(b.shape,bool)
for y in range(64):
  for x in range(64):
    v=b[y,x]
    if v in (0,1) or seen[y,x]: continue
    st=[(x,y)]; seen[y,x]=True; comp=[]
    while st:
      cx,cy=st.pop(); comp.append((cx,cy))
      for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx,ny=cx+dx,cy+dy
        if 0<=nx<64 and 0<=ny<64 and not seen[ny,nx] and b[ny,nx]==v: seen[ny,nx]=True; st.append((nx,ny))
    if len(comp)<3: print('kleur %X'%v,len(comp),comp)
