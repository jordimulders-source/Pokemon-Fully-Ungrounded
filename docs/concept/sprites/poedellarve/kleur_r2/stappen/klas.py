# klas.py: meetkaart (geen sprite): per spritepixel de modelklasse. #=zwart(gem<70) o=donker(70-110) -=lijnmix(p10<60, gem>=110)
#          verder helderheid gem: 1=<140 2=<170 3=<195 4=<215 5=<228 6=wit ; '.' buiten silhouet
import numpy as np
from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poedellarve/'
c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(float);L=c.mean(2)
g=(c[...,1]>c[...,0]+40)&(c[...,0]<120)
a=np.array(Image.open(P+'silhouet/silhouet.png'))[:,:,3]>0
x0,y0=236,346; s=13.55
print('   '+''.join(str(x%10) for x in range(10,54)))
for y in range(32,64):
  r=''
  for x in range(10,54):
    if not a[y,x]: r+='.'; continue
    sl=(slice(int(y0+(y-33)*s),int(y0+(y-32)*s)),slice(int(x0+(x-12)*s),int(x0+(x-11)*s)))
    f=~g[sl]; v=L[sl][f]; m=v.mean(); p=np.percentile(v,10)
    r+= '#' if m<70 else 'o' if m<110 else '-' if p<60 else '1' if m<140 else '2' if m<170 else '3' if m<195 else '4' if m<215 else '5' if m<228 else '6'
  print(f'{y:2d} '+r)
