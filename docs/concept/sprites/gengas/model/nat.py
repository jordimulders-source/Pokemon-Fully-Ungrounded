import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int); p=float(sys.argv[2]); ph=float(sys.argv[3])
xs=np.arange(ph+p/2,1024,p); W=len(xs); out=np.zeros((W,W,3),'uint8')
for j,y in enumerate(xs):
  for i,x in enumerate(xs):
    out[j,i]=np.median(a[int(y)-2:int(y)+3,int(x)-2:int(x)+3].reshape(-1,3),axis=0)
im=Image.fromarray(out); im.save(sys.argv[4]); im.resize((W*8,W*8),Image.NEAREST).save(sys.argv[4].replace('.png','_8x.png')); print(W)
