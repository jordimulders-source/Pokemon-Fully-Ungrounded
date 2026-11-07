# dek.py x0 y0 x1 y1 : per spritepixel aandeel zwart (L<60) en wit (L>225, grijs) in het model, in tienden: "zw" (meting)
import sys,json,numpy as np; from PIL import Image
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(G+k['model'])).astype(float)
x0,y0,x1,y1=map(int,sys.argv[1:5])
print('   '+''.join(f'{x:>4d}' for x in range(x0,x1)))
for y in range(y0,y1):
  r=''
  for x in range(x0,x1):
    b=c[int(Y0+y*s):int(Y0+(y+1)*s),int(X0+x*s):int(X0+(x+1)*s)]
    f=b[...,3]>0; L=b[...,:3].mean(2)
    if f.mean()<0.3: r+='   .'; continue
    zw=((L<60)&f).sum()/f.sum(); w=((L>225)&f).sum()/f.sum(); md=(((L>=60)&(L<100))&f).sum()/f.sum()
    r+=f' {min(9,int(zw*10))}{min(9,int(w*10))}{min(9,int(md*10))}'
  print(f'{y:3d}'+r)
