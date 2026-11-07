# Silhouet = model (lijf +30%, Jordi 7 nov: "de meest rechtse") direct verkleind naar 64x64 (poedelmot-methode).
import json, numpy as np; from PIL import Image; from collections import deque
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
im=Image.open(P+'model/model_lijf_30.png'); c=np.asarray(im).astype(float)
al=c[...,3]>0; ys,xs=np.where(al); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
HT=63; s=(y1-y0)/HT; Wd=int(np.ceil((x1-x0)/s)); top=64-HT; left=(64-Wd)//2
json.dump(dict(x0=float(x0-left*s),y0=float(y0-top*s),s=float(s)),open(P+'gereedschap/kader.json','w'))
X0,Y0=x0-left*s,y0-top*s
mean=np.zeros((64,64,3)); alpha=np.zeros((64,64))
for by in range(64):
  for bx in range(64):
    ya,yb=int(Y0+by*s),int(Y0+(by+1)*s); xa,xb=int(X0+bx*s),int(X0+(bx+1)*s)
    if ya<0 or xa<0 or yb>c.shape[0] or xb>c.shape[1]: continue
    f=al[ya:yb,xa:xb]
    if f.size: alpha[by,bx]=f.mean()
    if f.any(): mean[by,bx]=c[ya:yb,xa:xb,:3][f].mean(0)
m=alpha>=0.45
bg=np.zeros_like(m); q=deque([(0,0)]); bg[0,0]=1
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<64 and 0<=xx<64 and not m[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
m=~bg
print('px',m.sum(),'x',np.where(m.any(0))[0][[0,-1]],'y',np.where(m.any(1))[0][[0,-1]],'schaal',round(s,2))
a=np.zeros((64,64,4),'uint8'); a[m]=[0,0,0,255]; Image.fromarray(a).save(P+'silhouet/silhouet.png')
g=np.zeros((64,64,4),'uint8'); g[m,:3]=mean[m].astype('uint8'); g[m,3]=255; Image.fromarray(g).save(P+'silhouet/gids_gemiddeld.png')
bgim=Image.new('RGBA',im.size,(64,160,64,255)); bgim.alpha_composite(im)
src=bgim.convert('RGB').crop((int(X0),int(Y0),int(X0+64*s),int(Y0+64*s)))
src.resize((64,64),Image.BOX).save(P+'silhouet/model_64_box.png')
o=np.asarray(src.resize((512,512),Image.LANCZOS)).copy()
pad=np.pad(m,1); edge=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
o[np.kron(edge,np.ones((8,8),bool))]=[255,0,0]
Image.fromarray(o).save(P+'silhouet/silhouet_over_bron.png')
src.resize((768,768),Image.LANCZOS).save(P+'silhouet/model_12x.png')
