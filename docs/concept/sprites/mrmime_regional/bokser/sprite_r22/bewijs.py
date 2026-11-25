# bewijs r22: elke variant verschilt van r20 alleen in de V-zone (x26-38, y24-34) en alleen op romppixels
import numpy as np, glob
B=np.load('r20_basis.npy'); R=np.load('ruw.npy')
for f in sorted(glob.glob('var/*.npy')):
    a=np.load(f); d=[(int(x),int(y)) for y,x in zip(*np.where(a!=B))]
    print(f, len(d),'px | buiten V-zone',sum(not(26<=x<=38 and 24<=y<=34) for x,y in d),'| niet-romp',sum(R[y,x] not in(7,8) for x,y in d))
