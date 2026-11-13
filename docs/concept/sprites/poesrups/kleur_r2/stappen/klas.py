# klas.py: meetkaart (geen sprite): per spritepixel de modelklasse. #=zwart(gem<70) o=donker(70-110) -=lijnmix(p10<60, gem>=110)
#          verder helderheid gem: 1=<140 2=<170 3=<195 4=<215 5=<228 6=wit ; '.' buiten silhouet
import numpy as np
from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/poesrups/'
c=np.asarray(Image.open(P+'referenties/model_gekozen.png').convert('RGB')).astype(float);L=c.mean(2)
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from bg import masker; g=masker()
a=np.array(Image.open(P+'silhouet/silhouet.png'))[:,:,3]>0
x0,y0=69,240; s=16.648
print('   '+''.join(str(x%10) for x in range(4,60)))
for y in range(28,63):
  r=''
  for x in range(4,60):
    if not a[y,x]: r+='.'; continue
    sl=(slice(int(y0+(y-29)*s),int(y0+(y-28)*s)),slice(int(x0+(x-5)*s),int(x0+(x-4)*s)))
    f=~g[sl]; v=L[sl][f]; m=v.mean(); p=np.percentile(v,10)
    r+= '#' if m<70 else 'o' if m<110 else '-' if p<60 else '1' if m<140 else '2' if m<170 else '3' if m<195 else '4' if m<215 else '5' if m<228 else '6'
  print(f'{y:2d} '+r)
