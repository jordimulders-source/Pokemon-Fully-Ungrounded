# stap 2 (zoals Krassault glad.py): uitsteeksels van 1 px op tintgrenzen glad; alleen vulkleuren, per groep
import numpy as np; from PIL import Image
from collections import Counter
im=Image.open('r19.png'); pal=im.getpalette(); o=np.array(im).copy(); vap=np.load('r15w/vap.npy')
ICE={2,3,4,5}; PUR={7,8,9,10}; GAS={2,3,11,15}
tot=0
for it in range(2):
  p=o.copy(); n=0
  for y in range(1,63):
    for x in range(1,63):
      c=p[y,x]
      g=(GAS if c in GAS else None) if vap[y,x] else (ICE if c in ICE else (PUR if c in PUR else None))
      if g is None: continue
      nb=[p[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1)) if vap[y+dy,x+dx]==vap[y,x]]
      cnt=Counter(k for k in nb if k in g and k!=c)
      if cnt:
        t,k=cnt.most_common(1)[0]
        if k>=3: o[y,x]=t; n+=1
  tot+=n
print('glad',tot)
a=np.array(Image.open('r18.png')); assert ((np.isin(a,[1,6,13,12,14]))==(np.isin(o,[1,6,13,12,14]))).all()
out=Image.fromarray(o).convert('P'); out.putpalette(pal); out.save('r19.png',transparency=0)
