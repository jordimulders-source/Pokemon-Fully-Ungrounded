import sys
from PIL import Image
import numpy as np
from scipy import ndimage
im=np.array(Image.open(sys.argv[1]).convert('RGBA')).astype(int)
op=im[:,:,3]>0
key=im[:,:,0]*65536+im[:,:,1]*256+im[:,:,2]
for k in np.unique(key[op]):
  m=(key==k)&op
  lab,n=ndimage.label(m)  # 4-connectivity
  for i in range(1,n+1):
    ys,xs=np.where(lab==i)
    if len(ys)<3:
      c=(k>>16,(k>>8)&255,k&255)
      print(c,len(ys),list(zip(xs.tolist(),ys.tolist())))
