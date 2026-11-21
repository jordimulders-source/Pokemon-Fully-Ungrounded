# r6: alleen de linkerrand van de veer (r5V3). Naadsprong weg (rij 4: x9 -> x10), randkleur per deel zoals Rufflet:
# wit deel blauwgrijze rand -> a; rood deel donkerrode rand -> s (Rufflet index 8 aan de rand), voet donker -> n (bestond).
import numpy as np; from PIL import Image; import pal
from pal import *
pal.PAL+=[('r',(216,88,88)),('s',(160,64,64))]; pal.L={c:i for i,(c,_) in enumerate(pal.PAL)}; pal.RGB=np.array([c for _,c in pal.PAL])
b=lees('rufflet_r5V3.txt'); g=b.copy()
FIX=[(4,9,'.'),(4,10,'a'),(7,8,'s'),(8,8,'s'),(9,8,'s')]
for y,x,c in FIX: g[y,x]=c
z=np.zeros(g.shape,bool); z[0:12,6:16]=True   # linkerkant veer
print('gewijzigd:',int((g!=b).sum()),'| diff buiten veerzone links (rij 0-11, x6-15):',int(((g!=b)&~z).sum()),'| silhouet:',int(((g!='.')!=(b!='.')).sum()))
schrijf('rufflet_r6.txt',g)
s=np.full((64,64),'.'); h,w=g.shape; x0=(64-w)//2; s[64-h:64,x0:x0+w]=g
idx=np.vectorize(pal.L.get)(s).astype('uint8'); p=Image.fromarray(idx,'P'); pl=[v for _,c in pal.PAL for v in c]
p.putpalette(pl+[0]*(768-len(pl))); p.save('rufflet_r6.png',transparency=0)
Image.fromarray(pal.rgb(s,(255,255,255))).resize((512,512),Image.NEAREST).save('rufflet_r6_8x.png')
print('\n'.join(''.join(r[5:20]) for r in g[:13]))
