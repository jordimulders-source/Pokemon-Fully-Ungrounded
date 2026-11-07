# lgrid.py x0 y0 x1 y1: model-helderheid gem/p15 per spritepixel als tabel (meting).
import sys,json,numpy as np; from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
k=json.load(open(P+'gereedschap/kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(P+'model/model_lijf_30.png')).astype(float)
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('    '+''.join(f'{x:>8d}' for x in range(x0,x1)))
for y in range(y0,y1):
  r=f'{y:3d} '
  for x in range(x0,x1):
    b=c[int(Y0+y*s):int(Y0+(y+1)*s),int(X0+x*s):int(X0+(x+1)*s)]; f=b[...,3]>0
    if not f.any(): r+='       -'; continue
    L=b[...,:3][f].mean(1); r+=f' {L.mean():3.0f}/{np.percentile(L,15):<3.0f}'
  print(r)
