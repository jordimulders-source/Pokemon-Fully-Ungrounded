# bewijs r21: elke variant verschilt van r20 alleen in de V-zone (x26-38, y24-34) en alleen op romppixels (7/8 <-> 3)
import numpy as np
r20=np.load('../sprite_r20/bokser.npy'); ruw=np.load('ruw.npy')
for n in ['bokser','var/v_B_banen','var/v_C_steil']:
    a=np.load(n+'.npy'); d=[(int(x),int(y)) for y,x in zip(*np.where(a!=r20))]
    buiten=[p for p in d if not(26<=p[0]<=38 and 24<=p[1]<=34)]
    nietromp=[p for p in d if ruw[p[1],p[0]] not in (7,8)]
    V={(int(x),int(y)) for y,x in zip(*np.where((a==3)&np.isin(ruw,(7,8)))) if x>=26}
    print(f'{n}: diff {len(d)} px, buiten V-zone {len(buiten)}, niet-romp {len(nietromp)}, V {len(V)} px, punt {max(V,key=lambda p:(p[1],-p[0]))}')
