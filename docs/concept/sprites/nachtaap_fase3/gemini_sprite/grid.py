from PIL import Image; import numpy as np
a=np.asarray(Image.open('../gemini/gekozen_r4.png')).astype(int)
g=np.zeros((128,128,3),int)
for j in range(128):
  for i in range(128):
    x=8*i-2+4; y=8*j-1+4   # cell starts x=8i-2, y=8j-1
    x0,y0=max(0,x-2),max(0,y-2)
    blk=a[y0:y+2,x0:x+2].reshape(-1,3)
    g[j,i]=np.median(blk,0)
Image.fromarray(g.astype('uint8')).save('grid128.png')
Image.fromarray(g.astype('uint8')).resize((768,768),Image.NEAREST).save('grid128_6x.png')
