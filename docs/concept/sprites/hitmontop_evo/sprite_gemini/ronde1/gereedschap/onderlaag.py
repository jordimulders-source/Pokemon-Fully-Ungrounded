# onderlaag.py: MEETKAART/onderlaag (geen eindsprite). Per spritepixel van het (ingekorte) model:
# alpha>=0.45 -> silhouet; zwart-aandeel >=0.30 -> omlijning; anders meest voorkomende modelmateriaalkleur -> paletindex.
import json,numpy as np; from PIL import Image
from palet import PAL,CH
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde1/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(G+k['model'])).astype(float); H,W=c.shape[:2]
MOD=[((198,150,124),3),((150,102,78),4),((112,76,56),5),((248,248,248),6),((198,198,200),7),
     ((248,216,72),9),((180,146,80),10),((72,136,64),12),((120,184,72),11),((88,136,184),14),((56,88,136),15)]
M=np.array([m for m,_ in MOD],float); I=[i for _,i in MOD]
R=[]
for y in range(64):
  r=''
  for x in range(64):
    ya,yb=int(Y0+y*s),int(Y0+(y+1)*s); xa,xb=int(X0+x*s),int(X0+(x+1)*s)
    ya,xa=max(ya,0),max(xa,0); b=c[ya:min(yb,H),xa:min(xb,W)]
    if b.size==0: r+='.'; continue
    f=b[...,3]>0
    if f.mean()<0.45: r+='.'; continue
    rgb=b[...,:3][f]; L=rgb.mean(1)
    if (L<60).mean()>=0.30: r+='1'; continue
    rgb=rgb[L>=60]; d=((rgb[:,None,:]-M[None])**2).sum(2).argmin(1)
    r+=CH[I[np.bincount(d,minlength=len(I)).argmax()]]
  R.append(r)
open(G+'../onderlaag.txt','w').write('\n'.join(R)+'\n')
print('\n'.join(f'{i:2d} {l}' for i,l in enumerate(R)))
