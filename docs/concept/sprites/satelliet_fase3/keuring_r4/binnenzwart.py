# Keurder r4: zwarte pixels (idx 1) die nergens (8-buren) aan transparant grenzen = zwart als binnenlijn.
from PIL import Image; import numpy as np
a=np.array(Image.open('docs/concept/sprites/satelliet_fase3/sprite/r4/sprite.png'))
k=np.array(Image.open('docs/concept/sprites/satelliet_fase3/sprite/r4/kaal.png'))
r=[]
for y in range(1,63):
  for x in range(1,63):
    if a[y,x]==1 and (a[y-1:y+2,x-1:x+2]>0).all(): r.append((x,y,int(k[y,x])))
print(len(r)); print(r)
