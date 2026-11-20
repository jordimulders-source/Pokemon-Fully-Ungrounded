# tekstraster -> 64x64 geindexeerde png + 8x. Gebruik: python3 topng.py IN.txt UIT (zonder .png)
import numpy as np; from PIL import Image; import sys
from reduce_pal import PAL
o=np.loadtxt(sys.argv[1],dtype=int); H,W=o.shape
full=np.zeros((64,64),int); x0=(64-W)//2; full[63-H:63,x0:x0+W]=o
im=Image.fromarray(full.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL)))
im.save(sys.argv[2]+'.png',transparency=0)
rgb=np.array(PAL)[full].astype('uint8'); Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(sys.argv[2]+'_8x.png')
print((full>0).sum(),'px', 'kleuren',len(set(full.ravel()))-1)
