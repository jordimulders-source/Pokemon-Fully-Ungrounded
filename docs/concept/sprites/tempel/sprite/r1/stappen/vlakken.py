# vlakken.py: vlakken van het model = gebieden tussen de dikke (structurele) lijnen; per vlak de mediaan-helderheid
import numpy as np
from PIL import Image, ImageFilter
from collections import deque
M='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/tempel/referenties/model.webp'
im=Image.open(M).convert('RGB'); c=np.asarray(im).astype(int); L=c.mean(2)
lines=np.asarray(Image.open('lijnen_model.png'))>0
li=Image.fromarray((lines*255).astype('uint8'))
op=np.asarray(li.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5)))>0
thick=np.asarray(Image.fromarray((op*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0
fg=L<235
free=fg&~thick&~(L<45)
lab=np.zeros(L.shape,int); n=0
H,W=L.shape
for y0 in range(0,H,2):
  for x0 in range(0,W,2):
    if free[y0,x0] and not lab[y0,x0]:
      n+=1; q=deque([(y0,x0)]); lab[y0,x0]=n
      while q:
        y,x=q.popleft()
        for yy,xx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
          if 0<=yy<H and 0<=xx<W and free[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; q.append((yy,xx))
print('vlakken',n)
np.save('labels.npy',lab)
