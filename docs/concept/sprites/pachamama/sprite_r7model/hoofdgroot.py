# Jordi 27 nov ("hier kan je smokkelen"): gezicht groter binnen het huidige silhouet, vooral omhoog/omlaag.
# Op het natieve raster: gezicht + binnenlijn + kaprand (ring 5 px) vergroot (nearest, niets getekend) en teruggeplakt;
# buitenrand van het silhouet (2 px van de achtergrond) blijft origineel. Gebruik: python3 hoofdgroot.py SH SV X0 Y0 Y1 UIT
import sys; from PIL import Image; import numpy as np
SH,SV=float(sys.argv[1]),float(sys.argv[2]); TX0,TY0=int(sys.argv[3]),int(sys.argv[4]); UIT=sys.argv[5]
a=np.asarray(Image.open('natief.png')).copy(); bg=np.load('bg.npy'); g=np.load('gezmask.npy')
def dil(m,k):
    for _ in range(k):
        p=np.pad(m,1); m=p[1:-1,1:-1]|p[:-2,1:-1]|p[2:,1:-1]|p[1:-1,:-2]|p[1:-1,2:]
    return m
R=dil(g,5)&~bg; rand=dil(bg,2)
SX0,SY0=63,22          # bron: linkerkant en top van het gezicht
H,W=bg.shape; o=a.copy(); nm=np.zeros_like(g)
for y in range(H):
  for x in range(W):
    sy=int(np.floor(SY0+(y-TY0)/SV+.5)); sx=int(np.floor(SX0+(x-TX0)/SH+.5))
    if not(0<=sy<H and 0<=sx<W) or not R[sy,sx]: continue
    if bg[y,x]: continue
    if rand[y,x] and not g[sy,sx]: continue
    o[y,x]=a[sy,sx]; nm[y,x]=g[sy,sx]
Image.fromarray(o).save(UIT); np.save(UIT.replace('.png','_gez.npy'),nm)
ys,xs=np.where(nm); print('nieuw gezicht',xs.min(),xs.max(),ys.min(),ys.max(),'raakt rand',(nm&rand).sum())
