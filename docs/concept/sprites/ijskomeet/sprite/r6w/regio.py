import sys; sys.path.insert(0,'r6w')
import numpy as np; from PIL import Image
from p6 import CH, from_txt
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); lum=n.mean(2)
m=np.load('mask_r1.npy'); ox,oy=11,-4
o=from_txt('r6w/onder.txt')
cnt=np.zeros((64,64),int)
for j in range(64):
  for i in range(64):
    y=3*j+oy; x=3*i+ox
    if m[j,i] and y>=0: cnt[j,i]=(lum[y:y+3,x:x+3]<45).sum()
np.save('r6w/cnt.npy',cnt)
bar=(cnt>=2)|np.isin(o,[CH.index(c) for c in 'abcdG'])|~m
reg=np.zeros((64,64),bool); st=[(40,10),(50,20),(50,30)]
for s in st: reg[s]=True
while st:
  a,b=st.pop()
  for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
    y,x=a+dy,b+dx
    if 0<=y<64 and 0<=x<64 and not reg[y,x] and not bar[y,x]: reg[y,x]=True; st.append((y,x))
np.save('r6w/reg.npy',reg)
for j in range(15,64):
  print('%2d '%j+''.join('.' if not m[j,i] else ('#' if reg[j,i] else (str(min(cnt[j,i],9)) if cnt[j,i]>=2 else ' ')) for i in range(0,50)))
