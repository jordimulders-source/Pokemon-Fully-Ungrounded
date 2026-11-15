import numpy as np, sys; sys.path.insert(0,'maker'); from pal import PAL
S=np.load('sil56_rond.npy'); G=np.load('gids56.npy').astype(float)
keys=[k for k in PAL if k!='.']; C=np.array([PAL[k] for k in keys],float)
out=[]
for y in range(64):
  r=''
  for x in range(64):
    if not S[y,x]: r+='.'; continue
    d=((C-G[y,x])**2).sum(1); r+=keys[int(d.argmin())]
  out.append(r)
# buitenrand altijd omlijning
for y in range(64):
  r=list(out[y])
  for x in range(64):
    if S[y,x]:
      nb=[(y+dy,x+dx) for dy,dx in ((0,1),(1,0),(0,-1),(-1,0))]
      if any(not(0<=a<64 and 0<=b<64) or not S[a,b] for a,b in nb): r[x]='#'
  out[y]=''.join(r)
open('maker/onderlaag.txt','w').write('\n'.join(out)+'\n')
for i,l in enumerate(out[17:60]): print('%2d %s'%(i+17,l))
