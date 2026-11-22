import sys; from PIL import Image; import numpy as np
IN,OUT,p,ph=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4])
a=np.asarray(Image.open(IN).convert('RGB')).astype(int)
cs=np.arange(ph+p/2,1024,p); n=len(cs); out=np.zeros((n,n,3),'uint8')
for j,y in enumerate(cs):
  for i,x in enumerate(cs):
    r=max(1,int(p/4)); out[j,i]=np.median(a[int(y)-r:int(y)+r+1,int(x)-r:int(x)+r+1].reshape(-1,3),axis=0)
Image.fromarray(out).save(OUT); Image.fromarray(out).resize((n*8,n*8),Image.NEAREST).save(OUT.replace('.png','_8x.png')); print(n)
