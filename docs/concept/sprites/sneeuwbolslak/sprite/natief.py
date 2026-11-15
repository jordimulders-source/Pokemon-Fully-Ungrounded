import sys; from PIL import Image; import numpy as np
a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(int)
p,ph=10.24,9.5
xs=np.arange(ph+p/2,1024,p); W=len(xs)
out=np.zeros((W,W,3),'uint8')
for j,y in enumerate(xs):
    for i,x in enumerate(xs):
        y0,y1=int(y-2),int(y+3); x0,x1=int(x-2),int(x+3)
        out[j,i]=np.median(a[y0:y1,x0:x1].reshape(-1,3),axis=0)
g=out.astype(int).sum(axis=2); yy,xx=np.where(g<700)
print(W,'bbox',xx.min(),xx.max(),yy.min(),yy.max(), 'size',xx.max()-xx.min()+1,yy.max()-yy.min()+1)
cx=(xx.min()+xx.max())//2; cy=(yy.min()+yy.max())//2
crop=Image.fromarray(out).crop((cx-32,cy-32,cx+32,cy+32))
crop.save(sys.argv[2]); crop.resize((256,256),Image.NEAREST).save(sys.argv[2].replace('.png','_x4.png'))
