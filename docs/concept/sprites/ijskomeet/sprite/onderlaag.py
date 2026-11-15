# 3x-reductie van het natieve raster (klassen) naar 64x64-onderlaag.
import sys; from PIL import Image; import numpy as np
lab=np.load('lab.npy'); H,W=lab.shape
ox,oy=int(sys.argv[1]),int(sys.argv[2]); dx,dy=int(sys.argv[3]),int(sys.argv[4])  # fase en plek in het vak
names=['lijn','ijs_hi','ijs_l','ijs_m','ijs_d','ijs_dd','sp_d','sp_m','nev','nev_l','waas','gas','oog','oog_k','oog_r']
out=np.full((64,64),-1)
for j in range(64):
    for i in range(64):
        y0=oy+3*(j-dy); x0=ox+3*(i-dx)
        if y0<0 or x0<0 or y0+3>H or x0+3>W: continue
        b=lab[y0:y0+3,x0:x0+3].ravel(); fg=b[b>=0]
        if len(fg)<4: continue
        c=np.bincount(fg,minlength=15)
        if c[12]+c[13]+c[14]>=3: out[j,i]=12 if c[12]>=c[14] else 14
        elif c[0]>=3: out[j,i]=0
        else: out[j,i]=c.argmax()
np.save(sys.argv[5],out)
