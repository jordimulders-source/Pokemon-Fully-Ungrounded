# bouw2.py: kale reductie via vlakken -> raster (indices), zonder handwerk
import numpy as np, sys
from collections import deque
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/sprite/r1/stappen/'
d=np.load(D+'red.npz'); a=d['alpha']; mean=d['mean']; lum=d['lum']
v=np.load(D+'sv.npz'); LS=v['LS']; TN=v['TN']; THK=v['THK']; DOOR=v['DOOR']
m=a>=0.45
bg=np.zeros_like(m); q=deque([(0,0)]); bg[0,0]=1
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<64 and 0<=xx<64 and not m[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
m=~bg
door=m&(DOOR>=0.5)
LS=LS.copy(); LS[door]=-1
# 0 transp,1 zwart,2 lijn-donker,3..7 steen T0..T4,8,9 mos,10,11 oog,12 deur
G=np.zeros((64,64),int)
t=np.full((64,64),7); t[TN>=95]=6; t[TN>=118]=5; t[TN>=140]=4; t[TN>=160]=3
G[m]=t[m]
gr=mean[...,1]-mean[...,0]
moss=m&(gr>3)
G[moss&(lum>=110)]=8; G[moss&(lum<110)]=9
G[door]=12
# grenzen tussen vlakken: 1 px lijn op de kant met de meeste lijndekking
LN=np.zeros((64,64),bool)
for y in range(64):
  for x in range(64):
    if not m[y,x]: continue
    for yy,xx in ((y+1,x),(y,x+1)):
      if yy<64 and xx<64 and m[yy,xx] and LS[yy,xx]!=LS[y,x]:
        if LS[y,x]==-1: LN[yy,xx]=True
        elif LS[yy,xx]==-1: LN[y,x]=True
        elif THK[y,x]>=THK[yy,xx]: LN[y,x]=True
        else: LN[yy,xx]=True
G[LN]=2
pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
G[edge]=1
np.save(D+'kaal2.npy',G); np.save(D+'masker.npy',m)
