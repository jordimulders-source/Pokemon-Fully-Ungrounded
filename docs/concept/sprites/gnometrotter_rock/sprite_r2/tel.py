# tel.py: afwijking r2 t.o.v. de kale reductie (../sprite/kaal.png) en t.o.v. r1, per onderdeel
import sys, numpy as np; sys.path.insert(0,'../sprite')
from gemeen import *
o=lees('gnometrotter_rock.png'); k=lees('../sprite/kaal.png'); r1=lees('../sprite/gnometrotter_rock.png'); z=np.load('zone.npy'); naad=np.load('naad.npy')
fg=o>0
print('zone            anders-kaal/zone  anders-r1  waarvan naad')
for zz,n in ZNAAM.items():
    m=z==zz
    print('%-14s %4d / %4d   %4d   %4d'%(n,(m&(o!=k)).sum(),m.sum(),(m&(o!=r1)).sum(),(m&naad&(o!=k)).sum()))
print('totaal t.o.v. kaal %d / %d, t.o.v. r1 %d; silhouet t.o.v. r1: %d px'%((fg&(o!=k)).sum(),fg.sum(),(fg&(o!=r1)).sum(),((o>0)!=(r1>0)).sum()))
