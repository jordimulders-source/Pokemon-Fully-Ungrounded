import numpy as np, sys; sys.path.insert(0,'.')
from PIL import Image
from antennes import rods
o=np.load(sys.argv[1]); Zs=np.zeros_like(o,bool)
# beschermd: paneel (zone 2), lijf
k=np.load('klassen2.npy'); Z=np.array(Image.open('zones.png')); s=(978-46)/64
for j in range(o.shape[0]):
  for i in range(64):
    y0,y1=int(round(143+j*s)),int(round(143+(j+1)*s)); x0,x1=int(round(46+i*s)),int(round(46+(i+1)*s))
    b=k[y0:y1,x0:x1]; z=Z[y0:y1,x0:x1]
    if (z==2).mean()>0.5 or np.isin(b,[2,3,4,5]).mean()>0.35: Zs[j,i]=True
np.save('Zs.npy',Zs)
o=rods(o,Zs); np.save(sys.argv[2],o)
