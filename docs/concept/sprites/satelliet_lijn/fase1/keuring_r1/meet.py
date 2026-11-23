import numpy as np
from PIL import Image

def label(m):
  lab=np.zeros(m.shape,int);k=0
  for y,x in zip(*np.where(m)):
    if lab[y,x]: continue
    k+=1;st=[(y,x)];lab[y,x]=k
    while st:
      cy,cx=st.pop()
      for dy,dx in((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
        ny,nx=cy+dy,cx+dx
        if 0<=ny<m.shape[0] and 0<=nx<m.shape[1] and m[ny,nx] and not lab[ny,nx]: lab[ny,nx]=k;st.append((ny,nx))
  return lab,k
si=np.array(Image.open('sprite_r1/sprite.png'))
a=np.asarray(Image.open('model/model_gekozen_natief.png').convert('RGB')).astype(float)
H,W=a.shape[:2]; near=a.min(2)>=244
from collections import deque
bgm=np.zeros((H,W),bool);q=deque([(0,0)])
while q:
  y,x=q.popleft()
  if not(0<=y<H and 0<=x<W) or bgm[y,x] or not near[y,x]: continue
  bgm[y,x]=True;q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
fg=~bgm
# eigen afbeelding: modelpixel-dekking per spritecel
f=59/75; X0,Y0,OX,OY=17,16,2,6
cov=np.zeros((64,64)); n=np.zeros((64,64))
for y in range(H):
  for x in range(W):
    sx=int(OX+(x-X0+0.5)*f); sy=int(OY+(y-Y0+0.5)*f)
    if 0<=sx<64 and 0<=sy<64: cov[sy,sx]+=fg[y,x]; n[sy,sx]+=1
mm=(cov/np.maximum(n,1))>0.5
sm=si>0
print('silhouet: sprite-only',(sm&~mm).sum(),'model-only',(mm&~sm).sum())
for y,x in zip(*np.where(sm^mm)): print('  ',y,x,'S' if sm[y,x] else 'M', round(cov[y,x]/max(n[y,x],1),2))

for i in range(4,11):
  lab,k=label(si==i)
  small=[]
  for j in range(1,k+1):
    ys,xs=np.where(lab==j)
    if len(ys)<3: small.append((len(ys),list(zip(ys.tolist(),xs.tolist()))))
  if small: print('idx',i,'clusters<3:',small)
