# tel.py [sprite] [kaal] [r1] [zone]: afwijking per onderdeel t.o.v. de kale reductie en t.o.v. r1
import sys, numpy as np; sys.path.insert(0,'../sprite')
from gemeen import lees, ZNAAM
s=sys.argv[1] if len(sys.argv)>1 else 'gnometrotter_ice.png'; k=lees(sys.argv[2] if len(sys.argv)>2 else '../sprite/kaal.png')
r=lees(sys.argv[3] if len(sys.argv)>3 else '../sprite/gnometrotter_ice.png'); z=np.load(sys.argv[4] if len(sys.argv)>4 else 'zone_r2.npy'); o=lees(s)
print('| zone | anders t.o.v. kaal / zone | anders t.o.v. r1 |'); print('|---|---|---|')
for zz,n in ZNAAM.items():
    m=z==zz; print('| %s | %d / %d | %d |'%(n,((o!=k)&m).sum(),m.sum(),((o!=r)&m).sum()))
print('totaal t.o.v. kaal %d / %d, t.o.v. r1 %d; silhouet t.o.v. kaal %d, t.o.v. r1 %d'%((o!=k).sum(),(o>0).sum(),(o!=r).sum(),((o>0)!=(k>0)).sum(),((o>0)!=(r>0)).sum()))
