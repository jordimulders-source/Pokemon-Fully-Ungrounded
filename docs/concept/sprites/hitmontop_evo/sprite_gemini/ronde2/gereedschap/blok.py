# blok.py x0 y0 x1 y1 : per spritepixel de modelklasse (meest voorkomend) + dekking; '.'=leeg (<0.45). Meting.
import sys,json,numpy as np; from PIL import Image
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde2/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(G+k['model'])).astype(float)
MOD=[((198,150,124),'b'),((150,102,78),'B'),((112,76,56),'B'),((248,248,248),'w'),((198,198,200),'g'),
     ((248,216,72),'y'),((180,146,80),'o'),((72,136,64),'G'),((120,184,72),'l'),((88,136,184),'u'),((56,88,136),'U')]
M=np.array([m for m,_ in MOD],float)
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('    '+''.join(str(x%10) for x in range(x0,x1)))
for y in range(y0,y1):
  r=''
  for x in range(x0,x1):
    b=c[int(Y0+y*s):int(Y0+(y+1)*s),int(X0+x*s):int(X0+(x+1)*s)]; f=b[...,3]>0
    if f.mean()<0.45: r+='.'; continue
    rgb=b[...,:3][f]; L=rgb.mean(1)
    if (L<60).mean()>=0.35: r+='1'; continue
    rgb=rgb[L>=60]; r+=MOD[np.bincount(((rgb[:,None]-M[None])**2).sum(2).argmin(1),minlength=len(MOD)).argmax()][1]
  print(f'{y:3d} '+r)
