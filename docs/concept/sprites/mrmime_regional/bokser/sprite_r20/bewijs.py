# bewijs r20: elke afwijking t.o.v. r19 ligt in zone BAL of zone V; en de V-pixels t.o.v. r18
import numpy as np
r20=np.load('bokser.npy'); r19=np.load('../sprite_r19/bokser.npy'); r18=np.load('../sprite_r18/bokser.npy')
BAL=lambda x,y: 4<=x<=28 and 18<=y<=30
VZ =lambda x,y: 26<=x<=38 and 24<=y<=34
d=[(int(x),int(y)) for y,x in zip(*np.where(r20!=r19))]
buiten=[p for p in d if not(BAL(*p) or VZ(*p))]
print('diff r20-r19 totaal',len(d),'| bal',sum(BAL(*p) for p in d),'| V',sum(VZ(*p) and not BAL(*p) for p in d),'| BUITEN ZONES',len(buiten),buiten)
ruw=np.load('ruw.npy'); romp=np.isin(ruw,(7,8))     # V = donkergrijs (3) op romppixels
vb=lambda a:{(int(x),int(y)) for y,x in zip(*np.where((a==3)&romp)) if x>=26}
v18,v20=vb(r18),vb(r20)
print('V r18',len(v18),'px, r20',len(v20),'px; punt r18',max(v18,key=lambda p:p[1]),'r20',max(v20,key=lambda p:p[1]))
for y in range(25,34):
    f=lambda s:[x for x,yy in s if yy==y]
    print(y,'r18',min(f(v18)),'-',max(f(v18)),' r20',min(f(v20)),'-',max(f(v20)))
