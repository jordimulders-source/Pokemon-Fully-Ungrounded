# modelcel.py: gemiddelde modelkleur per spritecel (zelfde mapping als modelgrid.py) -> modelcel.npy (64,64,3) + dekking
import numpy as np; from PIL import Image
M=np.asarray(Image.open('../../MODEL.png').convert('RGB')).astype(float)
s=2.8888889; x0=32; y0=8
C=np.zeros((64,64,3)); A=np.zeros((64,64))
for cy in range(64):
  for cx in range(64):
    a=((x0+(cx-6)*s)*5.12-0.12,(y0+(cy-1)*s)*5.12-0.12); b=((x0+(cx-5)*s)*5.12-0.12,(y0+cy*s)*5.12-0.12)
    sl=M[max(0,int(round(a[1]))):min(1024,int(round(b[1]))),max(0,int(round(a[0]))):min(1024,int(round(b[0])))]
    if sl.size==0: continue
    fg=sl.reshape(-1,3); m=fg.min(1)<235
    A[cy,cx]=m.mean()
    if m.sum(): C[cy,cx]=fg[m].mean(0)
np.save('modelcel.npy',C); np.save('modeldek.npy',A)
