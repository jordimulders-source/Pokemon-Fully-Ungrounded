# r22 = r21 + ogen rond en omlijnd, kopomlijning zonder korrel, kern als gevormde gloed
import numpy as np; from PIL import Image
im=Image.open('r21.png'); pal=im.getpalette(); a=np.array(im).copy()
K,W,L,M,D,S,p,q,r,s,G,e,N,c,g=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
def put(pts,v):
  for x,y in pts: a[y,x]=v
# ogen: ring N, kern e, glans g linksboven, c rechtsonder als schaduw
for (x0,w) in ((4,4),(11,5)):
  x1=x0+w-1
  for y in range(33,38):
    for x in range(x0-1,x1+2):
      if a[y,x] in (e,c,g): a[y,x]=W        # oude oogpixels eerst weg
  put([(x,33) for x in range(x0+1,x1)],N); put([(x,37) for x in range(x0+1,x1)],N)
  for y in (34,35,36): put([(x0,y),(x1,y)],N); put([(x,y) for x in range(x0+1,x1)],e)
  put([(x0+1,34)],g); put([(x1-1,36)],c)
  for x,y in ((x0,33),(x1,33),(x0,37),(x1,37)):
    if a[y,x] in (N,): a[y,x]=W
# kopbovenkant: lavendel binnen de kop -> ijs, erboven -> gas
put([(13,23),(16,23)],L); put([(14,24),(15,24),(12,25),(13,25),(14,25),(11,26),(12,26)],W)
# linkerrand kop: dubbele lijn naast de buitenlijn weg, trap glad
put([(3,42)],L); put([(4,43)],M)
# kern: gevormde gloed (licht linksboven), alleen in paars
cy,cx=34.0,25.0
for y in range(27,42):
  for x in range(19,33):
    if a[y,x] not in (p,q,r,s): continue
    d=np.hypot((x-cx)*0.9,(y-cy))
    if d<=1.5: a[y,x]=s
    elif d<=3.0: a[y,x]=r
    elif d<=4.3: a[y,x]=q
o=Image.fromarray(a).convert('P'); o.putpalette(pal); o.save('r22.png',transparency=0)
o.convert('RGB').resize((512,512),Image.NEAREST).save('r22_8x.png')
