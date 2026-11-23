# toon.py raster.npy out.png [8x.png]: palet + opslaan
import numpy as np, sys
from PIL import Image
from pal import PAL
G=np.load(sys.argv[1])
im=Image.fromarray(G.astype('uint8'),'P'); im.putpalette([v for c in PAL+[(0,0,0)]*3 for v in c]); im.save(sys.argv[2],transparency=0)
if len(sys.argv)>3:
    rgb=np.array(PAL+[(0,0,0)]*3,dtype='uint8')[G]; rgb[G==0]=255
    Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(sys.argv[3])
