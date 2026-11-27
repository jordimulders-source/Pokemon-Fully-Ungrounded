from PIL import Image
import numpy as np
s=np.array(Image.open('staryu/sprite_r1/staryu_r1.png'))
H,W=s.shape; seen=np.zeros_like(s,bool)
for y in range(H):
  for x in range(W):
    if seen[y,x] or s[y,x]==0: continue
    v=s[y,x]; st=[(y,x)]; seen[y,x]=1; pts=[]
    while st:
      a,b=st.pop(); pts.append((b,a))
      for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
        c,d=a+da,b+db
        if 0<=c<H and 0<=d<W and not seen[c,d] and s[c,d]==v: seen[c,d]=1; st.append((c,d))
    if len(pts)<3: print('index',v,len(pts),'px (x,y):',pts)
