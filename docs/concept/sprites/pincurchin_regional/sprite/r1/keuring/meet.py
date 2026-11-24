import sys
from PIL import Image
import numpy as np
from collections import Counter
im=np.array(Image.open(sys.argv[1]).convert('RGBA'))
H,W=im.shape[:2]
cols=Counter()
for y in range(H):
  for x in range(W):
    if im[y,x,3]>0: cols[tuple(im[y,x,:3])]+=1
pal=sorted(cols,key=lambda c:sum(c))
idx={c:i for i,c in enumerate(pal)}
for c in pal:
  print(idx[c],c,'lum',int(0.299*c[0]+0.587*c[1]+0.114*c[2]),'n',cols[c])
# grid
chars='0123456789abcdefghijklmnopqrstuvwxyz'
for y in range(H):
  row=''
  for x in range(W):
    row+= chars[idx[tuple(im[y,x,:3])]] if im[y,x,3]>0 else '.'
  print('%2d %s'%(y,row))
