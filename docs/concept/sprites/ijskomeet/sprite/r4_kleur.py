# r4 stap 2: schotsen belichten (bovenvlak/naad linksboven licht, onderzijde donker), naden S.
from gio import from_txt, to_txt, CH
import numpy as np
exec(open('r4_lijf.py').read().split('# vlakken labelen')[0].split('for p in NADEN.values()')[0])
lab=np.load('r4_lab.npy'); seam=np.load('r4_seam.npy')
def reg(x,y): return lab[y,x]
R={'kop':reg(5,40),'P2':reg(24,41),'P3':reg(30,48),'P4':reg(4,48),'P5':reg(15,49),'F1':reg(9,55),'F2':reg(18,57),'F3':reg(27,56)}
inv={v:k for k,v in R.items()}
T={ # basis, bovenrand, schaduw
'kop':('L','L','M'),'P2':('W','W','M'),'P3':('L','W','D'),'P4':('L','W','M'),
'P5':('L','W','D'),'F1':('M','L','D'),'F2':('M','L','D'),'F3':('M','L','D')}
out=o.copy()
def isS(y,x): return seam[y,x]
for y in range(H):
    for x in range(W):
        if seam[y,x]: out[y,x]=C['S']; continue
        if lab[y,x]<0: continue
        k=inv.get(lab[y,x],'P3')
        base,bev,sh=T[k]
        if k=='P2' and y>=43: base='L'
        if k=='P3' and x>=30: base='M'
        if k=='P5' and (y-53)*(24.5-12) > -(x-12)*(53-49.5)*1.0 : base='M'   # onder de diagonaal (12,53)-(24.5,49.5)
        if k=='F2' and y>=58: base='D'
        down=seam[y+1,x] or (k[0]=='F' and fixed[y+1,x])
        right=seam[y,x+1] or (o[y,x+1]==C['K'] and k in('P3',))
        up=seam[y-1,x] ; left=seam[y,x-1] or (fixed[y,x-1] and k in ('kop','P4'))
        DK={'W':'L','L':'M','M':'D','D':'D'}
        if down or (right and k=='P3' and o[y,x+1]==C['K']): t=DK[base]
        elif up or left: t=bev
        else: t=base
        if k=='kop' and fixed[y,x-1]: t='W'
        out[y,x]=C[t]
to_txt(out,'r4_lijf.txt')
for y in range(38,61): print('%2d '%y+''.join('.' if v<0 else CH[v] for v in out[y,:36]))
print(R)
