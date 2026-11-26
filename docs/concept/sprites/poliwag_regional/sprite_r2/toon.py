# Raster (npy) -> 8x png voor controle. python3 toon.py raster.npy uit.png [schaal]
import sys, numpy as np; from PIL import Image
from palet import PAL
a=np.load(sys.argv[1]); s=int(sys.argv[3]) if len(sys.argv)>3 else 8
rgb=np.zeros(a.shape+(3,),'uint8'); rgb[:]=(255,255,255)
for k in range(1,16): rgb[a==k]=PAL[k]
Image.fromarray(rgb).resize((a.shape[1]*s,a.shape[0]*s),Image.NEAREST).save(sys.argv[2])
