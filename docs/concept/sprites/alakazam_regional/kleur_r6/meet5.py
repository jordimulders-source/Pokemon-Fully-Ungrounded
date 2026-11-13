# meet5: per spritepixel: fo = fractie omlijning (L<20) in het modelblok, med = mediaan RGB van de niet-omlijningspixels, p15, gem
import sys,os,numpy as np
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from geo import *
from PIL import Image
c=model().astype(float); L=c.mean(2)
sil=np.asarray(Image.open(H+'/../silhouet/silhouet.png'))[...,3]>0
med=np.zeros((64,64,3)); fo=np.zeros((64,64)); p15=np.zeros((64,64)); gem=np.zeros((64,64))
for Y in range(64):
  for X in range(64):
    ya,yb,xa,xb=blok(X,Y); ya,xa=max(ya,0),max(xa,0)
    b=c[ya:yb,xa:xb].reshape(-1,3); l=b.mean(1)
    fo[Y,X]=(l<20).mean(); p15[Y,X]=np.percentile(l,15); gem[Y,X]=l.mean()
    nb=b[l>=20]; med[Y,X]=np.median(nb,0) if len(nb) else 0
np.savez(H+'/meet5.npz',med=med,fo=fo,sil=sil,p15=p15,gem=gem)
