# 6. volume achterlijf (Gen 3, alleen tinten; banden en vorm blijven): licht linksboven op de bolling,
# sikkel rechtsonder. Lichte banden (5/6) -> 6/5/4, donkere banden (3/2) -> 3/2, naar lichtrichting.
import numpy as np, pickle
f=np.loadtxt('r5_basis.txt',dtype=int); Z=pickle.load(open('zones.pkl','rb'))
CX,CY,RX,RY=43.5,37.5,9.5,9.5
n=0; vol=set()
for y in range(28,47):
    for x in range(35,53):
        v=f[y,x]
        if v not in (2,3,5,6): continue
        l=-0.45*(x-CX)/RX-0.9*(y-CY)/RY
        nv = (6 if l>0.5 else 5 if l>-0.3 else 4) if v in (5,6) else (3 if l>-0.4 else 2)
        if nv!=v: f[y,x]=nv; n+=1; vol.add((x,y))
Z['volume achterlijf']=vol
np.savetxt('r5_basis_vol.txt',f,fmt='%2d'); pickle.dump(Z,open('zones.pkl','wb')); print('volume: pixels gewijzigd',n)
