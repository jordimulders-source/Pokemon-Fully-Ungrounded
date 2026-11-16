import sys; sys.path.insert(0,'sprite_r1')
from groepen import laad; import numpy as np; from PIL import Image
a,lum,g=laad('sprite_r2/natief.png')
im=Image.open('sprite_r2/pitahaya_r2.png'); S=np.array(im); P=np.array(im.getpalette()[:48]).reshape(16,3); L=(P*[.299,.587,.114]).sum(1)
def doel(x,y):
  r=3*(y+2); c=1+3*(x+1); gb=g[r:r+3,c:c+3]; b=lum[r:r+3,c:c+3]
  cnt={k:(gb==k).sum() for k in (1,2,3,4)}
  k=max((2,3,4),key=lambda k:cnt[k]) 
  m=gb==k; ml=b[m].mean()
  opts=[3,4,5] if k in(2,3) else [9,10,11]
  t=min(opts,key=lambda i:abs(L[i]-ml))
  return dict(px=(x,y),nu=int(S[y,x]),zwart9=int(cnt[1]),groep='roze' if k in(2,3) else 'groen',vullum=round(ml),vultint=t)
pts=[(37,10),(36,15),(29,18),(38,27),(33,16),(34,16),(41,24),(25,14),(30,13),(31,14),(31,15),(25,39),(25,40),(33,39),(20,43),(21,43),(21,44),(17,45),(33,45),(23,49),(23,50),(20,52),(21,52),(38,39),(39,39),(38,40),(37,31),(35,25),(42,27),(40,30),(42,15),(43,23),(40,19),(35,19)]
for p in pts: print(doel(*p))
