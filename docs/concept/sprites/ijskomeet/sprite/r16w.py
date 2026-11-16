# r16: kopbovenkant belijnd (modellijn), linker buitenlijn lichter, ontkorrelen (zoals Krassault glad.py)
import numpy as np; from PIL import Image
from collections import deque, Counter
o=np.load('r15w/o4.npy').copy(); pal=Image.open('r15.png').getpalette()
K,W,L,M,D,S,N,G,g,e,r=1,2,3,4,5,6,13,11,15,12,14
vap=np.load('r15w/vap.npy')
# 1. bovenkant kop: modellijn (drietand) als N
top=[(7,27),(8,27),(9,27),(10,26),(11,25),(12,24),(13,24),(14,23),(15,23),(16,24),(17,25)]
for x,y in top: o[y,x]=N
# alles onder de lijn binnen de kop dat lavendel/gas is -> ijs
for x in range(8,18):
  ytop=max(y for (xx,y) in top if xx==x) if any(xx==x for xx,_ in top) else None
  if ytop is None: continue
  for y in range(ytop+1,ytop+4):
    if o[y,x] in (G,g,L): o[y,x]=W
# 2. linker buitenlijn (lichtkant) lichter
fg=o>0
for y in range(64):
  for x in range(64):
    if o[y,x]==K and x<=14 and any(not fg[y+dy,x+dx] for dy,dx in((0,-1),(-1,0),(-1,-1),(1,-1)) if 0<=y+dy<64 and 0<=x+dx<64):
      o[y,x]=S if y<46 else N
# 3. ontkorrelen: clusters < 3 px nemen de buurkleur van hun eigen groep aan
ICE={W,L,M,D}; PUR={7,8,9,10}; GAS={W,L,G,g}
def grp(y,x,c):
  if vap[y,x]: return GAS if c in GAS else None
  if c in ICE: return ICE
  if c in PUR: return PUR
  return None
H=64
for it in range(4):
  seen=np.zeros((H,H),bool); ch=0
  for y in range(H):
    for x in range(H):
      c=o[y,x]
      if seen[y,x] or grp(y,x,c) is None: continue
      gset=grp(y,x,c); q=deque([(y,x)]); seen[y,x]=True; cl=[]
      while q:
        cy,cx=q.popleft(); cl.append((cy,cx))
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
          ny,nx=cy+dy,cx+dx
          if 0<=ny<H and 0<=nx<H and not seen[ny,nx] and o[ny,nx]==c and vap[ny,nx]==vap[y,x]: seen[ny,nx]=True; q.append((ny,nx))
      if len(cl)>=3: continue
      nb=Counter()
      for cy,cx in cl:
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
          ny,nx=cy+dy,cx+dx
          if 0<=ny<H and 0<=nx<H and o[ny,nx]!=c and o[ny,nx] in gset and vap[ny,nx]==vap[y,x]: nb[o[ny,nx]]+=1
      if nb:
        t=max(nb,key=lambda k:nb[k])
        for cy,cx in cl: o[cy,cx]=t
        ch+=len(cl)
  print('ronde',it,'pixels',ch)
  if not ch: break
np.save('r16.npy',o)
im=Image.fromarray(o.astype(np.uint8)).convert('P'); im.putpalette(pal); im.save('r16.png',transparency=0)
a=im.convert('RGB').resize((512,512),Image.NEAREST); a.save('r16_8x.png')
b=Image.open('r15.png').convert('RGB').resize((512,512),Image.NEAREST); m=Image.open('vel_r9.png').crop((1060,0,1590,520))
v=Image.new('RGB',(1600,530),'white'); v.paste(a,(0,8)); v.paste(b,(530,8)); v.paste(m,(1060,0)); v.save('voor_jordi_r16.png')
