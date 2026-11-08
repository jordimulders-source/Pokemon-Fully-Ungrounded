# onderlaag2.py [model.png] : ONDERLAAG (geen eindsprite). Silhouet = alpha>=0.45 van het ingekorte model (gaten die in het
# model achtergrond zijn blijven open); buitenste ring van het silhouet = omlijning 1; binnen: zwart-aandeel>=0.40 -> 1,
# anders het meest voorkomende modelmateriaal. Daarna gaat alles met de hand.
import sys,json,numpy as np; from PIL import Image
from palet import PAL,CH
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde1/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(G+(sys.argv[1] if len(sys.argv)>1 else k['model']))).astype(float); H,W=c.shape[:2]
MOD=[((198,150,124),3),((150,102,78),4),((112,76,56),5),((248,248,248),6),((198,198,200),7),
     ((248,216,72),9),((180,146,80),10),((72,136,64),12),((120,184,72),11),((88,136,184),14),((56,88,136),15)]
M=np.array([m for m,_ in MOD],float); I=[i for _,i in MOD]
A=np.zeros((64,64)); K=np.zeros((64,64),int); D=np.zeros((64,64))
for y in range(64):
  for x in range(64):
    ya,yb=max(int(Y0+y*s),0),min(int(Y0+(y+1)*s),H); xa,xb=max(int(X0+x*s),0),min(int(X0+(x+1)*s),W)
    if ya>=yb or xa>=xb: continue
    b=c[ya:yb,xa:xb]; f=b[...,3]>0; A[y,x]=f.mean()
    if not f.any(): continue
    rgb=b[...,:3][f]; L=rgb.mean(1); D[y,x]=(L<60).mean()
    r=rgb[L>=60]
    if len(r): K[y,x]=I[np.bincount(((r[:,None,:]-M[None])**2).sum(2).argmin(1),minlength=len(I)).argmax()]
    else: K[y,x]=1
m=A>=0.45
p=np.pad(m,1); rand=m&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
R=[]
for y in range(64):
  r=''
  for x in range(64):
    if not m[y,x]: r+='.'
    elif rand[y,x] or D[y,x]>=0.40: r+='1'
    else: r+=CH[K[y,x]]
  R.append(r)
print('\n'.join(R))
