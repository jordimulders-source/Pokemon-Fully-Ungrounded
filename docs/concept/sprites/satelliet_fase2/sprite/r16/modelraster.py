# Model op het 64-raster: per spritepixel de meest voorkomende (gekwantiseerde) kleur in het modelblok.
from PIL import Image
import numpy as np
m=np.array(Image.open('../../paneel_varianten/panelen_80b.png').convert('RGB')).astype(int)
X0,Y0,s,T=103,143,12.703,7
out=np.full((64,64,4),0,np.uint8)
for y in range(64):
  for x in range(64):
    ya,yb=int(Y0+(y-T)*s),int(Y0+(y+1-T)*s); xa,xb=int(X0+x*s),int(X0+(x+1)*s)
    if ya<0 or yb>1024 or xb>1024: continue
    blk=m[ya:yb,xa:xb].reshape(-1,3); q=(blk//24)*24+12
    u,c=np.unique(q,axis=0,return_counts=True); k=u[c.argmax()]
    if k.mean()<240: out[y,x,:3]=k; out[y,x,3]=255
Image.fromarray(out,'RGBA').save('modelraster64.png')
Image.fromarray(out,'RGBA').resize((512,512),Image.NEAREST).save('modelraster64_8x.png')
