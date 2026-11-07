from seg import *
c=np.asarray(Image.open('comp.png')).astype(int)
fg=~green(c); lum=c.mean(2)
fg&=~((c[...,1]>c[...,0]+8)&(lum<110)); fg[672:]=False
x0,x1,y0,y1=139,854,150,672
W=62; s=(x1-x0)/W; Hh=int(np.ceil((y1-y0)/s)); top=64-Hh-1; left=1
mean=np.zeros((64,64,3)); alpha=np.zeros((64,64))
for by in range(Hh):
  for bx in range(W):
    ya,yb=int(y0+by*s),int(y0+(by+1)*s); xa,xb=int(x0+bx*s),int(x0+(bx+1)*s)
    f=fg[ya:yb,xa:xb]; alpha[top+by,left+bx]=f.mean()
    if f.any(): mean[top+by,left+bx]=c[ya:yb,xa:xb][f].mean(0)
m=alpha>=0.45
# fill holes: background not connected to border
from collections import deque
bg=np.zeros_like(m); q=deque([(0,0)]); bg[0,0]=1
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<64 and 0<=xx<64 and not m[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
m=~bg
print('px',m.sum(),'box',np.where(m.any(0))[0][[0,-1]],np.where(m.any(1))[0][[0,-1]])
a=np.zeros((64,64,4),'uint8'); a[m]=[0,0,0,255]; Image.fromarray(a).save('silhouet.png')
g=np.zeros((64,64,4),'uint8'); g[m,:3]=mean[m].astype('uint8'); g[m,3]=255; Image.fromarray(g).save('gids_gemiddeld.png')
# overlay: source composite resized to 512 with red outline
src=Image.open('comp.png').crop((int(x0-left*s),int(y0-top*s),int(x0+(64-left)*s),int(y0+(64-top)*s))).resize((512,512),Image.LANCZOS)
o=np.asarray(src).copy()
pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
big=np.kron(edge,np.ones((8,8),bool)); o[big]=[255,0,0]
Image.fromarray(o).save('silhouet_over_bron.png')
