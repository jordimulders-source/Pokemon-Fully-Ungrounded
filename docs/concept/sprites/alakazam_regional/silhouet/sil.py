# silhouet = model verkleind; achtergrond = witte componenten die aan de rand hangen + gat arm/lijf (component bij x328-399,y501-572)
import numpy as np
from PIL import Image
from collections import deque
from geo import *
c=model(); L=c.mean(2); sat=c.max(2)-c.min(2)
wh=(L>225)&(sat<25)
H,W=wh.shape
def flood(seeds):
    m=np.zeros(wh.shape,bool); q=deque()
    for s in seeds:
        if wh[s]: m[s]=1; q.append(s)
    while q:
        y,x=q.popleft()
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=y+dy,x+dx
            if 0<=yy<H and 0<=xx<W and wh[yy,xx] and not m[yy,xx]: m[yy,xx]=1; q.append((yy,xx))
    return m
bg=flood([(0,0),(540,360)])   # rand + gat tussen arm en lijf
fg=~bg
mean=np.zeros((64,64,3)); alpha=np.zeros((64,64))
for Y in range(64):
  for X in range(64):
    ya,yb,xa,xb=blok(X,Y)
    ya,xa=max(ya,0),max(xa,0)
    f=fg[ya:yb,xa:xb]
    if f.size==0: continue
    alpha[Y,X]=f.mean()
    if f.any(): mean[Y,X]=c[ya:yb,xa:xb][f].mean(0)
m=alpha>=0.45
np.save('alpha.npy',alpha)
print('px',m.sum(),'box x',np.where(m.any(0))[0][[0,-1]],'y',np.where(m.any(1))[0][[0,-1]])
a=np.zeros((64,64,4),'uint8'); a[m]=[0,0,0,255]; Image.fromarray(a).save('silhouet.png')
g=np.zeros((64,64,4),'uint8'); g[m,:3]=mean[m].astype('uint8'); g[m,3]=255; Image.fromarray(g).save('gids_gemiddeld.png')
src=Image.open(D+'referenties/model_silhouet.png').convert('RGB').crop((int(OX),int(OY),int(OX+64*S),int(OY+64*S))).resize((512,512),Image.LANCZOS)
o=np.asarray(src).copy()
pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
big=np.kron(edge,np.ones((8,8),bool)); o[big]=[255,0,0]
Image.fromarray(o).save('silhouet_over_bron.png')
