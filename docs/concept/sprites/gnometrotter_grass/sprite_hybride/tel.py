# tel.py (Grass): afwijking van gnometrotter_grass.png t.o.v. de kale reductie (kaal.png), per onderdeel, uitgesplitst naar oorzaak
import numpy as np
from gemeen import *
o=lees('gnometrotter_grass_hybride.png'); k=lees('kaal.png'); r=lees('red.png'); z=np.load('zone_af.npy')
fg=(o>0)|(k>0); d=fg&(o!=k)
lijn=np.zeros((64,64),bool)
for Y,X in zip(*np.where(o>0)): lijn[Y,X]=o[Y,X] in (1,BASIS[z[Y,X]],6)
dc=(o!=r)
print('| zone | px anders / zone | lijn | DC | vlaktint/volume |'); print('|---|---|---|---|---|')
for zz,n in ZNAAM.items():
    m=z==zz
    print('| %s | %d / %d | %d | %d | %d |'%(n,(d&m).sum(),m.sum(),(d&m&lijn&~dc).sum(),(d&m&dc).sum(),(d&m&~lijn&~dc).sum()))
print('| **totaal** | **%d / %d** | %d | %d | %d |'%(d.sum(),(o>0).sum(),(d&lijn&~dc).sum(),(d&dc).sum(),(d&~lijn&~dc).sum()))
print('silhouet: %d px anders (in kaal niet in sprite: %d, andersom: %d)'%(((o>0)!=(k>0)).sum(),((k>0)&(o==0)).sum(),((o>0)&(k==0)).sum()))
ys,xs=np.where((o>0)&(k==0)); print('erbij:',list(zip(xs.tolist(),ys.tolist())))
ys,xs=np.where((o==0)&(k>0)); print('eraf:',list(zip(xs.tolist(),ys.tolist())))
