import numpy as np, sys; sys.path.insert(0,'.')
from PIL import Image
from antennes import rods
o=np.load(sys.argv[1]); Zs=np.zeros_like(o,bool)
# beschermd: paneel (zone 2), lijf
k=np.load('klassen2.npy'); Z=np.array(Image.open('zones.png')); from cfg import blok, oudrij
for j in range(o.shape[0]):
  for i in range(64):
    y0,y1,x0,x1=blok(j,i)
    b=k[y0:y1,x0:x1]; z=Z[y0:y1,x0:x1]
    if (z==2).mean()>0.5 or (np.isin(b,[2,3,4,5]).mean()>0.35 and j>=oudrij(7)): Zs[j,i]=True   # r5: lichte staafglans boven rij 7 (oud) is geen lijf
np.save('Zs.npy',Zs)
o2=rods(o,Zs); np.save(sys.argv[2],o2)
# r4: antennezone (niet-beschermd lijf/paneel, rijen 0-11, kolommen 24-49) beschermen tegen de losse-pixelopschoning
from antennes import AJ0,AJ1,AI0,AI1
A=np.zeros_like(Zs); A[AJ0:AJ1,AI0:AI1]=~Zs[AJ0:AJ1,AI0:AI1]; np.save(sys.argv[2].replace('.npy','_ant.npy'),A)
