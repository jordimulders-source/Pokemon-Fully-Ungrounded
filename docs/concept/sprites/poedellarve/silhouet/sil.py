# Silhouet = gekozen model (../referenties/model_gekozen.png) direct verkleind (methode poedelmot/silhouet/sil.py).
import numpy as np
from PIL import Image
from collections import deque
c=np.asarray(Image.open('../referenties/model_gekozen.png').convert('RGB')).astype(int)
fg=~((c[...,1]>c[...,0]+40)&(c[...,0]<120))
x0,x1,y0,y1=236,778,346,748
W=40; s=(x1-x0)/W; Hh=int(np.ceil((y1-y0)/s)); top=64-Hh-1; left=(64-W)//2
mean=np.zeros((64,64,3)); alpha=np.zeros((64,64))
for by in range(Hh):
  for bx in range(W):
    ya,yb=int(y0+by*s),int(y0+(by+1)*s); xa,xb=int(x0+bx*s),int(x0+(bx+1)*s)
    f=fg[ya:yb,xa:xb]; alpha[top+by,left+bx]=f.mean()
    if f.any(): mean[top+by,left+bx]=c[ya:yb,xa:xb][f].mean(0)
m=alpha>=0.45
bg=np.zeros_like(m); q=deque([(0,0)]); bg[0,0]=1
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<64 and 0<=xx<64 and not m[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
m=~bg
print('px',m.sum(),'box x',np.where(m.any(0))[0][[0,-1]],'y',np.where(m.any(1))[0][[0,-1]],'schaal',round(s,3),'top',top,'left',left)
a=np.zeros((64,64,4),'uint8'); a[m]=[0,0,0,255]; Image.fromarray(a).save('silhouet.png')
g=np.zeros((64,64,4),'uint8'); g[m,:3]=mean[m].astype('uint8'); g[m,3]=255; Image.fromarray(g).save('gids_gemiddeld.png')
src=Image.open('../referenties/model_gekozen.png').convert('RGB').crop((int(x0-left*s),int(y0-top*s),int(x0+(64-left)*s),int(y0+(64-top)*s))).resize((512,512),Image.LANCZOS)
o=np.asarray(src).copy()
pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
o[np.kron(edge,np.ones((8,8),bool))]=[255,0,0]
Image.fromarray(o).save('silhouet_over_bron.png')
