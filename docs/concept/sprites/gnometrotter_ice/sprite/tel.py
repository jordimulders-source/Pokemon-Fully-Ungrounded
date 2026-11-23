# tel.py: afwijking van gnometrotter_ice.png t.o.v. de kale reductie (kaal.png), per onderdeel, uitgesplitst naar oorzaak
import numpy as np
from gemeen import *
o=lees('gnometrotter_ice.png'); k=lees('kaal.png'); r=lees('red.png'); z=np.load('zone_af.npy'); oog=np.load('oog.npy')&(np.load('zone.npy')!=5)
fg=(o>0)|(k>0); d=fg&(o!=k)
lijn=np.zeros((64,64),bool)
for Y,X in zip(*np.where(o>0)): lijn[Y,X]=o[Y,X] in (1,BASIS[z[Y,X]]) or (z[Y,X] in (5,8,9) and o[Y,X]==6)
dc=(o!=r)
print('zone            anders/zone  lijn  oogstrook  DC+gesp  vlak(tint)')
for zz,n in ZNAAM.items():
    m=z==zz
    print('%-14s %4d / %4d  %4d  %4d  %4d  %4d'%(n,(d&m).sum(),m.sum(),(d&m&lijn&~dc).sum(),(d&m&oog).sum(),(d&m&dc).sum(),(d&m&~lijn&~oog&~dc).sum()))
print('silhouet: %d px anders (in kaal niet in sprite: %d, andersom: %d)'%(((o>0)!=(k>0)).sum(),((k>0)&(o==0)).sum(),((o>0)&(k==0)).sum()))
print('totaal anders %d / %d'%(d.sum(),(o>0).sum()))
ys,xs=np.where((o>0)&(k==0)); print('erbij:',list(zip(xs.tolist(),ys.tolist())))
