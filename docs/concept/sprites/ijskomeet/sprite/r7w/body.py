import sys; sys.path.insert(0,'r7w')
from zones import *
ok=isin(R,'WLMDerCg')
lim=np.zeros((64,64),bool)
for j in range(24,62):
  for i in range(64):
    lim[j,i]= i<=33 and not (j<=27 and i<10)
pl=flood(R,[(45,10),(50,20),(30,10),(42,25),(57,15),(35,5),(44,31),(47,4),(40,2),(55,9),(43,2)],ok&lim)
body=pl.copy()
for j in range(64):
  for i in range(64):
    if not pl[j,i] and isin(R,'SK')[j,i]:
      if pl[max(0,j-1):j+2,max(0,i-1):i+2].any(): body[j,i]=True
m=np.load('mask_r1.npy')
outer=np.zeros((64,64),bool)
for j in range(64):
  for i in range(64):
    if body[j,i]:
      for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        y,x=j+dy,i+dx
        if not(0<=y<64 and 0<=x<64) or not body[y,x]: outer[j,i]=True
np.save('r7w/body.npy',body); np.save('r7w/outer.npy',outer)
