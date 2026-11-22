# png.py: rufflet_r1.txt -> 64x64 geindexeerd (index 0 transparant), onderaan gecentreerd zoals de harpij, + 8x
import numpy as np; from PIL import Image; from pal import *
g=lees('rufflet_r1.txt'); h,w=g.shape
s=np.full((64,64),'.'); x0=(64-w)//2; s[64-h:64,x0:x0+w]=g
idx=np.vectorize(L.get)(s).astype('uint8')
p=Image.fromarray(idx,'P'); pal=[v for _,c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save('rufflet_r1.png',transparency=0)
open('rufflet_r1.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
q=Image.open('rufflet_r1.png'); print(q.mode,q.size,q.info.get('transparency'),'kleuren',len(set(idx.ravel())))
Image.fromarray(rgb(s,(255,255,255))).resize((512,512),Image.NEAREST).save('rufflet_r1_8x.png')
print("bbox x",x0,x0+w-1,"y",64-h,63)
