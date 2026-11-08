# silhouet = Gemini v4 verkleind (methode poedelmot/silhouet/sil.py)
import numpy as np
from PIL import Image
from collections import deque
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/olinguito_v2/'
c=np.asarray(Image.open(D+'gemini/ronde2_v4_pose.png').convert('RGB')).astype(int)
fg=c.min(2)<215
S=15.5            # bronpixels per spritepixel
X0=184-S*11       # spritekolom 0 in bron
Y0=977-S*62       # onderkant voeten = rij 61
H=64;W=64
mean=np.zeros((64,64,3)); alpha=np.zeros((64,64))
for by in range(64):
  for bx in range(64):
    ya,yb=int(Y0+by*S),int(Y0+(by+1)*S); xa,xb=int(X0+bx*S),int(X0+(bx+1)*S)
    if ya<0 or xa<0 or yb>1024 or xb>1024: continue
    f=fg[ya:yb,xa:xb]; alpha[by,bx]=f.mean()
    if f.any(): mean[by,bx]=c[ya:yb,xa:xb][f].mean(0)
m=alpha>=0.45
bg=np.zeros_like(m); q=deque([(0,0)]); bg[0,0]=1
while q:
    y,x=q.popleft()
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
        yy,xx=y+dy,x+dx
        if 0<=yy<64 and 0<=xx<64 and not m[yy,xx] and not bg[yy,xx]: bg[yy,xx]=1; q.append((yy,xx))
m=~bg
print('px',m.sum(),'box',np.where(m.any(0))[0][[0,-1]],np.where(m.any(1))[0][[0,-1]])
np.save('stappen/sil.npy',m); np.save('stappen/gids.npy',mean)
a=np.zeros((64,64,4),'uint8'); a[m]=[0,0,0,255]; Image.fromarray(a).save('silhouet.png')
g=np.zeros((64,64,4),'uint8'); g[m,:3]=mean[m].astype('uint8'); g[m,3]=255; Image.fromarray(g).resize((512,512),0).save('gids_gemiddeld_8x.png')
src=Image.open(D+'gemini/ronde2_v4_pose.png').convert('RGB')
pad=Image.new('RGB',(2000,2000),'white'); pad.paste(src,(500,500))
src=pad.crop((int(X0+500),int(Y0+500),int(X0+500+64*S),int(Y0+500+64*S))).resize((512,512),Image.LANCZOS)
src.save('stappen/model_512.png')
o=np.asarray(src).copy()
p=np.pad(m,1); edge=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
o[np.kron(edge,np.ones((8,8),bool))]=[255,0,0]
Image.fromarray(o).save('silhouet_over_model.png')
for r in m: print(''.join('#' if v else '.' for v in r))
