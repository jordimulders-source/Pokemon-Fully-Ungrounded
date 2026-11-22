# Lijnskelet van het model per spritepixel (spooktrein-methode)
import numpy as np; from skimage.morphology import skeletonize, binary_closing, disk
K=np.load('klassen.npy'); dr=np.load('draden_mask.npy')
ln=(K==1)&~dr
ln=binary_closing(ln,disk(2))
sk=skeletonize(ln)
S=968/62; X0,Y0,OX,OY=24,1,1,4
cnt=np.zeros((64,64))
for j in range(64):
  for i in range(64):
    x0=X0+(i-OX)*S; y0=Y0+(j-OY)*S
    xa,ya,xb,yb=max(int(round(x0)),0),max(int(round(y0)),0),min(int(round(x0+S)),1024),min(int(round(y0+S)),1024)
    if xb>xa and yb>ya: cnt[j,i]=sk[ya:yb,xa:xb].sum()
np.save('skel_cnt.npy',cnt); np.save('skel.npy',sk)
from PIL import Image; Image.fromarray((~sk*255).astype('uint8')).save('skel.png')
