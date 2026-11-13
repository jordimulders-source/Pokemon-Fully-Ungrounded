# Silhouet = gekozen model (../referenties/model_gekozen.png) direct verkleind (methode poedelmot/poedellarve sil.py).
# Achtergrond is wit (254): voorgrond = alles wat niet vanaf de rand bereikbaar is over bijna-wit.
import numpy as np
from PIL import Image
from collections import deque
c=np.asarray(Image.open('../referenties/model_gekozen.png').convert('RGB')).astype(int)
H0,W0=c.shape[:2]
wit=c.min(2)>=244
bgm=np.zeros((H0,W0),bool); q=deque()
for x in range(W0):
    for y in (0,H0-1):
        if wit[y,x] and not bgm[y,x]: bgm[y,x]=1; q.append((y,x))
for y in range(H0):
    for x in (0,W0-1):
        if wit[y,x] and not bgm[y,x]: bgm[y,x]=1; q.append((y,x))
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<H0 and 0<=xx<W0 and wit[yy,xx] and not bgm[yy,xx]: bgm[yy,xx]=1; q.append((yy,xx))
fg=~bgm
ys,xs=np.where(fg); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
W=54; s=(x1-x0)/W; Hh=int(np.ceil((y1-y0)/s)); top=64-Hh-1; left=(64-W)//2
mean=np.zeros((64,64,3)); alpha=np.zeros((64,64))
for by in range(Hh):
  for bx in range(W):
    ya,yb=int(y0+by*s),int(y0+(by+1)*s); xa,xb=int(x0+bx*s),int(x0+(bx+1)*s)
    f=fg[ya:yb,xa:xb]
    if f.size: alpha[top+by,left+bx]=f.mean()
    if f.any(): mean[top+by,left+bx]=c[ya:yb,xa:xb][f].mean(0)
m=alpha>=0.45
bg=np.zeros_like(m); q=deque([(0,0)]); bg[0,0]=1
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<64 and 0<=xx<64 and not m[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
gaten=(~bg&~m).sum(); m=~bg
print('model box',x0,x1,y0,y1,'fg-aandeel',round(fg[y0:y1,x0:x1].mean(),3))
print('px',m.sum(),'box x',np.where(m.any(0))[0][[0,-1]],'y',np.where(m.any(1))[0][[0,-1]],'schaal',round(s,3),'top',top,'left',left,'gevulde gaten',gaten)
a=np.zeros((64,64,4),'uint8'); a[m]=[0,0,0,255]; Image.fromarray(a).save('silhouet.png')
g=np.zeros((64,64,4),'uint8'); g[m,:3]=mean[m].astype('uint8'); g[m,3]=255; Image.fromarray(g).save('gids_gemiddeld.png')
big=Image.new('RGB',(int(64*s),int(64*s)),(254,254,254))
big.paste(Image.open('../referenties/model_gekozen.png').convert('RGB'),(int(left*s-x0),int(top*s-y0)))
o=np.asarray(big.resize((512,512),Image.LANCZOS)).copy()
pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
o[np.kron(edge,np.ones((8,8),bool))]=[255,0,0]
Image.fromarray(o).save('silhouet_over_bron.png')
Image.fromarray(np.kron(np.asarray(Image.open('gids_gemiddeld.png').convert('RGBA')),np.ones((8,8,1),'uint8'))).save('gids_8x.png')
