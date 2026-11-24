# Haalt het eigen pixelraster van het Gemini-model terug: pitch 10,24 px (gemeten met randsterkte), fase 9,25 -> natief.png (100x100)
from PIL import Image; import numpy as np
a=np.asarray(Image.open('../model.png').convert('RGB')).astype(int)
p,ph=10.24,9.25
cs=np.arange(ph+1+p/2-p, 1024, p); cs=cs[cs>=2]
W=len(cs); out=np.zeros((W,W,3),'uint8')
for j,y in enumerate(cs):
  for i,x in enumerate(cs):
    y0,y1=int(y-2),int(y+3); x0,x1=int(x-2),int(x+3)
    b=a[max(0,y0):min(1024,y1),max(0,x0):min(1024,x1)].reshape(-1,3)
    out[j,i]=np.median(b,0)
Image.fromarray(out).save('natief.png'); print(W)
im=Image.fromarray(out).resize((W*8,W*8),Image.NEAREST); im.save('natief_8x.png')
g=out.min(2); ys,xs=np.where(g<230); print('bbox',xs.min(),xs.max(),ys.min(),ys.max(),xs.max()-xs.min()+1,ys.max()-ys.min()+1)
