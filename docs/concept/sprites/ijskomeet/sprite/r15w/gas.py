import numpy as np; from PIL import Image
from collections import deque
o=np.load('r15w/o3.npy'); pal=Image.open('r15w/o3.png').getpalette()
fg=o>0; K,W,L,M,D,S=1,2,3,4,5,6; G,g,e=11,15,12
purp={7,8,9,10}
# ijslijf: flood vanaf het oog door alles behalve K/paars/achtergrond
seed=tuple(np.argwhere(o==e)[0]); body=np.zeros((64,64),bool); q=deque([seed]); body[seed]=True
while q:
  y,x=q.popleft()
  for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
    c,d=y+dy,x+dx
    if 0<=c<64 and 0<=d<64 and not body[c,d] and fg[c,d] and o[c,d]!=K and o[c,d] not in purp: body[c,d]=True; q.append((c,d))
print('lijf',body.sum())
np.save('r15w/body.npy',body)
im=np.zeros((64,64,3),np.uint8); im[body]=(255,0,0); im[fg&~body]=(0,0,255)
Image.fromarray(im).resize((256,256),Image.NEAREST).save('r15w/body.png')
