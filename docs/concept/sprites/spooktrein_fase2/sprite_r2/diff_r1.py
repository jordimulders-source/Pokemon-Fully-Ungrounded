# diff r2 t.o.v. r1 per zone
import numpy as np
a=np.load('../sprite_r1/post_B.npy'); b=np.load('post_r2.npy'); d=a!=b
Z={'gezicht (rij 7-20, x 24-48; bevroren)':(slice(7,21),slice(24,49)),'krul (rij 0-3, x 42-53)':(slice(0,4),slice(42,54)),
   'wielen (2x 6x6)':None,'ashout (rij 40-43, x 6-13)':(slice(40,44),slice(6,14))}
M={}
M['wielen (2x 6x6)']=np.zeros((64,64),bool); M['wielen (2x 6x6)'][39:45,0:6]=True; M['wielen (2x 6x6)'][39:45,14:20]=True
for k,v in Z.items():
    if v is not None: m=np.zeros((64,64),bool); m[v]=True; M[k]=m
used=np.zeros((64,64),bool)
for k in M: used|=M[k]
G=np.isin(b,[2,3,4,5])|np.isin(a,[2,3,4,5])
M['staart/wolk (groen, rij >=23)']=~used&G&(np.arange(64)[:,None]>=23)
M['geest overig (rij <23)']=~used&(np.arange(64)[:,None]<23)
used2=used|M['staart/wolk (groen, rij >=23)']|M['geest overig (rij <23)']
M['wagon']=~used2
tot=0
for k,m in M.items(): n=(d&m).sum(); tot+=n; print(f'{k}: {n}')
print('totaal',d.sum(),tot)
